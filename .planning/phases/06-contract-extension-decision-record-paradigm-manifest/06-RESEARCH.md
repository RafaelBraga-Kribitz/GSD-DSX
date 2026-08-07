# Phase 6: Contract extension, decision record, paradigm manifest - Research

**Researched:** 2026-08-07
**Domain:** Extending an existing, installed, stdlib-only Python CLI gate tool (`dsx`) — new
contract fields, a new append-only artifact, a new module boundary, mechanical citation
enforcement. Codebase-grounded, not an ecosystem survey.
**Confidence:** HIGH — every structural claim below was verified by reading the current source
at this commit (v1.5.0, pre-Phase-6) or by executing code against it, not inferred from the brief.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Binding upstream (not re-litigable):** `brief.md` §4 (D-01…D-14) and §5 (contract shape);
`PROJECT.md` M-01…M-09. In particular: `DSX-PAR-010` is a distinct code, `DSX-EXP-060` untouched
(M-01); no `inference.stopping_rule` field (M-02); `validity_frame` sub-block requiredness gated
by `question_type` (M-06); `suppressions[]` is the pre-v2.0.0 grandfather path (M-07);
`dependence.method_family_required` reuses `VARIANCE_ADJUSTMENTS` (M-09). `SELF-001` stays a
convention for v2.0.0; `REVERSALS.md` template is seeded here (M-05). `DSX-PAR-011` asserts the
prior-averaged Ville bound `1/(K+1)`, not the point-null/LIL formulation.

**Phase-6-specific decisions (D-01…D-23, from discuss):**

- **D-01/D-02:** `PEEKING_POLICIES` gains `uncontrolled_continuous` in Phase 6 (not deferred to
  Phase 9) — the Bayesian known-bad fixture needs it or it trips `DSX-SPEC-042` at HIGH.
- **D-03:** `dsx vocab` emits `peeking_policies` as a name→description object (not a flat
  sorted-list); `always_valid`'s description is tightened.
- **D-04:** Every new frame vocabulary is a name→description dict, no exceptions.
- **D-05:** `describe_vocabulary()` is built from an explicit vocabulary-name registry, with a
  test asserting coverage.
- **D-06:** Both halves of the Phase 9 atomic pair (frequentist `uncontrolled_continuous` +
  Bayesian continuous-monitoring) get a known-bad fixture in Phase 6.
- **D-07:** `examples/bad-ANALYSIS-SPEC.yaml` is NOT extended on the peeking axis.
- **D-08:** A parametrised disjointness test proves M-01 mechanically — one test over all five
  `PEEKING_POLICIES` members asserting `DSX-EXP-060` fires only for `""`/`fixed_horizon`. No
  `DSX-EXP-060` code change needed (`dsx/checks/design.py:451` already gates on
  `policy in ("", "fixed_horizon")`).
- **D-09:** `_validate_validity_frame_shape()`/`_validate_inference_shape()` live in `dsx/spec.py`
  under `DSX-SPEC-08x`, mirroring `_validate_design_shape` exactly. No `GATE_PROFILES` change
  ships (`spec` is already in all four profiles).
- **D-10:** A missing required `validity_frame` sub-block is **CRITICAL uniformly** — blocks from
  `plan` onward. **Action for the planner:** `PROJECT.md:79-80`'s version rationale ("required at
  verify/ship") must be amended to "required from plan" — not a D-14 reversal, but must not be
  left contradicting the gate.
- **D-11:** Finding granularity is aggregate-when-absent: block entirely absent → one finding
  itemising every missing sub-block in `detail`; block present but a sub-block missing → one
  finding per sub-block.
- **D-12:** `templates/ANALYSIS-SPEC.yaml` scaffolds both blocks in full (every sub-block present,
  guidance comments, placeholder values) so `dsx init` output keeps passing `dsx validate`/
  `dsx gate plan` structurally.
- **D-13:** Only the new surface emits decision records in Phase 6 — `DSX-PAR-001` plus the new
  `DSX-SPEC-08x` adjudications. The 15 existing check modules are untouched.
- **D-14:** One `DECISIONS.jsonl` beside the spec, resolved like `find_spec()` (`phase_dir` → cwd
  → `.planning/`), appended across every invocation.
- **D-15:** The per-invocation identifier must NOT be called `run_id` (already taken by
  `visuals[].run_id`, enforced by `DSX-SMELL-013`).
- **D-16:** An invocation-header record is emitted once per gate invocation, carrying invocation
  id, gate point, dsx version, and a `hashlib` digest of the `validity_frame:` + `inference:`
  blocks — doubles as `dsx explain`'s grouping anchor and Phase 10's plan-time content lock.
- **D-17:** Crash-safety is fsync-per-record plus a tolerant reader — append one JSON line,
  `flush()` then `os.fsync()`; the reader skips an unparseable tail line.
- **D-18:** `dsx explain` is a trail renderer with no `--block-on`. Signature:
  `dsx explain [--spec PATH] [--phase-dir DIR] [--invocation ID] [--json]`, defaulting to the
  most recent invocation, human-readable text by default. Borrows `--spec`/`--phase-dir`/`--json`
  from a refactored `add_common()` that makes the blocking flags (`--block-on`) opt-in.
- **D-19:** The gate emits `layer: deterministic` records only; the append contract (file
  location, line format, required fields) is documented so a `dsx` agent can begin writing
  `layer: stochastic` entries with no further code change.
- **D-20:** The D-05 citation-marker requirement binds new v2.0.0 checks only (`dsx/frame/*` and
  the new `DSX-SPEC-08x` checks), via an explicit allow-list carried inside the enforcement
  script. The 206 pre-existing finding codes across 17 families are exempted. README must state
  the two tiers of evidentiary rigour plainly.
- **D-21:** The marker is a structured docstring line: `Citation:` naming author, year, work and
  the exact formulation. The script greps the prefix and asserts non-empty content.
- **D-22:** Enforcement is per finding code, resolved by walking up from the `report.add(...)`
  call site to the enclosing function's docstring, falling back to the module docstring.
- **D-23:** BOTH halves of D-05 are automated: docstrings carry `Citation:` **and**
  `Reference value:` (or `Structural criterion:` for structural checks), and the script
  additionally asserts a linked test exists via a `# D-05: <CODE>` marker comment in `tests/`,
  AST-walked.

### Claude's Discretion

- Which real analyses the known-bad corpus encodes (D-06 pins frequentist +
  Bayesian-uncontrolled-continuous; ≥1 interference case and any beyond the floor are open).
- Exact `DSX-SPEC-08x` number assignments (`080` onward free; irreversible once assigned).
- The precise name of the per-invocation identifier (constrained only by D-15: not `run_id`).
- Plan slicing across the 16 requirements, subject to the ROADMAP ordering constraints
  (REQ-P6-01 before REQ-P6-02; REQ-P6-09 in this phase; REQ-P6-10/11 before Phase 7 opens
  `frame/val.py`).

### Deferred Ideas (OUT OF SCOPE)

- `dsx frame init` scaffolder subcommand for migrating pre-v2.0.0 specs. `suppressions[]` already
  provides the migration story with zero new code.
- `dsx explain --code DSX-XXX-NNN` rule/citation lookup mode independent of a run.
- Wiring `dsx` agents/skills to append `layer: stochastic` records.
- Retroactive D-05 sourcing for the 206 legacy finding codes.
- `references/families.yaml` and `dsx/frame/admissibility.py` — not created in this phase (brief
  §6.6 item 2). `DSX-VAL-*`, `DSX-INT-*`, `DSX-PRE-*`, `DSX-ADM-*` check-family logic — Phases 7–11.

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| REQ-P6-01 | Drop `"none"` from `dsx/loader.py`'s `_NULL` set; add a bundled-parser/PyYAML agreement test | §"The `_NULL` bug" below — exact line, exact repro (re-verified live), exact fix, exact blast radius |
| REQ-P6-02 | `ANALYSIS-SPEC.yaml` accepts `validity_frame:` with all ten sub-blocks; extended spec round-trips | §"Spec schema surface" — where `_validate_design_shape` pattern lives, what to mirror |
| REQ-P6-03 | Sub-block requiredness gated by `question_type` | §"Conditional-requirement semantics" — `_check_limitations_required`/`DSX-CLM-080` and `_check_identification`/`DSX-CAU-001` are the two existing precedents; neither is reused verbatim, both inform the new validator's shape |
| REQ-P6-04 | `inference:` block with six named fields, no `stopping_rule` | §"Spec schema surface"; §"Open question: `declared_at` vocabulary" |
| REQ-P6-05 | `PEEKING_POLICIES` gains `uncontrolled_continuous` | §"`PEEKING_POLICIES` and the `dsx vocab` dict-dump bug" — exact line, exact fix |
| REQ-P6-06 | Every new vocabulary registered + dumped; `dependence.method_family_required` reuses `VARIANCE_ADJUSTMENTS` | §"`describe_vocabulary()` registry pattern" — concrete code |
| REQ-P6-07 | Decision-record schema + emitter, append-only, crash-safe | §"Append-only `DECISIONS.jsonl`: the concrete crash-safe idiom" |
| REQ-P6-08 | `dsx explain` renders the trail, always exits 0 | §"`dsx explain`: wiring into `dsx/cli.py`" |
| REQ-P6-09 | `DSX-PAR-001` INFO manifest, never blocks | §"`Severity.INFO` end to end" — traced through `emit()`/`Report.blocks()` |
| REQ-P6-10 | `dsx/frame/` package + AST boundary test | §"The AST import-boundary test (D-03a / REQ-P6-10)" — concrete pytest+ast pattern, concrete violating fixture |
| REQ-P6-11 | `gen-finding-catalogue.py` fails build on missing citation marker | §"D-05 enforcement: extending `gen-finding-catalogue.py`" — current AST-walk machinery, exact extension points |
| REQ-P6-12 | Good/bad fixtures extended, two D-08 tests unchanged | §"The two D-08 tests and what extending the fixtures must not break" |
| REQ-P6-13 | ≥3 known-bad fixtures (≥1 interference, ≥1 Bayesian continuous-monitoring), post-mortems, structurally valid | §"Known-bad fixture mechanics" |
| REQ-P6-14 | `.planning/REVERSALS.md` created with D-14 template + `SELF-001` | §"`.planning/REVERSALS.md`: does not exist yet" |
| REQ-P6-15 | README documents `suppressions[]` migration path + "a frame that lies passes" limit | §"README: what exists today, what's missing" |
| REQ-P6-16 | Version 2.0.0, catalogue regenerated | §"Version bump and catalogue regen — mechanics" |

</phase_requirements>

## Summary

