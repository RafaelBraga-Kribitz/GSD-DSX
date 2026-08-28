---
phase: 10-pre-registered-inference-plan-dsx-pre
plan: 03
subsystem: testing
tags: [content-lock, decision-trail, provenance, exit-codes, dsx-frame]

# Dependency graph
requires:
  - phase: 10-pre-registered-inference-plan-dsx-pre (plan 02)
    provides: "check(spec, root=None, *, reconcile_trail=False) dispatcher, DSX-PRE-010/DSX-PRE-030, all five D-13 guards flipped (DSX-PRE- now under D-05 citation enforcement)"
provides:
  - "_recorded_plan_digests(root) — set membership over every plan-gate-point frame_digest in the decision trail, tolerant of a missing/corrupt/unreadable trail via read_all's never-raises contract"
  - "_check_content_lock(spec, root, report) — raises CheckError (exit 2) when no plan-time header is recorded at all, naming the ordinary fix (dsx gate plan) and the M-07 grandfather route (suppressions[] + ADR/SPEC authority) so a pre-v2.0.0 spec stays walkable; once a plan header exists, emits DSX-PRE-020 (CRITICAL) when declared_at: pre_data is contradicted by the recorded bytes, and stays silent for post_data or an absent claim"
  - "check() now gates _check_content_lock behind reconcile_trail — inert (zero-cost, no call at all) when a caller does not opt in, which is every caller today since prereg is still unregistered in GATE_PROFILES"
affects: [10-04-dsx-pre, 10-05-dsx-pre, 10-06-dsx-pre]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Read sub-fields off an already-validated dict (inference.get('declared_at')) rather than the module's dotted-path get(spec, 'inference.declared_at') helper — a positional 'inference.'-prefixed string literal passed to any call is exactly what tests/test_frame_boundary.py's D-11 AST scanner flags, regardless of which frame module the call lives in"
    - "No try/except around read_all() — its own contract is that it never raises for any on-disk state (missing, unreadable, or corrupt all degrade to []); wrapping it would suggest otherwise to the next reader"
    - "Set membership over every recorded plan-gate-point digest, never most-recent-or-earliest — InvocationHeader carries no spec identity, so a shared trail root mixes headers from every spec ever gated against it, and any ordering rule produces cross-specification false positives"

key-files:
  created: []
  modified:
    - dsx/frame/prereg.py
    - references/finding-codes.md
    - tests/test_frame_prereg.py

key-decisions:
  - "check()'s dispatcher is wired in this plan (not deferred to plan 04): reconcile_trail now gates a real call to _check_content_lock inside check() itself, because Task 1's own behavior tests (check(spec, root, reconcile_trail=True) raising CheckError) require it to actually run. Plan 02's forward-reference ('plan 04 wires reconcile_trail') is read as referring to the CLI-level decision of *when* a real caller passes reconcile_trail=True (dsx gate only, via the gate_invocation keyword and GATE_PROFILES registration) — not to the check() function signature, which this plan completes."
  - "The missing-header CheckError message names 'authority' explicitly (not just 'authorises') so a caller grepping the exit-2 text for the ADR/SPEC authority requirement finds it; matched to test 4's literal assertion."
  - "current_digest truncated to current_digest[:12] in both the DSX-PRE-020 detail text and the DecisionRecord choice field, per the plan's literal instruction (\"truncated to its first twelve characters\")."
  - "tests/test_gen_finding_catalogue.py needed no edit — confirmed by direct read, same finding as plan 02's SUMMARY: the covered-code-set test computes coverage dynamically from g.collect() against _D05_ALLOWLIST_PREFIXES (already includes 'DSX-PRE-' from plan 02), so DSX-PRE-020 is covered automatically once its docstring carries Citation/Structural criterion and a # D-05: DSX-PRE-020 test marker exists."

