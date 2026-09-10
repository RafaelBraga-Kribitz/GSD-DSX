---
phase: 28-evidence-case-magnitude-no-test-computed
reviewed: 2026-09-08T00:00:00Z
depth: deep
diff_base: caa9e4f
files_reviewed: 12
files_reviewed_list:
  - dsx/checks/claims.py
  - scripts/gen-finding-catalogue.py
  - templates/ANALYSIS-SPEC.yaml
  - references/finding-codes.md
  - examples/known-bad/magnitude-without-computed-effect-ANALYSIS-SPEC.yaml
  - examples/known-bad/magnitude-without-computed-effect-entrypoint.py
  - examples/known-bad/magnitude-without-computed-effect-POSTMORTEM.md
  - examples/known-bad/magnitude-without-computed-effect-ATTRIBUTION.yaml
  - tests/test_claims_supported_by.py
  - tests/test_known_bad_corpus.py
  - tests/test_finding_catalogue_invariant.py
  - tests/test_p19_categorical_rows.py
findings:
  blocker: 0
  high: 0
  medium: 1
  low: 2
  total: 3
status: issues_found
---

# Phase 28: Code Review Report

**Reviewed:** 2026-09-08
**Depth:** deep
**Files Reviewed:** 12 (diff base `caa9e4f`)
**Status:** issues_found (0 BLOCKER / 0 HIGH / 1 MEDIUM / 2 LOW)

## Summary

Phase 28 mints `DSX-CLM-034` (HIGH) — a declaration-gated claim→cited-test
magnitude traceability check — and promotes an honest MISS fixture
(`magnitude-without-computed-effect`). The core mint is correct, honestly
scoped, and defensively guarded. All 7 load-bearing invariants PASS on
mechanical verification: `dq.py` is byte-frozen, the catalogue moved 277→278 in
lockstep with the D-05 gate green, the fixture validates clean (CRITICAL=0) and
misses its target defect while firing only the swap-invariant DSX-COH-001
incidental, and the new `_PER_FIXTURE_INCIDENTAL_CODES` mechanism is read only by
the two completeness tests with its anti-laundering guard proven to have teeth
(a nobody's-target code injected into the map fails the membership guard; a
default-empty `incidental` leaves every existing call site byte-identical).

The full touched test surface is green on the real Python 3.12 interpreter
(725 passed / 1510 subtests; corpus + catalogue invariants 62 passed / 1102
subtests; catalogue `--check` exit 0).

No correctness, security, or data-loss defects were found. The three findings
below are quality/documentation drift: one stale test name+docstring that
asserts a different number than it advertises (MEDIUM), one stale docstring
enumeration (LOW), and one documented/behavioural asymmetry in how the new check
treats a claim's own declared CI versus DSX-CLM-033 (LOW, latent — no current
spec reaches it).

## Load-Bearing Invariant Verdicts

