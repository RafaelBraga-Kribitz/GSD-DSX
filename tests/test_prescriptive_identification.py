"""Prescriptive identification parity and the no-hedge rule (REQ-P11.2-02, D-03).

A prescriptive claim recommends an intervention, so it asserts both that an
effect exists and that acting on it is warranted. It is held to the SAME
identification standard as a causal claim, reusing DSX-CLM-020 (CRITICAL, for
blank/none identification) and DSX-CLM-021 (HIGH, for weak identification) — no
new code. Unlike a causal claim, a prescriptive claim's hedging does NOT rescue
it: a recommendation is an action commitment, not a probabilistic statement.

These tests pin four prescriptive behaviours (RED until the ctype gate at
dsx/checks/claims.py:147 is widened) plus two causal behaviours that MUST stay
unchanged (the causal hedge exemption is preserved).

Stdlib unittest — no pytest dependency.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsx.checks import claims  # noqa: E402
from dsx.findings import Report, Severity  # noqa: E402


def _codes(report: Report) -> set[str]:
    return {f.code for f in report.findings}


def _finding(report: Report, code: str):
    for f in report.findings:
        if f.code == code:
            return f
    return None


class TestPrescriptiveIdentification(unittest.TestCase):
    # ── prescriptive: blank/none identification → DSX-CLM-020 CRITICAL ──────────

    def test_prescriptive_no_identification_is_critical(self):
        spec = {
            "design": {"kind": "observational", "identification": "none"},
            "claims": [
                {
                    "text": "We should increase onboarding spend to lift activation",
                    "type": "prescriptive",
                    "evidence": "R.md#1",
                }
            ],
        }
        report = claims.check(spec)
        self.assertIn("DSX-CLM-020", _codes(report))
        finding = _finding(report, "DSX-CLM-020")
        self.assertIsNotNone(finding)
        self.assertEqual(finding.severity, Severity.CRITICAL)

    # ── prescriptive: weak identification, unhedged → DSX-CLM-021 HIGH ──────────

    def test_prescriptive_weak_unhedged_is_high(self):
        spec = {
            "design": {"kind": "observational"},
            "claims": [
                {
                    "text": "Roll out the programme to increase retention by 4pp",
                    "type": "prescriptive",
                    "identification": "regression_adjustment",
                    "evidence": "R.md#1",
                }
            ],
        }
        report = claims.check(spec)
        self.assertIn("DSX-CLM-021", _codes(report))
        finding = _finding(report, "DSX-CLM-021")
        self.assertIsNotNone(finding)
        self.assertEqual(finding.severity, Severity.HIGH)

    # ── prescriptive: weak identification, HEDGED → STILL DSX-CLM-021 HIGH ──────
    # No hedge exemption: a recommendation is an action commitment.

    def test_prescriptive_weak_hedged_still_high(self):
        spec = {
            "design": {"kind": "observational"},
            "claims": [
                {
                    "text": (
                        "Roll out the programme, which may be associated with "
                        "higher retention"
                    ),
                    "type": "prescriptive",
                    "identification": "regression_adjustment",
                    "evidence": "R.md#1",
                }
            ],
        }
        report = claims.check(spec)
        # Sanity: the text genuinely hedges (a causal claim would be exempted).
        lowered = spec["claims"][0]["text"].lower()
        self.assertTrue(
            any(term in lowered for term in claims.HEDGE_TERMS),
            "test text must contain a hedge term to exercise the no-exemption rule",
        )
        self.assertIn("DSX-CLM-021", _codes(report))
        self.assertEqual(_finding(report, "DSX-CLM-021").severity, Severity.HIGH)

    # ── prescriptive message shape: reads as a recommendation, not causal ───────

    def test_prescriptive_message_differs_from_causal(self):
        prescriptive_spec = {
            "design": {"kind": "observational", "identification": "none"},
            "claims": [
                {
                    "text": "We should increase onboarding spend to lift activation",
                    "type": "prescriptive",
                    "evidence": "R.md#1",
                }
            ],
        }
        causal_spec = {
            "design": {"kind": "observational", "identification": "none"},
            "claims": [
                {
                    "text": "Onboarding causes a 12% lift",
                    "type": "causal",
                    "evidence": "R.md#1",
                }
            ],
        }
        p_finding = _finding(claims.check(prescriptive_spec), "DSX-CLM-020")
        c_finding = _finding(claims.check(causal_spec), "DSX-CLM-020")
        self.assertIsNotNone(p_finding)
        self.assertIsNotNone(c_finding)
        # Parameterisation is real, not cosmetic: the messages differ.
        self.assertNotEqual(p_finding.title, c_finding.title)
        # The prescriptive message reads as a recommendation on an intervention.
        p_text = f"{p_finding.title} {p_finding.detail}".lower()
        self.assertTrue(
            "recommend" in p_text or "intervention" in p_text,
            f"prescriptive message should read as a recommendation: {p_finding.title!r}",
        )

    # ── causal parity guards: causal behaviour MUST be unchanged ───────────────
    # These two cases already pass on the pre-widening code; they pin that the
    # widening is a strict superset and does not touch the causal path.

    def test_causal_weak_hedged_has_no_finding(self):
        spec = {
            "design": {"kind": "observational", "identification": "matching"},
            "claims": [
                {
                    "text": "The programme may be associated with higher retention",
                    "type": "causal",
                    "evidence": "R.md#1",
                }
            ],
        }
        # Causal hedge exemption preserved: hedged weak causal → no DSX-CLM-021.
        self.assertNotIn("DSX-CLM-021", _codes(claims.check(spec)))

    def test_causal_weak_unhedged_still_high(self):
        spec = {
            "design": {"kind": "observational", "identification": "matching"},
            "claims": [
                {
                    "text": "The programme increases retention by 4pp",
                    "type": "causal",
                    "evidence": "R.md#1",
                }
            ],
        }
        report = claims.check(spec)
        self.assertIn("DSX-CLM-021", _codes(report))
        self.assertEqual(_finding(report, "DSX-CLM-021").severity, Severity.HIGH)


if __name__ == "__main__":
    unittest.main()
