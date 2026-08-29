"""Gate-path hermeticity standing guard (REQ-P14-06, D-01/D-03/D-07).

The deterministic ``dsx`` gate path must stay stdlib-pure and profiler-free: no gate
module — nor anything in its transitive internal import closure — may pull in a data
library (``pandas``/``scipy``/``numpy``) or the CSV-opening profiler. Phase 14 is a
doc/skill/template phase; the single way it could regress this is by a later "just
call the analysis entrypoint" simplification creeping onto the gate path. This module
pins the bound structurally so such a regression turns a test red rather than shipping.

It reads ``dsx/`` source via ``ast`` only — it imports no third-party package and adds
no ``report.add``, so it mints no finding code. It resolves the gate modules from the
live ``dsx.cli.GATE_PROFILES`` union, so it stays correct if gate-profile membership
changes.

CRLF discipline (repo CLAUDE.md): ``ast.parse`` tolerates ``\r\n``; nothing here is
``\n``-anchored.

Run:  python -m unittest tests.test_gate_path_hermetic -v
"""

from __future__ import annotations

import ast
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DSX = ROOT / "dsx"

# Top-level import names that must never reach a gate module's import closure.
FORBIDDEN = {"pandas", "scipy", "numpy", "csv"}


def _load_gate_profiles() -> dict:
    """Import ``dsx.cli`` (with ROOT on sys.path) and return its GATE_PROFILES."""
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from dsx import cli  # noqa: PLC0415 — lazy, so ROOT is on the path first

    return cli.GATE_PROFILES


def _resolve_check_file(name: str) -> Path | None:
    """Map a check name to its source file: dsx/checks/<name>.py then dsx/frame/<name>.py."""
    for sub in ("checks", "frame"):
        candidate = DSX / sub / f"{name}.py"
        if candidate.exists():
            return candidate.resolve()
    return None


def _module_from_relative(start: Path, level: int, module: str | None) -> list[Path]:
    """Resolve a relative import (level > 0) to candidate files under ROOT.

    Ascend ``level - 1`` directories from the importing file's package directory,
    then append the dotted module parts. Return the ``<parts>.py`` and
    ``<parts>/__init__.py`` candidates that exist.
    """
    base = start.parent
    for _ in range(level - 1):
        base = base.parent
    target = base
    if module:
        for part in module.split("."):
            target = target / part
    out = []
    for candidate in (target.with_suffix(".py"), target / "__init__.py"):
        if candidate.exists():
            out.append(candidate.resolve())
    return out


def _module_from_absolute_dsx(module: str) -> list[Path]:
    """Resolve a top-level ``dsx.*`` import to candidate files under ROOT."""
    target = ROOT
    for part in module.split("."):
        target = target / part
    out = []
    for candidate in (target.with_suffix(".py"), target / "__init__.py"):
        if candidate.exists():
            out.append(candidate.resolve())
    return out


def _closure(start_files: list[Path]) -> tuple[set[Path], set[str]]:
    """Walk the import closure of ``start_files`` to a fixpoint.

    Returns (visited files, union of top-level import names seen across them).
    """
    frontier = [f.resolve() for f in start_files]
    visited: set[Path] = set()
    top_level: set[str] = set()
    while frontier:
        current = frontier.pop()
        if current in visited or not current.exists():
            continue
        visited.add(current)
        tree = ast.parse(current.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top_level.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.level and node.level > 0:
                    for f in _module_from_relative(current, node.level, node.module):
                        if f not in visited:
                            frontier.append(f)
                elif node.module:
                    head = node.module.split(".")[0]
                    top_level.add(head)
                    if head == "dsx":
                        for f in _module_from_absolute_dsx(node.module):
                            if f not in visited:
                                frontier.append(f)
    return visited, top_level


class TestGatePathHermetic(unittest.TestCase):
    def _gate_roots(self) -> set[Path]:
        profiles = _load_gate_profiles()
        names = set().union(*(set(p) for p in profiles.values()))
        roots = {f for f in (_resolve_check_file(n) for n in names) if f is not None}
        # Sanity anchor against a vacuous pass.
        self.assertTrue(roots, "no gate-module source files resolved from GATE_PROFILES")
        self.assertIn(
            (DSX / "checks" / "dq.py").resolve(),
            roots,
            "dsx/checks/dq.py not among the resolved gate roots",
        )
        return roots

    def test_no_data_library_reaches_the_gate_path(self):
        """No pandas/scipy/numpy/csv in any gate module's import closure (D-01/D-03/D-07)."""
        roots = self._gate_roots()
        _, top_level = _closure(sorted(roots))
        offending = FORBIDDEN & top_level
        self.assertEqual(
            offending,
            set(),
            f"forbidden import(s) reached the gate path closure: {sorted(offending)}",
        )

    def test_profiler_absent_from_dq_closure(self):
        """The CSV-opening profiler is not in dsx/checks/dq.py's import closure (D-03)."""
        dq = (DSX / "checks" / "dq.py").resolve()
        self.assertTrue(dq.exists(), "dsx/checks/dq.py not found")
        visited, _ = _closure([dq])
        profiler = (DSX / "profiler.py").resolve()
        self.assertNotIn(
            profiler,
            visited,
            "dsx/profiler.py reached from dsx/checks/dq.py's import closure",
        )
        # Belt-and-braces: no visited module is named profiler by any path.
        self.assertFalse(
            any(f.stem == "profiler" for f in visited),
            "a 'profiler' module reached dq's closure",
        )


if __name__ == "__main__":
    unittest.main()
