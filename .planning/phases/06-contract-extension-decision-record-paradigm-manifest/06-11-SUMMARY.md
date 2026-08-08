---
phase: 06-contract-extension-decision-record-paradigm-manifest
plan: 11
subsystem: decision-trail
tags: [jsonl, decision-record, audit-trail, error-handling, gap-closure]

# Dependency graph
requires:
  - phase: 06-09
    provides: "dsx explain subcommand, gate-path decision-trail write (_write_decision_trail), the read_all()/next_invocation_id() reader this plan hardens"
  - phase: 06-VERIFICATION
    provides: "the reproduced BLOCKER (truth 3b failed) this plan closes: a non-UTF-8 byte in DECISIONS.jsonl made dsx explain exit 2 and dsx gate plan exit 2 on an otherwise-clean spec"
provides:
  - "dsx/decisions.py::read_all() that cannot raise for any on-disk state of its target path (encoding-tolerant via errors=\"replace\", unreadable-path-tolerant via an OSError guard)"
  - "dsx/cli.py::_write_decision_trail and dsx/cli.py::cmd_explain guards widened to Exception, so the two functions' documented invariants are structural properties rather than an enumeration of tested failure modes"
  - "9 committed regression tests (4 unit, 5 CLI-level control-comparison) proving a corrupted trail can never move a gate exit code and can never move dsx explain off exit 0"
  - "documented, deliberately-deferred WR-02 concurrency limitation at the function, module and README level"
affects: [10, decision-trail, dsx-explain, audit]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Structural exception containment: a function's docstring states an unconditional invariant, so its guard is Exception (not one class), proven by regression tests asserting degraded output, not just exit codes"
    - "Control-comparison testing: a corrupted-trail exit code is asserted equal to a fresh no-trail-file control run's exit code, so the assertion states the invariant itself rather than a hard-coded exit value"

key-files:
  created: []
  modified:
    - dsx/decisions.py
    - dsx/cli.py
    - tests/test_decisions.py
    - tests/test_dsx.py
    - README.md

key-decisions:
  - "read_all() uses errors=\"replace\" (not a stricter/looser strategy) so decoding itself cannot raise; a line degraded by replacement characters then falls through to the existing json.JSONDecodeError skip path — one mechanism handles both encoding-level and JSON-level corruption"
  - "Both dsx/cli.py call sites (_write_decision_trail, cmd_explain) are widened to except Exception, not a narrower class — the invariant each docstring states is unconditional, so a guard naming one exception class leaves it conditional on the exception taxonomy of everything read_all/next_invocation_id/DecisionRecord can transitively raise. Neither guard widens to BaseException — KeyboardInterrupt/SystemExit still propagate"
  - "WR-02 (non-atomic invocation-id read-then-write) is documented, not fixed — the locking remedy needs a platform-guarded fcntl/msvcrt split and a non-deterministic concurrency test, which is new engineering against a mode this phase's single-process suite does not exercise; deferred to whichever phase first needs concurrent gate invocations against one root"

requirements-completed: [REQ-P6-07, REQ-P6-08]

