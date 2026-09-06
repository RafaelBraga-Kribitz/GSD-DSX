# Phase 25: Hermetic profile depth — Context

**Milestone v2.6 Exploration Depth and Backlog Evidence · S1-1 discuss · 2026-09-06
(autonomous firing).** The foundation phase of the milestone: `dsx profile` grows to
produce, stdlib-only and hash-bound, the trust-core numbers the EDA explore protocol
currently asks the agent to compute, so `EDA.md` copies them ("never invent profile
numbers") and two runs over one extract carry identical numbers by construction.
Phase 25 **hard-blocks Phase 26** (the per-skill read contracts name the keys this
phase produces). Requirements: REQ-P25-01 … REQ-P25-03 (3). Phase 25 **mints zero
new finding codes** (REQ-P25-03, set-identity diff vs the S0-2 re-measured **276**
baseline); every change is additive, and `dsx/checks/dq.py`, the `data[].assertions`
vocabulary and the gate profiles stay **byte-unchanged**.

## Phase Boundary

The profiler is a **producer, not a gate** (milestone constraints D-01 stdlib-only /
D-02 declarations-only). **No new gate code, no gate reads a new profile key this
milestone, no pandas/numpy/scipy anywhere** — the profiler is `stdlib` and the gate
path stays untouched. Growing the assertion vocabulary so a gate could *compare* a new
key (e.g. `max_skew`) is a separate, later D-06 decision, explicitly out of scope here.
The new numbers are **additive keys**; existing profile keys and values are
**byte-stable**; two runs on the same extract are **byte-identical**. Every statistic
is a **declared definition with a cited source and a reference-value test** on a
hand-computed fixture CSV.

**In-scope code:** `dsx/profiler.py` (`profile_csv` grows the additive keys and gains
`unit`/`target` parameters; the date parser retains the hour component it currently
drops), `dsx/cli.py` (`cmd_profile` gains `--unit`/`--target` and help text), new
`tests/fixtures/profiler/` + reference-value/determinism/golden tests.
**Ripple (docs only):** `templates/DATA-PROFILE.yaml`, `references/data-quality-assertions.md`,
`skills/dsx-explore-data/SKILL.md` steps 1a/3a/4a/4b/4e/4f (say "copied from the
profile" where the profiler now supplies the number), installer re-sync.
**Frozen (must be proven byte-unchanged):** `dsx/checks/dq.py`, the `data[].assertions`
vocabulary, the gate profiles; catalogue set-identity **276 → 276**.

## Ground truth read this firing (assumptions mode)

Live structures read in full this firing:

- **`dsx/profiler.py::profile_csv`** — current return dict: `profile_version,
  computed_by, source_path, source_hash, row_count, columns{<col>:{null_rate,
  n_unique,dtype}}, primary_key, primary_key_unique, duplicate_rate,
  time{column,min,max,max_gap_days}, sentinels_found`. YAML is emitted by a hand-rolled
  stdlib `_dump`/`_scalar` that walks dicts in **insertion order** — so byte-stability
  of pre-existing keys holds **iff every new key is *appended* after the existing ones**
  in each mapping (additive = append, never interleave). `_scalar` already maps
  `NaN`/`inf` → `"null"` and renders floats via `f"{v:.6f}".rstrip("0").rstrip(".")`.
  `_parse_date` currently **drops** the optional `H:M:S` its regex captures.
- **`dsx/cli.py::cmd_profile`** — current flags: `csv` (positional), `--out/-o`,
  `--pk` (comma-split), `--time`, `--sentinel` (repeatable, int/float/str coerced),
  `--json`. Unknown `--pk`/`--time` columns raise `CheckError` (profiler L123-127).
- **`skills/dsx-explore-data/SKILL.md`** — the definitions the profiler must match:
  1a (`rows_per_unit` p50/p95/max, `largest_unit_share`); 3a (staleness [needs TODAY],
  first/last edge-period ratio "at the reporting grain", `share_at_hour_00 > 0.9` =
  "a date wearing a timestamp's clothes"); 4a (five-number + mean; robust half
  excluded); 4b (concentration on additive measures); 4e (`rare_share` = levels with
  <10 rows or <0.1%, `singleton_levels`); 4f (weekly base rate, `overall`,
  `weekly_range`, `verdict` drifting at ±20% relative).
- **Byte-stability guard reality:** there are **no source CSVs** in `examples/` and
  **no `tests/fixtures/profiler/`** today. `examples/good-DATA-PROFILE.yaml` is
  `computed_by: measured_export` (a FAKE sha256, 38412 rows, `source_path:
  warehouse.fct_signups`) and `examples/bad-DATA-PROFILE.yaml` is `computed_by: manual`.
  **Neither is `dsx profile` output**, so neither can literally be "regenerated" by the
  profiler — this shapes D-04.

## Persona round (LOOP-BRIEF §4)

**Architect** (`dsx-analysis-architect`) + **Statistician** (`dsx-statistician`), both
opus/high, spawned in parallel against the S0-verified ground truth (facts handed in so
neither re-explored — token discipline). The **Auditor is not separately engaged**: the
only integrity concerns (byte-stability, zero-codes set-identity, no-gate-reads-a-new-key)
are structural and are carried as explicit verification gates in D-04/"bound to" below,
not adjudicated by judgement. Tie-break **rigour > reliability > flexibility**.

The round **converged** on nesting, CLI shape, the guard shape, and every edge
convention, and **diverged on three points**, each resolved below by the tie-break:

1. **Quantile method — inclusive/type-7 (Statistician) vs the scope's parenthetical
   exclusive/default lean.** On pure rigour the two stdlib methods are a wash (both are
   legitimate Hyndman & Fan types; the type H&F actually recommend — type 8 — is not
   offered by `statistics`). Tie breaks on **reliability**: a "trust-core" number a
   sceptical statistician re-checks in pandas / numpy / R (all default to type 7) should
   **byte-agree** with those tools; type 7 also avoids exclusive's endpoint clamping.
   **Adopted: inclusive / type 7.** (Overrides HQ-40 row 40a's *parenthetical* "default
   = exclusive" assumption — the scope itself left the method open, "verified at plan
   time, not assumed". The human read of HQ-40 40a still confirms the type *number*; it
   already tabulates both mappings, so the choice does not change what the human checks.)
2. **Edge-period grain — ISO-week (Statistician) vs calendar day (Architect).** The
   ratio exists to detect **truncated edge periods** for trend statements; at day-grain
   an event extract's last day is almost always cut mid-day, so the ratio fires
   "partial" near-constantly → low information. **Rigour** favours ISO-week (populated
   weeks only, `<5` populated weeks → `null`). `rows_per_day` stays day-grain (it is a
   volume-shape stat, a different purpose). **Adopted: ISO-week.**
3. **`share_at_hour_00` on date-only data — null (Statistician) vs count-as-midnight.**
   A date-only value carries **no clock evidence**; counting it as hour 00 would make
   every genuine date column read `1.0` and false-flag it as "a date wearing a
   timestamp's clothes". **Adopted: denominator = rows carrying a time token; `null`
   when no row carries one.** (Requires retaining the hour before `_parse_date` drops it.)

## Decisions (loud, vetoable — LOOP-BRIEF §4; silence = accept, no code minted so no D-06 veto item)

- **D-01 — Additive key names & nesting (REQ-P25-01/02):** dtype-conditional stats nest
  under a named sub-map inside `columns[<col>]`, appended after `dtype` — `numeric:`
  present only for `integer`/`float`, `categorical:` present only for `string`/`mixed`;
  the new time stats append under the existing `time:` block; `unit:` and `target:` are
  **new top-level blocks omitted entirely when their flag is absent** (never emitted as
  `null`). Every new key is appended last so `_dump`'s insertion-order output leaves
  pre-existing bytes identical.
- **D-02 — Statistical definitions & hermeticity pins (REQ-P25-02):** quantiles via
  `statistics.quantiles(..., method='inclusive')` = **H&F type 7** (type number pinned
  against the paper at S1-2 plan research, per REQ-P25-02 — believed type 7, not
  asserted); `median` taken from the same `quantiles(n=4)` call, with a fixture guard
  that it equals `statistics.median`; `sd` = **sample sd (n−1)** via `statistics.stdev`;
  every undefined statistic emits JSON **`null`, never `0` or `NaN`**; staleness is
  **excluded as non-hermetic** (needs wall-clock TODAY). Full edge vocabulary below.
- **D-03 — `--unit`/`--target` CLI flags & validation (REQ-P25-01):** `--unit <col>`
  and `--target <col>`, single column each; absent → block omitted; **`--target`
  hard-requires `--time`** (raise `CheckError` otherwise) and its values must be
  **binary {0,1}** (non-binary → `CheckError` listing the offending values; `yes/no/
  true/false` NOT accepted); unknown header → `CheckError`, matching `--time`/`--pk`.
- **D-04 — Byte-stability guard shape + REQ-P25-02 recorded interpretation
  (REQ-P25-02):** Option B — commit small hand-computed CSVs under
  `tests/fixtures/profiler/`; the guard is (1) a **reference-value** test (`dsx profile`
  output equals hand-computed exact numbers), (2) a **determinism** test (two runs
  byte-identical), (3) a **pre-existing-key golden** (today's keys unperturbed by the
  additive change), and (4) the `measured_export`/`manual` example profiles kept
  **byte-invariant in git** and still passing their DQ gates. **Recorded interpretation:**
  because the example profiles are non-producer stand-ins, "the committed example
  profiles regenerate identically on every pre-existing key" (REQ-P25-02) is
  operationalised as (4) [example bytes invariant] + (3) [producer invariance proven on
  the fixtures `dsx profile` can actually produce]. This **operationalises, it does not
  reword**, the requirement — flagged for human ratification at the S1-2 plan gate;
  non-blocking.

### D-02 — the full edge / hermeticity vocabulary (frozen this firing, reference-tested at execute)

Every number is a pure function of the CSV bytes — no wall-clock, no locale, no
timezone, stable tie-breaks, no rounding beyond `_scalar`'s existing float format.

- **Numeric column** (`integer`/`float`): `min, q1, median, q3, max` (type-7 quantiles),
  `mean` (`statistics.mean`), `sd` (`statistics.stdev`, n−1), `n_zero` (parsed value
  `== 0`; collapses `0`/`+0`/`-0`/`0.0`), `n_negative` (parsed value `< 0`; `-0` is NOT
  negative), and **`n`** (non-null parseable-numeric count — an additive extra beyond
  the scope's enumerated list, included because it is the denominator that makes the
  null conventions and `n_zero`/`n_negative` interpretable; recorded as a deliberate,
  vetoable addition). Comparisons are on **parsed values**, never strings.
  Small-n: `n==0` → all stats `null`, counts `0`; `n==1` → min=max=q1=median=q3=mean=the
  value, `sd=null`; `n>=2` → all defined.
- **Categorical column** (`string`/`mixed`): `share_top1` = share of non-null rows in
  the single most-frequent level; `share_top10` = share in the top-10 levels by
  frequency (**tie-break: count desc, then level string asc**; `<10` levels → `1.0`);
  `rare_share` = share of rows in levels with **count < 10 OR count/N < 0.001** (both
  strict); `n_singleton` = count of levels with exactly 1 row. Denominator = non-null
  rows; **levels are exact raw strings** (no trim, no case-fold, no collation).
- **Time block** (additive under `time:`): `rows_per_day {min, median, max}` (counts per
  calendar day, day-grain); `first_period_ratio`/`last_period_ratio` at **ISO-week**
  grain over populated weeks (last = rows(last populated week) ÷ mean(previous 4
  populated weeks); first symmetric on the next 4; `<5` populated weeks → `null`);
  `share_at_hour_00` = share of **time-bearing** rows whose hour == 0 (`null` when no
  row carries a time token).
- **`--unit` block:** `rows_per_unit {p50, p95, max}` (type-7 quantiles over per-unit
  row counts; `<2` distinct units → p50/p95 `null`, max defined for ≥1),
  `largest_unit_share` = rows(most-frequent unit) ÷ total (tie-break count desc, unit
  string asc — does not change the value).
- **`--target` block:** week bucket = `(iso_year, iso_week)` from `date.isocalendar()`
  (deterministic, locale-free) on the `--time` column; `overall` = mean of target over
  non-null-target rows; a **weekly table** of `{week, n, base_rate}` rows (the "weekly
  base-rate table" REQ-P25-01 names, per skill 4f — includes per-week `n`);
  `weekly_range [min_week_rate, max_week_rate]`; `verdict='drifting'` iff any
  `week_rate < 0.8·overall` **or** `> 1.2·overall` (strict; multiplicative to dodge
  divide-by-zero — `overall∈{0,1}` → stable), else `'stable'`; `<2` populated weeks →
  `verdict=null`.

### Named exclusions (REQ-P25-01/03 — recorded with reasons, not omissions)

- **null cross-tabs vs the target** (skill step 2) — target-informed and split-first;
  a null pattern read off the full frame is target-informed cleaning. Stays agent-side.
- **outlier taxonomy** (4c) — needs categorical search and time windows; judgement-shaped.
- **impossible pairs / invariants** (4d) — needs invariants the analyst enumerates.
- **robust metric recomputes** (4a second half — trim10/mad/loc_gap/scale_ratio and
  metric recomputes) — need the metric definition; judgement-shaped.
- **staleness** (3a) — needs wall-clock TODAY; **non-hermetic**, disqualified from the
  producer. The profiler already emits the hermetic *input* (`time.max`), so the agent
  computes `today − max` itself without the profiler ever touching a clock.

## Reference values the fixture tests must hard-code (from the Statistician; pin exact float reprs at execute)

- `quantiles([1..10], n=4, inclusive)` → **q1=3.25, median=5.5, q3=7.75**;
  `exclusive` → 2.75 / 5.5 / 8.25; `statistics.median([1..10])=5.5` (== middle
  quantile under both methods — desync guard).
- numeric `[1..10]`: min=1, max=10, mean=5.5, **sd=sqrt(82.5/9)=3.0276503540974917**,
  n=10, n_zero=0, n_negative=0.
- zeros/negatives `[-2.0, -0, 0, 0.0, 5]`: n_negative=1, n_zero=3, min=-2.0, max=5, n=5.
- n=1 → sd=null, all quantiles=mean=the value; n=0 → all stats null, counts 0.
- categorical (A×50,B×30,C×15,D×4,E×1; N=100): share_top1=0.5, share_top10=1.0,
  rare_share=0.05, n_singleton=1.
- categorical percent-arm (N=20000, one level=15 rows): that level **is rare**
  (15/20000=0.00075 < 0.001) though 15 ≥ 10.
- categorical top-10 tie boundary (#10 "m" and #11 "n" both count 5): "m" in top10,
  "n" out (count desc, string asc).
- `share_at_hour_00`: all-`T00:00:00` (10 rows) → 1.0; 5×`00:00`+5×`13:00` → 0.5; all
  date-only → null; 2 date-only + 3 timed (1 midnight) → 1/3 = 0.3333333333333333.
- `rows_per_day` day counts [1,3,5,7,9]: min=1, median=5, max=9.
- first/last_period_ratio (ISO-week populated counts W1..W6=[2,10,10,10,10,1]):
  first=0.2, last=0.1; ≤4 populated weeks → both null.
- `rows_per_unit` (unit counts [1,2,3,4,100]): p50=3, max=100,
  largest_unit_share=100/110=0.9090909090909091, p95 = type-7 interpolation (pin exact
  repr from an actual run).
- `--target` drifting (W1 [1,1,0,0], W2 [1,0,0,0], W3 [1,1,1,0]): overall=0.5,
  weekly_range=[0.25,0.75], verdict='drifting'.
- `--target` stable (three weeks each rate 0.5): overall=0.5, weekly_range=[0.5,0.5],
  verdict='stable'.
- `--target` boundary (overall=0.5, week rates {0.4,0.6,0.5}): verdict='stable' (±20%
  boundary strict/exclusive).
- `--target` single week: verdict=null; non-binary target (contains a 2): error.

## What Phase 25 plan (S1-2) and execute (S1-3) are now bound to

1. **Plan research (S1-2) pins the H&F type number** against the paper + CPython docs
   before any test asserts a quantile (REQ-P25-02); confirms `statistics.mean/stdev`
   accumulate order-independently (byte-stable across platforms); ratifies the D-04
   interpretation at the plan gate. Plan-checker must pass (confirm Dimension-7 Context
   Compliance, not the known-false-blocking decision-coverage regex — HUMAN-QUEUE
   standing note).
2. **Execute (S1-3):** grow `profile_csv` (additive keys per D-01/D-02; retain the hour
   in the date parser; add `unit`/`target` params); add `--unit`/`--target` to
   `cmd_profile` (D-03); write `tests/fixtures/profiler/` CSVs + the reference-value,
   determinism, and pre-existing-key-golden tests (D-04); ripple the three doc files;
   `node install.mjs` re-sync.
3. **Phase-end gates (S1-4/S1-5), run by the orchestrator, not trusted from a report:**
   catalogue set-identity **276 → 276** (zero codes); `dsx/checks/dq.py` + assertion
   vocabulary + gate profiles byte-unchanged (prove the DQ gate ignores the new keys —
   check for a `dsx profile --help` snapshot/golden test before claiming CLI output
   byte-stability); example profiles byte-invariant in git; `node install.mjs --check`
   passes; full suite on the **real** interpreter
   (`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`).

## Open questions / carried caveats

- **Veto window (non-blocking, silence = accept):** D-01 nested `numeric`/`categorical`
  sub-maps (flat siblings were the Architect's acceptable fallback); **D-02 quantile
  method = inclusive/type-7** (overrides the scope's parenthetical exclusive lean —
  the most likely operator touch-point); D-02 the additive **`n`** key and per-week `n`
  beyond the scope's enumerated lists; the **D-04 REQ-P25-02 interpretation** (flagged
  for plan-gate ratification). Recorded here + in one ledger line; no code minted, so no
  HQ D-06 veto item is owed.
- **HQ-40 row 40a (Hyndman & Fan):** non-blocking for this phase (a definition test, not
  a mint); the plan pins the type. The human read confirms the type *number* for the
  inclusive method (= type 7); the row already tabulates both mappings.
- **Frozen-vocabulary risk:** the additive column sub-maps flow into a file the DQ gate
  parses — the plan/execute must **prove** the gate ignores unknown keys (a test), not
  assume it. Carried into S1-4's verification.
