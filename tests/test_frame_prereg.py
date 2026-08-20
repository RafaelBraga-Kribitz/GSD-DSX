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

from dsx.findings import CheckError  # noqa: E402
from dsx.frame import prereg  # noqa: E402
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


class TestFallbackRuleParsing(unittest.TestCase):
    def test_prose_with_no_arrow_returns_none(self):
        self.assertIsNone(
            prereg._parse_fallback_rule(
                "If the variance estimate is unstable, use a bootstrap"
            )
        )

    def test_non_string_and_blank_inputs_return_none_without_raising(self):
        for value in ("", None, 3):
            with self.subTest(value=value):
                self.assertIsNone(prereg._parse_fallback_rule(value))

    def test_worked_example_parses_with_annotation_discarded(self):
        rule = prereg._parse_fallback_rule(
            "if clusters < 30 -> wild cluster bootstrap, 9999 reps, seed 42"
        )
        self.assertEqual(rule.fact, "clusters")
        self.assertEqual(rule.op, "<")
        self.assertEqual(rule.threshold, 30.0)
        self.assertEqual(rule.branch, "wild cluster bootstrap")

    def test_leading_if_is_optional(self):
        rule = prereg._parse_fallback_rule("interim_looks >= 2 -> obrien_fleming")
        self.assertEqual(rule.fact, "interim_looks")
        self.assertEqual(rule.op, ">=")
        self.assertEqual(rule.threshold, 2.0)
        self.assertEqual(rule.branch, "obrien_fleming")

    def test_all_six_operators_parse_without_mis_splitting_two_char_forms(self):
        cases = {
            "<": "clusters < 30 -> a",
            "<=": "clusters <= 30 -> a",
            ">": "clusters > 30 -> a",
            ">=": "clusters >= 30 -> a",
            "==": "clusters == 30 -> a",
            "!=": "clusters != 30 -> a",
        }
        for op, text in cases.items():
            with self.subTest(op=op):
                rule = prereg._parse_fallback_rule(text)
                self.assertEqual(rule.op, op)
                self.assertEqual(rule.threshold, 30.0)

    def test_negative_and_decimal_thresholds_parse(self):
        rule_alpha = prereg._parse_fallback_rule("alpha <= 0.01 -> a")
        self.assertEqual(rule_alpha.threshold, 0.01)
        rule_effect = prereg._parse_fallback_rule("effect > -1.5 -> a")
        self.assertEqual(rule_effect.threshold, -1.5)

    def test_empty_left_hand_side_raises_check_error(self):
        with self.assertRaises(CheckError) as ctx:
            prereg._parse_fallback_rule("-> wild cluster bootstrap")
        message = str(ctx.exception)
        self.assertIn("<fact> <op> <number> -> <branch>", message)

    def test_prose_condition_raises_check_error(self):
        with self.assertRaises(CheckError) as ctx:
            prereg._parse_fallback_rule("if clusters is small -> bootstrap")
        message = str(ctx.exception)
        self.assertIn("clusters is small", message)
        self.assertIn("<fact> <op> <number> -> <branch>", message)

    def test_arrow_with_no_branch_label_raises_check_error(self):
        for text in ("if clusters < 30 ->", "if clusters < 30 -> , 9999 reps"):
            with self.subTest(text=text):
                with self.assertRaises(CheckError) as ctx:
                    prereg._parse_fallback_rule(text)
                self.assertIn("<fact> <op> <number> -> <branch>", str(ctx.exception))

    def test_check_error_messages_name_offending_text_and_expected_form(self):
        with self.assertRaises(CheckError) as ctx:
            prereg._parse_fallback_rule("if clusters is small -> bootstrap")
        message = str(ctx.exception)
        self.assertIn("clusters is small", message)
        self.assertIn("<fact> <op> <number> -> <branch>", message)

    def test_crlf_and_trailing_newline_parse_identically_to_lf(self):
        lf = prereg._parse_fallback_rule(
            "if clusters < 30 -> wild cluster bootstrap, 9999 reps, seed 42"
        )
        crlf = prereg._parse_fallback_rule(
            "if clusters < 30 -> wild cluster bootstrap, 9999 reps, seed 42\r\n"
        )
        trailing_newline = prereg._parse_fallback_rule(
            "if clusters < 30 -> wild cluster bootstrap, 9999 reps, seed 42\n"
        )
        self.assertEqual(lf, crlf)
        self.assertEqual(lf, trailing_newline)


