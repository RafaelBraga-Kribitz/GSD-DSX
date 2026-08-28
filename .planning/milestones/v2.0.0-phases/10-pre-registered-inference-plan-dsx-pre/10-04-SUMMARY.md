---
phase: 10-pre-registered-inference-plan-dsx-pre
plan: 04
subsystem: testing
tags: [gate-profiles, cli, registration, decision-trail, dsx-frame]

# Dependency graph
requires:
  - phase: 10-pre-registered-inference-plan-dsx-pre (plan 02)
    provides: "check(spec, root=None, *, reconcile_trail=False) dispatcher, DSX-PRE-010/DSX-PRE-030, all five D-13 guards flipped"
  - phase: 10-pre-registered-inference-plan-dsx-pre (plan 03)
    provides: "_recorded_plan_digests(root), _check_content_lock(spec, root, report), DSX-PRE-020, check() already gates _check_content_lock behind reconcile_trail"
provides:
  - "dsx/cli.py: CHECKS[\"prereg\"] = prereg.check; GATE_PROFILES[\"verify\"] and [\"ship\"] both carry \"prereg\", absent from \"plan\" and \"execute\""
  - "run_checks(..., gate_invocation: bool = False) — reconcile_trail = gate_invocation and gate_point in {\"verify\", \"ship\"}, computed beside the existing strict predicate and passed into prereg.check(spec, root, reconcile_trail=reconcile_trail) via a named elif branch"
  - "cmd_gate is the only run_checks caller passing gate_invocation=True; validate/check/audit keep the default False"
  - "_write_decision_trail's docstring narrowed: the write path stays an unconditional side channel, the plan-time header it writes is now a read-side gate input at verify/ship via prereg"
  - "tests/_trail_seed.py::seed_plan_header(root, spec_path) — writes a real InvocationHeader(gate_point=\"plan\") via the real decisions.py primitives, importable by any test module"
  - "5 pre-existing test call sites repaired to seed a plan-time header before reaching verify/ship in a root with no prior plan run (test_known_bad_corpus.py::_gate_findings, plus one site each in test_dsx.py x3, test_frame_interference.py, test_frame_val.py)"
  - "tests/test_frame_prereg.py::TestGateRegistration (4 tests) and TestAdHocCommandScope (6 tests) — ROADMAP Success Criterion 5's registration/reachability pair, and the gate-invocation-vs-read-only-inspection boundary, both pinned by test"
affects: [10-05-dsx-pre, 10-06-dsx-pre]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A shared, underscore-prefixed test helper module (tests/_trail_seed.py) outside unittest discover's test*.py pattern, importable by any test module needing to seed gate state — first instance of this pattern in the suite"
    - "Test modules importing the shared helper insert both ROOT (repo root) and ROOT / \"tests\" onto sys.path, because the module is executed under two different import identities depending on invocation (`python -m unittest discover -s tests` vs `python -m unittest tests.test_x`), and only the discover form puts tests/ itself on sys.path automatically"
    - "A synthetic test spec for an ad-hoc-command test is built by cloning examples/good-ANALYSIS-SPEC.yaml and dict-merging one block override, never a minimal hand-built dict — avoids every other check crashing or blocking on unrelated missing fields when only one code's behavior is under test"

key-files:
  created:
    - tests/_trail_seed.py
  modified:
    - dsx/cli.py
    - tests/test_known_bad_corpus.py
    - tests/test_dsx.py
    - tests/test_frame_interference.py
    - tests/test_frame_val.py
    - tests/test_frame_prereg.py

key-decisions:
  - "reconcile_trail is computed inside run_checks (dsx/cli.py), not inside prereg.check, mirroring where `strict` already lives — keeps the CLI-level policy of *when* a caller opts into trail reconciliation in one place, beside the strictness policy it parallels."
  - "gate_invocation=True is set only in cmd_gate. validate/check/audit are left at the default False, which is what makes prereg's trail-independent half (rule resolution, procedure reconciliation) run everywhere while the trail-dependent half (_check_content_lock) runs only for a real dsx gate verify/ship call — proved by TestAdHocCommandScope tests 1-5."
  - "The five call sites needing an explicit seed were found by direct read (per the plan's named list) plus one additional site (test_dsx.py::TestPhase9ParadigmJustification.test_good_fixture_never_fires_dsx_par_002_at_any_gate_point) surfaced only by actually running the full suite after wiring the registration — confirming the plan's own caveat that its named list was 'not asserted to be exhaustive'."
  - "scripts/check.sh's four-gate-point loop and test_dsx.py's test_good_fixture_passes_every_gate needed no change: both already run plan before verify/ship against the same shared root (examples/), so the set-membership precondition from plan 03 is satisfied by the earlier plan run in the same test process — matching the plan's explicit self-seeding exemption."
  - "TestAdHocCommandScope's synthetic spec is the good fixture cloned via json.dumps with one block-level override (analysis.test for test 5), never a minimal hand-built dict — cmd_audit passes gate_point=\"ship\" to run_checks internally (existing behaviour, unrelated to this plan), which makes repro.check run in strict mode even under `dsx audit`; a minimal spec risked crashing on an unrelated missing field before DSX-PRE-030 was ever reached."

