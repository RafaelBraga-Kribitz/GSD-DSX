---
phase: 26-per-skill-read-contracts
plan: 01
subsystem: skill-contracts
tags: [skill-contracts, repo-integrity, eda]
requires: []
provides:
  - "dsx-scope-analysis/SKILL.md <inputs> read step (7 EDA + 6 DATA-PROFILE keys)"
  - "dsx-define-metrics/SKILL.md <inputs> read step (4 EDA + 5 DATA-PROFILE keys, prose-only Joins ref)"
  - "dsx-design-experiment/SKILL.md <inputs> read step (6 EDA + 4 DATA-PROFILE keys)"
affects:
  - "Wave-2 guard tests/test_skill_read_contracts.py (26-03) validates these three blocks"
tech-stack:
  added: []
  patterns:
    - "Visible <inputs> block, one backtick-wrapped key per bullet line (D-26-01)"
    - "Three-tier absent-artifact honesty ladder: eda_artifact: none -> DATA-PROFILE fallback -> computed_by declaration (D-26-03)"
    - "Prose-only EDA refs named as zero-backtick Also-consult lines, never machine-parsed keys (D-26-02)"
key-files:
  created: []
  modified:
    - skills/dsx-scope-analysis/SKILL.md
    - skills/dsx-define-metrics/SKILL.md
    - skills/dsx-design-experiment/SKILL.md
decisions:
  - "Every backtick key copied verbatim from templates/EDA.md front-matter or templates/DATA-PROFILE.yaml (incl. commented example keys); zero new keys invented"
  - "define-metrics carries a zero-backtick Also-consult line for section 1 Joins; scope-analysis and design-experiment omit it"
metrics:
  duration: "~6 min"
  completed: 2026-09-07
  tasks: 3
  files: 3
status: complete
---

# Phase 26 Plan 01: Per-skill read contracts (three skills) Summary

Added one visible `<inputs>` read-step block to the head of three downstream skills — `dsx-scope-analysis`, `dsx-define-metrics`, `dsx-design-experiment` — each naming the exact EDA front-matter and DATA-PROFILE keys it consumes, what those keys set in its output, and the `eda_artifact: none` three-tier fallback, byte-scoped to `skills/` only.

## What was built

| Skill | Insert point | EDA keys | DATA-PROFILE keys | Also-consult |
|---|---|---|---|---|
| dsx-scope-analysis | between `</objective>` and `<process>` | 7 (`grain.verdict`, `grain.implied_dependence.structure`, `grain.implied_dependence.cluster_var`, `missingness[]`, `base_rate.verdict`, `contradictions`, `stop_triggered`) | 6 (`primary_key_unique`, `duplicate_rate`, `unit.rows_per_unit`, `unit.largest_unit_share`, `columns[].null_rate`, `target.verdict`) | none |
| dsx-define-metrics | between `</objective>` and `<definition_contract>` | 4 (`grain.declared`, `grain.observed`, `grain.verdict`, `grain.duplicate_rate`) | 5 (`primary_key`, `primary_key_unique`, `duplicate_rate`, `columns[].n_unique`, `columns[].dtype`) | section 1 Joins (zero backticks) |
| dsx-design-experiment | between `</objective>` and `<design_mode>` | 6 (`dependence.icc`, `dependence.outcome_sd`, `dependence.weekly_cycle_amplitude`, `base_rate.overall`, `grain.implied_dependence.structure`, `grain.implied_dependence.cluster_var`) | 4 (`target.overall`, `target.weekly_range`, `unit.rows_per_unit`, `unit.largest_unit_share`) | none |

Each block: bold "Read `EDA.md` front-matter first when it exists" clause with a one-clause reason, one backtick key per bullet in each region, a "These set:" prose line, and a "When absent:" line following D-26-03's `eda_artifact: none` -> DATA-PROFILE -> `computed_by` ladder. `dependence.weekly_cycle_amplitude` written with its full dotted path.

## Key verification

All backtick keys resolve verbatim against the live templates (per-key line references, verified this firing):
- EDA front-matter (`templates/EDA.md`): `grain.*` L26-37, `missingness[]` L39, `base_rate.overall/verdict` L51/L53, `dependence.icc/outcome_sd/weekly_cycle_amplitude` L67-69, `stop_triggered` L75, `contradictions` L76.
- DATA-PROFILE (`templates/DATA-PROFILE.yaml`): `primary_key(_unique)` L44-45, `duplicate_rate` L46; commented example keys (valid after the guard's uncomment pre-processor) `columns[].null_rate/n_unique/dtype` L21-23, `unit.rows_per_unit/largest_unit_share` L62-63, `target.overall/weekly_range/verdict` L68/71/72.

Per-task `<verify>` python one-liners: all three passed EXIT=0. define-metrics Also-consult zero-backtick assertion passed.

Skill-only invariant: `git diff --stat -- dsx/ templates/` empty. Only the three `SKILL.md` files modified. Zero finding codes minted.

## Deviations from Plan

None — plan executed exactly as written. No branch created or switched (remained on `gsd/v2.6.0-exploration-depth`).

## Single-writer note

Per the single-writer prohibition, this executor did NOT edit `.planning/REQUIREMENTS.md`, `.planning/STATE.md`, or `.planning/ROADMAP.md`. REQ-P26-01 completion (three of five skills) is reported back to the orchestrator for serial write after the wave merges.

## Commits

- 8215fdf: feat(26-01): add `<inputs>` read step to dsx-scope-analysis
- 5d47e57: feat(26-01): add `<inputs>` read step to dsx-define-metrics
- 22b6d0b: feat(26-01): add `<inputs>` read step to dsx-design-experiment

## Self-Check: PASSED

- skills/dsx-scope-analysis/SKILL.md — modified, `<inputs>` block present, verify EXIT=0
- skills/dsx-define-metrics/SKILL.md — modified, `<inputs>` block present, verify EXIT=0
- skills/dsx-design-experiment/SKILL.md — modified, `<inputs>` block present, verify EXIT=0
- Commits 8215fdf, 5d47e57, 22b6d0b present in git log
- `git diff --stat -- dsx/ templates/` empty (skill-only invariant holds)
