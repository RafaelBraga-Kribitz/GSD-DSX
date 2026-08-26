# Analytic Surface Research: comparison against Claude Code data-science packs

**Project:** gsd-dsx — queued milestone v2.1 Analytic Surface
**Domain:** Operator surface (skills, playbooks, compounding, conversational start) around
an existing declaration-adjudicating gate
**Researched:** 2026-08-26
**Confidence:** HIGH for architecture of this repo (read from source); MEDIUM for
comparison repos (READMEs, GitHub trees, and skill/playbook text fetched on the
research date — not a local clone, not a code review of their Python)

This file answers a load-bearing question that later discuss must not re-litigate
from marketing copy: **what did each comparison pack actually ship, and what of
that is a DSX skill, a DSX gate, or an anti-feature?** A README claim in a
comparison repo is not a D-05 source. It cannot justify a finding code and it
cannot excuse skipping one.

Binding constraints this research does not reopen: D-01 (stdlib-only gate path),
D-02 (gates adjudicate declarations), D-03 (extend DSX in place), D-05 (citation
plus published reference value per new check), D-12/D-12a (paradigm symmetry),
D-13 (deferred work carries an entry condition). Brief §3 ranks risk reduction
first and portfolio value last — v2.1 exists to close operator-surface gaps
*after* v2.0.0 ships, not instead of it.

---

## 1. What was actually read

Fetched 2026-08-26. Star counts are a snapshot from that fetch, not a quality
ranking.

