"""Phase 11.2 Plan 01 (REQ-P11.2-01): the prescriptive claim-type ladder.

D-01/D-02: adding ``prescriptive`` as a fifth ``CLAIM_TYPES`` member and the
fourth-rank ``CLAIM_STRENGTH`` row must (a) make ``DSX-COH-001`` fire on a
prescriptive claim under a weaker ``question_type``, (b) stop
``DSX-SPEC-062`` "unrecognised type" from misfiring on a ``type:
prescriptive`` claim, and (c) update both stale "four claim types" remedy
strings (``DSX-SPEC-061``/``DSX-SPEC-062``) to name all five types.

Run:  python -m unittest tests.test_prescriptive_ladder -v
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsx.checks import coherence  # noqa: E402
from dsx.findings import Report, Severity  # noqa: E402
from dsx.spec import validate_structure  # noqa: E402


def codes(report: Report) -> set[str]:
    return {f.code for f in report.findings}


class TestPrescriptiveLadder(unittest.TestCase):
    def test_prescriptive_claim_exceeds_weaker_question_fires_coh001(self):
        """Test 1: a prescriptive claim under a descriptive question must fire
        DSX-COH-001 CRITICAL exactly once. RED today because CLAIM_STRENGTH
        has no 'prescriptive' row, so the claim is silently skipped
        (coherence.py:61-62) and no finding is ever emitted."""
        report = coherence.check(
            {
                "question_type": "descriptive",
                "claims": [
                    {"text": "Offer bundled incentives to reduce churn", "type": "prescriptive"}
                ],
                "decision": {},
                "design": {},
            }
        )
        coh001 = [f for f in report.findings if f.code == "DSX-COH-001"]
        self.assertEqual(
            len(coh001), 1,
            f"expected exactly one DSX-COH-001, got codes={codes(report)}",
        )
        self.assertEqual(coh001[0].severity, Severity.CRITICAL)

    def test_prescriptive_claim_type_no_longer_trips_spec062(self):
        """Test 2: a claim typed 'prescriptive' must not fire DSX-SPEC-062
        'unrecognised type' from the structural validator. RED today because
        'prescriptive' is not a member of CLAIM_TYPES."""
        report = validate_structure(
            {
                "spec_version": 1,
                "title": "t",
                "question_type": "prescriptive",
                "decision": {"decision_rule": "r", "owner": "o", "action_if_null": "n"},
                "claims": [
                    {"text": "Offer bundled incentives to reduce churn", "type": "prescriptive"}
                ],
            }
        )
        self.assertNotIn(
            "DSX-SPEC-062", codes(report),
            f"prescriptive claim type should be recognised, got codes={codes(report)}",
        )

    def test_prescriptive_claim_equal_to_prescriptive_question_does_not_fire(self):
        """Test 3 (edge): claim strength equal to (not exceeding) question
        strength must not fire DSX-COH-001. This already passes today, but
        for the wrong reason (the claim is skipped entirely); after the fix
        it passes because 4 is not > 4."""
        report = coherence.check(
            {
                "question_type": "prescriptive",
                "claims": [
                    {"text": "Offer bundled incentives to reduce churn", "type": "prescriptive"}
                ],
                "decision": {},
                "design": {},
            }
        )
        self.assertNotIn("DSX-COH-001", codes(report))

    def test_remedy_strings_name_five_claim_types(self):
        """Test 4: both DSX-SPEC-061 and DSX-SPEC-062 remedy strings must name
        all five claim types and must not quote the stale four-type wording.
        Read from the emitted remedy (not by grepping source), so the test
        survives a refactor. RED today because both remedies are stale."""
        report = validate_structure(
            {
                "spec_version": 1,
                "title": "t",
                "question_type": "descriptive",
                "decision": {"decision_rule": "r", "owner": "o", "action_if_null": "n"},
                "claims": [
                    {"text": "a claim with no type"},
                    {"text": "a claim with a bogus type", "type": "not_a_real_type"},
                ],
            }
        )
        finding_061 = next(f for f in report.findings if f.code == "DSX-SPEC-061")
        finding_062 = next(f for f in report.findings if f.code == "DSX-SPEC-062")

        for finding in (finding_061, finding_062):
            self.assertNotIn(
                "four claim types", finding.remedy,
                f"{finding.code} remedy still quotes a stale four-type count: {finding.remedy!r}",
            )
            self.assertFalse(
                finding.remedy.rstrip(".").endswith("predictive or causal"),
                f"{finding.code} remedy still ends on the stale four-type list: {finding.remedy!r}",
            )
            for claim_type in ("descriptive", "association", "predictive", "causal", "prescriptive"):
                self.assertIn(
                    claim_type, finding.remedy,
                    f"{finding.code} remedy is missing claim type {claim_type!r}: {finding.remedy!r}",
                )


if __name__ == "__main__":
    unittest.main()
