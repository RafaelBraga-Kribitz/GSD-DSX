---
phase: 28
plan: 01
subsystem: dsx claims-discipline check + finding-catalogue
tags: [DSX-CLM-034, supported_by, traceability, D-05, D-13, live-miss]
status: complete
requires: [28-MEASUREMENT.md (VERDICT: LIVE MISS)]
provides: [DSX-CLM-034, _check_supported_by_traceability, claims[].supported_by, claims[].rounding]
affects: [dsx/checks/claims.py, references/finding-codes.md, templates/ANALYSIS-SPEC.yaml]
tech-stack:
  added: []
  patterns: [declaration-gated static check (DSX-REP-061 mould), significant-figures comparator, x100 percent/proportion scale bridge, exact-code D-05 allowlist]
key-files:
  created:
    - tests/test_claims_supported_by.py
  modified:
    - dsx/checks/claims.py
    - templates/ANALYSIS-SPEC.yaml
    - scripts/gen-finding-catalogue.py
    - references/finding-codes.md
    - tests/test_finding_catalogue_invariant.py
    - tests/test_phase20_zero_mint_close.py
    - tests/test_p19_categorical_rows.py
    - .planning/phases/28-evidence-case-magnitude-no-test-computed/28-MEASUREMENT.md
decisions:
  - "DSX-CLM-034 severity finalised HIGH (REQ-P28-02 + persona HIGH lean; traceability tier 030-032, non-overlapping with DSX-CLM-033 CRITICAL)."
  - "sig-figs comparator ANDs DSX-CLM-033's rel-5%/abs-5e-4 window so it is never looser (D-28-03 tighten-only)."
  - "supported_by single-string primary; list tolerated as an order-independent union (additive, no new code)."
metrics:
  tasks_completed: 3
  files_created: 1
  files_modified: 8
  full_suite: "OK (1606 tests)"
  catalogue_total: 278
requirements-completed: [REQ-P28-01, REQ-P28-02]
---

# Phase 28 Plan 01: Evidence case — magnitude no test computed (LIVE MISS mint) Summary

Minted `DSX-CLM-034` (HIGH) — a declaration-gated `claims[].supported_by` check that fires when a claim's headline magnitude cannot be traced to its cited `results.tests[]` entry within `claims[].rounding` significant figures — on the recorded `VERDICT: LIVE MISS`, with an honest Wilkinson & TFSI (1999) D-05 docstring (motivating principle only, stray-number bounded catch), moving the finding catalogue 277 → 278.

## What was executed (LIVE MISS branch)

Task 1 (the D-13 measurement) was already complete on entry: `28-MEASUREMENT.md` first line reads `VERDICT: LIVE MISS`. This run executed Tasks 2, 3, and Task 4 Branch B.

### Task 2 (RED)
Authored `tests/test_claims_supported_by.py` — 7 test methods (one per behaviour bullet: fires-on-uncovered, silent-when-covered, silent-when-absent, scale-bridge, tie-boundary, rounding-default, rounding-may-tighten), the standalone `# D-05: DSX-CLM-034` marker, and a Wilkinson-as-motivating-principle honesty comment (does NOT claim Wilkinson mandates the overlap mechanic). Confirmed RED: 3 "fires" assertions failed because `DSX-CLM-034` did not yet exist.

### Task 3 (GREEN)
- New function `_check_supported_by_traceability(claim, text, tests, where, report)` in `dsx/checks/claims.py`, dispatched from the per-claim loop alongside the other per-claim checks — a **separate** function, NOT inside `_check_numeric_overlap`. Returns early when `supported_by` is falsy (declaration-gated). Resolves reference numbers from ONLY the named test(s) (matched by `test["metric"]`), not the all-tests union DSX-CLM-033 uses. Reuses `_extract_claim_magnitudes` and the ×100 bridge; the sig-figs comparator (`_round_sig` / `_sig_figs_from_claim` / `_reconciles_to_sig_figs`) ANDs `_close_enough` so it is never looser than DSX-CLM-033's window (D-28-03). `report.add("DSX-CLM-034", "HIGH", …)` at `dsx/checks/claims.py:557` (severity as a string literal so the catalogue extractor picks it up). Docstring carries `Citation:` (Wilkinson & TFSI 1999, motivating principle only), `Structural criterion:` (declaration-level traceability corollary, DSX-REP-061 mould, never a recomputation), the tie-break/tolerance contract, and the bounded-catch honesty (catches via a stray number, not metric-identity).
- Two additive commented-optional keys `supported_by` / `rounding` in `templates/ANALYSIS-SPEC.yaml` after `# to_value: null`. No `dsx/spec.py` change (unknown claim keys are tolerated).
- `DSX-CLM-034` added to `_D05_ALLOWLIST_CODES` by **exact code** (never a `DSX-CLM-` prefix), with a precedent-style comment.
- Catalogue regenerated via `--write` (byte-deterministic across two writes): `references/finding-codes.md` Total 278, exactly one `DSX-CLM-034` HIGH row between 033 and 040.
- Count pins moved 277 → 278 in lockstep (see Deviations for the third pin).

