"""No-entrypoint-execution standing guard (REQ-P16-04, D-01/D-09).

The orthogonal complement to ``tests/test_gate_path_hermetic.py``. That test forbids
a forbidden *import* reaching a gate module's closure; this one forbids a gate module
*executing* the analysis entrypoint. The distinction is load-bearing:
``subprocess`` / ``runpy`` / ``os.system`` are all stdlib, so they sail through an
import-closure check — an execution primitive can only be caught by looking for the
*call*, which is what this module does.

It statically AST-walks every module under ``dsx/checks/`` and ``dsx/frame/`` and
asserts none of them calls an execution primitive (subprocess.*, os.system/popen/
exec*/spawn*, runpy.run_path/run_module, bare exec/eval, dynamic compile/__import__).
The scan is AST-based, never a substring grep, because ``dsx/checks/code.py``'s
docstring and body legitimately contain the strings ``exec`` / ``!pip`` and call
``ast.parse`` / ``ast.walk`` / ``ast.unparse`` — a grep would false-positive and an
``ast``-blind scan would too, so the ``ast`` and ``re`` roots are excluded explicitly.

Anti-vacuity (D-09): the scanned set is asserted non-empty and to include
``dsx/checks/code.py`` and ``dsx/checks/repro.py`` by name; a positive control proves
a synthetic ``subprocess.run`` / ``runpy.run_path`` / ``os.system`` / ``exec`` IS
flagged; a negative control proves ``ast.*`` / ``re.compile`` are NOT.

CRLF discipline (repo CLAUDE.md): ``ast.parse`` tolerates ``\r\n``; nothing here is
``\n``-anchored.

Run:  python -m unittest tests.test_no_entrypoint_execution -v
"""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DSX = ROOT / "dsx"


def _attr_root(func: ast.AST) -> "str | None":
    """The leftmost ``ast.Name`` id of an attribute chain (``a.b.c`` -> ``a``)."""
    cur = func
    while isinstance(cur, ast.Attribute):
        cur = cur.value
    return cur.id if isinstance(cur, ast.Name) else None


def _execution_primitives(source: str) -> set[str]:
    """Return the set of execution-primitive call descriptions found in ``source``.

    Detects the family that would run the analysis entrypoint on the gate path:
    ``subprocess.*``, ``os.system``/``popen``/``exec*``/``spawn*``/``posix_spawn*``,
    ``runpy.run_path``/``run_module``, a dynamic ``importlib.import_module``, and the
    bare builtins ``exec`` / ``eval`` / dynamic ``compile`` / ``__import__``. The
    ``ast`` and ``re`` roots are excluded so legitimate ``ast.parse``/``ast.walk``/
    ``ast.unparse`` and ``re.compile`` calls are not mistaken for execution.
    """
    tree = ast.parse(source)
    found: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute):
            root = _attr_root(func)
            attr = func.attr
            if root in ("ast", "re"):
                continue  # legitimate AST inspection / regex compilation
            if root == "subprocess":
                found.add(f"subprocess.{attr}")
            elif root == "os" and (
                attr in ("system", "popen", "posix_spawn", "posix_spawnp")
                or attr.startswith("exec")
                or attr.startswith("spawn")
            ):
                found.add(f"os.{attr}")
            elif root == "runpy" and attr in ("run_path", "run_module"):
                found.add(f"runpy.{attr}")
            elif root == "importlib" and attr == "import_module":
                first = node.args[0] if node.args else None
                if not isinstance(first, ast.Constant):
                    found.add("importlib.import_module")
        elif isinstance(func, ast.Name):
            name = func.id
            if name in ("exec", "eval"):
                found.add(name)
            elif name in ("compile", "__import__"):
                first = node.args[0] if node.args else None
                if not isinstance(first, ast.Constant):
                    found.add(name)
    return found


def _gate_source_modules() -> list[Path]:
    """Every ``*.py`` under ``dsx/checks/`` and ``dsx/frame/`` (the gate source tree)."""
    return sorted((DSX / "checks").glob("*.py")) + sorted((DSX / "frame").glob("*.py"))


class TestNoEntrypointExecution(unittest.TestCase):
    def test_no_gate_module_executes_the_entrypoint(self):
        """No dsx/checks or dsx/frame module calls an execution primitive (REQ-P16-04)."""
        modules = _gate_source_modules()
        scanned = {p.relative_to(ROOT).as_posix() for p in modules}

        # Anti-vacuity (D-09 a): the scan examined a real, named, non-empty set.
        self.assertTrue(scanned, "no gate-source modules resolved under dsx/checks or dsx/frame")
        self.assertIn("dsx/checks/code.py", scanned, scanned)
        self.assertIn("dsx/checks/repro.py", scanned, scanned)
        for rel in scanned:
            self.assertTrue(
                rel.startswith("dsx/checks/") or rel.startswith("dsx/frame/"),
                f"scanned a path outside the gate source tree: {rel}",
            )

        offenders: dict[str, set[str]] = {}
        for path in modules:
            prims = _execution_primitives(path.read_text(encoding="utf-8"))
            if prims:
                offenders[path.relative_to(ROOT).as_posix()] = prims
        self.assertEqual(
            offenders,
            {},
            "gate module(s) execute the entrypoint — a gate module must never run "
            f"the analysis (REQ-P16-04 / D-01): {offenders}",
        )

    def test_positive_control_flags_known_execution(self):
        """The scanner has teeth: a synthetic subprocess/runpy/os/exec call IS flagged."""
        subprocess_src = "import subprocess\nsubprocess.run([entrypoint])\n"
        runpy_src = "import runpy\nrunpy.run_path(entrypoint)\n"
        os_src = "import os\nos.system(entrypoint)\n"
        exec_src = "exec(open(entrypoint).read())\n"

        self.assertIn("subprocess.run", _execution_primitives(subprocess_src))
        self.assertIn("runpy.run_path", _execution_primitives(runpy_src))
        self.assertIn("os.system", _execution_primitives(os_src))
        self.assertIn("exec", _execution_primitives(exec_src))
        for src in (subprocess_src, runpy_src, os_src, exec_src):
            self.assertTrue(_execution_primitives(src), f"scanner missed: {src!r}")

    def test_negative_control_does_not_flag_ast_or_re(self):
        """ast.parse/walk/unparse and re.compile are not confused with execution."""
        clean_src = (
            "import ast\n"
            "import re\n"
            "tree = ast.parse(source)\n"
            "for node in ast.walk(tree):\n"
            "    rendered = ast.unparse(node)\n"
            "pattern = re.compile(r'x')\n"
        )
        self.assertEqual(_execution_primitives(clean_src), set())


if __name__ == "__main__":
    unittest.main()