coverage:
  - id: D1
    description: "read_all() never raises for any on-disk state (undecodable tail byte, undecodable middle line surrounded by valid records, or a directory in place of the trail file)"
    requirement: "REQ-P6-07"
    verification:
      - kind: unit
        ref: "tests/test_decisions.py#test_read_all_does_not_raise_on_undecodable_tail_bytes"
        status: pass
      - kind: unit
        ref: "tests/test_decisions.py#test_read_all_preserves_records_written_after_an_undecodable_line"
        status: pass
      - kind: unit
        ref: "tests/test_decisions.py#test_read_all_returns_empty_list_when_path_is_not_a_readable_file"
        status: pass
    human_judgment: false
  - id: D2
    description: "next_invocation_id() derives the correct next identifier over a trail whose bytes are partly undecodable, rather than raising into the gate path"
    requirement: "REQ-P6-07"
    verification:
      - kind: unit
        ref: "tests/test_decisions.py#test_next_invocation_id_unaffected_by_undecodable_bytes"
        status: pass
    human_judgment: false
  - id: D3
    description: "dsx explain exits 0 unconditionally for an undecodable byte and for a trail path that is a directory, and still renders the invocation id that survived the corruption"
    requirement: "REQ-P6-08"
    verification:
      - kind: integration
        ref: "tests/test_dsx.py#TestDecisionTrailCLI.test_explain_exits_zero_when_trail_holds_an_undecodable_byte"
        status: pass
      - kind: integration
        ref: "tests/test_dsx.py#TestDecisionTrailCLI.test_explain_still_renders_surviving_records_past_an_undecodable_byte"
        status: pass
      - kind: integration
        ref: "tests/test_dsx.py#TestDecisionTrailCLI.test_explain_exits_zero_when_trail_path_is_a_directory"
        status: pass
    human_judgment: false
  - id: D4
    description: "no on-disk failure mode of DECISIONS.jsonl can move a dsx gate exit code — a corrupted trail run's exit code equals a fresh no-trail control run's exit code, for both a passing and a blocking spec"
    requirement: "REQ-P6-07"
    verification:
      - kind: integration
        ref: "tests/test_dsx.py#TestDecisionTrailCLI.test_gate_pass_exit_code_matches_control_with_corrupted_trail"
        status: pass
      - kind: integration
        ref: "tests/test_dsx.py#TestDecisionTrailCLI.test_gate_block_exit_code_matches_control_with_corrupted_trail"
        status: pass
    human_judgment: false
  - id: D5
    description: "the WR-02 invocation-id collision under concurrent dsx gate runs is documented at the function, module and README level, with the locking remedy explicitly deferred"
    requirement: "REQ-P6-07"
    verification:
      - kind: other
        ref: "python3 -c \"import dsx.decisions as d; assert 'concurrent' in (d.next_invocation_id.__doc__ or '').lower() and 'unsupported' in (d.next_invocation_id.__doc__ or '').lower()\""
        status: pass
      - kind: other
        ref: "python3 -c \"import pathlib; t=pathlib.Path('README.md').read_text(encoding='utf-8').lower(); assert 'concurrent' in t and 'dsx gate' in t\""
        status: pass
    human_judgment: false

# Metrics
duration: ~10min
completed: 2026-08-08
status: complete
---

# Phase 06 Plan 11: Decision Trail Encoding and Unreadable-Path Hardening Summary

**`dsx/decisions.py::read_all()` cannot raise for any on-disk state of `DECISIONS.jsonl`, and both `dsx/cli.py` call sites contain every exception below `BaseException`, closing the Phase 6 verification BLOCKER (verified truth 3b) with 9 committed regression tests observed failing before the fix**

## Performance

- **Duration:** ~10 min
- **Started:** 2026-08-08T10:55:30+02:00 (first task commit)
- **Completed:** 2026-08-08T10:59:47+02:00 (final task commit)
- **Tasks:** 3
- **Files modified:** 5 (dsx/decisions.py, dsx/cli.py, tests/test_decisions.py, tests/test_dsx.py, README.md)

## Accomplishments

- `dsx/decisions.py::read_all()` now decodes with `errors="replace"` and wraps the read in `try/except OSError`, so it cannot raise for an undecodable byte, an undecodable line surrounded by valid records, or a path that exists but is not a readable file (a directory, reproduced live on Windows as `PermissionError`, itself an `OSError` subclass).
- `dsx/cli.py::_write_decision_trail`'s guard widened from `except OSError` to `except Exception` — the gate-path read-before-write can no longer turn a corrupted trail into an exit-2 operational error on a spec that would otherwise pass or block cleanly.
- `dsx/cli.py::cmd_explain` gained an outer `except Exception` guard around the trail read through the final print, on top of the now-non-raising `read_all()` — the "always returns 0" contract is now a structural property of the function, not an enumeration of previously-tested failure modes. The pre-existing `CheckError` guard around `find_spec` (root resolution) is unchanged, and no block-contract primitive (`Report`, `Severity`, `GATE_THRESHOLDS`, `emit`) was imported.
- Neither guard widens to `BaseException` — `KeyboardInterrupt`/`SystemExit` still propagate.
- 9 new regression tests (4 unit-level in `tests/test_decisions.py`, 5 CLI-level control-comparison tests plus 2 helper methods in `tests/test_dsx.py::TestDecisionTrailCLI`) were committed and observed RED against unmodified source before the fix, then GREEN after.
- WR-02 (the non-atomic `next_invocation_id()` + `append()` read-then-write) is documented as an unsupported-concurrency limitation at the function docstring, the module docstring, and a new README subsection — the locking remedy is explicitly deferred with recorded reasoning, not silently carried.
- Full suite: 279 tests (270 baseline + 9 new), 0 failures. `gen-finding-catalogue.py --check` still exits 0. No changes to `dsx/checks/`.

