"""D-14 / REQ-P11.2-07: the reader-less scaffold fields stay reader-less.

``decision.reversible`` and ``decision.deadline`` are documentation-only fields
in ``templates/ANALYSIS-SPEC.yaml`` — an operator records them for human readers,
but NO ``dsx`` check reads them. The template now says so explicitly (a
"Documentation-only — NOT gate-read" block). This test is the mechanical proof
that the label stays true: if a future change wires a gate to read
``decision.reversible`` or ``decision.deadline``, the honest label silently
becomes a lie unless something fails. This is that something.

Two proofs, not one — the same two-detectors-layered rationale as
``tests/test_frame_boundary.py`` (its lines 11-15):

  1. A blunt text-level scan for the dotted path ``decision.reversible`` /
     ``decision.deadline`` anywhere under ``dsx/`` (code, comment or message
     string). It deliberately keys on the *dotted* form so that unrelated prose
     such as ``dsx/spec.py``'s "date/deadline" window-token comment, or
     ``dsx/frame/admissibility.py``'s "irreversible" code-number comment, is not
     a false positive.
  2. A precise AST scan that names the offending line for a future contributor:
     a call-argument string literal equal to the dotted read path, a subscript
     chain ``["decision"]["reversible"|"deadline"]``, and a ``.get("reversible")``
     / ``.get("deadline")`` read.

And the scanner is shown to actually fire against deliberately-violating source
strings (plus permitted-read controls) it never has to commit as a real module —
a scan that only ever walks clean real files can never fail, which means it is
not enforcing anything.

A third, smaller invariant: the two narrative documents
(``agents/dsx-data-storyteller.md`` and ``skills/dsx-narrate/SKILL.md``) name
neither quarantined field, so the prompt cannot point a writer at an unenforced
scaffold field as though a gate reads it.

The repo checks out CRLF on Windows; every line-oriented match below tolerates
``\r?\n`` (splitlines() handles both; the doc scan lower-cases and substring-
tests, which is newline-agnostic).

Run:  python -m unittest tests.test_scaffold_quarantine -v
"""

from __future__ import annotations

import ast
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DSX_DIR = ROOT / "dsx"

# The quarantined decision fields — read by no check (D-14, grep-confirmed).
_QUARANTINED_FIELDS = ("reversible", "deadline")
_DECISION_SECTION = "decision"
# The dotted-path read form a dsx.spec.get(...) call would use.
_QUARANTINED_DOTTED = tuple(f"{_DECISION_SECTION}.{name}" for name in _QUARANTINED_FIELDS)

# CRLF-tolerant line splitter (repo checks out CRLF on Windows).
_LINE_SPLIT_RE = re.compile(r"\r?\n")

_DOC_FILES = (
    ROOT / "agents" / "dsx-data-storyteller.md",
    ROOT / "skills" / "dsx-narrate" / "SKILL.md",
)


def _scan_text_for_quarantined_dotted(text: str) -> list[str]:
    """Blunt text-level detector: flag any line containing a quarantined dotted
    read path (``decision.reversible`` / ``decision.deadline``) — in code, in a
    comment, or inside a message string. Keys on the dotted form specifically so
    unrelated prose ("date/deadline", "irreversible") is not a false positive.
    CRLF-tolerant via ``\\r?\\n`` splitting."""
    violations: list[str] = []
    for lineno, line in enumerate(_LINE_SPLIT_RE.split(text), start=1):
        for dotted in _QUARANTINED_DOTTED:
            if dotted in line:
                violations.append(f"line {lineno}: text contains {dotted!r}")
    return violations


def _subscript_key(slice_node: ast.AST) -> "str | None":
    """Return a subscript's string key, tolerating both the modern (3.9+) and
    legacy (pre-3.9 ``ast.Index``-wrapped) AST shapes. Ducktypes on the class
    name rather than referencing ``ast.Index`` directly (removed in newer
    versions). Mirrors the helper in ``tests/test_frame_boundary.py``."""
    node = slice_node
    if type(node).__name__ == "Index":
        node = node.value  # type: ignore[attr-defined]
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _scan_source_for_quarantined_reads_ast(text: str) -> list[str]:
    """Precise AST detector: flag a read of ``decision.reversible`` /
    ``decision.deadline`` in any of the three idioms dsx uses to read a spec
    field —

      * a call-argument string literal equal to the dotted path
        (``get(spec, "decision.reversible")``),
      * a subscript chain ``spec["decision"]["deadline"]``,
      * a ``.get("reversible")`` / ``.get("deadline")`` method call.
    """
    violations: list[str] = []
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # dotted-path string-literal argument
            for arg in node.args:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    if arg.value in _QUARANTINED_DOTTED:
                        violations.append(
                            f"line {node.lineno}: call argument string literal "
                            f"{arg.value!r} reads a quarantined decision field"
                        )
            # `.get("reversible")` / `.get("deadline")`
            if isinstance(node.func, ast.Attribute) and node.func.attr == "get":
                if node.args:
                    first = node.args[0]
                    if (
                        isinstance(first, ast.Constant)
                        and isinstance(first.value, str)
                        and first.value in _QUARANTINED_FIELDS
                    ):
                        violations.append(
                            f"line {node.lineno}: .get({first.value!r}) reads a "
                            f"quarantined decision field"
                        )
        elif isinstance(node, ast.Subscript):
            key = _subscript_key(node.slice)
            if key in _QUARANTINED_FIELDS and isinstance(node.value, ast.Subscript):
                inner = _subscript_key(node.value.slice)
                if inner == _DECISION_SECTION:
                    violations.append(
                        f"line {node.lineno}: subscript chain reads "
                        f"[{_DECISION_SECTION!r}][{key!r}]"
                    )
    return violations


