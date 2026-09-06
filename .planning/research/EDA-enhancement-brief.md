This project already has an EDA protocol. It is not a future roadmap item.

It lives in `skills/dsx-explore-data/SKILL.md`. The skill’s core rule is: **EDA is a protocol, not a browse** — same sequence every time, written as a re-runnable script, not scattered notebook cells.

The six steps, in order:

1. **Shape and identity** — row/column counts, grain, duplicate rate, why duplicates exist
2. **Completeness** — null rates and whether missingness is random or structured
3. **Time** — min/max, gaps, daily volume, timezone of every date column
4. **Distributions** — five-number summaries, zeros/negatives, sentinels, categorical cardinality
5. **Relationships** — only after 1–4; for predictive work, split first and compute feature-vs-target stats on training rows only
6. **Segments** — recompute the headline in the important splits (Simpson’s paradox)

The written output is `EDA.md` plus a hermetic `DATA-PROFILE.yaml` from `dsx profile`. Only the profile is gated: execute/verify compare `data[].assertions` in `ANALYSIS-SPEC.yaml` against that artifact (`DSX-DQ-*`). Gates do not open the warehouse, and they do not check `EDA.md`.

What stays agent judgement (documented in `references/data-quality-assertions.md`): whether structured missingness invalidates the design, and whether a gap is an outage vs a schema change.

Nothing in `.planning/` currently proposes a second EDA protocol. The planned/shipped machine-checkable slice is already the profile + assertion path (REQ-P1-01 / REQ-P1-02, done in v1.1.0).

The protocol is already a strong, reusable **data-trust recipe** for one table. It is not yet versatile across the question types this project actually ships, and it is not deep enough to drive most analytical insights. Steps 1–4 catch dirt that would silently ruin a result. Steps 5–6 are too thin to change a diagnostic, causal, or experimental conclusion. The gated path (`dsx profile`) implements even less than the skill writes. Nothing on the current roadmap deepens this into a full exploratory analysis loop.

## What it already does well

Treat it as a **data-trust protocol**, not as Tukey-style exploratory data analysis (EDA). On that narrower job it is unusually good, especially for an agent:

- **Fixed order beats browsing.** The interesting finding is often in the boring step. That is the right core principle for language-model agents, who otherwise wander, plot randomly, and then overfit a story to whatever they saw last.
- **Script, not a notebook session.** Re-runnable on refresh is the operational requirement this project actually has.
- **Several steps produce real findings, not summaries.** “Why do duplicates exist before you drop them,” “is nullness structured,” “confirm the timezone,” “sentinels masquerade as data,” and “a drifting base rate is a modelling constraint” are insight-shaped, not dashboard-shaped.
- **Split-first for predictive work** (in the repo copy of the skill) is the one leakage rule EDA usually forgets. The user-level copy of the same skill is weaker here: it still cross-tabulates nulls against the target on the full frame.
- **Output is wired into the contract.** Profile plus assertions is how this project makes later gates honest. That part is reusable.

So: as a **repeatable “can I trust this extract?” checklist**, it is already in the top tier of what this codebase does.

## Where it stops being EDA

Classic EDA is supposed to **change the next analysis**: re-express a skewed measure, see a residual pattern, generate a competing hypothesis, discover that the grain is wrong for the decision. This protocol mostly **invalidates assumptions about the table**. That is necessary. It is not sufficient.

The drop-off is visible in the writing itself. Steps 1–4 name concrete numbers (duplicate rate, null pattern by time, daily volume, five-number summary, cardinality, tail share). Steps 5–6 name vague verbs: “correlations,” “the headline number,” “the two or three most important splits.” An agent can finish 1–4 as a script. It cannot finish 5–6 without inventing a method, and different agents will invent different ones.

Three structural limits follow.

**1. It is one recipe for one flat extract.**  
The argument hint is `[dataset] [--target] [--time]`. That matches marketing event tables. It does not branch for:

- experiments (assignment logs, sample-ratio mismatch precursors, weekly cycle, novelty window)
- causal work (overlap / positivity, treatment over time, covariate balance)
- diagnostic work (volume vs rate vs mix decomposition)
- multi-table warehouse reality (join fan-out, grain after a join) — that lives in `dsx-define-metrics`, not here
- panel / user-day grain vs user grain
- nested events, text, or JSON

This project’s own mix is roughly 60% online experiments. The explore skill does not know that.

