---
phase: 11-frequentist-admissibility-adjudicator-dsx-adm
plan: 08
subsystem: infra
tags: [dsx, build-gate, citation-enforcement, ci, python, yaml]

# Dependency graph
requires:
  - phase: 11-04
    provides: "references/families.yaml -- the 14-family, 19-token, 4-rule cited frequentist ontology this plan's build-time gate reads and enforces citations against"
  - phase: 11-06
    provides: "dsx/frame/admissibility.py's DSX-ADM-010/DSX-ADM-020 report.add call sites, each already carrying a Citation: and Structural criterion: docstring line, plus the # D-05: DSX-ADM-010/020 test markers in tests/test_frame_admissibility.py, and the PREFIX_GROUPS row for DSX-ADM in scripts/gen-finding-catalogue.py -- all of which this plan's allowlist entry turns from convention into an enforced build gate"
provides:
  - "check_families_citations(families_path) -- the build-time half of citation enforcement: an uncited references/families.yaml entry (family, assumption_vocabulary token, or ranking_rule) fails python scripts/gen-finding-catalogue.py --check with exit 1 and a D-24: line naming the entry"
  - "\"DSX-ADM-\" in _D05_ALLOWLIST_PREFIXES -- the run-time half already existed (docstrings, test markers); this line is what makes D-05 actually inspect DSX-ADM-010/DSX-ADM-020 rather than silently pass them uncovered"
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "check_families_citations is a sibling to check_d05, not an extension of it: check_d05 walks Python ASTs for report.add(...) call sites and has no file-path parameter for data; check_families_citations reads one named YAML data file through dsx.loader.load() and has no awareness of Python source. The two mechanisms share the --check branch and the D-0X: prefix convention but never share code."
    - "The repository-root sys.path insertion (needed to import dsx.loader from a script under scripts/, not dsx/) happens inside the function body, guarded by an 'if root_str not in sys.path' check, rather than at module scope -- so loading the script by path for testing (as tests/test_gen_finding_catalogue.py already does via importlib.util.spec_from_file_location) never mutates the importing process's sys.path as a side effect of import alone, only when the function is actually called."
    - "Structural failure of the whole ontology file (missing path, unparseable YAML, top-level not a mapping, or a named block key absent/not-a-list) collapses to exactly one problem naming the path -- never a silent pass over zero entries. Per-entry citation problems (a blank or missing citation on an otherwise well-formed family/token/rule) accumulate across all three blocks rather than stopping at the first, matching check_d05's existing behavior."

key-files:
  created: []
  modified:
    - scripts/gen-finding-catalogue.py
    - tests/test_gen_finding_catalogue.py

key-decisions:
  - "check_families_citations() treats any exception from dsx.loader.load() (missing file, unparseable YAML, top-level-not-a-mapping) uniformly via a single broad except Exception, rather than only catching dsx.loader.SpecParseError -- the plan's own read_first pointed at SpecParseError specifically, but the 'never raise' contract on this function is stricter than that one exception type, and a stray UnicodeDecodeError or similar on a corrupted file must not escape as a traceback out of a build script either."
  - "One of the twelve Task-1 tests (sys.path duplicate-insertion guard) originally asserted the pre-call baseline count of ROOT on sys.path was exactly 1. Under python -m unittest discover -s tests (not tests.test_gen_finding_catalogue alone), several pre-existing test modules elsewhere in the suite already insert ROOT (or an equivalent path) onto sys.path unguarded at import time, so the real baseline under full discovery is >1. Fixed the test to assert the guard's own before/after call consistency instead of an absolute baseline -- this is a Rule 1 (auto-fix bug) correction to a test I wrote in this same plan, not a change to any pre-existing file or test outside this plan's scope."

requirements-completed: [REQ-P11-06]

