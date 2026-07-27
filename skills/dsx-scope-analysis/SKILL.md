---
name: dsx-scope-analysis
description: "Turn a business question into a checkable ANALYSIS-SPEC before touching data. Use at the start of any analytical phase, or whenever a request arrives as 'can you look into X'."
argument-hint: "[question] [--phase <N>] [--type descriptive|diagnostic|predictive|causal|prescriptive]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
---

<objective>
Produce `ANALYSIS-SPEC.yaml` — the contract every later gate reads. Nothing else
in the analytical loop is checkable until this exists.
</objective>

<process>

1. **Scaffold.** `dsx init --output <phase-dir>/ANALYSIS-SPEC.yaml`

2. **Spawn `dsx-analysis-architect`** with the question and the phase context.
   It owns the hard parts: extracting the decision, classifying the question
   type honestly, and deciding whether the available data can support the answer.

3. **Fill the spec in dependency order.** Each step is only checkable once the
   previous one is fixed:
   decision → metrics → design → data → analysis → visuals → claims.

   Coherence rules the plan gate enforces:
   - Claim `type` must not exceed `question_type` strength.
   - Do not write causal verbs into `decision_rule` when the question is only
     descriptive or diagnostic.
   - Experiments require `decision.minimum_practical_effect` and `action_if_null`
     before the plan gate will pass.
   - Causal / prescriptive questions need a non-empty `assumptions` list by ship.

4. **Do the arithmetic where arithmetic applies.**
   - Experiment: `dsx power --baseline <p> --mde <d> --alpha 0.05 --power 0.8`
   - Test choice: `dsx recommend-test <outcome_type> --groups <n>`
   Record the outputs in the spec rather than a prose approximation of them.

5. **Validate.** `dsx validate --phase-dir <phase-dir> --verbose`, then
   `dsx gate plan --phase-dir <phase-dir>`. Both must exit 0.

</process>

<gates>
The three questions that most often reveal the phase is not ready:

- **Who acts on this, and what changes?** No answer means no success criterion.
- **What is the smallest effect that would change their mind?** This number sets
  the sample size. Without it, the experiment is sized by convenience.
- **What happens if the answer is "no effect"?** If nobody has thought about it,
  a null result will be reframed rather than acted on.
</gates>

<references>
@references/question-taxonomy.md
@references/causal-identification.md
</references>
