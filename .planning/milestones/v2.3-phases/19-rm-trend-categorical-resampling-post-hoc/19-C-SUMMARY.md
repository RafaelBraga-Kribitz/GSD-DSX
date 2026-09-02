---
phase: 19-rm-trend-categorical-resampling-post-hoc
plan: C
subsystem: testing
tags: [statistics, declaration-gate, finding-codes, rm-anova, trend, resampling, post-hoc, variance-pretest, power-reporting, proportion-count, d05-allowlist, fixtures]

# Dependency graph
requires:
  - phase: 19-A
    provides: the eight Phase-19 sub-vocabs + POSTHOC_FAMILY_MAP in spec.py, the six _MEMBERSHIP_FIELDS entries + imported vocabs in stats.py, the six recommend_* routing surfaces, and the six mirror sections in test-selection.md
provides:
  - _check_declared_advanced_stats dispatcher + seven per-family gate helpers in dsx/checks/stats.py, wired at BOTH check() call sites
  - ten HIGH declaration-only finding codes DSX-STA-070/080/081/090/100/110/111/120/121/122
  - the ten codes citation-enforced by exact name in scripts/gen-finding-catalogue.py _D05_ALLOWLIST_CODES
  - references/finding-codes.md regenerated to 275; the invariant triple moved as a set
  - the variance/power gate-code doc entries in references/test-selection.md
  - examples/bad-ANALYSIS-SPEC.yaml extended to fire all ten in one audit
affects: [phase-20, secure-phase-19, milestone-audit]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Thin dispatcher over per-family gate helpers, each with its own attributable D-05 Citation:/Structural criterion: docstring (gen-finding-catalogue.py resolves citations per nearest-enclosing FunctionDef)"
    - "Declaration-only gates: is_blank short-circuit then exact normalized equality/membership; absence of a trigger field is non-blocking (D-10); no data path, no numeric boundary printed (D-07)"
    - "str-OR-list field handling: collect non-blank normalized tokens into a set before membership testing"

key-files:
  created:
    - tests/test_rm_sphericity_gate.py
    - tests/test_trend_gate.py
    - tests/test_resampling_gate.py
    - tests/test_posthoc_gate.py
    - tests/test_variance_role_gate.py
    - tests/test_power_reporting_gate.py
    - tests/test_proportion_count_gate.py
  modified:
    - dsx/checks/stats.py
    - scripts/gen-finding-catalogue.py
    - references/finding-codes.md
    - references/test-selection.md
    - tests/test_finding_catalogue_invariant.py
    - examples/bad-ANALYSIS-SPEC.yaml
    - tests/test_causal_verb_golden.py
    - tests/test_p19_categorical_rows.py

key-decisions:
  - "The seven helpers are separate functions (not a monolith) so each of the ten codes resolves its D-05 citation to the right function — a monolith would launder seven distinct obligations under one docstring (T-19-C-02)"
  - "The ten codes are allowlisted in _D05_ALLOWLIST_CODES by EXACT name, not via a DSX-STA- prefix, so the ~40 uncited legacy DSX-STA-* codes do not turn the build red (T-19-C-01)"
  - "8 of the 10 gate-code doc entries were already present in test-selection.md as 19-A 'Wave 2' forward-references; 19-C added only the missing DSX-STA-110/111 variance/power section to avoid duplication"

patterns-established:
  - "Pattern 1: over-block guards asserted by unit tests (070 never on repeated-measures presence; 110 silent on scale_estimand; 111 narrow; 081 is_blank not membership)"
  - "Pattern 2: gate helper unit tests drive the dispatcher directly and assert the codes set EXHAUSTIVELY, so a stray DSX-STA-040/041 cannot hide behind an `in` check (Pitfall 1)"

requirements-completed: [REQ-P19-01, REQ-P19-02, REQ-P19-04, REQ-P19-05, REQ-P19-06, REQ-P19-07]

