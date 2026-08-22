---
phase: 11-frequentist-admissibility-adjudicator-dsx-adm
plan: 06
subsystem: infra
tags: [dsx, admissibility, ranking, frequentist, decision-record, python]

# Dependency graph
requires:
  - phase: 11-05
    provides: "dsx/frame/admissibility.py's load_ontology(), alias_index(), candidate_families(), declared_procedure() and resolve_declared_procedure() -- the refuse-not-degrade loader and exact-match alias resolver this plan ranks and adjudicates on top of"
provides:
  - "rank_admissible(candidates, rules) -- a cited pairwise rule table with a Manski fewer-assumptions fallback and a lexicographic id tiebreak, byte-stable and permutation-invariant, never a numeric score"
  - "dominating_rules(family_id, candidates, rules) -- the rules naming a family as dominated within a candidate set, kept separate from ranking so a domination claim and an ordering stay two different questions"
  - "admissible_families(spec) -- a pure, JSON-serialisable return shape naming every admissible family's bought/charged assumption tokens, with the three collapsed refusal causes checked in a fixed order"
  - "check(spec, *, applies_to_frame=True) -- Report -- emits DSX-ADM-010 (HIGH) and DSX-ADM-020 (CRITICAL), the first shipped use of DecisionRecord.escalate and .alternatives_rejected"
affects: [11-07, 11-08]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Ranking is a comparator (functools.cmp_to_key) over a deterministic base sort ((len(charges), id)), never a scoring function -- a rule table is a partial order by construction and no single number could honestly stand in for it."
    - "The pure-ranking/refusing function (admissible_families) and the Report-emitting adjudicator (check) are split exactly the way dsx/checks/stats.py splits recommend_test() from _check_declared_test() -- check() calls the pure function exactly once and both finding helpers read its returned dict, never re-deriving the ranked set."
    - "The _NOT_SHIPPED deletion and a family's first report.add(...) call are a matched pair that must land in the same commit -- dsx/suppressions.py::known_codes() AST-scans call sites, not gate registration, so the honesty-control test flips at the call site regardless of whether GATE_PROFILES has been touched yet."

key-files:
  created: []
  modified:
    - dsx/frame/admissibility.py
    - dsx/frame/paradigm.py
    - scripts/gen-finding-catalogue.py
    - references/finding-codes.md
    - tests/test_frame_admissibility.py

key-decisions:
  - "RankedEntry carries a `rank` field (in addition to the eight the plan's behavior prose names) because the plan's own verify script accesses `.rank` directly on the returned tuple (`one[0].rank==1`) -- the task-body/acceptance-criteria text is authoritative over the header prose's field count, per the orchestrator's pre-execution note on header/body drafting inconsistencies."
  - "DecisionRecord.inputs names the declared-procedure field as prose (\"the declared primary procedure field\") rather than as a literal `inference.primary_procedure` dotted-path string, honoring the plan's explicit instruction not to name any dotted path beginning with the inference block name anywhere in this file -- stricter than what the D-11 boundary scanner mechanically enforces (which only flags positional call arguments and the exact `inference.paradigm` text), but the plan's prohibition is broader and load-bearing."
  - "Exactly one DecisionRecord is appended per check() call (not one per firing helper), because DSX-ADM-010 and DSX-ADM-020 are mutually exclusive by construction within a single call (ADM-010 requires resolution=='in_candidate_set'; ADM-020 requires the refusal state, which precludes in_candidate_set) -- the single record's fields (choice/rule/citation/counterfactual) are chosen by which of the three outcomes (refusal, ranking, clear) occurred."

requirements-completed: [REQ-P11-03, REQ-P11-04]

