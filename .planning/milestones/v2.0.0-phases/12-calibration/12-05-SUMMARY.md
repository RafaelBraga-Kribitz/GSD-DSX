---
phase: 12-calibration
plan: 05
subsystem: test-harness / calibration
status: complete
requirements-completed: [REQ-P12-03]
tags: [catch-rate, fpr, stratified, miss-rate, headline-invariance, D-04, D-09, D-10, D-18]
dependency_graph:
  requires:
    - "examples/good-corpus/ — 12 clean control specs (plan 12-04, the FPR denominator)"
    - "tests/test_known_bad_corpus.py::_gate_findings + _classify_target_defect (live measurement substrate)"
    - "examples/known-bad/*-ATTRIBUTION.yaml — 3 live-confirmed miss sidecars (plans 12-01/12-03)"
    - "_effective_target_map / _TARGET_DEFECT_CODES / _EXPECTED_CAUGHT_DEFECTS (PRESENT partition source)"
  provides:
    - "test_stratified_catch_rate_and_fpr_report — the live (miss-rate, FPR) headline (consumed by plan 12-07 §6.5 re-eval)"
    - "_false_positive_findings / _headline / _FPR_TEMPDIR_NOISE_CODES / _ABSENT_PARTITION_FLOOR reusable helpers"
  affects:
    - "plan 12-07 (re-evaluates §6.5 against this measured (miss-rate, FPR) headline)"
tech_stack:
  added: []
  patterns:
    - "two-proofs discipline: a live integration test over a clean-by-construction corpus, backed by filesystem-independent synthetic proofs that carry the non-degenerate RED signal"
    - "documented tempdir-noise allowlist mirroring _INCIDENTAL_GAP_CODES, kept a separate NEW constant (never lifted from a stale ledger, D-09)"
    - "headline function whose signature accepts the PRESENT partition but whose output ignores it — structural invariance to easy catches"
key_files:
  created:
    - ".planning/phases/12-calibration/12-05-SUMMARY.md"
  modified:
    - "tests/test_known_bad_corpus.py (stratified catch-rate + FPR harness, 2 helpers, 1 live test, 4 synthetic proofs)"
metrics:
  module_tests_before: 33
  module_tests_after: 38
  finding_codes_minted: 0
  completed: 2026-08-27
---

# Phase 12 Plan 05: Stratified Catch-Rate and FPR Harness Summary

The measurement step that turns "reduced risk" into a number. `tests/test_known_bad_corpus.py`
now carries `test_stratified_catch_rate_and_fpr_report`: a live-computed stratified catch rate
with independent PRESENT/ABSENT denominators, a false-positive rate over the plan-12-04
good-control corpus with tempdir-noise resolved, and the headline pair **(miss-rate, FPR)** with a
floored ABSENT partition and a target-present-invariance proof. Every number is computed live via
`self._gate_findings` + `_classify_target_defect` (D-09); nothing is lifted from
`_INCIDENTAL_GAP_CODES` or `_GOLDEN_SHIP_FINDINGS`. Zero finding codes minted; the catalogue stays
256 (D-18). Only `tests/test_known_bad_corpus.py` changed.

## The measured headline (all computed LIVE this run)

| Number | Value | Numerator / Denominator | Source |
|--------|-------|-------------------------|--------|
| **FPR (good-control corpus)** | **0.0** | **0 / 12** | `self._gate_findings(spec, "ship")` over `examples/good-corpus/*-ANALYSIS-SPEC.yaml`, tempdir-noise excluded |
| **ABSENT-partition miss-rate** | **1.0** | **3 / 3** | 3 attribution sidecars (kind "miss"); each named absent code fires nowhere CRITICAL across plan/execute/verify/ship |
| **PRESENT-partition catch rate** | **1.0** | **9 / 9** | `_classify_target_defect` over every (slug, point) cell the effective target map expects |
| **Headline** | **(1.0, 0.0)** | (miss-rate, FPR) | `_headline(present, absent, fpr)` — miss-rate from ABSENT alone, FPR from good corpus |