coverage:
  - id: D1
    description: "DSX-STA-070 fires only on declared sphericity_correction == mauchly_conditional, never on repeated-measures presence (REQ-P19-01)"
    requirement: "REQ-P19-01"
    verification:
      - kind: unit
        ref: "tests/test_rm_sphericity_gate.py"
        status: pass
    human_judgment: false
  - id: D2
    description: "DSX-STA-080/081 trend-companion gates; 081 is is_blank not membership (declared none/independent satisfies) (REQ-P19-02)"
    requirement: "REQ-P19-02"
    verification:
      - kind: unit
        ref: "tests/test_trend_gate.py"
        status: pass
    human_judgment: false
  - id: D3
    description: "DSX-STA-090 fires ONCE naming the missing member(s) of the {method, seed, B, unit} quadruple, never four, never checks B's value (REQ-P19-04)"
    requirement: "REQ-P19-04"
    verification:
      - kind: unit
        ref: "tests/test_resampling_gate.py"
        status: pass
    human_judgment: false
  - id: D4
    description: "DSX-STA-100 post-hoc/omnibus family-match via POSTHOC_FAMILY_MAP membership (REQ-P19-05)"
    requirement: "REQ-P19-05"
    verification:
      - kind: unit
        ref: "tests/test_posthoc_gate.py"
        status: pass
    human_judgment: false
  - id: D5
    description: "DSX-STA-110 variance-test-as-location-pretest (silent on scale_estimand) and DSX-STA-111 observed/post-hoc power (narrow) (REQ-P19-06)"
    requirement: "REQ-P19-06"
    verification:
      - kind: unit
        ref: "tests/test_variance_role_gate.py"
        status: pass
      - kind: unit
        ref: "tests/test_power_reporting_gate.py"
        status: pass
    human_judgment: false
  - id: D6
    description: "DSX-STA-120 (Wald, n-independent) / 121 (exposure w/o offset) / 122 (NNT w/o CI) (REQ-P19-07)"
    requirement: "REQ-P19-07"
    verification:
      - kind: unit
        ref: "tests/test_proportion_count_gate.py"
        status: pass
    human_judgment: false
  - id: D7
    description: "Ten codes citation-enforced by exact name; finding-codes.md regenerated to 275; invariant triple moved as a set"
    verification:
      - kind: automated
        ref: "python3 scripts/gen-finding-catalogue.py --check (exit 0)"
        status: pass
      - kind: unit
        ref: "tests/test_finding_catalogue_invariant.py"
        status: pass
    human_judgment: false
  - id: D8
    description: "bad-ANALYSIS-SPEC.yaml fires all ten in one audit; good stays silent and unedited"
    verification:
      - kind: integration
        ref: "tests/test_causal_verb_golden.py + direct stats.check audit"
        status: pass
    human_judgment: false

# Metrics
duration: ~35min
completed: 2026-09-02
status: complete
---

# Phase 19 Plan C: The Phase-19 Gate Surface Summary

**Ten HIGH declaration-only finding codes (DSX-STA-070/080/081/090/100/110/111/120/121/122) split into seven per-family `_check_declared_*` helpers dispatched from `_check_declared_advanced_stats` wired at both `check()` sites, citation-enforced by exact name, catalogue rebased 265 -> 275.**

## Performance

- **Duration:** ~35 min
- **Tasks:** 3 (Task 1 TDD: RED + GREEN)
- **Files modified:** 15 (7 new gate test modules + 8 modified)

## Accomplishments
- `_check_declared_advanced_stats` dispatcher + seven per-family helpers emit the ten HIGH codes with exact D-01/D-06 predicates and over-block guards; wired at BOTH `check()` call sites so a pure declaration-only spec (no `results.tests`) is still gated.
- Each of the ten codes carries its own attributable D-05 `Citation:` + `Structural criterion:` docstring; all ten allowlisted by exact name in `_D05_ALLOWLIST_CODES` (never via a `DSX-STA-` prefix); `gen-finding-catalogue.py --check` exits 0.
- `references/finding-codes.md` regenerated to 275; the invariant triple moved as a set (`_EXPECTED_TOTAL` 265 -> 275, +10 `_MINTED_CODES`, snapshot frozen at 256, method renamed `..._275_codes`).
- `examples/bad-ANALYSIS-SPEC.yaml` extended (not replaced) to fire all ten in one `stats.check` pass; `examples/good-ANALYSIS-SPEC.yaml` stays silent and unedited; the variance/power gate-code doc entries added to `test-selection.md`.

## Task Commits

1. **Task 1 (RED): seven gate test modules** - `a104e2b` (test) — 40 tests error on the missing dispatcher
2. **Task 1 (GREEN): dispatcher + seven helpers wired at both sites** - `936d080` (feat) — 40 tests pass
3. **Task 2: allowlist +10, regen to 275, invariant triple bump** - `8de0b75` (feat)
4. **Task 3: variance/power doc entries + bad fixture fires all ten** - `d9be259` (feat)
5. **Deviation: rebaseline two Wave-1 pins invalidated by the Wave-2 mint** - `bab4132` (test)

## Files Created/Modified
- `dsx/checks/stats.py` - dispatcher + seven per-family gate helpers; wired at both `check()` call sites (485, 501)
- `scripts/gen-finding-catalogue.py` - ten codes added to `_D05_ALLOWLIST_CODES` by exact name with a dated Phase-19 comment block
- `references/finding-codes.md` - regenerated (never hand-edited) 265 -> 275
- `references/test-selection.md` - new "Variance pretest and power reporting" section (DSX-STA-110/111)
- `tests/test_finding_catalogue_invariant.py` - triple moved as a set to 275
- `examples/bad-ANALYSIS-SPEC.yaml` - analysis block extended with ten dedicated in-vocabulary trigger fields
- `tests/test_{rm_sphericity,trend,resampling,posthoc,variance_role,power_reporting,proportion_count}_gate.py` - seven new gate modules with `# D-05` markers
- `tests/test_causal_verb_golden.py`, `tests/test_p19_categorical_rows.py` - Wave-1 pins rebaselined in lockstep (see Deviations)

