# Phase 25: Hermetic profile depth — Research

**Researched:** 2026-09-06
**Domain:** stdlib-only statistical computation (Python `statistics`/`csv`/`datetime`), hermetic
YAML serialization, byte-stability test design
**Confidence:** HIGH (the two mandatory pins — H&F type mapping and mean/stdev determinism —
are confirmed against the actual installed CPython 3.12.10 source and cross-checked against
two independent official sources; the D-04 ratification is a reasoned assessment, not a
measurement, and is flagged accordingly)

## Summary

Phase 25 grows `dsx/profiler.py::profile_csv` to compute, additively and stdlib-only, the
numbers `skills/dsx-explore-data/SKILL.md` currently asks an agent to eyeball (five-number
summaries, zero/negative counts, categorical concentration, daily volume and ISO-week edge
ratios, rows-per-unit, weekly base rate). Every number must be a pure function of the CSV
bytes and every existing key must stay byte-identical, because `dsx/checks/dq.py` reads this
file at the `execute` gate and the two committed example profiles must keep passing their
gates unperturbed.

The two binding research obligations are now closed with primary-source-grade evidence. First,
`statistics.quantiles(..., method='inclusive')` computes the sample quantile CPython's own
source comments name **"R7" / "PERCENTILE.INC"**, and `method='exclusive'` computes **"R6" /
"PERCENTILE.EXC"** — this is stated in an inline comment directly above `def quantiles` in
`Lib/statistics.py` (the file actually installed at
`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\Lib\statistics.py`), which
additionally quotes Hyndman & Fan by name. R's own `quantile()` documentation (a second,
independent official source) states the identical `p_k` formulas for its own types 6 and 7 and
explicitly attributes the whole nine-type taxonomy to Hyndman & Fan (1996), noting H&F's own
recommendation was type 8 (not offered by `statistics`) — this matches the CONTEXT.md
Statistician's tie-break note exactly. Comparing CPython's documented probability formula for
each method (`i/(m+1)` for exclusive, `(i-1)/(m-1)` for inclusive, from the public
docs.python.org page) against R's type-6/type-7 `p_k` formulas shows they are algebraically
identical. Three independent sources agree: **inclusive = type 7, exclusive = type 6.** The
type *number* itself is still formally pending HQ-40 row 40a's primary-source (the 1996 paper
itself) read — this research pins the mapping via CPython's own source attribution and R's
independent documentation, not via the paper directly, and flags that distinction rather than
asserting it as closed.

Second, `statistics.mean`, `statistics.stdev` and `statistics.quantiles` are order-independent
and cross-platform byte-stable by construction: `mean`/`stdev`/`variance` all route through
`_sum`/`_ss`, which accumulate in exact `Fraction` arithmetic (grouped by input type, summed as
exact rationals, only converted to `float` once at the end) — confirmed by reading the actual
installed source. This has no floating-point summation-order sensitivity and no locale
dependency. `statistics.fmean`, by contrast, uses `math.fsum` over floats and is a *different,
faster, non-exact* function — the plan must use `statistics.mean`, never `fmean`. `quantiles`
sorts its input first (`data = sorted(data)`), so its result is order-independent regardless of
row order in the CSV.

Third, D-04's operationalization of REQ-P25-02's "the committed example profiles regenerate
identically on every pre-existing key" is assessed as a **defensible reinterpretation, not a
literal satisfaction — recommend PASS with one added implementation condition** (below). The
literal requirement text cannot be executed as written because `examples/good-DATA-PROFILE.yaml`
(`computed_by: measured_export`, fabricated hash) and `examples/bad-DATA-PROFILE.yaml`
(`computed_by: manual`) were never produced by `dsx profile` and have no source CSV to
regenerate from — this is a fact about the existing repository, not a Phase-25 choice. D-04's
two-part split (byte-invariance of the committed files in git, plus producer invariance proven
separately on synthetic fixtures) captures the requirement's evident intent — new profiler
capability must not perturb any existing profile — using a mechanism that actually exists to
test. The one gap: "kept byte-invariant in git" is not self-enforcing; the plan must add an
explicit byte-diff assertion (checksum or git-tracked copy comparison), not rely on the absence
of an edit. `scripts/check.sh` already runs both example specs through all four gate points
(`plan`/`execute`/`verify`/`ship`) expecting good→pass, bad→block — this existing loop already
covers "still passing their DQ gates" for free, provided the two profile files are untouched.

**Primary recommendation:** implement the additive keys exactly per D-01/D-02's frozen
vocabulary using `statistics.mean`/`statistics.stdev`/`statistics.quantiles(method='inclusive')`
(never `fmean`, never a hand-rolled quantile), sort every tie-broken output explicitly by
`(-count, level_string)` rather than trusting `Counter.most_common()` or raw `set` iteration
order (both are event-order- or hash-seed-dependent and would silently break the D-04
determinism guard), and add one new byte-diff test asserting the two `examples/*-DATA-PROFILE.yaml`
files are untouched, alongside the reference-value/determinism/pre-existing-key-golden triad
D-04 already specifies.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Additive statistic computation (`profile_csv`) | CLI Producer (`dsx/profiler.py`) | — | Stdlib-only, hermetic; the sole place these numbers are computed (D-01/D-02) |
| YAML emission / byte-stability | CLI Producer (`_dump`/`_scalar`) | — | Hand-rolled insertion-order emitter; additive keys must append, never interleave |
| CLI surface (`--unit`/`--target`) | CLI Producer (`dsx/cli.py::cmd_profile`) | — | Flag parsing/validation only; no statistics live here (D-03) |
| Assertion adjudication (row_count, null_rate, gap, sentinel, PK) | Gate/Adjudicator (`dsx/checks/dq.py`) | — | Reads six specific keys via `.get()`; explicitly does NOT read any new Phase-25 key this milestone |
| Spec/profile parsing (generic YAML) | Loader (`dsx/loader.py`) | — | Full recursive-descent YAML-subset parser (or PyYAML passthrough); handles arbitrary new nesting without a schema, so new keys parse without special-casing |
| Copying numbers into `EDA.md` | Agent/Skill Consumer (`skills/dsx-explore-data/SKILL.md`) | — | "Copied from the profile, never recomputed" — Phase 25's numbers become the trust core these steps cite |
| Documentation of the vocabulary | Docs (`templates/DATA-PROFILE.yaml`, `references/data-quality-assertions.md`) | — | Ripple-only; no runtime effect, but must stay truthful |
| Byte-stability / regression proof | Test Harness (`tests/fixtures/profiler/`, `tests/test_dsx.py`) | — | New tier this phase adds; enforces every guarantee above without becoming a gate itself |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `statistics` (stdlib) | Python 3.12 (bundled) | `mean`, `stdev`, `quantiles`, `median` | Exact-arithmetic, order-independent implementation confirmed by reading the installed source `[VERIFIED: local CPython 3.12.10 source, C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\Lib\statistics.py]` |
| `csv` (stdlib) | Python 3.12 (bundled) | Already used by `profile_csv` for dialect sniffing and row iteration | No change needed; existing dependency `[VERIFIED: dsx/profiler.py L102-109]` |
| `datetime.date` (stdlib) | Python 3.12 (bundled) | `date.isocalendar()` for the ISO-week bucket key (`--target` weekly table, edge-period ratios) | Deterministic, locale-free per CONTEXT D-02; already imported in `dsx/profiler.py` `[VERIFIED: dsx/profiler.py L14]` |
| `collections.Counter` (stdlib) | Python 3.12 (bundled) | Level/unit frequency counts feeding `share_top1`/`share_top10`/`rare_share`/`n_singleton`/`rows_per_unit`/`largest_unit_share` | Already imported; a dict subclass — insertion-order iteration is deterministic regardless of hash-seed, unlike a bare `set` `[VERIFIED: dsx/profiler.py L13]` |

