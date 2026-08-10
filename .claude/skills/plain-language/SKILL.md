---
name: plain-language
description: How to write to the human in this project. Load at the start of any task and follow it for every response, not only for decisions. Covers plain sentences, acronym expansion, the five-line summary that must come before detail, and the requirement to state what choice you made and why.
---

# Plain language

The human reading your output is senior in marketing and junior in engineering.
Dense shorthand costs them real effort, and they run out of that effort before
they run out of time. Everything below exists to remove that cost.

## Writing

- **Write in plain sentences.** Not fragments, not bullet-only telegraphese, not
  tables where a sentence would do.
- **Expand every acronym on first use in each response.** Write "server-side
  rendering (SSR)" the first time, then "SSR" for the rest of that response. The
  next response starts the count again — do not assume the reader remembers.
- **Do not invent abbreviations.** If a short form does not already exist in this
  codebase or in the wider industry, spell the thing out every time.

## Structure

- **Before any detail, summarise what changed and why in five lines or fewer.**
  This goes at the top of the response. Five lines is a hard ceiling, not a
  target — fewer is better.
- Detail, evidence and command output come after the summary, never before it.

## Choices

- **When a choice is needed, follow `skills/decision-format/SKILL.md` exactly**,
  including the "If you do not answer" default line. Do not improvise a shorter
  form of that block.
- **State what choice you made and why — for both deterministic and stochastic
  steps.** A deterministic step is one where the same input always produces the
  same output, such as running a linter or reading a configuration file. A
  stochastic step is one where the output can vary between runs, such as asking
  a language model to draft text or picking among several plausible
  implementations. Both kinds of step involve choices. Name them.

## Pushing back

- **Ask what the real question is when the request is ambiguous.** Do not guess
  at intent and then build the wrong thing carefully.
- **Challenge the framing when you think it is wrong.** If the request assumes
  something that is not true of this codebase, say so plainly in a sentence or
  two, then either proceed under a stated assumption or ask. Do not stay silent
  to be agreeable.

## Honesty

- Report outcomes as they are. If a check failed, say so and paste the output.
  If a step was skipped, say it was skipped and why.
- Do not report something as done with a caveat attached. Either it is done and
  proven, or it is not done. Say which.
