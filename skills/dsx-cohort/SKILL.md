---
name: dsx-cohort
description: "Route a retention / cohort-grid question to the existing metric, chart-matrix and coherence gates that already adjudicate it. Use when the question is 'what share of a cohort returns, by cohort and by period' — not to author new retention rules."
argument-hint: "[cohort-field] [--metric <name>]"
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
`dsx-cohort` is a ROUTER, not an author. It does not define what "good retention" is, which
mark is allowed for a cohort grid, or when a re-visit trigger is discriminating enough — those
rulings already live in shipped, deterministic `dsx` gates. This skill's only job is to tell you
which `ANALYSIS-SPEC.yaml` field to fill for a cohort/retention question and which existing gate
reads it. Every number this skill would otherwise state lives in the gate it points at, not here.
</objective>

<when_to_reach_for_this>
Reach for `dsx-cohort` when the question is shaped like "of the users/accounts/orders that
entered in period N, what share is still active/returning in period N+k" — a cohort grid, a
retention curve, or a returning-cohort comparison. If the question is instead about ordered
step-to-step conversion through a funnel, use `dsx-funnel`. If it is about *why* a metric moved
between segments, use `dsx-root-cause` or `dsx-segment`.
</when_to_reach_for_this>

<field_to_gate_routing>
## What you write, and which existing gate reads it

| `ANALYSIS-SPEC.yaml` field you fill | What it looks like for a cohort question | Existing gate that adjudicates it |
|---|---|---|
| a `metrics[]` entry | a retention-ratio metric: `type: ratio`, with `numerator` = retained-in-period count and `denominator` = cohort-entry count, both declared explicitly | the metric structural checks `DSX-SPEC-020` (a metrics block exists at all) through `DSX-SPEC-026` (a ratio metric must declare both numerator and denominator) in `dsx/spec.py`, plus the `DSX-MET-*` metric-semantics family in `dsx/checks/metrics.py` |
| a chart declaration with `data_input_type: matrix` | the cohort grid itself (cohort-period × cohort-age) | the chart matrix consulted through `dsx charts`, adjudicated by `DSX-VIZ-013` — it fires when the declared mark is not admissible under the declared `data_input_type` |
| `decision.revisit_when` | the condition under which this retention read gets re-examined | the coherence check `DSX-COH-040`, which fires when `revisit_when` is missing or is not a usable, discriminating re-visit trigger |

Run `dsx gate plan` after filling the spec, `dsx charts matrix` (or `dsx charts <shape>`) before
picking a mark for the grid, and `dsx check` before treating any of the above as settled. The gate
output is the ruling; this skill only tells you where to look.
</field_to_gate_routing>

<naming_caveat>
## Naming caveat — read this before citing a code

`DSX-COH-*` is the **Coherence** family (question / claim / decision agreement) — the letters are
not short for "cohort". There is no `DSX-COH-*` family dedicated to cohort analysis. `dsx-cohort`
routes its re-visit trigger to the existing coherence check `DSX-COH-040` because a cohort read
needs a re-visit trigger like any other decision does — the routing is a consequence of that
shared need, not evidence of a cohort-specific family. When you cite `DSX-COH-040` in a spec,
comment, or narrative, name it as the existing coherence `revisit_when` check.
</naming_caveat>

<what_this_skill_does_not_do>
This skill states no threshold of its own: no retention-ratio floor, no minimum cohort size, no
rule for which chart mark within the `matrix` family reads best, and no wording for a
discriminating `revisit_when`. Those rulings belong to `DSX-SPEC-020` through `DSX-SPEC-026`,
`DSX-MET-*`, `DSX-VIZ-013`, and `DSX-COH-040` respectively — run the gates and read their output.
Filling the field and citing the gate is the whole contract; restating the gate's rule here would
create a second, drifting copy of the advice the gate already owns.
</what_this_skill_does_not_do>