patterns-established:
  - "_check_content_lock's docstring records the decision-trail status transition explicitly: before Phase 10 DECISIONS.jsonl was a write-only side channel (only dsx explain ever read it, never gating); from this function on, the plan-time header is a gate input at verify/ship. The write path (dsx/cli.py::_write_decision_trail) remains a side channel that can never itself change an exit code — the two statements are compatible because they describe opposite directions of the same file."

requirements-completed: [REQ-P10-02]

coverage:
  - id: D1
    description: "A gate run with reconcile_trail=True and no plan-gate-point header recorded anywhere in the trail (missing file, corrupt file, or a trail holding only execute/verify/ship headers) raises CheckError and exits 2, never a silent pass; the message names the resolved trail path, that dsx gate plan has never run, the ordinary fix, and the suppressions[]/ADR-SPEC-authority grandfather route by name. reconcile_trail=False leaves the trail-dependent half fully inert (no findings, no exception, no file access side effect visible to the caller). root=None degrades to the same CheckError shape, never a TypeError."
    requirement: "REQ-P10-02"
    verification:
      - kind: unit
        ref: "tests/test_frame_prereg.py#TestMissingPlanHeader"
        status: pass
    human_judgment: false
  - id: D2
    description: "DSX-PRE-020 fires at CRITICAL when inference.declared_at normalizes to pre_data and the spec's current frame_digest is absent from every recorded plan-gate-point digest; clears when the digest is present regardless of append order (proving set membership, not most-recent-or-earliest); declared_at: post_data and an absent declared_at both stay legal and silent even against a mismatching trail; an edit outside validity_frame:/inference: does not change the digest and therefore does not fire; detail names the recorded header count and the truncated current digest, remedy names the ordinary fix and the known re-registration limit; a DecisionRecord is appended in both the fired and clear case."
    requirement: "REQ-P10-02"
    verification:
      - kind: unit
        ref: "tests/test_frame_prereg.py#TestContentLockReconciliation"
        status: pass
  - id: D3
    description: "D-05 citation enforcement is live and green for DSX-PRE-020: gen-finding-catalogue.py --check exits 0, references/finding-codes.md lists DSX-PRE-020, the # D-05: DSX-PRE-020 test marker exists, dsx.suppressions.known_codes() reports all three DSX-PRE-* codes, and the module contains no 'Reference value:' literal (the family takes the Structural criterion branch throughout)."
    verification:
      - kind: unit
        ref: "tests/test_gen_finding_catalogue.py::TestD05RealTreeStandingGuarantee::test_real_tree_check_d05_is_empty"
        status: pass
      - kind: other
        ref: "python scripts/gen-finding-catalogue.py --check"
        status: pass
      - kind: other
        ref: "python -c \"from dsx.suppressions import known_codes; print(sorted(c for c in known_codes() if c.startswith('DSX-PRE-')))\""
        status: pass
    human_judgment: false
  - id: D4
    description: "Full suite green at 611/611 (up from the 595 baseline before this plan — 16 new tests), tests.test_frame_boundary green (the D-11 AST scanner does not flag _check_content_lock's inference.get('declared_at') dict read or the where='inference.declared_at' keyword argument), prereg still unregistered anywhere in dsx/cli.py so this plan carries no gate blast radius."
    verification:
      - kind: unit
        ref: "python -m unittest discover -s tests -q"
        status: pass
      - kind: unit
        ref: "tests.test_frame_boundary"
        status: pass
      - kind: other
        ref: "grep -n prereg dsx/cli.py (zero matches)"
        status: pass
    human_judgment: false

# Metrics
duration: ~11min
completed: 2026-08-20
status: complete
---

# Phase 10 Plan 03: DSX-PRE-020 content-lock reconciliation Summary

**`_check_content_lock` reads the plan-time frame_digest lock out of `DECISIONS.jsonl` — a missing plan-gate-point header now aborts the run at exit 2 with the M-07 grandfather route named, and a `declared_at: pre_data` claim never registered at plan blocks at CRITICAL under `DSX-PRE-020`, by set membership over every recorded plan digest, never most-recent-or-earliest.**

