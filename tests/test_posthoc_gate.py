"""DSX-STA-100: the post-hoc/omnibus family-match gate (REQ-P19-05).

Membership-only: normalize(analysis.posthoc) tested against
``POSTHOC_FAMILY_MAP.get(normalize(analysis.omnibus), frozenset())`` after an is_blank
short-circuit on both fields. A deprecated post-hoc (SNK) is never a member of any acceptable
set. Drives ``_check_declared_advanced_stats`` directly so no false DSX-STA-040/041 appears
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


class Sta100PosthocFamilyTest(unittest.TestCase):
    def test_fires_on_family_mismatch(self):
        codes = _codes({"omnibus": "kruskal_wallis", "posthoc": "tukey_hsd"})  # D-05: DSX-STA-100
        self.assertEqual(set(codes), {"DSX-STA-100"})

    def test_silent_on_matched_pair(self):
        codes = _codes({"omnibus": "welch_anova", "posthoc": "games_howell"})
        self.assertEqual(set(codes), set())

    def test_silent_on_matched_anova_pair(self):
        codes = _codes({"omnibus": "anova", "posthoc": "tukey_hsd"})
        self.assertEqual(set(codes), set())

    def test_deprecated_posthoc_is_never_a_member(self):
        codes = _codes({"omnibus": "anova", "posthoc": "snk"})
        self.assertEqual(set(codes), {"DSX-STA-100"})

    def test_silent_when_omnibus_blank(self):
        codes = _codes({"posthoc": "tukey_hsd"})
        self.assertEqual(set(codes), set())

    def test_silent_when_posthoc_blank(self):
        codes = _codes({"omnibus": "kruskal_wallis"})
        self.assertEqual(set(codes), set())


if __name__ == "__main__":
    unittest.main()
