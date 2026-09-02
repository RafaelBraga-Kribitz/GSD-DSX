---
gsd_state_version: 1.0
milestone: v2.3
milestone_name: Test Catalog
current_phase: 20
current_phase_name: calibration-and-reporting-close
status: executing
stopped_at: "S4-3 DONE — all four Phase-20 plans landed + Wave-2 merge gate GREEN → S4-3 CHECKED. This firing (2026-09-02T13:17Z): reconciled ledger vs repo (brief §0.4) — HEAD 595b7ea == ledger's 20-A-DONE claim, branch up-to-date with origin (0/0); no correction. Executed 20-B INLINE as orchestrator (small mechanical plan; NO handle_branching, branch confirmed unchanged == gsd/v2.3.0-test-catalog). Commit 142267e (Task 1 — good fixture EXTENDED not replaced, D-08: sphericity_correction:unconditional_gg → DSX-STA-070 silent, power_reporting_type:a_priori → DSX-STA-111 silent, both in-vocab → DSX-STA-040 silent; four-code golden baseline {CLM-031,DQ-001,FIG-001,NAR-010} preserved, golden test 6/6) + commit 8af492f (Task 2 — new tests/test_phase20_zero_mint_close.py, 5 oracles: catalogue 275 / phase-12 snapshot 256-frozen-and-subset / fifteen codes in _D05_ALLOWLIST_CODES by EXACT string & DSX-STA- not a prefix / 123-onward reserve absent & max code 122 / good silent; finding-codes.md regen = no-op; gen-finding-catalogue.py UNCHANGED = allowlist a VERIFY). WAVE-2 MERGE GATE re-run by orchestrator from a clean tree: full suite Ran 1462 OK (prior 1457 + 5 new; declared-twice warnings pre-existing legacy, none Phase-20; both explain tests passed); catalogue --check current @275; validate-capability conformant; gate contract (bin/dsx, DSX_PYTHON=python) good-passes/bad-blocks at plan/execute/verify/ship + missing-spec exit 2 + audit deterministic; the four Wave-2 modules together (golden+zero-mint+doc-agreement 19 OK, known-bad-corpus 47 OK) — 20-A's golden entry still matches 20-B's extended fixture; branch confirmed gsd/v2.3.0-test-catalog. Zero codes minted this phase (catalogue 275). Trimmed the 6 oldest Log entries (S1-5..S2-4) to LOOP-LEDGER-ARCHIVE.md (brief §5 hot-path lean; ledger was 21 entries). Stopped at the S4-3 unit boundary (~12-min pacing cap; S4-4 = code review + verification is an opus/high ceremony step warranting a fresh firing per brief §1). NEXT unblocked = S4-4 (Phase 20 code review + fixes; verification passed, REQ-P20-01..04). Never handle_branching."
last_updated: "2026-09-02T13:17:00Z"
last_activity: 2026-09-02
last_activity_desc: "S4-3 DONE — Phase 20 executes complete (all four plans 20-A/B/C/D) + Wave-2 merge gate GREEN → S4-3 CHECKED. This firing executed 20-B inline (REQ-P20-02, zero-mint catalogue close): good fixture extended (not replaced, D-08) with two silent in-vocab new-family fields; new tests/test_phase20_zero_mint_close.py (5 oracles) proves catalogue stays 275, phase-12 snapshot 256-frozen, fifteen codes allowlisted by exact string, 123-onward reserve absent (max 122), good silent; finding-codes.md regen no-op; gen-finding-catalogue.py unchanged. Wave-2 merge gate from a clean tree: full suite 1462 OK, catalogue --check @275, capability conformant, gate contract good-passes/bad-blocks + missing-exit-2 + deterministic, the four Wave-2 modules 19 OK + 47 OK together (20-A golden matches 20-B extended fixture). Zero codes minted (catalogue 275). Next: S4-4 (code review + verification, REQ-P20-01..04)."
progress:
  total_phases: 4
  completed_phases: 3
  total_plans: 7
  completed_plans: 7
  percent: 75
---

# Project state

**Status:** v2.3 Test Catalog — OPEN, executing under the autonomous ceremony
**Progress:** [███████████████░░░░░] v2.3 — 3/4 phases (17 foundation ✅ → 18 correlation/agreement ✅ → 19 RM/trend/categorical/resampling/post-hoc ✅ → 20 calibration [S4-1 discuss ✅ · S4-2 plan ✅ · S4-3 execute ✅ (20-A ∥ 20-B ∥ 20-C ∥ 20-D all landed, Wave-2 merge gate GREEN, catalogue 275, zero mint) · S4-4 review ⏳ · S4-5 secure+validate ⏳])
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

