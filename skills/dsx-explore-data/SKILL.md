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

**EDA computes evidence, the spec declares it, the gates adjudicate the
declaration.** Every step below ends in named outputs — a number, a table with
fixed columns, or a closed verdict. A step that produces an adjective produced
nothing. Where an output belongs in `ANALYSIS-SPEC.yaml`, the field is named;
nothing here asks a gate to compute anything.

Every step carries a skip condition. Skipping is legitimate; skipping silently
is not. A skipped step keeps its heading in `EDA.md` with one line:
`skipped: <reason>`.
</core_principle>

<setup>

## 0. Setup and contract

**0a. Read the contract.** Read `ANALYSIS-SPEC.yaml` in the phase directory:
`question_type`, `metrics[]`, `design`, `model` and the `validity_frame`
declarations. No spec (ad-hoc exploration) → record `spec_path: none`; the trust
core and every register still run in full, the question-type branch is skipped
with `branch.ran: none`, and the branch verdict is replaced by that skip line.

**0b. Profile first, then copy.** Run the profile per the `<output>` section
below. Facts `DATA-PROFILE.yaml` already carries — row count, per-column null
rates, unique counts, duplicate rate, time min/max/gap, sentinels — are
**copied** into `EDA.md`, never recomputed as independent truth. Record
`profile_path` and the profile's `source_hash` so the copy is traceable. If your
own pass disagrees with the profile, that disagreement is a `contradicts` row in
step 8 — the profile is stale, or you are reading a different extract. Re-run
`dsx profile` and reconcile before continuing. One extract, one set of numbers.
Skip only when the source is warehouse-only under `computed_by: measured_export`:
record `no local profile — measured_export` and cite the export query. A local
extract with no profile is not a skip; profile it.

**0c. Open the file and the registers.** Start `EDA.md` from `templates/EDA.md`.
The findings ledger (step 9), the searched-not-found register (step 10) and the
comparisons ledger (step 11) are **appended as you go**, not written at the end.
A flag that fires in step 2 is filed in step 2.

**0d. Scope the columns.** Per-column sub-steps (4a, 4c, 4d) treat in full: key
columns, the time column, every column feeding a declared metric, the target,
and declared covariates — plus the top 20 remaining columns ordered by null rate
then by declared order. List every other column under
`not individually profiled: <count>` with the names. Rows are cheap; the binding
cost of this protocol is bookkeeping. State the scope before you compute, so two
runs profile the same set.

</setup>

<protocol>

## 1. Shape and identity
Row count, column count, memory. Primary key candidate — is it actually unique?
Duplicate rate on the intended grain. If duplicates exist, find out why before
deduplicating; the reason is often the finding.

### 1a. Grain and dependence
Compute rows ÷ distinct(analysis unit) — the unit in
`validity_frame.units.analysis`; if the spec is unwritten, use the intended
decision unit and say so. Record `rows_per_unit` p50 | p95 | max and
`largest_unit_share`.

`p50 >= 2` means the table is a panel or an event log, not one row per unit:
`validity_frame.dependence.structure` **cannot** be `none`, and every naive
standard error downstream is too small. Write the implied declaration
(`clustered` or `repeated_measures`, with the unit as `cluster_var`) into
front-matter `grain.implied_dependence` — a measured value the spec copies, not
a guess.

When `implied_dependence.structure != none`, the spec's dependence block also
owes `method_family_required` (closed list: `cluster_robust` | `delta_method` |
`bootstrap_cluster` | `mixed_effects`). `DSX-VAL-020` fires when the observation
unit differs from the assignment unit and that field is blank. EDA measures
`structure` and `cluster_var`; choosing the method family is an analyst
declaration made at the same moment and recorded as the consequence of the
matching findings-ledger row — never left blank on a panel or event-grain table.

When the source grain differs from the analysis grain, add the **grain ladder** —
one rung per aggregation (event → session → user): rung | grain (key columns) |
rows | reduction vs previous | aggregation rule per metric column
(sum/max/first/any/mean). An unstated rule is where "active users" and "activity"
quietly diverge. The bottom rung must equal `validity_frame.units.observation`
and the top rung `validity_frame.units.analysis`; a mismatch is a step-8
`contradicts` row — stop before computing anything at the wrong grain.

*Skip:* primary key equals the analysis unit and step 1 proved it unique →
`rows_per_unit: 1.0 (pk = analysis unit)`, ladder `flat at <grain>`.

### 1b. Joins (multi-table only)
Before any join is trusted, build the fan-out matrix — one row per planned join:

| join_id | left | right | keys | type | rows_before | rows_after | fanout | left_match_rate | null_key_rate |

`fanout = rows_after / rows_before`. `left_match_rate` = share of left rows with
at least one match. `null_key_rate` = share of rows on either side with a null
join key — null never equals null, so those rows silently drop or explode
depending on the engine. A fanout other than 1.0 on a join declared one-to-one is
a **blocker**, not a dedupe chore: find which side carries the duplicate grain
first. The executor re-asserts each `rows_after` at execute time; EDA is where
the expected number is established.

*Skip:* single input table, no join planned → `joins: none planned`.

## 2. Completeness
Null rate per column (copied from the profile). Then the question that matters:
**is nullness random or structured?** A column null for every row before a launch
date is a schema change, not missing data. Cross-tabulate null indicators against
the time column and — for predictive work, **on the training rows only** —
against the target. A null pattern read off the full frame is target-informed
cleaning.

