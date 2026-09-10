---
phase: 26-per-skill-read-contracts
plan: 03
subsystem: repo-integrity
tags: [repo-integrity, tdd, guard, off-gate-path]
requires:
  - 26-01  # scope-analysis, define-metrics, design-experiment <inputs> blocks
  - 26-02  # build-model, narrate <inputs> blocks
provides:
  - tests/test_skill_read_contracts.py  # the anti-silent-orphan guard (REQ-P26-02)
affects:
  - templates/EDA.md            # read-only ground truth (byte-unchanged)
  - templates/DATA-PROFILE.yaml # read-only ground truth (byte-unchanged)
  - skills/dsx-*/SKILL.md        # <inputs> blocks validated (byte-unchanged)
tech-stack:
  added: []           # stdlib only (re, unittest, pathlib) — no new dependency
  patterns:
    - "stdlib line-oriented indent-stack YAML key-path extractor (no PyYAML)"
    - "uncomment pre-processor to recover commented example keys"
    - "full dotted-path set-membership (leaf-only matching rejected)"
    - "in-file negative control + anti-vacuity anchors"
key-files:
  created:
    - tests/test_skill_read_contracts.py
  modified: []
key-decisions:
  - "Push a key onto the indent stack only when its value is empty (potential block parent); scalars / scalar-lists / flow-maps never become parents. Keeps the fully-commented unit:/target: blocks — whose headers uncomment to indent 2 — at the document root instead of nesting under the preceding top-level scalar sentinels_found."
  - "Membership test is bidirectional: each skill's live <inputs> keys must equal the ratified D-26-02 matrix AND each key must exist in the live template key set — so both a skill-side rename and a template-side rename fail the suite."
requirements-completed: [REQ-P26-02]
coverage:
  - deliverable: "Off-gate-path repo-integrity guard: every EDA/DATA-PROFILE key named in the five skills' <inputs> blocks exists in the live templates"
    verification:
      - kind: test
        ref: "tests/test_skill_read_contracts.py#test_skill_keys_are_members_of_live_templates"
        status: pass
      - kind: test
        ref: "tests/test_skill_read_contracts.py#test_negative_control_orphan_key_is_rejected"
        status: pass
      - kind: test
        ref: "tests/test_skill_read_contracts.py#test_anchor_non_vacuity"
        status: pass
    human_judgment: false
  - deliverable: "Each of the five skills carries exactly one <inputs> block with >=1 populated key region; fallback line records eda_artifact: none; Also-consult lines carry zero backticks"
    verification:
      - kind: test
        ref: "tests/test_skill_read_contracts.py#test_every_skill_carries_at_least_one_key_region"
        status: pass
      - kind: test
        ref: "tests/test_skill_read_contracts.py#test_when_absent_names_eda_artifact_none"
        status: pass
      - kind: test
        ref: "tests/test_skill_read_contracts.py#test_also_consult_line_has_zero_backticks"
        status: pass
    human_judgment: false
  - deliverable: "Parser is CRLF-tolerant, deterministic, and order-independent across both templates (one CRLF, one bare-LF)"
    verification:
      - kind: test
        ref: "tests/test_skill_read_contracts.py#test_parse_is_deterministic_and_order_independent"
        status: pass
    human_judgment: false
  - deliverable: "Skill-only invariant: dsx/, templates/, skills/ byte-unchanged; no yaml/dsx imports"
    verification:
      - kind: command
        ref: "git diff --stat -- dsx/ templates/ skills/ (empty)"
        status: pass
      - kind: command
        ref: "grep -c 'import yaml' tests/test_skill_read_contracts.py == 0; no from/import dsx"
        status: pass
    human_judgment: false
duration: ~20 min
completed: 2026-09-07
status: complete
---

# Phase 26 Plan 03: Skill read-contract guard (RED/GREEN) Summary

A stdlib-only off-gate-path `unittest` guard (`tests/test_skill_read_contracts.py`) that
parses the live `templates/EDA.md` (CRLF) and `templates/DATA-PROFILE.yaml` (bare-LF) into
full dotted-path key sets and asserts every key named in the five downstream skills'
`<inputs>` blocks resolves — so a renamed or fabricated template key FAILS the suite instead
of silently orphaning a read step. Built test-first: RED (parser stubs raise) then GREEN
(indent-stack key-path extractor with an uncomment pre-processor).

## Metrics

- Duration: ~20 min
- Tasks: 2/2 (RED, GREEN)
- Files created: 1 (`tests/test_skill_read_contracts.py`)
- Files modified (production): 0
- Tests added: 7 methods; full suite 1583 → 1590, all OK
- EDA key set: 50 keys; DATA-PROFILE key set: 47 keys

## Accomplishments

