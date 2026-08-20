"""Machine-learning integrity checks. Codes DSX-ML-*.

Leakage is the defining failure mode of applied ML: it produces a model that
scores beautifully offline and collapses in production, and it is invisible to
every metric you would normally look at. These checks target it structurally —
from the split strategy, the preprocessing boundary and the feature roster —
rather than hoping someone notices an implausible AUC.
"""

from __future__ import annotations

import re

from ..decisions import DecisionRecord, record_decision
from ..findings import Report
from ..spec import (
    IMBALANCE_UNSAFE_METRICS,
    as_number,
    get,
    is_blank,
    items,
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

# Phase 11.1 (REQ-P11.1-03): the three values `_check_preprocessing` already
# accepted for the whole-pipeline `preprocessing_fit_on` field, lifted into a
# shared constant so `_check_cleaning`'s per-step boundary test and
# `_check_preprocessing`'s whole-pipeline test can never drift apart on what
# counts as "training rows only".
TRAIN_ONLY_FIT_VALUES = frozenset({"train_only", "train_fold_only", "none"})


def check(spec: dict) -> Report:
    report = Report(check="ml")
    model = section(spec, "model")
    qtype = normalize(spec.get("question_type", ""))

    # Phase 11.1 (REQ-P11.1-03): runs ahead of the no-model early return
    # below, because a data-only specification that declares a leaky
    # cleaning step is still leaky — the defect lives in the data
    # declaration, not in whether a model section happens to exist.
    _check_cleaning(spec, report)

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
    _check_prediction_time_definition(model, report)
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
    elif fit_on not in TRAIN_ONLY_FIT_VALUES:
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


def _check_cleaning(spec: dict, report: Report) -> None:
    """`data[].cleaning[]` per-step fit-boundary check (DSX-ML-023, DSX-ML-024).

    Phase 11.1 (REQ-P11.1-03): `_check_preprocessing` above states one fit
    boundary for the whole pipeline. The reproduction this requirement
    responds to declared that whole-pipeline boundary honestly — training
    rows only — and then imputed a column's missing values over the full
    frame during a cleaning stage that boundary was never understood to
    cover. Until the contract could carry a per-step boundary, an operator
    who wanted to declare the truth had no field to declare it in. This
    check reads that new, optional `data[].cleaning[].fit_on` declaration
    and applies the same accepted-value test `_check_preprocessing` applies
    to the whole-pipeline field, via the one constant both consult
    (`TRAIN_ONLY_FIT_VALUES`).

    Called from `check()`'s dispatch ahead of the no-model early return, so
    a data-only specification that declares a leaky cleaning step still
    blocks.

    A cleaning step with a blank or absent `fit_on` is skipped, not
    flagged: an incomplete declaration is treated exactly as no
    declaration, because punishing a partial declaration harder than none
    would push operators back to declaring nothing at all — the opposite of
    what this field exists to encourage.

    Citation: Kaufman, S., Rosset, S., Perlich, C. and Stitelman, O.
    (2012), "Leakage in Data Mining: Formulation, Detection, and
    Avoidance," ACM Transactions on Knowledge Discovery from Data, 6(4),
    article 15. The paper's formulation of attribute "legitimacy" — a
    feature value is legitimate only if it would genuinely have been
    available, for the entity in question, at the moment the target
    becomes known — is the general statement of the boundary both this
    check and `_check_preprocessing` enforce for a specific class of
    statistic-fitting operation (an imputation value or an outlier
    threshold fitted across rows outside that boundary). The exact
    section/page locator within the paper for the legitimacy formulation is
    UNVERIFIED — the ACM Digital Library PDF was not independently
    paginated in this session; do not invent a locator.

    Structural criterion: DSX-ML-023 is a membership test of a declared,
    non-blank `fit_on` value against `TRAIN_ONLY_FIT_VALUES` after
    normalisation — the same constant and the same test
    `_check_preprocessing` applies to the whole-pipeline field, so the two
    can never disagree about what counts as training rows only.
    DSX-ML-024 is a second, additional test on the same data: whether the
    model section's own `preprocessing_fit_on` normalises to a member of
    that same constant while at least one cleaning step's boundary does
    not — two declarations compared for agreement, not a third boundary
    value being introduced. DSX-ML-024 is emitted at most once per report.
    """
    datasets = items(spec, "data")
    if not datasets:
        return

    any_cleaning_declared = False
    leaky_steps: list[dict[str, str]] = []

    for d_index, dataset in enumerate(datasets):
        cleaning = dataset.get("cleaning")
        if not isinstance(cleaning, list):
            continue
        dataset_name = dataset.get("name", d_index)
        for c_index, step in enumerate(cleaning):
            if not isinstance(step, dict):
                continue
            any_cleaning_declared = True
            fit_on = step.get("fit_on")
            # Phase 11.1: an incomplete declaration (blank or absent fit_on)
            # is treated exactly as no declaration — see the docstring above
            # for why. This is not the CRITICAL branch below; it is a skip.
            if is_blank(fit_on):
                continue
            if normalize(fit_on) in TRAIN_ONLY_FIT_VALUES:
                continue

            column = step.get("column", "<unnamed column>")
            method = step.get("method")
            where = f"spec.data[{d_index}].cleaning[{c_index}].fit_on"
            leaky_steps.append({"dataset": str(dataset_name), "column": str(column)})
            report.add(
                "DSX-ML-023",
                "CRITICAL",
                f"Cleaning statistic for '{column}' was fitted outside the training rows",
                detail=(
                    f"Dataset {dataset_name!r}, column {column!r}"
                    + (f", method {method!r}" if method else "")
                    + f", declares fit_on: {fit_on!r}. An imputation value or an outlier "
                    "threshold computed across the whole frame carries held-out information "
                    "into training, whether or not the model's own preprocessing was fitted "
                    "correctly."
                ),
                remedy=(
                    "Compute the statistic on the training rows and apply it to the held-out "
                    "rows, then declare fit_on accordingly."
                ),
                where=where,
                dataset=str(dataset_name),
                column=str(column),
            )

    if not any_cleaning_declared:
        return

    whole_pipeline_fit_on = normalize(get(spec, "model.preprocessing_fit_on", ""))
    fired_024 = bool(leaky_steps) and whole_pipeline_fit_on in TRAIN_ONLY_FIT_VALUES
    if fired_024:
        steps_listing = "; ".join(f"{s['dataset']}.{s['column']}" for s in leaky_steps)
        report.add(
            "DSX-ML-024",
            "HIGH",
            "Cleaning declaration contradicts the declared whole-pipeline boundary",
            detail=(
                f"model.preprocessing_fit_on declares {whole_pipeline_fit_on!r} (training rows "
                f"only), but the following cleaning step(s) declare a boundary outside "
                f"training rows: {steps_listing}."
            ),
            remedy=(
                "Make the two declarations agree. If the cleaning declaration accurately "
                "describes what the pipeline does, the pipeline is what needs changing, not "
                "the declaration."
            ),
            where="spec.data[].cleaning[].fit_on",
        )

    # Phase 11.1 (D-04): a decision record covering both codes, appended once
    # per report whenever any cleaning step is declared at all — a "cleared"
    # or "no contradiction to compare against" judgment is still a judgment,
    # mirroring `_check_metric_choice`'s precedent (plan 11.1-04).
    record_decision(
        report,
        DecisionRecord(
            id="",
            invocation_id="",
            layer="deterministic",
            choice=(
                "DSX-ML-023 and DSX-ML-024 fired"
                if fired_024
                else f"DSX-ML-023 fired ({len(leaky_steps)} step(s)); no whole-pipeline "
                "boundary of training rows only to contradict"
                if leaky_steps
                else "cleared: every declared, non-blank cleaning boundary is within "
                "TRAIN_ONLY_FIT_VALUES"
            ),
            inputs=[
                f"model.preprocessing_fit_on:{whole_pipeline_fit_on or 'undeclared'}",
                f"cleaning_steps_outside_boundary:{len(leaky_steps)}",
            ],
            rule=(
                "DSX-ML-023 fires when a declared, non-blank data[].cleaning[].fit_on "
                "normalises to a value outside TRAIN_ONLY_FIT_VALUES. DSX-ML-024 "
                "additionally fires, once per report, when model.preprocessing_fit_on "
                "normalises to a member of TRAIN_ONLY_FIT_VALUES while any cleaning "
                "step's declared boundary does not."
            ),
            citation=(
                "Kaufman, S., Rosset, S., Perlich, C. and Stitelman, O. (2012), \"Leakage "
                "in Data Mining: Formulation, Detection, and Avoidance,\" ACM Transactions "
                "on Knowledge Discovery from Data, 6(4), article 15."
            ),
            counterfactual=(
                "A cleaning boundary declared inside TRAIN_ONLY_FIT_VALUES for every step "
                "would have cleared both codes."
            ),
        ),
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


def _check_prediction_time_definition(model: dict, report: Report) -> None:
    """`model.prediction_time_definition` presence check (DSX-ML-033).

    Phase 11.1 (REQ-P11.1-04): extracted from `_check_features` into its own
    call site so it runs whenever a model is declared at all, independent of
    whether `model.features` is populated. `_check_features` returns early on
    a blank features list, which used to hide this check entirely for a
    specification that never got as far as listing features — the check
    itself needs no feature list to be meaningful, since it evaluates a
    stated production trigger, not a derived property of `features`. Code
    number, severity, title, detail, remedy and location string are
    unchanged from the block this replaces.
    """
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
    """Primary-metric declaration and its fitness for the declared class balance.

    Phase 11.1 (REQ-P11.1-04) adds DSX-ML-043: a decision task (binary or
    multiclass classification) whose primary metric is a member of
    IMBALANCE_UNSAFE_METRICS, and whose positive rate is undeclared on both
    the model section and the results section, produces a HIGH finding
    instead of silence. A positive rate the numeric accessor (`as_number`)
    cannot parse — a non-numeric string, or a boolean — arrives at this
    branch as an absence, which is the correct reading: a rate nobody can
    evaluate is not a declared rate. Do not "fix" this by adding a separate
    branch for the unparseable case; it is intentionally folded into the
    same undeclared branch as the absent case.

    Citation: Saito, T. and Rehmsmeier, M. (2015), "The Precision-Recall
    Plot Is More Informative than the ROC Plot When Evaluating Binary
    Classifiers on Imbalanced Datasets," PLOS ONE, 10(3), e0118432, DOI
    10.1371/journal.pone.0118432. The finding that ROC-AUC overstates
    apparent classifier quality as the positive class becomes rarer is
    stated in the paper's own Abstract. The exact figure/table locator for
    the specific numeric illustration is UNVERIFIED — the paper's figures
    were not independently re-read pixel-by-pixel in this session (the paper
    is open access at the DOI above); do not invent a locator.

    Structural criterion: DSX-ML-043 fires on the joint absence of a
    parseable positive rate (read from model.positive_rate, falling back to
    results.positive_rate, both via as_number — which returns None for a
    boolean and for any string it cannot parse as a number) and membership
    of the primary metric in IMBALANCE_UNSAFE_METRICS, for a decision task
    only. This is a presence-and-membership test, not a numeric threshold
    test — the numeric threshold test (against IMBALANCE_THRESHOLD) belongs
    to the sibling DSX-ML-041 branch, which this task does not retune.
    """
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

    imbalance_applicable = task in DECISION_TASKS and primary in IMBALANCE_UNSAFE_METRICS
    fired_041 = False
    fired_043 = False

    if task in DECISION_TASKS and positive_rate is not None:
        minority = min(positive_rate, 1.0 - positive_rate)
        if minority < IMBALANCE_THRESHOLD and primary in IMBALANCE_UNSAFE_METRICS:
            fired_041 = True
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
    elif task in DECISION_TASKS and positive_rate is None and primary in IMBALANCE_UNSAFE_METRICS:
        # Phase 11.1 (REQ-P11.1-04): the sibling of DSX-ML-041's declared-and-
        # risky branch — this is the undeclared-or-unparseable branch. See
        # this function's own docstring for why an unparseable string is
        # treated identically to an absent field, not as a third case.
        fired_043 = True
        report.add(
            "DSX-ML-043",
            "HIGH",
            f"'{primary}' is imbalance-unsafe and the class balance it depends on is undeclared",
            detail=(
                f"'{primary}''s reliability as a metric is a function of the positive rate — "
                "how rare the minority class is. Without a declared rate on either the model "
                "section or the results section, this check cannot evaluate that reliability, "
                "and silence here would read as a pass when it is really an absence of the "
                "information the check needs to judge it at all."
            ),
            remedy=(
                "Declare model.positive_rate or results.positive_rate, or switch the primary "
                f"metric to {IMBALANCE_UNSAFE_METRICS[primary]}."
            ),
            where="spec.model.primary_metric",
        )

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

    # Phase 11.1 (D-04): the first decision record dsx/checks/ml.py has ever
    # emitted, covering the metric-choice imbalance judgment — appended once
    # a primary metric is declared (the point above where this function would
    # otherwise have returned), whether or not the imbalance branches were
    # even reachable for this task/metric combination. A judgment that the
    # imbalance question does not apply here is still a judgment.
    if imbalance_applicable:
        choice = (
            "DSX-ML-041 fired: declared positive rate's minority share is below "
            "IMBALANCE_THRESHOLD" if fired_041
            else "DSX-ML-043 fired: positive rate is undeclared or unparseable" if fired_043
            else "cleared: declared positive rate is not imbalance-risky"
        )
    else:
        choice = (
            "not applicable: task is not a decision task, or primary metric is "
            "not a member of IMBALANCE_UNSAFE_METRICS"
        )
    record_decision(
        report,
        DecisionRecord(
            id="",
            invocation_id="",
            layer="deterministic",
            choice=choice,
            inputs=[
                f"primary_metric:{primary}",
                f"task:{task}",
                f"positive_rate:{'undeclared' if positive_rate is None else positive_rate}",
            ],
            rule=(
                "DSX-ML-041 fires when a declared, parseable positive rate's minority share "
                "is strictly less than IMBALANCE_THRESHOLD and the primary metric is a member "
                "of IMBALANCE_UNSAFE_METRICS, for a decision task. DSX-ML-043 fires when the "
                "positive rate is undeclared or unparseable and the primary metric is a "
                "member of IMBALANCE_UNSAFE_METRICS, for the same task set."
            ),
            citation=(
                "Saito, T. and Rehmsmeier, M. (2015), \"The Precision-Recall Plot Is More "
                "Informative than the ROC Plot When Evaluating Binary Classifiers on "
                "Imbalanced Datasets,\" PLOS ONE, 10(3), e0118432."
            ),
            counterfactual=(
                "A declared, parseable positive rate would have sent the check to the "
                "evaluated branch (DSX-ML-041 fired, or cleared) instead of DSX-ML-043."
            ),
        ),
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