**Mechanism, by decision table.** For every key column and every column with a
null rate above 0.05, assign one value from the vocabulary the spec already uses
(`MCAR` | `MAR` | `MNAR` | `not_assessed`) — first match wins, evidence recorded:

| test | assign | evidence to record |
|---|---|---|
| Null share varies across time buckets or across levels of an observed column beyond the stated threshold | `MAR` | the predictor named, and the two extreme shares |
| Nulls concentrate at a constraint boundary, or the column's own magnitude predicts its nullness (proxied by a correlated column) | `MNAR` | the boundary or proxy, and the concentration |
| Both cross-tabs computed and flat | `MCAR` | the two computed numbers — evidence of absence |
| Cross-tabs not computable (no time column, single bucket, too few rows) | `not_assessed` | which input was missing |

`MNAR` is assertable from recorded domain or source knowledge as well; the
extract alone can only ever suggest it. Severity ordering, used by step 8:
`MNAR` > `MAR` > `MCAR`, and `not_assessed` on any key column outranks all of
them — an unassessed key column means the spec value stays or becomes
`not_assessed`, never a measured mechanism.

## 3. Time
Min, max, and the gaps. Count rows per day and plot it — outages, backfills and
double-loads all show up here and nowhere else.

### 3a. Time integrity
Three numbers per timestamp column, recorded, not eyeballed:

- **Staleness** — days between `max(timestamp)` and today. Beyond the refresh
  cadence, the extract is stale: name the periods the claims cannot cover.
- **Edge periods** — volume of the **last** calendar period at the reporting
  grain ÷ trailing mean of the previous four like periods. Ratio below 0.5 is a
  partial period: exclude it from every trend statement and record the exclusion.
  Repeat for the **first** period; partial starts are as common as partial ends.
- **Hour fingerprint** — histogram of the hour component.
  `share_at_hour_00 > 0.9` → the column is a date wearing a timestamp's clothes;
  read no intraday pattern from it. A modal business window shifted from where the
  population lives is a timezone error. Record
  `tz_verdict: utc | local | truncated` with its evidence, per column.

Table: column | staleness_days | first_period_ratio | last_period_ratio |
edge_verdict | share_at_hour_00 | tz_verdict — plus the list of periods excluded
from trend statements. This is what "confirm the timezone, explicitly" means.

*Skip:* no timestamp column → `time integrity: skipped (no time column)`.

## 4. Distributions
Per numeric column: five-number summary, and the count of exact zeros and
negatives. Sentinel values (-1, 999, 1900-01-01) masquerade as data. Per
categorical: cardinality, top values, and the share in the tail.

### 4a. Summaries — classical vs robust
The numeric table gains columns: mean | median | trim10 | sd | mad_s
(MAD × 1.4826; MAD zero → IQR/1.349; both zero → flag `degenerate_scale`) |
`loc_gap` = (mean − median)/mad_s | `scale_ratio` = sd/mad_s | flag.

Thresholds are protocol constants so two runs flag identically:
`|loc_gap| > 0.5` → `skew`; `scale_ratio > 1.5` → `heavy_tail`; both → `both`.
Columns with fewer than 30 non-null values get `insufficient_n` instead of ratios.

Any flagged column feeding a declared metric: recompute the metric with the
median or the 10% trimmed mean and record both side by side —
metric | classical | robust | agrees (y/n). Disagreement on direction, or one
value each side of the decision threshold, is a competing explanation: file a
findings-ledger row, and route the column into 4c.

*Skip:* no numeric column with n ≥ 30 → recorded.

### 4b. Concentration
For every additive measure — anything a declared metric sums — sort descending
and record: total, share of the total in the top 1% and top 10% of rows, the
largest single row's share, and `n_half` = rows needed to reach 50% of the total.
Signed measures: shares on absolute values, and say so.

Table: column | total | share_top1 | share_top10 | max_row_share | n_half | flag
(y when `share_top1 > 0.20`).

A flagged measure means every mean and total on this table is a statement about a
handful of rows. Then:

- name the top five rows by primary key — whales are often one entity counted
  twice under a different key, a duplicate steps 1–2 missed;
- recompute the headline excluding the top 1% and carry both numbers into step 7
  (this precomputes the `leverage` mechanism);
- record **one** summarisation decision from the closed list:
  `winsorize(<cap>)` | `log_transform` | `resistant_summary(median|trimmed_mean)` |
  `whale_segment` | `none(<reason>)`. It lands in the metric definition or in
  `data[].cleaning` with `fit_on` when acted on. This step removes no rows; it
  decides how rows will be summarised.

*Skip:* no additive measure at the analysis grain → record the skip **and** the
columns considered with each exclusion reason.

### 4c. Outlier taxonomy
One fence, no discretion: rows outside [Q1 − 3·IQR, Q3 + 3·IQR] per numeric
column. For each column with flagged rows, classify the flagged set — four tests,
in order, first hit wins:

1. `data_error` — values break a stated constraint (negative where impossible,
   matches a sentinel, date before launch). Evidence: the constraint broken.
2. `different_population` — at least half the flagged rows share one level of a
   categorical whose overall share is under 10%. Search only categoricals with
   2–20 levels, in declared column order; the first satisfying categorical wins
   and is named. No eligible categorical → this test is unsatisfiable, fall
   through.
3. `regime_change` — at least half the flagged rows fall in one contiguous window
   covering at most 10% of the time range. Evidence: the window's dates.
4. `heavy_tail` — none of the above. Evidence: flagged-row share per quarter of
   the time range (should be roughly flat).