The honest calibration story this headline tells: the gate has **zero false positives** on 12 clean
control specs, but **misses 100%** of the semantic-defect coverage class (the three miss fixtures —
undisclosed forking / data fabrication / undisclosed selective exclusion — that a declaration-only
gate structurally cannot catch and that need currently-unwritten §6.5 checks). A single catch-rate
number would have read ~100% and hidden the misses entirely; the (miss-rate, FPR) pair with a
floored ABSENT partition is what stops that.

### ABSENT-partition floor

`_ABSENT_PARTITION_FLOOR = 3` (matching the corpus's own ≥3 pair floor). The test asserts
`absent_denom (3) >= _ABSENT_PARTITION_FLOOR (3)` **and** `_ABSENT_PARTITION_FLOOR > 0`, so a
zero-representation (100%-present) corpus is rejected by construction — a corpus with too few miss
cases is a regression-pin dressed as detection, not a calibration (D-10).

### Invariance construction

`_headline(present, absent, fpr)` takes the PRESENT partition `(caught, denom)` for signature
symmetry but derives the miss-rate from the ABSENT partition alone and the FPR from the good corpus
alone — its output is structurally independent of `present`. The live test proves this by computing
`headline_after = _headline((present_caught+1, present_denom+1), absent, fpr)` — one synthetic
already-caught target-PRESENT case injected — and asserting it is byte-identical to `headline`.
Adding easy catches is therefore mathematically incapable of moving the headline (D-10). A
non-degenerate synthetic proof (`test_headline_is_invariant_to_adding_a_target_present_case`, with
`present=(2,5)`, `absent=(1,4)`, `fpr=(1,10)`) exercises the same invariant off degenerate values.

## What was built

- **`GOOD_CORPUS_DIR`** + a live FPR loop over `examples/good-corpus/` (denominator 12 ≥ 10, D-04).
- **`_FPR_TEMPDIR_NOISE_CODES`** — a NEW documented allowlist of the four artifact-stripping
  tempdir-noise codes (`DSX-DQ-001`, `DSX-CLM-031`, `DSX-FIG-001`, `DSX-NAR-010`), each carrying an
  inline reason, mirroring `_INCIDENTAL_GAP_CODES`' house style. Kept separate and never read from
  a stale ledger (D-09). A block whose `where` names a file path is excluded from the FPR count.
- **`_false_positive_findings(findings, noise_codes)`** — CRITICAL/HIGH blocking codes minus the
  noise allowlist. Parameterised so a synthetic proof drives it without the gate.
- **`_headline(present, absent, fpr)`** — the (miss-rate, FPR) pair, invariant to `present`.
- **`_ABSENT_PARTITION_FLOOR = 3`** — the minimum-representation gate.
- **`test_stratified_catch_rate_and_fpr_report`** — the live integration test computing all four
  numbers and asserting the floor, the headline shape, and the invariance.
- **`TestStratifiedHeadlineHelpers`** — four filesystem-independent synthetic proofs of the FPR
  noise-exclusion and the headline arithmetic (the RED signal).

## TDD gate compliance

- **RED** `4c10b5e` (`test(12-05)`): naive `_false_positive_findings` (counts noise) and naive
  `_headline` (folds PRESENT into miss-rate) — the four synthetic proofs fail (`FAILED (failures=4)`).
- **GREEN** `ce67345` (`feat(12-05)`): both helpers corrected — target test and full module green.
- **SUMMARY** this commit (`docs(12-05)`).

The `test(...)` → `feat(...)` gate sequence is satisfied. Note: both helpers live in the one test
file (`files_modified` is exactly `tests/test_known_bad_corpus.py`), so the RED/GREEN split is
between the naive and corrected forms of the measurement helpers rather than across a test/source
file boundary. The `feat` type is used for the GREEN commit because the live measurement harness is
this measurement-phase's product (the plan objective: "the measurement step that turns reduced risk
into a number").

## Deviations from Plan

1. **The RED signal comes from filesystem-independent synthetic proofs, not from the live
   good-corpus.** The plan's Task-1 RED narrative ("a naive FPR that counts the four noise codes
   reports a spuriously high rate; GREEN after seeding/exclusion") presupposes the *seed route*.
   Plan 12-04 explicitly did **not** take that route — it recorded a third, cleaner outcome
   ("minimal-reference via cwd-resolvable committed artifacts", 12-04-SUMMARY lines 61-81), so the
   good-corpus fires **no** tempdir-noise codes at all and the live FPR is 0/12 whether or not the
   exclusion is wired. The live measurement is therefore clean-by-construction and cannot carry a
   RED. Following the module's own two-proofs discipline (`TestClassifyTargetDefectHelper`), the
   non-degenerate RED is carried by fabricated-input synthetic proofs, and the tempdir-noise
   allowlist is retained as the standing guard that keeps the FPR honest if a future control spec
   ever references an unresolvable sibling artifact. This honours the plan's third prohibition
   (file-path-`where` findings never count) exactly, via the documented allowlist route the plan
   itself offers as the alternative to seeding.
2. **Tasks 1 and 2 committed as one RED + one GREEN pair, not two.** The plan's Task 2 literally
   "extend[s] `test_stratified_catch_rate_and_fpr_report`" — the same method Task 1 creates — and
   both share one verify command, so a single RED→GREEN pair covering the whole method is the
   atomic unit. No behaviour from either task was dropped.
3. **Floor / invariance are separate assertions.** The plan's verification bullet ("The invariance
   check demonstrably fails if the ABSENT partition floor is removed") conflates two guarantees;
   they are implemented as two distinct, independently-failing assertions (the floor gate and the
   `_headline` invariance), which is the substantive intent (floored ABSENT partition + provable
   easy-catch immunity).

## Boundary compliance

- **Touched only** `tests/test_known_bad_corpus.py` (`git diff --name-only` across both commits
  lists exactly that one file).
- **No change to** `dsx/` (any file), `references/finding-codes.md`, `GATE_PROFILES`/`CHECKS`, or
  `scripts/gen-finding-catalogue.py` — `git status --short` for those paths is empty. **Zero
  finding codes minted (D-18)**; catalogue verified unchanged at **256**.
- **Every reported number computed live** via `self._gate_findings` / `_classify_target_defect`;
  the new test body does not read `_INCIDENTAL_GAP_CODES` or `_GOLDEN_SHIP_FINDINGS` (D-09).
- **No shared tracking file edited** — `.planning/STATE.md`, `.planning/ROADMAP.md`,
  `.planning/LOOP-LEDGER.md` were not staged. The orchestrator writes those serially after the wave
  merges; the normal execute-plan STATE/ROADMAP advance step was intentionally skipped.
- **Not pushed** — the orchestrator re-gates the whole wave and pushes.

## Verification (verbatim)

### Target test — `python -m unittest tests.test_known_bad_corpus.TestKnownBadCorpus.test_stratified_catch_rate_and_fpr_report -v`

```
Ran 1 test in 2.243s

OK
```

### Full module — `python -m unittest tests.test_known_bad_corpus`

```
Ran 38 tests in 5.838s

OK
```

### Co-regression, golden suite — `python -m unittest tests.test_causal_verb_golden`

```
Ran 6 tests in 2.342s

OK
```

### RED confirmation (at commit 4c10b5e) — `python -m unittest tests.test_known_bad_corpus.TestStratifiedHeadlineHelpers`

```
Ran 4 tests in 0.001s

FAILED (failures=4)
```

## Self-Check: PASSED

- `.planning/phases/12-calibration/12-05-SUMMARY.md` exists on disk.
- Both code commits exist: `4c10b5e` (RED, test) and `ce67345` (GREEN, feat).
- `git diff --name-only` across both commits touches only `tests/test_known_bad_corpus.py`.
- Catalogue re-counted live at 256; `git status --short dsx/ references/finding-codes.md
  scripts/gen-finding-catalogue.py` is empty.
- Module green at 38 tests (was 33); golden suite green at 6.
