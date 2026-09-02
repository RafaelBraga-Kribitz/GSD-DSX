"""No-autoswitch routing proofs for resampling / post-hoc / power / proportion-CI
(REQ-P19-04/05/07).

Same load-bearing guarantee as the RM/trend module: every ``recommend_*`` here is
DATALESS — its ``inspect.signature`` carries ONLY declared-context string
parameters, never ``data`` / ``n`` / ``distribution`` (REQ-P18-06 doctrine). The
content assertions pin D-04: the resampling router draws only from
``RESAMPLING_METHODS`` with BCa as the house default, the post-hoc router returns
exactly ``POSTHOC_FAMILY_MAP[family]`` and NEVER a deprecated ``snk`` /
``unprotected_lsd``, the power router never endorses ``observed`` / ``post_hoc``,
and the proportion-CI router never endorses ``wald``.

Stdlib only (unittest, inspect). This test mints nothing.
"""

import inspect
import unittest

from dsx import spec
from dsx.checks import stats

BANNED_PARAMS = frozenset({
    "data", "n", "n_groups", "paired", "normal", "equal_variance",
    "n_per_group", "overdispersed", "distribution",
})


def _params(fn):
    return set(inspect.signature(fn).parameters)


class DatalessSignatureTest(unittest.TestCase):
    def test_recommend_resampling_is_dataless(self):
        self.assertEqual(BANNED_PARAMS & _params(stats.recommend_resampling), set())

    def test_recommend_posthoc_is_dataless(self):
        self.assertEqual(BANNED_PARAMS & _params(stats.recommend_posthoc), set())

    def test_recommend_power_is_dataless(self):
        self.assertEqual(BANNED_PARAMS & _params(stats.recommend_power), set())

    def test_recommend_proportion_ci_is_dataless(self):
        self.assertEqual(BANNED_PARAMS & _params(stats.recommend_proportion_ci), set())


class RecommendResamplingRoutingTest(unittest.TestCase):
    def test_interval_route_draws_only_from_resampling_methods(self):
        tests = stats.recommend_resampling("interval")["tests"]
        self.assertTrue(tests)
        self.assertTrue(tests <= set(spec.RESAMPLING_METHODS))

    def test_bca_is_the_house_default_for_intervals(self):
        self.assertEqual(stats.recommend_resampling("interval")["default"], "bca")

    def test_out_of_route_purpose_raises(self):
        with self.assertRaises(ValueError):
            stats.recommend_resampling("not_a_purpose")


class RecommendPosthocRoutingTest(unittest.TestCase):
    def test_returns_exactly_the_family_map_set(self):
        self.assertEqual(
            stats.recommend_posthoc("welch_anova")["tests"],
            spec.POSTHOC_FAMILY_MAP["welch_anova"],
        )

    def test_never_returns_a_deprecated_posthoc(self):
        for omnibus in spec.POSTHOC_FAMILY_MAP:
            tests = stats.recommend_posthoc(omnibus)["tests"]
            self.assertNotIn("snk", tests, omnibus)
            self.assertNotIn("unprotected_lsd", tests, omnibus)

    def test_welch_anova_house_default_is_games_howell(self):
        self.assertIn("games_howell", stats.recommend_posthoc("welch_anova")["tests"])

    def test_out_of_route_omnibus_raises(self):
        with self.assertRaises(ValueError):
            stats.recommend_posthoc("not_an_omnibus")


class RecommendPowerRoutingTest(unittest.TestCase):
    def test_endorsed_forms_exclude_observed_and_post_hoc(self):
        tests = stats.recommend_power("a_priori")["tests"]
        self.assertNotIn("observed", tests)
        self.assertNotIn("post_hoc", tests)

    def test_observed_input_redirects_away_from_the_misuse(self):
        # A declared observed/post-hoc power still routes to endorsed forms only.
        tests = stats.recommend_power("observed")["tests"]
        self.assertNotIn("observed", tests)
        self.assertNotIn("post_hoc", tests)
        self.assertIn("a_priori", tests)

    def test_out_of_route_type_raises(self):
        with self.assertRaises(ValueError):
            stats.recommend_power("not_a_power_type")


class RecommendProportionCiRoutingTest(unittest.TestCase):
    def test_house_default_is_wilson_and_never_wald(self):
        result = stats.recommend_proportion_ci("proportion")
        tests = result["tests"]
        self.assertIn("wilson", tests)
        self.assertIn("clopper_pearson", tests)
        self.assertIn("jeffreys", tests)
        self.assertIn("agresti_coull", tests)
        self.assertNotIn("wald", tests)
        self.assertEqual(result["default"], "wilson")

    def test_out_of_route_context_raises(self):
        with self.assertRaises(ValueError):
            stats.recommend_proportion_ci("not_a_proportion")


if __name__ == "__main__":
    unittest.main()
