---
gsd_state_version: 1.0
milestone: v2.3
milestone_name: Test Catalog
current_phase: 18
current_phase_name: correlation-association-and-agreement
status: executing
stopped_at: "S2-4 DONE — Phase 18 code review + fixes + verification PASSED (2026-09-02T02:31Z). Run inline by the orchestrator (opus/high, brief §3); branch confirmed, framework handle_branching NOT run. Read the full a266a9b..HEAD source diff (1003 insertions / 12 files). One LOW finding (18-REVIEW.md): CORRELATION_FAMILY vs _ASSOCIATION_ROUTES-union drift risk (comment claimed 'cannot drift', unenforced) → FIXED with an invariant test (test-only, mints no code). Three suspected defects adversarially probed + cleared (is_blank(0.0)=False → no p_pos=0.0 false-fire; normalize() str()-first tolerates non-string icc; DSX-STA-012 seam branch correct + inert-safe). 18-VERIFICATION.md = PASSED all 6 reqs goal-backward. GATE RE-RUN BY ORCHESTRATOR from a clean tree: full suite Ran 1367 OK (1366 + the 1 invariant test); catalogue --check exit 0 at 265 (5 codes each once); no-autoswitch test green; seam oracle RUNS (not skipped) + passes. Stopped at the S2-4 boundary (~12-min cap; S2-5 is a distinct secure+validate multi-step unit). NEXT firing: S2-5 — /gsd-secure-phase 18 + /gsd-validate-phase 18; sign-off batched to HUMAN-QUEUE."
last_updated: "2026-09-02T02:31:00Z"
last_activity: 2026-09-02
last_activity_desc: "S2-4 DONE — Phase 18 code review + verification PASSED (18-REVIEW.md 1 LOW finding fixed; 18-VERIFICATION.md all 6 reqs goal-backward). Gate re-run by orchestrator: full suite 1367 OK, catalogue 265, seam oracle live. Next: S2-5 secure + validate."
progress:
  total_phases: 4
  completed_phases: 1
  total_plans: 5
  completed_plans: 5
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

Phase: 18 (correlation-association-and-agreement) — S2-1 discuss / S2-2 plan / S2-3 execute / S2-4 review+verify all DONE. Only S2-5 (secure + validate) remains to close the phase.
Plan: 2 plans executed (18-A routing+gates+doc/catalogue lockstep ∥ 18-B effect-size convention bands); Wave-1 merge gate GREEN; code review PASS (1 LOW finding fixed) + verification PASSED all 6 reqs. Catalogue 265, full suite 1367 OK. NEXT firing: S2-5 — /gsd-secure-phase 18 + /gsd-validate-phase 18; end-of-phase security sign-off + UAT batched to HUMAN-QUEUE (non-blocking until S5-2), then Phase 18 CLOSES and S3-1 (Phase 19 discuss) unblocks.
Status: Executing — Phase 17 CLOSED (S1-1…S1-5); Phase 18 S2-1…S2-4 DONE; next firing runs S2-5 to close Phase 18.
Last activity: 2026-09-02 — S2-4 DONE: read the full a266a9b..HEAD source diff inline (opus/high); 18-REVIEW.md one LOW finding (CORRELATION_FAMILY drift risk) FIXED with an invariant test + three suspected defects adversarially cleared; 18-VERIFICATION.md PASSED all 6 reqs goal-backward; gate re-run by orchestrator from a clean tree (full suite 1367 OK, catalogue 265, seam oracle live). Branch-safety unchanged: never run the framework's handle_branching (milestone-template name `gsd/v2.3-test-catalog` mismatches the ceremony branch `gsd/v2.3.0-test-catalog`).

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
