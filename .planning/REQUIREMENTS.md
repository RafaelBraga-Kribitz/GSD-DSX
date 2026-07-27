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

## Phase 2–4

Tracked in ROADMAP.md; not in scope until explicitly started.
