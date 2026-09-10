---
phase: 25-hermetic-profile-depth
plan: 03
subsystem: infra
tags: [statistics, stdlib, csv, profiler, hermetic-testing, tdd, target, cli, base-rate]

# Dependency graph
requires:
  - "25-02: profile_csv single-pass accumulation, _parse_date/isocalendar week bucketing, unit block + additive-append discipline, tests/fixtures/profiler/ scaffolding"
provides:
  - "dsx/profiler.py::profile_csv gains a `target: str|None = None` keyword parameter (unknown header / --target-without-time / non-binary value -> CheckError)"
  - "new top-level `target` block: overall (mean of binary target over non-null rows), weekly [{week:[iso_year,iso_week], n, base_rate}, ...] ordered by (iso_year, iso_week), weekly_range [min,max], verdict (drifting | stable | null); omitted entirely when no target column is declared"
  - "dsx/cli.py cmd_profile gains --unit and --target flags (help text), wired into profile_csv(unit=..., target=...); CheckError -> CLI exit 2 (EXIT_ERROR)"
  - "tests/fixtures/profiler/ target reference fixtures (6 CSVs: drifting, stable, boundary, single_week, non_binary, yes_no)"
  - "tests/test_profiler_hermetic.py::TestTargetBlock; tests/test_dsx.py::TestProfiler CLI cases for --unit/--target/--help"
affects: [25-04]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Target accumulation folded into the existing single row loop: target_all (raw stripped non-null values, for overall + validation), target_distinct (for the offending-value error), target_week_raw (per (iso_year,iso_week) list) — no second pass."
    - "Binary validation is a CLOSED check against the literal set {\"0\",\"1\"} post-strip; yes/no/true/false are rejected (no truthy/falsy coercion reuse, 25-RESEARCH.md Pitfall 4); the CheckError lists EVERY distinct offending value (sorted, deterministic)."
    - "verdict is multiplicative and strict: drifting iff any week base_rate < 0.8*overall OR > 1.2*overall; the ±20% edge reads stable; null when <2 populated weeks. Multiplicative form dodges divide-by-zero for overall in {0,1}."
    - "target block appended to the return dict AFTER the unit block (or after sentinels_found when no unit) as the last insertion — preserves _dump insertion-order byte-stability; omitted (not null) when target is None so the 25-01/25-02 no-flag golden stays byte-identical."
    - "week key stored as a 2-int list [iso_year, iso_week] so the hand-rolled stdlib _dump renders it inline (a tuple would stringify/quote); weekly table ordered by sorted week key, order-independent."
    - "CLI stays thin: validation (requires-time, binary, unknown-header) lives in profile_csv, matching the existing --pk/--time placement; cmd_profile only parses args.unit/args.target and passes them through."

key-files:
  created:
    - tests/fixtures/profiler/target_drifting.csv
    - tests/fixtures/profiler/target_stable.csv
    - tests/fixtures/profiler/target_boundary.csv
    - tests/fixtures/profiler/target_single_week.csv
    - tests/fixtures/profiler/target_non_binary.csv
    - tests/fixtures/profiler/target_yes_no.csv
  modified:
    - dsx/profiler.py
    - dsx/cli.py
    - tests/test_profiler_hermetic.py
    - tests/test_dsx.py

key-decisions:
  - "week key rendered as a 2-int list [iso_year, iso_week] rather than a tuple or a 'YYYY-Www' string: a tuple would fall through _scalar and stringify/quote as \"(2024, 1)\"; a list of scalars renders inline and stays deterministic. CONTEXT D-02 specifies the bucket as (iso_year, iso_week) — the list preserves both components without a locale-dependent week-string format."
  - "overall is computed over ALL non-null-target rows (target_all), while weekly buckets only rows whose time cell also parses to a date. In every reference fixture every target row is dated, so the two populations coincide; the split is documented so a future partially-dated extract has a defined behaviour (row counted in overall, absent from any weekly bucket) rather than an accidental one."
  - "boundary float-equality holds under assertEqual (not assertAlmostEqual): statistics.mean uses exact-Fraction accumulation, so mean([1,1,0,0,0]) == 0.4 and mean([1,1,1,0,0]) == 0.6 as the identical IEEE-754 doubles as the literals; 0.8*0.5 == 0.4 and 1.2*0.5 == 0.6 exactly, so the strict < / > comparisons read the ±20% edge as stable. Verified on the real 3.12.10 interpreter."

requirements-completed: [REQ-P25-01, REQ-P25-02, REQ-P25-03]

