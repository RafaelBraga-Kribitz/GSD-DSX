---
gsd_state_version: 1.0
milestone: v2.4
milestone_name: Visual Excellence
current_phase: 24
current_phase_name: portfolio-exemplar-viz-calibration
status: executing
stopped_at: "S4-1 DONE (box CHECKED) — Phase 24 discuss, opus/high inline (S1-1/S2-1/S3-1 precedent — single-writer artifact, no compaction). Persona round Architect+Statistician+Auditor (Advisor not engaged — no external-tooling gray area). 24-CONTEXT.md written. Three gray areas settled + a D-06 zero-mint note. GA-1 (the main design choice): UPGRADE the existing examples/good-* onboarding-activation exemplar IN PLACE into the full v2.4 capstone (reuse a spec already green through every gate; add only the v2.4 presentation delta — figures via dsx-urban style layer + dsx_plotstyle.py, ONE uncertainty figure showing the real 95% CI on the activation uplift routed via DSX-VIZ-071, a SEALED FIGURE-MANIFEST via dsx seal, a strict What/So What/Now What NARRATIVE, a REPRO-REPORT) — NOT a net-new question (unanimous vote; rigour>reliability>flexibility: net-new re-opens estimand/power/SRM on a terminal phase for no coverage gain). GA-2: author the FIRST bad-chart-choice fixtures (none exist today — the known-bad corpus is all bad-test-choice), mirror the known-bad convention, extend test_known_bad_corpus.py + re-baseline catch-rate/FPR; minimal-honest 'per new code' set = one DSX-VIZ-071 fixture + one each for the new gauge/word_cloud DSX-VIZ-001 refusal rows + >=1 banned control; the exact gate SURFACE a chart defect is caught on is deferred to S4-2 plan-research (read viz.py) — flagged, not guessed. GA-3: REQ-P24-03 is verify-not-build — both selection surfaces already have doc/code agreement tests (test_doc_code_agreement.py for test-selection.md; test_selection_heuristic_docs.py for chart-selection.md); verify green + catalogue current + snapshots unmutated, close a gap only if S4-2 finds one. D-06 note: Phase 24 mints ZERO new codes → set-identity 276→276 target at S4-4 (re-measure live count at plan time). Veto window HQ-35 filed (non-blocking, silence=accept). NEXT: S4-2 (Phase 24 plan; plan-checker must pass; opus/high per brief §3)."
last_updated: "2026-09-03T09:56Z"
last_activity: 2026-09-03
last_activity_desc: "S4-1 DONE — Phase 24 discuss, opus/high inline. Persona round (Architect+Statistician+Auditor) settled the main design choice: UPGRADE the existing examples/good-* onboarding-activation exemplar in place into the full v2.4 capstone (sealed manifest, dsx-urban style layer, one real-CI uncertainty figure via DSX-VIZ-071, What/So What/Now What narrative, REPRO-REPORT) rather than author a net-new question. GA-2 = first bad-chart-choice fixtures + catch-rate/FPR re-baseline (exact gate surface deferred to S4-2 research). GA-3 = REQ-P24-03 verify-not-build (both doc/code agreement tests already exist). D-06 = zero new codes, 276→276. 24-CONTEXT.md written; HQ-35 veto window filed (non-blocking). Next = S4-2 (Phase 24 plan, opus/high)."
progress:
  total_phases: 4
  completed_phases: 3
  total_plans: 8
  completed_plans: 8
  percent: 75
---

# Project state

**Status:** v2.4 Visual Excellence — OPEN, executing under the autonomous ceremony
**Progress:** [░░░░░░░░░░░░░░░░░░░░] v2.4 — 0/4 phases (21 viz vocabulary reconciliation → 22 catalog spine/uncertainty/heuristic → 23 style/snippet layer → 24 portfolio exemplar/calibration)
**Predecessors:** v2.3 Test Catalog SHIPPED 2026-09-02 (tag `v2.3.0`); v2.2 Analytic Surface SHIPPED 2026-08-29 (tag `v2.2.0`); v2.0.0 DSX Validity Frame SHIPPED 2026-08-28 (tag `v2.1.0`). Archives under `.planning/milestones/`.

**Loop control:** the autonomous ceremony drives this milestone. Contract:
`.planning/LOOP-BRIEF.md`; backlog + gates: `.planning/LOOP-LEDGER.md`; human-only
items: `.planning/HUMAN-QUEUE.md`. Branch `gsd/v2.4.0-visual-excellence`, ships
as tag `v2.4.0` by explicit named merge (never the auto-detected branch — this
repo now carries five stale `gsd/*` branches from prior milestones).

