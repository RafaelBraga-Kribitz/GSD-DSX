"""Hermetic profiler depth tests (Phase 25).

Reference-value, determinism, and pre-existing-key golden tests for the
additive `columns[<col>].numeric` / `columns[<col>].categorical` blocks.
Stdlib unittest only — no pytest dependency.

Run:  python.exe -m unittest tests.test_profiler_hermetic -v
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dsx.profiler import _categorical_block, _numeric_block, profile_csv  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "profiler"


class TestNumericBlock(unittest.TestCase):
    def test_1_to_10_reference_values(self):
        block = _numeric_block([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(block["min"], 1)
        self.assertEqual(block["q1"], 3.25)
        self.assertEqual(block["median"], 5.5)
        self.assertEqual(block["q3"], 7.75)
        self.assertEqual(block["max"], 10)
        self.assertEqual(block["mean"], 5.5)
        self.assertEqual(block["sd"], 3.0276503540974917)
        self.assertEqual(block["n_zero"], 0)
        self.assertEqual(block["n_negative"], 0)
        self.assertEqual(block["n"], 10)

    def test_median_matches_statistics_median(self):
        import statistics

        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        block = _numeric_block(values)
        self.assertEqual(block["median"], statistics.median(values))

    def test_zeros_and_negatives(self):
        block = _numeric_block([-2.0, -0.0, 0.0, 0.0, 5])
        self.assertEqual(block["n_negative"], 1)
        self.assertEqual(block["n_zero"], 3)
        self.assertEqual(block["min"], -2.0)
        self.assertEqual(block["max"], 5)
        self.assertEqual(block["n"], 5)

    def test_empty(self):
        block = _numeric_block([])
        for key in ("min", "q1", "median", "q3", "max", "mean", "sd"):
            self.assertIsNone(block[key], key)
        self.assertEqual(block["n_zero"], 0)
        self.assertEqual(block["n_negative"], 0)
        self.assertEqual(block["n"], 0)

    def test_single_value(self):
        block = _numeric_block([7])
        for key in ("min", "max", "q1", "median", "q3", "mean"):
            self.assertEqual(block[key], 7, key)
        self.assertIsNone(block["sd"])
        self.assertEqual(block["n_zero"], 0)
        self.assertEqual(block["n_negative"], 0)
        self.assertEqual(block["n"], 1)

    def test_through_profile_csv_numeric_1_10(self):
        profile = profile_csv(FIXTURES / "numeric_1_10.csv")
        numeric = profile["columns"]["value"]["numeric"]
        self.assertEqual(numeric["min"], 1)
        self.assertEqual(numeric["q1"], 3.25)
        self.assertEqual(numeric["median"], 5.5)
        self.assertEqual(numeric["q3"], 7.75)
        self.assertEqual(numeric["max"], 10)
        self.assertEqual(numeric["mean"], 5.5)
        self.assertEqual(numeric["sd"], 3.0276503540974917)
        self.assertEqual(numeric["n_zero"], 0)
        self.assertEqual(numeric["n_negative"], 0)
        self.assertEqual(numeric["n"], 10)
        # D-01 append order: numeric is the LAST key in columns.value, after dtype.
        keys = list(profile["columns"]["value"].keys())
        self.assertEqual(keys, ["null_rate", "n_unique", "dtype", "numeric"])

    def test_numeric_key_absent_for_string_dtype(self):
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "strings.csv"
            csv_path.write_text("level\nA\nB\nA\n", encoding="utf-8")
            profile = profile_csv(csv_path)
            self.assertNotIn("numeric", profile["columns"]["level"])


class TestCategoricalBlock(unittest.TestCase):
    def test_abcde_reference_values(self):
        profile = profile_csv(FIXTURES / "categorical_abcde.csv")
        cat = profile["columns"]["level"]["categorical"]
        self.assertEqual(cat["share_top1"], 0.5)
        self.assertEqual(cat["share_top10"], 1.0)
        self.assertEqual(cat["rare_share"], 0.05)
        self.assertEqual(cat["n_singleton"], 1)
        # D-01 append order: categorical is the LAST key in columns.level, after dtype.
        keys = list(profile["columns"]["level"].keys())
        self.assertEqual(keys, ["null_rate", "n_unique", "dtype", "categorical"])

    def test_percent_arm_boundary(self):
        # N=20000, one level ("rare") has 15 rows: 15 >= 10 but 15/20000 = 0.00075 < 0.001,
        # so it must still be counted as rare (the OR is on count<10 OR share<0.001).
        profile = profile_csv(FIXTURES / "categorical_percent_arm.csv")
        cat = profile["columns"]["level"]["categorical"]
        self.assertAlmostEqual(cat["rare_share"], 15 / 20000)

    def test_top10_tie_boundary_count_desc_then_string_asc(self):
        # Levels a..i carry counts 15..7 (sum=109); "m" and "n" both have count 5, with
        # "n" appearing FIRST in CSV row order. The frozen tie-break (count desc, then
        # level string asc) puts "m" in the top-10 and "n" out — a Counter.most_common()
        # insertion-order tie-break would wrongly include "n" instead. N=119 total.
        profile = profile_csv(FIXTURES / "categorical_top10_tie.csv")
        cat = profile["columns"]["level"]["categorical"]
        self.assertAlmostEqual(cat["share_top10"], (109 + 5) / 119)

    def test_empty_counter(self):
        block = _categorical_block(Counter())
        self.assertIsNone(block["share_top1"])
        self.assertIsNone(block["share_top10"])
        self.assertIsNone(block["rare_share"])
        self.assertEqual(block["n_singleton"], 0)

    def test_categorical_key_absent_for_numeric_dtype(self):
        profile = profile_csv(FIXTURES / "numeric_1_10.csv")
        self.assertNotIn("categorical", profile["columns"]["value"])


if __name__ == "__main__":
    unittest.main()
