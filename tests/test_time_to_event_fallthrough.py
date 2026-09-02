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
from pathlib import Path

from dsx.checks import stats

ROOT = Path(__file__).resolve().parent.parent
TEST_SELECTION = ROOT / "references" / "test-selection.md"

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


class TimeToEventFallthroughPositionTest(unittest.TestCase):
    """REQ-P20-03: log_rank stays recommend_test's TERMINAL unconditional fallthrough, and
    time-to-event stays the TERMINAL outcome-type row of the decision table, after all six
    Phase-18/19 sections were appended to references/test-selection.md.

    The Phase-18/19 additions are SEPARATE ``##`` sections after the decision table, never new
    decision-table outcome rows — these two assertions pin that: a future contributor who
    appends an outcome branch AFTER the log_rank fallthrough (shadowing time_to_event's route)
    or inserts a decision-table outcome row after the time-to-event row turns this red.
    """

    def test_log_rank_is_recommend_test_terminal_fallthrough(self):
        # Code side: the LAST `return _rec(` in recommend_test's source names log_rank.
        source = inspect.getsource(stats.recommend_test)
        returns = [ln for ln in source.splitlines() if "return _rec(" in ln]
        self.assertTrue(returns, "no `return _rec(` sites found in recommend_test source")
        self.assertIn(
            "log_rank", returns[-1],
            "REQ-P20-03: recommend_test's terminal `return _rec(` must name log_rank so the "
            "time-to-event route stays the unconditional fallthrough; a new outcome branch "
            f"appended after it would shadow time_to_event. Last return: {returns[-1]!r}",
        )

    def test_time_to_event_is_decision_table_terminal_outcome_row(self):
        # Doc side: the FINAL data row of the "## Decision table" has Outcome = time-to-event.
        # The block is bounded by the NEXT ``##`` heading — NOT the bare ``[^1]`` marker, which
        # also appears in-cell in the proportion row (`...expected cell < 5)[^1]`) and would
        # truncate the table to that single row.
        text = TEST_SELECTION.read_text(encoding="utf-8")
        after = text.split("## Decision table", 1)[1]
        block = re.split(r"\r?\n##\s", after, 1)[0]
        rows = [
            r for r in re.split(r"\r?\n", block)
            if r.strip().startswith("|") and "---" not in r
        ]
        data = [r for r in rows if "outcome" not in r.lower()]  # drop the header row
        self.assertGreaterEqual(len(data), 2, "decision-table parse found too few data rows")
        last_outcome = data[-1].split("|")[1].strip().lower()
        self.assertIn("time", last_outcome)
        self.assertIn("event", last_outcome)


if __name__ == "__main__":
    unittest.main()
