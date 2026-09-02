"""REQ-P17-02 / REQ-P17-05: estimand_kind is a closed 6-member routing vocabulary
on the analysis block, dumped by `dsx vocab`, absence non-blocking, and a
mis-slotted value fires exactly one loud finding — reusing the existing
DSX-STA-040 code, minting none (17-CONTEXT.md D-01).

Stdlib-only, CRLF-agnostic (no line-anchored parsing).

# D-05: DSX-STA-040
The membership guard shares DSX-STA-040 with the outcome_type check (no new code —
REQ-P17-05); this marker keeps the shared-code test discoverable.
"""

import unittest

from dsx.checks import stats
from dsx.spec import ESTIMAND_KINDS, describe_vocabulary

_MEMBERS = frozenset({
    "linear_association",
    "monotone_association",
    "nominal_association",
    "agreement",
    "method_comparison",
    "ordered_trend",
})


def _codes(report):
    return [f.code for f in report.findings]


def _mentions_estimand_kind(report):
    return [
        f for f in report.findings
        if "estimand_kind" in f.title or "estimand_kind" in f.where
    ]


class EstimandKindVocabularyTest(unittest.TestCase):
    def test_six_member_identity(self):
        # Closed set, exactly the six D-01 members — no more, no fewer.
        self.assertEqual(set(ESTIMAND_KINDS), set(_MEMBERS))

    def test_vocab_dump_lists_all_six(self):
        # describe_vocabulary() is the exact object `dsx vocab` serialises.
        dumped = describe_vocabulary()["estimand_kind"]
        self.assertEqual(set(dumped), set(_MEMBERS))

    def test_absence_is_non_blocking(self):
        # No estimand_kind declared -> nothing about estimand_kind fires (D-10).
        spec = {"analysis": {"outcome_type": "proportion"}}
        report = stats.check(spec)
        self.assertEqual(_mentions_estimand_kind(report), [])

    def test_mis_slotted_value_fires_one_loud_finding(self):
        # A bogus estimand_kind (with a valid outcome_type, no test) -> exactly one
        # DSX-STA-040 naming analysis.estimand_kind.
        spec = {"analysis": {"outcome_type": "proportion", "estimand_kind": "difference_in_means"}}
        report = stats.check(spec)
        offenders = _mentions_estimand_kind(report)
        self.assertEqual(len(offenders), 1, _codes(report))
        self.assertEqual(offenders[0].code, "DSX-STA-040")

    def test_outcome_type_membership_fires_without_a_declared_test(self):
        # Pitfall-2 tightening: the membership loop runs independently of the
        # declared-test early return, so a bogus outcome_type with no test still fires.
        spec = {"analysis": {"outcome_type": "not_a_real_type"}}
        report = stats.check(spec)
        self.assertIn("DSX-STA-040", _codes(report))

    def test_valid_member_fires_nothing(self):
        # Every declared member is inert on the membership guard.
        for member in _MEMBERS:
            spec = {"analysis": {"outcome_type": "proportion", "estimand_kind": member}}
            report = stats.check(spec)
            self.assertEqual(_mentions_estimand_kind(report), [], member)


if __name__ == "__main__":
    unittest.main()