One action per class, executed, not debated:
`data_error` → a `cleaning` entry with `fit_on` declared; when the offending
value is a **discrete sentinel**, add it to `data[].assertions.banned_sentinels`
so the existing profile gate adjudicates it. Range-shaped violations have no
assertion type in the closed vocabulary and the profiler records no numeric
min/max — record them in the dataset's `known_gaps` plus a findings-ledger row;
do not invent an assertion key.
`different_population` → a candidate segment, noted in `sampling_frame`.
`regime_change` → a stop-and-re-scope candidate; check it against `known_gaps`.
`heavy_tail` → robust summaries stand; never trim.

Table: column | n_flagged | pct_flagged | class | evidence | action_taken.

*Skip:* no rows beyond the fence → recorded. Columns flagged
`degenerate_scale` in 4a → `fence undefined`.

### 4d. Pathologies and impossible pairs
Two tables, one pass.

**Pathology sweep** — column | pathology | count | consequence:
- constant or near-constant: dominant-value share ≥ 0.99 — a dead column, or an
  upstream filter nobody declared;
- mixed types: a numeric column containing unparseable strings, or an object
  column at least 95% numeric-parseable;
- label variants: per categorical, distinct count raw vs after `lower().strip()`;
  a gap lists the colliding variants — one category silently counted as several
  corrupts segments and joins;
- disguised key: distinct ÷ rows > 0.95 (distinct copied from the profile) →
  reclassify as an identifier, exclude from categorical treatment, and say so;
- infinities: ±inf count per numeric column;
- whole-row duplicates, reported separately from step 1's key duplicates: exact
  copies = double-load; same key with different values = a versioned table being
  double-counted. Name which case this is (`duplicate_kind`).

**Impossible pairs** — enumerate cross-column invariants from four closed
families: ordered timestamps (created ≤ updated ≤ closed); part ≤ whole (refund ≤
revenue, clicks ≤ impressions); bounded (rates in [0,1], percentages in [0,100],
ages in [0,120]); derived = formula (total = price × qty within rounding). One
boolean test each. Table: invariant | n_violations | violation_share |
example_row_id.

Zero violations is a recorded result. A violated part ≤ whole pair is join
fan-out or a unit error until proven otherwise: trace one example row to source
when the source is queryable from this session; otherwise record
`trace: source unavailable` and raise that row to `caveat` or above, naming the
untraceability as its alternative explanation.

*Skip:* the sweep skips only on a refresh whose profile `source_hash` matches the
previously swept extract (`pathology sweep: unchanged`). Invariants skip only as
`invariants: none identified`, listing the columns considered — proving the
enumeration happened.

### 4e. Wide categoricals
For each categorical with more than 50 distinct levels **or** top-20 coverage
below 80% of rows, record: distinct count; coverage at top-5 / top-20 / top-50;
`rare_share` (rows in levels with fewer than 10 rows or under 0.1%); and
`singleton_levels`.

*Skip:* no column met the test → `wide categoricals: none; max distinct = <n>`.

For predictive work this table also carries a `policy_recommendation` per column
from the closed list `keep_all` | `group_below_n(<n>)` | `group_below_share(<s>)` |
`top_k(<k>)` | `drop_column` | `identifier`; `dsx-build-model` consumes or
overrides it and records which. An unhandled 40,000-level column becomes a
40,000-column design matrix. Coverage and `rare_share` are computed on training
rows only.

### 4f. Base rate
When a declared metric or target exists: table week | n | rate for the primary
metric or target, plus one row per `design.guardrail_metrics` entry. Record
`base_rate.overall`, `weekly_range [lo, hi]`, and
`verdict: stable | drifting` — drifting when any week sits beyond ±20% relative
to overall. **A base rate that drifts is a modelling constraint, not a
footnote.** The base rate and its drift may use the full frame; every
per-feature target relationship may not (see the split-first rule).

*Skip:* no declared metric and no target → `base_rate: null (<reason>)`.

---

**[Checkpoint]** Any `blocker` row in the findings ledger stops the run here.
Do not proceed to the branch. Follow the abort close-out in step 9.

---

## 5. Question-type branch
Exactly one branch runs, selected by `question_type` (and `design.kind` for
experiments) — except `prescriptive`, which runs 5D then 5F, because prescriptive
subsumes causal. No spec → no branch; record `branch.ran: none (no spec)`.

Every branch check that touches an outcome, a target or a metric is one row in
the comparisons ledger. **Split-first governs every target-conditional
statistic**: `dsx-build-model` step 2 fixes the split before profiling,
imputation or feature engineering, and EDA gets no exemption.

### 5A. Branch: descriptive — is the number the number?
1. **Recompute the headline** from `metrics[].numerator` / `denominator` exactly
   as the spec writes them: spec_value | recomputed_value | match (y/n, tolerance).
   A mismatch is a definition dispute: stop and reconcile through
   `dsx-define-metrics` before describing anything. EDA produces the pair; that
   skill owns the dispute.
2. **Denominator drift**, per ratio metric: denominator per period, max
   period-over-period change; flag above 10% — the rate moved because the base
   moved. *Skip:* no ratio metric declared.
3. **Mix vs level**: two numbers summing to the headline change over the primary
   segment dimension — `within_segment_component` | `mix_component`. Mostly mix
   means the stakeholder asked "what" but means "why": re-scope toward
   diagnostic through the branch verdict. *Skip:* no segment dimension.

Period boundaries are covered by 3a and concentration by 4b — cite those tables;
do not recompute them.

### 5B. Branch: diagnostic — decompose the change, account for all of it
1. **Change statement.** One row: metric | P0 | P1 | value_P0 | value_P1 |
   delta_abs | delta_pct. Cannot state P0, P1 and the metric → this is not yet a
   diagnostic question; re-scope.
