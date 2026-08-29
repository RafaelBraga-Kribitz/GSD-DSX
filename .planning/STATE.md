---
gsd_state_version: 1.0
milestone: v2.2
milestone_name: Analytic Surface
current_phase: 15
current_phase_name: cuped-and-bi-declaration-checks
status: executing
stopped_at: "S4-5 COMPLETE — Phase 15 secure + validate, both PASS; S4 (Phase 15) fully complete → all four milestone phases (13,14,16,15) done. SECURE = SECURED, threats_open: 0 (23-entry register from the 6 plans' threat_model blocks = 22 threats + 1 SC-accept; 1 critical + 14 high + 7 medium; asvs1 L1 short-circuit, orchestrator re-gate — not auditor-trusted). VALIDATE = nyquist_compliant: true, 0 gaps (7/7 REQ-P15-01..07 COVERED; P15-04 PARTIAL consented at S4-1 via HQ-8). Loud op-decision (S3-5 precedent): crystallised phase-scoped coverage anchor tests/test_phase15_bi_checks.py (20 tests). RECONCILE FIND: first full-suite run showed 2 failures in CWD-non-isolating explain tests (test_dsx::test_explain_missing_spec_exits_zero_not_two, test_explain_self_reported::test_returns_zero_when_spec_cannot_be_loaded) — root-caused to a stray gitignored root DECISIONS.jsonl left by a prior firing's dsx run; NOT a P15 defect, not committed; proven clean by moving the 4 gitignored ledgers aside (tests pass) + check.sh runs the suite before its gate regenerates the ledger. Removed the 4 gitignored ledgers (routine env cleanup); standing note + rm fix steps added to HUMAN-QUEUE. Re-gate: --check exit 0 @260; invariant 2 OK (260 + set-identity vs snapshot∪{REP-060,061,EXP-070,MET-021}); frozen snapshot byte-unchanged; test_cuped 8 OK (gate-plan 0→1, EXP-070 CRITICAL); test_cohort_denominator 7 OK (MET-021 HIGH, disjoint from MET-020); gate-path modules import no pandas/scipy/numpy; both codes cite HQ-8-confirmed sources. Full suite: sh scripts/check.sh all passed, Ran 1312 tests OK (1292→+20) on a clean tree. Phase-15 security sign-off + UAT queued HQ-14 (non-blocking to S5-2); D-06 veto stays HQ-13. Artifacts: 15-SECURITY.md, 15-VALIDATION.md, tests/test_phase15_bi_checks.py. RESUME at S5-1 (/gsd-audit-uat cross-phase sweep — hand-cross-check each VERIFICATION.md, CLI under-reports; do NOT accept 'All Clear'). See LOOP-LEDGER.md Log."
last_updated: "2026-08-29T15:05:00.000Z"
last_activity: 2026-08-29
last_activity_desc: "S4-5 complete — Phase 15 secure (SECURED, threats_open:0) + validate (nyquist_compliant, 7/7 COVERED); S4 fully complete, all 4 phases done; full suite Ran 1312 tests OK (clean tree); reconciled 2 explain-test failures to gitignored DECISIONS.jsonl pollution (not a defect); resume at S5-1 close-out"
progress:
  total_phases: 4
  completed_phases: 4
  total_plans: 6
  completed_plans: 6
  percent: 95
---

# Project state

**Status:** Phase 15 COMPLETE (S4-1..S4-5) — **all four milestone phases (13,14,16,15) done; now in S5 close-out.** S4-5: secure = **SECURED** `threats_open:0` (23/23 closed, asvs1 L1 short-circuit, orchestrator re-gate); validate = **nyquist_compliant:true** 0 gaps (7/7 REQ-P15-01..07 COVERED, P15-04 PARTIAL consented). Coverage anchor `tests/test_phase15_bi_checks.py` (20 tests) crystallised. Reconcile find: 2 `explain` full-suite failures root-caused to a stray gitignored root `DECISIONS.jsonl` (CWD-isolation gap, not a P15 defect, not committed) — removed the 4 gitignored ledgers, standing note added to HUMAN-QUEUE. Full suite `sh scripts/check.sh` all passed, **Ran 1312 tests OK** (1292→+20) on a clean tree. Phase-15 security sign-off + UAT queued HQ-14; D-06 veto HQ-13. Next: **S5-1** (`/gsd-audit-uat`).
**Progress:** [███████████████████░] v2.2 — 4/4 phase ceremonies complete (13, 14, 16, 15); S5 close-out pending; order 13 → 14 → 16 → 15
**Predecessor:** [████████████████████] v2.0.0 SHIPPED 2026-08-28 — 11/11 phases, 89 plans, 208 tasks, tag `v2.1.0`, merged to `main`. Full record: `.planning/MILESTONES.md`; artifacts archived under `.planning/milestones/v2.0.0-*` (phases, ROADMAP, REQUIREMENTS, MILESTONE-AUDIT, loop ledgers).

