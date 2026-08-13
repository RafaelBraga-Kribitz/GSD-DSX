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
    # Dropping the last path segment is correct for both inputs by construction: an
    # __init__.py's package is its own directory (the path minus the __init__ segment),
    # and a plain module's package is its containing directory (the path minus the
    # module segment). Same operation, two derivations, one line.
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


# ── D-11 / REQ-P7-09: no dsx/frame check reads the declared inference paradigm ──
#
# A second, narrower detector living beside the import-boundary scanner above, not an
# extension of it: the import scanner walks import statements only and has no mechanism
# for flagging a string-literal call argument or a dictionary-subscript chain, which is
# exactly the shape a paradigm read takes (dsx/frame/paradigm.py:80 itself reads
# ``get(spec, "inference.paradigm")``). Two detectors, deliberately layered per this
# module's own two-proofs rationale at lines 11-15: a blunt text-level scan that catches
# any access style nobody anticipated (including inside a comment or message string), and
# a precise AST scan that names the offending line for a future contributor.

_PARADIGM_DOTTED_PATH = "inference.paradigm"
_INFERENCE_BLOCK_NAME = "inference"
_PARADIGM_FIELD_NAME = "paradigm"

# The one legitimate reader: paradigm.py IS the paradigm manifest, whose entire job is to
# report what inference.paradigm was declared. D-11 constrains the checks that adjudicate
# the frame, not the manifest that describes it. dsx/frame/interference.py (Phase 8,
# DSX-INT-*) is deliberately NOT excluded here: unlike the paradigm manifest, it
# adjudicates the frame rather than describing what was declared, so D-11 applies to it
# in full — it is covered by the FRAME_DIR.rglob("*.py") scan below like any other check.
_PARADIGM_READ_EXCLUDED_FILENAMES = {"paradigm.py"}


def _scan_source_for_paradigm_reads_text(text: str) -> list[str]:
    """Blunt text-level detector: flags the dotted path ``inference.paradigm`` anywhere
    in ``text`` — in code, in a comment, or inside a message string. Deliberately not
    AST-based, so it also catches a form the AST detector below was never taught to
    recognise."""
    violations: list[str] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        if _PARADIGM_DOTTED_PATH in line:
            violations.append(f"line {lineno}: text contains {_PARADIGM_DOTTED_PATH!r}")
    return violations


def _subscript_key(slice_node: ast.AST) -> "str | None":
    """Return a subscript's string key, tolerating both the modern (3.9+, the slice is
    the index expression directly) and legacy (pre-3.9, wrapped in ``ast.Index``) AST
    shapes. Ducktypes on the class name rather than referencing ``ast.Index`` directly —
    that name no longer exists in newer versions of the ``ast`` module."""
    node = slice_node
    if type(node).__name__ == "Index":
        node = node.value  # type: ignore[attr-defined]
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _scan_source_for_paradigm_reads_ast(text: str) -> list[str]:
    """Precise AST detector: flags a positional call argument that is the string literal
    ``inference.paradigm`` (or any dotted path beginning ``inference.`` — the dotted-path
    helper's convention), and flags a subscript chain that reads the ``inference`` key and
    then the ``paradigm`` key (``spec["inference"]["paradigm"]``)."""
    violations: list[str] = []
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            for arg in node.args:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    literal = arg.value
                    if literal == _PARADIGM_DOTTED_PATH or literal.startswith(
                        _INFERENCE_BLOCK_NAME + "."
                    ):
                        violations.append(
                            f"line {node.lineno}: call argument string literal "
                            f"{literal!r} names the inference block"
                        )
        elif isinstance(node, ast.Subscript):
            key = _subscript_key(node.slice)
            if key == _PARADIGM_FIELD_NAME and isinstance(node.value, ast.Subscript):
                inner_key = _subscript_key(node.value.slice)
                if inner_key == _INFERENCE_BLOCK_NAME:
                    violations.append(
                        f"line {node.lineno}: subscript chain reads "
                        f"[{_INFERENCE_BLOCK_NAME!r}][{_PARADIGM_FIELD_NAME!r}]"
                    )
    return violations


class TestFrameParadigmReadBoundary(unittest.TestCase):
    """D-11 mechanical proof (REQ-P7-09): no code path under dsx/frame/ reads the
    declared inference paradigm, except the paradigm manifest itself. Scans every
    Python file under the frame package, not only dsx/frame/val.py, so a future frame
    module inherits the invariant without anyone remembering to extend this test."""

    def test_real_frame_modules_read_no_declared_paradigm(self):
        violations: list[str] = []
        files = sorted(FRAME_DIR.rglob("*.py"))
        self.assertTrue(files, "dsx/frame/ has no *.py files to scan")
        for path in files:
            if path.name in _PARADIGM_READ_EXCLUDED_FILENAMES:
                continue
            text = path.read_text(encoding="utf-8")
            for problem in _scan_source_for_paradigm_reads_text(text):
                violations.append(f"{path.relative_to(ROOT)} (text): {problem}")
            for problem in _scan_source_for_paradigm_reads_ast(text):
                violations.append(f"{path.relative_to(ROOT)} (ast): {problem}")
        self.assertEqual(violations, [], "\n".join(violations))

    def test_ast_detector_fires_on_string_literal_paradigm_path_argument(self):
        source = (
            "from dsx.spec import get\n"
            "value = get(spec, \"inference.paradigm\")\n"
        )
        self.assertTrue(_scan_source_for_paradigm_reads_ast(source))

    def test_ast_detector_fires_on_direct_subscript_chain_reading_paradigm(self):
        source = "value = spec[\"inference\"][\"paradigm\"]\n"
        self.assertTrue(_scan_source_for_paradigm_reads_ast(source))

    def test_text_detector_fires_on_dotted_path_anywhere_including_comments(self):
        sources = [
            "# a comment mentioning inference.paradigm here\n",
            "message = \"do not read inference.paradigm\"\n",
        ]
        for source in sources:
            with self.subTest(source=source):
                self.assertTrue(_scan_source_for_paradigm_reads_text(source))

    def test_both_detectors_permit_a_validity_frame_field_read(self):
        source = (
            "from dsx.spec import get\n"
            "value = get(spec, \"validity_frame.estimand.quantity\")\n"
        )
        self.assertEqual(_scan_source_for_paradigm_reads_text(source), [])
        self.assertEqual(_scan_source_for_paradigm_reads_ast(source), [])

    def test_interference_module_is_inside_the_paradigm_read_scan_and_clean(self):
        """REQ-P8-06 traceability (08-03 Task 2): a named test proving
        ``dsx/frame/interference.py`` is inside ``FRAME_DIR.rglob("*.py")`` — the
        real-tree scan the class above runs — and reads the declared paradigm
        field by neither detector, rather than this being merely inferable from
        the glob covering every file under the package."""
        files = sorted(FRAME_DIR.rglob("*.py"))
        interference_path = FRAME_DIR / "interference.py"
        self.assertIn(
            interference_path, files,
            "dsx/frame/interference.py is not visible to the FRAME_DIR.rglob scan",
        )
        text = interference_path.read_text(encoding="utf-8")
        self.assertEqual(_scan_source_for_paradigm_reads_text(text), [])
        self.assertEqual(_scan_source_for_paradigm_reads_ast(text), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
