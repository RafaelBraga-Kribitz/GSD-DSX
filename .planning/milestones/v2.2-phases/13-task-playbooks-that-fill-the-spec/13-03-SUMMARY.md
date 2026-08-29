---
phase: 13-task-playbooks-that-fill-the-spec
plan: 03
type: execute
status: complete
requirements: [REQ-P13-02, REQ-P13-03]
files_modified:
  - skills/dsx-explore-data/SKILL.md
  - skills/dsx-narrate/SKILL.md
---

# 13-03 Summary — hypothesis register + What/So What/Now What shape

Two prompt-guidance edits to existing skills. Both ride existing carriers and
existing finding codes; neither mints a code, adds a check, or adds a schema field.

## Task 1 — dsx-explore-data hypothesis register (REQ-P13-02, D-03)

Added a `## Hypothesis register` subsection inside the existing `<registers>` block
(after §11 Comparisons ledger). It states the deterministic mapping rule keyed on
shape, over the EXISTING carriers:

- An untested belief the analysis rests on → an `assumptions[]` row
  (`{assumption, rationale, impact_if_wrong, checked, waiver}`), adjudicated by
  `DSX-COH-030` (present-when-causal/prescriptive) and `DSX-COH-031`
  (each row `checked: true` XOR `waiver`).
- A belief promoted to a confirmatory test → declared in
  `design.multiplicity.family[]` at scope, filled in `results.tests[]` at execute,
  adjudicated by `DSX-EXP-050..053`.

The "register" is the existing EDA.md ledgers; promotion reuses the §6 step-4
candidate handshake (spec amendment via `dsx-scope-analysis`; "EDA never promotes a
candidate into `decision.replay`" preserved). No new spec field.

## Task 2 — dsx-narrate What/So What/Now What shape (REQ-P13-03, D-04)

Added one paragraph to the existing five-part `<structure>` mapping the three-part
shape onto the existing sections: **What** = §1 the answer; **So What** = §2 what it
means / the pre-declared decision-rule action; **Now What** = §4 what would change
it, citing the gate-read `decision.revisit_when` (`DSX-COH-040`) and non-empty
`limitations[]` (`DSX-CLM-080`). Template-only: no new `DSX-NAR` code, no
heading-scanner gate.

## Gate evidence (re-run by orchestrator)

- Task 1 verify block: **PASS** — grep hits for `assumptions`, `DSX-COH-031`,
  `DSX-EXP-05`, `results.tests`, `decision.replay`.
- Task 2 verify block: **PASS** — grep hits for `So What`, `Now What`,
  `DSX-COH-040`, `DSX-CLM-080`, `revisit_when`; distinct `DSX-NAR-*` codes = **1**
  (`DSX-NAR-030` only).
- Scope fence: `git status --porcelain` shows only the two SKILL.md files modified;
  nothing under `dsx/`; no new `DSX-*` code (markdown edits only — the generator
  walks `dsx/**/*.py`). Phase-wide zero-mint certified by plan 13-05.

## Prohibitions honored

- Zero new `DSX-*` codes (catalogue stays 256; certified by 13-05 set-identity diff).
- No edit to the deterministic `dsx` gate path (no path under `dsx/` touched).
- No new schema field; routes to existing `assumptions[]` / `results.tests` /
  `design.multiplicity.family` carriers and the existing EDA.md ledgers.