2. **Additive decomposition.** Volume × rate, plus mix over one segment
   dimension (add price for revenue metrics). Columns: component |
   contribution_abs | contribution_pct_of_delta. **Rows must sum to
   `delta_abs`**; the unexplained row is named `interaction_residual` and is
   never omitted. The dimension is chosen by rule, not by feel: the spec's
   declared segment field when one exists, else the top-ranked split by step 6's
   rule.
3. **When `|interaction_residual| > 10%` of `|delta_abs|`**, decompose over the
   rule's next-ranked dimension and record both residuals side by side. **At most
   two dimensions are tried.** A residual still above 10% after the second is a
   `falls_short` input to the verdict — never a licence to keep hunting
   dimensions.
4. **Mix vs rate split.** Per segment: segment | share_P0 | share_P1 | rate_P0 |
   rate_P1 | within_contribution | mix_contribution. Copy `{name, effect, n}`
   rows into `results.segments` — that block drives the Simpson check.
5. **Denominator audit** (ratio metrics only): numerator and denominator at P0
   and P1, plus the rate recomputed holding the denominator at P0 →
   `denominator_driven_share`. *Skip:* count/sum metrics, with reason.
6. **Timing localisation.** `midpoint_date` = the day cumulative daily
   contribution reaches 50% of delta; list every `known_gaps` event within ±7
   days as `concurrent_events[]`. *Skip:* no daily time column.
7. **Concentration verdict.** Top component at or above 80% of the delta → name
   it; the diagnostic conclusion is about that segment.

Every later "accounted for X% of the change" must quote a
`contribution_pct_of_delta` cell, and nothing else.

### 5C. Branch: experiment (`design.kind: experiment`)
Tables, not advice.

1. **Assignment counts, arm × day.** day | n per arm | observed_share, plus
   cumulative totals and the max single-day deviation from
   `design.expected_allocation`. Copy totals into `results.observed_n`.
   Chi-square observed vs expected (agent-side): p < 0.001 means the assignment
   mechanism is broken — **stop, do not read outcomes**, find the defect. SRM is
   never noise you can adjust away.
2. **Sliced SRM.** Recompute per day and per segment using only columns present
   from {platform, browser, country, device} ∩ data: slice | n_per_arm | p |
   verdict. A mismatch confined to one day or one slice names a defect the total
   chi-square cannot. None of those columns present → `srm_slices: none available`.
3. **Multi-arm units.** `n_multi_arm` = units appearing in more than one arm, and
   its share. Nonzero is an assignment defect or an interference story — a ledger
   row, never noise.
4. **Differential attrition.** arm | assigned_n | outcome_observed_n |
   outcome_missing_rate | delta_vs_min_arm. A per-arm gap above 1 percentage
   point absolute, or a rate ratio above 1.1, is a **blocker candidate** under
   the same read-no-outcomes discipline as SRM: treatment that changes who logs
   an outcome at all biases every estimate computed from those who did. *Skip:*
   the outcome column has zero nulls in every arm — record the zeros.
5. **Pre-period A/A.** Primary outcome per arm on the window before assignment:
   arm | pre_mean | smd. `|SMD| > 0.05` → the arms differed before treatment
   (assignment or logging bias); stop. *Skip:* no pre-period.
6. **Weekly cycle.** Outcome or a guardrail by day of week, pre-period vs
   experiment period: dow | pre_mean | exp_mean | ratio. Record
   `weekly_cycle_amplitude` = (max − min daily rate) / overall.
7. **Run-window coverage.** `run_days`, `n_full_weeks = floor(run_days/7)`; flag
   fewer than one full week, or a window ending mid-cycle. EDA records the
   *inputs* to the novelty and primacy assessment. The week-1 vs week-2 effect
   ratio is a readout-stage statistic (`RESULTS.md#week1-vs-week2`) and is **not**
   computed here — `validity_frame.stability.novelty_primacy_assessed` is set at
   readout. EDA does not spend an interim look on the least-powered possible
   reading of the outcome.
8. **Triggering dilution.** eligible_n | triggered_n | observed_trigger_rate vs
   `validity_frame.triggering.expected_trigger_rate`;
   `dilution_factor = eligible / triggered`. *Skip:* triggering undefined.

When randomisation and analysis units may differ, compute the ICC of the outcome
on the candidate cluster variable (one-way ANOVA estimator) → front-matter
`dependence.icc`, the measured basis for the `variance_adjustment` declaration
`dsx-design-experiment` requires when the units differ (that skill declares
`cluster_robust` today with no measured input). Continuous outcomes: record
`outcome_sd` beside it. Neither is an input to any `dsx` command — `dsx power` is
two-proportion arithmetic — both are EDA-recorded inputs for agent-side design
and power arithmetic.

*Skip:* assignment log unavailable → skip checks 1–3 with
`assignment_log: unavailable` **and** downgrade
`validity_frame.identification.evidence` accordingly.

### 5D. Branch: causal / observational — is the design identified in THIS data?
1. **Treatment over time.** period | n | treated_n | treated_share. Any period at
   0 or 1 has no contemporaneous comparison — flag it.
2. **Never- and always-treated.** never_treated_n | never_treated_share |
   always_treated_n | always_treated_share. These bound who the estimand can
   cover.
3. **Balance.** Every declared covariate: covariate | mean_treated |
   mean_control | standardized_mean_difference; count `|SMD| > 0.1`. This is the
   evidence line for `validity_frame.identification.strength` — `strong` beside
   SMDs above 0.5 is a contradiction to record, not to smooth over.
