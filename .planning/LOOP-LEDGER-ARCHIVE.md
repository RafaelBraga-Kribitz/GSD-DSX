# LOOP-LEDGER-ARCHIVE — v2.4 Visual Excellence

Long-form evidence for ledger units, offloaded from `LOOP-LEDGER.md` to keep the
hot-path Log lean (brief §5). One `## <unit-id>` section per unit that needs more
than a pointer. The Log line in `LOOP-LEDGER.md` is the index into this file.

---

## S1-2 — Phase 21 plan (planned 2026-09-02, measured UTC ~22:40Z)

**Outcome: DONE. Plan-checker PASSED 12/12 dimensions.** Phase 21 planned via the
`gsd-plan-phase 21` workflow, driven headlessly through every quality gate, then
stopped at the plan-checker pass (the §15 auto-advance to execute was deliberately
NOT taken — see "Boundary held").

### Artifacts produced
- `21-RESEARCH.md` (gsd-phase-researcher, sonnet — adaptive routing).
- `21-VALIDATION.md` (seeded draft, Nyquist; committed `bfa9be7`).
- `21-01-PLAN.md` (gsd-planner, opus — adaptive routing): 1 plan, 1 wave, 3 TDD
  tasks. RED (write `tests/test_viz_vocabulary_invariant.py` — both D-01 clauses +
  frozen 14-mark CAPABILITY_ONLY allowlist + D-02 refusal completeness + gate
  smokes) → GREEN (home the 12 orphans in CHART_CAPABILITIES/RELATIONSHIP_CHARTS,
  then regenerate `dsx/data/input_types.json`) → GREEN (enrich BANNED_TYPES to
  `{reason,code,citation}`, fix the one `_check_banned` reader, annotate HQ-27,
  prove 275 → 275). Covers REQ-P21-01/02/03.

### Gates (all real, orchestrator-run or independently-agent-verified)
- **gsd-plan-checker (opus/high): `## VERIFICATION PASSED`, 12/12 dimensions**, no
  blockers/warnings. Verified against the LIVE tree, not the plan's prose. Notably
  went deeper than RESEARCH on the zero-mint proof: independently confirmed
  `gen-finding-catalogue.py::extract()` (lines 218-234) reads only the positional
  `report.add()` args `[0..2]` (code/severity/message); the `detail=` reference at
  line 250 is inside a *different* function (`extract_sql_rules()`), so the
  BANNED_TYPES `dict[str,str] → {reason,code,citation}` promotion provably cannot
  mint or alter a code. Also validated the IT040 gate smoke (real interval-range
  record, no EXTRA_MARKS entry, currently excludes histogram → will admit after
  regeneration). Nyquist Dim-8 PASS. CLAUDE.md/CRLF compliance PASS (invariant
  test reads live Python objects, no line-anchored parsing → CRLF N/A).
