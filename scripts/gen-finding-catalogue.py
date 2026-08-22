#!/usr/bin/env python3
"""Regenerate references/finding-codes.md from the source of truth.

The catalogue is extracted from the actual `report.add(...)` calls, so it cannot
drift from what the checks emit. Run after adding or changing any finding:

    python3 scripts/gen-finding-catalogue.py --write

Exits 1 when the checked-in catalogue is stale, which makes it usable as a CI gate:

    python3 scripts/gen-finding-catalogue.py --check
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "references" / "finding-codes.md"

PREFIX_GROUPS = [
    ("DSX-SPEC", "Contract structure", "Shape and vocabulary of ANALYSIS-SPEC itself."),
    ("DSX-EXP", "Experiment design", "Power, allocation, units, duration, multiplicity, peeking."),
    ("DSX-CAU", "Causal identification", "Whether the design licenses a causal reading."),
    ("DSX-STA", "Statistical validity", "Test selection, assumptions, and the reporting contract."),
    ("DSX-ML", "ML integrity", "Leakage, splits, metric choice, baselines, evaluation hygiene."),
    ("DSX-MET", "Metric semantics", "Definitions, reconciliation, drift, Simpson's paradox."),
    ("DSX-SQL", "SQL correctness", "Fan-out, NULL semantics, aggregation order."),
    ("DSX-CLM", "Claim discipline", "Causal language, evidence, generalisation, precision."),
    ("DSX-NAR", "Narrative discipline", "Deliverable path, claim⊆narrative, forbidden wording."),
    ("DSX-CODE", "Code reality", "Fit-before-split and leakage smells in the entrypoint."),
    ("DSX-DEC", "Decision replay", "Structured decision.replay thresholds vs results.tests."),
    ("DSX-VIZ", "Visualization", "Encoding correctness, proportionality, uncertainty, access."),
    ("DSX-REP", "Reproducibility", "Seeds, environment, data identity, entrypoint, repro_lock."),
    ("DSX-DQ", "Data quality", "Hermetic assertions against DATA-PROFILE artifacts."),
    ("DSX-COH", "Coherence", "Question ↔ claim ↔ decision agreement."),
    ("DSX-FIG", "Figure seals", "Artifact paths and svg_sha256 hermetic seals."),
    ("DSX-SMELL", "Plot smells", "Declaration-based plot-construction smells."),
    ("DSX-PAR", "Paradigm and monitoring discipline",
     "The declared inferential paradigm manifest and its symmetric peeking-monitoring pair."),
    ("DSX-VAL", "Validity frame",
     "Estimand, unit triad, dependence, identification, sampling frame, missingness and "
     "measurement content — whether a validity_frame block that is present and structurally "
     "well-formed is also internally coherent."),
    ("DSX-INT", "Interference, triggering and stability",
     "Interference and SUTVA risk, triggered-versus-eligible dilution, and novelty or primacy "
     "over the declared stability window."),
    ("DSX-PRE", "Pre-registered inference plan",
     "The declared fallback rule resolved against the declared observed facts, the plan-time "
     "content lock, and reconciliation of the declared branch against the executed procedure."),
    ("DSX-ADM", "Frequentist admissibility",
     "The ranked admissible set for a declared frequentist frame, naming the assumptions each "
     "family buys and charges, and the refusal when no procedure in the ontology is admissible."),
]

# D-20: the finite, visible exemption boundary for D-05 citation/reference-value
# enforcement. This list grows only as each later v2.0.0 phase adds its own
# new-in-this-milestone prefix (DSX-VAL-*, DSX-INT-*, ...) — never to exempt a
# code this milestone introduces from its citation and reference-value obligations.
# Rule: every entry here must end in a hyphen, so it can only ever match a whole
# code family (e.g. the entire DSX-PAR-* family) and never part of a numeric
# suffix — a bare numeric-string prefix like "DSX-SPEC-08" would silently admit
# any longer code sharing those digits (a future DSX-SPEC-0800, say) without a
# human noticing the allow-list needs updating. A single code that lives inside a
# pre-existing family — where a family prefix would drag the whole legacy family
# into enforcement — is named individually in `_D05_ALLOWLIST_CODES` instead.
_D05_ALLOWLIST_PREFIXES = ("DSX-PAR-", "DSX-VAL-", "DSX-INT-", "DSX-PRE-")

# The individually-enumerated half of D-20's finite, visible boundary: exact
# codes this milestone introduced inside a pre-existing family (DSX-SPEC-*,
# and — from Phase 11.1 — DSX-CODE-*), where a family prefix is not usable
# without pulling in that family's 200+ pre-existing legacy codes. Measured
# against the real tree, not copied from review prose — re-derive by
# enumerating `collect()`'s codes under the old bare-prefix match if this set
# is ever suspected stale.
#
# Phase 11.1 (REQ-P11.1-01, REQ-P11.1-03) adds DSX-CODE-020, DSX-CODE-021,
# DSX-CODE-030 and DSX-CODE-031 here, not to `_D05_ALLOWLIST_PREFIXES`:
# `DSX-CODE-*` is a pre-existing family (v1.3.0) with ~4 legacy codes
# (001-003, 010) that carry no `Citation:`/`Structural criterion:` docstring
# line and no `# D-05:` test marker. Adding the `"DSX-CODE-"` prefix to
# `_D05_ALLOWLIST_PREFIXES` would retroactively obligate every one of those
# legacy codes to carry a citation none of them have — the visible
# consequence is `scripts/check.sh --check` failing red on files this phase
# never touched. The exact-code path used here is the one Phase 6 already
# established for `DSX-SPEC-080`-`086` inside the pre-existing `DSX-SPEC-*`
# family; this is the same precedent applied to a second family.
#
# Phase 11.1 (REQ-P11.1-04) adds DSX-ML-043 here for the same reason:
# `DSX-ML-*` is a pre-existing family (v1.0.0) whose ~40 legacy codes carry
# no citation. DSX-ML-040, DSX-ML-041 and DSX-ML-042 — the three legacy
# codes sharing DSX-ML-043's enclosing function, `_check_metric_choice` —
# are deliberately NOT added here: they are pre-existing, uncited, and this
# plan only extended the function they already lived in. Naming them would
# turn the build red on a function this plan did not rewrite from scratch.
#
# Phase 11.1 (REQ-P11.1-03) adds DSX-ML-023 and DSX-ML-024 here for the same
# reason as DSX-ML-043 above: both live in `dsx/checks/ml.py`'s pre-existing
# `DSX-ML-*` family. DSX-ML-020, DSX-ML-021 and DSX-ML-022 — the legacy
# codes sharing `_check_preprocessing`, the function DSX-ML-023/024 borrow
# their shared accepted-value constant from — are deliberately NOT added
# here; this plan only extracted that constant out of _check_preprocessing
# without rewriting its citation-free body.
#
# Phase 11.1 (REQ-P11.1-05) adds DSX-ML-052 and DSX-ML-053 here for the same
# reason: both live inside `_check_baseline`, a pre-existing `DSX-ML-*`
# function. DSX-ML-050 and DSX-ML-051 — the two legacy codes sharing that
# same function — are deliberately NOT added here; this plan only extended
# the branch they already lived in, it did not rewrite their citation-free
# bodies.
#
# Phase 11.1 (REQ-P11.1-06) adds DSX-ML-090, DSX-ML-091 and DSX-ML-092 here.
# Unlike the DSX-ML-* entries above, all three live in a brand-new function,
# `_check_selection_ledger`, that this plan wrote from scratch — there is no
# legacy sibling code sharing the function to carry forward uncited.
_D05_ALLOWLIST_CODES = frozenset(
    {
        "DSX-SPEC-080", "DSX-SPEC-081", "DSX-SPEC-082", "DSX-SPEC-085", "DSX-SPEC-086",
        "DSX-CODE-020", "DSX-CODE-021", "DSX-CODE-030", "DSX-CODE-031",
        "DSX-ML-023", "DSX-ML-024", "DSX-ML-043", "DSX-ML-052", "DSX-ML-053",
        "DSX-ML-090", "DSX-ML-091", "DSX-ML-092",
    }
)

_CITATION_RE = re.compile(r"^\s*Citation:\s*\S", re.MULTILINE)
_REFVALUE_RE = re.compile(
    r"^\s*(?:Reference value|Structural criterion):\s*\S", re.MULTILINE
)
_TEST_MARKER_RE = re.compile(r"#\s*D-05:\s*(DSX-[A-Z]+-\d{3})")


def _literal(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts = []
        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                parts.append(value.value)
            else:
                parts.append("<…>")
        return "".join(parts)
    return None


def extract(path: Path) -> list[tuple[str, str, str]]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: list[tuple[str, str, str]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Attribute) and func.attr == "add"):
            continue
        if len(node.args) < 3:
            continue
        code = _literal(node.args[0])
        severity = _literal(node.args[1])
        title = _literal(node.args[2])
        if code and code.startswith("DSX-") and severity and title:
            found.append((code, severity, title.strip()))
    return found


def extract_sql_rules(path: Path) -> list[tuple[str, str, str]]:
    """Pull codes from `_SQL_RULES` tuple literals (not always passed as report.add args)."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: list[tuple[str, str, str]] = []

    def _from_list(value: ast.AST) -> None:
        if not isinstance(value, (ast.List, ast.Tuple)):
            return
        for elt in value.elts:
            if not isinstance(elt, (ast.Tuple, ast.List)) or len(elt.elts) < 4:
                continue
            code = _literal(elt.elts[0])
            severity = _literal(elt.elts[2])
            detail = _literal(elt.elts[3])
            if code and code.startswith("DSX-") and severity and detail:
                title = detail.split(".")[0].strip()
                found.append((code, severity, title))

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "_SQL_RULES":
                    _from_list(node.value)
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id == "_SQL_RULES":
                if node.value is not None:
                    _from_list(node.value)
    return found


