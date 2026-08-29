---
gsd_state_version: 1.0
milestone: v2.2
milestone_name: Analytic Surface
current_phase: 15
current_phase_name: cuped-and-bi-declaration-checks
status: executing
stopped_at: "S4-1 COMPLETE — Phase 15 discuss; 15-CONTEXT.md written (D-01..D-09, 6 sections). Architect+Statistician 2-persona round (opus/high, §4). D-06 mint (irreversible, decided by loop, next-free-in-family): DSX-EXP-070 CRITICAL in dsx/checks/design.py (_check_cuped, keyed on variance_adjustment==cuped, reads design.cuped.covariate_timing, computes nothing; cite Deng/Xu/Kohavi/Walker 2013 WSDM) + DSX-MET-021 HIGH in dsx/checks/metrics.py (_check_cohort_denominator_shift, reads NEW results.cohort_comparisons, cite Crook 2009 KDD §6 Pitfall 4). 258→260 additive; frozen phase-12 snapshot (256) untouched. Two tie-breaks (rigour>reliability>flexibility): changing-denom family MET not INT (INT causal-gated → skips descriptive BI specs); severity HIGH not CRITICAL (declaration-only evidences shift not proven reversal; sibling MET-020 is HIGH; REQ-P15-04 block-bad-fixture met at verify/ship; the CRITICAL lean conflated REQ-P15-02's plan-block). CRITICAL RECONCILE FIND for S4-2: DSX-MET-020 already exists (reads results.period_comparisons by count) — MET-021 must read results.cohort_comparisons by definition/share, proven disjoint by test. Survivorship NOT minted (HQ-8 does-not-transfer → brief.md §6.5 + D-13 entry cond); REQ-P15-04 ships PARTIAL, REQUIREMENTS.md reword queued S4-4. No new D-05 owed (both shipping cites confirmed in answered HQ-8). Baseline re-verified (§5): gen-finding-catalogue.py --check exit 0 @ 258; EXP-070+MET-021 both free. D-06 veto filed HQ-13 (non-blocking). Also did §5 Log-archive hygiene: 5 oldest Log entries moved to LOOP-LEDGER-ARCHIVE.md. RESUME at S4-2 (Phase 15 plan; plan-checker must pass). See LOOP-LEDGER.md Log."
last_updated: "2026-08-29T04:27:00.000Z"
last_activity: 2026-08-29
last_activity_desc: "S4-1 complete — Phase 15 discuss; 15-CONTEXT.md (D-01..D-09); D-06 mint DSX-EXP-070 (CRITICAL, CUPED covariate) + DSX-MET-021 (HIGH, changing-denominator), 258→260 additive; survivorship not shipped (§6.5, D-13); D-06 veto HQ-13; resume at S4-2 (Phase 15 plan)"
progress:
  total_phases: 4
  completed_phases: 3
  total_plans: 0
  completed_plans: 0
  percent: 0
---

# Project state

**Status:** Phase 15 IN PROGRESS (S4) — **S4-1 discuss COMPLETE**: `15-CONTEXT.md` written (D-01..D-09). D-06 mint decided (loud, irreversible): **`DSX-EXP-070`** CRITICAL (CUPED post-treatment-covariate) + **`DSX-MET-021`** HIGH (changing-denominator); catalogue 258→260 additive; survivorship **not** shipped (§6.5, D-13 entry cond). D-06 veto window HQ-13 (non-blocking). Next: S4-2 (plan; plan-checker must pass).
**Progress:** [███████████████░░░░░] v2.2 — 3/4 phases complete (13, 14, 16); Phase 15 in progress (S4-1 of 5 done); order 13 → 14 → 16 → 15
**Predecessor:** [████████████████████] v2.0.0 SHIPPED 2026-08-28 — 11/11 phases, 89 plans, 208 tasks, tag `v2.1.0`, merged to `main`. Full record: `.planning/MILESTONES.md`; artifacts archived under `.planning/milestones/v2.0.0-*` (phases, ROADMAP, REQUIREMENTS, MILESTONE-AUDIT, loop ledgers).

**Locked decisions (v2.2, carried from planning):** DQ = profile runner + hermetic gates; Glyph = hermetic svg_sha256 only (no MCP dep); forbidden claims = universal pack + optional phase YAML; repro_lock = ARS-style honest-null (not byte-replay); decision replay = structured thresholds only; suppressions = ADR/SPEC authority required (unknown codes → exit 2).

## Project Reference

See: .planning/PROJECT.md (updated 2026-08-13; Key Decisions table there is the full decision log)

**Core value:** Gate analytical work on validity before the data is touched.
**Current focus:** Phase 15 — cuped-and-bi-declaration-checks (S4-1 discuss done; next S4-2 plan)

## Current Position

