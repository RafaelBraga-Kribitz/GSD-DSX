# Roadmap

## Phase 1 — DQ + Evidence + Coherence (v1.1.0) — COMPLETE

**Dimensions strengthened:** 1 (Analytical Question), 4 (Missing Evidence), 5 (Data Quality)

- `DATA-PROFILE.yaml` contract + `dsx profile` CSV runner (stdlib)
- Hermetic `DSX-DQ-*` gates against assertions ↔ profile
- Evidence pointer resolution (`DSX-CLM-031`–`033`)
- Question ↔ claim ↔ decision coherence (`DSX-COH-*`)
- Skill/fragment updates; fixtures; catalogue; tests

## Phase 2 — Viz proof + plot construction (v1.2.0) — COMPLETE

**Dimensions:** 3 (Chart Type), 8 (Plot Construction), 9 (Visual Design)

- Chart_Audit Gate A–D ordering in verifier fragment
- `DSX-SMELL-*` from code smells B/G/I/J/K/M; richer `visuals[]` fields
- Figure manifest + `svg_sha256` (`DSX-FIG-*`); `dsx seal`
- Hermetic Glyph-ready seals when `renderer: glyph` (no live MCP)
- `data_input_type` × chart capability matrix
- Takeaway heuristics (≠ name; digit/comparison)

## Phase 3 — Storytelling + code reality (v1.3.0) — COMPLETE

**Dimensions:** 6 (Code Quality), 10 (Communication / Storytelling)

- Narrative deliverable path; `%` without base lint; limitations required
- Forbidden-claim SSOT regexes (universal + optional phase file)
- Entrypoint smell scan; require `metric.sql` for warehouse sources
- Broader SQL anti-patterns; optional `dashboard:` for BI

## Phase 4 — Analytical logic depth + stats extensions (v1.4.0) — COMPLETE

**Dimensions:** 2 (Analytical Logic), 7 (Statistical Issues extensions)

- Causal assumption checkoffs / waivers (`DSX-COH-031`)
- Null-as-no-effect requires TOST/CI-in-bounds or detectable MDE (`DSX-STA-020`/`021`)
- Exploratory comparison count vs multiplicity family (`DSX-EXP-051`/`052`)
- `repro_lock` honest-null pattern (`DSX-REP-050`–`053`)
- Decision replay against `results.tests` (`DSX-DEC-*`)
- Metric reconciliation class tolerances (`DSX-MET-012` + class defaults)

## Phase 5 — Chart review + suppressions (v1.5.0) — COMPLETE

**Dimensions:** Chart Audit residual (scored review artifact, ADR suppressions)

- ANALYSIS-SPEC `suppressions[]` with reason + authority; unknown codes → exit 2
- `DSX-SPEC-070`–`072` for malformed/unknown suppressions
- `templates/CHART-REVIEW.md` + `references/chart-review-schema.md` (`dsx-chart-review-v1`)
- `dsx-viz-critic` writes CHART-REVIEW.md; skill `dsx-chart-audit` for standalone runs
