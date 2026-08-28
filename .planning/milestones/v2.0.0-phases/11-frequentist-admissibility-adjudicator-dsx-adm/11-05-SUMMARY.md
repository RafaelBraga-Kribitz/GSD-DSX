---
phase: 11-frequentist-admissibility-adjudicator-dsx-adm
plan: 05
subsystem: infra
tags: [dsx, admissibility, ontology, alias-resolution, frequentist, python]

# Dependency graph
requires:
  - phase: 11-02
    provides: "ESTIMAND_TYPES closed vocabulary in dsx/spec.py and validity_frame.estimand.type populated on all nine committed specs"
  - phase: 11-03
    provides: "applies_to_frequentist_admissibility(spec) predicate in dsx/frame/paradigm.py, keeping the paradigm-scoping decision out of this module"
  - phase: 11-04
    provides: "references/families.yaml -- 14 cited frequentist family entries, 19-token cited assumption vocabulary, 4 cited ranking rules"
provides:
  - "dsx/frame/admissibility.py -- Family, RankingRule, Ontology, Resolution frozen dataclasses"
  - "load_ontology() -- refuses (CheckError) rather than degrades on a missing/malformed families.yaml; drops uncited family entries at load (run-time half of D-24); caches by resolved path"
  - "alias_index(ontology) -- (estimand, dependence) -> {normalized alias: family id}, raising CheckError on a same-pair alias collision"
  - "candidate_families(ontology, estimand, dependence) -- axis-matched families, sorted once lexicographically by id"
  - "declared_procedure(spec) -- guarded read of the declared primary procedure label, never as a single dotted-path string"
  - "resolve_declared_procedure(ontology, estimand, dependence, declared) -- four distinguishable outcomes (not_declared, in_candidate_set, outside_candidate_set, unresolved), exact-match only, no fuzzy/distance/containment resolution anywhere"
affects: [11-06, 11-07, 11-08]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Ontology data is read exclusively through dsx.loader.load() and coerced into frozen dataclasses with tuple sequence fields at load time, so the cached singleton can never be mutated by a caller."
    - "The declared-procedure field is read as spec.get(\"inference\") then a plain .get() on the resulting mapping -- never as one combined dotted-path string -- because a positional call-argument string literal beginning with the block name followed by a dot is exactly what tests/test_frame_boundary.py's AST detector flags on any call in any dsx/frame/ module."
    - "Every string comparison in the resolver is equality after dsx.spec.normalize(); no distance, containment or prefix match exists anywhere in the module (D-18)."

key-files:
  created:
    - dsx/frame/admissibility.py
    - tests/test_frame_admissibility.py

key-decisions:
  - "alias_index()'s collision error names the normalized alias key (not the raw, un-normalized alias string as authored on whichever family happened to be visited second) -- the normalized form is the actual value that collided, and naming it avoids a message that silently varies with which of two differently-cased spellings the ontology author used."
  - "declared_procedure() uses dsx.spec.is_blank_text() (not is_blank()) for the blank-primary_procedure check, because is_blank_text() already encodes exactly the required semantics -- 'blank unless it is a non-empty string' -- as a single existing helper, matching the project's one-helper-per-predicate convention rather than reimplementing the check inline."
  - "resolve_declared_procedure()'s outside-candidate-set tie-break sorts candidate (pair, family_id) tuples by family_id via Python's default tuple comparison on the second element, matching the plan's instruction to take the lexicographically first family id when more than one other pair matches -- this is a function of the ontology's contents, never of dict iteration order."

requirements-completed: [REQ-P11-02]

coverage:
  - id: D1
    description: "load_ontology() loads references/families.yaml (14 families, 4 rules, 19 tokens) once, caches the result, and raises CheckError (never returns an empty catalogue) on a missing or structurally wrong file"
    requirement: "REQ-P11-02"
    verification:
      - kind: unit
        ref: "tests/test_frame_admissibility.py#TestLoadOntologyGoldenPath"
        status: pass
      - kind: unit
        ref: "tests/test_frame_admissibility.py#TestLoadOntologyMissingFile"
        status: pass
      - kind: unit
        ref: "tests/test_frame_admissibility.py#TestLoadOntologyStructuralErrors"
        status: pass
    human_judgment: false
  - id: D2
    description: "load_ontology() drops any family entry with a blank citation at load time (run-time half of D-24), recording the dropped id in Ontology.dropped_uncited, without raising -- including the all-uncited case, which returns zero families cleanly"
    requirement: "REQ-P11-02"
    verification:
      - kind: unit
        ref: "tests/test_frame_admissibility.py#TestLoadOntologyDroppedUncited"
        status: pass
    human_judgment: false
  - id: D3
    description: "A named test resolves into a family by exact, normalized match against that family's own aliases, scoped to the candidate set for the frame's (estimand, dependence) pair; an alias outside the pair and an alias found nowhere are two distinguishable outcomes; no fuzzy/distance/containment match exists anywhere"
    requirement: "REQ-P11-02"
    verification:
      - kind: unit
        ref: "tests/test_frame_admissibility.py#TestResolveDeclaredProcedure"
        status: pass
      - kind: unit
        ref: "tests/test_frame_admissibility.py#TestAliasIndex"
        status: pass
      - kind: unit
        ref: "tests/test_frame_admissibility.py#TestCandidateFamilies"
        status: pass
    human_judgment: false
  - id: D4
    description: "The module imports nothing from dsx.checks and never reads the declared inferential paradigm field, proven mechanically by both scanners in tests/test_frame_boundary.py"
    requirement: "REQ-P11-02"
    verification:
      - kind: unit
        ref: "tests.test_frame_boundary (10 tests, both directions and both paradigm-read detectors)"
        status: pass
    human_judgment: false

