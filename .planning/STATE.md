---
gsd_state_version: 1.0
milestone: v2.2
milestone_name: Analytic Surface
current_phase: 15
current_phase_name: cuped-and-bi-declaration-checks
status: executing
stopped_at: "S4-4 COMPLETE — Phase 15 code review + verification, both PASS. Review PASS with 1 auto-fix: the full suite (deferred from S4-3 to here) caught a stale REQ-P7-03 byte-anchor — 15-04 legitimately added _check_cuped/DSX-EXP-070 to dsx/checks/design.py but the feature commit did not update tests/test_frame_val.py::_DESIGN_PY_SHA256 in the same commit; recomputed the CRLF-normalised hash independently (a4f296c2…e80c271) + added a dated sanctioned-update comment (the anchor's own documented escape hatch, used 3× before). REQ-P7-03's behavioural VAL/EXP disjointness invariant untouched (three disjointness tests passed pre-fix; EXP-070 disjoint from EXP-021/VAL-020, fires only on variance_adjustment==cuped). Verification PASSED 7/7 REQ-P15-01..07 (P15-04 PARTIAL, consented at S4-1 via answered HQ-8). Gate-path flip proven: post-treatment CUPED → dsx gate plan exit 1 DSX-EXP-070 (CRITICAL), good fixture silent at plan+verify, MET-021 fires on bucket mix-shift + disjoint from MET-020 both directions. D-08 additive (--check exit 0 @260, invariant 2 OK = 260 + set-identity vs snapshot∪{REP-060,061,EXP-070,MET-021}, _SNAPSHOT_TOTAL 256, frozen snapshot byte-unchanged). No pandas/scipy/numpy added to the gate path. Full suite: sh scripts/check.sh all passed, Ran 1292 tests OK (1263→+29). No new D-05 read owed (HQ-8 answered); HQ-13 (D-06 veto) finalised to exact shipped catalogue text. 1 non-blocking nit (N1 cosmetic spec.py comment). Artifacts: 15-.../REVIEW.md, 15-.../VERIFICATION.md, fix in tests/test_frame_val.py. RESUME at S4-5 (/gsd-secure-phase 15 + /gsd-validate-phase 15; --check exit 0 on new codes; both fixtures satisfy D-08; queue Phase-15 security sign-off + UAT to HUMAN-QUEUE). See LOOP-LEDGER.md Log."
last_updated: "2026-08-29T13:40:00.000Z"
last_activity: 2026-08-29
last_activity_desc: "S4-4 complete — Phase 15 code review PASS (1 auto-fix: stale REQ-P7-03 design.py byte-anchor) + verification PASSED 7/7; full suite Ran 1292 tests OK; gate-path flip proven; resume at S4-5 (secure + validate)"
progress:
  total_phases: 4
  completed_phases: 3
  total_plans: 6
  completed_plans: 6
  percent: 90
---

# Project state

**Status:** Phase 15 IN PROGRESS (S4) — **S4-4 code review + verification COMPLETE, both PASS**. Review PASS with 1 auto-fix (full suite deferred from S4-3 caught a stale REQ-P7-03 byte-anchor: 15-04 added `_check_cuped`/`DSX-EXP-070` to `dsx/checks/design.py`; recomputed `_DESIGN_PY_SHA256` independently + sanctioned-update comment; behavioural VAL/EXP disjointness untouched). Verification PASSED 7/7 REQ-P15-01..07 (P15-04 PARTIAL, consented). Gate-path flip proven (post-treatment CUPED → `dsx gate plan` exit 1 EXP-070; good fixture silent). Full suite `sh scripts/check.sh` all passed, **Ran 1292 tests OK** (1263→+29). No new D-05 owed (HQ-8 answered); HQ-13 (D-06 veto) finalised. Next: **S4-5** (`/gsd-secure-phase 15` + `/gsd-validate-phase 15`).
**Progress:** [██████████████████░░] v2.2 — 3/4 phases complete (13, 14, 16); Phase 15 in progress (S4-4 of 5 done); order 13 → 14 → 16 → 15
**Predecessor:** [████████████████████] v2.0.0 SHIPPED 2026-08-28 — 11/11 phases, 89 plans, 208 tasks, tag `v2.1.0`, merged to `main`. Full record: `.planning/MILESTONES.md`; artifacts archived under `.planning/milestones/v2.0.0-*` (phases, ROADMAP, REQUIREMENTS, MILESTONE-AUDIT, loop ledgers).

**Locked decisions (v2.2, carried from planning):** DQ = profile runner + hermetic gates; Glyph = hermetic svg_sha256 only (no MCP dep); forbidden claims = universal pack + optional phase YAML; repro_lock = ARS-style honest-null (not byte-replay); decision replay = structured thresholds only; suppressions = ADR/SPEC authority required (unknown codes → exit 2).

## Project Reference

See: .planning/PROJECT.md (updated 2026-08-13; Key Decisions table there is the full decision log)

**Core value:** Gate analytical work on validity before the data is touched.
**Current focus:** Phase 15 — cuped-and-bi-declaration-checks (S4-4 review+verify done, both PASS; next S4-5 secure + validate)

## Current Position

Phase: 15 (cuped-and-bi-declaration-checks-new-codes-d-05) — IN PROGRESS. **S4-1 discuss + S4-2 plan + S4-3 execute + S4-4 review/verify COMPLETE**; S4-5 pending. Phases 13/14/16 complete.
S4-2: 6-plan set (15-01..06) authored by `gsd-planner` (opus); independent `gsd-plan-checker` (opus, §3 override of profile haiku) verdict **REVISE (1 blocker) → 1 repair → PASS**. Blocker: 15-02 Task-1 verify's `ast.get_source_segment` scan included the docstring → tripped its own `period_comparisons`-not-in-body assert; fixed by scoping the negative scan to code (docstring excluded by node identity), re-verified empirically (OLD fails / NEW passes on a faithful synthetic impl). Orchestrator re-verified all PASS claims (§5): coverage union == exactly {REQ-P15-01..07}; single-writer waves (`spec.py`→15-01, `metrics.py`→15-02, `design.py`→15-04; every depends_on → earlier wave); trap #12 ordering; 2 mints (EXP-070 CRITICAL 15-04, MET-021 HIGH 15-02, disjoint from MET-020); D-08 additive + D-09 exact-code allowlist confined to 15-06; catalogue-staleness window safe. **S4-3 wave plan:** wave 1 = 15-01/02/03, wave 2 = 15-04, wave 3 = 15-05/06 (performs the 2 mints + additive 258→260 rebaseline). Artifacts `15-0{1..6}-PLAN.md`. D-06 veto HQ-13; HQ-9/10/12 (phase security sign-offs + UAT) + HQ-11 (P16 veto) open, all non-blocking to S5-2.
Last activity: 2026-08-29 — S4-4 Phase 15 code review PASS (1 auto-fix: stale REQ-P7-03 design.py byte-anchor) + verification PASSED 7/7; full suite Ran 1292 tests OK; resume at S4-5 (secure + validate)

Progress: [████░░░░░░] Phase 15 — 2 of 5 ceremony steps done (discuss, plan)

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
