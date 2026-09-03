---
gsd_state_version: 1.0
milestone: v2.4
milestone_name: Visual Excellence
current_phase: 22
current_phase_name: catalog-spine-uncertainty-heuristic
status: executing
stopped_at: "S2-3 (Phase 22 execute) IN PROGRESS — Waves 1-3 (22-01, 22-02, 22-03) COMPLETE, wave 4 remains. Executed inline by orchestrator (persona-lite, S1-3 precedent). Wave 1: RELATIONSHIP_CHARTS['uncertainty'] 11th key = ten Wilke §5.6 marks, all homed into CHART_CAPABILITIES['interval-range'], input_types.json regenerated; BANNED_TYPES completed to seven (gauge + word_cloud, radar→Duan 2023); DSX-SMELL-007 routes to facet_by. Wave 2: minted DSX-VIZ-071, catalogue 275→276 additive-only; DSX-VIZ-072 NOT minted (HQ-30). Wave 3: authored references/chart-catalog.md (81 rows = 60 dsx_admissible generated from live _mark_universe() + 14 reference_only FT/Wilke-sourced + 7 refusal = live BANNED_TYPES keys) with a fenced json payload (perceptual_ranks D-1 six-rank-with-ties map, length==angle tie, no density); added tests/test_chart_catalog_invariant.py (8 clauses green: band, three-axes+citation, conformance both directions, refusal drift guard, reference-only isolation, D-1 tie-break, citation traceability, non-vacuity). Reference-only rows deliberately FT/Wilke-cited (no DVC-URL) — recorded loudly in 22-03-SUMMARY (rigour > reliability; can't verify live DVC URLs this firing). Temp generator run once + deleted; only the .md ships. Zero new code minted (mint stays 276). GATES (orchestrator-run, final tree): catalog module 8 OK; full suite 1489 OK (1481→1489, +8). 22-03-SUMMARY.md written. NEXT: Wave 4 (22-04) — 5-layer heuristic route-and-cite into question-taxonomy.md (L1) + chart-selection.md (L2-L5, + correct the pre-HQ-27 perceptual line to D-1 six-rank-with-ties, + uncertainty relationship row), ripple skills/dsx-visualize/SKILL.md 10→11 relationships + chart-catalog.md pointer, add tests/test_selection_heuristic_docs.py. Then S2-3 checkbox is complete → S2-4."
last_updated: "2026-09-03T04:33Z"
last_activity: 2026-09-03
last_activity_desc: "S2-3 Waves 1-3 COMPLETE — uncertainty spine + DSX-VIZ-071 mint (Wave 1-2) + merged chart-catalog.md (81 rows, three axes + citation) with conformance/tie-break invariant (Wave 3); full suite 1489 OK. Wave 4 (heuristic route-and-cite) remains."
progress:
  total_phases: 4
  completed_phases: 1
  total_plans: 5
  completed_plans: 4
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
