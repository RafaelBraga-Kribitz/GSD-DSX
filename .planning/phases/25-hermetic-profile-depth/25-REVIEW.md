---
phase: 25-hermetic-profile-depth
reviewed: 2026-09-07T04:30:38Z
depth: deep
scope: dsx/profiler.py, dsx/cli.py (runtime); tests/test_profiler_hermetic.py, tests/test_dsx.py (discrimination)
diff_base: b739009
findings:
  high: 0
  medium: 1
  low: 2
  total: 3
status: issues_found
---

## Verdict: 3 findings (0 H / 1 M / 2 L)

No HIGH findings. The four hard invariants hold: determinism/byte-stability, type-7
(`inclusive`) quantiles + sample `stdev`, additive-only keys, and no gate coupling.
The three findings are a non-discriminating test (M) and two low-severity edge gaps (L).

Reference values independently re-derived and confirmed correct:
`_numeric_block(1..10)` q1/median/q3 = 3.25/5.5/7.75, sd = 3.0276503540974917;
`time_edge_ratio` weeks [2,10,10,10,10,1] → first 0.2 / last 0.1, max_gap 7;
`unit_counts` [1,2,3,4,100] → p50 3 / p95 80.8 / share 100/110; `target_boundary`
rates {0.4,0.6,0.5} vs 0.4/0.6 strict → stable. All match the pinned test values.

---

## Invariant verification (all pass)

1. **Determinism.** `statistics.mean`/`stdev` use exact-Fraction accumulation
   (order-independent). Every ordering with a tie has an explicit total-order key:
   categorical `sorted(key=lambda kv:(-count,label))`, week buckets
   `sorted(key=lambda kv:kv[0])` over `(iso_year, iso_week)`, unit ranking
   `sorted(key=lambda kv:(-count,unit))`. No `Counter.most_common()` on any output
   path. Float rendering is fixed `.6f`-strip. Shuffle tests pass for time/unit/target.
2. **Quantile / stat definition.** `statistics.quantiles(..., n=4, method="inclusive")`
   (numeric) and `n=100, method="inclusive"` (unit) — type 7, no `exclusive` default
   anywhere. `sd = statistics.stdev` (n-1). `rows_per_day.median` is `statistics.median`
   (a median, not a mis-declared quantile). Unit p50=cuts[49], p95=cuts[94] index the
   50th/95th of 99 cut points correctly.
3. **Additive keys.** numeric/categorical appended LAST under each column; four new
   `time.*` keys appended after `max_gap_days`; `unit`/`target` appended after
   `sentinels_found`. All new blocks gated on their flag; no-flag output shape frozen.
   Pinned byte-digest test + golden pre-existing-key test guard against mutation.
4. **No gate coupling.** `profiler.py` imports only `CheckError` from `.findings`.
   Nothing in the diff touches `dsx/checks/dq.py` or the gate path.

## Narrative Findings (AI reviewer)

### M-01 — Non-discriminating test: `test_top10_tie_boundary_count_desc_then_string_asc`
**File:** `tests/test_profiler_hermetic.py:150-157` (fixture `categorical_top10_tie.csv`)
**Claim:** The test asserts `share_top10 == (99+5)/109` and its docstring claims a
`Counter.most_common()` insertion-order tie-break "would wrongly include 'n' instead" of
"m". That is false. `share_top10` is the SUM of the top-10 counts divided by n. The two
boundary levels tie at count 5 (`m`=5, `n`=5), so whichever one fills the 10th slot
contributes exactly 5 — the sum, and therefore `share_top10 = 104/109`, is identical under
`most_common()`, under the frozen (count desc, label asc) rule, or under any tie order.
The test passes regardless of the code under test and does not exercise the frozen
tie-break at all.
**Deeper point:** No output of `_categorical_block` can discriminate the tie-break —
`share_top1` (max count), `share_top10` (sum of top counts), `rare_share` and
`n_singleton` are all count aggregates invariant to tie order. The frozen tie-break in
`_categorical_block` (and the identical one in the unit block) is therefore unobservable
via any emitted value. This is not a correctness or determinism defect (the outputs are
deterministic precisely because they are tie-order-independent), but the test gives false
confidence that a determinism-critical ordering is pinned when it structurally cannot be.
**Fix:** Either (a) drop the overstated docstring claim and re-label the test as a
`share_top10` boundary-sum check, or (b) if the intent is to pin the tie-break, expose a
tie-order-sensitive output (e.g. a `top_levels` label list) and assert on it — otherwise
no fixture can distinguish the rule from `most_common()`.

### L-01 — `target.overall` and weekly base rates are computed over different row populations
**File:** `dsx/profiler.py:412-413` vs `dsx/profiler.py:283-286, 416-422`
**Issue:** `overall = statistics.mean(binary_all)` is taken over `target_all` — every
non-null-target row, INCLUDING rows whose time cell fails `_parse_date`. The weekly table
and thus the `verdict` comparison (`r < 0.8*overall or r > 1.2*overall`) are built only
from rows whose time parsed. If a non-trivial share of rows carry a non-null target but an
unparseable time cell, `overall` is drawn from a superset of the weekly population, so the
drift verdict compares weekly rates against a baseline they were never part of — a run can
read `drifting` while every parseable week is internally stable (or vice-versa). The
counting rule is documented in the inline comment, but the *verdict* consequence is not,
and no fixture exercises it (all target fixtures have fully-parseable time), so it is not
test-pinned as intended behavior.
**Fix:** For a skeptical-statistician artifact, either compute `overall` over the same
parseable-time rows that populate the weekly buckets, or add an explicit
`overall_time_parseable` denominator so the drift comparison and its baseline share one
population. At minimum add a fixture with non-null targets on unparseable-time rows to pin
whichever choice is intended.

### L-02 — Empty-string `--unit ""` / `--target ""` bypasses validation but still emits a null block
**File:** `dsx/profiler.py:209, 213-216, 379, 402`
**Issue:** The guards use truthiness (`if unit and ...`, `if target and not time_column`)
while block emission uses identity (`if unit is not None:`, `if target is not None:`). An
explicit empty-string flag value (`dsx profile x.csv --target ""`) is falsy-but-not-None:
the column-existence check and the `--target requires --time` check are both skipped, yet
the emission guard fires. Result: `dsx profile x.csv --target ""` produces an all-null
`target:` block with NO `--time` and no error, and `--unit ""` emits an all-null `unit:`
block for a column name that was never validated against the header. Low severity — it
requires the operator to pass a deliberate empty string — but it is an inconsistent
validation/emission contract.
**Fix:** Normalize empty strings to `None` in `cmd_profile` (e.g.
`unit=args.unit or None`, `target=args.target or None`), or switch the emission guards to
the same truthiness test used by the validation guards.

## Notes (not findings)

- **Numeric block over integer columns** stores `float(stripped)`, so `min`/`max` are
  floats (e.g. `1.0`); `_scalar` renders them identically to the integer form (`1`) and
  `assertEqual(1.0, 1)` holds, so this is cosmetically and byte-invariant. No action.
- **`statistics.mean` return type** is `int` for all-equal binary weeks (e.g. an all-`1`
  week → `int 1`) and `float` otherwise; both render identically and are stable per file.
  No determinism impact.
- **dtype-driven block selection** depends on `_infer_dtype` over the first 50 samples
  (pre-existing cap). This is stable for a fixed extract (the invariant's definition of
  determinism) and only varies across *different* row orderings of a genuinely-mixed
  column — out of scope for same-extract byte-stability.

---

_Reviewed: 2026-09-07T04:30:38Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: deep_
