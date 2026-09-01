---
gsd_state_version: 1.0
milestone: v2.3
milestone_name: Test Catalog
current_phase: 17
current_phase_name: foundation-repairs-and-spec-vocabulary
status: executing
stopped_at: "S1-4 complete (2026-09-01T22:00Z) — Phase 17 code review + verification PASSED; stopped at the ~12-min pacing cap on the S1-4 boundary. Phase 17 code work (17-01/02/03) all executed + reviewed + verified; only S1-5 (secure + validate, sign-off batched to HUMAN-QUEUE, non-blocking until S5-2) remains before Phase 17 is closed. Next unblocked unit: S1-5. S1-5 hard-blocks S2 (Phase 18) and S3 (Phase 19)."
last_updated: "2026-09-01T22:00:00Z"
last_activity: 2026-09-01
last_activity_desc: "S1-4 done — Phase 17 code review + fixes (1 LOW: missing Any import in stats.py, fixed) + verification PASSED goal-backward vs REQ-P17-01..05 (17-REVIEW.md, 17-VERIFICATION.md). scripts/check.sh all checks passed (1323 OK, catalogue current @260 set-identity). All 3 plans (17-01/02/03) executed with SUMMARY. Next: S1-5 (secure + validate phase 17, sign-off batched to HUMAN-QUEUE; hard-blocks S2/S3)."
progress:
  total_phases: 4
  completed_phases: 0
  total_plans: 3
  completed_plans: 3
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

Phase: 17 (foundation-repairs-and-spec-vocabulary) — S0 done, S1-1 discuss done, S1-2 plan done; S1-3 execute IN PROGRESS (Wave 1 of 2 complete)
Plan: 17-03 (estimand_kind vocab + DSX-STA-040 widen + fixtures/catalogue regen + zero-new-codes) is the next incomplete plan — Wave 2, now unblocked (17-01 done). `/gsd-execute-phase 17` will auto-skip 17-01/02 via has_summary.
Status: Executing — Wave 1 done (17-01 Boschloo GREEN, 17-02 fallthrough pin); resume 17-03 next firing. See phase `.continue-here.md`.
Last activity: 2026-09-01 — S1-3 Wave 1: 17-01 + 17-02 executed inline (branch-safety: init's milestone-template branch name `gsd/v2.3-test-catalog` mismatches the ceremony branch `gsd/v2.3.0-test-catalog`; never run the framework's handle_branching)

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