## Decisions Made
- Seven separate helpers, not a monolith, so each code's D-05 citation resolves to its enclosing function (T-19-C-02 citation-laundering mitigation).
- Exact-name allowlisting (not a `DSX-STA-` prefix) so the ~40 uncited legacy `DSX-STA-*` codes stay green (T-19-C-01).
- Gate unit tests drive `_check_declared_advanced_stats` directly and assert the codes set exhaustively — no false `DSX-STA-040/041` can appear and no stray code can hide (Pitfall 1).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Rebaselined two Wave-1 test pins invalidated by the Wave-2 catalogue mint**
- **Found during:** Task 3 (full-suite verification after the bad-fixture extension and the 265 -> 275 catalogue regen)
- **Issue:** Two Wave-1 (19-A) tests pinned pre-Wave-2 realities the plan's own rebaseline invalidated: `tests/test_p19_categorical_rows.py` asserted the catalogue "still declares exactly 265" (a REQ-P19-03 no-mint proof whose own comment says it is kept in lockstep with `test_finding_catalogue_invariant.py::_EXPECTED_TOTAL`, which Task 2 bumped to 275); and `tests/test_causal_verb_golden.py`'s golden CRITICAL/HIGH set for `bad-ANALYSIS-SPEC.yaml` predated the fixture's Task-3 extension.
- **Fix:** Bumped the categorical guard's `_EXPECTED_TOTAL` to 275 (preserving its categorical-minted-nothing intent, which is carried by the rows-present assertions + the absent DSX-STA-06x decade, not by the absolute total) and renamed its method to `_275_codes`; added the ten measured DSX-STA gate codes to the bad-fixture golden set. The golden delta was MEASURED (added exactly the ten, dropped nothing) — the sanctioned "fixture built to demonstrate the new catch" case, not a golden-set edit to absorb an unexpected drift (T-11.2-13 honoured).
- **Files modified:** tests/test_p19_categorical_rows.py, tests/test_causal_verb_golden.py
- **Verification:** `python3 -m unittest discover -s tests -q` -> 1442 tests OK
- **Committed in:** bab4132

**Note on scope:** These two files are outside the plan's `files_modified` list but are direct lockstep consequences of the plan's own instructions (Task 2 catalogue 265 -> 275; Task 3 bad-fixture extension). No behaviour was weakened; both are pinned-constant rebaselines that keep the suite green.

**Observation (no edit owed):** 8 of the 10 gate-code doc entries (070/080/081/090/100/120/121/122) were already present in `references/test-selection.md`, written by 19-A as "Wave 2" forward-references. 19-C added only the missing DSX-STA-110/111 variance/power section rather than duplicating the eight.

---

**Total deviations:** 1 auto-fixed (1 blocking lockstep rebaseline)
**Impact on plan:** Necessary to keep the full suite green after the plan's own catalogue and fixture rebaselines. No scope creep, no behaviour weakened.

## Issues Encountered
- The pre-existing `DSX-VAL-021 / DSX-VAL-060 / DSX-SPEC-070 declared twice` generator warnings are legacy (not Phase-19); `--check` still exits 0 ("finding catalogue is current"). Left untouched (out of scope).

## Per-task verify results (real output)
- **Task 1:** `Ran 40 tests ... OK`; `dispatcher wired at both sites`.
- **Task 2:** `finding catalogue is current` / `check EXIT=0`; invariant `Ran 2 tests ... OK`; `allowlist + regen + invariant at 275 OK`.
- **Task 3:** corpus + good-fixture `Ran 48 tests ... OK`; `bad fires all ten; good silent; gate-code doc entries present`.
- **Merge gate:** `python3 -m unittest discover -s tests -q` -> `Ran 1442 tests ... OK`; `dsx validate` good EXIT=0, bad EXIT=1 (correct — bad blocks); `gen-finding-catalogue.py --check` EXIT=0.

## Next Phase Readiness
- The Phase-19 gate surface is complete and merge-gate green. Any catch-rate re-baseline of the known-bad corpus is REQ-P20-01 (a Phase-20 concern), not this plan.
- No tracking file was touched by any 19-C commit (verified: `git diff --name-only 0d9115d..HEAD` names no `.planning/` tracking file).

## Self-Check: PASSED

- Files verified present: 19-C-SUMMARY.md, dsx/checks/stats.py, all seven gate test modules.
- Commits verified in git log: a104e2b, 936d080, 8de0b75, d9be259, bab4132.

---
*Phase: 19-rm-trend-categorical-resampling-post-hoc*
*Completed: 2026-09-02*