4. **Common support.** Primary form, whenever at least one declared covariate
   exists: a treated × control cross-tab over deciles of the top declared
   confounder — `n_empty_cells`, the share of treated rows in cells with zero
   controls, and the converse. Optional propensity form only with two or more
   covariates: logistic regression, library defaults, **seeded**, covariates
   exactly as declared; record estimator, parameters and seed so a rerun refits
   identically. Off-support share above 20% → the estimand shrinks to the
   supported region; say so. Neither form possible → `common support:
   not_assessable`, and flag identification.
5. **Pre-trends** (`identification: difference_in_differences` only): period |
   treated_mean | control_mean | gap over at least three pre-periods; point
   `design.parallel_trends_evidence` at `EDA.md#pre-trends`. *Skip otherwise,
   with reason.*
6. **Adoption cohorts.** `n_adoption_cohorts` = distinct first-treatment periods.
   More than one means staggered adoption — record it; it constrains the
   estimator, and the architect must know before modelling.
7. **Collinearity** (`regression_adjustment` or `matching`): VIF per declared
   covariate; any VIF above 10 → a `caveat` row against
   `validity_frame.identification.strength`.

### 5E. Branch: predictive — split declared before any target statistic
1. **Split declaration first.** Before **any** feature-vs-target number, write:
   split | period | rows | positive_rate for train/validation/test, plus the
   embargo gap in days. Copy the periods into `model.train_period` /
   `model.test_period`. A target statistic computed before this table exists is a
   protocol violation — restart the branch.
2. **Availability audit.** Requires `model.prediction_time_definition`. Absent →
   file a `spec-amendment` row, record
   `blocked_on: prediction_time_definition`, and mark every audit row
   `available_at_prediction_time: unknown` until `dsx-scope-analysis` supplies
   it. EDA never authors design decisions; it measures against them.
   Table: feature | source | available_at_prediction_time (yes|no|unknown) |
   reason. The `no` and `unknown` rows **are** the leakage-suspects list: copy
   them into `model.features_excluded_for_leakage`, or justify each retention.
3. **Suspiciously-strong screen** (training rows only): feature | statistic |
   threshold | verdict. Single-feature AUC above 0.90, or `|r| > 0.8`, is a
   leakage suspect with a named reason — not a great feature.
4. **Target drift.** Cite 4f's weekly table; add monthly periods when the window
   is long. Any period beyond ±20% relative to the training-period mean →
   a `limitations` entry.
5. **Feature stability.** PSI per feature, training period vs latest period:
   feature | psi | flag (psi > 0.2); name the top five drifting. *Skip:* one
   period only → `psi not computable`.
6. **Entity overlap.** `n_entities_in_both_train_and_test`. Nonzero → the split
   must be `grouped_temporal`; record the count in
   `results.train_test_overlap_rows` and set `model.entity_column`.
7. **Wide-categorical policy.** The 4e table plus one `policy_recommendation`
   per wide column.

Correlations among features are not the goal of this branch and a full-frame
correlation matrix is not evidence. Split, then audit availability, then measure
drift.

### 5F. Branch: prescriptive — the decision inputs are data too
Runs after 5D. Checks 1–4 always run; none of them needs the causal estimate.

1. **Decision-input table.** Every parameter in `decision.decision_rule`'s cost
   model: parameter | point_value | p10 | p90 | basis (measured|assumed). Each
   `assumed` row becomes an `assumptions[]` entry with `impact_if_wrong`. The
   rule names no cost parameters → re-scope: a prescription without costs is a
   preference.
2. **Never-treated share** of the target population for the proposed action:
   never_treated_n | share. Zero → everyone already gets it, and the prescription
   is a removal question; re-scope.
3. **Break-even.** For the widest-interval parameter: the value where expected
   value crosses zero, against its p10–p90. Output: break_even_value |
   sign_robust_in_observed_range (y/n). Not robust → a `limitations` entry.
4. **Feasibility**, when capacity is stated: n_treated_at_threshold vs capacity →
   feasible (y/n). Capacity unstated is itself a recorded finding.

No causal estimate with an interval yet → the branch **verdict** records
`blocked_on: causal_estimate`. That blocks the prescriptive *conclusion*, not
these measurements, which stand as inputs awaiting the estimate.

### Branch verdict — every branch ends with one line
`verdict: meets | falls_short | re-scope` against the type's minimum-evidence bar
(`references/question-taxonomy.md`). When `falls_short`, add
`downgrade_to: <type>` and name the missing evidence.

Triggers: descriptive — the headline does not reproduce from its own definition;
diagnostic — `interaction_residual` above 10% after two dimensions; experiment —
unresolved SRM or differential attrition, or under one full week;
causal — off-support share above 20%, or diverging pre-trends; predictive —
`unknown` availability rows left on retained features; prescriptive — no causal
estimate.

**A recorded downgrade is a legitimate deliverable.** "We can say what changed
and when, not why" beats a confident coefficient. Amend `question_type` through
stop-and-re-scope; do not soldier on to the original licensed verb.

## 5x. Optional routines
Both are optional, run only after steps 1–4 and after step 6's planned-cuts list
is written, and are **exploratory — never evidence**.

- **Correlation funnel** (binarize → Pearson → tornado; reference implementation
  `funnel_correlation_py`): only when a binary or binarizable target exists.
  Datetime columns dropped or recoded first. Unresolved missingness → skip; do
  not impute in order to draw a funnel. Training rows only on predictive work —
  quantile cuts fitted on the full frame leak. Rare positives (under 5%)
  attenuate r; say so. Pearson on 0/1 columns is a phi coefficient: it ranks, it
  never carries a causal verb.