def collect() -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []
    dsx_root = ROOT / "dsx"
    sources = sorted(dsx_root.rglob("*.py"))
    for source in sources:
        module = str(source.relative_to(dsx_root).with_suffix("")).replace("\\", "/")
        for code, severity, title in extract(source):
            rows.append((code, severity, title, module))
        if source.name == "metrics.py":
            for code, severity, title in extract_sql_rules(source):
                rows.append((code, severity, title, module))
    rows.sort(key=lambda r: r[0])
    seen: dict[str, tuple[str, str, str, str]] = {}
    for row in rows:
        if row[0] in seen and seen[row[0]][1:] != row[1:]:
            print(f"warning: {row[0]} declared twice with different text", file=sys.stderr)
        seen[row[0]] = row
    return list(seen.values())


def render(rows: list[tuple[str, str, str, str]]) -> str:
    lines = [
        "# Finding codes",
        "",
        "> Generated by `scripts/gen-finding-catalogue.py`. Do not edit by hand.",
        "",
        "Every check emits findings with a stable code. Codes are never renumbered, so",
        "a suppression or a reference in a review stays valid across versions.",
        "",
        "**Severity ladder.** `CRITICAL` — the result is invalid, not merely weak.",
        "`HIGH` — the conclusion is likely to be wrong or materially overstated.",
        "`MEDIUM` — a real defect that should be stated as a limitation if not fixed.",
        "`LOW` — presentation and hygiene.",
        "",
        "**Gate thresholds.** `plan` and `execute` block at CRITICAL; `verify` and",
        "`ship` block at HIGH.",
        "",
        f"**Total: {len(rows)} codes.**",
        "",
    ]
    for prefix, heading, blurb in PREFIX_GROUPS:
        group = [r for r in rows if r[0].startswith(prefix + "-")]
        if not group:
            continue
        lines += [f"## {heading} — `{prefix}-*`", "", blurb, "",
                  "| Code | Severity | Finding |", "|---|---|---|"]
        for code, severity, title, _module in group:
            safe_title = title.replace("|", "\\|")
            lines.append(f"| `{code}` | {severity} | {safe_title} |")
        lines.append("")
    return "\n".join(lines)


