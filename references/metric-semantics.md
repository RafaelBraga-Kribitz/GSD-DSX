# Metric semantics

One number, one meaning. Most reconciliation incidents are two correct
computations of two different definitions.

## The definition contract

| Field | Why mandatory |
|---|---|
| name | stable, snake_case, unique in the registry |
| definition | a computable expression, not a label |
| grain | what one row represents; determines whether a sum double-counts |
| numerator | with filters stated |
| denominator | with filters stated |
| timezone | daily aggregates differ by a few percent between UTC and local |
| source | the table of record |
| owner | who arbitrates a change |

A ratio without an explicit denominator will drift the first time someone adds a
filter, and nobody will notice until finance disagrees.

## Reconciliation order

Sorted by how often each is the culprit:

1. **Time boundary.** Different timezones, or `BETWEEN` on a timestamp silently
   dropping the last day's events after 00:00:00.
2. **Filters.** Test accounts, internal traffic, bots, refunds, cancellations —
   excluded upstream in one source, not the other.
3. **Join fan-out.** One-to-many joins multiplying rows before aggregation.
4. **Late-arriving data.** The two extracts were taken on different days and the
   table backfills.
5. **Deduplication.** Different definitions of a duplicate.
6. **Aggregation order.** Average of ratios versus ratio of sums.

Record the resolution and the agreed tolerance in the spec. `dsx check metrics`
then enforces it on every subsequent run, so the reconciliation does not have to
be redone from memory.

## Traps in aggregation

**Average of averages.** `AVG(clicks / impressions)` weights a row with 10
impressions the same as one with 10 million. Use `SUM(clicks) / SUM(impressions)`.

**Simpson's paradox.** The aggregate can move opposite to every segment when the
segment mix changes. Always recompute the headline number inside the two or three
most important splits. If they disagree with the aggregate, the segments are the
finding.

**Denominator drift.** A period-over-period ratio comparison is only meaningful
if the denominator is comparable. If the population grew 40%, the ratio change is
partly composition. Decompose, or compare on a fixed cohort.

**Count distinct across a join.** `COUNT(DISTINCT x)` after a fan-out join is
correct; `COUNT(x)` is not, and `COUNT(*)` after a `LEFT JOIN` counts
non-matching rows as 1.

## SQL traps

| Pattern | What goes wrong |
|---|---|
| `NOT IN (SELECT …)` | returns zero rows if the subquery yields any NULL |
| `COUNT(*)` after `LEFT JOIN` | counts non-matches as 1 |
| `BETWEEN` on a timestamp | excludes everything after 00:00:00 on the end date |
| bare `UNION` | silently deduplicates |
| filter in an outer-join `ON` | silently converts it to an inner join |
| `SELECT DISTINCT` | usually patches a fan-out instead of fixing it |
