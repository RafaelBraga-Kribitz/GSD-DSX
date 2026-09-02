"""DSX-STA-090: the resampling-quadruple completeness gate (REQ-P19-04).

Presence-only over the declared ``analysis.resampling`` block: fires ONCE naming the missing
member(s) of ``{method, seed, B, unit}`` — never four codes, and B's VALUE is never checked.
Drives ``_check_declared_advanced_stats`` directly so no false DSX-STA-040/041 appears
(19-RESEARCH.md Pitfall 1); codes asserted EXHAUSTIVELY. Stdlib-only, CRLF-safe. Mints nothing.
"""

from __future__ import annotations

import unittest

from dsx.checks import stats
from dsx.findings import Report

_COMPLETE = {"method": "bca", "seed": 42, "B": 2000, "unit": "cluster"}


def _report(analysis: dict) -> Report:
    report = Report(check="test")
    stats._check_declared_advanced_stats(analysis, {"analysis": analysis}, report)
    return report


def _codes(analysis: dict) -> list[str]:
    return [f.code for f in _report(analysis).findings]


class Sta090ResamplingQuadrupleTest(unittest.TestCase):
    def test_fires_once_on_missing_B_and_unit(self):
        codes = _codes({"resampling": {"method": "bca", "seed": 42}})  # D-05: DSX-STA-090
        self.assertEqual(set(codes), {"DSX-STA-090"})
        self.assertEqual(codes.count("DSX-STA-090"), 1)

    def test_message_names_the_missing_members(self):
        findings = _report({"resampling": {"method": "bca", "seed": 42}}).findings
        detail = next(f.detail for f in findings if f.code == "DSX-STA-090")
        self.assertIn("B", detail)
        self.assertIn("unit", detail)

    def test_missing_two_still_one_code(self):
        codes = _codes({"resampling": {"method": "permutation"}})
        self.assertEqual(codes.count("DSX-STA-090"), 1)

    def test_silent_on_complete_quadruple(self):
        codes = _codes({"resampling": dict(_COMPLETE)})
        self.assertEqual(set(codes), set())

    def test_b_value_never_checked(self):
        """B's presence is required, its value is not — a complete block with B=1 passes."""
        codes = _codes({"resampling": dict(_COMPLETE, B=1)})
        self.assertEqual(set(codes), set())

    def test_silent_when_no_resampling_block(self):
        codes = _codes({"outcome_type_note": "no resampling declared"})
        self.assertEqual(set(codes), set())


if __name__ == "__main__":
    unittest.main()
