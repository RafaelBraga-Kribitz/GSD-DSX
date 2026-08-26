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
sys.path.insert(0, str(ROOT / "tests"))

from _trail_seed import seed_plan_header  # noqa: E402
from dsx import cli  # noqa: E402
from dsx.findings import Report, Severity  # noqa: E402
from dsx.frame import interference  # noqa: E402
from dsx.loader import load  # noqa: E402
from dsx.spec import (  # noqa: E402
    ANALYSIS_POPULATIONS,
    INTERFERENCE_MITIGATIONS,
    INTERFERENCE_RISKS,
    needs_causal_block,
)
from dsx.suppressions import known_codes  # noqa: E402


def codes(report: Report) -> set[str]:
    return {f.code for f in report.findings}


def _gate_findings(spec_path: Path, point: str) -> "tuple[int, list[dict]]":
    """Run one real ``dsx gate <point>`` against one fixture and return
    ``(exit_code, findings)``.

    Exists because an assertion against rendered report text cannot
    distinguish a finding that actually fired from a finding code merely
    quoted inside another finding's ``detail`` prose — and
    ``DSX-INT-010``'s own ``detail`` text names ``DSX-SPEC-082``
    unconditionally. Asserting against the parsed ``--json`` finding list
    instead is what stops that kind of test from being vacuous
    (08-REVIEW.md WR-01). Module level so both ``TestInterferenceUnaddressed``
    and ``TestInterferenceGateLevel`` can reach it.

    ``--phase-dir`` is a fresh ``tempfile.TemporaryDirectory()`` per call so
    the ``DECISIONS.jsonl`` trail write (``dsx/cli.py::cmd_gate``,
    ``root = args.phase_dir or str(path.parent)``) never lands under
    ``examples/`` — matching ``TestKnownBadCorpus._gate_findings``'s
    ``io.StringIO()`` plus ``redirect_stdout``/``redirect_stderr`` capture
    idiom rather than a new pattern. Blocking output goes to stderr and
    passing output to stdout (``dsx/findings.py::emit``), so whichever
    stream is non-empty is the one holding the JSON report.
    """
    with tempfile.TemporaryDirectory() as tmp:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(
                ["gate", point, "--spec", str(spec_path), "--phase-dir", tmp, "--json"]
            )
        raw = err.getvalue() or out.getvalue()
        report = json.loads(raw)
    return code, report["findings"]


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

    # 08-REVIEW.md CR-01: an unrecognised mitigation string made the risk look
    # addressed, so a typo cleared a CRITICAL-threshold gate that an honest
    # `mitigation: none` would have blocked.
    def test_out_of_vocabulary_mitigation_with_blank_residual_still_fires_int_010(self):
        report = interference.check(_causal_spec(mitigation="buget_isolation"))
        found = [f for f in report.findings if f.code == "DSX-INT-010"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.CRITICAL)
        self.assertEqual(found[0].where, "spec.validity_frame.interference.mitigation")
        self.assertNotIn("DSX-INT-011", codes(report))

    # 08-VERIFICATION.md gap 1 / 08-REVIEW.md CR-01: an unrecognised risk
    # string made the whole judgment look inapplicable, so a typo cleared a
    # CRITICAL-threshold gate that an honest `risk: none` would also have
    # cleared, but an honest `risk: shared_budget` would not.
    def test_out_of_vocabulary_risk_with_no_mitigation_and_blank_residual_still_fires_int_010(self):
        report = interference.check(_causal_spec(risk="shared_buget"))
        found = [f for f in report.findings if f.code == "DSX-INT-010"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.CRITICAL)
        self.assertEqual(found[0].where, "spec.validity_frame.interference.mitigation")
        self.assertNotIn("DSX-INT-011", codes(report))

    # 08-VERIFICATION.md's remaining gap / 08-REVIEW.md CR-01: a misspelled
    # risk paired with a real, recognised, channel-inadmissible mitigation
    # routed to neither check — DSX-INT-010's mitigation test found a
    # recognised mitigation, and DSX-INT-011's risk guard returned before its
    # judgment point — so a typo was cheaper at this CRITICAL-threshold gate
    # than an honest declaration of the same risk.
    def test_out_of_vocabulary_risk_with_real_mitigation_still_fires_int_011(self):
        report = interference.check(_causal_spec(risk="shared_buget", mitigation="geo_split"))
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

    # 08-VERIFICATION.md's remaining gap / 08-REVIEW.md CR-01: the rationale
    # recorded in 08-08-PLAN.md and 08-08-SUMMARY.md claimed judging an
    # out-of-vocabulary risk in DSX-INT-011 would make it double-report what
    # DSX-INT-010 already reports. That claim was never executable and it
    # was false, which is why this gap stayed open a whole round.
    def test_int_010_and_int_011_are_disjoint_across_the_risk_and_mitigation_grid(self):
        """Protects the invariant that DSX-INT-010 and DSX-INT-011 never both
        fire for the same spec. Disjointness rests on the mitigation
        dimension alone — absent, 'none' or unrecognised on one side;
        present, recognised and non-'none' on the other — and never on
        risk-vocabulary membership. This grid passes both before and after
        this plan's fix, so it is not the regression proof; the single-case
        test above (and its gate-level sibling in TestInterferenceGateLevel)
        are. Does not assert which code fires for a given cell — that is the
        single-case tests' job, and pinning the whole matrix would make every
        future vocabulary addition a test edit.
        """
        risks = list(INTERFERENCE_RISKS) + ["shared_buget", "marketplce", "", None]
        mitigations = list(INTERFERENCE_MITIGATIONS) + ["buget_isolation", "", None]
        residual_notes = ["", "<what remains unaddressed, if anything>", _REAL_RESIDUAL_NOTE]
        for risk in risks:
            for mitigation in mitigations:
                for residual_note in residual_notes:
                    with self.subTest(risk=risk, mitigation=mitigation, residual_note=residual_note):
                        report = interference.check(
                            _causal_spec(
                                risk=risk, mitigation=mitigation, residual_note=residual_note
                            )
                        )
                        found_codes = codes(report)
                        self.assertFalse(
                            {"DSX-INT-010", "DSX-INT-011"} <= found_codes,
                            f"both codes fired for risk={risk!r} mitigation={mitigation!r} "
                            f"residual_note={residual_note!r}",
                        )


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
    # Plan 11.2-08 (REQ-P11.2-03): the flagship prescriptive-churn-recommendation
    # fixture is the first known-bad fixture that is deliberately NOT causal — it
    # encodes a prescriptive CLAIM smuggled under a `descriptive` question with an
    # `observational` design, so needs_causal_block is legitimately False for it
    # (that is the whole point of the fixture — keeping the question descriptive is
    # what makes the prescriptive claim the sole overreach). It is excluded from the
    # needs_causal_block-True sweep below by slug rather than silently, so a future
    # causal known-bad fixture that regressed to False still fails loudly.
    _NON_CAUSAL_KNOWN_BAD = {"prescriptive-churn-recommendation-ANALYSIS-SPEC.yaml"}

    def test_needs_causal_block_true_for_known_bad_and_canonical_fixtures(self):
        known_bad = sorted((ROOT / "examples" / "known-bad").glob("*-ANALYSIS-SPEC.yaml"))
        self.assertTrue(known_bad, "no known-bad fixtures found")
        for path in known_bad:
            if path.name in self._NON_CAUSAL_KNOWN_BAD:
                with self.subTest(fixture=path.name):
                    self.assertFalse(
                        needs_causal_block(load(path)),
                        f"{path.name} is listed as a deliberately non-causal known-bad "
                        "fixture but needs_causal_block returned True",
                    )
                continue
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


