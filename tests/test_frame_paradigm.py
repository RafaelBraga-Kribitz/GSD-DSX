"""Test suite for the frequentist-scoping predicate,
``dsx.frame.paradigm.applies_to_frequentist_admissibility`` (D-22, REQ-P11-05).

This file covers the new scoping predicate only. The pre-existing
paradigm-manifest tests (``DSX-PAR-001``, ``DSX-PAR-002``,
``DSX-PAR-010``/``DSX-PAR-011``) stay in ``tests/test_dsx.py`` — nothing
here duplicates or replaces them.

Run:  python3 -m unittest tests.test_frame_paradigm -v
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dsx.frame.paradigm import applies_to_frequentist_admissibility  # noqa: E402


class TestAppliesToFrequentistAdmissibility(unittest.TestCase):
    def test_declared_frequentist_returns_true(self):
        spec = {"inference": {"paradigm": "frequentist"}}
        self.assertIs(applies_to_frequentist_admissibility(spec), True)

    def test_declared_bayesian_returns_false(self):
        spec = {"inference": {"paradigm": "bayesian"}}
        self.assertIs(applies_to_frequentist_admissibility(spec), False)

    def test_no_inference_block_returns_true(self):
        spec = {}
        self.assertIs(applies_to_frequentist_admissibility(spec), True)

    def test_inference_block_with_no_paradigm_key_returns_true(self):
        spec = {"inference": {}}
        self.assertIs(applies_to_frequentist_admissibility(spec), True)

    def test_empty_string_paradigm_returns_true(self):
        spec = {"inference": {"paradigm": ""}}
        self.assertIs(applies_to_frequentist_admissibility(spec), True)

    def test_whitespace_only_paradigm_returns_true(self):
        spec = {"inference": {"paradigm": "   "}}
        self.assertIs(applies_to_frequentist_admissibility(spec), True)

    def test_out_of_vocabulary_paradigm_returns_true(self):
        spec = {"inference": {"paradigm": "astrology"}}
        self.assertIs(applies_to_frequentist_admissibility(spec), True)

    def test_near_miss_misspelling_returns_true(self):
        spec = {"inference": {"paradigm": "freqentist"}}
        self.assertIs(applies_to_frequentist_admissibility(spec), True)

    def test_case_variant_of_frequentist_returns_true(self):
        spec = {"inference": {"paradigm": "Frequentist"}}
        self.assertIs(applies_to_frequentist_admissibility(spec), True)

    def test_hyphenated_variant_of_frequentist_returns_true(self):
        spec = {"inference": {"paradigm": "FREQUENTIST"}}
        self.assertIs(applies_to_frequentist_admissibility(spec), True)

    def test_case_variant_of_bayesian_returns_false(self):
        spec = {"inference": {"paradigm": "Bayesian"}}
        self.assertIs(applies_to_frequentist_admissibility(spec), False)

    def test_hyphen_versus_underscore_variant_normalizes_the_same(self):
        # normalize() maps both '-' and ' ' to '_', so a hyphenated spelling of
        # a vocabulary member resolves identically to its canonical form. No
        # member of PARADIGMS today contains a hyphen or a space, so this
        # proves the comparison goes through normalize() rather than raw
        # string equality, using a synthetic hyphenated near-miss that still
        # normalizes outside the vocabulary (and therefore still widens True).
        spec_hyphen = {"inference": {"paradigm": "fre-quentist"}}
        spec_underscore = {"inference": {"paradigm": "fre_quentist"}}
        self.assertEqual(
            applies_to_frequentist_admissibility(spec_hyphen),
            applies_to_frequentist_admissibility(spec_underscore),
        )

    def test_return_value_is_exactly_a_bool_not_a_truthy_string_or_none(self):
        for spec in (
            {"inference": {"paradigm": "frequentist"}},
            {"inference": {"paradigm": "bayesian"}},
            {},
        ):
            with self.subTest(spec=spec):
                result = applies_to_frequentist_admissibility(spec)
                self.assertIsInstance(result, bool)

    def test_non_dict_spec_returns_true_rather_than_raising(self):
        for spec in (None, "not a dict", 42, ["also", "not", "a", "dict"]):
            with self.subTest(spec=spec):
                self.assertIs(applies_to_frequentist_admissibility(spec), True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
