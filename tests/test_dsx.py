"""Test suite for dsx. Stdlib unittest — no pytest dependency.

Run:  python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import io
import json
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _trail_seed import seed_plan_header  # noqa: E402
from dsx import cli, mathx  # noqa: E402
from dsx.checks import claims, design, metrics, ml, repro, stats, viz  # noqa: E402
from dsx.findings import Report, Severity  # noqa: E402
from dsx.frame import interference  # noqa: E402
from dsx.loader import SpecParseError, _parse_yaml_subset, loads  # noqa: E402
from dsx.spec import PEEKING_POLICIES, describe_vocabulary, validate_structure  # noqa: E402


def codes(report: Report) -> set[str]:
    return {f.code for f in report.findings}


# ── mathx ────────────────────────────────────────────────────────────────────


class TestMath(unittest.TestCase):
    def test_norm_ppf_reference_values(self):
        for p, expected in ((0.975, 1.959964), (0.95, 1.644854), (0.80, 0.841621),
                            (0.99, 2.326348), (0.5, 0.0)):
            self.assertAlmostEqual(mathx.norm_ppf(p), expected, places=5, msg=f"p={p}")

    def test_norm_ppf_inverts_cdf(self):
        for x in (-3.0, -1.0, 0.0, 0.5, 2.5):
            self.assertAlmostEqual(mathx.norm_ppf(mathx.norm_cdf(x)), x, places=8)

    def test_chi2_sf_reference_values(self):
        # Critical values at alpha=0.05
        self.assertAlmostEqual(mathx.chi2_sf(3.841459, 1), 0.05, places=5)
        self.assertAlmostEqual(mathx.chi2_sf(5.991465, 2), 0.05, places=5)
        self.assertAlmostEqual(mathx.chi2_sf(16.918978, 9), 0.05, places=5)

    def test_sample_size_matches_reference(self):
        # p1=0.31, p2=0.33, alpha=.05 two-sided, power=.80 -> ~8.5k per arm
        n = mathx.sample_size_two_proportions(0.31, 0.02, 0.05, 0.80)
        self.assertTrue(8000 < n < 9200, n)

    def test_power_and_sample_size_are_consistent(self):
        n = mathx.sample_size_two_proportions(0.20, 0.03, 0.05, 0.80)
        achieved = mathx.power_two_proportions(0.20, 0.03, n, 0.05)
        self.assertGreaterEqual(achieved, 0.80)
        just_under = mathx.power_two_proportions(0.20, 0.03, n - 200, 0.05)
        self.assertLess(just_under, achieved)

    def test_mde_inverts_sample_size(self):
        n = mathx.sample_size_two_proportions(0.25, 0.05, 0.05, 0.80)
        detectable = mathx.mde_two_proportions(0.25, n, 0.05, 0.80)
        self.assertAlmostEqual(detectable, 0.05, places=2)

    def test_more_power_needs_more_sample(self):
        self.assertGreater(
            mathx.sample_size_two_proportions(0.3, 0.02, 0.05, 0.90),
            mathx.sample_size_two_proportions(0.3, 0.02, 0.05, 0.80),
        )

    def test_smaller_mde_needs_more_sample(self):
        self.assertGreater(
            mathx.sample_size_two_proportions(0.3, 0.01, 0.05, 0.80),
            mathx.sample_size_two_proportions(0.3, 0.04, 0.05, 0.80),
        )

    def test_srm_detects_imbalance(self):
        _, p_balanced, _ = mathx.srm_test([10000, 10020], [0.5, 0.5])
        self.assertGreater(p_balanced, 0.05)
        _, p_broken, _ = mathx.srm_test([10000, 9400], [0.5, 0.5])
        self.assertLess(p_broken, 0.001)

    def test_srm_normalizes_ratio(self):
        a = mathx.srm_test([100, 100], [1, 1])
        b = mathx.srm_test([100, 100], [0.5, 0.5])
        self.assertAlmostEqual(a[1], b[1])

    def test_bonferroni_and_holm(self):
        p = [0.01, 0.04, 0.03]
        adj_b, _ = mathx.bonferroni(p, 0.05)
        self.assertAlmostEqual(adj_b[0], 0.03)
        adj_h, rej_h = mathx.holm(p, 0.05)
        self.assertTrue(adj_h[0] <= adj_h[2] <= adj_h[1])  # monotone in rank order
        self.assertTrue(all(h <= b + 1e-12 for h, b in zip(adj_h, adj_b)))

    def test_benjamini_hochberg_is_monotone_and_less_strict(self):
        p = [0.001, 0.008, 0.039, 0.041, 0.042]
        adj, rejected = mathx.benjamini_hochberg(p, 0.05)
        self.assertTrue(all(adj[i] <= adj[i + 1] + 1e-12 for i in range(len(adj) - 1)))
        adj_bonf, _ = mathx.bonferroni(p, 0.05)
        self.assertTrue(all(a <= b + 1e-12 for a, b in zip(adj, adj_bonf)))
        self.assertTrue(rejected[0])

    def test_peeking_inflation_increases(self):
        self.assertAlmostEqual(mathx.inflation_from_peeking(1), 0.05)
        self.assertGreater(mathx.inflation_from_peeking(5), mathx.inflation_from_peeking(2))
        self.assertLess(mathx.inflation_from_peeking(10), 0.30)

    def test_obrien_fleming_tightens_early(self):
        self.assertGreater(mathx.obrien_fleming_boundary(1, 4), mathx.obrien_fleming_boundary(4, 4))
        self.assertAlmostEqual(mathx.obrien_fleming_boundary(4, 4), mathx.z_two_sided(0.05), places=9)

    def test_cohens_h_and_d(self):
        self.assertAlmostEqual(mathx.cohens_h(0.5, 0.5), 0.0)
        self.assertGreater(mathx.cohens_h(0.3, 0.5), 0)
        self.assertAlmostEqual(mathx.cohens_d(0.0, 1.0, 1.0, 1.0, 30, 30), 1.0, places=6)
        self.assertEqual(mathx.interpret_effect("d", 0.05), "negligible")
        self.assertEqual(mathx.interpret_effect("d", 1.2), "large")

    def test_invalid_inputs_raise(self):
        with self.assertRaises(ValueError):
            mathx.norm_ppf(1.5)
        with self.assertRaises(ValueError):
            mathx.sample_size_two_proportions(1.5, 0.02)
        with self.assertRaises(ValueError):
            mathx.apply_correction("nope", [0.1])
        with self.assertRaises(ValueError):
            mathx.chi2_sf(1.0, 0)

    # D-05: DSX-VAL-020
    def test_design_effect_matches_cochrane_worked_example(self):
        self.assertAlmostEqual(mathx.design_effect(29.8, 0.02), 1.576, places=3)

    def test_design_effect_cluster_of_one_inflates_nothing(self):
        self.assertEqual(mathx.design_effect(1, 0.5), 1.0)

    def test_design_effect_zero_icc_inflates_nothing(self):
        self.assertEqual(mathx.design_effect(50, 0.0), 1.0)

    def test_design_effect_cluster_size_below_one_raises(self):
        with self.assertRaises(ValueError):
            mathx.design_effect(0.5, 0.1)

    def test_design_effect_icc_out_of_range_raises(self):
        with self.assertRaises(ValueError):
            mathx.design_effect(30, -0.1)
        with self.assertRaises(ValueError):
            mathx.design_effect(30, 1.1)

    # D-05: DSX-INT-030
    def test_diluted_effect_matches_the_published_multiplicative_identity(self):
        # Deng & Hu (2015) Formula (1), section 2.1: delta_overall = delta_Tr x
        # N_Tr/N. The exact triggered effect and trigger rate behind the
        # paper's published -18 msec naive value could not be read from the
        # paper's own text (UNVERIFIED — see dsx.mathx.diluted_effect's
        # docstring); back-solving a pair that merely multiplies to -18 would
        # fabricate an unverified number, so this test asserts the formula's
        # multiplicative identity directly instead.
        self.assertAlmostEqual(mathx.diluted_effect(-10.0, 0.4), -4.0, places=6)

    # D-05: DSX-INT-030
    def test_diluted_effect_is_scoped_to_additive_metrics_not_the_counterexamples_ratio_metric(self):
        # Deng & Hu (2015) section 2.1: the paper's own counterexample metric
        # is time to success, a ratio metric, and the paper prints the
        # diverging -26/-18 msec pair precisely to show the additive formula
        # failing there. The scope boundary this test guards is that "ratio"
        # stays outside the partition DSX-INT-030 and diluted_effect are
        # scoped to — asserted against the real partition constants and the
        # docstring's own reference-value paragraph, not against two
        # hardcoded literals compared to each other (08-REVIEW.md WR-02).
        self.assertIn("ratio", interference._RATIO_METRIC_TYPES)
        self.assertNotIn("ratio", interference._ADDITIVE_METRIC_TYPES)
        docstring = mathx.diluted_effect.__doc__ or ""
        self.assertIn("-26", docstring)
        self.assertIn("-18", docstring)
        self.assertIn("additive", docstring)

    def test_diluted_effect_rejects_trigger_rate_below_zero(self):
        with self.assertRaises(ValueError):
            mathx.diluted_effect(-30.0, -0.1)

    def test_diluted_effect_rejects_trigger_rate_above_one(self):
        with self.assertRaises(ValueError):
            mathx.diluted_effect(-30.0, 1.1)

    def test_diluted_effect_accepts_both_closed_interval_endpoints(self):
        self.assertEqual(mathx.diluted_effect(-30.0, 1.0), -30.0)
        self.assertEqual(mathx.diluted_effect(-30.0, 0.0), 0.0)


# ── loader ───────────────────────────────────────────────────────────────────


class TestLoader(unittest.TestCase):
    SAMPLE = """
# a comment
spec_version: 1
title: "Onboarding checklist"
decision:
  owner: VP Growth
  reversible: true
  minimum_practical_effect: null
metrics:
  - name: activation_rate
    type: ratio
    tags: [growth, north_star]
  - name: retention_d7
    type: rate
design:
  alpha: 0.05
  arms: [control, treatment]
note: >
  folded text
  across lines