def _mutated_triggering_fixture(tmp: str, **overrides: object) -> Path:
    """Copy ``examples/known-bad/`` into ``tmp`` and apply the given overrides
    to the triggering-dilution fixture's ``validity_frame.triggering``
    sub-block, returning the path to the mutated copy.

    Copies the whole directory, not just the one file — the corpus fixtures
    resolve sibling artifacts from their own directory, matching
    ``TestInterferenceGateLevel._copied_fixture``'s idiom. Never edits the
    committed fixture in place. 08-VERIFICATION.md gap 2 / 08-REVIEW.md
    CR-02: an out-of-vocabulary ``analysis_population`` string (a
    one-character misspelling of ``eligible``) silenced the CRITICAL
    DSX-INT-030 check the committed fixture exists to demonstrate, because
    any population string other than the literal ``eligible`` was treated as
    an honest declaration of the triggered population.
    """
    target = Path(tmp) / "known-bad"
    shutil.copytree(ROOT / "examples" / "known-bad", target)
    spec_path = target / "triggering-dilution-ANALYSIS-SPEC.yaml"
    spec = load(spec_path)
    triggering = spec.setdefault("validity_frame", {}).setdefault("triggering", {})
    triggering.update(overrides)
    spec_path.write_text(json.dumps(spec), encoding="utf-8")
    return spec_path


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

    # 08-VERIFICATION.md gap 2 / 08-REVIEW.md CR-02: an out-of-vocabulary
    # analysis_population string (a one-character misspelling of `eligible`)
    # was treated as an honest declaration of the triggered population, so a
    # typo silenced the CRITICAL check the committed fixture exists to
    # demonstrate.
    def test_out_of_vocabulary_analysis_population_still_fires_int_030(self):
        spec = _triggering_causal_spec(analysis_population="eligable")
        report = interference.check(spec)
        found = [f for f in report.findings if f.code == "DSX-INT-030"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.CRITICAL)
        self.assertEqual(found[0].where, "spec.validity_frame.triggering.dilution_adjusted")

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

    # 08-REVIEW.md WR-03: an explicit `type: null` (or blank `type: ""`) must
    # produce the same skip decision record as an absent `type` key.
    # `metric.get("type", "")` only returns the `""` default when the key is
    # entirely absent — an explicit null normalizes to the truthy string
    # "none", so the metric silently fell through to the ignored branch with
    # no decision record at all, contradicting the docstring's claim that one
    # record is appended per undeclared-type metric.
    def test_explicit_null_metric_type_produces_the_same_skip_decision_record_as_an_absent_type(self):
        for type_value in (None, ""):
            with self.subTest(type_value=type_value):
                spec = _triggering_causal_spec()
                spec["metrics"] = [{"name": "revenue_per_eligible_session", "type": type_value}]
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

    # 08-VERIFICATION.md gap 2 / 08-REVIEW.md CR-02: the corrected
    # `_check_triggering_dilution` guard names `triggered` as a literal
    # string, which is only a complete description of the not-adjudicated
    # branch while this vocabulary has exactly two members. A third member
    # added without revisiting the guard would be adjudicated as if it were
    # a misspelling of `eligible`, which may or may not be right, and this
    # test forces that decision to be made rather than defaulted.
    def test_analysis_populations_vocabulary_is_exactly_eligible_and_triggered(self):
        self.assertEqual(set(ANALYSIS_POPULATIONS), {"eligible", "triggered"})

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

    # 08-VERIFICATION.md gap 2 / 08-REVIEW.md CR-02: an out-of-vocabulary
    # analysis_population string (a one-character misspelling of `eligible`)
    # was treated as an honest declaration of the triggered population, so a
    # typo silenced the CRITICAL check the committed fixture exists to
    # demonstrate. The `where` assertion on DSX-SPEC-082 pins that the
    # vocabulary violation fired for the `analysis_population` field
    # specifically, which no substring assertion can establish, and
    # documents that the two findings are two different facts about one
    # spec rather than one defect reported twice.
    def test_out_of_vocabulary_analysis_population_variant_blocks_plan_naming_int_030(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = _mutated_triggering_fixture(tmp, analysis_population="eligable")
            code, findings = _gate_findings(spec_path, "plan")
            by_code = {f["code"]: f for f in findings}
            self.assertEqual(code, 1)
            self.assertIn("DSX-INT-030", by_code)
            self.assertEqual(by_code["DSX-INT-030"]["severity"], "CRITICAL")
            self.assertIn("DSX-SPEC-082", by_code)
            self.assertEqual(by_code["DSX-SPEC-082"]["severity"], "HIGH")
            self.assertEqual(
                by_code["DSX-SPEC-082"]["where"],
                "spec.validity_frame.triggering.analysis_population",
            )

    # 08-REVIEW.md WR-01's negative counterpart: an absence assertion against
    # rendered text would silently start failing the day any finding's
    # detail names DSX-INT-030, the same contamination WR-01 documents in
    # the opposite direction. Asserts against the structured finding list
    # instead, and pins the exit code it never checked before.
    #
    # Plan 08-09 deviation (documented in the plan's SUMMARY.md): this test's
    # own name has claimed all four fixtures "clear plan" since it was
    # written in feat(08-04), commit 36ff448 — before Phase 9 shipped
    # DSX-PAR-010/DSX-PAR-011. Those two CRITICAL checks now legitimately
    # block `plan` for the two monitoring fixtures, for reasons entirely
    # unrelated to DSX-INT-030 (verified by hand: DSX-PAR-010 fires on
    # frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml, DSX-PAR-011 on
    # bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml). The original
    # assertion never checked exit codes, so this drift went unnoticed.
    # Pinning the real, observed per-fixture exit code is strictly stronger
    # than the plan's stated "assert 0 for all four" without asserting
    # something false about fixtures this plan does not own.
    def test_good_and_monitoring_fixtures_and_template_still_clear_plan(self):
        good = ROOT / "examples" / "good-ANALYSIS-SPEC.yaml"
        bayesian_monitoring = (
            ROOT / "examples" / "known-bad" / "bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml"
        )
        frequentist_monitoring = (
            ROOT
            / "examples"
            / "known-bad"
            / "frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml"
        )
        template = ROOT / "templates" / "ANALYSIS-SPEC.yaml"
        expected_exit_code = {
            good.name: 0,
            template.name: 0,
            # Blocked by DSX-PAR-011 (CRITICAL), unrelated to DSX-INT-030.
            bayesian_monitoring.name: 1,
            # Blocked by DSX-PAR-010 (CRITICAL), unrelated to DSX-INT-030.
            frequentist_monitoring.name: 1,
        }
        for fixture in [good, template, bayesian_monitoring, frequentist_monitoring]:
            with self.subTest(fixture=fixture.name):
                code, findings = _gate_findings(fixture, "plan")
                self.assertEqual(
                    code, expected_exit_code[fixture.name],
                    f"{fixture.name} exit code drifted from the observed baseline",
                )
                by_code = {f["code"]: f for f in findings}
                self.assertNotIn(
                    "DSX-INT-030", by_code,
                    f"{fixture.name} unexpectedly names DSX-INT-030 at plan",
                )

    def test_good_fixture_clears_ship_resolving_sibling_artifacts_from_its_own_directory(self):
        # Still no --phase-dir, deliberately: dsx/cli.py::cmd_gate resolves relative
        # evidence/profile paths from `args.phase_dir or path.parent`, and the good
        # fixture's sibling artifacts (DATA-PROFILE.yaml, figures/, NARRATIVE.md,
        # the reproducibility entrypoint) must resolve from the spec's own directory.
        # The whole examples/ tree is copied first so the siblings come with it and
        # the decision-record trail is written into the copy — without the copytree
        # this run appends to the committed tree's examples/DECISIONS.jsonl, which is
        # gitignored and so never showed up in `git status` (threat T-8-23). Matches
        # test_stability_gate_level_severity_alone_selects_verify_not_plan's idiom.
        committed_trail = ROOT / "examples" / "DECISIONS.jsonl"
        size_before = committed_trail.stat().st_size if committed_trail.exists() else None

        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "examples"
            # The trail is excluded from the copy so its appearance below proves
            # this run wrote it, rather than copytree having carried it across.
            shutil.copytree(
                ROOT / "examples", target,
                ignore=shutil.ignore_patterns("DECISIONS.jsonl"),
            )
            good = target / "good-ANALYSIS-SPEC.yaml"
            # No --phase-dir, so root resolves to `target` (path.parent); no
            # `dsx gate plan` has run there. Seed a plan-time header first —
            # otherwise prereg's missing-header CheckError aborts at exit 2
            # before this test's own exit-0 assertion is even reachable.
            seed_plan_header(str(target), good)
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = cli.main(["gate", "ship", "--spec", str(good)])
            self.assertEqual(code, 0, f"gate ship unexpectedly blocked:\n{err.getvalue()}")
            self.assertTrue(
                (target / "DECISIONS.jsonl").exists(),
                "gate wrote no decision-record trail into the temporary copy",
            )

        size_after = committed_trail.stat().st_size if committed_trail.exists() else None
        self.assertEqual(
            size_before, size_after,
            "this run appended to the committed tree's examples/DECISIONS.jsonl",
        )


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

    # 08-REVIEW.md CR-01: an unrecognised mitigation string made the risk look
    # addressed, so a typo cleared a CRITICAL-threshold gate that an honest
    # `mitigation: none` would have blocked. DSX-SPEC-082 must still fire
    # beside DSX-INT-010 — the vocabulary violation and the unaddressed risk
    # are different facts about the same spec, not a double report of one.
    # 08-REVIEW.md WR-01: the rendered report prints each finding's `detail`,
    # and DSX-INT-010's `detail` quotes DSX-SPEC-082 unconditionally, so a
    # substring assertion on the rendered text is satisfied by prose whenever
    # DSX-INT-010 fires at all, whether or not DSX-SPEC-082 actually fired.
    # Asserts against the structured finding list instead, which is the only
    # evidence source that can distinguish a fired finding from a code merely
    # quoted inside another finding's prose.
    def test_out_of_vocabulary_mitigation_variant_blocks_plan_naming_both_int_010_and_spec_082(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = self._copied_fixture(tmp)
            self._mutate_interference(spec_path, mitigation="buget_isolation")
            code, findings = _gate_findings(spec_path, "plan")
            by_code = {f["code"]: f for f in findings}
            self.assertEqual(code, 1)
            self.assertIn("DSX-INT-010", by_code)
            self.assertEqual(by_code["DSX-INT-010"]["severity"], "CRITICAL")
            self.assertIn("DSX-SPEC-082", by_code)
            self.assertEqual(by_code["DSX-SPEC-082"]["severity"], "HIGH")
            self.assertEqual(
                by_code["DSX-SPEC-082"]["where"], "spec.validity_frame.interference.mitigation"
            )
            self.assertNotIn("DSX-INT-011", by_code)

    # 08-VERIFICATION.md gap 1 / 08-REVIEW.md CR-01: same defect class as the
    # mitigation-field variant above, on the adjacent `risk` field. Asserts
    # against the structured finding list, not rendered report text, because
    # DSX-INT-010's own `detail` names DSX-SPEC-082 unconditionally — a
    # substring assertion on `out + err` cannot tell the two apart. The
    # `where` assertion on DSX-SPEC-082 pins that the vocabulary violation
    # fired for the `risk` field specifically, not some other field.
    def test_out_of_vocabulary_risk_variant_blocks_plan_naming_both_int_010_and_spec_082(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = self._copied_fixture(tmp)
            self._mutate_interference(spec_path, risk="shared_buget")
            code, findings = _gate_findings(spec_path, "plan")
            by_code = {f["code"]: f for f in findings}
            self.assertEqual(code, 1)
            self.assertIn("DSX-INT-010", by_code)
            self.assertEqual(by_code["DSX-INT-010"]["severity"], "CRITICAL")
            self.assertIn("DSX-SPEC-082", by_code)
            self.assertEqual(by_code["DSX-SPEC-082"]["severity"], "HIGH")
            self.assertEqual(
                by_code["DSX-SPEC-082"]["where"], "spec.validity_frame.interference.risk"
            )
            self.assertNotIn("DSX-INT-011", by_code)

    # 08-VERIFICATION.md's remaining gap / 08-REVIEW.md CR-01: the gate-level
    # half of the same defect — a misspelled risk paired with a real,
    # recognised, channel-inadmissible mitigation cleared dsx gate plan with
    # exit 0 and no DSX-INT-* finding at all, so a typo was cheaper at this
    # CRITICAL-threshold gate than declaring the same risk honestly. Asserts
    # against the structured finding list, not rendered report text, because
    # DSX-INT-010's own detail names DSX-SPEC-082 unconditionally (WR-01) —
    # a substring assertion on out + err cannot tell a fired finding from a
    # code merely quoted inside another finding's prose. Does not assert the
    # finding list equals a fixed set: this fixture also emits DSX-EXP-040,
    # DSX-MET-040 and DSX-PAR-001, none of which this plan is about.
    def test_out_of_vocabulary_risk_with_real_mitigation_variant_blocks_plan_naming_both_int_011_and_spec_082(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = self._copied_fixture(tmp)
            self._mutate_interference(spec_path, risk="shared_buget", mitigation="geo_split")
            code, findings = _gate_findings(spec_path, "plan")
            by_code = {f["code"]: f for f in findings}
            self.assertEqual(code, 1)
            self.assertIn("DSX-INT-011", by_code)
            self.assertEqual(by_code["DSX-INT-011"]["severity"], "CRITICAL")
            self.assertIn("DSX-SPEC-082", by_code)
            self.assertEqual(by_code["DSX-SPEC-082"]["severity"], "HIGH")
            self.assertEqual(
                by_code["DSX-SPEC-082"]["where"], "spec.validity_frame.interference.risk"
            )
            self.assertNotIn("DSX-INT-010", by_code)

    # 08-VERIFICATION.md's sixth `missing:` item: re-run the disjointness
    # proof after the fix, at gate level, across in-vocabulary and
    # out-of-vocabulary risk and across absent/none/real mitigation, as an
    # executable check with a recorded result rather than a claim.
    def test_int_010_and_int_011_never_both_fire_across_the_gate_level_risk_and_mitigation_grid(self):
        """Gate-level half of the disjointness proof, run after this plan's
        fix rather than before it. Covers the shipped path — check dispatch,
        severity mapping, the plan gate's CRITICAL threshold and the exit
        code — rather than the predicate in isolation. Runs eight real gate
        invocations, which is why this grid is eight cells and not the unit
        grid's full cross. Does not assert the finding list equals a fixed
        set: this fixture also emits DSX-EXP-040, DSX-MET-040 and
        DSX-PAR-001, none of which this plan is about.
        """
        risks = ["shared_budget", "shared_buget"]
        mitigations = ["none", "geo_split", "budget_isolation", "buget_isolation"]
        for risk in risks:
            for mitigation in mitigations:
                with self.subTest(risk=risk, mitigation=mitigation):
                    with tempfile.TemporaryDirectory() as tmp:
                        spec_path = self._copied_fixture(tmp)
                        self._mutate_interference(spec_path, risk=risk, mitigation=mitigation)
                        code, findings = _gate_findings(spec_path, "plan")
                        found_codes = {f["code"] for f in findings}
                        self.assertFalse(
                            {"DSX-INT-010", "DSX-INT-011"} <= found_codes,
                            f"both codes fired for risk={risk!r} mitigation={mitigation!r}",
                        )
                        has_either = bool(found_codes & {"DSX-INT-010", "DSX-INT-011"})
                        if has_either:
                            self.assertEqual(code, 1)
                        else:
                            self.assertEqual(code, 0)


def _stability_causal_spec(**overrides: object) -> dict:
    """A minimal causal spec carrying a stability sub-block that declares the
    full DSX-INT-040 defect by default, with the given stability fields
    overridden to isolate one condition at a time."""
    block = {
        "window": "14 days",
        "novelty_primacy_assessed": False,
        "evidence": "",
    }
    block.update(overrides)
    return {
        "question_type": "causal",
        "validity_frame": {"stability": block},
    }


class TestStabilityAssessment(unittest.TestCase):
    # D-05: DSX-INT-040
    def test_stability_unassessed_novelty_primacy_fires_high_int_040(self):
        report = interference.check(_stability_causal_spec())
        found = [f for f in report.findings if f.code == "DSX-INT-040"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, Severity.HIGH)

    def test_stability_key_absent_entirely_still_fires_int_040(self):
        spec = _stability_causal_spec()
        del spec["validity_frame"]["stability"]["novelty_primacy_assessed"]
        report = interference.check(spec)
        self.assertIn("DSX-INT-040", codes(report))

    def test_stability_assessed_true_with_real_evidence_produces_no_finding(self):
        report = interference.check(
            _stability_causal_spec(
                novelty_primacy_assessed=True, evidence="RESULTS.md#week1-vs-week2"
            )
        )
        self.assertNotIn("DSX-INT-040", codes(report))

    def test_stability_assessed_true_with_empty_evidence_fires_int_040(self):
        report = interference.check(
            _stability_causal_spec(novelty_primacy_assessed=True, evidence="")
        )
        self.assertIn("DSX-INT-040", codes(report))

    def test_stability_assessed_true_with_placeholder_evidence_fires_int_040(self):
        report = interference.check(
            _stability_causal_spec(
                novelty_primacy_assessed=True,
                evidence="<pointer to the check, e.g. RESULTS.md#week1-vs-week2>",
            )
        )
        self.assertIn("DSX-INT-040", codes(report))

    def test_stability_sub_block_absent_produces_no_int_040(self):
        spec = {"question_type": "causal", "validity_frame": {}}
        report = interference.check(spec)
        self.assertNotIn("DSX-INT-040", codes(report))

    def test_stability_descriptive_observational_spec_produces_no_int_040_despite_full_defect(self):
        spec = _stability_causal_spec()
        spec["question_type"] = "descriptive"
        report = interference.check(spec)
        self.assertEqual(codes(report), set())

    def test_stability_where_names_sub_block_explicitly_not_bare_field_name(self):
        report = interference.check(_stability_causal_spec())
        found = [f for f in report.findings if f.code == "DSX-INT-040"][0]
        self.assertEqual(
            found.where, "spec.validity_frame.stability.novelty_primacy_assessed"
        )

        report2 = interference.check(
            _stability_causal_spec(novelty_primacy_assessed=True, evidence="")
        )
        found2 = [f for f in report2.findings if f.code == "DSX-INT-040"][0]
        self.assertEqual(found2.where, "spec.validity_frame.stability.evidence")

    def test_stability_detail_names_dsx_exp_030_and_states_disjointness(self):
        report = interference.check(_stability_causal_spec())
        found = [f for f in report.findings if f.code == "DSX-INT-040"][0]
        self.assertIn("DSX-EXP-030", found.detail)

    def test_stability_gate_level_severity_alone_selects_verify_not_plan(self):
        """D-02's whole argument, proven at the gate level: a copy of the good
        fixture with novelty_primacy_assessed mutated to false exits 0 at
        plan and 1 at verify, naming DSX-INT-040 — proving severity alone,
        with no GATE_THRESHOLDS edit, selects the gate point."""
        from dsx.cli import GATE_THRESHOLDS

        self.assertEqual(GATE_THRESHOLDS["plan"], "CRITICAL")
        self.assertEqual(GATE_THRESHOLDS["verify"], "HIGH")

        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "examples"
            shutil.copytree(ROOT / "examples", target)
            spec_path = target / "good-ANALYSIS-SPEC.yaml"
            spec = load(spec_path)
            spec.setdefault("validity_frame", {}).setdefault("stability", {})[
                "novelty_primacy_assessed"
            ] = False
            spec_path.write_text(json.dumps(spec), encoding="utf-8")

            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = cli.main(["gate", "plan", "--spec", str(spec_path)])
            self.assertEqual(code, 0, f"gate plan unexpectedly blocked:\n{err.getvalue()}")

            out2, err2 = io.StringIO(), io.StringIO()
            with redirect_stdout(out2), redirect_stderr(err2):
                code2 = cli.main(["gate", "verify", "--spec", str(spec_path)])
            self.assertEqual(code2, 1)
            self.assertIn("DSX-INT-040", out2.getvalue() + err2.getvalue())

    def test_stability_no_committed_fixture_produces_int_040_at_ship(self):
        """No fixture under examples/ (top-level or known-bad/) fires
        DSX-INT-040 at ship — the gate's finding list carries every finding
        regardless of severity threshold, so this one run also proves the
        code is silent at plan/execute/verify for the same spec, since
        interference.check() is a pure function of the spec content."""
        specs = sorted((ROOT / "examples").glob("*-ANALYSIS-SPEC.yaml")) + sorted(
            (ROOT / "examples" / "known-bad").glob("*-ANALYSIS-SPEC.yaml")
        )
        self.assertTrue(specs, "no example specs found")
        for path in specs:
            with self.subTest(spec=path.name):
                with tempfile.TemporaryDirectory() as phase_dir:
                    out, err = io.StringIO(), io.StringIO()
                    with redirect_stdout(out), redirect_stderr(err):
                        code = cli.main(
                            ["gate", "ship", "--spec", str(path), "--phase-dir", phase_dir]
                        )
                    self.assertNotIn(
                        "DSX-INT-040", out.getvalue() + err.getvalue(),
                        f"{path.name} unexpectedly names DSX-INT-040 at ship",
                    )


_MALFORMED_SHAPES: "tuple[object, ...]" = ("s", [], None, 3, {})


class TestModuleHardenedAgainstMalformedShapes(unittest.TestCase):
    """Task 2 (T-8-01/T-8-02): every sub-block and list this module reads
    degrades to no finding and no exception, across the full malformed-shape
    table, and the module never converts a crash into a silent pass via
    exception handling."""

    def test_malformed_top_level_and_sub_block_values_raise_no_exception(self):
        targets = (
            "validity_frame",
            "validity_frame.interference",
            "validity_frame.triggering",
            "validity_frame.stability",
            "metrics",
        )
        for target in targets:
            for shape in _MALFORMED_SHAPES:
                with self.subTest(target=target, shape=repr(shape)):
                    spec: dict = {"question_type": "causal", "validity_frame": {}}
                    if target == "validity_frame":
                        spec["validity_frame"] = shape
                    elif target == "metrics":
                        spec["metrics"] = shape
                    else:
                        sub = target.split(".")[1]
                        spec["validity_frame"] = {sub: shape}
                    try:
                        interference.check(spec)
                    except Exception as exc:  # pragma: no cover - failure path
                        self.fail(f"check() raised {exc!r} for {target}={shape!r}")

    def test_malformed_top_level_and_sub_block_values_produce_no_int_finding(self):
        targets = (
            "validity_frame",
            "validity_frame.interference",
            "validity_frame.triggering",
            "validity_frame.stability",
            "metrics",
        )
        for target in targets:
            for shape in _MALFORMED_SHAPES:
                with self.subTest(target=target, shape=repr(shape)):
                    spec: dict = {"question_type": "causal", "validity_frame": {}}
                    if target == "validity_frame":
                        spec["validity_frame"] = shape
                    elif target == "metrics":
                        spec["metrics"] = shape
                    else:
                        sub = target.split(".")[1]
                        spec["validity_frame"] = {sub: shape}
                    report = interference.check(spec)
                    int_codes = {c for c in codes(report) if c.startswith("DSX-INT-")}
                    self.assertEqual(int_codes, set())

    def test_malformed_spec_itself_not_a_mapping_raises_no_exception(self):
        for bad_spec in ("s", [], None, 3):
            with self.subTest(bad_spec=repr(bad_spec)):
                try:
                    report = interference.check(bad_spec)
                except Exception as exc:  # pragma: no cover - failure path
                    self.fail(f"check() raised {exc!r} for spec={bad_spec!r}")
                self.assertEqual(codes(report), set())

    def test_malformed_metrics_entries_that_are_strings_raise_no_exception_and_no_finding(self):
        spec = {
            "question_type": "causal",
            "validity_frame": {
                "triggering": {"analysis_population": "eligible", "dilution_adjusted": False}
            },
            "metrics": ["revenue", "orders"],
        }
        try:
            report = interference.check(spec)
        except Exception as exc:  # pragma: no cover - failure path
            self.fail(f"check() raised {exc!r} for a metrics list of bare strings")
        self.assertEqual(codes(report), set())

    def test_module_contains_no_try_or_except_ast_nodes_for_malformed_shapes(self):
        import ast

        source = (ROOT / "dsx" / "frame" / "interference.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        try_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.Try)]
        self.assertEqual(
            try_nodes, [],
            "dsx/frame/interference.py must degrade by type check, never by "
            "exception handling — an exception handler here would convert a "
            "crash into a silent pass",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
