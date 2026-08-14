"""Test suite for dsx/frame/val.py — DSX-VAL-010 (estimand completeness) and
DSX-VAL-011 (estimand falsifiability). Stdlib unittest — no pytest dependency.

Run:  python3 -m unittest tests.test_frame_val -v
"""

from __future__ import annotations

import ast
import copy
import hashlib
import io
import json
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dsx import cli  # noqa: E402
from dsx.checks import design  # noqa: E402
from dsx.findings import Report, Severity  # noqa: E402
from dsx.frame import val  # noqa: E402
from dsx.loader import load  # noqa: E402


def codes(report: Report) -> set[str]:
    return {f.code for f in report.findings}


# The good fixture's own falsifier (examples/good-ANALYSIS-SPEC.yaml:302) — quoted
# verbatim so the "discriminating" test exercises the real accepted shape, not an
# invented one.
_GOOD_FALSIFIER = (
    "95% CI on the activation uplift includes zero, or its lower bound sits below "
    "+1.0pp"
)

# The template's placeholder falsifier (templates/ANALYSIS-SPEC.yaml:288), quoted
# verbatim.
_TEMPLATE_PLACEHOLDER_FALSIFIER = "<the observation that would prove this wrong>"


def _estimand_spec(**overrides: object) -> dict:
    """A minimal spec carrying a complete, discriminating estimand, with the
    given fields overridden to isolate one code at a time."""
    estimand = {
        "quantity": "difference in 7-day activation rate",
        "population": "new non-bot signups, 2026-06-01 to 2026-06-14",
        "contrast": "onboarding checklist vs current onboarding",
        "time_window": "7 days from signup",
        "falsifier": _GOOD_FALSIFIER,
    }
    estimand.update(overrides)
    return {"validity_frame": {"estimand": estimand}}


class TestValEstimand(unittest.TestCase):
    def test_complete_discriminating_estimand_produces_no_findings(self):
        report = val.check(_estimand_spec())
        self.assertEqual(codes(report), set())

    # D-05: DSX-VAL-010
    def test_blank_quantity_produces_exactly_one_critical_val_010(self):
        report = val.check(_estimand_spec(quantity=""))
        found = [f for f in report.findings if f.code == "DSX-VAL-010"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.CRITICAL)
        self.assertEqual(found[0].where, "spec.validity_frame.estimand")
        self.assertIn("quantity", found[0].detail)
        self.assertNotIn("DSX-VAL-011", codes(report))

    def test_three_blank_fields_produce_one_val_010_naming_all_three(self):
        report = val.check(
            _estimand_spec(population="", contrast="", time_window="")
        )
        found = [f for f in report.findings if f.code == "DSX-VAL-010"]
        self.assertEqual(len(found), 1)
        for name in ("population", "contrast", "time_window"):
            self.assertIn(name, found[0].detail)

    def test_blank_falsifier_produces_exactly_one_high_val_011_and_no_val_010(self):
        report = val.check(_estimand_spec(falsifier=""))
        found = [f for f in report.findings if f.code == "DSX-VAL-011"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.HIGH)
        self.assertEqual(codes(report), {"DSX-VAL-011"})

    # D-05: DSX-VAL-011
    def test_angle_bracket_placeholder_falsifier_produces_val_011(self):
        report = val.check(_estimand_spec(falsifier=_TEMPLATE_PLACEHOLDER_FALSIFIER))
        self.assertIn("DSX-VAL-011", codes(report))

    def test_refusal_token_falsifier_produces_val_011(self):
        report = val.check(_estimand_spec(falsifier="none"))
        self.assertIn("DSX-VAL-011", codes(report))

    def test_non_discriminating_prose_falsifier_produces_val_011(self):
        report = val.check(
            _estimand_spec(falsifier="We will look at the data and decide")
        )
        self.assertIn("DSX-VAL-011", codes(report))

    def test_good_fixture_falsifier_produces_no_val_011(self):
        report = val.check(_estimand_spec(falsifier=_GOOD_FALSIFIER))
        self.assertNotIn("DSX-VAL-011", codes(report))

    def test_missing_validity_frame_key_produces_no_findings_and_does_not_raise(self):
        report = val.check({"spec_version": 1, "title": "t"})
        self.assertEqual(codes(report), set())

    def test_non_dict_validity_frame_and_estimand_degrade_to_no_findings(self):
        for bad_frame in ("s", [], None, 3):
            with self.subTest(bad_frame=bad_frame):
                report = val.check({"validity_frame": bad_frame})
                self.assertEqual(codes(report), set())
        for bad_estimand in ("s", [], None, 3):
            with self.subTest(bad_estimand=bad_estimand):
                report = val.check({"validity_frame": {"estimand": bad_estimand}})
                self.assertEqual(codes(report), set())

    def test_check_returns_report_named_val(self):
        report = val.check({})
        self.assertEqual(report.findings, [])
        self.assertEqual(report.check, "val")

    def test_estimand_judgment_point_appends_exactly_one_decision_record(self):
        report = val.check(_estimand_spec(quantity=""))
        decisions = report.context.get("decisions") or []
        self.assertEqual(len(decisions), 1)
        self.assertEqual(decisions[0]["layer"], "deterministic")
        self.assertEqual(decisions[0]["id"], "")
        self.assertEqual(decisions[0]["invocation_id"], "")
        self.assertTrue(decisions[0]["counterfactual"].strip())


# ── units (DSX-VAL-020, DSX-VAL-021) ────────────────────────────────────────


def _units_spec(
    observation: object = "session",
    assignment: object = "user",
    method_family_required: object = "cluster_robust",
    analysis: object = None,
    design: "dict | None" = None,
) -> dict:
    """A minimal spec carrying only a units/dependence pair, isolating the
    unit judgments from the estimand judgment (no `estimand` key at all, so
    the estimand decision record does not also append). `analysis` is only
    added to `units` when given, so DSX-VAL-021's tests can control it
    independently of `observation`/`assignment` without disturbing the
    DSX-VAL-020 tests, which never set it."""
    units: dict = {"observation": observation, "assignment": assignment}
    if analysis is not None:
        units["analysis"] = analysis
    spec: dict = {
        "validity_frame": {
            "units": units,
            "dependence": {"method_family_required": method_family_required},
        }
    }
    if design is not None:
        spec["design"] = design
    return spec


