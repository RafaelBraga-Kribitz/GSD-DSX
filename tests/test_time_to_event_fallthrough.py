"""REQ-P17-04: recommend_test reaches log_rank for a time_to_event outcome by
UNCONDITIONAL fallthrough — there is no equality guard on the time_to_event
literal. Pinned before Phase 18/19 add outcome-type rows.

Dual idiom (behavioural + source-scan), modelled on
tests/test_no_shapiro_autoswitch.py. Stdlib-only, CRLF-safe (the guard regex is
whitespace-tolerant via \\s*, never line-anchored). This module mints no finding
code, so it carries no ``# D-05:`` marker.
"""

import inspect
import re
import unittest

from dsx.checks import stats

# An equality guard comparing the outcome variable to the time_to_event literal,
# in either order, quote-agnostic and whitespace-tolerant (CRLF-safe). A future
# contributor who adds such a guard turns the structural leg red, forcing a
# deliberate, reviewed change to the routing contract.
_TIME_TO_EVENT_GUARD = re.compile(
    r"""outcome(?:_type)?\s*==\s*['"]time_to_event['"]"""
    r"""|['"]time_to_event['"]\s*==\s*outcome(?:_type)?"""
)


class TimeToEventFallthroughTest(unittest.TestCase):
    def test_time_to_event_always_routes_to_log_rank(self):
        # Behavioural leg: for every n_groups and paired combination, a
        # time_to_event outcome routes to log_rank (nothing short-circuits it).
        for n_groups in (1, 2, 3):
            for paired in (True, False):
                rec = stats.recommend_test("time_to_event", n_groups, paired=paired)
                self.assertEqual(
                    rec["test"],
                    "log_rank",
                    f"REQ-P17-04: time_to_event with n_groups={n_groups}, paired={paired} "
                    f"must route to log_rank, got {rec['test']!r}",
                )

    def test_no_time_to_event_equality_guard_in_source(self):
        # Structural leg: log_rank is reached by unconditional fallthrough, not by
        # an explicit branch — so no `outcome == "time_to_event"` guard exists.
        source = inspect.getsource(stats.recommend_test)
        self.assertIsNone(
            _TIME_TO_EVENT_GUARD.search(source),
            "REQ-P17-04: recommend_test must reach log_rank for time_to_event by "
            "unconditional fallthrough — no equality guard on the time_to_event "
            "literal may be introduced without deliberately updating this contract.",
        )


if __name__ == "__main__":
    unittest.main()