patterns-established:
  - "GATE_PROFILES carries a comment (parallel to the existing paradigm note) documenting that prereg is the first family whose registered gate points diverge from the historical shape — verify/ship only, no plan/execute — and naming registration as the knob that keeps it off those two points, with severity as a separate, independent knob."

requirements-completed: [REQ-P10-02, REQ-P10-03]

coverage:
  - id: D1
    description: "prereg is registered in CHECKS and in GATE_PROFILES[\"verify\"]/[\"ship\"] only, threaded a project root through a named elif branch in run_checks (following the dq/code precedent), and reconciles the decision trail only when gate_invocation=True and the gate point is verify or ship — cmd_gate is the only caller passing gate_invocation=True."
    requirement: "REQ-P10-02"
    verification:
      - kind: unit
        ref: "tests/test_frame_prereg.py#TestGateRegistration::test_prereg_registered_in_verify_ship_absent_from_plan_and_execute"
        status: pass
      - kind: unit
        ref: "tests/test_frame_prereg.py#TestAdHocCommandScope::test_1_dsx_audit_in_a_trail_free_directory_exits_without_check_error"
        status: pass
      - kind: unit
        ref: "tests/test_frame_prereg.py#TestAdHocCommandScope::test_3_dsx_gate_verify_in_the_same_trail_free_directory_exits_2_naming_suppressions"
        status: pass
      - kind: unit
        ref: "tests/test_frame_prereg.py#TestAdHocCommandScope::test_6_after_seeding_a_plan_header_dsx_gate_verify_no_longer_exits_2"
        status: pass
    human_judgment: false
  - id: D2
    description: "Every DSX-PRE-* code (DSX-PRE-010, DSX-PRE-020, DSX-PRE-030) is reachable from a gate profile, the known code set is pinned to exactly those three (DSX-PRE-011 deliberately unspent), and every DSX-PRE-* finding this module can emit is CRITICAL, driven through the three real firing scenarios."
    requirement: "REQ-P10-03"
    verification:
      - kind: unit
        ref: "tests/test_frame_prereg.py#TestGateRegistration::test_every_dsx_pre_code_reachable_from_a_gate_profile"
        status: pass
      - kind: unit
        ref: "tests/test_frame_prereg.py#TestGateRegistration::test_known_dsx_pre_codes_are_exactly_010_020_030"
        status: pass
      - kind: unit
        ref: "tests/test_frame_prereg.py#TestGateRegistration::test_every_dsx_pre_finding_this_module_can_emit_is_critical"
        status: pass
    human_judgment: false
  - id: D3
    description: "Registering prereg's blast radius (every existing test reaching verify/ship without a prior plan run in the same root) is fully absorbed in the same commit as the GATE_PROFILES edit: _gate_findings seeds a plan header for verify/ship calls and guards json.loads so an exit-2 CheckError surfaces as a readable assertion, and five further call sites across three other test modules are repaired. Full suite green at 621/621 (up from 611 at fork), sh scripts/check.sh passes, no assertion weakened, no DSX-PRE-* code added to the incidental-gap allow-list."
    verification:
      - kind: unit
        ref: "python -m unittest discover -s tests -q"
        status: pass
      - kind: other
        ref: "sh scripts/check.sh"
        status: pass
      - kind: other
        ref: "python scripts/gen-finding-catalogue.py --check"
        status: pass
      - kind: other
        ref: "git show --stat f41e6bd (lists both dsx/cli.py and tests/test_known_bad_corpus.py)"
        status: pass
    human_judgment: false

# Metrics
duration: ~13min
completed: 2026-08-20
status: complete
---

