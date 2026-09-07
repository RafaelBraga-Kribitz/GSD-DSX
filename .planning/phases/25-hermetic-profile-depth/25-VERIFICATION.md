---
phase: 25-hermetic-profile-depth
verified: 2026-09-07T04:55:00Z
status: passed
verdict: PASSED
score: 3/3 requirements MET (REQ-P25-01/02/03); all four hard invariants proven; 3 review findings dispositioned (2 fixed, 1 accepted residual documented)
behavior_unverified: 0
overrides_applied: 0
re_verification: false
gaps: []
human_verification:
  - "End-of-phase security sign-off (S1-5 /gsd-secure-phase 25) — batched to HUMAN-QUEUE, non-blocking until S7-2 per brief §6."
  - "End-of-phase UAT round (S1-5 /gsd-validate-phase 25) — batched, non-blocking until S7-2."
  - "HQ-40 40a (Hyndman & Fan 1996 type-number primary read) — non-blocking: the quantile choice is a definition test with a hand-computed reference value, not a minted code; the plan pinned method='inclusive' = type 7 and the reference values are proven live. The citation's type-number authenticity remains the human's read."
---

# Phase 25: Hermetic profile depth — Verification Report

**Phase Goal:** `dsx profile` computes, stdlib-only and additively, the trust-core numbers the
explore protocol currently asks the agent to compute — per-column numeric/categorical blocks,
time-block depth, a declared `--unit` block and a declared `--target` weekly base-rate block —
with every pre-existing key and value byte-stable, every statistic a declared definition with a
cited source and a reference-value test, zero new finding codes, and the doc surface + installed
copies re-synced.

**Verified:** 2026-09-07 (orchestrator, gates re-run on real Python 3.12.10)
**Status:** passed — 3/3 requirements MET

## Verdict

`passed`. All three phase requirements are met, all four hard invariants are proven by
independently re-run gates (not trusted from a subagent report), and the code review's three
findings are dispositioned: two fixed in this unit (S1-4), one accepted as a documented residual
with its reasoning recorded. No HIGH findings. No requirement is provisional.

## Requirement verdicts

### REQ-P25-01 — MET
`dsx profile` computes, stdlib-only, additively, the full trust-core set into `DATA-PROFILE.yaml`:
per numeric column `min/q1/median/q3/max/mean/sd/n_zero/n_negative/n`; per categorical column
`share_top1/share_top10/rare_share/n_singleton`; on the time column `rows_per_day {min,median,max}`,
`first_period_ratio`, `last_period_ratio`, `share_at_hour_00`; on a declared `--unit` column
`rows_per_unit {p50,p95,max}` + `largest_unit_share`; on a declared `--target` column the weekly
base-rate table with `overall`, `weekly_range` and the ±20 % `verdict`. Evidence: `TestNumericBlock`,
`TestCategoricalBlock`, `TestTimeBlock`, `TestUnitBlock`, `TestTargetBlock` all green in the full
suite (1583 OK); reference values independently re-derived by the reviewer and by the orchestrator
(q1/median/q3 = 3.25/5.5/7.75, sd = 3.0276503540974917; unit p50/p95 = 3/80.8; edge ratios 0.2/0.1).
Additivity: all new blocks are flag-gated (`--time`/`--unit`/`--target`); the no-flag output shape is
frozen and guarded by `test_pre_existing_keys_match_golden`.

### REQ-P25-02 — MET
Every statistic is a declared definition with a cited source and a reference-value test on a
hand-computed fixture. The quantile method is pinned to `statistics.quantiles(..., method="inclusive")`
= Hyndman & Fan (1996) **type 7**, triangulated at plan time against the installed CPython 3.12.10
`statistics.py` source and the R type-6/7 identity (25-RESEARCH.md); `sd = statistics.stdev` (n-1);
`mean`/`stdev` use exact-Fraction accumulation (order-independent). Two runs on the same extract are
byte-identical (`test_two_runs_are_byte_identical`); the committed example profiles regenerate
identically on every pre-existing key (`test_pre_existing_keys_match_golden`) and match their pinned
sha256 digests over raw CRLF bytes (`test_example_profiles_match_pinned_digests`). The H&F
type-**number** primary-source read (HQ-40 40a) is non-blocking — it is a definition, not a minted code.

