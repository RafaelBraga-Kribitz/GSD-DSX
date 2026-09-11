"""Declaration-level claim->cited-test numeric traceability (DSX-CLM-034, REQ-P28-02).

`claims[].supported_by` names the `results.tests[]` entry a claim rests on. When
declared, every numeric literal in the claim text must trace to a reported number
of THAT cited test (the effect, its x100 proportion bridge, or a CI bound) within
`claims[].rounding` significant figures (default 2). A stray claim number outside
the cited test's numbers fires DSX-CLM-034 at HIGH. Absent `supported_by` -> silent
(declaration-gated: attribution, not detection -- the Phase-27 precedent).
"""

# D-05: DSX-CLM-034
# The D-05 citation for DSX-CLM-034 is Wilkinson, L. & the Task Force on Statistical
# Inference (1999), American Psychologist 54(8):594-604 -- cited as the MOTIVATING
# PRINCIPLE ("always present effect sizes / interval estimates for primary
# outcomes"). This is the principle that motivates the check; it is NOT claimed that
# Wilkinson mandates any numeric-overlap mechanism. The check enforces a
# declaration-level traceability corollary of that principle (a claim's headline
# magnitude must trace to the specific cited test), and it catches only via a stray
# claim number outside the cited test -- never via metric-identity (bounded-catch
# honesty, D-28-05).

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsx.checks import claims
from dsx.findings import Report, Severity


def _codes(report: Report) -> set[str]:
    return {f.code for f in report.findings}


def _finding(report: Report, code: str):
    for f in report.findings:
        if f.code == code:
            return f
    return None


class TestSupportedByTraceability(unittest.TestCase):
    # -- fires-on-uncovered: cited test does not cover a claim literal -> HIGH -----

    def test_fires_when_cited_test_does_not_cover_literal(self):
        spec = {
            "results": {
                "tests": [
                    {"metric": "churn_rate", "effect": 0.20, "ci": [0.16, 0.24]},
                ]
            },
            "claims": [
                {
                    "text": "Churn runs at 27% over the window.",
                    "type": "association",
                    "evidence": "R.md#1",
                    "supported_by": "churn_rate",
                }
            ],
        }
        report = claims.check(spec)
        self.assertIn("DSX-CLM-034", _codes(report))
        finding = _finding(report, "DSX-CLM-034")
        self.assertIsNotNone(finding)
        self.assertEqual(finding.severity, Severity.HIGH)

    # -- silent-when-covered: every literal traces to the cited test -> nothing ----

    def test_silent_when_cited_test_covers_every_literal(self):
        spec = {
            "results": {
                "tests": [
                    {"metric": "churn_rate", "effect": 0.27, "ci": [0.20, 0.34]},
                ]
            },
            "claims": [
                {
                    "text": "Churn runs at 27% over the window.",
                    "type": "association",
                    "evidence": "R.md#1",
                    "supported_by": "churn_rate",
                }
            ],
        }
        report = claims.check(spec)
        self.assertNotIn("DSX-CLM-034", _codes(report))

    # -- silent-when-absent: no supported_by key -> declaration-gated silence ------

    def test_silent_when_supported_by_absent(self):
        spec = {
            "results": {
                "tests": [
                    {"metric": "churn_rate", "effect": 0.20, "ci": [0.16, 0.24]},
                ]
            },
            "claims": [
                {
                    "text": "Churn runs at 27% over the window.",
                    "type": "association",
                    "evidence": "R.md#1",
                }
            ],
        }
        report = claims.check(spec)
        self.assertNotIn("DSX-CLM-034", _codes(report))

    # -- scale-bridge: pp literal reconciles with a proportion effect via x100 -----

    def test_scale_bridge_percent_literal_reconciles_with_proportion_effect(self):
        spec = {
            "results": {
                "tests": [
                    {"metric": "conversion", "effect": 0.15, "ci": [0.11, 0.19]},
                ]
            },
            "claims": [
                {
                    "text": "Conversion sits at 15% for the cohort.",
                    "type": "association",
                    "evidence": "R.md#1",
                    "supported_by": "conversion",
                }
            ],
        }
        report = claims.check(spec)
        self.assertNotIn("DSX-CLM-034", _codes(report))

    # -- tie-boundary: agree to exactly N sig figs is silent; last-digit miss fires --

    def test_tie_boundary_silent_at_sig_figs_and_fires_just_outside(self):
        silent_spec = {
            "results": {
                "tests": [
                    {"metric": "m1", "effect": 0.274},
                ]
            },
            "claims": [
                {
                    "text": "The rate is 27% over the window.",
                    "type": "association",
                    "evidence": "R.md#1",
                    "supported_by": "m1",
                    "rounding": 2,
                }
            ],
        }
        silent_report = claims.check(silent_spec)
        self.assertNotIn("DSX-CLM-034", _codes(silent_report))

        fires_spec = {
            "results": {
                "tests": [
                    {"metric": "m2", "effect": 0.28},
                ]
            },
            "claims": [
                {
                    "text": "The rate is 27% over the window.",
                    "type": "association",
                    "evidence": "R.md#1",
                    "supported_by": "m2",
                    "rounding": 2,
                }
            ],
        }
        fires_report = claims.check(fires_spec)
        self.assertIn("DSX-CLM-034", _codes(fires_report))

    # -- rounding-default: absent rounding uses 2 significant figures --------------

    def test_rounding_defaults_to_two_significant_figures(self):
        spec = {
            "results": {
                "tests": [
                    {"metric": "m", "effect": 0.274},
                ]
            },
            "claims": [
                {
                    "text": "The rate is 27% over the window.",
                    "type": "association",
                    "evidence": "R.md#1",
                    "supported_by": "m",
                    # no rounding key: comparator must default to 2 sig figs -> silent
                }
            ],
        }
        report = claims.check(spec)
        self.assertNotIn("DSX-CLM-034", _codes(report))

    # -- rounding-may-tighten: a smaller rounding makes a borderline literal fire --

    def test_rounding_may_tighten_to_fire_a_borderline_literal(self):
        spec = {
            "results": {
                "tests": [
                    {"metric": "m", "effect": 0.274},
                ]
            },
            "claims": [
                {
                    "text": "The rate is 27% over the window.",
                    "type": "association",
                    "evidence": "R.md#1",
                    "supported_by": "m",
                    "rounding": 3,  # tighter than the default 2 -> 27 no longer covers 27.4
                }
            ],
        }
        report = claims.check(spec)
        self.assertIn("DSX-CLM-034", _codes(report))


if __name__ == "__main__":
    unittest.main()
