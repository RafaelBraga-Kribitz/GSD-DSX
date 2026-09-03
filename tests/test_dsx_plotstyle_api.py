"""Public API of templates/dsx_plotstyle.py — signatures + mandatory source (REQ-P23-02, GA-2).

Repo-integrity test (off the gate path, no ``report.add``): asserts the three
GA-2 keyword-explicit functions exist with their pinned keyword-only shapes, and
that ``source`` is a *required* keyword on ``finalise_figure`` — omitting it is a
``TypeError`` at call binding (mirroring DSX-VIZ-062's "every figure cites its
source" doctrine as a signature property).

The helper imports matplotlib, so the whole module is guarded with
``@unittest.skipIf`` when matplotlib is absent (analyst-side only — the gate path
never imports it). It loads the helper by *file path* via ``importlib`` because
``templates/`` has no ``__init__.py`` (it is not an importable package).

CRLF discipline (repo CLAUDE.md): nothing here is ``\n``-anchored; the module is
loaded and inspected via ``importlib``/``inspect``, both CRLF-agnostic.

Run:  python -m unittest tests.test_dsx_plotstyle_api -v
"""

from __future__ import annotations

import importlib.util
import inspect
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HELPER_PATH = ROOT / "templates" / "dsx_plotstyle.py"

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
class TestDsxPlotstyleApi(unittest.TestCase):
    def setUp(self):
        self.mod = _load_helper()

    def test_finalise_figure_signature(self):
        sig = inspect.signature(self.mod.finalise_figure)
        params = sig.parameters
        # fig is positional; title/source/subtitle/note are keyword-only.
        self.assertEqual(
            params["fig"].kind, inspect.Parameter.POSITIONAL_OR_KEYWORD
        )
        for name in ("title", "source", "subtitle", "note"):
            self.assertIn(name, params, f"finalise_figure missing keyword {name!r}")
            self.assertEqual(
                params[name].kind,
                inspect.Parameter.KEYWORD_ONLY,
                f"finalise_figure param {name!r} is not keyword-only",
            )
        # source has NO default — it is a mandatory keyword.
        self.assertIs(
            params["source"].default,
            inspect.Parameter.empty,
            "finalise_figure `source` must have no default (mandatory keyword)",
        )
        # subtitle/note default to None.
        self.assertIsNone(params["subtitle"].default)
        self.assertIsNone(params["note"].default)

    def test_finalise_figure_without_source_raises_typeerror(self):
        # The TypeError fires at call binding (missing required keyword) before the
        # body runs, so a bare throwaway object as `fig` never gets touched.
        with self.assertRaises(TypeError):
            self.mod.finalise_figure(object(), title="a takeaway title")

    def test_direct_label_signature(self):
        self.assertTrue(hasattr(self.mod, "direct_label"), "direct_label missing")
        params = inspect.signature(self.mod.direct_label).parameters
        self.assertEqual(params["ax"].kind, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        for name in ("labels", "color_from_line", "x_offset", "fontsize"):
            self.assertIn(name, params, f"direct_label missing keyword {name!r}")
            self.assertEqual(
                params[name].kind,
                inspect.Parameter.KEYWORD_ONLY,
                f"direct_label param {name!r} is not keyword-only",
            )

    def test_save_deterministic_signature(self):
        self.assertTrue(
            hasattr(self.mod, "save_deterministic"), "save_deterministic missing"
        )
        params = inspect.signature(self.mod.save_deterministic).parameters
        self.assertEqual(params["fig"].kind, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        self.assertEqual(params["path"].kind, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        self.assertEqual(params["metadata"].kind, inspect.Parameter.KEYWORD_ONLY)
        self.assertIsNone(params["metadata"].default)
        # Accepts arbitrary **savefig_kwargs.
        self.assertTrue(
            any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values()),
            "save_deterministic must accept **savefig_kwargs",
        )

    def test_register_fonts_exists(self):
        self.assertTrue(
            callable(getattr(self.mod, "register_fonts", None)),
            "register_fonts helper missing",
        )


if __name__ == "__main__":
    unittest.main()
