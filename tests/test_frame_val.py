"""Test suite for dsx/frame/val.py — DSX-VAL-010 (estimand completeness) and
DSX-VAL-011 (estimand falsifiability). Stdlib unittest — no pytest dependency.

Run:  python3 -m unittest tests.test_frame_val -v
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dsx.findings import Report, Severity  # noqa: E402
from dsx.frame import val  # noqa: E402


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
    design: "dict | None" = None,
) -> dict:
    """A minimal spec carrying only a units/dependence pair, isolating the
    unit-triad judgment from the estimand judgment (no `estimand` key at all,
    so the estimand decision record does not also append)."""
    spec: dict = {
        "validity_frame": {
            "units": {"observation": observation, "assignment": assignment},
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

    def test_units_judgment_point_appends_exactly_one_decision_record(self):
        report = val.check(
            _units_spec(observation="impression", assignment="user", method_family_required="")
        )
        decisions = report.context.get("decisions") or []
        self.assertEqual(len(decisions), 1)
        self.assertEqual(decisions[0]["layer"], "deterministic")
        self.assertTrue(decisions[0]["counterfactual"].strip())


if __name__ == "__main__":
    unittest.main(verbosity=2)
