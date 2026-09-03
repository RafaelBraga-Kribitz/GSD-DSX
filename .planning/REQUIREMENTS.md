# Requirements

**Current milestone:** v2.4 Visual Excellence (Phases 21–24) — see below.
**Shipped:** v1.1.0–v1.5.0 (Phases 1–5, archived); v2.0.0 DSX Validity Frame
(Phases 6–12, archived at `.planning/milestones/v2.0.0-REQUIREMENTS.md`);
v2.2 Analytic Surface (Phases 13–16, archived at
`.planning/milestones/v2.2-REQUIREMENTS.md`); v2.3 Test Catalog (Phases 17–20,
archived at `.planning/milestones/v2.3-REQUIREMENTS.md`).

**Scope source:** `.planning/research/V2.3-V2.4-SCOPE.md` §3 (2026-08-29) —
carries the full research provenance, citations per source, license audit
findings, and the critique register these requirements answer. Entry condition
(D-13) met: v2.3 shipped 2026-09-02 (tag `v2.3.0`). Binding constraints: D-01
(stdlib gate path), D-02 (declarations only), D-05 (citation + published
reference value per check), D-06 (additive codes only; live catalogue count
re-verified at 275 before this milestone opened), D-12a (paradigm pairs).

---

## Phase 21 — Viz vocabulary reconciliation

- [x] REQ-P21-01 An **every-mark-has-a-home invariant test**: every chart type
  named anywhere (`RELATIONSHIP_CHARTS`, `CHART_CAPABILITIES`, smells sets,
  input-type extras) is reachable through at least one relationship AND one
  capability family; the current orphans (histogram, density, ecdf, strip,
  diverging_bar, waterfall, dumbbell, bump, sankey, kde, population_pyramid,
  butterfly) are homed.
- [x] REQ-P21-02 Banned/excluded types become first-class refusal entries
  cross-referencing their banning code and perception citation — present and
  routed-to-refusal, never silently absent.
- [x] REQ-P21-03 Zero new codes this phase, by set-identity diff against the
  live 275-code baseline.

## Phase 22 — Catalog spine, uncertainty family, selection heuristic

- [x] REQ-P22-01 A merged chart catalog (~80 entries, band 75–90) with three
  axes per entry (function; data signature; Cleveland–McGill perceptual rank)
  and a per-entry citation (FT Visual Vocabulary spine; Wilke chapters; DVC
  stable URLs; Datawrapper cardinality bands).
- [x] REQ-P22-02 The **uncertainty** function family enters the vocabulary (fan
  chart, quantile dot plot, half-eye, gradient CI band — Wilke ch. 16), with
  the vocabulary decision (11th relationship key vs new input-type ids) made
  at discuss and rippled across `viz.py`, skills, references, templates.
  D-12a-clean (covers frequentist CIs and Bayesian posteriors symmetrically).
- [x] REQ-P22-03 Faceting ships as an orthogonal `facet_by` declaration, not a
  chart type; smells remedies route to it.
- [x] REQ-P22-04 The 5-layer question→chart heuristic ships as edits to
  `references/question-taxonomy.md` / `chart-selection.md` plus skill
  pointers — route-and-cite, no parallel decision tree.
- [x] REQ-P22-05 Gates extended for the new vocabulary; every new code carries
  a D-05 citation; the perceptual tie-break ordering is asserted against the
  published Cleveland–McGill ranking as a named structural criterion (pure
  ordering assertion, no computation).

## Phase 23 — Style and snippet layer

- [x] REQ-P23-01 `styles/*.mplstyle` set: dsx-538 (forked from matplotlib,
  BSD), dsx-urban (Apache-2.0 palette, vendored OFL Lato — house default),
  dsx-econ and dsx-bbc reimplemented from published doctrine only (no GPL
  port, no unlicensed PDF embedding); per-file license/attribution headers;
  license audit as an explicit plan-review item.
- [x] REQ-P23-02 `templates/dsx_plotstyle.py` analyst-side helper
  (matplotlib-only, off the gate path): `finalise_figure()`, `direct_label()`,
  `save_deterministic()`.
- [x] REQ-P23-03 Determinism recipe proven: vendored OFL font registered via
  font_manager, `svg.fonttype: path`, `svg.hashsalt`, metadata date stripped,
  pinned matplotlib recorded in the manifest — verified by a double-render
  hash-equality test kept off the gate path (skipIf matplotlib absent);
  `test_gate_path_hermetic` stays true.
- [x] REQ-P23-04 A per-chart-type snippet catalog that imports the helper and
  routes to finding codes — snippets never restate gate thresholds.
- [x] REQ-P23-05 WCAG AA contrast-verified palettes ship in the style files
  with per-palette citations; any palette *gate* defers with a D-13 entry
  condition.

## Phase 24 — Portfolio exemplar and viz calibration

- [x] REQ-P24-01 One end-to-end portfolio exemplar: question → ANALYSIS-SPEC →
  tests via the v2.3 catalog → figures via the style layer → sealed
  FIGURE-MANIFEST → What/So What/Now What narrative → REPRO-REPORT — passing
  every gate at ship threshold.
- [x] REQ-P24-02 Known-bad chart-choice fixtures per new code; catch rate and
  FPR re-baselined.
- [x] REQ-P24-03 Milestone audit prerequisites: catalogue current, snapshots
  unmutated, doc/code agreement tests green for both selection surfaces
  (test-selection.md and chart-selection.md).