| # | Invariant | Verdict | Evidence |
|---|-----------|---------|----------|
| 1 | D-05 honesty (Wilkinson & TFSI 1999 = motivating principle only; `# D-05:` marker; code in `_D05_ALLOWLIST_CODES`) | **PASS** | Docstring cites Wilkinson & TFSI (1999) explicitly as "MOTIVATING PRINCIPLE only … does NOT mandate any numeric-overlap mechanism, and this check does not claim it does." `Citation:` and `Structural criterion:` lines both present (satisfy `_CITATION_RE`/`_REFVALUE_RE`). Marker `# D-05: DSX-CLM-034` at `tests/test_claims_supported_by.py:11`. Exact code in `_D05_ALLOWLIST_CODES` (`scripts/gen-finding-catalogue.py:218`), added by exact code not by prefix. `gen-finding-catalogue.py --check` exits 0. |
| 2 | Catalogue set-identity: one new HIGH row, 277→278, otherwise byte-stable, count pins in lockstep | **PASS (with MEDIUM doc-drift)** | Diff of `references/finding-codes.md` = only the `Total` line (277→278) + one `DSX-CLM-034 \| HIGH` row. `_EXPECTED_TOTAL=278` (invariant test), `test_p19_categorical_rows`/`test_phase20_zero_mint_close` pins at 278. Functional pins are in lockstep; the invariant test's *method name + docstring + failure message* were left at "277" (see WR-01). |
| 3 | DSX-CLM-034 SHIPPED, kept OUT of `_SECTION_65_BACKLOG_CODES` and any own-target/incidental map | **PASS** | Absent from `_SECTION_65_BACKLOG_CODES` (`test_known_bad_corpus.py:929-934`). `test_dsx_clm_034_is_not_a_per_fixture_incidental_anywhere` and `test_expected_caught_defects` confirm it is in neither the per-fixture incidental map nor any slug's own-target codes; `_EXPECTED_CAUGHT_DEFECTS[slug]=frozenset()`. |
| 4 | `dsx/checks/dq.py` byte-frozen | **PASS** | `git diff caa9e4f HEAD -- dsx/checks/dq.py` is empty. |
| 5 | Fixture stays an honest MISS | **PASS** | Spec declares NO `supported_by` on the magnitude claim. `dsx validate` → PASS, CRITICAL=0 HIGH=0. `_EXPECTED_CAUGHT_DEFECTS[slug]=frozenset()`. Live gate at ship fires `DSX-COH-001` CRITICAL and `DSX-CLM-034` ABSENT (`test_magnitude_fixture_lives_fires_coh_001_critical_at_ship` passes). ATTRIBUTION.yaml records the miss (absent_code: DSX-CLM-034, kind: miss). |
| 6 | `_PER_FIXTURE_INCIDENTAL_CODES` mechanism (D-28-06) | **PASS** | AST probe: `_classify_target_defect` references neither the constant nor `_per_fixture_incidental_codes` in executable code — `incidental` is a defaulted param used only in the no-expected branch (line 65), default `frozenset()` ⇒ byte-identical to prior behaviour. `_own_target_codes`/`_effective_target_map` do not read it. Anti-laundering guard proven live: injecting `DSX-QQQ-999` (nobody's target) yields `in other-targets == False` (guard trips); `DSX-COH-001` is another slug's declared target AND absent from global `_INCIDENTAL_GAP_CODES` (strictly narrower). DSX-CLM-034 (HIGH) deliberately excluded (severity trap preserved). |
| 7 | `_check_supported_by_traceability` correctness | **PASS (with LOW asymmetry, IN-01)** | Early-returns on absent `supported_by` and on empty `tests`; resolves reference from ONLY the named test(s); fires HIGH via string literal `"DSX-CLM-034"`; dispatched from the per-claim loop (`claims.py:84`). `_reconciles_to_sig_figs` is the AND of sig-figs equality and `_close_enough`, so it is never looser than DSX-CLM-033's window. Distinct code/severity from DSX-CLM-033 — no double-count, no weakening. `test_claims_supported_by.py` 13 tests pass. |

## Warnings

### WR-01: Catalogue-count invariant test name and docstring assert 277 while it enforces 278

**Severity:** MEDIUM
**File:** `tests/test_finding_catalogue_invariant.py:70-104`
**Issue:** The test method is named `test_finding_catalogue_stays_at_277_codes` and
its docstring states "declares, and enumerates, exactly 277 codes" and "Requiring
both to equal 277". The assertions, however, use `_EXPECTED_TOTAL = 278`
(line 42), so the test correctly enforces 278 and passes. The failure message
(lines 98-104) also enumerates mints only through DSX-VIZ-071 / Phase 22 and
omits Phase 27's DSX-ML-034 and Phase 28's DSX-CLM-034. This is a direct
violation of the phase's own "count pins moved to 278 in lockstep" discipline:
the numeric pin moved, but the human-facing name and docstring did not. A future
maintainer reading a green `...stays_at_277_codes` will be actively misled about
the enforced invariant.
**Failure scenario:** A later phase legitimately drops the total back to 277 (or a
mint/drop swap is investigated); a maintainer greps for the "277" test, sees it
green, and concludes the catalogue is at 277 — when it is at 278. The name lies
about what passed.
**Fix:** Rename to `test_finding_catalogue_stays_at_278_codes` and update the
docstring/failure-message prose (lines 71-82, 98-104) to read 278 and to name
DSX-ML-034 and DSX-CLM-034 in the mint chain, matching `_MINTED_CODES`.

## Info / Low

### IN-01: DSX-CLM-034 traces a claim's own declared `ci` to the cited test, unlike DSX-CLM-033

**Severity:** LOW
**File:** `dsx/checks/claims.py:325-360` (with `_extract_claim_magnitudes` at 405-437)
**Issue:** `_check_supported_by_traceability` builds its `reference` set from the
cited test(s) only (effect, effect×100, CI bounds and ×100). But `claim_numbers`
comes from the shared `_extract_claim_magnitudes(text, claim)`, which also folds
the claim's *own* declared `ci` bounds into the returned list (lines 431-436).
DSX-CLM-033 compensates by appending the claim's `ci` to its own `reference`
(lines 370-376) so a self-declared interval is self-consistent; DSX-CLM-034 does
not. The docstring says the check reads "every numeric literal in the claim
**text**", but a structured `claim.ci` field is also pulled in.
**Failure scenario:** A future, honest spec declares `supported_by: [some_test]`,
quotes the effect correctly, and also declares its own `claim.ci` that diverges
from the cited test's CI (e.g. a more conservative or separately-derived
interval). DSX-CLM-034 fires HIGH ("magnitude does not trace to its cited test")
on the claim's own interval even though nothing was copied from a wrong metric —
the exact false positive the "bounded-catch honesty" paragraph disclaims. No
current spec combines `supported_by` with a divergent `claim.ci`, so this is
latent, not live.
**Fix:** Either (a) mirror DSX-CLM-033 and append the claim's own `ci` to
`reference` before the reconciliation loop, or (b) if forcing the claim CI to
trace to the cited test is intended, tighten the docstring to say so explicitly
(drop "in the claim text") and add a covering test.

