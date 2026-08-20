"""Test suite for dsx/frame/prereg.py — DSX-PRE-010 (declared fallback rule does not
resolve to exactly one branch), DSX-PRE-020 (recorded plan-time content lock differs
from verify-time bytes) and DSX-PRE-030 (executed procedure differs from the declared
branch). Stdlib unittest — no pytest dependency.

Run:  python3 -m unittest tests.test_frame_prereg -v
"""

from __future__ import annotations

import copy
import io
import json
import re
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from _trail_seed import seed_plan_header  # noqa: E402
from dsx import __version__  # noqa: E402
from dsx import cli  # noqa: E402
from dsx.decisions import InvocationHeader  # noqa: E402
from dsx.decisions import append as append_decision  # noqa: E402
from dsx.decisions import decisions_path, frame_digest  # noqa: E402
from dsx.findings import CheckError, Report, Severity  # noqa: E402
from dsx.frame import prereg  # noqa: E402
from dsx.loader import load  # noqa: E402
from dsx.spec import PREREG_FACTS, as_number, describe_vocabulary, get  # noqa: E402
from dsx.suppressions import known_codes  # noqa: E402


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


class TestRuleResolutionFindings(unittest.TestCase):
    # D-05: DSX-PRE-010
    def test_rule_naming_a_fact_outside_the_registry_fires_naming_it_and_the_accepted_names(self):
        spec = {
            "inference": {
                "primary_procedure": "two_proportion_z",
                "fallback_rule": "clusters < 30 -> wild cluster bootstrap",
            },
        }
        report = prereg.check(spec)
        findings = [f for f in report.findings if f.code == "DSX-PRE-010"]
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, Severity.CRITICAL)
        self.assertIn("clusters", findings[0].detail)
        for name in ("alpha", "comparisons_looked_at", "interim_looks"):
            with self.subTest(name=name):
                self.assertIn(name, findings[0].detail)

    def test_rule_naming_an_undeclared_registry_fact_fires_naming_the_dotted_path(self):
        spec = {
            "inference": {
                "primary_procedure": "two_proportion_z",
                "fallback_rule": "alpha < 0.01 -> alpha_spending_obf",
            },
        }
        report = prereg.check(spec)
        findings = [f for f in report.findings if f.code == "DSX-PRE-010"]
        self.assertEqual(len(findings), 1)
        self.assertIn("design.alpha", findings[0].detail)

    def test_good_fixture_produces_zero_dsx_pre_010_findings(self):
        spec = load(str(ROOT / "examples" / "good-ANALYSIS-SPEC.yaml"))
        report = prereg.check(spec)
        findings = [f for f in report.findings if f.code == "DSX-PRE-010"]
        self.assertEqual(findings, [])

    def test_cleanly_resolving_rule_produces_zero_dsx_pre_010_findings(self):
        spec = {
            "inference": {
                "primary_procedure": "two_proportion_z",
                "fallback_rule": "interim_looks >= 1 -> alpha_spending_obf",
            },
            "results": {"interim_looks": 1},
        }
        report = prereg.check(spec)
        findings = [f for f in report.findings if f.code == "DSX-PRE-010"]
        self.assertEqual(findings, [])

    def test_unparseable_arrow_bearing_rule_raises_check_error_not_a_finding(self):
        spec = {
            "inference": {
                "primary_procedure": "two_proportion_z",
                "fallback_rule": "if clusters is small -> bootstrap",
            },
        }
        with self.assertRaises(CheckError):
            prereg.check(spec)

    def test_check_appends_one_decision_record_for_dsx_pre_010_fired_and_clear(self):
        fired_spec = {
            "inference": {
                "primary_procedure": "two_proportion_z",
                "fallback_rule": "clusters < 30 -> wild cluster bootstrap",
            },
        }
        fired_report = prereg.check(fired_spec)
        fired_decisions = fired_report.context.get("decisions") or []
        self.assertEqual(len(fired_decisions), 1)
        self.assertEqual(fired_decisions[0]["layer"], "deterministic")
        self.assertTrue(fired_decisions[0]["counterfactual"].strip())

        clear_spec = {
            "inference": {
                "primary_procedure": "two_proportion_z",
                "fallback_rule": "interim_looks >= 1 -> alpha_spending_obf",
            },
            "results": {"interim_looks": 1},
        }
        clear_report = prereg.check(clear_spec)
        clear_decisions = clear_report.context.get("decisions") or []
        self.assertEqual(len(clear_decisions), 1)
        self.assertTrue(clear_decisions[0]["counterfactual"].strip())

    def test_check_returns_empty_report_for_non_dict_spec(self):
        report = prereg.check("not a dict")
        self.assertIsInstance(report, Report)
        self.assertEqual(report.findings, [])


