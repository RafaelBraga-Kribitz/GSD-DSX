"""Repo-integrity invariant: references/chart-catalog.md conforms to the live
vocabulary, its refusal rows are backed by live bans, its reference-only rows
stay outside the gate, and its perceptual rank data obeys Cleveland & McGill's
ordering (D-1). Covers REQ-P22-01 (the merged three-axis catalog) and the
REQ-P22-05 perceptual tie-break (a pure ordering assertion, no computation).

Off the gate path by construction (``tests/`` is never in
``dsx.cli.GATE_PROFILES``' import closure). The catalog is Markdown, so every
regex here is CRLF-safe (``\r?\n`` / whitespace-lenient), unlike the pure-dict
vocabulary invariant.

Run: python -m unittest tests.test_chart_catalog_invariant -v
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import re
import unittest

from dsx.checks.viz import BANNED_TYPES

_ROOT = pathlib.Path(__file__).resolve().parents[1]
_CATALOG = _ROOT / "references" / "chart-catalog.md"
_VOCAB_INVARIANT = _ROOT / "tests" / "test_viz_vocabulary_invariant.py"

# The same fenced-json parse the input-type inventory uses (scripts/gen-input-types.py:
# re.search(r"```json\s*(\{.*?\})\s*```", text, re.S)) — DOTALL + lazy, so it captures
# the single json object regardless of CRLF line endings.
_JSON_BLOCK = re.compile(r"```json\s*(\{.*?\})\s*```", re.S)

# The eight HQ-27 still-unverified items and the two never-submitted heuristic
# sources. None may back a shipped catalog citation. Tokens are chosen to catch
# only the unverified forms, never the verified citations actually used (FT VV,
# Wilke §5.6, Cleveland & McGill 1984, Munzner ch.6, Tufte 1983, Duan et al. 2023,
# Muth 2018, Few 2006, Jacob Harris 2011).
_FORBIDDEN_CITATION_TOKENS = (
    "abela",
    "graph selection matrix",
    "mackinlay",
    "few 2013",
    "information graphics",  # R.L. Harris 1999 (distinct from Jacob Harris 2011)
    "cardinality",           # Munzner "cardinality" — the unverified item
)


def _load_mark_universe():
    """Load tests/test_viz_vocabulary_invariant.py by path and return its live
    _mark_universe() — the single source of truth for the admissible mark set,
    not a re-transcribed copy. Same importlib idiom that module uses for its own
    hyphenated sibling script; exec is side-effect-free (module body only defines
    classes and helpers)."""
    spec = importlib.util.spec_from_file_location("viz_vocab_invariant", _VOCAB_INVARIANT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module._mark_universe()


def _load_payload() -> dict:
    text = _CATALOG.read_text(encoding="utf-8")
    match = _JSON_BLOCK.search(text)
    assert match is not None, "no fenced ```json payload found in chart-catalog.md"
    return json.loads(match.group(1))


class TestChartCatalogInvariant(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = _load_payload()
        cls.rows = cls.payload["rows"]
        cls.ranks = cls.payload["perceptual_ranks"]
        cls.universe = _load_mark_universe()

    # (a) band
    def test_row_count_in_band(self):
        self.assertTrue(75 <= len(self.rows) <= 90, f"row count {len(self.rows)} outside 75-90")

    # (b) three-axes-plus-citation shape
    def test_every_row_has_three_axes_and_a_citation(self):
        allowed_flags = {"dsx_admissible", "reference_only", "refusal"}
        for row in self.rows:
            name = row.get("mark") or row.get("name")
            with self.subTest(name):
                for field in ("function", "data_signature", "perceptual_channel", "citation"):
                    self.assertTrue(str(row.get(field, "")).strip(), f"{name}.{field} is empty")
                self.assertIn(row.get("flag"), allowed_flags, f"{name} has bad flag {row.get('flag')!r}")

    # (c) catalog <-> vocabulary conformance, both directions
    def test_admissible_rows_set_equal_the_live_universe(self):
        adm = [r["mark"] for r in self.rows if r["flag"] == "dsx_admissible"]
        self.assertEqual(len(adm), len(set(adm)), f"duplicate dsx_admissible mark: {sorted(adm)}")
        self.assertEqual(
            set(adm), set(self.universe),
            "dsx_admissible rows must set-equal _mark_universe() exactly "
            f"(missing={sorted(set(self.universe) - set(adm))}, "
            f"extra={sorted(set(adm) - set(self.universe))})",
        )

    # (d) refusal drift guard against live BANNED_TYPES
    def test_refusal_rows_are_exactly_the_live_banned_types(self):
        refusal = [r for r in self.rows if r["flag"] == "refusal"]
        self.assertEqual(len(refusal), 7, "there must be exactly seven refusal rows")
        banned = {r["banned_type"] for r in refusal}
        self.assertEqual(banned, set(BANNED_TYPES), "refusal banned_types must equal live BANNED_TYPES")
        for row in refusal:
            bt = row["banned_type"]
            with self.subTest(bt):
                self.assertIn(bt, BANNED_TYPES, f"{bt} is not a live BANNED_TYPES key")
                self.assertEqual(
                    row["banning_code"], BANNED_TYPES[bt]["code"],
                    f"{bt} banning_code must equal the live code {BANNED_TYPES[bt]['code']}",
                )

    # (e) reference-only isolation
    def test_reference_only_rows_are_outside_the_admissible_universe(self):
        for row in self.rows:
            if row["flag"] != "reference_only":
                continue
            name = row.get("name") or row.get("mark")
            with self.subTest(name):
                self.assertNotIn(
                    name, self.universe,
                    f"reference_only row {name!r} is in the admissible universe — it would widen the gate",
                )

    # (f) perceptual tie-break structural criterion (D-1, pure ordering, no computation)
    def test_perceptual_tie_break_structural_criterion(self):
        self.assertNotIn("density", self.ranks, "density is absent from the 1984 paper — must not appear")
        # length and angle share rank 3 — a tie asserted both ways, never a strict <
        self.assertEqual(self.ranks["length"], self.ranks["angle"], "length and angle must be tied")
        self.assertLessEqual(self.ranks["length"], self.ranks["angle"])
        self.assertLessEqual(self.ranks["angle"], self.ranks["length"])
        # the monotone chain, using <= throughout (ties are legal, strict jumps are not required)
        chain = ["position_common", "position_nonaligned", "length", "area", "volume", "shading"]
        for lo, hi in zip(chain, chain[1:]):
            self.assertLessEqual(self.ranks[lo], self.ranks[hi], f"rank({lo}) must be <= rank({hi})")
        # every row's channel is a defined rank
        for row in self.rows:
            name = row.get("mark") or row.get("name")
            with self.subTest(name):
                self.assertIn(
                    row["perceptual_channel"], self.ranks,
                    f"{name} channel {row['perceptual_channel']!r} is not a perceptual_ranks key",
                )

    # (g) citation traceability — negative guard against off-limits sources
    def test_no_citation_draws_on_a_forbidden_source(self):
        blob = " ".join(str(r.get("citation", "")) for r in self.rows).lower()
        for token in _FORBIDDEN_CITATION_TOKENS:
            with self.subTest(token):
                self.assertNotIn(token, blob, f"forbidden citation token present: {token!r}")

    # (h) non-vacuity guard
    def test_non_vacuity_anchors_present(self):
        self.assertGreaterEqual(len(self.rows), 60, "catalog collapsed — conformance would pass vacuously")
        admissible = {r["mark"] for r in self.rows if r["flag"] == "dsx_admissible"}
        for anchor in ("bar", "line", "scatter", "error_bars"):
            self.assertIn(anchor, admissible, f"anchor mark {anchor!r} missing from dsx_admissible rows")


if __name__ == "__main__":
    unittest.main()
