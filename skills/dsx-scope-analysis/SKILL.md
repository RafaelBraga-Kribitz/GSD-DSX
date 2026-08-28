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

0. **Search dated learnings before framing.** Before scaffolding and before spawning
   the architect, search `docs/dsx/learnings/` for a prior analysis of the same
   question, metric or domain — framing happens *after* the search, so a prior result
   that contradicts the current framing reshapes it rather than arriving too late.
   Grep the dated files on the fixed frontmatter keys (`domain`, `question_type`,
   `metrics`, `tags`); a plain filename sort is chronological (`YYYY-MM-DD-<slug>.md`),
   so the most recent prior result is the last one listed. The schema authority for
   that key set is `docs/dsx/learnings/README.md`. Cite any prior result that
   contradicts or informs the current framing **directly in the scope reasoning**;
   when the directory yields nothing, record `searched dated learnings: none found`
   so the absence is a recorded result, not a skipped step. The producer of these
   dated files is the existing `gsd-extract-learnings` skill, run at phase close-out.
   This search uses the skill's already-granted tools and adds **no new tool grant, no
   `dsx` CLI subcommand, and no gate** — it reads the files, it never gates them:
   - Grep — match the fixed frontmatter keys across `docs/dsx/learnings/*.md`.
   - Glob — enumerate the dated files so the newest sorts last.
   - Read — open any hit whose `outcome` bears on the current question.

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

<ceremony_tier>
Before scaffolding, classify the engagement and recommend a **ceremony tier** — how
much of the GSD/DSX gate machinery this work runs under. This is advisory: the skill
classifies and PRINTS the command; the operator runs it. The scope skill never
mutates global configuration itself.

Fixed mapping (authority: `docs/gsd-tiers.md`, which lists exactly what each tier
flips):

| Engagement | Tier | What it means |
|---|---|---|
| **lookup** — throwaway, no audience | **Tier 0 exploratory** | `dsx.enforce=false`; the DS gates are off because a throwaway has no audience to mislead. |
| **ad-hoc** — a published artifact others read but do not re-run | **Tier 1 published artifact** | `dsx.enforce=true`; the DS gates are on. |
| **full pipeline** — code other people run | **Tier 2 code others run** | `dsx.enforce=true`, `mode=interactive`, full ceremony. |

For the recommended tier, emit the exact command for the operator to run:

```
pwsh scripts/gsd-tier.ps1 -Tier N     # N in {0,1,2}
```

`gsd-tier.ps1` is the thing that flips the global keys, and only when the operator
chooses to run it. Auto-apply is deferred behind an explicit operator opt-in flag;
recommending a tier is never an ungated side effect of writing a spec. Tier routing
configures ceremony, not statistics — it introduces no statistical threshold.
</ceremony_tier>

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