### IN-02: Stale mint enumeration in the set-identity test docstring

**Severity:** LOW
**File:** `tests/test_finding_catalogue_invariant.py:121-138`
**Issue:** The docstring of `test_code_set_is_phase12_snapshot_plus_the_sanctioned_mints`
enumerates the sanctioned delta ending at "Phase 22's DSX-VIZ-071" and never
mentions DSX-ML-034 (Phase 27) or DSX-CLM-034 (Phase 28), while the executable
`_MINTED_CODES` set (lines 49-57) correctly includes both. The test passes; only
the prose is stale.
**Failure scenario:** A reader auditing the sanctioned-mints list from the
docstring miscounts the expected set (misses two codes) and wrongly suspects an
unsanctioned mint. No functional impact.
**Fix:** Extend the docstring enumeration to list DSX-ML-034 and DSX-CLM-034,
matching `_MINTED_CODES`.

---

## Orchestrator disposition (S4-4, 2026-09-08 — gates re-run on real 3.12.10)

- **WR-01 (MEDIUM) — FIXED.** Renamed `test_finding_catalogue_stays_at_277_codes` →
  `..._278_codes`; docstring + failure message now read 278 and name DSX-ML-034 /
  DSX-CLM-034. Test-doc only, no assertion change. Suite still 1615 OK.
- **IN-02 (LOW) — FIXED** in the same edit (set-identity docstring enumeration extended).
- **IN-01 (LOW) — ACCEPTED (documented, tracked residual).** Latent, no shipped spec
  reaches the path (the fixture declares no `supported_by` → early return); the correct
  resolution is a genuine opposed design judgment (mirror DSX-CLM-033 vs. keep the
  stricter cite-only trace), deferred to a recorded decision rather than a rushed solo
  behavior change on a minted check. See `28-VERIFICATION.md` for the full rationale.

Verdict recorded in `28-VERIFICATION.md`: **passed, 3/3 REQ MET**.

---

_Reviewed: 2026-09-08_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: deep_
