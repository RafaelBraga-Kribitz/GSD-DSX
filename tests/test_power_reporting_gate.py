"""DSX-STA-111: the observed / post-hoc power-reporting gate (REQ-P19-06b).

Narrow membership: fires ONLY on ``analysis.power_reporting_type`` in {observed, post_hoc}.
a_priori / design / mde_sensitivity do NOT fire (D-06 narrow; broadening is a D-13 deferral).
Drives ``_check_declared_advanced_stats`` directly so no false DSX-STA-040/041 appears
(Pitfall 1); codes asserted EXHAUSTIVELY. Stdlib-only, CRLF-safe. Mints nothing.
"""

from __future__ import annotations

import unittest

from dsx.checks import stats
from dsx.findings import Report


def _codes(analysis: dict) -> list[str]:
    report = Report(check="test")
    stats._check_declared_advanced_stats(analysis, {"analysis": analysis}, report)
    return [f.code for f in report.findings]


class Sta111PowerReportingTest(unittest.TestCase):
    def test_fires_on_observed(self):
        codes = _codes({"power_reporting_type": "observed"})  # D-05: DSX-STA-111
        self.assertEqual(set(codes), {"DSX-STA-111"})

    def test_fires_on_post_hoc(self):
        codes = _codes({"power_reporting_type": "post_hoc"})
        self.assertEqual(set(codes), {"DSX-STA-111"})

    def test_silent_on_a_priori(self):
        codes = _codes({"power_reporting_type": "a_priori"})
        self.assertEqual(set(codes), set())

    def test_silent_on_design(self):
        codes = _codes({"power_reporting_type": "design"})
        self.assertEqual(set(codes), set())

    def test_silent_on_mde_sensitivity(self):
        codes = _codes({"power_reporting_type": "mde_sensitivity"})
        self.assertEqual(set(codes), set())


if __name__ == "__main__":
    unittest.main()