**2. It does not speak the rest of DSX.**  
The analysis architect is told to write the spec **before any data is touched**. Explore is the sanctioned exception, but the loop is not closed:

- `EDA.md` is mentioned once and never read by a gate, agent, or later skill.
- Completeness talk never names missing completely at random / missing at random / missing not at random, even though `validity_frame.missingness` now requires a mechanism.
- “Headline number” is undefined here; the metric contract lives in a different skill.
- Segments in step 6 are not the same object as `results.segments` (which drives the Simpson check) or the pre-declared cuts the architect is supposed to lock before seeing results.

So the protocol is reusable as **instructions to an agent**, not as a **portable artifact**. Two runs will not produce comparable `EDA.md` files, and nothing downstream is forced to consume them.

**3. The machine only enforces the shallow slice.**  
`dsx profile` currently writes: row count, per-column null rate / unique count / type, primary-key uniqueness, min/max date, max gap, sentinels found. It does **not** compute daily volume, structured-missingness tables, five-number summaries, skew, zeros/negatives, categorical tails, correlations, base-rate drift, or segment recomputes.

The skill says “run the protocol.” The gate says “did you write a profile and some assertions.” An agent can skip every insight-producing step, run `dsx profile`, and still look compliant. The references file already admits the interesting judgements (structured missingness vs schema change; gap vs outage) stay stochastic **after** the numbers exist — but those numbers are not even in the profile.

Phase 11.3 plans missingness-method vocabulary and optional profile-rate reconciliation. That tightens data-quality honesty. It does not deepen exploration.

## Is it deep enough to drive insights?

**Sometimes, and only of one kind:** “the data is not the data you thought.”

Those findings are high leverage in this project (wrong grain, silent schema change, double-load, sentinel `-1`, base-rate shift). They can and should change the spec.

They will not usually answer *why the metric moved*, *who the effect is for*, or *whether the planned design is even identified*. For that you need question-shaped next questions, for example:


| If the question is… | Step 5–6 should force…                                                                                      |
| ------------------- | ----------------------------------------------------------------------------------------------------------- |
| Descriptive         | Mix vs level, period boundaries, denominator drift                                                          |
| Diagnostic          | Full decomposition of the change (volume, rate, mix, price)                                                 |
| Experiment          | Observed vs expected weekly cycle, assignment integrity, novelty decay                                      |
| Causal              | Common support, treatment variation over time, who is never treated                                         |
| Predictive          | Split first, then leakage, drift, calibration of the base rate — not Pearson correlations on the full frame |


Pearson correlations as the default “relationship” tool are the weakest line in the protocol: they miss thresholds and lags, they leak if computed on the full frame, and they invite a modelling story before the grain is even trusted.

There is also no **stopping rule**. A 3% duplicate rate, a category that vanished in March, or a reversing segment is supposed to be “the finding” — but the skill never says “stop, amend the spec, do not proceed to modelling.” Without that, agents will note the dirt and keep going.

## Verdict


| Job                                                           | Already good enough?                                                |
| ------------------------------------------------------------- | ------------------------------------------------------------------- |
| Reusable data-trust checklist for one CSV                     | Yes                                                                 |
| Versatile across DSX question types and warehouse joins       | No                                                                  |
| Deep enough to drive analytical insight, not just cleanliness | No — strong at invalidating the table, thin at shaping the analysis |
| Planned to become that                                        | No. Upcoming work hardens missingness declarations, not exploration |


Keep steps 1–4 as the trust protocol; they are already the right reusable core. If you want this skill to drive insight, the gap is not “more profiling fields.” It is: a structured `EDA.md` (or spec patch) that later steps must read; question-type branches after step 4; and an explicit stop-and-re-scope rule when the table contradicts the planned grain, missingness, or segments.

I am in Ask mode, so this is evaluation only. If you want, the next useful decision is whether to deepen explore as a skill, or to keep it as trust-and-profile and put question-shaped exploration somewhere else (architect after a measured extract, or a new diagnostic skill).

Funnel correlation is worth an **optional** step after the table is trusted, not a new gate and not a v2.0.0 phase. The other high-value additions are mostly protocol text: stop-and-re-scope, question-type branches, and a structured `EDA.md`. Leave Phases 11–12 alone; plant seeds now; deepen the skill with a GSD Core quick task after 11.1.1.

## Funnel correlation: use it, do not promote it

