"""Repo-integrity invariant: the 5-layer question->chart selection heuristic
ships as route-and-cite edits into the two existing reference files plus the
visualize skill, never a parallel decision tree, and chart-selection.md's
perceptual line carries the D-1 six-rank-with-ties correction (not the
superseded strict chain, no stray "density" channel). Covers REQ-P22-04 and the
REQ-P22-05-adjacent Pitfall-3 correction.

Off the gate path by construction (``tests/`` is never in
``dsx.cli.GATE_PROFILES``' import closure): this reads Markdown, it does not
extend what the gate admits. Every match here is CRLF-safe -- the text is
whitespace-collapsed before matching multi-word phrases, so a ``\r\n`` line
ending or an incidental wrap never hides or invents a hit.

Run: python -m unittest tests.test_selection_heuristic_docs -v
"""

from __future__ import annotations

import pathlib
import re
import unittest

from dsx.checks.viz import RELATIONSHIP_CHARTS

_ROOT = pathlib.Path(__file__).resolve().parents[1]
_REFS = _ROOT / "references"
_CHART_SELECTION = _REFS / "chart-selection.md"
_QUESTION_TAXONOMY = _REFS / "question-taxonomy.md"
_SKILL = _ROOT / "skills" / "dsx-visualize" / "SKILL.md"

# The eleven relationship names the skill's <method> step 1 enumerates by hand.
# Plan 22-01 added the eleventh ("uncertainty"); the skill must name it or the
# agent-facing surface and the live vocabulary disagree.
_RELATIONSHIPS = (
    "comparison",
    "trend",
    "part_to_whole",
    "distribution",
    "correlation",
    "deviation",
    "ranking",
    "flow",
    "geographic",
    "composition_over_time",
    "uncertainty",
)

# Never HQ-27-submitted -- must not back any heuristic citation (Research Open
# Question 1, option (a): cite only Munzner ch.3 + the FT nine-category axis).
_FORBIDDEN_CITATION_TOKENS = ("abela", "graph selection matrix")

# Names that would mark a *parallel* standalone decision-tree document under
# references/ -- the "no second selection surface" structural guard (REQ-P22-04).
_DECISION_TREE_NAME_RE = re.compile(
    r"(decision[-_ ]?tree|selection[-_ ]?tree|chart[-_ ]?decision|decision[-_ ]?flow|flow ?chart)",
    re.IGNORECASE,
)


def _collapsed(path: pathlib.Path) -> str:
    """Whitespace-collapsed lowercase text: CRLF-agnostic, wrap-agnostic."""
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8")).lower()


class TestSelectionHeuristicDocs(unittest.TestCase):
    def test_skill_enumerates_eleven_relationships(self):
        """(a) SKILL.md step 1 names all eleven relationships, incl. uncertainty."""
        skill = _SKILL.read_text(encoding="utf-8")
        missing = [r for r in _RELATIONSHIPS if r not in skill]
        self.assertEqual(missing, [], f"SKILL.md missing relationship names: {missing}")
        # Non-vacuity: the eleventh key is the whole point of this ripple.
        self.assertIn("uncertainty", skill)

    def test_doc_relationship_names_bind_to_the_live_dict_both_directions(self):
        """(a2) REQ-P24-03 (GA-3) direct drift-guard: the hand-maintained
        relationship enumeration this file uses to check the docs must equal the
        LIVE ``RELATIONSHIP_CHARTS`` keys in *both* directions -- no live key
        missing from the doc list, no doc name absent from the live dict. Adding
        a twelfth relationship key, or renaming one, now fails HERE directly,
        not only transitively via test_viz_vocabulary_invariant's len==11 pin."""
        self.assertEqual(
            set(RELATIONSHIP_CHARTS),
            set(_RELATIONSHIPS),
            "chart-selection relationship vocabulary has drifted from the live "
            "dsx.checks.viz.RELATIONSHIP_CHARTS keys",
        )

    def test_perceptual_line_is_d1_six_rank_with_ties(self):
        """(b) chart-selection.md carries D-1's tie language + the Cleveland &
        McGill 1984 citation, and NOT the superseded strict chain nor a stray
        'density' channel among the perceptual ranks (Pitfall 3)."""
        low = _collapsed(_CHART_SELECTION)
        # Present: tie language + the 1984 citation tokens.
        self.assertTrue("tie" in low or "tied" in low, "no tie language in perceptual line")
        self.assertIn("cleveland", low, "Cleveland & McGill citation missing")
        self.assertIn("1984", low, "the 1984 locator is missing")
        self.assertTrue(
            "p.536" in low or "p.537" in low,
            "the p.536 list / p.537 tie-caveat locator is missing",
        )
        # Absent: the superseded strict chain that places colour saturation
        # before volume (match both arrow glyphs, whitespace-collapsed).
        self.assertNotIn("saturation → volume", low, "superseded ordering still present")
        self.assertNotIn("saturation -> volume", low, "superseded ordering still present")
        # Absent: 'density' as a ranked channel (arrow-chain member or tied-list
        # member). The correction is ALLOWED to *name* density to say it is
        # absent ("Density is not one of these channels"); it may never list it
        # AS a rank -- so only the adjacency-to-a-rank forms are forbidden.
        self.assertIsNone(
            re.search(r"(?:→|->|,)\s*density|density\s*(?:→|->)", low),
            "'density' appears as a ranked perceptual channel (D-1: absent from the 1984 paper)",
        )

    def test_both_surfaces_point_at_the_catalog(self):
        """(c) chart-selection.md and SKILL.md both reference chart-catalog.md."""
        self.assertIn("chart-catalog.md", _CHART_SELECTION.read_text(encoding="utf-8"))
        self.assertIn("chart-catalog.md", _SKILL.read_text(encoding="utf-8"))

    def test_l1_layer_cites_munzner_and_routes_onward(self):
        """(d) question-taxonomy.md carries the Munzner-cited L1 pointer that
        routes to chart-selection.md (reuse, not a restated table)."""
        q = _QUESTION_TAXONOMY.read_text(encoding="utf-8")
        self.assertIn("munzner", q.lower(), "L1 pointer does not cite Munzner")
        self.assertIn("chart-selection.md", q, "L1 pointer does not route to chart-selection.md")

    def test_no_parallel_decision_tree_file(self):
        """(e) No standalone decision-tree document exists under references/ --
        the heuristic is edits into the existing files, never a second surface."""
        offenders = [
            p.name
            for p in _REFS.glob("*.md")
            if _DECISION_TREE_NAME_RE.search(p.name)
        ]
        self.assertEqual(offenders, [], f"a parallel decision-tree file exists: {offenders}")

    def test_no_forbidden_heuristic_citations(self):
        """(f) None of the three edited files cites Abela 2008 or Few's Graph
        Selection Matrix (never HQ-27-submitted)."""
        for path in (_CHART_SELECTION, _QUESTION_TAXONOMY, _SKILL):
            low = _collapsed(path)
            for token in _FORBIDDEN_CITATION_TOKENS:
                self.assertNotIn(
                    token, low, f"{path.name} cites the un-submitted source {token!r}"
                )


if __name__ == "__main__":
    unittest.main()
