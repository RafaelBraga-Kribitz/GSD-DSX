---
phase: 11-frequentist-admissibility-adjudicator-dsx-adm
plan: 07
subsystem: infra
tags: [dsx, admissibility, gate, cli, frequentist, python]

# Dependency graph
requires:
  - phase: 11-06
    provides: "dsx/frame/admissibility.py's check(spec, *, applies_to_frame), admissible_families(spec), DSX-ADM-010/DSX-ADM-020"
  - phase: 11-03
    provides: "dsx/frame/paradigm.py::applies_to_frequentist_admissibility(spec) — the frequentist-only scoping predicate"
provides:
  - "CHECKS[\"admissibility\"] registered in dsx/cli.py, mapped to admissibility.check"
  - "\"admissibility\" in GATE_PROFILES at plan, verify and ship; absent from execute"
  - "run_checks's dedicated admissibility branch, computing the D-22 scoping boolean via paradigm.applies_to_frequentist_admissibility and passing it in as a plain parameter"
  - "dsx recommend-test --spec/--phase-dir, adding an additive admissibility key to its JSON output only when explicitly given"
  - "TestAdmissibilityGateRegistration, TestAdmissibilityRecommendComposition and TestAdmissibilityCorpusRegression in tests/test_dsx.py — 21 new tests pinning registration, composition and the whole committed corpus"