**Usage-limit posture (proven 2026-08-30 through 2026-09-02):** the firing
wrapper (`scripts/run-ceremony-firing.ps1`) detects limit hits, backs off
gracefully, and — critically — re-probes every 30 minutes during any hold to
catch an early release rather than blindly waiting the full computed window
(fixed 2026-09-01 after Anthropic released a weekly limit early and the
original dead-reckoning design missed it). Observed live: four separate
5-hour-window hits on 2026-09-02 each self-recovered in 2–7 minutes. Firings
must not retry in a loop — log one line and stop; the wrapper owns the pacing.

## Project Reference

See: .planning/PROJECT.md (updated 2026-09-02; Key Decisions table there is the full decision log)

**Core value:** Gate analytical work on validity before the data is touched.
**Current focus:** Phase 24 — portfolio exemplar and viz calibration (the terminal phase: one end-to-end capstone exercising both v2.3's test catalog and v2.4's style/uncertainty surfaces, plus the first bad-chart-choice fixtures and a catch-rate/FPR re-baseline). Phases 21 (viz vocabulary reconciliation), 22 (catalog spine / uncertainty family / selection heuristic), and 23 (style / snippet layer) are shipped.

## Current Position

Phase: 24 (portfolio-exemplar-viz-calibration) — S4-1 discuss DONE (box CHECKED); 24-CONTEXT.md written; next unit S4-2 (plan; plan-checker must pass)
Plan: Phases 21+22+23 all shipped. Phase 24 discuss settled the capstone design: upgrade the existing examples/good-* onboarding-activation exemplar in place (sealed manifest, dsx-urban style layer, one real-CI uncertainty figure via DSX-VIZ-071, What/So What/Now What narrative, REPRO-REPORT); first bad-chart fixtures + catch-rate/FPR re-baseline; REQ-P24-03 verify-not-build. Zero new codes (276→276 target). Full suite 1507 OK at Phase 23 close; catalogue 276
Status: Executing (v2.4 — 3/4 phases complete; Phase 24 discuss done; HQ-33/HQ-34 non-blocking until S5-2; HQ-35 discuss veto window filed non-blocking)
Last activity: 2026-09-03 — S4-1: Phase 24 discuss (opus/high inline), persona round Architect+Statistician+Auditor; GA-1/GA-2/GA-3 + D-06 zero-mint note settled; 24-CONTEXT.md + HQ-35 veto window

## Performance Metrics

No v2.4 plans executed yet. v2.3, v2.2, and v2.0.0 velocity are archived with their milestone artifacts.

## Accumulated Context

### Decisions

Full decision log: PROJECT.md Key Decisions. Standing v2.4 decisions (carried from the original v2.3/v2.4 scoping, operator-directed 2026-08-29, re-confirmed at open):

- **The chart catalog is citable, not exhaustive-for-its-own-sake** — union of five named taxonomies (FT Visual Vocabulary, Wilke, Graphic Continuum, DVC, Datawrapper) after synonym merge and principled exclusions, target band 75–90 entries.
- **License audit is a plan-review gate, not an afterthought** — dsx-538/dsx-urban forked or built from permissively-licensed sources; dsx-econ/dsx-bbc reimplemented from published doctrine only, never porting GPL code (bbplot) or embedding an unlicensed PDF (the 2017 Economist styleguide).
- **Faceting is a declaration, not a chart type** — `facet_by` orthogonal to the mark, per the scope research's completeness-critic finding.
- **Contingency:** split Phase 23–24 off as v2.5 if the D-05 queue materially outruns cadence (expected lighter than v2.3's — ~8–12 reads vs 27).

### Pending Todos

None beyond the ledger.

### Blockers/Concerns

None open.

## Deferred Items

Carried forward from v2.0.0 close — captured future ideas, not gaps:

| Category | Item | Status | Deferred At |
|----------|------|--------|-------------|
| seed | SEED-001-deepen-dsx-explore-data-eda-protocol | dormant — natural v2.4/v2.5 candidate | 2026-08-28 |
| seed | SEED-002-grow-data-profile-hermetic-eda-artifacts | dormant — natural v2.4/v2.5 candidate | 2026-08-28 |

## Session Continuity

Last session: 2026-09-02 (interactive session — v2.3 ship + v2.4 open, operator traveling with intermittent connectivity)
Stopped at: v2.4 fully scoped and the ceremony repointed; no ledger unit attempted yet.
Resume file: None — the next firing takes S0-1 from LOOP-LEDGER.md.
