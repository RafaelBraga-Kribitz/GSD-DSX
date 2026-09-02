---
gsd_state_version: 1.0
milestone: v2.4
milestone_name: Visual Excellence
current_phase: 21
current_phase_name: viz-vocabulary-reconciliation
status: executing
stopped_at: "S1-3 (Phase 21 execute) COMPLETE: 21-01-PLAN.md executed inline, 3 TDD tasks RED→GREEN→GREEN. Task 1 new tests/test_viz_vocabulary_invariant.py (off gate path) RED-confirmed with exact orphan lists (10 capability, 3 relationship). Task 2 homed 12 orphans one-family-each into CHART_CAPABILITIES/RELATIONSHIP_CHARTS, regenerated dsx/data/input_types.json (both gate smokes green). Task 3 enriched BANNED_TYPES→{reason,code,citation} (code=DSX-VIZ-001 all five), fixed _check_banned reader, annotated HQ-27 Tier-3 with per-mark citations + radar gap flagged. Gates: full suite 1470 OK; catalogue 275→275 three ways (zero mint, REQ-P21-03). 21-01-SUMMARY.md written. Next: S1-4 (code review + fixes; verification passed; REQ-P21-01..03, zero-new-codes set-identity)."
last_updated: "2026-09-02T23:00Z"
last_activity: 2026-09-02
last_activity_desc: "S1-3 Phase 21 execute complete; 12 orphans homed, 5 refusal entries enriched, 275→275 zero mint; full suite 1470 OK"
progress:
  total_phases: 4
  completed_phases: 0
  total_plans: 1
  completed_plans: 1
  percent: 0
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
**Current focus:** Phase 21 — viz vocabulary reconciliation (every chart-type orphan homed to both a relationship and a capability family; banned types become first-class refusal entries) before the catalog spine lands on top of it.

## Current Position

Phase: 21 (viz-vocabulary-reconciliation) — executed (S1-3); next ledger unit is S1-4 (code review + verification)
Plan: 21-01-PLAN.md executed — 3 TDD tasks RED→GREEN→GREEN; 21-01-SUMMARY.md written
Status: Executing (Phase 21 plan executed; full suite 1470 OK; catalogue 275→275 zero mint; verification pending S1-4)
Last activity: 2026-09-02 — S1-3 execute: 12 orphans homed, 5 refusal entries enriched, REQ-P21-01..03 gate evidence green

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
