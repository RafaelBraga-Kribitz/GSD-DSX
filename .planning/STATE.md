---
gsd_state_version: 1.0
milestone: v2.4
milestone_name: Visual Excellence
current_phase: 23
current_phase_name: style-snippet-layer
status: executing
stopped_at: "S3-1 (Phase 23 discuss) COMPLETE — 23-CONTEXT.md written, S3-1 checkbox checked. Discuss run inline by the orchestrator at opus/high (brief §3; S1-1/S2-1 precedent). Persona round Architect+Auditor+Advisor (Statistician NOT engaged — style/tooling/licensing phase, no statistical content). Ground truth read live: matplotlib 3.11.1 installed (analyst-side, not a gate dep); no styles/ dir, no vendored fonts; dsx/checks/figures.py already verifies svg_sha256 via stdlib hashlib only (DSX-FIG-010/011/020) so Phase 23 changes nothing on the gate path; test_gate_path_hermetic.FORBIDDEN={pandas,scipy,numpy,csv} walks only dsx/ roots → REQ-P23-03 holds by construction (helper lives in templates/); live catalogue 276. Three must-settle gray areas + two cross-cutting settled: GA-1 four styles/*.mplstyle (dsx-538 fork / dsx-urban Apache-2.0 + vendored OFL Lato = house default / dsx-econ + dsx-bbc reimplemented from doctrine, no PDF embed, no bbplot GPL port, no proprietary font), one vendored OFL font as the deterministic house face, per-file license headers; GA-2 finalise_figure(mandatory source)/direct_label/save_deterministic(writes only, dsx seal stays the single hasher); GA-3 svg.fonttype:path + fixed hashsalt + metadata Date:None + font_manager.addfont + pinned matplotlib version in manifest, proven by an off-gate-path double-render hash-equality test (skipIf matplotlib absent); D-P23-03 add matplotlib to test_gate_path_hermetic.FORBIDDEN; D-P23-04 ZERO new codes (routes to existing codes; determinism test off gate path; palette gate D-13-deferred) → set-identity 276→276 at S3-4. License-audit confirmation deferred to S3-2 plan-review (REQ-P23-01's explicit item). Veto window filed HQ-32 (non-blocking). NEXT: S3-2 (Phase 23 plan; plan-checker must pass, opus/high).\n\n---PRIOR (S2-4)---\nS2-4 (Phase 22 code review + verification) COMPLETE — verdict PASSED, S2-4 checkbox checked. Code review + verification run inline by the orchestrator at opus/high (brief §3; S1-4 precedent), every gate RE-RUN on the final tree 217cf68, not trusted from the S2-3 inline reports. 22-REVIEW.md: read all six production/data hunks (viz.py, smells.py, spec.py, input_types.json, gen-finding-catalogue.py, finding-codes.md) + all four new/extended test modules in full; targeted the three real risks — (1) vocabulary widening: CLOSED (uncertainty_mark is a NEW optional field, silent when blank, DSX-VIZ-071 only NARROWS via membership against RELATIONSHIP_CHARTS['uncertainty']; facet_by proven orthogonal); (2) Markdown-oracle false-pass: CLOSED (all four invariants carry non-vacuity anchors + derive truth from live _mark_universe()/BANNED_TYPES, not transcription); (3) count-pin ripple: CLOSED (all three lockstep pins bumped 275→276 keep their real zero-mint tells; set-identity diff catches a mint-one/drop-one swap). ZERO code fixes needed (contrast Phase 21's 2 LOW fixes). Two observations recorded (OBS-1 cosmetic prose omission of error_bars_2d; OBS-2 the 'declared twice' warnings are 8 distinct, pre-existing, not 3 — corrected prior Log narrative honestly; Phase 22 cannot have introduced them). 22-VERIFICATION.md verdict PASSED: REQ-P22-01..05 each re-verified (read as amended by HQ-27 D-1..D-4 where the original REQ named non-existent chart types). GATES (orchestrator-run, clean tree, final state): test_chart_catalog_invariant 8 OK incl. the perceptual tie-break structural criterion (density absent; length==angle tied both ways; ≤-only monotone chain); test_uncertainty_vocabulary 3 OK (DSX-VIZ-071 member/non-member/absent); test_selection_heuristic_docs 6 OK; test_viz_vocabulary_invariant 16 OK; finding-catalogue+p19+phase20 13 OK (count + set-identity 275→276 additive-only, DSX-VIZ-072 not minted); gen-finding-catalogue --check exit 0 @276; FULL SUITE 1495 OK (40.5s). REQ-P22-01..05 checked in REQUIREMENTS.md. S2-5 then done (secure+validate at opus/high, every gate re-run: twelve threats T-22-01..12 CLOSED, nyquist_compliant:true, 79 mitigation tests OK + gen --check exit 0 @276 + full suite 1495 OK; HQ-31 security sign-off filed, non-blocking until S5-2) — Phase 22 fully shipped (S2-1..S2-5). NEXT: S3-1 (Phase 23 discuss, style + snippet layer)."
last_updated: "2026-09-03T05:24Z"
last_activity: 2026-09-03
last_activity_desc: "S3-1 COMPLETE — Phase 23 discuss at opus/high, inline persona round (Architect+Auditor+Advisor; Statistician not engaged — no statistical content). 23-CONTEXT.md settles GA-1 (four license-audited styles/*.mplstyle, dsx-urban house default, one vendored OFL Lato font), GA-2 (finalise_figure/direct_label/save_deterministic signatures; dsx seal stays single hasher), GA-3 (svg.fonttype:path + fixed hashsalt + metadata Date:None + font_manager.addfont + pinned matplotlib in manifest, off-gate-path double-render test), D-P23-03 (add matplotlib to test_gate_path_hermetic.FORBIDDEN), D-P23-04 (zero new codes → 276→276 set-identity at S3-4). License-audit confirmation deferred to S3-2 plan-review. Veto window HQ-32 filed (non-blocking). Next = S3-2 (Phase 23 plan)."
progress:
  total_phases: 4
  completed_phases: 2
  total_plans: 5
  completed_plans: 5
  percent: 50
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
**Current focus:** Phase 23 — style and snippet layer (license-audited `.mplstyle` set, the analyst-side `dsx_plotstyle.py` helper, a proven SVG-determinism recipe, and a snippet catalog that routes to finding codes). Phases 21 (viz vocabulary reconciliation) and 22 (catalog spine / uncertainty family / selection heuristic) are shipped.

## Current Position

Phase: 23 (style-snippet-layer) — discuss COMPLETE (S3-1); 23-CONTEXT.md written; next ledger unit is S3-2 (plan; plan-checker must pass)
Plan: none yet (S3-2 pending). Phases 21 + 22 shipped (S1-1..S1-5, S2-1..S2-5); full suite 1495 OK; catalogue 276 (additive-only, DSX-VIZ-071 minted in Phase 22)
Status: Executing (v2.4 — 2/4 phases complete; Phase 23 discuss done, GA-1/GA-2/GA-3 + D-P23-03/04 settled; HQ-32 veto window filed non-blocking)
Last activity: 2026-09-03 — S3-1 Phase 23 discuss at opus/high; four license-audited styles + dsx_plotstyle.py signatures + determinism recipe settled; zero-mint decision (276→276)

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