Phase: 15 (cuped-and-bi-declaration-checks-new-codes-d-05) — IN PROGRESS. **S4-1 discuss COMPLETE**; S4-2..S4-5 pending. Phases 13/14/16 complete.
S4-1: Architect+Statistician 2-persona round (opus/high, §4). **D-06 mint (irreversible):** `DSX-EXP-070` CRITICAL (`dsx/checks/design.py`, CUPED post-treatment covariate; cite Deng et al. 2013 WSDM) + `DSX-MET-021` HIGH (`dsx/checks/metrics.py`, changing-denominator; cite Crook 2009 KDD §6). 258→260 additive; frozen snapshot untouched. Tie-breaks (rigour): changing-denom family MET not INT (INT causal-gated); severity HIGH not CRITICAL. Survivorship NOT minted (HQ-8 does-not-transfer → §6.5+D-13); REQ-P15-04 PARTIAL, reword queued S4-4. **S4-2 trap:** `DSX-MET-020` already reads `results.period_comparisons` — MET-021 reads NEW `results.cohort_comparisons`, prove disjoint. Artifact `15-CONTEXT.md`. D-06 veto HQ-13; HQ-9/10/12 (phase security sign-offs + UAT) + HQ-11 (P16 veto) open, all non-blocking to S5-2.
Last activity: 2026-08-29 — S4-1 Phase 15 discuss complete; D-06 mint recorded loudly; resume at S4-2 (Phase 15 plan)

Progress: [██░░░░░░░░] Phase 15 — 1 of 5 ceremony steps done (discuss)

**Loop control:** the autonomous ceremony drives this milestone. Contract: `.planning/LOOP-BRIEF.md`; backlog + gates: `.planning/LOOP-LEDGER.md`; human-only items: `.planning/HUMAN-QUEUE.md`.

## Performance Metrics

No v2.2 plans executed yet. v2.0.0 velocity is archived with its milestone artifacts.

## Accumulated Context

### Decisions

Full decision log: PROJECT.md Key Decisions. v2.2-specific decisions are recorded here and in each phase's CONTEXT.md as the loop reaches them. **First codes minted this milestone: Phase 16 S3-1 (D-06) assigns `DSX-REP-060`/`DSX-REP-061` (both HIGH) for the REQ-P16-02 reproduce-report gate check** — persona round unanimous Option A; catalogue moves 256→258 additively (D-08); ROADMAP "only Phase 15 extends the catalogue" amended (D-07); veto window HQ-11. Full rationale: `16-CONTEXT.md` D-01..D-11.

Ordering (see LOOP-LEDGER "Ordering rationale"): phases run 13 → 14 → 16 → 15, not numeric order — every declared dependency still holds. Phase 15 runs last because it is the only phase minting new finding codes, hence the only one carrying a D-05 human-read gate and a D-06 irreversible-numbering veto; its citation evidence pack is filed early as HQ-8 so the operator can answer asynchronously.

### Pending Todos

None active for v2.2.

### Blockers/Concerns

None open. HQ-8 (Phase 15 D-05 citation evidence pack) is filed early and is non-blocking — it only gates close-out (S5-2).

## Deferred Items

Carried forward from v2.0.0 close (closeout_type=override_closeout) — captured future ideas, not gaps:

| Category | Item | Status | Deferred At |
|----------|------|--------|-------------|
| seed | SEED-001-deepen-dsx-explore-data-eda-protocol | dormant — carry into v2.2 | 2026-08-28 |
| seed | SEED-002-grow-data-profile-hermetic-eda-artifacts | dormant — carry into v2.2 | 2026-08-28 |

## Session Continuity

Last session: 2026-08-29T04:27Z (autonomous firing)
Stopped at: S4-1 complete — Phase 15 discuss; `15-CONTEXT.md` written (D-01..D-09). D-06 mint DSX-EXP-070 (CRITICAL) + DSX-MET-021 (HIGH), 258→260 additive; survivorship not shipped (§6.5). D-06 veto HQ-13. No new commit to code yet (discuss artifact + ledger/state/queue only).
Resume file: None — the next firing takes S4-2 from LOOP-LEDGER.md (Phase 15 plan; plan-checker must pass). **S4-2 must honour the 15-CONTEXT.md traps**, above all: (1) MET-021 reads NEW `results.cohort_comparisons` (NOT `results.period_comparisons` = the pre-existing DSX-MET-020) and must be proven disjoint by test; (2) both new checks are declaration-only (no pandas/scipy/numpy on the gate path; CUPED θ/ρ reference impl in `dsx/mathx.py`, never imported by the check); (3) additive rebaseline in `tests/test_finding_catalogue_invariant.py` only (`_EXPECTED_TOTAL` 258→260, `_MINTED_CODES` += EXP-070,MET-021; frozen snapshot `finding-codes-phase12.md` @256 NOT mutated); (4) D-05 allow-list by exact code (`_D05_ALLOWLIST_CODES`), NOT family prefix; (5) REQ-P15-01 (cuped ∈ VARIANCE_ADJUSTMENTS) lands before REQ-P15-02. Ordering: plan-checker per brief §3 = opus (override the profile's haiku checker_model).
