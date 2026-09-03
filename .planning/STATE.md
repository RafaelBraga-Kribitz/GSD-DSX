---
gsd_state_version: 1.0
milestone: v2.4
milestone_name: Visual Excellence
current_phase: 24
current_phase_name: portfolio-exemplar-viz-calibration
status: executing
stopped_at: "S4-3 IN PROGRESS (box UNCHECKED — one checkbox spanning 3 plans / 2 waves; too large for one firing, S2-3/S3-3 precedent). This firing executed 24-01 (Wave 1, REQ-P24-01) INLINE to its gate (persona-lite: plan left no irreversible design judgment; orchestrator re-ran every gate on the final tree; STATE single-writer). Upgraded the examples/good-* exemplar IN PLACE (GA-1(a)): authored examples/analysis/charts.py (sole matplotlib importer, off the gate path) rendering all 3 figures through the dsx-urban style layer + dsx_plotstyle.finalise_figure(mandatory source)/save_deterministic; added the 3rd uncertainty visual (relationship:uncertainty, uncertainty_mark:error_bars → DSX-VIZ-071 valid member silent; data_input_type:interval-range admits error_bars → no DSX-VIZ-013); re-SEALED all 3 SVGs via dsx seal (two pre-existing seals were stale after re-render — Risk P2); wired manifest uncertainty row + matplotlib_version:3.11.1; rewrote good-NARRATIVE.md to What/So What/Now What keeping the 3 claims verbatim (DSX-NAR-020); authored good-REPRO-REPORT.md (status:reproduced, activation_rate:0.024 == results.tests[0].effect) + reproducibility.reproduce_report pointer. DETERMINISM PROVEN: two renders byte-identical (identical dsx seal digests). GATE: dsx gate ship --spec examples/good-ANALYSIS-SPEC.yaml --phase-dir examples → exit 0 (CRITICAL=0 HIGH=0 MEDIUM=3 INFO=1; the 3 MEDIUM DSX-STA-011 are PRE-EXISTING on the untouched results block, not introduced). DEVIATION (recorded loudly, honest, minimal): gate invoked with --phase-dir examples because dsx/cli.py wires repro.check(spec, phase_dir) with raw phase_dir (None when flag omitted) while every other check gets resolve_root=spec-parent; repro.py:313 resolves entrypoint/reproduce_report against the GSD phase dir by design → once reproduce_report is declared it only resolves when the phase dir is named. Strictly MORE rigorous; no dsx/ code touched (out of 24-01 scope). Zero mint: gen-finding-catalogue --check exit 0 @276, changed files == the 8 files_modified. test_gate_path_hermetic 2 OK. NEXT: S4-3 continues — 24-02 (first bad-chart fixtures + MEDIUM-stratum harness re-baseline, Wave 1) then 24-03 (verify-not-build, Wave 2, depends on both). Full-suite re-run + the holistic zero-mint set-identity are S4-4's job."
last_updated: "2026-09-03T13:04Z"
last_activity: 2026-09-03
last_activity_desc: "S4-3 partial: executed 24-01 (Wave 1) — upgraded examples/good-* exemplar in place into the v2.4 capstone (charts.py through the dsx-urban style layer, 3rd uncertainty figure via DSX-VIZ-071, all 3 SVGs re-sealed, What/So What/Now What narrative, REPRO-REPORT). Determinism proven byte-identical. Gate: dsx gate ship --phase-dir examples exit 0 (CRITICAL=0 HIGH=0; 3 pre-existing MEDIUM only). Zero mint @276. Deviation recorded: --phase-dir examples required by repro.check's phase-dir resolution. S4-3 box stays UNCHECKED — 24-02 + 24-03 remain."
progress:
  total_phases: 4
  completed_phases: 3
  total_plans: 11
  completed_plans: 9
  percent: 75
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
**Current focus:** Phase 24 — portfolio exemplar and viz calibration (the terminal phase: one end-to-end capstone exercising both v2.3's test catalog and v2.4's style/uncertainty surfaces, plus the first bad-chart-choice fixtures and a catch-rate/FPR re-baseline). Phases 21 (viz vocabulary reconciliation), 22 (catalog spine / uncertainty family / selection heuristic), and 23 (style / snippet layer) are shipped.

## Current Position

Phase: 24 (portfolio-exemplar-viz-calibration) — S4-1 discuss + S4-2 plan DONE (both boxes CHECKED); 3 plans / 2 waves written, plan-checker(opus) VERIFICATION PASSED; next unit S4-3 (execute)
Plan: Phases 21+22+23 all shipped. Phase 24 planned (3 plans / 2 waves): W1 24-01 exemplar upgrade in place (REQ-P24-01: dsx-urban style layer, one real-CI uncertainty figure via DSX-VIZ-071, re-sealed manifest, What/So What/Now What narrative, REPRO-REPORT) ∥ 24-02 first bad-chart fixtures + corpus harness re-baseline with a new MEDIUM stratum for DSX-VIZ-071 (REQ-P24-02); W2 24-03 verify-not-build + close the chart-selection live-dict binding gap (REQ-P24-03). Zero new codes (276→276 target). Full suite 1507 OK at Phase 23 close; catalogue re-measured live = 276
Status: Executing (v2.4 — 3/4 phases complete; Phase 24 discuss+plan done; HQ-33/HQ-34 non-blocking until S5-2; HQ-35 discuss veto window non-blocking)
Last activity: 2026-09-03 — S4-2: Phase 24 planned; recovered 2 stranded S4-2 commits (research + validation seed) then continued the pipeline — gsd-planner(opus) 3 plans / 2 waves, gsd-plan-checker(opus) VERIFICATION PASSED; zero-mint 276→276; no stray-branch trap (d00bd8e on canonical, pushed)

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