```markdown
C:\Users\Benutzer1\Dev\funnel_correlation_py - is a python package that allows you to analyze the correlation between two datasets.
```

`funnel_correlation_py` is a Python port of Business Science’s **correlation funnel**: quantile-bin numbers, one-hot encode categories, then Pearson r of each binary column against a target, plotted as a tornado. That is a faster, more readable version of this skill’s weak Step 5 (“correlations”). For marketing tables with a yes/no outcome, it is one of the few routines that actually **surfaces hypotheses**.

It is beneficial only with hard limits:

- **Optional, never default.** Needs a target that is already binary, or that you are willing to binarize. No target → skip. Datetime columns → drop or recode first (the library rejects them). Missing values → it **refuses to run**, which is correct: completeness (Step 2) must happen first. Do not impute just to draw the funnel.
- **After Steps 1–4, never instead of them.** Ranking `age__18_35` against conversion does not tell you the grain is wrong, that March was a schema change, or that the timezone is off.
- **Training rows only** on predictive work. Quantile cuts fitted on the full frame leak. Same split-first rule already in the repo skill.
- **Exploratory, not evidence.** Using the tornado to pick which segments later appear as confirmatory results is the garden of forking paths. Record it in `EDA.md`, increment `comparisons_looked_at`, do not promote a bin into `decision.replay`.
- **Association, not cause.** Pearson on 0/1 columns is a phi coefficient. Fine for ranking. Illegal as a causal claim. Rare positives attenuate it; the library already warns below 5%.
- **Not a conversion funnel.** This is not step-drop-off (visit → signup → pay). If you have an event order, that is a **different** optional routine.

Do **not** vendor this package into `dsx/`. Brief decision D-01 keeps the gate path stdlib-only. Decision D-02 says gates adjudicate declarations; they do not compute statistics. Pearson r on binarized columns is computation. The agent may import pandas in **its** environment and write numbers into `EDA.md`. The gate still only reads the spec and `DATA-PROFILE.yaml`.

## Other routines, ranked

**Put in the skill now (no new Python in** `dsx/`**):**

1. **Stop-and-re-scope.** Duplicate grain, structured missingness, vanishing category, reversing segment → amend the spec, do not continue to modelling.
2. **Question-type branches after Step 4.** Descriptive: mix vs level vs denominator drift. Diagnostic: volume / rate / mix decomposition of the change. Experiment: weekly cycle, assignment integrity, novelty window. Causal: who is never treated, treatment over time. Predictive: split first, then drift and leakage, not a full-frame correlation matrix.
3. **Structured** `EDA.md` **headings** so two runs are comparable, even if no gate reads the file yet.
4. **Map completeness onto the missingness vocabulary** the spec already requires (missing completely at random / missing at random / missing not at random / not assessed). Do not invent a new one.
5. **Join grain after every join** (already in the executor fragment; the explore skill should say it too).
6. **Optional correlation funnel** as specified above, when a binary (or binarizable) target exists.

**Optional later, still agent-side, still not gates:**

1. **Conversion funnel** (true step drop-off) when an ordered event list exists — complementary to correlation funnel, not a substitute.
2. **Population stability** (train vs later period) for predictive refresh.
3. **Overlap / common support** for causal designs.

**Do not add in this pass:**

- Growing `dsx profile` to compute five-number summaries, daily volume, or correlations (that is a later milestone; it changes fixtures Phase 12 will measure).
- New finding codes such as `DSX-EDA-*` before Phase 12.
- Plotly tornado charts as sealed deliverable figures (that pulls in viz gates for an exploratory plot).
- Mutual information / sklearn as a second ranker. One optional ranker is enough.
- Making the correlation funnel mandatory.



## How this should enter GSD Core

You are mid-milestone: Phase **11.1.1** is next, then 11, 11.2, 11.3, then **Phase 12 (calibration)**, which must stay last because it measures catch rate of **gates**. Exploratory-data-analysis (EDA) skill text is not a gate. Inserting an 11.4 would delay calibration and mix two different jobs.

