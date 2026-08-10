"""The IT001-IT040 input-type catalogue and the chart lookup built on it."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from dsx.checks.viz import check as viz_check
from dsx.findings import Severity
from dsx.input_types import (
    UnknownShape,
    canonical_id,
    family_of,
    input_types,
    permitted,
)
from dsx.spec import CHART_CAPABILITIES, DATA_INPUT_TYPES

ROOT = Path(__file__).resolve().parents[1]


class CatalogueIntegrity(unittest.TestCase):
    def test_forty_entries_numbered_it001_to_it040(self):
        ids = [item["id"] for item in input_types()]
        self.assertEqual(ids, [f"IT{n:03d}" for n in range(1, 41)])

    def test_every_family_is_a_known_data_input_type(self):
        for item in input_types():
            with self.subTest(item["id"]):
                self.assertIn(item["family"], DATA_INPUT_TYPES)
                self.assertIn(item["family"], CHART_CAPABILITIES)

    def test_every_entry_permits_at_least_one_mark(self):
        for item in input_types():
            with self.subTest(item["id"]):
                self.assertTrue(item["admissible"])

    def test_verbatim_fields_survive_generation(self):
        """The generated JSON must not have rewritten the inventory's content."""
        source = (ROOT / "references" / "input-type-inventory.md").read_text(
            encoding="utf-8", errors="replace"
        )
        start = source.index("```json") + len("```json")
        end = source.index("```", start)
        original = {i["id"]: i for i in json.loads(source[start:end])["input_types"]}

        for item in input_types():
            with self.subTest(item["id"]):
                for field in ("name", "signature", "columns", "example", "use_for", "pattern_code"):
                    self.assertEqual(item[field], original[item["id"]][field])


class Lookup(unittest.TestCase):
    def test_canonical_id_normalises_common_spellings(self):
        for raw in ("IT007", "it007", "it7", "IT-007", " it_7 "):
            with self.subTest(raw):
                self.assertEqual(canonical_id(raw), "IT007")

    def test_canonical_id_rejects_out_of_range_and_non_ids(self):
        for raw in ("IT041", "IT000", "composition", "", "bar"):
            with self.subTest(raw):
                self.assertIsNone(canonical_id(raw))

    def test_family_lookup(self):
        self.assertEqual(family_of("IT005"), "categorical-value")
        self.assertEqual(family_of("IT017"), "financial-ohlc")
        self.assertIsNone(family_of("composition"))

    def test_permitted_accepts_both_it_id_and_family(self):
        self.assertEqual(permitted("IT007"), permitted("composition"))

    def test_relationship_narrows_when_intersection_is_non_empty(self):
        wide = permitted("IT005")
        narrow = permitted("IT005", "comparison")
        self.assertTrue(set(narrow) < set(wide))
        self.assertIn("bar", narrow)
        self.assertNotIn("pie", narrow)

    def test_empty_intersection_falls_back_to_the_shape_set(self):
        # composition marks and comparison marks do not overlap.
        self.assertEqual(permitted("IT007", "comparison"), permitted("IT007"))

    def test_unknown_shape_raises(self):
        with self.assertRaises(UnknownShape):
            permitted("IT099")
        with self.assertRaises(UnknownShape):
            permitted("not-a-family")

    def test_lookup_is_deterministic(self):
        self.assertEqual(permitted("IT012"), permitted("IT012"))
        self.assertEqual(permitted("IT012"), sorted(permitted("IT012")))


class Gate(unittest.TestCase):
    def _spec(self, chart_type: str, shape: str) -> dict:
        return {
            "visuals": [
                {
                    "name": "test chart",
                    "relationship": "comparison",
                    "type": chart_type,
                    "data_input_type": shape,
                }
            ]
        }

    def _findings(self, spec: dict, code: str) -> list:
        report = viz_check(spec)
        return [f for f in report.findings if f.code == code]

    def test_gate_rejects_a_mark_the_shape_forbids(self):
        found = self._findings(self._spec("candlestick", "IT005"), "DSX-VIZ-013")
        self.assertEqual(len(found), 1)
        self.assertEqual(Severity.parse(found[0].severity), Severity.parse("HIGH"))

    def test_rejection_states_the_permitted_marks(self):
        found = self._findings(self._spec("candlestick", "IT005"), "DSX-VIZ-013")
        detail = found[0].detail
        for mark in permitted("IT005"):
            self.assertIn(mark, detail)

    def test_gate_admits_a_mark_the_shape_permits(self):
        self.assertEqual(self._findings(self._spec("bar", "IT005"), "DSX-VIZ-013"), [])

    def test_unknown_it_id_is_reported_not_silently_admitted(self):
        found = self._findings(self._spec("bar", "IT099"), "DSX-VIZ-013")
        self.assertEqual(len(found), 1)

    def test_coarse_family_names_still_work(self):
        self.assertEqual(self._findings(self._spec("bar", "categorical-value"), "DSX-VIZ-013"), [])


if __name__ == "__main__":
    unittest.main()