coverage:
  - id: D1
    description: "check_families_citations(path) is a sibling to check_d05, reads references/families.yaml through dsx.loader with the repository-root sys.path insertion guarded inside the function body, and imports no YAML library of its own"
    requirement: "REQ-P11-06"
    verification:
      - kind: unit
        ref: "tests/test_gen_finding_catalogue.py#TestFamiliesCitationGate.test_committed_families_yaml_has_no_citation_problems"
        status: pass
      - kind: unit
        ref: "tests/test_gen_finding_catalogue.py#TestFamiliesCitationGate.test_repeated_calls_do_not_duplicate_the_repository_root_on_sys_path"
        status: pass
      - kind: other
        ref: "grep -n 'def check_families_citations(' scripts/gen-finding-catalogue.py; grep for sys.path.insert, dsx.loader, D-24: literals; confirmed no 'import yaml' anywhere in the file"
        status: pass
    human_judgment: false
  - id: D2
    description: "A missing/blank citation on a families, assumption_vocabulary, or ranking_rules entry each produces exactly one problem naming that entry's id/token; every problem is reported rather than stopping at the first; a missing/unparseable/structurally-wrong file (or an absent/non-list families key) is one problem naming the path, never a silent pass"
    requirement: "REQ-P11-06"
    verification:
      - kind: unit
        ref: "tests/test_gen_finding_catalogue.py#TestFamiliesCitationGate (12 test methods covering blank/missing citation per block, accumulation across all three blocks, nonexistent path, top-level sequence, families key absent/non-list)"
        status: pass
    human_judgment: false
  - id: D3
    description: "python scripts/gen-finding-catalogue.py --check exits 0 on the committed tree and exits 1 with a D-24: line naming the entry when a families.yaml citation is blanked in a temporary copy of the tree; the D-05: and D-24: prefixes never appear on the same line"
    requirement: "REQ-P11-06"
    verification:
      - kind: unit
        ref: "tests/test_gen_finding_catalogue.py#TestFamiliesCitationGate.test_check_exits_0_against_the_committed_tree"
        status: pass
      - kind: unit
        ref: "tests/test_gen_finding_catalogue.py#TestFamiliesCitationGate.test_check_exits_1_with_d24_prefix_on_an_uncited_family"
        status: pass
      - kind: other
        ref: "manual subprocess run against a temp-copied tree with two_proportion_z's citation blanked -- exit code 1, stderr line 'D-24: families entry '\\''two_proportion_z'\\'' has a missing or blank citation'"
        status: pass
    human_judgment: false
  - id: D4
    description: "\"DSX-ADM-\" is present in _D05_ALLOWLIST_PREFIXES (an inclusion list, every entry still hyphen-terminated); check_d05 on the real tree stays empty; the covered code set now includes DSX-ADM-010 and DSX-ADM-020; removing each of the citation line, the structural-criterion line, or the test marker in turn against a synthetic tree is independently observed to produce a problem naming the code"
    requirement: "REQ-P11-06"
    verification:
      - kind: unit
        ref: "tests/test_gen_finding_catalogue.py#TestDsxAdmAllowlistEntry (7 test methods)"
        status: pass
      - kind: other
        ref: "python -c ... assert 'DSX-ADM-' in _D05_ALLOWLIST_PREFIXES; assert {'DSX-ADM-010','DSX-ADM-020'} <= covered; assert check_d05(...) == [] -- printed 'DSX-ADM codes are covered and compliant'"
        status: pass
    human_judgment: false
  - id: D5
    description: "No gate exit code moves: python -m dsx.cli gate plan and gate ship against examples/good-ANALYSIS-SPEC.yaml both still exit 0; the full suite (python -m unittest discover -s tests) exits 0"
    requirement: "REQ-P11-06"
    verification:
      - kind: other
        ref: "python -m dsx.cli gate plan --spec examples/good-ANALYSIS-SPEC.yaml"
        status: pass
      - kind: other
        ref: "python -m dsx.cli gate ship --spec examples/good-ANALYSIS-SPEC.yaml"
        status: pass
      - kind: unit
        ref: "python -m unittest discover -s tests (993 tests)"
        status: pass
    human_judgment: false

duration: ~5min (commit span; TDD implementation across 2 tasks, 4 commits)
completed: 2026-08-22
status: complete
---

# Phase 11 Plan 08: Build-Time Citation Gate Over the Ontology, and Live D-05 Enforcement for DSX-ADM Summary

**`check_families_citations()` fails `--check` on any uncited `references/families.yaml` entry with a `D-24:` line naming it, and `"DSX-ADM-"` in `_D05_ALLOWLIST_PREFIXES` switches on the D-05 citation/structural-criterion/test-marker gate that plan 11-06's docstrings and markers already satisfy — the two halves of REQ-P11-06's enforcement (build time here, run time in `load_ontology()`) now both exist.**

## Performance

