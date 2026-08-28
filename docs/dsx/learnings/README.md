# DSX dated learnings — the compounding loop

A prior result that contradicts the current framing is worth more than another week
of modelling. This directory is where those results accumulate, one dated markdown
file per finding, keyed on a **fixed frontmatter schema** so the framing-time search
is a deterministic grep rather than a hopeful skim.

The loop it closes is the one the Data Science Plugin's `/ds:plan` runs: before
framing a new analysis, a session **searches the dated learnings first**. If a prior
file already answered — or contradicts — the current question, metric or domain, that
result reshapes the framing instead of being rediscovered a week later.

## These files are written and read, never gated

No `dsx` check opens this directory. There is **no existence check, no schema scan,
no gate** over these files — reading them is prompt guidance inside
`dsx-scope-analysis` (and the researcher contract), never a deterministic gate. Adding
a gate check here would add a `report.add` under `dsx/checks/*` and mint a finding
code, which this phase explicitly does not do. Consequently these files mint **no
finding code**: they are analyst artifacts like `EDA.md` and `DATA-PROFILE.yaml` —
written, read, ungated.

## The producer

The producer of future dated files is the existing **`gsd-extract-learnings`** skill,
run at phase close-out (referenced here, not owned by DSX). It already harvests
decisions, lessons, patterns and surprises from completed-phase artifacts; this
directory is simply the dated home those harvested learnings land in. DSX supplies
only the home, the fixed schema, and the seed exemplar in this directory.

## Filename convention

`YYYY-MM-DD-<slug>.md` — the date prefix means a **plain lexical sort is
chronological**, so the most recent prior result is simply the last one listed. The
`date` frontmatter value must equal the date in the filename.

## Fixed frontmatter key set (closed order)

Every dated file MUST carry these keys, in this exact order:

| key | meaning |
|---|---|
| `date` | ISO date, equal to the filename date |
| `title` | one-line human title |
| `domain` | a `dsx.domain` enum value: `experimentation` \| `machine_learning` \| `business_intelligence` \| `marketing_science` \| `research` |
| `question_type` | closed vocab: `descriptive` \| `diagnostic` \| `predictive` \| `causal` \| `prescriptive` |
| `tags` | list of short tags |
| `metrics` | list of metric names touched, so a prior metric definition is findable by metric |
| `phase` | the phase this learning came out of |
| `source_spec` | path to the driving `ANALYSIS-SPEC.yaml`, or `none` |
| `outcome` | the one-line compounding payload — what a later session should know before framing |
| `supersedes` | *(optional)* the filename of an earlier learning this one overrides |

The search step and the files agree on **this same key set**: a deterministic grep on
`domain` / `question_type` / `metrics` / `tags` only finds a file that actually carries
those keys, so a file that drifts from this schema is silently invisible to the loop.
This README is the single schema authority the search instruction cites.

## Body shape — What / So What / Now What

The body follows the Phase-13 **What / So What / Now What** shape:

- **What** — the finding, stated plainly.
- **So What** — why it changes a decision or a framing.
- **Now What** — the concrete thing a later session does about it before framing.

## Authoring note (CRLF)

This repo checks out **CRLF** on Windows. Any parser that reads this frontmatter must
tolerate `\r\n` — use `\r?\n`, never a bare `\n`, when matching line starts or ends.
