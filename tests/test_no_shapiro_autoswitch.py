"""REQ-P15-06 / D-07: no skill or gate auto-switches a test on a normality test.

Pins references/test-selection.md's fixed assumption order (independence → equal
variance → normality), the unconditional Welch recommendation, and normality as a
declared small-n property; and greps the gate + skill decision surface (dsx/ and
skills/ only — never tests/, never the untracked references/ academic paper) for
normality-test CALLS.

Stdlib-only, CRLF-safe (r"\\r?\\n", never bare \\n). This test mints nothing.
"""

import inspect
import re
import unittest
from pathlib import Path

import dsx.checks.stats as _stats

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


class NoAutoswitchEveryNewCategoryTest(unittest.TestCase):
    """The no-autoswitch (anti-two-stage) proof, made CATEGORY-COMPLETE and future-proof.

    Enumerates every public ``recommend_*`` router in ``dsx.checks.stats`` dynamically and
    proves each new-category router is DATALESS — its ``inspect.signature`` carries no
    ``data`` / ``n`` / distribution parameter, so it mechanically cannot inspect-then-pick
    a test (REQ-P18-06, extended to every routing family added in Phases 17-19). Because the
    enumeration is ``dir()``-based, a NEW category added later without a dataless router is
    caught automatically, and the anti-vacuity assertion stops a rename from silently
    emptying the proof.

    ``recommend_test`` is the ONE legacy router that legitimately consumes DECLARED shape
    fields (``normal`` / ``equal_variance`` / ``n_per_group`` / ``overdispersed``); it is
    intentionally EXCLUDED from the dataless proof and is instead covered by the
    Welch-unconditional and normality-declared assertions in ``TestSelectionOrderTest`` above.
    """

    # The data-then-pick surface a two-stage router would need. Absence of every one of
    # these parameter NAMES (whole-name set intersection, not substring) is the mechanical
    # proof a router cannot inspect the data before choosing.
    _BANNED = frozenset(
        {"data", "n", "n_groups", "paired", "normal", "equal_variance",
         "n_per_group", "distribution", "overdispersed"}
    )
    # Every routing family shipped through Phase 19; the enumeration must be a superset of
    # this so a rename/refactor cannot make the proof pass vacuously.
    _KNOWN_NEW_CATEGORY = frozenset(
        {"recommend_association", "recommend_rm", "recommend_trend", "recommend_resampling",
         "recommend_posthoc", "recommend_variance_role", "recommend_power",
         "recommend_proportion_ci"}
    )

    def _routers(self):
        routers = {}
        for name in dir(_stats):
            if not name.startswith("recommend_"):
                continue
            fn = getattr(_stats, name)
            if callable(fn) and inspect.isfunction(fn):
                routers[name] = fn
        return routers

    def test_enumeration_is_non_vacuous_and_covers_every_new_category(self):
        routers = self._routers()
        self.assertIn("recommend_test", routers,
                      "recommend_test must be enumerated so the legacy/new-category split is real")
        new_category = set(routers) - {"recommend_test"}
        missing = self._KNOWN_NEW_CATEGORY - new_category
        self.assertFalse(
            missing,
            f"a known new-category router is missing from the enumeration (rename?): {sorted(missing)}",
        )

    def test_every_new_category_router_is_dataless(self):
        routers = self._routers()
        offenders = []
        for name in sorted(set(routers) - {"recommend_test"}):
            params = set(inspect.signature(routers[name]).parameters)
            leaked = params & self._BANNED
            if leaked:
                offenders.append(f"{name}{sorted(leaked)}")
        self.assertEqual(
            offenders, [],
            "data/n/distribution parameter(s) on new-category router(s) — a two-stage "
            f"(inspect-then-pick) surface has been reintroduced: {offenders}",
        )

    def test_recommend_test_is_the_only_declared_shape_router(self):
        # recommend_test legitimately consumes DECLARED shape fields; it is excluded from the
        # dataless proof above and covered by the Welch-unconditional/normality-declared
        # assertions. This pins that split: recommend_test DOES carry declared-shape params.
        params = set(inspect.signature(_stats.recommend_test).parameters)
        self.assertTrue(
            params & self._BANNED,
            "recommend_test is expected to carry declared-shape parameters (it is the "
            "legacy router excluded from the dataless proof); none found",
        )


if __name__ == "__main__":
    unittest.main()