class TestProcedureReconciliation(unittest.TestCase):
    # D-05: DSX-PRE-030
    def test_branch_mismatch_fires_naming_both_labels(self):
        spec = {
            "inference": {
                "primary_procedure": "two_proportion_z",
                "fallback_rule": "interim_looks >= 1 -> wild_cluster_bootstrap",
            },
            "results": {"interim_looks": 1},
            "analysis": {"test": "two_proportion_z"},
        }
        report = prereg.check(spec)
        findings = [f for f in report.findings if f.code == "DSX-PRE-030"]
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, Severity.CRITICAL)
        self.assertIn("wild_cluster_bootstrap", findings[0].detail)
        self.assertIn("two_proportion_z", findings[0].detail)

    def test_detail_names_the_source_of_each_label(self):
        spec = {
            "inference": {
                "primary_procedure": "two_proportion_z",
                "fallback_rule": "interim_looks >= 1 -> wild_cluster_bootstrap",
            },
            "results": {"interim_looks": 1},
            "analysis": {"test": "two_proportion_z"},
        }
        report = prereg.check(spec)
        findings = [f for f in report.findings if f.code == "DSX-PRE-030"]
        self.assertEqual(len(findings), 1)
        self.assertIn("fallback_rule", findings[0].detail)
        self.assertIn("analysis.test", findings[0].detail)

    def test_spacing_and_hyphenation_difference_alone_produces_zero_findings(self):
        spec = {
            "inference": {
                "primary_procedure": "two_proportion_z",
                "fallback_rule": "interim_looks >= 1 -> wild cluster bootstrap",
            },
            "results": {"interim_looks": 1},
            "analysis": {"test": "wild-cluster-bootstrap"},
        }
        report = prereg.check(spec)
        findings = [f for f in report.findings if f.code == "DSX-PRE-030"]
        self.assertEqual(findings, [])

    def test_good_fixture_produces_zero_dsx_pre_030_findings(self):
        spec = load(str(ROOT / "examples" / "good-ANALYSIS-SPEC.yaml"))
        report = prereg.check(spec)
        findings = [f for f in report.findings if f.code == "DSX-PRE-030"]
        self.assertEqual(findings, [])

    def test_unresolved_rule_produces_no_dsx_pre_030(self):
        spec = {
            "inference": {
                "primary_procedure": "two_proportion_z",
                "fallback_rule": "clusters < 30 -> wild_cluster_bootstrap",
            },
            "analysis": {"test": "something_else"},
        }
        report = prereg.check(spec)
        pre010 = [f for f in report.findings if f.code == "DSX-PRE-010"]
        pre030 = [f for f in report.findings if f.code == "DSX-PRE-030"]
        self.assertEqual(len(pre010), 1)
        self.assertEqual(pre030, [])

    def test_blank_or_missing_executed_procedure_produces_no_dsx_pre_030(self):
        for analysis_block in (None, {}, {"test": ""}, {"test": "   "}):
            with self.subTest(analysis_block=analysis_block):
                spec = {
                    "inference": {
                        "primary_procedure": "two_proportion_z",
                        "fallback_rule": "interim_looks >= 1 -> wild_cluster_bootstrap",
                    },
                    "results": {"interim_looks": 1},
                }
                if analysis_block is not None:
                    spec["analysis"] = analysis_block
                report = prereg.check(spec)
                pre030 = [f for f in report.findings if f.code == "DSX-PRE-030"]
                self.assertEqual(pre030, [])

    def test_decision_record_appended_fired_and_clear(self):
        fired_spec = {
            "inference": {
                "primary_procedure": "two_proportion_z",
                "fallback_rule": "interim_looks >= 1 -> wild_cluster_bootstrap",
            },
            "results": {"interim_looks": 1},
            "analysis": {"test": "two_proportion_z"},
        }
        fired_report = prereg.check(fired_spec)
        fired_pre030_decisions = [
            d for d in (fired_report.context.get("decisions") or [])
            if d["choice"].startswith("DSX-PRE-030")
        ]
        self.assertEqual(len(fired_pre030_decisions), 1)
        self.assertTrue(fired_pre030_decisions[0]["counterfactual"].strip())

        clear_spec = {
            "inference": {
                "primary_procedure": "two_proportion_z",
                "fallback_rule": "interim_looks >= 1 -> wild cluster bootstrap",
            },
            "results": {"interim_looks": 1},
            "analysis": {"test": "wild-cluster-bootstrap"},
        }
        clear_report = prereg.check(clear_spec)
        clear_pre030_decisions = [
            d for d in (clear_report.context.get("decisions") or [])
            if d["choice"].startswith("DSX-PRE-030")
        ]
        self.assertEqual(len(clear_pre030_decisions), 1)
        self.assertTrue(clear_pre030_decisions[0]["counterfactual"].strip())


class TestNoMeritConsultation(unittest.TestCase):
    def test_strictly_more_conservative_substitute_still_blocks(self):
        # two_proportion_z declared, fishers_exact executed — fishers_exact is the
        # strictly more conservative substitute (exact test vs. a normal
        # approximation). A more conservative substitution is still a substitution.
        spec = {
            "inference": {
                "primary_procedure": "welch_t",
                "fallback_rule": "interim_looks >= 1 -> two_proportion_z",
            },
            "results": {"interim_looks": 1},
            "analysis": {"test": "fishers_exact"},
        }
        report = prereg.check(spec)
        findings = [f for f in report.findings if f.code == "DSX-PRE-030"]
        self.assertEqual(
            len(findings),
            1,
            "a more conservative substitution is still a substitution",
        )

    def test_firing_is_symmetric_in_the_direction_of_the_swap(self):
        # Same pair, values swapped: fishers_exact declared, two_proportion_z
        # executed (strictly less conservative substitute). Same code, same
        # severity — the check consults no merit ordering in either direction.
        spec = {
            "inference": {
                "primary_procedure": "welch_t",
                "fallback_rule": "interim_looks >= 1 -> fishers_exact",
            },
            "results": {"interim_looks": 1},
            "analysis": {"test": "two_proportion_z"},
        }
        report = prereg.check(spec)
        findings = [f for f in report.findings if f.code == "DSX-PRE-030"]
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, Severity.CRITICAL)


