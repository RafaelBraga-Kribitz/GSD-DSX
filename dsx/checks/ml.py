"""Machine-learning integrity checks. Codes DSX-ML-*.

Leakage is the defining failure mode of applied ML: it produces a model that
scores beautifully offline and collapses in production, and it is invisible to
every metric you would normally look at. These checks target it structurally —
from the split strategy, the preprocessing boundary and the feature roster —
rather than hoping someone notices an implausible AUC.
"""

from __future__ import annotations

import re

from ..findings import Report
from ..spec import (
    IMBALANCE_UNSAFE_METRICS,
    as_number,
    get,
    is_blank,
    normalize,
    section,
)

# Feature-name patterns that are almost always recorded at or after the outcome.
# Each entry: (compiled pattern, why it leaks).
LEAKAGE_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(^|_)(cancel|cancelled|canceled|churn|churned)(_|$)"),
     "recorded when the outcome occurs"),
    (re.compile(r"(^|_)(refund|chargeback|reversal)(_|$)"),
     "downstream of the outcome"),
    (re.compile(r"(^|_)(closed|close|resolution|resolved|settled)_?(at|date|time|reason)?(_|$)"),
     "timestamp of the event being predicted"),
    (re.compile(r"(^|_)(final|total|lifetime|ltv|cumulative)(_|$)"),
     "aggregates the full horizon, including the future"),
    (re.compile(r"_after_|_post_|(^|_)(post|after)(_|$)"),
     "explicitly measured after the prediction point"),
    (re.compile(r"(^|_)(outcome|label|target|y_true|ground_truth)(_|$)"),
     "the target itself or a copy of it"),
    (re.compile(r"(^|_)(days?|months?|weeks?)_(to|until)_(churn|cancel|default|conversion|event)"),
     "derived from the outcome date"),
    (re.compile(r"(^|_)next_(month|week|day|period)(_|$)"),
     "sourced from a future period"),
    (re.compile(r"(^|_)(score|probability|pred|prediction)(_|$)"),
     "output of another model that may itself have seen the target"),
    (re.compile(r"(^|_)(reason|cause)_(code|desc|description)(_|$)"),
     "populated only once the outcome is known"),
]

IMBALANCE_THRESHOLD = 0.20
OVERFIT_GAP_THRESHOLD = 0.10
DECISION_TASKS = {"binary_classification", "multiclass_classification"}


def check(spec: dict) -> Report:
    report = Report(check="ml")
    model = section(spec, "model")
    qtype = normalize(spec.get("question_type", ""))

    if not model:
        if qtype == "predictive":
            report.add(
                "DSX-ML-001",
                "CRITICAL",
                "question_type is 'predictive' but no model block is declared",
                detail="Predictive work needs a declared task, target, split and baseline.",
                remedy="Add a model: block. See templates/ANALYSIS-SPEC.yaml.",
                where="spec.model",
            )
        return report

    task = normalize(model.get("task", ""))
    _check_split(model, report, task)
    _check_preprocessing(model, report)
    _check_features(model, report)
    _check_metric_choice(model, spec, report, task)
    _check_baseline(model, spec, report)
    _check_overfit(spec, report)
    _check_test_set_hygiene(model, spec, report)
    _check_calibration(model, spec, report, task)
    return report


# ── Splits ───────────────────────────────────────────────────────────────────


