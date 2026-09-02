---
gsd_state_version: 1.0
milestone: v2.3
milestone_name: Test Catalog
current_phase: 20
current_phase_name: calibration-and-reporting-close
status: executing
stopped_at: "S4-3 IN PROGRESS — Wave 2 plan 20-A of 2 DONE + orchestrator-verified. This firing (2026-09-02T13:02Z): reconciled ledger vs repo (brief §0.4) — HEAD e5f1b5b == Wave-1-COMPLETE claim, branch up-to-date with origin (0/0), on ceremony branch; no correction. Executed 20-A via a gsd-executor (adaptive, §3) — NO handle_branching, execute-plan only, branch confirmed before/after == gsd/v2.3.0-test-catalog by executor AND me (HQ branch-safety rule). Commits 23e21e9 (five Phase-18 PRESENT known-bad fixtures + measured re-baseline) / 849897a (three valid good-corpus controls + FPR-disjointness guard) / d57e401 (live HIGH verify/ship calibration stratum + corpus-matrix maintenance) / aeae4cb (SUMMARY). GATE RE-RUN BY ORCHESTRATOR from a clean tree (not trusted from subagent; stray DECISIONS.jsonl cleared): full suite Ran 1457 OK (1455 + 2 calibration tests); catalogue --check current @275; all THREE 20-A acceptance oracles green by me — (1) the five Phase-18 fixtures each fire EXACTLY {050/051/060/061/062} as clean singletons; (2) three valid controls silent (frozenset()), FPR denom 12→15, _FPR_TEMPDIR_NOISE_CODES disjoint from DSX-STA; (3) _classify_target_defect severity default CRITICAL, anchor (0.25,0.3)+floor 3 UNMOVED, HIGH-stratum source verified NOT to read _GOLDEN_SHIP_FINDINGS (D-09). Two deviations scrutinised+accepted: (a) inference.primary_procedure omitted on all 8 new specs (a MEASURED deviation — families.yaml has no correlation/agreement admissibility family so keeping it drew spurious DSX-ADM-020 / DSX-PRE-030; omission makes admissibility not_declared so each golden set = its ONE target code); (b) two corpus-matrix count tests (test_dsx.py 14→19, test_frame_val.py _EXPECTED_VAL_CODES) updated as a fixture-count consequence, disjoint from 20-B's single-writer set. Production dsx/+scripts/+references/ + both canonical fixtures BYTE-FROZEN. S4-3 NOT checked (atomic; 20-B + Wave-2 merge gate remain). Stopped clean at the 20-A per-plan boundary (executor was ~314k tokens/~31min wall, well past the ~12-min pacing cap; 20-B + the merge gate warrant a fresh firing per the anti-compaction rule). NEXT unblocked = S4-3 cont.: execute 20-B (extend examples/good-ANALYSIS-SPEC.yaml with silent in-vocab sphericity_correction:unconditional_gg + power_reporting_type:a_priori, preserve its 4-code golden baseline; new tests/test_phase20_zero_mint_close.py; no-op regen references/finding-codes.md @275; verify 15 codes allowlisted by exact string + 123-onward reserve absent), then the Wave-2 merge gate, then CHECK S4-3. Never handle_branching."
last_updated: "2026-09-02T13:02:00Z"
last_activity: 2026-09-02
last_activity_desc: "S4-3 IN PROGRESS — Wave-2 plan 20-A DONE + orchestrator-verified (REQ-P20-01, the load-bearing D-03 calibration harness extension). Executed 20-A via a gsd-executor on the ceremony branch (no handle_branching): five Phase-18 PRESENT known-bad fixtures each fire EXACTLY {050/051/060/061/062}; three valid good-corpus controls silent, FPR denom 12→15; the SINGLE calibration harness EXTENDED with a live HIGH verify/ship stratum (_classify_target_defect severity default CRITICAL; third readout read LIVE via _gate_findings, never _GOLDEN_SHIP_FINDINGS = D-09; anchor (0.25,0.3)+floor 3 unmoved); only _GOLDEN_SHIP_FINDINGS moved (8 measured keys). Deviation: inference.primary_procedure omitted on the 8 new specs (measured — no correlation/agreement admissibility family) so each golden set = its one target code. Orchestrator gate from a clean tree: full suite 1457 OK, catalogue --check @275, all 3 acceptance oracles green. Stopped at the 20-A boundary; 20-B (zero-mint close) + the Wave-2 merge gate remain for S4-3."
progress:
  total_phases: 4
  completed_phases: 3
  total_plans: 7
  completed_plans: 7
  percent: 75
---

# Project state

**Status:** v2.3 Test Catalog — OPEN, executing under the autonomous ceremony
**Progress:** [███████████████░░░░░] v2.3 — 3/4 phases (17 foundation ✅ → 18 correlation/agreement ✅ → 19 RM/trend/categorical/resampling/post-hoc ✅ → 20 calibration [S4-1 discuss ✅ · S4-2 plan ✅ · S4-3 execute IN PROGRESS: Wave 1 COMPLETE (20-C ✅ ∥ 20-D ✅), Wave 2 (20-A ✅ ∥ 20-B ⏳); merge gate pending])
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
