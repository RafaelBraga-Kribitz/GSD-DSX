---
phase: 06-contract-extension-decision-record-paradigm-manifest
plan: 03
subsystem: infra
tags: [d-05, catalogue-generator, ast, build-gate, stdlib-only]

requires:
  - phase: 06-01
    provides: loader `_NULL` fix and `dsx/spec.py` vocabulary registry (unrelated substrate, same wave)
  - phase: 06-02
    provides: dsx/decisions.py substrate (unrelated substrate, same wave)
provides:
  - "`check_d05()` wired into `scripts/gen-finding-catalogue.py --check`, making D-05 a mechanical build gate rather than review-only"
  - "`DSX-PAR` prefix group in `PREFIX_GROUPS`, ready for plan 06-04+ to populate `DSX-PAR-001`"
  - "A committed, deliberately violating fixture (`tests/fixtures/d05/bad_check.py`) proving both halves of D-05 can actually fail"
affects: [06-04, 06-09, 07, 08, 09, 11]

tech-stack:
  added: []
  patterns:
    - "AST parent-map walk-up: one ast.walk() pass building a child->parent dict, then walking upward from a Call node to the nearest enclosing FunctionDef/AsyncFunctionDef, falling back to the module docstring"
    - "Raw-text regex pass for test-linkage markers, since ast discards comments (mirrors dsx/suppressions.py::known_codes()'s directory-walk idiom, extended to text scanning)"
    - "Finite, visible allow-list literal (_D05_ALLOWLIST_PREFIXES) as the sole enforcement-scope boundary — grows only forward, never widened to exempt a new code"

key-files:
  created: [tests/test_gen_finding_catalogue.py, tests/fixtures/d05/bad_check.py]
  modified: [scripts/gen-finding-catalogue.py]

key-decisions:
  - "check_d05(rows, code_root, tests_root) takes explicit root parameters rather than deriving them from ROOT, so tests can point it at a fixture directory (per plan spec, matching D-22's docstring-resolution design)"
  - "collect()'s module label now derives from the source path relative to dsx/ (not the old two-branch source.parent.name==\"dsx\" test), so a future dsx/frame/*.py file is labelled frame/<stem> instead of mislabelled checks/<stem> — a latent bug this plan's action explicitly called out and fixed pre-emptively"
  - "Task 2's fixture-proof tests are not production-behavior TDD in the strict sense (check_d05 was already fully implemented in Task 1); RED was achieved by writing the fixture-referencing tests before the fixture file existed, so they failed on missing coverage, then the fixture creation turned them GREEN — documented here since it deviates slightly from a canonical new-code RED/GREEN cycle"

patterns-established:
  - "Per-task RED/GREEN TDD cycle within a single execute-type plan: test(06-03) commit precedes each implementation/fixture commit, one pair per task"

requirements-completed: [REQ-P6-11]

coverage:
  - id: D1
    description: "check_d05() enforces both halves of D-05 (Citation + Reference value/Structural criterion, plus linked test) for allow-listed prefixes only, resolving docstrings by walking up from the report.add(...) call site and finding test linkage via a raw-text # D-05: marker scan"
    requirement: "REQ-P6-11"
    verification:
      - kind: unit
        ref: "tests/test_gen_finding_catalogue.py#TestD05Core (10 tests: allow-list filtering, missing citation/reference-value/marker, fully compliant, docstring resolution function-level and module-fallback, test-marker collection, DSX-PAR registration, collect()-to-PREFIX_GROUPS coverage)"
        status: pass
    human_judgment: false
  - id: D2
    description: "Enforcement proven against a deliberately violating fixture committed to the suite (ROADMAP Success Criterion 4); unittest discover never collects the fixture module; the 206 pre-existing codes and the real tree produce zero new failures"
    requirement: "REQ-P6-11"
    verification:
      - kind: unit
        ref: "tests/test_gen_finding_catalogue.py#TestD05EnforcementFixture (6 tests) + #TestD05RealTreeStandingGuarantee (1 test)"
        status: pass
      - kind: unit
        ref: "python3 scripts/gen-finding-catalogue.py --check exits 0; python3 -m unittest discover -s tests exits 0 (206 tests, 2 pre-existing skips)"
        status: pass
    human_judgment: false

duration: 20min
completed: 2026-08-08
status: complete
---

# Phase 6 Plan 3: D-05 Enforcement in the Catalogue Generator Summary