```
DECISION NEEDED: How should the EDA deepening enter the existing GSD Core plan?

Option A: Leave v2.0.0 phases untouched
  In practice: Plant seeds now. After 11.1.1 (not during it), run a GSD Core
    quick task that edits the explore skill, an EDA.md template, and the
    executor note. After Phase 12, start a new milestone only if we later
    want gates to read EDA.md or grow DATA-PROFILE.yaml.
  This locks in: v2.0.0 still measures declaration gates. Agents get a
    deeper protocol without new finding codes or pandas on the gate path.
  Cost later: EDA.md remains ungated until a later milestone, so an agent
    can still skip Steps 5–6 and only run dsx profile.
  Reversibility: cheap to undo

Option B: Insert a decimal phase before Phase 12 (for example 11.4)
  In practice: /gsd-phase --insert after 11.3, then discuss/plan/execute
    EDA as if it were validity-frame work.
  This locks in: Phase 12’s catch-rate corpus must cover whatever you
    gated. Skill-only text would be a phase with almost nothing for
    calibration to measure.
  Cost later: Another insertion in an already-patched 11.x chain; D-01/D-02
    fights if anyone “helps” by computing correlations in dsx/.
  Reversibility: expensive to undo

Option C: Backlog only (999.x) and do nothing to the skill until a later milestone
  In practice: /gsd-capture --backlog, keep running 11.1.1 → 12 as today.
  This locks in: The protocol stays as a data-trust checklist until v2.1.
  Cost later: Agents keep producing ungated, incomparable EDA.md files
    (or none) through the rest of v2.0.0.
  Reversibility: cheap to undo

My recommendation: Option A, because the valuable part is agent protocol,
not a new gate, and Phase 12 must not be asked to measure skill prose.
If you do not answer: proceed with Option A.
```

Dropped: putting `funnel_correlation_py` inside `dsx/` or adding pandas to the gate path — brief D-01 forbids it.

---



## Full recipe (paste in Agent mode)

Use this after 11.1.1 is no longer the active execution, or in a **second chat** so it cannot steal that phase. Seeds (step 1) are safe to run immediately.