class TestBranchResolution(unittest.TestCase):
    def test_no_arrow_rule_resolves_to_primary_procedure_with_no_reason(self):
        spec = {
            "inference": {
                "primary_procedure": "two_proportion_z",
                "fallback_rule": "Use a bootstrap if the variance is unstable.",
            },
        }
        resolution = prereg._resolve_branch(spec)
        self.assertEqual(resolution.source, "primary_procedure")
        self.assertEqual(resolution.branch, "two_proportion_z")
        self.assertIsNone(resolution.reason)

    def test_missing_or_non_dict_inference_resolves_to_unresolved_no_raise(self):
        for spec in (
            {},
            {"inference": "not a dict"},
            {"inference": None},
            {"inference": []},
            {"inference": 3},
        ):
            with self.subTest(spec=spec):
                resolution = prereg._resolve_branch(spec)
                self.assertEqual(resolution.source, "unresolved")
                self.assertIsNone(resolution.branch)
                self.assertIsNone(resolution.reason)

    def test_true_condition_resolves_to_the_rule_branch(self):
        spec = {
            "inference": {
                "primary_procedure": "two_proportion_z",
                "fallback_rule": "interim_looks >= 1 -> alpha_spending_obf",
            },
            "results": {"interim_looks": 1},
        }
        resolution = prereg._resolve_branch(spec)
        self.assertEqual(resolution.source, "fallback_rule")
        self.assertEqual(resolution.branch, "alpha_spending_obf")
        self.assertIsNone(resolution.reason)

    def test_false_condition_resolves_to_primary_procedure(self):
        spec = {
            "inference": {
                "primary_procedure": "two_proportion_z",
                "fallback_rule": "interim_looks >= 1 -> alpha_spending_obf",
            },
            "results": {"interim_looks": 0},
        }
        resolution = prereg._resolve_branch(spec)
        self.assertEqual(resolution.source, "primary_procedure")
        self.assertEqual(resolution.branch, "two_proportion_z")
        self.assertIsNone(resolution.reason)

    def test_fact_outside_registry_resolves_unresolved_naming_accepted_names(self):
        spec = {
            "inference": {
                "primary_procedure": "two_proportion_z",
                "fallback_rule": "clusters < 30 -> wild cluster bootstrap",
            },
        }
        resolution = prereg._resolve_branch(spec)
        self.assertEqual(resolution.source, "unresolved")
        self.assertIsNone(resolution.branch)
        self.assertIn("clusters", resolution.reason)
        for name in ("alpha", "comparisons_looked_at", "interim_looks"):
            with self.subTest(name=name):
                self.assertIn(name, resolution.reason)

    def test_registry_fact_absent_from_spec_resolves_unresolved(self):
        spec = {
            "inference": {
                "primary_procedure": "two_proportion_z",
                "fallback_rule": "alpha < 0.01 -> x",
            },
        }
        resolution = prereg._resolve_branch(spec)
        self.assertEqual(resolution.source, "unresolved")
        self.assertIsNone(resolution.branch)
        self.assertIn("alpha", resolution.reason)
        self.assertIn("design.alpha", resolution.reason)

    def test_registry_fact_non_numeric_resolves_unresolved(self):
        spec = {
            "inference": {
                "primary_procedure": "two_proportion_z",
                "fallback_rule": "alpha < 0.01 -> x",
            },
            "design": {"alpha": "tbd"},
        }
        resolution = prereg._resolve_branch(spec)
        self.assertEqual(resolution.source, "unresolved")
        self.assertIsNone(resolution.branch)
        self.assertIn("alpha", resolution.reason)
        self.assertIn("design.alpha", resolution.reason)

    def test_resolution_is_identical_across_paradigms_true_and_false(self):
        def make_spec(paradigm: str, interim_looks: int) -> dict:
            return {
                "inference": {
                    "paradigm": paradigm,
                    "primary_procedure": "two_proportion_z",
                    "fallback_rule": "interim_looks >= 1 -> alpha_spending_obf",
                },
                "results": {"interim_looks": interim_looks},
            }

        freq_true = prereg._resolve_branch(make_spec("frequentist", 1))
        bayes_true = prereg._resolve_branch(make_spec("bayesian", 1))
        self.assertEqual(freq_true, bayes_true)

        freq_false = prereg._resolve_branch(make_spec("frequentist", 0))
        bayes_false = prereg._resolve_branch(make_spec("bayesian", 0))
        self.assertEqual(freq_false, bayes_false)

    def test_branch_label_returned_as_authored_not_normalized(self):
        spec = {
            "inference": {
                "primary_procedure": "two_proportion_z",
                "fallback_rule": "interim_looks >= 1 -> Wild Cluster Bootstrap",
            },
            "results": {"interim_looks": 1},
        }
        resolution = prereg._resolve_branch(spec)
        self.assertEqual(resolution.branch, "Wild Cluster Bootstrap")