**`scripts/gen-finding-catalogue.py --check` now fails the build when a check covered by a finite, visible D-05 allow-list lacks a `Citation:` line, a `Reference value:`/`Structural criterion:` line, or a linked test — proven against a committed violating fixture, with zero new failures across the 206 pre-existing finding codes.**

## Performance

- **Duration:** ~20 min
- **Started:** 2026-08-08 (immediately following 06-02)
- **Completed:** 2026-08-08
- **Tasks:** 2 completed
- **Files created:** 2 (`tests/test_gen_finding_catalogue.py`, `tests/fixtures/d05/bad_check.py`)
- **Files modified:** 1 (`scripts/gen-finding-catalogue.py`)

## Accomplishments

- `check_d05(rows, code_root, tests_root)` filters `rows` to codes matching `_D05_ALLOWLIST_PREFIXES = ("DSX-PAR-", "DSX-SPEC-08")` (D-20) and reports one problem string per missing `Citation:` line, missing `Reference value:`/`Structural criterion:` line, or missing `# D-05: <CODE>` test marker — reporting every problem found rather than short-circuiting on the first
- `_resolve_docstrings()` builds a one-pass AST parent map (Python's `ast` has no native parent pointers), then for each `report.add(...)` call walks upward to the nearest enclosing `FunctionDef`/`AsyncFunctionDef` and takes its docstring, falling back to the module docstring when no enclosing function is found (D-22)
- `_collect_test_markers()` raw-text scans every `*.py` under a `tests_root` for `# D-05: <CODE>` comments, since `ast` discards comments by design
- `main()`'s `--check` now calls `check_d05(collect(), ROOT / "dsx", ROOT / "tests")` and fails independently of catalogue staleness, printing each problem to stderr — both halves of `--check` (staleness + D-05) are asserted, neither masks the other
- `DSX-PAR` added to `PREFIX_GROUPS` so the family renders once populated (a no-op today — no `DSX-PAR-*` code exists yet)
- `collect()`'s module-label derivation switched from a two-branch `source.parent.name == "dsx"` test to deriving the label from the path relative to `dsx/`, fixing a latent mislabelling bug for any future `dsx/frame/*.py` file (would have been mislabelled `checks/<stem>`)
- `tests/fixtures/d05/bad_check.py` — a deliberately violating fixture with `DSX-PAR-999` (citation present, reference value/structural criterion absent) and a compliant `DSX-SPEC-089` (both lines present), proving `check_d05` can actually fail (ROADMAP Success Criterion 4); not `test`-prefixed so `unittest discover` never collects it
- 17 tests in `tests/test_gen_finding_catalogue.py`, all passing; full suite (`python3 -m unittest discover -s tests`) at 206 tests, 2 pre-existing skips, 0 failures
- `python3 scripts/gen-finding-catalogue.py --write` leaves `references/finding-codes.md` byte-identical (verified via `git status --short` showing no diff) — no code was added or removed, only enforcement machinery

## Task Commits

Each task followed the RED -> GREEN TDD cycle (per-task, within this `type="execute"` plan):

1. **Task 1: D-05 enforcement in the catalogue generator (REQ-P6-11)**
   - `ba6d226` test(06-03): add failing tests for D-05 core enforcement
   - `f18cbbf` feat(06-03): implement D-05 enforcement in catalogue generator
2. **Task 2: Prove the enforcement can fail, against a deliberately violating fixture**
   - `0812043` test(06-03): add failing tests proving D-05 fires against a violating fixture
   - `7c22b2b` test(06-03): add deliberately violating D-05 fixture (bad_check.py)

No REFACTOR commit was needed — GREEN implementations were minimal and required no cleanup pass.

**Plan metadata:** pending (final `docs(06-03)` commit below)

## Files Created/Modified

- `scripts/gen-finding-catalogue.py` - Added `_D05_ALLOWLIST_PREFIXES`, `_CITATION_RE`, `_REFVALUE_RE`, `_TEST_MARKER_RE`, `_resolve_docstrings()`, `_collect_test_markers()`, `check_d05()`; wired into `main()`'s `--check`; `DSX-PAR` prefix group added; `collect()`'s module-label derivation fixed.
- `tests/test_gen_finding_catalogue.py` - 17 `unittest` tests loading the script by path (`importlib.util.spec_from_file_location`, since it is a script not an installed module), covering allow-list filtering, docstring resolution, test-marker collection, and enforcement against the committed fixture.
- `tests/fixtures/d05/bad_check.py` - Deliberately violating fixture: `DSX-PAR-999` (missing reference value/structural criterion) and `DSX-SPEC-089` (fully compliant), both fixture-only codes never emitted under `dsx/`.

## Decisions Made

- `_D05_ALLOWLIST_PREFIXES` carries the exact D-20 comment stating it grows only forward, per each later phase's own new-in-v2.0.0 prefix, never to exempt a code this milestone introduces.
- `check_d05` takes `code_root`/`tests_root` as explicit parameters (not derived from `ROOT`) so the meta-tests can point it at synthetic temp directories and the committed fixture directory without touching `dsx/` or `tests/` proper.
- Task 2's "real tree stays green" standing test (`TestD05RealTreeStandingGuarantee`) lives as its own test class per the plan's explicit instruction — this is the guarantee that turns D-05 from a convention into a build gate for every later phase.
- `test_unittest_discover_excludes_fixture_module` runs `unittest discover` in an isolated subprocess scoped to `tests/fixtures/d05` alone (`start_dir == top_level_dir`) rather than the whole `tests/` directory, to avoid the subprocess recursively re-running this very test suite (discovered and fixed during Task 2 — recorded as a deviation below).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Recursive subprocess invocation in `test_unittest_discover_excludes_fixture_module`**

- **Found during:** Task 2, first RED run
- **Issue:** The initial test implementation ran `python -m unittest discover -s tests -v` in a subprocess from within a test that is itself collected by that same `tests/` discovery — causing unbounded recursive subprocess spawning that hung the shell.
- **Fix:** Scoped the subprocess's `discover -s` to `tests/fixtures/d05` alone (with `start_dir == top_level_dir`, avoiding `unittest`'s "Start directory is not importable" error that occurs when `-t` differs from `-s` without `__init__.py` chains), which validates the exact same acceptance requirement (`bad_check.py` never collected) without touching the outer suite.
- **Files modified:** `tests/test_gen_finding_catalogue.py`
- **Commit:** `0812043` (fixed before commit; the runaway process was killed manually and never landed in a commit)

