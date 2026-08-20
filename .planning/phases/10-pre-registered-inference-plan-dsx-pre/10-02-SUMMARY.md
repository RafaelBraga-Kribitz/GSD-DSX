---
phase: 10-pre-registered-inference-plan-dsx-pre
plan: 02
subsystem: testing
tags: [findings, citation, catalogue, stdlib, dsx-frame]

# Dependency graph
requires:
  - phase: 10-pre-registered-inference-plan-dsx-pre (plan 01)
    provides: "PREREG_FACTS closed fact registry, _parse_fallback_rule mini-language parser, _resolve_branch (dsx/frame/prereg.py)"
provides:
  - "DSX-PRE-010 (CRITICAL) — a declared fallback rule that resolves to no branch"
  - "DSX-PRE-030 (CRITICAL) — an executed procedure that differs from the declared branch, naming both labels, blocking on identity alone regardless of relative merit"
  - "dsx/frame/prereg.py::check(spec, root=None, *, reconcile_trail=False) — the family's public dispatcher, degrades to an empty Report on a non-dict spec"
  - "All five D-13 guards flipped in the landing commit: _NOT_SHIPPED no longer names DSX-PRE-, PREFIX_GROUPS gains a DSX-PRE entry, _D05_ALLOWLIST_PREFIXES gains \"DSX-PRE-\", references/finding-codes.md regenerated, D-05 enforcement now covers this family"
affects: [10-03-dsx-pre, 10-04-dsx-pre, 10-05-dsx-pre, 10-06-dsx-pre]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "check() dispatcher shape copied from interference.check: construct Report, guard non-dict spec, resolve once, dispatch to one private helper per adjudicated concept"
    - "root and reconcile_trail parameters defaulted and unused until plans 03/04, so a future CHECKS[\"prereg\"] registration without a matching elif degrades to this signature via the generic CHECKS[name](spec) fallback instead of raising TypeError"
    - "DSX-PRE-030's detail names both branch labels and their source (fallback_rule/primary_procedure, analysis.test) — a literal ROADMAP requirement, not a style choice"
    - "_D05_ALLOWLIST_PREFIXES is an inclusion list that starts D-05 enforcement, not an exemption list that skips it"

key-files:
  created: []
  modified:
    - dsx/frame/prereg.py
    - dsx/frame/paradigm.py
    - scripts/gen-finding-catalogue.py
    - references/finding-codes.md
    - tests/test_frame_prereg.py

key-decisions:
  - "DSX-PRE-010's detail is resolution.reason verbatim — the reason templates built in plan 01 (_UNKNOWN_FACT, _UNDECLARED_FACT) already carry the required specifics (the fact name, the accepted-names list, or the dotted path), so no re-derivation was needed at the finding site"
  - "The 'pinned covered-code set at tests/test_gen_finding_catalogue.py line 227' the plan's read_first named does not exist as a literal in the live tree — test_d05_covered_code_set_on_the_real_tree_is_exactly_the_documented_set computes the covered set dynamically from g.collect() and _D05_ALLOWLIST_PREFIXES/_D05_ALLOWLIST_CODES. No manual edit was needed there; adding \"DSX-PRE-\" to _D05_ALLOWLIST_PREFIXES was sufficient to bring DSX-PRE-010/-030 under D-05 enforcement and the test passed unmodified"
  - "TestParadigmIndependence's 'no inference: block at all' scenario declares the same spec for both the frequentist and bayesian variant by construction (no inference dict exists to declare a paradigm into) — the property holds trivially for that scenario while still running through the same comparison harness as the other three"

patterns-established:
  - "DSX-PRE-030's remedy states three things explicitly: what to do (run the declared procedure or amend the plan and record why before the data was seen), that a more conservative substitute still blocks and why (the substitution is itself a new researcher degree of freedom, Simmons et al. 2011 p. 1365), and the honest caveat that analysis.test is itself plan-time scaffolding, the same class of limit as declared_at"

requirements-completed: [REQ-P10-01, REQ-P10-03, REQ-P10-04]

