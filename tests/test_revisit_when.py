"""Phase 11.2 Plan 06 (REQ-P11.2-04): decision.revisit_when and the
window-aware sibling falsifier predicate.

D-07: revisit_when_is_discriminating(x) = falsifier_is_discriminating(x) AND
_has_window_token(x) — a NEW sibling, never a mutation of the shared
falsifier_is_discriminating(), because that function's two estimand callers
(dsx/frame/val.py:236, :637) validate a windowless logical falsifier and the
good fixture's estimand falsifier (examples/good-ANALYSIS-SPEC.yaml, the
validity_frame.estimand.falsifier field) has no window of its own.

Run:  python -m unittest tests.test_revisit_when -v
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsx.spec import (  # noqa: E402
    falsifier_is_discriminating,
    revisit_when_is_discriminating,
)

# The good fixture's own estimand falsifier (examples/good-ANALYSIS-SPEC.yaml, the
# validity_frame.estimand.falsifier field) — quoted verbatim, windowless, so the
# "falsifier unchanged" regression exercises the real accepted shape.
_GOOD_ESTIMAND_FALSIFIER = (
    "95% CI on the activation uplift includes zero, or its lower bound sits below "
    "+1.0pp"
)


class TestRevisitWhenIsDiscriminating(unittest.TestCase):
    """The sibling predicate: discriminating core AND a window token."""

    def test_named_metric_threshold_and_recurring_review_is_accepted(self):
        self.assertTrue(
            revisit_when_is_discriminating(
                "activation_rate below +1.0pp at the 2026-Q4 review"
            )
        )

    def test_duration_window_is_accepted(self):
        self.assertTrue(revisit_when_is_discriminating("churn above 5% for 8 weeks"))

    def test_bare_duration_reassessment_is_accepted(self):
        self.assertTrue(revisit_when_is_discriminating("reassess in 30 days"))

    def test_date_deadline_window_is_accepted(self):
        self.assertTrue(
            revisit_when_is_discriminating("by 2026-Q4 if CAC exceeds $40")
        )

    def test_open_ended_state_change_is_rejected(self):
        self.assertFalse(revisit_when_is_discriminating("when the market changes"))

    def test_as_needed_is_rejected(self):
        self.assertFalse(revisit_when_is_discriminating("as needed"))

    def test_vague_refusal_prose_is_rejected(self):
        self.assertFalse(revisit_when_is_discriminating("if things look bad"))

    def test_blank_is_rejected(self):
        self.assertFalse(revisit_when_is_discriminating(""))

    def test_placeholder_is_rejected(self):
        self.assertFalse(
            revisit_when_is_discriminating("<the condition for revisiting this>")
        )

    def test_refusal_token_is_rejected(self):
        self.assertFalse(revisit_when_is_discriminating("tbd"))

    def test_discriminating_but_windowless_is_rejected(self):
        """A falsifier-shaped value with no time anchor: revisit_when needs MORE
        than falsifier_is_discriminating alone."""
        self.assertTrue(falsifier_is_discriminating("activation_rate below +1.0pp"))
        self.assertFalse(
            revisit_when_is_discriminating("activation_rate below +1.0pp")
        )

    def test_good_fixture_falsifier_stays_discriminating_and_unperturbed(self):
        """The good fixture's own estimand falsifier stays True under
        falsifier_is_discriminating — proving the sibling predicate did not
        alter the shared function's behaviour on the real accepted value."""
        self.assertTrue(falsifier_is_discriminating(_GOOD_ESTIMAND_FALSIFIER))


if __name__ == "__main__":
    unittest.main()
