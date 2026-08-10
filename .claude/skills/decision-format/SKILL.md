---
name: decision-format
description: The required shape for every choice presented to the human in this project. Use whenever you are about to ask the human to pick between approaches, tools, libraries, schemas, chart types, or any other alternative. Also use when you are tempted to ask an open-ended question such as "how would you like to handle X?"
---

# Decision format

The human reading your output is senior in marketing and junior in engineering.
They lose more time to dense shorthand and to under-specified choices than to
anything else. This skill exists to remove both.

A choice is only useful if the reader can tell, without asking a follow-up
question, what each option actually does and what it costs them later.

## The required shape

Every decision you put in front of the human must use exactly this shape:

```
DECISION NEEDED: <one plain sentence, no acronyms>

Option A: <short name>
  In practice: <what you would actually do, concretely>
  This locks in: <the architectural consequence>
  Cost later: <what becomes harder or more expensive>
  Reversibility: cheap to undo / expensive to undo

Option B: <short name>
  In practice: <what you would actually do, concretely>
  This locks in: <the architectural consequence>
  Cost later: <what becomes harder or more expensive>
  Reversibility: cheap to undo / expensive to undo

My recommendation: <one sentence, and the reason>
If you do not answer: <the default I will proceed with>
```

## Rules

1. **Never present an option list without the "In practice" and "This locks in"
   lines filled in.** A bare list of names is not a decision, it is a quiz. If
   you cannot fill those two lines for an option, you do not understand the
   option well enough to offer it — go and find out first.

2. **Never use an acronym or abbreviation inside a decision block without
   expanding it on first use.** Write "server-side rendering (SSR)" once, then
   "SSR". Do not invent abbreviations that do not already exist in the codebase
   or in the wider industry.

3. **Always end with a default.** The "If you do not answer" line is mandatory.
   Silence must still move the work forward. Choose the default that is cheapest
   to undo, not the one you personally prefer.

4. **Maximum three options.** If the real space is larger, pick the three worth
   considering, present those, and add one line naming what you dropped and why.
   For example: "Dropped: a fourth option using a headless content management
   system — it needs a running service, and this site deploys as static files."

5. **"In practice" describes actions, not qualities.** Write "I would add a
   `chart_type` field to the frontmatter of every MDX file and validate it with
   the existing Zod schema" — not "a more structured approach".

6. **"Cost later" must be concrete and specific to this project.** Write "every
   new chart would need a matching entry in two places, so they can drift apart"
   — not "higher maintenance burden".

7. **"Reversibility" is exactly one of two values**: `cheap to undo` or
   `expensive to undo`. No middle value, no hedging. If you genuinely cannot
   tell, say `expensive to undo` — that is the safe assumption.

8. **One decision block per decision.** Do not stack three unrelated choices in
   one block. Present the one that blocks the work, take the answer, then move
   on to the next.

9. **The recommendation is mandatory and must name exactly one option.** "It
   depends" and "both have merit" are not recommendations — they hand the
   decision back with extra reading attached. State the option and the single
   reason it wins.

10. **The recommendation and the default must agree.** If you recommend Option A
    and would proceed with Option B in silence, one of the two is wrong. Fix it
    before sending, rather than making the reader notice the contradiction.

11. **If no option is safe to take by default, this is not a decision block.**
    Stop and say plainly why proceeding either way is unsafe. A block whose
    default you would not actually act on is worse than no block, because it
    reads as though silence is handled when it is not.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| "Option A: Postgres. Option B: SQLite." | Names products, not consequences | Fill in "In practice" and "This locks in" |
| "Reversibility: depends how far you get" | Not one of the two values | Pick one; when unsure, `expensive to undo` |
| "If you do not answer: I will ask again" | Silence stalls the work | Name the option you will take |
| "My recommendation: both have merit" | Hands the decision back | Name one option and one reason |
| Five options with two explained | The unexplained ones are noise | Cut to three, record what you dropped |
| "Use the ORM for the DTO layer" | Unexpanded acronyms | Expand on first use |

## When not to use this

Do not use a decision block for a choice that has an obvious conventional
default and no lasting consequence — for example, which of two equivalent
variable names to use. Make the call, state it in one line, and continue.
The decision block is for choices that change what gets built.

## Worked example

```
DECISION NEEDED: Where should the list of published articles live?

Option A: A folder of Markdown files with frontmatter
  In practice: Each article is one .mdx file under content/writing/blog/, with
    title, date and status in a frontmatter block at the top. The existing
    loader in src/lib/content.ts already reads this shape.
  This locks in: Content is versioned in git alongside the code, and the build
    fails if an article has bad frontmatter.
  Cost later: Publishing requires a git commit and a redeploy. A non-technical
    author cannot publish without touching the repository.
  Reversibility: cheap to undo

Option B: A hosted content service read at build time
  In practice: Articles live in an external service. The build calls its
    interface (API) and writes the results into the pages before deploying.
  This locks in: A network dependency in the build, and an account that must
    stay paid for the site to rebuild.
  Cost later: The build can fail for reasons that have nothing to do with the
    code, and the article history is no longer in git.
  Reversibility: expensive to undo

My recommendation: Option A, because the loader and the validation already
exist and the only author is the repository owner.
If you do not answer: I will proceed with Option A.
```
