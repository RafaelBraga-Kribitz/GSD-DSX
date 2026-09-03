---
gsd_state_version: 1.0
milestone: v2.4
milestone_name: Visual Excellence
current_phase: 24
current_phase_name: portfolio-exemplar-viz-calibration
status: executing
stopped_at: "S4-3 IN PROGRESS (box UNCHECKED — one checkbox spanning 3 plans / 2 waves; too large for one firing, S2-3/S3-3 precedent). 24-01 + 24-02 (Wave 1) DONE; 24-03 (Wave 2, verify-not-build, depends on both) remains. THIS firing executed 24-02 (REQ-P24-02) INLINE to its gate: authored the FIRST bad-CHART-choice fixtures (GA-2) — four fixtures under examples/known-bad/, each a copy of a proven-clean examples/good-corpus control + exactly ONE bad visuals[] entry (recipe MEASURED through the real corpus harness before + after authoring, not estimated). Three banned-type HIGH fixtures (gauge/word_cloud/radar → the EXISTING DSX-VIZ-001, zero mint) exit 0 at plan/execute and fire DSX-VIZ-001 HIGH (sole HIGH; incidental DSX-VIZ-010/014 MEDIUM only) at verify/ship; one MEDIUM fixture (chart-uncertainty-mark-misuse → DSX-VIZ-071, uncertainty_mark:gradient_band NOT a §5.6 member) exits 0 at the default HIGH threshold and exit 1 under --block-on MEDIUM. Task 3: added _MEDIUM_TARGET_DEFECT_CODES, threaded block_on through _gate_findings (default None keeps CRITICAL/HIGH strata byte-identical), extended test_stratified_catch_rate_and_fpr_report with a live MEDIUM readout reported BESIDE the headline + a headline-invariance re-assertion. DEVIATION (recorded loudly): three tree-wide registries beyond the plan's files_modified required per-fixture entries for any new committed spec, each updated with MEASURED values — test_dsx.py estimand count 19→23; test_frame_val.py _EXPECTED_VAL_CODES +4 (all set(), val.check empty); test_causal_verb_golden.py _GOLDEN_SHIP_FINDINGS +4 ({DSX-VIZ-001} banned / frozenset() misuse, measured CRITICAL/HIGH). GATES (orchestrator-run, clean tree): tests.test_known_bad_corpus 47 OK; gen-finding-catalogue --check exit 0 @276 (zero mint, no dsx/ code touched); FULL SUITE 1507 OK / 47.5s (top-level count unchanged — 4 fixtures add subtests, not new methods). Original 24-01 record follows. || S4-3 24-01: executed 24-01 (Wave 1, REQ-P24-01) INLINE to its gate (persona-lite: plan left no irreversible design judgment; orchestrator re-ran every gate on the final tree; STATE single-writer). Upgraded the examples/good-* exemplar IN PLACE (GA-1(a)): authored examples/analysis/charts.py (sole matplotlib importer, off the gate path) rendering all 3 figures through the dsx-urban style layer + dsx_plotstyle.finalise_figure(mandatory source)/save_deterministic; added the 3rd uncertainty visual (relationship:uncertainty, uncertainty_mark:error_bars → DSX-VIZ-071 valid member silent; data_input_type:interval-range admits error_bars → no DSX-VIZ-013); re-SEALED all 3 SVGs via dsx seal (two pre-existing seals were stale after re-render — Risk P2); wired manifest uncertainty row + matplotlib_version:3.11.1; rewrote good-NARRATIVE.md to What/So What/Now What keeping the 3 claims verbatim (DSX-NAR-020); authored good-REPRO-REPORT.md (status:reproduced, activation_rate:0.024 == results.tests[0].effect) + reproducibility.reproduce_report pointer. DETERMINISM PROVEN: two renders byte-identical (identical dsx seal digests). GATE: dsx gate ship --spec examples/good-ANALYSIS-SPEC.yaml → exit 0 (CRITICAL=0 HIGH=0 MEDIUM=3 INFO=1; the 3 MEDIUM DSX-STA-011 confirmed PRE-EXISTING by gating the pre-24-01 spec 08a65bf, not introduced). REGRESSION CAUGHT+FIXED within the plan: first pass set reproduce_report spec-dir-relative (good-REPRO-REPORT.md) but the repro check resolves it against phase_dir/CWD (not resolve_root like every other path field); the good-fixture-gating tests call run_checks(phase_dir=None) from repo-root CWD → DSX-REP-060 HIGH flipped 16 tests RED. Fixed by writing the path repo-root-relative (examples/good-REPRO-REPORT.md) — resolves under the CLI AND the harness, no --phase-dir needed. FULL SUITE 1507 OK from a clean tree (43.5s), same count as Phase 23 close. Seal-durability: .gitattributes examples/figures/*.svg binary stores exact sealed bytes (index blobs seal to spec values exactly). Zero mint: gen-finding-catalogue --check exit 0 @276, changed files scoped to examples/ + charts.py + .gitattributes. test_gate_path_hermetic 2 OK. NEXT: S4-3 continues — 24-02 (first bad-chart fixtures + MEDIUM-stratum harness re-baseline, Wave 1) then 24-03 (verify-not-build, Wave 2, depends on both). The holistic zero-mint set-identity is 24-03/S4-4's job."
last_updated: "2026-09-03T14:14Z"
last_activity: 2026-09-03
last_activity_desc: "S4-3 partial (Wave 1 complete): executed 24-02 (REQ-P24-02) — authored the FIRST bad-CHART-choice fixtures (4 under examples/known-bad/: gauge/word_cloud/radar → DSX-VIZ-001 HIGH, zero mint; chart-uncertainty-mark-misuse → DSX-VIZ-071 MEDIUM), each a clean good-corpus control + one bad visual (recipe measured through the corpus harness). Added the MEDIUM stratum (block_on threaded, readout beside the headline, headline invariant). Registered per-fixture entries in three tree-wide registries (deviation, measured): estimand count 19→23, _EXPECTED_VAL_CODES +4 empty, _GOLDEN_SHIP_FINDINGS +4. Gates: tests.test_known_bad_corpus 47 OK; zero mint @276 (no dsx/ code); full suite 1507 OK / 47.5s clean tree. S4-3 box stays UNCHECKED — 24-03 (Wave 2, verify-not-build) remains."
progress:
  total_phases: 4
  completed_phases: 3
  total_plans: 11
  completed_plans: 10
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