coverage:
  - id: D1
    description: "rank_admissible() orders a candidate set by a cited pairwise rule table (ontology order), a Manski fewer-assumptions fallback, and a lexicographic id tiebreak -- provably independent of input order (full-permutation test over a real four-family candidate set) and stated for the empty and one-element cases"
    requirement: "REQ-P11-03"
    verification:
      - kind: unit
        ref: "tests/test_frame_admissibility.py#TestRankAdmissible"
        status: pass
      - kind: unit
        ref: "tests/test_frame_admissibility.py#TestDominatingRules"
        status: pass
    human_judgment: false
  - id: D2
    description: "admissible_families(spec) returns a pure, JSON-serialisable dict naming every admissible family's bought/charged assumption tokens, with three refusal causes (blank axis, no matching family, unresolved declared procedure) collapsing into one no_admissible_procedure refusal, checked in a fixed order"
    requirement: "REQ-P11-03"
    verification:
      - kind: unit
        ref: "tests/test_frame_admissibility.py#TestAdmissibleFamilies"
        status: pass
    human_judgment: false
  - id: D3
    description: "check() emits DSX-ADM-010 (HIGH) only on a cited pairwise domination of the resolved family, and DSX-ADM-020 (CRITICAL) for an underdetermined frame, through the ordinary emit path (never CheckError); no committed spec draws DSX-ADM-010"
    requirement: "REQ-P11-04"
    verification:
      - kind: unit
        ref: "tests/test_frame_admissibility.py#TestCheck"
        status: pass
    human_judgment: false
  - id: D4
    description: "DecisionRecord.escalate and .alternatives_rejected carry non-default values for the first time in this codebase, exactly one record per check() call, escalate=True only on the DSX-ADM-020 refusal path"
    requirement: "REQ-P11-04"
    verification:
      - kind: unit
        ref: "tests/test_frame_admissibility.py#TestCheck.test_good_fixture_emits_zero_findings_and_one_unescalated_decision"
        status: pass
      - kind: unit
        ref: "tests/test_frame_admissibility.py#TestCheck.test_every_dsx_adm_020_path_escalates"
        status: pass
      - kind: unit
        ref: "tests/test_frame_admissibility.py#TestCheck.test_clear_path_lists_ranked_but_not_top_ids_as_alternatives_rejected"
        status: pass
    human_judgment: false
  - id: D5
    description: "references/finding-codes.md carries a DSX-ADM group (DSX-ADM-010 HIGH, DSX-ADM-020 CRITICAL) and the catalogue check is current; the honesty-control invariant (_NOT_SHIPPED) is cleared in the same commit as the first report.add"
    requirement: "REQ-P11-04"
    verification:
      - kind: unit
        ref: "tests/test_gen_finding_catalogue.py (full module)"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestPhase6ParadigmManifest::test_applied_prefixes_have_codes_and_not_shipped_prefixes_have_none"
        status: pass
      - kind: other
        ref: "python scripts/gen-finding-catalogue.py --check"
        status: pass
    human_judgment: false

duration: ~10min (commit span; TDD implementation across 3 tasks, 6 commits)
completed: 2026-08-22
status: complete
---

# Phase 11 Plan 06: Rank the Admissible Set and Ship the Guard Set Summary

**`rank_admissible()`/`dominating_rules()`/`admissible_families()`/`check()` in `dsx/frame/admissibility.py` — a rule-table ranking (never a numeric score) plus `DSX-ADM-010` (HIGH, cited-rule domination) and `DSX-ADM-020` (CRITICAL, three collapsed underdetermination causes), both reaching exit 1 through the ordinary emit path with `DecisionRecord.escalate`/`alternatives_rejected` shipping for the first time.**

## Performance

- **Duration:** ~10 min commit-to-commit (plus a longer context-reading phase across ~20 files before the first edit)
- **Tasks:** 3
- **Files modified:** 5 (`dsx/frame/admissibility.py`, `dsx/frame/paradigm.py`, `scripts/gen-finding-catalogue.py`, `references/finding-codes.md`, `tests/test_frame_admissibility.py`)

## Accomplishments

