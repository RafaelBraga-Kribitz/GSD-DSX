"""Repo-integrity invariant: the per-function snippet catalog
``references/chart-snippets.md`` ROUTES to existing finding codes by name and
never RESTATES a numeric gate threshold. Covers REQ-P23-04 and D-P23-04.

Two properties, both machine-checked so the catalog cannot drift from the gate:

1. **Cited codes exist.** Every ``DSX-<FAMILY>-<n>`` token the snippet catalog
   names must be a code that is actually defined in ``references/finding-codes.md``
   -- a mistyped or invented code (an ungrounded route) turns this red
   (T-23-08). Non-vacuity: the catalog must cite at least one code, so a catalog
   that routes to nothing cannot pass silently.

2. **No threshold restated.** No snippet may write the pie/donut slice maximum
   (``MAX_PIE_SLICES``) or the categorical-colour maximum
   (``MAX_CATEGORICAL_COLORS``) as a literal next to its threshold noun --
   routing by code name (``DSX-VIZ-040`` / ``DSX-VIZ-050``) is required instead,
   so ``dsx/checks/viz.py`` stays the single source of truth (T-23-06,
   D-P23-04). The forbidden values are read LIVE from the ``viz.py`` constants
   at runtime and the regexes are built from those integers -- nothing is
   transcribed here, so if ``viz.py`` changes a limit this guard tracks it (that
   live derivation is the non-vacuity anchor for property 2).

Off the gate path by construction (``tests/`` is never in
``dsx.cli.GATE_PROFILES``' import closure): this reads Markdown, it does not
extend what the gate admits. Every read is CRLF-safe -- ``_ROW_RE`` is the same
non-line-anchored shape ``tests/test_finding_catalogue_invariant.py`` uses, and
the restatement scan runs over the raw text without line anchoring, so a
``\r\n`` line ending never hides or invents a hit.

Run: python -m unittest tests.test_snippet_catalog_routing -v
"""

from __future__ import annotations

import pathlib
import re
import sys
import unittest

_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# Live threshold constants -- imported, never transcribed (D-P23-04). The
# forbidden-restatement regexes below are built from these integer VALUES, so
# the guard tracks viz.py rather than a copy of it.
from dsx.checks.viz import MAX_CATEGORICAL_COLORS, MAX_PIE_SLICES

_REFS = _ROOT / "references"
_SNIPPETS = _REFS / "chart-snippets.md"
_FINDING_CODES = _REFS / "finding-codes.md"

# Every finding-codes.md row is `| `DSX-<FAMILY>-<digits>` | ...`. Same shape as
# tests/test_finding_catalogue_invariant.py::_ROW_RE -- not line anchored, so
# it is agnostic to \n vs \r\n.
_ROW_RE = re.compile(r"\|\s*`(DSX-[A-Z]+-\d+)`\s*\|")
# A cited token anywhere in the snippet catalog (prose, "Gate-enforced:" lines,
# code comments). Bare token, no backticks required.
_CITE_RE = re.compile(r"DSX-[A-Z]+-\d+")


def _read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


class TestSnippetCatalogRouting(unittest.TestCase):
    def test_cited_codes_are_all_defined(self):
        """Every code the catalog names is a real, defined finding code.

        cited (set of tokens in chart-snippets.md) must be non-empty and a
        subset of defined (set of codes finding-codes.md declares). A route to a
        code that does not exist is an ungrounded citation (T-23-08).
        """
        self.assertTrue(
            _SNIPPETS.exists(),
            f"{_SNIPPETS} does not exist -- author the snippet catalog (RED until Task 2)",
        )
        defined = set(_ROW_RE.findall(_read(_FINDING_CODES)))
        self.assertTrue(defined, "finding-codes.md parsed to an empty defined set")
        cited = set(_CITE_RE.findall(_read(_SNIPPETS)))
        self.assertTrue(
            cited,
            "chart-snippets.md cites no finding code -- a catalog that routes to "
            "nothing must not pass vacuously (non-vacuity anchor)",
        )
        undefined = cited - defined
        self.assertFalse(
            undefined,
            f"chart-snippets.md cites codes not defined in finding-codes.md: "
            f"{sorted(undefined)}",
        )

    def test_no_snippet_restates_a_live_viz_threshold(self):
        """No snippet writes a live viz.py limit as a literal near its noun.

        The forbidden values come from the imported MAX_PIE_SLICES /
        MAX_CATEGORICAL_COLORS constants, and the patterns are constructed from
        those integers at runtime -- the number is never typed into this test.
        Route by code name (DSX-VIZ-040 / DSX-VIZ-050) instead (D-P23-04).
        """
        self.assertTrue(
            _SNIPPETS.exists(),
            f"{_SNIPPETS} does not exist -- author the snippet catalog (RED until Task 2)",
        )
        # Sanity: the imports resolved to usable positive integers (structural,
        # not a transcription of 5/7).
        self.assertIsInstance(MAX_PIE_SLICES, int)
        self.assertIsInstance(MAX_CATEGORICAL_COLORS, int)
        self.assertGreater(MAX_PIE_SLICES, 0)
        self.assertGreater(MAX_CATEGORICAL_COLORS, 0)

        text = _read(_SNIPPETS)
        p = MAX_PIE_SLICES
        c = MAX_CATEGORICAL_COLORS
        # A restatement = the live integer standing alone (\b..\b, so it does not
        # match inside a code like DSX-VIZ-050 or a hex/year) within a short
        # window of its threshold noun, in either order.
        forbidden = {
            f"slice-count restatement ({p} near a slice word)":
                re.compile(rf"\b{p}\b[^\n]{{0,25}}slic|slic\w*[^\n]{{0,25}}\b{p}\b", re.I),
            f"colour-count restatement ({c} near a colour/hue word)":
                re.compile(
                    rf"\b{c}\b[^\n]{{0,25}}(?:colou?rs?|hues?)"
                    rf"|(?:colou?rs?|hues?)[^\n]{{0,25}}\b{c}\b",
                    re.I,
                ),
        }
        for label, pat in forbidden.items():
            m = pat.search(text)
            self.assertIsNone(
                m,
                f"chart-snippets.md restates a live viz.py threshold [{label}] -- "
                f"route by code name instead. Matched span: "
                f"{m.group(0)!r}" if m else "",
            )


if __name__ == "__main__":
    unittest.main()
