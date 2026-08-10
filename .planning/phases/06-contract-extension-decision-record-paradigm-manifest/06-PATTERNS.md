# Phase 6: Contract extension, decision record, paradigm manifest - Pattern Map

**Mapped:** 2026-08-07
**Files analyzed:** 15 (10 modified, 8 new — some grouped)
**Analogs found:** 12 / 15 (3 genuinely new — no precedent)

All line numbers below were re-verified by direct read against the current repo state (not
copied blind from RESEARCH.md), except where noted.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `dsx/loader.py` (`_NULL` fix) | parser/utility | transform | itself (existing `_NULL`/`_scalar`) | exact (one-line fix) |
| `dsx/spec.py` — new vocabularies + `PEEKING_POLICIES` entry | config/model (closed vocab) | transform | `PEEKING_POLICIES`/`IDENTIFICATION_STRATEGIES` (`dsx/spec.py:31-68`) | exact |
| `dsx/spec.py::_validate_validity_frame_shape` / `_validate_inference_shape` | model/validator | request-response (structural check) | `_validate_design_shape` (`dsx/spec.py:422-479`) | exact for shape; **no precedent** for requiredness-aggregation half (see below) |
| `dsx/spec.py::describe_vocabulary` + `_VOCABULARIES` registry | config/utility | transform | current `describe_vocabulary()` body (`dsx/spec.py:544-563`) | exact (refactor of same function) |
| `dsx/decisions.py` (new) | storage/service | event-driven, append-only file I/O | **no analog** — first write path in codebase | no analog, genuinely new (fully spec'd in RESEARCH.md Pattern 5) |
| `dsx/frame/__init__.py` | package init/docstring | — | `dsx/checks/__init__.py` | role-match |
| `dsx/frame/paradigm.py` (`DSX-PAR-001`) | check module | request-response | `dsx/checks/design.py` (module shape, docstring, `report.add` idiom) | role-match, strong |
| `dsx/cli.py` — `explain` subcommand + `cmd_explain` | controller/CLI handler | request-response (read+render) | `cmd_vocab` (`dsx/cli.py:332-334`) for "always exit 0, pure print"; `cmd_validate`/`cmd_gate` for `find_spec` wiring | strong (composite) |
| `dsx/cli.py` — `add_common()` refactor (`include_block_on`) | CLI wiring | — | itself, `add_common` (`dsx/cli.py:427-433`) | exact (parametrize existing function) |
| `dsx/cli.py` — `CHECKS`/`GATE_PROFILES` gain `"paradigm"` | config/registry | — | existing `CHECKS` dict entries (`dsx/cli.py:52-67`), `GATE_PROFILES` (`:72-83`) | exact |
| `scripts/gen-finding-catalogue.py` — D-05 enforcement | build/CI script | batch (AST walk) | `extract()`/`collect()` in the same file (`:59-75`, `:108-124`); `dsx/suppressions.py::known_codes()` (`:24-54`) for the directory-AST-walk idiom | strong |
| `tests/test_frame_boundary.py` (new) | test (meta/AST) | batch | `dsx/suppressions.py::known_codes()` (`:24-54`) — closest AST-walk idiom in the codebase | role-match (no existing *test* does this, but the walk pattern is identical) |
| `tests/test_decisions.py` (new) | test | CRUD (write/read round-trip) | `TestCLI` class shape in `tests/test_dsx.py` (setup/assert idiom); no direct decisions-module precedent | no analog for subject matter, strong analog for test-file shape |
| `tests/test_gen_finding_catalogue.py` (new) | test (meta/build) | batch | same file's own existing invocation pattern (script is tested by direct import/call, confirm at implementation) | weak — script currently has no test file at all |
| `templates/ANALYSIS-SPEC.yaml`, `examples/{good,bad}-ANALYSIS-SPEC.yaml`, `examples/known-bad/*` | fixture/config | — | existing template/fixture files themselves (extend in place) | exact (same files, extended) |
| `.planning/REVERSALS.md` (new) | docs | — | no analog — first file of its kind | no analog, genuinely new (template is dictated by D-14/M-05, not code) |

## Pattern Assignments

### `dsx/loader.py` (parser, transform)

**Analog:** itself — `dsx/loader.py:32` and `:259-295` (`_scalar()`)

**Current state** (verified live):
```python
# dsx/loader.py:30-33
_TRUE = {"true", "yes", "on"}
_FALSE = {"false", "no", "off"}
_NULL = {"", "null", "~", "none"}
_NUM_RE = re.compile(r"^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$")
```

**The fix (REQ-P6-01):** drop `"none"` from the set literal:
```python
_NULL = {"", "null", "~"}
```

**Convention to replicate:** this is a single set-literal edit, not a new function. The
regression tests belong in the existing `TestLoader` class in `tests/test_dsx.py` (that class
currently spans roughly `:133-195` and has no test exercising the literal word `none` — confirmed
by RESEARCH.md's direct read). New test method naming should follow the existing
`test_<condition>` style already used in that class (no numbering prefix, plain snake_case
description).

---

### `dsx/spec.py` — new vocabularies (config, transform)

**Analog:** `PEEKING_POLICIES` / `IDENTIFICATION_STRATEGIES` (`dsx/spec.py:63-68`, `:31-47`)

**Exact shape to replicate** (verified live at `dsx/spec.py:1-95`):
```python
PEEKING_POLICIES = {
    "fixed_horizon": "One analysis at the pre-declared sample size. No interim looks.",
    "sequential_obf": "Interim looks against O'Brien-Fleming boundaries.",
    "sequential_pocock": "Interim looks against constant Pocock boundaries.",
    "always_valid": "Anytime-valid inference (mSPRT / confidence sequences).",
}
```
Every new module-level vocabulary constant is a plain `dict[str, str]` (name → one-sentence
description) at the same indentation level, grouped under the `# ── Closed vocabularies ──` banner
(`dsx/spec.py:19`). D-04 requires every *new* one to be this shape — no exceptions, no sets, even
for vocabularies that "feel" flat. New member: add `"uncontrolled_continuous": "..."` directly
into the `PEEKING_POLICIES` literal (D-01/D-02) — this is a one-entry addition, not a shape
change, since `PEEKING_POLICIES` is already a dict.

**Convention:** vocabulary constants use `UPPER_SNAKE_CASE`, are declared before any function in
the file, and are imported directly by name into `dsx/checks/*.py` (see `claims.py:19-28`'s
import block for the exact style: `from ..spec import (A, B, C, ...)`, one name per logical group,
alphabetically loose but grouped by use).

---

### `dsx/spec.py::_validate_validity_frame_shape` / `_validate_inference_shape` (validator, request-response)

**Analog:** `_validate_design_shape` (`dsx/spec.py:422-479`), quoted in full — this is the primary
template REQ-P6-02/03/09 must mirror.

```python
def _validate_design_shape(spec: dict, report: Report) -> None:
    design = section(spec, "design")
    if not design:
        return
    kind = normalize(design.get("kind", ""))
    if kind and kind not in DESIGN_KINDS:
        report.add(
            "DSX-SPEC-040",
            "HIGH",
            f"design.kind {design.get('kind')!r} is not recognised",
            detail="Allowed: " + ", ".join(sorted(DESIGN_KINDS)),
            remedy="Pick the design actually used; 'observational' is the honest default.",
            where="spec.design.kind",
        )

    strategy = normalize(design.get("identification", "")) if design.get("identification") else ""
    if strategy and strategy not in IDENTIFICATION_STRATEGIES:
        report.add(
            "DSX-SPEC-041", "HIGH",
            f"design.identification {design.get('identification')!r} is not recognised",
            detail="Allowed: " + ", ".join(sorted(IDENTIFICATION_STRATEGIES)),
            remedy="Name the strategy that licenses a causal reading, or set 'none'.",
            where="spec.design.identification",
        )
    # ... one block per sub-field: normalize() -> membership test -> report.add(code, sev, msg,
    #     detail=<allowed values joined>, remedy=<actionable next step>, where=<dotted path>)
```

Registered from `validate_structure()` (`dsx/spec.py:200-255`), which is the dispatch point the
new validators plug into:
```python
def validate_structure(spec: dict) -> Report:
    ...
    _validate_decision(spec, report)
    _validate_metrics(spec, report)
    _validate_data(spec, report)
    _validate_design_shape(spec, report)      # <- new validators join this call list
    _validate_model_shape(spec, report)
    _validate_claims_shape(spec, report)

    from .suppressions import validate_suppressions
    report.extend(validate_suppressions(spec))
    return report
```
`_validate_validity_frame_shape(spec, report)` and `_validate_inference_shape(spec, report)` must
be added to this same call chain (D-09) — no new registry, no `CHECKS` entry (already `spec` is
in every `GATE_PROFILES` tuple, `dsx/cli.py:72-83`).

**What is NOT covered by this analog — the genuinely new half.** `_validate_design_shape` never
asks *whether* `design:` should exist; it returns early on an absent section (`if not design:
return`). D-09/D-10/D-11 require the opposite for `validity_frame`: absence is itself CRITICAL,
gated by `question_type`, with aggregate-when-absent finding granularity. The two nearest partial
precedents for conditional requiredness (read in full below) do **not** cover "requiredness of a
set of sub-blocks with one aggregate finding" — that logic has no precedent in this codebase and
should be budgeted as new design work, not a copy-paste (RESEARCH.md Pitfall 3 flags this
explicitly; confirmed correct by this pass).

**Precedent 1 — `_check_limitations_required` / `DSX-CLM-080`** (`dsx/checks/claims.py:496-516`,
quoted in full, verified live):
```python
def _check_limitations_required(spec: dict, report: Report) -> None:
    qtype = normalize(spec.get("question_type", ""))
    if qtype not in {"causal", "prescriptive", "predictive"}:
        return
    limitations = spec.get("limitations")
    if isinstance(limitations, list) and any(
        isinstance(item, str) and item.strip() for item in limitations
    ):
        report.ok("limitations declared for a high-stakes question type")
        return
    report.add(
        "DSX-CLM-080",
        "HIGH",
        f"question_type {qtype!r} requires a non-empty limitations list at verify/ship",
        detail=(
            "Causal, prescriptive and predictive answers without stated limits read as "
            "complete. Put the limits where the decision-maker will see them."
        ),
        remedy="Add limitations: with at least one concrete sentence.",
        where="spec.limitations",
    )
```
This is the closest working "question_type-gated requiredness" shape. **Differences from what
Phase 6 needs:** (a) it tests one flat top-level field (`limitations`, a list), not a *set of
sub-blocks* of a section; (b) it lives in `dsx/checks/claims.py` under a `strict=` gate
(`if strict: _check_limitations_required(...)`, `claims.py:89-90`) called only at verify/ship —
D-10 instead wants `validity_frame` requiredness CRITICAL *uniformly from plan onward*, so the new
validator must NOT be gated by a `strict` flag the way this one is; (c) it emits exactly one
finding for exactly one missing thing — no aggregation logic exists here to copy.

**Precedent 2 — `_check_identification` / `DSX-CAU-010`** (`dsx/checks/design.py:477-507`, quoted
in full, verified live):
```python
def _check_identification(design: dict, spec: dict, report: Report) -> None:
    qtype = normalize(spec.get("question_type", ""))
    if qtype not in ("causal", "prescriptive"):
        return
    if not design:
        return

    kind = normalize(design.get("kind", ""))
    strategy = normalize(design.get("identification", "")) if design.get("identification") else ""

    if kind == "experiment" and not strategy:
        strategy = "randomized_experiment"

    if not strategy or strategy == "none":
        report.add(
            "DSX-CAU-010", "CRITICAL",
            f"Causal question with no identification strategy (design.kind={kind or 'unset'})",
            detail=(...),
            remedy=(...),
            where="spec.design.identification",
        )
        return
    # ... further per-field checks (DSX-CAU-011, DSX-CAU-012) follow the same section
```
This is the closest precedent for a **single required field** gated by `question_type`, at
CRITICAL severity (matching D-10's chosen severity). **Differences from what Phase 6 needs:** (a)
it requires one scalar field (`design.identification`) within an already-present section, not a
whole sub-block's presence; (b) it never aggregates — it is one `report.add` per distinct defect,
each independently triggered, not "list every missing thing in one `detail` string" (D-11); (c) it
lives in `dsx/checks/design.py`, a semantic check module, not `dsx/spec.py`'s structural layer —
D-09 deliberately puts the new validator in `dsx/spec.py` instead, which is itself a new
combination (a *shape* file doing a *requiredness* judgement).

**Aggregation logic the planner must design fresh (no precedent):**
```python
# Illustrative only (from RESEARCH.md) — exact code numbers/lists are Claude's Discretion,
# EXCEPT the always-required / causal-only split, which is LOCKED by CONTEXT.md R-01:
#   Always required (6): estimand, units, measurement, dependence, sampling_frame, missingness
#   Causal/experimental only (4): identification, interference, triggering, stability
def _validate_validity_frame_shape(spec: dict, report: Report) -> None:
    block = spec.get("validity_frame")
    qtype = normalize(spec.get("question_type", ""))
    design_kind = normalize(get(spec, "design.kind", ""))
    needs_causal_block = qtype in ("causal", "experimental") or design_kind == "experiment"

    required = list(_VALIDITY_FRAME_ALWAYS_REQUIRED)
    if needs_causal_block:
        required += list(_VALIDITY_FRAME_CAUSAL_REQUIRED)

    if not isinstance(block, dict) or not block:
        report.add(
            "DSX-SPEC-080", "CRITICAL",
            "validity_frame block is entirely absent",
            detail="Missing sub-blocks: " + ", ".join(required),   # aggregate, D-11
            remedy="Add validity_frame: with at least " + ", ".join(required) + ". "
                   "See templates/ANALYSIS-SPEC.yaml.",
            where="spec.validity_frame",
        )
        return

    missing = [n for n in required if not isinstance(block.get(n), dict) or not block[n]]
    if missing:
        report.add(  # one finding per D-11 when block present but sub-blocks missing — the
                      # skeleton above shows one aggregate call; D-11 actually requires ONE
                      # FINDING PER SUB-BLOCK in this branch (block-present case), not one
                      # aggregate call — implement the loop as N separate report.add() calls here,
                      # not the single call shown in this illustrative sketch.
            ...
        )
```
**Note the discrepancy in the RESEARCH.md sketch:** it shows one `report.add` for the
block-present-but-missing-sub-blocks case, but D-11 explicitly states "block present but a
required sub-block missing → **one finding per sub-block**." The planner must implement a loop of
separate `report.add(...)` calls in that branch, each `where=f"spec.validity_frame.{name}"`, not
a single aggregate call — only the block-entirely-absent case gets one aggregate finding.

---

### `dsx/spec.py::describe_vocabulary` + `_VOCABULARIES` registry (config/utility, transform)

**Analog:** current `describe_vocabulary()` body (`dsx/spec.py:544-563`, verified live):
```python
def describe_vocabulary() -> dict[str, Iterable[str]]:
    """Machine-readable dump of every closed vocabulary — used by `dsx vocab`."""
    return {
        "question_types": sorted(QUESTION_TYPES),
        "design_kinds": sorted(DESIGN_KINDS),
        "identification_strategies": sorted(IDENTIFICATION_STRATEGIES),
        "claim_types": sorted(CLAIM_TYPES),
        "multiplicity_corrections": sorted(MULTIPLICITY_CORRECTIONS),
        "peeking_policies": sorted(PEEKING_POLICIES),   # BUG (D-03): sorted(dict) = keys only
        "ml_tasks": sorted(ML_TASKS),
        "split_strategies": sorted(SPLIT_STRATEGIES),
        "variance_adjustments": sorted(VARIANCE_ADJUSTMENTS),
        "metric_types": sorted(METRIC_TYPES),
        "data_input_types": sorted(DATA_INPUT_TYPES),
        "renderers": sorted(RENDERERS),
        "series_roles": sorted(SERIES_ROLES),
        "chart_capabilities": {
            key: sorted(values) for key, values in sorted(CHART_CAPABILITIES.items())
        },
    }
```
Confirmed live: `"peeking_policies": sorted(PEEKING_POLICIES)` discards descriptions exactly as
RESEARCH.md states — `sorted()` on a dict sorts and returns only its keys.

**Replacement pattern (D-05, registry-based)** — this is new code but directly modeled on the
existing function's own return-dict shape:
```python
_VOCABULARIES: "list[tuple[str, Any]]" = [
    ("question_types", QUESTION_TYPES),
    ("design_kinds", DESIGN_KINDS),
    ("identification_strategies", IDENTIFICATION_STRATEGIES),
    ("claim_types", CLAIM_TYPES),
    ("multiplicity_corrections", MULTIPLICITY_CORRECTIONS),
    ("peeking_policies", PEEKING_POLICIES),
    ("ml_tasks", ML_TASKS),
    ("split_strategies", SPLIT_STRATEGIES),
    ("variance_adjustments", VARIANCE_ADJUSTMENTS),
    ("metric_types", METRIC_TYPES),
    ("data_input_types", DATA_INPUT_TYPES),
    ("renderers", RENDERERS),
    ("series_roles", SERIES_ROLES),
    # NEW this phase, every one a name->description dict per D-04:
    ("identification_strengths", IDENTIFICATION_STRENGTHS),
    ("constraint_sources", CONSTRAINT_SOURCES),
    ("dependence_structures", DEPENDENCE_STRUCTURES),
    ("interference_risks", INTERFERENCE_RISKS),
    ("interference_mitigations", INTERFERENCE_MITIGATIONS),
    ("missingness_mechanisms", MISSINGNESS_MECHANISMS),
    ("paradigms", PARADIGMS),
    ("paradigm_justifications", PARADIGM_JUSTIFICATIONS),
]

def describe_vocabulary() -> "dict[str, Any]":
    out: "dict[str, Any]" = {}
    for key, value in _VOCABULARIES:
        out[key] = ({k: value[k] for k in sorted(value)} if isinstance(value, dict)
                     else sorted(value))
    out["chart_capabilities"] = {
        key: sorted(values) for key, values in sorted(CHART_CAPABILITIES.items())
    }
    return out
```
**Convention to replicate:** `dsx/cli.py::cmd_vocab` (`:332-334`) is an unchanged thin wrapper —
`print(json.dumps(describe_vocabulary(), indent=2))` — and must stay that way; all dump logic
lives in `describe_vocabulary()` itself, never in the CLI layer.

**Coverage test convention:** add to `tests/test_dsx.py` (there is no dedicated vocab test class
today — search for the nearest existing spec-vocabulary test in `TestSpecStructure` and follow its
assertion style: direct dict/key membership assertions, no mocking framework, plain `unittest`
`assertIn`/`assertEqual`).

---

### `dsx/decisions.py` (new top-level module) — storage/service, append-only file I/O

**No analog exists in this codebase.** Confirmed: `dsx/loader.py` has a read path only (`load()`/
`loads()`), no writer anywhere in `dsx/`. This is the first append-only artifact writer in the
project. Do not force-fit this onto `dsx/loader.py` or `dsx/suppressions.py` — RESEARCH.md's
Pattern 5 (already reproduced verbatim in `06-RESEARCH.md`, lines ~604-687) is the fully-specified
design and should be implemented close to verbatim:

```python
# dsx/decisions.py — new top-level module, peer to findings.py/spec.py
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class DecisionRecord:
    id: str
    layer: str                     # "deterministic" | "stochastic"
    choice: str
    inputs: "list[str]" = field(default_factory=list)
    rule: str = ""
    citation: str = ""
    counterfactual: str = ""
    alternatives_rejected: "list[str]" = field(default_factory=list)
    confidence: "str | None" = None
    escalate: bool = False

    def to_dict(self) -> "dict[str, Any]":
        return asdict(self)


def append(path: "str | Path", record: DecisionRecord) -> None:
    line = json.dumps(record.to_dict(), sort_keys=True)
    with Path(path).open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def read_all(path: "str | Path") -> "list[dict]":
    p = Path(path)
    if not p.exists():
        return []
    records: "list[dict]" = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records
```

**Nearest structural analog for dataclass shape:** `Finding` in `dsx/findings.py` — a frozen
dataclass with a `to_dict()`-equivalent method (verify exact field/method names when implementing
against the current `dsx/findings.py`; RESEARCH.md asserts this without full quotation — read
`dsx/findings.py` directly before implementing to confirm the exact `Finding` shape/serialization
method name).

**Path resolution — analog is `find_spec()`** (`dsx/cli.py:95-114`, quoted in full, verified
live):
```python
def find_spec(explicit: "str | None", phase_dir: "str | None") -> Path:
    if explicit:
        path = Path(explicit)
        if not path.exists():
            raise CheckError(f"spec not found: {path}")
        return path

    roots = [Path(phase_dir)] if phase_dir else []
    roots.extend([Path.cwd(), Path.cwd() / ".planning"])
    for root in roots:
        for name in DEFAULT_SPEC_NAMES:
            candidate = root / name
            if candidate.exists():
                return candidate
    ...
```
D-14 says `DECISIONS.jsonl` resolves "the way `find_spec()` already resolves the spec" — in
practice this means reusing the `resolve_root` value already threaded through `run_checks()`
(`dsx/cli.py:117-134`, e.g. `cmd_gate`'s `args.phase_dir or str(path.parent)` at `dsx/cli.py:244`),
not re-implementing `find_spec()`'s search loop. `DECISIONS.jsonl` sits beside the resolved spec
(`path.parent / "DECISIONS.jsonl"`), it does not need its own multi-root search.

---

### `dsx/frame/paradigm.py` (`DSX-PAR-001`) — check module, request-response

**Analog:** `dsx/checks/design.py` module shape (docstring + import block, verified live at
`dsx/checks/design.py:1-30`):
```python
"""Experiment and causal-identification checks. Codes DSX-EXP-* and DSX-CAU-*.

These are the checks that compute rather than opine. When the spec declares a
baseline, an MDE, an alpha and a power target, the required sample size is not a
matter of judgement — it is arithmetic, and so is the verdict on whether the
planned sample meets it.
"""

from __future__ import annotations

from ..findings import Report
from ..mathx import (...)
from ..spec import (
    IDENTIFICATION_STRATEGIES,
    as_number,
    get,
    is_blank,
    items,
    normalize,
    section,
)
```
`dsx/checks/claims.py:1-28` shows the same docstring-first, `from __future__ import annotations`,
then `from ..findings import Report`, then `from ..spec import (...)` import ordering — this is
the codebase-wide convention every check module follows and `dsx/frame/paradigm.py` should match,
**except** the `from ..spec import (...)` becomes `from ..spec import (...)` still (paradigm.py
may import from `dsx.spec` — the D-03a boundary only forbids importing from `dsx.checks`, per
Integration Points in CONTEXT.md).

**Signature convention — no `gate_point` needed:** `dsx/checks/decision.py:15`
(`def check(spec: dict, *, gate_point: "str | None" = None) -> Report:`) is the pattern for a
check that DOES need gate-point differentiation. `paradigm.check(spec)` needs none (D-10/R-01 —
`DSX-PAR-001` behaves identically at every gate point), so it should be the simpler no-kwarg form
matching e.g. `smells.check(spec)` (called plainly at `dsx/cli.py:147`,
`reports.append(smells.check(spec))`), not the `decision.check`/`design.check(spec, strict=...)`
forms. This lets it fall through the generic `elif name in CHECKS: reports.append(CHECKS[name]
(spec))` branch in `run_checks()` (`dsx/cli.py:156-157`) with a plain `CHECKS["paradigm"] =
paradigm.check` entry — no new explicit-dispatch branch needed in `run_checks()`.

**Registration points (verified live, exact lines):**
```python
# dsx/cli.py:52-67
CHECKS: dict[str, Callable] = {
    "spec": validate_structure,
    "design": design.check,
    ...
    "decision": decision.check,
    # + "paradigm": paradigm.check,
}

# dsx/cli.py:72-83
GATE_PROFILES: dict[str, tuple[str, ...]] = {
    "plan": ("spec", "design", "metrics", "coherence"),           # + "paradigm"
    "execute": ("spec", "ml", "repro", "dq", "code"),              # + "paradigm"
    "verify": ("spec", "design", "stats", ..., "decision"),        # + "paradigm"
    "ship": ("spec", "design", "stats", ..., "decision"),          # + "paradigm"
}
```

---

### `dsx/cli.py::cmd_explain` + `explain` subcommand (controller/CLI, request-response)

**Analog for "always exit 0, pure read+print":** `cmd_vocab` (`dsx/cli.py:332-334`, quoted in
full, verified live):
```python
def cmd_vocab(args: argparse.Namespace) -> int:
    print(json.dumps(describe_vocabulary(), indent=2))
    return 0
```

**Analog for spec/path discovery + JSON/text dual output:** `cmd_validate`/`cmd_check`
(`dsx/cli.py:170-194`) for the `find_spec(args.spec, args.phase_dir)` → work → `emit(...)`
pattern, though `cmd_explain` deliberately skips `emit()`/`Severity`/`Report` entirely (D-18 — it
never touches the block contract):
```python
def cmd_validate(args: argparse.Namespace) -> int:
    path = find_spec(args.spec, args.phase_dir)
    spec = load(path)
    report = run_checks(spec, ("spec",), args.phase_dir,
                         resolve_root=args.phase_dir or str(path.parent))
    report.context["spec_path"] = str(path)
    return emit(report, Severity.parse(args.block_on), args.json, args.verbose)
```

**New handler sketch (composite of the two analogs above):**
```python
def cmd_explain(args: argparse.Namespace) -> int:
    from .decisions import read_all

    path = find_spec(args.spec, args.phase_dir)
    decisions_path = path.parent / "DECISIONS.jsonl"
    records = read_all(decisions_path)
    if args.invocation:
        records = [r for r in records if r.get("invocation_id") == args.invocation]
    elif records:
        latest = max((r.get("invocation_id", "") for r in records
                      if r.get("layer") == "header"), default="")
        records = [r for r in records if r.get("invocation_id") == latest]
    if args.json:
        print(json.dumps(records, indent=2))
    else:
        print(_render_decision_trail(records))
    return 0   # ALWAYS 0 — D-18
```

**`add_common()` refactor — exact current state** (`dsx/cli.py:427-433`, verified live):
```python
def add_common(p: argparse.ArgumentParser, default_block: str = "HIGH") -> None:
    p.add_argument("--spec", help="path to ANALYSIS-SPEC (auto-discovered when omitted)")
    p.add_argument("--phase-dir", help="GSD phase directory to search and resolve paths against")
    p.add_argument("--block-on", default=default_block,
                   help="minimum severity that fails the command (default: %(default)s)")
    p.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    p.add_argument("--verbose", action="store_true", help="list checks that passed")
```
This is a nested closure inside `build_parser()`, called by every existing subcommand
(`p_validate`, `p_check`, `p_audit`, `p_gate`) — note it currently also adds `--verbose`, not just
the three D-18 names. D-18's instruction is to make `--block-on` **opt-in**; the minimal
compliant refactor adds one boolean parameter and wraps the existing `--block-on` line:
```python
def add_common(p: argparse.ArgumentParser, default_block: str = "HIGH",
                include_block_on: bool = True) -> None:
    p.add_argument("--spec", help="path to ANALYSIS-SPEC (auto-discovered when omitted)")
    p.add_argument("--phase-dir", help="GSD phase directory to search and resolve paths against")
    if include_block_on:
        p.add_argument("--block-on", default=default_block,
                       help="minimum severity that fails the command (default: %(default)s)")
    p.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    p.add_argument("--verbose", action="store_true", help="list checks that passed")
```
Every existing call site (`add_common(p_validate, "CRITICAL")`, `add_common(p_check)`,
`add_common(p_audit)`, `add_common(p_gate, "")`) keeps working unchanged since
`include_block_on` defaults to `True`. New registration:
```python
p_explain = sub.add_parser("explain", help="render the decision trail (never blocks)")
add_common(p_explain, include_block_on=False)
p_explain.add_argument("--invocation", help="render one invocation id (default: most recent)")
p_explain.set_defaults(func=cmd_explain)
```
Add this `sub.add_parser(...)` block in `build_parser()` (`dsx/cli.py:419-507`) following the
exact placement/ordering convention of the existing subcommands (each is: `add_parser` → any
positional/extra args → `set_defaults(func=...)`, in the order the subcommands were introduced —
place `p_explain` near `p_vocab`/`p_gate` since it is a read-only reporting command, matching that
functional grouping rather than alphabetical order).

---

### `scripts/gen-finding-catalogue.py` — D-05 enforcement (build/CI script, batch)

**Analog:** the file's own existing `extract()` (`scripts/gen-finding-catalogue.py:59-75`, quoted
per RESEARCH.md — re-verify exact line numbers against the current file before implementing, this
pattern-mapper did not re-read the full script directly but RESEARCH.md's quotation is from a
direct read in that pass):
```python
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
```

**Analog for the directory-AST-walk idiom to reuse for docstring resolution and the `tests/`
walk:** `dsx/suppressions.py::known_codes()` (`:24-54`, quoted in full above under "File
Classification" section context) — walks `_DSX_ROOT.rglob("*.py")`, `ast.parse` per file inside a
`try/except SyntaxError: continue`, `ast.walk(tree)` looking for `ast.Call` nodes whose `func` is
an `ast.Attribute` with `.attr == "add"`, extracting the first string-constant arg. This exact
`rglob("*.py")` + per-file `try/except SyntaxError: continue` + `ast.walk` idiom is what the new
D-05 enforcement's docstring-resolution pass and the `tests/` marker-collection pass should both
reuse (the latter needs a **text-level regex pass**, not `ast.walk`, since `ast` discards
comments — confirmed correct in RESEARCH.md, `# D-05: <CODE>` markers must be found via
`re.finditer` over raw source text, not the AST).

**Convention to replicate:** keep the D-20 allow-list (`_D05_ALLOWLIST_PREFIXES`) as a plain
module-level tuple inside the script itself (not in `dsx/`), mirroring how `_CODE_RE` and other
regex/constant helpers already live at module scope in `dsx/suppressions.py` (`:19-21`) rather
than inside functions.

---

### `tests/test_frame_boundary.py` (new) — AST meta-test

**Analog:** `dsx/suppressions.py::known_codes()`'s AST-walk idiom (quoted in full above). The new
test needs `importlib.util.resolve_name()` (stdlib, 3.3+) to resolve relative imports found by
`ast.ImportFrom`, which `known_codes()` does not need (it only checks `Import`/call-attribute
patterns, no relative-import resolution). Full sketch is in RESEARCH.md Pattern 6 — implement
close to verbatim, including the required "prove it can fail" second test method
(`test_boundary_scanner_detects_a_real_violation`) that calls a standalone
`_scan_source_for_checks_imports(text, package)` function on a literal string, not just real files
under `dsx/frame/` — this refactor-for-testability step is explicitly required by ROADMAP SC 4 and
is easy to skip if the scan logic is written only as an inline test-method body.

---

### `tests/test_dsx.py::TestCLI` harness and the two D-08 fixture tests (test, request-response)

**Analog/contract to preserve exactly** (`tests/test_dsx.py:804-839`, quoted in full, verified
live):
```python
class TestCLI(unittest.TestCase):
    ROOT = Path(__file__).resolve().parent.parent

    def _run(self, argv: list[str]) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_good_fixture_passes_every_gate(self):
        fixture = self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml"
        for point in ("plan", "execute", "verify", "ship"):
            code, _, err = self._run(["gate", point, "--spec", str(fixture)])
            self.assertEqual(code, 0, f"gate {point} unexpectedly blocked:\n{err}")

    def test_bad_fixture_blocks_at_plan(self):
        fixture = self.ROOT / "examples" / "bad-ANALYSIS-SPEC.yaml"
        code, _, err = self._run(["gate", "plan", "--spec", str(fixture)])
        self.assertEqual(code, 1)
        self.assertIn("DSX-", err)

    def test_bad_fixture_blocks_at_ship(self):
        fixture = self.ROOT / "examples" / "bad-ANALYSIS-SPEC.yaml"
        code, _, _ = self._run(["gate", "ship", "--spec", str(fixture)])
        self.assertEqual(code, 1)
```
**REQ-P6-12/D-08 hard constraint: these three methods (and the `_run` helper) must remain
byte-for-byte unedited.** Any new CLI test (`dsx explain` exit-0 test, `dsx gate` with
`validity_frame` present/absent, etc.) must be a **new method** in `TestCLI`, reusing `self._run`
exactly as shown, never modifying these three. This is the concrete evidence the planner needs to
confirm extending `good-`/`bad-ANALYSIS-SPEC.yaml` cannot flip either fixture's gate outcome at
`plan`/`ship` — the extended `good-` fixture must still exit 0 at all four gates, and the extended
`bad-` fixture (not touched on the peeking axis per D-07) must still exit 1 at plan and ship.

**New `dsx explain` exit-0 test — follow the same `_run` harness:**
```python
def test_explain_always_exits_zero(self):
    fixture = self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml"
    code, out, _ = self._run(["explain", "--spec", str(fixture)])
    self.assertEqual(code, 0)
```

---

## Shared Patterns

### Closed vocabulary + membership check + `dsx vocab` dump
**Source:** `dsx/spec.py:31-95` (vocabulary constants), `:422-479` (`_validate_design_shape`
membership-check idiom), `:544-563`/new `_VOCABULARIES` registry (dump).
**Apply to:** every new frame vocabulary (`IDENTIFICATION_STRENGTHS`, `CONSTRAINT_SOURCES`,
`DEPENDENCE_STRUCTURES`, `INTERFERENCE_RISKS`, `INTERFERENCE_MITIGATIONS`,
`MISSINGNESS_MECHANISMS`, `PARADIGMS`, `PARADIGM_JUSTIFICATIONS`) and the new shape validators
that check membership against them.

### `report.add(code, severity, title, detail=..., remedy=..., where=...)` finding shape
**Source:** every check module (`dsx/checks/design.py`, `dsx/checks/claims.py`), `dsx/spec.py`'s
validators.
**Apply to:** all new findings emitted by `_validate_validity_frame_shape`,
`_validate_inference_shape`, and `dsx/frame/paradigm.py`. `detail` explains *why*, `remedy` states
the concrete next action, `where` is a dotted spec path — this triad is universal in this
codebase and none of the three should ever be omitted for a new code (D-11's actionability
argument depends on it).

### AST directory-walk idiom (`ast.parse` + `ast.walk` + per-file `try/except`)
**Source:** `dsx/suppressions.py::known_codes()` (`:24-54`).
**Apply to:** `tests/test_frame_boundary.py` (import-boundary scan), the D-05 docstring-resolution
half of `scripts/gen-finding-catalogue.py`'s extension. The test-linkage half (`# D-05: <CODE>`
markers) needs a **text-regex** pass instead, since AST discards comments — do not try to force
this half through `ast.walk` too.

### `find_spec()` / `resolve_root` path discovery
**Source:** `dsx/cli.py:95-114` (`find_spec`), `:117-134` (`run_checks`'s `resolve_root`
parameter), `:244` (`cmd_gate`'s `resolve_root=args.phase_dir or str(path.parent)`).
**Apply to:** `dsx/decisions.py`'s `DECISIONS.jsonl` path resolution and `cmd_explain`'s spec/path
discovery — reuse the value `cmd_gate` (and the new gate-invocation write call) already computes,
do not re-implement a search loop.

### `emit()` / `Severity` / block contract is bypassed by design for two commands
**Source:** `cmd_vocab` (`dsx/cli.py:332-334`) — the existing precedent for "always return 0,
never call `emit()`".
**Apply to:** `cmd_explain` — D-18 requires it never participate in the block contract; model it
on `cmd_vocab`'s bare `return 0`, not on `cmd_validate`/`cmd_gate`'s `emit(...)` return.

## No Analog Found

| File | Role | Data Flow | Reason |
|---|---|---|---|
| `dsx/decisions.py` | storage/service | append-only file I/O | First write path in this codebase — `dsx/loader.py` is read-only. Fully specified in RESEARCH.md Pattern 5 instead; implement from that spec, not from a codebase analog. |
| `.planning/REVERSALS.md` | docs | — | First file of its kind; template is dictated by D-14/M-05's own decision text (`SELF-001` convention), not by an existing doc's structure. Check `.planning/` for any existing `*.md` doc with a comparable "template + accumulating entries" shape (e.g. a changelog-style file) before writing from scratch, but none was found in this pass. |
| `_validate_validity_frame_shape`'s requiredness/aggregation logic (the D-10/D-11 half specifically, as distinct from its shape-checking half) | validator logic | request-response | No existing check in this codebase aggregates multiple missing sub-blocks into one finding with an itemised `detail`, nor conditions a whole *section's sub-block set* on `question_type` in one pass. Budget this as new design work per RESEARCH.md Pitfall 3 — do not estimate it at `_validate_design_shape`-sized effort. |

## Metadata

**Analog search scope:** `dsx/`, `dsx/checks/`, `dsx/frame/` (does not yet exist), `scripts/`,
`tests/`, `templates/`, `examples/` — all read directly in this pass or in the immediately
preceding RESEARCH.md pass (cross-checked, not blindly trusted).
**Files scanned directly in this pattern-mapping pass:** `dsx/loader.py` (partial, `_NULL`
region), `dsx/spec.py` (lines 1-95, 200-270, 422-568 read directly), `dsx/checks/design.py`
(lines 1-30, 440-548 read directly), `dsx/checks/claims.py` (lines 1-40, 474-516 read directly),
`dsx/suppressions.py` (full file), `dsx/checks/decision.py` (lines 1-30), `dsx/cli.py` (lines
1-40 imports implied, 40-340, 419-527 read directly), `tests/test_dsx.py` (lines 804-843 read
directly).
**Pattern extraction date:** 2026-08-07
