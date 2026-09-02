---
phase: 17-foundation-repairs-and-spec-vocabulary
plan: 02
subsystem: testing
tags: [statistics, routing-table, regression-pin, disposition-table, code-ranges]

requires:
  - phase: 17-foundation-repairs-and-spec-vocabulary
    provides: "D-02 D-12a disposition table + D-03 D-06 range pre-allocation (17-CONTEXT.md, committed 2a6b7c8)"
provides:
  - "regression pin: recommend_test routes every time_to_event input to log_rank via unconditional fallthrough; no equality guard on the literal exists in source"
  - "verified-discharged: D-12a disposition table (all 9 Phase 18/19 gates) and D-06 range pre-allocation present in committed 17-CONTEXT.md"
affects: [18-correlation-association-agreement, 19-rm-trend-categorical-resampling-posthoc, 20-calibration-and-reporting-close]

tech-stack:
  added: []
  patterns:
    - "structural regression pin: inspect.getsource + negative regex scan asserts a routing property (no guard) that a future edit would silently break"

key-files:
  created:
    - tests/test_time_to_event_fallthrough.py
  modified: []

key-decisions:
  - "REQ-P17-03 and the range half of REQ-P17-04 are recorded-decision requirements verified in place against committed 17-CONTEXT.md (2a6b7c8), not newly written — this plan mints no code and edits no production file."

patterns-established:
  - "Pattern: pin a correct-by-fallthrough routing contract with a source-scan test BEFORE later phases add branches that could silently reroute it."

requirements-completed: [REQ-P17-03, REQ-P17-04]

coverage:
  - id: D1
    description: "recommend_test routes every time_to_event input to log_rank (n_groups x paired) and no equality guard on the time_to_event literal exists in recommend_test source."
    requirement: "REQ-P17-04"
    verification:
      - kind: unit
        ref: "tests/test_time_to_event_fallthrough.py#test_time_to_event_always_routes_to_log_rank + test_no_time_to_event_equality_guard_in_source"
        status: pass
    human_judgment: false
  - id: D2
    description: "D-12a paradigm-disposition table records a disposition for all nine Phase 18/19 gate checks (incl. observed-power ban's Bayesian sibling named D-13-deferred) in committed 17-CONTEXT.md."
    requirement: "REQ-P17-03"
    verification:
      - kind: other
        ref: "python3 grep oracle over 17-CONTEXT.md: all 9 gate IDs + 'D-13' marker present"
        status: pass
    human_judgment: false
  - id: D3
    description: "D-06 DSX-STA range pre-allocation (decades 050-129 by theme, 130-139 reserve) present in committed 17-CONTEXT.md."
    requirement: "REQ-P17-04"
    verification:
      - kind: other
        ref: "python3 grep oracle over 17-CONTEXT.md: '050' and '130' range anchors present"
        status: pass
    human_judgment: false

duration: 2min
completed: 2026-09-01
status: complete
---

# Phase 17 — Plan 02: time_to_event fallthrough pin Summary

**Pinned the time_to_event → log_rank unconditional fallthrough with a behavioural + source-scan regression test, and verified the D-12a disposition table and D-06 range pre-allocation are discharged in committed 17-CONTEXT.md — zero production-code edits.**

## Performance

- **Duration:** ~2 min
- **Started:** 2026-09-01T21:30Z
- **Completed:** 2026-09-01T21:33Z
- **Tasks:** 2 (fallthrough pin; recorded-decision verification)
- **Files modified:** 1 (created)

## Accomplishments
- New `tests/test_time_to_event_fallthrough.py`: behavioural leg (every `time_to_event` call → `log_rank`) + structural leg (no `outcome == "time_to_event"` guard in `recommend_test` source). GREEN on first run — a pin over already-correct behaviour.
- Verified via a deterministic grep oracle that committed `17-CONTEXT.md` records the D-12a disposition for all nine Phase 18/19 gates (with the observed-power Bayesian sibling named `D-13-deferred`) — REQ-P17-03.
- Verified the D-06 DSX-STA range pre-allocation (050-129 by theme, 130-139 reserve) is present — REQ-P17-04 range half.

## Task Commits

1. **Task 1: pin the time_to_event fallthrough** - `048d203` (test)
2. **Task 2: verify recorded decisions in 17-CONTEXT.md** - no code change; deterministic grep oracle passed (recorded in this SUMMARY).

## Files Created/Modified
- `tests/test_time_to_event_fallthrough.py` - New dual-idiom regression module; stdlib unittest; CRLF-safe.

## Decisions Made
None beyond the plan. REQ-P17-03 and REQ-P17-04's range half were discharged at S1-1 (persona round, committed 2a6b7c8) and are verified in place here, not re-litigated.

## Deviations from Plan
None - plan executed exactly as written.

## Issues Encountered
None.

## Gate Evidence (orchestrator-run)
- `python3 -m unittest tests.test_time_to_event_fallthrough -v` → 2/2 GREEN (both legs) at commit `048d203`.
- Grep oracle over `17-CONTEXT.md` → `D-02 dispositions + D-03 ranges present` (all 9 gate IDs; `D-13` sibling; `050`/`130` range anchors).
- `dsx/checks/stats.py` byte-unchanged by this plan (git status clean for it after the commit).

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- REQ-P17-03 and REQ-P17-04 delivered. Wave 1 complete; Wave 2 (17-03) may proceed.

---
*Phase: 17-foundation-repairs-and-spec-vocabulary*
*Completed: 2026-09-01*