- **Conversion funnel** (ordered step drop-off): only when the question declares
  an ordered event sequence, and only after its integrity precondition — compute
  `n_ordering_violations` (units whose step-k timestamp exceeds their step-k+1
  timestamp) as a row in 4d's ordered-timestamps family, plus `violation_share`.
  Above 1% → the funnel is blocked, the number recorded, a ledger row filed.
  Below it, violating units are excluded and the exclusion count is reported
  beside every drop-off figure. This is **not** the correlation funnel; do not
  conflate them.

Every bin, bar and correlation inspected is a comparisons-ledger row. No funnel
result is promoted into `decision.replay` or a confirmatory claim without a spec
amendment through step 6.

*Skip:* `no binarizable target` / `no declared event order`, recorded.

## 6. Segments
"The most important splits" is computed, not felt.

1. **Declared cuts first.** Write the planned-cuts list: cut | source, where
   source is `design.multiplicity.family` (segment tests already declared for
   correction), a segment column named elsewhere in the spec, or
   `rule: top-k by between-level spread of the headline` (max pairwise gap for
   rates, eta² for continuous; k = 2, plus the time column bucketed to at most 12
   periods). Categoricals are eligible at 2–20 levels. Note that
   `results.segments` is filled at execute and is empty now.
2. **Compute exactly these.** Table: split | level | n | value | overall | delta |
   sign_agrees (y/n) | thin (y when n is under 1% of rows). Report
   `sign_agreement_rate` per split. Thin levels never headline.
3. **Simpson candidates.** Every `sign_agrees: n` level is copied as
   `{name, effect, n}` into `results.segments`, so the existing Simpson check
   adjudicates it. A reversal in a non-thin level inside the claim population is
   a stop-and-re-scope trigger. Replace-on-execute semantics: confirmatory
   execution recomputes and **replaces** `results.segments`; the EDA.md table
   remains the exploratory record. A reversal present here but absent from the
   confirmatory recompute is a `caveat` row, with the discrepancy as its
   discriminating number.
4. **Candidate handshake.** Emit at most five ranked `segments_candidates` in
   front-matter (column, levels, headline_range, n_min; any cell under n = 30
   marked `underpowered` — it stays a candidate, never a claim). Candidates are
   hypotheses. `ANALYSIS-SPEC.yaml` has no pre-declared-cuts field, so promoting
   one is a spec amendment through `dsx-scope-analysis` that adds the intended
   confirmatory test to `design.multiplicity.family` — the object the existing
   `comparisons_looked_at` check adjudicates. Per the `dsx-design-experiment`
   readout rule, a segment result whose test is not in that family is labelled
   exploratory at verify. **EDA never promotes a candidate into
   `decision.replay`.**
5. **Unplanned cuts.** Any further cut goes under `### Unplanned cuts` with a
   one-clause reason. It increments the comparisons ledger and may file findings
   rows, but it cannot become a headline finding unless the spec is amended to
   declare it.

*Skip:* no headline metric and no target → recorded. No categorical with 2–20
levels and no time column → `no split available`, and mark the reversing-segment
row of step 10 accordingly.

## 7. Second-order look
Compute the headline number the decision turns on. Then attack it. For **every**
mechanism below whose input exists, compute the discriminating number and give a
verdict — there is no plausibility selection, so two runs produce the same rows:

| mechanism | discriminating number |
|---|---|
| denominator_drift | denominator count per period; max period-over-period change |
| mix_shift | headline recomputed at first-period segment weights; delta vs raw |
| boundary_completeness | rows/day in the first and last three days vs the daily median |
| leverage | headline recomputed excluding the top 1% of rows by contribution (precomputed in 4b) |
| duplicate_inflation | headline recomputed after dedup on the declared grain; delta vs raw |
| sentinel_contamination | headline recomputed excluding declared sentinels; delta vs raw |

Table `second_order`: mechanism | discriminating_number | value | verdict
(`supports_artifact` / `refutes_artifact` / `inconclusive`) | evidence. A
mechanism whose input is absent records `n/a` — never an omitted row. A mechanism
the branch already computed (denominator drift, mix shift) is **cited** from the
branch table with its verdict, not recomputed.

Close with `artifact_status: clean | contested | supports_artifact`. A
`supports_artifact` verdict is a stop-and-re-scope trigger, not a footnote.

*Skip:* no declared metric and no target → `no headline metric declared`.

## 8. Spec reconciliation
The last analytical step. One row per spec path: spec_path | spec_value |
eda_value | verdict | action. The verdicts are closed:

- **confirms** — the spec matches the measurement; no action.
- **fills** — the spec is null or `not_assessed`; write the measured value into
  the spec with `EDA.md#<heading>` as its evidence.
- **contradicts** — the spec disagrees with the measurement. **Stop.** Set
  `stop_triggered: true`, list the path under `contradictions:`, and hand back to
  `dsx-scope-analysis` before any modelling or inference.

**This table is where stop-and-re-scope fires from — not from judgement.**

Fixed rows (add rows, never remove):

