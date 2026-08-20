---
name: dsx-explore-data
description: "Programmatic exploratory data analysis with a fixed protocol — profile, validate, then explore. Use before any modelling or inference, and whenever a dataset is new or has changed."
argument-hint: "[dataset-path-or-table] [--target <column>] [--time <column>]"
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Agent
---

<objective>
Learn what the data actually contains before assuming anything about it, and
record the answers as numbers the spec can carry.
</objective>

<core_principle>
**EDA is a protocol, not a browse.** Run the same sequence every time, in order.
The interesting finding is usually in the boring step — a duplicate key rate of
3%, a date column in the wrong timezone, a category that stopped appearing in
March.

Write EDA as a script, not as scattered cells. It will be re-run when the data
refreshes, and a script re-runs while a notebook session does not.
</core_principle>

<protocol>

## 1. Shape and identity
Row count, column count, memory. Primary key candidate — is it actually unique?
Duplicate rate on the intended grain. If duplicates exist, find out why before
deduplicating; the reason is often the finding.

## 2. Completeness
Null rate per column. Then the question that matters: **is nullness random or
structured?** A column null for every row before a launch date is a schema
change, not missing data. Cross-tabulate null indicators against the time column
and — for predictive work, on the training rows only — against the target. A
null pattern read off the full frame is target-informed cleaning.

## 3. Time
Min, max, and the gaps. Count rows per day and plot it — outages, backfills and
double-loads all show up here and nowhere else. Confirm the timezone of every
date column, explicitly.

## 4. Distributions
Per numeric column: five-number summary, skew, and the count of exact zeros and
negatives. Sentinel values (-1, 999, 1900-01-01) masquerade as data. Per
categorical: cardinality, top values, and the share in the tail.

## 5. Relationships
Only after 1-4. Correlations among features, each feature against the target,
and — for any target — the base rate and its stability over time. A base rate
that drifts is a modelling constraint, not a footnote.

**For predictive work, split first.** `dsx-build-model` step 2 fixes the split
before profiling, imputation or feature engineering — EDA gets no exemption.
Compute every feature-vs-target statistic on the training rows only. The base
rate and its drift over time may use the full frame; per-feature target
relationships may not.

## 6. Segments
Recompute the headline number within the two or three most important splits.
A relationship that reverses inside every segment is Simpson's paradox and it
changes the conclusion, not the appendix.

</protocol>

<output>
`EDA.md` with the numbers, plus a hermetic profile:

1. Prefer a local extract. Run:
   `dsx profile <extract.csv> --out DATA-PROFILE.yaml --pk <key> --time <col> --sentinel -1 --sentinel 999`
2. Wire into `ANALYSIS-SPEC.yaml` under `data[]`:
   - `profile_path: DATA-PROFILE.yaml`
   - `assertions:` for row_count, primary_key, max_null_rate, max_gap_days, banned_sentinels
   - durable facts: period, rows, known_gaps
3. Never invent profile numbers. If the source is warehouse-only, export a CSV first or write
   `computed_by: measured_export` with the query that produced the counts — not `manual`
   without a known_gaps note.

The execute/verify gates compare assertions to the profile artifact. They do not open the
warehouse.
</output>