class TestMalformedShapesDegradeGracefully(unittest.TestCase):
    def test_non_dict_spec_returns_empty_report_no_raise(self):
        for bad_spec in ("not a dict", [], None, 3):
            with self.subTest(bad_spec=bad_spec):
                report = prereg.check(bad_spec)
                self.assertIsInstance(report, Report)
                self.assertEqual(report.findings, [])

    def test_malformed_inference_block_degrades_no_findings(self):
        for bad_inference in ("not a dict", [], None, 3):
            with self.subTest(bad_inference=bad_inference):
                spec = {"inference": bad_inference}
                report = prereg.check(spec)
                pre_findings = [f for f in report.findings if f.code.startswith("DSX-PRE-")]
                self.assertEqual(pre_findings, [])

    def test_malformed_analysis_block_produces_no_dsx_pre_030_no_raise(self):
        for bad_analysis in ("not a dict", [], None, 3):
            with self.subTest(bad_analysis=bad_analysis):
                spec = {
                    "inference": {
                        "primary_procedure": "two_proportion_z",
                        "fallback_rule": "interim_looks >= 1 -> wild_cluster_bootstrap",
                    },
                    "results": {"interim_looks": 1},
                    "analysis": bad_analysis,
                }
                report = prereg.check(spec)
                pre030 = [f for f in report.findings if f.code == "DSX-PRE-030"]
                self.assertEqual(pre030, [])

    def test_non_string_fallback_rule_produces_no_finding_no_exception(self):
        for bad_rule in ([], {}, 3, None):
            with self.subTest(bad_rule=bad_rule):
                spec = {
                    "inference": {
                        "primary_procedure": "two_proportion_z",
                        "fallback_rule": bad_rule,
                    },
                }
                report = prereg.check(spec)
                pre_findings = [f for f in report.findings if f.code.startswith("DSX-PRE-")]
                self.assertEqual(pre_findings, [])


class TestParadigmIndependence(unittest.TestCase):
    """Test 5 (behavioural) is the primary proof; test 6 (source-level) is the
    corroborating one. A source-level grep proves only that a string is absent
    today; the behavioural comparison proves the property the requirement
    actually cares about, and survives a refactor that reads the field
    indirectly. Mirrors REQ-P7-09 and REQ-P8-06, which Phase 10 has no numbered
    requirement for but which 10-CONTEXT.md's locked-upstream section says
    should ship anyway.
    """

    def _scenarios(self):
        return {
            "clear": {
                "inference": {
                    "primary_procedure": "two_proportion_z",
                    "fallback_rule": "interim_looks >= 1 -> wild_cluster_bootstrap",
                },
                "results": {"interim_looks": 1},
                "analysis": {"test": "wild_cluster_bootstrap"},
            },
            "dsx_pre_010_fired": {
                "inference": {
                    "primary_procedure": "two_proportion_z",
                    "fallback_rule": "clusters < 30 -> wild_cluster_bootstrap",
                },
            },
            "dsx_pre_030_fired": {
                "inference": {
                    "primary_procedure": "welch_t",
                    "fallback_rule": "interim_looks >= 1 -> two_proportion_z",
                },
                "results": {"interim_looks": 1},
                "analysis": {"test": "fishers_exact"},
            },
            # No "inference:" block at all — there is nothing to declare a
            # paradigm into, so both variants below are the same spec by
            # construction. The property under test holds trivially and
            # unconditionally for this scenario, and it still exercises the
            # same comparison harness as the other three.
            "no_inference_block": {
                "results": {"interim_looks": 1},
                "analysis": {"test": "two_proportion_z"},
            },
        }

    def test_finding_sequences_identical_across_paradigms(self):
        for name, base in self._scenarios().items():
            variants = {}
            for paradigm in ("frequentist", "bayesian"):
                spec = copy.deepcopy(base)
                if "inference" in spec:
                    spec["inference"]["paradigm"] = paradigm
                variants[paradigm] = spec

            with self.subTest(scenario=name):
                freq_report = prereg.check(variants["frequentist"])
                bayes_report = prereg.check(variants["bayesian"])

                freq_signature = [
                    (f.code, f.severity, f.detail) for f in freq_report.findings
                ]
                bayes_signature = [
                    (f.code, f.severity, f.detail) for f in bayes_report.findings
                ]
                self.assertEqual(freq_signature, bayes_signature)

    def test_source_contains_no_attribute_access_to_paradigm_field(self):
        source = Path(prereg.__file__).read_text(encoding="utf-8")
        # Tolerate CRLF: the repository checks out with carriage returns.
        normalized = source.replace("\r\n", "\n")
        # The attribute-access form, not the bare word "paradigm" — the module
        # docstring and _resolve_branch's docstring legitimately mention the
        # concept in prose ("inferential paradigm field"); the concern is code
        # reading the field, not English describing why it never does.
        access_pattern = re.compile(r'''["']paradigm["']''')
        self.assertEqual(
            access_pattern.findall(normalized),
            [],
            "dsx/frame/prereg.py contains a quoted 'paradigm' key/string access",
        )