### Task 4 Branch B (verification-only)
`brief.md` left unchanged (its §6.5 item 8 rewrite belongs to Plan 28-02). Recorded the verification-complete handoff to Plan 28-02 in `28-MEASUREMENT.md`.

## Verification (real interpreter: C:/Users/Benutzer1/AppData/Local/Programs/Python/Python312/python.exe)

- `python -m unittest tests.test_claims_supported_by -q` → OK (RED before Task 3; GREEN after).
- `python scripts/gen-finding-catalogue.py --check` → exit 0, "finding catalogue is current" (D-05 gate green at 278).
- Determinism: two consecutive `--write` runs produce byte-identical `references/finding-codes.md` (sha256 match).
- `python -m unittest tests.test_finding_catalogue_invariant tests.test_phase20_zero_mint_close -q` → OK.
- `python -m unittest discover -s tests -q` → OK (Ran 1606 tests).
- `git diff --stat -- dsx/checks/dq.py` → empty (byte-frozen).
- `git status --porcelain` for `.planning/REQUIREMENTS.md .planning/STATE.md .planning/ROADMAP.md` → empty (single-writer untouched).
- No stray `DECISIONS.jsonl`.

Finalised severity: **HIGH**. `report.add` site: `dsx/checks/claims.py:557`.

## Deviations from Plan

**1. [Rule 3 - Blocking issue / Rule 1 - Stale assertion] Third catalogue-total pin moved 277 → 278**
- **Found during:** Task 3, full-suite run.
- **Issue:** The plan and the orchestrator baselines named only two count pins (`tests/test_finding_catalogue_invariant.py::_EXPECTED_TOTAL` and `tests/test_phase20_zero_mint_close.py`). The full suite surfaced a third lockstep pin, `tests/test_p19_categorical_rows.py:83` (`_EXPECTED_TOTAL = 277`), which also asserts the catalogue Total and enumerates the sanctioned additive mints. Left at 277 it failed the binding "full suite green" acceptance criterion.
- **Fix:** Moved that pin to 278 with the same honest additive-rebaseline rationale (added "Phase 28's DSX-CLM-034 (278)" to both the module comment and the assertion message). No behaviour change; it is the identical class of lockstep count-pin move the plan already prescribes for the other two.
- **Files modified:** `tests/test_p19_categorical_rows.py`.
- **Commit:** (uncommitted — this run is write-only per orchestrator instruction).

**2. [Rule 2 - Correctness] `_MINTED_CODES` set updated in the invariant test**
- **Found during:** Task 3.
- **Issue:** `tests/test_finding_catalogue_invariant.py` compares the live catalogue code SET to `snapshot ∪ _MINTED_CODES`. Moving only `_EXPECTED_TOTAL` would pass the count leg but fail the set-identity leg (278 catalogue vs 277 expected set).
- **Fix:** Added `"DSX-CLM-034"` to `_MINTED_CODES` and refreshed the stale "live catalogue is 275" cosmetic comment to 278.
- **Files modified:** `tests/test_finding_catalogue_invariant.py`.

No other deviations. The frozen design (D-28-00..05) was not re-opened. `dsx/checks/dq.py` untouched.

## Known Stubs
None.

## Threat Flags
None — no new network/auth/file-access surface. The new check reads `claim.get("supported_by")`/`claim.get("rounding")` off a parsed spec dict (V5 input validation); no entrypoint is executed.

## Self-Check: PASSED
- `tests/test_claims_supported_by.py` — FOUND.
- `dsx/checks/claims.py` `_check_supported_by_traceability` + `report.add("DSX-CLM-034", "HIGH", …)` at line 557 — FOUND.
- `references/finding-codes.md` Total: 278 codes, one `DSX-CLM-034` HIGH row — FOUND.
- Full suite OK (1606 tests); catalogue `--check` exit 0; `dq.py` frozen — CONFIRMED.

## Handoff
Phase proceeds to **Plan 28-02** (fixture promotion into `examples/known-bad/`, harness wiring incl. the `_PER_FIXTURE_INCIDENTAL_CODES` entry for the swap-invariant `DSX-COH-001` incidental per D-28-06, spec-count move 43 → 44, and the brief §6.5 item 8 rewrite). All edits from this run are left **uncommitted** in the working tree for the orchestrator to commit with plain git (write-only mandate).