def _check_split(model: dict, report: Report, task: str) -> None:
    split = normalize(model.get("split", ""))
    time_column = model.get("time_column")
    entity_column = model.get("entity_column")

    if not split:
        report.add(
            "DSX-ML-010", "CRITICAL", "model.split is not declared",
            detail="The split strategy determines whether the test score means anything.",
            remedy="Declare one of: random, stratified, temporal, grouped, grouped_temporal, nested_cv.",
            where="spec.model.split",
        )
        return

    temporal_required = bool(time_column) or task == "forecasting"
    if temporal_required and split not in ("temporal", "grouped_temporal", "nested_cv"):
        report.add(
            "DSX-ML-011",
            "CRITICAL",
            f"Temporal data split with '{split}' instead of a time-ordered split",
            detail=(
                f"time_column={time_column!r} means rows are ordered in time. A random split "
                "puts future rows in training, so the model learns from information that will "
                "not exist at prediction time. Test scores from this setup are fiction."
            ),
            remedy=(
                "Set model.split to temporal (or grouped_temporal when entities repeat) and "
                "declare train_period and test_period as disjoint, ordered windows."
            ),
            where="spec.model.split",
        )
    elif temporal_required:
        report.ok(f"temporal data uses '{split}' split")

    if entity_column and split not in ("grouped", "grouped_temporal", "nested_cv"):
        report.add(
            "DSX-ML-012",
            "HIGH",
            f"Repeated entities ('{entity_column}') split with '{split}'",
            detail=(
                "The same entity appearing in both train and test lets the model memorise the "
                "entity rather than learn the pattern. Test performance is then an upper bound "
                "that will not hold for new entities."
            ),
            remedy=f"Use a grouped split keyed on '{entity_column}'.",
            where="spec.model.split",
        )
    elif entity_column:
        report.ok(f"grouped split on '{entity_column}'")

    if split == "temporal":
        train_period = model.get("train_period")
        test_period = model.get("test_period")
        if is_blank(train_period) or is_blank(test_period):
            report.add(
                "DSX-ML-013", "HIGH", "Temporal split without declared train/test periods",
                detail="Undeclared windows cannot be checked for overlap.",
                remedy="Declare model.train_period and model.test_period as start..end ranges.",
                where="spec.model",
            )
        elif _periods_overlap(str(train_period), str(test_period)):
            report.add(
                "DSX-ML-014",
                "CRITICAL",
                "Train and test periods overlap",
                detail=f"train_period={train_period!r} overlaps test_period={test_period!r}.",
                remedy="Make the windows disjoint, with test strictly after train.",
                where="spec.model.test_period",
            )
        else:
            report.ok("train and test periods are disjoint")

    if task == "forecasting" and is_blank(model.get("horizon")):
        report.add(
            "DSX-ML-015", "HIGH", "Forecasting task with no declared horizon",
            detail="Accuracy is meaningless without the horizon it was measured at.",
            remedy="Declare model.horizon and evaluate with rolling-origin backtests.",
            where="spec.model.horizon",
        )


def _periods_overlap(a: str, b: str) -> bool:
    """Compare two ``start..end`` ranges lexically. ISO dates sort correctly as strings."""
    a_parts = [p.strip() for p in a.split("..")]
    b_parts = [p.strip() for p in b.split("..")]
    if len(a_parts) != 2 or len(b_parts) != 2:
        return False
    a_start, a_end = a_parts
    b_start, b_end = b_parts
    if not all(re.match(r"^\d{4}-\d{2}(-\d{2})?", p) for p in (a_start, a_end, b_start, b_end)):
        return False
    return a_start <= b_end and b_start <= a_end


# ── Preprocessing boundary ───────────────────────────────────────────────────


def _check_preprocessing(model: dict, report: Report) -> None:
    fit_on = normalize(model.get("preprocessing_fit_on", ""))
    if not fit_on:
        report.add(
            "DSX-ML-020",
            "HIGH",
            "model.preprocessing_fit_on is not declared",
            detail=(
                "Scalers, imputers, encoders and feature selectors fitted on the full dataset "
                "leak test-set statistics into training. This is the most common leakage bug "
                "and it never shows up as an error."
            ),
            remedy="Declare preprocessing_fit_on: train_only and fit inside a pipeline per fold.",
            where="spec.model.preprocessing_fit_on",
        )
    elif fit_on not in ("train_only", "train_fold_only", "none"):
        report.add(
            "DSX-ML-021",
            "CRITICAL",
            f"Preprocessing fitted on '{fit_on}' rather than training data only",
            detail=(
                "Any statistic computed across train and test — a mean, a category vocabulary, "
                "a selected feature set — carries test information into the model."
            ),
            remedy="Refit every transform inside the training fold. Use a pipeline object.",
            where="spec.model.preprocessing_fit_on",
        )
    else:
        report.ok(f"preprocessing fitted on {fit_on}")

    if normalize(model.get("resampling_applied_to", "")) in ("all", "full", "before_split"):
        report.add(
            "DSX-ML-022",
            "CRITICAL",
            "Class resampling applied before the train/test split",
            detail=(
                "SMOTE or oversampling before splitting copies rows across the boundary, so "
                "near-duplicates of test rows appear in training. Test scores become meaningless."
            ),
            remedy="Resample inside the training fold only, never before the split.",
            where="spec.model.resampling_applied_to",
        )


# ── Features ─────────────────────────────────────────────────────────────────