No new package is required or recommended — the phase constraint is stdlib-only and every
needed primitive already exists in the standard library the codebase already imports from.

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `re` (stdlib) | bundled | Extend `_DATE_RE` (or a sibling regex) to retain the captured hour group instead of discarding it | Only touch-point needed to unlock `share_at_hour_00`; the existing regex already captures `H:M:S` in groups 4-6, it is simply discarded today `[VERIFIED: dsx/profiler.py L23-25, L71-79]` |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `statistics.quantiles(method='inclusive')` | `statistics.quantiles(method='exclusive')` | Both are legitimate H&F types (6 vs 7); D-02 already resolved this in favour of inclusive/type-7 for cross-tool agreement with pandas/numpy/R defaults — not re-litigated here |
| `statistics.mean`/`stdev` | `statistics.fmean`/a manual float accumulator | `fmean` uses `math.fsum` (still exact-ish but a *different* algorithm producing potentially different last-bit floats than `mean`) and is explicitly documented as "faster, always float" — NOT the same numeric contract; a manual `sum(x)/n` accumulator is float-order-sensitive and NOT hermetic. Neither substitutes for `mean`/`stdev` under D-02 |
| Hand-rolled percentile interpolation | `statistics.quantiles` | The scope explicitly rejects hand-rolling (D-02 pins the stdlib call); a hand-rolled implementation would also have to independently reprove the exact-arithmetic property `statistics` gets for free |

**Installation:** none — no `pip install` step; every dependency is already imported by
`dsx/profiler.py` or is a stdlib module never before imported by it (`re` is already imported;
only `statistics` needs a new `import statistics` line).

**Version verification:** stdlib modules are not versioned independently of the Python
interpreter. Verified interpreter: `C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`
→ `Python 3.12.10` `[VERIFIED: ran `python.exe --version` this session]`. Per the repo's
CLAUDE.md and the HUMAN-QUEUE standing note, a bare `python3` on this machine can resolve to a
package-less Python 3.14.6 stub — **the planner and executor must invoke the real interpreter
path explicitly**, not `python3`.

## Package Legitimacy Audit

**Not applicable this phase.** Phase 25 introduces zero external packages — every primitive
used (`statistics`, `csv`, `re`, `collections.Counter`, `datetime.date`, `math`, `hashlib`) is
Python's standard library, already partially imported by `dsx/profiler.py`. The milestone
constraint (D-01, "no pandas/numpy/scipy anywhere") makes this a structural guarantee, not a
per-package judgement call. The Package Legitimacy Gate protocol (registry lookup,
`npm view`/`pip index versions`, postinstall-script scan) has no object to run against and is
skipped for this reason.

**Packages removed due to `[SLOP]` verdict:** none (n/a — no packages evaluated).
**Packages flagged as suspicious `[SUS]`:** none (n/a).

## Architecture Patterns

### System Architecture Diagram

```
                    ┌─────────────────────────┐
CSV bytes on disk → │  dsx profile <csv> ...  │  (dsx/cli.py::cmd_profile)
                    └───────────┬─────────────┘
                                │ parses --unit/--target (D-03), validates columns exist,
                                │ --target hard-requires --time, values must be binary {0,1}
                                ▼
                    ┌─────────────────────────┐
                    │   profile_csv()         │  (dsx/profiler.py)
                    │  single pass over rows: │
                    │  - existing: null/uniq/ │
                    │    dtype/pk/sentinels/  │
                    │    time min/max/gap     │
                    │  - NEW: retain hour     │
                    │    token per time-      │
                    │    bearing row          │
                    │  - NEW: per-column      │
                    │    numeric/categorical  │
                    │    accumulators         │
                    │  - NEW: per-unit /      │
                    │    per-ISO-week /       │
                    │    per-target-week      │
                    │    Counters             │
                    └───────────┬─────────────┘
                                │ post-loop: statistics.mean/stdev/quantiles,
                                │ Counter.most_common() re-sorted by (-count, level asc),
                                │ isocalendar() week bucketing
                                ▼
                    ┌─────────────────────────┐
                    │  dict returned, keys    │  existing keys first (untouched),
                    │  appended in D-01 order │  numeric:/categorical: nested under
                    │                         │  columns[<col>], time: additive keys
                    │                         │  appended, unit:/target: top-level
                    │                         │  blocks omitted when flag absent
                    └───────────┬─────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │  dump_profile_yaml() /  │  hand-rolled insertion-order _dump/
                    │  _dump / _scalar        │  _scalar — UNCHANGED this phase;
                    │  (unchanged)            │  byte-stability of pre-existing keys
                    │                         │  is a pure consequence of append-only
                    └───────────┬─────────────┘  key ordering in the dict above
                                ▼
                    DATA-PROFILE.yaml on disk
                                │
              ┌─────────────────┴──────────────────┐
              ▼                                     ▼
   ┌─────────────────────┐              ┌───────────────────────────┐
   │ dsx check dq /       │              │ skills/dsx-explore-data/  │
   │ dsx gate execute     │              │ SKILL.md steps 1a/3a/4a/  │
   │ (dsx/checks/dq.py)   │              │ 4b/4e/4f — agent copies   │
   │ reads ONLY 6 known   │              │ the new keys verbatim     │
   │ keys via .get():     │              │ into EDA.md instead of    │
   │ row_count,           │              │ computing them itself     │
   │ primary_key_unique,  │              └───────────────────────────┘
   │ duplicate_rate,      │
   │ columns.*.null_rate, │
   │ time.max_gap_days,   │
   │ sentinels_found,     │
   │ computed_by          │
   │ — every other key,   │
   │ old or new, is never │
   │ read (structurally   │
   │ ignored, D-05        │
   │ frozen-vocab risk)   │
   └───────────────────────┘
```