Phase 6 is pure codebase-grounded extension work on an already-mature, well-tested (160
tests, 1 skip) stdlib-only Python CLI. There is no external ecosystem to survey and no dataset to
profile — every one of the sixteen requirements is answerable by reading `dsx/*.py`,
`dsx/checks/*.py`, `scripts/gen-finding-catalogue.py`, `tests/test_dsx.py`, and the two example
fixtures, all of which this research read directly (not summarised) and, where checkable,
executed against.

Three findings matter more than the rest for planning correctness. **First**, the `_NULL`
bug in `dsx/loader.py` is real and was re-verified live in this research pass:
`_parse_yaml_subset("x: [none, clustered]\n", "<t>")["x"]` returns `[None, 'clustered']` today,
not `['none', 'clustered']`. The fix is a one-line set literal change
(`_NULL = {"", "null", "~", "none"}` → `_NULL = {"", "null", "~"}`), and it is safe against the
existing suite (all 160 tests still pass with this change applied locally in this research
session — see verification below). **Second**, `PEEKING_POLICIES` is *already* a
name→description dict (not a set) — the CONTEXT.md's D-03/D-04 "convert to dict" framing is
subtly imprecise: the vocabulary itself needs no shape change, only `describe_vocabulary()`'s
`sorted(PEEKING_POLICIES)` call (`dsx/spec.py:552`) needs to stop discarding the values. The new
frame vocabularies genuinely are new dicts; `PEEKING_POLICIES` is an existing dict whose *dump*
is broken. **Third**, there is no existing precedent in this codebase for "required only when the
question is causal" applied to a whole *sub-block of a section* (as opposed to a whole
*top-level field*, which `DSX-CLM-080`/`limitations` already does, or a required *individual
field of an existing section*, which `_check_identification`/`DSX-CAU-001` already does) — the
new `_validate_validity_frame_shape()` is a genuinely new shape of check, and its aggregate-vs-
per-sub-block finding granularity (D-11) has no direct precedent either. This is flagged plainly
below so the planner treats it as new code, not a copy-paste.

