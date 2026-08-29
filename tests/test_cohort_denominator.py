# D-05: DSX-MET-021
"""REQ-P15-04 (changing-denominator half): DSX-MET-021 fires on a declared cohort
comparison whose buckets are sampled at different rates with no reweighting, is
silent on well-behaved declarations, and is provably disjoint from DSX-MET-020.

Stdlib-only, CRLF-agnostic. The survivorship-bias half is NOT minted (brief.md
§6.5, D-13 entry condition); only DSX-MET-021 ships.
"""

import unittest

from dsx.checks import metrics


def codes(report):
    return {f.code for f in report.findings}


class CohortDenominatorShiftTest(unittest.TestCase):
    def test_met021_fires_on_unreweighted_rate_spread(self):
        spec = {
            "results": {
                "cohort_comparisons": [
                    {
                        "metric": "activation_rate",
                        "buckets": [
                            {"name": "a", "sampling_rate": 0.9},
                            {"name": "b", "sampling_rate": 0.1},
                        ],
                    }
                ]
            }
        }
        self.assertIn("DSX-MET-021", codes(metrics.check(spec)))

    def test_met021_fires_on_treatment_share_spread(self):
        # No sampling_rate declared → the treatment_share fallback axis decides.
        spec = {
            "results": {
                "cohort_comparisons": [
                    {
                        "metric": "activation_rate",
                        "buckets": [
                            {"name": "a", "treatment_share": 0.9},
                            {"name": "b", "treatment_share": 0.1},
                        ],
                    }
                ]
            }
        }
        self.assertIn("DSX-MET-021", codes(metrics.check(spec)))

    def test_met021_silent_when_reweighted_true(self):
        spec = {
            "results": {
                "cohort_comparisons": [
                    {
                        "metric": "activation_rate",
                        "reweighted": True,
                        "buckets": [
                            {"name": "a", "sampling_rate": 0.9},
                            {"name": "b", "sampling_rate": 0.1},
                        ],
                    }
                ]
            }
        }
        self.assertNotIn("DSX-MET-021", codes(metrics.check(spec)))

    def test_met021_silent_when_rates_equal(self):
        spec = {
            "results": {
                "cohort_comparisons": [
                    {
                        "metric": "activation_rate",
                        "buckets": [
                            {"name": "a", "sampling_rate": 0.5},
                            {"name": "b", "sampling_rate": 0.5},
                        ],
                    }
                ]
            }
        }
        self.assertNotIn("DSX-MET-021", codes(metrics.check(spec)))

    def test_met021_respects_declared_tolerance(self):
        def spec_with_tolerance(tol):
            return {
                "results": {
                    "cohort_comparisons": [
                        {
                            "metric": "activation_rate",
                            "sampling_tolerance": tol,
                            "buckets": [
                                {"name": "a", "sampling_rate": 0.50},
                                {"name": "b", "sampling_rate": 0.42},
                            ],
                        }
                    ]
                }
            }

        # spread ~0.08: within a declared 0.10 tolerance → silent;
        # above a declared 0.05 tolerance → fires.
        self.assertNotIn("DSX-MET-021", codes(metrics.check(spec_with_tolerance(0.10))))
        self.assertIn("DSX-MET-021", codes(metrics.check(spec_with_tolerance(0.05))))

    def test_met020_and_met021_are_disjoint(self):
        # (a) A period-drift spec (period_comparisons only) fires MET-020, NOT MET-021.
        period_spec = {
            "results": {
                "period_comparisons": [
                    {
                        "metric": "activation_rate",
                        "base_denominator": 1000,
                        "comparison_denominator": 1400,
                    }
                ]
            }
        }
        period_codes = codes(metrics.check(period_spec))
        self.assertIn("DSX-MET-020", period_codes)
        self.assertNotIn("DSX-MET-021", period_codes)

        # (b) A cohort mix-shift spec (cohort_comparisons only) fires MET-021, NOT MET-020.
        cohort_spec = {
            "results": {
                "cohort_comparisons": [
                    {
                        "metric": "activation_rate",
                        "buckets": [
                            {"name": "a", "sampling_rate": 0.9},
                            {"name": "b", "sampling_rate": 0.1},
                        ],
                    }
                ]
            }
        }
        cohort_codes = codes(metrics.check(cohort_spec))
        self.assertIn("DSX-MET-021", cohort_codes)
        self.assertNotIn("DSX-MET-020", cohort_codes)

    def test_only_met021_reachable_from_cohort_check(self):
        # The cohort path mints exactly one MET code — no silent survivorship code.
        spec = {
            "results": {
                "cohort_comparisons": [
                    {
                        "metric": "activation_rate",
                        "buckets": [
                            {"name": "a", "sampling_rate": 0.9},
                            {"name": "b", "sampling_rate": 0.1},
                        ],
                    }
                ]
            }
        }
        met_codes = {c for c in codes(metrics.check(spec)) if c.startswith("DSX-MET-")}
        self.assertEqual(met_codes, {"DSX-MET-021"})


if __name__ == "__main__":
    unittest.main()
