---
phase: 25-hermetic-profile-depth
plan: 01
subsystem: infra
tags: [statistics, stdlib, csv, profiler, hermetic-testing, tdd]

# Dependency graph
requires: []
provides:
  - "dsx/profiler.py::_numeric_block(values) -> dict — min/q1/median/q3/max/mean/sd/n_zero/n_negative/n, H&F type-7 inclusive quantiles"
  - "dsx/profiler.py::_categorical_block(counts) -> dict — share_top1/share_top10/rare_share/n_singleton with frozen (count desc, level asc) tie-break"
  - "columns[<col>].numeric appended after dtype for integer/float columns"
  - "columns[<col>].categorical appended after dtype for string/mixed columns"
  - "tests/fixtures/profiler/ hand-computed reference-value fixture CSVs (numeric + categorical)"
  - "tests/test_profiler_hermetic.py — TestNumericBlock, TestCategoricalBlock, TestProfilerDeterminism"
  - "golden_preexisting_numeric_1_10.yaml — byte-stability trip-wire for every pre-Phase-25 profile key"
affects: [25-02, 25-03, 25-04]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Single-pass accumulation: numeric_values / categorical_counts fed inside the existing `for row in reader:` loop, reduced once after the loop closes — no second file pass."
    - "Deterministic tie-break: every top-N/rare/singleton result goes through explicit `sorted(items, key=lambda kv: (-count, level))`, never Counter.most_common() (which ties by CSV row/insertion order)."
    - "Additive-append discipline: new dtype-conditional sub-maps are assigned as the LAST write to col_stats[col], after null_rate/n_unique/dtype, so the hand-rolled insertion-order YAML emitter (_dump) leaves every pre-existing rendered byte unchanged."
    - "null-not-zero: every undefined statistic is Python None, rendered as YAML `null` by the existing `_scalar` mapping — never 0 or NaN."

key-files:
  created:
    - tests/test_profiler_hermetic.py
    - tests/fixtures/profiler/numeric_1_10.csv
    - tests/fixtures/profiler/numeric_zeros_negatives.csv
    - tests/fixtures/profiler/numeric_n1.csv
    - tests/fixtures/profiler/categorical_abcde.csv
    - tests/fixtures/profiler/categorical_percent_arm.csv
    - tests/fixtures/profiler/categorical_top10_tie.csv
    - tests/fixtures/profiler/golden_preexisting_numeric_1_10.yaml
  modified:
    - dsx/profiler.py

key-decisions:
  - "Numeric accumulation parses via the existing _INT_RE/_FLOAT_RE gate with plain float() — no new locale-aware parsing call site (T-25-02 mitigation)."
  - "categorical/numeric accumulators are populated for every column during the row loop regardless of eventual dtype; only the post-loop dtype check decides whether the block is attached — harmless for columns whose accumulated values end up unused."
  - "Golden file embeds this machine's absolute fixture path (existing profile_csv behavior, unchanged) — acceptable since the golden test recomputes profile_csv on the same FIXTURES-relative path every run, so the comparison is reproducible on this checkout, consistent with the plan's real-interpreter/this-machine execution model."

requirements-completed: [REQ-P25-01, REQ-P25-02]

coverage:
  - id: D1
    description: "_numeric_block computes min/q1/median/q3/max/mean/sd/n_zero/n_negative/n per D-02 (H&F type-7 inclusive quantiles, statistics.mean/stdev, null-not-zero for n=0/n=1 edges)"
    requirement: "REQ-P25-01"
    verification:
      - kind: unit
        ref: "tests/test_profiler_hermetic.py#TestNumericBlock"
        status: pass
    human_judgment: false
  - id: D2
    description: "_categorical_block computes share_top1/share_top10/rare_share/n_singleton with the frozen count-desc/level-asc tie-break, provably independent of CSV row order"
    requirement: "REQ-P25-01"
    verification:
      - kind: unit
        ref: "tests/test_profiler_hermetic.py#TestCategoricalBlock"
        status: pass
    human_judgment: false
  - id: D3
    description: "Two profile_csv runs on the same fixture are byte-identical, and every pre-Phase-25 rendered key/line is byte-unchanged (golden)"
    requirement: "REQ-P25-02"
    verification:
      - kind: unit
        ref: "tests/test_profiler_hermetic.py#TestProfilerDeterminism"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py#TestProfiler"
        status: pass
    human_judgment: false