def _check_features(model: dict, report: Report) -> None:
    features = model.get("features")
    target = normalize(model.get("target", ""))
    if not isinstance(features, list) or not features:
        report.add(
            "DSX-ML-030",
            "MEDIUM",
            "model.features is not declared",
            detail="Without the feature roster, automated leakage screening cannot run.",
            remedy="List the features used, or point at the file that defines them.",
            where="spec.model.features",
        )
        return

    names = [normalize(f) for f in features if isinstance(f, str)]
    excluded = {normalize(f) for f in (model.get("features_excluded_for_leakage") or [])}

    if target and target in names:
        report.add(
            "DSX-ML-031",
            "CRITICAL",
            f"Target '{model.get('target')}' appears in the feature list",
            remedy="Remove the target from features.",
            where="spec.model.features",
        )

    suspects: list[dict[str, str]] = []
    for name in names:
        if name in excluded:
            continue
        for pattern, reason in LEAKAGE_PATTERNS:
            if pattern.search(name):
                suspects.append({"feature": name, "reason": reason})
                break

    if suspects:
        listing = "; ".join(f"{s['feature']} ({s['reason']})" for s in suspects[:12])
        report.add(
            "DSX-ML-032",
            "HIGH",
            f"{len(suspects)} feature(s) match known leakage patterns",
            detail=(
                f"{listing}. Each is typically populated at or after the moment the outcome "
                "becomes known, so it would not be available at prediction time."
            ),
            remedy=(
                "For each: confirm the value exists at the prediction timestamp. If it does, "
                "add it to model.features_excluded_for_leakage with a one-line justification "
                "to acknowledge the check. If it does not, drop the feature and retrain."
            ),
            where="spec.model.features",
            suspects=suspects,
        )
    else:
        report.ok(f"{len(names)} features screened, no leakage patterns matched")

    if is_blank(model.get("prediction_time_definition")):
        report.add(
            "DSX-ML-033",
            "MEDIUM",
            "model.prediction_time_definition is not declared",
            detail=(
                "Leakage is defined relative to a moment. Without stating when the model runs "
                "in production, 'available at prediction time' cannot be assessed."
            ),
            remedy="State the production trigger, e.g. 'nightly at 02:00 for active accounts'.",
            where="spec.model.prediction_time_definition",
        )


# ── Metric choice ────────────────────────────────────────────────────────────


def _check_metric_choice(model: dict, spec: dict, report: Report, task: str) -> None:
    primary = normalize(model.get("primary_metric", ""))
    if not primary:
        report.add(
            "DSX-ML-040", "HIGH", "model.primary_metric is not declared",
            detail="Without one primary metric, model selection drifts to whichever number looks best.",
            remedy="Name one primary metric before training. Everything else is secondary.",
            where="spec.model.primary_metric",
        )
        return

    positive_rate = as_number(model.get("positive_rate"))
    if positive_rate is None:
        positive_rate = as_number(get(spec, "results.positive_rate"))

    if task in DECISION_TASKS and positive_rate is not None:
        minority = min(positive_rate, 1.0 - positive_rate)
        if minority < IMBALANCE_THRESHOLD and primary in IMBALANCE_UNSAFE_METRICS:
            report.add(
                "DSX-ML-041",
                "HIGH",
                f"'{primary}' is the primary metric on data with a {minority:.1%} minority class",
                detail=(
                    f"At a {minority:.1%} positive rate, a model predicting the majority class "
                    f"for every row scores {1 - minority:.1%} accuracy. ROC-AUC is similarly "
                    "optimistic because the large true-negative pool suppresses the false "
                    "positive rate."
                ),
                remedy=f"Switch the primary metric to {IMBALANCE_UNSAFE_METRICS[primary]}.",
                where="spec.model.primary_metric",
                minority_rate=round(minority, 4),
            )
        else:
            report.ok(f"primary metric '{primary}' suits a {minority:.1%} minority class")

    if task == "regression" and primary in ("r2", "r_squared") and is_blank(
        model.get("secondary_metrics")
    ):
        report.add(
            "DSX-ML-042",
            "MEDIUM",
            "R² is the only regression metric declared",
            detail=(
                "R² is scale-free and hides absolute error. A model can post a strong R² while "
                "being useless at the magnitudes the decision depends on."
            ),
            remedy="Add an error metric in the target's own units — MAE, RMSE or MAPE.",
            where="spec.model.primary_metric",
        )


# ── Baseline and overfitting ─────────────────────────────────────────────────


def _check_baseline(model: dict, spec: dict, report: Report) -> None:
    baseline = model.get("baseline")
    if is_blank(baseline):
        report.add(
            "DSX-ML-050",
            "HIGH",
            "model.baseline is not declared",
            detail=(
                "A score without a baseline is uninterpretable. Many production models never "
                "beat 'predict the majority class' or 'repeat last period's value'."
            ),
            remedy=(
                "Declare a trivial baseline — majority_class, last_value, seasonal_naive or "
                "the current rules engine — and report both scores."
            ),
            where="spec.model.baseline",
        )
        return

    model_score = as_number(get(spec, "results.model_score"))
    baseline_score = as_number(get(spec, "results.baseline_score"))
    if model_score is None or baseline_score is None:
        report.ok(f"baseline declared ({baseline}); scores not yet reported")
        return

    if model_score <= baseline_score:
        report.add(
            "DSX-ML-051",
            "CRITICAL",
            f"Model does not beat its baseline ({model_score:.4g} vs {baseline_score:.4g})",
            detail=f"Baseline is '{baseline}'. The model adds cost and risk with no measured gain.",
            remedy="Ship the baseline, or state explicitly why the model is worth its complexity.",
            where="spec.results.model_score",
        )
    else:
        lift = (model_score - baseline_score) / abs(baseline_score) if baseline_score else float("inf")
        report.ok(f"model beats baseline by {lift:.1%}")


