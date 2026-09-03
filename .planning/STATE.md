---
gsd_state_version: 1.0
milestone: v2.4
milestone_name: Visual Excellence
current_phase: 24
current_phase_name: portfolio-exemplar-viz-calibration
status: executing
stopped_at: "S4-3 DONE (box CHECKED — all 3 plans / 2 waves complete: 24-01 + 24-02 Wave 1, 24-03 Wave 2). THIS firing executed 24-03 (REQ-P24-03, verify-not-build, GA-3) INLINE to its gate (persona-lite: plan-checker had already ruled CLOSE the narrow gap at S4-2, no fresh irreversible design judgment; orchestrator re-ran every gate on the final tree; STATE single-writer). TASK 1 (verify-not-build, mutated nothing): all four milestone-audit-prerequisite modules green on the FINAL post-24-01/24-02 tree — test_doc_code_agreement.py + test_selection_heuristic_docs.py + test_viz_vocabulary_invariant.py + test_chart_catalog_invariant.py = 38 tests OK; gen-finding-catalogue --check exit 0 @276; set-identity 276→276 proven live (CRLF-safe unique DSX-code count == 276 == the 'Total: 276 codes.' line, added={} removed={}). No invariant/agreement pin was mutated to force a pass. TASK 2 (RECOMMENDED close — plan-checker's approved call, one-assertion tightening): tests/test_selection_heuristic_docs.py now imports RELATIONSHIP_CHARTS from dsx.checks.viz and asserts set(RELATIONSHIP_CHARTS) == set(_RELATIONSHIPS) BOTH directions (new test_doc_relationship_names_bind_to_the_live_dict_both_directions) — a live 12th key or a rename now fails HERE directly, not only transitively via test_viz_vocabulary_invariant's len==11 pin. RED-behavior confirmed (equality breaks on add AND on remove/rename). test_doc_code_agreement.py's deliberate one-directionality left UNTOUCHED (documented-by-design, T-24-03-03). GATES (orchestrator-run, clean tree, DECISIONS.jsonl strays swept): module 7 OK (was 6, +1 new method); git diff dsx/ EMPTY (no gate/library code touched — only tests/test_selection_heuristic_docs.py, +16 lines); gen-finding-catalogue --check exit 0 @276 zero mint; FULL SUITE 1508 OK / 45.8s (1507→1508, +1 for the new test method — expected). NEXT: S4-4 (code review + verification passed, REQ-P24-01..03) — a separate unit for a fresh firing; the holistic phase set-identity 276→276 is already proven green here on the final tree."
last_updated: "2026-09-03T14:42Z"
last_activity: 2026-09-03
last_activity_desc: "S4-3 DONE (box CHECKED — all 3 plans complete): executed 24-03 (REQ-P24-03, verify-not-build + the plan-checker-approved one-assertion gap close). Verified all four audit-prerequisite modules green on the final tree (38 OK), catalogue current @276, set-identity 276→276 proven live. Closed the chart-selection live-dict binding gap: test_selection_heuristic_docs.py imports RELATIONSHIP_CHARTS and asserts set-equality both directions (drift now caught directly, not only transitively); test_doc_code_agreement.py untouched. git diff dsx/ empty (no gate code); full suite 1508 OK / 45.8s clean tree; zero mint @276. Phase 24 execution complete; S4-4 (code review + verification) next."
progress:
  total_phases: 4
  completed_phases: 3
  total_plans: 11
  completed_plans: 11
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

Phase: 24 (portfolio-exemplar-viz-calibration) — S4-1 discuss + S4-2 plan + S4-3 execute DONE (all three boxes CHECKED); 3 plans / 2 waves all executed; next unit S4-4 (code review + verification)
Plan: Phases 21+22+23 all shipped. Phase 24 EXECUTED (3 plans / 2 waves): W1 24-01 exemplar upgrade in place (REQ-P24-01: dsx-urban style layer, one real-CI uncertainty figure via DSX-VIZ-071, re-sealed manifest, What/So What/Now What narrative, REPRO-REPORT) ∥ 24-02 first bad-chart fixtures + corpus harness re-baseline with a new MEDIUM stratum for DSX-VIZ-071 (REQ-P24-02); W2 24-03 verify-not-build + closed the chart-selection live-dict binding gap (REQ-P24-03). Zero new codes proven live (276→276, set-identity added={} removed={}). Full suite 1508 OK on the final tree (was 1507 at Phase 23 close; +1 for 24-03's new both-directions test method); catalogue @276
Status: Executing (v2.4 — 3/4 phases complete; Phase 24 discuss+plan+execute done, S4-4 code review + verification next; HQ-33/HQ-34 non-blocking until S5-2; HQ-35 discuss veto window non-blocking)
Last activity: 2026-09-03 — S4-3: executed 24-03 (verify-not-build) — all four audit-prerequisite modules green on the final tree (38 OK), catalogue @276, set-identity 276→276 proven live; closed the chart-selection live-dict binding gap with a both-directions RELATIONSHIP_CHARTS assertion (test_doc_code_agreement.py untouched); git diff dsx/ empty; full suite 1508 OK / 45.8s clean tree; S4-3 box CHECKED (all 3 plans complete)

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
