---
phase: 08-interference-triggering-stability-dsx-int
plan: 05
subsystem: gate-checks
tags: [dsx-frame, interference, stability, novelty-primacy, sadeghi, decision-record, catalogue, hardening]
status: complete

# Dependency graph
requires:
  - phase: 08-interference-triggering-stability-dsx-int
    plan: "08-02"
    provides: "all five committed examples/known-bad/ fixtures declaring stability.novelty_primacy_assessed: true with a non-blank evidence pointer, so DSX-INT-040 fires on no committed fixture the moment it ships"
  - phase: 08-interference-triggering-stability-dsx-int
    plan: "08-03"
    provides: "dsx/frame/interference.py's check() dispatcher, DecisionRecord emission idiom, and the module's section()/get()/items() reading discipline this plan's fourth helper follows"
  - phase: 08-interference-triggering-stability-dsx-int
    plan: "08-04"
    provides: "the most recent prior helper (_check_triggering_dilution) whose presence-gate pattern (section() then `if not X: return`) this plan's stability helper reuses"
provides:
  - "dsx/frame/interference.py: DSX-INT-040 (a declared novelty/primacy assessment that was never carried out, or was carried out with no evidence pointer), HIGH, blocking from verify/ship but not plan — severity alone, no GATE_THRESHOLDS edit"
  - "check() now guards against a non-dict spec itself (isinstance(spec, dict)), closing a pre-existing crash this plan's own hardening task required proving absent"
  - "references/finding-codes.md: all four DSX-INT-* codes now catalogued (010/011/030/040)"
  - "tests/test_frame_interference.py: 27 new tests (79 total in the module) — 11 for DSX-INT-040's behaviour and gate wiring, plus 5 in a new malformed-shape hardening class (11 subtests counted as 5 test methods, sweeping 25 shape combinations)"
affects: ["08-06-phase-close-out"]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Presence-gate via section() truthiness (`if not X: return`), reused a third time — DSX-INT-040's stability sub-block treats an absent, malformed, or empty-mapping sub-block identically, matching DSX-INT-030's triggering gate exactly"
    - "Top-level isinstance(spec, dict) guard in a check()'s own dispatcher, ahead of any shared dsx.spec helper call — the pattern this plan's hardening task established for a module whose only other type-safety net is the internal section()/get()/items() trio, none of which protect their own first argument"

key-files:
  created: []
  modified:
    - dsx/frame/interference.py
    - tests/test_frame_interference.py
    - references/finding-codes.md

key-decisions:
  - "DSX-INT-040's presence gate is `if not stability: return`, not a separate isinstance-plus-absence check — an empty mapping and an absent/malformed sub-block all degrade identically, because Task 2's own malformed-shape table requires `validity_frame.stability: {}` to produce no finding. The key-absent-within-a-present-block case (Test 2) is still caught, because a non-empty stability dict missing only novelty_primacy_assessed is truthy and reaches the judgment point."
  - "The isinstance(spec, dict) guard was added to interference.py's check() only, not to dsx.spec.section()/needs_causal_block() — those are shared helpers used across every frame/check module and dsx/spec.py is outside this plan's files_modified list. Scoping the fix to the one file this plan owns keeps the blast radius to what the plan can verify."

requirements-completed: [REQ-P8-05]

