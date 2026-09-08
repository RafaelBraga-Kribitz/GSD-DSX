"""Phase 29 Plan 01 (REQ-P29-01/03): DSX-COH-041 subgroup-harm disposition check.

Unit tests for `_check_subgroup_harm_disposition` in dsx/checks/coherence.py — the
declaration-only disposition obligation: under a genuinely prescriptive recommendation,
a declared `results.segments[]` entry whose effect opposes `results.overall_effect` by
sign AND whose declared n is at or above `decision.subgroup_harm_floor` must carry a
matching `decision.subgroup_harm[]` disposition row, else DSX-COH-041 fires.
"""

# D-05: DSX-COH-041
# Citation provenance for DSX-COH-041 is Gail, M. & Simon, R. (1985), "Testing for
# qualitative interactions between treatment effects and patient subsets", Biometrics
# 41(2):361-372, PMID 4027319 -- cited as the MOTIVATING DEFINITION of a qualitative /
# crossover interaction (treatment effects of OPPOSITE SIGN across subsets = when a
# segment counts as harmed relative to the recommendation's premised direction). This is
# the definition that motivates the "harmed segment" criterion ONLY. Gail & Simon
# describe a likelihood-ratio TEST; this check runs NO such test and computes NO
# statistic on the gate path -- it enforces a declaration-level disposition obligation,
# NOT the Gail & Simon mechanic, and must not be read as detecting hidden, mis-signed, or
# omitted harm (bounded catch: attribution over honestly-declared segments only).

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsx.checks import coherence  # noqa: E402
from dsx.findings import Severity  # noqa: E402


def _coh041(report) -> list:
    """The DSX-COH-041 findings in a report, in emit order."""
    return [f for f in report.findings if f.code == "DSX-COH-041"]


def _spec(
    *,
    question_type: str = "prescriptive",
    overall_effect=0.032,
    segments=None,
    floor=None,
    subgroup_harm=None,
    include_overall: bool = True,
) -> dict:
    """A minimal in-memory prescriptive spec driving the disposition check.

    Only the fields the disposition check reads are populated; other coherence
    sub-checks may add their own findings, which the tests ignore by filtering on
    DSX-COH-041 alone.
    """
    results: dict = {"segments": list(segments) if segments is not None else []}
    if include_overall:
        results["overall_effect"] = overall_effect
    decision: dict = {}
    if floor is not None:
        decision["subgroup_harm_floor"] = floor
    if subgroup_harm is not None:
        decision["subgroup_harm"] = list(subgroup_harm)
    return {
        "question_type": question_type,
        "results": results,
        "decision": decision,
    }


# The frozen D-29-02 four-segment table: three positive, one minority opposing the
# positive +3.2pp aggregate at n=1000, well above the declared 500 floor.
_FOUR_SEGMENTS = [
    {"name": "A", "effect": 0.05, "n": 4000},
    {"name": "B", "effect": 0.04, "n": 3000},
    {"name": "C", "effect": 0.03, "n": 2000},
    {"name": "D", "effect": -0.06, "n": 1000},
]


class TestSubgroupHarmDisposition(unittest.TestCase):
    # D-05: DSX-COH-041
    def test_missing_row_critical(self):
        """An opposing segment above the floor with NO matching subgroup_harm[] row
        fires DSX-COH-041 at CRITICAL."""
        report = coherence.check(
            _spec(segments=_FOUR_SEGMENTS, floor=500, subgroup_harm=None)
        )
        hits = _coh041(report)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].severity, Severity.CRITICAL)

    def test_accept_blank_rationale_high(self):
        """A matching `accept` row with a blank/missing rationale fires DSX-COH-041 at
        HIGH — the harm was seen and accepted, but not justified."""
        report = coherence.check(
            _spec(
                segments=_FOUR_SEGMENTS,
                floor=500,
                subgroup_harm=[
                    {"segment": "D", "disposition": "accept", "rationale": ""}
                ],
            )
        )
        hits = _coh041(report)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].severity, Severity.HIGH)

    def test_matching_row_with_rationale_silent(self):
        """A matching row with a non-blank rationale (any valid disposition) emits no
        DSX-COH-041 finding."""
        report = coherence.check(
            _spec(
                segments=_FOUR_SEGMENTS,
                floor=500,
                subgroup_harm=[
                    {
                        "segment": "D",
                        "disposition": "accept",
                        "rationale": (
                            "Segment D is carved out of the first rollout wave and "
                            "monitored for four weeks before inclusion."
                        ),
                    }
                ],
            )
        )
        self.assertEqual(_coh041(report), [])

    def test_floor_boundary(self):
        """The sign+floor trigger boundary is exact: an opposing segment with n just
        BELOW the floor is silent; the same segment with n AT the floor fires."""
        below = coherence.check(
            _spec(
                segments=[
                    {"name": "A", "effect": 0.05, "n": 4000},
                    {"name": "D", "effect": -0.06, "n": 1000},
                ],
                floor=1500,  # D's n=1000 is below the floor
                subgroup_harm=None,
            )
        )
        self.assertEqual(_coh041(below), [])

        at = coherence.check(
            _spec(
                segments=[
                    {"name": "A", "effect": 0.05, "n": 4000},
                    {"name": "D", "effect": -0.06, "n": 1000},
                ],
                floor=1000,  # D's n=1000 exactly touches the floor
                subgroup_harm=None,
            )
        )
        hits = _coh041(at)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].severity, Severity.CRITICAL)

    def test_sign_gate(self):
        """A segment whose effect has the SAME sign as the aggregate never triggers,
        regardless of n — only opposite-sign segments are candidates."""
        report = coherence.check(
            _spec(
                segments=[
                    {"name": "A", "effect": 0.05, "n": 4000},
                    {"name": "B", "effect": 0.04, "n": 9000},
                ],
                floor=0,
                subgroup_harm=None,
            )
        )
        self.assertEqual(_coh041(report), [])

    def test_default_floor_zero(self):
        """When decision.subgroup_harm_floor is absent, the floor defaults to 0 — every
        declared opposing segment demands a disposition, even at n=1."""
        report = coherence.check(
            _spec(
                segments=[
                    {"name": "A", "effect": 0.05, "n": 4000},
                    {"name": "D", "effect": -0.06, "n": 1},
                ],
                floor=None,  # absent → default 0
                subgroup_harm=None,
            )
        )
        hits = _coh041(report)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].severity, Severity.CRITICAL)

    def test_empty_early_return(self):
        """Declaration-guarded silence: no segments, or overall_effect absent, or a
        non-prescriptive question_type — none emit DSX-COH-041."""
        no_segments = coherence.check(_spec(segments=[], floor=500))
        self.assertEqual(_coh041(no_segments), [])

        overall_absent = coherence.check(
            _spec(segments=_FOUR_SEGMENTS, floor=500, include_overall=False)
        )
        self.assertEqual(_coh041(overall_absent), [])

        not_prescriptive = coherence.check(
            _spec(question_type="causal", segments=_FOUR_SEGMENTS, floor=500)
        )
        self.assertEqual(_coh041(not_prescriptive), [])


if __name__ == "__main__":
    unittest.main()
