"""D-03a import-boundary enforcement for ``dsx/frame/`` — now in both directions.

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

D-04a: the boundary is enforced in both directions. Phase 11 composes the
checks layer and the frame layer inside ``dsx/cli.py`` — the only place the
two packages are allowed to meet — and the natural instinct once an alias
table exists under ``dsx/frame/`` is to import it straight from
``dsx/checks/stats.py``. ``TestChecksImportBoundary`` below is the mirror-image
scanner for that direction, reusing the same AST machinery with the forbidden
package name generalised into a parameter.

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

import dsx.checks  # noqa: E402
import dsx.frame  # noqa: E402 — RED proof: fails to import until dsx/frame/ exists

FRAME_DIR = Path(dsx.frame.__file__).resolve().parent
CHECKS_DIR = Path(dsx.checks.__file__).resolve().parent

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


def _scan_source_for_checks_imports(
    text: str, package: str, forbidden_package: str = _FORBIDDEN_PACKAGE
) -> list[str]:
    """Return one violation string per import of ``forbidden_package`` (or a
    submodule of it) found in ``text``, which is parsed as if it were a module
    belonging to ``package`` (used to resolve relative imports to their
    absolute dotted form). Returns ``[]`` when no violation is found.

    ``forbidden_package`` defaults to ``dsx.checks`` — the ``dsx/frame/`` →
    ``dsx/checks`` direction this scanner was originally written for. Passing
    ``forbidden_package="dsx.frame"`` (with ``package="dsx.checks"``) scans the
    mirror-image direction (D-04a) with the same AST machinery: one scanner
    function serves both directions rather than a second hand-rolled walker.

    Each violation names the line number and the offending resolved module
    name; the caller (a real-file scan) prepends the file path.
    """
    violations: list[str] = []
    tree = ast.parse(text)

    def _maybe_flag(name: str, lineno: int) -> None:
        if name == forbidden_package or name.startswith(forbidden_package + "."):
            violations.append(
                f"line {lineno}: forbidden import of {name!r} "
                f"(must not import {forbidden_package!r})"
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


class TestChecksImportBoundary(unittest.TestCase):
    """D-04a: the reverse-direction proof. Nothing under ``dsx/checks/`` may
    import ``dsx.frame`` or any submodule of it — the mirror image of
    ``TestFrameImportBoundary`` above, reusing the same AST scanner with the
    forbidden package name flipped. ``dsx/cli.py`` is the only place the two
    packages are allowed to meet (D-04); this is what makes crossing that
    boundary directly from ``dsx/checks/stats.py`` ship red instead of green."""

    def test_real_checks_modules_import_nothing_from_frame(self):
        violations: list[str] = []
        files = sorted(CHECKS_DIR.rglob("*.py"))
        self.assertTrue(files, "dsx/checks/ has no *.py files to scan")
        for path in files:
            text = path.read_text(encoding="utf-8")
            package = _package_for(path)
            for problem in _scan_source_for_checks_imports(
                text, package, forbidden_package="dsx.frame"
            ):
                violations.append(f"{path.relative_to(ROOT)}: {problem}")
        self.assertEqual(violations, [], "\n".join(violations))

    def test_scanner_fires_on_violating_sources_and_permits_allowed_ones(self):
        violating_sources = [
            "from dsx.frame import admissibility\n",
            "from ..frame import admissibility\n",
            "import dsx.frame.admissibility\n",
        ]
        for source in violating_sources:
            with self.subTest(source=source):
                result = _scan_source_for_checks_imports(
                    source, "dsx.checks", forbidden_package="dsx.frame"
                )
                self.assertTrue(result, f"expected a violation for: {source!r}")

        permitted_sources = [
            "from ..findings import Report\n",
            "from dsx.framework import x\n",
        ]
        for source in permitted_sources:
            with self.subTest(source=source):
                self.assertEqual(
                    _scan_source_for_checks_imports(
                        source, "dsx.checks", forbidden_package="dsx.frame"
                    ),
                    [],
                )


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


# ── D-18 / REQ-P11-02: no approximate-matching machinery in dsx/frame/admissibility ──
#
# Alias resolution happens only by equality after dsx.spec.normalize(), and by nothing
# else. D-18 forbids distance, containment, prefix, or any other approximate match.
# This scanner proves the prohibition is enforced in the source itself, not just by
# prose and behavioural tests.


def _scan_source_for_approx_matching(text: str) -> list[str]:
    """Return one violation string per approximate-matching construct found in
    ``text``. Detects difflib imports, attribute access to difflib, calls to
    distance-matching functions (get_close_matches, SequenceMatcher, ratio,
    quick_ratio, real_quick_ratio), and prefix/suffix matching via the
    startswith/endswith string methods.

    startswith/endswith are flagged unconditionally rather than only on a
    resolution path: this scanner is pointed at dsx/frame/admissibility.py,
    whose only permitted string operation on a declared label is equality after
    normalize(), so a prefix or suffix test anywhere in it is a D-18 violation
    by construction. The committed module calls neither.

    Does NOT flag membership tests (the `in` operator), because the AST walker
    cannot reliably distinguish a legitimate collection membership test
    (`if alias in index:`) from a substring check (`if declared in alias:`)
    without full dataflow analysis, and a scanner that cries wolf on the
    module's own alias-index lookups would be deleted by the next maintainer.
    That direction stays covered behaviourally by
    TestResolveDeclaredProcedure.test_near_miss_variants_of_a_real_alias_are_unresolved,
    whose near-miss inputs include a bare prefix of a real alias.

    Returns ``[]`` when no violation is found. Each violation names the line
    number and the offending construct; the caller prepends the file path.
    """
    violations: list[str] = []
    tree = ast.parse(text)

    # Forbidden function names and difflib access patterns
    _FORBIDDEN_FUNCS = {
        "get_close_matches", "SequenceMatcher", "ratio", "quick_ratio",
        "real_quick_ratio"
    }

    # String methods that resolve by prefix/suffix rather than by equality
    _PREFIX_MATCH_METHODS = {"startswith", "endswith"}

    for node in ast.walk(tree):
        # Detect: import difflib, from difflib import ...
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "difflib" or alias.name.startswith("difflib."):
                    violations.append(
                        f"line {node.lineno}: imports {alias.name!r} "
                        f"(difflib provides approximate matching)"
                    )
        elif isinstance(node, ast.ImportFrom):
            if node.module == "difflib" or (
                node.module is not None and node.module.startswith("difflib.")
            ):
                violations.append(
                    f"line {node.lineno}: imports from {node.module!r} "
                    f"(difflib provides approximate matching)"
                )

        # Detect: attribute access on difflib (e.g., difflib.SequenceMatcher)
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name) and node.value.id == "difflib":
                violations.append(
                    f"line {node.lineno}: accesses {node.attr!r} on difflib "
                    f"(difflib provides approximate matching)"
                )

        # Detect: calls to forbidden functions
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in _FORBIDDEN_FUNCS:
                violations.append(
                    f"line {node.lineno}: calls {node.func.id!r} "
                    f"(provides approximate matching)"
                )
            elif isinstance(node.func, ast.Attribute):
                if node.func.attr in _FORBIDDEN_FUNCS:
                    violations.append(
                        f"line {node.lineno}: calls {node.func.attr!r} "
                        f"(provides approximate matching)"
                    )
                elif node.func.attr in _PREFIX_MATCH_METHODS:
                    violations.append(
                        f"line {node.lineno}: calls {node.func.attr!r} "
                        f"(prefix/suffix matching is not exact match)"
                    )

    return violations


class TestFrameApproximateMatchingBoundary(unittest.TestCase):
    """D-18 mechanical proof (REQ-P11-02): dsx/frame/admissibility.py contains
    no approximate-matching machinery. Alias resolution is exact-match only,
    after normalize(), never by distance, containment, prefix or any other
    heuristic. The scanner below proves this prohibition is enforced in the
    source itself, not just in behavioural tests."""

    def test_real_admissibility_module_contains_no_approx_matching(self):
        admissibility_path = FRAME_DIR / "admissibility.py"
        self.assertTrue(
            admissibility_path.exists(),
            f"dsx/frame/admissibility.py not found at {admissibility_path}",
        )
        text = admissibility_path.read_text(encoding="utf-8")
        violations = _scan_source_for_approx_matching(text)
        self.assertEqual(violations, [], "\n".join(violations))

    def test_scanner_fires_on_difflib_import(self):
        source = "import difflib\n"
        result = _scan_source_for_approx_matching(source)
        self.assertTrue(result, f"expected a violation for: {source!r}")
        self.assertIn("difflib", result[0])

    def test_scanner_fires_on_difflib_from_import(self):
        source = "from difflib import get_close_matches\n"
        result = _scan_source_for_approx_matching(source)
        self.assertTrue(result, f"expected a violation for: {source!r}")
        self.assertIn("difflib", result[0])

    def test_scanner_fires_on_get_close_matches_call(self):
        source = "best = get_close_matches(declared, candidates, n=1, cutoff=0.6)\n"
        result = _scan_source_for_approx_matching(source)
        self.assertTrue(result, f"expected a violation for: {source!r}")
        self.assertIn("get_close_matches", result[0])

    def test_scanner_fires_on_sequence_matcher_similarity_ratio(self):
        source = (
            "import difflib\n"
            "score = difflib.SequenceMatcher(None, declared, alias).ratio()\n"
        )
        result = _scan_source_for_approx_matching(source)
        self.assertTrue(result, f"expected a violation for: {source!r}")
        self.assertTrue(
            any("SequenceMatcher" in violation for violation in result),
            f"no violation named SequenceMatcher: {result!r}",
        )

    def test_scanner_fires_on_startswith_prefix_match(self):
        source = (
            "for alias in candidates:\n"
            "    if alias.startswith(declared):\n"
            "        return alias\n"
        )
        result = _scan_source_for_approx_matching(source)
        self.assertTrue(result, f"expected a violation for: {source!r}")
        self.assertIn("startswith", result[0])

    def test_scanner_fires_on_endswith_suffix_match(self):
        source = (
            "for alias in candidates:\n"
            "    if alias.endswith(declared):\n"
            "        return alias\n"
        )
        result = _scan_source_for_approx_matching(source)
        self.assertTrue(result, f"expected a violation for: {source!r}")
        self.assertIn("endswith", result[0])

    def test_scanner_permits_exact_equality_after_normalize(self):
        source = (
            "from dsx.spec import normalize\n"
            "target = normalize(declared)\n"
            "if target == existing:\n"
            "    return True\n"
        )
        result = _scan_source_for_approx_matching(source)
        self.assertEqual(result, [])

    def test_scanner_permits_membership_test_against_dict_or_set_literal(self):
        source = (
            "if key in {\"a\", \"b\", \"c\"}:\n"
            "    return True\n"
        )
        result = _scan_source_for_approx_matching(source)
        self.assertEqual(result, [])

    def test_scanner_permits_membership_test_against_clear_collection_name(self):
        source = (
            "if key in index:\n"
            "    return True\n"
        )
        result = _scan_source_for_approx_matching(source)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
