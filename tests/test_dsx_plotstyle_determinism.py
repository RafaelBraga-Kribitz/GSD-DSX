"""Off-gate-path double-render determinism proof for save_deterministic (REQ-P23-03, GA-3).

Renders one representative figure through ``save_deterministic`` twice and asserts
the two SVG files are byte-identical under ``dsx.checks.figures.file_sha256`` — the
*same* stdlib ``hashlib.sha256`` hasher ``dsx seal`` uses. ``save_deterministic``
itself never hashes (GA-2, single-hasher rule); this test imports the one canonical
hasher rather than rolling a second one.

This proves the GA-3 recipe holds: a fixed ``svg.hashsalt`` makes element ids a pure
function of content (not a per-process ``uuid4``), and ``metadata={'Date': None}``
suppresses the per-render ``datetime.today()`` timestamp — the two mechanisms that
would otherwise break a byte-for-byte comparison across re-render.

This module is OFF the gate path: it carries no ``report.add``, sits outside every
``GATE_PROFILES`` closure, and mints no finding code (D-P23-04). It writes only into
a ``tempfile.TemporaryDirectory`` — never into ``./figures`` (which would trip
DSX-FIG-040 manifest coverage).

The whole module is ``@unittest.skipIf``-guarded on matplotlib: a matplotlib-free CI
skips cleanly rather than erroring at import (the helper imports matplotlib).

CRLF discipline (repo CLAUDE.md): this module compares raw bytes via a SHA-256 of the
file; no line-ending-sensitive text parsing is performed.

Run:  python -m unittest tests.test_dsx_plotstyle_determinism -v
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HELPER_PATH = ROOT / "templates" / "dsx_plotstyle.py"
STYLE_PATH = ROOT / "styles" / "dsx-urban.mplstyle"

try:
    import matplotlib  # noqa: F401

    _MPL_AVAILABLE = True
except ImportError:
    _MPL_AVAILABLE = False


def _load_helper():
    """Load templates/dsx_plotstyle.py by file path (templates/ is not a package)."""
    spec = importlib.util.spec_from_file_location("dsx_plotstyle", HELPER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@unittest.skipIf(not _MPL_AVAILABLE, "matplotlib not installed — analyst-side only")
class TestDeterministicSVG(unittest.TestCase):
    def test_double_render_hash_equality(self):
        mod = _load_helper()
        # register the vendored Lato face BEFORE the style resolves font.family to it
        # (Pitfall 1: the findfont cache clears forward-only, so registration must
        # precede the in-flight render's font resolution).
        mod.register_fonts()

        import matplotlib.pyplot as plt

        plt.style.use(str(STYLE_PATH))
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 9])
        try:
            with tempfile.TemporaryDirectory() as tmp:
                p1 = mod.save_deterministic(
                    fig, Path(tmp) / "det_1.svg", metadata={"Date": None}
                )
                p2 = mod.save_deterministic(
                    fig, Path(tmp) / "det_2.svg", metadata={"Date": None}
                )

                # dsx seal stays the single hashing authority (GA-2): reuse the SAME
                # file_sha256 dsx/checks/figures.py exports, not a second hasher.
                if str(ROOT) not in sys.path:
                    sys.path.insert(0, str(ROOT))
                from dsx.checks.figures import file_sha256

                self.assertEqual(
                    file_sha256(Path(p1)),
                    file_sha256(Path(p2)),
                    "double render of one figure produced non-identical SVG bytes — "
                    "the GA-3 determinism recipe (fixed svg.hashsalt + metadata Date:None) "
                    "is not holding",
                )
        finally:
            plt.close(fig)


if __name__ == "__main__":
    unittest.main()
