---
phase: 25
phase_name: "Hermetic profile depth"
project: "gsd-dsx"
generated: "2026-09-10"
counts:
  decisions: 6
  lessons: 6
  patterns: 6
  surprises: 5
missing_artifacts:
  - "UAT.md"
---

# Phase 25 Learnings: Hermetic profile depth

## Decisions

### D-01 — Additive key nesting & strict append-order
Dtype-conditional stats nest under a named sub-map inside `columns[<col>]` (`numeric:` only
for integer/float, `categorical:` only for string/mixed), appended **after** `dtype`; new
time stats append after the existing `time:` block; `unit:`/`target:` are new top-level
blocks **omitted entirely** when their flag is absent (never emitted as `null`). Every new
key is appended last so the hand-rolled insertion-order YAML emitter (`_dump`) leaves
pre-existing bytes byte-identical.

**Rationale:** `_dump` walks Python dicts in insertion order with no schema; byte-stability
of pre-existing keys holds *iff* every new key is appended, never interleaved. This is a
structural (code-shape) guarantee, not a convention to remember.
**Source:** 25-CONTEXT.md

### D-02 — Quantile method pinned to inclusive/type-7
Quantiles use `statistics.quantiles(..., method='inclusive')` = Hyndman & Fan type 7 (median
taken from the same `quantiles(n=4)` call, with a fixture guard that it equals
`statistics.median`); `sd` = sample sd (n−1) via `statistics.stdev`; every undefined
statistic emits JSON/YAML `null`, never `0` or `NaN`; staleness is excluded from the
profiler as non-hermetic (needs wall-clock TODAY).

**Rationale:** The persona round tie-broke on **reliability**: a "trust-core" number a
sceptical statistician re-checks in pandas/numpy/R (all default to type 7) should
byte-agree with those tools; type 7 also avoids exclusive's endpoint clamping. This
overrides the scope document's own parenthetical "default = exclusive" lean. H&F's own
recommended type (8) is not offered by Python's `statistics` module at all.
**Source:** 25-CONTEXT.md, 25-RESEARCH.md

### D-03 — `--unit`/`--target` CLI flags with closed-set validation
`--unit <col>` and `--target <col>` are single-column flags; absent → block omitted;
`--target` hard-requires `--time` (`CheckError` otherwise); target values must be binary
`{0,1}` (non-binary → `CheckError` listing every offending value; `yes/no/true/false` are
explicitly NOT accepted as synonyms); unknown header → `CheckError`, matching the existing
`--pk`/`--time` pattern.

**Rationale:** A closed check against the literal `{"0","1"}` set prevents silent
over-acceptance via reuse of some existing truthy/falsy coercion helper elsewhere in the
codebase — the requirement is deliberately narrower than "looks binary."
**Source:** 25-CONTEXT.md, confirmed in 25-03-SUMMARY.md

