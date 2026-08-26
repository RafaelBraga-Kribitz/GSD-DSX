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

from pathlib import Path as _Path

from dsx.checks import coherence  # noqa: E402
from dsx.findings import Report, Severity  # noqa: E402
from dsx.frame import val  # noqa: E402
from dsx.loader import load  # noqa: E402
from dsx.spec import (  # noqa: E402
    falsifier_is_discriminating,
    revisit_when_is_discriminating,
)

_GOOD_FIXTURE_PATH = _Path(__file__).resolve().parent.parent / "examples" / "good-ANALYSIS-SPEC.yaml"

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

    def test_metric_with_recurring_review_is_accepted(self):
        """A metric+threshold anchored to a digit-free recurring checkpoint is
        accepted — the residual after stripping "quarterly review" still carries
        the comparison, so a real condition + a time anchor passes (WR-02)."""
        self.assertTrue(
            revisit_when_is_discriminating(
                "activation_rate below +1.0pp at the next quarterly review"
            )
        )

    def test_bare_duration_reassessment_without_metric_is_rejected(self):
        """WR-02 (11.2 code review, §4 persona round): "reassess in 30 days"
        carries a time anchor but NO metric/threshold — the "30" is the
        duration's own count, not a discriminating value. It must be rejected,
        consistent with DSX-COH-040's contract ("a named metric, a threshold,
        AND a time anchor") and with the digit-free recurring-token path
        ("at the next quarterly review"), which was already rejected. This
        inverts the former test_bare_duration_reassessment_is_accepted, whose
        pass depended on the window's own digit masquerading as a threshold."""
        self.assertFalse(revisit_when_is_discriminating("reassess in 30 days"))

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


# ── DSX-COH-040: _check_revisit_completeness ─────────────────────────────────


def codes(report: Report) -> set[str]:
    return {f.code for f in report.findings}


def _spec(**overrides: object) -> dict:
    base: dict = {
        "question_type": "causal",
        "decision": {},
        "design": {},
    }
    base.update(overrides)
    return base


class TestRevisitCompleteness(unittest.TestCase):
    """DSX-COH-040: one code, both triggers (D-07)."""

    # D-05: DSX-COH-040
    def test_prescriptive_question_blank_revisit_when_fires_coh040(self):
        report = coherence.check(
            _spec(question_type="prescriptive", decision={}, design={})
        )
        coh040 = [f for f in report.findings if f.code == "DSX-COH-040"]
        self.assertEqual(len(coh040), 1)
        self.assertEqual(coh040[0].severity, Severity.CRITICAL)
        self.assertEqual(coh040[0].where, "spec.decision.revisit_when")

    def test_experiment_design_blank_revisit_when_fires_coh040(self):
        report = coherence.check(
            _spec(
                question_type="causal",
                decision={},
                design={"kind": "experiment"},
            )
        )
        self.assertIn("DSX-COH-040", codes(report))

    def test_both_triggers_true_fires_exactly_one_coh040(self):
        report = coherence.check(
            _spec(
                question_type="prescriptive",
                decision={},
                design={"kind": "experiment"},
            )
        )
        coh040 = [f for f in report.findings if f.code == "DSX-COH-040"]
        self.assertEqual(len(coh040), 1)

    def test_non_discriminating_revisit_when_under_prescriptive_fires_coh040(self):
        report = coherence.check(
            _spec(
                question_type="prescriptive",
                decision={"revisit_when": "when the market changes"},
                design={},
            )
        )
        self.assertIn("DSX-COH-040", codes(report))

    def test_valid_windowed_revisit_when_produces_no_coh040(self):
        report = coherence.check(
            _spec(
                question_type="prescriptive",
                decision={
                    "revisit_when": "activation_rate below +1.0pp at the 2026-Q4 review"
                },
                design={},
            )
        )
        self.assertNotIn("DSX-COH-040", codes(report))

    def test_placeholder_revisit_when_fires_coh040(self):
        report = coherence.check(
            _spec(
                question_type="prescriptive",
                decision={"revisit_when": "<the condition for revisiting this>"},
                design={},
            )
        )
        self.assertIn("DSX-COH-040", codes(report))

    def test_refusal_token_revisit_when_fires_coh040(self):
        report = coherence.check(
            _spec(
                question_type="prescriptive",
                decision={"revisit_when": "tbd"},
                design={},
            )
        )
        self.assertIn("DSX-COH-040", codes(report))

    def test_descriptive_non_experiment_spec_with_no_revisit_when_does_not_fire(self):
        report = coherence.check(
            _spec(question_type="descriptive", decision={}, design={})
        )
        self.assertNotIn("DSX-COH-040", codes(report))


# ── Task 3: fixture prophylaxis + the DSX-VAL-011-unchanged regression ───────


class TestGoodFixtureProphylaxis(unittest.TestCase):
    """The good fixture's own revisit_when is discriminating and window-anchored,
    it clears coherence.check(), and the estimand falsifier's DSX-VAL-011 firing
    set is unperturbed by the sibling predicate (D-07, RESEARCH landmine b)."""

    def test_good_fixture_revisit_when_is_discriminating(self):
        spec = load(_GOOD_FIXTURE_PATH)
        revisit_when = spec.get("decision", {}).get("revisit_when")
        self.assertTrue(revisit_when_is_discriminating(revisit_when))

    def test_good_fixture_draws_no_coh040(self):
        spec = load(_GOOD_FIXTURE_PATH)
        report = coherence.check(spec)
        self.assertNotIn("DSX-COH-040", codes(report))

    def test_good_fixture_val_011_firing_set_is_unchanged(self):
        """Regression: the good fixture's estimand falsifier still does not
        fire DSX-VAL-011 — proving falsifier_is_discriminating was not
        perturbed by adding the sibling predicate or the fixture's new
        revisit_when field."""
        spec = load(_GOOD_FIXTURE_PATH)
        report = val.check(spec)
        self.assertNotIn("DSX-VAL-011", codes(report))


if __name__ == "__main__":
    unittest.main()