def _check_overfit(spec: dict, report: Report) -> None:
    train = as_number(get(spec, "results.train_score"))
    test = as_number(get(spec, "results.test_score"))
    if train is None or test is None:
        return
    gap = train - test
    if gap > OVERFIT_GAP_THRESHOLD:
        report.add(
            "DSX-ML-060",
            "HIGH",
            f"Train/test gap of {gap:.3f} indicates overfitting",
            detail=(
                f"train={train:.4g}, test={test:.4g}. A gap above {OVERFIT_GAP_THRESHOLD} means "
                "the reported test score is unlikely to survive contact with new data."
            ),
            remedy="Regularise, reduce capacity, or gather more data. Re-evaluate on a held-out set.",
            where="spec.results",
            gap=round(gap, 4),
        )
    elif gap < -OVERFIT_GAP_THRESHOLD:
        report.add(
            "DSX-ML-061",
            "HIGH",
            f"Test score exceeds train score by {abs(gap):.3f}",
            detail=(
                "Test outperforming train by a wide margin usually signals leakage into the "
                "test split, a distribution mismatch, or an evaluation bug — not a good model."
            ),
            remedy="Audit the split and the evaluation code before trusting either number.",
            where="spec.results",
        )
    else:
        report.ok(f"train/test gap {gap:.3f} within tolerance")


def _check_test_set_hygiene(model: dict, spec: dict, report: Report) -> None:
    evaluations = as_number(get(spec, "results.test_set_evaluations"))
    if evaluations is not None and evaluations > 1:
        report.add(
            "DSX-ML-070",
            "HIGH",
            f"Test set evaluated {int(evaluations)} times during development",
            detail=(
                "Every look at the test set that informs a modelling choice turns it into a "
                "validation set. The final score is then optimistically biased by an unknown "
                "amount."
            ),
            remedy=(
                "Use a separate validation split for all model selection, and touch the test "
                "set exactly once. If it has already been reused, hold out a fresh set."
            ),
            where="spec.results.test_set_evaluations",
        )

    overlap = as_number(get(spec, "results.train_test_overlap_rows"))
    if overlap is not None and overlap > 0:
        report.add(
            "DSX-ML-071",
            "CRITICAL",
            f"{int(overlap)} rows appear in both train and test",
            detail="Duplicate or near-duplicate rows across the split inflate the test score directly.",
            remedy="Deduplicate before splitting, then re-split and retrain.",
            where="spec.results.train_test_overlap_rows",
        )
    elif overlap == 0:
        report.ok("no train/test row overlap")

    if normalize(model.get("threshold_selected_on", "")) in ("test", "test_set", "holdout"):
        report.add(
            "DSX-ML-072",
            "CRITICAL",
            "Decision threshold tuned on the test set",
            detail="Choosing the operating point on test makes the reported precision/recall optimistic.",
            remedy="Select the threshold on validation data; report test metrics at that fixed threshold.",
            where="spec.model.threshold_selected_on",
        )


def _check_calibration(model: dict, spec: dict, report: Report, task: str) -> None:
    if task not in DECISION_TASKS:
        return
    uses_probabilities = bool(model.get("uses_predicted_probabilities")) or not is_blank(
        model.get("threshold")
    )
    if not uses_probabilities:
        return
    if is_blank(model.get("calibration_method")) and is_blank(
        get(spec, "results.calibration_error")
    ):
        report.add(
            "DSX-ML-080",
            "MEDIUM",
            "Predicted probabilities are used for decisions without a calibration check",
            detail=(
                "Tree ensembles and margin-based models produce ranked scores, not calibrated "
                "probabilities. A '70% risk' bucket may contain 40% or 90% actual events, which "
                "breaks any expected-value calculation built on top."
            ),
            remedy=(
                "Report a reliability curve and expected calibration error, and apply Platt "
                "scaling or isotonic regression if the model is miscalibrated."
            ),
            where="spec.model.calibration_method",
        )
    else:
        report.ok("calibration addressed")
