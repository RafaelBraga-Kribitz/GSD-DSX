"""REQ-P17-01: the two-proportion small-expected-cell alternative names
``boschloo_exact`` (reconcile-to-doc, D-04), and the code/doc are pinned so the
divergence class cannot recur silently.

Stdlib-only, CRLF-agnostic (whitespace-collapse, never line-anchored parsing).
This module mints no finding code, so it carries no ``# D-05:`` marker —
``boschloo_exact`` is a routing test-name string, not a DSX-STA-* code.
"""

import re
import unittest
from pathlib import Path

from dsx.checks.stats import NONPARAMETRIC_TESTS, recommend_test

ROOT = Path(__file__).resolve().parent.parent
TEST_SELECTION = ROOT / "references" / "test-selection.md"


def _leading_tokens(alternatives):
    """The test-name token before any parenthetical qualifier — mirrors
    recommend_test's own acceptable-alternatives logic (``alt.split(' ')[0]``)."""
    return [alt.split(" ")[0] for alt in alternatives]


class BoschlooReconciliationTest(unittest.TestCase):
    def test_two_proportion_alternative_names_boschloo_exact(self):
        rec = recommend_test("proportion", 2)
        # The primary returned test is unchanged.
        self.assertEqual(rec["test"], "two_proportion_z")
        # The small-expected-cell alternative now names boschloo_exact.
        self.assertIn("boschloo_exact", _leading_tokens(rec["alternatives"]))

    def test_boschloo_exact_added_without_dropping_fisher_exact(self):
        # Additive, not a replace: boschloo_exact joins; fisher_exact stays
        # (it is still the correct 3-plus-group sparse-cell alternative).
        self.assertIn("boschloo_exact", NONPARAMETRIC_TESTS)
        self.assertIn("fisher_exact", NONPARAMETRIC_TESTS)

    def test_doc_still_names_boschloo(self):
        # Doc<->code pin: references/test-selection.md (the already-correct side)
        # still names Boschloo — proving the doc names what the code now emits.
        collapsed = re.sub(r"\s+", " ", TEST_SELECTION.read_text(encoding="utf-8").replace("\r\n", "\n"))
        self.assertIn("Boschloo", collapsed)


if __name__ == "__main__":
    unittest.main()
