"""`model.metric_direction` — the declared orientation of a reported score.

Before this module existed, `_check_baseline` and `_check_overfit` compared
`results.model_score`/`baseline_score` and `train_score`/`test_score` with raw
numeric comparisons that assumed a larger number is always better. That
assumption holds for accuracy, ROC-AUC and F1; it is exactly inverted for the
error metrics conventional in `regression` and `forecasting` work (root mean
squared error, mean absolute error, mean absolute percentage error, log loss),
both of which are members of `spec.ML_TASKS`.

The observable defect, measured against the shipped v2.4.0 tree: a regression
model reporting RMSE 5.0 against a baseline RMSE of 10.0 — half the error, an
unambiguous improvement — fired DSX-ML-051 CRITICAL "Model does not beat its
baseline", while the same model reporting RMSE 20.0 (twice the error, plainly
worse) passed silently. The overfitting pair inverted the same way: an ordinary
overfit signature on an error metric (train error far below test error) was
reported as DSX-ML-061 "test exceeds train ... usually signals leakage", and a
genuinely suspicious result was reported as ordinary overfitting.

`metric_direction` is a declaration, never an inference: the gate does not read
the metric's *name* and guess its orientation, because a name-based lookup is
the two-stage "inspect, then decide" pattern D-01/D-02 prohibit. An absent
field means `higher_is_better`, which is the pre-existing behaviour, so no
already-passing specification changes its verdict.

Known limitation, deliberate and recorded: a value that is present but outside
`METRIC_DIRECTIONS` (a misspelling such as `lower_is_beter`) falls back to
`higher_is_better` rather than firing a vocabulary finding. Catching it would
need a new `DSX-SPEC-*` code, since every sibling `model.*` field owns its own
"is not recognised" code (DSX-SPEC-050 for task, -051 for split) and the model
block has no generic one. Minting a code is irreversible under D-06 and is a
deliberate numbering decision, so it is not folded into this patch. The
fallback leaves a misdeclared spec exactly where it was before this change —
no new hazard, and no way to bypass a check by misspelling the field.
"""

import unittest

from dsx.checks import ml


def codes(report) -> "list[str]":
    return [f.code for f in report.findings]


def _spec(model_score, baseline_score, direction=None, task="regression",
          primary_metric="rmse"):
    model = {
        "task": task,
        "target": "revenue",
        "split": "temporal",
        "primary_metric": primary_metric,
        "baseline": "seasonal_naive",
    }
    if direction is not None:
        model["metric_direction"] = direction
    return {
        "question_type": "predictive",
        "model": model,
        "results": {
            "model_score": model_score,
            "baseline_score": baseline_score,
            "model_score_source": "holdout",
        },
    }


def _overfit_spec(train, test, direction=None):
    model = {
        "task": "regression",
        "target": "revenue",
        "split": "temporal",
        "primary_metric": "rmse",
        "baseline": "seasonal_naive",
    }
    if direction is not None:
        model["metric_direction"] = direction
    return {
        "question_type": "predictive",
        "model": model,
        "results": {"train_score": train, "test_score": test},
    }


class TestMetricDirectionVocabulary(unittest.TestCase):
    def test_metric_directions_vocabulary_is_locked(self):
        self.assertEqual(
            ml.METRIC_DIRECTIONS,
            frozenset({"higher_is_better", "lower_is_better"}),
        )


class TestBaselineUnderLowerIsBetter(unittest.TestCase):
    """DSX-ML-051 under a declared lower-is-better metric."""

    def test_halved_error_does_not_fire_051(self):
        # D-05: DSX-ML-051
        # RMSE 5.0 vs baseline 10.0 — half the error, an unambiguous improvement.
        spec = _spec(5.0, 10.0, direction="lower_is_better")
        self.assertNotIn("DSX-ML-051", codes(ml.check(spec)))

    def test_doubled_error_fires_051(self):
        # D-05: DSX-ML-051
        # RMSE 20.0 vs baseline 10.0 — twice the error, plainly worse.
        spec = _spec(20.0, 10.0, direction="lower_is_better")
        self.assertIn("DSX-ML-051", codes(ml.check(spec)))

    def test_equal_scores_fire_051_in_both_directions(self):
        # A tie beats nothing, whichever way the metric points.
        lower = _spec(10.0, 10.0, direction="lower_is_better")
        higher = _spec(0.7, 0.7, direction="higher_is_better")
        self.assertIn("DSX-ML-051", codes(ml.check(lower)))
        self.assertIn("DSX-ML-051", codes(ml.check(higher)))


