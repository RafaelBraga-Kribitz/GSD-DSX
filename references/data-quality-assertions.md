# Data quality assertions

Gates compare `ANALYSIS-SPEC.yaml` → `data[].assertions` against a hermetic
`DATA-PROFILE.yaml`. They never open the warehouse.

## Preferred production path

```bash
dsx profile extract.csv --out DATA-PROFILE.yaml \
  --pk user_id --time signup_at \
  --sentinel -1 --sentinel 999 --sentinel 1900-01-01
```

Then set on the matching `data[]` entry:

```yaml
profile_path: DATA-PROFILE.yaml
assertions:
  row_count: { equals: 38412, tol: 0.01 }
  primary_key: [user_id]
  max_null_rate:
    user_id: 0.0
    country: 0.05
  time_column: signup_at
  max_gap_days: 2
  banned_sentinels: [-1, 999, "1900-01-01"]
```

## Default thresholds (starting points)

Borrowed from programmatic EDA practice; tighten for financial grains:

| Check | Starting threshold | Severity when breached |
|---|---|---|
| Primary key uniqueness | `primary_key_unique: true` | CRITICAL |
| Null rate on keys | `0.0` | HIGH |
| Null rate on secondary columns | `0.05`–`0.30` depending on use | HIGH |
| Time continuity | `max_gap_days` ≤ expected cadence | HIGH |
| Row count vs plan | `equals` ± `tol` (often 1%) | CRITICAL |
| Sentinels | none of `-1`, `999`, `1900-01-01` | HIGH |

## computed_by honesty

| Value | Meaning |
|---|---|
| `dsx-profile` | Written by `dsx profile` (includes `source_hash`) |
| `measured_export` | Counts from a warehouse query / export script |
| `manual` | Hand-entered — requires a non-empty `known_gaps` note |

## Producer-only depth keys (not gated)

`dsx profile` also produces a deeper set of trust-core numbers — the ones the
explore protocol used to ask the agent to eyeball. They are **copied from the
profile** into `EDA.md`, never recomputed:

- per numeric column, a `numeric:` sub-map (`min`, `q1`, `median`, `q3`, `max`,
  `mean`, `sd`, `n_zero`, `n_negative`, `n`);
- per categorical column, a `categorical:` sub-map (`share_top1`, `share_top10`,
  `rare_share`, `n_singleton`);
- under `time:`, `rows_per_day`, `first_period_ratio`, `last_period_ratio`,
  `share_at_hour_00`;
- with `--unit <col>`, a top-level `unit:` block (`rows_per_unit`,
  `largest_unit_share`);
- with `--target <col>` (which hard-requires `--time`), a top-level `target:`
  block (`overall`, a weekly `{week, n, base_rate}` table, `weekly_range`,
  `verdict`).

**These keys are producer-only this milestone.** No gate reads them — `dsx check
dq` still adjudicates exactly the six keys above (`row_count`,
`primary_key_unique`, `duplicate_rate`, `columns.<col>.null_rate`,
`time.max_gap_days`, `sentinels_found`, plus `computed_by` honesty) via `.get()`
on a named path. The additive keys sit adjacent to those six but are never merged
into the verdict; growing the assertion vocabulary so a gate could compare a new
key is a separate, later decision. The profiler stays a producer, not a gate.

## What stays stochastic

Whether structured missingness invalidates the design, and whether a gap is an
outage or a schema change, remains agent judgement — after the numbers are in
the profile.
