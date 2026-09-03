---
gsd_state_version: 1.0
milestone: v2.4
milestone_name: Visual Excellence
current_phase: 23
current_phase_name: style-snippet-layer
status: executing
stopped_at: "S3-3 COMPLETE — all three Phase-23 plans executed (23-01/23-02/23-03); S3-3 checkbox CHECKED. Wave 3 (23-03) executed inline (persona-lite, S1-3/S2-3/23-01/23-02 precedent: plan left no irreversible design judgment — the routing test is the oracle; orchestrator re-runs every gate; STATE single-writer). TDD RED→GREEN→prove. RED: authored tests/test_snippet_catalog_routing.py (2 methods — cited⊆defined non-empty via the CRLF-safe _ROW_RE reused from test_finding_catalogue_invariant.py; no-threshold-restatement with MAX_PIE_SLICES/MAX_CATEGORICAL_COLORS imported LIVE from dsx.checks.viz and the forbidden regexes built from those integers, never transcribed) — RED confirmed both methods fail on file-absence, no assertion softened. GREEN: authored references/chart-snippets.md — a provenance note (describes, does not adjudicate), a Sealing-workflow section (save_deterministic → dsx seal → visuals[].svg_sha256, the GA-2 single-hasher flow), and one worked snippet per Function-axis category (Change over Time/line, Magnitude/bar, Distribution/histogram, Correlation/scatter, Ranking/bump, Part-to-whole/pie, Deviation/diverging_bar, Flow/sankey, Spatial/choropleth, Uncertainty/error_bars), each importing finalise_figure+save_deterministic and routing to governing codes BY NAME; part-to-whole cites DSX-VIZ-040 and colour guidance cites DSX-VIZ-050 WITHOUT writing either maximum. Every cited code verified present in references/finding-codes.md. Wired @references/chart-snippets.md into skills/dsx-visualize/SKILL.md <references>. PROVE (zero mint): touched NONE of the mint surfaces (finding-codes.md / gen-finding-catalogue.py / test_finding_catalogue_invariant.py — confirmed via git status). GATES (orchestrator-run, clean tree, DECISIONS.jsonl strays swept): routing 2 OK; 10 function sections present + skill wired; gen-finding-catalogue --check exit 0 @276 (zero mint); test_finding_catalogue_invariant set-identity SET-equal + count 276 (276→276, added={} removed={}); FULL SUITE 1507 OK, 41.3s (1505→1507, +2 routing methods; same 4 pre-existing declared-twice warnings). NEXT: S3-4 (Phase 23 code review + verification, opus/high — includes the off-gate-path double-render determinism test green per REQ-P23-03; a separate unit for a fresh firing).\n\n---PRIOR (S3-3 Wave 2 / 23-02)---\ntemplates/dsx_plotstyle.py (GA-2 helper: finalise_figure mandatory-source / direct_label / save_deterministic write-only-never-hash / register_fonts at import) + GA-3 recipe (svg.hashsalt=dsx, svg.fonttype=path, metadata Date:None, Lato via addfont) proven by off-gate-path double-render hash-equality; matplotlib_version 3.11.1 added to FIGURE-MANIFEST.yaml (additive); FORBIDDEN += matplotlib (D-P23-03, still green). api+determinism 6 OK, hermetic 2 OK, full suite 1505 OK, zero mint @276.\n\n---PRIOR (S3-3 Wave 1 / 23-01)---\nFour license-audited styles/*.mplstyle (dsx-538 fork / dsx-urban house default / dsx-econ / dsx-bbc) + vendored Lato OFL house face (checksums recorded, OFL.txt at-locator confirmed) + WCAG-AA palettes; style tests 4 OK, full suite 1499 OK, zero mint @276; HQ-33 filed non-blocking (Urban Apache-2.0 still needs an at-locator human read)."
last_updated: "2026-09-03T09:20Z"
last_activity: 2026-09-03
last_activity_desc: "S3-3 DONE (all 3 waves) — S3-3 checkbox CHECKED. Wave 3 (23-03) inline TDD: RED tests/test_snippet_catalog_routing.py (cited⊆defined non-empty; no-threshold-restatement with MAX_PIE_SLICES/MAX_CATEGORICAL_COLORS imported LIVE and regexes built from those integers, never transcribed) → GREEN references/chart-snippets.md (Sealing-workflow + 10 Function-axis snippets, each importing finalise_figure+save_deterministic and routing to codes BY NAME; DSX-VIZ-040/050 cited without their numeric maxima) + @references/chart-snippets.md wired into skills/dsx-visualize/SKILL.md → PROVE zero-mint (mint surfaces untouched). Gates (clean tree): routing 2 OK, 10 sections + skill wired, gen --check exit 0 @276, set-identity 276→276 (added={} removed={}), FULL SUITE 1507 OK (+2). Next = S3-4 (code review + verification, opus/high)."
progress:
  total_phases: 4
  completed_phases: 2
  total_plans: 8
  completed_plans: 8
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

Phase: 23 (style-snippet-layer) — S3-3 execute DONE (all 3 waves 23-01/23-02/23-03); S3-3 checkbox CHECKED; next unit S3-4 (code review + verification)
Plan: all three Phase-23 plans executed (styles + Lato + WCAG palettes; dsx_plotstyle.py helper + GA-3 determinism recipe; references/chart-snippets.md snippet catalog + skill wiring). Phases 21 + 22 shipped; full suite 1507 OK; catalogue 276 (zero mint across the whole phase)
Status: Executing (v2.4 — 2/4 phases complete; Phase 23 all execute waves landed; GA-1/GA-2/GA-3 + D-P23-03/D-P23-04 honored; HQ-33 filed non-blocking)
Last activity: 2026-09-03 — S3-3 Wave 3: references/chart-snippets.md (10 Function-axis snippets routing to finding codes by name, no threshold restated) + skill <references> wiring; routing 2 OK, set-identity 276→276, full suite 1507 OK, zero mint @276

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
