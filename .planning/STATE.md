---
gsd_state_version: 1.0
milestone: v2.3
milestone_name: Test Catalog
current_phase: 18
current_phase_name: correlation-association-and-agreement
status: executing
stopped_at: "S2-2 IN PROGRESS — plan preflight done (2026-09-01T23:26Z). gsd-phase-researcher (sonnet) → 18-RESEARCH.md committed 4e531df/pushed (all live locators verified; surfaced the _D05_ALLOWLIST_CODES by-exact-name gap, the gate-split-for-citation-docstrings pattern, the weights string-OR-matrix branch, and 3 open field-shape decisions for the planner). 18-VALIDATION.md seeded from RESEARCH §Validation Architecture (stdlib unittest; REQ-P18-01…06 oracle map; catalogue 260→265; D-07 pinned vs catalog-only). init now reports has_research:true, has_plans:false. Stopped at the GSD-native resumable boundary (~12-min pacing cap). S2-2 NOT checked — gate is plan-checker pass. NEXT firing: gsd-planner (opus) → gsd-plan-checker (haiku) revision loop → check S2-2 (single-writer D-08 waves: 18-A routing+gates+doc/catalogue lockstep ∥ 18-B effect-size convention bands)."
last_updated: "2026-09-01T23:26:00Z"
last_activity: 2026-09-01
last_activity_desc: "S2-2 plan preflight — 18-RESEARCH.md (gsd-phase-researcher, sonnet) + 18-VALIDATION.md seeded. Live locators verified; _D05_ALLOWLIST_CODES by-exact-name gap + 3 planner Open Questions surfaced. Next: gsd-planner → gsd-plan-checker (S2-2 plan; gate = checker pass)."
progress:
  total_phases: 4
  completed_phases: 1
  total_plans: 3
  completed_plans: 3
  percent: 25
---

# Project state

**Status:** v2.3 Test Catalog — OPEN, executing under the autonomous ceremony
**Progress:** [░░░░░░░░░░░░░░░░░░░░] v2.3 — 0/4 phases (17 foundation → 18 correlation/agreement → 19 RM/trend/categorical/resampling/post-hoc → 20 calibration)
**Predecessors:** v2.2 Analytic Surface SHIPPED 2026-08-29 (tag `v2.2.0`); v2.0.0 DSX Validity Frame SHIPPED 2026-08-28 (tag `v2.1.0`). Archives under `.planning/milestones/`.

**Loop control:** the autonomous ceremony drives this milestone. Contract:
`.planning/LOOP-BRIEF.md`; backlog + gates: `.planning/LOOP-LEDGER.md`; human-only
items: `.planning/HUMAN-QUEUE.md`. Branch `gsd/v2.3.0-test-catalog`, ships as tag
`v2.3.0` by explicit named merge (never the auto-detected branch).

**Usage-limit posture (operator-directed 2026-08-29):** the weekly token allowance
is expected to exhaust this week. The firing wrapper (`scripts/run-ceremony-firing.ps1`)
detects limit hits, backs off gracefully, and resumes by itself at the weekly reset
(Wednesday 10:00 América/São_Paulo = 13:00 UTC). Firings must not retry in a loop —
log one line and stop; the wrapper owns the pacing.

## Project Reference

See: .planning/PROJECT.md (updated 2026-08-29; Key Decisions table there is the full decision log)

**Core value:** Gate analytical work on validity before the data is touched.
**Current focus:** Phase 18 — correlation, association and agreement rows (keyed on DECLARED `estimand_kind`) + two new declaration-only gates (correlation scale/kind match; agreement declaration completeness) + effect-size convention bands. Phase 17 foundation is CLOSED.

## Current Position

Phase: 18 (correlation-association-and-agreement) — S2-1 discuss DONE; S2-2 plan IN PROGRESS (preflight done).
Plan: not yet written. S2-2 preflight complete — 18-RESEARCH.md (4e531df) + 18-VALIDATION.md seeded. NEXT firing: gsd-planner (opus) → gsd-plan-checker (haiku) revision loop → check S2-2 (plan-checker must pass). D-08 single-writer wave split decided (Plan 18-A routing+gates+doc/catalogue lockstep ∥ Plan 18-B effect-size convention bands).
Status: Executing — Phase 17 CLOSED (S1-1…S1-5); Phase 18 discuss complete + plan preflight done; next firing runs the planner→checker loop.
Last activity: 2026-09-01 — S2-2 plan preflight: gsd-phase-researcher (sonnet) → 18-RESEARCH.md; 18-VALIDATION.md seeded. Research surfaced the `_D05_ALLOWLIST_CODES` by-exact-name build-gate gap (prefix `DSX-STA-` not allowlisted), the citation-docstring gate-split pattern, the weights string-OR-matrix branch, and 3 open field-shape decisions for the planner. Branch-safety unchanged: init's milestone-template branch name `gsd/v2.3-test-catalog` mismatches the ceremony branch `gsd/v2.3.0-test-catalog` — never run the framework's handle_branching; execute inline on the ceremony branch.

## Performance Metrics

No v2.3 plans executed yet. v2.2 and v2.0.0 velocity are archived with their milestone artifacts.

## Accumulated Context

### Decisions

Full decision log: PROJECT.md Key Decisions. Standing v2.3 decisions (operator-directed at open, 2026-08-29):

- **Two sequential milestones, tests first** (v2.3 tests → v2.4 visual excellence) — both subjects write the same single-writer files and D-06 makes range collisions permanent; tests carry the heavier D-05 burden (~15–20 reads vs ~8–12) and start with mandatory repairs. Contingency: v2.4 splits into v2.4+v2.5 if v2.3's D-05 queue outruns cadence.
- **Citation granularity:** human D-05 read per new CODE; bibliographic citation per catalog ENTRY. Without this ruling the read burden triples to 90+.
- **The gate stays declaration-only** — the decision-table expansion is routing surface (`recommend_test` + references), not a per-test gate catalog; `families.yaml` stays the admissibility ontology.

### Pending Todos

None beyond the ledger.

### Blockers/Concerns

Weekly usage limit expected to hit this week — handled by wrapper backoff (see
Usage-limit posture above). Not a work blocker; a pacing fact.

## Deferred Items

Carried forward from v2.0.0 close — captured future ideas, not gaps:

| Category | Item | Status | Deferred At |
|----------|------|--------|-------------|
| seed | SEED-001-deepen-dsx-explore-data-eda-protocol | dormant — natural v2.4/v2.5 candidate | 2026-08-28 |
| seed | SEED-002-grow-data-profile-hermetic-eda-artifacts | dormant — natural v2.4/v2.5 candidate | 2026-08-28 |

## Session Continuity

Last session: 2026-08-29 (interactive session — v2.2 ship + v2.3 open)
Stopped at: v2.3 fully scoped and the ceremony repointed; no ledger unit attempted yet.
Resume file: None — the next firing takes S0-1 from LOOP-LEDGER.md.
