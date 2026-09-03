"""Style-file license/attribution header presence (REQ-P23-01, GA-1).

Repo-integrity test (off the gate path, no ``report.add``): each of the four
``styles/*.mplstyle`` files must open with a license/attribution header block
carrying a ``Source:`` line (whose value includes a URL), a ``License:`` line, a
``Vendoring:`` line, and a ``Font:`` line naming the vendored Lato face. The two
reimplemented styles (``dsx-econ``, ``dsx-bbc``) additionally carry the
``Reimplemented from published doctrine`` / ``not affiliated`` /
``no proprietary font`` lines (GA-1). These header lines are the machine proof
that REQ-P23-01's per-file license-audit discipline is met.

If a style file is missing or its header block is absent, this module goes red.

CRLF discipline (repo CLAUDE.md): this checkout may hold ``\r\n`` line endings,
so the file is split on ``r"\r?\n"`` and matched per stripped line, never by a
bare ``\n``-anchored pattern that a CRLF checkout would silently break.

Run:  python -m unittest tests.test_style_headers -v
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STYLES_DIR = ROOT / "styles"

# The four style files GA-1 pins; the last two additionally carry the
# reimplemented-from-doctrine header lines.
_ALL_STYLES = ("dsx-538", "dsx-urban", "dsx-econ", "dsx-bbc")
_REIMPLEMENTED = ("dsx-econ", "dsx-bbc")

# Header-line patterns, matched per stripped comment line (case-insensitive so a
# `# source:` and `# Source:` both count). Source must carry a URL.
_SOURCE_RE = re.compile(r"source\s*:\s*.*http", re.IGNORECASE)
_LICENSE_RE = re.compile(r"license\s*:\s*\S", re.IGNORECASE)
_VENDORING_RE = re.compile(r"vendoring\s*:\s*\S", re.IGNORECASE)
_FONT_RE = re.compile(r"font\s*:\s*.*lato", re.IGNORECASE)

# The three phrases the reimplemented styles must state (case-insensitive).
_REIMPL_PHRASES = (
    "reimplemented from published doctrine",
    "not affiliated",
    "no proprietary font",
)


def _comment_block(path: Path) -> str:
    """The leading run of comment lines (stripped `#` prefix), joined by newline.

    A header line ends the block only at the first content (non-blank,
    non-comment) line, so blank separators inside the header are tolerated.
    CRLF-safe: splits on ``\\r?\\n``.
    """
    text = path.read_text(encoding="utf-8")
    out: list[str] = []
    for raw in re.split(r"\r?\n", text):
        stripped = raw.strip()
        if stripped == "":
            # A blank line inside the leading comment run is allowed; keep going
            # only if we have not yet seen a content line.
            out.append("")
            continue
        if stripped.startswith("#"):
            out.append(stripped.lstrip("#").strip())
            continue
        break  # first real key: value line -> header block is over
    return "\n".join(out)


class TestStyleHeaders(unittest.TestCase):
    def test_every_style_carries_its_license_header(self):
        checked = 0
        for stem in _ALL_STYLES:
            path = STYLES_DIR / f"{stem}.mplstyle"
            with self.subTest(style=stem):
                self.assertTrue(path.exists(), f"missing style file: {path}")
                header = _comment_block(path)
                lines = header.splitlines()
                self.assertTrue(
                    any(_SOURCE_RE.search(ln) for ln in lines),
                    f"{stem}: header has no `Source:` line carrying a URL",
                )
                self.assertTrue(
                    any(_LICENSE_RE.search(ln) for ln in lines),
                    f"{stem}: header has no `License:` line",
                )
                self.assertTrue(
                    any(_VENDORING_RE.search(ln) for ln in lines),
                    f"{stem}: header has no `Vendoring:` line",
                )
                self.assertTrue(
                    any(_FONT_RE.search(ln) for ln in lines),
                    f"{stem}: header has no `Font:` line naming Lato",
                )
                checked += 1
        # Non-vacuity: exactly the four expected files were reached and checked.
        self.assertEqual(checked, 4, "expected exactly four style files checked")

    def test_reimplemented_styles_carry_the_doctrine_disclaimer(self):
        checked = 0
        for stem in _REIMPLEMENTED:
            path = STYLES_DIR / f"{stem}.mplstyle"
            with self.subTest(style=stem):
                self.assertTrue(path.exists(), f"missing style file: {path}")
                header = _comment_block(path).lower()
                for phrase in _REIMPL_PHRASES:
                    self.assertIn(
                        phrase,
                        header,
                        f"{stem}: header missing required phrase '{phrase}'",
                    )
                checked += 1
        # Non-vacuity: both reimplemented files were reached.
        self.assertEqual(checked, 2, "expected exactly two reimplemented styles checked")


if __name__ == "__main__":
    unittest.main()