class TestValUnits(unittest.TestCase):
    # D-05: DSX-VAL-020
    def test_finer_observation_with_no_method_family_fires_critical_units_020(self):
        report = val.check(
            _units_spec(observation="impression", assignment="user", method_family_required="")
        )
        found = [f for f in report.findings if f.code == "DSX-VAL-020"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.CRITICAL)
        self.assertEqual(found[0].where, "spec.validity_frame.units")

    def test_finer_observation_with_declared_method_family_produces_no_units_020(self):
        report = val.check(
            _units_spec(
                observation="session", assignment="user", method_family_required="cluster_robust"
            )
        )
        self.assertNotIn("DSX-VAL-020", codes(report))

    def test_matching_observation_and_assignment_produces_no_units_020_regardless_of_method(self):
        for method_family in ("", "cluster_robust", None):
            with self.subTest(method_family=method_family):
                report = val.check(
                    _units_spec(
                        observation="user", assignment="user",
                        method_family_required=method_family,
                    )
                )
                self.assertNotIn("DSX-VAL-020", codes(report))

    def test_blank_observation_or_blank_assignment_produces_no_units_020(self):
        report = val.check(
            _units_spec(observation="", assignment="user", method_family_required="")
        )
        self.assertNotIn("DSX-VAL-020", codes(report))
        report = val.check(
            _units_spec(observation="impression", assignment="", method_family_required="")
        )
        self.assertNotIn("DSX-VAL-020", codes(report))

    def test_same_unit_named_two_ways_fires_units_020_with_alignment_remedy(self):
        report = val.check(
            _units_spec(observation="user", assignment="user_id", method_family_required="")
        )
        found = [f for f in report.findings if f.code == "DSX-VAL-020"]
        self.assertEqual(len(found), 1)
        self.assertIn("align", found[0].remedy.lower())

    def test_units_020_detail_carries_the_deff_formula_and_illustration_wording(self):
        report = val.check(
            _units_spec(observation="impression", assignment="user", method_family_required="")
        )
        found = [f for f in report.findings if f.code == "DSX-VAL-020"]
        detail = found[0].detail
        self.assertIn("1.576", detail)
        self.assertIn("illustrat", detail.lower())

    def test_malformed_units_subblock_produces_no_finding_and_does_not_raise(self):
        for bad_units in ("s", [], None, 3):
            with self.subTest(bad_units=bad_units):
                report = val.check({"validity_frame": {"units": bad_units}})
                self.assertNotIn("DSX-VAL-020", codes(report))

    def test_unit_triad_judgment_point_appends_exactly_one_decision_record(self):
        report = val.check(
            _units_spec(observation="impression", assignment="user", method_family_required="")
        )
        decisions = report.context.get("decisions") or []
        triad_decisions = [d for d in decisions if d["choice"].startswith("unit triad:")]
        self.assertEqual(len(triad_decisions), 1)
        self.assertEqual(triad_decisions[0]["layer"], "deterministic")
        self.assertTrue(triad_decisions[0]["counterfactual"].strip())

    # D-05: DSX-VAL-021
    def test_assignment_vs_randomization_unit_disagreement_fires_high_units_021(self):
        report = val.check(
            _units_spec(assignment="user", design={"randomization_unit": "account"})
        )
        found = [f for f in report.findings if f.code == "DSX-VAL-021"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.HIGH)
        for token in ("validity_frame.units.assignment", "design.randomization_unit",
                      "user", "account"):
            self.assertIn(token, found[0].detail)

    def test_analysis_vs_design_analysis_unit_disagreement_fires_units_021(self):
        report = val.check(
            _units_spec(analysis="session", design={"analysis_unit": "user"})
        )
        self.assertIn("DSX-VAL-021", codes(report))

    def test_both_pairs_agreeing_produces_no_units_021(self):
        report = val.check(
            _units_spec(
                assignment="user", analysis="user",
                design={"randomization_unit": "user", "analysis_unit": "user"},
            )
        )
        self.assertNotIn("DSX-VAL-021", codes(report))

    def test_blank_design_randomization_unit_produces_no_units_021(self):
        report = val.check(_units_spec(assignment="user", design={"randomization_unit": ""}))
        self.assertNotIn("DSX-VAL-021", codes(report))
        report = val.check(_units_spec(assignment="user", design={}))
        self.assertNotIn("DSX-VAL-021", codes(report))

    def test_blank_validity_frame_assignment_produces_no_units_021(self):
        report = val.check(
            _units_spec(assignment="", design={"randomization_unit": "account"})
        )
        self.assertNotIn("DSX-VAL-021", codes(report))

    def test_units_021_normalises_case_and_whitespace_before_comparing(self):
        report = val.check(
            _units_spec(assignment="  User ", design={"randomization_unit": "user"})
        )
        self.assertNotIn("DSX-VAL-021", codes(report))

    def test_units_021_never_fires_on_the_canonical_or_corpus_fixtures(self):
        import sys
        from pathlib import Path

        root = Path(__file__).resolve().parent.parent
        sys.path.insert(0, str(root))
        from dsx.loader import load  # noqa: E402

        fixtures = [root / "examples" / "good-ANALYSIS-SPEC.yaml",
                    root / "examples" / "bad-ANALYSIS-SPEC.yaml"]
        fixtures += sorted((root / "examples" / "known-bad").glob("*-ANALYSIS-SPEC.yaml"))
        self.assertGreaterEqual(len(fixtures), 5)
        for path in fixtures:
            with self.subTest(fixture=path.name):
                spec = load(str(path))
                report = val.check(spec)
                self.assertNotIn("DSX-VAL-021", codes(report), path.name)


# ── dependence and identification (DSX-VAL-030, DSX-VAL-040, DSX-VAL-041) ──