- **Duration:** ~5 min commit-to-commit (2026-08-22T15:37:47 to T15:42:52)
- **Tasks:** 2
- **Files modified:** 2 (`scripts/gen-finding-catalogue.py`, `tests/test_gen_finding_catalogue.py`)

## Accomplishments

- `check_families_citations(families_path)` added directly after `check_d05` in `scripts/gen-finding-catalogue.py` as a documented sibling, not an extension: it has a docstring stating exactly why (`check_d05` has no file-path parameter for data and only reads Python via AST; this function reads one named YAML file through `dsx.loader.load()`, the same reader `dsx/frame/admissibility.py` uses at run time, and imports no YAML library of its own).
- The repository-root `sys.path` insertion — the first anywhere in this script — happens inside the function body, guarded against duplicate entries, so importing the script by path for tests never mutates the importing process's path as an import-time side effect.
- Checks the `families`, `assumption_vocabulary`, and `ranking_rules` blocks in that order, accumulating every missing-or-blank-citation problem rather than stopping at the first. A missing file, an unparseable file, a top-level-not-a-mapping file, or an absent/non-list block key each collapses to exactly one problem naming the path — never a silent pass over zero entries.
- Wired into `main()`'s `--check` branch immediately after the existing `check_d05` block, printing each problem with a `D-24:` prefix (distinct from `D-05:`) and setting exit code 1 when any are found. Not called from `--write`.
- `"DSX-ADM-"` appended to `_D05_ALLOWLIST_PREFIXES` (hyphen-terminated, milestone order preserved), with a comment sentence naming Phase 11 and pointing at the docstrings/markers plan 11-06 already wrote. This is what turned those into an enforced build gate rather than mere convention — proven live, not just allow-listed, by three synthetic-tree tests that each remove one requirement (citation line, structural-criterion line, test marker) in turn and observe `check_d05` report a problem naming `DSX-ADM-010`.
- `references/families.yaml`'s committed content passes `check_families_citations()` with zero problems (all 14 families, 19 assumption tokens, and 4 ranking rules already carry citations from plans 11-01/11-04).
- No D-26/D-27 citation-hygiene work was attempted — both were already completed in plans 11-01 and 11-04, confirmed by re-reading this plan's own text (neither D-26 nor D-27 appears anywhere in it) before starting, per the orchestrator's explicit correction.

## Task Commits

Each task followed a RED -> GREEN TDD cycle:

1. **Task 1: `check_families_citations()` — the build-time citation gate over the ontology data**
   - `244bcdd` (test) — 12 new tests in `TestFamiliesCitationGate`, all failing with `AttributeError` (function did not exist)
   - `2abce22` (feat) — the function, its `--check` wiring, and a test-baseline fix; all 33 tests in the module pass, 986 pass under full `discover`
2. **Task 2: Add `"DSX-ADM-"` to `_D05_ALLOWLIST_PREFIXES` and prove the enforcement is live**
   - `4537a80` (test) — 7 new tests in `TestDsxAdmAllowlistEntry`; 5 of 7 fail as expected (prefix absent, so `DSX-ADM-010`/`DSX-ADM-020` are excluded from the covered set and `check_d05` trivially returns `[]` for them)
   - `8a9923a` (feat) — the allowlist entry and comment; all 40 tests in the module pass, 993 pass under full `discover`

**Plan metadata:** this commit (docs: complete plan), made by the worktree executor before returning to the orchestrator.

## Files Created/Modified

- `scripts/gen-finding-catalogue.py` — adds `check_families_citations()` (placed directly after `check_d05`), its `--check`-branch wiring under the `D-24:` prefix, and `"DSX-ADM-"` in `_D05_ALLOWLIST_PREFIXES` with an updated comment block. `_D05_ALLOWLIST_CODES` and every other constant/function untouched. No `import yaml` anywhere in the file.
- `tests/test_gen_finding_catalogue.py` — adds `TestFamiliesCitationGate` (12 tests: committed-file pass, per-block blank/missing citation naming the id/token, cross-block accumulation, nonexistent path, top-level sequence, families-key absent/non-list, sys.path duplicate-guard, `--check` subprocess exit 0 and exit 1 with `D-24:`) and `TestDsxAdmAllowlistEntry` (7 tests: prefix presence and hyphen-termination, real-tree `check_d05()` empty, real-tree covered-set membership for both new codes, three synthetic-tree removal-proves-enforcement tests, `--check` exit 0). No existing test in this module was deleted or weakened; the module grew from 21 to 40 tests.