coverage:
  - id: D1
    description: "DSX-PRE-010 fires at CRITICAL when a declared fallback rule resolves to no branch (fact outside the registry, or a registry fact not declared as a number); clears on a cleanly resolving rule and on inert no-arrow prose; an unparseable arrow-bearing rule still raises CheckError out of check(), not a finding"
    requirement: "REQ-P10-01"
    verification:
      - kind: unit
        ref: "tests/test_frame_prereg.py#TestRuleResolutionFindings"
        status: pass
    human_judgment: false
  - id: D2
    description: "DSX-PRE-030 fires at CRITICAL when the executed procedure (analysis.test) differs from the declared branch after normalize(), naming both labels and their source in detail; clears on a normalize()-equivalent spelling difference; fires identically whether the substitute is strictly more or less conservative than the declared branch (no merit ordering consulted)"
    requirement: "REQ-P10-03"
    verification:
      - kind: unit
        ref: "tests/test_frame_prereg.py#TestProcedureReconciliation"
        status: pass
      - kind: unit
        ref: "tests/test_frame_prereg.py#TestNoMeritConsultation"
        status: pass
    human_judgment: false
  - id: D3
    description: "A strictly more conservative substituted procedure still blocks DSX-PRE-030, and firing is symmetric in the direction of the swap — the check structurally cannot rank procedures (brief D-02) so its indifference to merit is proved by fixture, not by a second code"
    requirement: "REQ-P10-04"
    verification:
      - kind: unit
        ref: "tests/test_frame_prereg.py#TestNoMeritConsultation"
        status: pass
    human_judgment: false
  - id: D4
    description: "All five D-13 guards satisfied in the landing commit: _NOT_SHIPPED/_PARADIGM_INDEPENDENT matched-pair flip, PREFIX_GROUPS DSX-PRE entry, _D05_ALLOWLIST_PREFIXES inclusion, references/finding-codes.md regenerated, D-05 citation/structural-criterion/test-marker enforcement live for the family"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestParadigmManifest::test_applied_prefixes_have_codes_and_not_shipped_prefixes_have_none"
        status: pass
      - kind: unit
        ref: "tests/test_gen_finding_catalogue.py::TestD05RealTreeStandingGuarantee::test_real_tree_check_d05_is_empty"
        status: pass
      - kind: other
        ref: "python scripts/gen-finding-catalogue.py --check"
        status: pass
    human_judgment: false
  - id: D5
    description: "Malformed input shapes (non-dict spec, non-dict inference/analysis blocks, non-string fallback_rule) degrade to an empty/no-DSX-PRE report and never raise; DSX-PRE checks are behaviourally and source-level paradigm-independent"
    verification:
      - kind: unit
        ref: "tests/test_frame_prereg.py#TestMalformedShapesDegradeGracefully"
        status: pass
      - kind: unit
        ref: "tests/test_frame_prereg.py#TestParadigmIndependence"
        status: pass
      - kind: unit
        ref: "tests/test_frame_boundary.py::TestFrameParadigmReadBoundary::test_real_frame_modules_read_no_declared_paradigm"
        status: pass
    human_judgment: false

# Metrics
duration: ~20min
completed: 2026-08-20
status: complete
---

# Phase 10 Plan 02: DSX-PRE-010/DSX-PRE-030 and the five D-13 guards Summary

**`DSX-PRE-010`/`DSX-PRE-030` ship at CRITICAL with citations the catalogue actually enforces — declared-rule resolution and executed-vs-declared branch reconciliation that reads no procedure-merit ordering — and all five D-13 forcing guards flip green in the same commits that land their codes.**

## Performance

- **Duration:** ~20 min
- **Started:** 2026-08-20T02:44:38+02:00 (base commit)
- **Completed:** 2026-08-20T02:59:30+02:00
- **Tasks:** 3
- **Files modified:** 5 (dsx/frame/prereg.py, dsx/frame/paradigm.py, scripts/gen-finding-catalogue.py, references/finding-codes.md, tests/test_frame_prereg.py)

## Accomplishments