coverage:
  - id: D1
    description: "target block: overall, weekly {week,n,base_rate} table ordered by (iso_year,iso_week), weekly_range [min,max], strict ±20% multiplicative verdict; drifting/stable/boundary/single-week reference values; omitted when --target absent; appended last (after unit / sentinels_found)"
    requirement: "REQ-P25-01"
    verification:
      - kind: unit
        ref: "tests/test_profiler_hermetic.py#TestTargetBlock"
        status: pass
    human_judgment: false
  - id: D2
    description: "--target validation in profile_csv: hard-requires --time (CheckError), unknown header (CheckError), binary {0,1} closed check rejecting yes/no with an error listing every distinct offending value (25-RESEARCH.md Pitfall 4)"
    requirement: "REQ-P25-01"
    verification:
      - kind: unit
        ref: "tests/test_profiler_hermetic.py#TestTargetBlock.test_non_binary_target_raises_listing_value"
        status: pass
      - kind: unit
        ref: "tests/test_profiler_hermetic.py#TestTargetBlock.test_yes_no_target_raises_listing_values"
        status: pass
      - kind: unit
        ref: "tests/test_profiler_hermetic.py#TestTargetBlock.test_target_requires_time"
        status: pass
  - id: D3
    description: "CLI --unit/--target parse, feed profile_csv, and their D-03 validation surfaces as CLI exit 2; --help documents both flags"
    requirement: "REQ-P25-01"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py#TestProfiler.test_profile_cli_unit_target_writes_blocks"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py#TestProfiler.test_profile_cli_target_without_time_exits_2"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py#TestProfiler.test_profile_cli_non_binary_target_exits_2"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py#TestProfiler.test_profile_help_names_unit_and_target"
        status: pass
    human_judgment: false
  - id: D4
    description: "target block deterministic across shuffled row order; no-flag golden unchanged (block omitted when target absent); zero new finding codes; no non-stdlib import"
    requirement: "REQ-P25-02"
    verification:
      - kind: unit
        ref: "tests/test_profiler_hermetic.py#TestTargetBlock.test_deterministic_across_shuffle"
        status: pass
      - kind: unit
        ref: "tests/test_profiler_hermetic.py#TestTargetBlock.test_target_block_omitted_when_absent"
        status: pass
      - kind: suite
        ref: "python.exe -m unittest discover -s tests -q (1576 OK)"
        status: pass
    human_judgment: false

duration: 15min
completed: 2026-09-07
status: complete
---

# Phase 25 Plan 03: Target weekly base-rate block + CLI --unit/--target Summary

**`dsx/profiler.py` gains a `target` keyword and a new top-level `target` block (overall, weekly {week,n,base_rate} table, weekly_range, strict ±20% multiplicative verdict), and `dsx/cli.py` grows the `--unit`/`--target` flags wired into `profile_csv` — hermetic, stdlib-only, with the binary check closed against {"0","1"} (yes/no/true/false rejected, every offending value listed), `--target` hard-requiring `--time`, and the block omitted entirely when the flag is absent so the 25-01/25-02 no-flag golden stays byte-identical.**

## Performance
- **Duration:** ~15 min (RED `07e864a` to Task 2 GREEN `cbff9ea`, 2026-09-07)
- **Tasks:** 2/2 completed
- **Files modified:** 4 (`dsx/profiler.py`, `dsx/cli.py`, `tests/test_profiler_hermetic.py`, `tests/test_dsx.py`)
- **Files created:** 6 fixtures

## Accomplishments
- `profile_csv` gains `target: str | None = None`. Validation (all `CheckError`, mapping to CLI exit 2):
  - `--target` without `--time` → `CheckError("--target requires --time")` (checked before the loop).
  - unknown target header → `CheckError(f"target column {target!r} not in CSV header")`, matching `--pk`/`--time`.
  - non-binary target → closed check against the literal set `{"0","1"}` post-strip; the error lists **every** distinct offending value, sorted; `yes`/`no`/`true`/`false` are rejected (no truthy/falsy coercion reuse — 25-RESEARCH.md Pitfall 4).
- New top-level `target` block, appended after the unit block (or after `sentinels_found` when no unit), omitted entirely (never null) when `target is None`:
  - `overall` — `statistics.mean` of the binary target over non-null-target rows.
  - `weekly` — a list of `{week: [iso_year, iso_week], n, base_rate}` rows, ordered by `(iso_year, iso_week)`; week bucket via `date.isocalendar()[:2]`.
  - `weekly_range` — `[min base_rate, max base_rate]` across populated weeks.
  - `verdict` — `'drifting'` iff any week `base_rate < 0.8*overall` OR `> 1.2*overall` (strict, multiplicative), else `'stable'`; `null` when fewer than 2 populated weeks.
