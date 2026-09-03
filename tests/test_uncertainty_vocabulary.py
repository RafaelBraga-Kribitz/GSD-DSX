"""DSX-VIZ-071 gate behaviour: a declared ``uncertainty_mark`` must be one of
Wilke's ten §5.6 members (Phase 22, REQ-P22-05).

Complementary to the property-based DSX-VIZ-070 (``_check_uncertainty``), which
asks whether uncertainty is shown at all; DSX-VIZ-071 asks whether the chosen
mark is a recognised member of the closed §5.6 vocabulary. Pure membership — no
computed threshold.

# D-05: DSX-VIZ-071

Run: python -m unittest tests.test_uncertainty_vocabulary -v
"""

from __future__ import annotations

import unittest

from dsx.checks.viz import check as viz_check


def _viz071(uncertainty_mark=None) -> list:
    """A one-visual spec declaring an uncertainty relationship; return the
    DSX-VIZ-071 findings only. Mirrors the _viz013 idiom in
    tests/test_viz_vocabulary_invariant.py."""
    visual = {"name": "estimate", "relationship": "uncertainty", "type": "error_bars"}
    if uncertainty_mark is not None:
        visual["uncertainty_mark"] = uncertainty_mark
    spec = {"visuals": [visual]}
    return [f for f in viz_check(spec).findings if f.code == "DSX-VIZ-071"]


class TestUncertaintyVocabularyGate(unittest.TestCase):
    def test_non_member_uncertainty_mark_fires(self):
        # "sparkline" is a real mark but not one of the ten §5.6 uncertainty
        # members, so declaring it as the uncertainty mark is refused.
        found = _viz071("sparkline")
        self.assertEqual(len(found), 1, "a non-member uncertainty_mark must fire DSX-VIZ-071")

    def test_member_uncertainty_mark_does_not_fire(self):
        self.assertEqual(
            _viz071("error_bars"), [], "a valid §5.6 member must not fire DSX-VIZ-071"
        )

    def test_absent_uncertainty_mark_is_silent(self):
        self.assertEqual(
            _viz071(None), [], "no uncertainty_mark field means the check is silent"
        )


if __name__ == "__main__":
    unittest.main()
