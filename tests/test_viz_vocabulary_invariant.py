"""Repo-integrity invariant: every chart mark has a home, every ban is a
complete refusal record.

Off the gate path by construction (``tests/`` is never in
``dsx.cli.GATE_PROFILES``' import closure). Reads the live vocabulary objects
directly — these are Python dicts/sets, so there is no CRLF or line-anchoring
concern here, unlike the Markdown-parsing catalogue invariant.

Covers REQ-P21-01 (D-01 every-mark-has-a-home, two clauses + frozen
CAPABILITY_ONLY allowlist) and REQ-P21-02 (D-02 refusal-record completeness).

Run: python -m unittest tests.test_viz_vocabulary_invariant -v
"""

from __future__ import annotations

import importlib.util
import pathlib
import unittest

from dsx.checks.smells import DENSITY_MARKS, STACKED_MARKS
from dsx.checks.viz import BANNED_TYPES, LENGTH_ENCODED, RELATIONSHIP_CHARTS
from dsx.checks.viz import check as viz_check
from dsx.spec import CHART_CAPABILITIES

_ROOT = pathlib.Path(__file__).resolve().parents[1]
_GEN_INPUT_TYPES = _ROOT / "scripts" / "gen-input-types.py"


def _load_gen_input_types():
    """Load scripts/gen-input-types.py without running its __main__ guard.

    The filename is hyphenated and has no ``__init__.py`` sibling, so a normal
    ``import`` is impossible; this is the same importlib precedent
    tests/test_phase20_zero_mint_close.py uses for its sibling script. The
    module body only defines dicts and a main() (the CHART_CAPABILITIES import
    is lazy, inside main()), so exec_module is side-effect-free.
    """
    spec = importlib.util.spec_from_file_location("gen_input_types_mod", _GEN_INPUT_TYPES)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


EXTRA_MARKS = _load_gen_input_types().EXTRA_MARKS

# Frozen per D-01 clause 2: marks that are capability-homed but deliberately
# have no relationship home (RELATIONSHIP_CHARTS is a curated recommendation
# surface, not exhaustive). Adding a mark here without justification fails
# review. Promotion of any of these to a relationship home is a Phase 22
# catalog decision, not a Phase 21 change.
CAPABILITY_ONLY = frozenset({
    "column", "grouped_bar", "multi_line", "bubble", "donut", "sunburst",
    "icicle", "circle_pack", "timeline", "gantt", "big_number",
    "candlestick", "ohlc_bar", "column_range",
})


def _mark_universe() -> frozenset[str]:
    """Every mark named by any surface or property set, minus the banned marks
    (which are exempt from homing and covered by the refusal invariant)."""
    marks: set[str] = set()
    for group in RELATIONSHIP_CHARTS.values():
        marks.update(group)
    for group in CHART_CAPABILITIES.values():
        marks.update(group)
    for group in EXTRA_MARKS.values():
        marks.update(group)
    marks.update(LENGTH_ENCODED, DENSITY_MARKS, STACKED_MARKS)
    return frozenset(marks) - frozenset(BANNED_TYPES)


def _capability_homed() -> frozenset[str]:
    """Gate-faithful capability home: exactly what _check_input_type_matrix
    (DSX-VIZ-013) admits from — CHART_CAPABILITIES values ∪ EXTRA_MARKS values."""
    homed: set[str] = set()
    for group in CHART_CAPABILITIES.values():
        homed.update(group)
    for group in EXTRA_MARKS.values():
        homed.update(group)
    return frozenset(homed)


def _relationship_homed() -> frozenset[str]:
    homed: set[str] = set()
    for group in RELATIONSHIP_CHARTS.values():
        homed.update(group)
    return frozenset(homed)


