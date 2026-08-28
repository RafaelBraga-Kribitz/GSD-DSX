---
name: dsx-segment
description: "Route a multi-cut 'who differs' segmentation question to the existing multiplicity, comparisons-ledger and Simpson-reversal gates that already adjudicate it. Use for segmentation and multi-cut comparison work, not to author a new correction rule."
argument-hint: "[segment-field] [--metrics <names>]"
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
`dsx-segment` is a ROUTER, not an author. It does not define which multiplicity correction to
apply, how many comparisons are too many to examine, or what counts as a genuine Simpson reversal
across cuts — those rulings already live in shipped, deterministic `dsx` gates. This skill's only
job is to tell you which `ANALYSIS-SPEC.yaml` field to fill for a multi-cut segmentation question
and which existing gate reads it. Every number this skill would otherwise state lives in the gate
it points at, not here.
</objective>

<when_to_reach_for_this>
Reach for `dsx-segment` when the question is shaped like "how does this metric differ across
segment X, Y, Z" or "which cuts show a different effect" — a multi-comparison question over
several declared cuts. If the question instead asks specifically why a single headline number
moved, without comparing many cuts at once, use `dsx-root-cause`. If only one cut is being
compared against a single alternative, this is not yet a multiplicity question and the plain
metric and experiment skills apply directly.
</when_to_reach_for_this>

<field_to_gate_routing>
## What you write, and which existing gate reads it

| `ANALYSIS-SPEC.yaml` field you fill | What it looks like for a segmentation question | Existing gate that adjudicates it |
|---|---|---|
| `design.multiplicity.family[]` and `design.multiplicity.correction` | the full list of cuts declared confirmatory, and the `correction` field naming the method — this skill names the field, it does not choose the correction | `DSX-SPEC-043` (`dsx/spec.py:1046-1055`, the correction value must be a recognised one) and `DSX-EXP-050`/`051`/`052`/`053` (`dsx/checks/design.py:362-412`, family-vs-reported-test coverage and comparisons-looked-at auditing) |
| `results.segments` — `{name, effect, n}` rows | the per-cut effect rows the segmentation produces | the Simpson/mixture-reversal check `DSX-MET-030` (CRITICAL) / `DSX-MET-031` (HIGH) in `dsx/checks/metrics.py` |
| `results.comparisons_looked_at` | the count of cuts actually examined, including exploratory ones never promoted to the family | `DSX-EXP-051`, which fires when this count exceeds the reported/declared test coverage |

Run `dsx gate plan` after filling the spec and `dsx check` before treating any cut as settled.
The gate output is the ruling; this skill only tells you where to look.
</field_to_gate_routing>

<candidate_promotion_handshake>
## Promoting a candidate cut — reuse the existing handshake, do not invent a new one

A cut noticed while exploring is a candidate, not a confirmatory test, until it is promoted.
`ANALYSIS-SPEC.yaml` has no separate pre-declared-cuts field — promotion is a spec amendment
through `dsx-scope-analysis` that adds the intended test to `design.multiplicity.family`, the
same field `DSX-SPEC-043`/`DSX-EXP-050` already read. Follow the promotion handshake exactly as
`skills/dsx-explore-data/SKILL.md` already specifies it (its candidate-handshake step under the
segmentation branch); do not re-derive a promotion rule here. A candidate is never promoted
straight into `decision.replay` — it goes through the family first, or it stays labelled
exploratory.
</candidate_promotion_handshake>

<what_this_skill_does_not_do>
This skill states no threshold or correction method of its own: no rule for which correction to
apply, no cap on how many cuts are too many to examine, and no reversal magnitude that trips a
Simpson finding. Those rulings belong to `DSX-SPEC-043`, `DSX-EXP-050` through `DSX-EXP-053`,
`DSX-MET-030`/`DSX-MET-031`, and the `dsx-explore-data` candidate-handshake step respectively —
run the gates and read their output. Filling the field and citing the gate is the whole contract;
restating the gate's rule here would create a second, drifting copy of the advice the gate
already owns.
</what_this_skill_does_not_do>
