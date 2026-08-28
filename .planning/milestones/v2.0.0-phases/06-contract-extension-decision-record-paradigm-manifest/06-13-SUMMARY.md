---
phase: 06-contract-extension-decision-record-paradigm-manifest
plan: 13
subsystem: testing
tags: [d-05, gen-finding-catalogue, ast, spec-validation, boundary-safety, gap-closure]

# Dependency graph
requires:
  - phase: 06-contract-extension-decision-record-paradigm-manifest
    provides: "06-03's D-05 mechanical-enforcement surface (scripts/gen-finding-catalogue.py) and 06-06's inference-block shape validators (dsx/spec.py) that this plan hardens"
provides:
  - "Boundary-safe D-05 enforcement set: hyphen-terminated family prefixes plus an explicit exact-code allow-list, replacing a mixed-shape tuple that silently over-matched on shared digits"
  - "A comment above dsx/spec.py::_INFERENCE_FIELDS that states exactly what inference-block validation enforces (3 of 6 fields vocabulary-checked, 1 rejected, unknown keys silently accepted)"
  - "A single-expression tests/test_frame_boundary.py::_package_for with the two-case reasoning kept as a comment instead of a dead branch"
affects: [06-review, phase-07, phase-08, phase-09, phase-11]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "D-05 allow-list boundary: hyphen-terminated family prefixes (startswith) OR an exact-code frozenset membership test — no bare numeric-string prefix"

key-files:
  created: []
  modified:
    - scripts/gen-finding-catalogue.py
    - tests/test_gen_finding_catalogue.py
    - dsx/spec.py
    - tests/test_frame_boundary.py

key-decisions:
  - "WR-01's alternative remedy (wire _INFERENCE_FIELDS into a real unknown-key check) explicitly declined — would mint a new finding code after this phase's catalogue was already regenerated and version-bumped, violating D-06's irreversible-numbering constraint. The comment was the defect; the comment is what changed."
  - "_D05_ALLOWLIST_CODES measured directly from collect() on the real tree (five DSX-SPEC-08x codes), not copied from review prose, per the plan's 'measure first' instruction"

patterns-established:
  - "D-20 exemption boundary is now structurally hyphen-safe rather than aspirationally so — a property test (test_every_d05_allowlist_prefix_ends_in_a_hyphen) fails immediately if a future contributor adds a non-hyphen-terminated prefix"

requirements-completed: []  # Deliberately empty — this plan hardens REQ-P6-11's delivery (06-03-PLAN.md) without re-claiming it; see <traceability> in 06-13-PLAN.md

coverage:
  - id: D1
    description: "D-05 enforcement boundary (_D05_ALLOWLIST_PREFIXES) is hyphen-terminated only; individually-enforced codes moved into a new exact-code frozenset (_D05_ALLOWLIST_CODES); check_d05 covers the union of both"
    requirement: null
    verification:
      - kind: unit
        ref: "tests/test_gen_finding_catalogue.py::TestD05Core::test_every_d05_allowlist_prefix_ends_in_a_hyphen"
        status: pass
      - kind: unit
        ref: "tests/test_gen_finding_catalogue.py::TestD05Core::test_check_d05_does_not_cover_a_longer_numeric_neighbour_of_an_enforced_code"
        status: pass
      - kind: unit
        ref: "tests/test_gen_finding_catalogue.py::TestD05Core::test_d05_covered_code_set_on_the_real_tree_is_exactly_the_documented_set"
        status: pass
      - kind: unit
        ref: "tests/test_gen_finding_catalogue.py::TestD05RealTreeStandingGuarantee::test_real_tree_check_d05_is_empty"
        status: pass
    human_judgment: false
  - id: D2
    description: "dsx/spec.py comment above _INFERENCE_FIELDS states four things true of the code as written: drift-guard-only consumer, not-a-closed-set, silently-accepted unknown keys, M-02's stopping_rule redirect — no executable line changed"
    requirement: null
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestSpecStructure (full class, includes test_inference_fields_constant_matches_req_p6_04)"
        status: pass
      - kind: other
        ref: "git diff -U0 dsx/spec.py — every changed line begins with '#' (comment-only diff)"
        status: pass
    human_judgment: false
  - id: D3
    description: "tests/test_frame_boundary.py::_package_for collapses two identical if/else arms into one unconditional parts[:-1] with a comment carrying the two-case reasoning"
    requirement: null
    verification:
      - kind: unit
        ref: "tests/test_frame_boundary.py::TestFrameImportBoundary (both tests, byte-identical, still green)"
        status: pass
      - kind: other
        ref: "direct call: _package_for(dsx/frame/__init__.py) == _package_for(dsx/frame/paradigm.py) == 'dsx.frame'"
        status: pass
    human_judgment: false