"""

    def test_bundled_parser_handles_the_template_subset(self):
        data = _parse_yaml_subset(self.SAMPLE, "<test>")
        self.assertEqual(data["spec_version"], 1)
        self.assertEqual(data["title"], "Onboarding checklist")
        self.assertEqual(data["decision"]["owner"], "VP Growth")
        self.assertIs(data["decision"]["reversible"], True)
        self.assertIsNone(data["decision"]["minimum_practical_effect"])
        self.assertEqual(len(data["metrics"]), 2)
        self.assertEqual(data["metrics"][0]["name"], "activation_rate")
        self.assertEqual(data["metrics"][0]["tags"], ["growth", "north_star"])
        self.assertEqual(data["metrics"][1]["type"], "rate")
        self.assertEqual(data["design"]["alpha"], 0.05)
        self.assertEqual(data["design"]["arms"], ["control", "treatment"])
        self.assertEqual(data["note"], "folded text across lines\n")  # ">" clips to one \n

    def test_bundled_parser_matches_pyyaml_when_available(self):
        try:
            import yaml
        except ImportError:  # pragma: no cover
            self.skipTest("PyYAML not installed")
        self.assertEqual(_parse_yaml_subset(self.SAMPLE, "<test>"), yaml.safe_load(self.SAMPLE))

    def test_json_is_accepted(self):
        self.assertEqual(loads('{"a": 1}', suffix=".json")["a"], 1)

    def test_duplicate_key_is_rejected(self):
        with self.assertRaises(SpecParseError):
            _parse_yaml_subset("a: 1\na: 2\n", "<test>")

    def test_tabs_are_rejected(self):
        with self.assertRaises(SpecParseError):
            _parse_yaml_subset("a:\n\tb: 1\n", "<test>")

    def test_inline_comment_after_value_is_stripped(self):
        data = _parse_yaml_subset("alpha: 0.05  # significance level\n", "<t>")
        self.assertEqual(data["alpha"], 0.05)

    def test_hash_inside_quotes_is_preserved(self):
        data = _parse_yaml_subset('color: "#ff0000"\n', "<t>")
        self.assertEqual(data["color"], "#ff0000")

    def test_bare_none_is_a_string_not_null(self):
        self.assertEqual(_parse_yaml_subset("x: none\n", "<t>")["x"], "none")
        self.assertEqual(
            _parse_yaml_subset("x: [none, clustered]\n", "<t>")["x"], ["none", "clustered"]
        )
        self.assertIsNone(_parse_yaml_subset("x: null\n", "<t>")["x"])
        self.assertIsNone(_parse_yaml_subset("x: ~\n", "<t>")["x"])
        self.assertIsNone(_parse_yaml_subset("x:\n", "<t>")["x"])

    def test_bare_none_matches_pyyaml(self):
        try:
            import yaml
        except ImportError:  # pragma: no cover
            self.skipTest("PyYAML not installed")
        self.assertEqual(
            _parse_yaml_subset("x: none\n", "<t>")["x"], yaml.safe_load("x: none\n")["x"]
        )
        self.assertEqual(
            _parse_yaml_subset("x: [none, clustered]\n", "<t>")["x"],
            yaml.safe_load("x: [none, clustered]\n")["x"],
        )


# ── spec structure ───────────────────────────────────────────────────────────


class TestSpecStructure(unittest.TestCase):
    def test_empty_spec_reports_every_required_field(self):
        report = validate_structure({})
        self.assertIn("DSX-SPEC-001", codes(report))
        self.assertTrue(report.blocks(Severity.CRITICAL))

    def test_missing_decision_rule_is_critical(self):
        report = validate_structure(
            {"spec_version": 1, "title": "t", "question_type": "descriptive",
             "decision": {"owner": "x"}}
        )
        self.assertIn("DSX-SPEC-010", codes(report))
        self.assertIn("DSX-SPEC-012", codes(report))

    def test_duplicate_metric_names_rejected(self):
        report = validate_structure(
            {"spec_version": 1, "title": "t", "question_type": "descriptive",
             "decision": {"decision_rule": "r", "owner": "o", "action_if_null": "n"},
             "metrics": [{"name": "rev", "definition": "d", "grain": "user", "type": "count"},
                         {"name": "rev", "definition": "e", "grain": "user", "type": "count"}]}
        )
        self.assertIn("DSX-SPEC-022", codes(report))

    def test_ratio_without_denominator_flagged(self):
        report = validate_structure(
            {"spec_version": 1, "title": "t", "question_type": "descriptive",
             "decision": {"decision_rule": "r", "owner": "o", "action_if_null": "n"},
             "metrics": [{"name": "cr", "definition": "d", "grain": "user", "type": "ratio"}]}
        )
        self.assertIn("DSX-SPEC-026", codes(report))

    def test_unknown_question_type_rejected(self):
        report = validate_structure(
            {"spec_version": 1, "title": "t", "question_type": "vibes",
             "decision": {"decision_rule": "r", "owner": "o", "action_if_null": "n"}}
        )
        self.assertIn("DSX-SPEC-003", codes(report))

    def test_vocabularies_registry_covers_the_dump(self):
        from dsx import spec as spec_mod

        out = describe_vocabulary()
        for name, obj in spec_mod._VOCABULARIES:
            self.assertIn(name, out, f"{name} missing from describe_vocabulary() output")
            self.assertTrue(out[name], f"{name} maps to an empty container")
        # identity, not equality — the registry holds the actual module constant
        registry = dict(spec_mod._VOCABULARIES)
        self.assertIs(registry["peeking_policies"], spec_mod.PEEKING_POLICIES)
        self.assertIs(registry["variance_adjustments"], spec_mod.VARIANCE_ADJUSTMENTS)
        self.assertIs(registry["paradigms"], spec_mod.PARADIGMS)
        self.assertIs(registry["missingness_mechanisms"], spec_mod.MISSINGNESS_MECHANISMS)

    def test_describe_vocabulary_dict_backed_are_sorted_dicts(self):
        out = describe_vocabulary()
        self.assertIsInstance(out["variance_adjustments"], list)
        self.assertEqual(out["variance_adjustments"], sorted(out["variance_adjustments"]))

    def test_describe_vocabulary_is_byte_stable(self):
        a = json.dumps(describe_vocabulary(), indent=2)
        b = json.dumps(describe_vocabulary(), indent=2)
        self.assertEqual(a, b)

    def test_peeking_policies_dump_is_a_description_dict(self):
        out = describe_vocabulary()["peeking_policies"]
        self.assertIsInstance(out, dict)
        self.assertEqual(set(out), set(PEEKING_POLICIES))
        self.assertTrue(out["always_valid"].strip())
        self.assertTrue(out["uncontrolled_continuous"].strip())
        self.assertNotEqual(out["always_valid"], out["uncontrolled_continuous"])

    def test_uncontrolled_continuous_peeking_policy_exists(self):
        self.assertIn("uncontrolled_continuous", PEEKING_POLICIES)
        self.assertTrue(PEEKING_POLICIES["uncontrolled_continuous"].strip())
        self.assertNotEqual(
            PEEKING_POLICIES["uncontrolled_continuous"], PEEKING_POLICIES["always_valid"]
        )

    def test_missingness_mechanisms_has_exactly_four_members_no_none(self):
        from dsx.spec import MISSINGNESS_MECHANISMS

        self.assertEqual(set(MISSINGNESS_MECHANISMS), {"MCAR", "MAR", "MNAR", "not_assessed"})

    # ── 11-02: estimand axis vocabulary (REQ-P11-01, REQ-P11-04) ───────────────

    def test_estimand_types_has_exactly_four_members_with_descriptions(self):
        from dsx.spec import ESTIMAND_TYPES

        self.assertEqual(
            set(ESTIMAND_TYPES),
            {
                "difference_in_proportions", "difference_in_means",
                "regression_coefficient", "ratio_of_means",
            },
        )
        for value in ESTIMAND_TYPES.values():
            self.assertTrue(value.strip())

    def test_estimand_types_registered_in_vocabularies_registry(self):
        from dsx import spec as spec_mod

        registry = dict(spec_mod._VOCABULARIES)
        self.assertIn("estimand_types", registry)
        self.assertIs(registry["estimand_types"], spec_mod.ESTIMAND_TYPES)

    def test_estimand_type_row_registered_in_validity_frame_membership(self):
        from dsx.spec import ESTIMAND_TYPES, _VALIDITY_FRAME_MEMBERSHIP

        self.assertIn(("estimand", "type", ESTIMAND_TYPES), _VALIDITY_FRAME_MEMBERSHIP)

    def test_estimand_types_dump_is_a_key_sorted_description_dict(self):
        out = describe_vocabulary()["estimand_types"]
        from dsx.spec import ESTIMAND_TYPES

        self.assertIsInstance(out, dict)
        self.assertEqual(set(out), set(ESTIMAND_TYPES))
        self.assertEqual(list(out), sorted(out))

    def test_out_of_vocabulary_estimand_type_reports_high(self):
        # D-05: DSX-SPEC-082
        spec = {
            "spec_version": 1, "title": "t", "question_type": "descriptive", "decision": {"owner": "x"},
            "validity_frame": {
                **{k: {"a": 1} for k in
                   ("units", "measurement", "dependence", "sampling_frame", "missingness")},
                "estimand": {"type": "not_a_real_estimand"},
            },
        }
        report = validate_structure(spec)
        found = [f for f in report.findings if f.code == "DSX-SPEC-082"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.HIGH)
        self.assertEqual(found[0].where, "spec.validity_frame.estimand.type")

    def test_estimand_type_absent_produces_no_finding(self):
        spec = {
            "spec_version": 1, "title": "t", "question_type": "descriptive", "decision": {"owner": "x"},
            "validity_frame": {
                k: {"a": 1} for k in
                ("estimand", "units", "measurement", "dependence", "sampling_frame", "missingness")
            },
        }
        report = validate_structure(spec)
        self.assertFalse([f for f in report.findings if f.code == "DSX-SPEC-082"])

    def test_estimand_type_empty_string_produces_no_finding(self):
        spec = {
            "spec_version": 1, "title": "t", "question_type": "descriptive", "decision": {"owner": "x"},
            "validity_frame": {
                **{k: {"a": 1} for k in
                   ("units", "measurement", "dependence", "sampling_frame", "missingness")},
                "estimand": {"quantity": "q", "type": ""},
            },
        }
        report = validate_structure(spec)
        self.assertFalse([f for f in report.findings if f.code == "DSX-SPEC-082"])

    def test_paradigms_and_paradigm_justifications(self):
        from dsx.spec import PARADIGM_JUSTIFICATIONS, PARADIGMS, VARIANCE_ADJUSTMENTS

        self.assertEqual(set(PARADIGMS), {"frequentist", "bayesian"})
        self.assertEqual(len(PARADIGM_JUSTIFICATIONS), 7)
        self.assertIsInstance(VARIANCE_ADJUSTMENTS, set)

    # ── 06-05: validity_frame / inference round-trip (REQ-P6-02, REQ-P6-04, D-12) ──

    def test_template_validity_frame_and_inference_round_trip(self):
        from dsx.loader import load

        template = Path(__file__).resolve().parent.parent / "templates" / "ANALYSIS-SPEC.yaml"
        spec = load(str(template))
        vf = spec["validity_frame"]
        need = [
            "estimand", "units", "identification", "dependence", "interference",
            "triggering", "stability", "sampling_frame", "missingness", "measurement",
        ]
        missing = [k for k in need if not isinstance(vf.get(k), dict)]
        self.assertEqual(missing, [], missing)
        self.assertEqual(
            set(spec["inference"]),
            {
                "paradigm", "paradigm_justification", "declared_at",
                "primary_procedure", "alpha_spending", "fallback_rule",
                "threshold_calibration", "prior_justification", "decision_threshold",
            },
        )

    def test_template_vocabulary_placeholders_are_legal_members(self):
        from dsx.loader import load
        from dsx.spec import (
            ANALYSIS_POPULATIONS,
            CONSTRAINT_SOURCES,
            DECLARATION_POINTS,
            DEPENDENCE_STRUCTURES,
            IDENTIFICATION_STRENGTHS,
            INTERFERENCE_MITIGATIONS,
            INTERFERENCE_RISKS,
            MISSINGNESS_MECHANISMS,
            PARADIGM_JUSTIFICATIONS,
            PARADIGMS,
        )

        template = Path(__file__).resolve().parent.parent / "templates" / "ANALYSIS-SPEC.yaml"
        spec = load(str(template))
        vf = spec["validity_frame"]
        inf = spec["inference"]
        self.assertIn(vf["identification"]["strength"], IDENTIFICATION_STRENGTHS)
        self.assertIn(vf["identification"]["constraint_source"], CONSTRAINT_SOURCES)
        self.assertIn(vf["dependence"]["structure"], DEPENDENCE_STRUCTURES)
        self.assertIn(vf["interference"]["risk"], INTERFERENCE_RISKS)
        self.assertIn(vf["interference"]["mitigation"], INTERFERENCE_MITIGATIONS)
        self.assertIn(vf["triggering"]["analysis_population"], ANALYSIS_POPULATIONS)
        self.assertIn(vf["missingness"]["mechanism"], MISSINGNESS_MECHANISMS)
        self.assertIn(inf["paradigm"], PARADIGMS)
        self.assertIn(inf["paradigm_justification"], PARADIGM_JUSTIFICATIONS)
        self.assertIn(inf["declared_at"], DECLARATION_POINTS)

    # ── 11.1-05: cleaning scaffold is commented, inert scaffold (REQ-P11.1-03) ──

    def test_template_cleaning_scaffold_is_commented_and_inert(self):
        from dsx.loader import load

        template = Path(__file__).resolve().parent.parent / "templates" / "ANALYSIS-SPEC.yaml"
        spec = load(str(template))
        data = spec.get("data") or []
        self.assertTrue(data, "template data section should not be empty")
        for entry in data:
            if isinstance(entry, dict):
                self.assertNotIn("cleaning", entry)

    def test_good_fixture_none_frame_fields_round_trip_as_strings(self):
        from dsx.loader import load

        fixture = Path(__file__).resolve().parent.parent / "examples" / "good-ANALYSIS-SPEC.yaml"
        vf = load(str(fixture))["validity_frame"]
        self.assertEqual(vf["interference"]["risk"], "none")
        self.assertEqual(vf["interference"]["mitigation"], "none")
        self.assertEqual(vf["identification"]["constraint_source"], "none")

    def test_no_shipped_spec_declares_removed_stopping_rule_field(self):
        from dsx.loader import load

        root = Path(__file__).resolve().parent.parent
        bad = []
        for p in list((root / "examples").rglob("*.yaml")) + list((root / "templates").rglob("*.yaml")):
            if "ANALYSIS-SPEC" not in p.name:
                continue
            inf = load(str(p)).get("inference") or {}
            if "stopping_rule" in inf:
                bad.append(str(p))
        self.assertEqual(bad, [])

    def test_every_committed_spec_declares_a_valid_estimand_type(self):
        # 11-02: REQ-P11-01 — a tenth spec added later inherits this assertion via glob.
        # Plan 11.1-08: full-frame-cleaning-ANALYSIS-SPEC.yaml is the tenth spec this
        # comment anticipated; count updated from 9 to 10 in the same commit that adds it.
        from dsx.loader import load
        from dsx.spec import ESTIMAND_TYPES

        root = Path(__file__).resolve().parent.parent
        paths = (
            sorted((root / "examples").glob("*-ANALYSIS-SPEC.yaml"))
            + sorted((root / "examples" / "known-bad").glob("*-ANALYSIS-SPEC.yaml"))
            + sorted((root / "templates").glob("ANALYSIS-SPEC.yaml"))
        )
        self.assertEqual(len(paths), 10, [str(p) for p in paths])
        bad = []
        for p in paths:
            estimand_type = load(str(p)).get("validity_frame", {}).get("estimand", {}).get("type")
            if not estimand_type or estimand_type not in ESTIMAND_TYPES:
                bad.append((str(p), estimand_type))
        self.assertEqual(bad, [])

    # ── 06-06: validity_frame requiredness, aggregation, membership (REQ-P6-02/03) ──

    def test_causal_spec_with_no_validity_frame_key_reports_one_critical_itemising_ten(self):
        # D-05: DSX-SPEC-080
        report = validate_structure(
            {"spec_version": 1, "title": "t", "question_type": "causal", "decision": {"owner": "x"}}
        )
        found = [f for f in report.findings if f.code == "DSX-SPEC-080"]
        self.assertEqual(len(found), 1)
        detail = found[0].detail
        for name in (
            "estimand", "units", "measurement", "dependence", "sampling_frame", "missingness",
            "identification", "interference", "triggering", "stability",
        ):
            self.assertIn(name, detail)

    def test_descriptive_spec_with_no_validity_frame_key_names_only_six(self):
        report = validate_structure(
            {"spec_version": 1, "title": "t", "question_type": "descriptive", "decision": {"owner": "x"}}
        )
        found = [f for f in report.findings if f.code == "DSX-SPEC-080"]
        self.assertEqual(len(found), 1)
        detail = found[0].detail
        for name in ("interference", "triggering", "stability", "identification"):
            self.assertNotIn(name, detail)

    def test_causal_spec_missing_three_sub_blocks_reports_three_findings(self):
        # D-05: DSX-SPEC-081
        base = {
            "spec_version": 1, "title": "t", "question_type": "causal", "decision": {"owner": "x"},
            "validity_frame": {
                k: {"a": 1} for k in
                ("estimand", "units", "measurement", "dependence", "sampling_frame",
                 "missingness", "identification")
            },
        }
        report = validate_structure(base)
        found = [f for f in report.findings if f.code == "DSX-SPEC-081"]
        self.assertEqual(len(found), 3, [f.where for f in found])
        self.assertEqual(
            {f.where for f in found},
            {"spec.validity_frame.interference", "spec.validity_frame.triggering",
             "spec.validity_frame.stability"},
        )
        self.assertTrue(all(f.severity == Severity.CRITICAL for f in found))

    def test_descriptive_spec_with_only_six_always_required_produces_no_findings(self):
        spec = {
            "spec_version": 1, "title": "t", "question_type": "descriptive", "decision": {"owner": "x"},
            "validity_frame": {
                k: {"a": 1} for k in
                ("estimand", "units", "measurement", "dependence", "sampling_frame", "missingness")
            },
        }
        report = validate_structure(spec)
        self.assertFalse([f for f in report.findings if f.code in ("DSX-SPEC-080", "DSX-SPEC-081")])

    def test_descriptive_experiment_design_still_requires_interference(self):
        spec = {
            "spec_version": 1, "title": "t", "question_type": "descriptive", "decision": {"owner": "x"},
            "design": {"kind": "experiment"},
            "validity_frame": {
                k: {"a": 1} for k in
                ("estimand", "units", "measurement", "dependence", "sampling_frame", "missingness",
                 "identification", "triggering", "stability")
            },
        }
        report = validate_structure(spec)
        found = [f for f in report.findings if f.code == "DSX-SPEC-081"]
        self.assertEqual({f.where for f in found}, {"spec.validity_frame.interference"})

    def test_out_of_vocabulary_sub_field_reports_high_with_allowed_members(self):
        # D-05: DSX-SPEC-082
        spec = {
            "spec_version": 1, "title": "t", "question_type": "descriptive", "decision": {"owner": "x"},
            "validity_frame": {
                **{k: {"a": 1} for k in
                   ("estimand", "units", "measurement", "sampling_frame", "missingness")},
                "dependence": {"structure": "not_a_member"},
            },
        }
        report = validate_structure(spec)
        found = [f for f in report.findings if f.code == "DSX-SPEC-082"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.HIGH)
        self.assertEqual(found[0].where, "spec.validity_frame.dependence.structure")
        self.assertIn("clustered", found[0].detail)

    def test_malformed_validity_frame_shapes_degrade_to_dsx_spec_080_not_a_crash(self):
        for bad in ("a string", [], {}, None):
            spec = {
                "spec_version": 1, "title": "t", "question_type": "causal", "decision": {"owner": "x"},
                "validity_frame": bad,
            }
            report = validate_structure(spec)  # must not raise
            self.assertIn("DSX-SPEC-080", codes(report))

    def test_good_fixture_produces_none_of_the_three_validity_frame_codes(self):
        from dsx.loader import load

        fixture = Path(__file__).resolve().parent.parent / "examples" / "good-ANALYSIS-SPEC.yaml"
        spec = load(str(fixture))
        report = validate_structure(spec)
        self.assertFalse(
            [f for f in report.findings if f.code in ("DSX-SPEC-080", "DSX-SPEC-081", "DSX-SPEC-082")]
        )

    # ── 06-06: inference block shape, removed-field redirect (REQ-P6-04) ──────────

    def test_absent_inference_block_produces_no_finding(self):
        spec = {
            "spec_version": 1, "title": "t", "question_type": "descriptive", "decision": {"owner": "x"},
        }
        report = validate_structure(spec)
        self.assertFalse([f for f in report.findings if f.code in ("DSX-SPEC-085", "DSX-SPEC-086")])

    def test_inference_fields_constant_matches_req_p6_04(self):
        # D-05: DSX-PAR-010, DSX-PAR-011
        from dsx.spec import _INFERENCE_FIELDS

        self.assertEqual(
            _INFERENCE_FIELDS,
            ("paradigm", "paradigm_justification", "declared_at",
             "primary_procedure", "alpha_spending", "fallback_rule",
             "threshold_calibration", "prior_justification", "decision_threshold"),
        )

    def test_describe_vocabulary_inference_fields_matches_the_constant(self):
        # D-05: DSX-PAR-010, DSX-PAR-011
        from dsx.spec import _INFERENCE_FIELDS

        out = describe_vocabulary()
        self.assertIn("inference_fields", out)
        self.assertEqual(out["inference_fields"], sorted(_INFERENCE_FIELDS))
        for name in ("threshold_calibration", "prior_justification", "decision_threshold"):
            self.assertIn(name, out["inference_fields"])

    def test_new_inference_fields_produce_no_shape_findings(self):
        # D-05: DSX-PAR-010, DSX-PAR-011
        base = {
            "spec_version": 1, "title": "t", "question_type": "descriptive", "decision": {"owner": "x"},
        }
        spec = dict(base, inference={
            "paradigm": "bayesian",
            "threshold_calibration": "simulated via 10k-trial FPR sweep at K=19",
            "prior_justification": "prior_information_available",
            "decision_threshold": "P(B>A) > 0.95",
        })
        report = validate_structure(spec)
        self.assertFalse(
            [f for f in report.findings if f.code in ("DSX-SPEC-085", "DSX-SPEC-086")]
        )

    def test_inference_vocabulary_violations_report_three_high_findings(self):
        # D-05: DSX-SPEC-085
        base = {
            "spec_version": 1, "title": "t", "question_type": "descriptive", "decision": {"owner": "x"},
            "validity_frame": {
                k: {"a": 1} for k in
                ("estimand", "units", "measurement", "dependence", "sampling_frame", "missingness")
            },
        }
        spec = dict(base, inference={
            "paradigm": "freqentist", "paradigm_justification": "nope", "declared_at": "whenever",
        })
        report = validate_structure(spec)
        found = [f for f in report.findings if f.code == "DSX-SPEC-085"]
        self.assertEqual(len(found), 3, [f.where for f in found])
        self.assertTrue(all(f.severity == Severity.HIGH for f in found))

    def test_removed_stopping_rule_field_redirects_to_peeking_policy(self):
        # D-05: DSX-SPEC-086
        base = {
            "spec_version": 1, "title": "t", "question_type": "descriptive", "decision": {"owner": "x"},
            "validity_frame": {
                k: {"a": 1} for k in
                ("estimand", "units", "measurement", "dependence", "sampling_frame", "missingness")
            },
        }
        spec = dict(base, inference={"paradigm": "frequentist", "stopping_rule": "fixed_horizon"})
        report = validate_structure(spec)
        found = [f for f in report.findings if f.code == "DSX-SPEC-086"]
        self.assertEqual(len(found), 1)
        self.assertIn("design.peeking_policy", found[0].remedy)

    def test_good_fixture_produces_none_of_the_inference_codes(self):
        from dsx.loader import load

        fixture = Path(__file__).resolve().parent.parent / "examples" / "good-ANALYSIS-SPEC.yaml"
        spec = load(str(fixture))
        report = validate_structure(spec)
        self.assertFalse([f for f in report.findings if f.code in ("DSX-SPEC-085", "DSX-SPEC-086")])

    # ── 06-06: decision records from structural adjudications (D-13, D-19) ────────

    def test_structural_adjudications_emit_deterministic_decision_records(self):
        s = {
            "spec_version": 1, "title": "t", "question_type": "causal", "decision": {"owner": "x"},
            "validity_frame": {
                k: {"a": 1} for k in
                ("estimand", "units", "measurement", "dependence", "sampling_frame", "missingness",
                 "identification", "interference", "triggering", "stability")
            },
            "inference": {"paradigm": "bayesian"},
        }
        report = validate_structure(s)
        decisions = report.context["decisions"]
        self.assertEqual(len(decisions), 2, decisions)
        self.assertTrue(all(d["layer"] == "deterministic" for d in decisions))
        self.assertTrue(all(d["id"] == "" and d["invocation_id"] == "" for d in decisions))
        self.assertTrue(decisions[0]["counterfactual"].strip())
        self.assertTrue(decisions[0]["rule"].strip())
        self.assertEqual(set(decisions[0]["inputs"]), {"question_type", "design.kind"})
        self.assertIn("inference.paradigm", decisions[1]["inputs"])

    def test_collect_from_report_returns_both_decisions_in_order(self):
        from dsx.decisions import collect_from_report
        from dsx.findings import merge

        s = {
            "spec_version": 1, "title": "t", "question_type": "causal", "decision": {"owner": "x"},
            "validity_frame": {
                k: {"a": 1} for k in
                ("estimand", "units", "measurement", "dependence", "sampling_frame", "missingness",
                 "identification", "interference", "triggering", "stability")
            },
            "inference": {"paradigm": "bayesian"},
        }
        merged = merge("x", [validate_structure(s)])
        collected = collect_from_report(merged)
        self.assertEqual(len(collected), 2)
        self.assertIn("question_type", collected[0]["inputs"])
        self.assertIn("inference.paradigm", collected[1]["inputs"])

    def test_no_check_module_appends_to_a_decisions_list(self):
        pattern = re.compile(r'context(\[.decisions.\]|\.setdefault\(.decisions.)')
        checks_dir = Path(__file__).resolve().parent.parent / "dsx" / "checks"
        offenders = []
        for path in sorted(checks_dir.glob("*.py")):
            text = path.read_text(encoding="utf-8")
            if pattern.search(text):
                offenders.append(str(path))
        self.assertEqual(offenders, [], offenders)


# ── 07-01: dependence structure -> admissible method-family map (D-04, REQ-P7-04) ──


class TestDependenceAdmissibleMethods(unittest.TestCase):
    def test_dependence_admissible_methods_keys_match_structures_minus_none(self):
        from dsx.spec import DEPENDENCE_ADMISSIBLE_METHODS, DEPENDENCE_STRUCTURES

        self.assertEqual(
            set(DEPENDENCE_ADMISSIBLE_METHODS), set(DEPENDENCE_STRUCTURES) - {"none"}
        )

    def test_every_dependence_admissible_method_is_a_variance_adjustment(self):
        from dsx.spec import DEPENDENCE_ADMISSIBLE_METHODS, VARIANCE_ADJUSTMENTS

        for structure, methods in DEPENDENCE_ADMISSIBLE_METHODS.items():
            self.assertTrue(
                methods <= VARIANCE_ADJUSTMENTS,
                f"{structure}: {methods} is not a subset of VARIANCE_ADJUSTMENTS",
            )

    def test_none_structure_has_no_dependence_admissible_methods_entry(self):
        from dsx.spec import DEPENDENCE_ADMISSIBLE_METHODS

        self.assertNotIn("none", DEPENDENCE_ADMISSIBLE_METHODS)

    def test_dependence_specific_admissibility(self):
        from dsx.spec import DEPENDENCE_ADMISSIBLE_METHODS

        self.assertIn("cluster_robust", DEPENDENCE_ADMISSIBLE_METHODS["clustered"])
        self.assertTrue(
            all(
                "delta_method" not in methods
                for methods in DEPENDENCE_ADMISSIBLE_METHODS.values()
            ),
            "delta_method must be admissible for no structure at all",
        )

    def test_dependence_admissible_methods_excluded_from_vocabulary_dump(self):
        out = describe_vocabulary()
        self.assertNotIn("dependence_admissible_methods", out)


# ── 07-01: falsifier placeholder/refusal/discrimination lexicon (D-05, REQ-P7-01) ──


class TestFalsifierLexicon(unittest.TestCase):
    def test_good_fixture_falsifier_is_discriminating_for_the_estimand(self):
        from dsx.spec import falsifier_is_discriminating

        # Verbatim from examples/good-ANALYSIS-SPEC.yaml:302
        value = (
            "95% CI on the activation uplift includes zero, or its lower bound "
            "sits below +1.0pp"
        )
        self.assertTrue(falsifier_is_discriminating(value))

    def test_empty_string_is_not_discriminating(self):
        from dsx.spec import falsifier_is_discriminating

        self.assertFalse(falsifier_is_discriminating(""))

    def test_template_angle_bracket_falsifier_is_not_discriminating(self):
        from dsx.spec import falsifier_is_discriminating

        # Verbatim from templates/ANALYSIS-SPEC.yaml:288
        value = "<the observation that would prove this wrong>"
        self.assertFalse(falsifier_is_discriminating(value))

    def test_refusal_tokens_are_not_discriminating(self):
        from dsx.spec import falsifier_is_discriminating

        for token in ("n/a", "N/A", "tbd", "TBD", "none", "unknown"):
            self.assertFalse(falsifier_is_discriminating(token), token)

    def test_prose_without_predicate_or_number_is_not_discriminating(self):
        from dsx.spec import falsifier_is_discriminating

        self.assertFalse(
            falsifier_is_discriminating("the result will look different than we expect")
        )

    def test_numeric_only_falsifier_is_discriminating(self):
        from dsx.spec import falsifier_is_discriminating

        self.assertTrue(
            falsifier_is_discriminating("the uplift must clear a 1.5pp threshold")
        )

    def test_none_identified_is_not_classified_as_a_refusal(self):
        from dsx.spec import is_placeholder_or_refusal

        # Verbatim from examples/good-ANALYSIS-SPEC.yaml:342 (sampling_frame.selection_risk)
        self.assertFalse(is_placeholder_or_refusal("none identified"))

    def test_long_input_classifies_without_catastrophic_backtracking(self):
        import time

        from dsx.spec import falsifier_is_discriminating

        text = ("the result will look different than we expect " * 500)[:20000]
        self.assertEqual(len(text), 20000)
        start = time.perf_counter()
        falsifier_is_discriminating(text)
        self.assertLess(time.perf_counter() - start, 1.0)


# ── design ───────────────────────────────────────────────────────────────────


class TestDesign(unittest.TestCase):
    BASE = {
        "question_type": "causal",
        "design": {
            "kind": "experiment",
            "randomization_unit": "user",
            "analysis_unit": "user",
            "baseline_rate": 0.31,
            "mde": 0.02,
            "alpha": 0.05,
            "power": 0.80,
            "planned_n_per_arm": 9000,
            "duration_days": 14,
            "guardrail_metrics": ["latency_p95"],
            "peeking_policy": "fixed_horizon",
        },
    }

    def test_adequately_powered_experiment_passes(self):
        report = design.check(self.BASE)
        self.assertNotIn("DSX-EXP-006", codes(report))
        self.assertFalse(report.blocks(Severity.CRITICAL))

    def test_underpowered_experiment_blocks_with_the_number(self):
        spec = {**self.BASE, "design": {**self.BASE["design"], "planned_n_per_arm": 2000}}
        report = design.check(spec)
        self.assertIn("DSX-EXP-006", codes(report))
        finding = next(f for f in report.findings if f.code == "DSX-EXP-006")
        self.assertEqual(finding.severity, Severity.CRITICAL)
        self.assertGreater(finding.data["required_n_per_arm"], 2000)
        self.assertLess(finding.data["achieved_power"], 0.80)

    def test_missing_power_inputs_block(self):
        spec = {**self.BASE, "design": {"kind": "experiment", "randomization_unit": "user",
                                        "analysis_unit": "user"}}
        report = design.check(spec)
        self.assertIn("DSX-EXP-001", codes(report))

    def test_unit_mismatch_without_adjustment_blocks(self):
        spec = {**self.BASE, "design": {**self.BASE["design"], "analysis_unit": "session"}}
        report = design.check(spec)
        self.assertIn("DSX-EXP-021", codes(report))

    def test_unit_mismatch_with_cluster_robust_passes(self):
        spec = {**self.BASE, "design": {**self.BASE["design"], "analysis_unit": "session",
                                        "variance_adjustment": "cluster_robust"}}
        self.assertNotIn("DSX-EXP-021", codes(design.check(spec)))

    def test_srm_is_detected(self):
        spec = {**self.BASE, "results": {"observed_n": [10000, 9400]}}
        report = design.check(spec)
        self.assertIn("DSX-EXP-011", codes(report))

    def test_balanced_allocation_passes_srm(self):
        spec = {**self.BASE, "results": {"observed_n": [10000, 10020]}}
        self.assertNotIn("DSX-EXP-011", codes(design.check(spec)))

    def test_peeking_under_fixed_horizon_blocks(self):
        spec = {**self.BASE, "results": {"interim_looks": 5}}
        report = design.check(spec)
        self.assertIn("DSX-EXP-060", codes(report))
        finding = next(f for f in report.findings if f.code == "DSX-EXP-060")
        self.assertGreater(finding.data["inflated_alpha"], 0.05)

    def test_peeking_under_sequential_policy_passes(self):
        spec = {**self.BASE,
                "design": {**self.BASE["design"], "peeking_policy": "sequential_obf"},
                "results": {"interim_looks": 5}}
        self.assertNotIn("DSX-EXP-060", codes(design.check(spec)))

    def test_dsx_exp_060_fires_only_for_empty_and_fixed_horizon(self):
        # D-08: pins the property, not just the current members — fails if _check_peeking
        # is later widened to fire on a member it should not.
        for policy in list(PEEKING_POLICIES) + [""]:
            with self.subTest(policy=policy):
                spec = {**self.BASE,
                        "design": {**self.BASE["design"], "peeking_policy": policy},
                        "results": {"interim_looks": 5}}
                fires = "DSX-EXP-060" in codes(design.check(spec))
                if policy in ("", "fixed_horizon"):
                    self.assertTrue(fires, f"expected DSX-EXP-060 for peeking_policy={policy!r}")
                else:
                    self.assertFalse(fires, f"unexpected DSX-EXP-060 for peeking_policy={policy!r}")

    def test_uncorrected_multiplicity_flagged(self):
        spec = {**self.BASE,
                "design": {**self.BASE["design"],
                           "multiplicity": {"family": ["a", "b", "c"], "correction": "none"}}}
        self.assertIn("DSX-EXP-050", codes(design.check(spec)))

    def test_corrected_multiplicity_passes(self):
        spec = {**self.BASE,
                "design": {**self.BASE["design"],
                           "multiplicity": {"family": ["a", "b", "c"],
                                            "correction": "benjamini_hochberg"}}}
        self.assertNotIn("DSX-EXP-050", codes(design.check(spec)))

    def test_causal_question_without_identification_blocks(self):
        spec = {"question_type": "causal",
                "design": {"kind": "observational", "identification": "none"}}
        self.assertIn("DSX-CAU-010", codes(design.check(spec)))

    def test_matching_without_sensitivity_analysis_flagged(self):
        spec = {"question_type": "causal",
                "design": {"kind": "observational", "identification": "matching",
                           "covariates": ["age", "tenure"]}}
        report = design.check(spec)
        self.assertIn("DSX-CAU-011", codes(report))
        self.assertIn("DSX-CAU-012", codes(report))

    def test_short_experiment_flagged(self):
        spec = {**self.BASE, "design": {**self.BASE["design"], "duration_days": 3}}
        self.assertIn("DSX-EXP-030", codes(design.check(spec)))

    def test_mde_above_practical_floor_flagged(self):
        spec = {**self.BASE, "decision": {"minimum_practical_effect": 0.005}}
        self.assertIn("DSX-EXP-007", codes(design.check(spec)))


# ── ml ───────────────────────────────────────────────────────────────────────


class TestML(unittest.TestCase):
    BASE = {
        "question_type": "predictive",
        "model": {
            "task": "binary_classification",
            "target": "churned_90d",
            "split": "temporal",
            "time_column": "signup_date",
            "train_period": "2025-01-01..2025-09-30",
            "test_period": "2025-10-01..2025-12-31",
            "features": ["tenure_days", "plan_tier", "sessions_last_30d"],
            "preprocessing_fit_on": "train_only",
            "primary_metric": "pr_auc",
            "baseline": "majority_class",
            "positive_rate": 0.04,
            "prediction_time_definition": "nightly 02:00 for active accounts",
        },
    }

    def test_clean_model_spec_passes(self):
        report = ml.check(self.BASE)
        self.assertFalse(report.blocks(Severity.HIGH), report.render(Severity.HIGH))

    def test_random_split_on_temporal_data_blocks(self):
        spec = {**self.BASE, "model": {**self.BASE["model"], "split": "random"}}
        report = ml.check(spec)
        self.assertIn("DSX-ML-011", codes(report))
        self.assertTrue(report.blocks(Severity.CRITICAL))

    def test_overlapping_periods_block(self):
        spec = {**self.BASE, "model": {**self.BASE["model"],
                                       "test_period": "2025-09-01..2025-12-31"}}
        self.assertIn("DSX-ML-014", codes(ml.check(spec)))

    def test_leaky_feature_names_detected(self):
        spec = {**self.BASE, "model": {**self.BASE["model"],
                                       "features": ["tenure_days", "cancel_date",
                                                    "days_to_churn", "refund_amount"]}}
        report = ml.check(spec)
        self.assertIn("DSX-ML-032", codes(report))
        suspects = next(f for f in report.findings if f.code == "DSX-ML-032").data["suspects"]
        self.assertEqual(len({s["feature"] for s in suspects}), 3)

    def test_acknowledged_leaky_features_are_not_reflagged(self):
        spec = {**self.BASE,
                "model": {**self.BASE["model"],
                          "features": ["tenure_days", "cancel_date"],
                          "features_excluded_for_leakage": ["cancel_date"]}}
        self.assertNotIn("DSX-ML-032", codes(ml.check(spec)))

    def test_target_in_features_blocks(self):
        spec = {**self.BASE, "model": {**self.BASE["model"],
                                       "features": ["tenure_days", "churned_90d"]}}
        self.assertIn("DSX-ML-031", codes(ml.check(spec)))

    def test_preprocessing_on_full_data_blocks(self):
        spec = {**self.BASE, "model": {**self.BASE["model"], "preprocessing_fit_on": "all_data"}}
        self.assertIn("DSX-ML-021", codes(ml.check(spec)))

    def test_resampling_before_split_blocks(self):
        spec = {**self.BASE, "model": {**self.BASE["model"], "resampling_applied_to": "before_split"}}
        self.assertIn("DSX-ML-022", codes(ml.check(spec)))

    def test_accuracy_on_imbalanced_target_flagged(self):
        spec = {**self.BASE, "model": {**self.BASE["model"], "primary_metric": "accuracy"}}
        report = ml.check(spec)
        self.assertIn("DSX-ML-041", codes(report))

    def test_roc_auc_on_imbalanced_target_flagged(self):
        spec = {**self.BASE, "model": {**self.BASE["model"], "primary_metric": "roc_auc"}}
        self.assertIn("DSX-ML-041", codes(ml.check(spec)))

    def test_grouped_data_needs_grouped_split(self):
        spec = {**self.BASE, "model": {**self.BASE["model"], "entity_column": "account_id",
                                       "split": "temporal"}}
        self.assertIn("DSX-ML-012", codes(ml.check(spec)))

    def test_model_not_beating_baseline_blocks(self):
        spec = {**self.BASE, "results": {"model_score": 0.61, "baseline_score": 0.63}}
        self.assertIn("DSX-ML-051", codes(ml.check(spec)))

    def test_overfitting_gap_flagged(self):
        spec = {**self.BASE, "results": {"train_score": 0.98, "test_score": 0.72}}
        self.assertIn("DSX-ML-060", codes(ml.check(spec)))

    def test_test_above_train_flagged(self):
        spec = {**self.BASE, "results": {"train_score": 0.61, "test_score": 0.95}}
        self.assertIn("DSX-ML-061", codes(ml.check(spec)))

    def test_train_test_overlap_blocks(self):
        spec = {**self.BASE, "results": {"train_test_overlap_rows": 812}}
        self.assertIn("DSX-ML-071", codes(ml.check(spec)))

    def test_threshold_tuned_on_test_blocks(self):
        spec = {**self.BASE, "model": {**self.BASE["model"], "threshold_selected_on": "test"}}
        self.assertIn("DSX-ML-072", codes(ml.check(spec)))

    def test_repeated_test_set_use_flagged(self):
        spec = {**self.BASE, "results": {"test_set_evaluations": 14}}
        self.assertIn("DSX-ML-070", codes(ml.check(spec)))


# ── Phase 11.1 plan 04: prediction-time check extraction + DSX-ML-043 ──────────


class TestPhase11_1ML(unittest.TestCase):
    # Derived from TestML.BASE (REQ-P11.1-04's plan instruction), with
    # primary_metric overridden per-test since TestML.BASE's 'pr_auc' is not a
    # member of IMBALANCE_UNSAFE_METRICS.
    BASE = TestML.BASE

    def _model(self, **overrides):
        model = {k: v for k, v in self.BASE["model"].items()}
        model.update(overrides)
        for key, value in list(model.items()):
            if value is None:
                del model[key]
        return model

    # ── DSX-ML-033: prediction-time check no longer gated on features ───────

    def test_no_features_no_prediction_time_produces_both_030_and_033(self):
        spec = {
            "question_type": "predictive",
            "model": self._model(
                features=None, prediction_time_definition=None, primary_metric="roc_auc"
            ),
        }
        found = codes(ml.check(spec))
        self.assertIn("DSX-ML-030", found)
        self.assertIn("DSX-ML-033", found)

    def test_features_declared_no_prediction_time_produces_033_not_030(self):
        spec = {**self.BASE, "model": self._model(prediction_time_definition=None)}
        found = codes(ml.check(spec))
        self.assertIn("DSX-ML-033", found)
        self.assertNotIn("DSX-ML-030", found)

    def test_prediction_time_declared_produces_no_033_with_features(self):
        self.assertNotIn("DSX-ML-033", codes(ml.check(self.BASE)))

    def test_prediction_time_declared_produces_no_033_without_features(self):
        spec = {**self.BASE, "model": self._model(features=None)}
        self.assertNotIn("DSX-ML-033", codes(ml.check(spec)))

    def test_dsx_ml_033_appears_at_most_once_in_a_report(self):
        spec = {**self.BASE, "model": self._model(prediction_time_definition=None)}
        found = [f for f in ml.check(spec).findings if f.code == "DSX-ML-033"]
        self.assertEqual(len(found), 1)

    def test_early_return_of_check_features_is_unaffected(self):
        # A blank features list still produces DSX-ML-030 exactly as before —
        # this task only relocates the prediction-time check, not the gate.
        spec = {**self.BASE, "model": self._model(features=None)}
        found = [f for f in ml.check(spec).findings if f.code == "DSX-ML-030"]
        self.assertEqual(len(found), 1)

    # ── DSX-ML-043: undeclared positive rate under an imbalance-unsafe metric

    def test_no_positive_rate_imbalance_unsafe_metric_produces_043_at_high(self):
        # D-05: DSX-ML-043
        spec = {
            **self.BASE,
            "model": self._model(primary_metric="roc_auc", positive_rate=None),
        }
        report = ml.check(spec)
        found = [f for f in report.findings if f.code == "DSX-ML-043"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.HIGH)

    def test_positive_rate_declared_on_results_section_clears_043(self):
        spec = {
            **self.BASE,
            "model": self._model(primary_metric="roc_auc", positive_rate=None),
            "results": {"positive_rate": 0.04},
        }
        self.assertNotIn("DSX-ML-043", codes(ml.check(spec)))

    def test_positive_rate_at_threshold_boundary_produces_neither_code(self):
        from dsx.checks.ml import IMBALANCE_THRESHOLD

        spec = {
            **self.BASE,
            "model": self._model(primary_metric="roc_auc", positive_rate=IMBALANCE_THRESHOLD),
        }
        found = codes(ml.check(spec))
        self.assertNotIn("DSX-ML-041", found)
        self.assertNotIn("DSX-ML-043", found)

    def test_positive_rate_one_step_below_threshold_produces_041(self):
        from dsx.checks.ml import IMBALANCE_THRESHOLD

        spec = {
            **self.BASE,
            "model": self._model(
                primary_metric="roc_auc", positive_rate=IMBALANCE_THRESHOLD - 0.01
            ),
        }
        self.assertIn("DSX-ML-041", codes(ml.check(spec)))

    def test_positive_rate_one_step_above_threshold_produces_neither_code(self):
        from dsx.checks.ml import IMBALANCE_THRESHOLD

        spec = {
            **self.BASE,
            "model": self._model(
                primary_metric="roc_auc", positive_rate=IMBALANCE_THRESHOLD + 0.01
            ),
        }
        found = codes(ml.check(spec))
        self.assertNotIn("DSX-ML-041", found)
        self.assertNotIn("DSX-ML-043", found)

    def test_positive_rate_one_half_produces_neither_code(self):
        spec = {**self.BASE, "model": self._model(primary_metric="roc_auc", positive_rate=0.5)}
        found = codes(ml.check(spec))
        self.assertNotIn("DSX-ML-041", found)
        self.assertNotIn("DSX-ML-043", found)

    def test_non_numeric_positive_rate_produces_043_not_an_exception(self):
        spec = {
            **self.BASE,
            "model": self._model(primary_metric="roc_auc", positive_rate="not a number"),
        }
        found = codes(ml.check(spec))  # must not raise
        self.assertIn("DSX-ML-043", found)

    def test_numeric_string_positive_rate_takes_same_branch_as_number(self):
        spec_str = {
            **self.BASE, "model": self._model(primary_metric="roc_auc", positive_rate="0.04")
        }
        spec_num = {
            **self.BASE, "model": self._model(primary_metric="roc_auc", positive_rate=0.04)
        }
        self.assertEqual(codes(ml.check(spec_str)), codes(ml.check(spec_num)))

    def test_regression_task_produces_no_043(self):
        spec = {
            "question_type": "predictive",
            "model": {
                "task": "regression",
                "target": "revenue",
                "split": "random",
                "primary_metric": "roc_auc",
                "baseline": "majority_class",
            },
        }
        self.assertNotIn("DSX-ML-043", codes(ml.check(spec)))

    def test_non_imbalance_unsafe_primary_metric_produces_no_043(self):
        spec = {**self.BASE, "model": self._model(primary_metric="pr_auc", positive_rate=None)}
        self.assertNotIn("DSX-ML-043", codes(ml.check(spec)))

    def test_two_consecutive_calls_produce_identical_finding_sequences(self):
        spec = {
            **self.BASE,
            "model": self._model(primary_metric="roc_auc", positive_rate=None, features=None),
        }
        r1 = [f.code for f in ml.check(spec).findings]
        r2 = [f.code for f in ml.check(spec).findings]
        self.assertEqual(r1, r2)

    # ── DSX-ML-052: baseline comparison's reported score provenance ─────────

    def test_score_sources_vocabulary_is_locked(self):
        self.assertEqual(
            ml.SCORE_SOURCES,
            frozenset({"cv_mean", "holdout", "nested_cv", "best_fold", "unknown"}),
        )

    def test_blank_score_source_produces_052_at_high(self):
        # D-05: DSX-ML-052
        spec = {**self.BASE, "results": {"model_score": 0.72, "baseline_score": 0.70}}
        report = ml.check(spec)
        found = [f for f in report.findings if f.code == "DSX-ML-052"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.HIGH)

    def test_best_fold_score_source_produces_052_at_high(self):
        spec = {
            **self.BASE,
            "results": {
                "model_score": 0.72, "baseline_score": 0.70,
                "model_score_source": "best_fold",
            },
        }
        self.assertIn("DSX-ML-052", codes(ml.check(spec)))

    def test_unknown_score_source_produces_052_at_high(self):
        spec = {
            **self.BASE,
            "results": {
                "model_score": 0.72, "baseline_score": 0.70,
                "model_score_source": "unknown",
            },
        }
        self.assertIn("DSX-ML-052", codes(ml.check(spec)))

    def test_misspelled_score_source_produces_052(self):
        # An unrecognised value is not a recognised one — a typo of an
        # accepted value must not buy silence.
        spec = {
            **self.BASE,
            "results": {
                "model_score": 0.72, "baseline_score": 0.70,
                "model_score_source": "cv_meen",
            },
        }
        self.assertIn("DSX-ML-052", codes(ml.check(spec)))

    def test_accepted_score_sources_produce_no_052(self):
        for source in ("cv_mean", "holdout", "nested_cv"):
            with self.subTest(source=source):
                spec = {
                    **self.BASE,
                    "results": {
                        "model_score": 0.72, "baseline_score": 0.70,
                        "model_score_source": source,
                    },
                }
                self.assertNotIn("DSX-ML-052", codes(ml.check(spec)))

    # ── DSX-ML-053: margin inside the model's own fold-to-fold variation ────

    def test_margin_smaller_than_fold_spread_produces_053_at_medium(self):
        # D-05: DSX-ML-053
        spec = {
            **self.BASE,
            "results": {
                "model_score": 0.72, "baseline_score": 0.70,
                "model_score_source": "cv_mean",
                "fold_scores": [0.66, 0.78],
            },
        }
        report = ml.check(spec)
        found = [f for f in report.findings if f.code == "DSX-ML-053"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.MEDIUM)
        detail = found[0].detail
        self.assertIn("0.02", detail)
        self.assertIn("0.12", detail)

    def test_margin_equal_to_fold_spread_produces_no_053(self):
        spec = {
            **self.BASE,
            "results": {
                "model_score": 0.72, "baseline_score": 0.70,
                "model_score_source": "cv_mean",
                "fold_scores": [0.70, 0.72],
            },
        }
        self.assertNotIn("DSX-ML-053", codes(ml.check(spec)))

    def test_margin_larger_than_fold_spread_produces_no_053(self):
        spec = {
            **self.BASE,
            "results": {
                "model_score": 0.72, "baseline_score": 0.70,
                "model_score_source": "cv_mean",
                "fold_scores": [0.715, 0.725],
            },
        }
        self.assertNotIn("DSX-ML-053", codes(ml.check(spec)))

    def test_single_fold_score_produces_no_053(self):
        spec = {
            **self.BASE,
            "results": {
                "model_score": 0.72, "baseline_score": 0.70,
                "model_score_source": "cv_mean",
                "fold_scores": [0.66],
            },
        }
        self.assertNotIn("DSX-ML-053", codes(ml.check(spec)))

    def test_empty_fold_scores_list_produces_no_053(self):
        spec = {
            **self.BASE,
            "results": {
                "model_score": 0.72, "baseline_score": 0.70,
                "model_score_source": "cv_mean",
                "fold_scores": [],
            },
        }
        self.assertNotIn("DSX-ML-053", codes(ml.check(spec)))

    def test_no_fold_scores_field_produces_no_053(self):
        spec = {
            **self.BASE,
            "results": {
                "model_score": 0.72, "baseline_score": 0.70,
                "model_score_source": "cv_mean",
            },
        }
        self.assertNotIn("DSX-ML-053", codes(ml.check(spec)))

    def test_non_numeric_fold_score_entry_is_skipped_not_raised(self):
        spec = {
            **self.BASE,
            "results": {
                "model_score": 0.72, "baseline_score": 0.70,
                "model_score_source": "cv_mean",
                "fold_scores": [0.66, "n/a", 0.78],
            },
        }
        found = codes(ml.check(spec))  # must not raise
        self.assertIn("DSX-ML-053", found)

    # ── Existing early returns and beat/not-beat branches are unchanged ─────

    def test_no_baseline_declared_produces_050_and_neither_new_code(self):
        spec = {**self.BASE, "model": self._model(baseline=None)}
        found = codes(ml.check(spec))
        self.assertIn("DSX-ML-050", found)
        self.assertNotIn("DSX-ML-052", found)
        self.assertNotIn("DSX-ML-053", found)

    def test_baseline_declared_scores_not_reported_produces_neither_new_code(self):
        spec = {**self.BASE, "results": {}}
        found = codes(ml.check(spec))
        self.assertNotIn("DSX-ML-050", found)
        self.assertNotIn("DSX-ML-052", found)
        self.assertNotIn("DSX-ML-053", found)

    def test_model_not_beating_baseline_produces_051_and_no_053(self):
        spec = {
            **self.BASE,
            "results": {
                "model_score": 0.61, "baseline_score": 0.63,
                "model_score_source": "cv_mean",
                "fold_scores": [0.60, 0.62],
            },
        }
        found = codes(ml.check(spec))
        self.assertIn("DSX-ML-051", found)
        self.assertNotIn("DSX-ML-052", found)
        self.assertNotIn("DSX-ML-053", found)

    # ── DSX-ML-090/091/092: selection ledger (REQ-P11.1-06) ──────────────────

    def test_selection_bases_vocabulary_is_locked(self):
        # Plan 11.1-07's acceptance criteria also assert
        # `not (SELECTION_BASES & SCORE_SOURCES)`, which is unsatisfiable as
        # written: SCORE_SOURCES already carries 'nested_cv' (shipped and
        # test-locked in plan 11.1-06's test_accepted_score_sources_produce_no_052),
        # and this plan's own <action> text and its embedded <automated>
        # verify commands require SELECTION_BASES to carry 'nested_cv' too —
        # the two vocabularies share one term for one concept ("a nested
        # cross-validation protocol") used in two different roles. Rewriting
        # SCORE_SOURCES to drop 'nested_cv' would break the prior plan's
        # shipped test, which this plan's own prohibitions forbid. See
        # 11.1-07-SUMMARY.md's Deviations section.
        self.assertEqual(
            ml.SELECTION_BASES,
            frozenset({"train", "validation", "test", "cv_same_fold", "nested_cv"}),
        )

    def test_algorithm_declared_no_ledger_key_produces_090_at_high(self):
        # D-05: DSX-ML-090
        spec = {**self.BASE, "model": self._model(algorithm="gradient_boosting")}
        report = ml.check(spec)
        found = [f for f in report.findings if f.code == "DSX-ML-090"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.HIGH)

    def test_algorithm_declared_empty_ledger_mapping_produces_090(self):
        spec = {
            **self.BASE,
            "model": self._model(algorithm="gradient_boosting", selection_ledger={}),
        }
        self.assertIn("DSX-ML-090", codes(ml.check(spec)))

    def test_empty_candidate_list_produces_090(self):
        spec = {
            **self.BASE,
            "model": self._model(
                algorithm="gradient_boosting",
                selection_ledger={
                    "candidates_evaluated": [],
                    "configurations_tried": 18,
                    "selected_on": "validation",
                },
            ),
        }
        self.assertIn("DSX-ML-090", codes(ml.check(spec)))

    def test_missing_configuration_count_key_produces_090(self):
        spec = {
            **self.BASE,
            "model": self._model(
                algorithm="gradient_boosting",
                selection_ledger={
                    "candidates_evaluated": ["a", "b"],
                    "selected_on": "validation",
                },
            ),
        }
        self.assertIn("DSX-ML-090", codes(ml.check(spec)))

    def test_configuration_count_zero_with_others_declared_produces_no_090(self):
        spec = {
            **self.BASE,
            "model": self._model(
                algorithm="gradient_boosting",
                selection_ledger={
                    "candidates_evaluated": ["a"],
                    "configurations_tried": 0,
                    "selected_on": "validation",
                },
            ),
        }
        self.assertNotIn("DSX-ML-090", codes(ml.check(spec)))

    def test_blank_selection_basis_produces_090(self):
        spec = {
            **self.BASE,
            "model": self._model(
                algorithm="gradient_boosting",
                selection_ledger={
                    "candidates_evaluated": ["a", "b"],
                    "configurations_tried": 18,
                    "selected_on": "",
                },
            ),
        }
        self.assertIn("DSX-ML-090", codes(ml.check(spec)))

    def test_misspelled_selection_basis_produces_090_not_a_bypass(self):
        # An unrecognised value is not a recognised one — a typo of an
        # accepted value must not clear DSX-ML-091's CRITICAL.
        spec = {
            **self.BASE,
            "model": self._model(
                algorithm="gradient_boosting",
                selection_ledger={
                    "candidates_evaluated": ["a", "b"],
                    "configurations_tried": 18,
                    "selected_on": "tset",
                },
            ),
        }
        self.assertIn("DSX-ML-090", codes(ml.check(spec)))

    def test_090_detail_names_each_missing_field_individually(self):
        spec = {
            **self.BASE,
            "model": self._model(
                algorithm="gradient_boosting",
                selection_ledger={"candidates_evaluated": ["a", "b"]},
            ),
        }
        report = ml.check(spec)
        found = next(f for f in report.findings if f.code == "DSX-ML-090")
        self.assertIn("configurations tried", found.detail)
        self.assertIn("selection basis", found.detail)
        self.assertNotIn("candidates evaluated", found.detail)

    def test_complete_ledger_selected_on_test_produces_091_at_critical_not_090(self):
        # D-05: DSX-ML-091
        spec = {
            **self.BASE,
            "model": self._model(
                algorithm="gradient_boosting",
                selection_ledger={
                    "candidates_evaluated": ["a", "b"],
                    "configurations_tried": 18,
                    "selected_on": "test",
                },
            ),
        }
        report = ml.check(spec)
        found = [f for f in report.findings if f.code == "DSX-ML-091"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.CRITICAL)
        self.assertNotIn("DSX-ML-090", codes(report))

    def test_complete_ledger_selected_on_same_folds_produces_092_at_high_not_090_or_091(self):
        # D-05: DSX-ML-092
        spec = {
            **self.BASE,
            "model": self._model(
                algorithm="gradient_boosting",
                selection_ledger={
                    "candidates_evaluated": ["a", "b"],
                    "configurations_tried": 18,
                    "selected_on": "cv_same_fold",
                },
            ),
        }
        report = ml.check(spec)
        found = [f for f in report.findings if f.code == "DSX-ML-092"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.HIGH)
        found_codes = codes(report)
        self.assertNotIn("DSX-ML-090", found_codes)
        self.assertNotIn("DSX-ML-091", found_codes)

    def test_complete_ledger_selected_on_nested_validation_or_train_produces_none_of_three(self):
        for basis in ("nested_cv", "validation", "train"):
            with self.subTest(basis=basis):
                spec = {
                    **self.BASE,
                    "model": self._model(
                        algorithm="gradient_boosting",
                        selection_ledger={
                            "candidates_evaluated": ["a", "b"],
                            "configurations_tried": 18,
                            "selected_on": basis,
                        },
                    ),
                }
                report = ml.check(spec)
                found_codes = codes(report)
                self.assertNotIn("DSX-ML-090", found_codes)
                self.assertNotIn("DSX-ML-091", found_codes)
                self.assertNotIn("DSX-ML-092", found_codes)
                self.assertTrue(any(basis in ok for ok in report.passed_checks))

    def test_blank_algorithm_produces_none_of_three_codes_regardless_of_ledger(self):
        spec = {
            **self.BASE,
            "model": self._model(algorithm=None, selection_ledger={}),
        }
        found_codes = codes(ml.check(spec))
        self.assertNotIn("DSX-ML-090", found_codes)
        self.assertNotIn("DSX-ML-091", found_codes)
        self.assertNotIn("DSX-ML-092", found_codes)

    def test_ledger_declared_as_a_list_is_treated_as_no_ledger(self):
        spec = {
            **self.BASE,
            "model": self._model(algorithm="gradient_boosting", selection_ledger=["a"]),
        }
        found = codes(ml.check(spec))  # must not raise
        self.assertIn("DSX-ML-090", found)

    def test_two_consecutive_calls_over_ledger_spec_produce_identical_finding_sequences(self):
        spec = {
            **self.BASE,
            "model": self._model(
                algorithm="gradient_boosting",
                selection_ledger={
                    "candidates_evaluated": ["a", "b"],
                    "configurations_tried": 18,
                    "selected_on": "test",
                },
            ),
        }
        r1 = [f.code for f in ml.check(spec).findings]
        r2 = [f.code for f in ml.check(spec).findings]
        self.assertEqual(r1, r2)

    # ── Plan 11.1-07 backstop truth, resolved at UAT (11.1-UAT.md, test 1) ──
    #
    # Plan 11.1-07 carried a `verification: backstop` truth reading "When more
    # than one selection-ledger condition holds at once, the findings
    # DSX-ML-090, DSX-ML-091 and DSX-ML-092 are emitted in a stable order across
    # repeated runs". Reading _check_selection_ledger shows that scenario cannot
    # arise: the three codes hang off a single if/elif/elif/else chain, so at
    # most one of them fires per report and there is no order to stabilise. The
    # truth is vacuously satisfied.
    #
    # The two tests below pin the invariant that makes it vacuous. A future edit
    # splitting that chain into independent `if` statements would turn emission
    # order into a real, unpinned question; it fails here instead of changing
    # behaviour silently.

    def test_at_most_one_selection_ledger_code_fires_across_the_branch_space(self):
        ledger_codes = ("DSX-ML-090", "DSX-ML-091", "DSX-ML-092")
        # Every basis in the locked vocabulary, plus blank, whitespace, a
        # differently-cased member, an out-of-vocabulary misspelling, and the
        # field being absent altogether.
        bases = sorted(ml.SELECTION_BASES) + ["", "   ", "Test", "tset", None]
        for algorithm in ("gradient_boosting", None):
            for candidates in (["a", "b"], [], None):
                for configurations in (18, 0, None):
                    for basis in bases:
                        ledger: dict = {}
                        if candidates is not None:
                            ledger["candidates_evaluated"] = candidates
                        if configurations is not None:
                            ledger["configurations_tried"] = configurations
                        if basis is not None:
                            ledger["selected_on"] = basis
                        spec = {
                            **self.BASE,
                            "model": self._model(
                                algorithm=algorithm, selection_ledger=ledger
                            ),
                        }
                        with self.subTest(
                            algorithm=algorithm,
                            candidates=candidates,
                            configurations=configurations,
                            basis=basis,
                        ):
                            emitted = [
                                f.code
                                for f in ml.check(spec).findings
                                if f.code in ledger_codes
                            ]
                            self.assertLessEqual(
                                len(emitted),
                                1,
                                f"expected at most one selection-ledger code, got {emitted}",
                            )

    def test_incomplete_ledger_selected_on_test_emits_only_090(self):
        # The exact "more than one condition holds at once" case the backstop
        # truth names: the ledger is incomplete (DSX-ML-090's condition) while
        # the declared basis is the test set (DSX-ML-091's condition). The elif
        # chain resolves it to DSX-ML-090 alone, so no ordering question arises.
        ledger_codes = ("DSX-ML-090", "DSX-ML-091", "DSX-ML-092")
        spec = {
            **self.BASE,
            "model": self._model(
                algorithm="gradient_boosting",
                selection_ledger={"selected_on": "test"},
            ),
        }
        emitted = [
            f.code for f in ml.check(spec).findings if f.code in ledger_codes
        ]
        self.assertEqual(emitted, ["DSX-ML-090"])


# ── Phase 11.1 plan 05: per-step cleaning boundary (DSX-ML-023/024) ────────────


class TestPhase11_1MLCleaning(unittest.TestCase):
    # Derived from TestML.BASE (REQ-P11.1-03's plan instruction).
    BASE = TestML.BASE

    def _model(self, **overrides):
        model = {k: v for k, v in self.BASE["model"].items()}
        model.update(overrides)
        for key, value in list(model.items()):
            if value is None:
                del model[key]
        return model

    def _leaky_dataset(self, fit_on="all_data", column="Age", method="mean_impute", name="churn"):
        return {
            "name": name,
            "cleaning": [{"column": column, "method": method, "fit_on": fit_on}],
        }

    # ── DSX-ML-023: leaky per-step cleaning boundary ─────────────────────────

    def test_leaky_cleaning_step_produces_023_at_critical(self):
        # D-05: DSX-ML-023
        spec = {
            "question_type": "predictive",
            "data": [self._leaky_dataset()],
            "model": self._model(preprocessing_fit_on=None),
        }
        report = ml.check(spec)
        found = [f for f in report.findings if f.code == "DSX-ML-023"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.CRITICAL)

    def test_leaky_cleaning_with_train_only_whole_pipeline_also_produces_024_at_high(self):
        # D-05: DSX-ML-024
        spec = {
            "question_type": "predictive",
            "data": [self._leaky_dataset()],
            "model": self._model(preprocessing_fit_on="train_only"),
        }
        report = ml.check(spec)
        found = codes(report)
        self.assertIn("DSX-ML-023", found)
        self.assertIn("DSX-ML-024", found)
        fired_024 = next(f for f in report.findings if f.code == "DSX-ML-024")
        self.assertEqual(fired_024.severity, Severity.HIGH)

    def test_leaky_cleaning_with_no_whole_pipeline_boundary_produces_023_not_024(self):
        spec = {
            "question_type": "predictive",
            "data": [self._leaky_dataset()],
            "model": self._model(preprocessing_fit_on=None),
        }
        found = codes(ml.check(spec))
        self.assertIn("DSX-ML-023", found)
        self.assertNotIn("DSX-ML-024", found)

    def test_accepted_fit_boundary_produces_neither_code(self):
        spec = {
            "question_type": "predictive",
            "data": [self._leaky_dataset(fit_on="train_only")],
            "model": self._model(preprocessing_fit_on="train_only"),
        }
        found = codes(ml.check(spec))
        self.assertNotIn("DSX-ML-023", found)
        self.assertNotIn("DSX-ML-024", found)

    def test_misspelled_fit_boundary_produces_023(self):
        spec = {
            "question_type": "predictive",
            "data": [self._leaky_dataset(fit_on="train_onlyy")],
            "model": self._model(preprocessing_fit_on="train_only"),
        }
        self.assertIn("DSX-ML-023", codes(ml.check(spec)))

    def test_missing_fit_on_key_produces_neither_code(self):
        dataset = {"name": "churn", "cleaning": [{"column": "Age", "method": "mean_impute"}]}
        spec = {"question_type": "predictive", "data": [dataset], "model": self._model()}
        found = codes(ml.check(spec))
        self.assertNotIn("DSX-ML-023", found)
        self.assertNotIn("DSX-ML-024", found)

    def test_blank_fit_on_produces_neither_code(self):
        spec = {
            "question_type": "predictive",
            "data": [self._leaky_dataset(fit_on="   ")],
            "model": self._model(preprocessing_fit_on="train_only"),
        }
        found = codes(ml.check(spec))
        self.assertNotIn("DSX-ML-023", found)
        self.assertNotIn("DSX-ML-024", found)

    def test_no_data_section_produces_neither_code_and_no_ok_line(self):
        spec = {"question_type": "predictive", "model": self._model()}
        report = ml.check(spec)
        found = codes(report)
        self.assertNotIn("DSX-ML-023", found)
        self.assertNotIn("DSX-ML-024", found)
        self.assertFalse(any("cleaning" in ok.lower() for ok in report.passed_checks))

    def test_empty_data_list_produces_neither_code(self):
        spec = {"question_type": "predictive", "data": [], "model": self._model()}
        found = codes(ml.check(spec))
        self.assertNotIn("DSX-ML-023", found)
        self.assertNotIn("DSX-ML-024", found)

    def test_dataset_with_no_cleaning_key_produces_neither_code(self):
        spec = {
            "question_type": "predictive",
            "data": [{"name": "churn", "source": "warehouse.churn"}],
            "model": self._model(),
        }
        found = codes(ml.check(spec))
        self.assertNotIn("DSX-ML-023", found)
        self.assertNotIn("DSX-ML-024", found)

    def test_leaky_cleaning_with_no_model_section_still_produces_023(self):
        spec = {"question_type": "predictive", "data": [self._leaky_dataset()]}
        self.assertIn("DSX-ML-023", codes(ml.check(spec)))

    def test_non_mapping_cleaning_element_does_not_raise(self):
        dataset = {"name": "churn", "cleaning": ["not_a_mapping", 42, None]}
        spec = {"question_type": "predictive", "data": [dataset], "model": self._model()}
        found = codes(ml.check(spec))  # must not raise
        self.assertNotIn("DSX-ML-023", found)
        self.assertNotIn("DSX-ML-024", found)

    def test_two_leaky_steps_in_two_datasets_produce_two_023_and_one_024(self):
        spec = {
            "question_type": "predictive",
            "data": [
                self._leaky_dataset(column="Age", name="churn"),
                self._leaky_dataset(column="Income", name="orders"),
            ],
            "model": self._model(preprocessing_fit_on="train_only"),
        }
        report = ml.check(spec)
        findings_023 = [f for f in report.findings if f.code == "DSX-ML-023"]
        findings_024 = [f for f in report.findings if f.code == "DSX-ML-024"]
        self.assertEqual(len(findings_023), 2)
        self.assertEqual(len(findings_024), 1)
        datasets_named = {f.data.get("dataset") for f in findings_023}
        columns_named = {f.data.get("column") for f in findings_023}
        self.assertEqual(datasets_named, {"churn", "orders"})
        self.assertEqual(columns_named, {"Age", "Income"})

    def test_train_only_fit_values_is_shared_by_both_checks(self):
        import inspect

        self.assertEqual(
            ml.TRAIN_ONLY_FIT_VALUES, frozenset({"train_only", "train_fold_only", "none"})
        )
        self.assertIn("TRAIN_ONLY_FIT_VALUES", inspect.getsource(ml._check_preprocessing))
        self.assertIn("TRAIN_ONLY_FIT_VALUES", inspect.getsource(ml._check_cleaning))

    def test_check_cleaning_wired_into_dispatch(self):
        import inspect

        self.assertIn("_check_cleaning", inspect.getsource(ml.check))


# ── stats ────────────────────────────────────────────────────────────────────


class TestStats(unittest.TestCase):
    def test_test_selection_table(self):
        self.assertEqual(stats.recommend_test("proportion", 2)["test"], "two_proportion_z")
        self.assertEqual(stats.recommend_test("proportion", 2, paired=True)["test"], "mcnemar")
        self.assertEqual(stats.recommend_test("proportion", 4)["test"], "chi_square")
        self.assertEqual(
            stats.recommend_test("continuous", 2, normal=True, equal_variance=False)["test"],
            "welch_t",
        )
        self.assertEqual(
            stats.recommend_test("continuous", 2, normal=False, n_per_group=30)["test"],
            "mann_whitney",
        )
        self.assertEqual(
            stats.recommend_test("continuous", 2, paired=True, normal=True)["test"], "paired_t"
        )
        self.assertEqual(
            stats.recommend_test("continuous", 3, normal=True, equal_variance=True)["test"], "anova"
        )
        self.assertEqual(
            stats.recommend_test("continuous", 3, normal=False, n_per_group=20)["test"],
            "kruskal_wallis",
        )
        self.assertEqual(
            stats.recommend_test("count", 2, overdispersed=True)["test"],
            "negative_binomial_regression",
        )
        self.assertEqual(stats.recommend_test("time_to_event", 2)["test"], "log_rank")

    def test_clt_rescues_non_normality_at_large_n(self):
        self.assertEqual(
            stats.recommend_test("continuous", 2, normal=None, n_per_group=5000)["test"], "welch_t"
        )

    def test_unknown_outcome_type_raises(self):
        with self.assertRaises(ValueError):
            stats.recommend_test("nonsense", 2)

    def test_p_value_without_effect_or_ci_flagged(self):
        spec = {"results": {"tests": [{"metric": "cr", "p_value": 0.03}]}}
        report = stats.check(spec)
        self.assertIn("DSX-STA-002", codes(report))
        self.assertIn("DSX-STA-003", codes(report))

    def test_complete_result_passes(self):
        spec = {"results": {"tests": [{"metric": "cr", "p_value": 0.03, "effect": 0.021,
                                       "ci": [0.002, 0.040]}]}}
        report = stats.check(spec)
        self.assertNotIn("DSX-STA-002", codes(report))
        self.assertNotIn("DSX-STA-003", codes(report))

    def test_effect_outside_its_own_ci_flagged(self):
        spec = {"results": {"tests": [{"metric": "cr", "p_value": 0.03, "effect": 0.5,
                                       "ci": [0.002, 0.040]}]}}
        self.assertIn("DSX-STA-005", codes(stats.check(spec)))

    def test_significant_but_ci_spans_null_flagged(self):
        spec = {"results": {"tests": [{"metric": "cr", "p_value": 0.01, "effect": 0.01,
                                       "ci": [-0.01, 0.03]}]}}
        self.assertIn("DSX-STA-006", codes(stats.check(spec)))

    def test_null_accepted_without_equivalence_test_flagged(self):
        spec = {"results": {"tests": [{"metric": "cr", "p_value": 0.42, "effect": 0.001,
                                       "ci": [-0.01, 0.012],
                                       "interpretation": "no difference between arms"}]}}
        self.assertIn("DSX-STA-020", codes(stats.check(spec)))

    def test_equivalence_bound_satisfies_null_claim(self):
        spec = {"results": {"tests": [{"metric": "cr", "p_value": 0.42, "effect": 0.001,
                                       "ci": [-0.01, 0.012], "equivalence_bound": 0.02,
                                       "interpretation": "no difference between arms"}]}}
        found = codes(stats.check(spec))
        self.assertNotIn("DSX-STA-020", found)
        self.assertNotIn("DSX-STA-021", found)

    def test_equivalence_bound_without_ci_proof_flagged(self):
        spec = {"results": {"tests": [{"metric": "cr", "p_value": 0.42, "effect": 0.05,
                                       "ci": [-0.01, 0.12], "equivalence_bound": 0.02,
                                       "interpretation": "no difference between arms"}]}}
        found = codes(stats.check(spec))
        self.assertIn("DSX-STA-021", found)
        self.assertNotIn("DSX-STA-020", found)

    def test_detectable_mde_escapes_null_claim(self):
        spec = {"results": {"tests": [{"metric": "cr", "p_value": 0.42, "effect": 0.001,
                                       "ci": [-0.01, 0.012], "detectable_mde": 0.05,
                                       "interpretation": "no difference between arms"}]}}
        self.assertNotIn("DSX-STA-020", codes(stats.check(spec)))

    def test_correction_flips_significance(self):
        spec = {
            "design": {"alpha": 0.05, "multiplicity": {"correction": "bonferroni"}},
            "results": {"tests": [
                {"metric": "a", "p_value": 0.04, "effect": 0.01, "ci": [0.001, 0.02]},
                {"metric": "b", "p_value": 0.045, "effect": 0.01, "ci": [0.001, 0.02]},
                {"metric": "c", "p_value": 0.048, "effect": 0.01, "ci": [0.001, 0.02]},
            ]},
        }
        report = stats.check(spec)
        self.assertIn("DSX-STA-031", codes(report))
        self.assertEqual(len(next(f for f in report.findings
                                  if f.code == "DSX-STA-031").data["flipped_indices"]), 3)

    def test_declared_test_mismatch_flagged(self):
        spec = {"analysis": {"outcome_type": "proportion", "n_groups": 2, "test": "welch_t"}}
        report = stats.check(spec)
        self.assertIn("DSX-STA-041", codes(report))

    def test_declared_test_match_passes(self):
        spec = {"analysis": {"outcome_type": "proportion", "n_groups": 2,
                             "test": "two_proportion_z", "normality_ok": True,
                             "equal_variance": True, "independence_ok": True}}
        self.assertNotIn("DSX-STA-041", codes(stats.check(spec)))

    def test_violated_independence_blocks(self):
        spec = {"analysis": {"outcome_type": "continuous", "n_groups": 2, "test": "welch_t",
                             "normality_ok": True, "equal_variance": False,
                             "independence_ok": False}}
        self.assertIn("DSX-STA-043", codes(stats.check(spec)))

    def test_significant_but_trivial_effect_flagged(self):
        spec = {"design": {"alpha": 0.05},
                "results": {"tests": [{"metric": "cr", "p_value": 0.001, "effect": 0.0004,
                                       "ci": [0.0001, 0.0007],
                                       "minimum_practical_effect": 0.01}]}}
        self.assertIn("DSX-STA-010", codes(stats.check(spec)))


# ── metrics ──────────────────────────────────────────────────────────────────


class TestMetrics(unittest.TestCase):
    def test_undefined_referenced_metric_flagged(self):
        spec = {"metrics": [{"name": "activation_rate"}],
                "results": {"tests": [{"metric": "retention_d7"}]}}
        self.assertIn("DSX-MET-001", codes(metrics.check(spec)))

    def test_reconciliation_gap_beyond_tolerance_flagged(self):
        spec = {"metrics": [{"name": "revenue", "reconciliation": {
            "tolerance": 0.01,
            "sources": [{"name": "warehouse", "value": 1_000_000},
                        {"name": "finance", "value": 1_080_000}]}}]}
        report = metrics.check(spec)
        self.assertIn("DSX-MET-011", codes(report))

    def test_reconciliation_within_tolerance_passes(self):
        spec = {"metrics": [{"name": "revenue", "reconciliation": {
            "tolerance": 0.02,
            "sources": [{"name": "warehouse", "value": 1_000_000},
                        {"name": "finance", "value": 1_005_000}]}}]}
        self.assertNotIn("DSX-MET-011", codes(metrics.check(spec)))

    def test_simpsons_paradox_detected(self):
        spec = {"results": {"overall_effect": -0.03,
                            "segments": [{"name": "mobile", "effect": 0.02},
                                         {"name": "desktop", "effect": 0.015},
                                         {"name": "tablet", "effect": 0.008}]}}
        report = metrics.check(spec)
        self.assertIn("DSX-MET-030", codes(report))
        self.assertTrue(report.blocks(Severity.CRITICAL))

    def test_consistent_segments_pass(self):
        spec = {"results": {"overall_effect": 0.03,
                            "segments": [{"name": "mobile", "effect": 0.02},
                                         {"name": "desktop", "effect": 0.04}]}}
        self.assertNotIn("DSX-MET-030", codes(metrics.check(spec)))

    def test_denominator_drift_flagged(self):
        spec = {"results": {"period_comparisons": [
            {"metric": "cr", "base_denominator": 100_000, "comparison_denominator": 140_000}]}}
        self.assertIn("DSX-MET-020", codes(metrics.check(spec)))

    def test_sql_fanout_detected(self):
        spec = {"metrics": [{"name": "rev", "sql":
                             "SELECT SUM(o.amount) FROM orders o "
                             "JOIN items i ON i.order_id = o.id "
                             "JOIN users u ON u.id = o.user_id"}]}
        self.assertIn("DSX-SQL-010", codes(metrics.check(spec)))

    def test_not_in_subquery_detected(self):
        spec = {"metrics": [{"name": "x", "sql":
                             "SELECT id FROM users WHERE id NOT IN (SELECT user_id FROM churn)"}]}
        self.assertIn("DSX-SQL-001", codes(metrics.check(spec)))

    def test_average_of_ratio_detected(self):
        spec = {"metrics": [{"name": "x", "sql": "SELECT AVG(clicks / impressions) FROM ads"}]}
        self.assertIn("DSX-SQL-004", codes(metrics.check(spec)))

    def test_sql_comments_do_not_trigger_rules(self):
        spec = {"metrics": [{"name": "x", "sql": "-- NOT IN (SELECT ...) was removed\nSELECT 1"}]}
        self.assertNotIn("DSX-SQL-001", codes(metrics.check(spec)))


# ── claims ───────────────────────────────────────────────────────────────────


class TestClaims(unittest.TestCase):
    def test_causal_verb_in_association_claim_blocks(self):
        spec = {"claims": [{"text": "The new onboarding drives a 12% lift in activation",
                            "type": "association", "evidence": "R.md#1"}]}
        report = claims.check(spec)
        self.assertIn("DSX-CLM-011", codes(report))
        self.assertTrue(report.blocks(Severity.CRITICAL))

    def test_association_wording_passes(self):
        spec = {"claims": [{"text": "Completing onboarding is associated with higher activation",
                            "type": "association", "evidence": "R.md#1"}]}
        self.assertNotIn("DSX-CLM-011", codes(claims.check(spec)))

    def test_causal_claim_without_identification_blocks(self):
        spec = {"design": {"kind": "observational", "identification": "none"},
                "claims": [{"text": "Onboarding causes a 12% lift", "type": "causal",
                            "evidence": "R.md#1"}]}
        self.assertIn("DSX-CLM-020", codes(claims.check(spec)))

    def test_causal_claim_from_experiment_passes(self):
        spec = {"design": {"kind": "experiment"},
                "claims": [{"text": "Onboarding causes a 12% lift", "type": "causal",
                            "evidence": "R.md#1"}]}
        report = claims.check(spec)
        self.assertNotIn("DSX-CLM-020", codes(report))
        self.assertNotIn("DSX-CLM-011", codes(report))

    def test_unhedged_matching_claim_flagged(self):
        spec = {"design": {"kind": "observational", "identification": "matching"},
                "claims": [{"text": "The programme increases retention by 4pp", "type": "causal",
                            "evidence": "R.md#1"}]}
        self.assertIn("DSX-CLM-021", codes(claims.check(spec)))

    def test_missing_evidence_pointer_flagged(self):
        spec = {"claims": [{"text": "Revenue grew 8%", "type": "descriptive"}]}
        self.assertIn("DSX-CLM-030", codes(claims.check(spec)))

    def test_predictive_claim_without_test_score_flagged(self):
        spec = {"model": {"task": "binary_classification"},
                "claims": [{"text": "The model identifies at-risk accounts", "type": "predictive",
                            "evidence": "R.md#1"}]}
        self.assertIn("DSX-CLM-041", codes(claims.check(spec)))

    def test_overbroad_generalisation_flagged(self):
        spec = {"data": [{"name": "d"}],
                "claims": [{"text": "All users prefer the new layout", "type": "descriptive",
                            "evidence": "R.md#1"}]}
        self.assertIn("DSX-CLM-050", codes(claims.check(spec)))

    def test_false_precision_flagged(self):
        spec = {"claims": [{"text": "Uplift was 2.4173% across the cohort", "type": "descriptive",
                            "evidence": "R.md#1", "ci": [0.5, 4.5]}]}
        self.assertIn("DSX-CLM-060", codes(claims.check(spec)))


# ── viz ──────────────────────────────────────────────────────────────────────


class TestViz(unittest.TestCase):
    GOOD = {"visuals": [{"name": "activation by cohort", "relationship": "comparison",
                         "type": "bar", "y_axis_starts_at_zero": True, "units": "%",
                         "takeaway": "March cohort activates 9pp below every other cohort",
                         "category_order": "by_value", "source": "warehouse, 2026-01..06"}]}

    def test_good_chart_passes(self):
        report = viz.check(self.GOOD)
        self.assertFalse(report.blocks(Severity.HIGH), report.render(Severity.HIGH))

    def test_truncated_bar_axis_blocks(self):
        spec = {"visuals": [{**self.GOOD["visuals"][0], "y_axis_starts_at_zero": False,
                             "y_axis_min": 40}]}
        report = viz.check(spec)
        self.assertIn("DSX-VIZ-020", codes(report))
        self.assertTrue(report.blocks(Severity.CRITICAL))

    def test_truncated_line_axis_is_fine(self):
        spec = {"visuals": [{"name": "trend", "relationship": "trend", "type": "line",
                             "y_axis_starts_at_zero": False, "y_axis_min": 40, "units": "%",
                             "takeaway": "t", "source": "s"}]}
        self.assertNotIn("DSX-VIZ-020", codes(viz.check(spec)))

    def test_wrong_chart_for_relationship_flagged(self):
        spec = {"visuals": [{**self.GOOD["visuals"][0], "relationship": "distribution",
                             "type": "pie"}]}
        self.assertIn("DSX-VIZ-012", codes(viz.check(spec)))

    def test_dual_axis_flagged(self):
        spec = {"visuals": [{**self.GOOD["visuals"][0], "dual_axis": True}]}
        self.assertIn("DSX-VIZ-030", codes(viz.check(spec)))

    def test_too_many_pie_slices_flagged(self):
        spec = {"visuals": [{"name": "mix", "relationship": "part_to_whole", "type": "pie",
                             "category_count": 11, "units": "%", "takeaway": "t", "source": "s"}]}
        self.assertIn("DSX-VIZ-040", codes(viz.check(spec)))

    def test_red_green_only_flagged(self):
        spec = {"visuals": [{**self.GOOD["visuals"][0], "palette": "red_green"}]}
        self.assertIn("DSX-VIZ-051", codes(viz.check(spec)))

    def test_estimates_without_uncertainty_flagged(self):
        spec = {"visuals": [{**self.GOOD["visuals"][0], "shows_estimates": True}]}
        self.assertIn("DSX-VIZ-070", codes(viz.check(spec)))

    def test_missing_units_flagged(self):
        spec = {"visuals": [{**self.GOOD["visuals"][0], "units": None}]}
        self.assertIn("DSX-VIZ-061", codes(viz.check(spec)))

    def test_banned_3d_chart_flagged(self):
        spec = {"visuals": [{**self.GOOD["visuals"][0], "type": "3d_bar"}]}
        self.assertIn("DSX-VIZ-001", codes(viz.check(spec)))


# ── repro ────────────────────────────────────────────────────────────────────


class TestRepro(unittest.TestCase):
    def test_stochastic_model_without_seed_flagged(self):
        spec = {"model": {"algorithm": "gradient_boosting", "task": "binary_classification"},
                "reproducibility": {"entrypoint": "train.py", "lockfile": "uv.lock"}}
        self.assertIn("DSX-REP-001", codes(repro.check(spec)))

    def test_seed_present_passes(self):
        spec = {"model": {"algorithm": "gradient_boosting"},
                "reproducibility": {"random_seed": 42, "entrypoint": "train.py",
                                    "lockfile": "uv.lock", "language_version": "3.12"}}
        self.assertNotIn("DSX-REP-001", codes(repro.check(spec)))

    def test_missing_entrypoint_flagged(self):
        self.assertIn("DSX-REP-030", codes(repro.check({"reproducibility": {}})))

    def test_unpinned_environment_flagged(self):
        spec = {"reproducibility": {"entrypoint": "a.py"}}
        self.assertIn("DSX-REP-010", codes(repro.check(spec)))

    def test_unpinned_data_flagged(self):
        spec = {"data": [{"name": "events", "source": "t"}],
                "reproducibility": {"entrypoint": "a.py", "lockfile": "l"}}
        self.assertIn("DSX-REP-020", codes(repro.check(spec)))

    def test_notebook_without_clean_run_flagged(self):
        spec = {"reproducibility": {"entrypoint": "analysis.ipynb", "lockfile": "l"}}
        self.assertIn("DSX-REP-040", codes(repro.check(spec)))

    def test_missing_entrypoint_file_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = {"reproducibility": {"entrypoint": "nope.py", "lockfile": "l"}}
            self.assertIn("DSX-REP-031", codes(repro.check(spec, phase_dir=tmp)))


# ── CLI end to end ───────────────────────────────────────────────────────────


class TestCLI(unittest.TestCase):
    ROOT = Path(__file__).resolve().parent.parent

    def _run(self, argv: list[str]) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_good_fixture_passes_every_gate(self):
        fixture = self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml"
        for point in ("plan", "execute", "verify", "ship"):
            code, _, err = self._run(["gate", point, "--spec", str(fixture)])
            self.assertEqual(code, 0, f"gate {point} unexpectedly blocked:\n{err}")

    def test_bad_fixture_blocks_at_plan(self):
        fixture = self.ROOT / "examples" / "bad-ANALYSIS-SPEC.yaml"
        code, _, err = self._run(["gate", "plan", "--spec", str(fixture)])
        self.assertEqual(code, 1)
        self.assertIn("DSX-", err)

    def test_bad_fixture_blocks_at_ship(self):
        fixture = self.ROOT / "examples" / "bad-ANALYSIS-SPEC.yaml"
        # Seeded explicitly, rather than relying on an alphabetically earlier
        # test (test_bad_fixture_blocks_at_plan) to have already run `gate
        # plan` and written a header into examples/DECISIONS.jsonl — Phase
        # 10's prereg check makes a missing plan-time header a hard exit-2
        # precondition at ship, and this test should not depend on ordering.
        seed_plan_header(str(self.ROOT / "examples"), fixture)
        code, _, _ = self._run(["gate", "ship", "--spec", str(fixture)])
        self.assertEqual(code, 1)

    def test_missing_spec_is_an_error_not_a_block(self):
        code, _, err = self._run(["gate", "plan", "--spec", "/nonexistent/spec.yaml"])
        self.assertEqual(code, 2)
        self.assertIn("dsx:", err)

    def test_allow_missing_skips_cleanly(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out, _ = self._run(["gate", "plan", "--phase-dir", tmp, "--allow-missing"])
            self.assertEqual(code, 0)
            self.assertIn("skipping", out)

    def test_json_output_is_parseable(self):
        import json

        fixture = self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml"
        _, out, _ = self._run(["audit", "--spec", str(fixture), "--json"])
        payload = json.loads(out)
        self.assertIn("findings", payload)
        self.assertIn("counts", payload)
        self.assertIs(payload["block"], False)

    def test_report_file_is_written(self):
        fixture = self.ROOT / "examples" / "bad-ANALYSIS-SPEC.yaml"
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "DATA-REVIEW.md"
            self._run(["audit", "--spec", str(fixture), "--report", str(target)])
            text = target.read_text(encoding="utf-8")
            self.assertIn("# dsx report", text)
            self.assertIn("BLOCKED", text)

    def test_template_validates_structurally_as_a_scaffold(self):
        # The template ships with placeholders, so it must NOT pass — proving the
        # gate cannot be satisfied by shipping the unedited scaffold.
        template = self.ROOT / "templates" / "ANALYSIS-SPEC.yaml"
        # No `dsx gate plan` has ever run against templates/, so a plan-time
        # header must be seeded before ship — otherwise prereg's missing-
        # header CheckError would abort at exit 2 and silently satisfy this
        # assertEqual(code, 1) for the wrong reason. Seeding keeps the point
        # of the test — the unedited scaffold blocks on its own merits —
        # exactly what is proved.
        seed_plan_header(str(self.ROOT / "templates"), template)
        code, _, _ = self._run(["gate", "ship", "--spec", str(template)])
        self.assertEqual(code, 1)

    def test_recommend_test_cli(self):
        code, out, _ = self._run(["recommend-test", "proportion", "--groups", "2"])
        self.assertEqual(code, 0)
        self.assertIn("two_proportion_z", out)

    def test_power_cli(self):
        code, out, _ = self._run(["power", "--baseline", "0.3", "--mde", "0.02"])
        self.assertEqual(code, 0)
        self.assertIn("required_n_per_arm", out)

    def test_mixed_project_phase_dirs_behave_correctly(self):
        """The real usage path: gates resolve the spec from --phase-dir.

        An analytical phase with a sound spec passes; one with a defective spec
        blocks; a non-analytical phase with no spec passes through untouched.
        """
        import shutil

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            good_phase = root / "phases" / "03-readout"
            bad_phase = root / "phases" / "04-model"
            plain_phase = root / "phases" / "05-etl"
            for phase in (good_phase, bad_phase, plain_phase):
                phase.mkdir(parents=True)

            shutil.copy(
                self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml",
                good_phase / "ANALYSIS-SPEC.yaml",
            )
            shutil.copy(
                self.ROOT / "examples" / "good-DATA-PROFILE.yaml",
                good_phase / "good-DATA-PROFILE.yaml",
            )
            shutil.copy(
                self.ROOT / "examples" / "RESULTS.md",
                good_phase / "RESULTS.md",
            )
            shutil.copy(
                self.ROOT / "examples" / "good-FIGURE-MANIFEST.yaml",
                good_phase / "good-FIGURE-MANIFEST.yaml",
            )
            shutil.copy(
                self.ROOT / "examples" / "good-NARRATIVE.md",
                good_phase / "good-NARRATIVE.md",
            )
            shutil.copytree(
                self.ROOT / "examples" / "figures",
                good_phase / "figures",
            )
            charts = good_phase / "analysis" / "charts.py"
            charts.parent.mkdir(parents=True)
            charts.write_text("# charts\n", encoding="utf-8")
            # The good spec declares an entrypoint; with --phase-dir it is resolved
            # on disk, so it has to exist.
            entrypoint = good_phase / "analysis" / "activation_readout.py"
            entrypoint.write_text("# readout\n", encoding="utf-8")
            (good_phase / "analysis" / "requirements.lock").write_text("#\n", encoding="utf-8")
            shutil.copy(
                self.ROOT / "examples" / "bad-ANALYSIS-SPEC.yaml",
                bad_phase / "ANALYSIS-SPEC.yaml",
            )
            shutil.copy(
                self.ROOT / "examples" / "bad-DATA-PROFILE.yaml",
                bad_phase / "bad-DATA-PROFILE.yaml",
            )
            shutil.copy(
                self.ROOT / "examples" / "bad-NARRATIVE.md",
                bad_phase / "bad-NARRATIVE.md",
            )
            leaky = bad_phase / "analysis" / "leaky_model.py"
            leaky.parent.mkdir(parents=True)
            shutil.copy(
                self.ROOT / "examples" / "analysis" / "leaky_model.py",
                leaky,
            )
            (bad_phase / "analysis" / "requirements.lock").write_text("#\n", encoding="utf-8")

            for point in ("plan", "execute", "verify", "ship"):
                code, _, err = self._run(
                    ["gate", point, "--phase-dir", str(good_phase), "--allow-missing"]
                )
                self.assertEqual(code, 0, f"sound phase blocked at {point}:\n{err}")

                code, _, _ = self._run(
                    ["gate", point, "--phase-dir", str(bad_phase), "--allow-missing"]
                )
                self.assertEqual(code, 1, f"defective phase passed at {point}")

                code, out, _ = self._run(
                    ["gate", point, "--phase-dir", str(plain_phase), "--allow-missing"]
                )
                self.assertEqual(code, 0, f"non-analytical phase blocked at {point}")
                self.assertIn("skipping", out)

    def test_missing_entrypoint_blocks_when_phase_dir_given(self):
        import shutil

        with tempfile.TemporaryDirectory() as tmp:
            phase = Path(tmp)
            shutil.copy(
                self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml",
                phase / "ANALYSIS-SPEC.yaml",
            )
            shutil.copy(
                self.ROOT / "examples" / "good-DATA-PROFILE.yaml",
                phase / "good-DATA-PROFILE.yaml",
            )
            shutil.copy(
                self.ROOT / "examples" / "RESULTS.md",
                phase / "RESULTS.md",
            )
            shutil.copy(
                self.ROOT / "examples" / "good-FIGURE-MANIFEST.yaml",
                phase / "good-FIGURE-MANIFEST.yaml",
            )
            shutil.copy(
                self.ROOT / "examples" / "good-NARRATIVE.md",
                phase / "good-NARRATIVE.md",
            )
            shutil.copytree(
                self.ROOT / "examples" / "figures",
                phase / "figures",
            )
            charts = phase / "analysis" / "charts.py"
            charts.parent.mkdir(parents=True)
            charts.write_text("# charts\n", encoding="utf-8")
            # This phase directory has never had `dsx gate plan` run against
            # it in this test; seed a plan-time header for the spec this test
            # itself wrote, so ship reaches DSX-REP-031 instead of stopping
            # earlier at prereg's missing-header exit 2.
            seed_plan_header(str(phase), phase / "ANALYSIS-SPEC.yaml")
            code, _, err = self._run(["gate", "ship", "--phase-dir", str(phase)])
            self.assertEqual(code, 1)
            self.assertIn("DSX-REP-031", err)

    def test_determinism_same_input_same_output(self):
        fixture = self.ROOT / "examples" / "bad-ANALYSIS-SPEC.yaml"
        first = self._run(["audit", "--spec", str(fixture), "--json"])
        second = self._run(["audit", "--spec", str(fixture), "--json"])
        self.assertEqual(first, second)

    # ── 06-05: scaffolded template still passes its own structural gates ──────

    def test_template_validity_frame_and_inference_pass_dsx_validate(self):
        template = self.ROOT / "templates" / "ANALYSIS-SPEC.yaml"
        code, _, err = self._run(["validate", "--spec", str(template)])
        self.assertEqual(code, 0, err)

    def test_template_validity_frame_and_inference_pass_gate_plan(self):
        template = self.ROOT / "templates" / "ANALYSIS-SPEC.yaml"
        code, _, err = self._run(["gate", "plan", "--spec", str(template)])
        self.assertEqual(code, 0, err)

    # ── 06-07: DSX-PAR-001 registered at all four default gate thresholds ─────
    # (CRITICAL at plan/execute, HIGH at verify/ship) — REQ-P6-09's "cannot
    # block at any gate threshold" is a claim about those four defaults, not
    # an arbitrary operator --block-on override.

    def test_paradigm_check_registered_in_every_gate_profile(self):
        from dsx.cli import CHECKS, GATE_PROFILES
        from dsx.frame import paradigm

        self.assertIs(CHECKS["paradigm"], paradigm.check)
        for point, checks in GATE_PROFILES.items():
            with self.subTest(point=point):
                self.assertIn("paradigm", checks)

    def _bayesian_variant_spec_path(self, tmp: str) -> Path:
        """Copy examples/ into tmp and flip inference.paradigm to bayesian on
        the good fixture, in place — no second committed fixture, and the
        good fixture's own paradigm is never edited. JSON round-tripping the
        mutated dict back into the .yaml-named file works regardless of
        whether PyYAML is installed: dsx.loader.loads() tries a JSON parse
        before YAML/the bundled parser whenever the stripped text starts with
        '{', independent of the .yaml suffix.
        """
        import json
        import shutil

        from dsx.loader import load

        target = Path(tmp) / "examples"
        shutil.copytree(self.ROOT / "examples", target)
        spec_path = target / "good-ANALYSIS-SPEC.yaml"
        spec = load(spec_path)
        spec.setdefault("inference", {})["paradigm"] = "bayesian"
        spec_path.write_text(json.dumps(spec), encoding="utf-8")
        return spec_path

    def test_bayesian_variant_exits_zero_at_every_gate_with_manifest_printed(self):
        with tempfile.TemporaryDirectory() as tmp:
            variant = self._bayesian_variant_spec_path(tmp)
            for point in ("plan", "execute", "verify", "ship"):
                with self.subTest(point=point):
                    code, out, err = self._run(["gate", point, "--spec", str(variant)])
                    self.assertEqual(code, 0, f"gate {point} unexpectedly blocked:\n{err}")
                    self.assertIn("DSX-PAR-001", out + err)

    def test_bayesian_variant_audit_json_contains_dsx_par_001_at_info(self):
        with tempfile.TemporaryDirectory() as tmp:
            variant = self._bayesian_variant_spec_path(tmp)
            _, out, _ = self._run(["audit", "--spec", str(variant), "--json"])
            payload = json.loads(out)
            findings = [f for f in payload["findings"] if f["code"] == "DSX-PAR-001"]
            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0]["severity"], "INFO")

    def test_bad_fixture_still_blocks_with_paradigm_registered(self):
        fixture = self.ROOT / "examples" / "bad-ANALYSIS-SPEC.yaml"
        for point in ("plan", "ship"):
            with self.subTest(point=point):
                code, _, _ = self._run(["gate", point, "--spec", str(fixture)])
                self.assertEqual(code, 1)

    # D-05: DSX-PAR-001
    def test_every_dsx_par_code_reachable_from_a_gate_profile(self):
        from dsx.cli import GATE_PROFILES
        from dsx.suppressions import known_codes

        par_codes = [c for c in known_codes() if c.startswith("DSX-PAR-")]
        self.assertTrue(par_codes, "expected at least DSX-PAR-001 to be known")
        reachable_checks = set().union(*GATE_PROFILES.values())
        self.assertIn("paradigm", reachable_checks)

    def test_suppressing_dsx_par_001_needs_zero_suppressions_py_changes(self):
        from dsx.cli import run_checks
        from dsx.loader import load

        spec = load(self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml")
        spec["suppressions"] = [
            {
                "code": "DSX-PAR-001",
                "reason": "manifest is informational",
                "authority": ".planning/ROADMAP.md",
            }
        ]
        report = run_checks(spec, ("spec", "paradigm"), None, resolve_root="examples")
        self.assertNotIn("DSX-PAR-001", {f.code for f in report.findings})

    # ── 06-09 Task 1: `dsx explain` and the add_common refactor (D-18) ────────
    # `dsx explain` is deliberately outside the block contract (D-04): it
    # always exits 0 and carries no --block-on. Every case below proves a
    # different failure mode still exits 0 rather than surfacing exit 2.

    def test_explain_prints_no_trail_message_when_none_written(self):
        import shutil

        with tempfile.TemporaryDirectory() as tmp:
            spec_path = Path(tmp) / "ANALYSIS-SPEC.yaml"
            shutil.copy(self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml", spec_path)
            code, out, _ = self._run(["explain", "--spec", str(spec_path)])
            self.assertEqual(code, 0)
            self.assertIn("no decision trail", (out).lower())

    def test_explain_missing_spec_exits_zero_not_two(self):
        code, out, err = self._run(["explain", "--spec", "/nonexistent/spec.yaml"])
        self.assertEqual(code, 0)
        self.assertIn("no decision trail", (out + err).lower())

    def test_explain_no_args_from_dir_with_no_spec_exits_zero(self):
        import os

        with tempfile.TemporaryDirectory() as tmp:
            cwd = os.getcwd()
            try:
                os.chdir(tmp)
                code, _, _ = self._run(["explain"])
            finally:
                os.chdir(cwd)
            self.assertEqual(code, 0)

    def test_explain_empty_trail_file_exits_zero(self):
        import shutil

        with tempfile.TemporaryDirectory() as tmp:
            spec_path = Path(tmp) / "ANALYSIS-SPEC.yaml"
            shutil.copy(self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml", spec_path)
            (Path(tmp) / "DECISIONS.jsonl").write_text("", encoding="utf-8")
            code, out, _ = self._run(["explain", "--spec", str(spec_path)])
            self.assertEqual(code, 0)
            self.assertIn("no decision trail", out.lower())

    def test_explain_truncated_tail_line_still_renders_intact_records(self):
        import shutil

        from dsx.decisions import InvocationHeader, append

        with tempfile.TemporaryDirectory() as tmp:
            spec_path = Path(tmp) / "ANALYSIS-SPEC.yaml"
            shutil.copy(self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml", spec_path)
            trail = Path(tmp) / "DECISIONS.jsonl"
            append(
                trail,
                InvocationHeader(
                    invocation_id="INV-0001", gate_point="plan", dsx_version="0.0.0",
                    frame_digest="deadbeef",
                ),
            )
            trail.write_text(
                trail.read_text(encoding="utf-8") + '{"id": "DEC-9', encoding="utf-8"
            )
            code, out, _ = self._run(
                ["explain", "--spec", str(spec_path), "--phase-dir", tmp]
            )
            self.assertEqual(code, 0)
            self.assertIn("INV-0001", out)

    def test_explain_unknown_invocation_id_exits_zero_and_reports_not_found(self):
        import shutil

        from dsx.decisions import InvocationHeader, append

        with tempfile.TemporaryDirectory() as tmp:
            spec_path = Path(tmp) / "ANALYSIS-SPEC.yaml"
            shutil.copy(self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml", spec_path)
            trail = Path(tmp) / "DECISIONS.jsonl"
            append(
                trail,
                InvocationHeader(
                    invocation_id="INV-0001", gate_point="plan", dsx_version="0.0.0",
                    frame_digest="deadbeef",
                ),
            )
            code, out, _ = self._run(
                [
                    "explain", "--spec", str(spec_path), "--phase-dir", tmp,
                    "--invocation", "INV-9999",
                ]
            )
            self.assertEqual(code, 0)
            self.assertIn("INV-9999", out)

    def test_explain_json_is_parseable(self):
        fixture = self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml"
        code, out, _ = self._run(["explain", "--spec", str(fixture), "--json"])
        self.assertEqual(code, 0)
        json.loads(out)

    def test_explain_help_offers_no_block_on_flag(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            with self.assertRaises(SystemExit):
                cli.main(["explain", "--help"])
        help_text = buf.getvalue()
        self.assertIn("--spec", help_text)
        self.assertIn("--phase-dir", help_text)
        self.assertIn("--invocation", help_text)
        self.assertIn("--json", help_text)
        self.assertNotIn("--block-on", help_text)

    def test_other_subcommands_still_accept_block_on(self):
        for sub in ("validate", "check", "audit", "gate"):
            buf = io.StringIO()
            with redirect_stdout(buf):
                with self.assertRaises(SystemExit):
                    cli.main([sub, "--help"])
            self.assertIn("--block-on", buf.getvalue(), sub)

    # ── 06-09 Task 2: gate-path trail write (REQ-P6-07, D-14, D-16) ────────────

    def test_gate_writes_one_header_and_sequential_decision_records(self):
        import shutil

        with tempfile.TemporaryDirectory() as tmp:
            spec_path = Path(tmp) / "ANALYSIS-SPEC.yaml"
            shutil.copy(self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml", spec_path)
            code, _, err = self._run(["gate", "plan", "--phase-dir", tmp])
            self.assertEqual(code, 0, err)
            trail = Path(tmp) / "DECISIONS.jsonl"
            self.assertTrue(trail.exists())
            records = [
                json.loads(line) for line in trail.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(records[0]["record_type"], "invocation")
            self.assertEqual(records[0]["gate_point"], "plan")
            self.assertTrue(records[0]["frame_digest"])
            inv = records[0]["invocation_id"]
            body = records[1:]
            self.assertTrue(body)
            self.assertTrue(all(r["invocation_id"] == inv for r in body))
            self.assertEqual([r["id"] for r in body], [f"DEC-{i+1:03d}" for i in range(len(body))])

    def test_second_gate_run_appends_new_header_leaving_first_run_intact(self):
        import shutil

        with tempfile.TemporaryDirectory() as tmp:
            spec_path = Path(tmp) / "ANALYSIS-SPEC.yaml"
            shutil.copy(self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml", spec_path)
            self._run(["gate", "plan", "--phase-dir", tmp])
            trail = Path(tmp) / "DECISIONS.jsonl"
            first_records = trail.read_text(encoding="utf-8").splitlines()
            self._run(["gate", "plan", "--phase-dir", tmp])
            second_records = trail.read_text(encoding="utf-8").splitlines()
            self.assertGreater(len(second_records), len(first_records))
            self.assertEqual(second_records[: len(first_records)], first_records)
            headers = [
                json.loads(line) for line in second_records
                if json.loads(line).get("record_type") == "invocation"
            ]
            self.assertEqual(len(headers), 2)
            self.assertNotEqual(headers[0]["invocation_id"], headers[1]["invocation_id"])

    def test_decisions_jsonl_is_gitignored(self):
        text = (self.ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("DECISIONS.jsonl", text)

    def test_validate_check_audit_do_not_write_a_trail(self):
        import shutil

        with tempfile.TemporaryDirectory() as tmp:
            spec_path = Path(tmp) / "ANALYSIS-SPEC.yaml"
            shutil.copy(self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml", spec_path)
            for sub in ("validate", "check", "audit"):
                self._run([sub, "--phase-dir", tmp])
            self.assertFalse((Path(tmp) / "DECISIONS.jsonl").exists())

    def test_gate_every_point_still_exits_correctly_with_trail_write_added(self):
        fixture = self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml"
        for point in ("plan", "execute", "verify", "ship"):
            code, _, err = self._run(["gate", point, "--spec", str(fixture)])
            self.assertEqual(code, 0, f"gate {point} unexpectedly blocked:\n{err}")
        bad = self.ROOT / "examples" / "bad-ANALYSIS-SPEC.yaml"
        code, _, _ = self._run(["gate", "plan", "--spec", str(bad)])
        self.assertEqual(code, 1)

    def test_unwritable_trail_directory_does_not_change_exit_code(self):
        import shutil

        with tempfile.TemporaryDirectory() as tmp:
            spec_path = Path(tmp) / "ANALYSIS-SPEC.yaml"
            shutil.copy(self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml", spec_path)
            control_code, _, control_err = self._run(["gate", "plan", "--spec", str(spec_path)])

            # A regular file can never be a directory: DECISIONS.jsonl's parent
            # cannot be created there, forcing an OSError on write, without
            # relying on filesystem permission bits (which differ on Windows).
            blocker = Path(tmp) / "not-a-directory"
            blocker.write_text("x", encoding="utf-8")
            unwritable_root = str(blocker / "nested")
            code, _, err = self._run(
                ["gate", "plan", "--spec", str(spec_path), "--phase-dir", unwritable_root]
            )
            self.assertEqual(code, control_code, err)


class TestDecisionTrailCLI(unittest.TestCase):
    """06-09 Task 3: end-to-end decision-trail round-trip at the CLI level
    (REQ-P6-07, REQ-P6-08). Kept separate from ``TestCLI`` so the D-08
    fixture tests and their harness stay untouched. Every test copies
    ``examples/good-ANALYSIS-SPEC.yaml`` into a ``tempfile.TemporaryDirectory()``
    and drives both ``gate`` and ``explain`` through ``--phase-dir``, so
    nothing writes into ``examples/``."""

    ROOT = Path(__file__).resolve().parent.parent

    def _run(self, argv: "list[str]") -> "tuple[int, str, str]":
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(argv)
        return code, out.getvalue(), err.getvalue()

    def _gated_spec(self, tmp: str) -> Path:
        import shutil

        spec_path = Path(tmp) / "ANALYSIS-SPEC.yaml"
        shutil.copy(self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml", spec_path)
        return spec_path

    def _append_undecodable_bytes(self, trail_path: "Path") -> None:
        """06-11 Task 1: write the exact corrupting byte sequence the reviewer
        and verifier used — the lead byte of a two-byte UTF-8 sequence whose
        continuation byte never arrives."""
        with trail_path.open("ab") as fh:
            fh.write(b"caf\xc3")

    def _control_exit_code(self, spec_source_name: str, point: str) -> int:
        """06-11 Task 1: run ``point`` against a fresh copy of the named
        ``examples/`` fixture in a clean temporary directory with no trail
        file present at all, and return the exit code — the baseline a
        corrupted-trail run must match."""
        import shutil

        with tempfile.TemporaryDirectory() as tmp:
            spec_path = Path(tmp) / "ANALYSIS-SPEC.yaml"
            shutil.copy(self.ROOT / "examples" / spec_source_name, spec_path)
            code, _, _ = self._run(["gate", point, "--spec", str(spec_path), "--phase-dir", tmp])
            return code

    def test_explain_names_the_invocation_id_the_gate_wrote(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = self._gated_spec(tmp)
            self._run(["gate", "plan", "--spec", str(spec_path), "--phase-dir", tmp])
            trail = Path(tmp) / "DECISIONS.jsonl"
            header = json.loads(trail.read_text(encoding="utf-8").splitlines()[0])
            code, out, _ = self._run(["explain", "--phase-dir", tmp])
            self.assertEqual(code, 0)
            self.assertIn(header["invocation_id"], out)

    def test_explain_renders_only_the_second_runs_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = self._gated_spec(tmp)
            self._run(["gate", "plan", "--spec", str(spec_path), "--phase-dir", tmp])
            self._run(["gate", "plan", "--spec", str(spec_path), "--phase-dir", tmp])
            trail = Path(tmp) / "DECISIONS.jsonl"
            records = [
                json.loads(line) for line in trail.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            headers = [r for r in records if r["record_type"] == "invocation"]
            second_id = headers[1]["invocation_id"]

            code, out, _ = self._run(["explain", "--phase-dir", tmp])
            self.assertEqual(code, 0)
            self.assertIn(second_id, out)
            self.assertNotIn(headers[0]["invocation_id"], out)

    def test_explain_invocation_flag_selects_the_first_runs_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = self._gated_spec(tmp)
            self._run(["gate", "plan", "--spec", str(spec_path), "--phase-dir", tmp])
            self._run(["gate", "plan", "--spec", str(spec_path), "--phase-dir", tmp])
            trail = Path(tmp) / "DECISIONS.jsonl"
            records = [
                json.loads(line) for line in trail.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            headers = [r for r in records if r["record_type"] == "invocation"]
            first_id = headers[0]["invocation_id"]

            code, out, _ = self._run(
                ["explain", "--phase-dir", tmp, "--invocation", first_id]
            )
            self.assertEqual(code, 0)
            self.assertIn(first_id, out)
            self.assertNotIn(headers[1]["invocation_id"], out)

    def test_truncated_tail_line_leaves_explain_at_exit_zero_with_survivors(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = self._gated_spec(tmp)
            self._run(["gate", "plan", "--spec", str(spec_path), "--phase-dir", tmp])
            trail = Path(tmp) / "DECISIONS.jsonl"
            before = trail.read_text(encoding="utf-8")
            trail.write_text(before + '{"id": "DEC-9', encoding="utf-8")

            code, out, _ = self._run(["explain", "--phase-dir", tmp])
            self.assertEqual(code, 0)
            header = json.loads(before.splitlines()[0])
            self.assertIn(header["invocation_id"], out)

    def test_non_json_tail_line_leaves_explain_at_exit_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = self._gated_spec(tmp)
            self._run(["gate", "plan", "--spec", str(spec_path), "--phase-dir", tmp])
            trail = Path(tmp) / "DECISIONS.jsonl"
            with trail.open("a", encoding="utf-8") as fh:
                fh.write("not json at all\n")

            code, _, _ = self._run(["explain", "--phase-dir", tmp])
            self.assertEqual(code, 0)

    def test_explain_json_after_gate_emits_array_with_expected_record_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = self._gated_spec(tmp)
            self._run(["gate", "plan", "--spec", str(spec_path), "--phase-dir", tmp])
            code, out, _ = self._run(["explain", "--phase-dir", tmp, "--json"])
            self.assertEqual(code, 0)
            payload = json.loads(out)
            self.assertIsInstance(payload, list)
            self.assertTrue(payload)
            header = next(r for r in payload if r["record_type"] == "invocation")
            self.assertEqual(
                set(header),
                {"invocation_id", "gate_point", "dsx_version", "frame_digest", "record_type"},
            )
            decisions = [r for r in payload if r["record_type"] == "decision"]
            self.assertTrue(decisions)
            expected_keys = {
                "id", "invocation_id", "layer", "choice", "inputs", "rule", "citation",
                "counterfactual", "alternatives_rejected", "confidence", "escalate",
                "record_type",
            }
            for record in decisions:
                self.assertEqual(set(record), expected_keys)

    def test_rendered_text_names_the_counterfactual_of_at_least_one_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = self._gated_spec(tmp)
            self._run(["gate", "plan", "--spec", str(spec_path), "--phase-dir", tmp])
            trail = Path(tmp) / "DECISIONS.jsonl"
            records = [
                json.loads(line) for line in trail.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            counterfactuals = [
                r["counterfactual"] for r in records
                if r["record_type"] == "decision" and r.get("counterfactual")
            ]
            self.assertTrue(counterfactuals)

            code, out, _ = self._run(["explain", "--phase-dir", tmp])
            self.assertEqual(code, 0)
            self.assertTrue(any(cf in out for cf in counterfactuals))

    # ── 06-11 Task 1: CR-01 regression — a corrupted trail can never move a
    #    gate verdict, and explain always exits 0 ─────────────────────────

    def test_explain_exits_zero_when_trail_holds_an_undecodable_byte(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = self._gated_spec(tmp)
            self._run(["gate", "plan", "--spec", str(spec_path), "--phase-dir", tmp])
            trail = Path(tmp) / "DECISIONS.jsonl"
            self._append_undecodable_bytes(trail)

            code, _, _ = self._run(["explain", "--phase-dir", tmp])
            self.assertEqual(code, 0)

    def test_explain_still_renders_surviving_records_past_an_undecodable_byte(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = self._gated_spec(tmp)
            self._run(["gate", "plan", "--spec", str(spec_path), "--phase-dir", tmp])
            trail = Path(tmp) / "DECISIONS.jsonl"
            header = json.loads(trail.read_text(encoding="utf-8").splitlines()[0])
            self._append_undecodable_bytes(trail)

            code, out, _ = self._run(["explain", "--phase-dir", tmp])
            self.assertEqual(code, 0)
            self.assertIn(header["invocation_id"], out)

    def test_explain_exits_zero_when_trail_path_is_a_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._gated_spec(tmp)
            trail = Path(tmp) / "DECISIONS.jsonl"
            trail.mkdir()

            code, _, _ = self._run(["explain", "--phase-dir", tmp])
            self.assertEqual(code, 0)

    def test_gate_pass_exit_code_matches_control_with_corrupted_trail(self):
        control = self._control_exit_code("good-ANALYSIS-SPEC.yaml", "plan")
        self.assertEqual(control, 0)
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = self._gated_spec(tmp)
            trail = Path(tmp) / "DECISIONS.jsonl"
            trail.write_bytes(
                b'{"record_type": "invocation", "invocation_id": "INV-0001", '
                b'"gate_point": "plan", "dsx_version": "x", "frame_digest": "y"}\n'
                b"caf\xc3"
            )
            code, _, _ = self._run(["gate", "plan", "--spec", str(spec_path), "--phase-dir", tmp])
            self.assertEqual(code, control)

    def test_gate_block_exit_code_matches_control_with_corrupted_trail(self):
        control = self._control_exit_code("bad-ANALYSIS-SPEC.yaml", "plan")
        self.assertEqual(control, 1)
        with tempfile.TemporaryDirectory() as tmp:
            import shutil

            spec_path = Path(tmp) / "ANALYSIS-SPEC.yaml"
            shutil.copy(self.ROOT / "examples" / "bad-ANALYSIS-SPEC.yaml", spec_path)
            trail = Path(tmp) / "DECISIONS.jsonl"
            trail.write_bytes(
                b'{"record_type": "invocation", "invocation_id": "INV-0001", '
                b'"gate_point": "plan", "dsx_version": "x", "frame_digest": "y"}\n'
                b"caf\xc3"
            )
            code, _, _ = self._run(["gate", "plan", "--spec", str(spec_path), "--phase-dir", tmp])
            self.assertEqual(code, control)


# ── Phase 1: profiler, DQ, coherence, evidence ───────────────────────────────


class TestProfiler(unittest.TestCase):
    def test_profile_csv_computes_hash_and_nulls(self):
        from dsx.profiler import profile_csv, write_profile

        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "sample.csv"
            csv_path.write_text(
                "user_id,signup_at,country\n"
                "u1,2026-06-01,US\n"
                "u2,2026-06-02,\n"
                "u3,2026-06-04,DE\n",
                encoding="utf-8",
            )
            profile = profile_csv(
                csv_path,
                primary_key=["user_id"],
                time_column="signup_at",
                sentinels=["-1"],
            )
            self.assertEqual(profile["row_count"], 3)
            self.assertTrue(profile["source_hash"].startswith("sha256:"))
            self.assertEqual(profile["computed_by"], "dsx-profile")
            self.assertTrue(profile["primary_key_unique"])
            self.assertAlmostEqual(profile["columns"]["country"]["null_rate"], 1 / 3, places=5)
            self.assertEqual(profile["time"]["max_gap_days"], 2)
            out = write_profile(profile, Path(tmp) / "DATA-PROFILE.yaml")
            self.assertTrue(out.exists())

    def test_profile_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "sample.csv"
            csv_path.write_text("id,ts\na,2026-01-01\nb,2026-01-02\n", encoding="utf-8")
            out = Path(tmp) / "p.yaml"
            code, stdout, err = self._run_cli(
                ["profile", str(csv_path), "--out", str(out), "--pk", "id", "--time", "ts", "--json"]
            )
            self.assertEqual(code, 0, err)
            self.assertTrue(out.exists())
            self.assertIn("row_count", stdout)

    def _run_cli(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(argv)
        return code, out.getvalue(), err.getvalue()


class TestDQAndCoherence(unittest.TestCase):
    ROOT = Path(__file__).resolve().parent.parent

    def test_dq_blocks_bad_profile(self):
        from dsx.checks import dq
        from dsx.loader import load

        spec = load(self.ROOT / "examples" / "bad-ANALYSIS-SPEC.yaml")
        report = dq.check(spec, str(self.ROOT / "examples"))
        found = codes(report)
        self.assertTrue({"DSX-DQ-010", "DSX-DQ-020", "DSX-DQ-030", "DSX-DQ-040", "DSX-DQ-050"} & found)
        self.assertIn("DSX-DQ-060", found)  # manual without known_gaps

    def test_dq_passes_good_profile(self):
        from dsx.checks import dq
        from dsx.loader import load

        spec = load(self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml")
        report = dq.check(spec, str(self.ROOT / "examples"))
        self.assertFalse(report.blocks(Severity.HIGH), codes(report))

    def test_coherence_claim_exceeds_question(self):
        from dsx.checks import coherence

        report = coherence.check(
            {
                "question_type": "descriptive",
                "claims": [{"text": "X increases Y", "type": "causal"}],
                "decision": {},
                "design": {},
            }
        )
        self.assertIn("DSX-COH-001", codes(report))

    def test_coherence_causal_decision_on_descriptive(self):
        from dsx.checks import coherence

        report = coherence.check(
            {
                "question_type": "descriptive",
                "decision": {"decision_rule": "Ship because the change increases retention"},
                "design": {},
                "claims": [],
            }
        )
        self.assertIn("DSX-COH-010", codes(report))

    def test_coherence_experiment_needs_mpe(self):
        from dsx.checks import coherence

        report = coherence.check(
            {
                "question_type": "causal",
                "decision": {},
                "design": {"kind": "experiment"},
                "claims": [],
                "assumptions": [{"assumption": "stable bucketing"}],
            }
        )
        self.assertIn("DSX-COH-020", codes(report))

    def test_evidence_resolves_and_numeric_overlap(self):
        from dsx.checks import claims as claims_mod
        from dsx.loader import load

        spec = load(self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml")
        report = claims_mod.check(spec, str(self.ROOT / "examples"))
        self.assertNotIn("DSX-CLM-031", codes(report))
        self.assertNotIn("DSX-CLM-032", codes(report))
        self.assertNotIn("DSX-CLM-033", codes(report))

    def test_evidence_missing_file_blocks(self):
        from dsx.checks import claims as claims_mod

        report = claims_mod.check(
            {
                "claims": [
                    {
                        "text": "Uplift is 2.4pp",
                        "type": "descriptive",
                        "evidence": "NO-SUCH-FILE.md#anchor",
                    }
                ],
                "design": {},
                "results": {"tests": [{"effect": 0.024, "ci": [0.01, 0.04]}]},
            },
            str(self.ROOT / "examples"),
        )
        self.assertIn("DSX-CLM-031", codes(report))


class TestPhase2VizFiguresSmells(unittest.TestCase):
    ROOT = Path(__file__).resolve().parent.parent

    def _run(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_seal_cli(self):
        path = self.ROOT / "examples" / "figures" / "activation_uplift.svg"
        code, out, err = self._run(["seal", str(path)])
        self.assertEqual(code, 0, err)
        self.assertTrue(out.strip().startswith("sha256:"))

    def test_input_type_matrix_blocks(self):
        from dsx.checks import viz as viz_mod

        report = viz_mod.check(
            {
                "visuals": [
                    {
                        "name": "bad",
                        "relationship": "comparison",
                        "type": "bar",
                        "data_input_type": "hierarchical",
                        "takeaway": "A grew 12% vs B",
                        "units": "%",
                        "source": "x",
                    }
                ]
            }
        )
        self.assertIn("DSX-VIZ-013", codes(report))

    def test_takeaway_equals_name_blocks(self):
        from dsx.checks import viz as viz_mod

        report = viz_mod.check(
            {
                "visuals": [
                    {
                        "name": "Revenue by region",
                        "relationship": "comparison",
                        "type": "bar",
                        "data_input_type": "categorical-value",
                        "takeaway": "Revenue by region",
                        "units": "USD",
                        "source": "x",
                        "y_axis_starts_at_zero": True,
                    }
                ]
            }
        )
        self.assertIn("DSX-VIZ-063", codes(report))

    def test_stacked_scenario_smell(self):
        from dsx.checks import smells as smells_mod

        report = smells_mod.check(
            {
                "visuals": [
                    {
                        "name": "scenarios",
                        "type": "stacked_area",
                        "series_role": "scenario",
                    }
                ]
            }
        )
        self.assertIn("DSX-SMELL-009", codes(report))

    def test_figure_seal_mismatch(self):
        from dsx.checks import figures as figures_mod

        report = figures_mod.check(
            {
                "visuals": [
                    {
                        "name": "x",
                        "artifact_path": "figures/activation_uplift.svg",
                        "svg_sha256": "sha256:deadbeef",
                    }
                ]
            },
            str(self.ROOT / "examples"),
            strict=True,
        )
        self.assertIn("DSX-FIG-010", codes(report))

    def test_good_figures_pass(self):
        from dsx.checks import figures as figures_mod
        from dsx.loader import load

        spec = load(self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml")
        report = figures_mod.check(spec, str(self.ROOT / "examples"), strict=True)
        self.assertFalse(report.blocks(Severity.HIGH), codes(report))


# ── Phase 3: narrative, claims base, SQL expand, code smells ─────────────────


class TestPhase3NarrativeClaims(unittest.TestCase):
    ROOT = Path(__file__).resolve().parent.parent

    def test_clm_070_relative_percent_without_base(self):
        from dsx.checks import claims as claims_mod

        spec = {
            "question_type": "descriptive",
            "claims": [{"text": "Churn is up 40% after launch.", "type": "descriptive"}],
        }
        self.assertIn("DSX-CLM-070", codes(claims_mod.check(spec)))

    def test_clm_070_passes_with_base_n(self):
        from dsx.checks import claims as claims_mod

        spec = {
            "claims": [
                {
                    "text": "Churn is up 40% after launch.",
                    "type": "descriptive",
                    "base_n": 500,
                }
            ]
        }
        self.assertNotIn("DSX-CLM-070", codes(claims_mod.check(spec)))

    def test_clm_080_empty_limitations_on_causal(self):
        from dsx.checks import claims as claims_mod

        spec = {
            "question_type": "causal",
            "claims": [{"text": "X raises Y by 2pp.", "type": "causal"}],
            "limitations": [],
        }
        self.assertIn("DSX-CLM-080", codes(claims_mod.check(spec, strict=True)))
        self.assertNotIn("DSX-CLM-080", codes(claims_mod.check(spec, strict=False)))

    def test_nar_forbidden_and_claim_subset(self):
        from dsx.checks import narrative as narrative_mod
        from dsx.loader import load

        bad = load(self.ROOT / "examples" / "bad-ANALYSIS-SPEC.yaml")
        report = narrative_mod.check(bad, str(self.ROOT / "examples"), gate_point="ship")
        found = codes(report)
        self.assertIn("DSX-NAR-030", found)
        self.assertIn("DSX-NAR-020", found)

    def test_good_narrative_passes(self):
        from dsx.checks import narrative as narrative_mod
        from dsx.loader import load

        good = load(self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml")
        report = narrative_mod.check(good, str(self.ROOT / "examples"), gate_point="ship")
        self.assertFalse(report.blocks(Severity.HIGH), codes(report))
        self.assertNotIn("DSX-NAR-030", codes(report))


class TestPhase3SqlWarehouse(unittest.TestCase):
    def test_sql_null_compare_and_select_star(self):
        from dsx.checks import metrics as metrics_mod

        spec = {
            "metrics": [
                {
                    "name": "x",
                    "definition": "x",
                    "grain": "user",
                    "source": "warehouse.x",
                    "sql": "SELECT * FROM t WHERE status = NULL",
                }
            ]
        }
        found = codes(metrics_mod.check(spec))
        self.assertIn("DSX-SQL-008", found)
        self.assertIn("DSX-SQL-009", found)

    def test_met_040_warehouse_without_sql(self):
        from dsx.checks import metrics as metrics_mod

        spec = {
            "metrics": [
                {
                    "name": "x",
                    "definition": "x",
                    "grain": "user",
                    "source": "warehouse.fct_x",
                }
            ]
        }
        self.assertIn("DSX-MET-040", codes(metrics_mod.check(spec)))

    def test_sql_007_division_without_nullif(self):
        from dsx.checks import metrics as metrics_mod

        spec = {
            "metrics": [
                {
                    "name": "x",
                    "definition": "x",
                    "grain": "user",
                    "source": "app.events",
                    "sql": "SELECT a / b FROM t",
                }
            ]
        }
        self.assertIn("DSX-SQL-007", codes(metrics_mod.check(spec)))


class TestPhase3Code(unittest.TestCase):
    ROOT = Path(__file__).resolve().parent.parent

    def test_fit_before_split_is_critical(self):
        from dsx.checks import code as code_mod

        report = code_mod.check(
            {
                "model": {"task": "binary_classification"},
                "reproducibility": {"entrypoint": "analysis/leaky_model.py"},
            },
            str(self.ROOT / "examples"),
        )
        found = codes(report)
        self.assertIn("DSX-CODE-001", found)
        self.assertIn("DSX-CODE-002", found)

    def test_good_entrypoint_without_ml_passes(self):
        from dsx.checks import code as code_mod
        from dsx.loader import load

        spec = load(self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml")
        report = code_mod.check(spec, str(self.ROOT / "examples"))
        self.assertNotIn("DSX-CODE-001", codes(report))


# ── Phase 4: assumptions, null/TOST, exploratory, decision, repro_lock ───────


class TestPhase4AnalyticalLogic(unittest.TestCase):
    ROOT = Path(__file__).resolve().parent.parent

    def test_coh_031_unchecked_assumption(self):
        from dsx.checks import coherence as coherence_mod

        spec = {
            "question_type": "causal",
            "assumptions": [
                {
                    "assumption": "X",
                    "rationale": "Y",
                    "impact_if_wrong": "Z",
                    "checked": False,
                }
            ],
        }
        self.assertIn("DSX-COH-031", codes(coherence_mod.check(spec, strict=True)))
        self.assertNotIn("DSX-COH-031", codes(coherence_mod.check(spec, strict=False)))

    def test_exp_051_looks_exceed_family(self):
        from dsx.checks import design as design_mod

        spec = {
            "design": {
                "kind": "observational",
                "multiplicity": {
                    "family": ["a", "b"],
                    "correction": "benjamini_hochberg",
                },
            },
            "results": {"comparisons_looked_at": 9, "tests": [{"metric": "a", "p_value": 0.1}]},
        }
        self.assertIn("DSX-EXP-051", codes(design_mod.check(spec)))

    def test_decision_replay_fail_and_pass(self):
        from dsx.checks import decision as decision_mod

        fail_spec = {
            "question_type": "causal",
            "design": {"kind": "experiment", "alpha": 0.05},
            "decision": {
                "replay": {
                    "metric": "activation_rate",
                    "ci_lower_min": 0.05,
                    "on_pass": "roll",
                    "on_fail": "hold",
                }
            },
            "results": {
                "tests": [
                    {
                        "metric": "activation_rate",
                        "p_value": 0.01,
                        "effect": 0.02,
                        "ci": [0.01, 0.03],
                    }
                ]
            },
        }
        self.assertIn("DSX-DEC-020", codes(decision_mod.check(fail_spec, gate_point="ship")))

        pass_spec = {
            "question_type": "causal",
            "design": {"kind": "experiment", "alpha": 0.05},
            "decision": {
                "replay": {
                    "metric": "activation_rate",
                    "ci_lower_min": 0.009,
                    "on_pass": "roll",
                    "on_fail": "hold",
                }
            },
            "results": {
                "tests": [
                    {
                        "metric": "activation_rate",
                        "p_value": 0.01,
                        "effect": 0.02,
                        "ci": [0.01, 0.03],
                    }
                ]
            },
        }
        found = codes(decision_mod.check(pass_spec, gate_point="ship"))
        self.assertNotIn("DSX-DEC-020", found)
        self.assertNotIn("DSX-DEC-021", found)

    def test_repro_lock_missing_and_null(self):
        from dsx.checks import repro as repro_mod

        missing = {
            "results": {"tests": [{"metric": "a", "p_value": 0.1}]},
            "reproducibility": {"entrypoint": "x.py", "lockfile": "l"},
        }
        self.assertIn("DSX-REP-050", codes(repro_mod.check(missing, strict=True)))

        opted = {
            "results": {"tests": [{"metric": "a", "p_value": 0.1}]},
            "reproducibility": {
                "entrypoint": "x.py",
                "lockfile": "l",
                "repro_lock": None,
            },
        }
        self.assertIn("DSX-REP-051", codes(repro_mod.check(opted, strict=True)))

    def test_met_012_unknown_class(self):
        from dsx.checks import metrics as metrics_mod

        spec = {
            "metrics": [
                {
                    "name": "x",
                    "definition": "x",
                    "grain": "user",
                    "source": "app.x",
                    "reconciliation": {
                        "class": "galaxy",
                        "sources": [
                            {"name": "a", "value": 1.0},
                            {"name": "b", "value": 1.0},
                        ],
                    },
                }
            ]
        }
        self.assertIn("DSX-MET-012", codes(metrics_mod.check(spec)))

    def test_good_fixture_phase4_fields(self):
        from dsx.loader import load

        spec = load(self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml")
        self.assertIn("replay", spec["decision"])
        self.assertEqual(spec["results"]["comparisons_looked_at"], 3)
        self.assertIsInstance(spec["reproducibility"]["repro_lock"], dict)


class TestPhase5Suppressions(unittest.TestCase):
    ROOT = Path(__file__).resolve().parent.parent

    def test_missing_reason_flagged(self):
        from dsx.suppressions import validate_suppressions

        report = validate_suppressions(
            {
                "suppressions": [
                    {
                        "code": "DSX-VIZ-030",
                        "authority": "docs/SPEC.md",
                    }
                ]
            }
        )
        self.assertIn("DSX-SPEC-070", {f.code for f in report.findings})

    def test_unknown_code_critical(self):
        from dsx.suppressions import validate_suppressions

        report = validate_suppressions(
            {
                "suppressions": [
                    {
                        "code": "DSX-FAKE-999",
                        "reason": "nope",
                        "authority": "docs/x.md",
                    }
                ]
            }
        )
        self.assertIn("DSX-SPEC-072", {f.code for f in report.findings})

    def test_apply_suppresses_dual_axis(self):
        from dsx.checks import viz
        from dsx.cli import run_checks
        from dsx.loader import load
        from dsx.suppressions import apply_suppressions

        spec = load(self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml")
        # Mutate first visual to dual-axis (would emit DSX-VIZ-030)
        spec["visuals"][0]["dual_axis"] = True
        viz_report = viz.check(spec)
        self.assertIn("DSX-VIZ-030", {f.code for f in viz_report.findings})

        spec["suppressions"] = [
            {
                "code": "DSX-VIZ-030",
                "chart_id": spec["visuals"][0]["chart_id"],
                "reason": "SPEC requires twin axes for this readout",
                "authority": "docs/SPEC.md#twin-axes",
            }
        ]
        cleared = apply_suppressions(spec, viz_report)
        self.assertNotIn("DSX-VIZ-030", {f.code for f in cleared.findings})
        self.assertTrue(cleared.context.get("suppressions_applied"))

        # Full run_checks path also clears it
        full = run_checks(spec, ("viz",), None)
        self.assertNotIn("DSX-VIZ-030", {f.code for f in full.findings})

    def test_unknown_code_apply_raises(self):
        from dsx.findings import CheckError, Report
        from dsx.suppressions import apply_suppressions

        report = Report(check="t")
        with self.assertRaises(CheckError):
            apply_suppressions(
                {
                    "suppressions": [
                        {
                            "code": "DSX-ZZZ-001",
                            "reason": "x",
                            "authority": "y",
                        }
                    ]
                },
                report,
            )


# ── Phase 6 (06-07): DSX-PAR-001 paradigm manifest (REQ-P6-09, D-10) ─────────


class TestPhase6ParadigmManifest(unittest.TestCase):
    """DSX-PAR-001 — the informational paradigm manifest.

    Two of these tests are the honesty invariant the plan's prohibition exists
    to enforce (T-6-14): every prefix the manifest calls 'applied' must have at
    least one matching emitted code, and every prefix it calls 'not shipped'
    must have none. ``known_codes()`` is imported here, in the test — never
    inside ``dsx/frame/paradigm.py`` itself, since the gate path must not
    AST-walk the package on every invocation.
    """

    def test_every_paradigm_and_undeclared_case_yields_exactly_one_info_finding(self):
        from dsx.findings import Severity
        from dsx.frame import paradigm
        from dsx.spec import PARADIGMS

        specs = [{"inference": {"paradigm": q}} for q in PARADIGMS] + [{}, {"inference": {}}]
        for spec in specs:
            with self.subTest(spec=spec):
                report = paradigm.check(spec)
                par = [f for f in report.findings if f.code == "DSX-PAR-001"]
                self.assertEqual(len(par), 1)
                self.assertEqual(par[0].severity, Severity.INFO)
                self.assertTrue(par[0].detail.strip())

    def test_undeclared_paradigm_names_the_gap_rather_than_assuming_frequentist(self):
        from dsx.frame import paradigm

        for spec in ({}, {"inference": {}}):
            with self.subTest(spec=spec):
                report = paradigm.check(spec)
                finding = [f for f in report.findings if f.code == "DSX-PAR-001"][0]
                combined = (finding.title + " " + finding.detail).lower()
                self.assertIn("no", combined)
                self.assertIn("paradigm", combined)
                self.assertNotIn("frequentist", finding.title.lower())

    def test_detail_names_an_applied_set_and_a_not_applied_set_with_reasons(self):
        from dsx.frame import paradigm

        report = paradigm.check({"inference": {"paradigm": "bayesian"}})
        finding = [f for f in report.findings if f.code == "DSX-PAR-001"][0]
        self.assertIn("applied", finding.detail.lower())
        self.assertTrue(finding.data.get("applied"))
        not_applied = finding.data.get("not_applied") or {}
        self.assertTrue(not_applied)
        for prefix, reason in not_applied.items():
            self.assertTrue(reason.strip(), f"{prefix} has a blank reason")

    def test_manifest_never_blocks_at_any_default_gate_threshold(self):
        # A non-blank paradigm_justification keeps DSX-PAR-002 (Phase 9,
        # HIGH) silent so this test isolates what it names: DSX-PAR-001
        # itself, INFO, never blocks. Without it this spec would also carry
        # DSX-PAR-002's HIGH finding, which correctly blocks at verify/ship
        # (09-05-PLAN.md's resolved_open_questions) — a fact this test must
        # not obscure by picking a spec that happens to dodge it.
        from dsx.cli import GATE_THRESHOLDS
        from dsx.findings import Severity
        from dsx.frame import paradigm

        report = paradigm.check(
            {"inference": {"paradigm": "bayesian", "paradigm_justification": "team_convention"}}
        )
        for point, label in GATE_THRESHOLDS.items():
            with self.subTest(point=point):
                self.assertFalse(report.blocks(Severity.parse(label)))

    def test_check_appends_one_decision_record_per_emitting_judgement_point(self):
        """One DecisionRecord per judgement point that actually emits a
        finding — never a fixed count. A spec declaring a paradigm with no
        justification now legitimately emits two: DSX-PAR-001's manifest
        record and DSX-PAR-002's requiredness record (Phase 9, 09-05-PLAN.md).
        A spec that also clears DSX-PAR-002 (a valid paradigm_justification
        declared) emits only the manifest's one. Pinning both counts is what
        makes a future check that emits a record unconditionally, or one that
        emits none at its judgement point, visible.
        """
        from dsx.frame import paradigm

        # DSX-PAR-001 (always) + DSX-PAR-002 (paradigm declared, no justification)
        report = paradigm.check({"inference": {"paradigm": "frequentist"}})
        decisions = report.context.get("decisions") or []
        self.assertEqual(len(decisions), 2)
        for record in decisions:
            self.assertEqual(record["layer"], "deterministic")
            self.assertEqual(record["id"], "")
            self.assertEqual(record["invocation_id"], "")
            self.assertTrue(record["counterfactual"].strip())

        # DSX-PAR-001 only — a valid paradigm_justification clears DSX-PAR-002
        cleared_report = paradigm.check(
            {"inference": {"paradigm": "frequentist", "paradigm_justification": "team_convention"}}
        )
        cleared_decisions = cleared_report.context.get("decisions") or []
        self.assertEqual(len(cleared_decisions), 1)
        self.assertEqual(cleared_decisions[0]["layer"], "deterministic")
        self.assertEqual(cleared_decisions[0]["id"], "")
        self.assertTrue(cleared_decisions[0]["counterfactual"].strip())

    # D-05: DSX-PAR-001
    def test_applied_prefixes_have_codes_and_not_shipped_prefixes_have_none(self):
        """A prefix reported 'not applied' is not applied for one of two
        distinct reasons, conflated before Phase 9 shipped its first
        paradigm-conditional code alongside a still-unshipped one:

        - **not shipped** (the reason came from ``_NOT_SHIPPED``): no known
          code may start with that prefix — the original, still-valid half
          of this test.
        - **not selected for the declared paradigm** (the other paradigm's
          own conditional family, now that it has shipped): a known code
          *must* start with that prefix — a shipped-but-currently-unselected
          prefix is not the same thing as an unshipped one, and asserting
          the same "resolves to zero known codes" property against it would
          be wrong now that DSX-PAR-010/DSX-PAR-011 exist. This positive half
          is strictly additive: it proves the reverse direction the original
          test never checked, it does not weaken the original assertion.
        """
        from dsx.frame import paradigm
        from dsx.spec import PARADIGMS
        from dsx.suppressions import known_codes

        known = known_codes()
        for declared in list(PARADIGMS) + [""]:
            spec = {"inference": {"paradigm": declared}} if declared else {}
            with self.subTest(declared=declared or "undeclared"):
                report = paradigm.check(spec)
                finding = [f for f in report.findings if f.code == "DSX-PAR-001"][0]
                for prefix in finding.data.get("applied", []):
                    self.assertTrue(
                        [c for c in known if c.startswith(prefix)],
                        f"{prefix} reported applied but no known code starts with it",
                    )
                for prefix, reason in finding.data.get("not_applied", {}).items():
                    has_known_code = bool([c for c in known if c.startswith(prefix)])
                    if reason == "not selected for the declared paradigm":
                        self.assertTrue(
                            has_known_code,
                            f"{prefix} reported not-selected-for-paradigm but no "
                            "known code starts with it — a shipped-but-unselected "
                            "prefix must still resolve to a real code",
                        )
                    else:
                        self.assertFalse(
                            has_known_code,
                            f"{prefix} reported not-shipped but a known code exists",
                        )
        for prefix in paradigm._NOT_SHIPPED:
            self.assertFalse([c for c in known if c.startswith(prefix)], prefix)


# ── Phase 9 (09-03): DSX-PAR-010/DSX-PAR-011 symmetric monitoring pair ───────
# (REQ-P9-01, REQ-P9-02, REQ-P9-03, REQ-P9-05, brief D-12). See
# references/paradigm-symmetry.md for the locked clearing-condition contract
# this class asserts against — the same table the implementation is required
# to match exactly.


class TestPhase9MonitoringDiscipline(unittest.TestCase):
    """DSX-PAR-010 (frequentist) / DSX-PAR-011 (bayesian) — the atomic,
    symmetric monitoring-discipline pair. Both trigger on exactly one
    condition, design.peeking_policy normalizing to uncontrolled_continuous,
    and are cleared by non-blank free-text declarations evaluated by one
    shared predicate.
    """

    ROOT = Path(__file__).resolve().parent.parent

    UNCONTROLLED_DESIGN = {"peeking_policy": "uncontrolled_continuous", "alpha": 0.05}

    def _spec(self, paradigm=None, **inference_fields):
        inference = dict(inference_fields)
        if paradigm is not None:
            inference["paradigm"] = paradigm
        return {"design": dict(self.UNCONTROLLED_DESIGN), "inference": inference}

    def _gate_plan(self, spec_path):
        with tempfile.TemporaryDirectory() as tmp:
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = cli.main(
                    ["gate", "plan", "--spec", str(spec_path), "--phase-dir", tmp, "--json"]
                )
            raw = err.getvalue() or out.getvalue()
            report = json.loads(raw)
        return code, report["findings"]

    def _retype_and_gate(self, source_slug, other_paradigm):
        from dsx.loader import load

        source = self.ROOT / "examples" / "known-bad" / f"{source_slug}-ANALYSIS-SPEC.yaml"
        spec = load(str(source))
        spec.setdefault("inference", {})["paradigm"] = other_paradigm
        with tempfile.TemporaryDirectory() as tmp:
            retyped = Path(tmp) / "retyped-ANALYSIS-SPEC.json"
            retyped.write_text(json.dumps(spec), encoding="utf-8")
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = cli.main(
                    ["gate", "plan", "--spec", str(retyped), "--phase-dir", tmp, "--json"]
                )
            raw = err.getvalue() or out.getvalue()
            report = json.loads(raw)
        return code, report["findings"]

    # ── unit-level: clearing conditions and symmetry ────────────────────────

    def test_dsx_par_010_fires_for_frequentist_with_both_clearing_fields_blank(self):
        from dsx.frame import paradigm

        report = paradigm.check(
            self._spec(paradigm="frequentist", alpha_spending="", threshold_calibration="")
        )
        found = [f for f in report.findings if f.code == "DSX-PAR-010"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.CRITICAL)

    def test_dsx_par_011_fires_for_bayesian_with_both_clearing_fields_blank(self):
        from dsx.frame import paradigm

        report = paradigm.check(
            self._spec(paradigm="bayesian", prior_justification="", threshold_calibration="")
        )
        found = [f for f in report.findings if f.code == "DSX-PAR-011"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.CRITICAL)

    def test_declaring_alpha_spending_clears_only_the_frequentist_half(self):
        from dsx.frame import paradigm

        spec = self._spec(alpha_spending="a spending function", threshold_calibration="")
        found = codes(paradigm.check(spec))
        self.assertNotIn("DSX-PAR-010", found)
        self.assertIn("DSX-PAR-011", found)  # undeclared paradigm: bayesian half still open

    def test_declaring_prior_justification_clears_only_the_bayesian_half(self):
        from dsx.frame import paradigm

        spec = self._spec(prior_justification="a stated prior", threshold_calibration="")
        found = codes(paradigm.check(spec))
        self.assertIn("DSX-PAR-010", found)
        self.assertNotIn("DSX-PAR-011", found)

    def test_declaring_threshold_calibration_clears_both_halves(self):
        from dsx.frame import paradigm

        spec = self._spec(threshold_calibration="a calibration procedure")
        found = codes(paradigm.check(spec))
        self.assertNotIn("DSX-PAR-010", found)
        self.assertNotIn("DSX-PAR-011", found)

    def test_undeclared_paradigm_can_fire_both_codes(self):
        from dsx.frame import paradigm

        found = codes(paradigm.check(self._spec()))
        self.assertIn("DSX-PAR-010", found)
        self.assertIn("DSX-PAR-011", found)

    def test_declaring_either_paradigm_never_increases_the_finding_count(self):
        from dsx.frame import paradigm

        undeclared = {c for c in codes(paradigm.check(self._spec())) if c.startswith("DSX-PAR-01")}
        for member in ("frequentist", "bayesian"):
            with self.subTest(paradigm=member):
                declared = {
                    c for c in codes(paradigm.check(self._spec(paradigm=member)))
                    if c.startswith("DSX-PAR-01")
                }
                self.assertLessEqual(len(declared), len(undeclared))

    def test_neither_code_fires_for_a_non_uncontrolled_peeking_policy(self):
        from dsx.frame import paradigm

        for policy in list(PEEKING_POLICIES) + ["", None]:
            if policy == "uncontrolled_continuous":
                continue
            with self.subTest(policy=policy):
                spec = {"design": {"peeking_policy": policy}, "inference": {}}
                found = codes(paradigm.check(spec))
                self.assertNotIn("DSX-PAR-010", found)
                self.assertNotIn("DSX-PAR-011", found)

    def test_neither_code_fires_with_no_design_block(self):
        from dsx.frame import paradigm

        found = codes(paradigm.check({"inference": {}}))
        self.assertNotIn("DSX-PAR-010", found)
        self.assertNotIn("DSX-PAR-011", found)

    def test_dsx_par_010_and_dsx_exp_060_are_disjoint_across_every_peeking_policy(self):
        # D-08-style guard, inherited from TestDesign's parametrised peeking test:
        # the two peeking codes must never both fire against the same spec.
        from dsx.checks import design as design_check
        from dsx.frame import paradigm

        for policy in list(PEEKING_POLICIES) + [""]:
            with self.subTest(policy=policy):
                spec = {
                    "question_type": "causal",
                    "design": {"kind": "experiment", "peeking_policy": policy, "alpha": 0.05},
                    "inference": {"paradigm": "frequentist"},
                    "results": {"interim_looks": 5},
                }
                exp_codes = codes(design_check.check(spec))
                par_codes = codes(paradigm.check(spec))
                self.assertFalse(
                    "DSX-PAR-010" in par_codes and "DSX-EXP-060" in exp_codes,
                    f"policy={policy!r} produced both DSX-PAR-010 and DSX-EXP-060",
                )

    def test_monitoring_discipline_map_is_symmetric_across_paradigms(self):
        from dsx.frame import paradigm
        from dsx.spec import PARADIGMS

        self.assertEqual(set(paradigm._MONITORING_DISCIPLINE), set(PARADIGMS))
        lengths = {len(fields) for _code, fields in paradigm._MONITORING_DISCIPLINE.values()}
        self.assertEqual(len(lengths), 1, "every row must have the same clearing-tuple length")
        for _code, fields in paradigm._MONITORING_DISCIPLINE.values():
            self.assertIn("threshold_calibration", fields)

    def test_arbitrary_decision_threshold_string_produces_identical_finding_text(self):
        # T-9-01: nothing on the gate path parses or computes over a
        # decision_threshold string — proven behaviourally, not by inspection.
        from dsx.frame import paradigm

        blank_spec = self._spec(paradigm="bayesian", decision_threshold="")
        weird_spec = self._spec(
            paradigm="bayesian",
            decision_threshold="{P(B>A)} > 0.95%; `rm -rf /` ${HOME}",
        )
        blank_findings = [f for f in paradigm.check(blank_spec).findings if f.code == "DSX-PAR-011"]
        weird_findings = [f for f in paradigm.check(weird_spec).findings if f.code == "DSX-PAR-011"]
        self.assertEqual(len(blank_findings), 1)
        self.assertEqual(len(weird_findings), 1)
        blank_finding, weird_finding = blank_findings[0], weird_findings[0]
        self.assertEqual(blank_finding.title, weird_finding.title)
        self.assertEqual(blank_finding.detail, weird_finding.detail)
        self.assertEqual(blank_finding.remedy, weird_finding.remedy)
        self.assertEqual(blank_finding.where, weird_finding.where)

    def test_dsx_par_010_reference_values_reuse_inflation_from_peeking(self):
        # No second inflation table exists (REQ-P9-01) — this pins the same
        # anchors dsx.mathx.inflation_from_peeking() itself is pinned against.
        self.assertAlmostEqual(mathx.inflation_from_peeking(5, 0.05), 0.142, places=3)
        self.assertAlmostEqual(mathx.inflation_from_peeking(20, 0.05), 0.248, places=3)
        # D-05: DSX-PAR-010

    def test_dsx_par_011_reference_value_boundary_arithmetic(self):
        self.assertEqual(1 / (19 + 1), 0.05)
        self.assertEqual(1 / (24 + 1), 0.04)
        self.assertEqual(1 / (15 + 1), 0.0625)
        # D-05: DSX-PAR-011

    # ── type-domain closure (09-06-PLAN.md gap closure, REQ-P9-06) ──────────
    # A bare 0, 0.0 or False previously read as "declared" and cleared the
    # CRITICAL pair with no declared content. These tests pin the full type
    # domain of all three clearing declarations, on both paradigms, as a
    # genuine runtime cross product over _MONITORING_DISCIPLINE rather than
    # a hand-written list of the three field names.

    NON_CLEARING_VALUES = (
        None, "", "   ", 0, 0.0, False, True, [], ["a"], {}, {"m": "obf"},
    )

    def test_non_text_and_blank_values_never_clear_either_half(self):
        from dsx.frame import paradigm

        all_codes = {code for code, _fields in paradigm._MONITORING_DISCIPLINE.values()}
        for member, (code, clearing_fields) in paradigm._MONITORING_DISCIPLINE.items():
            for field in clearing_fields:
                for value in self.NON_CLEARING_VALUES:
                    with self.subTest(paradigm=member, field=field, value=repr(value)):
                        spec = self._spec(paradigm=member, **{field: value})
                        found = codes(paradigm.check(spec))
                        self.assertIn(code, found)
                        # Declaring one paradigm applies only that paradigm's
                        # row (see _check_monitoring_discipline), so the other
                        # code must never appear here — this is what proves
                        # the tightening did not start firing the other half.
                        other_codes = all_codes - {code}
                        self.assertFalse(other_codes & found, other_codes & found)

    def test_non_blank_string_still_clears(self):
        from dsx.frame import paradigm

        for member, (code, clearing_fields) in paradigm._MONITORING_DISCIPLINE.items():
            for field in clearing_fields:
                with self.subTest(paradigm=member, field=field):
                    spec = self._spec(paradigm=member, **{field: "a spending function"})
                    found = codes(paradigm.check(spec))
                    self.assertNotIn(code, found)

    def test_single_character_string_zero_still_clears(self):
        # The audit's documented cheapest dishonest path is one free-text
        # declaration, unchanged — a string is text regardless of content.
        from dsx.frame import paradigm

        for member, (code, clearing_fields) in paradigm._MONITORING_DISCIPLINE.items():
            for field in clearing_fields:
                with self.subTest(paradigm=member, field=field):
                    spec = self._spec(paradigm=member, **{field: "0"})
                    found = codes(paradigm.check(spec))
                    self.assertNotIn(code, found)

    def test_is_blank_unchanged_for_numeric_and_boolean_scalars(self):
        # Blast-radius guard: fails loudly if a future change moves the
        # tightening into the shared helper where 138 other call sites would
        # inherit it.
        from dsx.spec import is_blank

        for value in (0, 0.0, False, True):
            with self.subTest(value=repr(value)):
                self.assertFalse(is_blank(value))

    def test_numeric_threshold_calibration_blocks_plan_with_both_codes(self):
        spec_dict = {
            "design": {"peeking_policy": "uncontrolled_continuous", "alpha": 0.05},
            "inference": {"threshold_calibration": 0},
        }
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = Path(tmp) / "numeric-threshold-ANALYSIS-SPEC.json"
            spec_path.write_text(json.dumps(spec_dict), encoding="utf-8")
            code, findings = self._gate_plan(spec_path)
        self.assertEqual(code, 1)
        critical_codes = {f["code"] for f in findings if f["severity"] == "CRITICAL"}
        self.assertIn("DSX-PAR-010", critical_codes)
        self.assertIn("DSX-PAR-011", critical_codes)

    # ── end-to-end: both known-bad fixtures, both retype directions ─────────

    def test_frequentist_known_bad_fixture_blocks_plan_with_dsx_par_010(self):
        path = (
            self.ROOT / "examples" / "known-bad"
            / "frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml"
        )
        code, findings = self._gate_plan(path)
        self.assertEqual(code, 1)
        self.assertIn("DSX-PAR-010", {f["code"] for f in findings})

    def test_bayesian_known_bad_fixture_blocks_plan_with_dsx_par_011(self):
        path = (
            self.ROOT / "examples" / "known-bad"
            / "bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml"
        )
        code, findings = self._gate_plan(path)
        self.assertEqual(code, 1)
        self.assertIn("DSX-PAR-011", {f["code"] for f in findings})

    def test_retyping_frequentist_fixture_to_bayesian_yields_dsx_par_011_not_010(self):
        code, findings = self._retype_and_gate("frequentist-uncontrolled-continuous", "bayesian")
        self.assertEqual(code, 1)
        found = {f["code"] for f in findings}
        self.assertIn("DSX-PAR-011", found)
        self.assertNotIn("DSX-PAR-010", found)

    def test_retyping_bayesian_fixture_to_frequentist_yields_dsx_par_010_not_011(self):
        code, findings = self._retype_and_gate("bayesian-continuous-monitoring", "frequentist")
        self.assertEqual(code, 1)
        found = {f["code"] for f in findings}
        self.assertIn("DSX-PAR-010", found)
        self.assertNotIn("DSX-PAR-011", found)

    # ── 09-07 gap closure (REQ-P9-03): DSX-PAR-011's detail= attribution ────
    # The docstring already states the correct three-part attribution (Theorem
    # 1 licenses the bound under optional stopping; the bound itself is
    # unnumbered prose at Theorem 1 and again at Section 3.2); the emitted
    # detail= string did not. This asserts on the emitted finding, not the
    # source file — the operator reads the emitted string, and a source grep
    # would pass on a docstring that never reaches a user.

    def test_dsx_par_011_detail_attributes_the_bound_without_a_locator_error(self):
        from dsx.frame import paradigm

        spec = self._spec(paradigm="bayesian", prior_justification="", threshold_calibration="")
        report = paradigm.check(spec)
        found = [f for f in report.findings if f.code == "DSX-PAR-011"]
        self.assertEqual(len(found), 1)
        detail = " ".join(found[0].detail.split())

        required = (
            "(Deng, Lu & Chen 2016)",
            "1/(K+1) = 1/20 = 0.05 at K = 19",
            "Theorem 1 licenses",
            "unnumbered prose",
            "Section 3.2",
        )
        for substring in required:
            with self.subTest(required=substring):
                self.assertIn(
                    substring, detail,
                    f"DSX-PAR-011 detail no longer states {substring!r}",
                )

        self.assertNotIn(
            "2016, Theorem 1", detail,
            "DSX-PAR-011 detail still pairs the theorem number with the "
            "1/(K+1) parenthetical — this is the locator error REQ-P9-03 "
            "exists to retire",
        )


# ── Phase 9 (09-05): DSX-PAR-002 requiredness and symmetry ──────────────────
# (REQ-P9-04, D-08, D-09, brief D-12). DSX-PAR-002 owns absence only — the
# membership check over PARADIGM_JUSTIFICATIONS is DSX-SPEC-085's job
# (dsx/spec.py::_validate_inference_shape). This class proves the two
# requiredness cases, the one-finding-per-spec ceiling, the no-double-firing
# boundary against DSX-SPEC-085, and — the load-bearing property — that no
# member of PARADIGM_JUSTIFICATIONS and no member of PARADIGMS has its own
# code path, via a genuine fourteen-case cross product.


class TestPhase9ParadigmJustification(unittest.TestCase):
    """DSX-PAR-002 — requiredness for inference.paradigm_justification, and
    the requiredness half of the missing-paradigm message. Membership is
    DSX-SPEC-085's job; this code never re-checks it (D-08).
    """

    ROOT = Path(__file__).resolve().parent.parent

    def _run(self, argv: list[str]) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(argv)
        return code, out.getvalue(), err.getvalue()

    # ── requiredness: missing/blank paradigm_justification ──────────────────

    def test_declared_paradigm_with_no_justification_fires_dsx_par_002_at_high(self):
        from dsx.frame import paradigm
        from dsx.spec import PARADIGMS

        for member in PARADIGMS:
            with self.subTest(paradigm=member):
                report = paradigm.check({"inference": {"paradigm": member}})
                found = [f for f in report.findings if f.code == "DSX-PAR-002"]
                self.assertEqual(len(found), 1)
                self.assertEqual(found[0].severity, Severity.HIGH)
                # D-05: DSX-PAR-002
                self.assertEqual(found[0].where, "spec.inference.paradigm_justification")

    def test_declared_paradigm_with_blank_justification_fires_dsx_par_002(self):
        from dsx.frame import paradigm
        from dsx.spec import PARADIGMS

        for member in PARADIGMS:
            with self.subTest(paradigm=member):
                spec = {"inference": {"paradigm": member, "paradigm_justification": ""}}
                report = paradigm.check(spec)
                found = [f for f in report.findings if f.code == "DSX-PAR-002"]
                self.assertEqual(len(found), 1)
                self.assertEqual(found[0].severity, Severity.HIGH)
                self.assertEqual(found[0].where, "spec.inference.paradigm_justification")

    # ── requiredness: missing paradigm under an uncontrolled design ─────────

    def test_uncontrolled_design_with_no_paradigm_fires_dsx_par_002_naming_paradigm(self):
        from dsx.frame import paradigm

        spec = {"design": {"peeking_policy": "uncontrolled_continuous"}, "inference": {}}
        report = paradigm.check(spec)
        found = [f for f in report.findings if f.code == "DSX-PAR-002"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.HIGH)
        self.assertEqual(found[0].where, "spec.inference.paradigm")

    def test_uncontrolled_design_with_absent_inference_block_fires_dsx_par_002(self):
        from dsx.frame import paradigm

        spec = {"design": {"peeking_policy": "uncontrolled_continuous"}}
        report = paradigm.check(spec)
        found = [f for f in report.findings if f.code == "DSX-PAR-002"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].where, "spec.inference.paradigm")

    # ── no finding when nothing is wrong ─────────────────────────────────────

    def test_no_inference_block_and_controlled_or_absent_policy_fires_nothing(self):
        from dsx.frame import paradigm

        for policy in list(PEEKING_POLICIES) + ["", None]:
            if policy == "uncontrolled_continuous":
                continue
            with self.subTest(policy=policy):
                spec = {"design": {"peeking_policy": policy}} if policy is not None else {}
                report = paradigm.check(spec)
                self.assertNotIn("DSX-PAR-002", codes(report))

    # ── at most one finding per spec ─────────────────────────────────────────

    def test_dsx_par_002_never_fires_twice_for_one_spec(self):
        from dsx.frame import paradigm
        from dsx.spec import PARADIGMS

        specs = (
            [{"inference": {"paradigm": m}} for m in PARADIGMS]
            + [{"inference": {"paradigm": m, "paradigm_justification": ""}} for m in PARADIGMS]
            + [
                {"design": {"peeking_policy": "uncontrolled_continuous"}, "inference": {}},
                {"design": {"peeking_policy": "uncontrolled_continuous"}},
                {},
                {"inference": {}},
            ]
        )
        for spec in specs:
            with self.subTest(spec=spec):
                report = paradigm.check(spec)
                found = [f for f in report.findings if f.code == "DSX-PAR-002"]
                self.assertLessEqual(len(found), 1, [f.where for f in found])

    # ── the fourteen-case symmetry proof (D-09, brief D-12) ──────────────────

    def test_every_justification_clears_dsx_par_002_identically_under_both_paradigms(self):
        # D-05: DSX-PAR-002
        # Genuine cross product, not fourteen hand-written assertions: for
        # every member of PARADIGM_JUSTIFICATIONS against every member of
        # PARADIGMS, a declared justification clears DSX-PAR-002, and the
        # emitted code set for that justification is identical under both
        # paradigms — the mechanical proof that no reason and no paradigm has
        # its own code path.
        from dsx.frame import paradigm
        from dsx.spec import PARADIGM_JUSTIFICATIONS, PARADIGMS

        by_justification: "dict[str, dict[str, set[str]]]" = {}
        for justification in PARADIGM_JUSTIFICATIONS:
            by_justification[justification] = {}
            for member in PARADIGMS:
                with self.subTest(justification=justification, paradigm=member):
                    spec = {
                        "inference": {
                            "paradigm": member,
                            "paradigm_justification": justification,
                        }
                    }
                    report = paradigm.check(spec)
                    found = [f for f in report.findings if f.code == "DSX-PAR-002"]
                    self.assertEqual(len(found), 0, [f.where for f in found])
                    by_justification[justification][member] = codes(report)

        # Symmetry: for each justification, the emitted code set is identical
        # across both paradigms.
        for justification, per_paradigm in by_justification.items():
            with self.subTest(justification=justification):
                members = list(per_paradigm)
                first = per_paradigm[members[0]]
                for other in members[1:]:
                    self.assertEqual(
                        first, per_paradigm[other],
                        f"{justification}: {members[0]} emitted {first}, "
                        f"{other} emitted {per_paradigm[other]}",
                    )

        # No reason is treated as weaker: every justification's finding set is
        # the same size as every other's, under each paradigm.
        for member in PARADIGMS:
            sizes = {
                len(by_justification[j][member]) for j in PARADIGM_JUSTIFICATIONS
            }
            self.assertEqual(
                len(sizes), 1,
                f"paradigm={member}: justifications did not all produce "
                f"finding sets of identical size: {sizes}",
            )

    # ── no double-firing with DSX-SPEC-085 ────────────────────────────────────

    def test_bad_fixture_out_of_vocab_justification_is_dsx_spec_085_only(self):
        # One defect, one code (T-9-14): examples/bad-ANALYSIS-SPEC.yaml
        # declares an out-of-vocabulary paradigm_justification. DSX-PAR-002
        # must never re-check membership, so it must stay silent while
        # DSX-SPEC-085 owns the finding. Asserted independently of the
        # existing pinned three-finding test elsewhere in this module (which
        # exercises a synthetic spec with three invalid inference fields), so
        # a future narrowing of DSX-SPEC-085 breaks in both places.
        #
        # Note: the fixture on disk declares only paradigm_justification
        # (gut_feeling) out of vocabulary — paradigm (frequentist) and
        # declared_at (pre_data) are both valid members — so this pins one
        # DSX-SPEC-085 finding, not three. Three is the count the synthetic
        # spec at test_inference_vocabulary_violations_report_three_high_findings
        # exercises; that count does not apply to this real fixture.
        from dsx.frame import paradigm
        from dsx.loader import load

        spec = load(str(self.ROOT / "examples" / "bad-ANALYSIS-SPEC.yaml"))
        structure_report = validate_structure(spec)
        spec_085 = [f for f in structure_report.findings if f.code == "DSX-SPEC-085"]
        self.assertEqual(len(spec_085), 1, [f.where for f in spec_085])
        self.assertEqual(spec_085[0].where, "spec.inference.paradigm_justification")

        paradigm_report = paradigm.check(spec)
        self.assertNotIn("DSX-PAR-002", codes(paradigm_report))

    def test_good_fixture_never_fires_dsx_par_002_at_any_gate_point(self):
        fixture = self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml"
        for point in ("plan", "execute", "verify", "ship"):
            with self.subTest(point=point):
                with tempfile.TemporaryDirectory() as tmp:
                    if point in ("verify", "ship"):
                        # A fresh temporary directory has no recorded plan-time
                        # header; prereg's missing-header CheckError would
                        # otherwise abort verify/ship before this test's own
                        # DSX-PAR-002 assertion is even reachable.
                        seed_plan_header(tmp, fixture)
                    out, err = io.StringIO(), io.StringIO()
                    with redirect_stdout(out), redirect_stderr(err):
                        cli.main(
                            ["gate", point, "--spec", str(fixture), "--phase-dir", tmp, "--json"]
                        )
                    raw = err.getvalue() or out.getvalue()
                    report = json.loads(raw)
                found = {f["code"] for f in report["findings"]}
                self.assertNotIn("DSX-PAR-002", found)


class TestParadigmOutOfVocabularyFallback(unittest.TestCase):
    """An ``inference.paradigm`` that is non-blank but outside ``PARADIGMS``.

    ``inference.paradigm`` has no enum enforcement that blocks ``dsx gate
    plan`` — membership is ``DSX-SPEC-085``'s job at HIGH, which is below
    plan's CRITICAL threshold — so a typo like ``bayesain`` reaches every
    check in this module as a live third state, alongside "a valid member"
    and "blank or absent".

    ``_check_monitoring_discipline`` has always handled that third state by
    treating it exactly like an undeclared paradigm. These tests pin the
    other two readers of the field to the same reading, so the manifest can
    never assert that a family was "not selected" in the very report where
    that family fired.
    """

    # Every entry must still be outside PARADIGMS *after* normalize() — a
    # case or whitespace variant of a real member is a valid declaration,
    # not an out-of-vocabulary one, and is pinned separately below.
    OUT_OF_VOCAB = ("bayesain", "bayes", "not-a-paradigm", "freq")

    def test_manifest_never_calls_a_family_not_applied_when_it_fired(self):
        # T-6-14's honesty invariant, extended to the out-of-vocabulary case:
        # every prefix DSX-PAR-001 reports as 'not applied' must match no code
        # that actually fired in the same report. A manifest that contradicts
        # its own run is the one defect this code exists to make impossible.
        from dsx.frame import paradigm
        from dsx.spec import PARADIGMS

        declarations = list(PARADIGMS) + list(self.OUT_OF_VOCAB) + ["", None]
        for declared in declarations:
            for policy in ("uncontrolled_continuous", "fixed_horizon"):
                spec = {
                    "inference": {"paradigm": declared},
                    "design": {"peeking_policy": policy},
                }
                with self.subTest(paradigm=declared, policy=policy):
                    report = paradigm.check(spec)
                    fired = {f.code for f in report.findings}
                    manifest = [f for f in report.findings if f.code == "DSX-PAR-001"][0]
                    for prefix in manifest.data.get("not_applied") or {}:
                        contradicted = sorted(c for c in fired if c.startswith(prefix))
                        self.assertEqual(
                            contradicted,
                            [],
                            f"DSX-PAR-001 reports {prefix} as not applied, but "
                            f"{contradicted} fired in the same report",
                        )

    def test_out_of_vocabulary_paradigm_selects_every_conditional_family(self):
        # Same fallback as an undeclared paradigm: narrowing the applied set
        # is what declaring a *recognised* paradigm buys (D-10). An
        # unrecognised string must never buy that narrowing.
        from dsx.frame import paradigm

        undeclared = paradigm.check({"inference": {}})
        baseline = set(
            [f for f in undeclared.findings if f.code == "DSX-PAR-001"][0].data["applied"]
        )
        for declared in self.OUT_OF_VOCAB:
            with self.subTest(paradigm=declared):
                report = paradigm.check({"inference": {"paradigm": declared}})
                manifest = [f for f in report.findings if f.code == "DSX-PAR-001"][0]
                self.assertEqual(set(manifest.data["applied"]), baseline)

    def test_out_of_vocabulary_paradigm_under_uncontrolled_design_fires_par_002(self):
        # DSX-PAR-002's requiredness half asks whether a usable paradigm was
        # declared under a design that needs one. An unrecognised string is
        # not a usable declaration, so the gap is still open and the code
        # must still fire — exactly once, pointing at the paradigm field.
        from dsx.frame import paradigm

        for declared in self.OUT_OF_VOCAB:
            with self.subTest(paradigm=declared):
                spec = {
                    "inference": {"paradigm": declared},
                    "design": {"peeking_policy": "uncontrolled_continuous"},
                }
                report = paradigm.check(spec)
                found = [f for f in report.findings if f.code == "DSX-PAR-002"]
                self.assertEqual(len(found), 1)
                self.assertEqual(found[0].severity, Severity.HIGH)
                # D-05: DSX-PAR-002
                self.assertEqual(found[0].where, "spec.inference.paradigm")

    def test_out_of_vocabulary_paradigm_under_controlled_design_stays_silent(self):
        # The requiredness half is gated on the uncontrolled policy, not on
        # membership. Without that policy there is no DSX-PAR-002 gap to
        # report, and membership stays DSX-SPEC-085's to own (D-08).
        from dsx.frame import paradigm

        for declared in self.OUT_OF_VOCAB:
            with self.subTest(paradigm=declared):
                spec = {
                    "inference": {"paradigm": declared},
                    "design": {"peeking_policy": "fixed_horizon"},
                }
                report = paradigm.check(spec)
                self.assertNotIn("DSX-PAR-002", codes(report))

    def test_every_out_of_vocab_fixture_is_still_out_of_vocab_after_normalize(self):
        # Guards the tuple above against rot: normalize() lowercases and
        # folds separators, so an entry like "Frequentist " would silently
        # become a valid member and stop testing anything.
        from dsx.spec import PARADIGMS, normalize

        for declared in self.OUT_OF_VOCAB:
            with self.subTest(paradigm=declared):
                self.assertNotIn(normalize(declared), PARADIGMS)

    def test_case_and_whitespace_variants_of_a_member_stay_declared(self):
        # The fallback must key on membership *after* normalization, never on
        # a raw string compare — otherwise "  BAYESIAN " would be demoted to
        # undeclared and wrongly widen the applied set.
        from dsx.frame import paradigm
        from dsx.spec import PARADIGMS

        for member in PARADIGMS:
            for variant in (member.upper(), f"  {member} ", member.capitalize()):
                with self.subTest(variant=variant):
                    report = paradigm.check({"inference": {"paradigm": variant}})
                    manifest = [f for f in report.findings if f.code == "DSX-PAR-001"][0]
                    canonical = paradigm.check({"inference": {"paradigm": member}})
                    expected = [f for f in canonical.findings if f.code == "DSX-PAR-001"][0]
                    self.assertEqual(manifest.data["applied"], expected.data["applied"])


# ── Phase 11.1-01: full-frame cleaning + fit-after-split (DSX-CODE-020/021) ────


class TestPhase11_1Code(unittest.TestCase):
    ROOT = Path(__file__).resolve().parent.parent

    def _entrypoint(self, tmp: str, text: str, name: str = "entry.py") -> str:
        Path(tmp, name).write_text(text, encoding="utf-8")
        return name

    def _check(self, tmp: str, entry: str):
        from dsx.checks import code as code_mod

        return code_mod.check(
            {
                "model": {"task": "binary_classification"},
                "reproducibility": {"entrypoint": entry},
            },
            tmp,
        )

    # ── DSX-CODE-020: full-frame cleaning before the split ──────────────────

    def test_fillna_mean_before_split_is_critical(self):
        # D-05: DSX-CODE-020
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "df['Age'] = df['Age'].fillna(df['Age'].mean())\n"
                "train_test_split(df)\n",
            )
            report = self._check(tmp, entry)
            found = [f for f in report.findings if f.code == "DSX-CODE-020"]
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].severity, Severity.CRITICAL)

    def test_spread_filter_before_split_is_critical(self):
        entry_text = (
            "from sklearn.model_selection import train_test_split\n"
            "df = df[(df['Balance'] - df['Balance'].mean()).abs() "
            "/ df['Balance'].std() < 3]\n"
            "train_test_split(df)\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(tmp, entry_text)
            report = self._check(tmp, entry)
            self.assertIn("DSX-CODE-020", codes(report))

    def test_full_frame_cleaning_at_or_after_split_produces_no_finding(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n"
                "df['Age'] = df['Age'].fillna(df['Age'].mean())\n",
            )
            report = self._check(tmp, entry)
            self.assertNotIn("DSX-CODE-020", codes(report))

    def test_no_split_marker_full_frame_cleaning_still_fires(self):
        # A missing split is not a licence.
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp, "df['Age'] = df['Age'].fillna(df['Age'].mean())\n"
            )
            report = self._check(tmp, entry)
            self.assertIn("DSX-CODE-020", codes(report))

    def test_idiom_in_comment_or_import_line_produces_no_finding(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "# df['Age'] = df['Age'].fillna(df['Age'].mean())\n"
                "from x import fillna_mean_helper\n",
            )
            report = self._check(tmp, entry)
            self.assertNotIn("DSX-CODE-020", codes(report))

    def test_at_most_one_dsx_code_020_lowest_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "df['Age'] = df['Age'].fillna(df['Age'].mean())\n"
                "df['Bal'] = df['Bal'].fillna(df['Bal'].median())\n",
            )
            report = self._check(tmp, entry)
            found = [f for f in report.findings if f.code == "DSX-CODE-020"]
            self.assertEqual(len(found), 1)
            self.assertIn("Line 1", found[0].detail)

    def test_empty_and_comment_only_source_no_exception(self):
        with tempfile.TemporaryDirectory() as tmp:
            for text in ("", "# only a comment\n"):
                with self.subTest(text=text):
                    entry = self._entrypoint(tmp, text)
                    report = self._check(tmp, entry)
                    self.assertNotIn("DSX-CODE-020", codes(report))

    def test_good_fixture_entrypoint_produces_no_dsx_code_020(self):
        from dsx.checks import code as code_mod

        report = code_mod.check(
            {
                "model": {"task": "binary_classification"},
                "reproducibility": {"entrypoint": "analysis/activation_readout.py"},
            },
            str(self.ROOT / "examples"),
        )
        self.assertNotIn("DSX-CODE-020", codes(report))

    def test_full_frame_impute_predicate_matches_paper_style_idiom(self):
        from dsx.checks import code as code_mod

        self.assertTrue(
            code_mod._is_full_frame_impute(
                "df['Age'] = df['Age'].fillna(df['Age'].mean())"
            )
        )
        # Phase 11.1.1: both halves are required. Splitting the old single
        # pattern into two independent searches must not have widened it.
        self.assertFalse(code_mod._is_full_frame_impute("s.fillna(0)"))
        self.assertFalse(code_mod._is_full_frame_impute("x = df['a'].mean()"))

    def test_full_frame_spread_filter_predicate_matches_paper_style_idiom(self):
        from dsx.checks import code as code_mod

        self.assertTrue(
            code_mod._is_full_frame_spread_filter(
                "df = df[(df['Balance'] - df['Balance'].mean()).abs() "
                "/ df['Balance'].std() < 3]"
            )
        )
        # Phase 11.1.1: both halves are required, and the subscript half still
        # demands an identifier character immediately before the bracket.
        self.assertFalse(code_mod._is_full_frame_spread_filter("no brackets .std()"))
        self.assertFalse(code_mod._is_full_frame_spread_filter("df['a'] only"))
        self.assertFalse(code_mod._is_full_frame_spread_filter("a[0]"))

    # ── DSX-CODE-021: fit at/after split not on a recognised training frame ─

    def test_fit_call_bare_frame_after_split_is_critical(self):
        # D-05: DSX-CODE-021
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "X_train, X_test = train_test_split(df)\n"
                "model.fit(df)\n",
            )
            report = self._check(tmp, entry)
            found = [f for f in report.findings if f.code == "DSX-CODE-021"]
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].severity, Severity.CRITICAL)
            self.assertNotIn("DSX-CODE-001", codes(report))

    def test_imputer_constructed_inline_after_split_fires(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n"
                "SimpleImputer().fit(df)\n",
            )
            report = self._check(tmp, entry)
            self.assertIn("DSX-CODE-021", codes(report))

    def test_fit_transform_bracketed_full_frame_after_split_fires(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(data)\n"
                "min_max_scaler.fit_transform(data[['Balance']])\n",
            )
            report = self._check(tmp, entry)
            self.assertIn("DSX-CODE-021", codes(report))

    def test_fit_call_x_train_after_split_no_finding(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "X_train, X_test = train_test_split(df)\n"
                "imputer.fit(X_train)\n",
            )
            report = self._check(tmp, entry)
            found = codes(report)
            self.assertNotIn("DSX-CODE-021", found)
            self.assertNotIn("DSX-CODE-001", found)

    def test_lexicon_prefix_variants_after_split_no_finding(self):
        variants = ("X_train_scaled", "train_df[cols]", "X_train.values")
        for variant in variants:
            with self.subTest(variant=variant):
                with tempfile.TemporaryDirectory() as tmp:
                    entry = self._entrypoint(
                        tmp,
                        "from sklearn.model_selection import train_test_split\n"
                        "train_test_split(df)\n"
                        f"model.fit({variant})\n",
                    )
                    report = self._check(tmp, entry)
                    self.assertNotIn("DSX-CODE-021", codes(report))

    def test_fit_call_before_split_no_dsx_code_021(self):
        # That case is DSX-CODE-001's.
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "model.fit(df)\n"
                "train_test_split(df)\n",
            )
            report = self._check(tmp, entry)
            self.assertNotIn("DSX-CODE-021", codes(report))
            self.assertIn("DSX-CODE-001", codes(report))

    def test_no_split_marker_no_dsx_code_021(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(tmp, "model.fit(df)\n")
            report = self._check(tmp, entry)
            self.assertNotIn("DSX-CODE-021", codes(report))

    def test_malformed_fit_calls_no_finding_no_exception(self):
        # Phase 11.1.1 plan 01: this fixture's unclosed `imputer.fit(df` raises
        # `SyntaxError: '(' was never closed` under ast.parse, so this test is
        # already the committed pin on the FALLBACK (text-scan) path, not an
        # AST test. Do not "fix" it to parse.
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n"
                "imputer.fit(df\n"
                "model.fit(42)\n",
            )
            report = self._check(tmp, entry)
            self.assertNotIn("DSX-CODE-021", codes(report))

    # ── Phase 11.1.1 plan 02: DSX-CODE-021 argument extraction moves to ──────
    # ── AST call-node resolution (SC2/SC3), fallback hardened to agree ───────

    # -- SC2 firing: keyword arguments, partial_fit, chained and multi-line --

    def test_fit_keyword_argument_after_split_fires_code_021(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n"
                "model.fit(X=data, y=target)\n",
            )
            report = self._check(tmp, entry)
            found = [f for f in report.findings if f.code == "DSX-CODE-021"]
            self.assertEqual(len(found), 1)
            self.assertIn("'data'", found[0].detail)
            self.assertNotIn("'X'", found[0].detail)
            self.assertNotIn("'target'", found[0].detail)

    def test_fit_transform_keyword_argument_after_split_fires_code_021(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n"
                "scaler.fit_transform(X=data[['Age']])\n",
            )
            report = self._check(tmp, entry)
            found = [f for f in report.findings if f.code == "DSX-CODE-021"]
            self.assertEqual(len(found), 1)
            self.assertIn("data[['Age']]", found[0].detail)

    def test_partial_fit_after_split_fires_code_021(self):
        """Deliberate widening: `partial_fit` is already in FIT_LEAK_MARKERS,
        so the same call BEFORE the split already fires DSX-CODE-001 today;
        holding the AST method set at {fit, fit_transform} would mean
        deliberately writing a known blind spot into new code."""
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n"
                "model.partial_fit(data)\n",
            )
            report = self._check(tmp, entry)
            found = [f for f in report.findings if f.code == "DSX-CODE-021"]
            self.assertEqual(len(found), 1)
            self.assertIn("'data'", found[0].detail)

    def test_chained_call_argument_after_split_fires_code_021(self):
        """One of the three forms superseded plan 03 was written to pin as
        knowingly-uncaught, promoted to a FIRING test under that plan's own
        promotion protocol now that the AST path resolves a chained-call
        argument."""
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n"
                "model.fit(loader.get_full_frame())\n",
            )
            report = self._check(tmp, entry)
            found = [f for f in report.findings if f.code == "DSX-CODE-021"]
            self.assertEqual(len(found), 1)
            self.assertIn("loader.get_full_frame()", found[0].detail)

    def test_multi_line_fit_call_after_split_fires_code_021(self):
        # The call opens on one line and the argument sits on the next; the
        # reported line is the line the CALL opens on.
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n"
                "model.fit(\n"
                "    data\n"
                ")\n",
            )
            report = self._check(tmp, entry)
            found = [f for f in report.findings if f.code == "DSX-CODE-021"]
            self.assertEqual(len(found), 1)
            self.assertIn("Line 3", found[0].detail)
            self.assertIn("'data'", found[0].detail)

    # -- SC2 silence: keyword training frame, out-of-allowlist, constants ----

    def test_keyword_training_frame_after_split_no_finding(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n"
                "model.fit(X=X_train)\n",
            )
            report = self._check(tmp, entry)
            self.assertNotIn("DSX-CODE-021", codes(report))

    def test_out_of_allowlist_keyword_draws_nothing_on_both_paths(self):
        # The false-positive parity case: an any-identifier keyword prefix
        # on the fallback would make model.fit(y=y_test) a CRITICAL finding
        # there while the AST path stays silent -- the two mechanisms
        # disagreeing about one source line. Both must stay silent.
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n"
                "model.fit(y=y_test)\n",
            )
            report = self._check(tmp, entry)
            self.assertNotIn("DSX-CODE-021", codes(report))

        # Forced onto the fallback by a trailing unclosed parenthesis.
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n"
                "model.fit(y=y_test)\n"
                "unclosed(\n",
            )
            report = self._check(tmp, entry)
            reached_fallback = any(
                f.data.get("scan") == "text-fallback" for f in report.findings
            ) or any("fallback scan" in line for line in report.passed_checks)
            self.assertTrue(reached_fallback)
            self.assertNotIn("DSX-CODE-021", codes(report))

    def test_constant_first_argument_draws_nothing_on_both_paths(self):
        # Today's documented behaviour (dsx/checks/code.py: FIT_CALL_RE's
        # [A-Za-z_] anchor) already excludes a bare NUMERIC or STRING first
        # argument on both paths -- verified against unmodified source
        # before writing this test -- and must not change direction.
        # `model.fit(None)` is deliberately NOT pinned here: measured
        # against unmodified source, it currently FIRES on both paths
        # (FIT_CALL_RE has no bareword-constant exclusion -- "None" reads
        # as an ordinary identifier to a regex), contradicting the naive
        # expectation that dsx/checks/code.py:112-114's numeric-anchor
        # comment already covers it. See
        # test_bareword_constant_first_argument_draws_nothing_on_the_ast_path
        # below for that case, deviation documented in the plan-02 SUMMARY.
        for literal in ("42", "'x'"):
            with self.subTest(literal=literal):
                with tempfile.TemporaryDirectory() as tmp:
                    entry = self._entrypoint(
                        tmp,
                        "from sklearn.model_selection import train_test_split\n"
                        "train_test_split(df)\n"
                        f"model.fit({literal})\n",
                    )
                    report = self._check(tmp, entry)
                    self.assertNotIn("DSX-CODE-021", codes(report))

                with tempfile.TemporaryDirectory() as tmp:
                    entry = self._entrypoint(
                        tmp,
                        "from sklearn.model_selection import train_test_split\n"
                        "train_test_split(df)\n"
                        f"model.fit({literal})\n"
                        "unclosed(\n",
                    )
                    report = self._check(tmp, entry)
                    self.assertNotIn("DSX-CODE-021", codes(report))

    def test_bareword_constant_first_argument_draws_nothing_on_the_ast_path(self):
        # [Rule 1 deviation, see plan-02 SUMMARY] `model.fit(None)` fires
        # DSX-CODE-021 on unmodified source (measured), because
        # DSX-CODE-021 is not yet wired to the AST path and FIT_CALL_RE has
        # no bareword-constant exclusion. `_first_argument`'s
        # ast.Constant -> None rule (task 2) closes this on the PRIMARY
        # path only; the fallback keeps the pre-existing miss, which is
        # out of this plan's scope and not asserted here.
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n"
                "model.fit(None)\n",
            )
            report = self._check(tmp, entry)
            self.assertNotIn("DSX-CODE-021", codes(report))

    # -- SC3: multiple calls, source order, nested tie-break -----------------

    def test_semicolon_joined_two_fit_calls_fire_code_021(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n"
                "imputer.fit(X_train); scaler.fit_transform(data)\n",
            )
            report = self._check(tmp, entry)
            found = [f for f in report.findings if f.code == "DSX-CODE-021"]
            self.assertEqual(len(found), 1)
            self.assertIn("'data'", found[0].detail)

    def test_every_fit_call_on_a_line_is_extracted_in_source_order(self):
        # White-box on the extraction mechanism task 2 builds
        # (_call_sites + _first_argument + _render_token). Three fit calls
        # on one line yield three tokens left to right; called twice and
        # compared for equality pins stability.
        import ast

        from dsx.checks import code as code_mod

        source = "imputer.fit(a); scaler.fit_transform(b); model.partial_fit(c)\n"
        tree = ast.parse(source)

        def _tokens():
            sites = code_mod._call_sites(tree)
            return [
                code_mod._render_token(code_mod._first_argument(s.node))
                for s in sites
                if s.name in code_mod.FIT_METHOD_NAMES
            ]

        tokens1 = _tokens()
        self.assertEqual(tokens1, ["a", "b", "c"])
        tokens2 = _tokens()
        self.assertEqual(tokens1, tokens2)

    def test_nested_fit_calls_report_the_textually_first_token(self):
        # [Deviation, see plan-02 SUMMARY] this already passes against
        # unmodified source (single-line `.search()` finds the leftmost
        # `.fit(` occurrence, which happens to be the textually-first
        # call), so it is not part of this task's RED failure set -- the
        # same pattern plan 01's SUMMARY documented for the multi-line
        # open-paren case. Retained as the committed pin for the
        # (line, col, end_col) tie-break `_call_sites` implements: the two
        # Call nodes collide on (line, col), and ascending end_col picks
        # the inner/textually-first-closing call, matching today's answer.
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n"
                "m.fit(full_frame_a).fit(full_frame_b)\n",
            )
            report = self._check(tmp, entry)
            found = [f for f in report.findings if f.code == "DSX-CODE-021"]
            self.assertEqual(len(found), 1)
            self.assertIn("'full_frame_a'", found[0].detail)

    def test_at_most_one_dsx_code_021_lowest_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n"
                "imputer.fit(df)\n"
                "scaler.fit_transform(features)\n",
            )
            report = self._check(tmp, entry)
            found = [f for f in report.findings if f.code == "DSX-CODE-021"]
            self.assertEqual(len(found), 1)
            self.assertIn("Line 3", found[0].detail)

    # ── Phase 11.1.1 plan 03 task 1, Part A: the three forms superseded ──────
    # ── plan 03 was written to pin as permanently uncaught, promoted to ──────
    # ── FIRING tests because the mechanism change closed all three. All ──────
    # ── three already exist, added by plan 02 as part of its own SC2/SC3 ─────
    # ── firing set, before this plan's own task 1 was executed: ──────────────
    # ── test_partial_fit_after_split_fires_code_021 (line ~4739 above), ──────
    # ── test_chained_call_argument_after_split_fires_code_021 (~4756), and ───
    # ── test_multi_line_fit_call_after_split_fires_code_021 (~4773). ─────────
    # ── Measured against the live suite rather than assumed absent -- see ────
    # ── this plan's own SUMMARY, "Part A already satisfied" -- no new test ───
    # ── is added here to avoid a duplicate method name colliding with an ─────
    # ── existing one in the same class. ───────────────────────────────────────

    # ── Phase 11.1.1 plan 03 task 1, Part B: deliberate scope boundaries ─────
    # ── this phase does not close, not true negatives. Each pin's docstring ──
    # ── states the input is a REAL leak (or, for the two fallback-prose ──────
    # ── pins, a REAL false positive) knowingly outside the scanner's reach, ──
    # ── and carries the superseded plan's promotion protocol verbatim: if ────
    # ── this test ever fails because a finding appeared (or, for the two ─────
    # ── fallback-prose pins, disappeared), that is good news and the test ────
    # ── should be promoted to a firing test rather than deleted. ─────────────

    def test_dynamic_dispatch_fit_stays_uncaught_by_design(self):
        """Not a regression -- dynamic dispatch was never caught by the text
        scan either, since neither `getattr(model, "fit")(data)` nor
        `handlers["fit"](data)` carries literal `.fit(`-shaped text.
        `_resolve_callee_name` returns "" for both shapes -- `node.func` is
        a Call in the first case and a Subscript in the second, neither an
        `ast.Name` nor an `ast.Attribute` -- which matches nothing in
        FIT_METHOD_NAMES by construction. Both are REAL leaks before the
        split, measured against the shipped code before writing this test.
        If this test ever fails because a finding appeared, that is good
        news and the
        test should be promoted to a firing test rather than deleted.
        """
        for source in (
            "getattr(model, 'fit')(data)\n"
            "from sklearn.model_selection import train_test_split\n"
            "train_test_split(df)\n",
            "handlers['fit'](data)\n"
            "from sklearn.model_selection import train_test_split\n"
            "train_test_split(df)\n",
        ):
            with self.subTest(source=source):
                with tempfile.TemporaryDirectory() as tmp:
                    entry = self._entrypoint(tmp, source)
                    report = self._check(tmp, entry)
                    self.assertNotIn("DSX-CODE-001", codes(report))

    def test_out_of_allowlist_keyword_stays_uncaught_by_design(self):
        """Deliberate, not a bug: `model.fit(training_frame=data)` after the
        split draws no DSX-CODE-021, because `training_frame` is outside
        FIT_FIRST_PARAM_NAMES. An allowlist trades this miss for immunity
        from the false-positive flood threat T-11.1.1-07 names -- the
        alternative, a blocklist, would report an unrelated keyword's value
        as "the frame this was fitted on". `data` here is a REAL leak: the
        full frame, unsplit. If this test ever fails because a finding
        appeared, that is good news and the
        test should be promoted to a firing test rather than deleted.
        """
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n"
                "model.fit(training_frame=data)\n",
            )
            report = self._check(tmp, entry)
            self.assertNotIn("DSX-CODE-021", codes(report))

    def test_starred_first_argument_stays_uncaught_by_design(self):
        """Deliberate: `model.fit(*args)` after the split draws no
        DSX-CODE-021. `_first_argument` skips a starred `node.args[0]`
        rather than resolving it (§3.4 of 11.1.1-AST-DESIGN.md), and no
        keyword is present to fall back to, so the call resolves to no
        token and no finding. Whatever `args` unpacks to is a REAL,
        unexamined leak surface. If this test ever fails because a finding
        appeared, that is good news and the
        test should be promoted to a firing test rather than deleted.
        """
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n"
                "model.fit(*args)\n",
            )
            report = self._check(tmp, entry)
            self.assertNotIn("DSX-CODE-021", codes(report))

    def test_laundered_training_frame_name_stays_uncaught_by_design(self):
        """Deliberate: `X_train_like = data` then `model.fit(X_train_like)`
        after the split draws no DSX-CODE-021, because `_is_training_frame`
        PREFIX-matches the rendered token's NAME against
        TRAINING_FRAME_NAMES and never follows the assignment --
        `"X_train_like".startswith("X_train")` is True, so the token reads
        as a training frame by name alone. `data` is the REAL leak: the
        full, unsplit frame laundered through a training-frame-shaped
        variable name. If this test ever fails because a finding appeared,
        that is good news and the
        test should be promoted to a firing test rather than deleted.
        """
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n"
                "X_train_like = data\n"
                "model.fit(X_train_like)\n",
            )
            report = self._check(tmp, entry)
            self.assertNotIn("DSX-CODE-021", codes(report))

    def test_split_through_an_alias_stays_uncaught_by_design(self):
        """Different in kind from the other pins in this block: the file
        DOES split -- `do_split` is imported from another module and called
        on line 2 -- but what is pinned is that the scanner reads it as
        having NO split at all, because neither the AST call-name walk
        (`do_split` is not in SPLIT_CALL_NAMES) nor the text-marker union
        (no line contains the literal substring "train_test_split" or any
        other SPLIT_MARKERS entry) can see a split performed entirely
        inside an imported helper. Measured against the shipped code:
        `first_split` is None, so `scaler.fit_transform(data)` (a REAL leak
        if `data` is the unsplit frame) fires DSX-CODE-001 instead of
        DSX-CODE-021, and DSX-CODE-010 ALSO fires, its own text asserting
        "entrypoint has no declared split marker" for a file that plainly
        contains one -- a known false statement in the finding's own text,
        raised here for the end-of-phase human check rather than silently
        absorbed. If this test ever fails because the code set changed,
        that is worth a fresh look either way and the
        test should be promoted to a firing test rather than deleted.
        """
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from mymodule import do_split\n"
                "a, b = do_split(df)\n"
                "scaler.fit_transform(data)\n",
            )
            report = self._check(tmp, entry)
            found = codes(report)
            self.assertEqual(found, {"DSX-CODE-001", "DSX-CODE-010"})
            code_010 = [f for f in report.findings if f.code == "DSX-CODE-010"]
            self.assertIn("no declared split marker", code_010[0].title)

    def test_backslash_continuation_on_the_fallback_stays_uncaught_by_design(
        self,
    ):
        """A backslash-continued fit call IS caught on the parsed path
        (pinned by test_fit_backslash_continuation_before_split_fires_
        code_001 above -- the join happens inside ast.parse itself). This
        pin is the fallback's own limitation: forced onto the fallback by
        an unrelated unclosed parenthesis elsewhere in the file, the same
        backslash-continued `model.fit \` / `(df)` pair draws NOTHING,
        because the fallback's FIT_LEAK_MARKERS regex matches one physical
        line at a time and the joining helper was deliberately never
        written (11.1.1-AST-DESIGN.md §2.2, "Not carried over"). This is a
        REAL leak before the split. If this test ever fails because a
        finding appeared, that is good news and the
        test should be promoted to a firing test rather than deleted.
        """
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "model.fit " + chr(92) + "\n"
                "(df)\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n"
                "unclosed(\n",
            )
            report = self._check(tmp, entry)
            reached_fallback = any(
                f.data.get("scan") == "text-fallback" for f in report.findings
            ) or any("fallback scan" in line for line in report.passed_checks)
            self.assertTrue(reached_fallback)
            self.assertNotIn("DSX-CODE-001", codes(report))

    def test_trailing_comment_fit_on_the_fallback_stays_uncaught_by_design(
        self,
    ):
        """The REVERSE direction from every other pin in this block: this
        one documents a false positive that STAYS OPEN on the fallback,
        rather than a leak that stays unseen. `z = 1  # scaler.fit(data)`
        is pure prose -- the fit call is inside a trailing comment, not
        code -- and forced onto the fallback by an unrelated unclosed
        parenthesis elsewhere, it STILL fires DSX-CODE-001 CRITICAL.
        Every text guard in this module tests only `stripped.startswith(
        "#")`, a LEADING comment; a line that carries real code before a
        trailing `#` is not skipped, so FIT_LEAK_MARKERS matches inside the
        comment text. Measured, not assumed. If this test ever fails
        because the finding disappeared, that would mean the fallback's
        comment guard was widened -- good news -- but until then this pin
        records the false positive that stays, and the
        test should be promoted to a firing test rather than deleted.
        """
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "z = 1  # scaler.fit(data)\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n"
                "unclosed(\n",
            )
            report = self._check(tmp, entry)
            reached_fallback = any(
                f.data.get("scan") == "text-fallback" for f in report.findings
            ) or any("fallback scan" in line for line in report.passed_checks)
            self.assertTrue(reached_fallback)
            self.assertIn("DSX-CODE-001", codes(report))

    def test_multiline_string_interior_line_stays_uncaught_by_design(self):
        """A split marker written on a STRICTLY INTERIOR line of a
        triple-quoted string is masked deliberately (Rule B,
        `_prose_line_indices`), so it does not count as a split.
        `_prose_line_indices` currently has exactly ONE consumer in the
        shipped code -- the split-marker text scan via `_first_line_
        matching`'s `masked` parameter -- named "In this wave the mask has
        exactly one consumer" in the source comment above it. The plan's
        own draft framed this pin around a "cleaning idiom" (DSX-CODE-020),
        but measured against the shipped code, DSX-CODE-020's own text loop
        applies NO masking at all -- a cleaning idiom inside a multi-line
        string's interior line still fires DSX-CODE-020 unconditionally,
        which is the larger, separately-documented finding of this plan
        (see this plan's SUMMARY, "prose mask coverage"). This pin is
        rewritten to test the one place the mask genuinely applies: a split
        marker string on the interior line of a triple-quoted assignment
        stays masked, so a REAL split-then-fit sequence with a marker
        mentioned only in prose reads, incorrectly, as having no split. If
        this test ever fails because the split was suddenly detected, that
        is good news and the
        test should be promoted to a firing test rather than deleted.
        """
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "sql = " + '"""' + "\n"
                "train_test_split lives here\n"
                + '"""' + "\n"
                "scaler.fit_transform(data)\n",
            )
            report = self._check(tmp, entry)
            found = codes(report)
            self.assertNotIn("DSX-CODE-021", found)
            self.assertIn("DSX-CODE-001", found)
            self.assertIn("DSX-CODE-010", found)

    # ── Phase 11.1.1 plan 03 task 1, Part C: the documentation obligation ────
    # ── made executable. FAILS until task 4 lands README.md's new section; ───
    # ── this and task 4 are RED and GREEN of one obligation. ──────────────────

    def test_entrypoint_scan_scope_boundary_is_documented(self):
        readme = (self.ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("### What the entrypoint scan does not catch", readme)
        required_substrings = (
            "getattr",
            "handlers[",
            "bound method",
            "training_frame",
            "starred",
            "laundered",
            "alias",
            "exec",
            "backslash",
            "trailing comment",
        )
        for substring in required_substrings:
            with self.subTest(substring=substring):
                self.assertIn(substring, readme)

    # ── Phase 11.1.1 plan 01: AST call-node walk replaces the line-ordered ──
    # ── regex scan that decides DSX-CODE-001 ─────────────────────────────────

    # -- SC1 firing: whitespace, tab, backslash and multi-line forms --------

    def test_fit_space_before_paren_before_split_fires_code_001(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "model.fit (df)\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n",
            )
            report = self._check(tmp, entry)
            found = [f for f in report.findings if f.code == "DSX-CODE-001"]
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].severity, Severity.CRITICAL)

    def test_fit_double_space_before_paren_before_split_fires_code_001(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "model.fit  (df)\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n",
            )
            report = self._check(tmp, entry)
            found = [f for f in report.findings if f.code == "DSX-CODE-001"]
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].severity, Severity.CRITICAL)

    def test_fit_tab_before_paren_before_split_fires_code_001(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "model.fit" + chr(9) + "(df)\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n",
            )
            report = self._check(tmp, entry)
            found = [f for f in report.findings if f.code == "DSX-CODE-001"]
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].severity, Severity.CRITICAL)

    def test_fit_backslash_continuation_before_split_fires_code_001(self):
        # A fit call split across two physical lines by a trailing backslash.
        # Reported at the FIRST physical line of the statement.
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "model.fit " + chr(92) + "\n"
                "(df)\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n",
            )
            report = self._check(tmp, entry)
            found = [f for f in report.findings if f.code == "DSX-CODE-001"]
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].severity, Severity.CRITICAL)
            self.assertIn("Line 1", found[0].detail)

    def test_fit_multiline_open_paren_before_split_fires_code_001(self):
        # `model.fit(` on one line, the frame on the next. Uncatchable by a
        # per-physical-line scan; new coverage the AST walk buys.
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "model.fit(\n"
                "    df\n"
                ")\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n",
            )
            report = self._check(tmp, entry)
            found = [f for f in report.findings if f.code == "DSX-CODE-001"]
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].severity, Severity.CRITICAL)
            self.assertIn("Line 1", found[0].detail)

    # -- Preservation: must pass against unmodified source and keep passing --

    def test_fit_zero_whitespace_before_split_still_fires_code_001(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "model.fit(df)\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n",
            )
            report = self._check(tmp, entry)
            self.assertIn("DSX-CODE-001", codes(report))

    # -- Silence, and no exception -------------------------------------------

    def test_empty_and_fitless_and_lone_backslash_sources_produce_no_code_001(self):
        with tempfile.TemporaryDirectory() as tmp:
            cases = ("", "# only a comment\n", "x = 1\n", chr(92) + "\n")
            last_entry = None
            for text in cases:
                with self.subTest(text=repr(text)):
                    entry = self._entrypoint(tmp, text)
                    report = self._check(tmp, entry)
                    self.assertNotIn("DSX-CODE-001", codes(report))
                last_entry = entry

            # Re-pin: the lone-backslash fixture (the last case above) is a
            # SyntaxError under ast.parse, so it is proven to reach the
            # fallback path rather than assumed to.
            report = self._check(tmp, last_entry)
            findings_signal = any(
                f.data.get("scan") == "text-fallback" for f in report.findings
            )
            passed_signal = any(
                "text-fallback" in line for line in report.passed_checks
            )
            self.assertTrue(findings_signal or passed_signal)

    # -- Ordering and sort ----------------------------------------------------

    def test_lowest_physical_line_reported_for_code_001(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "imputer.fit(df)\n"
                "scaler.fit_transform(df)\n"
                "model.fit(df)\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n",
            )
            report1 = self._check(tmp, entry)
            found1 = [f for f in report1.findings if f.code == "DSX-CODE-001"]
            self.assertEqual(len(found1), 1)
            self.assertEqual(found1[0].data.get("fit_line"), 1)
            self.assertIn("Line 1", found1[0].detail)

            report2 = self._check(tmp, entry)
            found2 = [f for f in report2.findings if f.code == "DSX-CODE-001"]
            self.assertEqual(len(found2), 1)
            self.assertEqual(
                found2[0].data.get("fit_line"), found1[0].data.get("fit_line")
            )

    def test_call_sites_are_sorted_by_line_col_and_end_col(self):
        # White-box on _call_sites. (line, col) alone collides on nested and
        # chained calls -- m.fit(x).fit(y) yields two sites at (0, 0) -- so
        # the tie-break is ascending end_col_offset, which reproduces today's
        # left-to-right finditer token.
        import ast

        from dsx.checks import code as code_mod

        tree = ast.parse("m.fit(full_frame_a).fit(full_frame_b)\n")
        sites = code_mod._call_sites(tree)
        fit_sites = [s for s in sites if s.name == "fit"]
        self.assertGreaterEqual(len(fit_sites), 2)
        first_arg = fit_sites[0].node.args[0]
        self.assertEqual(ast.unparse(first_arg), "full_frame_a")

    # -- The two measured false positives --------------------------------------

    def test_docstring_mentioning_fit_draws_no_code_001(self):
        """Control: deleting the sentence below makes the identical file pass
        under the pre-AST text scan today already -- the sentence alone is
        what draws DSX-CODE-001 CRITICAL there."""
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                '"""We never call scaler.fit(X) on the full frame."""\n'
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n",
            )
            report = self._check(tmp, entry)
            self.assertNotIn("DSX-CODE-001", codes(report))

    def test_notebook_markdown_cell_mentioning_fit_draws_no_code_001(self):
        nb = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "source": [
                        "We must never call `scaler.fit(X)` on the full "
                        "frame before the split.\n"
                    ],
                },
                {
                    "cell_type": "code",
                    "source": [
                        "from sklearn.model_selection import train_test_split\n",
                        "train_test_split(df)\n",
                    ],
                },
            ]
        }
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(tmp, json.dumps(nb), name="entry.ipynb")
            report = self._check(tmp, entry)
            self.assertNotIn("DSX-CODE-001", codes(report))

    # -- Notebook line geometry, both shapes, against the baseline measured --
    # -- this session with the UNMODIFIED reader (not against post-change --
    # -- code) ------------------------------------------------------------

    def test_notebook_code_cell_line_numbers_are_unchanged_by_the_markdown_filter(
        self,
    ):
        # Two notebooks identical except that the markdown cell's last
        # `source` element ends with a newline in one and not the other.
        # Measured this session against the unmodified reader: Line 6 for
        # the trailing-newline shape, Line 5 for the no-trailing-newline
        # shape (0-based indices 5 and 4). Hardcoded literals -- a test that
        # recomputes the expectation from the new reader cannot detect a
        # shift.
        for trailing, expected_line in ((True, 6), (False, 5)):
            with self.subTest(trailing=trailing):
                last = "before splitting.\n" if trailing else "before splitting."
                nb = {
                    "cells": [
                        {
                            "cell_type": "markdown",
                            "source": [
                                "We must never fit on the full frame.\n",
                                last,
                            ],
                        },
                        {
                            "cell_type": "code",
                            "source": [
                                "from sklearn.model_selection import train_test_split\n",
                                "train_test_split(df)\n",
                                "scaler.fit_transform(data)\n",
                            ],
                        },
                    ]
                }
                with tempfile.TemporaryDirectory() as tmp:
                    entry = self._entrypoint(tmp, json.dumps(nb), name="entry.ipynb")
                    report = self._check(tmp, entry)
                    found = [f for f in report.findings if f.code == "DSX-CODE-021"]
                    self.assertEqual(len(found), 1)
                    self.assertIn(f"Line {expected_line}", found[0].detail)

    # -- Phase 11.1.1 plan 02 task 3: the notebook reader ---------------------
    # -- Notebook markdown prose and both trailing-newline geometry shapes ---
    # -- are already pinned by test_notebook_markdown_cell_mentioning_fit_ ---
    # -- draws_no_code_001 and test_notebook_code_cell_line_numbers_are_ -----
    # -- unchanged_by_the_markdown_filter above -- plan 01 closed the ------
    # -- notebook markdown false positive one task early (character-wise ----
    # -- blanking), so those two are not duplicated here (see the plan-02 ---
    # -- SUMMARY). What remains for this task: BOM handling, magic repair, --
    # -- the uncaught cell-magic-body pin, and degenerate notebook shapes. --

    def test_notebook_magics_are_repaired_and_take_the_ast_path(self):
        nb = {
            "cells": [
                {
                    "cell_type": "code",
                    "source": [
                        "%matplotlib inline\n",
                        "!pip install pandas\n",
                        "t = %timeit -o f()\n",
                        "from sklearn.model_selection import train_test_split\n",
                        "train_test_split(df)\n",
                        "model.fit(df)\n",
                    ],
                }
            ]
        }
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(tmp, json.dumps(nb), name="entry.ipynb")
            report = self._check(tmp, entry)
            # model.fit(df) sits AFTER train_test_split(df) here, so a
            # successful repair-then-parse fires DSX-CODE-021 (fit at/after
            # the split on a non-training-frame token), not DSX-CODE-001.
            found = [f for f in report.findings if f.code == "DSX-CODE-021"]
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].data.get("scan"), "ast")

    def test_notebook_cell_magic_body_stays_on_the_fallback(self):
        """Uncaught-by-design: a `%%bash` cell body is not Python and is not
        repaired (blanking only the `%%bash` line would leave a non-Python
        body behind), so the notebook scans on the fallback. This is a REAL
        limitation, not a true negative. If this test ever fails because
        the notebook took the AST path, that is good news and the test
        should be promoted rather than deleted."""
        nb = {
            "cells": [
                {"cell_type": "code", "source": ["%%bash\n", "echo hi\n"]},
            ]
        }
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(tmp, json.dumps(nb), name="entry.ipynb")
            report = self._check(tmp, entry)
            reached_fallback = any(
                f.data.get("scan") == "text-fallback" for f in report.findings
            ) or any("fallback scan" in line for line in report.passed_checks)
            self.assertTrue(reached_fallback)

    def test_notebook_degenerate_shapes_produce_no_finding_no_exception(self):
        shapes = {
            "no_cells": {"cells": []},
            "empty_source": {"cells": [{"cell_type": "code", "source": ""}]},
            "raw_cell": {
                "cells": [{"cell_type": "raw", "source": ["model.fit(df)\n"]}]
            },
        }
        for name, nb in shapes.items():
            with self.subTest(shape=name):
                with tempfile.TemporaryDirectory() as tmp:
                    entry = self._entrypoint(tmp, json.dumps(nb), name="entry.ipynb")
                    report = self._check(tmp, entry)
                    self.assertNotIn("DSX-CODE-001", codes(report))
                    self.assertNotIn("DSX-CODE-021", codes(report))

        # Malformed JSON: the whole document, not a per-cell shape.
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(tmp, "{not valid json", name="entry.ipynb")
            report = self._check(tmp, entry)
            self.assertEqual(codes(report), set())
            self.assertTrue(any("NOT scanned" in line for line in report.passed_checks))

    def test_bom_notebook_entrypoint_takes_the_ast_path(self):
        # A BOM breaks json.loads exactly as it breaks ast.parse -- the
        # .ipynb read needs the same utf-8-sig fix the .py read already
        # has (plan 01), or a BOM'd notebook silently reads as "could not
        # be read" (NOT scanned) rather than being scanned.
        nb = {
            "cells": [
                {
                    "cell_type": "code",
                    "source": [
                        "model.fit(df)\n",
                        "from sklearn.model_selection import train_test_split\n",
                        "train_test_split(df)\n",
                    ],
                }
            ]
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "entry.ipynb")
            path.write_bytes(b"\xef\xbb\xbf" + json.dumps(nb).encode("utf-8"))
            report = self._check(tmp, "entry.ipynb")
            found = [f for f in report.findings if f.code == "DSX-CODE-001"]
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].data.get("scan"), "ast")

    # -- Line axis --------------------------------------------------------

    def test_form_feed_line_does_not_desynchronise_reported_line_numbers(self):
        # A lone form-feed line is itself a line-break under str.splitlines(),
        # which the CPython tokenizer does not treat as one. Measured this
        # session: splitlines() reports 6 lines here where the tokenizer
        # sees 5, shifting every reported line number below the form-feed
        # line by one.
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                chr(12) + "\n"
                "df['Age'] = df['Age'].fillna(df['Age'].mean())\n"
                "model.fit(df)\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n",
            )
            report = self._check(tmp, entry)
            code_020 = [f for f in report.findings if f.code == "DSX-CODE-020"]
            code_001 = [f for f in report.findings if f.code == "DSX-CODE-001"]
            self.assertEqual(len(code_020), 1)
            self.assertEqual(len(code_001), 1)
            self.assertIn("Line 2", code_020[0].detail)
            self.assertIn("Line 3", code_001[0].detail)

    def test_string_literal_line_separator_does_not_desynchronise_reported_line_numbers(
        self,
    ):
        # U+2028 (LINE SEPARATOR) is valid inside a single-quoted Python
        # string literal and creates no real physical line break at the
        # tokenizer level, but str.splitlines() treats it as one anyway.
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "s = 'before" + chr(8232) + "after'\n"
                "df['Age'] = df['Age'].fillna(df['Age'].mean())\n"
                "model.fit(df)\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n",
            )
            report = self._check(tmp, entry)
            code_020 = [f for f in report.findings if f.code == "DSX-CODE-020"]
            code_001 = [f for f in report.findings if f.code == "DSX-CODE-001"]
            self.assertEqual(len(code_020), 1)
            self.assertEqual(len(code_001), 1)
            self.assertIn("Line 2", code_020[0].detail)
            self.assertIn("Line 3", code_001[0].detail)

    # -- Fallback contract and degrade signalling ------------------------------

    def test_unparseable_entrypoint_reaches_text_fallback_and_says_so(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "model.fit(df\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n",
            )
            report = self._check(tmp, entry)
            found = [f for f in report.findings if f.code == "DSX-CODE-001"]
            self.assertEqual(len(found), 1)
            self.assertTrue(
                all(f.data.get("scan") == "text-fallback" for f in report.findings)
            )
            self.assertIn("scanned as text only", found[0].detail)
            self.assertTrue(
                any("fallback scan" in line for line in report.passed_checks)
            )

    def test_parsed_entrypoint_says_so_on_the_pass_line_and_in_finding_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "model.fit(df)\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n",
            )
            report = self._check(tmp, entry)
            found = [f for f in report.findings if f.code == "DSX-CODE-001"]
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].data.get("scan"), "ast")
            self.assertIn(
                "entrypoint parsed with ast (call-level scan)", report.passed_checks
            )

    def test_recursion_error_during_parse_reaches_fallback_not_a_traceback(self):
        # Do NOT pin a chain length -- measured this session, 3.12.10 raises
        # well before a chain of 70,000 and 3.14.6 needs a far deeper chain
        # than its own default recursion limit would suggest (its C parser
        # does not honour sys.setrecursionlimit until very large depths).
        # A temporarily lowered recursion limit combined with a chain long
        # enough to exceed it on both interpreters is the portable trigger.
        with tempfile.TemporaryDirectory() as tmp:
            chain_expr = "x = 1" + " + 1" * 70000
            entry = self._entrypoint(
                tmp,
                chain_expr + "\n"
                "model.fit(df)\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n",
            )
            original_limit = sys.getrecursionlimit()
            sys.setrecursionlimit(150)
            try:
                report = self._check(tmp, entry)
            finally:
                sys.setrecursionlimit(original_limit)
            found = [f for f in report.findings if f.code == "DSX-CODE-001"]
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].data.get("scan"), "text-fallback")
            self.assertIn("scanned as text only", found[0].detail)

    def test_bom_entrypoint_takes_the_ast_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = (
                "model.fit(df)\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n"
            )
            path = Path(tmp, "entry.py")
            path.write_bytes(b"\xef\xbb\xbf" + text.encode("utf-8"))
            report = self._check(tmp, "entry.py")
            found = [f for f in report.findings if f.code == "DSX-CODE-001"]
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].data.get("scan"), "ast")

    def test_unscannable_entrypoint_is_reported_as_not_scanned(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(tmp, "model.fit(df)\n", name="entry.txt")
            report = self._check(tmp, entry)
            self.assertTrue(any("NOT scanned" in line for line in report.passed_checks))
            self.assertEqual(codes(report), set())

    def test_undecodable_entrypoint_is_still_scanned(self):
        with tempfile.TemporaryDirectory() as tmp:
            # A latin-1 byte that is not valid standalone UTF-8, in a file
            # that still carries a real pre-split fit call that must still
            # be found rather than the whole scan being skipped.
            text_bytes = (
                b"# comment with a latin-1 byte: \xe9\n"
                b"model.fit(df)\n"
                b"from sklearn.model_selection import train_test_split\n"
                b"train_test_split(df)\n"
            )
            path = Path(tmp, "entry.py")
            path.write_bytes(text_bytes)
            report = self._check(tmp, "entry.py")
            found = [f for f in report.findings if f.code == "DSX-CODE-001"]
            self.assertEqual(len(found), 1)

    # -- Split-detection union (Decision 5) ------------------------------------

    def test_aliased_split_still_counts_as_a_split(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "splitter = train_test_split\n"
                "a, b = splitter(X, y)\n"
                "scaler.fit_transform(data)\n",
            )
            report = self._check(tmp, entry)
            found = codes(report)
            self.assertIn("DSX-CODE-021", found)
            self.assertNotIn("DSX-CODE-001", found)
            self.assertNotIn("DSX-CODE-010", found)

    def test_split_marker_only_in_a_docstring_no_longer_counts_as_a_split(self):
        # The announced stricter case: a split marker inside a docstring
        # stops counting as a split, so DSX-CODE-001 fires where
        # DSX-CODE-021 used to be silently correct-by-accident.
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                '"""We call train_test_split somewhere in this pipeline."""\n'
                "scaler.fit_transform(data)\n",
            )
            report = self._check(tmp, entry)
            found = codes(report)
            self.assertNotIn("DSX-CODE-021", found)
            self.assertIn("DSX-CODE-001", found)

    # -- Uncaught-by-design: real leaks this plan does not close --------------
    # -- If any of these ever fails because a finding appeared, that is ------
    # -- good news -- promote it to a firing test rather than deleting it. ---

    def test_exec_of_a_fit_string_stays_uncaught_by_design(self):
        """REGRESSION, not a standing limit, reproduced by review:
        `exec("scaler.fit(data)")` before the split is a REAL leak. It fires
        DSX-CODE-001 today through the text scan (the regex sees the string
        literal's contents) and fires nothing under the call-node walk,
        because the string is data to the parser, not a Call. If this test
        ever fails because a finding appeared, that is good news and the
        test should be promoted to a firing test rather than deleted."""
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "src = 'scaler.fit(data)'\n"
                "exec(src)\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n",
            )
            report = self._check(tmp, entry)
            self.assertNotIn("DSX-CODE-001", codes(report))

    def test_getattr_dispatched_fit_stays_uncaught_by_design(self):
        """Not a regression -- dynamic dispatch was never caught by the text
        scan either, since there is no literal `.fit(` text to match.
        `getattr(model, "fit")(data)` before the split is a REAL leak whose
        callee cannot be resolved to a name. If this test ever fails because
        a finding appeared, that is good news and the test should be
        promoted to a firing test rather than deleted."""
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "getattr(model, 'fit')(data)\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n",
            )
            report = self._check(tmp, entry)
            self.assertNotIn("DSX-CODE-001", codes(report))

    def test_bound_method_in_a_variable_stays_uncaught_by_design(self):
        """Not a regression -- a bound method assigned to a variable was
        never caught by the text scan either, since the fit call itself
        carries no `.fit(`-shaped text. `f = model.fit` then `f(data)`
        before the split is a REAL leak. If this test ever fails because a
        finding appeared, that is good news and the
        test should be promoted to a firing test rather than deleted."""
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "f = model.fit\n"
                "f(data)\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n",
            )
            report = self._check(tmp, entry)
            self.assertNotIn("DSX-CODE-001", codes(report))

    def test_lexicon_locked(self):
        from dsx.checks import code as code_mod

        self.assertEqual(len(code_mod.TRAINING_FRAME_NAMES), 14)
        self.assertIn("X_train", code_mod.TRAINING_FRAME_NAMES)
        self.assertTrue(code_mod._is_training_frame("X_train_scaled"))
        self.assertTrue(code_mod._is_training_frame("train_df[cols]"))
        self.assertFalse(code_mod._is_training_frame("df"))
        self.assertFalse(code_mod._is_training_frame("data[['Balance']]"))

    def test_fit_call_re_extracts_full_frame_token(self):
        from dsx.checks import code as code_mod

        m = code_mod.FIT_CALL_RE.search(
            "min_max_scaler.fit_transform(data[['Balance']])"
        )
        self.assertIsNotNone(m)
        self.assertTrue(m.group(1).startswith("data"))

    def test_fit_call_re_timing_no_catastrophic_backtracking(self):
        import time

        from dsx.checks import code as code_mod

        text = ".fit(" + ("a" * 19990)
        self.assertEqual(len(text), 19995)
        start = time.perf_counter()
        code_mod.FIT_CALL_RE.search(text)
        self.assertLess(time.perf_counter() - start, 1.0)

    # ── Phase 11.1.1 plan 02: this mechanism's own timing pins, not ──────────
    # ── inherited from a sibling's linearity proof (T-11.1-01, Rule from ────
    # ── 11.1.1-RESEARCH.md Pitfall 6) ─────────────────────────────────────

    def test_ast_fit_argument_extraction_timing_is_linear(self):
        # House shape: local imports, inline input, one perf_counter bracket
        # per size, hard assertLess, no subTest. Measures parse + walk +
        # sort + ast.unparse of every fit argument -- the mechanism task 2
        # wires into DSX-CODE-021's consumer loop --
        # NOT the full check() pipeline (test_ast_scan_timing_is_linear_
        # on_a_large_entrypoint above already covers that). Passes before
        # task 2: ast.parse, _call_sites (plan 01) and ast.unparse are
        # already fast at these sizes -- measured this session, well under
        # budget on both rows.
        import ast
        import time

        from dsx.checks import code as code_mod

        for size, budget in ((5_000, 0.5), (20_000, 1.0)):
            source = "model.fit(df)\n" * size
            start = time.perf_counter()
            tree = ast.parse(source)
            for site in code_mod._call_sites(tree):
                if site.name in code_mod.FIT_METHOD_NAMES and site.node.args:
                    ast.unparse(site.node.args[0])
            elapsed = time.perf_counter() - start
            self.assertLess(
                elapsed,
                budget,
                f"AST fit-argument extraction took {elapsed:.4f}s over "
                f"{size} lines (budget {budget}s) -- possible quadratic "
                "regression",
            )

    def test_fit_call_re_timing_no_catastrophic_backtracking_with_keyword_form(self):
        # The widened FALLBACK pattern gets its own measurement, not an
        # inherited figure. A 19,995-character non-matching input and a
        # 1,000,000-character adversarial near-miss built from ".fit("
        # followed by 500,000 repetitions of "x=", each under a
        # 1.0-second budget. Uses code_mod.FIT_CALL_RE directly, so this
        # re-measures whatever pattern is currently installed -- passes
        # before task 2 (the unwidened pattern is already linear) and
        # continues to pass after task 2 widens it.
        import time

        from dsx.checks import code as code_mod

        non_matching = ".fit(" + ("a" * 19990)
        self.assertEqual(len(non_matching), 19995)
        start = time.perf_counter()
        code_mod.FIT_CALL_RE.search(non_matching)
        self.assertLess(time.perf_counter() - start, 1.0)

        near_miss = ".fit(" + ("x=" * 500_000)
        self.assertEqual(len(near_miss), 1_000_005)
        start = time.perf_counter()
        code_mod.FIT_CALL_RE.search(near_miss)
        self.assertLess(time.perf_counter() - start, 1.0)

    def test_full_frame_cleaning_predicates_timing_no_catastrophic_backtracking(self):
        # Phase 11.1.1 (threat T-11.1-01). The previous single-pattern
        # construction was cubic (spread filter) and quadratic (imputation) in
        # line length: 800 characters already took 1.4 seconds, so at this size
        # it would not have finished in any practical time. Same house bar as
        # test_fit_call_re_timing_no_catastrophic_backtracking above (20,000
        # characters), but an order of magnitude tighter, because the replacement
        # runs in well under a millisecond and a loose threshold would let a
        # regression back to a backtracking construction slip through.
        import time

        from dsx.checks import code as code_mod

        # The sizes ascend deliberately, and this loop must NOT use subTest: a
        # regression to the old cubic construction has to abort at 800
        # characters (about 1.4 seconds) rather than continue to 20,000, where
        # the same construction runs for hours and would hang the suite instead
        # of failing it. subTest records a failure and keeps going, which is
        # exactly the wrong behaviour here.
        for size, budget in ((800, 0.05), (20000, 0.1)):
            for predicate in (
                code_mod._is_full_frame_impute,
                code_mod._is_full_frame_spread_filter,
            ):
                line = "x" * size  # satisfies neither predicate
                start = time.perf_counter()
                self.assertFalse(predicate(line))
                elapsed = time.perf_counter() - start
                self.assertLess(
                    elapsed,
                    budget,
                    f"{predicate.__name__} took {elapsed:.4f}s on a "
                    f"{size}-character non-matching line (budget {budget}s) — "
                    "super-linear regression",
                )

    def test_good_fixture_still_passes_all_four_gate_points(self):
        from dsx import cli

        good = self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml"
        for point in ("plan", "execute", "verify", "ship"):
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = cli.main(["gate", point, "--spec", str(good)])
            self.assertEqual(code, 0, f"gate {point} unexpectedly blocked:\n{err.getvalue()}")

    def test_bad_fixture_still_blocks_at_execute(self):
        from dsx import cli

        bad = self.ROOT / "examples" / "bad-ANALYSIS-SPEC.yaml"
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(["gate", "execute", "--spec", str(bad)])
        self.assertEqual(code, 1)

    # ── Task 3: decision-record emission (D-04) ──────────────────────────────

    def test_check_over_tripping_entrypoint_leaves_a_decision_record(self):
        from dsx.checks import code as code_mod

        report = code_mod.check(
            {
                "model": {"task": "binary_classification"},
                "reproducibility": {"entrypoint": "analysis/leaky_model.py"},
            },
            str(self.ROOT / "examples"),
        )
        decisions = report.context.get("decisions") or []
        self.assertTrue(decisions)
        self.assertEqual(decisions[0]["layer"], "deterministic")

    def test_check_over_clean_entrypoint_still_leaves_a_decision_record(self):
        # A cleared judgment is a judgment.
        from dsx.checks import code as code_mod

        report = code_mod.check(
            {
                "model": {"task": "binary_classification"},
                "reproducibility": {"entrypoint": "analysis/activation_readout.py"},
            },
            str(self.ROOT / "examples"),
        )
        decisions = report.context.get("decisions") or []
        self.assertTrue(decisions)
        self.assertEqual(decisions[0]["layer"], "deterministic")

    def test_run_twice_over_same_entrypoint_is_deterministic(self):
        from dsx.checks import code as code_mod

        spec = {
            "model": {"task": "binary_classification"},
            "reproducibility": {"entrypoint": "analysis/leaky_model.py"},
        }
        r1 = code_mod.check(spec, str(self.ROOT / "examples"))
        r2 = code_mod.check(spec, str(self.ROOT / "examples"))
        self.assertEqual([f.code for f in r1.findings], [f.code for f in r2.findings])
        counts_020 = sum(1 for f in r1.findings if f.code == "DSX-CODE-020")
        counts_021 = sum(1 for f in r1.findings if f.code == "DSX-CODE-021")
        self.assertLessEqual(counts_020, 1)
        self.assertLessEqual(counts_021, 1)

    # ── DSX-CODE-030/031: statistical test sees the declared target ─────────

    def _check_with_target(self, tmp: str, entry: str, target: "str | None"):
        from dsx.checks import code as code_mod

        model: dict = {"task": "binary_classification"}
        if target is not None:
            model["target"] = target
        return code_mod.check(
            {
                "model": model,
                "reproducibility": {"entrypoint": entry},
            },
            tmp,
        )

    def test_stat_test_call_re_matches_every_recognised_test_name(self):
        from dsx.checks import code as code_mod

        calls = (
            "chi2_contingency(t)",
            "ttest_ind(a, b)",
            "ttest_rel(a, b)",
            "pearsonr(a, b)",
            "mannwhitneyu(a, b)",
            "f_oneway(a, b, c)",
            "kruskal(a, b, c)",
        )
        for call in calls:
            with self.subTest(call=call):
                self.assertTrue(code_mod.STAT_TEST_CALL_RE.search(call))

    def test_chi_square_before_split_referencing_target_is_critical(self):
        # D-05: DSX-CODE-030
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "import pandas as pd\n"
                "from scipy.stats import chi2_contingency\n"
                "less_products = dataset['NumOfProducts'] < 2\n"
                "contingency_table = pd.crosstab(less_products, dataset['Exited'])\n"
                "chi2, p, _, _ = chi2_contingency(contingency_table)\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(dataset)\n",
            )
            report = self._check_with_target(tmp, entry, "Exited")
            found = [f for f in report.findings if f.code == "DSX-CODE-030"]
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].severity, Severity.CRITICAL)
            self.assertNotIn("DSX-CODE-031", codes(report))

    def test_chi_square_after_split_referencing_target_is_high(self):
        # D-05: DSX-CODE-031
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "import pandas as pd\n"
                "from scipy.stats import chi2_contingency\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(dataset)\n"
                "less_products = dataset['NumOfProducts'] < 2\n"
                "contingency_table = pd.crosstab(less_products, dataset['Exited'])\n"
                "chi2, p, _, _ = chi2_contingency(contingency_table)\n",
            )
            report = self._check_with_target(tmp, entry, "Exited")
            found = [f for f in report.findings if f.code == "DSX-CODE-031"]
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].severity, Severity.HIGH)
            self.assertNotIn("DSX-CODE-030", codes(report))

    def test_call_on_same_line_as_split_marker_is_at_or_after(self):
        # The comparison is strictly-less-than for "before", never <=.
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from sklearn.model_selection import train_test_split\n"
                "contingency_table = pd.crosstab(x, dataset['Exited']); "
                "chi2, p, _, _ = chi2_contingency(contingency_table); "
                "train_test_split(dataset)\n",
            )
            report = self._check_with_target(tmp, entry, "Exited")
            self.assertIn("DSX-CODE-031", codes(report))
            self.assertNotIn("DSX-CODE-030", codes(report))

    def test_various_stat_tests_each_trigger_the_scan(self):
        calls = (
            "ttest_ind(group_a, dataset['Exited'])",
            "pearsonr(feature, dataset['Exited'])",
            "mannwhitneyu(group_a, dataset['Exited'])",
            "f_oneway(g1, g2, dataset['Exited'])",
            "kruskal(g1, g2, dataset['Exited'])",
        )
        for call in calls:
            with self.subTest(call=call):
                with tempfile.TemporaryDirectory() as tmp:
                    entry = self._entrypoint(tmp, f"result = {call}\n")
                    report = self._check_with_target(tmp, entry, "Exited")
                    self.assertIn("DSX-CODE-030", codes(report))

    def test_blank_target_produces_neither_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from scipy.stats import chi2_contingency\n"
                "contingency_table = pd.crosstab(x, dataset['Exited'])\n"
                "chi2, p, _, _ = chi2_contingency(contingency_table)\n",
            )
            for blank_target in ("", "   "):
                with self.subTest(target=repr(blank_target)):
                    report = self._check_with_target(tmp, entry, blank_target)
                    found = codes(report)
                    self.assertNotIn("DSX-CODE-030", found)
                    self.assertNotIn("DSX-CODE-031", found)

    def test_absent_target_produces_neither_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from scipy.stats import chi2_contingency\n"
                "contingency_table = pd.crosstab(x, dataset['Exited'])\n"
                "chi2, p, _, _ = chi2_contingency(contingency_table)\n",
            )
            report = self._check_with_target(tmp, entry, None)
            found = codes(report)
            self.assertNotIn("DSX-CODE-030", found)
            self.assertNotIn("DSX-CODE-031", found)

    def test_no_stat_test_call_produces_neither_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(tmp, "x = dataset['Exited'].sum()\n")
            report = self._check_with_target(tmp, entry, "Exited")
            found = codes(report)
            self.assertNotIn("DSX-CODE-030", found)
            self.assertNotIn("DSX-CODE-031", found)

    def test_empty_source_produces_neither_code_and_no_exception(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(tmp, "")
            report = self._check_with_target(tmp, entry, "Exited")
            found = codes(report)
            self.assertNotIn("DSX-CODE-030", found)
            self.assertNotIn("DSX-CODE-031", found)

    def test_three_before_split_calls_produce_exactly_one_030_lowest_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "from scipy.stats import chi2_contingency\n"
                "c1 = pd.crosstab(a, dataset['Exited']); chi2_contingency(c1)\n"
                "c2 = pd.crosstab(b, dataset['Exited']); chi2_contingency(c2)\n"
                "c3 = pd.crosstab(c, dataset['Exited']); chi2_contingency(c3)\n",
            )
            report = self._check_with_target(tmp, entry, "Exited")
            found = [f for f in report.findings if f.code == "DSX-CODE-030"]
            self.assertEqual(len(found), 1)
            self.assertIn("Line 2", found[0].detail)

    def test_target_substring_of_longer_identifier_not_a_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "contingency_table = pd.crosstab(x, dataset.ExitedFlag)\n"
                "chi2, p, _, _ = chi2_contingency(contingency_table)\n",
            )
            report = self._check_with_target(tmp, entry, "Exited")
            found = codes(report)
            self.assertNotIn("DSX-CODE-030", found)
            self.assertNotIn("DSX-CODE-031", found)

    def test_target_reference_recognised_bracket_both_quotes_and_attribute(self):
        forms = (
            "dataset['Exited']",
            'dataset["Exited"]',
            "dataset.Exited",
        )
        for form in forms:
            with self.subTest(form=form):
                with tempfile.TemporaryDirectory() as tmp:
                    entry = self._entrypoint(
                        tmp,
                        f"contingency_table = pd.crosstab(x, {form})\n"
                        "chi2, p, _, _ = chi2_contingency(contingency_table)\n",
                    )
                    report = self._check_with_target(tmp, entry, "Exited")
                    self.assertIn("DSX-CODE-030", codes(report))

    def test_stat_test_scan_leaves_a_second_decision_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "contingency_table = pd.crosstab(x, dataset['Exited'])\n"
                "chi2, p, _, _ = chi2_contingency(contingency_table)\n",
            )
            report = self._check_with_target(tmp, entry, "Exited")
            decisions = report.context.get("decisions") or []
            self.assertEqual(len(decisions), 2)
            self.assertEqual(decisions[1]["layer"], "deterministic")

    def test_good_and_bad_fixtures_gate_contract_unchanged(self):
        from dsx import cli

        cases = [
            ("good-ANALYSIS-SPEC.yaml", "plan", 0),
            ("good-ANALYSIS-SPEC.yaml", "execute", 0),
            ("good-ANALYSIS-SPEC.yaml", "verify", 0),
            ("good-ANALYSIS-SPEC.yaml", "ship", 0),
            ("bad-ANALYSIS-SPEC.yaml", "execute", 1),
            ("bad-ANALYSIS-SPEC.yaml", "ship", 1),
        ]
        for spec_name, point, expected in cases:
            with self.subTest(spec=spec_name, point=point):
                spec_path = self.ROOT / "examples" / spec_name
                out, err = io.StringIO(), io.StringIO()
                with redirect_stdout(out), redirect_stderr(err):
                    code = cli.main(["gate", point, "--spec", str(spec_path)])
                self.assertEqual(code, expected)

    # -- Task 5: performance -- the new mechanism measured, the one -------
    # -- already-over-budget quadratic fixed, the one retained pattern ----
    # -- made linear by construction -----------------------------------

    def test_ast_scan_timing_is_linear_on_a_large_entrypoint(self):
        # The subject here is OUR code, not CPython's parser: the
        # regression guard against re-walking the tree per code, rendering
        # tokens for non-fit calls, or any accidental quadratic in
        # call-site assembly. House shape: local imports, inline input,
        # perf_counter around one check() call, hard assertLess, NO
        # subTest (a super-linear regression must abort at the small size
        # rather than hang the suite at the large one). Measured this
        # session, full check() pipeline (not just ast.parse + walk):
        # 0.107 s / 0.431 s on `python` 3.12.10, 0.104 s / 0.479 s on
        # `python3` 3.14.6, at 5,000 / 20,000 lines of `model.fit(df)`.
        import time

        from dsx.checks import code as code_mod

        for size, budget in ((5000, 0.5), (20000, 1.0)):
            with tempfile.TemporaryDirectory() as tmp:
                entry = self._entrypoint(tmp, "model.fit(df)\n" * size)
                start = time.perf_counter()
                code_mod.check(
                    {
                        "model": {"task": "binary_classification"},
                        "reproducibility": {"entrypoint": entry},
                    },
                    tmp,
                )
                elapsed = time.perf_counter() - start
                self.assertLess(
                    elapsed,
                    budget,
                    f"AST scan took {elapsed:.4f}s over {size} lines "
                    f"(budget {budget}s) -- possible quadratic regression",
                )

    def test_scaler_full_loop_timing_is_linear(self):
        # Phase 11.1.1 plan 01 (threat T-11.1.1-13). Input IS the matching
        # shape a non-matching-input pin would be structurally blind to:
        # one X_train = 1 line followed by N StandardScaler().fit_transform
        # lines, each SUPPRESSED (X_train already in prior), which is
        # exactly the shape that made the old (break-inside-the-inner-if)
        # loop rebuild `"\n".join(lines[:index])` for every one of the N
        # matching lines. Measured this session, the OLD loop alone (not
        # the full check() pipeline): 0.0223 / 0.0852 / 0.4545 / 1.4211 s
        # at 2,000 / 4,000 / 8,000 / 16,000 matching lines -- roughly 4x
        # per doubling. No subTest: a regression must abort at the small
        # size.
        import time

        from dsx.checks import code as code_mod

        for size, budget in ((8000, 0.6), (16000, 1.0)):
            with tempfile.TemporaryDirectory() as tmp:
                entry = self._entrypoint(
                    tmp,
                    "X_train = 1\n"
                    + "StandardScaler().fit_transform(X)\n" * size,
                )
                start = time.perf_counter()
                report = code_mod.check(
                    {
                        "model": {"task": "binary_classification"},
                        "reproducibility": {"entrypoint": entry},
                    },
                    tmp,
                )
                elapsed = time.perf_counter() - start
                self.assertNotIn("DSX-CODE-002", codes(report))
                self.assertLess(
                    elapsed,
                    budget,
                    f"DSX-CODE-002 scan took {elapsed:.4f}s over {size} "
                    f"suppressed matching lines (budget {budget}s) -- "
                    "possible quadratic regression",
                )

    def test_scaler_full_loop_finding_set_unchanged_by_the_break_hoist(self):
        # The equivalence proof (see the comment above the loop in
        # dsx/checks/code.py): lines[:j] is a prefix superset of lines[:i]
        # for j > i, so once "X_train" is in `prior` it is in every later
        # `prior` too -- a suppressed first match can never be followed by
        # an accepted later one. Both shapes below are pinned so the hoist
        # is proven behaviour-preserving, not merely fast.
        with tempfile.TemporaryDirectory() as tmp:
            # Suppressed: X_train appears before the only matching line.
            entry = self._entrypoint(
                tmp,
                "X_train = 1\n"
                "StandardScaler().fit_transform(X)\n"
                "StandardScaler().fit_transform(df)\n",
            )
            report = self._check(tmp, entry)
            self.assertNotIn("DSX-CODE-002", codes(report))

        with tempfile.TemporaryDirectory() as tmp:
            # Accepted: no X_train anywhere above the first matching line.
            entry = self._entrypoint(
                tmp,
                "StandardScaler().fit_transform(X)\n"
                "StandardScaler().fit_transform(df)\n",
            )
            report = self._check(tmp, entry)
            found = [f for f in report.findings if f.code == "DSX-CODE-002"]
            self.assertEqual(len(found), 1)
            self.assertIn("Line 1", found[0].detail)

    def test_pipeline_fit_train_re_timing_on_its_worst_shape(self):
        # Phase 11.1.1 plan 01 (Decision 9, threat T-11.1-01). The
        # adversarial shape is literal: "Pipeline(" * n + ").fit(X_trai" --
        # deliberately malformed (missing the closing paren and the final
        # "n" of X_train) so the overall match fails everywhere and
        # re.search must retry from every one of the n "Pipeline(" start
        # positions. Measured this session at n = 4,000: the OLD `.*`
        # pattern and an UNBOUNDED `[^)\n]*` swap are both still quadratic
        # (0.1357s / 0.4360s); only bounding the repetition
        # (`[^)\n]{0,200}`) makes each retry O(1) instead of
        # O(remaining-length), measured 0.0048s at n = 4,000 and 0.33s
        # even at n = 256,000. A budget a quadratic construction breaks.
        import time

        from dsx.checks import code as code_mod

        text = "Pipeline(" * 4000 + ").fit(X_trai"
        start = time.perf_counter()
        code_mod.PIPELINE_FIT_TRAIN_RE.search(text)
        elapsed = time.perf_counter() - start
        self.assertLess(elapsed, 1.0)

    def test_pipeline_fit_train_re_match_set_unchanged_across_probe_shapes(self):
        # 14 probe shapes (matching and non-matching), recorded in the
        # plan's SUMMARY. The bounded pattern's match set is identical to
        # the pre-fix pattern's on every probe except a nested-parenthesis
        # shape, which dropping `.` in favour of any `)`-excluding
        # character class already excludes on its own -- not something the
        # length bound itself introduces.
        from dsx.checks import code as code_mod

        matching = (
            "Pipeline(steps).fit(X_train)",
            "Pipeline(steps).fit(X_train, y_train)",
            "pipeline(steps).fit(X_train)",
            "Pipeline( steps ) . fit ( X_train )",
            "Pipeline().fit(X_train)",
            "Pipeline(a, b, c).fit(X_train)",
            "not_a_pipeline(steps).fit(X_train)",
            "Pipeline(steps.something).fit(X_train)",
        )
        non_matching = (
            "Pipeline(steps).fit(X_test)",
            "Pipeline(steps).fit(y_train)",
            "Pipeline(steps).transform(X_train)",
            "PipelineX(steps).fit(X_train)",
            "Pipeline(\n    steps\n).fit(X_train)",
            "Pipeline((a, b)).fit(X_train)",  # nested paren: pre-existing miss
        )
        probes = matching + non_matching
        self.assertEqual(len(probes), 14)
        for text in matching:
            with self.subTest(text=text):
                self.assertIsNotNone(code_mod.PIPELINE_FIT_TRAIN_RE.search(text))
        for text in non_matching:
            with self.subTest(text=text):
                self.assertIsNone(code_mod.PIPELINE_FIT_TRAIN_RE.search(text))

    # ── Phase 11.1.1 plan 03 task 2: non-regression pins for the mechanism ───
    # ── change -- line-index stability, the line axis, notebook geometry, ────
    # ── determinism/ordering, degraded-path signalling and prose-mask ────────
    # ── boundaries. Groups 1 (line-index stability) and 3 (notebook ──────────
    # ── geometry, including the third false-positive fixture) are already ────
    # ── fully pinned by existing tests above -- test_multi_line_fit_call_ ────
    # ── after_split_fires_code_021, test_fit_multiline_open_paren_before_ ────
    # ── split_fires_code_001, test_lowest_physical_line_reported_for_ ────────
    # ── code_001, test_at_most_one_dsx_code_021_lowest_line, test_run_ ───────
    # ── twice_over_same_entrypoint_is_deterministic, test_notebook_code_ ─────
    # ── cell_line_numbers_are_unchanged_by_the_markdown_filter and test_ ─────
    # ── notebook_markdown_cell_mentioning_fit_draws_no_code_001 -- cited ──────
    # ── here rather than duplicated, per this plan's SUMMARY. What follows ───
    # ── is the remainder: Group 2's split-line supplement, Group 4's ─────────
    # ── module-state pin, Group 5's decision-record and blank/not-scanned ────
    # ── pins, and Group 6's prose-mask boundary pins -- the last of which ────
    # ── are measured against the shipped code rather than against AST- ───────
    # ── DESIGN.md's fuller promise, and two of which pin a PERSISTING false ──
    # ── positive (assertIn, not assertNotIn) because that is what was ────────
    # ── measured. See this plan's SUMMARY, "prose mask coverage", for the ────
    # ── full account. ──────────────────────────────────────────────────────

    def test_line_axis_desync_fixtures_also_report_the_true_split_line(self):
        """Supplements test_form_feed_line_does_not_desynchronise_reported_
        line_numbers and test_string_literal_line_separator_does_not_
        desynchronise_reported_line_numbers above (both left unmodified,
        per this task's instruction): the split line named inside
        DSX-CODE-001's own detail text must also equal the TRUE physical
        line of the split call, not a splitlines()-shifted one, for the
        same two desynchronising shapes."""
        for prefix in (chr(12) + "\n", "s = 'before" + chr(8232) + "after'\n"):
            with self.subTest(prefix=repr(prefix)):
                with tempfile.TemporaryDirectory() as tmp:
                    entry = self._entrypoint(
                        tmp,
                        prefix
                        + "df['Age'] = df['Age'].fillna(df['Age'].mean())\n"
                        "model.fit(df)\n"
                        "from sklearn.model_selection import train_test_split\n"
                        "train_test_split(df)\n",
                    )
                    report = self._check(tmp, entry)
                    code_001 = [
                        f for f in report.findings if f.code == "DSX-CODE-001"
                    ]
                    self.assertEqual(len(code_001), 1)
                    self.assertIn("line 5", code_001[0].detail)

    def test_no_module_level_cache_grows_across_repeated_check_calls(self):
        """No committed module-level mutable container may grow across
        check() calls -- that would be exactly the shared mutable state
        the determinism guarantee forbids (11.1.1-AST-DESIGN.md §7, "not
        used: any parse caching"). Every module-level name bound to a
        list, dict or set is enumerated and its size recorded before and
        after ten check() calls over distinct inputs; none may grow."""
        from dsx.checks import code as code_mod

        def container_sizes():
            return {
                name: len(value)
                for name, value in vars(code_mod).items()
                if isinstance(value, (list, dict, set))
            }

        before = container_sizes()
        for i in range(10):
            with tempfile.TemporaryDirectory() as tmp:
                entry = self._entrypoint(tmp, f"model.fit(df_{i})\n")
                self._check(tmp, entry)
        after = container_sizes()
        self.assertEqual(before, after)

    def test_decision_records_carry_scan_path_on_both_mechanisms(self):
        """Channel 4 of the four degrade-signalling channels
        (11.1.1-AST-DESIGN.md §2.3): both decision records gain a
        scan_path:ast or scan_path:text-fallback:<reason> input -- the
        durable channel that lands in DECISIONS.jsonl and is replayable
        through `dsx explain`. Verified directly on report.context here,
        not only inferred from the pass line and finding data channels
        the two existing tests above already cover."""
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "model.fit(df)\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n",
            )
            report = self._check(tmp, entry)
            decisions = report.context["decisions"]
            self.assertTrue(decisions)
            self.assertTrue(
                all(
                    any(i == "scan_path:ast" for i in d["inputs"])
                    for d in decisions
                )
            )

        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp,
                "model.fit(df\n"
                "from sklearn.model_selection import train_test_split\n"
                "train_test_split(df)\n",
            )
            report = self._check(tmp, entry)
            decisions = report.context["decisions"]
            self.assertTrue(decisions)
            self.assertTrue(
                all(
                    any(
                        i.startswith("scan_path:text-fallback:")
                        for i in d["inputs"]
                    )
                    for d in decisions
                )
            )

    def test_blank_entrypoint_retains_silence_including_no_decision_record(
        self,
    ):
        """Deliberately NOT changed (11.1.1-AST-DESIGN.md blocker B4/B6
        table, "Deliberately NOT changed"): no entrypoint declared at all
        is a different case from an entrypoint that exists but cannot be
        scanned. Nothing was declared, so nothing is repudiated -- the
        early return fires before any record_decision call, exactly as it
        did before this phase. Named here so the retention is deliberate
        and visible, not an oversight this test would otherwise silently
        accept."""
        from dsx.checks import code as code_mod

        report = code_mod.check(
            {
                "model": {"task": "binary_classification"},
                "reproducibility": {"entrypoint": ""},
            },
            ".",
        )
        self.assertEqual(report.findings, [])
        self.assertIsNone(report.context.get("decisions"))
        self.assertTrue(
            any("no entrypoint declared" in line for line in report.passed_checks)
        )

    def test_unscannable_entrypoint_also_produces_no_decision_record(self):
        """Measured, not assumed, against 11.1.1-AST-DESIGN.md's blocker
        B4/B6 table, which specifies a scan_path:not-scanned:<reason>
        decision input for a declared entrypoint that cannot be scanned.
        Measured against the shipped code: check() returns before any
        record_decision call for an entrypoint that resolves but cannot
        be read (unsupported suffix, unreadable, or invalid notebook
        JSON) -- the SAME early-return shape as the blank-entrypoint case,
        so no decision record of any kind is produced here, not one
        carrying a not-scanned scan_path. Channel 1 (the report.ok pass
        line) is the only channel that actually fires for this case;
        channels 2-4 do not apply because no Finding and no DecisionRecord
        are ever constructed on this path. Flagged here for the
        end-of-phase human check as a possible gap between design and
        ship, named in this plan's SUMMARY."""
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(tmp, "model.fit(df)\n", name="entry.txt")
            report = self._check(tmp, entry)
            self.assertEqual(report.findings, [])
            self.assertIsNone(report.context.get("decisions"))
            self.assertTrue(
                any("NOT scanned" in line for line in report.passed_checks)
            )

    def test_docstring_and_comment_mentioning_fit_both_stay_closed_on_the_parsed_path(
        self,
    ):
        """DSX-CODE-001's docstring false positive (test_docstring_
        mentioning_fit_draws_no_code_001 above) closes STRUCTURALLY, not
        via the prose mask: a comment is stripped by the tokenizer before
        ast.parse ever sees it, so neither a docstring NOR a trailing
        comment mentioning a fit call produces a Call node, on the parsed
        path -- both shapes pinned here."""
        for source in (
            '"""We never call scaler.fit(X) on the full frame."""\n'
            "from sklearn.model_selection import train_test_split\n"
            "train_test_split(df)\n",
            "x = 1  # scaler.fit(X) on the full frame\n"
            "from sklearn.model_selection import train_test_split\n"
            "train_test_split(df)\n",
        ):
            with self.subTest(source=source):
                with tempfile.TemporaryDirectory() as tmp:
                    entry = self._entrypoint(tmp, source)
                    report = self._check(tmp, entry)
                    self.assertNotIn("DSX-CODE-001", codes(report))

    def test_comment_mentioning_smote_still_fires_code_003_measured_not_assumed(
        self,
    ):
        """Measured, not assumed, against 11.1.1-AST-DESIGN.md §3.8, which
        specifies a comment guard for DSX-CODE-002 and DSX-CODE-003 ("The
        guard is added to both, on both paths"). Measured against the
        shipped code: RESAMPLE_BEFORE_RE's loop over `lines` carries no
        `#`-leading guard at all -- unlike every other text scanner in
        this module -- so a comment mentioning SMOTE still fires
        DSX-CODE-003 HIGH. This is a genuine implementation gap relative
        to the design, not this plan's to fix (plan 03's own scope
        excludes mechanism work); it is named in this plan's SUMMARY and
        raised for the end-of-phase human check. If this test ever fails
        because the finding disappeared, that would mean the guard was
        added -- good news -- but until then this pin records the false
        positive that stays, and the
        test should be promoted to a firing test rather than deleted.
        """
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(tmp, "# never use SMOTE before the split\n")
            report = self._check(tmp, entry)
            self.assertIn("DSX-CODE-003", codes(report))

    def test_comment_mentioning_scaler_fit_transform_still_fires_code_002_measured_not_assumed(
        self,
    ):
        """Same measured gap as test_comment_mentioning_smote_still_fires_
        code_003_measured_not_assumed above, for DSX-CODE-002:
        SCALER_FULL_RE's loop also carries no `#`-leading guard. If this
        test ever fails because the finding disappeared, that would mean
        the guard was added -- good news -- but until then this pin
        records the false positive that stays, and the
        test should be promoted to a firing test rather than deleted.
        """
        with tempfile.TemporaryDirectory() as tmp:
            entry = self._entrypoint(
                tmp, "# StandardScaler().fit_transform(X)\n"
            )
            report = self._check(tmp, entry)
            self.assertIn("DSX-CODE-002", codes(report))

    def test_split_marker_on_the_opening_or_closing_line_of_a_multiline_string_still_counts(
        self,
    ):
        """Completes blocker B2's boundary proof for the one place the
        prose mask is actually wired in the shipped code (the split-marker
        text scan; see test_multiline_string_interior_line_stays_
        uncaught_by_design above, task 1). Rule B masks only strictly
        interior lines -- the opening and closing lines of a multi-line
        string are spared, so a split marker written on either one still
        counts as a split."""
        for source, label in (
            (
                "sql = " + '"""' + "train_test_split\n"
                "abc\n" + '"""' + "\n"
                "scaler.fit_transform(data)\n",
                "opening",
            ),
            (
                "sql = " + '"""' + "\n"
                "abc\n"
                "train_test_split" + '"""' + "\n"
                "scaler.fit_transform(data)\n",
                "closing",
            ),
        ):
            with self.subTest(line=label):
                with tempfile.TemporaryDirectory() as tmp:
                    entry = self._entrypoint(tmp, source)
                    report = self._check(tmp, entry)
                    self.assertIn("DSX-CODE-021", codes(report))


if __name__ == "__main__":
    unittest.main(verbosity=2)
