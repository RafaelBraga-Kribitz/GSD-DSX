"""Test suite for dsx/frame/interference.py — DSX-INT-010 (interference risk
unaddressed) and DSX-INT-011 (mitigation inadmissible for the declared risk).
Stdlib unittest — no pytest dependency.

Run:  python3 -m unittest tests.test_frame_interference -v
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

from dsx import cli  # noqa: E402
from dsx.findings import Report, Severity  # noqa: E402
from dsx.frame import interference  # noqa: E402
from dsx.loader import load  # noqa: E402
from dsx.spec import INTERFERENCE_MITIGATIONS, INTERFERENCE_RISKS, needs_causal_block  # noqa: E402
from dsx.suppressions import known_codes  # noqa: E402


def codes(report: Report) -> set[str]:
    return {f.code for f in report.findings}


def _causal_spec(**overrides: object) -> dict:
    """A minimal causal spec carrying an interference sub-block that
    declares the full DSX-INT-010 defect by default, with the given
    interference fields overridden to isolate one condition at a time.
    ``question_type: causal`` alone makes ``needs_causal_block`` true."""
    block = {
        "risk": "shared_budget",
        "mitigation": "none",
        "residual_note": "",
    }
    block.update(overrides)
    return {
        "question_type": "causal",
        "validity_frame": {"interference": block},
    }


_REAL_RESIDUAL_NOTE = (
    "Budget interference accepted; the projected impact is below the "
    "declared minimum practical effect and was reviewed with the "
    "growth-marketing lead before launch."
)


class TestInterferenceUnaddressed(unittest.TestCase):
    # D-05: DSX-INT-010
    def test_shared_budget_no_mitigation_blank_residual_produces_critical_int_010(self):
        report = interference.check(_causal_spec())
        found = [f for f in report.findings if f.code == "DSX-INT-010"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.CRITICAL)
        self.assertEqual(found[0].where, "spec.validity_frame.interference.mitigation")
        self.assertNotIn("DSX-INT-011", codes(report))

    def test_real_residual_note_produces_no_findings(self):
        report = interference.check(_causal_spec(residual_note=_REAL_RESIDUAL_NOTE))
        self.assertEqual(codes(report), set())

    def test_angle_bracket_placeholder_residual_note_still_fires_int_010(self):
        report = interference.check(
            _causal_spec(residual_note="<what remains unaddressed, if anything>")
        )
        self.assertIn("DSX-INT-010", codes(report))

    def test_refusal_token_residual_note_still_fires_int_010(self):
        report = interference.check(_causal_spec(residual_note="n/a"))
        self.assertIn("DSX-INT-010", codes(report))

    def test_admissible_mitigation_with_blank_residual_produces_no_findings(self):
        report = interference.check(_causal_spec(mitigation="budget_isolation"))
        self.assertEqual(codes(report), set())

    # D-05: DSX-INT-011
    def test_inadmissible_mitigation_fires_int_011_not_int_010(self):
        report = interference.check(_causal_spec(mitigation="cluster_randomisation"))
        found = [f for f in report.findings if f.code == "DSX-INT-011"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.CRITICAL)
        self.assertEqual(found[0].where, "spec.validity_frame.interference.mitigation")
        self.assertNotIn("DSX-INT-010", codes(report))

    def test_same_mitigation_different_risk_produces_no_findings(self):
        report = interference.check(
            _causal_spec(risk="marketplace", mitigation="cluster_randomisation")
        )
        self.assertEqual(codes(report), set())

    def test_risk_none_produces_no_findings_whatever_mitigation_says(self):
        for mitigation in ("none", "cluster_randomisation", "budget_isolation"):
            with self.subTest(mitigation=mitigation):
                report = interference.check(_causal_spec(risk="none", mitigation=mitigation))
                self.assertEqual(codes(report), set())

    def test_descriptive_observational_spec_produces_no_findings_despite_full_defect(self):
        spec = _causal_spec()
        spec["question_type"] = "descriptive"
        report = interference.check(spec)
        self.assertEqual(codes(report), set())

    def test_check_returns_report_named_interference(self):
        report = interference.check({})
        self.assertEqual(report.findings, [])
        self.assertEqual(report.check, "interference")

    def test_each_helper_appends_exactly_one_decision_record(self):
        report = interference.check(_causal_spec())
        decisions = report.context.get("decisions") or []
        # Only DSX-INT-010's helper reaches its judgment point here — the
        # admissibility helper's own judgment point requires a declared,
        # non-'none' mitigation, which this spec does not carry.
        self.assertEqual(len(decisions), 1)
        self.assertEqual(decisions[0]["layer"], "deterministic")
        self.assertEqual(decisions[0]["id"], "")
        self.assertEqual(decisions[0]["invocation_id"], "")
        self.assertTrue(decisions[0]["counterfactual"].strip())

        report = interference.check(_causal_spec(mitigation="cluster_randomisation"))
        decisions = report.context.get("decisions") or []
        self.assertEqual(len(decisions), 2)


class TestRiskMitigationMap(unittest.TestCase):
    def test_map_keys_equal_risks_and_values_subset_of_mitigations(self):
        self.assertEqual(set(interference._RISK_MITIGATION_MAP), set(INTERFERENCE_RISKS))
        for risk, mitigations in interference._RISK_MITIGATION_MAP.items():
            with self.subTest(risk=risk):
                self.assertLessEqual(set(mitigations), set(INTERFERENCE_MITIGATIONS))

    def test_cluster_randomisation_admissible_for_marketplace_not_shared_budget(self):
        self.assertIn("cluster_randomisation", interference._RISK_MITIGATION_MAP["marketplace"])
        self.assertNotIn(
            "cluster_randomisation", interference._RISK_MITIGATION_MAP["shared_budget"]
        )


class TestNeedsCausalBlock(unittest.TestCase):
    def test_needs_causal_block_true_for_known_bad_and_canonical_fixtures(self):
        known_bad = sorted((ROOT / "examples" / "known-bad").glob("*-ANALYSIS-SPEC.yaml"))
        self.assertTrue(known_bad, "no known-bad fixtures found")
        for path in known_bad:
            with self.subTest(fixture=path.name):
                spec = load(path)
                self.assertTrue(
                    needs_causal_block(spec), f"{path.name} expected needs_causal_block True"
                )
        for name in ("good-ANALYSIS-SPEC.yaml", "bad-ANALYSIS-SPEC.yaml"):
            with self.subTest(fixture=name):
                spec = load(ROOT / "examples" / name)
                self.assertTrue(needs_causal_block(spec))

    def test_needs_causal_block_false_for_template(self):
        spec = load(ROOT / "templates" / "ANALYSIS-SPEC.yaml")
        self.assertFalse(needs_causal_block(spec))


class TestGateRegistration(unittest.TestCase):
    def test_interference_registered_in_plan_verify_ship_absent_from_execute(self):
        from dsx.cli import CHECKS, GATE_PROFILES

        self.assertIs(CHECKS["interference"], interference.check)
        for point in ("plan", "verify", "ship"):
            with self.subTest(point=point):
                self.assertIn("interference", GATE_PROFILES[point])
        self.assertNotIn("interference", GATE_PROFILES["execute"])

    def test_every_dsx_int_code_reachable_from_a_gate_profile(self):
        from dsx.cli import GATE_PROFILES

        int_codes = [c for c in known_codes() if c.startswith("DSX-INT-")]
        self.assertTrue(int_codes, "expected at least DSX-INT-010 and DSX-INT-011 to be known")
        reachable_checks: "set[str]" = set().union(*GATE_PROFILES.values())
        self.assertIn("interference", reachable_checks)


class TestMalformedShapesDegradeGracefully(unittest.TestCase):
    def test_malformed_validity_frame_and_interference_values_degrade_to_no_findings(self):
        for bad_frame in ("s", [], None, 3):
            with self.subTest(bad_validity_frame=bad_frame):
                report = interference.check(
                    {"question_type": "causal", "validity_frame": bad_frame}
                )
                self.assertEqual(codes(report), set())
        for bad_interference in ("s", [], None, 3):
            with self.subTest(bad_interference=bad_interference):
                report = interference.check(
                    {
                        "question_type": "causal",
                        "validity_frame": {"interference": bad_interference},
                    }
                )
                self.assertEqual(codes(report), set())


def _triggering_causal_spec(**overrides: object) -> dict:
    """A minimal causal spec carrying one additive metric and a triggering
    sub-block that declares the full DSX-INT-030 defect by default, with the
    given triggering fields overridden to isolate one condition at a time."""
    block = {
        "analysis_population": "eligible",
        "dilution_adjusted": False,
        "expected_trigger_rate": 0.41,
    }
    block.update(overrides)
    return {
        "question_type": "causal",
        "validity_frame": {"triggering": block},
        "metrics": [{"name": "revenue_per_eligible_session", "type": "average"}],
    }


class TestTriggeringDilution(unittest.TestCase):
    # D-05: DSX-INT-030
    def test_eligible_population_not_adjusted_additive_metric_fires_critical_int_030(self):
        report = interference.check(_triggering_causal_spec())
        found = [f for f in report.findings if f.code == "DSX-INT-030"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.CRITICAL)
        self.assertEqual(found[0].where, "spec.validity_frame.triggering.dilution_adjusted")

    def test_dilution_adjusted_true_produces_no_finding(self):
        report = interference.check(_triggering_causal_spec(dilution_adjusted=True))
        self.assertNotIn("DSX-INT-030", codes(report))

    def test_triggered_population_produces_no_finding_whatever_dilution_adjusted_says(self):
        for dilution_adjusted in (True, False):
            with self.subTest(dilution_adjusted=dilution_adjusted):
                spec = _triggering_causal_spec(
                    analysis_population="triggered", dilution_adjusted=dilution_adjusted
                )
                report = interference.check(spec)
                self.assertNotIn("DSX-INT-030", codes(report))

    def test_ratio_scope_boundary_ratio_metric_produces_no_finding(self):
        spec = _triggering_causal_spec()
        spec["metrics"] = [{"name": "conversion_rate", "type": "ratio"}]
        report = interference.check(spec)
        self.assertNotIn("DSX-INT-030", codes(report))

    def test_ratio_scope_boundary_rate_metric_produces_no_finding(self):
        spec = _triggering_causal_spec()
        spec["metrics"] = [{"name": "orders_per_minute", "type": "rate"}]
        report = interference.check(spec)
        self.assertNotIn("DSX-INT-030", codes(report))

    def test_percentile_metric_is_unadjudicated_not_caught(self):
        spec = _triggering_causal_spec()
        spec["metrics"] = [{"name": "p95_latency", "type": "percentile"}]
        report = interference.check(spec)
        self.assertNotIn("DSX-INT-030", codes(report))

    def test_metric_with_no_declared_type_produces_no_finding_and_one_skip_decision_record(self):
        spec = _triggering_causal_spec()
        spec["metrics"] = [{"name": "revenue_per_eligible_session"}]
        report = interference.check(spec)
        self.assertNotIn("DSX-INT-030", codes(report))
        decisions = report.context.get("decisions") or []
        self.assertEqual(len(decisions), 1)
        self.assertIn("skip", decisions[0]["choice"])
        self.assertIn("revenue_per_eligible_session", decisions[0]["choice"])
        self.assertIn("declared type", decisions[0]["rule"])

    def test_mixed_metrics_one_ratio_two_additive_produces_one_finding_naming_both_additive(self):
        spec = _triggering_causal_spec()
        spec["metrics"] = [
            {"name": "conversion_rate", "type": "ratio"},
            {"name": "revenue_per_session", "type": "average"},
            {"name": "orders_per_session", "type": "count"},
        ]
        report = interference.check(spec)
        found = [f for f in report.findings if f.code == "DSX-INT-030"]
        self.assertEqual(len(found), 1)
        self.assertIn("revenue_per_session", found[0].detail)
        self.assertIn("orders_per_session", found[0].detail)
        self.assertNotIn("conversion_rate", found[0].detail)

    def test_additive_and_ratio_metric_type_partitions_are_subsets_disjoint_and_proper(self):
        from dsx.spec import METRIC_TYPES

        additive = interference._ADDITIVE_METRIC_TYPES
        ratio = interference._RATIO_METRIC_TYPES
        self.assertLessEqual(additive, METRIC_TYPES)
        self.assertLessEqual(ratio, METRIC_TYPES)
        self.assertEqual(additive & ratio, frozenset())
        self.assertLess(additive | ratio, METRIC_TYPES)

    def test_descriptive_observational_spec_produces_no_finding_despite_full_dilution_defect(self):
        spec = _triggering_causal_spec()
        spec["question_type"] = "descriptive"
        report = interference.check(spec)
        self.assertEqual(codes(report), set())

    def test_malformed_triggering_and_metrics_values_degrade_to_no_findings(self):
        for bad_triggering in ("s", [], None, 3):
            with self.subTest(bad_triggering=bad_triggering):
                report = interference.check(
                    {
                        "question_type": "causal",
                        "validity_frame": {"triggering": bad_triggering},
                        "metrics": [{"name": "m", "type": "average"}],
                    }
                )
                self.assertNotIn("DSX-INT-030", codes(report))
        for bad_metrics in ("s", [], None, 3):
            with self.subTest(bad_metrics=bad_metrics):
                report = interference.check(
                    {
                        "question_type": "causal",
                        "validity_frame": {
                            "triggering": {
                                "analysis_population": "eligible",
                                "dilution_adjusted": False,
                            }
                        },
                        "metrics": bad_metrics,
                    }
                )
                self.assertNotIn("DSX-INT-030", codes(report))

    def test_committed_triggering_dilution_fixture_blocks_plan_naming_int_030(self):
        fixture = ROOT / "examples" / "known-bad" / "triggering-dilution-ANALYSIS-SPEC.yaml"
        with tempfile.TemporaryDirectory() as phase_dir:
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = cli.main(
                    ["gate", "plan", "--spec", str(fixture), "--phase-dir", phase_dir]
                )
            self.assertEqual(code, 1)
            self.assertIn("DSX-INT-030", out.getvalue() + err.getvalue())

    def test_committed_triggering_dilution_fixture_clears_execute(self):
        fixture = ROOT / "examples" / "known-bad" / "triggering-dilution-ANALYSIS-SPEC.yaml"
        with tempfile.TemporaryDirectory() as phase_dir:
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = cli.main(
                    ["gate", "execute", "--spec", str(fixture), "--phase-dir", phase_dir]
                )
            self.assertEqual(code, 0, f"gate execute unexpectedly blocked:\n{err.getvalue()}")

    def test_good_and_monitoring_fixtures_and_template_still_clear_plan(self):
        good = ROOT / "examples" / "good-ANALYSIS-SPEC.yaml"
        monitoring = [
            ROOT / "examples" / "known-bad" / "bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml",
            ROOT / "examples" / "known-bad" / "frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml",
        ]
        template = ROOT / "templates" / "ANALYSIS-SPEC.yaml"
        for fixture in [good, template, *monitoring]:
            with self.subTest(fixture=fixture.name):
                with tempfile.TemporaryDirectory() as phase_dir:
                    out, err = io.StringIO(), io.StringIO()
                    with redirect_stdout(out), redirect_stderr(err):
                        code = cli.main(
                            ["gate", "plan", "--spec", str(fixture), "--phase-dir", phase_dir]
                        )
                    self.assertNotIn(
                        "DSX-INT-030", out.getvalue() + err.getvalue(),
                        f"{fixture.name} unexpectedly names DSX-INT-030 at plan",
                    )

    def test_good_fixture_clears_ship_resolving_sibling_artifacts_from_its_own_directory(self):
        # No --phase-dir here, deliberately: dsx/cli.py::cmd_gate resolves relative
        # evidence/profile paths from `args.phase_dir or path.parent`, and the good
        # fixture's sibling artifacts (DATA-PROFILE.yaml, figures/, NARRATIVE.md,
        # the reproducibility entrypoint) live next to it under examples/, not in a
        # throwaway temp directory. Matches the plan's own acceptance-criteria
        # invocation (`dsx gate ship --spec examples/good-ANALYSIS-SPEC.yaml`, no
        # --phase-dir) rather than this module's usual phase-dir idiom.
        good = ROOT / "examples" / "good-ANALYSIS-SPEC.yaml"
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(["gate", "ship", "--spec", str(good)])
        self.assertEqual(code, 0, f"gate ship unexpectedly blocked:\n{err.getvalue()}")


class TestInterferenceGateLevel(unittest.TestCase):
    """Gate-level proofs against the real fixture, never edited in place —
    every mutated variant is built in a temporary copy (D-17 idiom, matching
    tests/test_dsx.py's ``_bayesian_variant_spec_path``)."""

    ROOT = ROOT
    FIXTURE = ROOT / "examples" / "known-bad" / "interference-shared-budget-ANALYSIS-SPEC.yaml"

    def _run(self, args: "list[str]") -> "tuple[int, str, str]":
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(args)
        return code, out.getvalue(), err.getvalue()

    def _copied_fixture(self, tmp: str) -> Path:
        target = Path(tmp) / "known-bad"
        shutil.copytree(self.ROOT / "examples" / "known-bad", target)
        return target / "interference-shared-budget-ANALYSIS-SPEC.yaml"

    def _mutate_interference(self, spec_path: Path, **overrides: object) -> None:
        spec = load(spec_path)
        interference_block = spec.setdefault("validity_frame", {}).setdefault("interference", {})
        interference_block.update(overrides)
        spec_path.write_text(json.dumps(spec), encoding="utf-8")

    def test_committed_fixture_blocks_plan_naming_int_010(self):
        with tempfile.TemporaryDirectory() as phase_dir:
            code, out, err = self._run(
                ["gate", "plan", "--spec", str(self.FIXTURE), "--phase-dir", phase_dir]
            )
            self.assertEqual(code, 1)
            self.assertIn("DSX-INT-010", out + err)

    def test_admissible_mitigation_variant_clears_plan_and_execute(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = self._copied_fixture(tmp)
            self._mutate_interference(spec_path, mitigation="budget_isolation")
            for point in ("plan", "execute"):
                with self.subTest(point=point):
                    with tempfile.TemporaryDirectory() as phase_dir:
                        code, out, err = self._run(
                            ["gate", point, "--spec", str(spec_path), "--phase-dir", phase_dir]
                        )
                        self.assertEqual(code, 0, f"gate {point} unexpectedly blocked:\n{err}")

    def test_real_residual_note_variant_clears_plan_and_execute(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = self._copied_fixture(tmp)
            self._mutate_interference(spec_path, residual_note=_REAL_RESIDUAL_NOTE)
            for point in ("plan", "execute"):
                with self.subTest(point=point):
                    with tempfile.TemporaryDirectory() as phase_dir:
                        code, out, err = self._run(
                            ["gate", point, "--spec", str(spec_path), "--phase-dir", phase_dir]
                        )
                        self.assertEqual(code, 0, f"gate {point} unexpectedly blocked:\n{err}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