class TestMissingPlanHeader(unittest.TestCase):
    """`_check_content_lock`'s missing-plan-header guard (Task 1): a trail with no
    recorded `plan`-gate-point header stops the run at exit 2 (`CheckError`) rather
    than passing silently, and names the M-07 grandfather route so a pre-v2.0.0 spec
    stays walkable."""

    def _spec(self):
        return {"inference": {"declared_at": "pre_data"}}

    def test_1_reconcile_false_with_no_trail_file_produces_no_findings_no_exception(self):
        with tempfile.TemporaryDirectory() as root:
            report = prereg.check(self._spec(), root, reconcile_trail=False)
            self.assertIsInstance(report, Report)
            self.assertEqual(report.findings, [])

    def test_2_reconcile_true_with_no_trail_file_raises_check_error(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(CheckError):
                prereg.check(self._spec(), root, reconcile_trail=True)

    def test_3_trail_with_no_plan_header_raises_check_error(self):
        with tempfile.TemporaryDirectory() as root:
            target = decisions_path(root)
            for point in ("execute", "verify", "ship"):
                append_decision(
                    target,
                    InvocationHeader(
                        invocation_id=f"INV-{point}",
                        gate_point=point,
                        dsx_version=__version__,
                        frame_digest="deadbeef",
                    ),
                )
            with self.assertRaises(CheckError):
                prereg.check(self._spec(), root, reconcile_trail=True)

    def test_4_message_names_suppressions_and_authority_and_trail_path(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(CheckError) as ctx:
                prereg.check(self._spec(), root, reconcile_trail=True)
            message = str(ctx.exception)
            self.assertIn("suppressions", message)
            self.assertIn("authority", message)
            self.assertIn(str(decisions_path(root)), message)

    def test_5_message_states_gate_plan_has_never_run(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(CheckError) as ctx:
                prereg.check(self._spec(), root, reconcile_trail=True)
            message = str(ctx.exception)
            self.assertIn("dsx gate plan", message)
            self.assertIn("never run", message)

    def test_6_trail_with_a_plan_header_raises_no_check_error(self):
        with tempfile.TemporaryDirectory() as root:
            target = decisions_path(root)
            append_decision(
                target,
                InvocationHeader(
                    invocation_id="INV-0001",
                    gate_point="plan",
                    dsx_version=__version__,
                    frame_digest="deadbeef",
                ),
            )
            report = prereg.check(self._spec(), root, reconcile_trail=True)
            self.assertIsInstance(report, Report)

    def test_7_corrupt_trail_lines_treated_as_no_headers_raises_check_error(self):
        with tempfile.TemporaryDirectory() as root:
            target = decisions_path(root)
            target.write_text("not json\n{also not json\n", encoding="utf-8")
            with self.assertRaises(CheckError):
                prereg.check(self._spec(), root, reconcile_trail=True)

    def test_8_root_none_with_reconcile_true_raises_check_error_not_type_error(self):
        with self.assertRaises(CheckError) as ctx:
            prereg.check(self._spec(), None, reconcile_trail=True)
        message = str(ctx.exception)
        self.assertIn("suppressions", message)
        self.assertIn("dsx gate plan", message)

    def test_9_message_names_dsx_pre_020_explicitly(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(CheckError) as ctx:
                prereg.check(self._spec(), root, reconcile_trail=True)
            message = str(ctx.exception)
            self.assertIn("DSX-PRE-020", message)

    def _spec_with_suppression(self, code="DSX-PRE-020", reason="predates the plan gate", authority="ADR-999"):
        row = {}
        if code is not None:
            row["code"] = code
        if reason is not None:
            row["reason"] = reason
        if authority is not None:
            row["authority"] = authority
        spec = self._spec()
        spec["suppressions"] = [row]
        return spec

    def test_10_usable_dsx_pre_020_suppression_unlocks_the_missing_header_route(self):
        """CR-01: a suppressions[] row naming DSX-PRE-020 with a reason and an
        authority is the real grandfather route — no CheckError, no finding."""
        with tempfile.TemporaryDirectory() as root:
            report = prereg.check(
                self._spec_with_suppression(), root, reconcile_trail=True
            )
            self.assertIsInstance(report, Report)
            self.assertEqual(report.findings, [])

    def test_11_suppression_missing_reason_does_not_unlock(self):
        with tempfile.TemporaryDirectory() as root:
            spec = self._spec_with_suppression(reason="")
            with self.assertRaises(CheckError):
                prereg.check(spec, root, reconcile_trail=True)

    def test_12_suppression_missing_authority_does_not_unlock(self):
        with tempfile.TemporaryDirectory() as root:
            spec = self._spec_with_suppression(authority="")
            with self.assertRaises(CheckError):
                prereg.check(spec, root, reconcile_trail=True)

    def test_13_suppression_naming_a_different_code_does_not_unlock(self):
        with tempfile.TemporaryDirectory() as root:
            spec = self._spec_with_suppression(code="DSX-PRE-010")
            with self.assertRaises(CheckError):
                prereg.check(spec, root, reconcile_trail=True)

    def test_14_unknown_suppression_code_still_aborts_even_with_a_usable_grandfather_row(self):
        """The property CR-01 requires still hold: an unknown code anywhere in
        suppressions[] still aborts the run at exit 2 — that happens later, in
        apply_suppressions, once the early return here lets execution continue
        that far."""
        from dsx.cli import run_checks

        spec = self._spec_with_suppression()
        spec["suppressions"].append(
            {"code": "DSX-FAKE-999", "reason": "typo", "authority": "ADR-1"}
        )
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(CheckError):
                run_checks(
                    spec,
                    ("prereg",),
                    root,
                    gate_point="verify",
                    resolve_root=root,
                    gate_invocation=True,
                )


class TestContentLockReconciliation(unittest.TestCase):
    """`_check_content_lock`'s DSX-PRE-020 reconciliation (Task 2): a `pre_data`
    claim whose current frame content was never registered at plan blocks at
    CRITICAL; `post_data` and an absent claim stay legal and silent; the comparison
    is set membership over every recorded plan-gate-point digest."""

    def _append_plan_header(self, root, digest, invocation_id="INV-0001"):
        append_decision(
            decisions_path(root),
            InvocationHeader(
                invocation_id=invocation_id,
                gate_point="plan",
                dsx_version=__version__,
                frame_digest=digest,
            ),
        )

    def test_1_matching_digest_produces_no_finding(self):
        spec = {"validity_frame": {"a": 1}, "inference": {"declared_at": "pre_data"}}
        with tempfile.TemporaryDirectory() as root:
            self._append_plan_header(root, frame_digest(spec))
            report = prereg.check(spec, root, reconcile_trail=True)
            findings = [f for f in report.findings if f.code == "DSX-PRE-020"]
            self.assertEqual(findings, [])

    # D-05: DSX-PRE-020
    def test_2_mismatching_digest_fires_exactly_one_critical_finding(self):
        spec = {"validity_frame": {"a": 1}, "inference": {"declared_at": "pre_data"}}
        with tempfile.TemporaryDirectory() as root:
            self._append_plan_header(root, "not-the-real-digest")
            report = prereg.check(spec, root, reconcile_trail=True)
            findings = [f for f in report.findings if f.code == "DSX-PRE-020"]
            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0].severity, Severity.CRITICAL)

    def test_3_post_data_with_mismatching_trail_produces_no_finding(self):
        spec = {"validity_frame": {"a": 1}, "inference": {"declared_at": "post_data"}}
        with tempfile.TemporaryDirectory() as root:
            self._append_plan_header(root, "not-the-real-digest")
            report = prereg.check(spec, root, reconcile_trail=True)
            findings = [f for f in report.findings if f.code == "DSX-PRE-020"]
            self.assertEqual(findings, [])

    def test_4_declared_at_absent_with_mismatching_trail_produces_no_finding(self):
        spec = {"validity_frame": {"a": 1}, "inference": {}}
        with tempfile.TemporaryDirectory() as root:
            self._append_plan_header(root, "not-the-real-digest")
            report = prereg.check(spec, root, reconcile_trail=True)
            findings = [f for f in report.findings if f.code == "DSX-PRE-020"]
            self.assertEqual(findings, [])

    def test_5_membership_holds_regardless_of_append_order(self):
        # The matching digest is appended FIRST and the non-matching digest LAST —
        # the ordering a most-recent rule would fail on (it would compare against
        # the non-matching digest and fire a false positive on a spec that did
        # nothing wrong). Set membership is indifferent to append order.
        spec = {"validity_frame": {"a": 1}, "inference": {"declared_at": "pre_data"}}
        with tempfile.TemporaryDirectory() as root:
            self._append_plan_header(root, frame_digest(spec), invocation_id="INV-0001")
            self._append_plan_header(
                root, "a-different-digest-appended-last", invocation_id="INV-0002"
            )
            report = prereg.check(spec, root, reconcile_trail=True)
            findings = [f for f in report.findings if f.code == "DSX-PRE-020"]
            self.assertEqual(
                findings,
                [],
                "membership must hold even when the non-matching digest is "
                "appended last — the ordering a most-recent rule would fail on",
            )

    def test_6_edit_outside_frame_blocks_does_not_change_digest(self):
        base = {"validity_frame": {"a": 1}, "inference": {"declared_at": "pre_data"}}
        spec_a = dict(base, title="Spec A")
        spec_b = dict(base, title="Spec B")
        self.assertEqual(frame_digest(spec_a), frame_digest(spec_b))
        with tempfile.TemporaryDirectory() as root:
            self._append_plan_header(root, frame_digest(spec_a))
            report = prereg.check(spec_b, root, reconcile_trail=True)
            findings = [f for f in report.findings if f.code == "DSX-PRE-020"]
            self.assertEqual(findings, [])

    def test_7_detail_and_remedy_name_recorded_count_digest_and_known_limit(self):
        spec = {"validity_frame": {"a": 1}, "inference": {"declared_at": "pre_data"}}
        current_digest = frame_digest(spec)
        with tempfile.TemporaryDirectory() as root:
            self._append_plan_header(root, "mismatch-one", invocation_id="INV-0001")
            self._append_plan_header(root, "mismatch-two", invocation_id="INV-0002")
            report = prereg.check(spec, root, reconcile_trail=True)
            findings = [f for f in report.findings if f.code == "DSX-PRE-020"]
            self.assertEqual(len(findings), 1)
            finding = findings[0]
            self.assertIn("2", finding.detail)
            self.assertIn(current_digest[:12], finding.detail)
            self.assertIn("dsx gate plan", finding.remedy)
            self.assertIn("re-running", finding.remedy)

    def test_8_decision_record_appended_fired_and_clear(self):
        fired_spec = {
            "validity_frame": {"a": 1}, "inference": {"declared_at": "pre_data"}
        }
        with tempfile.TemporaryDirectory() as root:
            self._append_plan_header(root, "mismatch")
            fired_report = prereg.check(fired_spec, root, reconcile_trail=True)
            fired_decisions = [
                d for d in (fired_report.context.get("decisions") or [])
                if d["choice"].startswith("DSX-PRE-020")
            ]
            self.assertEqual(len(fired_decisions), 1)

        clear_spec = {
            "validity_frame": {"a": 1}, "inference": {"declared_at": "pre_data"}
        }
        with tempfile.TemporaryDirectory() as root:
            self._append_plan_header(root, frame_digest(clear_spec))
            clear_report = prereg.check(clear_spec, root, reconcile_trail=True)
            clear_decisions = [
                d for d in (clear_report.context.get("decisions") or [])
                if d["choice"].startswith("DSX-PRE-020")
            ]
            self.assertEqual(len(clear_decisions), 1)


class TestGateRegistration(unittest.TestCase):
    """ROADMAP Success Criterion 5's pair for `prereg` (plan 04, Task 2):
    `prereg` is registered at verify and ship only, and every `DSX-PRE-` code
    is reachable from a gate profile — mirroring
    `tests/test_frame_interference.py`'s `TestGateRegistration` with the
    present/absent point sets inverted."""

    def test_prereg_registered_in_verify_ship_absent_from_plan_and_execute(self):
        from dsx.cli import CHECKS, GATE_PROFILES

        self.assertIs(CHECKS["prereg"], prereg.check)
        for point in ("verify", "ship"):
            with self.subTest(point=point):
                self.assertIn("prereg", GATE_PROFILES[point])
        for point in ("plan", "execute"):
            with self.subTest(point=point):
                self.assertNotIn("prereg", GATE_PROFILES[point])

    def test_every_dsx_pre_code_reachable_from_a_gate_profile(self):
        from dsx.cli import GATE_PROFILES

        pre_codes = [c for c in known_codes() if c.startswith("DSX-PRE-")]
        self.assertTrue(
            pre_codes,
            "expected at least DSX-PRE-010, DSX-PRE-020 and DSX-PRE-030 to be known",
        )
        reachable_checks: "set[str]" = set().union(*GATE_PROFILES.values())
        self.assertIn("prereg", reachable_checks)

    def test_known_dsx_pre_codes_are_exactly_010_020_030(self):
        pre_codes = {c for c in known_codes() if c.startswith("DSX-PRE-")}
        self.assertEqual(
            pre_codes,
            {"DSX-PRE-010", "DSX-PRE-020", "DSX-PRE-030"},
            "brief D-06 makes finding-code numbering irreversible; DSX-PRE-011 was "
            "deliberately left unspent for a case where the remedy for an unknown "
            "fact genuinely diverges from the remedy for an unresolvable rule "
            "(10-CONTEXT D-12) — getting the count of known DSX-PRE- codes wrong "
            "here is worse than getting the digits wrong, because a silent drift "
            "in the count would mean a future code shipped without a reader ever "
            "confronting the numbering decision this test exists to pin.",
        )

    def test_every_dsx_pre_finding_this_module_can_emit_is_critical(self):
        # A HIGH DSX-PRE code would still exit 1 at verify and ship, and would
        # still fail the known-bad corpus classifier (tests/test_known_bad_corpus.py
        # line 176's severity == "CRITICAL" filter) — severity is not redundant
        # with registration here, it is what makes the corpus classification
        # meaningful once the code fires.
        scenarios = {
            "DSX-PRE-010": {
                "inference": {
                    "primary_procedure": "two_proportion_z",
                    "fallback_rule": "clusters < 30 -> wild cluster bootstrap",
                },
            },
            "DSX-PRE-030": {
                "inference": {
                    "primary_procedure": "two_proportion_z",
                    "fallback_rule": "interim_looks >= 1 -> wild_cluster_bootstrap",
                },
                "results": {"interim_looks": 1},
                "analysis": {"test": "two_proportion_z"},
            },
        }
        for code, spec in scenarios.items():
            with self.subTest(code=code):
                report = prereg.check(spec)
                findings = [f for f in report.findings if f.code == code]
                self.assertEqual(len(findings), 1, f"{code} did not fire as expected")
                self.assertEqual(
                    findings[0].severity, Severity.CRITICAL,
                    f"{code} must be CRITICAL — a HIGH finding would still exit 1 at "
                    "verify/ship and still fail the known-bad corpus classifier, so "
                    "severity is not redundant with registration",
                )

        pre_020_spec = {"validity_frame": {"a": 1}, "inference": {"declared_at": "pre_data"}}
        with tempfile.TemporaryDirectory() as root:
            append_decision(
                decisions_path(root),
                InvocationHeader(
                    invocation_id="INV-0001",
                    gate_point="plan",
                    dsx_version=__version__,
                    frame_digest="not-the-real-digest",
                ),
            )
            report = prereg.check(pre_020_spec, root, reconcile_trail=True)
            findings = [f for f in report.findings if f.code == "DSX-PRE-020"]
            self.assertEqual(len(findings), 1, "DSX-PRE-020 did not fire as expected")
            self.assertEqual(
                findings[0].severity, Severity.CRITICAL,
                "DSX-PRE-020 must be CRITICAL — a HIGH finding would still exit 1 at "
                "verify/ship and still fail the known-bad corpus classifier, so "
                "severity is not redundant with registration",
            )


class TestAdHocCommandScope(unittest.TestCase):
    """Pins the boundary between a real gate invocation and a read-only
    inspection command (plan 04, Task 3; see the plan's "Settled decision:
    which invocations reconcile the trail" section).

    The trail-dependent half of `prereg` runs only for a real `dsx gate
    verify` or `dsx gate ship` invocation; `dsx audit` and `dsx check` are
    read-only inspection commands that never call `_write_decision_trail`
    (`dsx/cli.py::cmd_audit`, `cmd_check`), so requiring a trail from them
    would create a precondition no sequence of commands could satisfy — an
    availability failure disguised as a control. This does not soften the
    rule at the gate: tests 3 and 4 assert the exit-2 block directly, in the
    same trail-free directory that tests 1 and 2 pass in.
    """

    def _run(self, argv: "list[str]") -> "tuple[int, str, str]":
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(argv)
        return code, out.getvalue(), err.getvalue()

    def _write_spec(self, tmp: str, **field_overrides: dict) -> Path:
        """Clone the good fixture into `tmp`, applying the given top-level
        block overrides (dict-merged onto the existing block), so the spec
        is otherwise complete and no unrelated defect crashes the ad-hoc
        commands under test. Written as JSON regardless of the .yaml suffix,
        matching the precedent at tests/test_frame_val.py's
        `_write_identification_variant`."""
        spec = load(str(ROOT / "examples" / "good-ANALYSIS-SPEC.yaml"))
        for key, value in field_overrides.items():
            block = spec.setdefault(key, {})
            if isinstance(value, dict) and isinstance(block, dict):
                block.update(value)
            else:
                spec[key] = value
        path = Path(tmp) / "ANALYSIS-SPEC.yaml"
        path.write_text(json.dumps(spec), encoding="utf-8")
        return path

    def test_1_dsx_audit_in_a_trail_free_directory_exits_without_check_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_spec(tmp)
            code, out, err = self._run(
                ["audit", "--spec", str(path), "--phase-dir", tmp, "--json"]
            )
            self.assertIn(code, (0, 1), f"unexpected exit code {code}: {err}")
            payload = json.loads(out or err)
            self.assertIn("findings", payload)

    def test_2_dsx_check_in_a_trail_free_directory_exits_without_check_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_spec(tmp)
            code, out, err = self._run(
                ["check", "--spec", str(path), "--phase-dir", tmp, "--json"]
            )
            self.assertIn(code, (0, 1), f"unexpected exit code {code}: {err}")
            payload = json.loads(out or err)
            self.assertIn("findings", payload)

    def test_3_dsx_gate_verify_in_the_same_trail_free_directory_exits_2_naming_suppressions(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_spec(tmp)
            code, _out, err = self._run(["gate", "verify", "--spec", str(path), "--phase-dir", tmp])
            self.assertEqual(code, 2)
            self.assertIn("suppressions", err)

    def test_4_dsx_gate_ship_in_the_same_trail_free_directory_also_exits_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_spec(tmp)
            code, _out, err = self._run(["gate", "ship", "--spec", str(path), "--phase-dir", tmp])
            self.assertEqual(code, 2)
            self.assertIn("suppressions", err)

    def test_5_dsx_audit_still_reports_dsx_pre_030_for_a_switched_procedure(self):
        # The trail-independent half (rule resolution, procedure reconciliation)
        # runs everywhere, including a read-only inspection command — scoping the
        # trail half narrows nothing except the trail half.
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_spec(tmp, analysis={"test": "one_proportion_z"})
            code, out, err = self._run(
                ["audit", "--spec", str(path), "--phase-dir", tmp, "--json"]
            )
            self.assertNotEqual(code, 2, f"dsx audit unexpectedly errored: {err}")
            payload = json.loads(out or err)
            codes_seen = {f["code"] for f in payload["findings"]}
            self.assertIn("DSX-PRE-030", codes_seen)

    def test_6_after_seeding_a_plan_header_dsx_gate_verify_no_longer_exits_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_spec(tmp)
            seed_plan_header(tmp, path)
            code, _out, err = self._run(["gate", "verify", "--spec", str(path), "--phase-dir", tmp])
            self.assertNotEqual(code, 2, f"gate verify still errored after seeding: {err}")


def _normalize_whitespace(text: str) -> str:
    """Collapse every run of whitespace, including the carriage returns this
    repository checks out on Windows, to a single space, so a substring check
    against a sentence that wraps across lines does not depend on line endings."""
    return " ".join(text.split())


class TestDocumentedLimits(unittest.TestCase):
    """ROADMAP Success Criterion 4 has a README half that correct code does not
    satisfy on its own: the finding remedies in ``dsx/frame/prereg.py`` (plans 02
    and 03) are only half of REQ-P10-02. A substring assertion is the only part
    of that documentation half a machine can hold — it proves the sentences this
    plan wrote into ``README.md`` still exist, not that a human reads them as
    honest limits rather than a boast. That reading is a human judgement, carried
    on the phase's manual-verification list, not decided here.
    """

    @classmethod
    def setUpClass(cls):
        cls.readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
        cls.readme_normalized = _normalize_whitespace(cls.readme_text)
        cls.prereg_source = (ROOT / "dsx" / "frame" / "prereg.py").read_text(
            encoding="utf-8"
        )
        cls.prereg_source_normalized = _normalize_whitespace(cls.prereg_source)

    # D-05: DSX-PRE-010
    def test_1_known_limits_heading_precedes_declared_at(self):
        self.assertIn(
            "## Known limits",
            self.readme_text,
            "README.md must carry the `## Known limits` heading",
        )
        heading_index = self.readme_text.index("## Known limits")
        self.assertIn(
            "declared_at",
            self.readme_text[heading_index:],
            "the literal `declared_at` must appear under `## Known limits`",
        )

    def test_2_declared_at_stated_as_an_unverifiable_self_declaration(self):
        self.assertIn(
            "operator self-declaration that the tool cannot verify",
            self.readme_normalized,
            "README.md must state that `declared_at` is an operator "
            "self-declaration the tool cannot verify",
        )

    def test_3_analysis_test_named_as_plan_time_scaffolding(self):
        self.assertIn(
            "analysis.test",
            self.readme_text,
            "README.md must name `analysis.test` as the executed-side field",
        )
        self.assertIn(
            "scaffolded into the specification at plan time",
            self.readme_normalized,
            "README.md must state that `analysis.test` is scaffolded at plan time",
        )

    def test_4_states_no_ordering_is_enforced_between_gate_points(self):
        self.assertIn(
            "nothing in the code enforces an ordering between the four gate points",
            self.readme_normalized,
            "README.md must state that nothing enforces an ordering between gate "
            "points",
        )

    def test_5_every_prereg_fact_is_named_in_the_readme(self):
        # Derived from PREREG_FACTS itself, never hard-coded — a registry member
        # added without documentation must fail this test.
        for name in sorted(PREREG_FACTS):
            with self.subTest(fact=name):
                self.assertIn(
                    name,
                    self.readme_text,
                    f"README.md must name the prereg fact {name!r}, sourced from "
                    "PREREG_FACTS",
                )

    def test_6_dsx_pre_030_remedy_states_a_more_conservative_substitute_still_blocks(
        self,
    ):
        # Drives a real DSX-PRE-030 firing rather than reading the source text —
        # the remedy is what an operator actually sees.
        spec = {
            "inference": {
                "primary_procedure": "welch_t",
                "fallback_rule": "interim_looks >= 1 -> two_proportion_z",
            },
            "results": {"interim_looks": 1},
            "analysis": {"test": "fishers_exact"},
        }
        report = prereg.check(spec)
        findings = [f for f in report.findings if f.code == "DSX-PRE-030"]
        self.assertEqual(len(findings), 1)
        self.assertIn(
            "more conservative substituted procedure still blocks",
            findings[0].remedy,
            "the DSX-PRE-030 remedy and the README must agree on the "
            "more-conservative-substitute limit",
        )

    def test_7_dsx_pre_020_remedy_states_the_re_running_limit(self):
        # Drives a real DSX-PRE-020 firing, same reasoning as test 6.
        spec = {"validity_frame": {"a": 1}, "inference": {"declared_at": "pre_data"}}
        with tempfile.TemporaryDirectory() as root:
            append_decision(
                decisions_path(root),
                InvocationHeader(
                    invocation_id="INV-0001",
                    gate_point="plan",
                    dsx_version=__version__,
                    frame_digest="not-the-real-digest",
                ),
            )
            report = prereg.check(spec, root, reconcile_trail=True)
        findings = [f for f in report.findings if f.code == "DSX-PRE-020"]
        self.assertEqual(len(findings), 1)
        self.assertIn(
            "nothing in the code enforces an ordering between the four gate points",
            findings[0].remedy,
            "the DSX-PRE-020 remedy and the README must agree on the "
            "re-running limit",
        )

    def test_8_the_two_gelman_and_loken_locator_flags_are_still_present(self):
        # A future editor tidying these into confident locators must fail this
        # test — both flags exist to stop a fabricated locator, not to be tidied.
        self.assertIn(
            "no numbered sections, tables or theorems",
            self.prereg_source_normalized,
            "dsx/frame/prereg.py must still flag that the article carries no "
            "numbered sections, tables or theorems",
        )
        self.assertIn(
            "unpublished 2013 Columbia working paper",
            self.prereg_source_normalized,
            "dsx/frame/prereg.py must still flag the unpublished 2013 Columbia "
            "working paper as a notation source only",
        )
