---
phase: 13-task-playbooks-that-fill-the-spec
plan: 02
subsystem: skills
tags: [dsx, skill, playbook, root-cause, segment, routing, multiplicity, simpson-paradox, causal-guard]

# Dependency graph
requires:
  - phase: 13-task-playbooks-that-fill-the-spec (plan 01)
    provides: capability.json registration of dsx-root-cause and dsx-segment skill names (single writer)
provides:
  - "skills/dsx-root-cause/SKILL.md — router for diagnostic 'why did X move' questions to DSX-MET-030/031 and the causal guard"
  - "skills/dsx-segment/SKILL.md — router for multi-cut segmentation questions to DSX-SPEC-043/DSX-EXP-050..053 and DSX-MET-030/031"
affects: [13-05 (catalogue set-identity diff certifies both files add zero DSX-* codes)]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Route-and-cite skill authoring: name the ANALYSIS-SPEC field + the DSX-* code that adjudicates it, never restate the gate's numeric rule (D-02)"

key-files:
  created:
    - skills/dsx-root-cause/SKILL.md
    - skills/dsx-segment/SKILL.md
  modified: []

key-decisions:
  - "Followed the house structure established by the sibling plan 13-01 (dsx-cohort, dsx-funnel): objective / when_to_reach_for_this / field_to_gate_routing table / a topic-specific section / what_this_skill_does_not_do — for consistency across all four new playbooks."
  - "dsx-root-cause's topic-specific section is split into two: decomposition_body (points at EDA 5B, does not restate it) and causal_guard (explains why DSX-CAU-001/010 and DSX-COH-001/010 exist and what wording they forbid) — the plan's Task 1 action named both concerns distinctly enough to warrant separate sections rather than merging them."
  - "dsx-segment's correction field is named but zero correction-method names (bonferroni/holm/benjamini/fdr/sidak) appear anywhere in the file — sidesteps the correction-method half of D-02 entirely rather than trying to attribute a method name to a DSX- line."
  - "Both files carry zero numeric-threshold-shaped prose (no percentages, no decimal comparisons, no p-value syntax, no alpha) — same technique 13-01 used successfully, so the KNOWN VERIFY-BLOCK NIT flagged in the task brief (grep -q 'DSX-\\|.' over-matching any non-empty line) never triggers: the anti-parallel-advice pipeline output was empty for both files, and the literal <verify> blocks as written in PLAN.md passed without needing the acceptance-aligned rewrite."

patterns-established:
  - "Router SKILL.md files for the DSX playbook family carry a field_to_gate_routing table (spec field | what it looks like | existing gate) as their structural core, with a dedicated 'what_this_skill_does_not_do' closing section that explicitly disclaims authoring any threshold."

requirements-completed: [REQ-P13-01]

coverage:
  - id: D1
    description: "skills/dsx-root-cause/SKILL.md exists with house frontmatter and routes question_type: diagnostic, results.segments {name,effect,n} to DSX-MET-030/031, and the causal-honesty guard to DSX-CAU-001/010 and DSX-COH-001/010"
    requirement: REQ-P13-01
    verification:
      - kind: other
        ref: "grep -q '^name: dsx-root-cause' && grep -q diagnostic && grep -q DSX-MET-030 && grep -q dsx-explore-data skills/dsx-root-cause/SKILL.md"
        status: pass
      - kind: other
        ref: "anti-parallel-advice grep (grep -hEi '(p ?[<>=]|\\balpha\\b|α|[0-9]+ ?%|[<>]=? ?0?\\.[0-9]|\\bbonferroni\\b|\\bholm\\b|\\bbenjamini\\b|\\bfdr\\b|\\bsidak\\b)' skills/dsx-root-cause/SKILL.md | grep -v 'DSX-') returns zero lines"
        status: pass
    human_judgment: false
  - id: D2
    description: "skills/dsx-segment/SKILL.md exists with house frontmatter and routes design.multiplicity.family[]+correction, results.segments, results.comparisons_looked_at to DSX-SPEC-043, DSX-EXP-050..053, and DSX-MET-030/031, naming the correction field without prescribing a method"
    requirement: REQ-P13-01
    verification:
      - kind: other
        ref: "grep -q '^name: dsx-segment' && grep -q DSX-SPEC-043 && grep -q DSX-EXP-050 && grep -q design.multiplicity.family skills/dsx-segment/SKILL.md"
        status: pass
      - kind: other
        ref: "anti-parallel-advice grep (grep -hEi '(p ?[<>=]|\\balpha\\b|α|[0-9]+ ?%|[<>]=? ?0?\\.[0-9]|\\bbonferroni\\b|\\bholm\\b|\\bbenjamini\\b|\\bfdr\\b|\\bsidak\\b)' skills/dsx-segment/SKILL.md | grep -v 'DSX-') returns zero lines"
        status: pass
    human_judgment: false

# Metrics
duration: ~10min
completed: 2026-08-28
status: complete
---

# Phase 13 Plan 02: dsx-root-cause and dsx-segment router playbooks Summary

