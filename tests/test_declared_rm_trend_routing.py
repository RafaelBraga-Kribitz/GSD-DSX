"""No-autoswitch routing proofs for RM / trend / variance-role (REQ-P19-01/02/06).

The load-bearing guarantee (REQ-P18-06 doctrine, extended to the Phase-19
families): every ``recommend_*`` routing function is DATALESS. Its
``inspect.signature`` carries ONLY declared-context string parameters — there is
no ``data`` / ``n`` / ``n_groups`` / ``paired`` / ``normal`` / ``distribution``
argument anywhere. A future contributor who adds a data/n/distribution parameter
(reintroducing two-stage, data-then-pick selection) turns this proof red.

Beyond the signature proof, this module pins the acceptable-set CONTENT: the RM
router never offers a two-stage / Mauchly-conditional procedure as a route (D-04),
the trend router surfaces the ordered-trend family, and the variance-role router
never endorses a variance PRETEST as a location-choice gate.

Stdlib only (unittest, inspect). This test mints nothing.
"""

import inspect
import unittest

from dsx.checks import stats

# Any of these appearing as a parameter name reintroduces data-then-pick
# selection — the exact anti-pattern the dataless contract forbids.
BANNED_PARAMS = frozenset({
    "data", "n", "n_groups", "paired", "normal", "equal_variance",
    "n_per_group", "overdispersed", "distribution",
})


def _params(fn):
    return set(inspect.signature(fn).parameters)


class DatalessSignatureTest(unittest.TestCase):
    def test_recommend_rm_is_dataless(self):
        self.assertEqual(BANNED_PARAMS & _params(stats.recommend_rm), set())

    def test_recommend_trend_is_dataless(self):
        self.assertEqual(BANNED_PARAMS & _params(stats.recommend_trend), set())

    def test_recommend_variance_role_is_dataless(self):
        self.assertEqual(BANNED_PARAMS & _params(stats.recommend_variance_role), set())


class RecommendRmRoutingTest(unittest.TestCase):
    def test_continuous_routes_unconditional_gg_never_mauchly(self):
        tests = stats.recommend_rm("continuous")["tests"]
        self.assertIn("rm_anova_gg", tests)
        # NEVER a two-stage / Mauchly-conditional procedure (D-04).
        joined = " ".join(tests)
        self.assertNotIn("mauchly", joined)
        self.assertNotIn("conditional", joined)

    def test_rank_cases_route_friedman_page_l(self):
        tests = stats.recommend_rm("ranks")["tests"]
        self.assertIn("friedman", tests)
        self.assertIn("page_l", tests)

    def test_binary_case_routes_cochran_q(self):
        self.assertIn("cochran_q", stats.recommend_rm("binary")["tests"])

    def test_no_route_offers_a_mauchly_conditional_procedure(self):
        for ctx in ("continuous", "ranks", "binary"):
            joined = " ".join(stats.recommend_rm(ctx)["tests"])
            self.assertNotIn("mauchly", joined, ctx)

    def test_out_of_route_context_raises(self):
        with self.assertRaises(ValueError):
            stats.recommend_rm("not_a_repeated_measure")


class RecommendTrendRoutingTest(unittest.TestCase):
    def test_ordered_trend_surfaces_the_family(self):
        tests = stats.recommend_trend("ordered_trend")["tests"]
        self.assertIn("cochran_armitage", tests)
        self.assertIn("jonckheere_terpstra", tests)
        self.assertIn("mann_kendall", tests)
        self.assertIn("sens_slope", tests)

    def test_out_of_route_context_raises(self):
        with self.assertRaises(ValueError):
            stats.recommend_trend("no_trend_here")


class RecommendVarianceRoleRoutingTest(unittest.TestCase):
    def test_scale_estimand_role_routes_a_variance_test_as_the_estimand(self):
        tests = stats.recommend_variance_role("scale_estimand")["tests"]
        # A variance test is a legitimate estimand target under this role.
        self.assertTrue(tests & {"levene", "brown_forsythe", "fligner_killeen", "bartlett"})

    def test_precondition_role_never_gates_location_on_a_pretest(self):
        result = stats.recommend_variance_role("precondition_to_location")
        joined = " ".join(result["tests"])
        # The only acceptable disposition is to NOT pretest — use Welch
        # unconditionally. It must never endorse a pretest-then-switch gate.
        self.assertNotIn("pretest", joined)
        self.assertIn("welch", joined)

    def test_out_of_route_role_raises(self):
        with self.assertRaises(ValueError):
            stats.recommend_variance_role("not_a_role")


if __name__ == "__main__":
    unittest.main()
