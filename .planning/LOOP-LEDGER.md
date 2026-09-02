# LOOP-LEDGER — v2.4 Visual Excellence

Source of truth for the autonomous loop. One checkbox = one unit.
Check a box ONLY with its gate evidence pasted in the Log (one line; long
evidence to `LOOP-LEDGER-ARCHIVE.md`).

**Scope source:** `.planning/research/V2.3-V2.4-SCOPE.md` §3 (2026-08-29) and
`.planning/REQUIREMENTS.md` (16 requirements, REQ-P21-01 … REQ-P24-03). Both
carry full goals, citations, license-audit findings and ordering constraints —
**this milestone needs execution, not a fresh scoping round.**

**Predecessors:** v2.3 Test Catalog shipped 2026-09-02 (tag `v2.3.0`); v2.2
shipped 2026-08-29 (tag `v2.2.0`); v2.0.0 shipped 2026-08-28 (tag `v2.1.0`).
Loop artifacts archived at `.planning/milestones/v2.3-LOOP-*`,
`v2.3-HUMAN-QUEUE.md`, and earlier milestones' equivalents.

## Ordering rationale

Phases run in numeric order **21 → 22 → 23 → 24**: Phase 21 is the foundation
Phase 22's catalog spine is built on (a reconciled chart-type vocabulary, no
orphans) and hard-blocks it; Phase 24 is terminal and consumes both v2.3's test
catalog and v2.4's chart/style surfaces for the portfolio exemplar. The D-05
human reads for Phase 22 (the catalog's per-entry citations plus the
uncertainty-family sources) are the longest pole this milestone, though far
lighter than v2.3's — expect ~8–12 reads, mostly stable-URL verifications
rather than paper reads — so the evidence pack is filed at S0.

**Standing v2.4 rules (from the brief §5, repeated because they bind every unit):**
license audit is a plan-review item, not an afterthought, for every Phase 23
style file; the perceptual tie-break ordering is asserted as a structural
criterion against the published Cleveland–McGill ranking, never computed; the
SVG determinism recipe is proven by a double-render hash-equality test kept
OFF the gate path.

## S0 — Milestone bootstrap

- [x] S0-1 Verify GSD state points at v2.4 (STATE.md frontmatter `milestone: v2.4`,
  `current_phase: 21`, progress 0/4) and `gsd-tools query init.milestone-op`
  resolves it (4 phases, 0 complete); `.planning/phases/` is empty (v2.3 dirs
  archived). Gate: command output pasted.
- [x] S0-2 Re-verify the inherited scope against the live tree before planning on
  it: per-requirement verdict table (still-valid / already-satisfied /
  contradicted) written to `.planning/v2.4-SCOPE-RECHECK.md`. Key premises to
  re-confirm: the exact orphan list in `RELATIONSHIP_CHARTS`/`CHART_CAPABILITIES`/
  smells sets (histogram, density, ecdf, strip, diverging_bar, waterfall,
  dumbbell, bump, sankey, kde, population_pyramid, butterfly) still matches the
  live `dsx/checks/viz.py` and `dsx/spec.py`; `BANNED_TYPES` still the same five;
  live catalogue count re-measured (do NOT assume 275). Gate: the recheck file
  with evidence.
- [x] S0-3 File the **Phase 22 D-05 citation evidence pack** to HUMAN-QUEUE
  (catalog spine sources: FT Visual Vocabulary 2016, Wilke 2019 chs. 5+16, the
  Graphic Continuum, the Data Visualisation Catalogue, Datawrapper cardinality
  guidance, Cleveland & McGill 1984 + Heer & Bostock 2010 for the perceptual
  ranking, Munzner 2014 for the task/data-abstraction layers). Per-citation
  table: locator, the exact claim the catalog will cite, confirmed-by-loop vs
  UNVERIFIED-for-human split. **Do not sign — D-05 is a human read.**

## S1 — Phase 21: Viz vocabulary reconciliation (3 requirements)

