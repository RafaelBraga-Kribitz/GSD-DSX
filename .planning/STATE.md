---
gsd_state_version: 1.0
milestone: v2.3
milestone_name: Test Catalog
current_phase: 20
current_phase_name: calibration-and-reporting-close
status: executing
stopped_at: "S5-3 DONE — `/gsd-extract-learnings` (close-out S5). This firing (2026-09-02T16:49Z): reconciled ledger vs repo (brief §0.4) — HEAD ad48b2e == ledger's S5-1-DONE claim, branch up-to-date with origin; no correction. Ran extract-learnings for all 4 phases via 4 file-disjoint sonnet subagents (one per phase dir; LEARNINGS.md is not a single-writer tracking file): 17-LEARNINGS.md (9 dec/5 les/6 pat/4 sur = 24), 18-LEARNINGS.md (9/5/6/4 = 24), 19-LEARNINGS.md (10/6/7/5 = 28), 20-LEARNINGS.md (9/7/7/6 = 29) = 105 items. Orchestrator gate re-run per brief rigour bar (gate re-run by orchestrator, not trusted from subagent report): all 4 files exist; every frontmatter count == actual ###-item count per ## section (no drift); every cited DSX-STA-### code + test-name grounded in that phase's source artifacts (zero UNGROUNDED). Stopped at the S5-3 boundary (pacing cap). NEXT headless-runnable = S5-4 (`/gsd-audit-milestone` — must reach passed; hand-verify its output per v2.2 note). S5-2 (4 operator security sign-offs HQ-19/21/23/25 — §4 human read, loop may NOT self-sign), S5-5 (complete-milestone — interactive, NOT headless-safe), S5-6 (ship — outward-facing) all remain human-gated. Never handle_branching."
last_updated: "2026-09-02T16:49:00Z"
last_activity: 2026-09-02
last_activity_desc: "S5-3 DONE — /gsd-extract-learnings: 4 per-phase LEARNINGS.md (17: 24 items, 18: 24, 19: 28, 20: 29 = 105) via 4 file-disjoint sonnet subagents. Orchestrator gate: every frontmatter count == actual ###-item count per section; every cited DSX-STA code + test-name grounded in source artifacts (zero UNGROUNDED). S5-1 (/gsd-audit-uat, 4/4 phases PASSED) + S5-3 both done. Next headless-runnable = S5-4 (/gsd-audit-milestone, must reach passed). S5-2 (4 operator security sign-offs HQ-19/21/23/25), S5-5 (complete-milestone, interactive), S5-6 (ship) are human-gated."
progress:
  total_phases: 4
  completed_phases: 4
  total_plans: 7
  completed_plans: 7
  percent: 90
---

# Project state

**Status:** v2.3 Test Catalog — OPEN, in **close-out (S5)** under the autonomous ceremony (all four phases complete)
**Progress:** [██████████████████░░] v2.3 — 4/4 phases complete → close-out S5 (17 foundation ✅ → 18 correlation/agreement ✅ → 19 RM/trend/categorical/resampling/post-hoc ✅ → 20 calibration ✅ CLOSED [S4-1 discuss ✅ · S4-2 plan ✅ · S4-3 execute ✅ (catalogue 275, zero mint) · S4-4 review+verify ✅ (PASSED, suite 1462 OK) · S4-5 secure+validate ✅ (21 threats threats_open:0; 4/4 reqs nyquist_compliant:true)]) · **S5 close-out remains: S5-1 audit-uat ⏳ · S5-2 drain HUMAN-QUEUE · S5-3 extract-learnings · S5-4 audit-milestone · S5-5 complete-milestone (interactive) · S5-6 ship (operator-approved merge+tag)**
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

