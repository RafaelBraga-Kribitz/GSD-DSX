"""D-03a import-boundary enforcement for ``dsx/frame/``.

Modules under ``dsx/frame/`` may import from ``dsx.findings``, ``dsx.spec``,
``dsx.loader`` and ``dsx.decisions`` — never from ``dsx.checks`` (T-6-01). This
scanner is the mechanical proof, not a convention: it AST-parses source text,
resolves every ``import``/``from ... import`` statement to its absolute dotted
module name (relative imports included, via ``importlib.util.resolve_name`` —
never hand-rolled dot counting), and flags any name that is ``dsx.checks``
itself or starts with ``dsx.checks.``.

Two proofs, not one: the real ``dsx/frame/*.py`` tree scans clean, AND the
scanner is shown to actually fire against three deliberately violating source
strings (plus two permitted-import controls) it never has to commit as a real
module. A boundary test that only ever walks real files can never fail, which
means it is not actually enforcing anything (06-RESEARCH.md Pattern 6).

Run:  python3 -m unittest tests.test_frame_boundary -v
"""

from __future__ import annotations

import ast
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import dsx.frame  # noqa: E402 — RED proof: fails to import until dsx/frame/ exists

FRAME_DIR = Path(dsx.frame.__file__).resolve().parent

_FORBIDDEN_PACKAGE = "dsx.checks"


def _package_for(path: "str | Path") -> str:
    """Derive the dotted package a module at ``path`` lives in, relative to the
    repository root — the exact value Python assigns to that module's
    ``__package__`` at runtime, which is what relative-import resolution uses.

    A non-``__init__.py`` module's package is its *containing* directory's
    dotted path (the module name itself is not part of the package); an
    ``__init__.py``'s package is its own directory's dotted path.
    """
    resolved = Path(path).resolve()
    rel = resolved.relative_to(ROOT).with_suffix("")
    parts = list(rel.parts)
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    else:
        parts = parts[:-1]
    return ".".join(parts)


def _scan_source_for_checks_imports(text: str, package: str) -> list[str]:
    """Return one violation string per import of ``dsx.checks`` (or a submodule
    of it) found in ``text``, which is parsed as if it were a module belonging
    to ``package`` (used to resolve relative imports to their absolute dotted
    form). Returns ``[]`` when no violation is found.

    Each violation names the line number and the offending resolved module
    name; the caller (a real-file scan) prepends the file path.
    """
    violations: list[str] = []
    tree = ast.parse(text)

    def _maybe_flag(name: str, lineno: int) -> None:
        if name == _FORBIDDEN_PACKAGE or name.startswith(_FORBIDDEN_PACKAGE + "."):
            violations.append(
                f"line {lineno}: forbidden import of {name!r} (dsx.frame must not import dsx.checks)"
            )

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                _maybe_flag(alias.name, node.lineno)
        elif isinstance(node, ast.ImportFrom):
            level = node.level or 0
            if level:
                target = ("." * level) + (node.module or "")
                resolved = importlib.util.resolve_name(target, package)
            else:
                resolved = node.module or ""
            _maybe_flag(resolved, node.lineno)

    return violations


class TestFrameImportBoundary(unittest.TestCase):
    def test_real_frame_modules_import_nothing_from_checks(self):
        violations: list[str] = []
        files = sorted(FRAME_DIR.rglob("*.py"))
        self.assertTrue(files, "dsx/frame/ has no *.py files to scan")
        for path in files:
            text = path.read_text(encoding="utf-8")
            package = _package_for(path)
            for problem in _scan_source_for_checks_imports(text, package):
                violations.append(f"{path.relative_to(ROOT)}: {problem}")
        self.assertEqual(violations, [], "\n".join(violations))

    def test_scanner_fires_on_violating_sources_and_permits_allowed_ones(self):
        violating_sources = [
            "from dsx.checks import design\n",
            "from ..checks import design\n",
            "import dsx.checks.design\n",
        ]
        for source in violating_sources:
            with self.subTest(source=source):
                result = _scan_source_for_checks_imports(source, "dsx.frame")
                self.assertTrue(result, f"expected a violation for: {source!r}")

        permitted_sources = [
            "from ..findings import Report\n",
            "from dsx.checksum import x\n",
        ]
        for source in permitted_sources:
            with self.subTest(source=source):
                self.assertEqual(_scan_source_for_checks_imports(source, "dsx.frame"), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