duration: 8min
completed: 2026-09-06
status: complete
---

# Phase 25 Plan 01: Hermetic numeric/categorical column blocks Summary

**`dsx/profiler.py` gains `_numeric_block`/`_categorical_block`, computing D-02's trust-core numeric and categorical statistics (type-7 inclusive quantiles, sample sd, frozen tie-break) additively under `columns[<col>].numeric`/`.categorical`, with a determinism guard and pre-existing-key golden proving zero byte drift.**

## Performance

- **Duration:** ~8 min (first RED commit `d78a738` to last commit `cd86894`, both 2026-09-06)
- **Tasks:** 3/3 completed
- **Files modified:** 1 (`dsx/profiler.py`)
- **Files created:** 8 (1 test module, 7 fixtures including the golden)

## Accomplishments
- `_numeric_block(values)` — min/q1/median/q3/max/mean/sd/n_zero/n_negative/n via `statistics.quantiles(..., n=4, method="inclusive")` (H&F type 7), `statistics.mean`/`statistics.stdev` (never `fmean`, never a hand-rolled float loop); n=0 → all-null; n=1 → min=max=q1=median=q3=mean=value, sd=null.
- `_categorical_block(counts)` — share_top1/share_top10/rare_share/n_singleton via an explicit `sorted(items, key=lambda kv: (-count, level))` tie-break, never `Counter.most_common()`; rare = count<10 OR count/n<0.001 (both strict).
- Both blocks wired into `profile_csv`'s existing single-pass row loop (new `numeric_values`/`categorical_counts` accumulators) and assigned as the LAST write to `col_stats[col]`, after `null_rate`/`n_unique`/`dtype` — proven by an explicit key-order assertion and the golden test.
- Determinism guard: two `write_profile()` runs on `numeric_1_10.csv` produce byte-identical files.
- Pre-existing-key golden: every pre-Phase-25 rendered line (`profile_version`, `computed_by`, `source_path`, `source_hash`, `row_count`, `columns.<col>.{null_rate,n_unique,dtype}`, `primary_key`, `primary_key_unique`, `duplicate_rate`, `time.*`, `sentinels_found`) is byte-compared (raw text, CRLF-tolerant, never parsed-as-dict) against a committed golden that contains zero `numeric:`/`categorical:` lines.
- All three pinned reference literals confirmed exactly: `_numeric_block([1..10])["sd"] == 3.0276503540974917`, `["q1"] == 3.25`, `["q3"] == 7.75`.

## Task Commits

Each task was committed atomically (TDD RED → GREEN pairs):

1. **Task 1: Numeric column block** — RED `d78a738`, GREEN `6d5b312`
2. **Task 2: Categorical column block** — RED `0d6415b`, GREEN `c038ba9`
3. **Task 3: Determinism guard + pre-existing-key golden** — `cd86894` (type="execute", single commit)

Branch: `gsd/v2.6.0-exploration-depth` (unpushed by design — orchestrator reconciles and pushes).

## Files Created/Modified
- `dsx/profiler.py` — `import statistics`; `_numeric_block`, `_categorical_block`; `numeric_values`/`categorical_counts` accumulators in the existing row loop; post-loop dtype-conditional append of `numeric`/`categorical` as the last key in each column's sub-dict.
- `tests/test_profiler_hermetic.py` — `TestNumericBlock`, `TestCategoricalBlock`, `TestProfilerDeterminism`, plus a `_strip_new_blocks` CRLF-tolerant line filter used by the golden test.
- `tests/fixtures/profiler/numeric_1_10.csv`, `numeric_zeros_negatives.csv`, `numeric_n1.csv` — hand-computed numeric reference fixtures.
- `tests/fixtures/profiler/categorical_abcde.csv`, `categorical_percent_arm.csv`, `categorical_top10_tie.csv` — hand-computed categorical reference fixtures (generated deterministically by a throwaway script, verified byte counts before commit).
- `tests/fixtures/profiler/golden_preexisting_numeric_1_10.yaml` — the D-04 guard #3 golden, generated once from the real profiler output and containing zero additive-block lines.

