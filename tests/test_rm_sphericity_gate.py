"""DSX-STA-070: the two-stage Mauchly-conditional sphericity gate (REQ-P19-01).

Declaration-only: keys on the declared ``analysis.sphericity_correction`` string ONLY,
never on the mere presence of a repeated-measures design (D-06 over-block guard — the
mixed-model / GEE route has no sphericity step). Drives ``_check_declared_advanced_stats``
directly, so the untouched ``_check_declared_test`` cannot fire a false DSX-STA-040/041 on a
fixture that also carried ``outcome_type`` + ``test`` (19-RESEARCH.md Pitfall 1); the
fixtures here carry neither, and the codes set is asserted EXHAUSTIVELY so a stray code
cannot hide behind an ``in`` check.

Stdlib-only, CRLF-safe. Mints nothing.
"""

from __future__ import annotations

import unittest

from dsx.checks import stats
from dsx.findings import Report


def _codes(analysis: dict) -> list[str]:
    report = Report(check="test")
    stats._check_declared_advanced_stats(analysis, {"analysis": analysis}, report)
    return [f.code for f in report.findings]


class Sta070SphericityGateTest(unittest.TestCase):
    def test_fires_on_mauchly_conditional(self):
        codes = _codes({"sphericity_correction": "mauchly_conditional"})  # D-05: DSX-STA-070
        self.assertEqual(set(codes), {"DSX-STA-070"})

    def test_fires_exactly_once(self):
        codes = _codes({"sphericity_correction": "mauchly_conditional"})
        self.assertEqual(codes.count("DSX-STA-070"), 1)

    def test_silent_on_unconditional_gg(self):
        codes = _codes({"sphericity_correction": "unconditional_gg"})
        self.assertEqual(set(codes), set())

    def test_silent_when_correction_absent(self):
        codes = _codes({"measure_kind": "continuous"})
        self.assertNotIn("DSX-STA-070", codes)

    def test_over_block_guard_silent_on_repeated_measures_presence(self):
        """D-06: a spec that merely declares a repeated-measures design (no two-stage
        token) must NOT fire — the gate keys on the declared correction, not the design."""
        codes = _codes(
            {"measure_kind": "continuous", "dependence_structure": "repeated_measures"}
        )
        self.assertEqual(set(codes), set())


if __name__ == "__main__":
    unittest.main()
