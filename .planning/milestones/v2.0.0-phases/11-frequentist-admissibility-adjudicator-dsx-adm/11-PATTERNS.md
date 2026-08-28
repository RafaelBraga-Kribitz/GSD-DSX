# Phase 11: Frequentist admissibility adjudicator (`DSX-ADM-*`) - Pattern Map

**Mapped:** 2026-08-20
**Files analyzed:** 13 (4 new, 9 modified/extended — per 11-CONTEXT.md and 11-RESEARCH.md)
**Analogs found:** 12 / 13

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `references/families.yaml` | config/data | batch (loaded once, read-only) | `references/finding-codes.md` shape via `dsx.loader.load()` idiom used on `templates/ANALYSIS-SPEC.yaml` | role-match |
| `dsx/frame/admissibility.py` (module: `check(spec, applies_to_frame)`, `admissible_families(spec)`) | frame-layer check module | CRUD-ish (load ontology, filter/rank, emit findings) | `dsx/frame/prereg.py` (primary), `dsx/checks/stats.py::recommend_test`/`_check_declared_test` split | exact (prereg.py), role-match (stats.py split) |
| `dsx/frame/paradigm.py` (new `applies_to_frequentist_admissibility` helper) | frame-layer helper | request-response (pure predicate) | itself — `_check_monitoring_discipline`'s paradigm-branch idiom in same file | exact |
| `dsx/spec.py` (`ESTIMAND_TYPES` vocabulary + `_VALIDITY_FRAME_MEMBERSHIP` row) | model/vocabulary registry | CRUD (static registration) | existing `_VOCABULARIES`/`_VALIDITY_FRAME_MEMBERSHIP` rows (e.g. `DEPENDENCE_STRUCTURES`) | exact |
| `dsx/cli.py` (`CHECKS`, `GATE_PROFILES`, `run_checks`, `cmd_recommend`) | controller/route dispatch | request-response | itself — `"prereg"` special-case branch in `run_checks`; `cmd_recommend`'s existing 13-line body | exact |
| `scripts/gen-finding-catalogue.py` (`check_families_citations`, `_D05_ALLOWLIST_PREFIXES`, `sys.path` edit) | build-time validation script | batch | itself — `check_d05()`'s sibling-function shape and `_D05_ALLOWLIST_PREFIXES` tuple | exact |
| `tests/test_families_yaml.py` | test | batch/transform | `tests/test_frame_boundary.py` (dual-path parser proof style), `dsx.loader` round-trip usage in RESEARCH.md | role-match |
| `tests/test_frame_admissibility.py` | test | request-response | existing `tests/test_dsx.py` patterns for `prereg.check(...)`-style Report assertions (not read in full; inferred from `prereg.py` docstrings naming `TestRuleResolutionFindings`) | role-match |
| `tests/test_frame_boundary.py` (new reverse-direction scanner) | test | transform (AST scan) | itself — `_scan_source_for_checks_imports`/`TestFrameImportBoundary` | exact |
| `tests/test_gen_finding-catalogue.py` (extend) | test | batch | not read in full this session; extend existing test style per its own conventions | role-match |
| `references/finding-codes.md` | generated doc | batch | regenerated via `scripts/gen-finding-catalogue.py --write` — no hand-editing | exact |
| `references/test-selection.md` | doc (D-27 fix) | — | — | n/a (prose fix, no code analog needed) |
| nine committed example specs (`examples/*.yaml`, `examples/known-bad/*.yaml`, `templates/ANALYSIS-SPEC.yaml`) | fixture/data | — | `examples/good-ANALYSIS-SPEC.yaml`'s existing `estimand:` sub-block (already always-required) | exact |

## Pattern Assignments

### `dsx/frame/admissibility.py` (frame-layer check module)

