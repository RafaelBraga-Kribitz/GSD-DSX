---
gsd_state_version: 1.0
milestone: v2.4
milestone_name: Visual Excellence
current_phase: 22
current_phase_name: catalog-spine-uncertainty-heuristic
status: executing
stopped_at: "S2-3 (Phase 22 execute) IN PROGRESS — Waves 1-2 (22-01, 22-02) COMPLETE, waves 3-4 remain. Executed inline by orchestrator (persona-lite, S1-3 precedent). Wave 1: RELATIONSHIP_CHARTS['uncertainty'] 11th key = ten Wilke §5.6 marks, all homed into CHART_CAPABILITIES['interval-range'], input_types.json regenerated; BANNED_TYPES completed to seven (gauge + word_cloud, radar→Duan 2023); DSX-SMELL-007 routes to facet_by. Wave 2: minted DSX-VIZ-071 in _check_uncertainty_vocabulary (Citation: Wilke §5.6+§16.2, Structural criterion:, wired into check()), allowlisted by exact string, regenerated finding-codes.md 275→276; set-identity diff added={DSX-VIZ-071} removed={} (additive-only proof); DSX-VIZ-072 deliberately NOT minted (HQ-30). Two sibling lockstep count-pins (test_p19_categorical_rows.py, test_phase20_zero_mint_close.py) bumped 275→276 — necessary ripple, recorded loudly in 22-02-SUMMARY. GATES (orchestrator-run, final tree): gen-finding-catalogue --check exit 0 @276; catalogue Total=276 with DSX-VIZ-071 row; full suite 1481 OK. 22-01/22-02-SUMMARY.md written. NEXT: Wave 3 (22-03) — author references/chart-catalog.md (75-90 rows, three axes + citation) + test_chart_catalog_invariant.py; then Wave 4 (22-04) heuristic route-and-cite. LARGE unit — start Wave 3 fresh (authoring the full catalog against the now-final 60-mark universe)."
last_updated: "2026-09-03T03:37Z"
last_activity: 2026-09-03
last_activity_desc: "S2-3 Waves 1-2 COMPLETE — uncertainty vocabulary spine + DSX-VIZ-071 mint (275→276 additive-only); full suite 1481 OK. Waves 3-4 (catalog + heuristic) remain."
progress:
  total_phases: 4
  completed_phases: 1
  total_plans: 5
  completed_plans: 3
  percent: 25
---

# Project state

**Status:** v2.4 Visual Excellence — OPEN, executing under the autonomous ceremony
**Progress:** [░░░░░░░░░░░░░░░░░░░░] v2.4 — 0/4 phases (21 viz vocabulary reconciliation → 22 catalog spine/uncertainty/heuristic → 23 style/snippet layer → 24 portfolio exemplar/calibration)
**Predecessors:** v2.3 Test Catalog SHIPPED 2026-09-02 (tag `v2.3.0`); v2.2 Analytic Surface SHIPPED 2026-08-29 (tag `v2.2.0`); v2.0.0 DSX Validity Frame SHIPPED 2026-08-28 (tag `v2.1.0`). Archives under `.planning/milestones/`.

**Loop control:** the autonomous ceremony drives this milestone. Contract:
`.planning/LOOP-BRIEF.md`; backlog + gates: `.planning/LOOP-LEDGER.md`; human-only
items: `.planning/HUMAN-QUEUE.md`. Branch `gsd/v2.4.0-visual-excellence`, ships
as tag `v2.4.0` by explicit named merge (never the auto-detected branch — this
repo now carries five stale `gsd/*` branches from prior milestones).

**Usage-limit posture (proven 2026-08-30 through 2026-09-02):** the firing
wrapper (`scripts/run-ceremony-firing.ps1`) detects limit hits, backs off
gracefully, and — critically — re-probes every 30 minutes during any hold to
catch an early release rather than blindly waiting the full computed window
(fixed 2026-09-01 after Anthropic released a weekly limit early and the
original dead-reckoning design missed it). Observed live: four separate
5-hour-window hits on 2026-09-02 each self-recovered in 2–7 minutes. Firings
must not retry in a loop — log one line and stop; the wrapper owns the pacing.

## Project Reference

See: .planning/PROJECT.md (updated 2026-09-02; Key Decisions table there is the full decision log)

**Core value:** Gate analytical work on validity before the data is touched.
**Current focus:** Phase 21 — viz vocabulary reconciliation (every chart-type orphan homed to both a relationship and a capability family; banned types become first-class refusal entries) before the catalog spine lands on top of it.

## Current Position

Phase: 21 (viz-vocabulary-reconciliation) — executed + reviewed + verified (S1-4 PASSED); next ledger unit is S1-5 (secure + validate)
Plan: 21-01-PLAN.md executed; 21-REVIEW.md + 21-VERIFICATION.md (verdict PASSED) written
Status: Executing (Phase 21 verification PASSED; REQ-P21-01..03 delivered; full suite 1471 OK; catalogue 275==275 set-identity zero mint; S1-5 secure/validate pending)
Last activity: 2026-09-02 — S1-4 code review + verification PASSED; 2 LOW findings fixed; set-identity diff empty (275==275)

## Performance Metrics

No v2.4 plans executed yet. v2.3, v2.2, and v2.0.0 velocity are archived with their milestone artifacts.

## Accumulated Context

### Decisions

Full decision log: PROJECT.md Key Decisions. Standing v2.4 decisions (carried from the original v2.3/v2.4 scoping, operator-directed 2026-08-29, re-confirmed at open):

- **The chart catalog is citable, not exhaustive-for-its-own-sake** — union of five named taxonomies (FT Visual Vocabulary, Wilke, Graphic Continuum, DVC, Datawrapper) after synonym merge and principled exclusions, target band 75–90 entries.
- **License audit is a plan-review gate, not an afterthought** — dsx-538/dsx-urban forked or built from permissively-licensed sources; dsx-econ/dsx-bbc reimplemented from published doctrine only, never porting GPL code (bbplot) or embedding an unlicensed PDF (the 2017 Economist styleguide).
- **Faceting is a declaration, not a chart type** — `facet_by` orthogonal to the mark, per the scope research's completeness-critic finding.
- **Contingency:** split Phase 23–24 off as v2.5 if the D-05 queue materially outruns cadence (expected lighter than v2.3's — ~8–12 reads vs 27).

### Pending Todos

None beyond the ledger.

### Blockers/Concerns

None open.

## Deferred Items

Carried forward from v2.0.0 close — captured future ideas, not gaps:

| Category | Item | Status | Deferred At |
|----------|------|--------|-------------|
| seed | SEED-001-deepen-dsx-explore-data-eda-protocol | dormant — natural v2.4/v2.5 candidate | 2026-08-28 |
| seed | SEED-002-grow-data-profile-hermetic-eda-artifacts | dormant — natural v2.4/v2.5 candidate | 2026-08-28 |

## Session Continuity

Last session: 2026-09-02 (interactive session — v2.3 ship + v2.4 open, operator traveling with intermittent connectivity)
Stopped at: v2.4 fully scoped and the ceremony repointed; no ledger unit attempted yet.
Resume file: None — the next firing takes S0-1 from LOOP-LEDGER.md.
