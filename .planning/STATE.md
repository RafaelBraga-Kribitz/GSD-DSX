---
gsd_state_version: 1.0
milestone: v2.3
milestone_name: Test Catalog
current_phase: 17
current_phase_name: foundation-repairs-and-spec-vocabulary
status: executing
stopped_at: "Milestone opened 2026-08-29 by operator direction (interactive session). Scope researched (6-agent workflow) and written: .planning/research/V2.3-V2.4-SCOPE.md; REQUIREMENTS.md REQ-P17-01..REQ-P20-04; ROADMAP.md Phases 17-20. Loop repointed: branch gsd/v2.3.0-test-catalog, LOOP-BRIEF/LOOP-LEDGER/HUMAN-QUEUE rewritten for v2.3, firing script updated (branch + usage-limit backoff). Next: the loop's S0-1 (verify state + scope recheck)."
last_updated: "2026-08-30T00:20:53.743Z"
last_activity: 2026-08-30
last_activity_desc: "S1-2 Phase 17 planning complete — 3 plans (17-01 Boschloo, 17-02 fallthrough pin + disposition/range verify, 17-03 estimand_kind vocab + guard + zero-new-codes); gsd-plan-checker VERIFICATION PASSED; dsx plan:post gate clean spec-less (exit 0)"
progress:
  total_phases: 4
  completed_phases: 0
  total_plans: 3
  completed_plans: 0
  percent: 0
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
**Current focus:** Phase 17 — foundation repairs (Boschloo doc/code reconciliation, `estimand_kind` vocabulary, D-12a dispositions, D-06 range pre-allocation) before any catalog row lands.

## Current Position

Phase: 17 (foundation-repairs-and-spec-vocabulary) — S0 bootstrap done, S1-1 discuss done; next ledger unit is S1-2 (plan)
Plan: — (S1-2 will create 17-PLAN via /gsd-plan-phase; plan-checker must pass)
Status: Executing — discuss complete (17-CONTEXT.md), planning next
Last activity: 2026-08-29 — S1-1 Phase 17 discuss: estimand_kind vocab, D-12a dispositions, D-06 range pre-allocation settled

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
