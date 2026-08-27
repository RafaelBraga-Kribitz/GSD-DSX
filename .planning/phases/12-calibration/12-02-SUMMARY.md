---
phase: 12-calibration
plan: 02
subsystem: dsx-cli
status: complete
tags: [reader, paradigm-split, decision-trail, calibration]
requires: [dsx.decisions.read_all, dsx.decisions.frame_digest, dsx/frame/paradigm.py::choice="paradigm=…"]
provides: ["dsx stats --paradigm (operator paradigm split reader)"]
affects: [dsx/cli.py, tests/test_cli_stats.py]
tech-stack:
  added: []
  patterns: [pure-reader-returns-0-by-construction, glob-discovery, allowlist-exclusion-by-path-component, distinct-frame-digest-dedup]
key-files:
  created: [tests/test_cli_stats.py]
  modified: [dsx/cli.py]
decisions: [D-12, D-13, D-14, D-18]
metrics:
  duration: ~25m
  completed: 2026-08-27
  tasks: 2
  files: 2
  commits: 4
requirements: [REQ-P12-04]
---

# Phase 12 Plan 02: dsx stats --paradigm Summary

`dsx stats --paradigm` — a pure-reader subcommand reporting the operator's own frequentist/Bayesian/undeclared frame split, deduplicated by distinct `frame_digest`, that hard-excludes the polluted `examples/**` and `templates/**` fixture floors, always exits 0, and mints no code and no gate registration.

## What Was Built

- **`dsx/cli.py::cmd_stats`** — reader modelled on `cmd_explain`'s structural safety: defensive root-resolution fallback, an inner `try/except Exception` around discovery-through-print (so `KeyboardInterrupt`/`SystemExit` propagate but every other failure degrades to an honest empty result), and `return 0` unconditionally. Never imports `Severity`, `GATE_THRESHOLDS`, or `Report`.
- **`dsx/cli.py::_discover_operator_trails`** — `Path(root).rglob("DECISIONS.jsonl")` with a D-13 hard-exclude predicate that drops any trail whose path passes through an `examples/` tree OR a `templates/` tree, matched by **path component** (not a single literal), so `examples/DECISIONS.jsonl`, `examples/known-bad/DECISIONS.jsonl`, and `templates/DECISIONS.jsonl` are all excluded.
- **`dsx/cli.py::_print_stats`** — text + `--json` (`json.dumps(..., indent=2, sort_keys=True)`) rendering; labels the raw invocation count as a secondary diagnostic.
- **`dsx/cli.py` `p_stats` subparser** — `--paradigm`, `--json`, `--root` (default `.planning`), `--verbose`; deliberately no `--block-on` and not routed through `add_common`.
- **`tests/test_cli_stats.py::TestCmdStats`** — 5 tests (see verification).

## How It Works (D-14 aggregation)

Per surviving trail, `read_all()` is reused (no reparsing). Invocation headers give `invocation_id -> frame_digest` (mapped per-file, since ids are only unique within one trail, WR-02); each `choice="paradigm=…"` decision record is tied back to its frame via `invocation_id`. One paradigm per distinct `frame_digest`; out-of-vocabulary values fold to `undeclared`. **Denominator = count of distinct `frame_digest`s**; raw invocation count is secondary. Zero surviving frames ⇒ honest "no operator history yet" message, never a divide-by-zero.

## Verification

Repo gate `bash scripts/check.sh`: **1205 tests OK**, finding catalogue current (**256**, unchanged), capability manifest conformant, gate contract + determinism pass — "all checks passed".

`python -m unittest tests.test_cli_stats -v` — all 5 green:
- `test_always_exits_zero` (empty + unreadable source) — ok
- `test_never_sources_the_known_bad_floor` (D-13) — ok
- `test_block_on_flag_is_rejected` (exit 2) — ok
- `test_dedup_is_by_distinct_frame_digest` (Bayesian share = 1/(N+1)) — ok
- `test_out_of_vocabulary_paradigm_folds_to_undeclared` — ok

CLI in this repo: `python -m dsx stats --paradigm` → "no operator history yet — no operator decision trails found under '.planning' (examples/ and templates/ excluded)." exit 0. `python -m dsx stats --paradigm --block-on high` → argparse "unrecognized arguments: --block-on high", exit 2.

Untouched (git diff `eaecc41..HEAD`): only `dsx/cli.py` + `tests/test_cli_stats.py` changed; `dsx/findings.py`, `references/finding-codes.md`, `CHECKS`, and `GATE_PROFILES` unchanged.

## Deviations from Plan

None — plan executed exactly as written. TDD gate sequence honored per task (RED `test(...)` commit → GREEN `feat(...)` commit).

## Commits

- `88c7bd5` test(12-02): failing reader-contract tests (Task 1 RED)
- `4030ef9` feat(12-02): dsx stats --paradigm reader with D-13 exclusion (Task 1 GREEN)
- `85f1c84` test(12-02): failing distinct-frame dedup + OOV tests (Task 2 RED)
- `3da1e94` feat(12-02): dedup paradigm split by distinct frame_digest (Task 2 GREEN)

## Known Stubs

None.

## Self-Check: PASSED

- `dsx/cli.py::cmd_stats`, `_discover_operator_trails`, `p_stats` present (verified via source read + live CLI run).
- `tests/test_cli_stats.py` exists; 5 tests pass.
- All four commit hashes present in `git log`.