affects: [11.1, 11.2, 11.3, 12]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A frame-layer check that needs a paradigm-scoped boolean gets a dedicated run_checks elif branch (beside prereg's), computing the boolean inline from dsx/frame/paradigm.py and passing it as a keyword argument — never hoisted alongside strict/reconcile_trail, and never read inside the check module itself (D-11/D-22)."
    - "A CLI subcommand that never blocks gets exactly the flags its contract needs, not add_common(...)'s full set — dsx recommend-test gained --spec/--phase-dir but not --block-on, matching the reasoning already recorded for `explain`."
    - "Additive CLI composition proven by subprocess byte-diff, not by a key-list assertion alone — a key-list check would pass even if auto-discovery had been left in; only comparing stdout across two working directories proves independence."

key-files:
  created: []
  modified:
    - dsx/cli.py
    - tests/test_dsx.py

key-decisions:
  - "Blocking gate output goes to stderr, not stdout (dsx.findings.emit's existing stream-by-verdict routing) — a test bug caught during task 1's GREEN run, fixed in the same session (478ec71) rather than carried forward."
  - "str(Path(...)) renders with backslashes on Windows, so the missing-spec exit-2 test (task 2) asserts on the filename and \"not found\" rather than the forward-slash path string — a portability fix, not a behavior change."
  - "CHECKS[\"admissibility\"] is appended after prereg rather than resorted alphabetically into the whole dict — the plan's alphabetical instruction applies to the frame import line only (`from .frame import admissibility, interference, paradigm, prereg, val`), which is alphabetical; CHECKS itself is not alphabetically ordered anywhere else in the file."

requirements-completed: [REQ-P11-04, REQ-P11-05]

coverage:
  - id: D1
    description: "admissibility is registered in CHECKS and GATE_PROFILES at plan, verify and ship, absent from execute; run_checks computes the D-22 scoping boolean via dsx/frame/paradigm.py and passes it in, never re-deriving it inside the adjudicator"
    requirement: "REQ-P11-04"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py#TestAdmissibilityGateRegistration"
        status: pass
    human_judgment: false
  - id: D2
    description: "A deliberately underdetermined frame (blank estimand.type) exits 1 at dsx gate plan with DSX-ADM-020 among its CRITICAL findings via the ordinary emit path; an honest Bayesian declaration draws no DSX-ADM-* finding at plan, verify or ship"
    requirement: "REQ-P11-04"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py#TestAdmissibilityGateRegistration.test_blank_estimand_type_exits_1_at_gate_plan_with_dsx_adm_020_critical"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py#TestAdmissibilityGateRegistration.test_bayesian_declaration_draws_no_dsx_adm_finding_at_plan_verify_or_ship"
        status: pass
    human_judgment: false
  - id: D3
    description: "dsx recommend-test with no --spec/--phase-dir is byte-identical to v1.5.0 regardless of working directory; with --spec it gains exactly one additive admissibility key with the four original values unchanged; a named missing --spec exits 2"
    requirement: "REQ-P11-05"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py#TestAdmissibilityRecommendComposition"
        status: pass
    human_judgment: false
  - id: D4
    description: "recommend_test() in dsx/checks/stats.py is not moved, wrapped or edited, and dsx/checks/stats.py imports nothing from dsx.frame"
    requirement: "REQ-P11-05"
    verification:
      - kind: unit
        ref: "tests/test_frame_boundary.py (full module, reverse-direction scanner)"
        status: pass
      - kind: other
        ref: "git diff --stat dsx/checks/stats.py (empty)"
        status: pass
    human_judgment: false
  - id: D5
    description: "Every committed spec's dsx gate exit code at plan/execute/verify/ship is unchanged from before this plan; tests/test_known_bad_corpus.py is not edited; no known-bad fixture draws any DSX-ADM-* finding"
    requirement: "REQ-P11-04"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py#TestAdmissibilityCorpusRegression"
        status: pass
      - kind: unit
        ref: "tests/test_known_bad_corpus.py (full module, 30 tests)"
        status: pass
      - kind: other
        ref: "git diff --stat tests/test_known_bad_corpus.py (empty)"
        status: pass
    human_judgment: false

duration: ~8min (commit span; TDD implementation across 3 tasks, 6 commits)
completed: 2026-08-22
status: complete
---

# Phase 11 Plan 07: Wire the Adjudicator Into the Gate and Into `dsx recommend-test` Summary

**`CHECKS["admissibility"]` and `GATE_PROFILES["plan"/"verify"/"ship"]` now reach `dsx/frame/admissibility.py::check()`, routed by a scoping boolean `run_checks` computes from `dsx/frame/paradigm.py` and never by the adjudicator itself; `dsx recommend-test` gained an additive `admissibility` key behind an explicit `--spec`/`--phase-dir` flag, with v1.5.0's no-flag output proven byte-identical across working directories by subprocess diff.**

## Performance

- **Duration:** ~8 min commit-to-commit (plus a longer context-reading phase across the plan, the 11-06 summary, `dsx/cli.py`, `dsx/frame/admissibility.py`, `dsx/frame/paradigm.py`, `references/families.yaml`, the committed corpus fixtures, and `tests/test_dsx.py`'s existing conventions before the first edit)
- **Tasks:** 3
- **Files modified:** 2 (`dsx/cli.py`, `tests/test_dsx.py`)

## Accomplishments

- `CHECKS["admissibility"]` maps to `admissibility.check`, registered for discoverability the same way `design` and `prereg` already are, even though the dedicated `elif name == "admissibility":` branch in `run_checks` always intercepts it before the generic `elif name in CHECKS:` dispatch reaches it.
- `"admissibility"` is appended to `GATE_PROFILES["plan"]`, `["verify"]` and `["ship"]`, and left out of `["execute"]` — an underdetermined frame is a planning-time defect an analyst can fix before touching data, and there is nothing about a run in progress for this family to adjudicate, the same reasoning already recorded for `prereg`'s asymmetric registration.
- `run_checks` gained a new `elif name == "admissibility":` branch, placed beside the existing `prereg` branch and before the generic dispatch, calling `admissibility.check(spec, applies_to_frame=paradigm.applies_to_frequentist_admissibility(spec))`. The boolean is computed inside the branch — never hoisted alongside `strict`/`reconcile_trail` — so the call is paid only when the check actually runs and the helper and its consumer stay on adjacent lines. `dsx/frame/admissibility.py` itself never reads `inference.paradigm`; the D-11 boundary scanner (`tests/test_frame_boundary.py`) still passes 10/10 with the reverse-direction check confirming this.
- `p_rec` (the `recommend-test` argparse subparser) gained exactly `--spec` and `--phase-dir` — not `add_common(...)`'s full flag set, since `--block-on` on a command that never blocks would be a lie in the help text (the same reasoning already recorded for `explain`, D-04).
- `cmd_recommend` copies `recommend_test()`'s four-key result into a new dict, preserving insertion order, and adds one additive `"admissibility"` key from `admissible_families(spec)` only when `--spec` or `--phase-dir` is explicitly given. `find_spec(None, None)` is never called — auto-discovery would make the no-flag output depend on the operator's working directory, which the byte-identity requirement (REQ-P11-05) forbids. A named-but-missing `--spec` path propagates `CheckError` to the existing top-level handler, exiting 2.
- Swept the whole committed corpus directly against `dsx/frame/admissibility.py::check()`: `examples/bad-ANALYSIS-SPEC.yaml` is the single spec that draws `DSX-ADM-020` (it declares no `validity_frame.dependence.structure` at all — the blank-axis refusal cause), and every other committed spec (good, template, and all seven `examples/known-bad/*` fixtures) draws nothing. No known-bad corpus exit code moved and `tests/test_known_bad_corpus.py` is untouched (`git diff --stat` empty, 30/30 green throughout).
- Added 21 new tests across three classes in `tests/test_dsx.py`: `TestAdmissibilityGateRegistration` (8), `TestAdmissibilityRecommendComposition` (5), `TestAdmissibilityCorpusRegression` (8) — the last discovers every committed spec by globbing (`examples/*-ANALYSIS-SPEC.yaml`, `examples/known-bad/*-ANALYSIS-SPEC.yaml`, `templates/ANALYSIS-SPEC.yaml`), never nine hard-coded paths, so a tenth committed spec inherits every assertion automatically.

## Task Commits

Task 1 and Task 2 followed a RED → GREEN TDD cycle; Task 3 adds no production code (the behavior it pins already shipped in Task 1), so it has a single commit.

1. **Task 1: Register admissibility in CHECKS, GATE_PROFILES and run_checks**
   - `1623645` (test) — 8 tests added; 4 fail/error against the unregistered check, confirming RED
   - `36331f6` (feat) — import, `CHECKS` entry, three `GATE_PROFILES` entries, the `run_checks` branch; all 8 pass
   - `478ec71` (fix) — corrected a test bug found during GREEN: blocking JSON goes to stderr, not stdout
2. **Task 2: Extend `dsx recommend-test` by composition, additively**
   - `88945d4` (test) — 5 tests added; 2 fail against the unextended parser, confirming RED
   - `edad96b` (feat) — `--spec`/`--phase-dir` on `p_rec`, additive `admissibility` key in `cmd_recommend`; all 5 pass after a Windows path-separator test fix folded into the same commit
3. **Task 3: A durable corpus regression test for the registered check**
   - `71e8b0c` (test) — 8 tests added, all pass immediately (no new behavior to make pass)

**Plan metadata:** this commit (docs: complete plan), made by the worktree executor before returning to the orchestrator.

## Files Created/Modified

- `dsx/cli.py` — `admissibility` added to the frame import line; `CHECKS["admissibility"]`; three `GATE_PROFILES` entries plus an explanatory comment paragraph; a new `run_checks` dispatch branch; `--spec`/`--phase-dir` on `p_rec`; `cmd_recommend` extended by flat dictionary merge.
- `tests/test_dsx.py` — three new test classes (`TestAdmissibilityGateRegistration`, `TestAdmissibilityRecommendComposition`, `TestAdmissibilityCorpusRegression`), 21 tests total, appended before `if __name__ == "__main__":`.

## Decisions Made

- Blocking gate output routes to stderr, not stdout, per `dsx.findings.emit`'s existing verdict-based stream selection — this is pre-existing behavior, not something this plan changed, but it was the source of a test bug caught and fixed during Task 1's GREEN run (`478ec71`).
- `str(Path(...))` renders with backslashes on this Windows worktree; the missing-spec exit-2 test in Task 2 was written to match on the filename and "not found" rather than a forward-slash path literal, so it holds on both platforms.
- `CHECKS["admissibility"]` was appended after `prereg` rather than resorted into strict alphabetical order across the whole dict — the plan's "keep it alphabetical" instruction names the frame import line specifically, which is alphabetical; `CHECKS`'s own key order carries no such constraint elsewhere in the file.

## Deviations from Plan

None — the plan's three tasks were executed as written, in the order written, with the exact registration points, branch placement, flag set and additive-composition shape the plan specified. Both orchestrator-flagged risk areas were explicitly checked and hold:

- **Known-bad corpus fixture exit codes.** Registering `admissibility` in `GATE_PROFILES["plan"/"verify"/"ship"]` did not move any fixture's exit code. Direct sweep of `dsx/frame/admissibility.py::check()` against every committed spec confirms `examples/bad-ANALYSIS-SPEC.yaml` is the only one drawing `DSX-ADM-020` (blank `validity_frame.dependence.structure` — a pre-existing gap in that fixture, not something this plan's registration revealed as new). `tests/test_known_bad_corpus.py` was not edited (`git diff --stat` empty) and its 30 tests stayed green throughout all three tasks.
- **`gen-finding-catalogue.py --check` warning count.** Confirmed 7 pre-existing "declared twice with different text" warnings (`DSX-COH-030`, `DSX-PAR-002`, `DSX-SPEC-070` x3, `DSX-VAL-021`, `DSX-VAL-060`), unchanged by this plan's work — matching the orchestrator's pre-execution note (7, not 4) rather than the plan's own header prose. `--check` exits 0 either way; not a regression.

## Issues Encountered

None beyond the two test-authoring bugs documented in "Decisions Made" above, both caught and fixed within the same TDD cycle that introduced them.

## Next Phase Readiness

- The frequentist admissibility adjudicator is now live end to end: registered, scoped by paradigm, reachable from `dsx gate plan/verify/ship`, `dsx check`, `dsx audit`, and `dsx recommend-test --spec`.
- Plan 11-08 (concurrent, disjoint scope — `scripts/gen-finding-catalogue.py`, `tests/test_gen_finding_catalogue.py`) is unaffected by this plan's changes; neither plan touched the other's files.
- No blockers for the remainder of Phase 11 or for Phases 11.1–11.3/12.

## Self-Check: PASSED

- `dsx/cli.py` contains `from .frame import admissibility, interference, paradigm, prereg, val` — FOUND
- `dsx/cli.py` contains `"admissibility": admissibility.check` — FOUND
- `dsx/cli.py` contains `applies_to_frequentist_admissibility` — FOUND
- `dsx/cli.py` contains `p_rec.add_argument("--spec"` and `p_rec.add_argument("--phase-dir"` — FOUND
- `.planning/phases/11-frequentist-admissibility-adjudicator-dsx-adm/11-07-SUMMARY.md` — FOUND
- Commits `1623645`, `36331f6`, `478ec71`, `88945d4`, `edad96b`, `71e8b0c` — all FOUND in `git log --oneline`

---
*Phase: 11-frequentist-admissibility-adjudicator-dsx-adm*
*Completed: 2026-08-22*
