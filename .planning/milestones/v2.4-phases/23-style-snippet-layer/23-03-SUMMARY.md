---
phase: 23-style-snippet-layer
plan: 03
wave: 3
status: complete
requirements:
  - REQ-P23-04
completed: 2026-09-03
---

# 23-03 SUMMARY — per-function snippet catalog (route-to-codes) + skill wiring + phase-close zero-mint

Wave 3 of 3, Phase 23 (S3-3). Executed **inline by the orchestrator** (persona-lite,
S1-3/S2-3/23-01/23-02 precedent: the plan left no irreversible design judgment — the routing
test is the oracle; every gate is re-run by the orchestrator on the final clean tree; STATE is
single-writer, so no subagent touches it). TDD RED→GREEN→prove. Consumes Wave 2's
`templates/dsx_plotstyle.py` helper and Phase 22's `references/chart-catalog.md`. **This wave
completes S3-3 (all three Phase-23 plans executed).**

## What shipped

- **`references/chart-snippets.md`** (new) — a per-function cookbook. Opens with a provenance
  note (it **describes/demonstrates, does not adjudicate**; the gate reads `dsx/checks/*.py`,
  never this file — mirrors `chart-catalog.md`'s stance). A **Sealing-workflow** section wires
  `save_deterministic` → `dsx seal <path>` → `spec.visuals[].svg_sha256` (the GA-2 single-hasher
  flow, with `metadata={'Date': None}` explained as required, not optional). Then **one worked
  snippet per Function-axis category** (ten): Change over Time (`line` + `direct_label`),
  Magnitude (`bar`), Distribution (`histogram`), Correlation (`scatter`), Ranking (`bump`),
  Part-to-whole (`pie`), Deviation (`diverging_bar`), Flow (`sankey`), Spatial (`choropleth`),
  Uncertainty (`error_bars`). Each snippet imports `finalise_figure` + `save_deterministic`,
  calls `finalise_figure(title=<takeaway>, source=<dataset, period>)` then
  `save_deterministic(fig, path, metadata={'Date': None})`, and ends with a **"Gate-enforced:"
  line that routes to the governing finding codes BY NAME**. Every representative mark is a live
  `dsx_admissible` mark verified against `chart-catalog.md`.
- **`skills/dsx-visualize/SKILL.md`** (edit) — `@references/chart-snippets.md` added to the
  `<references>` block (alongside chart-catalog / chart-selection / data-input-types /
  viz-smells). Nothing else in the skill changed.
- **`tests/test_snippet_catalog_routing.py`** (new, 2 methods) — the repo-integrity oracle,
  off the gate path (reads Markdown; no `report.add`; `tests/` is never in `GATE_PROFILES`).

## Route-not-restate (D-P23-04) — the load-bearing constraint

- **Cited codes exist.** `test_cited_codes_are_all_defined` parses every `DSX-<FAMILY>-<n>`
  token from `chart-snippets.md` and asserts the set is **non-empty and ⊆** the codes defined in
  `references/finding-codes.md` (parsed with the CRLF-safe `_ROW_RE` reused from
  `test_finding_catalogue_invariant.py`). A mistyped/invented code turns it red (T-23-08).
- **No threshold restated.** `test_no_snippet_restates_a_live_viz_threshold` imports
  `MAX_PIE_SLICES` and `MAX_CATEGORICAL_COLORS` **LIVE** from `dsx.checks.viz` and builds the
  forbidden-restatement regexes **from those integers at runtime** — the numbers are never typed
  into the test (that live derivation is the non-vacuity anchor; if `viz.py` changes a limit the
  guard tracks it, T-23-06). Accordingly the pie section cites **DSX-VIZ-040** and the
  categorical-colour guidance cites **DSX-VIZ-050** by name, with the constraint described
  qualitatively and **neither maximum written** anywhere in the catalog.

## Gates (orchestrator-run, clean tree — DECISIONS.jsonl strays swept per standing note)

- **RED confirmed first:** both routing methods failed on file-absence (imports resolved,
  `finding-codes.md` parsed → not a test bug); no assertion softened.
- `tests.test_snippet_catalog_routing` — **2 OK** (GREEN): cited ⊆ defined (non-empty); no live
  threshold restated.
- Section + wiring check — **all 10 Function-axis sections present; `references/chart-snippets.md`
  wired into the skill `<references>`**.
- `python scripts/gen-finding-catalogue.py --check` — **exit 0, catalogue current @276** (zero
  mint; same 4 pre-existing "declared twice" warnings, unchanged).
- `tests.test_finding_catalogue_invariant` — **2 OK**: the count invariant (276 two ways) and
  the set-identity diff (`current_set == snapshot ∪ _MINTED_CODES`).
- **Full suite (clean tree): 1507 OK, 41.3s** (1505→1507, +2 = the two new routing methods).

## Zero mint — the phase-close 276 → 276 set-identity

Phase 23 mints **zero** finding codes (D-P23-04). Proof, exactly as Phase 21 recorded 275→275:
the mint surfaces (`references/finding-codes.md`, `scripts/gen-finding-catalogue.py`,
`tests/test_finding_catalogue_invariant.py`) are **unedited** (confirmed via `git status`), the
set-identity diff shows **added={}, removed={}** (`current_set` equals the frozen Phase-12
snapshot ∪ the sanctioned mints, `_EXPECTED_TOTAL = 276`), and `gen --check` exits 0.
**276 → 276.**

## REQ-P23-01..05 → green automated test (whole-phase coverage)

| Req | Behaviour | Test (green) |
|-----|-----------|--------------|
| REQ-P23-01 | `.mplstyle` license/attribution headers | `tests.test_style_headers` (Wave 1) |
| REQ-P23-05 | WCAG-AA palette contrast | `tests.test_style_wcag_contrast` (Wave 1) |
| REQ-P23-02 | `finalise_figure`/`direct_label`/`save_deterministic` signatures + mandatory `source` | `tests.test_dsx_plotstyle_api` (Wave 2) |
| REQ-P23-03 | double-render byte-identical SVG (off gate path) | `tests.test_dsx_plotstyle_determinism` (Wave 2) |
| REQ-P23-03 | matplotlib stays off the gate path | `tests.test_gate_path_hermetic` (`FORBIDDEN += matplotlib`, Wave 2) |
| REQ-P23-04 | snippets route to existing codes; no threshold restated | `tests.test_snippet_catalog_routing` (this wave) |
| REQ-P23-05 / D-P23-04 | catalogue set-identity 276 → 276 | `tests.test_finding_catalogue_invariant` + `gen --check` |

## Boundary

S3-3 is now **COMPLETE** (all three plans executed). Next unit is **S3-4** (code review +
verification, opus/high) — which must show the off-gate-path double-render determinism test
green per REQ-P23-03 — a separate unit for a fresh firing.