| spec_path | measured against |
|---|---|
| `validity_frame.units.observation` | `grain.observed` |
| `validity_frame.dependence.structure` / `cluster_var` | `grain.implied_dependence` (with `method_family_required` owed when structure is not `none`) |
| `validity_frame.missingness.mechanism` | the worst mechanism in `missingness[]` (`MNAR` > `MAR` > `MCAR`; `not_assessed` on any key column outranks all) |
| `validity_frame.missingness.rate` | the max rate in `missingness[]` |
| `validity_frame.sampling_frame.known_exclusions` | exclusions found in steps 1–4 |
| `validity_frame.measurement.known_gaps` | measurement-shaped findings only: a `truncated` tz verdict, sentinel contamination of a measured column, or a metric-definition mismatch from 5A. Outages and backfills reconcile through `data[].known_gaps`, not here |
| `data[].rows` / `period` / `known_gaps` | profile row_count, time min/max, gaps |
| `design.baseline_rate` (experiment only) | `base_rate.overall` from 4f |

A spec field that does not apply to this `question_type` records `n/a` with the
reason. No spec → the whole step records `no spec in phase dir`, with
`contradictions: []`.

</protocol>

<registers>

## 9. Findings ledger
Every flag raised in any step is filed the moment it fires — no anomaly lives
only in prose. Columns: id (F-nn) | step | finding (one number, with units) |
severity | alternative_explanation | discriminating_number | consequence.

Severity is closed, and each severity has a non-optional consequence:

- **blocker** — the data contradicts a spec declaration (grain, period,
  population, missingness mechanism), or the design's integrity fails (SRM,
  differential attrition, pre-period imbalance, fan-out on a declared one-to-one
  join, `artifact_status: supports_artifact`, a non-thin segment reversal inside
  the claim population), or the numbers are irreproducible (rerun mismatch).
  **Stop at the step where the row fired**; run no further analytical step. Still
  write the close-out for work already done: this ledger; step 10 rows for steps
  that ran, the rest marked `skipped: aborted`; the comparisons ledger for looks
  actually taken; reconciliation rows computable from completed steps. Set
  `stop_triggered: true` and `completed_through: <last completed step>`, and hand
  back to `dsx-scope-analysis`. Write **no** fills and no spec side-effects except
  `contradictions[]` and the comparisons count for looks actually taken.
- **spec-amendment** — a spec field is wrong but the design survives: name the
  field, patch it, run `dsx validate`, record its exit in the consequence cell,
  then continue.
- **caveat** — survives EDA but must land in `limitations[]` or the dataset's
  `known_gaps`: name the destination and write the `draft_limitation` sentence
  `dsx-narrate` may reuse verbatim.
- **note** — recorded, no action.

For every row at `caveat` or above, `alternative_explanation` names the strongest
competing explanation and `discriminating_number` cites the value already in this
file that separates them, or `untested` — and an untested row must state why
proceeding is safe. "The data is weird" is not an explanation.

`consequence` records the action taken, not the plan. **EDA is not complete while
any blocker or spec-amendment row has an empty consequence.** Close with
`ledger_rows: N`. Zero anomalies is itself a claim: file
`F-00 | all | none found | note | — | — | see Searched-not-found`.

*Never skipped.* An aborted run still ships its ledger — the abort is its top row.

## 10. Searched, not found
Fill the fixed-row register — one row per pathology this protocol hunts:
duplicates on the declared grain; structured nulls vs time; structured nulls vs
target (train rows only); timezone mismatch; daily-volume spikes or outages;
sentinels; a category that stops appearing; base-rate drift; a reversing segment;
join fan-out (when any join ran); whale concentration; impossible pairs. The
branch that ran appends its own rows (SRM, attrition, pre-trend divergence,
leakage suspects on retained features).

Columns: pathology | checked (yes | skipped:`<reason>`) | result
(found:F-nn | not_found) | evidence.

**`not_found` requires the computed number that demonstrates absence** — e.g.
`dup_rate = 0.0%` — never a bare "no". `found` points at a findings-ledger id.
A step cannot be skipped and then claimed clean.

## 11. Comparisons ledger
Every exploratory statistic computed against an outcome, target or metric — a
correlation, a segment recompute, a funnel bin, a branch check, a cut computed
and discarded — is one comparison, **counted at its first computation**, not when
reported. Append as you look: k | what_was_compared | step | kept_as_candidate
(yes/no).

**Counting unit, closed:** one row per (statistic × split-or-column), never per
level or cell. A segment split's full level table is one row. Each
correlation-funnel feature is one row. Each branch check touching the outcome is
one row. The step-6 ranking scan is one row per categorical scanned. State the
rule in the ledger header so counts compare across runs.

A re-execution of the same script over the same extract (step 12, or a resume
after re-scope) reproduces looks already in the ledger: **it never appends.** Diff
the regenerated looks against the ledger; only a look absent from it — a new cut,
a new step, a new extract by `profile_source_hash` — earns a row. Counting
executions instead of looks would double `comparisons_looked_at` and make a
fixed-horizon experiment look like uncontrolled peeking.

Close with `comparisons_this_run: N` (N = ledger rows) and write it into
`results.comparisons_looked_at`, additively with later confirmatory looks — never
reset, never confirmatory-alone, never re-added for rows already counted. For
experiments, outcome looks also increment `results.interim_looks` under the same
first-computation rule. A headline citing a cut absent from this ledger is a
blocker. A cut promoted to a confirmatory result must show
`kept_as_candidate: yes` here **and** a matching entry in
`design.multiplicity.family` — this ledger is the garden-of-forking-paths
evidence either way.

*Skip:* only when no statistic touched any outcome or metric (pure trust
profiling of a lookup table) → `comparisons_this_run: 0 (no outcome touched)`.

## Hypothesis register
The findings, comparisons and searched-not-found ledgers above ARE the hypothesis
register — no new format and no new spec field. Every untested belief the analysis
rests on is routed to a carrier a shipped check already reads, keyed on its shape:

