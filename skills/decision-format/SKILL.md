---
name: decision-format
description: "Present every choice that needs a human answer in a fixed, plain-language block that states what each option means in practice, what it locks in, what it costs later, and what happens if nobody answers. Use whenever you are about to ask the user to pick between options."
allowed-tools:
  - Read
---

<objective>
A person who is senior in their own field and junior in engineering can pick the
right option without asking a follow-up question, and silence still moves the
work forward.
</objective>

<when_to_use>

Use this format whenever you would otherwise ask the user to choose: an
architecture fork, a library choice, a schema decision, a naming convention, a
scope cut, a tool selection. It applies to interactive menu widgets and to plain
text lists equally.

Do **not** use it for questions with a single correct answer that you can verify
yourself. Verify it and proceed. A decision block is for genuine forks where the
user's preference, not the codebase, decides the outcome.

</when_to_use>

<format>

Reproduce this shape exactly. Every line is required.

```
DECISION NEEDED: <one plain sentence, no acronyms>

Option A: <short name>
  In practice: <what you would actually do, concretely>
  This locks in: <the architectural consequence>
  Cost later: <what becomes harder or more expensive>
  Reversibility: cheap to undo / expensive to undo

Option B: <same four lines>

My recommendation: <one sentence, and the reason>
If you do not answer: <the default I will proceed with>
```

</format>

<rules>

1. **Never present an option list without the "In practice" and "This locks in"
   lines filled in.** An option named but not explained is not an option, it is a
   vocabulary quiz. "In practice" describes the concrete work you would do, in
   the imperative: which files you would create, which command would run, what
   the user would type. "This locks in" names the consequence that outlives the
   decision.

2. **Never use an acronym in a decision block without expanding it.** Write
   "continuous integration (CI)" on first use, then "CI". This applies to
   library names, protocol names and internal project shorthand. Do not invent
   new abbreviations anywhere in the block.

3. **Always end with a default, so that silence still moves the work forward.**
   The "If you do not answer" line names one specific option and commits to it.
   It is never "I will wait" or "I will ask again". If no option is safe to take
   by default, the correct move is not a decision block — it is to stop and say
   plainly why proceeding is unsafe.

4. **Maximum three options.** If there are more, pick the three worth
   considering and add one line naming what you dropped and why:
   `Dropped: <option> — <one-clause reason>`. Three is a ceiling, not a target;
   two well-drawn options beat three padded ones.

5. **Reversibility is one of the two literal phrases** — `cheap to undo` or
   `expensive to undo`. It is not a paragraph. If a choice is cheap to undo, say
   so plainly, because that is usually the argument for deciding fast and moving
   on.

6. **The recommendation is mandatory and must name one option.** "It depends" is
   not a recommendation. State the option and the single reason it wins. If the
   recommendation and the default differ, that is a contradiction — fix one of
   them.

7. **One decision per block.** If two choices are genuinely independent, write
   two blocks. If the second only matters given a particular answer to the
   first, do not ask it yet.

</rules>

<worked_example>

```
DECISION NEEDED: Where should the plain-language writing rules live so that
every agent in this project reads them?

Option A: A project instruction file at the repository root
  In practice: I create AGENTS.md at the repository root holding the rules as
    prose. Every agent reads it during its mandatory initial read.
  This locks in: One shared file that all agents see, versioned in git with the
    project.
  Cost later: The rules apply to every agent equally; you cannot give the
    planner different instructions from the executor without adding a second
    mechanism.
  Reversibility: cheap to undo

Option B: A skill wired to named agents through the agent_skills config key
  In practice: I write the rules as a skill under skills/, then point
    agent_skills.gsd-planner, agent_skills.gsd-executor and
    agent_skills.gsd-verifier at it.
  This locks in: Per-agent targeting, so different agents can get different
    rules later.
  Cost later: Each new agent type must be added to the config by hand, and an
    agent nobody wired up silently gets nothing.
  Reversibility: cheap to undo

My recommendation: Option A, because the rules are about how you want to be
written to, and that does not vary by agent.

If you do not answer: I will proceed with Option A.
```

</worked_example>

<anti_patterns>

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| "Option A: Postgres. Option B: SQLite." | Names a product, not a consequence | Fill in "In practice" and "This locks in" |
| "Reversibility: depends on how far you get" | Not one of the two phrases | Pick `cheap to undo` or `expensive to undo` |
| "If you do not answer: I will ask again" | Silence stalls the work | Name the option you will take |
| "My recommendation: both have merit" | Pushes the decision back | Name one option and one reason |
| Five options with two explained | The unexplained ones are noise | Cut to three, record what you dropped |
| "Use the ORM for the DTO layer" | Unexpanded acronyms | "object-relational mapper (ORM)" on first use |

</anti_patterns>
