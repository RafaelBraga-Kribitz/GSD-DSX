---
name: dsx-funnel
description: "Route an ordered step-conversion / drop-off question to the existing metric, chart-matrix and conversion-funnel gates that already adjudicate it. Use when the question is 'how many drop off between step N and step N+1', not to author new funnel rules."
argument-hint: "[funnel-steps] [--event-field <name>]"
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
`dsx-funnel` is a ROUTER, not an author. It does not define what counts as a step-conversion rate,
which mark is admissible for an ordered-event visual, or how to test whether the step ordering
itself is trustworthy before you draw the funnel — those rulings already live in shipped,
deterministic checks. This skill's only job is to tell you which `ANALYSIS-SPEC.yaml` field to
fill for a funnel question and which existing gate or routine reads it.
</objective>

<when_to_reach_for_this>
Reach for `dsx-funnel` when the question is shaped like "of the units that entered step 1, what
share reaches step 2, step 3, … step N" — an ordered event sequence with drop-off between
consecutive steps. If the question is instead about a cohort's return rate over calendar periods
rather than an ordered step sequence, use `dsx-cohort`. If it is about *why* the drop-off differs
between segments, use `dsx-root-cause` or `dsx-segment`.
</when_to_reach_for_this>

<field_to_gate_routing>
## What you write, and which existing gate reads it

| `ANALYSIS-SPEC.yaml` field you fill | What it looks like for a funnel question | Existing gate that adjudicates it |
|---|---|---|
| one `metrics[]` entry per step-conversion | a `type: ratio` metric per step transition, with `numerator` = units reaching the next step and `denominator` = units reaching the current step, both declared explicitly | the metric structural checks `DSX-SPEC-020` through `DSX-SPEC-026` in `dsx/spec.py`, plus the `DSX-MET-*` metric-semantics family in `dsx/checks/metrics.py` |
| a chart declaration with `data_input_type: event-time` and mark `funnel` | the ordered step visual itself | the chart matrix consulted through `dsx charts` — the `funnel` mark is admitted only under `data_input_type: event-time`; any other pairing is refused by `DSX-VIZ-013` |

Run `dsx charts event-time` (or `dsx charts <shape>`) before declaring the mark, and `dsx gate
plan` / `dsx check` before treating the metric declarations as settled.
</field_to_gate_routing>

<ordering_integrity_routing>
## Before you draw the funnel: route to the existing conversion-funnel routine

A funnel built on out-of-order events is not a funnel, it is noise shaped like one. This skill
does not restate that check or its threshold — `dsx-explore-data` already owns the conversion-
funnel ordering routine (its "Conversion funnel" step under exploratory branch 5). That routine
computes the ordering-violation count and share for the declared step sequence, decides whether
the funnel is blocked or the violating units are excluded, and files the ledger row. Run
`dsx-explore-data`'s conversion-funnel step first and follow its verdict; do not re-derive an
ordering-violation rule inside this skill or inside the spec you are filling.
</ordering_integrity_routing>

<what_this_skill_does_not_do>
This skill states no threshold of its own: no conversion-rate floor, no ordering-violation
tolerance, and no rule for which event-time mark reads best beyond the `funnel`/`event-time`
pairing the chart matrix already enforces. Those rulings belong to `DSX-SPEC-020` through
`DSX-SPEC-026`, `DSX-MET-*`, `DSX-VIZ-013`, and the existing conversion-funnel routine in
`dsx-explore-data` — run them and read their output. Filling the field and citing the gate is the
whole contract; restating the gate's rule here would create a second, drifting copy of the advice
the gate already owns.
</what_this_skill_does_not_do>