### D-04 — Byte-stability guard shape (4-part) + REQ-P25-02 reinterpretation
The guard is: (1) a reference-value test (`dsx profile` output equals hand-computed exact
numbers), (2) a determinism test (two runs byte-identical), (3) a pre-existing-key golden
(today's keys unperturbed, raw text diff not parsed-dict compare), and (4) the two example
profiles kept byte-invariant in git and still passing their DQ gates. Because
`examples/good-DATA-PROFILE.yaml` (`computed_by: measured_export`, a fabricated sha256) and
`examples/bad-DATA-PROFILE.yaml` (`computed_by: manual`) were never actually produced by
`dsx profile` and have no source CSV, the literal requirement text ("committed example
profiles regenerate identically on every pre-existing key") cannot be executed as written.
D-04 operationalizes it as (4) byte-invariance-in-git + (3) producer-invariance proven on
synthetic fixtures the profiler can actually produce.

**Rationale:** This is a defensible reinterpretation of intent using a mechanism that
actually exists to test, not a reworded requirement — flagged for plan-gate ratification,
which happened at S1-3/25-04 and was recorded as ratified with a pinned-sha256 test
(`TestExampleProfilesByteInvariant`) supplying the missing self-enforcing byte-diff
assertion.
**Source:** 25-CONTEXT.md, 25-RESEARCH.md, ratified in 25-04-SUMMARY.md

### Edge-period grain = ISO-week, not calendar day
The first/last edge-period ratio (for detecting truncated periods) is computed at
**ISO-week** grain over populated weeks (`<5` populated weeks → `null`), not calendar-day
grain. `rows_per_day` stays day-grain — a different-purpose volume-shape stat.

**Rationale:** At day-grain an event extract's last day is almost always cut mid-day, so
the ratio would fire "partial" near-constantly and carry low information. Rigour favours
ISO-week for a truncation signal that is actually informative.
**Source:** 25-CONTEXT.md (persona round divergence #2)

### `share_at_hour_00` null convention on date-only data
The denominator is rows carrying a time token (not all rows); the statistic is `null` when
no row carries a time token, rather than counting date-only values as hour 00.

**Rationale:** A date-only value carries no clock evidence — counting it as hour 00 would
make every genuine date column read `1.0` and false-flag it as "a date wearing a
timestamp's clothes," defeating the statistic's purpose.
**Source:** 25-CONTEXT.md (persona round divergence #3)

---

## Lessons

### `Counter.most_common()` ties break by row order, not by the frozen rule
`Counter.most_common()`'s documented tie behaviour breaks ties by first-insertion order
(CSV row order), not by the "count desc, then string asc" rule every top-N/rare/singleton
output in this phase needed. Two CSVs holding an identical multiset in different row order
would silently produce a different top-10 boundary or `largest_unit_share` winner under
`most_common()` alone.

**Context:** Identified as the single most concrete way the byte-stability guard could be
silently violated by an otherwise-correct-looking implementation; every tie-broken output
was instead built via explicit `sorted(items, key=lambda kv: (-count, level))`.
**Source:** 25-RESEARCH.md (Pitfall 1)

### A tie-break test can pass without discriminating the rule it claims to test
`test_top10_tie_boundary_count_desc_then_string_asc` asserted `share_top10` at a count-5
tie boundary and claimed a row-order-dependent implementation would fail it. Independent
re-derivation showed this is false: `share_top10` is the *sum* of the top-10 counts, and
both tied levels contribute the same count either way — the assertion passes identically
regardless of which order-sensitive or order-independent tie-break is used. No output of
`_categorical_block` (share_top1, share_top10, rare_share, n_singleton) can actually observe
which tied level won, because all four are count aggregates invariant to tie order.

**Context:** Code review finding M-01. The underlying `_categorical_block`/unit-block
implementation was correct and deterministic; only the test's docstring over-claimed what
it pinned. Fixed by renaming the test and its docstring to state it pins top-10 truncation
at a tie boundary, not the tie-break winner, since no fixture can distinguish the two
without adding a new tie-order-sensitive output field.
**Source:** 25-REVIEW.md, disposition in 25-VERIFICATION.md

### Truthiness-guarded validation + identity-guarded emission is an exploitable mismatch
Validation guards used truthiness (`if unit and ...`, `if target and not time_column`) while
block-emission guards used identity (`if unit is not None:`). An explicit empty string
(`--target ""`) is falsy-but-not-None, so it skipped both the column-existence check and the
"--target requires --time" check, yet still triggered emission of a degenerate all-null
`target:` block with no error.

**Context:** Code review finding L-02, low severity (requires a deliberate empty-string
flag) but an inconsistent contract. Fixed by coercing `unit = unit or None` / `target =
target or None` at the top of `profile_csv`, covering all callers rather than only the CLI.
**Source:** 25-REVIEW.md, disposition in 25-VERIFICATION.md

### One statistic drawing from two different row populations can silently mismatch its own baseline
`target.overall` is computed over *every* non-null-target row (including rows whose time
cell fails to parse), while the weekly table and the drift `verdict` comparison are built
only from rows whose time parsed. When every target row is dated the two populations
coincide (the shipped case); with a material share of untimed target rows, the drift
verdict would compare weekly rates against a baseline they were never part of.

**Context:** Code review finding L-01, accepted as a documented residual rather than fixed
in this firing — the split is a producer heuristic, never a gate input, and no shipped
fixture exercised it. A clarifying comment was added at the verdict site; a semantic
redefinition (or separate parseable-time denominator) was deliberately deferred as a
candidate follow-up.
**Source:** 25-REVIEW.md, disposition in 25-VERIFICATION.md

### `statistics.fmean` is not a substitute for `statistics.mean`
`fmean` uses `math.fsum` over floats and is a different, faster, non-exact algorithm — not
guaranteed byte-identical to `mean`'s exact-`Fraction`-accumulation path in all cases. D-02
pins `mean`/`stdev`, never `fmean` or a hand-rolled float accumulator (which is
float-summation-order sensitive and not hermetic at all).

**Context:** Confirmed by reading the actual installed CPython 3.12.10 `statistics.py`
source: `mean`/`stdev`/`variance` all route through `_sum`/`_ss`, which accumulate in exact
`Fraction` arithmetic, converting to float only once at the end.
**Source:** 25-RESEARCH.md

### Golden/byte-stability tests must diff raw rendered text, never a parsed dict
A per-key JSON/dict-level comparison is order-insensitive and would not catch a regression
where a new key gets inserted ahead of an existing key in the same sub-dict (which, for a
plain Python dict, does not raise — it just silently changes iteration/insertion order and
therefore the rendered YAML byte sequence).

**Context:** Named explicitly as Pitfall 3's warning sign; the plan's pre-existing-key
golden test was built as a raw text/byte diff (CRLF-tolerant, `\r?\n` split) of only the
pre-Phase-25 rendered lines, specifically to remain sensitive to ordering regressions a
dict-equality check would miss.
**Source:** 25-RESEARCH.md, implemented per 25-01-SUMMARY.md

---

## Patterns

### Single-pass accumulation, post-loop reduction
`profile_csv` already reads the CSV in exactly one pass. Every new statistic extends the
existing per-column accumulators (e.g. `numeric_values`, `categorical_counts`, `unit_counts`,
`hour_of_time_bearing_rows`) inside the existing `for row in reader:` block; all reductions
(`statistics.mean`/`stdev`/`quantiles`, tie-broken sorts) happen once, after the loop closes,
exactly where the pre-existing `time_block` was already assembled.

**When to use:** Any time a producer needs to add new aggregate statistics to a function
that already streams its input once — never add a second pass over the file.
**Source:** 25-RESEARCH.md (Pattern 1), confirmed in 25-01-SUMMARY.md/25-02-SUMMARY.md

### Deterministic tie-break: explicit sort, never trust container order
Every "top-N"/"most frequent" result with a frozen tie-break rule is produced via
`sorted(items, key=lambda kv: (-count, level))`, never `Counter.most_common()` (ties by
insertion/row order) and never `list(some_set)[i]` (CPython randomizes string-hash-based set
iteration order per process by default).

**When to use:** Any serialized "most frequent"/"top-N" output where determinism across
runs and across row-order-shuffled inputs is required.
**Source:** 25-RESEARCH.md (Pattern 2, Anti-Patterns), applied throughout 25-01…25-03

### Additive-append discipline for insertion-order-sensitive serializers
When a serializer's byte-stability depends on dict insertion order (as `_dump` does here),
new keys must be assigned as the **last** write to their containing dict/sub-dict — built
only after every pre-existing key in that same dict has already been assigned in a prior
statement.

**When to use:** Any hand-rolled or insertion-order-dependent serializer being extended
additively; the trip-wire is a pre-existing-key golden test that does a raw-text diff.
**Source:** 25-RESEARCH.md (Pitfall 3), applied in every plan's `col_stats[col][...]` /
return-dict assembly per 25-01…25-03 SUMMARYs

### Separate parallel accumulator to extend a parser without touching its frozen output
To retain the hour that `_DATE_RE` already captures but `_parse_date` discards, a new
`_extract_hour(value) -> int | None` helper re-matches the same regex and feeds a brand-new,
separate accumulator (`hour_of_time_bearing_rows`) — `_parse_date`'s signature and the
existing `dates: list[date]` accumulator (which feeds the frozen `time.min`/`time.max`/
`max_gap_days`) are left completely untouched.

**When to use:** Whenever new capability needs data a shared upstream parser already has
in hand but discards, and the shared parser's existing consumers must not be perturbed.
**Source:** 25-RESEARCH.md (Pitfall 2), implemented per 25-02-SUMMARY.md

### Flag-gated block omission — omit entirely, never emit null
Top-level blocks driven by an optional CLI flag (`unit:`, `target:`) are omitted from the
output dict entirely when the flag is absent, rather than being present with `null`/empty
contents. This keeps the no-flag output shape byte-identical to before the phase and lets a
single golden test cover the "nothing changed for callers who don't opt in" case.

**When to use:** Any additive, opt-in capability layered onto an existing byte-stable
producer output.
**Source:** 25-CONTEXT.md (D-01), verified across 25-02/03-SUMMARY.md ("omitted, not null")

### "Producer, not gate" — prove structural inertness with a test, not a code read
New keys are added to a file a schema-less gate (`dsx/checks/dq.py`) parses generically.
Rather than assuming the gate ignores unknown keys because a code read shows it only calls
`.get()` on six named paths, the phase adds `TestDQGateIgnoresNewKeys`, which runs the real
`dq.check()` path against a profile with every new key populated vs. the same profile
stripped, and asserts the finding-code set and HIGH-block verdict are identical.

**When to use:** Any time a producer's output flows into a consumer with implicit
"unknown keys are safe" behavior — the safety property should be a running assertion, not
an inferred guarantee from reading the consumer's source once.
**Source:** 25-CONTEXT.md (frozen-vocabulary risk), 25-RESEARCH.md, implemented per
25-04-SUMMARY.md

---

## Surprises

### The two committed example profiles were never actually `dsx profile` output
`examples/good-DATA-PROFILE.yaml` has `computed_by: measured_export` with a fabricated
sha256 and a `source_path` pointing at a warehouse table with no corresponding CSV;
`examples/bad-DATA-PROFILE.yaml` has `computed_by: manual`. Neither can be literally
"regenerated" by the profiler — this is a pre-existing fact about the repository, not a
choice made in this phase, and it forced D-04's two-part reinterpretation of REQ-P25-02's
literal text.

**Impact:** Required flagging a requirement-interpretation gap for explicit plan-gate
ratification rather than silently reading the requirement as satisfied; ultimately resolved
by adding a pinned-sha256 byte-invariance test as the missing self-enforcing check.
**Source:** 25-CONTEXT.md, 25-RESEARCH.md

### A "determinism-critical" tie-break turned out to be unobservable in any output
The frozen count-desc/string-asc tie-break in `_categorical_block` (and the identical rule
in the unit block) cannot be distinguished from `Counter.most_common()`'s insertion-order
tie-break by *any* value the function emits — `share_top1`, `share_top10`, `rare_share`, and
`n_singleton` are all count aggregates that are mathematically invariant to which tied item
wins. The code is correct specifically *because* its outputs are tie-order-independent, but
a fixture test written to "pin" the tie-break passed for the wrong reason.

**Impact:** A structural property (some rules genuinely can't be tested via output
observation) surfaced only in independent code review, not during TDD authoring; the fix was
to correct the test's claim rather than add new output surface just to make the rule
testable.
**Source:** 25-REVIEW.md (M-01)

### H&F's own recommended quantile type isn't available in Python's stdlib at all
Hyndman & Fan (1996) themselves recommend type 8, but `statistics.quantiles` only offers
`'inclusive'` (type 7) and `'exclusive'` (type 6) — the two most common defaults in other
tools (pandas/numpy/R), but not the authors' own preferred choice.

**Impact:** Reframed the "correct" choice as "reliability via cross-tool agreement" rather
than "authorial intent," which is what actually broke the tie in favour of inclusive/type-7.
**Source:** 25-RESEARCH.md (citing R's `quantile()` docs)

### `statistics.mean`/`stdev` are exact-Fraction internally — determinism came "for free"
Reading the actual installed CPython 3.12.10 source showed `mean`/`stdev`/`variance` all
route through `_sum`/`_ss`, which accumulate as exact `Fraction`s grouped by input type and
convert to float only once at the end — meaning order-independence and cross-platform
byte-stability were structural properties of the stdlib call, not something the phase had to
engineer or test defensively beyond confirming the fact.

**Impact:** Simplified the determinism guard to "two runs byte-identical" plus a
shuffled-row-order re-run, rather than needing custom summation-order-stable arithmetic.
**Source:** 25-RESEARCH.md

### Near-zero deviations across three of four plans
25-02, 25-03, and 25-04 each report either zero deviations or a single documented
clarification (not a rework); the phase's only actual bug-fix deviation was in a test's own
hand-computed arithmetic (a manual summation error in the RED test's expected value), not in
any production code, caught by running the assertion against the real implementation's
output during the first GREEN attempt.

**Impact:** Suggests the CONTEXT/RESEARCH pre-work (persona round, reference-value table,
pitfall catalogue) front-loaded enough precision that execution had very little to discover
or correct on the fly.
**Source:** 25-01-SUMMARY.md, 25-02-SUMMARY.md, 25-03-SUMMARY.md, 25-04-SUMMARY.md
