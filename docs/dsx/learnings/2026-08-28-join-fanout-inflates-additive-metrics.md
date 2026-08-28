---
date: 2026-08-28
title: A join fan-out other than 1.0 silently inflates every additive metric computed after it
domain: business_intelligence
question_type: diagnostic
tags: [grain, join-fanout, additive-metrics, data-onboarding]
metrics: [revenue]
phase: 14
source_spec: none
outcome: A total that looks too high after a join is fan-out until proven otherwise — check fanout == 1.0 on every declared one-to-one join before framing, not the number itself.
---

## What

A join declared one-to-one that actually fans out — any `fanout` value other than
`1.0` — silently multiplies the row count on the fanning side, and therefore
**inflates every additive metric computed after the join**. Sum an additive column
(revenue, units, sessions) across the fanned-out result and the total is wrong by the
fan-out factor, with no error raised: the join succeeds, the rows just quietly
duplicate. The fan-out matrix in `dsx-explore-data`
(`join_id | left | right | keys | type | rows_before | rows_after | fanout |
left_match_rate | null_key_rate`) is where this becomes visible — a `fanout` column
that is not `1.0` on a join declared one-to-one is the tell.

## So What

A total that looks *too high* right after a join is **fan-out until proven
otherwise**, not a genuine uplift. The fix is to find which side of the join carries
the duplicate grain and correct the join — never to "divide the number down" to make
it look right, which hides the grain error and leaves the next metric wrong too.
Fan-out is the single most common cause of numbers that disagree, and it is
structurally invisible unless you measure it, because nothing in the join itself
fails.

## Now What

Before framing an analysis on joined sources, **build the fan-out matrix and confirm
`fanout == 1.0` on every join declared one-to-one.** Treat any mismatch as a blocker
on the framing — resolve the grain (identify the duplicating side, fix or
de-duplicate the join) before any additive metric is computed or reported, not after.
If a prior spec already asserted a one-to-one join here, this file is the standing
reason to re-check it rather than trust it.
