---
phase: 25-hermetic-profile-depth
plan: 02
subsystem: infra
tags: [statistics, stdlib, csv, profiler, hermetic-testing, tdd, time, unit]

# Dependency graph
requires:
  - "25-01: single-pass accumulation + additive-append discipline + pre-existing-key golden scaffolding"
provides:
  - "dsx/profiler.py::_extract_hour(value) -> int|None — hour token retention via a separate accumulator, frozen `dates` list untouched"
  - "time: block gains rows_per_day {min,median,max} (day-grain), first_period_ratio/last_period_ratio (ISO-week grain, <5 populated weeks -> null), share_at_hour_00 (time-bearing denominator, null when none), appended after max_gap_days and only when a time column is declared"
  - "profile_csv gains a `unit: str|None = None` keyword parameter (unknown header -> CheckError)"
  - "new top-level `unit` block: rows_per_unit {p50,p95,max} (type-7 inclusive quantiles over per-unit counts), largest_unit_share (count desc / unit asc tie-break); omitted entirely when no unit is declared"
  - "tests/fixtures/profiler/ hand-computed time + unit reference fixtures (8 CSVs)"
  - "tests/test_profiler_hermetic.py — TestTimeBlock, TestUnitBlock"
affects: [25-03, 25-04]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Separate parallel accumulator for hour retention (hour_of_time_bearing_rows / day_counts / iso_week_counts) fed inside the existing single row loop — never appended to the frozen `dates` list, so time.min/max/max_gap_days stay byte-stable."
    - "Additive time keys gated on `time_column` being declared: a profile without --time keeps the frozen 4-key time block byte-identical (25-01 golden trip-wire)."
    - "ISO-week bucketing via date.isocalendar()[:2] (locale-free, deterministic); edge ratios over populated weeks sorted by (iso_year, iso_week) — order-independent."
    - "unit block appended to the return dict AFTER sentinels_found as the last insertion, preserving _dump insertion-order byte-stability; omitted (not null) when unit is None."
    - "largest_unit_share winner chosen via explicit sorted((-count, unit_string)) tie-break, never Counter.most_common()."

key-files:
  created:
    - tests/fixtures/profiler/time_hour_all_midnight.csv
    - tests/fixtures/profiler/time_hour_half.csv
    - tests/fixtures/profiler/time_hour_date_only.csv
    - tests/fixtures/profiler/time_hour_mixed.csv
    - tests/fixtures/profiler/time_rows_per_day.csv
    - tests/fixtures/profiler/time_edge_ratio.csv
    - tests/fixtures/profiler/time_edge_ratio_short.csv
    - tests/fixtures/profiler/unit_counts.csv
  modified:
    - dsx/profiler.py
    - tests/test_profiler_hermetic.py

key-decisions:
  - "New time sub-keys are appended only when a time column is declared. The plan action did not state this gate explicitly, but the 25-01 pre-existing-key golden (run on numeric_1_10.csv with no --time) requires the time block to stay a byte-identical 4-key shape when no time column is passed. Gating on time_column keeps the golden green while still emitting all-null time stats when a time column is supplied but carries no dated rows."
  - "largest_unit_share denominator = row_count (the literal 'total rows' reading). The unit_counts.csv fixture is fully populated (110 rows, no nulls), so row_count == sum(per-unit counts) == 110 and the reference value 100/110 is unambiguous under either denominator."
  - "rows_per_unit p50/p95 selected as cuts[49]/cuts[94] from statistics.quantiles(per_unit, n=100, method='inclusive'); p95 literal (80.8) pinned from an actual run on the real 3.12.10 interpreter, not hand-estimated."

requirements-completed: [REQ-P25-01, REQ-P25-02]

coverage:
  - id: D1
    description: "Time-block depth: _extract_hour, share_at_hour_00 (time-bearing denominator, null on date-only), rows_per_day (day-grain), first/last_period_ratio (ISO-week grain, <5 weeks -> null), all appended after max_gap_days; frozen time.* keys unchanged"
    requirement: "REQ-P25-01"
    verification:
      - kind: unit
        ref: "tests/test_profiler_hermetic.py#TestTimeBlock"
        status: pass
      - kind: unit
        ref: "tests/test_profiler_hermetic.py#TestProfilerDeterminism"
        status: pass
    human_judgment: false
  - id: D2
    description: "Unit block: rows_per_unit p50/p95/max (type-7 quantiles), largest_unit_share (count-desc/unit-asc tie-break); omitted when unit absent; unknown unit -> CheckError"
    requirement: "REQ-P25-01"
    verification:
      - kind: unit
        ref: "tests/test_profiler_hermetic.py#TestUnitBlock"
        status: pass
    human_judgment: false
  - id: D3
    description: "Every new time and unit statistic is byte-identical across a shuffled row order; frozen time.min/max/max_gap_days byte-unchanged (25-01 golden green)"
    requirement: "REQ-P25-02"
    verification:
      - kind: unit
        ref: "tests/test_profiler_hermetic.py#TestTimeBlock.test_new_time_keys_deterministic_across_shuffle"
        status: pass
      - kind: unit
        ref: "tests/test_profiler_hermetic.py#TestUnitBlock.test_deterministic_across_shuffle"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py#TestProfiler"
        status: pass
    human_judgment: false

duration: 12min
completed: 2026-09-07
status: complete
---

# Phase 25 Plan 02: Time-block depth + unit block Summary

**`dsx/profiler.py` gains `_extract_hour` and additive time keys (rows_per_day, ISO-week first/last_period_ratio, share_at_hour_00) plus a new top-level `unit` block (rows_per_unit p50/p95/max, largest_unit_share) — hermetic, stdlib-only, with the three frozen `time.*` keys provably byte-unchanged and every new statistic order-independent.**

