---
name: dsx-narrate
description: "Turn a verified analysis into a decision-ready narrative without overstating it. Use after the statistical review passes, for executive summaries, readouts and reports."
argument-hint: "[--audience executive|product|technical] [--format md|docx|pptx]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
  - Skill
---

<objective>
The version the decision-maker reads, in which every sentence still survives the
audit.
</objective>

<precondition>
Run only after `dsx gate verify` passes and `STATS-REVIEW.md` exists. Narrating
an unverified result is how a leaked feature becomes a strategy.
</precondition>

<structure>
Lead with the decision, not the method. Analysts write chronologically;
decision-makers read for the answer first.

1. **The answer** — one sentence, with the number and its interval.
2. **What it means** — the action the pre-declared rule implies.
3. **How confident, and why** — the design in plain language, and its limits.
4. **What would change it** — the specific evidence that would flip the verdict.
5. **Method** — last, for the reader who wants it.
</structure>

<discipline>
- Match the verb to the design. A claim typed `association` gets associational
  verbs, however much better the causal phrasing reads.
- Never a percentage without its base. "Up 40%" from 5 to 7 is a different story
  from 500 to 700, and readers assume the larger one.
- State uncertainty as a range, not as a hedge. "Between 1 and 4 points" is
  actionable; "roughly 2.4%, though there's uncertainty" is neither.
- Name the population. Readers default to "everyone".
- Put limitations up front. Stated early they read as competence; discovered late
  they read as concealment.
- Round to what the interval supports. Four significant figures on a wide
  interval projects precision the estimate does not have.

Verify the final wording: `dsx check claims --phase-dir <phase-dir>`. The causal
language guard reads what you actually wrote, not what you meant.
</discipline>

<delegation>
Spawn `dsx-data-storyteller` for the draft. For a Word or PowerPoint deliverable,
compose with the `docx` / `pptx` skills after the wording passes the claims check.
</delegation>