duration: ~30min (investigation + TDD implementation across 2 tasks, 4 commits)
completed: 2026-08-22
status: complete
---

# Phase 11 Plan 05: Frequentist Admissibility Loader and Alias Resolver Summary

**`dsx/frame/admissibility.py` -- a refuse-not-degrade ontology loader over `references/families.yaml` plus an exact-match, pair-scoped alias resolver with four distinguishable outcomes, built test-first across two RED/GREEN cycles with zero finding codes emitted.**

## Performance

- **Duration:** ~30 min of active work (context reading across ~15 files, two full RED/GREEN TDD cycles)
- **Tasks:** 2
- **Files modified:** 2 (`dsx/frame/admissibility.py` created, `tests/test_frame_admissibility.py` created)

## Accomplishments

- `dsx/frame/admissibility.py` created with `Family`, `RankingRule`, `Ontology` and `Resolution` frozen dataclasses (all sequence fields are tuples, so no caller can mutate the cached singleton).
- `load_ontology()` resolves `references/families.yaml` as a package sibling (`Path(__file__).resolve().parents[2] / "references" / "families.yaml"`), caches by resolved path string, and translates any `SpecParseError` (missing file, non-mapping top level) into `CheckError` naming the resolved path -- an installation defect is never reported as a defect in the analyst's frame.
- `load_ontology()` drops any family entry whose citation is blank or absent after stripping, recording the dropped id in `Ontology.dropped_uncited` (sorted) -- the run-time half of the two-sided D-24 citation enforcement. An all-uncited file returns zero families cleanly, without raising, because "nothing is admissible" is a real reportable state and a bad file is not.
- `alias_index()` builds `(estimand, dependence) -> {normalized alias: family id}` and raises `CheckError` naming both family ids and the colliding normalized alias the instant two families in the *same* pair declare the same alias -- never a silent last-one-wins that would make the answer depend on file order.
- `candidate_families()` matches both axes after `normalize()` and sorts its result exactly once, lexicographically by family id, so every downstream ordering (this plan's own tests, and the ranking plan 11-06 builds next) is a function of the candidate set, never of the ontology file's own entry order.
- `declared_procedure()` reads the declared primary-procedure label with `spec.get("inference")` then a plain `.get()` on the result -- never as one combined dotted-path string -- because that shape is exactly what the D-11 boundary scanner's AST detector flags on any positional call argument in any `dsx/frame/` module.
- `resolve_declared_procedure()` looks the normalized label up in the frame's own candidate set first (`in_candidate_set`), then across every other pair (`outside_candidate_set`, naming the family and its own axes, ties broken lexicographically by family id), and returns `unresolved` when the alias appears nowhere -- including for a one-character variant of a real alias. `not_declared` covers a blank, absent or whitespace-only label. The only string comparison anywhere in the module is equality after `normalize()`.
- Both `tests/test_frame_boundary.py` scanners (import-direction and paradigm-read, 10 tests total) confirmed clean against the new module on its first commit.

## Task Commits

Each task followed a RED -> GREEN TDD cycle, two commits per task:

1. **Task 1: Create the module and load_ontology(), refusing rather than degrading**
   - `e69e72f` (test) -- 14 failing tests confirming `dsx.frame.admissibility` did not exist
   - `db49cb6` (feat) -- `Family`/`RankingRule`/`Ontology` dataclasses and `load_ontology()`; all 14 tests pass
2. **Task 2: Exact-match alias resolution scoped to the candidate set**
   - `3a1093b` (test) -- 20 new failing tests confirming `alias_index`, `candidate_families`, `declared_procedure`, `resolve_declared_procedure` and `Resolution` did not exist (24 errors: some tests exercise multiple missing names)
   - `f98be2e` (feat) -- `Resolution` dataclass, `_RESOLUTION_STATUSES`, and the four functions; all 34 tests pass

**Plan metadata:** this commit (docs: complete plan), made by the worktree executor before returning to the orchestrator.

## Files Created/Modified

- `dsx/frame/admissibility.py` -- the module: 4 frozen dataclasses, `load_ontology()`, `alias_index()`, `candidate_families()`, `declared_procedure()`, `resolve_declared_procedure()`. No `Report`, no finding, no gate registration -- none of that is built until plan 11-06.
- `tests/test_frame_admissibility.py` -- 34 tests across 8 `TestCase` classes: `TestLoadOntologyGoldenPath`, `TestLoadOntologyMissingFile`, `TestLoadOntologyStructuralErrors`, `TestLoadOntologyDroppedUncited`, `TestFamilyAndRankingRuleFrozen`, `TestAliasIndex`, `TestCandidateFamilies`, `TestResolveDeclaredProcedure`, `TestDeclaredProcedure`.

## Decisions Made

- alias-collision error message names the *normalized* alias (not the raw, un-normalized spelling on whichever family the collision scanner happened to visit second) -- the normalized form is what actually collided, and naming anything else would make the message's exact wording depend on which of two differently-cased aliases the ontology's author happened to write on the second-visited family.
- `declared_procedure()` uses the existing `dsx.spec.is_blank_text()` helper (rather than `is_blank()` or a hand-rolled `isinstance` + strip check) for the blank-`primary_procedure` guard, because it already encodes exactly the needed semantics ("blank unless it is a non-empty string") as a single project-standard predicate.
- `resolve_declared_procedure()`'s cross-pair tie-break sorts `(pair, family_id)` candidates by `family_id`, matching the plan's instruction that the outcome must be a function of the ontology's own contents, never of `dict` iteration order.

## Deviations from Plan

None. The plan's two tasks were executed as written, in the order written, with the exact function names, dataclass shapes and refuse-not-degrade contract the plan specified.

## Orchestrator-flagged items -- explicitly checked

- **The 4-vs-7 `gen-finding-catalogue.py --check` warning count.** This plan's own `<verification>` section, taken literally, implies 4 pre-existing "declared twice with different text" warnings. The actual run produced **7**: `DSX-COH-030`, `DSX-PAR-002`, `DSX-SPEC-070` (three times), `DSX-VAL-021`, `DSX-VAL-060`. Per the orchestrator's pre-execution briefing, this is the correct, expected current baseline -- the plan's text predates plans 02-04 growing the warning count and was never rebased. `--check` still exits 0 in both cases (the warnings are non-blocking). Not treated as a regression; no code change made.
- **The alias-resolution design gap the plan's own `flagged_assumptions` names.** The plan states its pair-scoped design (filter candidates by `(estimand, dependence)` first, then resolve the alias only within that set) is the planner's own settled reading of D-03/D-16/D-18, not confirmed by an automated edge-case probe. During implementation, no case arose that this design left ambiguous: every behavior in the plan's `<behavior>` list (own-pair hit, cross-pair hit with tie-break, no hit anywhere, blank declaration) mapped onto exactly one of the four `Resolution.status` values with no residual case. The one edge worth naming explicitly: when a declared label matches an alias in *more than one* other `(estimand, dependence)` pair, the plan's own text supplies the resolution (lexicographically-first family id, recorded in `detail`) -- so even that case was specified, not left open. No unresolved design gap was encountered.

## Issues Encountered

None.

## Next Phase Readiness

- `load_ontology()`, `alias_index()`, `candidate_families()` and `resolve_declared_procedure()` are ready for plan 11-06 (`rank_admissible()`, `admissible_families()`, `check()`, the two `DSX-ADM-*` finding codes) to build directly on top of.
- `declared_procedure(spec)` is ready for plan 11-07 to call alongside the frequentist scoping predicate `applies_to_frequentist_admissibility(spec)` (already shipped in `dsx/frame/paradigm.py`, plan 11-03) -- this module still never reads the declared paradigm or decides scoping itself, matching D-03/D-11.
- The alias table built here has exactly one intended consumer, this module itself -- confirmed by `git diff --stat` showing no change to `dsx/checks/stats.py` or `dsx/frame/prereg.py`, and the `DSX-STA-041` `fishers_exact`/`fisher_exact` spelling mismatch was left untouched, per the orchestrator's briefing.
- No blockers for plan 11-06.

---
*Phase: 11-frequentist-admissibility-adjudicator-dsx-adm*
*Completed: 2026-08-22*
