---
# EDA front-matter — the machine-readable half of this file.
#
# Downstream skills read THIS BLOCK; the prose below is the evidence trail.
# Every value here must have an anchor in a section table. A front-matter value
# with no anchor is an invented number.
#
# A skipped step keeps its heading below with one line `skipped: <reason>` and
# its key here set to null — never absent. Two runs of the same protocol over
# the same extract must diff cleanly at this block.
#
# Authoring note: this repo checks out CRLF on Windows. Any parser that reads
# this front-matter must tolerate \r\n — use `\r?\n`, never a bare `\n`, when
# matching line starts or ends.

eda_version: 1
dataset: <data[].name>
spec_path: <ANALYSIS-SPEC.yaml | none>
profile_path: DATA-PROFILE.yaml
profile_source_hash: <copied from the profile>
question_type: <descriptive | diagnostic | predictive | causal | prescriptive | none>
columns_scoped: <int>              # fully profiled; the rest are listed under step 0d
completed_through: <step id>       # the last completed step; the whole protocol when clean

grain:
  declared: <validity_frame.units.observation>
  observed: <key columns proven unique>
  verdict: match | mismatch | undeclared
  duplicate_rate: <float, copied from the profile>
  rows_per_unit: { p50: , p95: , max: }
  largest_unit_share: <float>
  implied_dependence:
    # The spec's full closed list. Rows-per-unit and time evidence can only ever
    # imply the first four; spatial and hierarchical are accepted values an
    # agent may set from other evidence — never a separate vocabulary.
    structure: none | clustered | repeated_measures | temporal | spatial | hierarchical
    cluster_var: <column | null>

missingness:                       # every key column, plus any column above 0.05
  - { column: , rate: , mechanism: MCAR | MAR | MNAR | not_assessed, evidence: }

time:
  staleness_days: <int>
  first_period_ratio: <float>
  last_period_ratio: <float>
  tz_verdicts: [ { column: , verdict: utc | local | truncated } ]
  gaps: [ { start: , end: , kind: outage | schema_change | unknown } ]

base_rate:
  metric: <name | null>
  overall: <float | null>
  weekly_range: [ <lo>, <hi> ]
  verdict: stable | drifting     # drifting = any week beyond ±20% relative

branch:
  ran: <question_type | none>    # prescriptive runs causal then prescriptive
  verdict: meets | falls_short | re-scope
  downgrade_to: <type | null>
  blocked_on: <null | causal_estimate | prediction_time_definition>

segments_candidates:               # max 5, ranked by absolute headline spread
  - { column: , levels: , headline_range: , n_min: , underpowered: }

leakage_suspects: [ { column: , reason: } ]

dependence:                        # experiment / causal branches only
  icc: <float | null>
  outcome_sd: <float | null>
  weekly_cycle_amplitude: <float | null>

artifact_status: clean | contested | supports_artifact
comparisons_looked_at: <int>       # = comparisons-ledger rows, not executions
interim_looks: <int | null>
ledger_rows: <int>                 # = findings-ledger rows
stop_triggered: false
contradictions: []                 # spec paths from the reconciliation table
spec_validate_exit: <0 | 1 | 2 | null>
rerun_clean: yes | no | not_verified
seed: <reproducibility.random_seed>
---

# EDA — <dataset>

One paragraph: what this extract is, what decision it feeds, and what the run
concluded about whether it can. Written last, from the numbers below.

## 0. Setup

Spec read, profile copied (`source_hash`), column scope (fully profiled vs
`not individually profiled: <count>` with names).

## 1. Shape and identity

Rows, columns, primary key, duplicate rate on the intended grain — and why the
duplicates exist.

### Grain and dependence

`rows_per_unit` p50/p95/max, `largest_unit_share`, implied dependence, and the
grain ladder when the source grain differs from the analysis grain.

### Joins

The fan-out matrix — join_id | left | right | keys | type | rows_before |
rows_after | fanout | left_match_rate | null_key_rate — or `joins: none planned`.

## 2. Completeness

Null rates (copied). Structured-null cross-tabs vs time, and vs target on
training rows only. The mechanism table: column | rate | mechanism | evidence.

## 3. Time

Min, max, gaps, rows per day.

### Time integrity

column | staleness_days | first_period_ratio | last_period_ratio | edge_verdict |
share_at_hour_00 | tz_verdict — plus the periods excluded from trend statements.

## 4. Distributions

Five-number summaries, zeros and negatives, sentinels, categorical tails.

### Summaries

The classical-vs-robust table, and the robust-recompute pairs for flagged
metric-feeding columns.

### Concentration

column | total | share_top1 | share_top10 | max_row_share | n_half | flag; the
top-five rows by key for flagged measures; one summarisation decision each.

### Outliers

column | n_flagged | pct_flagged | class | evidence | action_taken.

### Pathologies and impossible pairs

The pathology sweep, the invariant-violation table, and `duplicate_kind`.

### Wide categoricals

Coverage and rare-share table, with `policy_recommendation` on predictive work.

### Base rate

week | n | rate for the primary metric or target and each guardrail;
overall, weekly_range, verdict.

## 5. Branch: <question_type>

The branch tables. Prescriptive carries the causal branch first.

### Verdict

`meets | falls_short (downgrade_to: <type>) | re-scope`, with the missing
evidence named.

## 5x. Optional routines

Correlation-funnel and conversion-funnel output, or the skip lines with reasons.

## 6. Segments

The planned-cuts list; split | level | n | value | overall | delta | sign_agrees |
thin; `sign_agreement_rate` per split; the Simpson candidates copied to
`results.segments`.

### Unplanned cuts

cut | reason. Never promoted without a spec amendment.

## 7. Second-order look

`headline_value` with its formula; the `second_order` table over every applicable
mechanism; `artifact_status`.

## 8. Spec reconciliation

spec_path | spec_value | eda_value | verdict | action.

## 9. Findings ledger

F-nn | step | finding | severity | alternative_explanation |
discriminating_number | consequence. Close with `ledger_rows: N`.

## 10. Searched, not found

pathology | checked | result | evidence. `not_found` carries the number that
demonstrates absence.

## 11. Comparisons ledger

Counting unit: one row per (statistic × split-or-column), never per level or
cell. k | what_was_compared | step | kept_as_candidate. Close with
`comparisons_this_run: N`.

## 12. Spec writes

What was written, and the `dsx validate` exit status.

## 13. Rerun

`rerun_clean`, `rerun_mismatches`, `rerun_at`, `seed`.