class TestValDependenceIdentification(unittest.TestCase):
    # D-05: DSX-VAL-030
    def test_dependence_structure_with_blank_method_family_fires_critical_val_030(self):
        report = val.check(
            {
                "validity_frame": {
                    "dependence": {"structure": "clustered", "method_family_required": ""}
                }
            }
        )
        found = [f for f in report.findings if f.code == "DSX-VAL-030"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.CRITICAL)
        self.assertEqual(found[0].where, "spec.validity_frame.dependence")

    def test_dependence_structure_with_admissible_method_family_produces_no_val_030(self):
        report = val.check(
            {
                "validity_frame": {
                    "dependence": {
                        "structure": "clustered",
                        "method_family_required": "cluster_robust",
                    }
                }
            }
        )
        self.assertNotIn("DSX-VAL-030", codes(report))

    def test_dependence_structure_with_inadmissible_method_family_names_the_admissible_set(self):
        report = val.check(
            {
                "validity_frame": {
                    "dependence": {
                        "structure": "clustered",
                        "method_family_required": "delta_method",
                    }
                }
            }
        )
        found = [f for f in report.findings if f.code == "DSX-VAL-030"]
        self.assertEqual(len(found), 1)
        for member in ("cluster_robust", "bootstrap_cluster", "mixed_effects"):
            self.assertIn(member, found[0].detail)

    def test_dependence_structure_none_with_blank_method_family_produces_no_val_030(self):
        report = val.check(
            {"validity_frame": {"dependence": {"structure": "none", "method_family_required": ""}}}
        )
        self.assertNotIn("DSX-VAL-030", codes(report))

    def test_absent_dependence_subblock_produces_no_val_030(self):
        report = val.check({"validity_frame": {"estimand": {}}})
        self.assertNotIn("DSX-VAL-030", codes(report))

    def test_out_of_vocabulary_dependence_structure_produces_no_val_030(self):
        report = val.check(
            {
                "validity_frame": {
                    "dependence": {"structure": "not_a_member", "method_family_required": ""}
                }
            }
        )
        self.assertNotIn("DSX-VAL-030", codes(report))

    def test_every_dependence_admissible_map_structure_is_exercised_at_least_once(self):
        from dsx.spec import DEPENDENCE_ADMISSIBLE_METHODS

        for structure, admissible in DEPENDENCE_ADMISSIBLE_METHODS.items():
            with self.subTest(structure=structure):
                blocked = val.check(
                    {
                        "validity_frame": {
                            "dependence": {"structure": structure, "method_family_required": ""}
                        }
                    }
                )
                self.assertIn("DSX-VAL-030", codes(blocked))

                passing_method = sorted(admissible)[0]
                passed = val.check(
                    {
                        "validity_frame": {
                            "dependence": {
                                "structure": structure,
                                "method_family_required": passing_method,
                            }
                        }
                    }
                )
                self.assertNotIn("DSX-VAL-030", codes(passed))

    def test_malformed_dependence_subblock_produces_no_finding_and_does_not_raise(self):
        for bad_dependence in ("s", [], None, 3):
            with self.subTest(bad_dependence=bad_dependence):
                report = val.check({"validity_frame": {"dependence": bad_dependence}})
                self.assertNotIn("DSX-VAL-030", codes(report))

    def test_dependence_judgment_point_appends_exactly_one_decision_record(self):
        report = val.check(
            {
                "validity_frame": {
                    "dependence": {"structure": "clustered", "method_family_required": ""}
                }
            }
        )
        decisions = report.context.get("decisions") or []
        dependence_decisions = [d for d in decisions if d["choice"].startswith("dependence:")]
        self.assertEqual(len(dependence_decisions), 1)
        self.assertEqual(dependence_decisions[0]["layer"], "deterministic")
        self.assertTrue(dependence_decisions[0]["counterfactual"].strip())

    # D-05: DSX-VAL-040
    def test_weak_identification_with_no_constraint_fires_critical_val_040_and_no_val_041(self):
        report = val.check(
            {
                "validity_frame": {
                    "identification": {"strength": "weak", "constraint_source": "none"}
                }
            }
        )
        found = [f for f in report.findings if f.code == "DSX-VAL-040"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.CRITICAL)
        self.assertEqual(found[0].where, "spec.validity_frame.identification")
        self.assertNotIn("DSX-VAL-041", codes(report))

    def test_weak_identification_with_a_real_constraint_produces_neither_identification_code(self):
        report = val.check(
            {
                "validity_frame": {
                    "identification": {
                        "strength": "weak",
                        "constraint_source": "informative_priors",
                    }
                }
            }
        )
        self.assertNotIn("DSX-VAL-040", codes(report))
        self.assertNotIn("DSX-VAL-041", codes(report))

    # D-05: DSX-VAL-041
    def test_strong_identification_with_informative_priors_fires_high_val_041_and_no_val_040(self):
        report = val.check(
            {
                "validity_frame": {
                    "identification": {
                        "strength": "strong",
                        "constraint_source": "informative_priors",
                    }
                }
            }
        )
        found = [f for f in report.findings if f.code == "DSX-VAL-041"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.HIGH)
        self.assertNotIn("DSX-VAL-040", codes(report))

    def test_strong_identification_with_each_parameter_scale_constraint_fires_val_041(self):
        for constraint in ("penalisation", "design_restriction", "hierarchical_pooling"):
            with self.subTest(constraint=constraint):
                report = val.check(
                    {
                        "validity_frame": {
                            "identification": {
                                "strength": "strong",
                                "constraint_source": constraint,
                            }
                        }
                    }
                )
                self.assertIn("DSX-VAL-041", codes(report))

    def test_strong_identification_with_constraint_source_none_produces_neither_identification_code(self):
        report = val.check(
            {
                "validity_frame": {
                    "identification": {"strength": "strong", "constraint_source": "none"}
                }
            }
        )
        self.assertNotIn("DSX-VAL-040", codes(report))
        self.assertNotIn("DSX-VAL-041", codes(report))

    def test_moderate_identification_produces_neither_identification_code_with_any_constraint(self):
        for constraint in (
            "none", "informative_priors", "penalisation", "design_restriction",
            "hierarchical_pooling",
        ):
            with self.subTest(constraint=constraint):
                report = val.check(
                    {
                        "validity_frame": {
                            "identification": {
                                "strength": "moderate",
                                "constraint_source": constraint,
                            }
                        }
                    }
                )
                self.assertNotIn("DSX-VAL-040", codes(report))
                self.assertNotIn("DSX-VAL-041", codes(report))

    def test_out_of_vocabulary_identification_strength_or_constraint_produces_neither_code(self):
        report = val.check(
            {
                "validity_frame": {
                    "identification": {
                        "strength": "not_a_member",
                        "constraint_source": "none",
                    }
                }
            }
        )
        self.assertNotIn("DSX-VAL-040", codes(report))
        self.assertNotIn("DSX-VAL-041", codes(report))
        report = val.check(
            {
                "validity_frame": {
                    "identification": {
                        "strength": "weak",
                        "constraint_source": "not_a_member",
                    }
                }
            }
        )
        self.assertNotIn("DSX-VAL-040", codes(report))
        self.assertNotIn("DSX-VAL-041", codes(report))

    def test_blank_identification_strength_or_constraint_source_produces_neither_code(self):
        report = val.check(
            {"validity_frame": {"identification": {"strength": "", "constraint_source": "none"}}}
        )
        self.assertNotIn("DSX-VAL-040", codes(report))
        self.assertNotIn("DSX-VAL-041", codes(report))
        report = val.check(
            {
                "validity_frame": {
                    "identification": {"strength": "weak", "constraint_source": ""}
                }
            }
        )
        self.assertNotIn("DSX-VAL-040", codes(report))
        self.assertNotIn("DSX-VAL-041", codes(report))

    def test_malformed_identification_subblock_produces_no_finding_and_does_not_raise(self):
        for bad_identification in ("s", [], None, 3):
            with self.subTest(bad_identification=bad_identification):
                report = val.check({"validity_frame": {"identification": bad_identification}})
                self.assertNotIn("DSX-VAL-040", codes(report))
                self.assertNotIn("DSX-VAL-041", codes(report))

    def test_identification_judgment_point_appends_one_decision_record_distinguishing_outcomes(self):
        weak_report = val.check(
            {
                "validity_frame": {
                    "identification": {"strength": "weak", "constraint_source": "none"}
                }
            }
        )
        weak_decisions = [
            d
            for d in (weak_report.context.get("decisions") or [])
            if d["choice"].startswith("identification:")
        ]
        self.assertEqual(len(weak_decisions), 1)
        self.assertIn("DSX-VAL-040", weak_decisions[0]["choice"])

        strong_report = val.check(
            {
                "validity_frame": {
                    "identification": {
                        "strength": "strong",
                        "constraint_source": "informative_priors",
                    }
                }
            }
        )
        strong_decisions = [
            d
            for d in (strong_report.context.get("decisions") or [])
            if d["choice"].startswith("identification:")
        ]
        self.assertEqual(len(strong_decisions), 1)
        self.assertIn("DSX-VAL-041", strong_decisions[0]["choice"])
        self.assertNotEqual(weak_decisions[0]["choice"], strong_decisions[0]["choice"])


# ── disjointness (REQ-P7-03): DSX-VAL-020 and DSX-EXP-021 never both fire ──


def _all_fixture_paths() -> "list[Path]":
    root = Path(__file__).resolve().parent.parent
    paths = [
        root / "examples" / "good-ANALYSIS-SPEC.yaml",
        root / "examples" / "bad-ANALYSIS-SPEC.yaml",
        root / "templates" / "ANALYSIS-SPEC.yaml",
    ]
    paths += sorted((root / "examples" / "known-bad").glob("*-ANALYSIS-SPEC.yaml"))
    return paths


# The content hash of dsx/checks/design.py (REQ-P7-03's other half — this
# family must never be edited during Phase 7). Measured 2026-08-12 against
# the file as it stood at the start of plan 07-04, over UTF-8 bytes with
# CRLF normalised to LF before hashing (this repository checks out CRLF on
# Windows, and a hash taken over raw bytes would differ between a Windows
# and a Linux checkout for no real reason — see .claude/CLAUDE.md's line-
# ending guidance). A deliberate future change to dsx/checks/design.py must
# update this constant in the same commit and say why in the commit message
# — this test is what forces that, rather than letting a silent edit pass.
_DESIGN_PY_SHA256 = "b7807c3480da7515b8019cf50ea815af88954bde1f51f67e887a147c7292604a"


def _design_py_hash() -> str:
    root = Path(__file__).resolve().parent.parent
    data = (root / "dsx" / "checks" / "design.py").read_bytes()
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


