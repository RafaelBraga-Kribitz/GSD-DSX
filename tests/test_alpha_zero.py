"""Regression: a declared ``design.alpha: 0`` must be honoured, not silently
replaced by the 0.05 default.

The bug was the falsy-``or`` idiom ``as_number(get(spec, "design.alpha")) or 0.05``:
``as_number(0)`` is ``0.0``, which is falsy, so ``0.0 or 0.05`` evaluated to
``0.05`` and an explicitly declared alpha of zero was thrown away. It was present
at five call sites across four checks — dsx/checks/decision.py, dsx/checks/stats.py,
dsx/frame/paradigm.py and dsx/checks/design.py (two of them) — flagged as WR-02/WR-04
by the Phase 7/8/9 reviews and carried into the v2.0.0 milestone audit as an
uncounted tech-debt item. The fix applies the default on ``None`` (absent) rather
than on falsiness.

Each test declares ``design.alpha: 0`` and asserts the finding text the check
emits reflects a zero alpha, which only holds once the default stops firing on
``0.0``. Existing tests use normal alphas and are unaffected, because the fix
changes behaviour only when ``as_number`` returns exactly ``0.0``.

Run:  python3 -m unittest tests.test_alpha_zero -v
"""

from __future__ import annotations

import unittest

from dsx.checks import decision, stats
from dsx.checks.design import _check_peeking
from dsx.findings import Report
from dsx.frame.paradigm import _check_monitoring_discipline


class AlphaZeroHonoured(unittest.TestCase):
    def _find(self, report: Report, code: str):
        for finding in report.findings:
            if finding.code == code:
                return finding
        self.fail(f"expected {code} in {[f.code for f in report.findings]}")

    def test_stats_reporting_ci_uses_declared_zero_alpha(self):
        # A test with a p-value but no CI fires DSX-STA-003, whose remedy quotes
        # the (1 - alpha) confidence level. alpha=0 -> a 100% CI, not the
        # default's 95%.
        spec = {
            "design": {"alpha": 0},
            "results": {"tests": [{"metric": "conv", "p_value": 0.5}]},
        }
        finding = self._find(stats.check(spec), "DSX-STA-003")
        self.assertIn("100%", finding.remedy)
        self.assertNotIn("95%", finding.remedy)

    def test_decision_replay_pass_compares_against_declared_zero_alpha(self):
        # A replay PASS with any p >= alpha fires DSX-DEC-021. Under the bug
        # (alpha silently 0.05) p=0.03 < 0.05 cleared it; honouring alpha=0
        # means 0.03 >= 0 and the incoherence fires, naming alpha=0.0.
        spec = {
            "question_type": "causal",
            "design": {"alpha": 0},
            "results": {"tests": [{"metric": "conv", "effect": 0.5, "p_value": 0.03}]},
            "decision": {
                "replay": {
                    "metric": "conv",
                    "on_pass": "ship",
                    "on_fail": "hold",
                    "effect_min": 0.1,
                }
            },
        }
        finding = self._find(decision.check(spec), "DSX-DEC-021")
        self.assertIn("alpha=0.0", finding.title)

    def test_design_peeking_inflation_uses_declared_zero_alpha(self):
        # A fixed-horizon design peeked more than once fires DSX-EXP-060, whose
        # detail states the type-I inflation "from {alpha} to roughly {inflated}".
        # alpha=0 -> "from 0.00 to roughly 0.00", never the default's "from 0.05".
        design = {"peeking_policy": "fixed_horizon", "alpha": 0}
        spec = {"results": {"interim_looks": 5}}
        report = Report(check="design")
        _check_peeking(design, spec, report)
        finding = self._find(report, "DSX-EXP-060")
        self.assertIn("from 0.00 to roughly 0.00", finding.detail)
        self.assertNotIn("from 0.05", finding.detail)

    def test_paradigm_monitoring_reference_uses_declared_zero_alpha(self):
        # Uncontrolled continuous monitoring under a frequentist paradigm with no
        # discipline declared fires DSX-PAR-010; its detail quotes the nominal
        # alpha and the resulting inflation anchors. alpha=0 -> a nominal 0.00
        # and 0.000 inflation at every anchor, not 0.05 / 0.142.
        spec = {
            "design": {"peeking_policy": "uncontrolled_continuous", "alpha": 0},
            "inference": {"paradigm": "frequentist"},
        }
        report = Report(check="paradigm")
        _check_monitoring_discipline(spec, report)
        finding = self._find(report, "DSX-PAR-010")
        self.assertIn("alpha of 0.00", finding.detail)
        self.assertIn("0.000 at five interim looks", finding.detail)
        self.assertNotIn("0.142", finding.detail)


if __name__ == "__main__":
    unittest.main()