def _resolve_docstrings(code_root: Path) -> dict[str, str]:
    """Map each ``DSX-`` finding code to its enclosing function's docstring.

    Walks every ``*.py`` under ``code_root``, builds a child->parent map (the
    ``ast`` module has no parent pointers), then for every ``report.add(...)``
    call whose first argument is a ``DSX-`` string literal, walks upward to the
    nearest ``FunctionDef``/``AsyncFunctionDef`` and takes its docstring, falling
    back to the module docstring when no enclosing function is found (D-22).
    """
    docstrings: dict[str, str] = {}
    for path in sorted(code_root.rglob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError:
            continue
        parents: dict[ast.AST, ast.AST] = {}
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                parents[child] = parent
        module_doc = ast.get_docstring(tree) or ""
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if not (isinstance(func, ast.Attribute) and func.attr == "add"):
                continue
            if not node.args:
                continue
            code = _literal(node.args[0])
            if not (code and code.startswith("DSX-")):
                continue
            doc = module_doc
            current: ast.AST = node
            while current in parents:
                current = parents[current]
                if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    doc = ast.get_docstring(current) or ""
                    break
            docstrings[code] = doc
    return docstrings


def _collect_test_markers(tests_root: Path) -> set[str]:
    """Codes named by a ``# D-05: <CODE>`` comment anywhere under ``tests_root``.

    ``ast`` discards comments, so this is a raw-text regex pass, not an AST walk
    — mirrors the rationale in ``dsx/suppressions.py::known_codes()`` for staying
    text-level where AST cannot see what is needed.
    """
    markers: set[str] = set()
    for path in sorted(tests_root.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        for match in _TEST_MARKER_RE.finditer(text):
            markers.add(match.group(1))
    return markers


def check_d05(
    rows: list[tuple[str, str, str, str]], code_root: Path, tests_root: Path
) -> list[str]:
    """D-05 enforcement: citation, reference value/structural criterion, linked test.

    Only codes matching a hyphen-terminated family prefix in ``_D05_ALLOWLIST_PREFIXES``
    or named exactly in ``_D05_ALLOWLIST_CODES`` (D-20) are checked — the 206
    pre-existing legacy codes must produce zero new failures. Reports every
    problem found rather than short-circuiting on the first.
    """
    covered = [
        row
        for row in rows
        if row[0].startswith(_D05_ALLOWLIST_PREFIXES) or row[0] in _D05_ALLOWLIST_CODES
    ]
    if not covered:
        return []
    docstrings = _resolve_docstrings(code_root)
    test_markers = _collect_test_markers(tests_root)
    problems: list[str] = []
    for code, *_rest in covered:
        doc = docstrings.get(code, "")
        if not _CITATION_RE.search(doc):
            problems.append(f"{code}: missing 'Citation:' line in docstring")
        if not _REFVALUE_RE.search(doc):
            problems.append(
                f"{code}: missing 'Reference value:'/'Structural criterion:' line in docstring"
            )
        if code not in test_markers:
            problems.append(f"{code}: no '# D-05: {code}' test marker found under {tests_root}")
    return problems


def check_families_citations(families_path: Path) -> list[str]:
    """Build-time citation gate over ``references/families.yaml`` (D-23, D-24).

    This is a sibling to ``check_d05`` above, not an extension of it.
    ``check_d05`` operates exclusively on rows extracted by walking abstract
    syntax trees for ``report.add(...)`` call sites and on docstrings
    resolved from Python sources under a code root — it has no file-path
    parameter for a data file and no awareness of any data format, and until
    this function was written the script never inserted the repository root
    onto the import path, so it could not import the loader at all. This
    function supplies exactly that capability, scoped to the one data file
    it needs. It reads the ontology through ``dsx.loader`` — the same reader
    ``dsx/frame/admissibility.py`` uses at run time — and imports no YAML
    library of its own, so the build-time gate and the run-time reader can
    never disagree about what the file says.

    Returns a list of problem strings, never raises and never prints —
    ``main()`` owns all output, exactly as it does for ``check_d05``.
    """
    families_path = Path(families_path)

    root_str = str(ROOT)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
    from dsx.loader import load  # noqa: PLC0415 (import kept local, see docstring)

    try:
        data = load(families_path)
    except Exception as exc:  # a missing/unparseable/structurally-wrong file
        return [f"{families_path}: {exc}"]

    problems: list[str] = []
    for block_name, key_field in (
        ("families", "id"),
        ("assumption_vocabulary", "token"),
        ("ranking_rules", "id"),
    ):
        entries = data.get(block_name)
        if not isinstance(entries, list):
            problems.append(f"{families_path}: '{block_name}' is missing or not a list")
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue  # malformed list item — tolerated, not raised on (D-24)
            ident = entry.get(key_field, "<unknown>")
            citation = entry.get("citation")
            if citation is None or (isinstance(citation, str) and not citation.strip()):
                problems.append(
                    f"{block_name} entry '{ident}' has a missing or blank citation"
                )
    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    rows = collect()
    content = render(rows)
    if args.write:
        TARGET.parent.mkdir(parents=True, exist_ok=True)
        TARGET.write_text(content, encoding="utf-8")
        print(f"wrote {TARGET.relative_to(ROOT)}")
        return 0
    if args.check:
        exit_code = 0
        current = TARGET.read_text(encoding="utf-8") if TARGET.exists() else ""
        if current != content:
            print("finding catalogue is stale — run with --write", file=sys.stderr)
            exit_code = 1
        problems = check_d05(rows, ROOT / "dsx", ROOT / "tests")
        for problem in problems:
            print(f"D-05: {problem}", file=sys.stderr)
        if problems:
            exit_code = 1
        citation_problems = check_families_citations(ROOT / "references" / "families.yaml")
        for problem in citation_problems:
            print(f"D-24: {problem}", file=sys.stderr)
        if citation_problems:
            exit_code = 1
        if exit_code == 0:
            print("finding catalogue is current")
        return exit_code
    print(content)
    return 0


if __name__ == "__main__":
    sys.exit(main())
