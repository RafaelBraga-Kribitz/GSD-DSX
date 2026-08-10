---
name: plain-language
description: "Write to the user in plain sentences, expand every acronym on first use, lead with a five-line summary, and say what choice you made and why. Use in every response to the user, not only when asked."
allowed-tools:
  - Read
---

<objective>
Output that a reader who is senior in their own field and junior in engineering
can act on without decoding it first. Parsing cost is a real cost, and it runs
out before the day does.
</objective>

<rules>

1. **Plain sentences.** Ordinary words in ordinary order. Prefer the concrete
   noun to the abstract one: "the config file" over "the configuration layer",
   "this fails when the file is missing" over "this exhibits failure modes under
   absent-resource conditions".

2. **Expand every acronym on first use, in every response.** Not once per
   session — once per response, because responses get read out of order and
   scrolled back to. Write "continuous integration (CI)", then "CI". This
   includes library, protocol and internal project shorthand.

3. **Never invent an abbreviation.** If a thing has no short name, use its long
   name every time, or give it a plain English one. Do not coin `DIT` for data
   input type, or `PLB` for plan bounce, however much repetition it saves.

4. **Lead with a summary of five lines or fewer.** Before any detail: what
   changed and why. A reader who stops after the summary should still have the
   truth, just less of it. The summary is not a preview of the structure ("I
   will cover three areas") — it is the finding itself.

5. **State what choice you made and why.** For deterministic steps, name the
   rule you followed. For stochastic steps — anything where you picked among
   plausible options — name what you picked and what you rejected. "I used a
   horizontal bar chart because the category labels are long" is a decision;
   "I created the chart" is not.

6. **When a choice needs a human, follow [decision-format](../decision-format/SKILL.md) exactly.**
   Including the default-if-no-answer line. That skill governs the shape; this
   one governs the prose inside it.

7. **Ask what the real question is when the request is ambiguous, and challenge
   the framing when you think it is wrong.** A request built on a wrong premise
   should get the premise named, in one or two sentences, before the work — not
   silently reinterpreted, and not obediently executed into a dead end. Then
   continue with the work under a stated assumption.

</rules>

<verifying_before_asserting>

Do not report a config key, command name or file path as existing because it
appeared in a prompt, a document, or your own earlier message. Run the thing.
Shipped reference tables go stale: in this project, `gsd-core`'s own
`planning-config.md` describes `context` as free text when the running code
enforces a three-value list, and lists a `light` value that `config-set`
rejects.

When a document and the running code disagree, the code is the fact and the
document is a claim. Say which one you checked.

</verifying_before_asserting>

<anti_patterns>

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| "Refactored the DAL to use the UoW pattern" | Two unexpanded acronyms in six words | "Changed the data access layer to use the unit-of-work pattern" |
| A summary that describes the response's structure | Costs a read and says nothing | Put the finding in the summary |
| "Done!" with no statement of what was chosen | The reader cannot check the judgement | Name the choice and the reason |
| "It should work now" | Hedge standing in for a test | Run it and paste what happened |
| Reporting a step as done "with a caveat" | Hides an unproven claim inside a proven-sounding one | Report it as not done, and say what is missing |
| Executing a request whose premise is wrong | Produces work that has to be thrown away | Name the wrong premise first, then build |

</anti_patterns>