1. **RED (commit `915e62b`)** — `test(26-03)`. Wrote the full guard as failing tests with the
   five parser helpers (`_lines`, `parse_eda_keys`, `parse_profile_keys`,
   `extract_inputs_block`, `extract_key_region`) stubbed to raise `NotImplementedError`.
   All 7 tests errored (exit 1) — the RED lever. Module docstring states the CORRECTED
   rationale from 26-RESEARCH.md (comments are invisible to every YAML parser; PyYAML is an
   optional dependency in this repo — not "won't load"), the `\r?\n` CRLF discipline (EDA.md
   CRLF, DATA-PROFILE.yaml bare-LF, verified live), the `column_name` single-placeholder-token
   note (residual #5), and the off-gate-path note.

2. **GREEN (commit `3d60f63`)** — `feat(26-03)`. Implemented the indent-stack extractor:
   records every intermediate dotted path (not leaves only), marks list-of-map elements with
   `[]`, and matches full dotted paths (leaf-only matching rejected — proven necessary by the
   `overall`/`verdict` leaf collisions across `base_rate`/`target`/`grain`/`branch`). The
   DATA-PROFILE side uncomments each `#` example line first (`raw.replace("#", " ", 1)`,
   length-preserving), then strips trailing inline `# ...`, then normalizes
   `columns.column_name.*` → `columns[].*`. All 7 tests pass (exit 0); full suite 1590 OK.

3. **Anti-silent-orphan proof works.** Verified live that `base_rate.overall` is a member but
   bare `overall` is not, and a renamed-parent `baseline.overall` does not match — so a parent
   rename cannot be masked by a same-named leaf elsewhere (the exact failure REQ-P26-02
   forbids). `columns[].null_rate` is a member ONLY because the uncomment step ran.

## Deviations from Plan

**[Rule 1 - correctness] Empty-value-only stack push**
- **Found during:** Task 2 (GREEN) — the first parser implementation failed
  `test_skill_keys_are_members_of_live_templates` with `unit.rows_per_unit` resolving as
  `sentinels_found.unit.rows_per_unit`.
- **Issue:** 26-RESEARCH.md traced the uncomment indentation math only for the `columns:`
  block, where the block header (`columns:`) is a real, uncommented top-level key. The `unit:`
  and `target:` blocks are fully commented — their headers (`# unit:`, `# target:`) sit at
  column 0 and uncomment to **indent 2**, not 0. A naive push-every-key indent stack nested
  them under the preceding top-level scalar `sentinels_found: []`.
- **Fix:** Push a key onto the indent stack only when its value is empty (a potential block
  parent). Scalars, scalar-lists (`[]`, `[lo, hi]`), and flow-maps (`{ ... }`) are
  self-contained and never become parents, so an indent-2 block header with an empty stack
  resolves to the root. This is a correctness detail within D-26-04's "indent-stack +
  inline-flow awareness", not a design change — the mapping and contract are unchanged.
- **Files modified:** `tests/test_skill_read_contracts.py` (parser body only).
- **Verification:** all 7 tests pass; `unit.rows_per_unit`, `unit.largest_unit_share`,
  `target.overall`, `target.weekly_range`, `target.verdict` all resolve to the correct root
  paths; EDA/DATA-PROFILE counts (50/47) unchanged in structure.
- **Commit:** `3d60f63` (part of the GREEN commit).

**Total deviations:** 1 auto-fixed (1 correctness). **Impact:** none on scope — the fix lives
entirely inside the new test file's parser; `dsx/`, templates, and skills are byte-unchanged.

## TDD Gate Compliance

- RED gate: `test(26-03)` commit `915e62b` — suite exits non-zero (7 errors). ✓
- GREEN gate: `feat(26-03)` commit `3d60f63` — suite exits 0 (7 pass). ✓
- No REFACTOR commit: the GREEN implementation is cohesive (shared `_extract_paths` already
  factors the two parsers); no separate cleanup warranted.

## Verification Results

| Check | Command | Result |
|-------|---------|--------|
| RED gate | `python -m unittest tests.test_skill_read_contracts -v` (at `915e62b`) | exit 1, `FAILED (errors=7)` |
| GREEN gate | `python -m unittest tests.test_skill_read_contracts -v` (at `3d60f63`) | exit 0, `OK` (7 tests) |
| Full suite | `python -m unittest discover -s tests -q` | `Ran 1590 tests ... OK` |
| No yaml import | `grep -c "import yaml" tests/test_skill_read_contracts.py` | `0` |
| No dsx import | `grep -nE "(from dsx|import dsx)"` | none |
| Skill-only invariant | `git diff --stat -- dsx/ templates/ skills/` | empty |

## Notes for the Orchestrator

- **Single-writer files untouched:** `.planning/REQUIREMENTS.md`, `.planning/STATE.md`,
  `.planning/ROADMAP.md` were NOT edited (per plan + project CLAUDE.md). REQ-P26-02 is
  satisfied and ready for the orchestrator to mark complete.
- **Not pushed** — per instruction, the orchestrator reconciles and pushes.
- **Phase-end reminders (not in this plan's scope, flagged forward):** REQ-P26-03's
  `node install.mjs && node install.mjs --check` re-sync and the 276→276 catalogue re-measure
  are phase-gate steps owned elsewhere, not this plan.

## Self-Check: PASSED

- `tests/test_skill_read_contracts.py` exists on disk. ✓
- Commit `915e62b` (RED) present in `git log`. ✓
- Commit `3d60f63` (GREEN) present in `git log`. ✓
- All 7 acceptance-criteria checks (both tasks) re-run and pass. ✓