duration: ~20min
completed: 2026-08-08
status: complete
---

# Phase 06 Plan 13: D-05 Boundary Safety, Inference-Comment Honesty, Dead-Branch Collapse Summary

**Closed WR-03/WR-01/IN-01 from 06-REVIEW.md: the D-05 allow-list is now hyphen-safe with an exact-code set, `dsx/spec.py`'s inference-field comment states only what the code enforces, and a test helper's dead branch was collapsed to one expression — zero behavior change, zero new finding codes, catalogue byte-unchanged.**

## Performance

- **Duration:** ~20 min
- **Tasks:** 3
- **Files modified:** 4 (`scripts/gen-finding-catalogue.py`, `tests/test_gen_finding_catalogue.py`, `dsx/spec.py`, `tests/test_frame_boundary.py`)

## Accomplishments

- **WR-03 closed (D-05 boundary safety):** `_D05_ALLOWLIST_PREFIXES` narrowed to `("DSX-PAR-",)` — the only hyphen-terminated entry it ever held. The bare numeric-string prefix `"DSX-SPEC-08"` (which matched any code sharing those digits, with no boundary check after them) is gone, replaced by `_D05_ALLOWLIST_CODES = frozenset({"DSX-SPEC-080", "DSX-SPEC-081", "DSX-SPEC-082", "DSX-SPEC-085", "DSX-SPEC-086"})` — the exact five codes measured directly from `collect()` on the real tree. `check_d05`'s coverage comprehension now includes a row when its code starts with a family-prefix member *or* is a member of the exact-code set. Three new tests in `TestD05Core` prove the boundary structurally: every prefix ends in a hyphen, a synthetic longer numeric neighbour of an enforced code (e.g. `DSX-SPEC-0809`) is proven *not* swept into enforcement while the enforced code itself with the same non-compliant docstring still produces a problem, and the real-tree covered set equals exactly the union of family-matched and exact-code-matched codes.
- **WR-01 closed (inference-comment honesty):** The comment above `dsx/spec.py::_INFERENCE_FIELDS` no longer claims the six field names are read by "the catalogue" (they aren't — the only consumer is `tests/test_dsx.py::test_inference_fields_constant_matches_req_p6_04`). It now states plainly: the tuple is a drift-guard manifest, not an enforced closed set; only three fields (`paradigm`, `paradigm_justification`, `declared_at`) are vocabulary-checked; exactly one non-member (`stopping_rule`) is rejected; an unrecognised or misspelled key under `inference:` is accepted silently today. No executable line changed. The declined alternative remedy (wiring the constant into a real unknown-key check) was explicitly not taken — it would mint a new finding code after this phase's catalogue was already regenerated and version-bumped (D-06 makes numbering irreversible).
- **IN-01 closed (dead branch collapsed):** `tests/test_frame_boundary.py::_package_for`'s `if parts[-1] == "__init__": parts = parts[:-1] else: parts = parts[:-1]` collapsed to a single unconditional `parts = parts[:-1]`, with a comment carrying the two-case reasoning the docstring already narrates (an `__init__.py`'s package is its own directory; a plain module's package is its containing directory — both are "path minus last segment"). Verified directly against both real `dsx/frame/__init__.py` and `dsx/frame/paradigm.py`, both resolving to `dsx.frame`. The two `TestFrameImportBoundary` tests (REQ-P6-10's D-03a mechanical proof) are byte-for-byte unedited.

## Measured D-05 Covered Code Set (Task 1 evidence)