## Task Commits

Each task was committed atomically, RED before GREEN:

1. **Task 1: RED — commit the regression tests the verifier specified, and observe them fail** — `d60e61e` (test)
2. **Task 2: GREEN — make the trail unable to change a verdict, at the reader and at both call sites** — `e701a69` (fix)
3. **Task 3: Record the concurrency limitation WR-02 rather than silently carrying it** — `5c2a111` (docs)

_This plan is `type: tdd`; Task 1 is the RED gate, Task 2 is the GREEN gate. No REFACTOR commit was needed — the GREEN implementation matched the specified fix shape with no follow-up cleanup._

**RED evidence (Task 1, observed against unmodified source):**

```
Ran 35 tests in 0.333s
FAILED (failures=4, errors=5)
```

9/9 new tests failed (4 `FAIL` assertion mismatches on exit codes, 5 `ERROR`s). Representative root-cause traceback:

```
File "dsx/decisions.py", line 117, in read_all
    for line in p.read_text(encoding="utf-8").splitlines():
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc3 in position 251: unexpected end of data
```

The directory-as-trail-path case raised `PermissionError` (an `OSError` subclass) rather than `IsADirectoryError` — a Windows-specific manifestation of the same underlying condition ("path exists but is not a readable file"), caught by the same planned `except OSError` guard.

**GREEN evidence (Task 2):**

```
Ran 279 tests in 1.779s
OK (skipped=2)
```

## Files Created/Modified

- `dsx/decisions.py` (+42, Task 2; +21, Task 3) — `read_all()` decode/OSError tolerance and docstring, `next_invocation_id()` and module docstring gain the WR-02 concurrency limitation
- `dsx/cli.py` (+~40) — `_write_decision_trail` guard widened to `Exception`; `cmd_explain` gains an outer `Exception` guard and an expanded docstring
- `tests/test_decisions.py` (+69) — 4 new unit tests in `TestDecisions`, placed after `test_read_all_skips_blank_lines`
- `tests/test_dsx.py` (+85) — 2 new helper methods and 5 new tests in `TestDecisionTrailCLI`; the original 804-839 line range and the D-08 fixture tests/harness in `TestCLI` are untouched (confirmed via `git diff -U0 8882b2e..HEAD -- tests/test_dsx.py`, hunks only at 1710/1825)
- `README.md` (+14) — new "Concurrent `dsx gate` invocations are not supported" subsection under `## Known limits`, beside the existing "a frame that lies passes" limit

## Decisions Made

- **`errors="replace"` over a stricter per-byte recovery strategy.** The minimal, review-specified fix: decoding itself cannot raise, and a replacement-character-degraded line either still parses as JSON (harmless) or falls into the pre-existing `json.JSONDecodeError` skip (also harmless). No new decode-error taxonomy to maintain.
- **`except Exception`, not a named subclass, at both `dsx/cli.py` call sites.** Both docstrings state an unconditional invariant ("never blocks", "can never change the exit code"); a guard naming one exception class would leave the invariant conditional on the exception taxonomy of everything the guarded code calls transitively, including the `DecisionRecord` constructor's `TypeError` on future shape drift.
- **WR-02 is documented, not locked.** An OS-level advisory lock needs a platform-guarded `fcntl`/`msvcrt` split, a lock-file lifecycle, and a genuinely non-deterministic concurrency test — new engineering against a mode this phase's single-process `unittest` suite cannot exercise deterministically. Consistent with D-19's recorded reasoning about two writers on one append-only file. Deferred to whichever phase first reads recorded invocation history as an input (Phase 10 is the first plausible candidate).