Phase: 20 (calibration-and-reporting-close) — **S4-1 discuss DONE + S4-2 plan DONE + S4-3 execute IN PROGRESS (Wave 1 COMPLETE: 20-C `65a49e6` ∥ 20-D; Wave 2: 20-A ✅ this firing ∥ 20-B ⏳)**. S4-3 remaining: 20-B + the Wave-2 merge gate; then S4-4 review+verify / S4-5 secure+validate. Phase 19 CLOSED (S3-1…S3-5).
Plan: **4 plans written & checked; Wave 1 (20-C ∥ 20-D) executed (S4-3 continues with Wave 2 next)** — 20-A/B/C/D, file-disjoint single-writer across 2 waves (W1 = 20-C ✅ + 20-D ✅ structural guards `depends_on:[]` ∥ W2 = 20-A + 20-B calibration `depends_on:[20-C,20-D]`); execute INLINE on the ceremony branch, never `handle_branching`. **20-C DONE** (REQ-P20-03): no-autoswitch category-complete + fallthrough-position regression; zero codes, byte-frozen. **20-D DONE** (REQ-P20-04): new read-only `tests/test_doc_code_agreement.py` (8 tests) — Tier-1 cell-equality of all 15 Decision rows ↔ `recommend_test` (+ Boschloo fallback), Tier-2 set-membership of the six `recommend_*` mirror tables, visible skip-list + exhaustiveness (57 rows = 31 bound + 26 skip); NO divergence → `test-selection.md` + `stats.py` byte-frozen; zero codes; suite **1455 OK**, catalogue @275. Discuss settled: **D-03 load-bearing** — the 15 new Phase-18/19 codes are HIGH/verify-ship-only, so the existing CRITICAL/plan-execute `test_stratified_catch_rate_and_fpr_report` is a provable no-op on them → EXTEND the one harness with a live HIGH verify/ship stratum (read via `_gate_findings`, never `_GOLDEN_SHIP_FINDINGS` = D-09). **D-02** REQ-P20-04 = cross-check test (rows 8–24 cell-equality ↔ `recommend_test` + set-membership for the six `recommend_*` tables + skip-list), not a generated mirror. **D-04** all 15 PRESENT-caught, none ABSENT; the 5 Phase-18 codes (050/051/060/061/062) fire nowhere in examples/ → dedicated PRESENT fixtures; floor stays 3. **D-05** add good-corpus negative controls (FPR silent-not-clean on the 15). **D-06** only `_GOLDEN_SHIP_FINDINGS` moves; anchor (0.25,0.3) + floor 3 frozen. **D-07** two-wave rigour split (C+D structural guards → A+B calibration), file-disjoint single-writer. **D-01** zero-mint @275. Veto = HQ-24 (non-blocking).
Status: Executing — Phase 17 CLOSED (S1-1…S1-5); Phase 18 CLOSED (S2-1…S2-5); Phase 19 CLOSED (S3-1…S3-5); Phase 20 S4-1 + S4-2 DONE, **S4-3 IN PROGRESS (Wave 1 COMPLETE: 20-C ✅ `65a49e6` ∥ 20-D ✅; Wave 2: 20-A ✅ this firing ∥ 20-B ⏳)**; next firing runs S4-3 cont. = execute 20-B (zero-mint catalogue close, REQ-P20-02) then the Wave-2 MERGE GATE (full suite + catalogue + no-autoswitch + doc/code + calibration + zero-mint from a clean tree), then CHECK S4-3. Branch-safety unchanged: never run the framework `handle_branching` (milestone-template name `gsd/v2.3-test-catalog` mismatches the ceremony branch `gsd/v2.3.0-test-catalog`).
Last activity: 2026-09-02T13:02Z — S4-3 IN PROGRESS (Wave-2 plan 20-A DONE + orchestrator-verified, REQ-P20-01): executed 20-A via a gsd-executor on the ceremony branch (no `handle_branching`) — five Phase-18 PRESENT known-bad fixtures each fire EXACTLY {050/051/060/061/062}; three valid good-corpus controls silent, FPR denom **12→15**; the single calibration harness EXTENDED with a live HIGH verify/ship stratum (`_classify_target_defect` severity default CRITICAL; third readout read LIVE via `_gate_findings`, never `_GOLDEN_SHIP_FINDINGS` = D-09; anchor (0.25,0.3)+floor 3 unmoved); only `_GOLDEN_SHIP_FINDINGS` moved. Deviation: `inference.primary_procedure` omitted on the 8 new specs (measured — no correlation/agreement admissibility family) so each golden set = its one target code; two corpus-matrix count tests updated (disjoint from 20-B). Orchestrator gate from a clean tree: full suite **1457 OK**, catalogue `--check` @275, all 3 acceptance oracles green. Stopped clean at the 20-A boundary; 20-B + the Wave-2 merge gate remain for S4-3.

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