Phase: 20 (calibration-and-reporting-close) — **S4-1 discuss ✅ + S4-2 plan ✅ + S4-3 execute ✅ (all four plans + Wave-2 merge gate GREEN, catalogue 275) + S4-4 review+verify ✅ (1 LOW fixed, verification PASSED, suite 1462 OK)**. Remaining: **S4-5 secure+validate** (then Phase 20 CLOSED → S5 close-out). Phase 19 CLOSED (S3-1…S3-5).
Plan: **4 plans written & checked; Wave 1 (20-C ∥ 20-D) executed (S4-3 continues with Wave 2 next)** — 20-A/B/C/D, file-disjoint single-writer across 2 waves (W1 = 20-C ✅ + 20-D ✅ structural guards `depends_on:[]` ∥ W2 = 20-A + 20-B calibration `depends_on:[20-C,20-D]`); execute INLINE on the ceremony branch, never `handle_branching`. **20-C DONE** (REQ-P20-03): no-autoswitch category-complete + fallthrough-position regression; zero codes, byte-frozen. **20-D DONE** (REQ-P20-04): new read-only `tests/test_doc_code_agreement.py` (8 tests) — Tier-1 cell-equality of all 15 Decision rows ↔ `recommend_test` (+ Boschloo fallback), Tier-2 set-membership of the six `recommend_*` mirror tables, visible skip-list + exhaustiveness (57 rows = 31 bound + 26 skip); NO divergence → `test-selection.md` + `stats.py` byte-frozen; zero codes; suite **1455 OK**, catalogue @275. Discuss settled: **D-03 load-bearing** — the 15 new Phase-18/19 codes are HIGH/verify-ship-only, so the existing CRITICAL/plan-execute `test_stratified_catch_rate_and_fpr_report` is a provable no-op on them → EXTEND the one harness with a live HIGH verify/ship stratum (read via `_gate_findings`, never `_GOLDEN_SHIP_FINDINGS` = D-09). **D-02** REQ-P20-04 = cross-check test (rows 8–24 cell-equality ↔ `recommend_test` + set-membership for the six `recommend_*` tables + skip-list), not a generated mirror. **D-04** all 15 PRESENT-caught, none ABSENT; the 5 Phase-18 codes (050/051/060/061/062) fire nowhere in examples/ → dedicated PRESENT fixtures; floor stays 3. **D-05** add good-corpus negative controls (FPR silent-not-clean on the 15). **D-06** only `_GOLDEN_SHIP_FINDINGS` moves; anchor (0.25,0.3) + floor 3 frozen. **D-07** two-wave rigour split (C+D structural guards → A+B calibration), file-disjoint single-writer. **D-01** zero-mint @275. Veto = HQ-24 (non-blocking).
Status: Executing — Phase 17 CLOSED (S1-1…S1-5); Phase 18 CLOSED (S2-1…S2-5); Phase 19 CLOSED (S3-1…S3-5); Phase 20 S4-1 + S4-2 + S4-3 + **S4-4 DONE** (review+verify PASSED); next firing runs **S4-5** (`/gsd-secure-phase 20` + `/gsd-validate-phase 20`; sign-off batched to HUMAN-QUEUE), which closes Phase 20 → S5 close-out (audit-uat → drain HUMAN-QUEUE → extract-learnings → audit-milestone → complete-milestone → ship). Branch-safety unchanged: never run the framework `handle_branching` (milestone-template name `gsd/v2.3-test-catalog` mismatches the ceremony branch `gsd/v2.3.0-test-catalog`).
Last activity: 2026-09-02T13:30Z — S4-4 DONE (Phase 20 code review + fix + verification PASSED, REQ-P20-01..04): reviewed the tests/fixtures-only execute diff (production+catalogue byte-frozen, zero-mint); one LOW finding (dead `dist_key` local in test_doc_code_agreement.py) FIXED; six adversarial false-pass probes cleared; goal-backward verification PASSED all 4 reqs. Orchestrator gate from a clean tree: full suite **1462 OK**, targeted Phase-20 oracles 77 OK, catalogue `--check` @275, `git diff -- dsx scripts references` empty. Stopped at the S4-4 boundary; S4-5 (secure+validate) remains to close Phase 20.

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