**Locked decisions (v2.2, carried from planning):** DQ = profile runner + hermetic gates; Glyph = hermetic svg_sha256 only (no MCP dep); forbidden claims = universal pack + optional phase YAML; repro_lock = ARS-style honest-null (not byte-replay); decision replay = structured thresholds only; suppressions = ADR/SPEC authority required (unknown codes → exit 2).

## Project Reference

See: .planning/PROJECT.md (updated 2026-08-13; Key Decisions table there is the full decision log)

**Core value:** Gate analytical work on validity before the data is touched.
**Current focus:** S5 close-out — all four phase ceremonies (13,14,16,15) complete; next S5-1 `/gsd-audit-uat` cross-phase sweep

## Current Position

Phase: 15 (cuped-and-bi-declaration-checks-new-codes-d-05) — **CEREMONY COMPLETE (S4-1..S4-5)**. All four milestone phases done. Now at **S5 close-out** (S5-1 `/gsd-audit-uat` → S5-2 drain HUMAN-QUEUE → S5-3 extract-learnings → S5-4 audit-milestone → S5-5 complete-milestone → S5-6 ship). Phases 13/14/16 complete.
S4-2: 6-plan set (15-01..06) authored by `gsd-planner` (opus); independent `gsd-plan-checker` (opus, §3 override of profile haiku) verdict **REVISE (1 blocker) → 1 repair → PASS**. Blocker: 15-02 Task-1 verify's `ast.get_source_segment` scan included the docstring → tripped its own `period_comparisons`-not-in-body assert; fixed by scoping the negative scan to code (docstring excluded by node identity), re-verified empirically (OLD fails / NEW passes on a faithful synthetic impl). Orchestrator re-verified all PASS claims (§5): coverage union == exactly {REQ-P15-01..07}; single-writer waves (`spec.py`→15-01, `metrics.py`→15-02, `design.py`→15-04; every depends_on → earlier wave); trap #12 ordering; 2 mints (EXP-070 CRITICAL 15-04, MET-021 HIGH 15-02, disjoint from MET-020); D-08 additive + D-09 exact-code allowlist confined to 15-06; catalogue-staleness window safe. **S4-3 wave plan:** wave 1 = 15-01/02/03, wave 2 = 15-04, wave 3 = 15-05/06 (performs the 2 mints + additive 258→260 rebaseline). Artifacts `15-0{1..6}-PLAN.md`. D-06 veto HQ-13; HQ-9/10/12 (phase security sign-offs + UAT) + HQ-11 (P16 veto) open, all non-blocking to S5-2.
Last activity: 2026-08-29 — S4-5 Phase 15 secure (SECURED, threats_open:0) + validate (nyquist_compliant, 7/7 COVERED); S4 fully complete, all 4 phases done; full suite Ran 1312 tests OK (clean tree); resume at S5-1 close-out

Progress: [██████████] Phase 15 — 5 of 5 ceremony steps done (discuss, plan, execute, review/verify, secure/validate)

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

Last session: 2026-08-29T06:30Z (autonomous firing)
Stopped at: S4-2 complete — Phase 15 planned; 6-plan set (15-01..06) passes the plan-checker gate (REVISE→1 repair→PASS). Plans authored + gated + orchestrator-re-verified; ledger/state/queue synced. No code committed yet (S4-3 executes the plans). D-06 veto HQ-13 stays open (non-blocking).
Resume file: None — the next firing takes S4-3 from LOOP-LEDGER.md (execute all Phase 15 plans). **S4-3 wave plan:** wave 1 = 15-01 (`cuped`→VARIANCE_ADJUSTMENTS + `CUPED_COVARIATE_TIMINGS`) / 15-02 (mint MET-021 HIGH in `metrics.py`) / 15-03 (APA template + Shapiro negative-assertion tests); wave 2 = 15-04 (mint EXP-070 CRITICAL in `design.py` + θ/ρ² ref in `mathx.py`); wave 3 = 15-05 (extend good fixture, silent at every threshold) / 15-06 (regen catalogue → 260 + D-08 additive rebaseline + D-09 exact-code allowlist). **Honour the traps at execute:** (1) MET-021 reads ONLY `results.cohort_comparisons`, proven disjoint from MET-020 both directions; (2) declaration-only, no pandas/scipy/numpy on the gate path, CUPED θ/ρ ref impl in `mathx.py` never imported by the check; (3) additive rebaseline in `test_finding_catalogue_invariant.py` only (`_EXPECTED_TOTAL` 258→260, `_MINTED_CODES` += EXP-070,MET-021; frozen snapshot @256 NOT mutated); (4) D-09 exact-code allowlist not prefix; (5) do NOT run `gen-finding-catalogue.py --check`/the invariant in 15-02/04/05 (catalogue intentionally stale until 15-06 regenerates once). 3 non-blocking checker nits carried (see LOOP-LEDGER-ARCHIVE.md#S4-2; nit1 already fixed). Model routing: S4-3 executor = profile default (sonnet-class), medium (brief §3); orchestrator re-runs every plan's own verify block (§5).