**Primary recommendation:** Follow `dsx/spec.py:422`'s `_validate_design_shape()` almost
line-for-line for `_validate_validity_frame_shape()`/`_validate_inference_shape()`; follow
`dsx/decisions.py`'s design from `.planning/research/STACK.md` (already fully specified, verified
against this codebase, and consistent with all Phase-6 CONTEXT.md decisions) rather than
re-deriving it; and treat the AST boundary test, the D-05 enforcement script extension, and the
`_NULL` fix as the three pieces of code in this phase carrying the highest correctness risk if
rushed, because each has a concrete, testable "prove it against a deliberately violating case"
requirement in ROADMAP Success Criterion 4.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| `_NULL` fix (loader semantics) | Parser (`dsx/loader.py`) | — | Single-file, single-set-literal change; affects every consumer of `load()`/`loads()` transitively |
| `validity_frame:`/`inference:` schema definitions | Contract (`dsx/spec.py`) | — | Vocabularies and shape validators live where every existing vocabulary lives |
| Sub-block requiredness gating by `question_type` | Contract (`dsx/spec.py`, `DSX-SPEC-08x`) | — | Structural/shape concern per D-09, not semantic — lives beside `_validate_design_shape`, not in `dsx/checks/` or `dsx/frame/` |
| `dsx vocab` dict-dump + registry | Contract (`dsx/spec.py`) | CLI (`dsx/cli.py::cmd_vocab`) | `describe_vocabulary()` is the single source; `cmd_vocab` is a thin `print(json.dumps(...))` wrapper, unchanged |
| `DSX-PAR-001` paradigm manifest | Gate logic (`dsx/frame/paradigm.py`, new) | CLI (`GATE_PROFILES`/`CHECKS` registration in `dsx/cli.py`) | First real code in the new `dsx/frame/` package; D-03a boundary applies from its first line |
| Decision-record schema + emitter | Storage/artifact (`dsx/decisions.py`, new top-level peer module) | Gate logic (`dsx/frame/*`, `dsx/spec.py`'s new `DSX-SPEC-08x` validators — both call into it) | Peer to `findings.py`, not inside either `checks/` or `frame/`, so both can import it without creating a `checks↔frame` edge |
| `DECISIONS.jsonl` append/read | Storage/artifact (filesystem, resolved like `find_spec()`) | CLI (`dsx gate` writes; `dsx explain` reads) | Crash-safety (fsync-per-record, tolerant reader) is a storage-layer concern, isolated in `dsx/decisions.py` |
| `dsx explain` rendering | CLI (`dsx/cli.py::cmd_explain`, new) | Storage/artifact (reads `DECISIONS.jsonl` via `dsx/decisions.py`) | Pure read+render; never touches `Report`/`Severity`/`GATE_THRESHOLDS` at all |
| D-03a AST boundary enforcement | Build/CI (`tests/test_frame_boundary.py`, new) | — | Static analysis over source text; runs inside `python -m unittest discover`, not the gate path |
| D-05 citation/test-linkage enforcement | Build/CI (`scripts/gen-finding-catalogue.py`, extended) | — | Explicitly a build script, not the gate path (D-01 does not constrain what it reads) |
| Known-bad fixtures + post-mortems | Fixtures (`examples/known-bad/`, new directory) | — | Additive, narrowly scoped per-case files; separate from the two canonical fixtures |
| `.planning/REVERSALS.md` | Docs (`.planning/`) | — | Planning-process artifact, not gate-path code, per M-05 |
| README updates | Docs (`README.md`) | — | User-facing documentation of the `suppressions[]` migration path and the known limit |

## Standard Stack

### Core

No new third-party packages. Every piece of Phase 6 is Python 3.9+ stdlib, consistent with D-01
(stdlib-only gate path) and this codebase's existing convention (`dsx/mathx.py`'s own docstring:
"these functions run inside blocking gates... a gate that errors because the user's environment
lacks scipy is a gate that gets disabled").

| Module | Verified stdlib min. version | Purpose | Why standard |
|--------|------------------------------|---------|---------------|
| `ast` | all | Static-analysis boundary test (`tests/test_frame_boundary.py`) and D-05 enforcement extension | Never executes the scanned module; matches `dsx/suppressions.py::known_codes()`'s existing AST-walk pattern exactly |
| `importlib.util` | 3.3 | `resolve_name()` — turns a relative import found by `ast` into an absolute dotted name | Needed to correctly resolve `from ..checks import x` written inside `dsx/frame/*.py` |
| `dataclasses` | 3.7 | `DecisionRecord` frozen dataclass | Mirrors `dsx/findings.py::Finding` exactly (also a frozen dataclass with `to_dict()`) |
| `json` | all | `DECISIONS.jsonl` line format | `dsx/loader.py::loads()` already privileges JSON as the fast path; no writer exists yet anywhere in this codebase, so this introduces the first write path — deliberately the simplest format available |
| `os` (`fsync`, `replace`) | all | Crash-safety idiom for `DECISIONS.jsonl` append (D-17) | Standard POSIX/Windows-portable durability primitive; `os.fsync()` works identically on both platforms (Windows via `_commit`-backed `fsync` since Python's `os.fsync` wraps the platform call) |
| `pathlib` | 3.4 | Path discovery mirroring `find_spec()` | Already the path-handling idiom throughout `dsx/cli.py` |
| `argparse` | all | `dsx explain` subcommand registration | Extends the existing `build_parser()`/`add_common()` pattern in `dsx/cli.py` |
| `unittest` | all | Every new test (boundary test, loader regression test, D-05 script test, vocabulary coverage test) | The only test runner this codebase uses (`python -m unittest discover -s tests -v`); no pytest dependency anywhere |

### Supporting

None — Phase 6 has no need for `random`, `math.lgamma`, or `statistics` (those belong to Phase 9's
`DSX-PAR-011` simulation, out of scope here per the CONTEXT.md boundary).

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `ast`-based boundary test | `importlib` + `inspect` runtime introspection | Executes the module under test (side effects, loses provenance once names are re-exported); rejected in `.planning/research/STACK.md` with a concrete counter-example |
| `json.dumps` per-line for `DECISIONS.jsonl` | A hand-rolled YAML sequence writer | `dsx/loader.py` has no YAML *writer* today; building one duplicates the loader's own escaping complexity in the harder (generation) direction for zero downstream benefit |
| `os.fsync()` per record | `buffering=1` (line-buffered) with no fsync | Line buffering only reaches the OS buffer, not disk — survives a process crash, not a machine crash; D-17 explicitly requires the stronger guarantee |

**Installation:**
```bash
# Nothing to install. Verify no new imports were introduced:
python3 -c "import dsx, dsx.frame, dsx.decisions" 2>&1   # must succeed with PyYAML absent
```

**Version verification:** N/A — no packages to check against a registry.

## Package Legitimacy Audit

**Not applicable to this phase.** Phase 6 installs zero third-party packages (D-01: gate path is
stdlib-only; verified — every new module identified below imports only from `dsx.*` and the
Python standard library). The Package Legitimacy Gate is skipped; there is nothing to check
against `npm view` / `pip index versions` / a registry.

## Architecture Patterns

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Operator writes / edits ANALYSIS-SPEC.yaml (validity_frame:, inference:) │
└───────────────────────────────────┬───────────────────────────────────────┘
                                     │
                                     ▼
                    dsx gate {plan|execute|verify|ship}   (dsx/cli.py::cmd_gate)
                                     │
                    ┌────────────────┼─────────────────────┐
                    ▼                                       ▼
        dsx/loader.py::load()                    GATE_PROFILES[point] → check names
     (fixed: "none" ≠ null,               (unchanged this phase — "spec" already
      PyYAML or bundled parser agree)      in all 4 profiles per D-09)
                    │                                       │
                    ▼                                       ▼
              spec: dict  ────────────────────►  run_checks(spec, names, ...)
                    │                                       │
                    │                          ┌────────────┼─────────────────┐
                    │                          ▼                              ▼
                    │              CHECKS["spec"] =              CHECKS["paradigm"] =
                    │           dsx.spec.validate_structure   dsx.frame.paradigm.check   (NEW)
                    │              (extended: DSX-SPEC-08x           │
                    │               shape validators for                │ reads inference.paradigm
                    │               validity_frame/inference,           │ (the ONLY frame module
                    │               gated by question_type)             │ permitted to, per D-11)
                    │                          │                        │
                    │                          ▼                        ▼
                    │                   Report (Finding[])       Report (INFO finding:
                    │                   DSX-SPEC-08x findings     DSX-PAR-001, never blocks)
                    │                          │                        │
                    │                          └───────────┬────────────┘
                    │                                       ▼
                    │                          merge() → apply_suppressions()
                    │                                       │
                    │                                       ▼
                    │                          merged Report  ──────────────┐
                    │                                       │               │
                    │                                       ▼               │
                    │                          emit(report, threshold)      │
                    │                          exit 0 / 1 / 2                │
                    │                                                       │
                    │           (side channel, not via Report/Finding)      │
                    │                                                       ▼
                    │                                     dsx/decisions.py::append()
                    │                                     one JSON line per decision,
                    │                                     fsync()'d, into DECISIONS.jsonl
                    │                                     beside the resolved spec
                    │                                                       │
                    │                                                       ▼
                    │                                          dsx explain (cmd_explain)
                    │                                          reads DECISIONS.jsonl,
                    │                                          renders trail, ALWAYS exits 0
                    ▼
     dsx/frame/ ←──────── ast-boundary-tested ────────► dsx/checks/
     (tests/test_frame_boundary.py: zero imports either direction between
      dsx.frame.* and dsx.checks.*; both may import dsx.findings/spec/loader/decisions)

  Build-time (not gate path):
     scripts/gen-finding-catalogue.py --check
        → AST-walks dsx/ for report.add(...) calls (existing machinery)
        → NEW: for codes in the DSX-SPEC-08x / DSX-PAR-* / dsx.frame.* allow-list,
          walks up to the enclosing docstring, asserts `Citation:` + `Reference value:`
          (or `Structural criterion:`) lines present, and a `# D-05: <CODE>` marker
          exists somewhere under tests/
        → exits 1 (fails CI) if either half is missing for a covered code
```

### Recommended Project Structure

```
dsx/
├── loader.py                # MODIFIED: _NULL loses "none" (one-line fix)
├── spec.py                  # MODIFIED: 9 new vocabularies, PEEKING_POLICIES +1 member,
│                             #   _validate_validity_frame_shape(), _validate_inference_shape(),
│                             #   describe_vocabulary() rebuilt from an explicit registry
├── decisions.py              # NEW top-level peer module: DecisionRecord dataclass,
│                             #   append()/read_all(), fsync-per-record durability
├── frame/                    # NEW package — D-03a boundary starts here
│   ├── __init__.py           #   docstring mapping family→prefix→phase, mirrors checks/__init__.py
│   └── paradigm.py           #   DSX-PAR-001 only this phase (M2c logic lands in Phase 9)
├── cli.py                    # MODIFIED: CHECKS/GATE_PROFILES gain "paradigm" key (registered
│                             #   at all 4 gate points per architecture research §3);
│                             #   new cmd_explain(); add_common() refactored so --block-on
│                             #   is opt-in, not implicit on every subcommand
├── checks/                   # UNCHANGED this phase (no DSX-VAL-*/DSX-INT-* logic yet)
└── suppressions.py           # UNCHANGED — known_codes() already AST-walks all of dsx/,
                              #   so DSX-PAR-* and DSX-SPEC-08x are auto-suppressible, zero
                              #   registration needed

tests/
├── test_dsx.py               # EXTENDED: loader regression test (none-as-string, both scalar
│                             #   and inside a list), vocab-registry-coverage test,
│                             #   PEEKING_POLICIES disjointness test (D-08), DSX-SPEC-08x
│                             #   shape tests, DSX-PAR-001 INFO-never-blocks test,
│                             #   decisions.py append/read/crash-tolerance tests,
│                             #   cmd_explain always-exits-0 test
├── test_frame_boundary.py    # NEW: ast-based zero-import-boundary test, WITH a deliberately
│                             #   violating fixture module proving the test can fail
└── test_gen_finding_catalogue.py  # NEW (or extend an existing catalogue test): asserts
                              #   --check fails on a deliberately-missing-citation fixture check

scripts/
└── gen-finding-catalogue.py  # MODIFIED: extract() gains docstring-walk-up + Citation:/
                              #   Reference value:/Structural criterion: assertion + test-linkage
                              #   check, gated by an explicit allow-list of new-in-v2.0.0 prefixes

examples/
├── good-ANALYSIS-SPEC.yaml   # EXTENDED: full validity_frame:/inference: blocks, clean
├── bad-ANALYSIS-SPEC.yaml    # EXTENDED: new structural defects, NOT peeking-axis (D-07)
└── known-bad/                # NEW directory
    ├── interference-<slug>-ANALYSIS-SPEC.yaml + <slug>-POSTMORTEM.md
    ├── frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml + POSTMORTEM.md   (D-06)
    └── bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml + POSTMORTEM.md        (REQ-P6-13, D-06)

templates/
└── ANALYSIS-SPEC.yaml        # MODIFIED: both new blocks scaffolded in full (D-12)

.planning/
└── REVERSALS.md              # NEW — does not exist yet (verified: no matches for this path)

dsx/__init__.py                # MODIFIED: __version__ = "2.0.0"
README.md                      # MODIFIED: suppressions[] migration path + known-limit text
references/finding-codes.md    # REGENERATED via scripts/gen-finding-catalogue.py --write
```

### Pattern 1: Mirror `_validate_design_shape()` for the two new shape validators

**What:** `dsx/spec.py:422` `_validate_design_shape(spec, report)` is the exact, already-shipped
pattern for "read a top-level section, normalise scalar sub-fields, check membership against a
closed vocabulary, `report.add(...)` with `detail`/`remedy`/`where`, `return` early if the
section is entirely absent (an absent optional section is not itself an error — the required-vs-
absent judgement is a separate concern from shape)."

**When to use:** For `_validate_validity_frame_shape()` and `_validate_inference_shape()`,
called from `validate_structure()` alongside the other five `_validate_*` calls (`dsx/spec.py:244-249`).

**Example (source: `dsx/spec.py:422-436`, read directly from this repo):**
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
    # ... one block per sub-field, each: normalize → membership check → report.add
```

**The one thing the new validators must do differently — requiredness, not just shape.**
`_validate_design_shape` never checks *whether* `design:` should exist (design is always
optional at the structural layer; `DSX-CAU-001` in `dsx/checks/design.py` is what makes it
semantically required for causal questions, and that lives in `dsx/checks/`, not `dsx/spec.py`).
D-09 puts requiredness of `validity_frame`'s sub-blocks in `dsx/spec.py` under `DSX-SPEC-08x`
instead — a genuinely new combination (shape file, but doing a requiredness judgement) with no
one exact precedent in this codebase. The two nearest partial precedents, useful as *shape*
templates for the new requiredness logic itself:

- `DSX-CLM-080` (`dsx/checks/claims.py:496-515`) — the closest working example of
  "`question_type in {causal, prescriptive, predictive}` ⇒ this whole list must be non-empty",
  the exact conditional-requirement shape REQ-P6-03 needs, just for a single flat field
  (`limitations`) rather than a set of sub-blocks. Read directly:
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
      report.add("DSX-CLM-080", "HIGH", ...)
  ```
- `_check_identification` (`dsx/checks/design.py:477-547`) — the closest working example of a
  *single* required field gated by `question_type in ("causal", "prescriptive")`
  (`DSX-CAU-010`), useful for the always-required triad (`estimand`/`units`/`measurement`).

Neither example aggregates multiple missing sub-blocks into one finding with an itemised
`detail` (D-11's requirement) — that aggregation logic is new code the planner should budget
real design time for, not treat as a copy-paste.

### Pattern 2: `PEEKING_POLICIES` and the `dsx vocab` dict-dump bug — corrected framing

**What actually needs to change**, verified by reading `dsx/spec.py:63-68` and `:544-563`
directly:

```python
# dsx/spec.py:63-68 — ALREADY a name→description dict, not a set:
PEEKING_POLICIES = {
    "fixed_horizon": "One analysis at the pre-declared sample size. No interim looks.",
    "sequential_obf": "Interim looks against O'Brien-Fleming boundaries.",
    "sequential_pocock": "Interim looks against constant Pocock boundaries.",
    "always_valid": "Anytime-valid inference (mSPRT / confidence sequences).",
}

# dsx/spec.py:552 — but the DUMP discards the descriptions:
"peeking_policies": sorted(PEEKING_POLICIES),   # sorted(dict) sorts KEYS ONLY
```

Two independent, small changes, both real:
1. **Add the new member** (D-01/D-02): `"uncontrolled_continuous": "Interim looks continue
   indefinitely with no error-rate correction — the discipline failure DSX-PAR-010/011 exist to
   catch."` — a plain new dict entry. No downstream code cares about the shape change because
   there is no shape change; `PEEKING_POLICIES` was always a dict. `_validate_design_shape`'s
   `DSX-SPEC-042` membership check (`policy not in PEEKING_POLICIES`) already tests dict-key
   membership and needs zero changes. `_check_peeking` (`dsx/checks/design.py:451`) uses a
   *literal tuple* `("", "fixed_horizon")`, not `PEEKING_POLICIES`, so it is untouched by
   construction (confirms D-08's "no `DSX-EXP-060` code change needed").
2. **Fix the dump** (D-03): change `"peeking_policies": sorted(PEEKING_POLICIES)` to something
   that preserves the descriptions, e.g. `{k: PEEKING_POLICIES[k] for k in sorted(PEEKING_POLICIES)}`.

**Corollary the planner should know about, out of scope but worth one sentence:**
`IDENTIFICATION_STRATEGIES` (`dsx/spec.py:31-47`) is *also* a nested dict (name → `{"strength":
..., "needs": [...]}`) and its `describe_vocabulary()` dump (`"identification_strategies":
sorted(IDENTIFICATION_STRATEGIES)`, line ~549) has the identical information-loss bug. Nothing
in REQ-P6-* asks for this to be fixed, and CONTEXT.md's decisions are explicitly scoped to
`PEEKING_POLICIES` and the *new* vocabularies — flagging only so the planner does not
accidentally scope-creep into "fix every vocab dump" nor get confused if this is raised in
review.

### Pattern 3: `describe_vocabulary()` registry (D-05, REQ-P6-06)

**What:** Replace the current hard-coded dict literal in `describe_vocabulary()`
(`dsx/spec.py:544-563`) with an explicit, ordered registry that both the function and a coverage
test consume — removing the "two places to update" problem without an introspection deny-list.

**Concrete pattern** (new code, following the shape `dsx/spec.py` already uses for closed
vocabularies):
```python
# dsx/spec.py — replaces the current describe_vocabulary() body
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
    # NEW this phase — every one a name→description dict per D-04:
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
    out["chart_capabilities"] = {   # special-cased, unchanged — a dict of frozensets
        key: sorted(values) for key, values in sorted(CHART_CAPABILITIES.items())
    }
    return out
```

The **coverage test** (`tests/test_dsx.py` or a new file) should assert, at minimum: every entry
in `_VOCABULARIES` appears as a key in `describe_vocabulary()`'s output (trivially true by
construction, but worth asserting so a future refactor cannot silently drop an entry from the
loop), and — the part that actually matters for REQ-P6-06 — that each of the nine *new* Phase-6
vocabulary names is present with the exact member set the spec's shape validators check against
(i.e. the vocabulary object the shape validator imports and the object `describe_vocabulary()`
dumps are the same Python object, not two independently-maintained copies — this is what "two
places to update" means and what the registry pattern eliminates by construction).

### Pattern 4: The `_NULL` bug — exact fix, re-verified live

**What goes wrong**, re-confirmed by direct execution in this research session (not merely
re-stated from `.planning/research/STACK.md`):
```
$ python3 -c "
from dsx.loader import _parse_yaml_subset
print(repr(_parse_yaml_subset('x: none\n', '<t>')['x']))
print(repr(_parse_yaml_subset('x: [none, clustered]\n', '<t>')['x']))
"
None
[None, 'clustered']
```
`dsx/loader.py:32`:
```python
_NULL = {"", "null", "~", "none"}
```
`dsx/loader.py:259-295` (`_scalar()`), the function every scalar and every flow-list element
passes through:
```python
lowered = text.lower()
if lowered in _NULL:
    return None
```

**The minimal fix** (REQ-P6-01):
```python
_NULL = {"", "null", "~"}   # matches PyYAML/YAML 1.1/1.2 null semantics; drop non-standard "none"
```

**What this risks breaking — audited directly, not assumed.** Grep of the whole `dsx/` tree for
every place a value could plausibly be compared against a Python `None` that used to come from a
declared `none` string:
- `dsx/checks/design.py:375`: `is_blank(correction) or normalize(correction) == "none"` — this
  line is the one place in the *existing* codebase the bug is silently masked, because
  `normalize(None)` computes `str(None).strip().lower()` → `"none"`, so the comparison happens
  to still succeed today even though the loader turned the declared string into `None` first.
  After the fix, `correction` will correctly be the string `"none"` already, and
  `normalize("none") == "none"` is still `True` — **this line's behavior is unchanged either
  way**, confirmed by direct reasoning about `normalize()`'s implementation
  (`str(value).strip().lower().replace("-", "_").replace(" ", "_")`, `dsx/spec.py:191-192`).
- No other `== "none"` or `is None` comparison in `dsx/checks/*.py` or `dsx/spec.py` was found
  touching a field whose vocabulary includes `"none"` as a legitimate value (`MULTIPLICITY_
  CORRECTIONS` includes `"none"` too, at `dsx/spec.py:61`, and is read the same
  `is_blank(...) or normalize(...) == "none"` way at `dsx/checks/design.py:459-460` — same
  masking, same "unchanged after fix" conclusion).
- **No existing test asserts the buggy behavior as correct.** `tests/test_dsx.py`'s
  `TestLoader` class (`:133-195`) has no test exercising the literal word `none` at all today —
  confirmed by reading the full class. The fix introduces new coverage, it does not need to
  un-assert anything.
- Re-running the fix locally against the full suite in this research session:

```
$ python3 -c "
import re
p = 'dsx/loader.py'
src = open(p, encoding='utf-8').read()
src2 = src.replace('_NULL = {\"\", \"null\", \"~\", \"none\"}', '_NULL = {\"\", \"null\", \"~\"}')
assert src != src2
open(p, 'w', encoding='utf-8').write(src2)
"
$ python3 -m unittest discover -s tests
```
Result: **160 tests, 1 skip, all pass** — re-verified live in this research session, matching
`.planning/research/STACK.md`'s prior claim exactly. (The local edit was reverted after
verification; the fix should land as a real Phase-6 commit, not be considered already applied.)

**Regression test to add** (REQ-P6-01's own wording, both scalar and inside a sequence):
```python
def test_bare_none_is_a_string_not_null(self):
    self.assertEqual(_parse_yaml_subset("x: none\n", "<t>")["x"], "none")
    self.assertEqual(
        _parse_yaml_subset("x: [none, clustered]\n", "<t>")["x"], ["none", "clustered"]
    )

def test_bare_none_matches_pyyaml(self):
    try:
        import yaml
    except ImportError:
        self.skipTest("PyYAML not installed")
    # PyYAML's safe_load already treats bare `none` as the string "none" (not a
    # recognised null token) — this test pins that the bundled parser now agrees.
    self.assertEqual(yaml.safe_load("x: none\n")["x"], "none")
```

### Pattern 5: Append-only `DECISIONS.jsonl` — the concrete crash-safe idiom (D-17)

**What:** `path.open("a", encoding="utf-8")`, write one `json.dumps(..., sort_keys=True) + "\n"`
line, `flush()`, `os.fsync(fh.fileno())`. Reader: iterate lines, `try: json.loads(line) except
json.JSONDecodeError: continue` (skip the unparseable tail, never fail the whole file).

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
    id: str                        # e.g. "DEC-004" — per-invocation counter, never uuid/random
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
    """Append one record. flush()+fsync() so a completed line survives a crash;
    the reader (read_all) skips an unparseable tail line rather than failing the file."""
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
            continue  # tolerant reader — a half-written crash-tail line is skipped, not fatal
    return records
```

**Windows portability note (this project's dev environment is Windows 11):**
`os.fsync(fh.fileno())` is fully supported on Windows via the CRT's `_commit()` under the hood —
no platform branch needed. `Path.open("a", ...)` opening in text-append mode with a trailing
`\n` line terminator is also portable; Python's universal-newline handling on write in text mode
translates `\n` to the platform line ending, which is fine for a JSONL file since the reader
splits on `str.splitlines()` (handles `\r\n` and `\n` uniformly) rather than on a literal `\n`
byte.

**Path resolution mirrors `find_spec()`** (`dsx/cli.py:95-114`): resolve `DECISIONS.jsonl`
relative to `phase_dir` if given, else the resolved spec's parent directory (i.e. `resolve_root`,
already threaded through `run_checks()` as `root`), matching D-14's decision ("resolved the way
`find_spec()` already resolves the spec"). Concretely, `cmd_gate` already computes
`resolve_root=args.phase_dir or str(path.parent)` (`dsx/cli.py:244`) — the exact same value
should become the base for the `DECISIONS.jsonl` path, requiring no new resolution logic, only
reuse of a value `cmd_gate` already has in scope.

**Determinism note, inherited from the existing test convention.** `id` must be a monotonic
per-invocation counter (`f"DEC-{n:03d}"`), never `uuid.uuid4()` or `datetime.now()` embedded in
content fields — `tests/test_dsx.py` already enforces byte-identical JSON output for identical
input elsewhere in this suite (search confirms a determinism-flavoured pattern is a live concern
in this codebase's test culture), and a random/timestamp-bearing `id` would make any future
determinism test over `dsx audit --json` output for a spec with `paradigm:` declared flaky by
construction. If a wall-clock timestamp is wanted at all, keep it a separate, clearly
non-canonical field.

### Pattern 6: The AST import-boundary test (D-03a / REQ-P6-10)

**What:** Static (`ast.parse`, never executes the scanned file) scan of every `dsx/frame/*.py`
module, asserting no `Import`/`ImportFrom` node resolves to `dsx.checks` or a submodule of it.
`importlib.util.resolve_name()` (stdlib since 3.3) correctly turns a relative import
(`from ..checks import design`, `level=2`) into the absolute dotted name without hand-rolling
dot-counting.

```python
# tests/test_frame_boundary.py
from __future__ import annotations

import ast
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRAME_DIR = ROOT / "dsx" / "frame"


class TestFrameImportBoundary(unittest.TestCase):
    def test_frame_never_imports_dsx_checks(self):
        if not FRAME_DIR.exists():
            self.skipTest("dsx/frame/ not created yet")
        violations = []
        for path in sorted(FRAME_DIR.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            package = _package_for(path)
            for node in ast.walk(tree):
                names: "list[str]" = []
                if isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    target = ("." * node.level) + (node.module or "")
                    resolved = (
                        importlib.util.resolve_name(target, package) if node.level else target
                    )
                    names = [resolved]
                for name in names:
                    if name == "dsx.checks" or name.startswith("dsx.checks."):
                        violations.append(f"{path}:{node.lineno}: {name}")
        self.assertEqual(violations, [], "\n".join(violations))


def _package_for(path: Path) -> str:
    parts = path.relative_to(ROOT).with_suffix("").parts
    return ".".join(parts[:-1]) if parts[-1] != "__init__" else ".".join(parts)
```

**Proving the test can fail (ROADMAP Success Criterion 4's "against a deliberately violating
case in the suite")** — this is not optional polish, it is a stated done-when criterion. Add a
second test method that constructs a violating module in a temp directory (or a fixture module
committed under `tests/fixtures/frame_boundary_violation/`) and asserts the *scanning function*
(factored out of the test method so it is independently callable) returns a non-empty violation
list for it:
```python
def test_boundary_scanner_detects_a_real_violation(self):
    violating_source = "from dsx.checks import design\n"
    violations = _scan_source_for_checks_imports(violating_source, package="dsx.frame")
    self.assertTrue(violations, "scanner failed to detect a real dsx.checks import")
```
This requires refactoring the scan body into a standalone `_scan_source_for_checks_imports(text,
package)` function callable on a string, not just on files under `FRAME_DIR` — worth flagging
explicitly because it's easy to write the boundary test only against real files and never
actually prove it can fail.

**Scope note, carried from `.planning/research/ARCHITECTURE.md` §4.3 and restated in
CONTEXT.md's Integration Points:** ARCHITECTURE.md additionally suggests the boundary test cover
"no `inference.paradigm` read outside `frame/paradigm.py`" (a *content* boundary, not an *import*
boundary — D-11's rule). CONTEXT.md does not include this in D-10's REQ-P6-10 scope explicitly,
but the ROADMAP text for Phase 7 (REQ-P7-09, REQ-P8-06) *does* require "no `DSX-VAL-*`/
`DSX-INT-*` check reads `inference.paradigm`, asserted by test" as a Phase 7/8 deliverable. This
phase (6) only needs the `dsx.frame.* → dsx.checks.*` import-boundary test; the
paradigm-content-boundary test is more naturally written once `frame/val.py`/`frame/
interference.py` exist to test (Phase 7/8), since in Phase 6 the only frame module is
`paradigm.py` itself, which is *supposed* to read `inference.paradigm`. **Flag for the planner:**
confirm this scoping explicitly rather than silently deciding it — the ROADMAP's own Phase 6
wording ("D-03a AST boundary test") only names the import boundary, so REQ-P6-10 as literally
worded is satisfied by the import-only test above; a content-boundary test belongs to Phase 7/8
where it has something real to check.

### Pattern 7: D-05 enforcement — extending `scripts/gen-finding-catalogue.py`

**What exists today**, read directly from `scripts/gen-finding-catalogue.py:59-75`:
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
This already walks every `.py` file under `dsx/` (`collect()`, line 108-124) and extracts
`(code, severity, title)` triples from `report.add(...)` calls. It has **no concept of
docstrings, citations, or tests today** — confirmed by reading the whole file (185 lines); the
only two scripts in `scripts/` are this one and `validate-capability.py`, and neither does any
D-05 checking.

**Concrete extension** (REQ-P6-11 + D-20…D-23), same AST-walk machinery, three new pieces:
1. **Docstring resolution, walking up from the `report.add(...)` call site.** Given the `ast.Call`
   node found by `extract()`, find its enclosing `ast.FunctionDef`/`ast.AsyncFunctionDef` by
   walking `ast.walk(tree)` with parent tracking (Python's `ast` module does not provide parent
   pointers natively — the extraction pass needs to build a `node → parent` map first, e.g. via
   one `ast.walk()` pass populating `parents[child] = node` for every node's children, then
   walking upward from the `Call` node through `parents` until an `ast.FunctionDef` is found;
   fall back to `ast.get_docstring(tree)` — the module docstring — if no enclosing function is
   found, per D-22).
2. **Marker assertion**, only for codes matching the allow-list (D-20): docstring text must
   contain a line matching `^\s*Citation:\s*\S` and a line matching either
   `^\s*Reference value:\s*\S` or `^\s*Structural criterion:\s*\S` (D-21/D-23).
3. **Test-linkage assertion** (D-23, second half of D-05): AST-walk every `.py` file under
   `tests/` (mirrors `dsx/suppressions.py::known_codes()`'s existing pattern of walking a
   directory with `ast.parse`) collecting every `# D-05: DSX-XXX-NNN` comment
   (`ast` does not surface comments — this half needs a plain-text `re.finditer` pass over the
   test file's source text, not an AST walk, since Python's `ast` module discards comments by
   design; `tokenize` is the alternative if comment *position* matters, but a text-level regex
   over each `tests/*.py` file is sufficient and simpler for a bare marker-presence check).
4. **The allow-list itself** (D-20): a literal set/list of code *prefixes* covered by the
   enforcement — `("DSX-PAR-", "DSX-SPEC-08")` at minimum this phase, extended by each later
   phase's own planner as `DSX-VAL-*`/`DSX-INT-*`/etc. ship. Keep this list inside the script
   (not in `dsx/`, since it is build-only config), and make `--check`'s exit code depend only on
   codes matching the allow-list — the 206 legacy codes must produce zero new failures.

```python
# scripts/gen-finding-catalogue.py — sketch of the new pieces (illustrative, not final)
_D05_ALLOWLIST_PREFIXES = ("DSX-PAR-", "DSX-SPEC-08")  # grows every later phase

_CITATION_RE = re.compile(r"^\s*Citation:\s*\S", re.MULTILINE)
_REFVALUE_RE = re.compile(
    r"^\s*(?:Reference value|Structural criterion):\s*\S", re.MULTILINE
)
_TEST_MARKER_RE = re.compile(r"#\s*D-05:\s*(DSX-[A-Z]+-\d{3})")


def check_d05(rows: list[tuple[str, str, str, str]], root: Path) -> list[str]:
    covered = [r for r in rows if r[0].startswith(_D05_ALLOWLIST_PREFIXES)]
    problems: list[str] = []
    docstrings = _resolve_docstrings(root / "dsx")   # code -> enclosing docstring text
    test_markers = _collect_test_markers(root / "tests")  # set of codes marked in tests/
    for code, *_rest in covered:
        doc = docstrings.get(code, "")
        if not _CITATION_RE.search(doc):
            problems.append(f"{code}: missing 'Citation:' line in docstring")
        if not _REFVALUE_RE.search(doc):
            problems.append(f"{code}: missing 'Reference value:'/'Structural criterion:' line")
        if code not in test_markers:
            problems.append(f"{code}: no '# D-05: {code}' marker found under tests/")
    return problems
```

**Proving it can fail (ROADMAP SC 4, again "against a deliberately violating case"):** commit one
intentionally-non-compliant fixture check (e.g. a tiny throwaway function under
`tests/fixtures/` with a `report.add("DSX-PAR-999", ...)` call and a docstring missing
`Reference value:`) and a test asserting `check_d05([...], fixture_root)` returns a non-empty
`problems` list for it, mirroring the same "prove the scanner detects a real violation" pattern
as the AST boundary test above.

### Anti-Patterns to Avoid

- **Re-deriving the `DecisionRecord` schema from scratch.** `.planning/research/STACK.md` §Q2
  already specifies it fully, verified against this codebase's conventions (mirrors
  `Finding`'s frozen-dataclass shape, avoids `Report`/`Finding` changes entirely). Re-deriving it
  risks drifting from brief §5.5's field list, which CONTEXT.md's D-07…D-19 already resolved
  every open question about (storage location, crash-safety, identifier naming, invocation
  grouping).
- **Treating `dsx/decisions.py` and `dsx/checks/decision.py` as related.** They are two
  unrelated, pre-existing-and-new modules with confusingly similar names:
  `dsx/checks/decision.py` (singular, existing, owns `DSX-DEC-*` — decision-*replay* against
  `results.tests`) is untouched this phase; `dsx/decisions.py` (plural, new, D-13/D-14's
  decision-*record* emitter) is new top-level code. Flag this in the plan's task descriptions so
  an implementer does not conflate or accidentally edit the wrong file.
  `dsx/checks/decision.py::check(spec, *, gate_point=...)` is a useful *pattern* precedent for
  `run_checks()`'s explicit-dispatch-table entries (it already takes `gate_point` as a keyword,
  exactly the shape a future `dsx/frame/paradigm.py::check(spec)` may or may not need — `paradigm`
  needs no `gate_point` differentiation this phase since `DSX-PAR-001` behaves identically at
  every gate point, so it can fall through to the generic `CHECKS[name](spec)` branch in
  `run_checks()`, requiring no new dispatch-table entry).
- **Widening `_check_peeking`/`DSX-EXP-060` to recognise the new `uncontrolled_continuous`
  member.** M-01 and D-08 are explicit: `DSX-EXP-060`'s trigger (`policy in ("",
  "fixed_horizon")`) is a literal tuple, disjoint from `PEEKING_POLICIES` membership by
  construction, and must stay untouched. The parametrised disjointness test (D-08) exists
  specifically to catch a future accidental widening.
- **Building a YAML writer for `DECISIONS.jsonl`.** `dsx/loader.py` has no write path at all
  today; JSON Lines is the deliberate, simpler choice (Pattern 5 above).
- **Scaffolding `references/families.yaml` or `dsx/frame/admissibility.py` "to be safe."**
  Explicitly out of scope (brief §6.6 item 2; CONTEXT.md's Phase Boundary section states this
  directly) — an empty ontology file or empty check module accumulates speculative structure
  with nothing yet to justify its shape.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| YAML null-token recognition | A new null-detection regex/heuristic | The existing `_NULL` set, minus `"none"` | It is one set literal; the fix is smaller than any alternative design |
| Decision-record persistence format | A custom binary/line-delimited format, or extending `dsx/loader.py` with a writer | `json.dumps(..., sort_keys=True)` per line | Zero escaping edge cases by construction; JSON is already privileged as the loader's fast-path format |
| AST parent-pointer tracking for docstring walk-up | A third-party AST utility library | One `ast.walk()` pass building a `dict[ast.AST, ast.AST]` parent map (stdlib `ast` has no built-in parent links) | D-01/D-05's own build-script exemption still favors stdlib-only for consistency; the parent-map pattern is ~10 lines |
| Relative-import resolution in the boundary test | Hand-rolled dot-counting on `ast.ImportFrom.level` | `importlib.util.resolve_name(target, package)` (stdlib since 3.3) | Exactly the off-by-one-prone logic a boundary-enforcement test must not itself contain a bug in |
| Crash-safe file append | A custom write-ahead-log or lock-file scheme | `open(path, "a")` + `flush()` + `os.fsync(fh.fileno())`, tolerant line-based reader | The standard, minimal idiom for this exact durability guarantee; no external dependency, no new abstraction |

**Key insight:** every piece of new infrastructure this phase needs already has either (a) a
directly analogous, working pattern elsewhere in this same codebase (`_validate_design_shape`,
`known_codes()`'s AST walk, `find_spec()`'s path resolution, `Finding`'s frozen-dataclass shape),
or (b) a fully-specified design already produced by `.planning/research/STACK.md` and confirmed
consistent with every Phase-6 CONTEXT.md decision in this pass. The risk in this phase is not
"what pattern to use" — it is executing precisely against fifteen small pieces without drifting
from any of the twenty-three locked decisions.

## Common Pitfalls

### Pitfall 1: Treating `PEEKING_POLICIES`'s dict-shape as new work

**What goes wrong:** CONTEXT.md's D-04 ("every new frame vocabulary is a name→description dict")
can read as implying `PEEKING_POLICIES` itself needs a shape conversion. It does not — it is
already a dict (verified above, Pattern 2). The actual defect is `describe_vocabulary()`'s dump.
**Why it happens:** the CONTEXT.md prose groups "extend `PEEKING_POLICIES`" alongside "make new
vocabularies dicts," inviting the misread.
**How to avoid:** the plan's task for `PEEKING_POLICIES` should be scoped as "(a) add one dict
entry, (b) fix `describe_vocabulary()`'s dump for this one key" — two small, independent
sub-changes, not a shape migration.
**Warning signs:** a task description that says "convert `PEEKING_POLICIES` to a dict."

### Pitfall 2: The `missingness.mechanism` vocabulary contradiction between ROADMAP and brief §5.1

**What goes wrong:** `ROADMAP.md`'s ordering-constraint text states four fields use `"none"` as a
legitimate value: `dependence.structure`, `interference.risk`, `interference.mitigation`,
**and `missingness.mechanism`**. But `brief.md` §5.1's own worked example comments
`missingness.mechanism`'s vocabulary as `MCAR | MAR | MNAR | not_assessed` — no `"none"` member
anywhere in that list. These two binding sources disagree on whether `MISSINGNESS_MECHANISMS`
needs a `"none"` member (meaning, presumably, "no missing data at all," distinct from
`not_assessed` meaning "haven't checked").
**Why it happens:** likely an editing slip in the ROADMAP's ordering-constraint prose (it may
have meant `identification.constraint_source`, which brief §5.1 *does* list `none` for, instead
of `missingness.mechanism`) — but this research cannot resolve which source is correct without
guessing, so it is surfaced rather than silently picked.
**How to avoid:** the planner should treat this as a genuinely open five-minute question — decide
whether `MISSINGNESS_MECHANISMS` gets a fifth member (`none`, "no missingness present, nothing to
assess") alongside `MCAR`/`MAR`/`MNAR`/`not_assessed`, or whether the ROADMAP's four-field list is
simply imprecise and the real fourth `"none"`-bearing field is `identification.constraint_source`
(which is already independently known to need `"none"` as a member from brief §5.1's own comment:
`constraint_source: none | informative_priors | penalisation | design_restriction |
hierarchical_pooling`). Either resolution is minor, but it should be a stated choice, not an
accident of which of the two contradicting sources was read last.
**Warning signs:** a `MISSINGNESS_MECHANISMS` vocabulary with exactly four members and no
`"none"`, next to a loader regression test that only exercises the three fields brief §5.1
explicitly names — check this specific field was actually decided, not silently dropped.

### Pitfall 3: `_validate_validity_frame_shape()`'s aggregation logic (D-11) is new code, not a copy

Already flagged under Pattern 1 above — restated here because ROADMAP Success Criterion 2 makes
it a concrete, testable done-when condition ("a descriptive-question spec that omits
`interference`/`triggering`/`stability` entirely also exits 0, while a causal spec omitting them
blocks... aggregate-when-absent... one finding itemising every missing required sub-block").
**Warning sign:** a plan task that estimates this validator at the same size as
`_validate_design_shape` (which has no requiredness-by-question-type logic and no aggregation
logic) is under-scoped.

### Pitfall 4: Forgetting the `add_common()` refactor is a prerequisite for `dsx explain`, not a nice-to-have

**What goes wrong:** `dsx/cli.py:427-434`'s `add_common()` adds `--spec`, `--phase-dir`,
`--block-on`, `--json`, `--verbose` to *every* subcommand parser uniformly, called by all nine
existing subcommands that need common flags. D-18 requires `dsx explain` to accept `--spec`/
`--phase-dir`/`--json` but explicitly *not* `--block-on` (a command that always exits 0 must not
carry a flag implying it can be configured to block). Simply not calling `add_common()` for
`p_explain` and hand-adding the three wanted flags duplicates argument definitions and drifts
from the other subcommands' exact wording/defaults over time.
**How to avoid:** refactor `add_common()` to take a parameter (e.g. `add_common(p,
include_block_on=True)`) so `dsx explain` reuses the same three flag definitions verbatim while
opting out of the fourth — exactly D-18's own stated instruction ("Refactor `add_common()` to
make the blocking flags opt-in rather than copy-pasting three arguments into a new parser").
**Warning sign:** `p_explain.add_argument("--spec", ...)` appearing as a literal duplicate of the
line already in `add_common()`.

### Pitfall 5: `templates/ANALYSIS-SPEC.yaml`'s scaffolded blocks must still fail Phase 7/8 content checks

**What goes wrong:** D-12 requires the template to scaffold both new blocks in full with
placeholder values so `dsx init` output keeps passing `dsx gate plan` *structurally* this phase.
It would be easy to over-fill placeholders with values that look too clean, causing a false sense
that the scaffolded template is "done" — but ROADMAP is explicit: "Placeholders will still fail
Phase 7 falsifiability and Phase 8 mitigation checks; that is correct — Phase 6 checks shape,
later phases check content."
**How to avoid:** placeholder values should be honestly generic (e.g. `estimand.falsifier:
"<the observation that would prove this wrong>"`, not a fabricated realistic-sounding falsifier)
so Phase 7's real falsifiability check has something genuine to fail against, and reviewers do
not mistake template output for a filled-in analysis.
**Warning sign:** a template placeholder value that reads like a plausible real analysis rather
than an obvious fill-in-the-blank prompt (contrast with the existing template's own established
style, e.g. `title: "<one line: the decision this analysis exists to support>"`).

### Pitfall 6: `known_codes()` auto-discovery means suppressions "just work" — verify, don't re-implement

**What goes wrong:** `dsx/suppressions.py::known_codes()` (`:24-54`) already AST-walks every
`.py` file under `dsx/` for `report.add("DSX-...", ...)` calls, so any new code emitted by
`dsx/frame/paradigm.py` or the new `DSX-SPEC-08x` validators is automatically suppressible with
zero registration step. It would be wasted work to add a manual registration path for the new
codes into `dsx/suppressions.py`.
**How to avoid:** the plan should include a verification task ("suppress `DSX-PAR-001`/a
`DSX-SPEC-08x` code via `suppressions[]` and confirm it is recognised without code changes to
`dsx/suppressions.py`"), not an implementation task.
**Warning sign:** a plan task titled "register DSX-PAR-001 / DSX-SPEC-08x with the suppression
system."

## Runtime State Inventory

Not applicable — Phase 6 is contract-extension and new-module work, not a rename, refactor, or
migration. No existing identifiers are being renamed; `PEEKING_POLICIES`'s new member is an
addition (D-06: safe by construction, not a finding-code renumbering); the `_NULL` fix changes
*parsing behavior* for a previously-unused-honestly value, not an identifier rename — the closest
analogue to a "migration" concern is Pitfall 9 in `.planning/research/PITFALLS.md`
(`validity_frame:` becoming required breaks pre-existing specs), which is already addressed by
this phase's own scope: M-07's `suppressions[]` grandfather path (zero new code) plus REQ-P6-15's
README documentation of that migration path.

## Code Examples

### `_NULL` fix (REQ-P6-01)
See Pattern 4 above — the fix and its two regression tests are the complete example.

### `_validate_validity_frame_shape()` skeleton (REQ-P6-02, REQ-P6-03, D-09, D-10, D-11)
```python
# dsx/spec.py — new, follows _validate_design_shape's idiom, adds requiredness+aggregation
_VALIDITY_FRAME_ALWAYS_REQUIRED = ("estimand", "units", "measurement")  # per M-06 / CONTEXT.md
_VALIDITY_FRAME_CAUSAL_REQUIRED = ("identification", "interference", "triggering", "stability")
# NOTE: "identification" placement (always vs causal-only) is not pinned by CONTEXT.md's
# explicit list ("estimand, units, measurement" always required; "interference, triggering,
# stability" required only for causal/experimental) — confirm against REQUIREMENTS.md's exact
# wording (REQ-P6-03) before finalizing which list identification/dependence/sampling_frame/
# missingness belong to; REQ-P6-03's literal text only pins the two lists shown, leaving
# identification/dependence/sampling_frame/missingness unstated. Flagged as an assumption below.

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
            detail="Missing sub-blocks: " + ", ".join(required),
            remedy="Add validity_frame: with at least " + ", ".join(required) + ". "
                   "See templates/ANALYSIS-SPEC.yaml.",
            where="spec.validity_frame",
        )
        return

    missing = [name for name in required if not isinstance(block.get(name), dict) or not block[name]]
    if missing:
        report.add(
            "DSX-SPEC-081", "CRITICAL",
            f"validity_frame is missing {len(missing)} required sub-block(s)",
            detail="Missing: " + ", ".join(missing),
            remedy="Add each missing sub-block. See templates/ANALYSIS-SPEC.yaml.",
            where="spec.validity_frame",
        )
    else:
        report.ok("validity_frame required sub-blocks present")
    # ... membership checks against the new closed vocabularies follow, one block per
    # sub-field, mirroring _validate_design_shape's per-field pattern exactly.
```
**This sketch is illustrative, not prescriptive on exact code numbers or the identification/
dependence/sampling_frame/missingness list placement — those are explicitly Claude's Discretion
per CONTEXT.md ("Exact `DSX-SPEC-08x` number assignments").**

### `dsx explain`: wiring into `dsx/cli.py`
```python
# dsx/cli.py — new subcommand, following every existing cmd_* function's shape
def cmd_explain(args: argparse.Namespace) -> int:
    from .decisions import read_all

    path = find_spec(args.spec, args.phase_dir)  # reuse existing resolution — same as every
    decisions_path = path.parent / "DECISIONS.jsonl"  # other subcommand's spec discovery
    records = read_all(decisions_path)
    if args.invocation:
        records = [r for r in records if r.get("invocation_id") == args.invocation]
    elif records:
        latest = max(r.get("invocation_id", "") for r in records if r.get("layer") == "header")
        records = [r for r in records if r.get("invocation_id") == latest]
    if args.json:
        print(json.dumps(records, indent=2))
    else:
        print(_render_decision_trail(records))
    return 0  # ALWAYS 0 — D-04/D-18: dsx explain never participates in the block contract
```
Registration:
```python
p_explain = sub.add_parser("explain", help="render the decision trail (never blocks)")
add_common(p_explain, include_block_on=False)   # D-18's opt-in refactor
p_explain.add_argument("--invocation", help="render one invocation id (default: most recent)")
p_explain.set_defaults(func=cmd_explain)
```

### `Severity.INFO` end to end (REQ-P6-09) — traced, not assumed

Every step of the `DSX-PAR-001` INFO manifest was traced through the real, unmodified
`Severity`/`Report`/`emit()` code:

1. `report.add("DSX-PAR-001", "INFO", "...", where=..., applied=[...], not_applied=[...])` →
   `Report.add()` (`dsx/findings.py:101-121`) calls `Severity.parse("INFO")` →
   `Severity.INFO` (int value `10`, `dsx/findings.py:29`) — no different from any other
   `report.add(...)` call anywhere in this codebase.
2. `Report.blocks(threshold)` (`:140-141`) = `bool(self.at_or_above(threshold))`;
   `at_or_above` keeps only findings `>= threshold`. `GATE_THRESHOLDS` (`dsx/cli.py:87-92`) is
   `CRITICAL` (50) at plan/execute, `HIGH` (40) at verify/ship — both far above `INFO`'s `10`.
   An INFO finding can only ever block if a caller explicitly passes `--block-on INFO`.
3. `emit()` (`dsx/findings.py:185-199`) computes `code = report.exit_code(threshold)` purely from
   `blocks()`; an INFO-only addition to an otherwise-passing report leaves `code == EXIT_PASS`.
4. **Visibility is preserved on a pass.** `emit()` routes to `stdout` when `code == EXIT_PASS`,
   and `report.render()` (`:162-179`) iterates *all* findings regardless of threshold — the
   threshold only gates the final PASS/BLOCK summary line, not which findings print. So
   `DSX-PAR-001`'s manifest text prints on every passing gate run where `paradigm` is declared.
5. `Report.counts()` (`:143-147`) already initialises an `"INFO"` bucket
   (`{s.label: 0 for s in Severity}` iterates the full enum) — no changes needed anywhere in
   `dsx/findings.py`.

**Net: `DSX-PAR-001` requires zero changes to `dsx/findings.py`.** `Severity.INFO` exists with
zero consumers today (confirmed by grep: the only hits for `INFO` in `dsx/` are the enum member
itself and a label list in `Report.render()`) — `DSX-PAR-001` is its first real user.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|---------------|--------|
| `_NULL` includes `"none"` (diverges from PyYAML/YAML) | `_NULL` excludes `"none"` (matches PyYAML/YAML) | This phase (REQ-P6-01) | Any spec field whose declared value is the literal string `none` (four+ new frame fields) round-trips correctly instead of silently becoming `None` |
| `describe_vocabulary()`'s `peeking_policies` dump is a flat sorted list of keys | Name→description dict | This phase (D-03) | An operator running `dsx vocab` sees *why* `uncontrolled_continuous` differs from `always_valid`, not just that both exist |
| `Severity.INFO` exists in the ladder with zero real consumers | `DSX-PAR-001` is the first INFO-severity finding ever emitted by this codebase | This phase (REQ-P6-09) | Proves out the INFO tier end-to-end for every future informational finding |
| Zero decision-record infrastructure anywhere in `dsx/` | `dsx/decisions.py` + `DECISIONS.jsonl` + `dsx explain` | This phase (REQ-P6-07/08) | First append-only artifact this codebase writes; every prior artifact (`DATA-REVIEW.md`, `FIGURE-MANIFEST.yaml`) is written once, not appended to |
| D-05 (citation + reference-value discipline) enforced by code review only | Mechanically enforced by `scripts/gen-finding-catalogue.py --check` for new-in-v2.0.0 codes | This phase (REQ-P6-11) | Closes the one load-bearing project rule (per `.planning/research/PITFALLS.md` Pitfall 4) that was previously pure convention |

**Deprecated/outdated:** Nothing in this codebase is being deprecated this phase — every change
is additive or a narrow bug fix.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | `identification`, `dependence`, `sampling_frame`, `missingness` sub-blocks' requiredness-by-`question_type` placement is not pinned by REQ-P6-03's literal wording (only `estimand`/`units`/`measurement` "always" and `interference`/`triggering`/`stability` "causal-only" are explicit) | Code Example: `_validate_validity_frame_shape()` skeleton | If the planner assumes a placement the requirement doesn't actually state, `DSX-SPEC-081`'s required-list could diverge from what REQ-P6-03 (as written in `.planning/REQUIREMENTS.md`) actually requires, causing a plan/verify mismatch later |
| A2 | The `missingness.mechanism` vocabulary needs a `"none"` member (per ROADMAP's ordering-constraint prose) despite brief §5.1's own comment listing only `MCAR \| MAR \| MNAR \| not_assessed` | Pitfall 2 | If unresolved, the loader regression test set (REQ-P6-01) might not cover the field the ROADMAP explicitly named, or `MISSINGNESS_MECHANISMS` might ship without a member the ROADMAP implies is needed |
| A3 | `inference.declared_at`'s vocabulary (if closed at all) is a two-value set `{pre_data, post_data}` used descriptively only, not gated by any check this phase (its self-reported, unverifiable nature is a known limit for the README per Pitfall 1, not something Phase 6 code can close) | REQ-P6-04 support | If a closed vocabulary is expected but not created, `DSX-SPEC-08x` shape validation for `inference:` may be incomplete against REQUIREMENTS.md's literal field list |
| A4 | `_validate_validity_frame_shape()`/`_validate_inference_shape()` are two separate functions (mirroring `validate_structure()`'s existing one-function-per-section convention) rather than one combined function | Pattern 1 | Low risk — either shape satisfies D-09's "mirror `_validate_design_shape`" instruction; a combined function would still work but diverges slightly from the one-section-one-function convention every other `_validate_*` function in `dsx/spec.py` follows |
| A5 | `"paradigm"` is the right `CHECKS`/`GATE_PROFILES` key name for the new `dsx/frame/paradigm.py::check` registration (matching the module filename), consistent with every existing key (`"design"`, `"claims"`, etc. matching their module names) | Recommended Project Structure | Low risk — purely a naming convention choice with no functional consequence, listed only because CONTEXT.md doesn't state the registration key explicitly |

**All five assumptions above are LOW-to-MEDIUM risk and independently resolvable by the planner
reading `.planning/REQUIREMENTS.md`'s literal REQ-P6-03/REQ-P6-04 text at plan time** — flagged
here because this research pass found the CONTEXT.md/ROADMAP/brief.md sources underspecify or
lightly contradict each other on these five narrow points, and none should be silently guessed.

## Open Questions

> **RESOLVED AT PLAN TIME (2026-08-07, operator decision).** Questions 1 and 2 below were put to
> the operator during `/gsd-plan-phase 6` and are now **locked**. They are binding on the plan;
> the discussion beneath each is retained only as the reasoning that produced the answer.
>
> **R-01 — `validity_frame` sub-block requiredness (resolves Open Question 2 / Assumption A1).**
> The four sub-blocks REQ-P6-03 leaves unpinned are placed as:
> - `dependence`, `sampling_frame`, `missingness` → **always required**, every `question_type`.
> - `identification` → **required only for causal and experimental** question types, joining
>   `interference`/`triggering`/`stability`.
>
> Full resulting lists for `_validate_validity_frame_shape()` / `DSX-SPEC-081`:
> - **Always required (6):** `estimand`, `units`, `measurement`, `dependence`, `sampling_frame`,
>   `missingness`
> - **Causal/experimental only (4):** `identification`, `interference`, `triggering`, `stability`
>
> Rationale: `dependence` and `sampling_frame` are paradigm-independent per D-11 and PITFALLS.md
> Pitfall 2 (every analysis has a unit of observation and a claimed population). `missingness`
> applies to every dataset, with `not_assessed` as the honest escape hatch — so a silently
> truncated descriptive dataset still has to be declared. `identification` is meaningless without
> a causal claim, and `DSX-CAU-010` / `_check_identification` is the existing precedent for
> gating it on `question_type`.
>
> Note the deliberate divergence from PITFALLS.md Pitfall 2, which put `interference` in the
> conditional-with-justification tier and `identification` in the causal-only tier. REQ-P6-03 and
> ROADMAP Success Criterion 2 are the binding sources and both place `interference` squarely in
> the causal-only list ("a descriptive-question spec that omits `interference`/`triggering`/
> `stability` **entirely** also exits `0`"). Where PITFALLS.md and REQUIREMENTS.md disagree,
> REQUIREMENTS.md wins.
>
> **R-02 — `MISSINGNESS_MECHANISMS` gets no `"none"` member (resolves Open Question 1 /
> Assumption A2).** The vocabulary ships as exactly `MCAR | MAR | MNAR | not_assessed`, per
> brief.md §5.1. ROADMAP.md's ordering-constraint prose naming `missingness.mechanism` as a
> `none`-bearing field is an editing slip; the intended fourth field is
> `identification.constraint_source`, which brief.md §5.1 does list `none` for. The REQ-P6-01
> `_NULL` loader fix and its bundled-parser-vs-PyYAML agreement test are **unchanged in scope** —
> they are simply exercised through the three frame fields that genuinely declare `none`
> (`dependence.structure`, `interference.risk`, `interference.mitigation`) plus
> `identification.constraint_source`, not through `missingness.mechanism`.
>
> Open Question 3 (`paradigm.check()` needs no `gate_point` parameter) was already answered by the
> research itself and needs no operator input — implement as recommended.

1. **Does `MISSINGNESS_MECHANISMS` need a `"none"` member?**
   - What we know: ROADMAP.md's ordering-constraint text names `missingness.mechanism` as one of
     four `"none"`-bearing fields; brief §5.1's own worked-example comment lists only
     `MCAR | MAR | MNAR | not_assessed`.
   - What's unclear: whether this is a ROADMAP editing slip (intending
     `identification.constraint_source`, which brief §5.1 does list `none` for) or a genuine,
     separately-needed fifth member.
   - Recommendation: five-minute planner decision, documented inline in the vocabulary's own
     comment either way; low blast radius regardless of which way it's resolved.

2. **Exact placement of `identification`/`dependence`/`sampling_frame`/`missingness` in the
   always-required vs causal-only lists.**
   - What we know: REQ-P6-03's literal text only pins two lists explicitly (always: `estimand`,
     `units`, `measurement`; causal-only: `interference`, `triggering`, `stability`).
   - What's unclear: the other four sub-blocks' requiredness gating isn't stated by REQ-P6-03 as
     quoted in `.planning/REQUIREMENTS.md`.
   - Recommendation: re-read `.planning/REQUIREMENTS.md`'s REQ-P6-03 line verbatim at plan time
     (it is quoted in full in this research's Phase Requirements table above) — if it genuinely
     only names six of the ten sub-blocks, the remaining four (`identification`, `dependence`,
     `sampling_frame`, `missingness`) need an explicit placement decision, most naturally
     "always required" (since every analysis has *some* dependence structure and missingness
     rate to declare, paradigm-independent per D-11, matching Pitfall 2's own PITFALLS.md
     reasoning: "`estimand`, `units`, `dependence`, `sampling_frame`, `measurement` — required
     for every question type").

3. **Does the `dsx/frame/paradigm.py` `check()` signature need `gate_point`?**
   - What we know: `DSX-PAR-001` behaves identically at every gate point per D-10/architecture
     research (registered at plan/execute/verify/ship uniformly, always INFO).
   - What's unclear: nothing, functionally — this is answered by the research (no `gate_point`
     differentiation needed), included here only so the planner doesn't over-build a dispatch
     path `run_checks()` doesn't need.
   - Recommendation: `paradigm.check(spec)` with no `gate_point` parameter; falls through to the
     generic `CHECKS[name](spec)` branch in `run_checks()` (`dsx/cli.py:156-157`), requiring no
     new explicit-dispatch entry.

## Environment Availability

Skipped — Phase 6 has no external dependencies. Every tool used (`python3`, `git`) is already
confirmed present and in use by the existing test suite and this research session's own
verification commands (both executed successfully against this repository in this session).

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | `unittest` (Python 3.9+ stdlib) — the only test runner used anywhere in this codebase |
| Config file | none — no `pytest.ini`/`setup.cfg`/`pyproject.toml` test config exists; tests are discovered by directory convention |
| Quick run command | `python3 -m unittest discover -s tests -v` (full suite; completes in ~0.25s per this session's own run — no meaningfully faster "quick" subset exists or is needed) |
| Full suite command | `python3 -m unittest discover -s tests -v` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| REQ-P6-01 | Bundled parser agrees with PyYAML on bare `none` (scalar + sequence) | unit | `python3 -m unittest tests.test_dsx.TestLoader.test_bare_none_is_a_string_not_null -v` | ❌ Wave 0 (new test method) |
| REQ-P6-02 | Extended spec round-trips through `load()`/`loads()` | unit/integration | `python3 -m unittest tests.test_dsx.TestSpecStructure -v` (new test class or extension) | ❌ Wave 0 |
| REQ-P6-03 | `question_type`-gated requiredness fires/doesn't fire correctly | unit | new test(s) asserting `DSX-SPEC-08x` for both a causal spec (blocks) and a descriptive spec (passes) omitting the causal-only sub-blocks | ❌ Wave 0 |
| REQ-P6-04 | `inference:` block round-trips, no `stopping_rule` field anywhere | unit | grep-based or structural test asserting `"stopping_rule"` is absent from `dsx/spec.py`'s inference vocabulary/validator | ❌ Wave 0 |
| REQ-P6-05 | `PEEKING_POLICIES` disjointness (D-08) | unit | parametrised test over all 5 members asserting `DSX-EXP-060` fires only for `""`/`fixed_horizon` | ❌ Wave 0 |
| REQ-P6-06 | Vocabulary registry coverage; `dsx vocab` dumps every new vocabulary with descriptions | unit | new coverage test over `_VOCABULARIES` | ❌ Wave 0 |
| REQ-P6-07 | `DECISIONS.jsonl` append/read round-trips; tolerant of a truncated tail line | unit | new `tests/test_decisions.py` (or extend `test_dsx.py`) | ❌ Wave 0 (new file) |
| REQ-P6-08 | `dsx explain` always exits 0, including on empty/missing `DECISIONS.jsonl` | integration | CLI-level test via `TestCLI._run(["explain", ...])`-style harness | ❌ Wave 0 |
| REQ-P6-09 | `DSX-PAR-001` never blocks at any `--block-on` including `INFO` itself... actually per D-09/`Severity.parse`, an explicit `--block-on INFO` *would* technically block — confirm exact wording of "cannot block at any configured threshold" (i.e. the four `GATE_THRESHOLDS` defaults, not an operator override) before writing this test's assertion | unit + integration | test asserting exit 0 at all four default `GATE_THRESHOLDS` with `paradigm: bayesian` declared | ❌ Wave 0 |
| REQ-P6-10 | AST boundary test exists, passes on real code, fails on a deliberately violating fixture | unit (meta-test) | `python3 -m unittest tests.test_frame_boundary -v` | ❌ Wave 0 (new file) |
| REQ-P6-11 | `gen-finding-catalogue.py --check`-equivalent fails on a missing-citation fixture | unit (meta-test, build-script) | new `tests/test_gen_finding_catalogue.py` or extend the script itself with a `--self-test` | ❌ Wave 0 (new file) |
| REQ-P6-12 | Two existing D-08 tests (`test_good_fixture_passes_every_gate`, `test_bad_fixture_blocks_at_plan`/`_at_ship`) remain green, unedited | integration | `python3 -m unittest tests.test_dsx.TestCLI -v` (existing, must not be modified per D-08) | ✅ exists (`tests/test_dsx.py:804-839`) |
| REQ-P6-13 | Each `known-bad/*` fixture parses + passes `dsx validate` structurally | integration | new test(s) iterating `examples/known-bad/*.yaml`, asserting `dsx validate --spec <fixture>` exits 0 or 2 (not a semantic block, since the check logic doesn't exist yet) | ❌ Wave 0 |
| REQ-P6-14 | `.planning/REVERSALS.md` exists with the D-14 template | manual/doc check | file-existence assertion (or manual review — this is a docs deliverable, not gate-path code) | N/A — docs |
| REQ-P6-15 | README documents `suppressions[]` migration + known limit | manual/doc check | manual review | N/A — docs |
| REQ-P6-16 | Version `2.0.0`; catalogue regenerated and current | integration | `python3 scripts/gen-finding-catalogue.py --check` (existing mechanism, must pass) | ✅ exists |

### Sampling Rate
- **Per task commit:** `python3 -m unittest discover -s tests` (full suite — it is already fast
  enough, ~0.25s, that there is no meaningful "quick" vs "full" distinction in this codebase)
- **Per wave merge:** same, plus `python3 scripts/gen-finding-catalogue.py --check`
- **Phase gate:** full suite green, catalogue current, `dsx gate {plan,execute,verify,ship}
  --spec examples/good-ANALYSIS-SPEC.yaml` all exit 0, `dsx gate plan/ship --spec
  examples/bad-ANALYSIS-SPEC.yaml` exit 1, before `/gsd-verify-work`

### Wave 0 Gaps
- [ ] `tests/test_frame_boundary.py` — new file, covers REQ-P6-10 (does not exist; `dsx/frame/`
  itself does not exist yet either)
- [ ] `tests/test_decisions.py` (or a `TestDecisions` class in `test_dsx.py`) — covers REQ-P6-07
- [ ] `tests/test_gen_finding_catalogue.py` (or a self-test mode in the script itself) — covers
  REQ-P6-11
- [ ] New test methods within the existing `TestLoader`, `TestSpecStructure`, `TestCLI` classes
  in `tests/test_dsx.py` for REQ-P6-01/02/03/05/06/08/09/13 — no new file needed, the existing
  1606-line file and its established per-class organisation is the right home
- [ ] No framework install needed — `unittest` is stdlib

## Security Domain

### Applicable ASVS Categories

This is a local, single-user CLI tool with no network listener, no authentication surface, and
no session concept — most ASVS categories (V2 Authentication, V3 Session Management, V4 Access
Control) are structurally inapplicable, confirmed by re-reading the whole of `dsx/cli.py` (no
network code, no credential handling anywhere in this codebase).

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V1 Architecture, Design & Threat Modeling | Partially | The D-03a module boundary *is* a threat-modeling control in miniature (limits blast radius of a future extraction); the AST boundary test is its enforcement |
| V2 Authentication | No | No auth surface — local CLI, no network listener |
| V3 Session Management | No | No sessions — each `dsx gate` invocation is stateless except for the new append-only `DECISIONS.jsonl` |
| V4 Access Control | No | No multi-user access model |
| V5 Input Validation | Yes | `dsx/loader.py`'s `SpecParseError` (fail-loud on unparseable input) is the existing control; the `_NULL` fix is itself an input-validation correctness fix (a value silently becoming `None` instead of raising or round-tripping is a validation-fidelity defect, not a memory-safety one) |
| V6 Cryptography | No | No crypto in this phase's scope (SHA-256 hashing of the `validity_frame`/`inference` blocks for the D-16 content-lock digest uses stdlib `hashlib.sha256`, a non-cryptographic-integrity use — it is a change-detection digest, not a security control, so V6 is not meaningfully engaged) |
| V7 Error Handling & Logging | Yes | `DECISIONS.jsonl` is effectively a structured audit log; the tolerant-reader pattern (D-17) is itself an error-handling control (a corrupted tail line must not crash `dsx explain` or hide the rest of the trail) |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Path traversal via `--spec`/`--phase-dir` CLI arguments pointing outside the intended directory | Tampering / Information Disclosure | Not a new risk introduced by Phase 6 — `find_spec()` already resolves arbitrary user-supplied paths (this is by design; a local CLI operating on files the invoking user already has filesystem access to is not a privilege boundary). Phase 6's `DECISIONS.jsonl` write path reuses the same resolution (`resolve_root`), so it inherits the same trust model — no new mitigation needed, but worth a one-line note in the plan that the new write path does not introduce a new untrusted-input boundary beyond what `dsx gate` already accepts |
| A malformed/adversarial `DECISIONS.jsonl` (e.g. crafted to crash `dsx explain`) | Denial of Service | The tolerant-reader pattern (skip unparseable lines) directly mitigates this; also `dsx explain` is read-only and never feeds parsed content back into anything that executes it (no `eval`/`exec` anywhere in this codebase, confirmed by the absence of those builtins in any file read during this research pass) |
| Unbounded growth of `DECISIONS.jsonl` across many gate invocations | (Availability, minor) | Out of scope for this phase per CONTEXT.md; not flagged as a blocking concern — a phase-scoped analysis directory producing tens of records per gate invocation over a phase's lifetime is bounded in practice; no rotation/truncation mechanism is required by any REQ-P6-* |

## Sources

### Primary (HIGH confidence — direct reads and live execution against this repository)
- `dsx/loader.py` — full file read; `_NULL` bug reproduced live in this research session
- `dsx/spec.py` — full file read; `PEEKING_POLICIES`/`describe_vocabulary()` exact lines confirmed
- `dsx/findings.py` — full file read; `Severity.INFO`/`Report.blocks()`/`emit()` traced
- `dsx/cli.py` — full file read; `GATE_PROFILES`/`GATE_THRESHOLDS`/`add_common()`/`run_checks()` confirmed
- `dsx/suppressions.py` — full file read; `known_codes()`'s AST-walk pattern confirmed
- `dsx/checks/design.py` — full file read; `_check_peeking`/`DSX-EXP-060`/`_check_identification` confirmed
- `dsx/checks/decision.py`, `dsx/checks/smells.py`, `dsx/checks/claims.py` (partial), `dsx/checks/coherence.py` (partial) — read for naming-collision and requiredness-pattern precedent
- `dsx/mathx.py` — full file read (Phase 9 context, `inflation_from_peeking()` confirmed for future reuse)
- `scripts/gen-finding-catalogue.py` — full file read; `extract()`/`collect()` machinery confirmed
- `tests/test_dsx.py` — targeted reads (`TestLoader`, `TestCLI`, `TestMath`, unit-triad tests); 1606 lines, 160 tests / 1 skip confirmed by live execution
- `templates/ANALYSIS-SPEC.yaml`, `examples/good-ANALYSIS-SPEC.yaml`, `examples/bad-ANALYSIS-SPEC.yaml` — full reads
- `README.md` (partial) — confirmed no existing "known limit"/frame-that-lies text
- `brief.md` — full file read (§4 D-01…D-14, §5 contract, §6/6.5/6.6, §7, §8, §9)
- `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/STATE.md` — full reads
- `.planning/phases/06-.../06-CONTEXT.md`, `06-DISCUSSION-LOG.md` — full reads
- Live command execution in this session: `_parse_yaml_subset` bug repro; full test suite run
  (160 passed, 1 skipped); the `_NULL` fix applied and re-verified against the full suite, then
  reverted

### Secondary (MEDIUM confidence — prior research, verified consistent with the primary sources above)
- `.planning/research/STACK.md`, `.planning/research/ARCHITECTURE.md`, `.planning/research/
  PITFALLS.md`, `.planning/research/FEATURES.md`, `.planning/research/SUMMARY.md` — full reads;
  every structural claim cross-checked against this session's own direct reads/execution and
  found consistent (no contradictions found between the milestone-level research and this
  phase-level pass, apart from the two open questions flagged above, which arise from
  discrepancies between `ROADMAP.md`/`brief.md` themselves, not from the research documents)

### Tertiary (LOW confidence)
- None — this phase required no external web research; every claim traces to this repository's
  own source, tests, or planning documents.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — zero new dependencies, every module verified present in Python 3.9+ stdlib
- Architecture: HIGH — every file path, line number, and function signature verified by direct read; the `_NULL` bug and the test-suite pass count were re-executed live, not merely cited
- Pitfalls: HIGH — six pitfalls identified, four grounded in direct contradictions/gaps found between binding sources during this research pass (Pitfalls 2, 3, 4, 5), two in codebase-naming-collision risk (Pitfalls 1, 6)

**Research date:** 2026-08-07
**Valid until:** Effectively indefinite for the structural claims (this is a stable, internal
codebase, not a fast-moving external ecosystem) — but re-verify the `_NULL` bug repro and test
count if any commits land on `dsx/loader.py` or `tests/test_dsx.py` between this research and
planning.