class TestBaselineUnderHigherIsBetterUnchanged(unittest.TestCase):
    """The pre-existing behaviour must be byte-for-byte preserved."""

    def test_absent_direction_keeps_higher_is_better_pass(self):
        spec = _spec(0.72, 0.70, direction=None, task="binary_classification",
                     primary_metric="pr_auc")
        self.assertNotIn("DSX-ML-051", codes(ml.check(spec)))

    def test_absent_direction_keeps_higher_is_better_fail(self):
        spec = _spec(0.68, 0.70, direction=None, task="binary_classification",
                     primary_metric="pr_auc")
        self.assertIn("DSX-ML-051", codes(ml.check(spec)))

    def test_explicit_higher_is_better_matches_absent(self):
        absent = _spec(0.68, 0.70, direction=None, task="binary_classification",
                       primary_metric="pr_auc")
        explicit = _spec(0.68, 0.70, direction="higher_is_better",
                         task="binary_classification", primary_metric="pr_auc")
        self.assertEqual(codes(ml.check(absent)), codes(ml.check(explicit)))

    def test_unrecognised_direction_falls_back_to_higher_is_better(self):
        # Documented limitation: a misspelling is not caught (that would need a
        # new DSX-SPEC code, an irreversible D-06 mint). It must at least behave
        # exactly like the pre-existing default rather than inventing a verdict.
        typo = _spec(0.68, 0.70, direction="lower_is_beter",
                     task="binary_classification", primary_metric="pr_auc")
        absent = _spec(0.68, 0.70, direction=None, task="binary_classification",
                       primary_metric="pr_auc")
        self.assertEqual(codes(ml.check(typo)), codes(ml.check(absent)))
        self.assertIn("DSX-ML-051", codes(ml.check(typo)))


class TestOverfitUnderLowerIsBetter(unittest.TestCase):
    """DSX-ML-060/061 under a declared lower-is-better metric."""

    def test_train_error_far_below_test_error_is_overfitting_not_leakage(self):
        # D-05: DSX-ML-060
        # train RMSE 0.10, test RMSE 0.50 — the ordinary overfit signature for
        # an error metric. Before the fix this fired DSX-ML-061 (leakage).
        spec = _overfit_spec(0.10, 0.50, direction="lower_is_better")
        found = codes(ml.check(spec))
        self.assertIn("DSX-ML-060", found)
        self.assertNotIn("DSX-ML-061", found)

    def test_test_error_far_below_train_error_is_suspicious_not_overfitting(self):
        # D-05: DSX-ML-061
        # test RMSE implausibly better than train RMSE — the leakage signature.
        spec = _overfit_spec(0.50, 0.10, direction="lower_is_better")
        found = codes(ml.check(spec))
        self.assertIn("DSX-ML-061", found)
        self.assertNotIn("DSX-ML-060", found)

    def test_small_error_gap_is_within_tolerance(self):
        spec = _overfit_spec(0.30, 0.32, direction="lower_is_better")
        found = codes(ml.check(spec))
        self.assertNotIn("DSX-ML-060", found)
        self.assertNotIn("DSX-ML-061", found)


class TestOverfitUnderHigherIsBetterUnchanged(unittest.TestCase):
    def test_train_above_test_still_overfitting(self):
        spec = _overfit_spec(0.95, 0.80, direction=None)
        found = codes(ml.check(spec))
        self.assertIn("DSX-ML-060", found)
        self.assertNotIn("DSX-ML-061", found)

    def test_test_above_train_still_suspicious(self):
        spec = _overfit_spec(0.80, 0.95, direction=None)
        found = codes(ml.check(spec))
        self.assertIn("DSX-ML-061", found)
        self.assertNotIn("DSX-ML-060", found)


class TestMarginUnderLowerIsBetter(unittest.TestCase):
    """DSX-ML-053 compares margin-over-baseline to the model's own fold spread.

    The margin is direction-sensitive for the same reason the baseline verdict
    is: `model_score - baseline_score` is negative for an improving error
    metric, which made the comparison against a positive spread fire almost
    unconditionally.
    """

    def _with_folds(self, model_score, baseline_score, folds, direction):
        spec = _spec(model_score, baseline_score, direction=direction)
        spec["results"]["fold_scores"] = folds
        return spec

    def test_wide_margin_on_error_metric_does_not_fire_053(self):
        # D-05: DSX-ML-053
        # Margin of 5.0 (10.0 -> 5.0) against a fold spread of 0.4.
        spec = self._with_folds(5.0, 10.0, [4.8, 5.0, 5.2], "lower_is_better")
        self.assertNotIn("DSX-ML-053", codes(ml.check(spec)))

    def test_narrow_margin_on_error_metric_fires_053(self):
        # D-05: DSX-ML-053
        # Margin of 0.1 (10.0 -> 9.9) against a fold spread of 2.0.
        spec = self._with_folds(9.9, 10.0, [9.0, 10.0, 11.0], "lower_is_better")
        self.assertIn("DSX-ML-053", codes(ml.check(spec)))


class TestDeterminism(unittest.TestCase):
    def test_two_consecutive_calls_produce_identical_sequences(self):
        spec = _spec(5.0, 10.0, direction="lower_is_better")
        self.assertEqual(codes(ml.check(spec)), codes(ml.check(spec)))


if __name__ == "__main__":
    unittest.main()