class TestEveryMarkHasAHome(unittest.TestCase):
    """D-01, REQ-P21-01: the two directional homing clauses + allowlist staleness,
    plus the gate smokes proving the homing removed real DSX-VIZ-013 friction."""

    def test_mark_universe_is_non_vacuous(self):
        # Anti-vacuity guard for every clause that subtracts from the universe:
        # if the vocabulary were ever emptied (a bad import, a renamed module),
        # the two capability/relationship set-difference clauses below would pass
        # VACUOUSLY — an empty set is trivially a subset of any home. Anchor on a
        # handful of marks that must always exist and a floor well under the live
        # count (50), mirroring the anti-vacuity superset guards used elsewhere.
        universe = _mark_universe()
        self.assertGreaterEqual(
            len(universe), 30, "mark universe collapsed — homing clauses would pass vacuously"
        )
        anchors = frozenset({"bar", "line", "scatter", "histogram", "box"})
        missing = sorted(anchors - universe)
        self.assertFalse(missing, f"core marks missing from the universe: {missing}")

    def test_every_mark_has_a_capability_home(self):
        universe = _mark_universe()
        orphans = sorted(universe - _capability_homed())
        self.assertFalse(orphans, f"marks with no capability home: {orphans}")

    def test_every_mark_has_a_relationship_home_or_is_allowlisted(self):
        universe = _mark_universe()
        unhomed = universe - _relationship_homed()
        not_allowlisted = sorted(unhomed - CAPABILITY_ONLY)
        self.assertFalse(
            not_allowlisted,
            f"marks with no relationship home and not on CAPABILITY_ONLY: {not_allowlisted}",
        )

    def test_capability_only_allowlist_is_exact_not_a_superset(self):
        # An allowlist entry that secretly HAS a relationship home is stale —
        # it hides a mark that is actually homed, defeating the "loud" intent.
        stale = sorted(CAPABILITY_ONLY & _relationship_homed())
        self.assertFalse(
            stale, f"CAPABILITY_ONLY entries that already have a relationship home: {stale}"
        )
        # A phantom allowlist entry (a mark no surface actually names) rots
        # silently: it is subtracted from `unhomed` but guards nothing real.
        # Every allowlisted mark must be a genuine member of the mark universe.
        phantom = sorted(CAPABILITY_ONLY - _mark_universe())
        self.assertFalse(
            phantom, f"CAPABILITY_ONLY entries absent from the mark universe: {phantom}"
        )

    # ── Gate smokes: the homing is only real if the DSX-VIZ-013 friction is gone
    # on both admissibility paths (coarse family reads CHART_CAPABILITIES live;
    # the IT-id path reads the generated dsx/data/input_types.json). ──────────

    @staticmethod
    def _viz013(chart_type: str, shape: str) -> list:
        spec = {
            "visuals": [
                {
                    "name": "smoke",
                    "relationship": "distribution",
                    "type": chart_type,
                    "data_input_type": shape,
                }
            ]
        }
        return [f for f in viz_check(spec).findings if f.code == "DSX-VIZ-013"]

    def test_coarse_family_path_admits_a_homed_mark(self):
        # interval-range + histogram must not fire DSX-VIZ-013 once histogram is
        # homed into CHART_CAPABILITIES["interval-range"].
        self.assertEqual(self._viz013("histogram", "interval-range"), [])

    def test_input_type_id_path_admits_a_homed_mark(self):
        # IT040 is an interval-range-family id with no EXTRA_MARKS entry, so its
        # admissible set is regenerated from CHART_CAPABILITIES["interval-range"].
        # After regeneration it must admit histogram (proves the generated JSON
        # was refreshed, not just the live dict).
        self.assertEqual(self._viz013("histogram", "IT040"), [])


class TestRefusalEntryCompleteness(unittest.TestCase):
    """D-02, REQ-P21-02: every banned mark is a complete {reason, code, citation}
    refusal record, every code is the one _check_banned emits, and the enriched
    reason still reaches the finding detail."""

    def test_every_banned_type_has_a_complete_refusal_record(self):
        for mark, record in BANNED_TYPES.items():
            with self.subTest(mark):
                self.assertIsInstance(record, dict)
                for field in ("reason", "code", "citation"):
                    self.assertIn(field, record)
                    self.assertTrue(str(record[field]).strip(), f"{mark}.{field} is empty")

    def test_every_refusal_code_is_the_code_check_banned_emits(self):
        for mark, record in BANNED_TYPES.items():
            with self.subTest(mark):
                self.assertEqual(record["code"], "DSX-VIZ-001")

    def test_check_banned_detail_is_the_reason_string(self):
        spec = {"visuals": [{"name": "bad", "type": "radar", "relationship": "comparison"}]}
        found = [f for f in viz_check(spec).findings if f.code == "DSX-VIZ-001"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].detail, BANNED_TYPES["radar"]["reason"])


if __name__ == "__main__":
    unittest.main()