class TestValSamplingMissingnessMeasurement(unittest.TestCase):
    # D-05: DSX-VAL-050
    def test_blank_claim_population_fires_high_val_050_naming_the_field(self):
        report = val.check(
            {
                "validity_frame": {
                    "sampling_frame": {
                        "claim_population": "",
                        "known_exclusions": [],
                        "selection_risk": "none identified",
                    }
                }
            }
        )
        found = [f for f in report.findings if f.code == "DSX-VAL-050"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.HIGH)
        self.assertEqual(found[0].where, "spec.validity_frame.sampling_frame.claim_population")

    def test_sampling_frame_known_exclusions_with_blank_selection_risk_fires_val_050(self):
        report = val.check(
            {
                "validity_frame": {
                    "sampling_frame": {
                        "claim_population": "all new signups",
                        "known_exclusions": ["bots"],
                        "selection_risk": "",
                    }
                }
            }
        )
        self.assertIn("DSX-VAL-050", codes(report))

    def test_sampling_frame_known_exclusions_with_a_stated_selection_risk_produces_no_finding(
        self,
    ):
        # The good fixture's own configuration (examples/good-ANALYSIS-SPEC.yaml:338-342).
        report = val.check(
            {
                "validity_frame": {
                    "sampling_frame": {
                        "claim_population": "all new signups, 2026-06-01 to 2026-06-14",
                        "known_exclusions": ["bot-flagged traffic"],
                        "selection_risk": "none identified",
                    }
                }
            }
        )
        self.assertNotIn("DSX-VAL-050", codes(report))

    def test_sampling_frame_no_exclusions_and_blank_selection_risk_produces_no_finding(self):
        report = val.check(
            {
                "validity_frame": {
                    "sampling_frame": {
                        "claim_population": "all new signups",
                        "known_exclusions": [],
                        "selection_risk": "",
                    }
                }
            }
        )
        self.assertNotIn("DSX-VAL-050", codes(report))

    def test_placeholder_claim_population_produces_no_val_050(self):
        # The template's own configuration (templates/ANALYSIS-SPEC.yaml:330-334) — plain
        # blankness only, never the placeholder detector (D-06).
        report = val.check(
            {
                "validity_frame": {
                    "sampling_frame": {
                        "claim_population": "<the population the claim will be made about>",
                        "known_exclusions": [],
                        "selection_risk": (
                            "<how it could differ systematically from the claim population>"
                        ),
                    }
                }
            }
        )
        self.assertNotIn("DSX-VAL-050", codes(report))

    # D-05: DSX-VAL-070
    def test_measurement_construct_with_blank_operationalisation_fires_high_val_070(self):
        report = val.check(
            {
                "validity_frame": {
                    "measurement": {"construct": "activation", "operationalisation": ""}
                }
            }
        )
        found = [f for f in report.findings if f.code == "DSX-VAL-070"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.HIGH)
        self.assertEqual(
            found[0].where, "spec.validity_frame.measurement.operationalisation"
        )

    def test_blank_measurement_construct_produces_no_val_070_whatever_operationalisation_says(
        self,
    ):
        for operationalisation in ("", "some rule", "<placeholder>"):
            with self.subTest(operationalisation=operationalisation):
                report = val.check(
                    {
                        "validity_frame": {
                            "measurement": {
                                "construct": "",
                                "operationalisation": operationalisation,
                            }
                        }
                    }
                )
                self.assertNotIn("DSX-VAL-070", codes(report))

    def test_placeholder_measurement_construct_and_operationalisation_produce_no_finding(self):
        # The template's own configuration (templates/ANALYSIS-SPEC.yaml:341-344).
        report = val.check(
            {
                "validity_frame": {
                    "measurement": {
                        "construct": "<the concept being measured>",
                        "operationalisation": "<the exact rule that turns the construct into a number>",
                    }
                }
            }
        )
        self.assertNotIn("DSX-VAL-070", codes(report))

    # D-05: DSX-VAL-060
    def test_missingness_mar_mechanism_with_complete_case_fires_high_val_060(self):
        report = val.check(
            {
                "validity_frame": {
                    "missingness": {"mechanism": "MAR", "method_implied": "complete_case"}
                }
            }
        )
        found = [f for f in report.findings if f.code == "DSX-VAL-060"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.HIGH)

    def test_missingness_mar_mechanism_with_available_case_fires_val_060(self):
        report = val.check(
            {
                "validity_frame": {
                    "missingness": {"mechanism": "MAR", "method_implied": "available_case"}
                }
            }
        )
        found = [f for f in report.findings if f.code == "DSX-VAL-060"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.HIGH)

    def test_mar_mechanism_with_multiple_imputation_produces_no_missingness_finding(self):
        report = val.check(
            {
                "validity_frame": {
                    "missingness": {"mechanism": "MAR", "method_implied": "multiple_imputation"}
                }
            }
        )
        self.assertNotIn("DSX-VAL-060", codes(report))

    def test_mcar_mechanism_with_complete_case_produces_no_missingness_finding(self):
        report = val.check(
            {
                "validity_frame": {
                    "missingness": {"mechanism": "MCAR", "method_implied": "complete_case"}
                }
            }
        )
        self.assertNotIn("DSX-VAL-060", codes(report))

    def test_missingness_mnar_mechanism_with_complete_case_fires_critical_val_060(self):
        report = val.check(
            {
                "validity_frame": {
                    "missingness": {"mechanism": "MNAR", "method_implied": "complete_case"}
                }
            }
        )
        found = [f for f in report.findings if f.code == "DSX-VAL-060"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.CRITICAL)

    def test_missingness_mnar_mechanism_with_an_explicit_mechanism_model_produces_no_finding(self):
        for method in ("mechanism_model", "selection_model", "pattern_mixture_model"):
            with self.subTest(method=method):
                report = val.check(
                    {
                        "validity_frame": {
                            "missingness": {"mechanism": "MNAR", "method_implied": method}
                        }
                    }
                )
                self.assertNotIn("DSX-VAL-060", codes(report))

    def test_missingness_mnar_mechanism_with_an_unrecognised_method_fires_critical_val_060(self):
        report = val.check(
            {
                "validity_frame": {
                    "missingness": {
                        "mechanism": "MNAR",
                        "method_implied": "some_novel_approach",
                    }
                }
            }
        )
        found = [f for f in report.findings if f.code == "DSX-VAL-060"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.CRITICAL)

    def test_missingness_mar_mechanism_with_an_unrecognised_method_produces_no_finding(self):
        report = val.check(
            {
                "validity_frame": {
                    "missingness": {
                        "mechanism": "MAR",
                        "method_implied": "some_novel_approach",
                    }
                }
            }
        )
        self.assertNotIn("DSX-VAL-060", codes(report))

    def test_not_assessed_missingness_mechanism_produces_no_finding_for_any_method(self):
        for method_implied in (
            "complete_case", "available_case", "multiple_imputation", "", None,
        ):
            with self.subTest(method_implied=method_implied):
                report = val.check(
                    {
                        "validity_frame": {
                            "missingness": {
                                "mechanism": "not_assessed",
                                "method_implied": method_implied,
                            }
                        }
                    }
                )
                self.assertNotIn("DSX-VAL-060", codes(report))

    def test_missingness_rate_is_never_read_by_the_check(self):
        baseline = None
        for rate in (0, 0.4, None, "not_a_number"):
            with self.subTest(rate=rate):
                missingness = {"mechanism": "MAR", "method_implied": "complete_case"}
                if rate is not None:
                    missingness["rate"] = rate
                report = val.check({"validity_frame": {"missingness": missingness}})
                found = [
                    (f.code, f.severity) for f in report.findings if f.code == "DSX-VAL-060"
                ]
                if baseline is None:
                    baseline = found
                    self.assertEqual(len(baseline), 1)
                else:
                    self.assertEqual(found, baseline)

    def test_malformed_missingness_subblock_produces_no_finding_and_does_not_raise(self):
        for malformed in ("a string", ["a", "list"], None, 5):
            with self.subTest(malformed=malformed):
                report = val.check({"validity_frame": {"missingness": malformed}})
                self.assertNotIn("DSX-VAL-060", codes(report))

    def test_missingness_known_bad_corpus_fixtures_never_fire_val_060(self):
        root = Path(__file__).resolve().parent.parent
        fixtures = sorted((root / "examples" / "known-bad").glob("*-ANALYSIS-SPEC.yaml"))
        self.assertGreaterEqual(len(fixtures), 3)
        for path in fixtures:
            with self.subTest(fixture=path.name):
                spec = load(str(path))
                report = val.check(spec)
                self.assertNotIn("DSX-VAL-060", codes(report), path.name)

    def test_malformed_sampling_frame_and_measurement_subblocks_produce_no_finding_and_do_not_raise(
        self,
    ):
        for malformed in ("a string", ["a", "list"], None, 5):
            with self.subTest(malformed=malformed):
                report = val.check(
                    {
                        "validity_frame": {
                            "sampling_frame": malformed,
                            "measurement": malformed,
                        }
                    }
                )
                self.assertNotIn("DSX-VAL-050", codes(report))
                self.assertNotIn("DSX-VAL-070", codes(report))

    def test_sampling_frame_and_measurement_judgment_points_each_append_one_decision_record(
        self,
    ):
        report = val.check(
            {
                "validity_frame": {
                    "sampling_frame": {
                        "claim_population": "",
                        "known_exclusions": [],
                        "selection_risk": "",
                    },
                    "measurement": {"construct": "activation", "operationalisation": ""},
                }
            }
        )
        decisions = report.context["decisions"]
        by_choice_prefix = {
            prefix: [d for d in decisions if d["choice"].startswith(prefix)]
            for prefix in ("sampling frame:", "measurement:")
        }
        for prefix, matches in by_choice_prefix.items():
            self.assertEqual(len(matches), 1, prefix)
            record = matches[0]
            self.assertEqual(record["layer"], "deterministic")
            self.assertTrue(record["counterfactual"])