| Repo | What was read | Snapshot stars |
|---|---|---|
| [eduardocornelsen/unified-ai-data-framework](https://github.com/eduardocornelsen/unified-ai-data-framework) | `README.md` (raw, main); GitHub tree; `playbooks/09_EXPERIMENTATION.md` (CUPED section); `skills/03-data-analysis-investigation/` listing | 1 |
| [eduardocornelsen/data-skills](https://github.com/eduardocornelsen/data-skills) | `README.md` (the playbook-only predecessor the unified hub merged) | — |
| [DAAF-Contribution-Community/daaf](https://github.com/DAAF-Contribution-Community/daaf) | `README.md`; `user_reference/02_understanding_daaf.md`; `agent_reference/PLAN_TEMPLATE.md`; `agent_reference/WORKFLOW_PHASE2_PLANNING.md`; `.claude/skills/daaf-orchestrator/SKILL.md`; GitHub tree | 230 |
| [TerryFYL/claude-statistical-analysis-skill](https://github.com/TerryFYL/claude-statistical-analysis-skill) | `README.md`; `SKILL.md` (v4 "diagnose before analyze"); GitHub tree | 14 |
| [liangdabiao/claude-data-analysis](https://github.com/liangdabiao/claude-data-analysis) | `README.md` (raw, main) | 439 |
| [liangdabiao/claude-data-analysis-ultra](https://github.com/liangdabiao/claude-data-analysis-ultra) | `README.md` (same Week-1.1 text as the non-ultra repo) | 3 |
| [andikarachman/data-science-plugin](https://github.com/andikarachman/data-science-plugin) | `README.md` (raw, **master** — `main` 404s); GitHub trees for `skills/`, `agents/`, `commands/` | 14 |
| Secondary | [AI Builder Club skills guide](https://www.aibuilderclub.com/blog/claude-code-for-data-scientists-skills-guide) (What / So What / Now What reporting); [mcpmarket scientific-data-science blurb](https://mcpmarket.com/tools/skills/scientific-data-science) (not treated as a source) | — |

**This repo, verified against source rather than against earlier planning prose:**
[`README.md`](../../README.md), [`brief.md`](../../brief.md),
[`dsx/spec.py`](../../dsx/spec.py) (`VARIANCE_ADJUSTMENTS`),
[`references/test-selection.md`](../../references/test-selection.md),
[`references/leakage-taxonomy.md`](../../references/leakage-taxonomy.md),
[`references/experiment-pitfalls.md`](../../references/experiment-pitfalls.md),
[`skills/dsx-explore-data/SKILL.md`](../../skills/dsx-explore-data/SKILL.md),
[`skills/dsx-design-experiment/SKILL.md`](../../skills/dsx-design-experiment/SKILL.md),
[`capabilities/dsx/capability.json`](../../capabilities/dsx/capability.json)
(`"hooks": []`).

---

## 2. What this project already is (the fact, from code)

Agents fill `ANALYSIS-SPEC.yaml`. Python gates block when the spec and artifacts
do not hold. Gates never read a warehouse and never compute test statistics.
v1.5.0 already covers power, sample-ratio mismatch, multiplicity (including
Benjamini–Hochberg / false-discovery-rate aliases), peeking, leakage as code
(`DSX-ML-*`, `DSX-CODE-*`), chart seals, narrative wording, and decision replay.
v2.0.0 (Phases 6–12) adds the layer underneath: estimand, units, interference,
triggering, paradigm symmetry.

`VARIANCE_ADJUSTMENTS` in `dsx/spec.py` on the research date is
`{cluster_robust, delta_method, bootstrap_cluster, mixed_effects}`. CUPED is not
a member. That is a real vocabulary gap, not a README gap.

`skills/dsx-explore-data/SKILL.md` already says write EDA as a script, not as
scattered cells. That rule is guidance. It is not a ship preference the executor
fragment enforces.

`references/test-selection.md` already says: independence first, Welch by
default, Shapiro–Wilk on a large sample is theatre. TerryFYL's auto-switch on
Shapiro–Wilk is therefore an anti-feature relative to this repo, not a missing
best practice.

None of the comparison repos, on the text that was read, check shared-budget
interference, triggered-versus-eligible dilution, or a Bayesian continuous-
monitoring story against a published reference value. That is the v2.0.0 gap
this project already owns. v2.1 must not delay it.

---

## 3. Repo-by-repo

### 3.1 Unified AI Data Framework

**What it is.** A markdown hub: twelve playbooks, nine personas, 33 tactical
skills. Claude reads them and writes Jupyter notebooks, reusable `utils/*.py`,
and (in the experimentation playbook) CUPED-adjusted metrics. Quality is "Claude
followed the playbook." There is no blocking gate.

**Playbooks actually listed.** Problem framing, data contract, dimensional
modeling, EDA (with a hypothesis register), hypothesis testing, feature
engineering, model training, model evaluation, inferencing, monitoring,
experimentation (standalone), stakeholder communication. A `/batch-analysis`
command runs the machine-learning path end to end.

**Tactical skills in `skills/03-data-analysis-investigation/` (verified listing).**
`ab-test-analysis`, `business-metrics-calculator`, `cohort-analysis`,
`funnel-analysis`, `root-cause-investigation`, `segmentation-analysis`,
`time-series-analysis`.

**CUPED (verified against `playbooks/09_EXPERIMENTATION.md`).** Section 8 ships
a Python snippet that adjusts the metric with a pre-experiment covariate and
asks for correlation typically `r > 0.3`. It does not gate a post-treatment
covariate. The method's primary paper is Deng, Xu, Kohavi and Walker, *Improving
the Sensitivity of Online Controlled Experiments by Utilizing Pre-Experiment
Data*, WSDM 2013 — that paper is the D-05 candidate for a DSX check, not the
playbook.

**Steal.** Cohort / funnel / root-cause / segmentation *what to do*, expressed
as skills that fill `ANALYSIS-SPEC.yaml`. The EDA hypothesis register, mapped
into `assumptions[]` / `results.tests`. CUPED as a closed-vocabulary member plus
a pre-experiment covariate check.

**Do not steal.** Notebooks as the unit of work. MLflow as a required tracker.
Nine personas that overlap the six DSX agents. `/batch-analysis` that would skip
the plan gate. Dimensional-modeling / dbt / Streamlit product surface (wrong
layer: this overlay specialises GSD, it does not become an analytics stack).

### 3.2 DAAF (Data Analyst Augmentation Framework)

**What it is.** The closest peer on research discipline. An instructions
framework for Claude Code that keeps the human in the driver's seat: file-first
Python or R scripts, nine engagement modes, a six-dimension plan checker,
`LEARNINGS.md`, a reproducibility-verification mode that re-runs scripts against
the report, GUIDE-LLM disclosure of AI use, a Docker sandbox, and DAAFBench
(protocol adherence, not research quality). Still prompt-and-review. Not a
hermetic gate.

**Modes (from README + `02_understanding_daaf.md`).** Data Onboarding, Data
Lookup, Data Discovery, Ad Hoc Collaboration, Full Pipeline, Revision and
Extension, Reproducibility Verification, Framework Development, User Support.
The orchestrator names the mode and asks the human to confirm before proceeding.

**Artifacts of a full pipeline.** `Plan.md` (research spec) + `Plan_Tasks.md`
(executable sequence) + `STATE.md` + `LEARNINGS.md` + stage-scoped scripts as
the real work product + a report. The documentation is explicit: the scripts are
the product, not the notebook.

**Steal.** File-first scripts as the shipped entrypoint (already stated in
explore-data; make it an executor preference). Three engagement modes mapped
onto ceremony tiers already in `docs/gsd-tiers.md` (lookup → Tier 0, ad-hoc →
Tier 1, full pipeline → Tier 2) — DAAF's mode idea without Docker. Portable
data documentation produced at onboarding (`DATA-DICTIONARY.md` next to
`DATA-PROFILE.yaml`). Optional AI-assistance disclosure when `dsx.domain` is
`research`. A reproduce *skill* that re-runs the entrypoint and writes
`REPRO-REPORT.md`; the gate only checks that the report exists and that named
numbers overlap. A `protocol_adherence` tag on the Phase 12 corpus so "the
agent skipped the skill" is countable.

**Do not steal.** Docker as a required runtime. Bundled education datasets.
R as a co-equal execution lane (optional later; not v2.1). The six-dimension
plan checker as a second GSD plan-check — GSD already has a plan-checker
fragment. Putting pandas or R on the gate path to "really" re-run the analysis.

### 3.3 Claude Statistical Analysis Skill (TerryFYL)

**What it is.** One drop-in skill (`~/.claude/skills/`). Trigger: upload a data
file, say "analyze", or name a method. v4 workflow: profile → assumption checks
→ pick a method → output triple (APA 7th-edition table + 300dpi figure + results
paragraph). Complexity paths: simple (0 confirmations), medium (1), complex
(3–4: SEM/CFA, HLM, IRT, meta-analysis). Optional R Docker for the complex path.

**Verified anti-feature.** `SKILL.md` Step 0 runs Shapiro–Wilk for `n < 50` and
skewness/kurtosis otherwise, then auto-switches (e.g. failed normality →
Mann–Whitney). This project's `references/test-selection.md` forbids that order:
independence first, Welch by default, normality only at small n, and
non-parametric tests do not test the same hypothesis as a mean comparison.
Copying the auto-switch would launder a procedure this repo already rejected.

**Steal.** Diagnose-before-analyze as a *skill protocol* that already matches
`dsx-explore-data` then `dsx recommend-test`. The output triple, **only** as an
optional research-domain APA template. Marketing-domain stays narrative + sealed
figure + claim evidence (already gated). Power-analysis as a dedicated no-data
path — `dsx power` already exists; the skill should call it.

**Do not steal.** Shapiro–Wilk auto-switch. SEM/HLM/IRT/meta-analysis as a test
catalogue (brief §3: families, not tests; Phase 11 already owns admissibility).
R Docker as a runtime.

### 3.4 Claude Data Analysis (liangdabiao) and ultra

**What it is.** Slash commands (`/analyze`, `/visualize`, `/generate`, `/report`,
`/quality`, `/hypothesis`), a `data_storage/` folder, hooks on upload, advertised
sub-agents. Both READMEs still say **Week 1.1 — Project Initialization**, with
report-writer, quality-assurance, and hypothesis-generator agents unchecked.
The ultra fork's README is the same text.

**Steal.** A conversational start: slash-command aliases for the eight DSX
skills that already exist, so a CSV-first conversation does not require knowing
GSD phase names. A file-drop hook that runs `dsx profile` **if** GSD Core
exposes hooks for this overlay (`capability.json` currently has `"hooks": []`).
Document the skip if it does not.

**Do not steal.** A `data_storage/` special folder. Multi-language code
generation (R, SQL, JavaScript) as a v2.1 deliverable. Treating the advertised
agent set as a design to copy — several of those agents are not in the repo
yet.

### 3.5 Data Science Plugin (andikarachman)

**What it is.** A Claude Code plugin: nine agents, eight commands, nineteen
skills, nine templates. Loop: Frame → Preprocess → Validate → Explore →
Experiment → Review → Ship → Compound. The distinctive idea is compounding:
`/ds:compound` writes dated YAML-frontmatter files under `docs/ds/learnings/`;
`/ds:plan` and `/ds:experiment` search them before new work.

**Skills actually listed.** Includes `eda-checklist`, `split-strategy`,
`target-leakage-detection`, `statistical-analysis`, `reproducibility-checklist`,
`model-card`, plus library-pattern skills (pandas, polars, scikit-learn,
statsmodels, SHAP, aeon). Prerequisites install pandas/scipy/statsmodels into
the *user* environment — not into a gate.

**Steal.** `docs/dsx/learnings/` with dated YAML frontmatter, searched at
plan-pre. That is the compounding loop. Model-card *template* for predictive
work can wait; it is not a Class A failure and is not in the v2.1 phase list.

**Do not steal.** Great Expectations / dbt tests on the gate path (third-party;
breaks D-01). Library-pattern skills that teach pandas APIs — out of overlay
scope. HuggingFace model cards as a blocking ship requirement.

---

## 4. Head-to-head (plain)

**GSD-DSX is ahead on.** Blocking findings with computed evidence. Experiment
pitfalls (power, peeking, sample-ratio mismatch). Leakage as code. Chart and
narrative gates. Validity frame and paradigm symmetry (in flight in v2.0.0).
Citation-plus-published-reference-value for new checks. Install that works on
Cursor / Codex / OpenCode, not only Claude Code.

**The packs are ahead on.** Ready-made cohort / funnel / root-cause playbooks.
CUPED as a named method. A portable data dictionary from onboarding. Learnings
that compound across projects. File-first scripts as the product (DAAF). A
conversational start ("drop a CSV"). Academic output triples (optional,
research domain). Optional AI-use disclosure.

**Do not copy — anti-features.** Docker as a required runtime. MLflow or Great
Expectations on the gate path. Notebooks as the unit of work. Auto-running
Shapiro–Wilk. SEM / HLM / IRT. Bundled education datasets. A second catalogue of
named tests (Phase 11 already chooses families, not tests). `/batch-analysis`
that skips the plan gate.

---

## 5. Translation rule

Advice in a playbook becomes a **skill or reference** that fills the spec.
Generated notebooks become **scripts** (already the explore-data rule).
"Run the test inside the tool" becomes **declare the test, then gate it**
(`dsx recommend-test` already exists). New finding codes still need a
primary-source citation and a published reference value (D-05). If that
citation is not in hand, the item stays in `brief.md` §6.5 with an entry
condition (D-13).

Vendor blogs, Medium posts, tool-marketing pages, and comparison-repo READMEs
are inadmissible as D-05 citations in either direction.

---

## 6. Placement (locked for v2.1 planning)

v2.1 Analytic Surface is **queued after Phase 12**. It does not reopen Phases
7–12. Skill-only files that invent no new finding codes may be drafted after
Phase 6 in parallel, but they do not gate v2.0.0.

Reason: brief §3 ranks catastrophe-prevention above portfolio value, and Phase
11's ontology is supposed to be built from the calibration corpus, not from a
skill-template wish list. Folding cohort/funnel/CUPED into Phases 7–9 would
give every validity-frame plan a second job and would pressure `families.yaml`
before the dependence taxonomy is stable.

---

## 7. Ready vs gated (for the queued requirements)

**Ready as skill-only (Phases 13–14), no new `DSX-*` codes.**

- Cohort / funnel / root-cause / segmentation skills that fill the spec.
- Hypothesis register from EDA.
- What / So What / Now What in the narrate skill.
- Engagement-mode routing onto existing ceremony tiers.
- Executor preference for `scripts/*.py`.
- `docs/dsx/learnings/` compounding loop.
- `DATA-DICTIONARY.md` beside `DATA-PROFILE.yaml`.
- Optional GUIDE-LLM-style disclosure when `dsx.domain` is `research`.
- Slash-command aliases for the eight existing skills.
- File-drop hook → `dsx profile`, or a documented skip.

**Ready as a gate only with a named primary source (Phase 15).**

- `cuped` added to `VARIANCE_ADJUSTMENTS`. Citation: Deng, Xu, Kohavi and
  Walker (2013), WSDM. Check: covariates declared as pre-experiment; a
  post-treatment covariate blocks. Worked value belongs in the docstring and
  fixture, not as a gate-path computation (D-02).
- Thin spec fields for cohort grain and funnel steps, with survivorship and
  changing-denominator findings — only if each code carries its own D-05
  citation at implement time. If a citation is missing, that code stays in
  §6.5 rather than shipping on a plausible-sounding rule.

**Off the gate path (Phase 16).**

- `dsx-reproduce` skill re-runs the entrypoint and writes `REPRO-REPORT.md`.
- The gate checks presence and number overlap. It does not execute the
  analysis.
- `protocol_adherence` on Phase 12 corpus tags. Extends calibration; does not
  replace catch rate / false-positive rate.

---

## 8. Sources (comparison text, not D-05)

Deng, A., Xu, Y., Kohavi, R. & Walker, T. (2013). "Improving the Sensitivity of
Online Controlled Experiments by Utilizing Pre-Experiment Data." *WSDM '13*.
**This is the D-05 candidate for CUPED.** Confirm the exact formulation and a
published worked value from the paper (or a later Kohavi/Tang/Xu restatement
that quotes it) before Phase 15 ships a code. Do not cite the Unified
playbook's Python snippet as the source.

All other comparison claims in this file trace to the files listed in §1,
fetched 2026-08-26.

---

*Analytic-surface research for: gsd-dsx queued milestone v2.1*
*Researched: 2026-08-26*
*Does not authorise finding codes. Does not reopen D-01…D-14.*