## Performance

- **Duration:** ~11 min
- **Started:** 2026-08-20T03:02:44+02:00 (base commit)
- **Completed:** 2026-08-20T03:13:37+02:00
- **Tasks:** 2
- **Files modified:** 3 (dsx/frame/prereg.py, references/finding-codes.md, tests/test_frame_prereg.py)

## Accomplishments

- `_recorded_plan_digests(root)` in `dsx/frame/prereg.py`: builds `decisions_path(root)`, reads it with `read_all` (no try/except — the function's contract is that it never raises), and collects `frame_digest` from every record whose `record_type` is `"invocation"` and `gate_point` is `"plan"`. `root=None` guards to an empty set before any `Path()` construction.
- `_check_content_lock(spec, root, report)`: raises `CheckError` when the recorded set is empty, with a four-clause message (what happened, why it stops the run, the ordinary fix `dsx gate plan`, and the `suppressions[]`/ADR-SPEC-authority grandfather route named explicitly). Once a plan header exists, reads `declared_at` off the already-validated `inference` dict (never a dotted-path positional literal, avoiding the D-11 AST scanner's `"inference."`-prefix trap) and returns silently unless it normalises to `pre_data`. Computes `frame_digest(spec)`, tests membership in the recorded set, and emits `DSX-PRE-020` (CRITICAL) when absent. A `DecisionRecord` is appended in both the fired and clear case.
- `check(spec, root=None, *, reconcile_trail=False)` dispatcher: now calls `_check_content_lock(spec, root, report)` when `reconcile_trail` is `True`, and calls it not at all otherwise — the trail-dependent half stays fully inert for every caller today (`prereg` is still unregistered in `dsx/cli.py`, confirmed by direct grep).
- `references/finding-codes.md` regenerated (`--write`): `DSX-PRE-020` now listed under the `Pre-registered inference plan` group.
- `tests/test_frame_prereg.py` gains two classes: `TestMissingPlanHeader` (8 tests, Task 1) and `TestContentLockReconciliation` (8 tests, Task 2) — 16 new tests total, all green on first run after one message-wording fix.

## Task Commits

Each task was committed atomically:

1. **Task 1: Read the decision trail and refuse to run without a plan-time header** - `dcee132` (feat)
2. **Task 2: DSX-PRE-020 — the pre_data claim contradicted by the recorded bytes** - `112350b` (feat)

_No TDD RED/GREEN split — `tdd="true"` tasks were implemented with behavior and tests landing together per task, verified green before commit, matching the pattern established in plans 01/02._

## Files Created/Modified

- `dsx/frame/prereg.py` - Adds `_recorded_plan_digests`, `_check_content_lock`; imports `decisions_path`, `frame_digest`, `read_all` from `..decisions`; `check()` now conditionally calls `_check_content_lock` on `reconcile_trail`
- `references/finding-codes.md` - Regenerated via `--write`; `DSX-PRE-020` now listed
- `tests/test_frame_prereg.py` - Two new test classes (`TestMissingPlanHeader`, `TestContentLockReconciliation`), 16 tests, one `# D-05: DSX-PRE-020` marker

## Decisions Made

- **`check()`'s dispatcher is wired to `reconcile_trail` in this plan, not deferred to plan 04.** Task 1's own behavior tests call `check(spec, root, reconcile_trail=True)` and require it to raise `CheckError` — that only works if `check()` actually invokes `_check_content_lock` when the flag is set. Plan 02's SUMMARY forward-reference ("plan 04 wires `reconcile_trail`") is read as describing the CLI-level decision of *when* a real caller (only `dsx gate`, never `validate`/`check`/`audit`) passes `reconcile_trail=True` at all — via the `gate_invocation` keyword and `GATE_PROFILES` registration that plan 04 adds — not the `check()` function signature itself, which this plan completes. No `GATE_PROFILES` entry exists yet, so this wiring carries zero blast radius today.
- **`declared_at` is read via `inference.get("declared_at")` on the already-validated dict, never `get(spec, "inference.declared_at")`.** The known trap flagged in this plan's prior-wave context — `tests/test_frame_boundary.py`'s D-11 AST scanner flags any positional `"inference."`-prefixed string literal passed to a call, regardless of intent. `where="inference.declared_at"` in `report.add(...)` is safe because it's a keyword argument, which the scanner does not inspect (only `node.args`).
- **The missing-header message says "...that is its authority (the ADR/SPEC authority requirement)"** rather than only "...that authorises it" — the literal word "authority" is what a caller (and this plan's own test 4) greps for; "authorises" alone does not contain that substring.
- **`tests/test_gen_finding_catalogue.py` needed no manual edit**, confirmed by direct read before relying on it: the pinned "covered code set" is computed dynamically from `g.collect()` against `_D05_ALLOWLIST_PREFIXES` (which already includes `"DSX-PRE-"` from plan 02), so `DSX-PRE-020` is covered automatically the moment its docstring carries a compliant `Citation:`/`Structural criterion:` pair and a `# D-05: DSX-PRE-020` test marker exists anywhere in `tests/`.

## Deviations from Plan

None — plan executed exactly as written. One implementation-order note worth flagging: my first pass wrote Tasks 1 and 2's code changes in a single combined edit before realizing the plan requires atomic per-task commits; I reverted `_check_content_lock` to a Task-1-only scope (raise-only, no `pre_data`/digest logic, trimmed docstring) before the first commit, then re-added Task 2's extension as a second edit and commit. No functional deviation — final code and tests match the plan's Task 1/Task 2 boundary exactly; this is a self-correction during authoring, not a deviation from what was specified.

## Issues Encountered

One test-authoring iteration: `test_4_message_names_suppressions_and_authority_and_trail_path` initially failed because the `CheckError` message said "...authorises it" without the standalone word "authority". Fixed by rewording the message to "...that is its authority (the ADR/SPEC authority requirement)"; all 8 `TestMissingPlanHeader` tests then passed. No other iteration was needed — `TestContentLockReconciliation`'s 8 tests passed on the first run.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- All three `DSX-PRE-*` codes now ship (`DSX-PRE-010`, `DSX-PRE-020`, `DSX-PRE-030`), all D-05-compliant, all reachable from `dsx.suppressions.known_codes()`.
- `_check_content_lock` and `_recorded_plan_digests` give plan 04 a stable base: `check()`'s `reconcile_trail` parameter already gates a real, tested code path — plan 04's job is narrowed to the CLI-level wiring (the `gate_invocation` keyword on `run_checks`, `GATE_PROFILES` registration, and repairing `_write_decision_trail`'s docstring to match the now-conditional read side), not to teaching `check()` a new capability.
- `prereg` remains unregistered anywhere in `dsx/cli.py` (confirmed by direct grep) — this plan carries zero gate blast radius, matching the phase's wave ordering.
- No blockers. Full suite green (611/611, up from the 595 baseline before this plan), finding catalogue current (only the three phase-07-owned pre-existing double-declaration warnings remain: `DSX-VAL-021`, `DSX-VAL-060`, `DSX-COH-030`/`DSX-SPEC-070`/`DSX-PAR-002` — none introduced by this plan), D-05 real-tree standing guarantee holds, D-11 paradigm-read boundary scanner clean against the extended module.

## Self-Check: PASSED

- FOUND: dsx/frame/prereg.py (`_recorded_plan_digests`, `_check_content_lock`, updated `check()`)
- FOUND: references/finding-codes.md (regenerated, contains `DSX-PRE-020`)
- FOUND: tests/test_frame_prereg.py (`TestMissingPlanHeader`, `TestContentLockReconciliation`)
- FOUND: dcee132 (Task 1 commit)
- FOUND: 112350b (Task 2 commit)

---
*Phase: 10-pre-registered-inference-plan-dsx-pre*
*Completed: 2026-08-20*