- `cmd_profile` gains `--unit` and `--target` argparse flags with help text, wired into `profile_csv(unit=args.unit, target=args.target)`. The previously-deferred `unit=` wiring (added to `profile_csv` in 25-02 but not yet exposed on the CLI) is now connected too. Validation stays in `profile_csv`; the CLI is thin.
- Reference values confirmed on the real interpreter: drifting → overall=0.5, per-week rates [0.5, 0.25, 0.75], weekly_range=[0.25, 0.75], verdict='drifting'; stable → weekly_range=[0.5, 0.5], verdict='stable'; boundary → weekly_range=[0.4, 0.6], verdict='stable' (strict edge); single-week → verdict=null; non-binary (a 2) and yes/no both raise `CheckError` naming the offending value(s).

## Task Commits
1. **RED (both tasks):** `07e864a` — `test(25-03): add failing tests + fixtures for target block + CLI --unit/--target` (14 errors + 1 failure before implementation).
2. **Task 1 GREEN:** `93c0395` — `feat(25-03): target weekly base-rate block -- overall, weekly table, weekly_range, strict +/-20% verdict`.
3. **Task 2 GREEN:** `cbff9ea` — `feat(25-03): CLI --unit/--target flags wired into profile_csv with --help surface (D-03)`.

Branch: `gsd/v2.6.0-exploration-depth` (no branch created/switched; commits are plain `git commit`, unpushed by design — orchestrator re-verifies the gate and pushes).

## Verification
- `tests.test_profiler_hermetic.TestTargetBlock`: **12 tests OK** (Task 1 verify command).
- `tests.test_dsx.TestProfiler`: **6 tests OK** (Task 2 verify command; 2 pre-existing + 4 new).
- Full suite `-m unittest discover -s tests -q`: **1576 tests OK** on the real interpreter (`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`, 3.12.10) — 1560 (25-02 baseline) + 16 new. The pre-existing "DSX-*** declared twice" catalogue warnings are unrelated (no finding codes or gate modules touched).
- `git diff --name-only bada1ba..HEAD -- dsx/checks/` → empty; the three commits touch only `dsx/profiler.py`, `dsx/cli.py`, `tests/`, and `tests/fixtures/profiler/`.
- Deletion check across all three commits: none (285 insertions, 0 deletions).

## Deviations from Plan
None — the two tasks executed exactly as written; every reference value matched on first GREEN, and the boundary float-equality held under `assertEqual` (exact-Fraction `statistics.mean`), so no move to `assertAlmostEqual` was needed.

One clarification carried (not a deviation): `overall` is computed over all non-null-target rows while the weekly table buckets only rows whose time cell parses. In every reference fixture the two populations coincide (all target rows are dated); the split is documented in key-decisions for a future partially-dated extract.

## Prohibitions honored
- Zero new finding codes; no gate module touched (`dsx/checks/` diff empty).
- Stdlib-only — no pandas/numpy/scipy or any non-stdlib import added (`statistics`, `csv`, `re`, `datetime`, `collections.Counter` already imported).
- Binary target validation is a closed check against `{"0","1"}` — yes/no/true/false rejected; no truthy/falsy coercion reused; the error lists every distinct offending value.
- `target` block appended last (after unit / `sentinels_found`), never interleaved; omitted (not null) when the flag is absent, so the 25-01/25-02 no-flag golden stays byte-identical.
- `--target` hard-requires `--time`; `CheckError` maps to CLI exit 2 (EXIT_ERROR).
- ISO-week bucketing via `date.isocalendar()`, never manual `//7`.
- No branch created or switched — all commits on `gsd/v2.6.0-exploration-depth` via plain `git commit`.
- No edits to REQUIREMENTS.md, STATE.md, ROADMAP.md, LOOP-LEDGER.md, LOOP-BRIEF.md, or HUMAN-QUEUE.md (single-writer — orchestrator owns those).

## Known Stubs
None.

## Next Phase Readiness
- The full trust-core vocabulary (numeric, categorical, time, unit, target) is now produced by `profile_csv` and reachable from `dsx profile` via `--unit`/`--target`. 25-04 (doc ripple: `templates/DATA-PROFILE.yaml`, `references/data-quality-assertions.md`, `skills/dsx-explore-data/SKILL.md`, installer re-sync) can proceed against a stable producer surface.
- Phase-end gates remain for the orchestrator: catalogue set-identity 276→276, `dsx/checks/dq.py` + assertion vocabulary + gate profiles byte-unchanged (prove the DQ gate ignores the new `target`/`unit` keys), example profiles byte-invariant, `node install.mjs --check`, full suite on the real interpreter.
- No blockers.

---
*Phase: 25-hermetic-profile-depth*
*Completed: 2026-09-07*

## Self-Check: PASSED

All 6 fixtures + `dsx/profiler.py`, `dsx/cli.py`, `tests/test_profiler_hermetic.py`, `tests/test_dsx.py`, and this SUMMARY confirmed present. All 3 task commit hashes (`07e864a`, `93c0395`, `cbff9ea`) confirmed present in `git log`. `dsx/checks/` diff confirmed empty.
