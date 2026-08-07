"""Tests for scripts/gen-finding-catalogue.py — D-05 citation/reference-value/
test-linkage enforcement (REQ-P6-11, D-20 through D-23).

`scripts/gen-finding-catalogue.py` is a script, not an installed module, so it is
loaded by path via `importlib.util.spec_from_file_location`.

Run:  python3 -m unittest tests.test_gen_finding_catalogue -v
"""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = _ROOT / "scripts" / "gen-finding-catalogue.py"


def _load_script():
    spec = importlib.util.spec_from_file_location("gen_finding_catalogue", _SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


g = _load_script()


def _write(root: Path, name: str, content: str) -> None:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# ── Task 1: check_d05 core mechanics (synthetic code_root/tests_root) ──────────


class TestD05Core(unittest.TestCase):
    def test_check_d05_ignores_uncovered_prefix(self):
        # DSX-VIZ-030 matches no allow-list prefix — must return [] no matter how
        # bare its docstring is, and even against directories that do not exist.
        rows = [("DSX-VIZ-030", "HIGH", "t", "viz")]
        missing = Path(tempfile.mkdtemp()) / "does-not-exist"
        self.assertEqual(g.check_d05(rows, missing, missing), [])

    def test_check_d05_flags_missing_citation(self):
        with tempfile.TemporaryDirectory() as code_dir, tempfile.TemporaryDirectory() as tests_dir:
            _write(
                Path(code_dir),
                "check.py",
                '''
def f(report):
    """
    Reference value: 42
    """
    report.add("DSX-PAR-001", "HIGH", "t")
''',
            )
            _write(Path(tests_dir), "test_marker.py", "# D-05: DSX-PAR-001\n")
            rows = [("DSX-PAR-001", "HIGH", "t", "frame/paradigm")]
            problems = g.check_d05(rows, Path(code_dir), Path(tests_dir))
            self.assertTrue(any("Citation" in p and "DSX-PAR-001" in p for p in problems))

    def test_check_d05_flags_missing_reference_value(self):
        with tempfile.TemporaryDirectory() as code_dir, tempfile.TemporaryDirectory() as tests_dir:
            _write(
                Path(code_dir),
                "check.py",
                '''
def f(report):
    """
    Citation: Example, A. (2020), "A Study", Table 1.
    """
    report.add("DSX-PAR-001", "HIGH", "t")
''',
            )
            _write(Path(tests_dir), "test_marker.py", "# D-05: DSX-PAR-001\n")
            rows = [("DSX-PAR-001", "HIGH", "t", "frame/paradigm")]
            problems = g.check_d05(rows, Path(code_dir), Path(tests_dir))
            self.assertTrue(
                any("Reference value" in p and "DSX-PAR-001" in p for p in problems)
            )

    def test_check_d05_flags_missing_test_marker(self):
        with tempfile.TemporaryDirectory() as code_dir, tempfile.TemporaryDirectory() as tests_dir:
            _write(
                Path(code_dir),
                "check.py",
                '''
def f(report):
    """
    Citation: Example, A. (2020), "A Study", Table 1.
    Reference value: 42
    """
    report.add("DSX-PAR-001", "HIGH", "t")
''',
            )
            # tests_dir deliberately left without a matching marker file.
            _write(Path(tests_dir), "test_other.py", "# D-05: DSX-PAR-002\n")
            rows = [("DSX-PAR-001", "HIGH", "t", "frame/paradigm")]
            problems = g.check_d05(rows, Path(code_dir), Path(tests_dir))
            self.assertTrue(any("marker" in p and "DSX-PAR-001" in p for p in problems))

    def test_check_d05_passes_fully_compliant_code(self):
        with tempfile.TemporaryDirectory() as code_dir, tempfile.TemporaryDirectory() as tests_dir:
            _write(
                Path(code_dir),
                "check.py",
                '''
def f(report):
    """
    Citation: Example, A. (2020), "A Study", Table 1.
    Reference value: 42
    """
    report.add("DSX-PAR-001", "HIGH", "t")
''',
            )
            _write(Path(tests_dir), "test_marker.py", "# D-05: DSX-PAR-001\n")
            rows = [("DSX-PAR-001", "HIGH", "t", "frame/paradigm")]
            self.assertEqual(g.check_d05(rows, Path(code_dir), Path(tests_dir)), [])

    def test_resolve_docstrings_function_level(self):
        with tempfile.TemporaryDirectory() as code_dir:
            _write(
                Path(code_dir),
                "check.py",
                '''
"""Module docstring — must not be picked up when a function docstring exists."""


def f(report):
    """Citation: Function Level (2020), "Case"."""
    report.add("DSX-PAR-001", "HIGH", "t")
''',
            )
            docstrings = g._resolve_docstrings(Path(code_dir))
            self.assertIn("Function Level", docstrings["DSX-PAR-001"])

    def test_resolve_docstrings_module_level_fallback(self):
        with tempfile.TemporaryDirectory() as code_dir:
            _write(
                Path(code_dir),
                "check.py",
                '''
"""Citation: Module Level (2020), "Case".

Reference value: 1
"""
report.add("DSX-PAR-001", "HIGH", "t")
''',
            )
            docstrings = g._resolve_docstrings(Path(code_dir))
            self.assertIn("Module Level", docstrings["DSX-PAR-001"])

    def test_collect_test_markers_finds_marker(self):
        with tempfile.TemporaryDirectory() as tests_dir:
            _write(
                Path(tests_dir),
                "test_marker.py",
                "class T:\n    def test_x(self):\n        pass  # D-05: DSX-PAR-001\n",
            )
            markers = g._collect_test_markers(Path(tests_dir))
            self.assertIn("DSX-PAR-001", markers)

    def test_dsx_par_prefix_group_registered(self):
        prefixes = [prefix for prefix, _heading, _blurb in g.PREFIX_GROUPS]
        self.assertIn("DSX-PAR", prefixes)

    def test_every_collected_code_resolves_to_a_prefix_group(self):
        prefixes = [prefix for prefix, _heading, _blurb in g.PREFIX_GROUPS]
        unresolved = [
            row[0]
            for row in g.collect()
            if not any(row[0].startswith(prefix + "-") for prefix in prefixes)
        ]
        self.assertEqual(unresolved, [])


if __name__ == "__main__":
    unittest.main()