```text
You are operating in the gsd-dsx repo. Follow GSD Core commands end-to-end;
do not improvise around their workflows. Do not edit ROADMAP integer phases
11, 11.1, 11.1.1, 11.2, 11.3, or 12. Do not add finding codes. Do not import
pandas/numpy/plotly into dsx/. Do not vendor C:\Users\Benutzer1\Dev\funnel_correlation_py
into this package.

LOCKED DECISIONS
- D-01: gate path stays stdlib-only.
- D-02: gates adjudicate declarations; they do not compute statistics.
- EDA deepening in this pass is agent protocol, not a gate family.
- Correlation funnel is OPTIONAL, after protocol steps 1–4, only when a
  binary or binarizable target exists. Training rows only on predictive
  work. Labelled exploratory; increment comparisons_looked_at. Never a
  causal claim. Never a sealed deliverable figure.
- Distinguish correlation funnel (binarize → Pearson → tornado) from a
  conversion funnel (ordered step drop-off). Conversion funnel is a
  separate optional routine when an event order exists.
- Missing values: do not impute solely to run the funnel; completeness
  must already have decided what nulls mean.
- Stop-and-re-scope when grain, structured missingness, a vanished
  category, or a reversing segment contradicts the spec.
- After step 4, branch by question_type:
  descriptive → mix vs level vs denominator drift
  diagnostic → volume / rate / mix decomposition
  experiment → weekly cycle, assignment integrity, novelty window
  causal → who is never treated, treatment over time
  predictive → split first, then drift/leakage (not full-frame Pearson)
- Map completeness onto existing validity_frame.missingness vocabulary
  (MCAR / MAR / MNAR / not_assessed). Do not invent a parallel vocabulary.
- Structured EDA.md with fixed headings. Still ungated.
- Source of truth: skills/dsx-explore-data/SKILL.md in this repo. If you
  touch the skill, keep the user-level copy
  C:\Users\Benutzer1\.claude\skills\dsx-explore-data\SKILL.md in sync,
  including the split-first paragraph the user copy currently lacks.

OPERATIONAL SEQUENCE (run in this order)

1) Plant seeds NOW (does not change current_phase; safe during 11.1.1):

/gsd-capture --seed Deepen dsx-explore-data into a reusable EDA protocol: structured EDA.md, stop-and-rescope, question-type branches after trust steps, optional correlation-funnel and conversion-funnel routines; keep computation off the gate path (D-01/D-02). Trigger: when v2.0.0 Phase 12 has shipped, or when starting a milestone about agent workflow, data-trust, or exploration.

Then enrich the seed so trigger_when is not left as "when relevant":
- trigger_when: v2.0.0 Phase 12 complete, OR a new milestone whose scope includes exploration / agent skills / DATA-PROFILE
- why: skill is a data-trust checklist; steps 5–6 do not drive insight; funnel_correlation_py is a good optional ranker for binary targets but must not become a gate
- scope: skills/dsx-explore-data, templates/EDA.md, capabilities/dsx/fragments/executor.md; NOT dsx/checks, NOT new DSX-* codes in v2.0.0
- breadcrumbs: skills/dsx-explore-data/SKILL.md; references/data-quality-assertions.md; brief.md D-01 D-02; C:\Users\Benutzer1\Dev\funnel_correlation_py (reference implementation only)

Optional second seed (gated profile growth — do not implement in the quick task):
/gsd-capture --seed Grow DATA-PROFILE / dsx profile so daily volume, structured missingness, and distribution summaries are hermetic artifacts gates can read. Entry condition (D-13): Phase 12 catch-rate published AND real phases produce EDA.md that gates ignore. Do not do this before Phase 12.

2) Do NOT run /gsd-phase --insert. Do NOT /gsd-new-milestone yet. Do NOT
   /gsd-review-backlog to promote this into v2.0.0.

3) After 11.1.1 is idle (SUMMARY complete, or explicitly paused), run a
   quick task — this updates .planning/quick/ and STATE.md quick table,
   not ROADMAP.md:

/gsd-quick --full Deepen the dsx-explore-data protocol without touching gates or DATA-PROFILE. Edit skills/dsx-explore-data/SKILL.md: keep steps 1–4 as the trust core; add stop-and-rescope; add question-type branches after step 4; specify a structured EDA.md outline; add optional correlation-funnel routine (reference C:\Users\Benutzer1\Dev\funnel_correlation_py: binarize → correlate → plot; agent may import that package if present, otherwise skip with a recorded reason; training rows only; exploratory label; no causal verbs; no sealed figures; skip when no target / datetime-only / unresolved missingness). Add optional conversion-funnel routine when an ordered event list exists. Add templates/EDA.md. Point capabilities/dsx/fragments/executor.md at the new EDA.md contract. Sync ~/.claude/skills/dsx-explore-data/SKILL.md. No new finding codes, no dsx/ imports of pandas, no profiler changes, no fixture changes, no version bump required unless a skill/fragment change already demands the existing catalogue/docs habit.

During quick --discuss, lock these if asked:
- Funnel is optional skip-with-reason, not required.
- Agent-side pandas is allowed; dsx/ stays stdlib.
- EDA.md is not a ship-gate artifact in this pass.
- Do not seal exploratory plots.

4) Execute the quick task the way GSD Core tells you
   (/gsd-execute-phase is for ROADMAP phases; quick has its own execute
   path inside /gsd-quick). Do not start /gsd-plan-phase 11.1.1 or 12
   from this chat.

5) After v2.0.0 Phase 12 ships, if we want gates to notice EDA:

/gsd-new-milestone v2.1 Exploratory protocol and profile depth

That milestone is the only place to consider: extra DATA-PROFILE fields,
optional dsx CLI that wraps correlation funnel *outside* the gate path,
or a non-blocking check that EDA.md exists when data[] is present.
Revisit D-01/D-02 before any of those become blocking codes.

SUCCESS CRITERIA FOR THE QUICK TASK
- skills/dsx-explore-data/SKILL.md states the six trust steps, stop rule,
  question-type branches, structured EDA.md, optional correlation funnel,
  optional conversion funnel.
- templates/EDA.md exists with those headings.
- dsx/checks/ and dsx/profiler.py are unchanged.
- ROADMAP.md phase list 11–12 is unchanged.
- python -m unittest still green (no fixture drift).
```

**How to operationalize in practice**


| When                      | Command                                                    | What it changes                                              |
| ------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------ |
| Today, even during 11.1.1 | `/gsd-capture --seed …`                                    | `.planning/seeds/` only                                      |
| After 11.1.1 is idle      | `/gsd-quick --full …`                                      | skill, template, executor note; not the roadmap              |
| After Phase 12            | `/gsd-new-milestone` only if you want gated profile/EDA.md | new milestone, then `/gsd-discuss-phase` / `/gsd-plan-phase` |


Switch to Agent mode to run step 1 now. Keep this chat’s locked decisions in the paste; a fresh agent will otherwise try to put Pearson on the gate path or insert 11.4.