"""WCAG-AA contrast verification for the style-file palettes (REQ-P23-05, GA-1).

Repo-integrity test (off the gate path, no ``report.add``; stdlib-only, no
matplotlib import — it reads the plain-text ``.mplstyle`` files). For each of the
four ``styles/*.mplstyle`` files it parses the ``axes.prop_cycle`` hex list and
the ``axes.facecolor`` / ``figure.facecolor`` / ``text.color`` /
``axes.labelcolor`` single hexes, then asserts:

  * every series colour clears WCAG 1.4.11 graphical-object contrast (>= 3:1)
    against that file's ``axes.facecolor``; and
  * text/label colours clear WCAG 1.4.3 text contrast (>= 4.5:1) against
    ``figure.facecolor``.

The relative-luminance and contrast-ratio arithmetic is the ~15-line stdlib
WCAG 2.x formula (W3C Understanding SC 1.4.3), not a third-party dependency
(D-01 in spirit; this is a build-time property test, not a gate code — D-P23-04).

CRLF discipline (repo CLAUDE.md): the file is split on ``r"\r?\n"`` and parsed
per stripped line, never by a bare ``\n``-anchored pattern.

Run:  python -m unittest tests.test_style_wcag_contrast -v
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STYLES_DIR = ROOT / "styles"

_ALL_STYLES = ("dsx-538", "dsx-urban", "dsx-econ", "dsx-bbc")

_HEX6 = re.compile(r"([0-9A-Fa-f]{6})")


def _relative_luminance(hexstr: str) -> float:
    """WCAG relative luminance of a ``RRGGBB`` (optionally ``#``-prefixed) hex."""
    h = hexstr.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    chans = []
    for c in (r, g, b):
        cs = c / 255.0
        chans.append(cs / 12.92 if cs <= 0.03928 else ((cs + 0.055) / 1.055) ** 2.4)
    return 0.2126 * chans[0] + 0.7152 * chans[1] + 0.0722 * chans[2]


def _contrast(hex_a: str, hex_b: str) -> float:
    """WCAG contrast ratio between two hex colours (order-independent)."""
    la, lb = _relative_luminance(hex_a), _relative_luminance(hex_b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def _parse_style(path: Path) -> dict:
    """Parse an ``.mplstyle`` file into the palette values this test checks.

    Returns a dict with ``cycle`` (list of hex str) and single-hex values for
    ``axes.facecolor`` / ``figure.facecolor`` / ``text.color`` /
    ``axes.labelcolor``. CRLF-safe; ignores comment and blank lines.
    """
    text = path.read_text(encoding="utf-8")
    kv: dict[str, str] = {}
    for raw in re.split(r"\r?\n", text):
        line = raw.strip()
        if line == "" or line.startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            continue
        kv[key.strip()] = value.strip()

    out: dict = {}
    cycle_raw = kv.get("axes.prop_cycle", "")
    bracket = re.search(r"\[([^\]]*)\]", cycle_raw)
    out["cycle"] = _HEX6.findall(bracket.group(1)) if bracket else []
    for single in ("axes.facecolor", "figure.facecolor", "text.color", "axes.labelcolor"):
        m = _HEX6.search(kv.get(single, ""))
        out[single] = m.group(1) if m else None
    return out


class TestStyleWCAGContrast(unittest.TestCase):
    def test_series_colours_clear_3to1_on_axes_facecolor(self):
        checked = 0
        for stem in _ALL_STYLES:
            path = STYLES_DIR / f"{stem}.mplstyle"
            with self.subTest(style=stem):
                self.assertTrue(path.exists(), f"missing style file: {path}")
                style = _parse_style(path)
                cycle = style["cycle"]
                # Non-vacuity anchor: at least three series colours were parsed.
                self.assertGreaterEqual(
                    len(cycle), 3, f"{stem}: fewer than 3 prop_cycle colours parsed"
                )
                bg = style["axes.facecolor"]
                self.assertIsNotNone(bg, f"{stem}: axes.facecolor not parsed")
                for hexc in cycle:
                    ratio = _contrast(hexc, bg)
                    self.assertGreaterEqual(
                        ratio,
                        3.0,
                        f"{stem}: series #{hexc} vs axes.facecolor #{bg} "
                        f"is {ratio:.2f}:1 (< 3:1, WCAG 1.4.11)",
                    )
                checked += 1
        self.assertEqual(checked, 4, "expected exactly four style files checked")

    def test_text_colours_clear_4point5to1_on_figure_facecolor(self):
        checked = 0
        for stem in _ALL_STYLES:
            path = STYLES_DIR / f"{stem}.mplstyle"
            with self.subTest(style=stem):
                self.assertTrue(path.exists(), f"missing style file: {path}")
                style = _parse_style(path)
                fig_bg = style["figure.facecolor"]
                self.assertIsNotNone(fig_bg, f"{stem}: figure.facecolor not parsed")
                for role in ("text.color", "axes.labelcolor"):
                    fg = style[role]
                    self.assertIsNotNone(fg, f"{stem}: {role} not parsed")
                    ratio = _contrast(fg, fig_bg)
                    self.assertGreaterEqual(
                        ratio,
                        4.5,
                        f"{stem}: {role} #{fg} vs figure.facecolor #{fig_bg} "
                        f"is {ratio:.2f}:1 (< 4.5:1, WCAG 1.4.3)",
                    )
                checked += 1
        self.assertEqual(checked, 4, "expected exactly four style files checked")


if __name__ == "__main__":
    unittest.main()