- **An untested belief the analysis leans on** (a load-bearing assumption — "the
  join is one-to-one", "the pre-period is comparable") becomes a row in
  `assumptions[]` (`{assumption, rationale, impact_if_wrong, checked, waiver}`).
  `DSX-COH-030` requires the register present when the question is causal or
  prescriptive; `DSX-COH-031` requires each row `checked: true` XOR a `waiver`.
- **A belief promoted to a confirmatory test** is declared in
  `design.multiplicity.family[]` at scope time and filled in `results.tests[]` at
  execute, adjudicated by `DSX-EXP-050..053` (a test outside the declared family
  is exploratory at verify). Promotion follows the §6 step-4 candidate handshake —
  a spec amendment through `dsx-scope-analysis`; EDA never promotes a candidate
  into `decision.replay`.

This rule only says which existing carrier each hypothesis lands in so a
deterministic check adjudicates it; it rides the EDA.md ledgers and declares no
new spec field.

</registers>

<close_out>

## 12. Write the spec, once
Spec side-effects are written **exactly once**, here, after every analytical step
has settled: step 8's `fills`; `results.segments` from step 6; `model.*` fields
from 5E; `results.observed_n` and `interim_looks` from 5C;
`results.comparisons_looked_at` from step 11; `cleaning` entries from 4b/4c.
`dependence.method_family_required` is an analyst declaration owed whenever the
implied structure is not `none` — not a measured fill.

Then run `dsx validate --phase-dir <phase-dir>` and record its exit status in
`EDA.md`. An out-of-vocabulary fill — a misspelled mechanism, a malformed
segments row — is otherwise discovered at the next gate, far from the write and
blamed on the wrong actor.

## 13. Rerun contract (last action)
EDA is a script; prove it. Re-run it once from a clean interpreter in
**comparison mode**: it computes every number and **writes nothing** — no spec
writes, no ledger appends, no fills — emitting the regenerated values to a
scratch path.

Diff scope: front-matter values only (ledger counts compared as the recorded
integers). Tolerance: exact for integers and strings; floats equal at their
printed precision. Section tables are regenerated but not diffed cell by cell;
the ledgers are behaviour records and are out of scope. The seed comes from
`reproducibility.random_seed`.

Record `rerun_clean: yes|no`, `rerun_mismatches: N`, `seed: <value>`. N above
zero is a **blocker**: the numbers are irreproducible — hidden state, unseeded
sampling, or a mutating source — and nothing downstream may cite them until N is
zero or the mutating source is named in the dataset's `known_gaps`.

*Skip:* a warehouse-only source where re-querying is rate-limited or costly →
`rerun_clean: not_verified (<reason>)`. A local extract never qualifies.

## 14. Lifecycle
- **After a stop.** `dsx-scope-analysis` owns the amendment and clears
  `stop_triggered`. On re-entry the trust core always re-runs; a branch re-runs
  when any of its inputs changed. Resume from `completed_through` only when the
  amendment touched nothing the completed steps measured.
- **On supersede.** Never overwrite an `EDA.md` whose contradictions were cited
  in a hand-back: archive it as `EDA-<source_hash_prefix>.md` and start fresh.
- **On refresh.** A new extract means a new `profile_source_hash`, and a new
  `EDA.md`. Same hash, same file.

</close_out>

<output>
`EDA.md` — start from `templates/EDA.md`, keep its front-matter contract and its
fixed headings in protocol order. Downstream steps read the front-matter; the
prose is the evidence trail. **A front-matter value with no anchor in a section
table is an invented number.** A skipped step keeps its heading with
`skipped: <reason>`; its front-matter key is `null`, never absent.

Plus a hermetic profile:

1. Prefer a local extract. Run:
   `dsx profile <extract.csv> --out DATA-PROFILE.yaml --pk <key> --time <col> --sentinel -1 --sentinel 999`
2. Wire into `ANALYSIS-SPEC.yaml` under `data[]`:
   - `profile_path: DATA-PROFILE.yaml`
   - `assertions:` for row_count, primary_key, max_null_rate, max_gap_days, banned_sentinels
   - durable facts: period, rows, known_gaps
3. Never invent profile numbers. If the source is warehouse-only, export a CSV first or write
   `computed_by: measured_export` with the query that produced the counts — not `manual`
   without a known_gaps note.

Plus a data dictionary, authored next to the profile:

4. Right after `dsx profile` runs, author `DATA-DICTIONARY.md` next to `DATA-PROFILE.yaml`,
   starting from `templates/DATA-DICTIONARY.md`. **Copy** the column roster (`column`, `dtype`,
   `null_rate`, `unique_count`) and `source_hash` **verbatim** from `DATA-PROFILE.yaml` — the same
   "never invent profile numbers / one extract, one set of numbers" discipline the `EDA.md` copy
   already follows; a roster that disagrees with the profile is an invented number. Then **author**
   only the semantics the CSV cannot carry: `grain` (one row = one ...), `primary_key`, `join_keys`
   ({column, joins_to, cardinality}), per-column `semantic_type` (closed set), `description`,
   `source`, `pii`, plus `timezone` and `owner`. The dictionary is **written and read by later
   sessions but NOT gated** — no `dsx` check opens it, so it mints no finding code (the `EDA.md`
   precedent). Do not add or imply a gate for it.

The execute/verify gates compare assertions to the profile artifact. They do not open the
warehouse, and they do not read `EDA.md` or `DATA-DICTIONARY.md`.
</output>