## Decisions Made

- `check_families_citations()` catches any exception from `dsx.loader.load()` via a broad `except Exception`, not only `dsx.loader.SpecParseError` — stricter than the plan's `read_first` pointer at that one exception type, because the "never raise" contract on this function covers any failure mode a corrupted or unreadable file could produce (e.g. a stray `UnicodeDecodeError`), not just the loader's own declared error class.
- Fixed the sys.path duplicate-insertion test's assumption that the pre-call baseline count of `ROOT` on `sys.path` is exactly 1 — under `python -m unittest discover -s tests` (as opposed to running only this module), several pre-existing test modules elsewhere in the suite already insert `ROOT` unguarded at import time, so the real baseline is higher and varies with discovery order. The fixed assertion checks the guard's own before/after call consistency (`before == after`), which is what the plan's behavior clause actually requires ("does not leave a duplicate... entry"), rather than an absolute count this plan has no control over. This is a Rule 1 self-correction to a test written in this same plan, not a change to any file outside this plan's scope.

## Deviations from Plan

None beyond the one self-correction documented above under Decisions Made (a bug in a test I wrote in this plan's own Task 1, fixed before Task 1's GREEN commit). The plan's two tasks were executed as written, in the order written, with the exact function name, placement, prefix strings, and allowlist entry the plan specified.

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed an incorrect absolute-baseline assumption in a self-authored test**
- **Found during:** Task 1, before the GREEN commit (running `python -m unittest discover -s tests` after the module-level tests already passed)
- **Issue:** `test_repeated_calls_do_not_duplicate_the_repository_root_on_sys_path` asserted the `sys.path` count of `ROOT` was exactly 1 before any call — true when running `tests.test_gen_finding_catalogue` alone, false under full-suite discovery because other pre-existing test modules already insert `ROOT` unguarded at import time (13 entries observed at that point in discovery order)
- **Fix:** Changed the assertion to compare the count before and after a repeated call (`before == after`), which proves the guard this plan's function implements without depending on what state other, out-of-scope test modules left `sys.path` in
- **Files modified:** `tests/test_gen_finding_catalogue.py`
- **Commit:** `2abce22` (part of Task 1's GREEN commit)

---

**Total deviations:** 1 auto-fixed (1 bug, in a test authored within this same plan)
**Impact on plan:** No scope creep — the fix stayed inside the one test file this plan already modifies and did not touch any pre-existing test module's unguarded `sys.path.insert` calls, which are out of this plan's file scope.

## Issues Encountered

None.

## Threat Flags

None — this plan's threat model (T-11-32 through T-11-35, T-11-SC) covers exactly the surface this plan touches; no new network endpoint, auth path, file-access pattern, or schema change outside that register was introduced.

## Known Stubs

None.

## Next Phase Readiness

- REQ-P11-06's citation enforcement is now two-sided and complete: `check_families_citations()` here (build time) and `load_ontology()`'s uncited-family drop from plan 11-05 (run time). Neither substitutes for the other; a `references/families.yaml` hand-edited after install with a blanked citation is caught by the run-time drop even if `--check` is never re-run, and a blanked citation committed to the repository is caught by `--check` before it ships.
- Plan 11-07 (executing concurrently in a separate worktree, touching `dsx/cli.py` and `tests/test_dsx.py` only) had no file overlap with this plan's scope and required no coordination.
- No blockers for any later plan in Phase 11.

## Self-Check: PASSED

- `scripts/gen-finding-catalogue.py` — FOUND, contains `def check_families_citations(`, `sys.path.insert`, `dsx.loader`, `D-24:`, `"DSX-ADM-"` inside `_D05_ALLOWLIST_PREFIXES`, no `import yaml`
- `tests/test_gen_finding_catalogue.py` — FOUND, contains `TestFamiliesCitationGate` and `TestDsxAdmAllowlistEntry`
- `.planning/phases/11-frequentist-admissibility-adjudicator-dsx-adm/11-08-SUMMARY.md` — FOUND (this file)
- Commits `244bcdd`, `2abce22`, `4537a80`, `8a9923a` — all FOUND in `git log --oneline`

---
*Phase: 11-frequentist-admissibility-adjudicator-dsx-adm*
*Completed: 2026-08-22*