**2. [Rule 1 - Bug] `unittest discover` exits 5, not 0, when zero tests are collected**

- **Found during:** Task 2, after the fixture was added
- **Issue:** Python's `unittest` (this environment: 3.12/3.14) returns exit code 5 for "no tests ran," not 0 — the test's original assertion (`returncode == 0`) failed even though the actual behavior (fixture excluded) was correct.
- **Fix:** Assert on the `"NO TESTS RAN"` marker in stderr instead of the return code.
- **Files modified:** `tests/test_gen_finding_catalogue.py`
- **Commit:** `7c22b2b`

No architectural deviations (Rule 4). Plan executed as written otherwise; `dsx/` untouched (`git diff --stat dsx/` reports no changes, matching the plan's own `<verification>` requirement).

## Issues Encountered

None beyond the two auto-fixed test-harness bugs above, both caught and resolved within Task 2 before committing.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `check_d05` is live in `--check` and enforces zero problems today (no `DSX-PAR-*` or `DSX-SPEC-08x` code exists yet) — plan 06-04+ inherits a build gate that will immediately catch an uncited new check the moment one is added under an allow-listed prefix.
- `DSX-PAR` prefix group exists in `PREFIX_GROUPS`, ready for `DSX-PAR-001` (plan 06-04+) to render without further catalogue-generator changes.
- The D-20 allow-list boundary (`_D05_ALLOWLIST_PREFIXES`) is the single point later phases extend as `DSX-VAL-*`, `DSX-INT-*`, etc. ship — carried as a literal tuple, finite and visible in every diff.
- `python3 -m dsx gate plan --spec examples/good-ANALYSIS-SPEC.yaml` unaffected — this plan touches only build-time/test code, no `dsx/` runtime module.

---
*Phase: 06-contract-extension-decision-record-paradigm-manifest*
*Completed: 2026-08-08*

## Self-Check: PASSED

- FOUND: scripts/gen-finding-catalogue.py
- FOUND: tests/test_gen_finding_catalogue.py
- FOUND: tests/fixtures/d05/bad_check.py
- FOUND commit: ba6d226 (test(06-03): D-05 core enforcement tests)
- FOUND commit: f18cbbf (feat(06-03): D-05 enforcement implementation)
- FOUND commit: 0812043 (test(06-03): fixture-proof tests)
- FOUND commit: 7c22b2b (test(06-03): violating fixture)