- `_check_rule_resolves(spec, resolution, report)` in `dsx/frame/prereg.py`: emits `DSX-PRE-010` (CRITICAL) when `resolution.reason` is set (a fallback rule naming a fact outside `PREREG_FACTS`, or a registry fact the spec does not declare as a number). Docstring carries the Gelman & Loken (2014) page-460 citation and a `Structural criterion:` line (no `Reference value:` anywhere in the module — D-15). Appends a `DecisionRecord` in both the fired and clear case.
- `_check_procedure_reconciliation(spec, resolution, report)`: emits `DSX-PRE-030` (CRITICAL) when `normalize(resolution.branch) != normalize(analysis.test)`. `detail` names both labels (the declared branch and its source — `fallback_rule` or `primary_procedure` — and the executed procedure at `analysis.test`). Returns early with no finding when the resolution is unresolved (a `DSX-PRE-010` case — one defect, one code) or when `analysis.test` is blank (no executed side to reconcile against). Docstring carries the Gelman & Loken (2014) page-463 and Simmons et al. (2011) page-1365 citations and the exact `Structural criterion: branch identity, never procedure merit` line. `remedy` states plainly that a more conservative substitute still blocks, why, and the `analysis.test` plan-time-scaffolding caveat.
- `check(spec, root=None, *, reconcile_trail=False) -> Report` dispatcher: guards non-dict spec, resolves the rule once, dispatches to both private helpers. `root`/`reconcile_trail` are defaulted and documented as unused until plans 03/04.
- All five D-13 guards flipped in the Task 1 commit: `_NOT_SHIPPED` (`dsx/frame/paradigm.py`) loses its `DSX-PRE-` entry; `_PARADIGM_INDEPENDENT` needed no edit (already listed it); `PREFIX_GROUPS` gains a `DSX-PRE` heading; `_D05_ALLOWLIST_PREFIXES` gains `"DSX-PRE-"`; `references/finding-codes.md` regenerated. `scripts/gen-finding-catalogue.py --check` exits 0 with zero D-05 problems.
- `tests/test_frame_prereg.py` gains four classes: `TestRuleResolutionFindings` (7 tests), `TestProcedureReconciliation` (7 tests) + `TestNoMeritConsultation` (2 tests, exactly the plan's required 9), `TestMalformedShapesDegradeGracefully` (4 tests), `TestParadigmIndependence` (2 tests) — 20 new tests total.

## Task Commits

Each task was committed atomically:

1. **Task 1: DSX-PRE-010, the check dispatcher, and all five D-13 guards in one commit** - `f361e4f` (feat)
2. **Task 2: DSX-PRE-030 naming both branch labels, blocking on identity and never on merit** - `948f88d` (feat)
3. **Task 3: Malformed shapes degrade gracefully and no DSX-PRE check reads paradigm** - `57710dd` (test)

_No TDD RED/GREEN split — `tdd="true"` tasks were implemented with behavior and tests landing together per task, verified green before commit, per the same pattern plan 01 established._

## Files Created/Modified

- `dsx/frame/prereg.py` - Adds `_check_rule_resolves`, `_check_procedure_reconciliation`, `check()`; imports `DecisionRecord` and `is_blank`
- `dsx/frame/paradigm.py` - `_NOT_SHIPPED` loses its `"DSX-PRE-"` entry (matched-pair flip with `_PARADIGM_INDEPENDENT`, which needed no change)
- `scripts/gen-finding-catalogue.py` - `PREFIX_GROUPS` gains a `DSX-PRE` entry; `_D05_ALLOWLIST_PREFIXES` gains `"DSX-PRE-"`
- `references/finding-codes.md` - Regenerated via `--write`, twice (once per code landing)
- `tests/test_frame_prereg.py` - Four new test classes, 20 tests, two `# D-05: DSX-PRE-0XX` markers

## Decisions Made

- **`DSX-PRE-010`'s `detail` is `resolution.reason` verbatim.** The reason templates built in plan 01 (`_UNKNOWN_FACT`, `_UNDECLARED_FACT`) already carry every specific the plan's behavior tests require (the offending fact name, the sorted accepted-names list, or the dotted registry path), so no re-derivation was needed at the finding call site.
- **The "pinned covered-code set at `tests/test_gen_finding_catalogue.py` line 227" the plan's `read_first` named does not exist as a literal in the live tree.** `test_d05_covered_code_set_on_the_real_tree_is_exactly_the_documented_set` computes the covered set dynamically from `g.collect()` against `_D05_ALLOWLIST_PREFIXES`/`_D05_ALLOWLIST_CODES` — it was already refactored to be self-verifying before this phase. No manual edit was needed there; adding `"DSX-PRE-"` to `_D05_ALLOWLIST_PREFIXES` was sufficient, and the test passed unmodified. Confirmed by direct read before relying on this.
- **`TestParadigmIndependence`'s "no `inference:` block at all" scenario declares the identical spec for both the frequentist and bayesian variant**, since there is no `inference` dict to declare a paradigm into. The property holds trivially and unconditionally for that scenario while still running through the same four-scenario comparison harness as the other three, matching the plan's literal instruction to include it as one of the four.

## Deviations from Plan

None - plan executed exactly as written. The one clarification worth flagging (the non-existent "pinned covered-code set" literal) is documented above under Decisions Made rather than as a deviation, since no fix was required — the dynamic test already covered the requirement.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `DSX-PRE-010` and `DSX-PRE-030` are live, CRITICAL, D-05-compliant, and paradigm-independent (behaviourally and source-level proven).
- `check(spec, root=None, *, reconcile_trail=False)` is ready for plan 03 to add `_check_content_lock` (wiring `root`) and for plan 04 to wire `reconcile_trail` and register the family in `GATE_PROFILES`/`run_checks` — `check()` is not yet registered anywhere in `dsx/cli.py`, which is out of this plan's scope and unaffected by these changes.
- `DSX-PRE-020` (the third code, plan 03's content-lock reconciliation) is untouched — `PREREG_FACTS`, `_resolve_branch`, and this plan's two new helpers give it a stable base to build on.
- No blockers. Full suite green (595/595, up from the 573/573 baseline before this plan), finding catalogue current, D-05 real-tree standing guarantee holds, D-03a and D-11 boundary scanners both clean against the extended module.

## Self-Check: PASSED

- FOUND: dsx/frame/prereg.py (both new functions and check() dispatcher)
- FOUND: dsx/frame/paradigm.py (_NOT_SHIPPED edit)
- FOUND: scripts/gen-finding-catalogue.py (PREFIX_GROUPS, _D05_ALLOWLIST_PREFIXES edits)
- FOUND: references/finding-codes.md (regenerated, contains DSX-PRE-010 and DSX-PRE-030)
- FOUND: tests/test_frame_prereg.py (four new classes)
- FOUND: f361e4f (Task 1 commit)
- FOUND: 948f88d (Task 2 commit)
- FOUND: 57710dd (Task 3 commit)

---
*Phase: 10-pre-registered-inference-plan-dsx-pre*
*Completed: 2026-08-20*