class TestValExpUnitsDisjointness(unittest.TestCase):
    def test_bad_fixture_trips_exp_021_and_not_val_020(self):
        from dsx.loader import load

        root = Path(__file__).resolve().parent.parent
        spec = load(str(root / "examples" / "bad-ANALYSIS-SPEC.yaml"))
        design_codes = codes(design.check(spec))
        val_codes = codes(val.check(spec))
        self.assertIn("DSX-EXP-021", design_codes)
        self.assertNotIn("DSX-VAL-020", val_codes)

    def test_unit_triad_defect_with_agreeing_design_units_trips_val_020_and_not_exp_021(self):
        spec = {
            "question_type": "causal",
            "design": {
                "kind": "experiment",
                "randomization_unit": "user",
                "analysis_unit": "user",
            },
            "validity_frame": {
                "units": {"observation": "impression", "assignment": "user"},
                "dependence": {"method_family_required": ""},
            },
        }
        design_codes = codes(design.check(spec))
        val_codes = codes(val.check(spec))
        self.assertIn("DSX-VAL-020", val_codes)
        self.assertNotIn("DSX-EXP-021", design_codes)

    def test_no_fixture_in_the_repository_trips_both_units_codes_at_once(self):
        from dsx.loader import load

        fixtures = _all_fixture_paths()
        self.assertGreaterEqual(len(fixtures), 6)
        for path in fixtures:
            with self.subTest(fixture=path.name):
                spec = load(str(path))
                design_codes = codes(design.check(spec))
                val_codes = codes(val.check(spec))
                self.assertFalse(
                    "DSX-EXP-021" in design_codes and "DSX-VAL-020" in val_codes,
                    f"{path.name} trips both DSX-EXP-021 and DSX-VAL-020",
                )

    def test_editing_only_validity_frame_never_changes_which_design_codes_fire(self):
        base = {
            "question_type": "causal",
            "design": {
                "kind": "experiment",
                "randomization_unit": "user",
                "analysis_unit": "session",
            },
            "validity_frame": {
                "units": {"observation": "user", "assignment": "user"},
                "dependence": {"method_family_required": ""},
            },
        }
        edited = copy.deepcopy(base)
        edited["validity_frame"]["units"]["observation"] = "impression"
        edited["validity_frame"]["dependence"]["method_family_required"] = ""
        self.assertEqual(codes(val.check(base)), set())
        self.assertIn("DSX-VAL-020", codes(val.check(edited)))
        self.assertEqual(codes(design.check(base)), codes(design.check(edited)))

    def test_editing_only_design_never_changes_which_validity_codes_fire(self):
        base = {
            "question_type": "causal",
            "design": {
                "kind": "experiment",
                "randomization_unit": "user",
                "analysis_unit": "session",
            },
            "validity_frame": {
                "units": {"observation": "user", "assignment": "user"},
                "dependence": {"method_family_required": ""},
            },
        }
        edited = copy.deepcopy(base)
        edited["design"]["analysis_unit"] = "user"
        self.assertIn("DSX-EXP-021", codes(design.check(base)))
        self.assertNotIn("DSX-EXP-021", codes(design.check(edited)))
        self.assertEqual(codes(val.check(base)), codes(val.check(edited)))

    def test_design_checks_py_content_is_unmodified_since_phase_start(self):
        self.assertEqual(
            _design_py_hash(), _DESIGN_PY_SHA256,
            "dsx/checks/design.py was edited during Phase 7 — REQ-P7-03 requires it "
            "unmodified; if this is a deliberate change, update _DESIGN_PY_SHA256 in "
            "this test and say why in the commit message",
        )


# ── gate-level severity split (REQ-P7-05, ROADMAP success criterion 1) ─────
#
# Proves the roadmap's severity wording at the gate, not just at the unit
# level: DSX-VAL-040 (CRITICAL) blocks from plan onward; DSX-VAL-041 (HIGH)
# prints at plan without blocking, and blocks at verify and ship; neither
# code runs at execute, because "val" is not in that gate profile.


