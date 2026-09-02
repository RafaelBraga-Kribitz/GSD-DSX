"""REQ-P19-03 doc-presence proof: the categorical rows minted NOTHING.

REQ-P19-03 (categorical) is delivered in full as DOCUMENTATION ONLY — rows plus
one DEPRECATED Yates row, one SURFACED CMH-stratification row, one log-linear
POINTER row, and one Fisher-Freeman-Halton honesty footnote — and mints ZERO
finding codes. This module proves both halves:

  1. the four load-bearing categorical rows/footnote are present in
     references/test-selection.md; and
  2. the finding-code catalogue declared total is STILL exactly 265 — the
     categorical section (and the whole of Wave 1) added no report.add site.

CRLF discipline (repo CLAUDE.md): this checkout may hold ``\r\n`` line endings, so
every assertion runs over a whitespace-collapsed, ``\r\n``-normalised form; no
bare ``\n``-anchored pattern is used. Stdlib only. This test mints nothing.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_TEST_SELECTION = ROOT / "references" / "test-selection.md"
_CATALOGUE = ROOT / "references" / "finding-codes.md"

# The pinned Wave-1 total — REQ-P19-03 and all of Wave 1 mint nothing over the
# Phase-18 baseline of 265 (kept in lockstep with
# tests/test_finding_catalogue_invariant.py::_EXPECTED_TOTAL).
_EXPECTED_TOTAL = 265
_TOTAL_RE = re.compile(r"\*\*Total:\s*(\d+)\s*codes\.\*\*")


def _flat(path: Path) -> str:
    """CRLF-agnostic, whitespace-collapsed, lowercased form for substring tests."""
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8").replace("\r\n", "\n")).lower()


class CategoricalRowsPresentTest(unittest.TestCase):
    def setUp(self):
        self.flat = _flat(_TEST_SELECTION)

    def test_categorical_section_header_present(self):
        self.assertIn("## categorical", self.flat)

    def test_yates_deprecated_row_present(self):
        self.assertIn("yates", self.flat)
        self.assertIn("deprecated", self.flat)
        # The Yates row routes to the N-1 chi-square replacement.
        self.assertIn("n-1 chi-square", self.flat)

    def test_cmh_surfaced_stratification_row_present(self):
        self.assertTrue(
            "cmh" in self.flat or "cochran-mantel-haenszel" in self.flat,
            "the CMH surfaced-stratification row is missing",
        )
        self.assertIn("surfaced", self.flat)

    def test_log_linear_pointer_row_present(self):
        self.assertIn("log-linear", self.flat)
        self.assertIn("pointer", self.flat)

    def test_fisher_freeman_halton_footnote_present(self):
        self.assertIsNotNone(
            re.search(r"fisher.freeman.halton", self.flat),
            "the Fisher-Freeman-Halton honesty footnote is missing",
        )


class CategoricalMintedNothingTest(unittest.TestCase):
    def test_catalogue_still_declares_exactly_265(self):
        collapsed = " ".join(_CATALOGUE.read_text(encoding="utf-8").split())
        match = _TOTAL_RE.search(collapsed)
        self.assertIsNotNone(match, "no '**Total: N codes.**' line found in the catalogue")
        self.assertEqual(
            int(match.group(1)), _EXPECTED_TOTAL,
            f"catalogue declares {match.group(1)} codes, expected {_EXPECTED_TOTAL} — "
            "REQ-P19-03 (and all of Wave 1) must mint zero codes; a change here means a "
            "report.add site slipped in",
        )


if __name__ == "__main__":
    unittest.main()
