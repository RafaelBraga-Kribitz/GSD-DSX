---
gsd_state_version: 1.0
milestone: v2.4
milestone_name: Visual Excellence
current_phase: 21
current_phase_name: viz-vocabulary-reconciliation
status: executing
stopped_at: "S1-2 (Phase 21 plan) COMPLETE: 21-01-PLAN.md (1 plan, 1 wave, 3 TDD tasks RED→GREEN→GREEN). gsd-plan-checker PASSED 12/12 dimensions (opus/high); requirements coverage 3/3; decision-coverage gate 2/2 (planner added a machine-readable D-01/D-02 bullet index to 21-CONTEXT.md — the known context-coverage parser false-block, resolved legitimately; authoritative ### bodies unchanged). Research ON (21-RESEARCH.md) surfaced the input_types.json regeneration gotcha + mechanically verified zero-mint; 21-VALIDATION.md seeded (draft, Nyquist). Boundary held: did NOT auto-advance to execute despite auto_advance=true — S1-3 is a separate ceremony unit. Next: S1-3 (execute Phase 21 plans; invariant test, orphans homed, refusal entries added)."
last_updated: "2026-09-02T22:40Z"
last_activity: 2026-09-02
last_activity_desc: "S1-2 Phase 21 plan complete; plan-checker PASSED 12/12; 21-01-PLAN.md (home 12 orphans, enrich 5 refusal entries, prove 275→275)"
progress:
  total_phases: 4
  completed_phases: 0
  total_plans: 1
  completed_plans: 0
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

Phase: 21 (viz-vocabulary-reconciliation) — planned (S1-2); ready to execute; next ledger unit is S1-3 (execute)
Plan: 21-01-PLAN.md (1 plan, 1 wave, 3 TDD tasks) — plan-checker PASSED 12/12
Status: Executing (Phase 21 planned; RESEARCH + VALIDATION + PLAN written; gates green)
Last activity: 2026-09-02 — S1-2 Phase 21 plan: plan-checker PASSED 12/12, requirements 3/3, decisions 2/2

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