### Recommended Project Structure

No new modules. Everything lands inside the two files the phase boundary already names:

```
dsx/
├── profiler.py         # profile_csv() grows additive keys; _parse_date retains hour;
│                        # new small helper(s) for numeric/categorical/time/unit/target
│                        # blocks, called from inside the existing single CSV pass
└── cli.py               # cmd_profile gains --unit/--target parsing + validation (D-03)

tests/
└── fixtures/
    └── profiler/         # NEW directory — hand-computed CSVs, one per reference-value
                           # case in CONTEXT.md's table (quantiles, zeros/negatives, n=0/1,
                           # categorical shares, hour fingerprint, rows_per_day, edge ratios,
                           # rows_per_unit, target drift/stable/boundary/single-week/non-binary)
```

### Pattern 1: Single-pass accumulation, post-loop reduction

**What:** `profile_csv` already reads the CSV in exactly one pass (`for row in reader:`),
building per-column accumulators (`null_counts`, `uniques`, `samples`, `dates`). All reductions
(min/max/gap, dtype inference) happen *after* the loop closes.

**When to use:** every new statistic. Do not add a second pass over the file — extend the
existing accumulators (e.g. add `numeric_values: dict[str, list[float]]`,
`categorical_counts: dict[str, Counter[str]]`, `unit_counts: Counter[str]`,
`week_target_counts: dict[tuple[int,int], list[int]]`, `hour_counts: dict[str, Counter[int]]`)
inside the existing `for row in reader:` block, and compute `statistics.mean`/`stdev`/
`quantiles` and the tie-broken top-N sorts once, after the loop, exactly where `time_block` is
already assembled today.

**Example:**
```python
# Source: dsx/profiler.py L129-193 (existing pattern, extend in place)
for row in reader:
    row_count += 1
    ...
    for col in columns:
        raw = row.get(col)
        text = "" if raw is None else str(raw)
        if _is_null(text):
            null_counts[col] += 1
            continue
        stripped = text.strip()
        uniques[col].add(stripped)
        # NEW: feed numeric_values[col] / categorical_counts[col] here,
        # keyed by the dtype already inferred from `samples[col]`

# ... after the loop, where time_block is built today:
if numeric_values[col]:
    ordered = sorted(numeric_values[col])
    q = statistics.quantiles(ordered, n=4, method="inclusive")  # [q1, median, q3]
    mean = statistics.mean(ordered)
    sd = statistics.stdev(ordered) if len(ordered) >= 2 else None
```

### Pattern 2: Deterministic tie-break — sort explicitly, never trust container order

**What:** every "top-N" / "largest X" computation in D-02's vocabulary (`share_top10`'s
top-10 levels, `largest_unit_share`'s most-frequent unit) has a frozen tie-break: **count desc,
then the level/unit string asc**. `collections.Counter.most_common()` breaks ties by
**insertion order** (i.e. CSV row order) for equal counts — not by string — so two CSVs holding
the same multiset of values in different row order would silently produce a different `top-10`
membership or a different `largest_unit_share` winner under `most_common()` alone. This is the
single most concrete way D-04's byte-stability guard could be violated by a naive
implementation, so name it as a pattern, not just a pitfall.

**When to use:** every place a "most frequent" or "top-N" result feeds a serialized key.

**Example:**
```python
# Source: mechanical requirement from 25-CONTEXT.md D-02 ("tie-break: count desc,
# then level string asc" / "tie-break count desc, unit string asc")
counts = Counter(level for level in raw_levels)  # dict, insertion-order = CSV row order
ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))  # deterministic regardless
                                                                   # of row order or hash seed
top10_levels = {level for level, _ in ranked[:10]}
```

**Do NOT** use `counts.most_common(10)` directly for anything the tie-break rule governs — it
is correct for total ordering by count alone, but silently wrong at ties. `Counter.most_common()`
with no argument still returns entries "in the order encountered" for ties per the stdlib docs.

### Anti-Patterns to Avoid

- **Building a plain `set` and relying on its iteration order for anything serialized:** CPython
  randomizes string hashing per-process by default (`PYTHONHASHSEED`), so `set` iteration order
  for `str` elements is **not** guaranteed identical across two separate `dsx profile` invocations
  even on the same machine with the same CSV — this would break D-04's two-runs-byte-identical
  guard in a way that is invisible in ordinary testing (it "usually" doesn't manifest because
  most stats are order-independent aggregates, but any code path that does `list(some_set)[0]`
  or similar is a latent nondeterminism bug). The existing `uniques: dict[str, set[str]]`
  accumulator is safe today because it is only ever consumed via `len()` (an order-independent
  reduction) — new code must preserve that discipline or switch to a `Counter`/sorted structure.
- **Using `statistics.fmean` instead of `statistics.mean`:** `fmean` is a *different* function
  (float-only, `math.fsum`-based) explicitly documented as faster and always-float — it is not
  guaranteed to produce byte-identical results to `mean`'s exact-`Fraction` path in all cases,
  and D-02 pins `mean`/`stdev`, not `fmean`/anything else.
- **Emitting `0` or `NaN` for an undefined statistic:** D-02 is explicit — every undefined
  statistic emits YAML `null`. `_scalar` already maps Python `None` → `"null"` and NaN/inf floats
  → `"null"` (`dsx/profiler.py` L257-268) — return Python `None`, not `float('nan')` or `0`, for
  n=0 numeric stats, `<2` populated-week ratios, etc., so the existing `_scalar` mapping is used
  rather than re-implemented.
- **Interleaving new keys into an existing sub-dict instead of appending:** `_dump`'s
  byte-stability guarantee depends entirely on Python 3.7+ dict insertion order. Any code that
  does `col_stats[col]["numeric"] = {...}` **before** `col_stats[col]["dtype"]` is finalized in
  the same statement block, or that inserts a key into `col_stats[col]` ahead of its existing
  keys, would break the pre-existing-key-golden byte comparison. Build the pre-existing keys
  exactly as today, then assign the new nested block as the *last* statement writing to that
  dict.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Quantile interpolation | A custom linear-interpolation percentile function | `statistics.quantiles(data, n=4, method='inclusive')` | Re-implementing risks a subtly different position formula than the pinned H&F type; the stdlib version is exact-Fraction-adjacent (sorts once, interpolates on sorted floats) and is what D-02 pins |