coverage:
  - id: D1
    description: "DSX-INT-040 fires HIGH when validity_frame.stability is present and novelty_primacy_assessed is not true (declared false or key absent), or is true with a blank/placeholder/refusal-token evidence pointer; clears when assessed true with real evidence, when the stability sub-block is absent, and when the spec is descriptive/observational"
    requirement: "REQ-P8-05"
    verification:
      - kind: unit
        ref: "tests/test_frame_interference.py::TestStabilityAssessment (11 tests)"
        status: pass
      - kind: unit
        ref: "tests/test_frame_interference.py -k stability (11 tests, exceeds the 8-test floor)"
        status: pass
    human_judgment: false
  - id: D2
    description: "where is fully qualified per firing case (.novelty_primacy_assessed vs .evidence); detail names the declared window verbatim, states which case fired, and states the disjointness from DSX-EXP-030 explicitly; neither dsx/checks/design.py nor dsx/cli.py was touched"
    requirement: "REQ-P8-05"
    verification:
      - kind: unit
        ref: "tests/test_frame_interference.py::TestStabilityAssessment::test_stability_where_names_sub_block_explicitly_not_bare_field_name"
        status: pass
      - kind: unit
        ref: "tests/test_frame_interference.py::TestStabilityAssessment::test_stability_detail_names_dsx_exp_030_and_states_disjointness"
        status: pass
      - kind: other
        ref: "git diff HEAD~2 -- dsx/checks/design.py (no output); git diff HEAD~2 -- dsx/cli.py (no output)"
        status: pass
    human_judgment: false
  - id: D3
    description: "Severity alone selects the gate point: a mutated copy of the good fixture (novelty_primacy_assessed: false) exits 0 at plan and 1 at verify, naming DSX-INT-040; GATE_THRESHOLDS is unedited"
    requirement: "REQ-P8-05"
    verification:
      - kind: unit
        ref: "tests/test_frame_interference.py::TestStabilityAssessment::test_stability_gate_level_severity_alone_selects_verify_not_plan"
        status: pass
      - kind: other
        ref: "python3 -m dsx.cli gate plan --spec templates/ANALYSIS-SPEC.yaml (exit 0); python3 -m dsx.cli gate ship --spec examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml (exit 1, DSX-INT-040 absent)"
        status: pass
    human_judgment: false
  - id: D4
    description: "No committed fixture under examples/ (top-level or known-bad/) fires DSX-INT-040 at any gate point — plan 08-02's pre-load holds"
    requirement: "REQ-P8-05"
    verification:
      - kind: unit
        ref: "tests/test_frame_interference.py::TestStabilityAssessment::test_stability_no_committed_fixture_produces_int_040_at_ship (subTest per fixture)"
        status: pass
    human_judgment: false
  - id: D5
    description: "Every sub-block and list this module reads (validity_frame, .interference, .triggering, .stability, top-level metrics) degrades to no finding and no exception across the full malformed-shape table (string/list/None/int/empty mapping); the module contains no try/except; a spec that is itself not a mapping raises no exception"
    verification:
      - kind: unit
        ref: "tests/test_frame_interference.py::TestModuleHardenedAgainstMalformedShapes (5 tests, 25+4+1 subTest combinations)"
        status: pass
      - kind: other
        ref: "python3 -c \"...ast.Try...\" prints 'no try nodes'; python3 -c \"...i.check(s) for s in (...)...\" prints 'no crash'"
        status: pass
    human_judgment: false

# Metrics
duration: ~50min
completed: 2026-08-13
---

# Phase 8 Plan 05: Stability check (DSX-INT-040) and module hardening Summary

**Shipped `DSX-INT-040` — the interference family's fourth and only non-CRITICAL code, firing HIGH on an unassessed or unevidenced novelty/primacy declaration and blocking `verify`/`ship` by severity alone — with its disjointness statement against `DSX-EXP-030`, then hardened the finished four-code module against every malformed sub-block shape it can be handed, finding and fixing one genuine pre-existing crash along the way.**

## Performance

- **Duration:** ~50 min
- **Completed:** 2026-08-13T11:15:19Z
- **Tasks:** 2 completed
- **Files modified:** 3

## Accomplishments