- [x] S1-1 Discuss (assumptions mode + persona round); `21-CONTEXT.md` written.
  Must settle: the every-mark-has-a-home invariant's exact scope (which sets
  count as "capability families"); how banned-type refusal entries are
  represented (a new sub-map vs an annotation on `BANNED_TYPES`).
- [ ] S1-2 Plan (plan-checker must pass).
- [ ] S1-3 Execute all plans (invariant test; orphans homed; refusal entries
  added).
- [ ] S1-4 Code review + fixes; verification `passed` (REQ-P21-01..03;
  REQ-P21-03 zero-new-codes asserted by set-identity diff).
- [ ] S1-5 `/gsd-secure-phase 21` verified + `/gsd-validate-phase 21` compliant.
  End-of-phase security sign-off + UAT batched to HUMAN-QUEUE (non-blocking
  until S5-2).

## S2 — Phase 22: Catalog spine, uncertainty family, selection heuristic (5 requirements)

- [ ] S2-1 Discuss + persona round; `22-CONTEXT.md`. Must settle: the exact
  merged-entry count and list (target band 75–90); the uncertainty-family
  vocabulary shape (11th relationship key vs new input-type ids); the D-06
  numbering for any new gate codes (REQ-P22-05), from a freshly re-measured
  live catalogue count. Blocked until S1-5 AND the S0-3 evidence pack is
  human-answered for every citation a shipping code depends on.
- [ ] S2-2 Plan (plan-checker must pass).
- [ ] S2-3 Execute all plans (catalog entries + citations; uncertainty family;
  `facet_by` declaration; heuristic edits to question-taxonomy.md/
  chart-selection.md; gate extensions).
- [ ] S2-4 Code review + fixes; verification `passed` (REQ-P22-01..05; the
  perceptual-ranking structural-criterion test green).
- [ ] S2-5 `/gsd-secure-phase 22` + `/gsd-validate-phase 22`; sign-off batched.

## S3 — Phase 23: Style and snippet layer (5 requirements)

- [ ] S3-1 Discuss + persona round; `23-CONTEXT.md`. Must settle: the exact
  `.mplstyle` file list and each one's license/attribution header text; the
  `dsx_plotstyle.py` helper's public function signatures; the determinism
  recipe's exact rcParams. **License audit is this discuss's own explicit
  checklist item** — confirm no GPL port (bbplot), no unlicensed PDF embed
  (Economist 2017 styleguide), OFL font is genuinely vendorable.
- [ ] S3-2 Plan (plan-checker must pass).
- [ ] S3-3 Execute all plans (style files; helper module; snippet catalog;
  palette citations).
- [ ] S3-4 Code review + fixes; verification `passed` (REQ-P23-01..05; the
  double-render hash-equality determinism test green, off the gate path).
- [ ] S3-5 `/gsd-secure-phase 23` + `/gsd-validate-phase 23`; sign-off batched.

## S4 — Phase 24: Portfolio exemplar and viz calibration (3 requirements)