| Sample standard deviation | `sqrt(sum((x-mean)**2 for x in xs) / (n-1))` via a float loop | `statistics.stdev(xs)` | The naive float loop suffers catastrophic cancellation and float-summation-order sensitivity across platforms; `stdev` routes through `_ss`'s exact-Fraction accumulator, which the naive loop cannot replicate byte-for-byte |
| ISO week bucketing | Manual `(date - epoch).days // 7` arithmetic | `date.isocalendar()` | ISO-8601 week numbering has edge cases (week 1 contains the first Thursday of the year; some years have a week 53) that a naive `//7` calculation gets wrong; `isocalendar()` is stdlib, deterministic and locale-free per D-02 |
| "Most frequent N with a tie-break" | `sorted(counts, key=counts.get, reverse=True)[:10]` (silently uses whatever order `counts` iterates in for ties) | Explicit `sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))` | The frozen tie-break (count desc, then string asc) is a spec requirement, not an incidental detail — see Pattern 2 above |

**Key insight:** every "don't hand-roll" item above is really the same insight restated: the
`statistics` module and `datetime.isocalendar()` were built precisely to remove the
floating-point and calendar edge cases a bespoke implementation would have to independently
reprove correct — and D-04's whole guard exists because a subtly different implementation would
still "look right" on eyeball inspection while failing byte-identity on a second run or a second
machine.

## Common Pitfalls

### Pitfall 1: `Counter.most_common()` tie order is CSV row order, not the frozen tie-break

**What goes wrong:** `share_top10`, `n_singleton`, `largest_unit_share`, and the target/unit
Counters all have a D-02-frozen tie-break (count desc, string asc). `Counter.most_common(n)`
breaks ties by first-insertion order — which is the order values first appeared in the CSV.
Two CSVs holding the identical multiset of category values but in a different row order would
produce a different top-10 boundary or a different `largest_unit_share` winner.

**Why it happens:** `Counter.most_common()`'s documented tie behaviour ("elements with equal
counts are ordered in the order first encountered") is easy to miss because it "usually" agrees
with the frozen rule by coincidence on hand-written test fixtures, especially small ones typed
in alphabetical order.

**How to avoid:** always re-sort with an explicit `key=lambda kv: (-count, level_string)` before
taking the top-N or the single winner — see Pattern 2.

**Warning signs:** a reference-value fixture test that only exercises small, already-sorted
input data would pass even with the bug present. CONTEXT.md's own reference table anticipates
this — "categorical top-10 tie boundary (#10 'm' and #11 'n' both count 5)" is explicitly a
tie-break stress case; the fixture CSV for it must place "n" before "m" in row order so a
row-order-dependent implementation fails the test while a correctly-sorted one passes.

### Pitfall 2: retaining the hour without perturbing `time.min`/`time.max`/`max_gap_days`

**What goes wrong:** `_parse_date`'s regex already captures `H:M:S` in groups 4-6 but the
function currently returns only a `date` object, discarding them (`dsx/profiler.py` L71-79).
`share_at_hour_00` needs the hour *and* needs to distinguish "no time token present" (→ `null`
denominator) from "time token present, hour happens to be 0". A naive fix that changes
`_parse_date`'s return type (e.g. to a `datetime`) would ripple into the `dates: list[date]`
accumulator used for `time.min`/`time.max`/`max_gap_days`, which sorts and diffs `date` objects
today — any change to what gets appended to that list risks perturbing those three existing,
byte-frozen values.

**Why it happens:** the obvious refactor ("just return a `datetime` instead of a `date`") is the
one most likely to touch code shared with the frozen keys.

**How to avoid:** keep the existing `_parse_date(str) -> date | None` signature and its
`dates: list[date]` accumulator completely untouched. Add a second, additive extraction (either
a second regex-group read inline in the row loop, or a small new helper called alongside
`_parse_date` on the same raw string) that populates a *separate* accumulator — e.g.
`hour_of_time_bearing_rows: list[int]` — only for rows whose match object has a non-`None` hour
group. `share_at_hour_00`'s denominator is `len(hour_of_time_bearing_rows)`, `None` when that is
zero; the numerator is the count of `0`s in it. This guarantees zero interference with the
`dates` list or the three frozen `time.*` keys.