class TestNoCheckReadsQuarantinedDecisionFields(unittest.TestCase):
    """D-14 mechanical proof: no code path under ``dsx/`` reads
    ``decision.reversible`` or ``decision.deadline``. Scans every Python file
    under the package, so a future module inherits the invariant without anyone
    remembering to extend this test."""

    def test_real_dsx_modules_read_no_quarantined_decision_field(self):
        violations: list[str] = []
        files = sorted(DSX_DIR.rglob("*.py"))
        self.assertTrue(files, "dsx/ has no *.py files to scan")
        for path in files:
            text = path.read_text(encoding="utf-8")
            for problem in _scan_text_for_quarantined_dotted(text):
                violations.append(f"{path.relative_to(ROOT)} (text): {problem}")
            for problem in _scan_source_for_quarantined_reads_ast(text):
                violations.append(f"{path.relative_to(ROOT)} (ast): {problem}")
        self.assertEqual(violations, [], "\n".join(violations))

    def test_ast_detector_fires_on_dotted_path_call_argument(self):
        for dotted in _QUARANTINED_DOTTED:
            source = f'from dsx.spec import get\nv = get(spec, "{dotted}")\n'
            with self.subTest(dotted=dotted):
                self.assertTrue(_scan_source_for_quarantined_reads_ast(source))

    def test_ast_detector_fires_on_subscript_chain(self):
        for name in _QUARANTINED_FIELDS:
            source = f'v = spec["decision"]["{name}"]\n'
            with self.subTest(name=name):
                self.assertTrue(_scan_source_for_quarantined_reads_ast(source))

    def test_ast_detector_fires_on_get_method_read(self):
        for name in _QUARANTINED_FIELDS:
            source = f'v = decision.get("{name}")\n'
            with self.subTest(name=name):
                self.assertTrue(_scan_source_for_quarantined_reads_ast(source))

    def test_text_detector_fires_on_dotted_path_including_comments(self):
        for dotted in _QUARANTINED_DOTTED:
            source = f"# a comment mentioning {dotted} here\n"
            with self.subTest(dotted=dotted):
                self.assertTrue(_scan_text_for_quarantined_dotted(source))

    def test_detectors_permit_a_gate_read_decision_field(self):
        # decision.owner / decision.revisit_when ARE read by checks — must not fire.
        for source in (
            'from dsx.spec import get\nv = get(spec, "decision.owner")\n',
            'from dsx.spec import get\nv = get(spec, "decision.revisit_when")\n',
            'v = decision.get("revisit_when")\n',
            'v = spec["decision"]["owner"]\n',
        ):
            with self.subTest(source=source):
                self.assertEqual(_scan_text_for_quarantined_dotted(source), [])
                self.assertEqual(_scan_source_for_quarantined_reads_ast(source), [])

    def test_text_detector_ignores_unrelated_date_deadline_prose(self):
        # dsx/spec.py's "date/deadline" window-token comment and
        # admissibility.py's "irreversible" comment must not be false positives.
        for source in (
            "# A date/deadline: an ISO calendar date or a fiscal-quarter date\n",
            "# finding numbers are irreversible (D-06). Splitting them\n",
        ):
            with self.subTest(source=source):
                self.assertEqual(_scan_text_for_quarantined_dotted(source), [])


class TestNarrativeDocsNameNoQuarantinedField(unittest.TestCase):
    """The storyteller prompt and the narrate skill must not point a writer at a
    reader-less scaffold field as though a gate reads it. Neither file names
    ``reversible`` or ``deadline`` (substring match, CRLF-agnostic)."""

    def test_doc_files_exist(self):
        for path in _DOC_FILES:
            with self.subTest(path=str(path)):
                self.assertTrue(path.exists(), f"missing doc file: {path}")

    def test_doc_files_name_neither_quarantined_field(self):
        offenders: list[str] = []
        for path in _DOC_FILES:
            lowered = path.read_text(encoding="utf-8").lower()
            for name in _QUARANTINED_FIELDS:
                if name in lowered:
                    offenders.append(f"{path.relative_to(ROOT)} names {name!r}")
        self.assertEqual(offenders, [], "\n".join(offenders))


if __name__ == "__main__":
    unittest.main(verbosity=2)
