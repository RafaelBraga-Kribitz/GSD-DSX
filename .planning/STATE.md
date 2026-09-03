---
gsd_state_version: 1.0
milestone: v2.4
milestone_name: Visual Excellence
current_phase: 22
current_phase_name: catalog-spine-uncertainty-heuristic
status: executing
stopped_at: "S2-4 (Phase 22 code review + verification) COMPLETE — verdict PASSED, S2-4 checkbox checked. Code review + verification run inline by the orchestrator at opus/high (brief §3; S1-4 precedent), every gate RE-RUN on the final tree 217cf68, not trusted from the S2-3 inline reports. 22-REVIEW.md: read all six production/data hunks (viz.py, smells.py, spec.py, input_types.json, gen-finding-catalogue.py, finding-codes.md) + all four new/extended test modules in full; targeted the three real risks — (1) vocabulary widening: CLOSED (uncertainty_mark is a NEW optional field, silent when blank, DSX-VIZ-071 only NARROWS via membership against RELATIONSHIP_CHARTS['uncertainty']; facet_by proven orthogonal); (2) Markdown-oracle false-pass: CLOSED (all four invariants carry non-vacuity anchors + derive truth from live _mark_universe()/BANNED_TYPES, not transcription); (3) count-pin ripple: CLOSED (all three lockstep pins bumped 275→276 keep their real zero-mint tells; set-identity diff catches a mint-one/drop-one swap). ZERO code fixes needed (contrast Phase 21's 2 LOW fixes). Two observations recorded (OBS-1 cosmetic prose omission of error_bars_2d; OBS-2 the 'declared twice' warnings are 8 distinct, pre-existing, not 3 — corrected prior Log narrative honestly; Phase 22 cannot have introduced them). 22-VERIFICATION.md verdict PASSED: REQ-P22-01..05 each re-verified (read as amended by HQ-27 D-1..D-4 where the original REQ named non-existent chart types). GATES (orchestrator-run, clean tree, final state): test_chart_catalog_invariant 8 OK incl. the perceptual tie-break structural criterion (density absent; length==angle tied both ways; ≤-only monotone chain); test_uncertainty_vocabulary 3 OK (DSX-VIZ-071 member/non-member/absent); test_selection_heuristic_docs 6 OK; test_viz_vocabulary_invariant 16 OK; finding-catalogue+p19+phase20 13 OK (count + set-identity 275→276 additive-only, DSX-VIZ-072 not minted); gen-finding-catalogue --check exit 0 @276; FULL SUITE 1495 OK (40.5s). REQ-P22-01..05 checked in REQUIREMENTS.md. NEXT: S2-5 (/gsd-secure-phase 22 + /gsd-validate-phase 22; end-of-phase security sign-off + UAT batched to HUMAN-QUEUE, non-blocking until S5-2)."
last_updated: "2026-09-03T05:05Z"
last_activity: 2026-09-03
last_activity_desc: "S2-4 COMPLETE — Phase 22 code review (verdict PASS, zero fixes) + verification (verdict PASSED, REQ-P22-01..05) run at opus/high with every gate re-run by the orchestrator; perceptual structural-criterion test green; full suite 1495 OK; mint 276 additive by set-identity. 22-REVIEW.md + 22-VERIFICATION.md written. Next = S2-5 (secure + validate)."
progress:
  total_phases: 4
  completed_phases: 1
  total_plans: 5
  completed_plans: 5
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