Before this plan (bare-prefix `startswith(("DSX-PAR-", "DSX-SPEC-08"))`) and after this plan
(hyphen-prefix-or-exact-code), `collect()` on the real tree produces the **identical** 6-code
covered set:

```
DSX-PAR-001
DSX-SPEC-080
DSX-SPEC-081
DSX-SPEC-082
DSX-SPEC-085
DSX-SPEC-086
```

This is the evidence the boundary change is set-preserving: no previously-enforced code became
exempt, and no previously-exempt legacy code became newly enforced. `python3 scripts/gen-finding-catalogue.py --check` exits 0 both structurally (catalogue current) and for D-05 (zero problems on the real tree).

## Task Commits

Each task was committed atomically:

1. **Task 1: Make the D-05 enforcement boundary boundary-safe (WR-03, D-20)** - `9023be7` (fix)
2. **Task 2: Correct the inference-validation comment to match what the code does (WR-01)** - `693fe0b` (docs)
3. **Task 3: Collapse the dead branch in the frame-boundary test helper (IN-01)** - `4e6044c` (refactor)

_Note: no plan-metadata commit is included above — the worktree executor's final metadata commit is created by the orchestrator after this SUMMARY is written, per the parallel-execution protocol._

## Files Created/Modified

- `scripts/gen-finding-catalogue.py` - `_D05_ALLOWLIST_PREFIXES` narrowed to hyphen-terminated family prefixes only; new `_D05_ALLOWLIST_CODES` frozenset; `check_d05`'s coverage comprehension and docstring updated for the two-part boundary
- `tests/test_gen_finding_catalogue.py` - Three new `TestD05Core` methods: hyphen-termination property test, longer-numeric-neighbour non-coverage test, real-tree covered-set regression test
- `dsx/spec.py` - Comment block above `_INFERENCE_FIELDS` rewritten to state the constant's real consumer, its non-closed-set status, and the silently-accepted unknown-key gap; no executable line changed
- `tests/test_frame_boundary.py` - `_package_for`'s two identical `if`/`else` arms collapsed to one `parts = parts[:-1]` with a reasoning comment

## Decisions Made

- **WR-01's alternative remedy declined.** Wiring `_INFERENCE_FIELDS` into a real unknown-key check would mint a new finding code (D-06: numbering is irreversible), and this phase's finding catalogue was already regenerated and version-bumped by earlier plans in this wave — minting a code here would be a contract addition smuggled in as a cleanup. The comment was the defect; only the comment changed.
- **`_D05_ALLOWLIST_CODES` measured, not transcribed.** The plan's "measure first" instruction was followed literally: `collect()` was run against the real tree before writing the constant, confirming the review's prose ("five `DSX-SPEC-08x` codes") matched the measured set exactly, rather than trusting the review's prose as the source of truth.

## Deviations from Plan

None — plan executed exactly as written. All three tasks' acceptance criteria passed on the first implementation without needing a Rule 1/2/3 auto-fix.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- All three carried-forward maintainability findings this plan targets (WR-01, WR-03, IN-01) are closed; `references/finding-codes.md` is byte-for-byte unchanged; `dsx/spec.py`'s only change is comment text; `_INFERENCE_FIELDS` is unmodified in value and order.
- WR-02 (non-atomic `next_invocation_id()` + `append()`) remains deliberately deferred per the plan's `<deferred_with_rationale>` — its documentation half lands in plan 06-11 (parallel in this wave); its OS-level-lock remedy is deferred to whichever phase first needs concurrent gate invocations (Phase 10 candidate).
- No blockers for downstream phases (7–12): this plan touched no code path any later phase depends on beyond the D-05 enforcement mechanism itself, which remains equally strict (same covered-code set, same `--check` exit-0 guarantee).

## Self-Check: PASSED

- FOUND: scripts/gen-finding-catalogue.py
- FOUND: tests/test_gen_finding_catalogue.py
- FOUND: dsx/spec.py
- FOUND: tests/test_frame_boundary.py
- FOUND: 9023be7 (git log)
- FOUND: 693fe0b (git log)
- FOUND: 4e6044c (git log)

---
*Phase: 06-contract-extension-decision-record-paradigm-manifest*
*Completed: 2026-08-08*