**Two new SKILL.md router playbooks — dsx-root-cause routes diagnostic decomposition to DSX-MET-030/031 and the causal-honesty guard (DSX-CAU-001/010, DSX-COH-001/010); dsx-segment routes multi-cut segmentation to the multiplicity gate (DSX-SPEC-043, DSX-EXP-050..053) — both citing existing gates with zero authored thresholds.**

## Performance

- **Duration:** ~10 min
- **Completed:** 2026-08-28T15:29:25-03:00
- **Tasks:** 2
- **Files modified:** 2 (both new)

## Accomplishments
- `skills/dsx-root-cause/SKILL.md` created: routes `question_type: diagnostic` and `results.segments {name,effect,n}` to `DSX-MET-030`/`DSX-MET-031`, points at `dsx-explore-data` branch 5B for the decomposition body instead of restating it, and holds diagnostic wording to `DSX-CAU-001`/`DSX-CAU-010`/`DSX-COH-001`/`DSX-COH-010` so a diagnostic finding cannot silently upgrade itself to a causal claim.
- `skills/dsx-segment/SKILL.md` created: routes `design.multiplicity.family[]`+`correction` to `DSX-SPEC-043` and `DSX-EXP-050`/`051`/`052`/`053`, routes `results.segments`/`results.comparisons_looked_at` to `DSX-MET-030`/`031` and `DSX-EXP-051`, and reuses the existing candidate→confirmatory promotion handshake from `dsx-explore-data` rather than inventing a second one.
- Both files pass the D-02 anti-parallel-advice grep with zero output — neither file states a numeric threshold, p-value comparison, alpha, percentage, or correction-method name anywhere, attributed or not.

## Task Commits

Each task was committed atomically:

1. **Task 1: Author skills/dsx-root-cause/SKILL.md as a router to the diagnostic + Simpson gates** - `e5e9a98` (feat)
2. **Task 2: Author skills/dsx-segment/SKILL.md as a router to the multiplicity + Simpson gates** - `7c27aef` (feat)

_No TDD tasks in this plan (pure markdown authoring)._

## Files Created/Modified
- `skills/dsx-root-cause/SKILL.md` - New router playbook for diagnostic "why did X move" questions
- `skills/dsx-segment/SKILL.md` - New router playbook for multi-cut segmentation questions

## Decisions Made
- Mirrored the exact structural pattern the sibling plan 13-01 established for `dsx-cohort`/`dsx-funnel` (objective / when_to_reach_for_this / field_to_gate_routing table / topic section / what_this_skill_does_not_do) for cross-playbook consistency, even though the plan's `<action>` prose did not mandate that exact section layout — Claude's Discretion per 13-CONTEXT.md covers prose/section ordering.
- Split dsx-root-cause's routing explanation into two sections (`decomposition_body` pointing at EDA 5B, `causal_guard` explaining the DSX-CAU-*/DSX-COH-001/010 boundary) rather than one, since the plan named these as two distinct concerns (mirror-not-rewrite vs. causal-honesty).
- Avoided naming any correction method (bonferroni/holm/benjamini/fdr/sidak) anywhere in `dsx-segment/SKILL.md`, rather than naming one and attributing it to a DSX- line — simpler and unambiguously inside the D-02 boundary.

## Deviations from Plan

None — plan executed exactly as written. The KNOWN VERIFY-BLOCK NIT flagged in the orchestrator's brief (the literal `<verify>` block's second grep, `grep -q 'DSX-\|.'`, over-matches any non-empty line, which could false-fail a threshold correctly attributed to a `DSX-*` code on the same line) did not trigger for either file: both files were authored with zero threshold-shaped prose at all (no percentages, no decimal comparisons, no p-value syntax, no alpha, no correction-method names), so the anti-parallel-advice grep pipeline's intermediate output was empty before the final `grep -q` step ever ran. The literal `<verify>` blocks exactly as written in `13-02-PLAN.md` were run unmodified and both passed (exit 0) — no acceptance-aligned rewrite was needed.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- All four Phase 13 REQ-P13-01 skills now exist: `dsx-cohort`, `dsx-funnel` (13-01), `dsx-root-cause`, `dsx-segment` (this plan). All four are registered by name in `capabilities/dsx/capability.json` (13-01, single writer) and none is loop-wired.
- No path under `dsx/` was touched; no new `DSX-*` finding code was minted by this plan (markdown-only, catalogue generator only walks `dsx/**/*.py`). This plan does not itself run the phase-wide catalogue set-identity diff — that is plan 13-05's job, certifying the whole phase at once.
- `capabilities/dsx/capability.json` was not touched by this plan (confirmed via `git diff` against both new commits) — 13-01 remains the sole writer as instructed.
- Ready for the remaining Phase 13 plans (hypothesis register, narrate shape, tier routing, executor fragment, and the 13-05 catalogue set-identity gate).

---
*Phase: 13-task-playbooks-that-fill-the-spec*
*Completed: 2026-08-28*

## Self-Check: PASSED

- FOUND: skills/dsx-root-cause/SKILL.md
- FOUND: skills/dsx-segment/SKILL.md
- FOUND: .planning/phases/13-task-playbooks-that-fill-the-spec/13-02-SUMMARY.md
- FOUND: e5e9a98 (Task 1 commit)
- FOUND: 7c27aef (Task 2 commit)
