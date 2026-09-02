---
gsd_state_version: 1.0
milestone: v2.3
milestone_name: Test Catalog
current_phase: 20
current_phase_name: calibration-and-reporting-close
status: executing
stopped_at: "S4-1 DONE — Phase 20 discuss (light), run inline by the orchestrator (opus/high) on gsd/v2.3.0-test-catalog (branch confirmed; framework handle_branching NOT run — discuss doesn't switch branches). Phase 19 CLOSED (S3-1…S3-5) → Phase 20 is the terminal calibration + reporting close (REQ-P20-01…04). Reconciled ledger vs repo: HEAD d993fe7 == ledger S3-5-DONE / Phase-19-CLOSED; STATE.md was stale (still Phase-19 S3-3) — REFRESHED this firing. §4 persona round Architect + Statistician (opus/high, concurrent; Auditor lens folded into Statistician); first Statistician spawn returned 0 file reads → discarded + re-run. 20-CONTEXT.md written, 8 decisions + 1 named deferral. LOAD-BEARING (D-03), both personas live-verified: all 15 new Phase-18/19 codes are HIGH and stats runs only at verify/ship, so the existing test_stratified_catch_rate_and_fpr_report (CRITICAL/plan-execute only) is a PROVABLE NO-OP on them → the real REQ-P20-01 deliverable is EXTENDING the one harness with a live HIGH verify/ship stratum (read via _gate_findings, never _GOLDEN_SHIP_FINDINGS = D-09), not a re-run/sibling. D-02 REQ-P20-04 = cross-check test not generated mirror. D-01 zero-mint (catalogue 275). D-04 all 15 PRESENT-caught none ABSENT; 5 Phase-18 codes need dedicated fixtures. D-05 add good-corpus negative controls (FPR silent-not-clean). D-06 only _GOLDEN_SHIP_FINDINGS moves; anchor (0.25,0.3)+floor 3 frozen. D-07 two-wave rigour split. Veto = HQ-24. PUSH still failing (github.com unreachable — network down, not rate-limit; d993fe7 + this commit local-only). NEXT unblocked = S4-2 (Phase 20 plan; plan-checker must pass; single-writer waves per D-07)."
last_updated: "2026-09-02T08:32:00Z"
last_activity: 2026-09-02
last_activity_desc: "S4-1 DONE — Phase 20 discuss (light, opus/high, inline). Architect + Statistician persona round (Auditor folded in). 20-CONTEXT.md: 8 decisions + D-13-a deferral. Load-bearing D-03: the 15 new codes are HIGH/verify-ship-only → the existing CRITICAL/plan-execute calibration is a provable no-op on them → EXTEND the harness with a live HIGH verify/ship stratum (never read _GOLDEN_SHIP_FINDINGS). D-02 REQ-P20-04 = cross-check test. D-01 zero-mint @275. D-04 all 15 PRESENT-caught; 5 Phase-18 codes need dedicated fixtures. D-05 add FPR negative controls. Veto = HQ-24 (non-blocking). Push failing (network down); commits local-only. Next: S4-2 plan."
progress:
  total_phases: 4
  completed_phases: 3
  total_plans: 7
  completed_plans: 7
  percent: 75
---

# Project state

**Status:** v2.3 Test Catalog — OPEN, executing under the autonomous ceremony
**Progress:** [███████████████░░░░░] v2.3 — 3/4 phases (17 foundation ✅ → 18 correlation/agreement ✅ → 19 RM/trend/categorical/resampling/post-hoc ✅ → 20 calibration [S4-1 discuss ✅])
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
**Current focus:** Phase 20 — the terminal calibration + reporting close (REQ-P20-01…04): known-bad fixtures for every new blocking code, the stratified catch-rate/FPR re-measured, and the REQ-P20-04 doc/code agreement test. Phases 17/18/19 are CLOSED (15 codes minted, catalogue @275). Phase 20 mints ZERO codes.

## Current Position

Phase: 20 (calibration-and-reporting-close) — **S4-1 discuss DONE** (20-CONTEXT.md, 8 decisions + D-13-a deferral). S4-2 plan / S4-3 execute / S4-4 review+verify / S4-5 secure+validate remain. Phase 19 CLOSED (S3-1…S3-5).
Plan: none yet (S4-2 next). Discuss settled: **D-03 load-bearing** — the 15 new Phase-18/19 codes are HIGH/verify-ship-only, so the existing CRITICAL/plan-execute `test_stratified_catch_rate_and_fpr_report` is a provable no-op on them → EXTEND the one harness with a live HIGH verify/ship stratum (read via `_gate_findings`, never `_GOLDEN_SHIP_FINDINGS` = D-09). **D-02** REQ-P20-04 = cross-check test (rows 8–24 cell-equality ↔ `recommend_test` + set-membership for the six `recommend_*` tables + skip-list), not a generated mirror. **D-04** all 15 PRESENT-caught, none ABSENT; the 5 Phase-18 codes (050/051/060/061/062) fire nowhere in examples/ → dedicated PRESENT fixtures; floor stays 3. **D-05** add good-corpus negative controls (FPR silent-not-clean on the 15). **D-06** only `_GOLDEN_SHIP_FINDINGS` moves; anchor (0.25,0.3) + floor 3 frozen. **D-07** two-wave rigour split (C+D structural guards → A+B calibration), file-disjoint single-writer. **D-01** zero-mint @275. Veto = HQ-24 (non-blocking).
Status: Executing — Phase 17 CLOSED (S1-1…S1-5); Phase 18 CLOSED (S2-1…S2-5); Phase 19 CLOSED (S3-1…S3-5); Phase 20 S4-1 DONE; next firing runs S4-2 (plan; plan-checker must pass). Branch-safety unchanged: never run the framework `handle_branching` (milestone-template name `gsd/v2.3-test-catalog` mismatches the ceremony branch `gsd/v2.3.0-test-catalog`).
Last activity: 2026-09-02 — S4-1 DONE: Architect + Statistician persona round (opus/high, concurrent; Auditor folded in) → 20-CONTEXT.md. Load-bearing D-03 (15 HIGH codes invisible to the current CRITICAL calibration → HIGH-stratum extension needed). **Push failing this firing (github.com unreachable — network down, not a rate-limit); d993fe7 + the S4-1 commit are LOCAL-ONLY, unpushed.**

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