- [ ] S4-1 Discuss (light — calibration shape is Phase-12/20-precedented, the
  exemplar's analytical question is the main design choice); `24-CONTEXT.md`.
- [ ] S4-2 Plan (plan-checker must pass).
- [ ] S4-3 Execute (the end-to-end exemplar; known-bad chart fixtures;
  catch-rate/FPR re-baseline).
- [ ] S4-4 Code review + fixes; verification `passed` (REQ-P24-01..03).
- [ ] S4-5 `/gsd-secure-phase 24` + `/gsd-validate-phase 24`; sign-off batched.

## S5 — Close-out

- [ ] S5-1 `/gsd-audit-uat` cross-phase sweep. **Do NOT accept the CLI's "All
  Clear"** — known under-reporting defects documented in Standing framework
  notes; hand-check every phase's `NN-VERIFICATION.md`.
- [ ] S5-2 Drain HUMAN-QUEUE (the only permitted blocking wait).
- [ ] S5-3 `/gsd-extract-learnings`.
- [ ] S5-4 `/gsd-audit-milestone` — must reach `passed`.
- [ ] S5-5 `/gsd-complete-milestone` — **NOT headless-safe** (interactive
  prompts + `git rm REQUIREMENTS.md`); runs in an interactive session per
  operator approval. Hand-verify the CLI's generated accomplishments and the
  archived REQUIREMENTS checkboxes (wrong at both v2.2's and v2.3's close and
  needed correction each time — expect the same defect class again).
- [ ] S5-6 Ship: merge to `main` **by explicit branch name**
  (`git merge --no-ff gsd/v2.4.0-visual-excellence`, verified on a throwaway
  branch first, full suite + `scripts/check.sh` green BEFORE touching `main`)
  and tag `v2.4.0`. **Never** the framework's alphabetical `gsd/*` auto-detect
  (this repo now carries five stale `gsd/*` branches — the auto-detect would
  pick `gsd/v1.1.0-milestone`); **never** `/gsd-pr-branch`; **never** force-move
  a published tag. Outward-facing — queue to HUMAN-QUEUE for the operator, do
  not self-approve.

## Log

(append one line per firing: `YYYY-MM-DDTHH:MMZ | unit | outcome | evidence`.
Keep the most recent ~15–20; archive older entries to `LOOP-LEDGER-ARCHIVE.md`.)

2026-09-02T21:30Z | milestone-open | v2.4 opened by operator direction in an interactive session (operator traveling, connected from a hotel): scope reused from .planning/research/V2.3-V2.4-SCOPE.md §3 (researched 2026-08-29 alongside v2.3) and re-verified against the live tree at open (dsx/checks/viz.py untouched since before v2.3; catalogue confirmed at 275). REQUIREMENTS.md (REQ-P21-01..P24-03) + ROADMAP.md (Phases 21-24 active) written; STATE.md repointed (v2.4, phase 21, 0/4); PROJECT.md Active Milestone section updated; v2.3 loop artifacts archived to .planning/milestones/v2.3-LOOP-*, v2.3-HUMAN-QUEUE.md; this ledger + LOOP-BRIEF + HUMAN-QUEUE rewritten for v2.4; branch gsd/v2.4.0-visual-excellence created from main; firing script repointed. Usage-limit backoff (with the periodic early-release probe fixed 2026-09-01) carries forward unchanged — proven across v2.3's close. Next = S0-1. | .planning/research/V2.3-V2.4-SCOPE.md §3; scripts/run-ceremony-firing.ps1
2026-09-03T00:00Z | firing-start | Read brief+ledger+queue; reconciled ledger vs repo: HEAD=699c341 (milestone-open commit) matches ledger claim exactly, no correction needed. Untracked operator-local files present (.claude/*, .vscode/, EDA_enhancement_BRIEF.md, graphify-out/, references/The AI Data Scientist.md) — NOT ceremony work, left untouched per brief §1, staging only my own planning files. `gsd-tools` not on PATH; invoke via `node ~/.claude/gsd-core/bin/gsd-tools.cjs`. | git status
2026-09-03T00:00Z | S0-1 | DONE. STATE.md frontmatter milestone:v2.4 current_phase:21 progress 0/4 total_phases:4 completed_phases:0. `init.milestone-op` → milestone_version:v2.4 phase_count:4 completed_phases:0 all_phases_complete:false roadmap/state/project all exist. .planning/phases/ holds only .gitkeep (v2.3 dirs archived). Gate: three command outputs confirmed. | .planning/STATE.md; gsd-tools query init.milestone-op
2026-09-03T00:05Z | S0-2 | DONE. Scope recheck written to .planning/v2.4-SCOPE-RECHECK.md. All 3 key premises re-verified against live tree: (1) 12-orphan list EXACT — 9 relationship-homed-only (histogram/density/ecdf/strip/diverging_bar/waterfall/dumbbell/bump/sankey), kde smells-only, population_pyramid+butterfly IT011-inventory-only (gen-input-types.py:78); none in CHART_CAPABILITIES. (2) BANNED_TYPES = same five {3d_bar,3d_pie,3d_line,radar,dual_axis_line}, still a flat reason-dict (no refusal structure). (3) catalogue count RE-MEASURED 3 ways (invariant test 2-pass; Total line; unique-code grep) = 275, not assumed. viz.py untouched since edf862c (2026-08-10). All 16 reqs still-valid; none satisfied/contradicted. Phase 21 unblocked. | .planning/v2.4-SCOPE-RECHECK.md
2026-09-03T00:12Z | S0-3 | DONE. Phase 22 D-05 evidence pack PREPARED (not signed — D-05 is a human read) and filed as HQ-27. Full per-citation table in .planning/v2.4-D05-EVIDENCE-PACK.md; concise pointer + tiered source list in HUMAN-QUEUE.md Open. Grounded in scope §3 (2026-08-29 research). Tier 1 (code-critical deep read): C&M 1984 JASA 79:531-554, Heer&Bostock 2010 CHI, Wilke ch.16. Tier 2 (per-entry authenticity): FT VV 2016 MIT, Wilke ch.5, Graphic Continuum, DVC, Datawrapper, Munzner 2014. Tier 3 (refusal doctrine): Few/Harris/Tufte/Muth. confirmed-by-loop column scoped honestly = prior-research + bibliographic only (no live fetch this firing); authenticity-at-locator left for human. Non-blocking for Phase 21; blocks S2-1 per-code. **S0 stage COMPLETE.** Next = S1-1 (Phase 21 discuss). | .planning/v2.4-D05-EVIDENCE-PACK.md; HUMAN-QUEUE.md HQ-27
2026-09-03T00:35Z | firing-start | Read brief+ledger+queue; reconciled ledger vs repo: HEAD=22875c8 (S0-3 commit) matches ledger exactly, no correction. Operator-local untracked files (.claude/*, .vscode/, EDA_enhancement_BRIEF.md, graphify-out/, references/*) left untouched per brief §1. S0 complete; first unblocked unit = S1-1 (Phase 21 non-blocking on HQ-27). | git status
2026-09-03T00:35Z | S1-1 | DONE. Phase 21 discuss written to .planning/phases/21-viz-vocabulary-reconciliation/21-CONTEXT.md. Assumptions mode read live RELATIONSHIP_CHARTS/CHART_CAPABILITIES/EXTRA_MARKS/BANNED_TYPES + smells sets with all consumers traced (BANNED_TYPES blast radius = 1 call site, viz.py:86). Architect+Auditor persona round (inline, opus/high, Statistician not engaged — structural discuss) settled both required gray areas: **D-01** invariant scope = two-clause repo-integrity test OFF the gate path; capability-home defined gate-faithfully as CHART_CAPABILITIES ∪ EXTRA_MARKS; frozen CAPABILITY_ONLY allowlist for recommendation-exempt marks. **D-02** refusal entries = enrich BANNED_TYPES in place to {reason,code,citation} records (single registry, no drift surface), reject parallel sub-map; cross-refs existing DSX-VIZ-001 (zero new codes holds). Two findings beyond S0-2 recorded loudly: (1) population_pyramid/butterfly are relationship-orphans ONLY (capability-homed via EXTRA_MARKS[IT011]), not double orphans — corrects S0-2's label, reduces execute churn; (2) ~14 capability-only marks (column/grouped_bar/bubble/donut/sunburst/icicle/circle_pack/timeline/gantt/big_number/candlestick/ohlc_bar/column_range/multi_line) lack a relationship home — documented-exempt, promotion deferred to Phase 22. Homing guidance table pre-staged for S1-2 (plan-checker-verifiable). Veto window HQ-28 filed (non-blocking). STATE.md repointed (single-writer). Next = S1-2 (Phase 21 plan). | .planning/phases/21-viz-vocabulary-reconciliation/21-CONTEXT.md; HUMAN-QUEUE.md HQ-28