### REQ-P25-03 — MET
`templates/DATA-PROFILE.yaml`, `references/data-quality-assertions.md` and
`skills/dsx-explore-data/SKILL.md` (steps 1a, 3a, 4a, 4b, 4e, 4f) say "copied from the profile" where
the profiler now supplies the number, with the named exclusions (null cross-tabs, outlier taxonomy,
impossible pairs, robust metric recomputes) left to the agent. `dsx/checks/dq.py`, the
`data[].assertions` vocabulary and the gate profiles are byte-unchanged (phase-base diff empty for
`dsx/checks/` and `references/finding-codes.md`). Zero new codes: catalogue set-identity **276 → 276**,
re-measured live (`gen-finding-catalogue.py --check` → "finding catalogue is current"; 276 rows counted).
`node install.mjs --check` passed at S1-3 (5 gates, 14/14 skills, 6/6 agents) and no `skills/`,
`templates/` or `references/` file changed in S1-4, so the installed copies remain in sync.

## Hard-invariant proof (gates re-run by the orchestrator on real 3.12.10)

| Invariant | Evidence | Result |
|---|---|---|
| Full test suite green | `python312 -m unittest discover -s tests -q` | **Ran 1583 tests — OK** (+1 = the S1-4 empty-flag test) |
| Determinism / byte-stability | exact-Fraction mean/stdev; every tie has an explicit total-order key (`(-count,label)`, `(iso_year,iso_week)`); no `Counter.most_common()` on any output path; shuffle tests pass for time/unit/target; `test_two_runs_are_byte_identical` | PASS |
| Existing keys byte-stable | example profiles diff empty vs committed; `test_pre_existing_keys_match_golden` + pinned-digest test green | PASS |
| Quantile / stat definition | `method="inclusive"` (type 7) in numeric + unit blocks; `sd = statistics.stdev` (n-1); no `exclusive` default anywhere | PASS |
| `dsx/checks/dq.py` byte-identical | `git diff b739009 -- dsx/checks/ references/finding-codes.md` empty | PASS |
| Catalogue set-identity 276 → 276 | `gen-finding-catalogue.py --check` "current"; 276 rows | PASS |
| No gate coupling | `profiler.py` imports only `CheckError`; nothing touches the gate path | PASS |

## Code review disposition (`25-REVIEW.md` — 0 HIGH / 1 MEDIUM / 2 LOW)

- **M-01 (test-efficacy) — FIXED.** `test_top10_tie_boundary_count_desc_then_string_asc` claimed to
  pin the count-desc/string-asc tie-break, but `share_top10` is a sum of the top-10 counts and the two
  boundary levels tie at count 5, so the result is identical under any tie order — and no
  `_categorical_block` aggregate can observe the tie-break at all. Renamed to
  `test_top10_truncates_at_ten_with_boundary_tie` with an honest docstring stating it pins top-10
  *truncation* at a boundary tie and that the frozen tie-break is unobservable determinism insurance.
  The code is correct and deterministic (the outputs are deterministic *because* they are
  tie-order-independent); only the test's over-claim was removed.
- **L-02 (empty-string flag) — FIXED.** `--unit ""` / `--target ""` were falsy-but-not-None:
  truthiness validation guards were skipped while identity emission guards fired, so `--target ""` with
  no `--time` emitted a degenerate all-null block instead of behaving as "not declared." Fixed by
  coercing `unit = unit or None` / `target = target or None` at the top of `profile_csv` (covers all
  callers, not just the CLI). Pinned by the new `test_empty_flag_values_treated_as_absent`
  (discriminating: fails before the coercion, passes after).
- **L-01 (verdict baseline population) — ACCEPTED RESIDUAL, documented.** `target.overall` is the base
  rate over all non-null-target rows, whereas the weekly rates and the drift `verdict` cover only
  rows whose time cell parsed. When every target row has a parseable timestamp (the shipped case) the
  populations coincide; a material fraction of untimed target rows would draw the drift baseline from a
  superset of the weekly population. This is a producer heuristic, never a gate input, and no shipped
  fixture exercises it. A clarifying comment was added at the verdict site making the population choice
  explicit; a semantic redefinition of `overall` (or a separate parseable-time denominator) is
  deliberately deferred rather than rushed in this firing. Recorded as a candidate follow-up.

## Human Verification Required

Batched, non-blocking until S7-2 (per brief §6): the Phase 25 `/gsd-secure-phase 25` security
sign-off and `/gsd-validate-phase 25` UAT round (both S1-5), and the HQ-40 40a H&F type-number
primary-source read (a definition, not a mint). None gate this `passed` verdict.

---

_Verified: 2026-09-07 by the autonomous ceremony orchestrator (gates re-run on real Python 3.12.10)._
