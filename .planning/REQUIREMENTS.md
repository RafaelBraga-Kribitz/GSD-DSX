# Requirements

## Phase 1 (v1.1.0) — complete

- [x] REQ-P1-01 Spec `data[]` supports `profile_path` and `assertions`
- [x] REQ-P1-02 `templates/DATA-PROFILE.yaml` documents the profile contract
- [x] REQ-P1-03 `dsx profile <csv>` writes a profile with `computed_by: dsx-profile` and `source_hash`
- [x] REQ-P1-04 `DSX-DQ-*` blocks execute/verify/ship when assertions disagree with the profile
- [x] REQ-P1-05 Evidence paths resolve on disk; `#anchor` must exist in markdown
- [x] REQ-P1-06 Claim numbers must overlap `results.tests` when tests are present
- [x] REQ-P1-07 Claim type cannot exceed `question_type` strength
- [x] REQ-P1-08 Causal verbs in `decision_rule` blocked when question is descriptive/diagnostic
- [x] REQ-P1-09 Experiments require MPE + `action_if_null`
- [x] REQ-P1-10 Causal/prescriptive questions require non-empty `assumptions` by ship
- [x] REQ-P1-11 Good fixture passes every gate; bad fixture blocks every gate
- [x] REQ-P1-12 Finding catalogue regenerated; tests green
- [x] REQ-P1-13 Capability/plugin version bumped to 1.1.0

## Phase 2 (v1.2.0) — complete

- [x] REQ-P2-01 `visuals[]` supports chart_id, data_input_type, artifact_path, svg_sha256, series_role, run_id
- [x] REQ-P2-02 `DSX-VIZ-013/014` enforce data_input_type × chart matrix
- [x] REQ-P2-03 `DSX-VIZ-063/064` takeaway heuristics
- [x] REQ-P2-04 `DSX-FIG-*` hermetic seals + `dsx seal`; FIGURE-MANIFEST coverage
- [x] REQ-P2-05 `DSX-SMELL-*` for B/G/I/J/K/M
- [x] REQ-P2-06 Verifier Gate A–D protocol; visualize skill + viz-critic updated
- [x] REQ-P2-07 Good/bad fixtures + SVG stubs; version 1.2.0; catalogue current

## Phase 3 (v1.3.0) — complete

- [x] REQ-P3-01 `narrative` / `dashboard` / claim `base_n`/`from_value`/`to_value` in ANALYSIS-SPEC
- [x] REQ-P3-02 `FORBIDDEN-CLAIMS.yaml` template + `references/narrative-discipline.md`
- [x] REQ-P3-03 `DSX-CLM-070` relative % without base; `DSX-CLM-080` limitations for causal|prescriptive|predictive
- [x] REQ-P3-04 `DSX-NAR-*` narrative path, claim⊆file, forbidden wording, dashboard path
- [x] REQ-P3-05 `DSX-SQL-007`–`014` + `DSX-MET-040` warehouse requires sql; timezone → `DSX-MET-041`
- [x] REQ-P3-06 `DSX-CODE-*` fit-before-split entrypoint scan; wired on execute/verify/ship
- [x] REQ-P3-07 Skills/agents/fragments updated (narrate, storyteller, build-model, define-metrics)
- [x] REQ-P3-08 Good/bad fixtures + tests; catalogue regen; version 1.3.0

## Phase 4 (v1.4.0) — complete

- [x] REQ-P4-01 Assumption `checked:true` XOR `waiver` at verify/ship (`DSX-COH-031`)
- [x] REQ-P4-02 Null-as-no-effect requires CI-in-bounds / TOST / `detectable_mde` (`DSX-STA-020`/`021`)
- [x] REQ-P4-03 `comparisons_looked_at` vs multiplicity family (`DSX-EXP-051`/`052`)
- [x] REQ-P4-04 `repro_lock` honest-null (`DSX-REP-050`–`053`)
- [x] REQ-P4-05 Structured `decision.replay` vs `results.tests` (`DSX-DEC-*`)
- [x] REQ-P4-06 Reconciliation class tolerances + `DSX-MET-012`
- [x] REQ-P4-07 Skills/agents/fragments + fixtures/tests; catalogue; version 1.4.0
