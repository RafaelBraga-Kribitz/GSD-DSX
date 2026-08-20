"""Test suite for dsx/frame/prereg.py — DSX-PRE-010 (declared fallback rule does not
resolve to exactly one branch), DSX-PRE-020 (recorded plan-time content lock differs
from verify-time bytes) and DSX-PRE-030 (executed procedure differs from the declared
branch). Stdlib unittest — no pytest dependency.

Run:  python3 -m unittest tests.test_frame_prereg -v
"""

from __future__ import annotations

import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dsx.loader import load  # noqa: E402
from dsx.spec import PREREG_FACTS, as_number, describe_vocabulary, get  # noqa: E402


class TestFactRegistry(unittest.TestCase):
    def test_prereg_facts_has_exactly_three_members(self):
        self.assertEqual(
            PREREG_FACTS,
            {
                "alpha": "design.alpha",
                "comparisons_looked_at": "results.comparisons_looked_at",
                "interim_looks": "results.interim_looks",
            },
        )

    def test_every_registry_fact_resolves_to_a_number_in_the_good_fixture(self):
        spec = load(str(ROOT / "examples" / "good-ANALYSIS-SPEC.yaml"))
        for name, path in PREREG_FACTS.items():
            with self.subTest(fact=name, path=path):
                value = get(spec, path)
                number = as_number(value)
                self.assertIsNotNone(
                    number,
                    f"{name} ({path}) must resolve to a number in the good fixture, "
                    f"got {value!r}",
                )

    def test_describe_vocabulary_prereg_facts_matches_registry_sorted(self):
        vocab = describe_vocabulary()
        self.assertIn("prereg_facts", vocab)
        self.assertEqual(vocab["prereg_facts"], PREREG_FACTS)
        self.assertEqual(list(vocab["prereg_facts"]), sorted(vocab["prereg_facts"]))

    def test_observed_n_is_not_a_registry_member_because_it_is_a_list(self):
        self.assertNotIn(
            "observed_n",
            PREREG_FACTS,
            "results.observed_n is a list of per-arm counts in the fixture, not a "
            "scalar, so it is deliberately excluded from PREREG_FACTS (D-04)",
        )
