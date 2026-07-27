# Roadmap

## Phase 1 — DQ + Evidence + Coherence (v1.1.0) — COMPLETE

**Dimensions strengthened:** 1 (Analytical Question), 4 (Missing Evidence), 5 (Data Quality)

- `DATA-PROFILE.yaml` contract + `dsx profile` CSV runner (stdlib)
- Hermetic `DSX-DQ-*` gates against assertions ↔ profile
- Evidence pointer resolution (`DSX-CLM-031`–`033`)
- Question ↔ claim ↔ decision coherence (`DSX-COH-*`)
- Skill/fragment updates; fixtures; catalogue; tests

## Phase 2 — Viz proof + plot construction

**Dimensions:** 3 (Chart Type), 8 (Plot Construction), 9 (Visual Design)

- Chart_Audit Gate A–D ordering in verifier fragment
- `DSX-SMELL-*` from code smells A–M; richer `visuals[]` fields
- Figure manifest + `svg_sha256` (`DSX-FIG-*`)
- Glyph seal when `renderer: glyph`
- `data_input_type` × chart capability matrix
- Takeaway heuristics (≠ name; digit/comparison)

## Phase 3 — Storytelling + code reality

**Dimensions:** 6 (Code Quality), 10 (Communication / Storytelling)

- Narrative deliverable path; `%` without base lint; limitations required
- Forbidden-claim SSOT regexes
- Entrypoint smell scan; require `metric.sql` for warehouse sources
- Broader SQL anti-patterns; optional `dashboard:` for BI

## Phase 4 — Analytical logic depth + stats extensions

**Dimensions:** 2 (Analytical Logic), 7 (Statistical Issues extensions)

- Causal assumption checkoffs / waivers
- Null-as-no-effect requires TOST or detectable MDE
- Exploratory comparison count vs multiplicity family
- `repro_lock` honest-null pattern
- Decision replay against `results.tests`
- Metric reconciliation class tolerances