class TestValGateSeverity(unittest.TestCase):
    ROOT = Path(__file__).resolve().parent.parent

    def _run(self, argv: "list[str]") -> "tuple[int, str, str]":
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(argv)
        return code, out.getvalue(), err.getvalue()

    def _write_identification_variant(self, tmp: str, identification: dict) -> str:
        """Clone the good fixture into ``tmp``, replacing only its
        validity_frame.identification block, so the spec is otherwise
        complete and no unrelated defect blocks the gate and masks the
        result under test. Written as JSON regardless of the .yaml suffix —
        ``dsx.loader.loads()`` tries a JSON parse before YAML/the bundled
        parser whenever the stripped text starts with '{' — matching the
        precedent at ``tests/test_dsx.py``'s
        ``_bayesian_variant_spec_path``.
        """
        spec = load(str(self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml"))
        spec["validity_frame"]["identification"] = identification
        path = Path(tmp) / "ANALYSIS-SPEC.yaml"
        path.write_text(json.dumps(spec), encoding="utf-8")
        return str(path)

    def test_weak_no_constraint_spec_blocks_gate_plan_naming_val_040(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_identification_variant(
                tmp,
                {
                    "strength": "weak",
                    "evidence": "covariate adjustment only, no design-based support",
                    "constraint_source": "none",
                    "constraint_justification": "",
                },
            )
            code, _, err = self._run(["gate", "plan", "--spec", path])
            self.assertEqual(code, 1)
            self.assertIn("DSX-VAL-040", err)

    def test_strong_informative_priors_spec_passes_gate_plan_but_still_prints_val_041(self):
        """The behaviour most likely to be gotten wrong: a HIGH-severity
        finding at the plan gate must be visible in the output and must not
        flip the exit code. Asserting only the exit code would pass even if
        the finding were silently dropped — assert both halves."""
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_identification_variant(
                tmp,
                {
                    "strength": "strong",
                    "evidence": "Assignment is randomized per user at first pageview.",
                    "constraint_source": "informative_priors",
                    "constraint_justification": "A weakly informative prior on the effect size.",
                },
            )
            code, out, err = self._run(["gate", "plan", "--spec", path])
            self.assertEqual(code, 0, err)
            # Passing output goes to stdout (dsx/findings.py::emit) — blocking
            # output would go to stderr, but this gate does not block.
            self.assertIn("DSX-VAL-041", out)

    def test_strong_informative_priors_spec_blocks_gate_verify_and_gate_ship_naming_val_041(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_identification_variant(
                tmp,
                {
                    "strength": "strong",
                    "evidence": "Assignment is randomized per user at first pageview.",
                    "constraint_source": "informative_priors",
                    "constraint_justification": "A weakly informative prior on the effect size.",
                },
            )
            for point in ("verify", "ship"):
                with self.subTest(point=point):
                    code, _, err = self._run(["gate", point, "--spec", path])
                    self.assertEqual(code, 1)
                    self.assertIn("DSX-VAL-041", err)

    def test_neither_identification_spec_produces_a_validity_frame_finding_at_gate_execute(self):
        variants = (
            {
                "strength": "weak",
                "evidence": "covariate adjustment only, no design-based support",
                "constraint_source": "none",
                "constraint_justification": "",
            },
            {
                "strength": "strong",
                "evidence": "Assignment is randomized per user at first pageview.",
                "constraint_source": "informative_priors",
                "constraint_justification": "A weakly informative prior on the effect size.",
            },
        )
        for identification in variants:
            with self.subTest(strength=identification["strength"]):
                with tempfile.TemporaryDirectory() as tmp:
                    path = self._write_identification_variant(tmp, identification)
                    _, out, err = self._run(["gate", "execute", "--spec", path])
                    combined = out + err
                    self.assertNotIn("DSX-VAL-040", combined)
                    self.assertNotIn("DSX-VAL-041", combined)

    def test_val_check_is_reachable_from_at_least_one_gate_profile(self):
        """The standing per-phase deliverable (STATE.md): every validity
        frame code shipped so far is reachable from at least one gate
        profile. Every DSX-VAL-* code fires through the single "val" check
        dispatcher (dsx/frame/val.py::check), so proving "val" is a
        registered check reachable from at least one gate profile proves
        every code this module ships is reachable from that profile —
        derived by intersecting the registered checks with the profile
        tuples, not from a hand-written list of codes that would silently
        stop holding once plan 07-06 adds three more.
        """
        from dsx.cli import CHECKS, GATE_PROFILES

        self.assertIn("val", CHECKS)
        self.assertIs(CHECKS["val"], val.check)

        registered_checks = set(CHECKS)
        reachable_profiles = [
            point
            for point, checks in GATE_PROFILES.items()
            if "val" in (set(checks) & registered_checks)
        ]
        self.assertTrue(
            reachable_profiles,
            "val is registered in CHECKS but reachable from no gate profile — every "
            "DSX-VAL-* code would then be unreachable from any gate",
        )


# ── fixture matrix (REQ-P7-*, whole family): every spec file in the repo ───
#
# Discovers every analysis-spec fixture using the same glob idiom
# tests/test_known_bad_corpus.py uses (never a hardcoded filename list), so a
# fixture added by a later phase is picked up structurally rather than by
# someone remembering to list it. _all_fixture_paths() (defined above) is
# already that discovery: examples/good-ANALYSIS-SPEC.yaml,
# examples/bad-ANALYSIS-SPEC.yaml, templates/ANALYSIS-SPEC.yaml, and every
# *-ANALYSIS-SPEC.yaml under examples/known-bad/.

# Measured 2026-08-12 against the fixtures as they stand after plan 07-06:
# loaded each path in _all_fixture_paths() via dsx.loader.load(), ran
# dsx.frame.val.check(spec), and recorded {f.code for f in report.findings}.
# A constant that looks derived but was actually guessed is worse than no
# constant — the same discipline tests/test_known_bad_corpus.py's own
# measured allow-list documents.
_EXPECTED_VAL_CODES: "dict[str, set[str]]" = {
    "good-ANALYSIS-SPEC.yaml": set(),
    "bad-ANALYSIS-SPEC.yaml": {"DSX-VAL-011"},
    "ANALYSIS-SPEC.yaml": {"DSX-VAL-011"},
    "bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml": {"DSX-VAL-041"},
    "frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml": set(),
    "interference-shared-budget-ANALYSIS-SPEC.yaml": set(),
    # Measured 2026-08-12 (plan 07-07) against the fixture as committed in this
    # plan: loaded via dsx.loader.load(), ran dsx.frame.val.check(spec), recorded
    # {f.code for f in report.findings}. identification.strength: weak paired with
    # constraint_source: none is the fixture's sole encoded defect (DSX-VAL-040);
    # every other validity_frame sub-block is clean.
    "weak-identification-mmm-ANALYSIS-SPEC.yaml": {"DSX-VAL-040"},
    # Measured 2026-08-12 (plan 08-02) against the fixture as committed in this
    # plan: loaded via dsx.loader.load(), ran dsx.frame.val.check(spec), recorded
    # {f.code for f in report.findings}. This fixture's encoded defect lives in
    # validity_frame.triggering (DSX-INT-030, Phase 8, plan 08-04) — units,
    # dependence, identification, sampling_frame, missingness and measurement
    # are all populated the same way the good fixture's are, so no DSX-VAL-*
    # code fires.
    "triggering-dilution-ANALYSIS-SPEC.yaml": set(),
}


class TestValFixtureMatrix(unittest.TestCase):
    # Behaviour 1
    def test_every_discovered_fixture_loads_and_checks_without_raising(self):
        fixtures = _all_fixture_paths()
        self.assertGreaterEqual(len(fixtures), 6)
        for path in fixtures:
            with self.subTest(fixture=path.name):
                spec = load(str(path))
                val.check(spec)  # must not raise

    # Behaviour 3: the guard that makes this class worth having — a fixture
    # discovered by glob with no expectation must fail loudly, not skip
    # silently, so a fixture added later cannot slip through unexamined.
    def test_discovered_fixture_set_equals_the_expected_dictionarys_key_set(self):
        discovered = {path.name for path in _all_fixture_paths()}
        expected = set(_EXPECTED_VAL_CODES)
        missing = discovered - expected
        self.assertEqual(
            missing,
            set(),
            "Fixture(s) discovered by glob with no entry in _EXPECTED_VAL_CODES: "
            f"{sorted(missing)}. Add an entry naming the DSX-VAL-* codes this fixture "
            "is expected to produce (an empty set if none), measured by running "
            "dsx.frame.val.check() against the loaded fixture — do not guess it.",
        )
        stale = expected - discovered
        self.assertEqual(
            stale,
            set(),
            f"_EXPECTED_VAL_CODES names file(s) no longer discovered by glob: "
            f"{sorted(stale)}. Remove the stale entry.",
        )

    # Behaviour 2
    def test_each_fixture_produces_exactly_its_expected_val_code_set(self):
        for path in _all_fixture_paths():
            with self.subTest(fixture=path.name):
                expected = _EXPECTED_VAL_CODES.get(path.name)
                if expected is None:
                    continue  # the guard test above already fails this case loudly
                spec = load(str(path))
                report = val.check(spec)
                self.assertEqual(codes(report), expected, path.name)

    # Behaviour 4
    def test_good_fixture_expected_val_code_set_is_empty(self):
        self.assertEqual(_EXPECTED_VAL_CODES["good-ANALYSIS-SPEC.yaml"], set())

    # Behaviour 5: closes the decision-trail obligation for the family as a
    # whole in one place, rather than repeating a partial assertion in every
    # per-code test.
    def test_every_decision_record_the_family_produces_has_the_standard_shape(self):
        saw_at_least_one_decision = False
        for path in _all_fixture_paths():
            with self.subTest(fixture=path.name):
                spec = load(str(path))
                report = val.check(spec)
                decisions = report.context.get("decisions") or []
                for decision in decisions:
                    saw_at_least_one_decision = True
                    self.assertEqual(decision["id"], "")
                    self.assertEqual(decision["invocation_id"], "")
                    self.assertEqual(decision["layer"], "deterministic")
                    self.assertTrue(decision["counterfactual"].strip())
        self.assertTrue(
            saw_at_least_one_decision,
            "no fixture in the repository reached any validity-frame judgment point",
        )


# ── gate integration for the weak-identification-mmm fixture (REQ-P7-05, ────
# ROADMAP Success Criterion 1, plan 07-07) ──────────────────────────────────
#
# The other TestValGateSeverity tests above prove the plan/verify/ship/execute
# split against synthetic identification-block variants cloned from the good
# fixture. This class proves the roadmap's own success criterion directly,
# against the real committed corpus fixture the roadmap names by filename —
# the end-to-end edge plan 07-07's threat model calls out: the fixture must
# block at one gate point and clear another, in the same repository,
# discovered by the same glob tests/test_known_bad_corpus.py uses.


class TestValGateIntegration(unittest.TestCase):
    ROOT = Path(__file__).resolve().parent.parent
    FIXTURE = ROOT / "examples" / "known-bad" / "weak-identification-mmm-ANALYSIS-SPEC.yaml"

    def _run(self, argv: "list[str]") -> "tuple[int, str, str]":
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_weak_identification_mmm_fixture_exists(self):
        self.assertTrue(
            self.FIXTURE.is_file(),
            f"{self.FIXTURE} does not exist — ROADMAP Success Criterion 1 names this exact path",
        )

    def test_weak_identification_mmm_fixture_blocks_gate_plan_naming_val_040(self):
        code, _out, err = self._run(["gate", "plan", "--spec", str(self.FIXTURE)])
        self.assertEqual(code, 1, f"expected dsx gate plan to block; stderr: {err}")
        self.assertIn("DSX-VAL-040", err)

    def test_weak_identification_mmm_fixture_clears_gate_execute(self):
        code, _out, err = self._run(["gate", "execute", "--spec", str(self.FIXTURE)])
        self.assertEqual(code, 0, f"expected dsx gate execute to pass; stderr: {err}")


# ── citation obligations for the DSX-VAL-* family (D-05, plan 07-07 Task 2) ─
#
# scripts/gen-finding-catalogue.py --check is the mechanical, repository-wide
# enforcement of D-05 and must stay green (see the module docstring's `Run:`
# line and this phase's acceptance criteria). This class exists so a future
# change to that script cannot silently stop enforcing this family's citation
# obligations without a test noticing — it re-derives the same three facts
# from dsx/frame/val.py directly, by parsing rather than by a hand-written
# list of function or code names, so a helper this module adds later is
# covered automatically.

_VAL_MODULE_PATH = Path(__file__).resolve().parent.parent / "dsx" / "frame" / "val.py"
_TESTS_ROOT = Path(__file__).resolve().parent
_CATALOGUE_PATH = Path(__file__).resolve().parent.parent / "references" / "finding-codes.md"

# Same two patterns scripts/gen-finding-catalogue.py's D-05 check compiles —
# multiline, with no line-end anchor, so this repository's CRLF checkout
# cannot change the result (`^` under re.MULTILINE re-anchors at the start of
# every line regardless of whether it ends `\n` or `\r\n`).
_CITATION_LINE_RE = re.compile(r"^\s*Citation:\s*\S", re.MULTILINE)
_REFVALUE_LINE_RE = re.compile(
    r"^\s*(?:Reference value|Structural criterion):\s*\S", re.MULTILINE
)
_TEST_MARKER_LINE_RE = re.compile(r"#\s*D-05:\s*(DSX-[A-Z]+-\d{3})")


def _val_module_tree() -> ast.Module:
    return ast.parse(
        _VAL_MODULE_PATH.read_text(encoding="utf-8"), filename=str(_VAL_MODULE_PATH)
    )


def _functions_emitting_findings() -> "dict[str, str]":
    """Every function in dsx/frame/val.py that calls ``report.add(...)``,
    mapped to its own docstring (``""`` if it has none). Derived by walking
    the module's AST and, for each qualifying call, climbing to its nearest
    enclosing ``FunctionDef`` — not by naming functions by hand, so a helper
    added later is covered automatically."""
    tree = _val_module_tree()
    parents: "dict[ast.AST, ast.AST]" = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[child] = parent

    functions: "dict[str, str]" = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Attribute) and func.attr == "add"):
            continue
        current: ast.AST = node
        while current in parents:
            current = parents[current]
            if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions[current.name] = ast.get_docstring(current) or ""
                break
    return functions


def _codes_emitted_by_val_module() -> "set[str]":
    """Every ``DSX-VAL-*`` code named as the first argument of a
    ``report.add(...)`` call in dsx/frame/val.py, derived by parsing rather
    than by naming codes by hand."""
    tree = _val_module_tree()
    emitted: "set[str]" = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Attribute) and func.attr == "add"):
            continue
        if not node.args:
            continue
        first = node.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            if first.value.startswith("DSX-VAL-"):
                emitted.add(first.value)
    return emitted


