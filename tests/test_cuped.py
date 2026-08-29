# D-05: DSX-EXP-070
"""REQ-P15-02: the CUPED post-treatment-covariate gate check (DSX-EXP-070, CRITICAL)
plus its off-gate-path reference arithmetic.

Proves the WSDM ρ²=0.25 worked value, DSX-EXP-070 firing on post_treatment / absent /
unrecognised timing and silence on pre_experiment / non-cuped, the `dsx gate plan`
exit_code 0→1 flip over the good fixture, and that the gate check never imports the
CUPED math. Stdlib-only, CRLF-agnostic.
"""

import copy
import math
import unittest
from pathlib import Path

from dsx.checks import design
from dsx.cli import GATE_PROFILES, GATE_THRESHOLDS, run_checks
from dsx.findings import Severity
from dsx.loader import load
from dsx.mathx import cuped_theta, cuped_variance_reduction

ROOT = Path(__file__).resolve().parent.parent
GOOD = ROOT / "examples" / "good-ANALYSIS-SPEC.yaml"
DESIGN_SRC = ROOT / "dsx" / "checks" / "design.py"


def codes(report):
    return {f.code for f in report.findings}


class CupedWorkedValueTest(unittest.TestCase):
    def test_cuped_variance_reduction_matches_wsdm_identity(self):
        self.assertTrue(math.isclose(cuped_variance_reduction(0.5), 0.25))
        self.assertTrue(math.isclose(1 - cuped_variance_reduction(0.5), 0.75))
        self.assertTrue(math.isclose(cuped_theta(0.5, 2.0), 0.25))


class Exp070CheckTest(unittest.TestCase):
    @staticmethod
    def _spec(*, adjustment="cuped", cuped=None):
        d = {"variance_adjustment": adjustment}
        if cuped is not None:
            d["cuped"] = cuped
        return {"design": d}

    def test_exp070_fires_on_post_treatment(self):
        report = design.check(self._spec(cuped={"covariate_timing": "post_treatment"}))
        self.assertIn("DSX-EXP-070", codes(report))
        finding = next(f for f in report.findings if f.code == "DSX-EXP-070")
        self.assertEqual(finding.severity, Severity.parse("CRITICAL"))

    def test_exp070_fires_on_absent_timing(self):
        report = design.check(self._spec(cuped={}))
        self.assertIn("DSX-EXP-070", codes(report))

    def test_exp070_fires_on_unrecognised_timing(self):
        report = design.check(self._spec(cuped={"covariate_timing": "during_experiment"}))
        self.assertIn("DSX-EXP-070", codes(report))

    def test_exp070_silent_on_pre_experiment(self):
        report = design.check(self._spec(cuped={"covariate_timing": "pre_experiment"}))
        self.assertNotIn("DSX-EXP-070", codes(report))

    def test_exp070_does_not_run_without_cuped(self):
        report = design.check(self._spec(adjustment="cluster_robust"))
        self.assertNotIn("DSX-EXP-070", codes(report))


class GatePlanExitTest(unittest.TestCase):
    def setUp(self):
        self.good = load(str(GOOD))
        self.threshold = Severity.parse(GATE_THRESHOLDS["plan"])
        self.resolve = str(ROOT / "examples")

    def _plan(self, spec):
        return run_checks(
            spec, GATE_PROFILES["plan"], None, gate_point="plan", resolve_root=self.resolve
        )

    def test_gate_plan_exit_flips_on_post_treatment_cuped(self):
        # Baseline: the unmutated good fixture is clean at plan.
        base = self._plan(self.good)
        self.assertEqual(base.exit_code(self.threshold), 0)
        self.assertNotIn("DSX-EXP-070", codes(base))

        # A post-treatment CUPED covariate flips plan 0 → 1, attributable to DSX-EXP-070.
        bad = copy.deepcopy(self.good)
        bad["design"]["variance_adjustment"] = "cuped"
        bad["design"]["cuped"] = {
            "covariate": "pre_period_activation",
            "covariate_timing": "post_treatment",
            "covariate_source": "warehouse.fct_signups_prior",
        }
        bad_report = self._plan(bad)
        self.assertEqual(bad_report.exit_code(self.threshold), 1)
        self.assertIn("DSX-EXP-070", codes(bad_report))

        # A pre-experiment covariate stays clean.
        good_cuped = copy.deepcopy(self.good)
        good_cuped["design"]["variance_adjustment"] = "cuped"
        good_cuped["design"]["cuped"] = {
            "covariate": "pre_period_activation",
            "covariate_timing": "pre_experiment",
            "covariate_source": "warehouse.fct_signups_prior",
        }
        good_report = self._plan(good_cuped)
        self.assertEqual(good_report.exit_code(self.threshold), 0)
        self.assertNotIn("DSX-EXP-070", codes(good_report))


class GateCheckPurityTest(unittest.TestCase):
    def test_gate_check_does_not_import_cuped_math(self):
        src = DESIGN_SRC.read_text(encoding="utf-8")
        self.assertNotIn("cuped_theta", src)
        self.assertNotIn("cuped_variance_reduction", src)


if __name__ == "__main__":
    unittest.main()
