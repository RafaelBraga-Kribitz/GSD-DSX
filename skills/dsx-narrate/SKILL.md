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
  from 500 to 700, and readers assume the larger one. Set `base_n` or
  `from_value`/`to_value` on the claim when the text uses a relative %.
- State uncertainty as a range, not as a hedge. "Between 1 and 4 points" is
  actionable; "roughly 2.4%, though there's uncertainty" is neither.
- Name the population. Readers default to "everyone".
- Put limitations up front. Required non-empty at verify/ship for causal,
  prescriptive and predictive questions (`DSX-CLM-080`).
- For a prescriptive readout, name the `revisit_when` trigger (metric +
  threshold + time anchor) that would retire the recommendation — a gate-read
  field (`DSX-COH-040`), not an unenforced scaffold note.
- Round to what the interval supports. Four significant figures on a wide
  interval projects precision the estimate does not have.
- Write `narrative.path` (e.g. `NARRATIVE.md`) and embed every `claims[].text`
  verbatim. Forbidden wording (`data proves`, `with high confidence`, …) is
  `DSX-NAR-030`.

Verify the final wording:

```bash
dsx check claims narrative --phase-dir <phase-dir> --verbose
```

Cite NAR/CLM findings unmodified. Do not rephrase a CRITICAL into a soft note.
</discipline>

<references>
@references/narrative-discipline.md
</references>

<delegation>
Spawn `dsx-data-storyteller` for the draft. For a Word or PowerPoint deliverable,
compose with the `docx` / `pptx` skills after the wording passes the claims check.
</delegation>