def _test_markers_under_tests_root() -> "set[str]":
    markers: "set[str]" = set()
    for path in sorted(_TESTS_ROOT.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        for match in _TEST_MARKER_LINE_RE.finditer(text):
            markers.add(match.group(1))
    return markers


class TestValCitationObligations(unittest.TestCase):
    def test_every_finding_emitting_function_has_citation_and_reference_value_lines(self):
        functions = _functions_emitting_findings()
        self.assertTrue(functions, "no function in dsx/frame/val.py calls report.add(...)")
        for name, doc in sorted(functions.items()):
            with self.subTest(function=name):
                self.assertRegex(
                    doc, _CITATION_LINE_RE,
                    f"{name}'s docstring has no 'Citation:' line with non-whitespace after "
                    "the colon",
                )
                self.assertRegex(
                    doc, _REFVALUE_LINE_RE,
                    f"{name}'s docstring has no 'Reference value:'/'Structural criterion:' "
                    "line with non-whitespace after the colon",
                )

    def test_every_emitted_code_has_a_test_marker_under_tests(self):
        emitted = _codes_emitted_by_val_module()
        self.assertTrue(emitted, "dsx/frame/val.py emits no DSX-VAL-* code")
        markers = _test_markers_under_tests_root()
        missing = emitted - markers
        self.assertEqual(
            missing, set(),
            f"code(s) with no '# D-05: <CODE>' marker anywhere under {_TESTS_ROOT}: "
            f"{sorted(missing)}",
        )

    def test_every_emitted_code_appears_in_the_rendered_catalogue(self):
        emitted = _codes_emitted_by_val_module()
        self.assertTrue(emitted, "dsx/frame/val.py emits no DSX-VAL-* code")
        catalogue_text = _CATALOGUE_PATH.read_text(encoding="utf-8")
        missing = {code for code in emitted if code not in catalogue_text}
        self.assertEqual(
            missing, set(),
            f"code(s) emitted by dsx/frame/val.py but absent from {_CATALOGUE_PATH}: "
            f"{sorted(missing)} — run scripts/gen-finding-catalogue.py --write",
        )


# ── Kish citation coherence (gap G-07-4, 07-UAT.md test 4, plan 07-08) ──────
#
# A citation may not simultaneously name a section locator for a source and
# also claim that only page-level locators were confirmed for that source —
# that self-contradiction is exactly the defect UAT test 4 found in
# _UNIT_TRIAD_CITATION. Nor may two citation sites for the same source and
# the same result silently disagree about what locators were confirmed, the
# way dsx/frame/val.py and dsx/mathx.py disagreed before this plan. This
# class enforces both, and holds every file the collector below reaches to
# the same locator set — including one that does not exist yet.

_DSX_PACKAGE_DIR = _VAL_MODULE_PATH.parent.parent
_REPO_ROOT = _DSX_PACKAGE_DIR.parent
_BRIEF_MD_PATH = _REPO_ROOT / "brief.md"

# Distinct from an empty frozenset(): "found no locators" and "could not even
# find the Kish clause to look inside" are different failures.
_UNPARSEABLE_KISH_CLAUSE = object()

_KISH_CLAUSE_RE = re.compile(r"Kish.*?Survey Sampling,(.*?);")
_KISH_LOCATOR_RE = re.compile(r"\b(section|sections|page|pages)\s+(\d+(?:\.\d+)?(?:\s*-\s*\d+)?)")

# A family of wordings for one claim — that page-level locators were the
# only ones confirmed for Kish — rather than one exact string, because what
# this forbids is the claim, not the sentence it happens to be written in
# today.
_PAGES_ONLY_KISH_DETECTOR_PATTERNS = (
    # dsx/frame/val.py's _UNIT_TRIAD_CITATION and _check_unit_triad docstring, before this plan
    re.compile(r"only the page numbers", re.IGNORECASE),
    # dsx/mathx.py's design_effect docstring, before this plan
    re.compile(
        r"page numbers[^.;]*were confirmed,[^.]*section number was not", re.IGNORECASE
    ),
    # the generalisation: any future wording of the same claim
    re.compile(r"(?:only|nothing but)(?:\s+the)?\s+pages?[^.;]*confirmed", re.IGNORECASE),
)


def _collect_kish_strings() -> "list[tuple[str, Path, int]]":
    """Every string constant mentioning Kish in every ``*.py`` file beneath
    the ``dsx`` package, collected by walking each file's AST rather than
    its raw text — this catches module constants and docstrings alike, and
    Python has already folded adjacent parenthesised string literals into
    one constant by the time the AST exists, so a citation split across
    several physical lines arrives already joined. Each string is
    normalised by collapsing whitespace runs to a single space, so the
    repository's CRLF checkout and its hard line-wrapping cannot change a
    match. Scoped to the ``dsx`` package and nowhere else — not the
    repository root, not the tests directory, because the detector patterns
    live in this file and a collector reaching the tests directory would
    match its own patterns and fail permanently for the wrong reason."""
    collected: "list[tuple[str, Path, int]]" = []
    for path in sorted(_DSX_PACKAGE_DIR.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
                continue
            if "Kish" not in node.value:
                continue
            normalized = re.sub(r"\s+", " ", node.value).strip()
            collected.append((normalized, path, node.lineno))
    return collected


def _kish_locators(normalized_string: str):
    """The set of ``(kind, number)`` locator pairs (``kind`` one of
    ``"section"``/``"page"``) named inside the Kish clause of a normalised
    citation string, or the ``_UNPARSEABLE_KISH_CLAUSE`` sentinel when the
    clause itself cannot be found — distinct from an empty set, so a future
    citation mentioning Kish in a shape this helper does not understand
    fails loudly instead of silently passing as having no locators. The
    clause is bounded by the work's title and a comma at the start and the
    first semicolon at the end, which is what keeps the Cochrane Handbook's
    own section numbers out of the Kish locator set."""
    match = _KISH_CLAUSE_RE.search(normalized_string)
    if not match:
        return _UNPARSEABLE_KISH_CLAUSE
    clause = match.group(1)
    locators = set()
    for kind, number in _KISH_LOCATOR_RE.findall(clause):
        normalized_kind = "section" if kind.startswith("section") else "page"
        locators.add((normalized_kind, number.replace(" ", "")))
    return frozenset(locators)


class TestKishCitationCoherence(unittest.TestCase):
    """Written against the defect recorded as gap G-07-4 in 07-UAT.md test 4:
    dsx/frame/val.py's Kish citation named section 8.2 as a confirmed locator
    and, one sentence later, claimed only page numbers were confirmed — a
    self-contradiction — and dsx/mathx.py's Kish citation named a different
    locator set for the same source and the same result."""

    def test_no_kish_citation_both_names_a_section_and_claims_pages_only(self):
        collected = _collect_kish_strings()
        self.assertTrue(collected, f"no string mentioning Kish found under {_DSX_PACKAGE_DIR}")
        violations = []
        for text, path, lineno in collected:
            locators = _kish_locators(text)
            if locators is _UNPARSEABLE_KISH_CLAUSE:
                continue
            if not any(kind == "section" for kind, _number in locators):
                continue
            for pattern in _PAGES_ONLY_KISH_DETECTOR_PATTERNS:
                if pattern.search(text):
                    violations.append(
                        f"{path}:{lineno} names a section locator "
                        f"({sorted(locators)}) and also matches the pages-only "
                        f"pattern {pattern.pattern!r}"
                    )
        self.assertEqual(
            violations, [],
            "a Kish citation both names a section locator and claims pages were "
            "the only confirmed locators:\n" + "\n".join(violations),
        )

    def test_every_kish_citation_in_the_dsx_package_names_the_same_locators(self):
        """This is the assertion that would have caught the divergence between
        dsx/frame/val.py and dsx/mathx.py, and it holds for a file that does
        not exist yet — any future ``*.py`` under dsx/ citing Kish for the
        same result must name this same locator set."""
        collected = _collect_kish_strings()
        self.assertTrue(collected, f"no string mentioning Kish found under {_DSX_PACKAGE_DIR}")
        unparseable_sites = []
        groups: "dict[frozenset, list[str]]" = {}
        for text, path, lineno in collected:
            locators = _kish_locators(text)
            site = f"{path}:{lineno}"
            if locators is _UNPARSEABLE_KISH_CLAUSE:
                unparseable_sites.append(site)
                continue
            if not locators:
                continue
            groups.setdefault(locators, []).append(site)
        self.assertEqual(
            unparseable_sites, [],
            f"Kish clause could not be located/parsed at: {unparseable_sites}",
        )
        self.assertEqual(
            len(groups), 1,
            "the dsx package's Kish citations do not all name the same locators:\n"
            + "\n".join(
                f"  {sorted(locator_set)}: {sites}" for locator_set, sites in groups.items()
            ),
        )

    def test_brief_md_citation_ledger_does_not_claim_pages_were_the_only_kish_locators(self):
        text = _BRIEF_MD_PATH.read_text(encoding="utf-8")
        normalized = re.sub(r"\s+", " ", text)
        matched = [
            pattern.pattern
            for pattern in _PAGES_ONLY_KISH_DETECTOR_PATTERNS
            if pattern.search(normalized)
        ]
        self.assertEqual(
            matched, [],
            f"{_BRIEF_MD_PATH} still claims pages were the only confirmed Kish "
            f"locators (matched pattern(s): {matched})",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
