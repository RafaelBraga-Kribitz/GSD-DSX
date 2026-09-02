"""DSX-STA-110: the variance-test-as-location-precondition gate (REQ-P19-06a).

Keys on the DECLARED ``analysis.variance_test_role`` (after membership of
``analysis.variance_test`` in VARIANCE_TESTS): fires on a blank role (declaration
incompleteness) OR ``precondition_to_location``; SILENT on ``scale_estimand`` (the scale test
IS the correct primary analysis when scale is the estimand). Never keys on the presence of
Levene/BF/Bartlett/Fligner alone (D-06). Drives ``_check_declared_advanced_stats`` directly so
no false DSX-STA-040/041 appears (Pitfall 1); codes asserted EXHAUSTIVELY. Stdlib-only,
CRLF-safe. Mints nothing.
"""

from __future__ import annotations

import unittest

from dsx.checks import stats
from dsx.findings import Report


def _codes(analysis: dict) -> list[str]:
    report = Report(check="test")
    stats._check_declared_advanced_stats(analysis, {"analysis": analysis}, report)
    return [f.code for f in report.findings]


class Sta110VarianceRoleTest(unittest.TestCase):
    def test_fires_on_precondition_role(self):
        codes = _codes(
            {"variance_test": "levene", "variance_test_role": "precondition_to_location"}
        )  # D-05: DSX-STA-110
        self.assertEqual(set(codes), {"DSX-STA-110"})

    def test_fires_on_blank_role(self):
        """Declaration incompleteness: a declared variance_test with no role blocks."""
        codes = _codes({"variance_test": "levene"})
        self.assertEqual(set(codes), {"DSX-STA-110"})

    def test_silent_on_scale_estimand(self):
        codes = _codes(
            {"variance_test": "brown_forsythe", "variance_test_role": "scale_estimand"}
        )
        self.assertEqual(set(codes), set())

    def test_silent_when_no_variance_test_declared(self):
        """Over-block guard: never fires without a declared variance_test."""
        codes = _codes({"variance_test_role": "precondition_to_location"})
        self.assertEqual(set(codes), set())


if __name__ == "__main__":
    unittest.main()
