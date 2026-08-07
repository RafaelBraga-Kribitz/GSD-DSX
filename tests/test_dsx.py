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

from dsx import cli, mathx  # noqa: E402
from dsx.checks import claims, design, metrics, ml, repro, stats, viz  # noqa: E402
from dsx.findings import Report, Severity  # noqa: E402
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
        from dsx.spec import _INFERENCE_FIELDS

        self.assertEqual(
            _INFERENCE_FIELDS,
            ("paradigm", "paradigm_justification", "declared_at",
             "primary_procedure", "alpha_spending", "fallback_rule"),
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
        from dsx.cli import GATE_THRESHOLDS
        from dsx.findings import Severity
        from dsx.frame import paradigm

        report = paradigm.check({"inference": {"paradigm": "bayesian"}})
        for point, label in GATE_THRESHOLDS.items():
            with self.subTest(point=point):
                self.assertFalse(report.blocks(Severity.parse(label)))

    def test_check_appends_one_deterministic_decision_record(self):
        from dsx.frame import paradigm

        report = paradigm.check({"inference": {"paradigm": "frequentist"}})
        decisions = report.context.get("decisions") or []
        self.assertEqual(len(decisions), 1)
        self.assertEqual(decisions[0]["layer"], "deterministic")
        self.assertEqual(decisions[0]["id"], "")
        self.assertTrue(decisions[0]["counterfactual"].strip())

    # D-05: DSX-PAR-001
    def test_applied_prefixes_have_codes_and_not_shipped_prefixes_have_none(self):
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
                for prefix in finding.data.get("not_applied", {}):
                    self.assertFalse(
                        [c for c in known if c.startswith(prefix)],
                        f"{prefix} reported not-shipped but a known code exists",
                    )
        for prefix in paradigm._NOT_SHIPPED:
            self.assertFalse([c for c in known if c.startswith(prefix)], prefix)


if __name__ == "__main__":
    unittest.main(verbosity=2)