## Performance
- **Duration:** ~12 min (RED `e2068a5` to GREEN `578e0b5`, 2026-09-07)
- **Tasks:** 2/2 completed
- **Files modified:** 2 (`dsx/profiler.py`, `tests/test_profiler_hermetic.py`)
- **Files created:** 8 fixtures

## Accomplishments
- `_extract_hour(value) -> int | None` — re-matches `_DATE_RE`, returns `None` when no time token (group 4 absent), else `int(group(4))`. `_parse_date` and the `dates: list[date]` accumulator are byte-for-byte untouched.
- Time-block extension appended after `max_gap_days`, gated on a declared time column:
  - `rows_per_day {min, median, max}` — day-grain counts via `statistics.median`; all-null when no dated rows.
  - `first_period_ratio` / `last_period_ratio` — ISO-week grain over populated weeks sorted by `(iso_year, iso_week)`; last = rows(last week) / mean(prev 4), first = rows(first week) / mean(next 4); both `None` when fewer than 5 populated weeks.
  - `share_at_hour_00` — count of hour-0 in `hour_of_time_bearing_rows` / len; `None` when that list is empty (date-only column never reads 1.0).
- `profile_csv` gains a `unit: str | None = None` keyword parameter; unknown header raises `CheckError` (matching `--pk`/`--time`).
- New top-level `unit` block appended after `sentinels_found`, omitted entirely when `unit is None`:
  - `rows_per_unit {p50, p95, max}` — type-7 inclusive quantiles over per-unit counts (`cuts[49]`/`cuts[94]` from `quantiles(n=100)`); `<2` distinct units → p50/p95 `None`, max defined for ≥1.
  - `largest_unit_share` — max count / row_count, winner via explicit `sorted((-count, unit))` tie-break.
- Pinned reference literals confirmed on the real interpreter: `rows_per_unit.p50 == 3`, `p95 == 80.8`, `max == 100`, `largest_unit_share == 0.9090909090909091`; `share_at_hour_00` == 1.0 / 0.5 / null / 0.3333333333333333; `rows_per_day` == {1, 5, 9}; edge ratios == 0.2 / 0.1 (null on ≤4 weeks).

## Task Commits
1. **RED (both tasks):** `e2068a5` — `test(25-02): add failing tests + fixtures for time-block and unit-block depth`
2. **Task 1 GREEN:** `d867f23` — `feat(25-02): time-block depth -- hour retention, rows_per_day, ISO-week edge ratios`
3. **Task 2 GREEN:** `578e0b5` — `feat(25-02): unit block -- rows_per_unit p50/p95/max, largest_unit_share`

Branch: `gsd/v2.6.0-exploration-depth` (unpushed by design — orchestrator re-verifies the gate and pushes).

## Verification
- `tests.test_profiler_hermetic.TestTimeBlock` + `TestProfilerDeterminism`: 14 tests OK (Task 1 verify command).
- `tests.test_profiler_hermetic.TestUnitBlock`: 6 tests OK (Task 2 verify command).
- `tests.test_profiler_hermetic` (all classes, incl. 25-01's): 32 tests OK.
- `tests.test_dsx.TestProfiler`: 2 tests OK (no regression).
- Full suite `-m unittest discover -s tests -q`: **1560 tests OK** on the real interpreter (`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`, 3.12.10). The pre-existing "DSX-*** declared twice" catalogue warnings are unrelated (no finding codes or gate modules touched).
- Deletion check across all three commits: none.

## Deviations from Plan
### Auto-fixed / clarified
**1. [Rule 3 - clarification] New time sub-keys gated on a declared time column**
- **Found during:** Task 1 GREEN.
- **Issue:** The plan action described appending the new time keys "after max_gap_days" without stating whether they emit when no `--time` is given. The 25-01 pre-existing-key golden runs on `numeric_1_10.csv` (no time column) and requires the `time:` block to stay a byte-identical 4-key shape.
- **Resolution:** Emit the four new time keys only when `time_column` is declared; a time column present but carrying no dated rows still emits all-null stats. Keeps the golden green (verified) and matches D-01's "omitted when absent" philosophy.
- **Files:** `dsx/profiler.py` — **Commit:** `d867f23`.

No other deviations — reference values matched on first GREEN for both tasks.

## Prohibitions honored
- Zero new finding codes; no gate module (`dsx/checks/*`, `dsx/checks/dq.py`) touched.
- Stdlib-only — no pandas/numpy/scipy or any non-stdlib import added (`statistics`, `csv`, `re`, `datetime`, `collections.Counter` already imported).
- `_parse_date` signature and the `dates` accumulator unchanged; hour retention uses a separate accumulator.
- New time keys append after `time.max_gap_days`; unit block appends after `sentinels_found` — never interleaved.
- ISO-week arithmetic via `date.isocalendar()`, never manual `//7`.
- No edits to REQUIREMENTS.md, STATE.md, or ROADMAP.md (single-writer — orchestrator owns those).

## Known Stubs
None.

## Next Phase Readiness
- `time.*` additive keys and the `unit` block are live and byte-stable. 25-03 (CLI `--unit`/`--target` flags that feed these parameters) and the `--target` block can build on the same separate-accumulator and append-last patterns.
- No blockers.

---
*Phase: 25-hermetic-profile-depth*
*Completed: 2026-09-07*

## Self-Check: PASSED

All files referenced above (`dsx/profiler.py`, `tests/test_profiler_hermetic.py`, all 8 fixtures, this SUMMARY) confirmed present via `[ -f ... ]`. All 3 task commit hashes (`e2068a5`, `d867f23`, `578e0b5`) confirmed present via `git cat-file -e`.
