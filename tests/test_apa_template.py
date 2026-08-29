"""REQ-P15-05: the optional research-domain APA results-table template exists with
the APA column vocabulary and the domain framing, and does not relax the
marketing-domain ship path. Stdlib-only, CRLF-agnostic. Mints nothing."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates" / "APA-TABLE-research.md"


class ApaTemplateTest(unittest.TestCase):
    def setUp(self):
        self.text = TEMPLATE.read_text(encoding="utf-8")
        self.lower = self.text.lower()

    def test_template_exists(self):
        self.assertTrue(TEMPLATE.is_file())

    def test_carries_apa_column_vocabulary(self):
        # Several distinct APA columns must be present so an empty / non-APA file fails.
        self.assertIn("df", self.lower)
        self.assertTrue(
            "| p " in self.lower or "p value" in self.lower or "p-value" in self.lower,
            "p-value column token missing",
        )
        self.assertTrue(
            "ci" in self.lower or "confidence interval" in self.lower,
            "CI column token missing",
        )
        self.assertTrue(
            "effect size" in self.lower or "effect" in self.lower,
            "effect-size column token missing",
        )
        self.assertIn("statistic", self.lower)
        self.assertIn("note", self.lower)

    def test_frames_domain_and_leaves_marketing_ship_unchanged(self):
        self.assertIn("research", self.lower)
        self.assertIn("optional", self.lower)
        # Names the unchanged marketing ship contract.
        self.assertTrue(
            "nar" in self.lower and "fig" in self.lower and "clm" in self.lower,
            "must state the marketing NAR/FIG/CLM ship path is unchanged",
        )


if __name__ == "__main__":
    unittest.main()
