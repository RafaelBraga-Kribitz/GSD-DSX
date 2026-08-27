"""DSX-STA-012: an unrecognised effect_size_kind is a visible MEDIUM, not a silent skip.

REQ-P11.3-05. A dedicated module (disjoint from test_dsx.py, which Wave-1 and other
plans read) pinning the membership guard that must PRECEDE interpret_effect in
dsx/checks/stats.py: an effect_size_kind outside the recognised {d, h, r} set fires
DSX-STA-012 MEDIUM and never raises (interpret_effect's ValueError-on-unknown-kind must
not reach the gate path), while a recognised kind stays silent.

Run:  python -m unittest tests.test_effect_size_kind -v
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dsx.checks import stats  # noqa: E402


def _codes(report) -> set[str]:
    return {f.code for f in report.findings}


def _spec(kind: str, *, standardized: float = 0.42, p: float = 0.001) -> dict:
    """A single significant test carrying a non-null standardized effect and a kind."""
    return {
        "design": {"alpha": 0.05},
        "results": {
            "tests": [
                {
                    "metric": "conversion",
                    "p_value": p,
                    "standardized_effect": standardized,
                    "effect_size_kind": kind,
                }
            ]
        },
    }


class TestEffectSizeKindGuard(unittest.TestCase):
    def test_unrecognised_kind_fires_medium(self):  # REQ-P11.3-05
        report = stats.check(_spec("cohens_d"))
        self.assertIn("DSX-STA-012", _codes(report))
        finding = next(f for f in report.findings if f.code == "DSX-STA-012")
        self.assertEqual(finding.severity.label, "MEDIUM")

    def test_unrecognised_kind_does_not_raise(self):  # REQ-P11.3-05
        # interpret_effect's raise ValueError (mathx.py:302) must never reach the
        # gate path: the guard decides membership BEFORE the call. No try/except.
        try:
            report = stats.check(_spec("glass_delta"))
        except Exception as exc:  # noqa: BLE001 - the whole point is that none escapes
            self.fail(f"unrecognised kind raised through the gate path: {exc!r}")
        self.assertIn("DSX-STA-012", _codes(report))

    def test_recognised_kind_stays_silent(self):  # REQ-P11.3-05
        # A recognised kind (d) still reaches the DSX-STA-011 magnitude guard and does
        # NOT fire DSX-STA-012. standardized=0.6 is a "small/medium" band, not negligible.
        report = stats.check(_spec("d", standardized=0.6))
        self.assertNotIn("DSX-STA-012", _codes(report))

    def test_crafted_mixed_case_whitespace_is_caught(self):  # REQ-P11.3-05
        # A crafted mixed-case/whitespace unrecognised kind must be routed through
        # normalize() and still treated as unrecognised — it cannot slip past the guard.
        report = stats.check(_spec("  Cohen's D  "))
        self.assertIn("DSX-STA-012", _codes(report))
        finding = next(f for f in report.findings if f.code == "DSX-STA-012")
        self.assertEqual(finding.severity.label, "MEDIUM")


class TestEffectSizeKindAbsentVsNull(unittest.TestCase):
    """Pin the absent-key vs explicit-null asymmetry as a documented invariant.

    IN-02 (11.3 S2-4 review, §4 persona round — BY-DESIGN, keep firing): an
    *absent* effect_size_kind defaults to the recognised "d" (backward-compatible
    "use the default") and stays silent; an *explicitly-null* kind is an author
    actively declaring an effect-size analysis with no valid kind — a real
    reporting gap — so it fires DSX-STA-012 MEDIUM rather than silently skipping
    the magnitude guard (D-11 intent). Treating null as absent would re-open that
    silent skip, so this asymmetry is pinned deliberately, not incidental.
    """

    @staticmethod
    def _base_test() -> dict:
        return {
            "metric": "conversion",
            "p_value": 0.001,
            "standardized_effect": 0.42,
        }

    def test_absent_effect_size_kind_stays_silent(self):
        spec = {"design": {"alpha": 0.05}, "results": {"tests": [self._base_test()]}}
        self.assertNotIn("DSX-STA-012", _codes(stats.check(spec)))

    def test_explicit_null_effect_size_kind_fires_medium(self):
        test = dict(self._base_test(), effect_size_kind=None)
        spec = {"design": {"alpha": 0.05}, "results": {"tests": [test]}}
        report = stats.check(spec)
        self.assertIn("DSX-STA-012", _codes(report))
        finding = next(f for f in report.findings if f.code == "DSX-STA-012")
        self.assertEqual(finding.severity.label, "MEDIUM")


if __name__ == "__main__":
    unittest.main()