**Warning signs:** the pre-existing-key-golden test (D-04 guard #3) is the trip-wire — if it
fails after adding hour retention, the hour-tracking code touched something shared with the
frozen path.

### Pitfall 3: dtype-conditional block placement breaks additive-append if column order changes

**What goes wrong:** D-01 requires `numeric:`/`categorical:` to be *appended after* `dtype` in
each `columns[<col>]` sub-map, present only for the matching dtype. If the code path that
decides "is this numeric or categorical" runs before `dtype` is written into `col_stats[col]`,
or reorders the dict construction, the appended-last guarantee silently breaks even though the
final YAML *looks* identical for old keys in isolation — the actual failure mode is inserting
`numeric`/`categorical` **before** an existing key gets its value assigned in a later
statement, which for a plain Python `dict` does not raise, it just changes iteration/insertion
order.

**How to avoid:** build `col_stats[col]` exactly as today (three keys: `null_rate`, `n_unique`,
`dtype`) first, completing that dict literal or those three assignments before any conditional
`col_stats[col]["numeric"] = {...}` / `col_stats[col]["categorical"] = {...}` line executes.

**Warning signs:** the pre-existing-key-golden test again — but also, more subtly, a byte-diff
of the whole file rather than a per-key comparison would catch this even if a per-key JSON-level
comparison (which is order-insensitive) would not. Confirm the golden test does a raw text/byte
diff of the pre-existing lines' *rendered YAML*, not a parsed-and-compared-as-dict check —
the latter is blind to ordering regressions entirely.

### Pitfall 4: `--target` non-binary detection must reject `yes/no`/`true`/`false`, not just non-numeric

**What goes wrong:** D-03 requires `--target` values to be strictly `{0, 1}` — explicitly *not*
accepting `yes/no`/`true`/`false` as synonyms. A validation routine that reuses any existing
truthy/falsy coercion helper elsewhere in the codebase (there may be one for boolean-like CLI
flags) would silently over-accept and violate the spec.

**How to avoid:** write the `--target` validator as a closed check against the literal string
set `{"0", "1"}` (post-strip) or the parsed-numeric set `{0, 1}`, and raise `CheckError` listing
every offending distinct value found — not just the first — so the error is actionable.

**Warning signs:** a reference-value fixture using `yes`/`no` values should be added as a
negative test case explicitly, since CONTEXT.md's reference table only shows a numeric
non-binary case ("contains a 2"); the `yes/no` rejection is stated as a rule but has no listed
fixture — flag this as a planner action item, not assume it is covered.

## Runtime State Inventory

**Not applicable — this is a greenfield-additive phase, not a rename/refactor/migration.**
No renamed identifiers, no data migration, no re-registration of external state. Every change is
new, additive code inside two existing files plus new test fixtures; nothing that already exists
changes name or meaning. Section omitted per the trigger condition in the standard protocol.

## Common Pitfalls — Implementation Research (DQ gate / catalogue / installer / test harness)

### DQ gate parses the profile generically and reads only six named keys

`dsx/checks/dq.py::check()` calls `load(profile_file)` (`dsx/loader.py`), which is a full
recursive-descent YAML-subset parser (or a PyYAML passthrough when PyYAML is installed) — it
parses **arbitrary** nesting, sequences, and scalars with no schema and no "unknown key"
rejection of any kind `[VERIFIED: dsx/loader.py L36-296, full mapping/sequence/scalar grammar,
no allow-list]`. Once parsed into a plain `dict`, `dq.py`'s six helper functions
(`_check_row_count`, `_check_primary_key`, `_check_null_rates`, `_check_time_gaps`,
`_check_sentinels`, `_check_manual_honesty`) each call `.get()` on exactly one named path:
`profile.get("row_count")`, `profile.get("primary_key_unique")`, `profile.get("duplicate_rate")`,
`columns.get(col)` → `.get("null_rate")`, `profile.get("time")` → `.get("max_gap_days")`,
`profile.get("sentinels_found")`, `profile.get("computed_by")`
`[VERIFIED: dsx/checks/dq.py L111-342, every field access uses .get(), no key-set validation,
no "reject unexpected keys" branch anywhere in the file]`. This is a structural (code-shape)
guarantee, not an assumption: there is no code path in `dq.py` capable of noticing a new
`numeric:`, `categorical:`, `unit:`, or `target:` key exists at all.

**Guard the plan must add, not assume:** a test that runs `dsx check dq` (or `dsx gate execute`)
against a profile file containing every Phase-25 new key populated, asserting the same pass/fail
verdict as the same spec+profile pair with the new keys stripped. This is the "prove the gate
ignores unknown keys" test CONTEXT.md's frozen-vocabulary risk note explicitly asks for — a
structural code read is necessary but the CONTEXT explicitly says do not stop at "assume it",
run the test.

**CLI output byte-stability:** no `dsx profile --help` snapshot/golden test exists in the repo
today `[VERIFIED: grep across tests/ for "profile --help" and "cmd_profile.*help" returned no
match]`. D-03 adds two new flags (`--unit`, `--target`) to `cmd_profile`'s argparse definition,
which changes `--help` output. If any existing test asserts exact `--help` text (none currently
do for `profile`), it would need updating; since none exist, this is a **net-new** test to add,
not a regression to fix — recommend the planner add one `dsx profile --help` snapshot test as
part of this phase specifically because two new flags are landing, so the CLI's documented
surface is captured going forward.

### Catalogue set-identity mechanism (276 → 276)

`scripts/gen-finding-catalogue.py` regenerates `references/finding-codes.md` from the actual
`report.add(...)` call sites across `dsx/checks/*.py` and `dsx/frame/*.py`
`[VERIFIED: scripts/gen-finding-catalogue.py header docstring L1-12]`. `--check` exits 1 when
the checked-in file is stale relative to a fresh regeneration. Separately,
`tests/test_finding_catalogue_invariant.py` pins the catalogue to exactly 276 codes two ways: a
regex match on the `**Total: N codes.**` line, and a count + **set-identity** diff of every
`` `DSX-<FAMILY>-<digits>` `` table-row code against `tests/fixtures/finding-codes-phase12.md`
(the frozen Phase-12 snapshot of 256 codes) unioned with an explicit `_MINTED_CODES` set of the
20 codes added since `[VERIFIED: tests/test_finding_catalogue_invariant.py L44-52, L116-156]`.
Since Phase 25 adds **zero** new `report.add(...)` call sites (the profiler is a producer, no
gate code changes), `gen-finding-catalogue.py --check` should exit 0 with no regeneration
needed, and `test_finding_catalogue_invariant.py` needs **no edit at all** — the 276→276 gate is
satisfied by *not touching* `dsx/checks/*.py`/`dsx/frame/*.py`, which the phase boundary already
guarantees. The plan-gate proof is: run `python.exe scripts/gen-finding-catalogue.py --check`
and the full test module, both green, with a git diff showing zero changes to
`references/finding-codes.md`.

### `node install.mjs` / `--check` — why every phase touching skills/templates/references must re-sync

`install.mjs` projects a fixed payload list — `capability.json`, `fragments/`, `dsx/`, `bin/`,
`references/`, `templates/`, `examples/` — from the repo root into the host runtime's overlay
directory (e.g. `~/.claude/capabilities/dsx` or a `--local` project copy)
`[VERIFIED: install.mjs L39-47, CAPABILITY_PAYLOAD list]`. `dsx/` and `references/` and
`templates/` are all in that list — Phase 25 changes `dsx/profiler.py`, `dsx/cli.py`,
`templates/DATA-PROFILE.yaml`, and `references/data-quality-assertions.md`, every one of which
is copied by the installer. Per the HUMAN-QUEUE standing note, `--check` became a real gate in
v2.5.0 (previously it only ran `gate ship` and missed drift entirely); running `node install.mjs`
then `node install.mjs --check` is now the correct verification that the installed copy matches
the repo copy after this phase's edits land — this is a phase-end gate (S1-4/S1-5), not
something the plan needs to script per-task, but the plan must include it as an explicit
verification step, not assume it happens automatically.

### Test-harness facts the planner needs

- **Full-suite entrypoint:** `scripts/check.sh` — runs `python3 -m unittest discover -s tests -q`,
  then `gen-finding-catalogue.py --check`, `validate-capability.py`, the four-gate-point good/bad
  spec loop (isolated temp copies of `examples/`), and a determinism check on `dsx audit`
  `[VERIFIED: scripts/check.sh L1-55]`. This is a `sh` script; on this Windows/PowerShell machine
  it needs Git Bash or WSL, or its steps can be run individually via the real interpreter.
- **Real-interpreter requirement:** a bare `python3` on this machine can resolve to a
  package-less Python 3.14.6 stub (per repo CLAUDE.md / HUMAN-QUEUE); the verified real
  interpreter is `C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`
  (3.12.10, confirmed this session). Every unit-test invocation and every `dsx profile`/`dsx
  gate` invocation in the plan and its verification steps must use this explicit path, not
  `python3`.
- **Stray-`DECISIONS.jsonl` false-fail:** running the full suite from an unclean tree can
  false-fail exactly two `explain` tests
  (`tests/test_dsx.py::test_explain_missing_spec_exits_zero_not_two`,
  `tests/test_explain_self_reported.py::test_returns_zero_when_spec_cannot_be_loaded`) if a
  stray root `DECISIONS.jsonl` exists. If exactly these two tests fail, `rm -f DECISIONS.jsonl
  examples/DECISIONS.jsonl examples/known-bad/DECISIONS.jsonl templates/DECISIONS.jsonl` and
  re-run before treating it as a real regression `[CITED: .planning/HUMAN-QUEUE.md L145-150]`.
- **`decision-coverage-plan` false-block:** the plan-checker's decision-coverage regex does not
  match this project's `- **D-NN title** — text` CONTEXT.md bullet style and reports
  `total:0, could-not-parse` — this is a known parser format mismatch, not a real coverage gap;
  confirm coverage via the plan-checker's own Dimension-7 (Context Compliance) pass instead of
  treating a `total:0` result as blocking `[CITED: .planning/HUMAN-QUEUE.md L85-95]`.

## Code Examples

### Retaining the hour without touching the frozen `date`-based accumulator

```python
# Source: mechanical extension of the existing regex, dsx/profiler.py L23-25 / L71-79
_DATE_RE = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})(?:[ T](\d{2}):(\d{2})(?::(\d{2}))?)?"
)

def _parse_date(value: str) -> date | None:
    # UNCHANGED — feeds the frozen `dates: list[date]` accumulator (time.min/max/max_gap_days).
    match = _DATE_RE.match(value.strip())
    if not match:
        return None
    year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
    try:
        return date(year, month, day)
    except ValueError:
        return None

# NEW — additive, feeds a *separate* accumulator; never touches `dates`.
def _extract_hour(value: str) -> "int | None":
    """None means 'no time token present' (date-only value or unparseable)."""
    match = _DATE_RE.match(value.strip())
    if not match or match.group(4) is None:
        return None
    return int(match.group(4))
```

### Numeric summary block per D-02's small-n rules

```python
# Source: mechanical implementation of 25-CONTEXT.md D-02 numeric block + small-n table
def _numeric_block(values: "list[float]") -> dict:
    n = len(values)
    if n == 0:
        return {"min": None, "q1": None, "median": None, "q3": None, "max": None,
                "mean": None, "sd": None, "n_zero": 0, "n_negative": 0, "n": 0}
    ordered = sorted(values)
    n_zero = sum(1 for v in values if v == 0)
    n_negative = sum(1 for v in values if v < 0)
    if n == 1:
        v = ordered[0]
        return {"min": v, "q1": v, "median": v, "q3": v, "max": v,
                "mean": v, "sd": None, "n_zero": n_zero, "n_negative": n_negative, "n": 1}
    q1, median, q3 = statistics.quantiles(ordered, n=4, method="inclusive")
    return {
        "min": ordered[0], "q1": q1, "median": median, "q3": q3, "max": ordered[-1],
        "mean": statistics.mean(ordered), "sd": statistics.stdev(ordered),
        "n_zero": n_zero, "n_negative": n_negative, "n": n,
    }
```

### Deterministic top-10 / rare-share categorical block

```python
# Source: mechanical implementation of 25-CONTEXT.md D-02 categorical block + Pattern 2 above
def _categorical_block(counts: "Counter[str]") -> dict:
    n = sum(counts.values())
    if n == 0:
        return {"share_top1": None, "share_top10": None, "rare_share": None, "n_singleton": 0}
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))  # count desc, string asc
    share_top1 = ranked[0][1] / n
    top10 = ranked[:10]
    share_top10 = 1.0 if len(ranked) < 10 else sum(c for _, c in top10) / n
    rare = sum(c for _, c in ranked if c < 10 or c / n < 0.001)
    singleton = sum(1 for _, c in ranked if c == 1)
    return {
        "share_top1": share_top1, "share_top10": share_top10,
        "rare_share": rare / n, "n_singleton": singleton,
    }
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|---------------|--------|
| Agent eyeballs five-number summaries / concentration / edge ratios each EDA run | `dsx profile` computes them once, hermetically | This phase | `EDA.md` copies numbers instead of re-deriving them; two runs on the same extract are byte-identical by construction (D-04) |
| `_parse_date` silently drops the hour it captures | Hour retained via a parallel accumulator | This phase | Unlocks `share_at_hour_00` without touching the three frozen `time.*` keys |

**Deprecated/outdated:** none — this phase only adds capability; nothing in the existing
profiler contract is deprecated or removed.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The Hyndman & Fan (1996) paper's own Table 1 formally assigns the labels "type 6" and "type 7" to exactly the `p_k = k/(n+1)` and `p_k = (k-1)/(n-1)` formulas this research confirms match CPython's `exclusive`/`inclusive` methods | H&F type-number pin (Summary; Package/Stack sections) | This is the exact question HQ-40 row 40a's pending human read exists to close; if the paper itself numbers these differently than every secondary source (CPython's own source comment, R's docs) claims, the docstrings/citations the plan writes would carry a wrong type number. Non-blocking for this phase per CONTEXT.md — it is a definition test, not a minted finding code, and the mapping itself (which method matches which formula) is independently confirmed regardless of the label's exact number |
| A2 | D-04's REQ-P25-02 operationalization ("kept byte-invariant in git" + "producer invariance on synthetic fixtures") is the CONTEXT-round's intended resolution and does not require further architect/statistician re-litigation at plan time | D-04 ratification (Summary) | If the plan-gate ratification (explicitly flagged as required by CONTEXT.md) disagrees with this research's PASS recommendation, the byte-diff test design below would need to change; the recommendation is reasoned, not a measured fact, and is presented as such |

**If this table is empty:** N/A — two assumptions logged above; both are explicitly flagged as
non-blocking pending items already tracked by the milestone (HQ-40 40a) or the plan-gate
ratification CONTEXT.md itself requires.

## Open Questions

1. **Categorical block on an all-null column (n=0 denominator).**
   - What we know: D-02 defines the numeric small-n table for n=0/n=1 explicitly. The
     categorical block's denominator is "non-null rows"; CONTEXT.md's reference-value table does
     not include an explicit N=0 categorical case.
   - What's unclear: whether `share_top1`/`share_top10`/`rare_share` should all be `null` (by
     analogy with the numeric n=0 row) or whether `n_singleton: 0` alone is expected with the
     shares also `0`/`null` mixed.
   - Recommendation: follow the stated blanket rule ("every undefined statistic emits null,
     never 0 or NaN") — a share of nothing is undefined, so all four keys should be `null`/`0`
     symmetric with the numeric n=0 row (`n_singleton: 0` is a count, stays `0`; the three share
     fields are `null`). Add this exact case to `tests/fixtures/profiler/` as a reference-value
     fixture so it is pinned rather than inferred at execute time.

2. **`--help` snapshot format.**
   - What we know: no `dsx profile --help` golden test exists today; D-03 adds two flags.
   - What's unclear: whether the planner should add a full golden-text snapshot (brittle to any
     future help-text wording change) or a narrower assertion (e.g. `--unit`/`--target` appear
     in the help output, exit code 0).
   - Recommendation: narrower assertion — assert the new flag names appear in `--help` stdout
     and the command still exits 0, rather than a byte-exact snapshot of the full help text,
     which would create an unrelated maintenance burden every time any other flag's help string
     changes.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|--------------|-----------|---------|----------|
| Python 3.12 (real interpreter) | All profiler code, all tests | Yes | 3.12.10, confirmed at `C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe` `[VERIFIED: ran this session]` | None needed — do not use a bare `python3` alias, it may resolve to a package-less 3.14.6 stub per repo CLAUDE.md |
| `statistics` stdlib module | `mean`/`stdev`/`quantiles` | Yes | bundled with 3.12.10 | None needed |
| `node` (for `install.mjs`) | Phase-end installer re-sync gate | Not directly probed this session — pre-existing project dependency the milestone's every prior phase already relies on (v2.5.0 fixed `--check`) | — | If unavailable, the phase-end installer re-sync gate cannot run; this would block S1-4/S1-5, not S1-2/S1-3 |
| `sh`/Git Bash (for `scripts/check.sh`) | Full-suite entrypoint | Windows/PowerShell primary shell per repo CLAUDE.md; `scripts/check.sh` is a POSIX script | Git Bash (commonly bundled with Git for Windows) or run the script's individual steps directly via the real Python interpreter and `node install.mjs --check` | Run each `scripts/check.sh` step as a separate PowerShell-invoked command if `sh` is unavailable |

**Missing dependencies with no fallback:** none identified as blocking for S1-2 (plan) or S1-3
(execute) — the two Python-only steps are self-contained.
**Missing dependencies with fallback:** `sh`/Git Bash for the bundled `scripts/check.sh` — the
individual verification steps it runs can be executed directly.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | `unittest` (stdlib), invoked via `python -m unittest discover -s tests -q` |
| Config file | none — `scripts/check.sh` is the closest thing to a config/entrypoint wrapper |
| Quick run command | `C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe -m unittest tests.test_dsx.TestProfiler -v` (existing profiler test class; new fixture tests should live alongside or in a new `tests/test_profiler_hermetic.py`) |
| Full suite command | `C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe -m unittest discover -s tests -q` then `python.exe scripts/gen-finding-catalogue.py --check` then `node install.mjs --check` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|--------------------|-------------|
| REQ-P25-01 | Every listed statistic (numeric, categorical, time, unit, target) computed correctly | unit / reference-value | `python.exe -m unittest tests.test_profiler_hermetic -v` (new) | ❌ Wave 0 |
| REQ-P25-01 | `--unit`/`--target` CLI flags parse, validate, and gate correctly (D-03) | unit | `python.exe -m unittest tests.test_dsx.TestProfiler.test_profile_cli -v` (extend existing) | ✅ extend existing `tests/test_dsx.py` `TestProfiler` |
| REQ-P25-02 | Quantile method matches the pinned type (reference values) | unit / reference-value | new fixture test using `tests/fixtures/profiler/quantiles.csv` against the CONTEXT.md reference values | ❌ Wave 0 |
| REQ-P25-02 | Two runs on the same extract are byte-identical | determinism | run `dsx profile` twice on the same fixture CSV, diff the two output files byte-for-byte | ❌ Wave 0 |
| REQ-P25-02 | Every existing profile key/value stays byte-stable (pre-existing-key golden) | golden | run `dsx profile` on a fixture CSV before/after the phase's code change, diff only the pre-existing key lines | ❌ Wave 0 |
| REQ-P25-02 | Committed example profiles stay byte-invariant + still pass their DQ gates | golden + gate | git-tracked byte comparison of `examples/{good,bad}-DATA-PROFILE.yaml` + `scripts/check.sh`'s existing four-gate-point loop (already covers the gate-pass half) | ⚠️ byte-diff assertion is Wave 0; gate-pass loop already exists in `scripts/check.sh` |
| REQ-P25-03 | DQ gate ignores unknown/new profile keys | integration | run `dsx check dq` / `dsx gate execute` against a profile with every new key populated vs. stripped, assert identical verdict | ❌ Wave 0 |
| REQ-P25-03 | Catalogue set-identity 276 → 276 | golden | `python.exe scripts/gen-finding-catalogue.py --check` + `python.exe -m unittest tests.test_finding_catalogue_invariant -v` (no edit needed if zero `report.add` sites touched) | ✅ existing, no change expected |
| REQ-P25-03 | `dsx/checks/dq.py`, assertion vocabulary, gate profiles byte-unchanged | golden | git diff showing zero changes to `dsx/checks/dq.py`, `dsx/checks/*` vocabulary constants, `dsx/cli.py::GATE_PROFILES` | trivially satisfied by not editing those files; verify via git diff at phase-end, not a new test |
| REQ-P25-03 | `node install.mjs --check` passes after ripple | smoke | `node install.mjs && node install.mjs --check` | ✅ existing installer, phase-end gate |

### Sampling Rate

- **Per task commit:** `python.exe -m unittest tests.test_dsx.TestProfiler tests.test_profiler_hermetic -v` (fast — profiler-scoped subset)
- **Per wave merge:** `python.exe -m unittest discover -s tests -q` (full suite)
- **Phase gate:** full suite green + `gen-finding-catalogue.py --check` + `node install.mjs --check` + `scripts/check.sh`'s four-gate-point good/bad loop, all on the real interpreter, from a clean tree (watch for the stray-`DECISIONS.jsonl` false-fail noted above)

### Wave 0 Gaps

- [ ] `tests/fixtures/profiler/` — does not exist yet; needs one hand-computed CSV per
      reference-value case in CONTEXT.md's table (quantiles [1..10], zeros/negatives, n=0, n=1,
      categorical A/B/C/D/E, categorical percent-arm N=20000, categorical top-10 tie boundary,
      `share_at_hour_00` all four sub-cases, `rows_per_day` [1,3,5,7,9], edge-period-ratio W1-W6,
      `rows_per_unit` [1,2,3,4,100], `--target` drifting/stable/boundary/single-week/non-binary)
- [ ] `tests/test_profiler_hermetic.py` (or equivalent new module) — reference-value assertions
      against the fixtures above
- [ ] A determinism test (two `dsx profile` runs on one fixture, byte-diff the outputs)
- [ ] A pre-existing-key golden test (byte-diff of only the pre-Phase-25 key lines, before/after)
- [ ] A DQ-gate-ignores-new-keys integration test
- [ ] A byte-diff assertion for `examples/good-DATA-PROFILE.yaml` /
      `examples/bad-DATA-PROFILE.yaml` (the added condition on D-04's ratification, above)
- [ ] Framework install: none — `unittest` is stdlib, already in use project-wide

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|----------------|---------|-------------------|
| V2 Authentication | No | Local CLI tool, no auth surface |
| V3 Session Management | No | No session concept |
| V4 Access Control | No | No access-control surface |
| V5 Input Validation | Yes | CSV parsing already uses `csv.DictReader` with sniffed dialect (stdlib, not a hand-rolled parser); new `--unit`/`--target` column-name validation reuses the existing `CheckError`-on-unknown-header pattern already used by `--pk`/`--time` (`dsx/profiler.py` L123-127) |
| V6 Cryptography | Partial | `source_hash` uses `hashlib.sha256` (already in place, unchanged this phase) — no new cryptographic surface introduced |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|----------------------|
| CSV injection / formula injection in a value later opened in a spreadsheet | Tampering | Out of scope for `dsx profile` itself — it only reads and aggregates values into YAML; it does not write CSV output that could be re-opened as a formula. No change needed. |
| Malformed/adversarial CSV causing a parse crash instead of a clean `CheckError` | Denial of Service (local) | `profile_csv` already wraps missing-file/missing-header/unknown-column cases in `CheckError` (exit 2, not a crash) — new `--unit`/`--target` validation must follow the same pattern (raise `CheckError`, never let an uncaught exception propagate to a stack trace) |
| Numeric parsing accepting locale-dependent decimal separators, silently producing wrong stats | Tampering (data integrity) | `_FLOAT_RE`/`_INT_RE` are already locale-free ASCII-digit regexes (`dsx/profiler.py` L26-27); new numeric accumulation must parse via the same regex-gated path, never via a locale-aware `float()` call site that could vary by machine locale |

## Sources

### Primary (HIGH confidence)
- CPython 3.12.10 installed source, `Lib/statistics.py` (`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\Lib\statistics.py`) — read directly via `inspect.getsource` this session for `quantiles`, `mean`, `stdev`, `variance`, `_sum`, `_ss`, `fmean`, and the module-level R6/R7 comment block naming Hyndman & Fan.
- Local reproduction of every reference value in 25-CONTEXT.md's table (`quantiles([1..10], n=4, exclusive/inclusive)`, `median([1..10])`, `stdev([1..10])`, and a shuffled-order re-run of `mean`/`stdev`/`quantiles` confirming order-independence) — all matched exactly, including on shuffled input order.
- `dsx/profiler.py`, `dsx/cli.py`, `dsx/checks/dq.py`, `dsx/loader.py`, `skills/dsx-explore-data/SKILL.md`, `examples/good-DATA-PROFILE.yaml`, `examples/bad-DATA-PROFILE.yaml`, `examples/good-ANALYSIS-SPEC.yaml`, `examples/bad-ANALYSIS-SPEC.yaml`, `templates/DATA-PROFILE.yaml`, `references/data-quality-assertions.md`, `install.mjs`, `scripts/check.sh`, `scripts/gen-finding-catalogue.py`, `tests/test_finding_catalogue_invariant.py`, `tests/test_dsx.py` — read in full or targeted this session.

### Secondary (MEDIUM confidence)
- `docs.python.org/3.12/library/statistics.html#statistics.quantiles` (WebFetch this session) — documents the exact probability formulas (`i/(m+1)` exclusive, `(i-1)/(m-1)` inclusive) without naming H&F types explicitly.
- `stat.ethz.ch/R-manual/R-devel/library/stats/html/quantile.html` (WebFetch this session) — states R's own type-6 (`p_k = k/(n+1)`) and type-7 (`p_k = (k-1)/(n-1)`) formulas, explicitly attributed to Hyndman & Fan (1996), and notes H&F's own recommendation was type 8.

### Tertiary (LOW confidence — flagged, not relied on for the type-number claim)
- General WebSearch results locating the Hyndman & Fan (1996) paper's bibliographic record (title, journal, volume/issue/pages: *The American Statistician* 50(4), 361-365) — the paper's own PDF/Table 1 was not opened this session; the type-number mapping is triangulated from the two secondary sources above plus the CPython source comment, not from the primary paper text itself. This gap is exactly what HQ-40 row 40a's pending human read exists to close.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no new packages, every primitive already imported or a stdlib sibling of an existing import; version confirmed against the actual installed interpreter.
- Architecture: HIGH — every architectural claim (single-pass loop, insertion-order YAML emitter, gate reads exactly six keys via `.get()`, generic YAML parser with no schema) is a direct read of the live source, not an inference.
- Pitfalls: HIGH for the mechanical ones (tie-break/hash-seed/fmean/append-order — all derived from reading the actual `Counter`/`set`/`statistics` semantics and the actual `_dump` implementation); MEDIUM for the D-04 ratification recommendation, which is a reasoned judgement flagged for the plan-gate's own required ratification, not a measured fact.

**Research date:** 2026-09-06
**Valid until:** stable — pinned to the installed Python 3.12.10 interpreter and the current repo state; re-verify if the project's Python version changes or if `dsx/profiler.py`/`dsx/checks/dq.py` are touched by an intervening phase before Phase 25 executes.
