"""DSX-STA-080/081: the trend-companion gates (REQ-P19-02).

Declaration-only: ``analysis.trend_test`` is str OR list — its non-blank normalized tokens
are collected into a set. DSX-STA-080 fires on a declared ``cochran_armitage`` with a blank
``analysis.dose_scores``; DSX-STA-081 on a declared ``mann_kendall`` / ``sens_slope`` with a
blank ``analysis.autocorrelation_handling``. DSX-STA-081 is an is_blank predicate, NOT a
membership one — a declared ``none`` / ``independent`` is non-blank and SATISFIES (Pitfall 5).

Drives ``_check_declared_advanced_stats`` directly so no false DSX-STA-040/041 can appear
(19-RESEARCH.md Pitfall 1); codes asserted EXHAUSTIVELY. Stdlib-only, CRLF-safe. Mints nothing.
"""

from __future__ import annotations

import unittest

from dsx.checks import stats
from dsx.findings import Report


def _codes(analysis: dict) -> list[str]:
    report = Report(check="test")
    stats._check_declared_advanced_stats(analysis, {"analysis": analysis}, report)
    return [f.code for f in report.findings]


class Sta080DoseScoresTest(unittest.TestCase):
    def test_fires_on_cochran_armitage_without_dose_scores(self):
        codes = _codes({"trend_test": "cochran_armitage"})  # D-05: DSX-STA-080
        self.assertEqual(set(codes), {"DSX-STA-080"})

    def test_silent_when_dose_scores_present(self):
        codes = _codes({"trend_test": "cochran_armitage", "dose_scores": [0, 1, 2]})
        self.assertEqual(set(codes), set())


class Sta081AutocorrelationTest(unittest.TestCase):
    def test_fires_on_mann_kendall_without_handling(self):
        codes = _codes({"trend_test": "mann_kendall"})  # D-05: DSX-STA-081
        self.assertEqual(set(codes), {"DSX-STA-081"})

    def test_fires_on_sens_slope_without_handling(self):
        codes = _codes({"trend_test": "sens_slope"})
        self.assertEqual(set(codes), {"DSX-STA-081"})

    def test_silent_on_declared_none_handling(self):
        """The is_blank tell: a declared 'none' is non-blank and SATISFIES (Pitfall 5)."""
        codes = _codes({"trend_test": "mann_kendall", "autocorrelation_handling": "none"})
        self.assertEqual(set(codes), set())

    def test_silent_on_declared_independent_handling(self):
        codes = _codes(
            {"trend_test": "mann_kendall", "autocorrelation_handling": "independent"}
        )
        self.assertEqual(set(codes), set())


class TrendListTest(unittest.TestCase):
    def test_list_trend_fires_both_when_both_companions_blank(self):
        codes = _codes({"trend_test": ["cochran_armitage", "mann_kendall"]})
        self.assertEqual(set(codes), {"DSX-STA-080", "DSX-STA-081"})


if __name__ == "__main__":
    unittest.main()
