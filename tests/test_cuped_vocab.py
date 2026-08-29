"""REQ-P15-01: CUPED joins VARIANCE_ADJUSTMENTS additively and the two-member
covariate-timing vocabulary is dumped by `dsx vocab`.

Stdlib-only, CRLF-agnostic (no line-anchored parsing). This module mints no
finding code, so it carries no `# D-05:` marker.
"""

import unittest

from dsx.spec import (
    CUPED_COVARIATE_TIMINGS,
    VARIANCE_ADJUSTMENTS,
    describe_vocabulary,
)

_LEGACY = {"cluster_robust", "delta_method", "bootstrap_cluster", "mixed_effects"}


class CupedVocabularyTest(unittest.TestCase):
    def test_cuped_is_a_variance_adjustment(self):
        self.assertIn("cuped", VARIANCE_ADJUSTMENTS)

    def test_four_legacy_variance_adjustments_round_trip(self):
        # Additive, not a replace: the four prior members remain and the set is exactly five.
        self.assertTrue(_LEGACY <= VARIANCE_ADJUSTMENTS)
        self.assertEqual(len(VARIANCE_ADJUSTMENTS), 5, VARIANCE_ADJUSTMENTS)

    def test_vocab_dump_lists_cuped(self):
        # describe_vocabulary() is the exact object cmd_vocab serialises.
        dumped = describe_vocabulary()["variance_adjustments"]
        self.assertIn("cuped", dumped)
        for member in _LEGACY:
            self.assertIn(member, dumped)

    def test_cuped_covariate_timings_is_exactly_two_valued(self):
        self.assertEqual(CUPED_COVARIATE_TIMINGS, {"pre_experiment", "post_treatment"})
        self.assertEqual(
            set(describe_vocabulary()["cuped_covariate_timings"]),
            {"pre_experiment", "post_treatment"},
        )


if __name__ == "__main__":
    unittest.main()