**Primary analog:** `dsx/frame/prereg.py` (Phase 10, most recent frame module; takes an extra
routing parameter from `run_checks`, exactly D-22's shape).
**Secondary analog:** `dsx/checks/stats.py` (`recommend_test` / `_check_declared_test` pure/wrapper split, for `admissible_families()` vs `check()`).

**Module docstring + citation format** (`dsx/frame/prereg.py:1-18`):
```python
"""DSX-PRE-* — pre-registered inference plan reconciliation (Phase 10).

The declared fallback rule is the preregistered test-selection function, and the
executed procedure is the test-selection function evaluated on the data ...

Citation: Gelman, A. and Loken, E. (2014), "The Statistical Crisis in Science",
American Scientist 102(6):460-465, page 460, unnumbered section "How to Test a
Hypothesis". ...
"""

from __future__ import annotations

import operator
import re
from dataclasses import dataclass

from ..decisions import DecisionRecord, decisions_path, frame_digest, read_all
from ..findings import CheckError, Report
from ..spec import PREREG_FACTS, as_number, get, is_blank, items, normalize
```
Mirror this shape exactly for `admissibility.py`'s imports: `from ..decisions import DecisionRecord`, `from ..findings import Report` (never import anything from `dsx.checks` — D-03a, mechanically enforced by `tests/test_frame_boundary.py`), `from ..spec import get, is_blank, normalize` (and the new `ESTIMAND_TYPES` if referenced for validation, though D-03a means the *vocabulary constant* lives in `dsx/spec.py`, not the alias/family data).

**Entry point signature and dispatch** (`dsx/frame/prereg.py:623-651`):
```python
def check(spec: dict, root: "str | None" = None, *, reconcile_trail: bool = False) -> Report:
    """Emit the pre-registered inference plan findings (``DSX-PRE-*``).

    Degrades to an empty report, never a traceback, when ``spec`` is not a dict, ...
    """
    report = Report(check="prereg")

    if not isinstance(spec, dict):
        return report

    resolution = _resolve_branch(spec)
    _check_rule_resolves(spec, resolution, report)
    _check_procedure_reconciliation(spec, resolution, report)

    if reconcile_trail:
        _check_content_lock(spec, root, report)

    return report
```
`admissibility.check(spec, applies_to_frame: bool) -> Report` follows the same shape: degrade to empty `Report(check="admissibility")` on non-dict `spec`; the `applies_to_frame` bool (never a paradigm string — D-22/D-07) gates whether the two findings are emitted at all, mirroring how `reconcile_trail` gates `_check_content_lock`.

**Finding emission with detail/remedy/where** (`dsx/frame/prereg.py:247-258`):
```python
report.add(
    "DSX-PRE-010",
    "CRITICAL",
    "Declared fallback rule does not resolve to a branch",
    detail=resolution.reason,
    remedy=(
        "Declare the fact the rule names in the closed prereg fact registry "
        f"({', '.join(sorted(PREREG_FACTS))}), or rewrite the rule to "
        "reference one of those registry facts."
    ),
    where="inference.fallback_rule",
)
```
Copy this exact `report.add(code, severity, title, detail=..., remedy=..., where=...)` call shape for both `DSX-ADM-010` (HIGH) and `DSX-ADM-020` (CRITICAL). `where` should point at `inference.primary_procedure` or `validity_frame.estimand.type` / `validity_frame.dependence.structure` depending on which of D-16's three collapsed causes fired.

**DecisionRecord emission, including `escalate`/`alternatives_rejected`** (`dsx/frame/prereg.py:260-285`, dataclass shape at `dsx/decisions.py:65-83`):
```python
report.context.setdefault("decisions", []).append(
    DecisionRecord(
        id="",
        invocation_id="",
        layer="deterministic",
        choice=(
            f"DSX-PRE-010 {'fired' if fired else 'clear'}: "
            f"{resolution.reason or 'rule resolves to exactly one branch, or is inert prose'}"
        ),
        inputs=inputs,
        rule="...",
        citation="Gelman & Loken (2014), The Statistical Crisis in Science, page 460",
        counterfactual="...",
    ).to_dict()
)
```
`DecisionRecord` fields (`dsx/decisions.py:65-83`) already include `escalate: bool = False` and `alternatives_rejected: list[str] = field(default_factory=list)` — Phase 11 is the first check to actually pass non-default values for these two kwargs. For the `DSX-ADM-020` refusal path, pass `escalate=True`; for `DSX-ADM-010`/successful ranking, populate `alternatives_rejected` with the ranked-but-not-top family ids.

**Pure/wrapper split** (`dsx/checks/stats.py:32-46` header, RESEARCH.md's excerpt at lines 850-860):
```python
def recommend_test(outcome_type, n_groups, paired=False, ...) -> dict[str, object]:
    """Pure and total — every input combination yields a recommendation. No Report,
    no findings, no side effects."""
    ...
```
`admissible_families(spec) -> dict` in `dsx/frame/admissibility.py` must be this same pure, `Report`-free function; `check()` calls it internally and translates the result into findings — do not fold ranking logic and finding-emission into one function.

---

### `dsx/frame/paradigm.py` (new `applies_to_frequentist_admissibility` helper, D-22)

**Analog:** itself — the existing `_check_monitoring_discipline` paradigm-membership branch and `_PARADIGM_CONDITIONAL` table in the same file.

**Existing paradigm-conditional table already lists `"DSX-ADM-"`** (`dsx/frame/paradigm.py:54-57`):
```python
_PARADIGM_CONDITIONAL: "dict[str, tuple[str, ...]]" = {
    "frequentist": ("DSX-PAR-010", "DSX-ADM-"),
    "bayesian": ("DSX-PAR-011",),
}
```
And the not-shipped-yet honesty table (`:65-67`) already documents the phase:
```python
_NOT_SHIPPED: "dict[str, str]" = {
    "DSX-ADM-": "Phase 11 ships DSX-ADM-* (frequentist procedure admissibility).",
}
```
Remove `"DSX-ADM-"` from `_NOT_SHIPPED` once the module ships.

**Locator-honesty citation convention** (`dsx/frame/paradigm.py`, referenced at `:66-72` per CONTEXT.md D-09) — mirror this for every `families.yaml` entry's `locator_status: verified | unverified` field; do not silently omit an unconfirmed locator.

**New helper — write it as a plain boolean predicate, never reading/naming `inference.paradigm` as a string literal outside `paradigm.py` itself:**
```python
def applies_to_frequentist_admissibility(spec: dict) -> bool:
    """True when DSX-ADM-* should be evaluated against this frame (D-22): the declared
    inference.paradigm is 'frequentist', or no recognised paradigm is declared at all —
    undeclared/unrecognised widens to every paradigm-conditional family, matching
    _check_monitoring_discipline's own fallback, so an honest paradigm declaration never
    costs more than silence (D-10)."""
    declared = get(spec, "inference.paradigm")
    paradigm = normalize(declared) if not is_blank(declared) else ""
    return paradigm not in PARADIGMS or paradigm == "frequentist"
```
This is the only place in the codebase permitted to read `inference.paradigm` under D-11/D-07 (`tests/test_frame_boundary.py:145` exempts only `paradigm.py`).

---

### `dsx/spec.py` (new `ESTIMAND_TYPES` vocabulary + membership row)

**Analog:** existing `_VOCABULARIES` entries and `_VALIDITY_FRAME_MEMBERSHIP` rows.

**Existing membership table shape** (`dsx/spec.py:838-853`):
```python
_VALIDITY_FRAME_ALWAYS_REQUIRED = (
    "estimand", "units", "measurement", "dependence", "sampling_frame", "missingness",
)
_VALIDITY_FRAME_CAUSAL_REQUIRED = ("identification", "interference", "triggering", "stability")

# (sub-block, sub-field, closed vocabulary). `dependence.method_family_required` reuses
# VARIANCE_ADJUSTMENTS verbatim (M-09) — no parallel set is defined for it.
_VALIDITY_FRAME_MEMBERSHIP: "tuple[tuple[str, str, Any], ...]" = (
    ("identification", "strength", IDENTIFICATION_STRENGTHS),
    ("identification", "constraint_source", CONSTRAINT_SOURCES),
    ("dependence", "structure", DEPENDENCE_STRUCTURES),
    ("dependence", "method_family_required", VARIANCE_ADJUSTMENTS),
    ("interference", "risk", INTERFERENCE_RISKS),
    ("interference", "mitigation", INTERFERENCE_MITIGATIONS),
    ("triggering", "analysis_population", ANALYSIS_POPULATIONS),
    ("missingness", "mechanism", MISSINGNESS_MECHANISMS),
    ...
)
```
Add `ESTIMAND_TYPES = {...}` (name -> description dict, same shape as every other vocabulary), register it in `_VOCABULARIES` (name `"estimand_types"`), and add `("estimand", "type", ESTIMAND_TYPES)` as a new row to `_VALIDITY_FRAME_MEMBERSHIP`. Because `estimand` is already in `_VALIDITY_FRAME_ALWAYS_REQUIRED` and the membership loop `continue`s on blank values, this new field is structurally optional with zero new code paths (per RESEARCH.md's verified claim against `dsx/spec.py:948-967`).

---

### `dsx/cli.py` (CHECKS, GATE_PROFILES, run_checks, cmd_recommend)

**Analog:** itself.

**Import block** (`dsx/cli.py:23-52`) — `.frame` import gains `admissibility`, alphabetically:
```python
from .frame import interference, paradigm, prereg, val
```
becomes:
```python
from .frame import admissibility, interference, paradigm, prereg, val
```

**CHECKS registry** (`dsx/cli.py:63-82`):
```python
CHECKS: dict[str, Callable] = {
    "spec": validate_structure,
    ...
    "prereg": prereg.check,
}
```
Add `"admissibility": admissibility.check` for discoverability even though it is always intercepted by the special-case branch below (mirrors `"design"`'s / `"prereg"`'s own already-shipped precedent of being in `CHECKS` yet special-cased in `run_checks`).

**GATE_PROFILES** (`dsx/cli.py:100-113`) — add `"admissibility"` to `plan`, `verify`, `ship`; absent from `execute` (D-20):
```python
GATE_PROFILES: dict[str, tuple[str, ...]] = {
    "plan": ("spec", "design", "metrics", "coherence", "paradigm", "val", "interference"),
    "execute": ("spec", "ml", "repro", "dq", "code", "paradigm"),
    "verify": (
        "spec", "design", "stats", "ml", "metrics", "claims", "viz", "repro",
        "dq", "coherence", "smells", "figures", "narrative", "code", "decision",
        "paradigm", "val", "interference", "prereg",
    ),
    "ship": ( ... same as verify ... ),
}
```

**`run_checks` special-case dispatch pattern** (`dsx/cli.py:171-200`) — the exact precedent D-22 follows (an existing branch computing a routing value before dispatch, e.g. `prereg`'s `reconcile_trail`):
```python
strict = gate_point in {"verify", "ship"}
reconcile_trail = gate_invocation and gate_point in {"verify", "ship"}
root = resolve_root or phase_dir
for name in names:
    ...
    elif name == "prereg":
        reports.append(prereg.check(spec, root, reconcile_trail=reconcile_trail))
    elif name in CHECKS:
        reports.append(CHECKS[name](spec))
    else:
        raise CheckError(...)
```
Add a new `elif name == "admissibility":` branch computing `paradigm.applies_to_frequentist_admissibility(spec)` and passing it in — same idiom as `reconcile_trail`, computed outside the check module (D-22).

**`cmd_recommend` composition point** (`dsx/cli.py:396-409`, current form):
```python
def cmd_recommend(args: argparse.Namespace) -> int:
    from .checks.stats import recommend_test

    recommendation = recommend_test(
        args.outcome_type,
        args.groups,
        paired=args.paired,
        normal=_tri(args.normal),
        equal_variance=_tri(args.equal_variance),
        n_per_group=args.n_per_group,
        overdispersed=_tri(args.overdispersed),
    )
    print(json.dumps(recommendation, indent=2))
    return 0
```
Extend by flat-dict merge, additive-only key (`"admissibility"`), preserving byte-identical output with no `--spec`, per RESEARCH.md's exact recommended diff (already verified against this signature) — see RESEARCH.md lines 514-541 for the full worked implementation, including the new `--spec`/`--phase-dir` flags on `p_rec`.

---

### `scripts/gen-finding-catalogue.py` (new sibling function + allowlist)

**Analog:** itself — `check_d05()`'s shape and the `_D05_ALLOWLIST_PREFIXES` tuple.

**Existing allowlist** (`scripts/gen-finding-catalogue.py:57-68`):
```python
_D05_ALLOWLIST_PREFIXES = ("DSX-PAR-", "DSX-VAL-", "DSX-INT-", "DSX-PRE-")
```
Add `"DSX-ADM-"` (D-25) — this is an **inclusion** list; omitting the prefix means `--check` passes green while enforcing nothing.

**New sibling function** (D-23/D-24), full recommended body already worked out in RESEARCH.md (lines 659-691) — read `references/families.yaml` via `dsx.loader.load()` (requires a new `sys.path.insert(0, str(ROOT))` line, confirmed absent from the script today), and fail on any family entry with a blank/missing `citation`. Wire into `main()`'s `--check` branch alongside the existing `check_d05(...)` call (`scripts/gen-finding-catalogue.py:312-316` per RESEARCH.md), prefixed `"D-24:"` in stderr output (distinct from `"D-05:"`) to disambiguate the two mechanisms.

**PREFIX_GROUPS table** (`scripts/gen-finding-catalogue.py:24-49`) — add a new `("DSX-ADM", "Frequentist admissibility", "...")` row, matching the existing tuple shape used by every other prefix group (e.g. the `DSX-PRE` row: `("DSX-PRE", "Pre-registered inference plan", "The declared fallback rule resolved against ... ")`).

---

### `tests/test_frame_boundary.py` (D-04a reverse-direction scanner)

**Analog:** itself — `TestFrameImportBoundary`/`_scan_source_for_checks_imports` (`tests/test_frame_boundary.py:1-60+`).

```python
"""D-03a import-boundary enforcement for ``dsx/frame/``. ...
Modules under ``dsx/frame/`` may import from ``dsx.findings``, ``dsx.spec``,
``dsx.loader`` and ``dsx.decisions`` — never from ``dsx.checks`` (T-6-01). ...
"""
from __future__ import annotations

import ast
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import dsx.frame  # noqa: E402

FRAME_DIR = Path(dsx.frame.__file__).resolve().parent
_FORBIDDEN_PACKAGE = "dsx.checks"
```
Add the mirror-image scanner: iterate `dsx/checks/**/*.py` (new `CHECKS_DIR`), reuse `_package_for`/AST-import-resolution helpers already in this file, and assert no file under `dsx/checks/` imports `dsx.frame` or a submodule of it. This is D-04a's cheapest-moment closure — reuse the existing AST machinery, do not hand-roll a second one.

---

## Shared Patterns

### Frame-module `check(spec) -> Report` shape with routing param
**Source:** `dsx/frame/prereg.py:623-651`
**Apply to:** `dsx/frame/admissibility.py::check`
```python
def check(spec: dict, root: "str | None" = None, *, reconcile_trail: bool = False) -> Report:
    report = Report(check="prereg")
    if not isinstance(spec, dict):
        return report
    ...
    return report
```

### DecisionRecord emission (first user of `escalate`/`alternatives_rejected`)
**Source:** `dsx/decisions.py:65-88`, usage pattern at `dsx/frame/prereg.py:260-285`
**Apply to:** all `DSX-ADM-*` finding emission
```python
@dataclass(frozen=True)
class DecisionRecord:
    id: str
    invocation_id: str
    layer: str
    choice: str
    inputs: "list[str]" = field(default_factory=list)
    rule: str = ""
    citation: str = ""
    counterfactual: str = ""
    alternatives_rejected: "list[str]" = field(default_factory=list)
    confidence: "str | None" = None
    escalate: bool = False

    def to_dict(self) -> "dict[str, Any]":
        out = asdict(self)
        out["record_type"] = "decision"
        return out
```

### Finding emission (`Report.add`)
**Source:** `dsx/findings.py:101-121`
**Apply to:** `DSX-ADM-010`/`DSX-ADM-020`
```python
def add(self, code, severity, title, detail="", remedy="", where="", **data) -> Finding:
    finding = Finding(code=code, severity=Severity.parse(severity), title=title,
                       detail=detail, remedy=remedy, where=where, data=data)
    self.findings.append(finding)
    return finding
```

### Paradigm-boundary honesty and `_NOT_SHIPPED` bookkeeping
**Source:** `dsx/frame/paradigm.py:51-67`
**Apply to:** removing the `"DSX-ADM-"` entry from `_NOT_SHIPPED` once this phase ships; confirming `_PARADIGM_CONDITIONAL["frequentist"]` already contains `"DSX-ADM-"` (no edit needed there — verify only).

### Vocabulary registration idiom
**Source:** `dsx/spec.py:838-853` (`_VALIDITY_FRAME_MEMBERSHIP`), `_VOCABULARIES` list
**Apply to:** `ESTIMAND_TYPES` registration — same dict-of-name-to-description shape, same membership-row tuple shape, blank-skips-validation already built in.

### Citation/docstring D-05 format (Citation:, Structural criterion:/Reference value:, Falsifier:)
**Source:** `dsx/frame/prereg.py:207-234`, `:288-319`
**Apply to:** both `_check_*` helper docstrings inside `admissibility.py` — every `report.add(...)` call site needs an enclosing docstring with a `Citation:` line and a `Structural criterion:`/`Reference value:` line for `check_d05()` (existing mechanism) to find once `"DSX-ADM-"` is allowlisted.

## No Analog Found

| File | Role | Data Flow | Reason |
|---|---|---|---|
| `references/families.yaml` schema itself | config/data | batch | No prior `dsx/` data file has this exact three-key top-level shape (header flag + two block sequences); closest precedent is `dsx/loader.py`'s general contract (top level must be a mapping) plus RESEARCH.md's own verified worked example (reproduced in RESEARCH.md "Families.yaml Schema" section) — use that worked example directly, it was executed and round-tripped in the research session |
| `dsx/input_types.py` missing-file behaviour | precedent to **avoid** | file-I/O | CONTEXT.md D-05 explicitly departs from this file's graceful-empty-catalogue-on-missing-file pattern (`dsx/input_types.py:32-33`); `admissibility.py` must instead raise `CheckError` on a missing/unreadable `families.yaml`, following `cli.py:594`'s idiom for `templates/ANALYSIS-SPEC.yaml` instead |

## Metadata

**Analog search scope:** `dsx/frame/*.py`, `dsx/checks/stats.py`, `dsx/cli.py`, `dsx/spec.py`, `dsx/decisions.py`, `dsx/findings.py`, `dsx/input_types.py`, `dsx/loader.py`, `scripts/gen-finding-catalogue.py`, `tests/test_frame_boundary.py`
**Files scanned:** 12 read directly (several in full per RESEARCH.md's own sourcing), 4 line-ranged via grep + targeted `Read`
**Pattern extraction date:** 2026-08-20