- `rank_admissible(candidates, rules)` orders any candidate set by a cited pairwise rule table (kept in ontology order), a Manski's-Law-of-Decreasing-Credibility fewer-assumptions fallback, and a lexicographic `id` tiebreak — a `functools.cmp_to_key` comparator over a deterministic base sort `(len(charges), id)`, so the result is a pure function of the candidate set, provably independent of the caller's input order (a full-permutation test over the real four-family `difference_in_proportions`/`none` candidate set enumerates all 24 orderings and asserts one output). No arithmetic anywhere combines more than one family attribute into a single number.
- `dominating_rules(family_id, candidates, rules)` returns the ontology-ordered rules naming a family as dominated within a candidate set, empty for a one-element set — the predicate `DSX-ADM-010` keys on, kept separate from ordering.
- `admissible_families(spec)` is a pure, total, JSON-serialisable-dict-returning function mirroring the `recommend_test()`/`_check_declared_test()` split already shipped in `dsx/checks/stats.py`: no `Report`, no finding, no `DecisionRecord`, no file write. Three refusal causes — a required axis blank or absent, the axis pair matching zero families, and a declared procedure resolving to no family in its own candidate set (or resolving only outside it) — collapse into one `no_admissible_procedure` refusal, checked in a fixed order (blank axis, then no-match, then unresolved), exactly one ever reported.
- `check(spec, *, applies_to_frame=True)` calls `admissible_families(spec)` exactly once and emits `DSX-ADM-010` (HIGH) only when the declared procedure resolved into its own candidate set *and* a cited pairwise rule names another candidate as preferred — never on the fewer-assumptions criterion or the identifier tiebreak alone, and the clustered-regression CV1/CV3 pair's hedged reliability ordering is worded as a hedge, never as a domination. `DSX-ADM-020` (CRITICAL) fires for whichever of the three collapsed causes applies, naming the concrete cause in `detail` and `where`; neither code ever raises `CheckError`, both reach exit 1 through the ordinary emit path.
- Every `check()` call that clears the two guards (`applies_to_frame` and a mapping `spec`) appends exactly one `DecisionRecord` — the first shipped use of both `escalate` (`True` on every `DSX-ADM-020` refusal path, `False` otherwise) and `alternatives_rejected` (the ranked-but-not-top family ids, in rank order, whenever a ranked set exists).
- `dsx/frame/paradigm.py::_NOT_SHIPPED` is emptied (`{}`) in the same commit as `check()`'s first `report.add("DSX-ADM-010", ...)` call: `dsx/suppressions.py::known_codes()` AST-scans call sites rather than gate registration, so `tests/test_dsx.py`'s honesty-control invariant flips the instant the call site exists, independent of `GATE_PROFILES` registration (plan 11-07's job). `_PARADIGM_CONDITIONAL` and `_PARADIGM_INDEPENDENT` are untouched.
- `scripts/gen-finding-catalogue.py::PREFIX_GROUPS` gains the `DSX-ADM` row in the same commit as the first `report.add` call, and `references/finding-codes.md` is regenerated via `--write` — without the row, `render()` silently drops both new codes from the rendered catalogue while still counting them in the header total. `_D05_ALLOWLIST_PREFIXES` is deliberately **not** touched — that lands in plan 11-08 alongside the citation-checking function; this plan's docstrings and `# D-05:` test markers are what let that land green.
- No committed spec draws `DSX-ADM-010` — swept over every `examples/*-ANALYSIS-SPEC.yaml`, `examples/known-bad/*-ANALYSIS-SPEC.yaml` and `templates/ANALYSIS-SPEC.yaml` fixture. No gate exit code moved: the check is not registered in any `GATE_PROFILES` entry in this plan.

## Task Commits

Each task followed a RED -> GREEN TDD cycle:

1. **Task 1: `rank_admissible()` and `dominating_rules()` — the comparator, the rule table, and byte-stable order**
   - `fa6a757` (test) — 12 failing tests confirming the two names did not exist
   - `e149759` (feat) — `RankedEntry` dataclass and both functions; all 46 tests pass
2. **Task 2: `admissible_families()` — the pure return shape**
   - `777aeb6` (test) — 14 failing tests confirming the name did not exist
   - `3b50d30` (feat) — the pure function and its three-cause refusal shape; all 59 tests pass
3. **Task 3: `check()` — `DSX-ADM-010`/`DSX-ADM-020` with the whole guard set in one commit**
   - `3c6326b` (test) — 17 failing tests confirming `check()` did not exist (plus one expected pre-existing `known_codes()` assertion failure, since the codes did not exist yet)
   - `f407495` (feat) — `check()`, both `report.add` helpers, the `_NOT_SHIPPED` deletion, the `PREFIX_GROUPS` row, and the regenerated catalogue, all in one commit; all 73 tests pass

**Plan metadata:** this commit (docs: complete plan), made by the worktree executor before returning to the orchestrator.

## Files Created/Modified

- `dsx/frame/admissibility.py` — adds `RankedEntry`, `rank_admissible()`, `dominating_rules()`, `admissible_families()`, `_check_declared_procedure_ranking()`, `_check_no_admissible_procedure()`, and `check()`. No dataclass or tuple leaks out of `admissible_families()`'s return value; no `raise CheckError` anywhere on an underdetermined-frame path.
- `dsx/frame/paradigm.py` — `_NOT_SHIPPED` emptied to `{}`, comment updated to explain why and to preserve the mechanism for the next unshipped family.
- `scripts/gen-finding-catalogue.py` — one `PREFIX_GROUPS` row added for `DSX-ADM`; `_D05_ALLOWLIST_PREFIXES` untouched.
- `references/finding-codes.md` — regenerated via `--write`; carries the new `## Frequentist admissibility — DSX-ADM-*` section.
- `tests/test_frame_admissibility.py` — 73 tests total across all three tasks' new classes (`TestRankAdmissible`, `TestDominatingRules`, `TestAdmissibleFamilies`, `TestCheck`), including the `# D-05: DSX-ADM-010` / `# D-05: DSX-ADM-020` raw-text markers the catalogue's test-linkage check requires.

## Decisions Made

- `RankedEntry` carries a `rank` field in addition to the eight fields the plan's behavior prose names, because the plan's own verify script accesses `.rank` directly (`one[0].rank==1`) — task-body/verify-script text is authoritative over the header prose's field count.
- `DecisionRecord.inputs` names the declared-procedure field as prose ("the declared primary procedure field") rather than the literal dotted-path string `inference.primary_procedure`, honoring the plan's explicit, broader-than-mechanically-enforced instruction never to name a dotted path beginning with the inference block name anywhere in `admissibility.py`.
- Exactly one `DecisionRecord` is appended per `check()` call rather than one per firing helper, because `DSX-ADM-010` and `DSX-ADM-020` are mutually exclusive by construction within a single call — the record's fields are selected by which of the three outcomes (refusal / ranking / clear) actually occurred.

## Deviations from Plan

None — the plan's three tasks were executed as written, in the order written, with the exact function names, dataclass shapes, code assignments and guard-set commit structure the plan specified. The two orchestrator-flagged risk areas were both explicitly checked and hold: `_D05_ALLOWLIST_PREFIXES` was not touched (confirmed via `git diff`), and the good fixture (`examples/good-ANALYSIS-SPEC.yaml`) still resolves top-ranked with zero findings, so `DSX-ADM-010` does not newly fire on the project's own always-passes invariant.

## Orchestrator-flagged items — explicitly checked

- **The 4-vs-7 `gen-finding-catalogue.py --check` warning count.** Confirmed still 7 pre-existing "declared twice with different text" warnings (`DSX-COH-030`, `DSX-PAR-002`, `DSX-SPEC-070` x3, `DSX-VAL-021`, `DSX-VAL-060`), unchanged by this plan's work. `--check` exits 0 either way; not a regression.
- **`_D05_ALLOWLIST_PREFIXES` not touched.** Verified via `git diff scripts/gen-finding-catalogue.py | grep _D05_ALLOWLIST_PREFIXES` — no match. Only `PREFIX_GROUPS` was edited.
- **Good-fixture regression check.** `admissibility.check(load('examples/good-ANALYSIS-SPEC.yaml'), applies_to_frame=True).findings == []`, confirmed directly and via the committed `TestCheck.test_good_fixture_emits_zero_findings_and_one_unescalated_decision` test.

## Issues Encountered

None.

## Next Phase Readiness

- `check(spec, *, applies_to_frame)` is ready for plan 11-07 to wire into `GATE_PROFILES` alongside `applies_to_frequentist_admissibility(spec)` (already shipped in `dsx/frame/paradigm.py`, plan 11-03) — this plan does not touch `dsx/cli.py` at all, so no gate exit code moved.
- `admissible_families(spec)` is ready for `dsx/cli.py::cmd_recommend` (or an equivalent future CLI surface) to call directly for the additive `"admissibility"` key the plan's header names as a future artifact — not built in this plan, since `check()`/`admissible_families()` were the deliverables, not the CLI surface.
- The docstrings, `# D-05:` test markers, and `PREFIX_GROUPS` row this plan wrote are exactly what plan 11-08 needs to add `"DSX-ADM-"` to `_D05_ALLOWLIST_PREFIXES` and land green on its first run.
- No blockers for plan 11-07.

---
*Phase: 11-frequentist-admissibility-adjudicator-dsx-adm*
*Completed: 2026-08-22*
