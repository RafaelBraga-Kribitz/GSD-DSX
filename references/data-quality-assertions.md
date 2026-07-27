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

## What stays stochastic

Whether structured missingness invalidates the design, and whether a gap is an
outage or a schema change, remains agent judgement — after the numbers are in
the profile.