- **Requirements coverage: 3/3** — REQ-P21-01/02/03 in plan frontmatter (YAML
  block list; the workflow's inline grep missed the block form, verified directly)
  and confirmed by plan-checker Dim-1.
- **Decision-coverage gate: 2/2 passed** (`check.decision-coverage-plan`). The
  planner added a machine-readable `- **D-01 …:**` / `- **D-02 …:**` bullet index
  to the top of `21-CONTEXT.md`'s `## Decisions` section — this is the known
  context-coverage parser false-block documented in HUMAN-QUEUE standing notes
  (discuss writes `### D-01 —` headings the parser can't read). Resolved
  legitimately: the gate is now GENUINELY green (no override needed); the edit is
  purely additive, explicitly comment-marked "decision CONTENT is unchanged," and
  the authoritative `### D-01`/`### D-02` bodies are untouched. Verified faithful
  by reading the diff before accepting.

### Persona-round decisions this firing (loud, per brief §4)
1. **Research ON, not `--skip-research`.** Revised mid-firing after reading config:
   `research=true` AND `nyquist_validation=true`, so skipping would NOT cleanly
   disable the Nyquist expectation (it would warn + risk a plan-checker Dim-8 gap)
   — the brief forbids skipping a Nyquist gate to save time. Also: one authoritative
   CONTEXT.md + a role-distinct RESEARCH.md is not the duplicate-truth drift surface
   D-02 rejected. Rigour > flexibility → run the config's designed pipeline.
2. **Plan-checker at opus, not the adaptive-default haiku.** Brief §3 explicitly
   routes plan-check → opus/high; I am the direct spawner, and this is the S1-2 gate
   on a portfolio-grade repo. Rigour tier.

### Skipped as redundant/non-gate (recorded, not silent)
- **pattern-mapper (§7.8, optional/non-blocking):** RESEARCH already mapped the exact
  analog test files (`test_finding_catalogue_invariant.py`,
  `test_phase20_zero_mint_close.py:79-84`) + the importlib idiom.
- **intel api-surface (§7.9):** advisory HINT ("may be incomplete, never exhaustive"),
  not a gate; planner had exhaustive CONTEXT/RESEARCH grounding; avoids committing a
  repo-wide intel artifact as a planning side effect.
- **spec-less probe fallback (§7.95):** no SPEC.md; requirements are precise; the
  planner did standard goal-backward must_haves derivation (checker Dim-6 PASS).
- **dsx-scope-analysis step (§5.6 dsx hook):** self-gating — "if it produces no
  number/model/chart, skip"; Phase 21 is non-analytical → no ANALYSIS-SPEC.yaml,
  `dsx gate plan` passes cleanly.

### RESEARCH findings beyond CONTEXT (carried into the plan)
- **input_types.json regeneration gotcha:** CHART_CAPABILITIES/EXTRA_MARKS edits only
  reach the gate's IT-id path through the *generated static* `dsx/data/input_types.json`
  — the plan makes `python scripts/gen-input-types.py` + committing the JSON a task step.
- **Zero-mint mechanically verified** (see plan-checker note above).
- **HQ-27 Tier-3 has NO source mapped to `radar`** — the plan populates a best-fit
  provisional citation and flags radar for S5-2 operator correction (D-02's designed
  non-blocking D-05 path), NOT a silent choice. Open item for HQ-27 signing.

### Boundary held
`auto_advance=true` in config means `gsd-plan-phase` §15 would auto-launch
`gsd-execute-phase`. I did NOT take it: S1-2 (plan) and S1-3 (execute) are separate
gated ceremony units, and the plan-checker pass must be committed with its evidence
before any execution. Did not flip the operator's persistent `auto_advance` config.

### Clock note
`date -u` reads 2026-09-02T22:xxZ (machine is UTC-3; local 19:xx). Prior firings'
`2026-09-03T00:xxZ` Log labels ran ~2h ahead of true UTC. This firing uses measured
UTC — so its timestamp reads earlier than the prior line. Git commit timestamps are
the authoritative chronology; Log timestamps are human markers only.

## S2-2 — Phase 22 plan (2026-09-03)

Planned via `gsd-plan-phase 22`, driven by the orchestrator following the workflow
faithfully — researcher, planner, and plan-checker each spawned as a **separate
Agent** (roles never collapsed inline, per the workflow's hard rule that independent
agent contexts are required for a meaningful plan-checker gate).

**Pipeline (all committed):**
- `gsd-phase-researcher` (sonnet) → `22-RESEARCH.md`, committed `0ba32d1`. Surfaced
  three gaps CONTEXT does not name (all verified by running the live tests, not
  inferred): (1) the ten new Wilke uncertainty marks need a `CHART_CAPABILITIES`
  home or Phase 21's `test_every_mark_has_a_capability_home` invariant goes red;
  (2) `tests/test_finding_catalogue_invariant.py` hard-codes `_EXPECTED_TOTAL=275`
  and an exact `_MINTED_CODES` set — this file *is* the additive-mint proof;
  (3) `DSX-VIZ-*` is absent from `gen-finding-catalogue.py`'s `_D05_ALLOWLIST_PREFIXES`,
  so the new code's D-05 enforcement needs an exact-string add to `_D05_ALLOWLIST_CODES`.
  Also flagged: `chart-selection.md`'s "Encoding accuracy" line still ships the OLD
  false 7-item strict order (correct it to D-1's 6-rank-with-ties); `dsx-visualize`
  SKILL enumerates 10 relationships (ripple for the 11th key); recommend dropping
  Abela 2008 / Few's Graph Selection Matrix (never in HQ-27).
- Orchestrator wrote the Nyquist `22-VALIDATION.md` seed (§5.5), committed `684530e`.
- `gsd-planner` (opus) → `22-01..04-PLAN.md` (4 plans / 4 waves), committed `81ea14c`
  (see BRANCH REMEDIATION below — the commit was salvaged onto the canonical branch).
- `gsd-plan-checker` (**opus** — brief §3 override of the adaptive profile's haiku
  default, exactly as S1-2 did) → `## VERIFICATION PASSED`, all 7 focus items green.

**Plans (wave order forced by shared ownership of `dsx/checks/viz.py` + real deps):**
- 22-01 (wave 1, tdd; REQ-P22-02,-03): 11th `RELATIONSHIP_CHARTS["uncertainty"]` key
  + ten §5.6 marks; homes them into `CHART_CAPABILITIES["interval-range"]` (gap 1);
  adds `gauge`/`word_cloud` refusal records + swaps `radar`→Duan 2023; `facet_by`
  orthogonal → routes to DSX-SMELL-007. Mints 0 codes (275→275 at this wave).
- 22-02 (wave 2, tdd; REQ-P22-05): mints `DSX-VIZ-071` (`_check_uncertainty_vocabulary`),
  allowlists by exact string (gap 3), bumps invariant 275→276 + `_MINTED_CODES` (gap 2);
  records the loud **DSX-VIZ-072-not-minted** decision.
- 22-03 (wave 3, execute; REQ-P22-01,-05): `references/chart-catalog.md` (~80 rows,
  three axes + citation, fenced-JSON payload) split acquisition/authoring/verification;
  new conformance + perceptual-tie-break repo-integrity tests.
- 22-04 (wave 4, execute; REQ-P22-04): 5-layer heuristic route-and-cite into the two
  existing taxonomy files + skill ripple (10→11 relationships); corrects the superseded
  perceptual line; drops Abela 2008 / Few's Graph Selection Matrix.

**DSX-VIZ-072 not minted (persona-round decision, GA-3 contingent reservation, HQ-30
veto window).** GA-3 reserved 072 only "if a second distinct uncertainty check is
warranted (e.g. paradigm-mismatch)." The planner found it is not: several §5.6 marks
(error bars, graded error bars) legitimately render either a frequentist confidence
interval or a Bayesian credible interval, so no mark→paradigm partition exists to gate
against; REQ-P22-02's "D-12a-clean" is satisfied by the 11th-key structure by
construction. Matches the research recommendation. Phase 22 blocking-code footprint =
exactly one; set-identity diff proves 275→276, additive-only.

**Plan-checker advisory (non-blocking, no revision required):** 2 LOW warnings —
(1) 22-02 lacks a cosmetic `<artifacts_this_phase_produces>` section (coverage NOT
lost: 22-01's canonical index enumerates 22-02's artifacts and 22-02 lists them in
`must_haves.artifacts` + a loud decision block); (2) chained `&&` verify commands
assume Bash/pwsh7 — executor should run them through the Bash tool, not Windows
PowerShell 5.1. No BLOCKERs.

**BRANCH REMEDIATION (loud — the honesty this project's standard demands).** Mid-plan,
the `gsd-planner` subagent ran `git checkout -b gsd/v2.4-visual-excellence` (no `.0`)
and committed the four plans (`81ea14c`) on that new branch — a direct violation of
plan-phase §0's Git Branch Invariant ("do not create, rename, or switch git branches
during plan-phase"). Its own return then confidently asserted the canonical
`.0` branch name "was inaccurate" — the claim was itself the error. The **reflog was
the fact** (`HEAD@{1}: checkout: moving from gsd/v2.4.0-visual-excellence to
gsd/v2.4-visual-excellence`). The canonical branch is unambiguously
`gsd/v2.4.0-visual-excellence` (with `.0`): it is what `origin` tracks, what
LOOP-BRIEF/STATE/ledger all name, and what session-start reported. Because `81ea14c`
is a **linear descendant** of the canonical branch's tip (`684530e`), the orchestrator
`git checkout gsd/v2.4.0-visual-excellence` → `git merge --ff-only` (Updating
684530e..81ea14c) → `git branch -d gsd/v2.4-visual-excellence` (the safe `-d` confirmed
it was fully merged — no commit lost). Stale `gsd/*` branch count restored to five (the
prior-milestone set), NOT a new sixth — which matters because the ship auto-detect
picks the alphabetically-first `gsd/*`. This is exactly the class of subagent error the
brief's "verify against the repo, not the claim" rule exists to catch.

---

## Log entries trimmed 2026-09-03 (bootstrap S0 + Phase 21 S1)

The 15 oldest `LOOP-LEDGER.md` Log entries, relocated verbatim to keep the hot-path
file lean (brief §5: most recent ~15-20 entries in the ledger; archive older,
never delete). Covers milestone-open, S0-1..S0-3, and Phase 21 S1-1..S1-5 plus their
firing-start reconciliation lines. Chronology is by git commit time, not the (early,
clock-skewed) UTC labels — see the note in the S1-2/S1-3 lines below.

2026-09-02T21:30Z | milestone-open | v2.4 opened by operator direction in an interactive session (operator traveling, connected from a hotel): scope reused from .planning/research/V2.3-V2.4-SCOPE.md §3 (researched 2026-08-29 alongside v2.3) and re-verified against the live tree at open (dsx/checks/viz.py untouched since before v2.3; catalogue confirmed at 275). REQUIREMENTS.md (REQ-P21-01..P24-03) + ROADMAP.md (Phases 21-24 active) written; STATE.md repointed (v2.4, phase 21, 0/4); PROJECT.md Active Milestone section updated; v2.3 loop artifacts archived to .planning/milestones/v2.3-LOOP-*, v2.3-HUMAN-QUEUE.md; this ledger + LOOP-BRIEF + HUMAN-QUEUE rewritten for v2.4; branch gsd/v2.4.0-visual-excellence created from main; firing script repointed. Usage-limit backoff (with the periodic early-release probe fixed 2026-09-01) carries forward unchanged — proven across v2.3's close. Next = S0-1. | .planning/research/V2.3-V2.4-SCOPE.md §3; scripts/run-ceremony-firing.ps1
2026-09-03T00:00Z | firing-start | Read brief+ledger+queue; reconciled ledger vs repo: HEAD=699c341 (milestone-open commit) matches ledger claim exactly, no correction needed. Untracked operator-local files present (.claude/*, .vscode/, EDA_enhancement_BRIEF.md, graphify-out/, references/The AI Data Scientist.md) — NOT ceremony work, left untouched per brief §1, staging only my own planning files. `gsd-tools` not on PATH; invoke via `node ~/.claude/gsd-core/bin/gsd-tools.cjs`. | git status
2026-09-03T00:00Z | S0-1 | DONE. STATE.md frontmatter milestone:v2.4 current_phase:21 progress 0/4 total_phases:4 completed_phases:0. `init.milestone-op` → milestone_version:v2.4 phase_count:4 completed_phases:0 all_phases_complete:false roadmap/state/project all exist. .planning/phases/ holds only .gitkeep (v2.3 dirs archived). Gate: three command outputs confirmed. | .planning/STATE.md; gsd-tools query init.milestone-op
2026-09-03T00:05Z | S0-2 | DONE. Scope recheck written to .planning/v2.4-SCOPE-RECHECK.md. All 3 key premises re-verified against live tree: (1) 12-orphan list EXACT — 9 relationship-homed-only (histogram/density/ecdf/strip/diverging_bar/waterfall/dumbbell/bump/sankey), kde smells-only, population_pyramid+butterfly IT011-inventory-only (gen-input-types.py:78); none in CHART_CAPABILITIES. (2) BANNED_TYPES = same five {3d_bar,3d_pie,3d_line,radar,dual_axis_line}, still a flat reason-dict (no refusal structure). (3) catalogue count RE-MEASURED 3 ways (invariant test 2-pass; Total line; unique-code grep) = 275, not assumed. viz.py untouched since edf862c (2026-08-10). All 16 reqs still-valid; none satisfied/contradicted. Phase 21 unblocked. | .planning/v2.4-SCOPE-RECHECK.md
2026-09-03T00:12Z | S0-3 | DONE. Phase 22 D-05 evidence pack PREPARED (not signed — D-05 is a human read) and filed as HQ-27. Full per-citation table in .planning/v2.4-D05-EVIDENCE-PACK.md; concise pointer + tiered source list in HUMAN-QUEUE.md Open. Grounded in scope §3 (2026-08-29 research). Tier 1 (code-critical deep read): C&M 1984 JASA 79:531-554, Heer&Bostock 2010 CHI, Wilke ch.16. Tier 2 (per-entry authenticity): FT VV 2016 MIT, Wilke ch.5, Graphic Continuum, DVC, Datawrapper, Munzner 2014. Tier 3 (refusal doctrine): Few/Harris/Tufte/Muth. confirmed-by-loop column scoped honestly = prior-research + bibliographic only (no live fetch this firing); authenticity-at-locator left for human. Non-blocking for Phase 21; blocks S2-1 per-code. **S0 stage COMPLETE.** Next = S1-1 (Phase 21 discuss). | .planning/v2.4-D05-EVIDENCE-PACK.md; HUMAN-QUEUE.md HQ-27
2026-09-03T00:35Z | firing-start | Read brief+ledger+queue; reconciled ledger vs repo: HEAD=22875c8 (S0-3 commit) matches ledger exactly, no correction. Operator-local untracked files (.claude/*, .vscode/, EDA_enhancement_BRIEF.md, graphify-out/, references/*) left untouched per brief §1. S0 complete; first unblocked unit = S1-1 (Phase 21 non-blocking on HQ-27). | git status
2026-09-03T00:35Z | S1-1 | DONE. Phase 21 discuss written to .planning/phases/21-viz-vocabulary-reconciliation/21-CONTEXT.md. Assumptions mode read live RELATIONSHIP_CHARTS/CHART_CAPABILITIES/EXTRA_MARKS/BANNED_TYPES + smells sets with all consumers traced (BANNED_TYPES blast radius = 1 call site, viz.py:86). Architect+Auditor persona round (inline, opus/high, Statistician not engaged — structural discuss) settled both required gray areas: **D-01** invariant scope = two-clause repo-integrity test OFF the gate path; capability-home defined gate-faithfully as CHART_CAPABILITIES ∪ EXTRA_MARKS; frozen CAPABILITY_ONLY allowlist for recommendation-exempt marks. **D-02** refusal entries = enrich BANNED_TYPES in place to {reason,code,citation} records (single registry, no drift surface), reject parallel sub-map; cross-refs existing DSX-VIZ-001 (zero new codes holds). Two findings beyond S0-2 recorded loudly: (1) population_pyramid/butterfly are relationship-orphans ONLY (capability-homed via EXTRA_MARKS[IT011]), not double orphans — corrects S0-2's label, reduces execute churn; (2) ~14 capability-only marks (column/grouped_bar/bubble/donut/sunburst/icicle/circle_pack/timeline/gantt/big_number/candlestick/ohlc_bar/column_range/multi_line) lack a relationship home — documented-exempt, promotion deferred to Phase 22. Homing guidance table pre-staged for S1-2 (plan-checker-verifiable). Veto window HQ-28 filed (non-blocking). STATE.md repointed (single-writer). Next = S1-2 (Phase 21 plan). | .planning/phases/21-viz-vocabulary-reconciliation/21-CONTEXT.md; HUMAN-QUEUE.md HQ-28
2026-09-02T22:38Z | firing-start | Read brief+ledger+queue; reconciled ledger vs repo: HEAD=09335d9 (S1-1 commit) matched ledger exactly, no correction. Operator-local untracked files (.claude/*, .vscode/, EDA_enhancement_BRIEF.md, graphify-out/, references/*) left untouched per brief §1. First unblocked unit = S1-2 (Phase 21 plan; non-blocking on HQ-27). CLOCK: `date -u`=2026-09-02T22:xxZ (machine UTC-3); prior firings' 2026-09-03T00:xxZ labels ran ~2h ahead of true UTC — this + later lines use MEASURED UTC, so they read earlier than the line above (git commit times are the real chronology). | git log/status
2026-09-02T22:53Z | firing-start | Read brief+ledger+queue; reconciled ledger vs repo: HEAD=ba09357 (S1-2 DONE commit) matches ledger exactly, no correction. Operator-local untracked files (.claude/*, .vscode/, EDA_enhancement_BRIEF.md, graphify-out/, references/The AI Data Scientist.md) left untouched per brief §1. HQ-27/HQ-28 still open, non-blocking for Phase 21. First unblocked unit = S1-3 (execute). Measured UTC (`date -u`)=22:53Z — machine now on true UTC; using measured stamps. | git log/status
2026-09-02T23:00Z | S1-3 | DONE. Phase 21 plan (21-01-PLAN.md) executed INLINE by orchestrator (persona-lite decision, recorded: plan left zero design judgment, orchestrator must re-run all gates regardless, CONTEXT required single-firing no-compaction, STATE is single-writer — inline avoids the subagent-touches-tracking-file tension; §3's no-waste-opus intent met since re-verify costs comparable tokens). 3 TDD tasks RED→GREEN→GREEN. **Task 1 RED**: new tests/test_viz_vocabulary_invariant.py (off gate path; EXTRA_MARKS via importlib) — RED-confirmed exact orphan lists: 10 capability [bump,density,diverging_bar,dumbbell,ecdf,histogram,kde,sankey,strip,waterfall], 3 relationship [butterfly,kde,population_pyramid]; no assertion softened. **Task 2 GREEN**: homed 12 orphans one-family-each — spec.py CHART_CAPABILITIES (interval-range +histogram/density/ecdf/strip/kde; categorical-value +diverging_bar; composition +waterfall; categorical-multi +dumbbell/bump; matrix +sankey), viz.py RELATIONSHIP_CHARTS (distribution +kde/population_pyramid; comparison +butterfly); population_pyramid/butterfly NOT touched in CHART_CAPABILITIES (already EXTRA_MARKS[IT011], Pitfall 2); regenerated dsx/data/input_types.json (Pitfall 1). Gate: 22 OK (TestEveryMarkHasAHome incl. both gate smokes + tests.test_input_types). **Task 3 GREEN**: BANNED_TYPES→{reason,code,citation} in place (code=DSX-VIZ-001 all five), _check_banned reader fixed to ["reason"]; citations 3d_*→Munzner ch.6+Tufte, dual_axis_line→Muth 2018 (+see DSX-VIZ-030), radar→PROVISIONAL flagged; HQ-27 Tier-3 annotated with per-mark map + radar gap for S5-2. Gate: 54 OK. **REQ-P21-03**: catalogue 275→275 three ways (Total-line grep, CRLF-safe unique-code count, catalogue-invariant test) — zero mint. **Phase suite**: `unittest discover -s tests` = 1470 OK. 21-01-SUMMARY.md + STATE.md (completed_plans 0→1) written. BOUNDARY: did NOT advance to S1-4 (separate unit; code review + verification is opus/high, better for a fresh firing). Next = S1-4. | 21-01-SUMMARY.md; tests/test_viz_vocabulary_invariant.py; LOOP-LEDGER-ARCHIVE.md not needed
2026-09-02T22:42Z | S1-2 | DONE. Phase 21 planned via gsd-plan-phase (research ON). 21-01-PLAN.md = 1 plan/1 wave/3 TDD tasks (RED invariant test → GREEN home 12 orphans + regen input_types.json → GREEN enrich BANNED_TYPES to {reason,code,citation} + prove 275→275; covers REQ-P21-01/02/03). GATES: gsd-plan-checker (opus/high per brief §3) PASSED 12/12 incl. goal-backward + Nyquist Dim-8 + zero-mint (checker independently proved gen-finding-catalogue.py extract() never reads detail= — dict-of-dict promotion cannot mint a code); requirements 3/3; decision-coverage 2/2. Research (sonnet) surfaced 3 findings beyond CONTEXT (input_types.json MUST be regenerated or IT-id gate path stays stale; zero-mint mechanically verified; HQ-27 Tier-3 has NO `radar` source → plan flags for S5-2, not silent). Persona decisions (loud): research ON not --skip (Nyquist gate + no drift surface); plan-checker opus not adaptive-haiku (brief §3). Skipped non-gate: pattern-mapper/intel-api-surface/spec-less-probe/dsx-scope (all redundant or self-gating). Planner added a D-01/D-02 bullet index to 21-CONTEXT.md — the known context-coverage false-block (HUMAN-QUEUE standing note), resolved legitimately (genuinely green; authoritative ### bodies unchanged). BOUNDARY HELD: did NOT auto-advance to execute despite auto_advance=true (S1-3 is a separate unit). Full detail: LOOP-LEDGER-ARCHIVE.md ## S1-2. Next = S1-3 (execute). | .planning/phases/21-viz-vocabulary-reconciliation/21-01-PLAN.md; 21-RESEARCH.md; LOOP-LEDGER-ARCHIVE.md#S1-2
2026-09-02T23:12Z | firing-start | Read brief+ledger+queue; reconciled ledger vs repo: HEAD=4b5c32d (S1-3 execute commit) matches ledger exactly, no correction. Operator-local untracked files (.claude/*, .vscode/, EDA_enhancement_BRIEF.md, graphify-out/, references/The AI Data Scientist.md) left untouched per brief §1. HQ-27/HQ-28 open, non-blocking for Phase 21. First unblocked unit = S1-4. Measured UTC (`date -u`) = 23:09Z. | git log/status
2026-09-02T23:25Z | S1-4 | DONE. Phase 21 code review + verification, opus/high (brief §3), gates ALL re-run by orchestrator on the final post-fix tree (not trusted from S1-3 inline report). **Review** (21-REVIEW.md): read both production hunks + the new invariant module in full; the one real risk (BANNED_TYPES str→dict) swept repo-wide — exactly 2 runtime consumers, both in viz.py (membership check unaffected, detail reader correctly →["reason"]); not vocab-dumped, no CLI surface; no second reader breaks. Homing math exact (10 capability + 3 relationship orphans, kde double-homed; population_pyramid/butterfly relationship-only per Pitfall 2). **2 LOW findings fixed this unit** (test-hardening only, cannot touch production/275): LOW-1 invariant test had no non-vacuity guard on _mark_universe() (3 clauses would pass vacuously if the vocab emptied) → added test_mark_universe_is_non_vacuous (anchors {bar,line,scatter,histogram,box} + floor ≥30, live 50); LOW-2 CAPABILITY_ONLY could carry a phantom entry undetected → added CAPABILITY_ONLY ⊆ universe guard. **Verification** (21-VERIFICATION.md, verdict PASSED): REQ-P21-01 invariant 9 OK incl. both gate smokes (coarse-family + IT040 JSON path); REQ-P21-02 refusal records complete (5×{reason,code,citation}, code=DSX-VIZ-001, radar detail contract green); REQ-P21-03 **set-identity diff** codes(4b5c32d^) vs codes(HEAD) = 275==275, symmetric difference EMPTY, gen --check "catalogue is current" @275 (3 declared-twice warnings pre-existing, unchanged by empty diff). Full suite 1470→**1471 OK** (final tree). REQ-P21-01..03 checked in REQUIREMENTS.md. STATE repointed (single-writer): next = S1-5. BOUNDARY: S1-5 (secure+validate) is a separate unit, opus/high, left for next firing. | 21-REVIEW.md; 21-VERIFICATION.md
2026-09-02T23:23Z | firing-start | Read brief+ledger+queue; reconciled ledger vs repo: HEAD=7a6e7e6 (S1-4 DONE commit) matches ledger exactly, no correction. Operator-local untracked files (.claude/*, .vscode/, EDA_enhancement_BRIEF.md, graphify-out/, references/The AI Data Scientist.md) left untouched per brief §1. HQ-27/HQ-28 open, non-blocking for Phase 21. First unblocked unit = S1-5. Measured UTC (`date -u`) = 23:23Z. | git log/status
2026-09-02T23:33Z | S1-5 | DONE. Phase 21 secure+validate, opus/high; **both gates re-run by the orchestrator, not trusted from S1-4**. **secure-phase** (State B create → 21-SECURITY.md): security step hook active; 3 plan-time threats T-21-01/02/03, register_authored_at_plan_time=true + ASVS-L1 → valid short-circuit (threats_open:0). Each classified CLOSED by re-running its mitigation — TestEveryMarkHasAHome (T-21-01) + TestRefusalEntryCompleteness/code=DSX-VIZ-001 (T-21-02) + finding_catalogue_invariant/gen 275→275 set-identity (T-21-03) = 55 tests OK. status:verified; no threat ≥high → non-blocking; no packages → no supply-chain gate. Human approval line filed **HQ-29** (brief §4 item 4; non-blocking until S5-2). **validate-phase** (State A, 21-VALIDATION.md draft→validated): nyquist step hook active; gap analysis all 3 reqs COVERED with green automated tests, 0 MISSING/0 PARTIAL → **nyquist_compliant:true**, no auditor spawn. Filled Per-Task map (3 tasks/1 wave); one Manual-Only row = refusal-citation *authenticity* (D-05, tracked under HQ-27, not duplicated). Full suite re-run **1471 OK, 40.4s measured** (clean tree, DECISIONS.jsonl swept). STATE repointed (single-writer): completed_phases 0→1, current_phase→22, percent 25. **Phase 21 fully shipped (S1-1..S1-5).** BLOCKED-STATE (logged once per §9): with S1-5 done, S2-1 is blocked on **HQ-27** (D-05 pack unsigned — no operator edits to .planning/v2.4-D05-EVIDENCE-PACK.md) and S2-2..S5-6 are gated behind it by numeric phase order → all remaining units blocked on HUMAN-QUEUE, the milestone's designed pause point. Later firings in this state do a TRUE no-op until HQ-27 is answered. | 21-SECURITY.md; 21-VALIDATION.md; HUMAN-QUEUE HQ-29