## Deviations from Plan

None — plan executed exactly as written. All three tasks, their read_first/action/acceptance-criteria instructions, and the prohibitions (D-08 fixture tests untouched, no 06-01..06-10 artifact renumbered/rewritten/deleted, `dsx/spec.py` and `scripts/gen-finding-catalogue.py` untouched, stdlib-only, no `dsx/checks/` change) were followed as specified. One clarification worth recording: the plan's stated prohibition line range for `tests/test_dsx.py` (804-839) did not correspond to the D-08 fixture tests in the file as it exists at this plan's base commit — those tests (`test_good_fixture_passes_every_gate`, `test_bad_fixture_blocks_at_plan`, `test_bad_fixture_blocks_at_ship`) live at lines ~1192-1207 in `class TestCLI`. This plan's edits touched neither range, so the diff-assertion (`git diff -U0 tests/test_dsx.py` showing no change in 804-839) and the actual prohibition's intent (D-08 fixture tests stay unedited) both hold regardless of the line-number discrepancy.

One additional discretionary choice: the plan's Task 3 `read_first` assumed an existing "decision-trail / dsx explain" documentation section in README.md to extend. No such section exists in the committed README — `dsx explain` and `DECISIONS.jsonl` are not documented there at all as of this plan's base commit (06-09's SUMMARY did not add README content for them). Per the task's own fallback instruction ("next to the 'a frame that lies passes' limit"), the new subsection was added under the existing `## Known limits` heading at that exact location, matching its heading depth (`###`) and voice. This is not a new deviation rule invocation — it is following the task's own literal placement instruction where its assumed precondition did not hold.

## Issues Encountered

None. All acceptance criteria and the plan's `<verification>` block were reproduced directly, including the verifier's two originally-failing live reproductions (`dsx explain --phase-dir <corrupted>` and `dsx gate plan --spec examples/good-ANALYSIS-SPEC.yaml` with the same corrupted trail present), both now exiting 0.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- The Phase 6 verification BLOCKER (06-VERIFICATION.md truth 3b, "failed") is closed: both live reproductions that falsified it now hold, backed by 9 committed regression tests observed RED before the fix.
- Full 279-test suite baseline for any remaining Phase 6 gap-closure plan (06-12, 06-13) to build on; `gen-finding-catalogue.py --check` exits 0.
- **Carried concern, not introduced by this plan and out of this plan's scope:** CR-02 from `06-REVIEW.md` (the `examples/known-bad/*` fixtures' header/postmortem prose overstating "passes every gate at every severity threshold") is unresolved by this plan — it is a separate BLOCKER-adjacent finding tracked for a different gap-closure plan in this phase.
- **Carried concern, deliberately deferred by this plan (WR-02):** concurrent `dsx gate` invocations against one root remain unsupported; the collision mode is now documented at three levels rather than silently carried. The advisory-lock remedy is open for whichever phase first needs concurrent gate invocations (Phase 10 is the first plausible candidate per this plan's Task 3 reasoning).
- **Carried concern, not introduced by this plan:** WR-01 (`dsx/spec.py::_INFERENCE_FIELDS` dead code) and WR-03 (`gen-finding-catalogue.py`'s non-boundary-safe `"DSX-SPEC-08"` allow-list prefix) from `06-REVIEW.md` remain open — neither was in this plan's `files_modified` scope.

## Self-Check: PASSED

- `dsx/decisions.py` — FOUND
- `dsx/cli.py` — FOUND
- `tests/test_decisions.py` — FOUND
- `tests/test_dsx.py` — FOUND
- `README.md` — FOUND
- Commit `d60e61e` — FOUND
- Commit `e701a69` — FOUND
- Commit `5c2a111` — FOUND

---
*Phase: 06-contract-extension-decision-record-paradigm-manifest*
*Completed: 2026-08-08*
