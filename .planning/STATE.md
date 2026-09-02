---
gsd_state_version: 1.0
milestone: v2.3
milestone_name: Test Catalog
current_phase: 20
current_phase_name: calibration-and-reporting-close
status: executing
stopped_at: "S4-2 DONE + PUSH BACKLOG CLEARED — Phase 20 planned; plan-checker VERIFICATION PASSED (0 blockers). This firing (2026-09-02T11:28Z): network RESTORED (git ls-remote origin resolves; the 08:05Z/09:19Z github.com:443 outage is over). Reconciled ledger vs repo (brief §0.4): the 09:19Z firing COMPLETED S4-2 (4 plans 20-A/B/C/D on disk, 227/167/151/176 lines; plan-check evidence in the S4-2 checkbox + 09:19Z Log line) but could not commit/push (network down). Corrected STATE.md drift (it still read S4-1/next=S4-2 though S4-2 is done). Committed the S4-2 unit (ledger + archive trim of 7 old Log entries + 4 plans + this STATE) and PUSHED all three backlog commits to origin/gsd/v2.3.0-test-catalog: d993fe7 S3-5 + dddcd1f S4-1 + this S4-2 commit. Did NOT start S4-3 — the terminal-calibration execute (4 plans / 2 waves + catch-rate/FPR re-baseline + full-suite Wave merge gates) is too large to finish + gate in one firing's remaining context without risking mid-unit auto-compaction (brief §1 + anti-compaction rule); stopped clean at the S4-2/S4-3 boundary. NEXT unblocked = S4-3 (execute 20-C ∥ 20-D → 20-A ∥ 20-B INLINE on the ceremony branch — never handle_branching; single-writer per wave; catalogue stays 275; catch-rate/FPR readouts route opus/fable high per brief §3)."
last_updated: "2026-09-02T11:28:00Z"
last_activity: 2026-09-02
last_activity_desc: "S4-2 DONE + push backlog cleared. Network restored; committed the 09:19Z firing's completed-but-uncommitted S4-2 plan work (4 plans 20-A/B/C/D + archive trim) and pushed all three backlog commits (d993fe7 S3-5 + dddcd1f S4-1 + S4-2) to origin. Corrected stale STATE.md (read S4-1/next=S4-2 though S4-2 is done). Plan gate: gsd-plan-checker VERIFICATION PASSED, 0 blockers, REQ-P20-01…04 each covered, 4 plans file-disjoint single-writer across 2 waves (W1=C+D structural guards ∥ W2=A+B calibration). Did NOT start S4-3 (terminal-calibration execute is too large to finish+gate in one firing without mid-unit compaction risk). Next: S4-3 execute (inline, never handle_branching)."
progress:
  total_phases: 4
  completed_phases: 3
  total_plans: 7
  completed_plans: 7
  percent: 75
---

# Project state

**Status:** v2.3 Test Catalog — OPEN, executing under the autonomous ceremony
**Progress:** [███████████████░░░░░] v2.3 — 3/4 phases (17 foundation ✅ → 18 correlation/agreement ✅ → 19 RM/trend/categorical/resampling/post-hoc ✅ → 20 calibration [S4-1 discuss ✅ · S4-2 plan ✅ · S4-3 execute next])
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

Phase: 20 (calibration-and-reporting-close) — **S4-1 discuss DONE + S4-2 plan DONE** (4 plans 20-A/B/C/D, plan-checker VERIFICATION PASSED). S4-3 execute / S4-4 review+verify / S4-5 secure+validate remain. Phase 19 CLOSED (S3-1…S3-5).
Plan: **4 plans written & checked (S4-3 execute next)** — 20-A/B/C/D, file-disjoint single-writer across 2 waves (W1 = 20-C + 20-D structural guards `depends_on:[]` ∥ W2 = 20-A + 20-B calibration `depends_on:[20-C,20-D]`); execute INLINE on the ceremony branch, never `handle_branching`. Discuss settled: **D-03 load-bearing** — the 15 new Phase-18/19 codes are HIGH/verify-ship-only, so the existing CRITICAL/plan-execute `test_stratified_catch_rate_and_fpr_report` is a provable no-op on them → EXTEND the one harness with a live HIGH verify/ship stratum (read via `_gate_findings`, never `_GOLDEN_SHIP_FINDINGS` = D-09). **D-02** REQ-P20-04 = cross-check test (rows 8–24 cell-equality ↔ `recommend_test` + set-membership for the six `recommend_*` tables + skip-list), not a generated mirror. **D-04** all 15 PRESENT-caught, none ABSENT; the 5 Phase-18 codes (050/051/060/061/062) fire nowhere in examples/ → dedicated PRESENT fixtures; floor stays 3. **D-05** add good-corpus negative controls (FPR silent-not-clean on the 15). **D-06** only `_GOLDEN_SHIP_FINDINGS` moves; anchor (0.25,0.3) + floor 3 frozen. **D-07** two-wave rigour split (C+D structural guards → A+B calibration), file-disjoint single-writer. **D-01** zero-mint @275. Veto = HQ-24 (non-blocking).
Status: Executing — Phase 17 CLOSED (S1-1…S1-5); Phase 18 CLOSED (S2-1…S2-5); Phase 19 CLOSED (S3-1…S3-5); Phase 20 S4-1 + S4-2 DONE; next firing runs S4-3 (execute the 4 plans across 2 waves; catch-rate/FPR re-baseline; opus/fable high per brief §3). Branch-safety unchanged: never run the framework `handle_branching` (milestone-template name `gsd/v2.3-test-catalog` mismatches the ceremony branch `gsd/v2.3.0-test-catalog`).
Last activity: 2026-09-02T11:28Z — S4-2 DONE + push backlog cleared. Network restored; committed the 09:19Z firing's completed-but-uncommitted S4-2 plan work and **pushed all three backlog commits (`d993fe7` S3-5 + `dddcd1f` S4-1 + the S4-2 commit) to `origin`**. Corrected stale STATE.md (read S4-1/next=S4-2 though S4-2 is done).

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
