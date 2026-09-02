"""DSX-STA-120/121/122: the proportion-interval and count-model gates (REQ-P19-07).

Declaration-only equality/presence. DSX-STA-120 fires on
normalize(analysis.proportion_ci_method) == 'wald' (n-independent; NO hard-coded n<=40).
DSX-STA-121 on a declared ``analysis.exposure`` with a blank ``analysis.offset``. DSX-STA-122
on a declared ``analysis.nnt`` with a blank ``analysis.nnt_ci``. Drives
``_check_declared_advanced_stats`` directly so no false DSX-STA-040/041 appears (Pitfall 1);
codes asserted EXHAUSTIVELY. Stdlib-only, CRLF-safe. Mints nothing.
"""

from __future__ import annotations

import unittest

from dsx.checks import stats
from dsx.findings import Report


def _codes(analysis: dict) -> list[str]:
    report = Report(check="test")
    stats._check_declared_advanced_stats(analysis, {"analysis": analysis}, report)
    return [f.code for f in report.findings]


class Sta120WaldIntervalTest(unittest.TestCase):
    def test_fires_on_wald(self):
        codes = _codes({"proportion_ci_method": "wald"})  # D-05: DSX-STA-120
        self.assertEqual(set(codes), {"DSX-STA-120"})

    def test_silent_on_wilson(self):
        codes = _codes({"proportion_ci_method": "wilson"})
        self.assertEqual(set(codes), set())

    def test_silent_on_jeffreys(self):
        codes = _codes({"proportion_ci_method": "jeffreys"})
        self.assertEqual(set(codes), set())


class Sta121ExposureOffsetTest(unittest.TestCase):
    def test_fires_on_exposure_without_offset(self):
        codes = _codes({"exposure": "person_years"})  # D-05: DSX-STA-121
        self.assertEqual(set(codes), {"DSX-STA-121"})

    def test_silent_when_offset_present(self):
        codes = _codes({"exposure": "person_years", "offset": "log_person_years"})
        self.assertEqual(set(codes), set())


class Sta122NntCiTest(unittest.TestCase):
    def test_fires_on_nnt_without_ci(self):
        codes = _codes({"nnt": 12})  # D-05: DSX-STA-122
        self.assertEqual(set(codes), {"DSX-STA-122"})

    def test_silent_when_nnt_ci_present(self):
        codes = _codes({"nnt": 12, "nnt_ci": [8, 25]})
        self.assertEqual(set(codes), set())


if __name__ == "__main__":
    unittest.main()
