---
name: dsx-define-metrics
description: "Define, register and reconcile metrics so one number means one thing. Use when creating a metric, building a dashboard, or investigating why two sources disagree."
argument-hint: "[metric-name] [--reconcile] [--sql <file>]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
---

<objective>
A metric definition precise enough that two people implementing it independently
produce the same number.
</objective>

<definition_contract>
Every metric declares, without exception:

| Field | Why it is mandatory |
|---|---|
| `name` | snake_case, stable, unique |
| `definition` | a computable expression, not a label |
| `grain` | what one row represents — determines whether a sum double-counts |
| `numerator` | with its filters stated |
| `denominator` | with its filters stated — most disputes are denominator disputes |
| `timezone` | daily aggregates in UTC and local time disagree by a few percent |
| `source` | the table of record |
| `owner` | who arbitrates a change |

Search the semantic layer, dbt models and existing dashboards before writing a
new definition. Two definitions of one word is the most expensive artefact you
can create.
</definition_contract>

<reconciliation>
When sources disagree, find the definitional difference. Do not average them.
Work this order — sorted by frequency:

1. Time boundary — timezone, or `BETWEEN` on a timestamp dropping the final day.
2. Filters — test accounts, internal traffic, bots, refunds, cancellations.
3. Join fan-out — one-to-many multiplying rows before aggregation.
4. Late-arriving data — the two extracts were taken on different days.
5. Deduplication rules.
6. Aggregation order — average of ratios versus ratio of sums.

Record the outcome in the spec's `reconciliation` block with an agreed tolerance.
`dsx check metrics` then enforces it on every run.
</reconciliation>

<sql_review>
```bash
dsx check metrics --phase-dir <phase-dir> --verbose
```
Lints for `NOT IN` against a nullable subquery, `COUNT(*)` after a `LEFT JOIN`,
averaging a ratio, bare `UNION`, `BETWEEN` on timestamps, and aggregation across
multiple joins with no fan-out guard.

Read for what the linter cannot: does the result's grain match the declared
grain, and is every filter in `WHERE` rather than in an outer-join `ON` clause
where it silently converts the join to an inner one.
</sql_review>

<references>
@references/metric-semantics.md
</references>
