"""REQ-P15-03 / D-08: the canonical good fixture, extended with thin cohort/funnel BI
fields and a pre_experiment CUPED block, still passes every gate at every threshold and
draws no findings from the new DSX-MET-021 / DSX-EXP-070 checks. Stdlib-only. Mints nothing."""

import json
import unittest
from pathlib import Path

from dsx.cli import GATE_PROFILES, GATE_THRESHOLDS, run_checks
from dsx.findings import Severity
from dsx.loader import load
from dsx.spec import get, items, section

ROOT = Path(__file__).resolve().parent.parent
GOOD = ROOT / "examples" / "good-ANALYSIS-SPEC.yaml"
RESOLVE = str(ROOT / "examples")
GATE_POINTS = ("plan", "execute", "verify", "ship")


def codes(report):
    return {f.code for f in report.findings}


class GoodFixturePhase15Test(unittest.TestCase):
    def setUp(self):
        self.good = load(str(GOOD))

    def _run(self, point):
        return run_checks(
            self.good, GATE_PROFILES[point], None, gate_point=point, resolve_root=RESOLVE
        )

    def test_good_fixture_passes_every_gate_at_every_threshold(self):
        for point in GATE_POINTS:
            report = self._run(point)
            threshold = Severity.parse(GATE_THRESHOLDS[point])
            self.assertEqual(
                report.exit_code(threshold), 0, f"good fixture blocks at {point}"
            )

    def test_new_checks_stay_silent_on_the_good_fixture(self):
        report = self._run("ship")  # strictest gate point
        found = codes(report)
        self.assertNotIn("DSX-MET-021", found)
        self.assertNotIn("DSX-EXP-070", found)

    def test_thin_fields_are_present_and_outside_validity_frame(self):
        self.assertEqual(get(self.good, "design.cuped.covariate_timing"), "pre_experiment")
        results = section(self.good, "results")
        self.assertTrue(items(results, "cohort_comparisons"), "cohort_comparisons missing")
        self.assertTrue(items(results, "funnel_steps"), "funnel_steps missing")
        self.assertTrue(
            any(m.get("cohort_grain") for m in items(self.good, "metrics")),
            "cohort_grain missing",
        )
        # The D-04 placement invariant: none of the new keys live inside validity_frame,
        # so frame_digest is unchanged.
        vf_blob = json.dumps(self.good.get("validity_frame") or {})
        for key in ("cohort_comparisons", "funnel_steps", "cuped", "cohort_grain"):
            self.assertNotIn(key, vf_blob, f"{key} must not be inside validity_frame")


if __name__ == "__main__":
    unittest.main()