# Phase 10 Plan 04: Register prereg at verify/ship and absorb the blast radius Summary

**`prereg` is live in `GATE_PROFILES["verify"]`/`["ship"]` with the project root threaded through a named `run_checks` branch, gated on a `gate_invocation` discriminator that scopes trail reconciliation to real `dsx gate` runs alone — and every one of the six pre-existing call sites this registration would otherwise break (found by direct read plus one more found only by running the suite) now seeds a plan-time header instead of depending on test order.**

## Performance

- **Duration:** ~13 min
- **Started:** 2026-08-20T03:17:05+02:00 (fork base commit)
- **Completed:** 2026-08-20T03:30:13+02:00
- **Tasks:** 3
- **Files modified:** 7 (1 created: `tests/_trail_seed.py`; 6 modified: `dsx/cli.py`, `tests/test_known_bad_corpus.py`, `tests/test_dsx.py`, `tests/test_frame_interference.py`, `tests/test_frame_val.py`, `tests/test_frame_prereg.py`)

## Accomplishments

- `dsx/cli.py`: `CHECKS["prereg"] = prereg.check`; `GATE_PROFILES["verify"]`/`["ship"]` both append `"prereg"`, `"plan"`/`"execute"` untouched; a new comment above `GATE_PROFILES` names `prereg` as the first family whose registered points diverge from the historical shape, and states registration and severity are separate knobs.
- `run_checks` gains `gate_invocation: bool = False`, documented in its docstring in one sentence. Immediately after the existing `strict = gate_point in {"verify", "ship"}` line, `reconcile_trail = gate_invocation and gate_point in {"verify", "ship"}` is computed the same way. A new elif branch, placed after the `decision` branch and before the generic `CHECKS[name](spec)` fallback, calls `prereg.check(spec, root, reconcile_trail=reconcile_trail)` — following the `dq`/`code` shape for the positional root argument.
- `cmd_gate` is the only `run_checks` caller passing `gate_invocation=True`; `cmd_validate`, `cmd_check`, `cmd_audit` all keep the default `False`.
- `_write_decision_trail`'s docstring narrowed: the write path remains an unconditional side channel that can never itself change an exit code, and a new paragraph states the plan-time header it writes is now, from Phase 10, a read-side gate input at verify/ship via `prereg`, naming why the two statements are compatible (opposite directions of the same file).
- `tests/_trail_seed.py` created: `seed_plan_header(root, spec_path)` loads the spec with the real `dsx.loader.load`, computes the real `dsx.decisions.frame_digest`, and appends a real `InvocationHeader(gate_point="plan")` via the real `dsx.decisions.append` — so the header it writes is byte-for-byte what a genuine `dsx gate plan` run would write. Underscore-prefixed to stay outside `unittest discover`'s `test*.py` pattern.
- `tests/test_known_bad_corpus.py::_gate_findings` seeds a plan-time header before any `verify`/`ship` call and guards `json.loads(raw)` so a plain-text exit-2 `CheckError` surfaces as a readable `AssertionError` naming the raw text, never an opaque `JSONDecodeError`.
- Six pre-existing call sites repaired to seed a plan-time header (the plan's four named sites, plus `test_frame_val.py`'s `test_strong_informative_priors_spec_blocks_gate_verify_and_gate_ship_naming_val_041`, plus one more — `test_dsx.py`'s `test_good_fixture_never_fires_dsx_par_002_at_any_gate_point` — found only by running the full suite after wiring the registration, exactly the "not asserted to be exhaustive" caveat the plan named).
- `tests/test_frame_prereg.py` gains `TestGateRegistration` (4 tests: registration presence/absence per point, code reachability, the exactly-three-codes pin, and the all-CRITICAL severity proof) and `TestAdHocCommandScope` (6 tests: `audit`/`check` never require a trail, a real `gate verify`/`ship` still exits 2 naming `suppressions` in the same trail-free directory, the trail-independent half still runs under `audit`, and seeding clears the block).

## Task Commits

Each task was committed atomically:

1. **Task 1: Register prereg, thread the root, and repair every call site registration breaks** - `f41e6bd` (feat)
2. **Task 2: Registration and reachability, the pair Success Criterion 5 requires** - `877454e` (test)
3. **Task 3: Pin what the read-only inspection commands do and do not reconcile** - `75d3436` (test)

_No TDD RED/GREEN split — `tdd="true"` tasks (2, 3) were implemented with behavior and tests landing together per task, verified green before commit, matching the pattern established in plans 01-03._

## Files Created/Modified

- `dsx/cli.py` - `CHECKS["prereg"]`, `GATE_PROFILES["verify"]`/`["ship"]` registration, `run_checks(gate_invocation=...)`, the `prereg` elif branch, `cmd_gate` passes `gate_invocation=True`, `_write_decision_trail` docstring narrowed
- `tests/_trail_seed.py` - New shared helper: `seed_plan_header(root, spec_path)`
- `tests/test_known_bad_corpus.py` - `_gate_findings` seeds a plan header for verify/ship, guards `json.loads`
- `tests/test_dsx.py` - Three sites seeded (`test_bad_fixture_blocks_at_ship`, `test_template_validates_structurally_as_a_scaffold`, `test_missing_entrypoint_blocks_when_phase_dir_given`) plus one more found by running the suite (`test_good_fixture_never_fires_dsx_par_002_at_any_gate_point`)
- `tests/test_frame_interference.py` - One site seeded (`test_good_fixture_clears_ship_resolving_sibling_artifacts_from_its_own_directory`)
- `tests/test_frame_val.py` - One site seeded (`test_strong_informative_priors_spec_blocks_gate_verify_and_gate_ship_naming_val_041`)
- `tests/test_frame_prereg.py` - Two new test classes (`TestGateRegistration`, `TestAdHocCommandScope`), 10 tests total

## Decisions Made

- **`reconcile_trail` is computed inside `run_checks`, not inside `prereg.check`**, mirroring exactly where the pre-existing `strict` predicate already lives — the CLI-level policy of *when* a caller opts into trail reconciliation stays in one place, beside the strictness policy it parallels, rather than duplicated or pushed down into the check module.
- **Only `cmd_gate` passes `gate_invocation=True`.** `validate`, `check`, `audit` all keep the default `False`, which is what makes `prereg`'s trail-independent half (rule resolution, procedure reconciliation) run everywhere those commands run it, while the trail-dependent half (`_check_content_lock`) runs only for a real `dsx gate verify`/`ship` call — proved directly by `TestAdHocCommandScope` tests 1-5, not merely asserted in prose.
- **The five call sites the plan named were not exhaustive, confirmed empirically.** Running `python -m unittest discover -s tests -q` after wiring the registration surfaced one more failure beyond the plan's named list: `test_dsx.py::TestPhase9ParadigmJustification::test_good_fixture_never_fires_dsx_par_002_at_any_gate_point`, which loops all four gate points against a fresh `tempfile.TemporaryDirectory()` per point (never self-seeding, unlike the loops the plan explicitly exempted). Repaired the same way as the plan's named sites — seed before `verify`/`ship` only.
- **`scripts/check.sh`'s loop and `test_dsx.py::test_good_fixture_passes_every_gate` needed no change**, confirmed by direct read and by the green `sh scripts/check.sh` run: both already run `plan` before `verify`/`ship` against the same shared root (`examples/`), so plan 03's set-membership rule is satisfied by the earlier `plan` invocation in the same process — exactly the plan's stated self-seeding exemption, not a gap.
- **`TestAdHocCommandScope`'s synthetic spec clones the good fixture and overrides one block**, rather than a minimal hand-built dict. `cmd_audit` passes `gate_point="ship"` internally to `run_checks` (pre-existing behaviour, unrelated to this plan), which puts `repro.check` into strict mode even under a bare `dsx audit` call; a minimal spec risked an unrelated crash before `DSX-PRE-030` was ever reached in test 5.
- **Test modules importing `_trail_seed` insert both the repo root and `tests/` itself onto `sys.path`.** The helper is executed under two different import identities depending on invocation shape (`python -m unittest discover -s tests` puts `tests/` on `sys.path[0]` automatically; `python -m unittest tests.test_x` does not), confirmed by a failing import (`ModuleNotFoundError: No module named '_trail_seed'`) under the second invocation shape before this fix.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] `tests/_trail_seed.py` import failed under `python -m unittest tests.<module>` invocation**
- **Found during:** Task 1, immediately after adding `from _trail_seed import seed_plan_header` to `tests/test_known_bad_corpus.py`
- **Issue:** The plan's own acceptance criterion (`python -m unittest tests.test_known_bad_corpus -v` exits 0) runs the module under an import identity (`tests.test_known_bad_corpus`) where `tests/` itself is not automatically on `sys.path` — only the repo root is, via the existing `sys.path.insert(0, str(ROOT))` line. A plain top-level `from _trail_seed import ...` therefore raised `ModuleNotFoundError`.
- **Fix:** Added a second `sys.path.insert(0, str(ROOT / "tests"))` line before the `_trail_seed` import in every module that imports it (`test_known_bad_corpus.py`, `test_dsx.py`, `test_frame_interference.py`, `test_frame_val.py`, `test_frame_prereg.py`).
- **Files modified:** the same five test modules listed above
- **Verification:** `python -m unittest tests.test_known_bad_corpus -v` (and the equivalent for each other module) now imports and runs cleanly
- **Committed in:** `f41e6bd` (Task 1) and `877454e`/`75d3436` (Task 2/3, for `test_frame_prereg.py`'s own import)

**2. [Rule 1 - Bug] One additional pre-existing call site broke beyond the plan's named list**
- **Found during:** Task 1, after wiring the registration and running the full suite
- **Issue:** `test_dsx.py::TestPhase9ParadigmJustification::test_good_fixture_never_fires_dsx_par_002_at_any_gate_point` loops all four gate points against a fresh, non-self-seeding temporary directory per point, and failed with `JSONDecodeError` at `verify`/`ship` once `prereg` was registered — the same failure mode as the plan's four named sites, just not named by the plan's own direct-read list.
- **Fix:** Seed a plan-time header into the loop's temporary directory before the `verify`/`ship` iterations only (`plan`/`execute` need no seed).
- **Files modified:** `tests/test_dsx.py`
- **Verification:** `python -m unittest tests.test_dsx -q` — 295/295 pass; full suite 621/621
- **Committed in:** `f41e6bd` (Task 1)

---

**Total deviations:** 2 auto-fixed (1 bug in the new helper's import portability, 1 bug in an additional call site the plan's direct-read list missed). Both are exactly the class of discovery the plan's own text anticipated ("not asserted to be exhaustive... repair whatever else is red by the same mechanism") and neither weakens any assertion or adds a `DSX-PRE-*` code to `_INCIDENTAL_GAP_CODES`.
**Impact on plan:** Both auto-fixes are mechanical extensions of the plan's own named pattern (seed a header; fix a portability bug in shared test infrastructure). No scope creep, no architectural change.

## Issues Encountered

None beyond the two auto-fixed items above, both resolved on the first iteration.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `prereg` is fully live in `GATE_PROFILES["verify"]`/`["ship"]`, the project root is threaded through, and trail reconciliation is scoped to real `dsx gate` invocations only — plans 05 and 06 (fixture pair, README/brief citations) build on a registration that is now proven by test, not merely wired.
- ROADMAP Success Criterion 5's second clause (every code reachable from a gate profile) is satisfied by test for the `DSX-PRE-*` family, matching the pattern already established for `DSX-INT-*`/`DSX-VAL-*`.
- Full suite green at 621/621 (up from 611 at this plan's fork point — 10 new tests: 4 in `TestGateRegistration`, 6 in `TestAdHocCommandScope`), `sh scripts/check.sh` passes printing `all checks passed`, `python scripts/gen-finding-catalogue.py --check` exits 0 (only the three pre-existing, not-mine-to-fix `DSX-VAL-021`/`DSX-VAL-060`/`DSX-COH-030` etc. double-declaration warnings remain, per this plan's prior-wave context).
- No blockers. `tests/_trail_seed.py` is now available for plan 05's fixture-pair work if it needs to seed a plan-time header for a new corpus fixture's gate-level test.

## Self-Check: PASSED

- FOUND: dsx/cli.py (CHECKS["prereg"], GATE_PROFILES registration, gate_invocation, elif branch, cmd_gate wiring, docstring narrowing)
- FOUND: tests/_trail_seed.py (seed_plan_header)
- FOUND: tests/test_known_bad_corpus.py (_gate_findings repair)
- FOUND: tests/test_dsx.py (four repaired sites)
- FOUND: tests/test_frame_interference.py (one repaired site)
- FOUND: tests/test_frame_val.py (one repaired site)
- FOUND: tests/test_frame_prereg.py (TestGateRegistration, TestAdHocCommandScope)
- FOUND: f41e6bd (Task 1 commit)
- FOUND: 877454e (Task 2 commit)
- FOUND: 75d3436 (Task 3 commit)

---
*Phase: 10-pre-registered-inference-plan-dsx-pre*
*Completed: 2026-08-20*
