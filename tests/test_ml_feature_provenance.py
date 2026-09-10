"""Unit tests for the DSX-ML-034 feature-provenance check (REQ-P27-02).

DSX-ML-034 is a declaration-only feature-provenance check. It reads a declared
``model.feature_provenance[]`` block and fires CRITICAL when a feature is declared
``available_at: after_prediction`` and HIGH when ``available_at: unknown`` without a
waiver. It buys attribution, not detection: a spec that omits or lies in the block
still passes (the standing "a frame that lies passes" limit).

# D-05: DSX-ML-034
The citation carried by ``_check_feature_provenance`` — Kaufman, Rosset, Perlich &
Stitelman (2012), "Leakage in Data Mining: Formulation, Detection, and Avoidance,"
ACM Transactions on Knowledge Discovery from Data 6(4), Article 15 — was
read first-hand from the ACM PDF on 2026-09-11 (operator-supplied copy; locators
recorded in the check docstring: Sec. 3.1 p. 15:8 and Sec. 3.2 eq. (3) p. 15:9).
From 2026-09-07 until that read it had been secondary-corroborated only, the PDF
paywalled (27-CONTEXT.md §S3-1-CLOSE; HUMAN-QUEUE HQ-40 row 40b, dated update).
These tests assert the check's behaviour; the read is recorded, not re-performed,
here.
"""

from __future__ import annotations

import unittest

from dsx.checks.ml import check
from dsx.findings import Severity


def _codes(report) -> set[str]:
    return {f.code for f in report.findings}


def _find(report, code: str):
    return [f for f in report.findings if f.code == code]


class TestFeatureProvenance(unittest.TestCase):
    """Drive each behaviour bullet of the frozen §S3-1-CLOSE severity map."""

    def _spec(self, provenance=None, include_key: bool = True) -> dict:
        model = {
            "task": "binary_classification",
            "target": "churned_90d",
            "split": "temporal",
        }
        if include_key:
            model["feature_provenance"] = provenance if provenance is not None else []
        return {"question_type": "predictive", "model": model}

    def test_after_prediction_fires_critical(self):
        # A feature declared available_at after_prediction fires DSX-ML-034 CRITICAL.
        spec = self._spec(
            [{"feature": "account_health_index", "available_at": "after_prediction"}]
        )
        report = check(spec)
        found = _find(report, "DSX-ML-034")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.CRITICAL)

    def test_unknown_without_waiver_fires_high(self):
        # available_at unknown with no waiver fires DSX-ML-034 HIGH.
        spec = self._spec([{"feature": "risk_flag", "available_at": "unknown"}])
        report = check(spec)
        found = _find(report, "DSX-ML-034")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.HIGH)

    def test_unknown_with_waiver_is_silent(self):
        # available_at unknown AND a truthy waiver emits no DSX-ML-034.
        spec = self._spec(
            [{"feature": "risk_flag", "available_at": "unknown", "waiver": "reviewed 2026-09-07"}]
        )
        self.assertNotIn("DSX-ML-034", _codes(check(spec)))

    def test_before_and_at_prediction_are_legitimate(self):
        # before_prediction and at_prediction emit no DSX-ML-034.
        spec = self._spec(
            [
                {"feature": "tenure_days", "available_at": "before_prediction"},
                {"feature": "plan_tier", "available_at": "at_prediction"},
            ]
        )
        self.assertNotIn("DSX-ML-034", _codes(check(spec)))

    def test_silent_when_block_absent(self):
        # A model block with no feature_provenance key emits no DSX-ML-034
        # (the empty/absent boundary).
        spec = self._spec(include_key=False)
        self.assertNotIn("DSX-ML-034", _codes(check(spec)))

    def test_normalization_of_available_at(self):
        # "  After_Prediction  " (mixed case / surrounding whitespace) is treated
        # identically to "after_prediction".
        spec = self._spec(
            [{"feature": "account_health_index", "available_at": "  After_Prediction  "}]
        )
        report = check(spec)
        found = _find(report, "DSX-ML-034")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.CRITICAL)

    def test_missing_available_at_fires_high(self):
        # WR-01 (27-REVIEW.md): an entry that OMITS available_at must not be more
        # permissive than an honest 'unknown'. It is unattested → HIGH.
        spec = self._spec([{"feature": "risk_flag", "source": "billing"}])
        report = check(spec)
        found = _find(report, "DSX-ML-034")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.HIGH)

    def test_offvocabulary_available_at_fires_high(self):
        # WR-01: an off-vocabulary / typo'd available_at is unattested → HIGH,
        # never silently cleared.
        spec = self._spec(
            [{"feature": "risk_flag", "available_at": "afterprediction"}]
        )
        report = check(spec)
        found = _find(report, "DSX-ML-034")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.HIGH)

    def test_missing_available_at_with_waiver_is_silent(self):
        # WR-01: a waiver suppresses an unattested (missing) availability the same
        # way it suppresses an honest 'unknown' — the escape hatch is symmetric.
        spec = self._spec(
            [{"feature": "risk_flag", "source": "billing", "waiver": "reviewed 2026-09-07"}]
        )
        self.assertNotIn("DSX-ML-034", _codes(check(spec)))


if __name__ == "__main__":
    unittest.main()
