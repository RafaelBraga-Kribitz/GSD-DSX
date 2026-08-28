---
name: dsx-root-cause
description: "Route a 'why did this metric move' diagnostic question to the existing decomposition, Simpson-reversal and causal-guard gates that already adjudicate it. Use for diagnostic attribution work, not to author a new causal claim."
argument-hint: "[metric-name] [--dimension <field>]"
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
`dsx-root-cause` is a ROUTER, not an author. It does not define what counts as a valid
decomposition, what reversal trips the Simpson check, or when a diagnostic finding is allowed to
read as causal — those rulings already live in shipped, deterministic `dsx` gates. This skill's
only job is to tell you which `ANALYSIS-SPEC.yaml` field to fill for a diagnostic "why did X
move" question and which existing gate reads it. Every number this skill would otherwise state
lives in the gate it points at, not here.
</objective>

<when_to_reach_for_this>
Reach for `dsx-root-cause` when the question is shaped like "why did this metric move between P0
and P1" — a decomposition/attribution question over observed data, not a forecast and not a claim
about what an intervention would do. If the question instead asks how a metric splits across many
cuts at once, without an implied single "why", use `dsx-segment`. If the question requires an
identification strategy for what an intervention caused, that is a causal question, not a
diagnostic one — route it through `dsx-design-experiment` instead.
</when_to_reach_for_this>

<field_to_gate_routing>
## What you write, and which existing gate reads it

| `ANALYSIS-SPEC.yaml` field you fill | What it looks like for a root-cause question | Existing gate that adjudicates it |
|---|---|---|
| `question_type: diagnostic` | declares the question as decomposition/attribution within observed data, not a causal or predictive claim (`dsx/spec.py:22-28`) | the coherence claim-ceiling check `DSX-COH-001` and the decision-language check `DSX-COH-010`, both in `dsx/checks/coherence.py`, both keyed off `question_type` |
| `results.segments` — `{name, effect, n}` rows | the per-segment effect rows the decomposition produces | the Simpson/mixture-reversal check in `dsx/checks/metrics.py`: `DSX-MET-030` (CRITICAL) when every segment opposes the aggregate sign, `DSX-MET-031` (HIGH) when a majority do |

Run `dsx gate plan` after filling the spec and `dsx check` before treating any decomposition row
as settled. The gate output is the ruling; this skill only tells you where to look.
</field_to_gate_routing>

<decomposition_body>
## The decomposition itself is not authored here

The additive-decomposition table, the mix-vs-rate split, the residual-dimension rule, and the
concentration verdict that fill `results.segments` are already specified — do not re-derive them.
Follow `skills/dsx-explore-data/SKILL.md`'s branch 5B ("diagnostic — decompose the change,
account for all of it") exactly as written; this skill points at that body rather than restating
it. Copy its `{name, effect, n}` output straight into `results.segments` and let
`DSX-MET-030`/`DSX-MET-031` adjudicate the reversal.
</decomposition_body>

<causal_guard>
## The causal guard — what keeps a diagnostic label honest

A diagnostic finding names a decomposition, not a cause. `question_type: diagnostic` is strictly
weaker than `causal` or `prescriptive` (`dsx/spec.py:22-28`), and two coherence checks hold every
claim to that ceiling: `DSX-COH-001` fires when a claim's stated type exceeds the declared
`question_type`, and `DSX-COH-010` fires when a decision rule under a `descriptive`/`diagnostic`
question uses causal language (`dsx/checks/coherence.py`). Do not write a claim or a decision
rule here that says the moved segment caused the change, or was driven by, or was because of, an
intervention — that is a causal claim and belongs under a `causal`/`prescriptive` `question_type`,
which then owes the causal guard `DSX-CAU-001` (a causal/prescriptive question declared with no
`design` block) and `DSX-CAU-010` (no identification strategy declared), both in
`dsx/checks/design.py`. If the identification strategy the data supports does not clear those
checks, the finding stays diagnostic and the wording stays attributional, not causal.
</causal_guard>

<what_this_skill_does_not_do>
This skill states no threshold of its own: no reversal magnitude that trips a Simpson finding, no
rule for which dimension the decomposition tries first, and no wording that upgrades a diagnostic
finding into a causal one. Those rulings belong to `DSX-MET-030`/`DSX-MET-031`, the
`dsx-explore-data` 5B decomposition body, and the causal guard
`DSX-CAU-001`/`DSX-CAU-010`/`DSX-COH-001`/`DSX-COH-010` respectively — run the gates and read
their output. Filling the field and citing the gate is the whole contract; restating the gate's
rule here would create a second, drifting copy of the advice the gate already owns.
</what_this_skill_does_not_do>