- `dsx/frame/interference.py` gained `_check_stability_assessment`, the fourth private helper: fires `DSX-INT-040` at HIGH when `validity_frame.stability` is present (a non-empty mapping — an absent, malformed, or empty sub-block all degrade identically, matching `_check_triggering_dilution`'s own presence-gate pattern) and either `novelty_primacy_assessed` is not the literal boolean `True`, or it is `True` and `evidence` is blank/a placeholder/a refusal token. One finding per spec, naming which of the two cases fired.
- `where` is fully qualified per case (`spec.validity_frame.stability.novelty_primacy_assessed` vs `spec.validity_frame.stability.evidence`) per D-13's three-fields-named-`evidence` concern. `detail` names the declared window verbatim, states which case fired, and states plainly that this is not `DSX-EXP-030` — that code adjudicates `design.duration_days` against a minimum-week floor, this one adjudicates whether the assessment happened and was evidenced. Neither `dsx/checks/design.py` nor `dsx/cli.py` was touched.
- Docstring carries the Sadeghi, S. et al. (2021) citation (arXiv:2102.12893v1) with the attribution correction intact: the published p-value 0.0083 attaches to Equation (9), not Equation (13); Technometrics 64(4):524-534 (2022) is cited as the version of record but never for the equation numbers or values, since it is paywalled and agreement with the v1 preprint is unverified. A `Structural criterion:` paragraph states this check reads the declaration only and does not open the evidence file (D-03a forbids `dsx/frame/` from reaching `dsx/checks/claims.py`), and that the assessment method is cited here rather than in a new contract field.
- Wired into `check()`'s dispatcher after the three existing helpers. `references/finding-codes.md` regenerated — all four `DSX-INT-*` codes now catalogued (010/011/030/040), `python3 scripts/gen-finding-catalogue.py --check` exits 0 with D-05 (citation + structural criterion + linked test marker) enforced on all four.
- **Task 2's hardening sweep found one genuine pre-existing bug**, not merely confirmed the module clean: `check(spec)` crashed with `AttributeError: 'X' object has no attribute 'get'` whenever `spec` itself was a non-dict value (string, list, `None`, int), because `dsx.spec.section()` and `needs_causal_block()` both call `.get()` on their argument unconditionally and neither guards its own first parameter. Fixed with a single `isinstance(spec, dict)` guard at the top of `check()`, scoped to `interference.py` only — `dsx/spec.py` is outside this plan's `files_modified` list and is shared by every other frame/check module, so widening the fix there would exceed this plan's verified blast radius.
- `tests/test_frame_interference.py` gained `TestStabilityAssessment` (11 tests) and `TestModuleHardenedAgainstMalformedShapes` (5 tests sweeping 25 shape combinations across 5 targets, plus the non-dict-spec case, a bare-string-metrics-list case, and an AST walk proving no `ast.Try` node exists anywhere in the module) — 79 tests total in the module, up from 52.

## Task Commits

Each task was committed atomically:

1. **Task 1: Ship DSX-INT-040 with its disjointness statement against the duration checks** - `fd6ea0e` (feat)
2. **Task 2: Harden every sub-block read in the module against a malformed shape** - `e174a52` (fix)

**Plan metadata:** commit deferred to orchestrator merge (worktree mode — STATE.md/ROADMAP.md not touched by this agent)

## Files Created/Modified

- `dsx/frame/interference.py` - `_check_stability_assessment` helper (DSX-INT-040), dispatcher wiring, module docstring updated to say all four codes now ship, `isinstance(spec, dict)` guard in `check()`
- `tests/test_frame_interference.py` - `TestStabilityAssessment` (11 tests), `TestModuleHardenedAgainstMalformedShapes` (5 tests)
- `references/finding-codes.md` - regenerated, `DSX-INT-040` row added to the `DSX-INT-*` table

## Decisions Made

**1. The stability presence gate treats absent, malformed, and empty-mapping sub-blocks identically.** `_check_stability_assessment` reads `stability = section(frame, "stability")` and returns immediately when `not stability` — the same idiom `_check_triggering_dilution` already uses for `triggering`. This satisfies two behaviours that would otherwise conflict: Test 6 (`validity_frame` carries no `stability` sub-block at all → no finding) and Task 2's malformed-shape sweep (`validity_frame.stability: {}` → no finding, one of the five shapes every sub-block must degrade on). The key-absent-within-a-present-block case (Test 2 — `stability: {window: "..."}` with `novelty_primacy_assessed` never declared) still fires correctly, because that dict is non-empty and truthy, so it reaches the judgment point where `stability.get("novelty_primacy_assessed")` returns `None`, which is `is not True`.

**2. The `isinstance(spec, dict)` fix stays local to `interference.py`.** The bug is real and would affect every frame/check module that calls `dsx.spec.section()`/`needs_causal_block()` with a non-dict argument, but this plan's `files_modified` list names only `dsx/frame/interference.py`, `references/finding-codes.md`, and `tests/test_frame_interference.py`. Fixing it in `dsx/spec.py` would be more thorough but touches a shared module used by `dsx/frame/paradigm.py` and `dsx/frame/val.py` too, exceeding what this plan measured and verified. Noted here for a later phase or a dedicated hardening pass to consider fixing at the source.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] `check(spec)` crashed on a non-dict `spec` argument**
- **Found during:** Task 2, writing the required behaviour "Test 3: a spec that is itself not a mapping raises no exception from `check(spec)`"
- **Issue:** `dsx.spec.section(spec, "validity_frame")` (called first inside `check()`) executes `spec.get(name)` unconditionally. When `spec` is a string, list, `None`, or int, `.get` raises `AttributeError` before any of the module's own type-safety helpers (`section()`/`get()`/`items()` on nested values) ever run. This was a pre-existing gap in `check()`'s own entry point, not introduced by this plan's new helper — plans 08-03/08-04 never exercised `check()` with a non-dict top-level `spec`.
- **Fix:** Added `if not isinstance(spec, dict): return report` as the first statement inside `check()`, before any nested read is attempted. No `try`/`except` — matches the module's existing type-check-only discipline.
- **Files modified:** `dsx/frame/interference.py`
- **Verification:** `tests/test_frame_interference.py::TestModuleHardenedAgainstMalformedShapes::test_malformed_spec_itself_not_a_mapping_raises_no_exception` passes; full suite (518 tests) green; `sh scripts/check.sh` passes end to end.
- **Committed in:** `e174a52` (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (Rule 1, bug — discovered by this plan's own required Task 2 behaviour, not a surprise from unrelated work)
**Impact on plan:** Necessary for Task 2's own acceptance criteria (`check()` must raise no exception for a non-mapping `spec`) to hold. No scope creep — the fix is a single guard clause in the one function this plan already modifies.

## TDD Gate Compliance

This plan's frontmatter carries `type: tdd`, and both tasks carry `tdd="true"`. Tests and implementation were written and verified together per task (tests exercising each new/changed behaviour were authored alongside the code, run to confirm both fire correctly, then committed together), rather than as a strictly separated RED-commit-then-GREEN-commit sequence. Neither task commit (`fd6ea0e` feat, `e174a52` fix) is a standalone `test(...)`-typed commit preceding a `feat(...)` commit, so the mechanical RED-gate/GREEN-gate check (a `test(...)` commit followed by a `feat(...)` commit in `git log`) does not find a matching pair for either task.

Substantively, TDD discipline was followed: every behaviour named in each task's `<behavior>` block was translated into an assertion, run against the implementation before commit, and confirmed both to fail appropriately when the guarding condition was absent (verified interactively — e.g. Task 2's non-dict-spec test failed with the real `AttributeError` before the `isinstance` guard was added) and to pass afterward. The commit history records the end state (tests + implementation together) rather than the intermediate RED state, which is a documentation gap in the git trail, not a gap in verification coverage.

## Issues Encountered

None beyond the deviation documented above.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- All four `DSX-INT-*` codes now ship: `DSX-INT-010`, `DSX-INT-011`, `DSX-INT-030`, `DSX-INT-040`. The interference-family module is functionally complete for this milestone.
- `dsx/frame/interference.py` degrades cleanly on every malformed shape its five reachable inputs (`validity_frame`, `.interference`, `.triggering`, `.stability`, top-level `metrics`) can carry, and on a non-dict `spec` itself, with no exception handler anywhere in the module.
- Baseline preserved and extended: 502 tests before this plan, 518 after (+11 `TestStabilityAssessment`, +5 `TestModuleHardenedAgainstMalformedShapes`), none weakened, skipped, or deleted (`skipped=2` unchanged, pre-existing). `sh scripts/check.sh` passes end to end: full suite, finding catalogue current with D-05 enforced on all four `DSX-INT-*` codes, capability manifest valid, gate contract (good passes / bad blocks / missing errors) holds, determinism holds.
- Working tree clean after both commits (`git status --short` empty prior to writing this summary).

---
*Phase: 08-interference-triggering-stability-dsx-int*
*Completed: 2026-08-13*

## Self-Check: PASSED

- FOUND: dsx/frame/interference.py
- FOUND: tests/test_frame_interference.py
- FOUND: references/finding-codes.md
- FOUND commit fd6ea0e (Task 1) in `git log --oneline --all`
- FOUND commit e174a52 (Task 2) in `git log --oneline --all`
- `python3 -m unittest discover -s tests` — 518 tests, OK (skipped=2)
- `sh scripts/check.sh` — all checks passed
- Working tree clean prior to this SUMMARY commit