## Decisions Made
- Numeric values are parsed via `float(stripped)` uniformly (both int- and float-looking matches) rather than preserving int type — harmless since `_scalar`'s existing float formatting renders `1.0` as `1`, and every reference-value assertion uses `assertEqual` (int/float equality) so no test result depends on the distinction.
- `numeric_values`/`categorical_counts` accumulate for every column during the row loop regardless of final dtype; only the post-loop dtype branch decides attachment. This keeps the single-pass discipline (no second file read) at the cost of small, row-count-bounded unused accumulation for columns that turn out not to need the block — accepted per the plan's T-25-01 threat disposition.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug, in test code] Fixed hand-computed arithmetic error in the top-10 tie-break test**
- **Found during:** Task 2 (Categorical column block), first GREEN run
- **Issue:** `test_top10_tie_boundary_count_desc_then_string_asc` asserted `share_top10 == (109 + 5) / 119`, based on a manual arithmetic error (summed `15+14+13+12+11+10+9+8+7` as 109 instead of the correct 99). This was a bug in the RED test's hand-computed expectation, not in `_categorical_block` — running the assertion against the actual profiler output (`share_top10 = 0.9541284403669725`, `row_count = 109`) confirmed the implementation was correct and the test's expected value was wrong.
- **Fix:** Recomputed the sum (`15+14+13+12+11+10+9+8+7 = 99`) and corrected the assertion to `(99 + 5) / 109`, matching the fixture's actual 109 total rows (99 for levels a–i + 5 "n" + 5 "m").
- **Files modified:** `tests/test_profiler_hermetic.py`
- **Verification:** `TestCategoricalBlock` and the full `test_profiler_hermetic` module green after the fix; re-verified the corrected arithmetic independently via `python -c "print(15+14+13+12+11+10+9+8+7)"` → 99.
- **Committed in:** `c038ba9` (part of Task 2's GREEN commit — the test file was not yet "shipped" in a prior commit as correct, so no separate fix commit was needed; the RED commit `0d6415b` still contains the original, since-corrected value for historical record).

---

**Total deviations:** 1 auto-fixed (Rule 1, test-arithmetic bug, no production code affected)
**Impact on plan:** None on scope — the implementation matched the plan and D-02 exactly on first GREEN attempt; only the test's own hand-computed expected value needed correction.

## Issues Encountered
None beyond the deviation above.

## User Setup Required
None — no external service configuration required.

## Next Phase Readiness

- `columns[<col>].numeric`/`.categorical` are live and byte-stable; 25-02/03/04 (time block, `--unit`, `--target`) can build on the same single-pass-accumulation and append-last patterns established here.
- The pre-existing-key golden (`golden_preexisting_numeric_1_10.yaml`) and its `_strip_new_blocks` filter are reusable scaffolding for subsequent plans' own byte-stability guards on the `time:`/`unit:`/`target:` blocks.
- No blockers. Full test suite (1542 tests) green on the real interpreter (`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`) with zero regressions in `tests.test_dsx.TestProfiler`.

---
*Phase: 25-hermetic-profile-depth*
*Completed: 2026-09-06*

## Self-Check: PASSED

All files referenced above (`dsx/profiler.py`, `tests/test_profiler_hermetic.py`, all 7 fixtures, this SUMMARY) confirmed present via `[ -f ... ]`. All 5 commit hashes (`d78a738`, `6d5b312`, `0d6415b`, `c038ba9`, `cd86894`) confirmed present via `git cat-file -e`.
