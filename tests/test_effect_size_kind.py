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

_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from dsx import mathx  # noqa: E402
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


# ── Plan 18-B: report-only correlation/agreement convention bands (REQ-P18-05) ──
#
# These extend, never rewrite, the DSX-STA-011/012 shapes above. They pin the
# D-06 firewall (EFFECT_SIZE_KINDS stays {d, h, r}), the D-07 pins (0.7598 @
# ordinal; Landis-Koch kappa bands), and the catalog-only presence contract
# (ICC/Kendall's W/dCor/partial/Cronbach->omega named, no numeric boundary).


class TestEffectSizeKindsFirewall(unittest.TestCase):
    """D-06 firewall: the blocking magnitude-band domain never widens."""

    def test_effect_size_kinds_is_exactly_d_h_r(self):  # REQ-P18-05
        # Equality, NOT subset — a future add of a convention kind turns this red.
        self.assertEqual(mathx.EFFECT_SIZE_KINDS, frozenset({"d", "h", "r"}))

    def test_interpret_effect_still_rejects_a_report_only_kind(self):  # REQ-P18-05
        # interpret_effect's domain is unchanged: a report-only kind is unknown
        # to it and must still raise, never be flat-banded.
        with self.assertRaises(ValueError):
            mathx.interpret_effect("kappa", 0.7)


class TestReportOnlyEffectKindsRegistry(unittest.TestCase):
    """The recognition set the DSX-STA-012 branch (Plan 18-A) consults."""

    def test_registry_is_a_frozenset_with_the_required_kinds(self):  # REQ-P18-05
        self.assertIsInstance(mathx.REPORT_ONLY_EFFECT_KINDS, frozenset)
        required = {"kappa", "icc", "kendalls_w", "phi", "cramers_v", "tau_b", "rho"}
        self.assertTrue(
            required <= set(mathx.REPORT_ONLY_EFFECT_KINDS),
            f"missing report-only kinds: {required - set(mathx.REPORT_ONLY_EFFECT_KINDS)}",
        )

    def test_registry_is_disjoint_from_the_blocking_domain(self):  # REQ-P18-05
        self.assertTrue(
            set(mathx.EFFECT_SIZE_KINDS).isdisjoint(mathx.REPORT_ONLY_EFFECT_KINDS),
            "a kind may not be both a blocking band and a report-only convention",
        )


class TestKrippendorffReferencePin(unittest.TestCase):
    """D-07: 0.7598 is pinned AT level=ordinal and ALWAYS carries its level."""

    def test_ordinal_value_is_pinned(self):  # REQ-P18-05 (pinned)
        # Numeric equality is allowed here: confirmed at source (HQ-16 B4).
        self.assertEqual(mathx.KRIPPENDORFF_REFERENCE["ordinal"], 0.7598)

    def test_other_levels_carry_their_own_values(self):  # REQ-P18-05 (pinned)
        self.assertEqual(mathx.KRIPPENDORFF_REFERENCE["nominal"], 0.4765)
        self.assertEqual(mathx.KRIPPENDORFF_REFERENCE["interval"], 0.7574)
        self.assertEqual(mathx.KRIPPENDORFF_REFERENCE["ratio"], 0.6621)

    def test_the_value_is_level_keyed_not_level_free(self):  # REQ-P18-05 (pinned)
        # A level-free pin is wrong (D-07): the value is level-dependent, so the
        # ordinal value is reachable ONLY by asking for the ordinal level.
        self.assertEqual(mathx.KRIPPENDORFF_REFERENCE.get("ordinal"), 0.7598)
        self.assertIsNone(mathx.KRIPPENDORFF_REFERENCE.get(None))
        self.assertIsNone(mathx.KRIPPENDORFF_REFERENCE.get(""))


class TestLandisKochKappaBands(unittest.TestCase):
    """D-07: Landis-Koch kappa bands pinned as a labeled convention."""

    def test_representative_points_across_published_boundaries(self):  # REQ-P18-05 (pinned)
        cases = [
            (-0.10, "poor"),
            (0.10, "slight"),
            (0.30, "fair"),
            (0.50, "moderate"),
            (0.70, "substantial"),
            (0.90, "almost perfect"),
        ]
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(mathx.label_convention_band("kappa", value), expected)

    def test_edge_tie_is_only_a_labeled_convention(self):  # REQ-P18-05 (pinned)
        # A value ON a published boundary (0.20) is resolved by a labeled
        # CONVENTION (lower band takes the tie), NOT claimed as the paper's exact
        # wording — so we assert only that it yields SOME Landis-Koch band label.
        label = mathx.label_convention_band("kappa", 0.20)
        self.assertIn(label, {lbl for _, lbl in mathx.KAPPA_BANDS})

    def test_label_convention_band_never_raises_for_a_catalog_only_kind(self):  # REQ-P18-05
        # Distinct from interpret_effect: report-only, never a blocking guard, so
        # it returns a "convention" label rather than raising for a report-only kind.
        try:
            label = mathx.label_convention_band("icc", 0.8)
        except Exception as exc:  # noqa: BLE001 - the point is that it must not raise
            self.fail(f"label_convention_band raised as if a blocking guard: {exc!r}")
        self.assertIsInstance(label, str)
        self.assertTrue(label.strip())


class TestConventionCatalogPresence(unittest.TestCase):
    """D-07: catalog-only items are NAMED entries with NO numeric boundary.

    Presence/substring assertions ONLY — never a numeric equality assertion for
    ICC/Koo-Li, Kendall's W, dCor, partial correlation, or Cronbach->omega.
    """

    def test_named_catalog_entries_present_and_boundary_free(self):  # REQ-P18-05 (catalog-only)
        for key in (
            "icc",
            "kendalls_w",
            "distance_correlation",
            "partial_correlation",
            "cronbach_to_omega",
        ):
            with self.subTest(key=key):
                self.assertIn(key, mathx.CONVENTION_CATALOG)
                self.assertIsInstance(mathx.CONVENTION_CATALOG[key], str)
                self.assertTrue(mathx.CONVENTION_CATALOG[key].strip())

    def test_kendalls_w_carries_the_no_band_citation_note(self):  # REQ-P18-05 (catalog-only)
        self.assertIn(
            "no band citation exists",
            mathx.CONVENTION_CATALOG["kendalls_w"].lower(),
        )


if __name__ == "__main__":
    unittest.main()
