"""REQ-P15-06 / D-07: no skill or gate auto-switches a test on a normality test.

Pins references/test-selection.md's fixed assumption order (independence → equal
variance → normality), the unconditional Welch recommendation, and normality as a
declared small-n property; and greps the gate + skill decision surface (dsx/ and
skills/ only — never tests/, never the untracked references/ academic paper) for
normality-test CALLS.

Stdlib-only, CRLF-safe (r"\\r?\\n", never bare \\n). This test mints nothing.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEST_SELECTION = ROOT / "references" / "test-selection.md"

# A normality-test CALL on a decision path (not a prose mention of Shapiro-Wilk).
_NORMALITY_CALL_TOKENS = ("scipy.stats", "shapiro(", "normaltest(", "anderson(", "kstest(")


def _collapse(text: str) -> str:
    """CRLF-agnostic, whitespace-collapsed, lowercased form for substring order tests."""
    return re.sub(r"\s+", " ", text.replace("\r\n", "\n")).lower()


class TestSelectionOrderTest(unittest.TestCase):
    def setUp(self):
        self.flat = _collapse(TEST_SELECTION.read_text(encoding="utf-8"))
        # Scope order assertions to the "in order of how much they matter" section.
        marker = "in order of how much they matter"
        self.assertIn(marker, self.flat)
        self.section = self.flat[self.flat.index(marker):]

    def test_test_selection_assumption_order_is_fixed(self):
        i_indep = self.section.index("independence")
        i_var = self.section.index("equal variance")
        i_norm = self.section.index("normality")
        self.assertLess(i_indep, i_var, "independence must precede equal variance")
        self.assertLess(i_var, i_norm, "equal variance must precede normality")

    def test_continuous_two_group_recommendation_is_welch_unconditional(self):
        # The equal-variance response is Welch, stated unconditionally.
        self.assertIn("welch", self.section)
        self.assertIn("use welch", self.section)
        # No "if <a computed variance test> then <switch the test>" conditional.
        self.assertIsNone(
            re.search(r"if\b[^.]*variance test[^.]*(then|switch|use)", self.flat),
            "the recommended test must not branch on a computed variance test",
        )

    def test_normality_is_declared_not_tool_run(self):
        # Normality is a declared shape+n property: matters at small n only, not a tool-run test.
        self.assertIn("matters at small n only", self.section)
        self.assertIn("irrelevant above", self.section)


class DecisionSurfaceScanTest(unittest.TestCase):
    def _decision_surface_files(self):
        files = []
        for base in (ROOT / "dsx", ROOT / "skills"):
            if not base.is_dir():
                continue
            for pattern in ("*.py", "*.md"):
                files.extend(base.rglob(pattern))
        return files

    def test_no_normality_test_call_on_the_decision_surface(self):
        files = self._decision_surface_files()
        # Anti-vacuity: the scan set is non-empty and spans both dsx/ and skills/.
        self.assertTrue(files, "decision-surface scan set is empty")
        parts = {tuple(p.relative_to(ROOT).parts) for p in files}
        self.assertTrue(any(pt and pt[0] == "dsx" for pt in parts), "no dsx/ module scanned")
        self.assertTrue(any(pt and pt[0] == "skills" for pt in parts), "no skills/ file scanned")

        offenders = []
        for path in files:
            text = path.read_text(encoding="utf-8", errors="replace")
            for token in _NORMALITY_CALL_TOKENS:
                if token in text:
                    offenders.append(f"{path.relative_to(ROOT)} :: {token}")
        self.assertEqual(offenders, [], f"normality-test call(s) on the decision surface: {offenders}")


if __name__ == "__main__":
    unittest.main()
