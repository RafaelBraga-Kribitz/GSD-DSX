"""Tests for scripts/gen-finding-catalogue.py — D-05 citation/reference-value/
test-linkage enforcement (REQ-P6-11, D-20 through D-23).

`scripts/gen-finding-catalogue.py` is a script, not an installed module, so it is
loaded by path via `importlib.util.spec_from_file_location`.

Run:  python3 -m unittest tests.test_gen_finding_catalogue -v
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
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


# ── Task 2: enforcement proven against a committed violating fixture ───────────

_FIXTURE_DIR = _ROOT / "tests" / "fixtures" / "d05"


class TestD05EnforcementFixture(unittest.TestCase):
    """Proves both halves of D-05 can actually fail (ROADMAP Success Criterion 4).

    `tests/fixtures/d05/bad_check.py` is not test*-named, so `unittest discover`
    never collects it as a test module (nothing in it is ever imported or run).
    """

    def test_violating_fixture_flags_missing_reference_value(self):
        rows = [("DSX-PAR-999", "HIGH", "t", "fixtures")]
        with tempfile.TemporaryDirectory() as tests_dir:
            _write(Path(tests_dir), "test_marker.py", "# D-05: DSX-PAR-999\n")
            problems = g.check_d05(rows, _FIXTURE_DIR, Path(tests_dir))
        self.assertTrue(
            any("Reference value" in p and "DSX-PAR-999" in p for p in problems),
            f"enforcement failed to detect the violating fixture: {problems!r}",
        )

    def test_violating_fixture_flags_missing_test_marker(self):
        rows = [("DSX-PAR-999", "HIGH", "t", "fixtures")]
        # No `# D-05: DSX-PAR-999` marker anywhere under this empty tests root.
        empty_tests_dir = Path(tempfile.mkdtemp())
        problems = g.check_d05(rows, _FIXTURE_DIR, empty_tests_dir)
        self.assertTrue(
            any("marker" in p and "DSX-PAR-999" in p for p in problems),
            f"enforcement failed to detect the missing test marker: {problems!r}",
        )

    def test_check_d05_ignores_uncovered_code_against_fixture_dir(self):
        rows = [("DSX-VIZ-030", "HIGH", "t", "viz")]
        self.assertEqual(
            g.check_d05(rows, _FIXTURE_DIR, Path(tempfile.mkdtemp())), []
        )

    def test_compliant_fixture_code_produces_no_problem(self):
        rows = [("DSX-SPEC-089", "HIGH", "t", "fixtures")]
        with tempfile.TemporaryDirectory() as tests_dir:
            _write(Path(tests_dir), "test_marker.py", "# D-05: DSX-SPEC-089\n")
            problems = g.check_d05(rows, _FIXTURE_DIR, Path(tests_dir))
        self.assertEqual(problems, [])

    def test_unittest_discover_excludes_fixture_module(self):
        # Isolated subprocess scoped to the fixture directory alone (start_dir ==
        # top_level_dir) — avoids self-recursively re-running the whole `tests/`
        # suite (which would include this very test) while still proving
        # `unittest discover`'s default `test*.py` pattern never collects
        # `bad_check.py`.
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(_FIXTURE_DIR), "-v"],
            cwd=str(_ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("NO TESTS RAN", result.stderr)
        self.assertNotIn("bad_check", result.stderr)

    def test_collect_excludes_fixture_only_codes(self):
        fixture_codes = {row[0] for row in g.collect()}
        self.assertNotIn("DSX-PAR-999", fixture_codes)
        self.assertNotIn("DSX-SPEC-089", fixture_codes)


class TestD05RealTreeStandingGuarantee(unittest.TestCase):
    """The standing guarantee: the real tree returns zero D-05 problems.

    This is what turns D-05 from a convention into a build gate for every later
    phase — the 206 pre-existing codes produce zero new failures, and every
    allow-listed code this phase ships is compliant.
    """

    def test_real_tree_check_d05_is_empty(self):
        self.assertEqual(g.check_d05(g.collect(), g.ROOT / "dsx", g.ROOT / "tests"), [])


if __name__ == "__main__":
    unittest.main()
