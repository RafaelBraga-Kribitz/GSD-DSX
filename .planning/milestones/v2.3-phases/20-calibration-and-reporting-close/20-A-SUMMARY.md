---
phase: 20-calibration-and-reporting-close
plan: A
subsystem: calibration-and-known-bad-corpus
tags: [calibration, catch-rate, fpr, known-bad-corpus, high-stratum, negative-controls, re-baseline, measurement-integrity, fixtures]
requires: [20-C, 20-D]
provides:
  - five PRESENT known-bad fixtures firing the five Phase-18 codes (DSX-STA-050/051/060/061/062)
  - three valid good-corpus negative controls (correlation / ICC / weighted-kappa families)
  - live HIGH verify/ship calibration stratum (third readout beside the miss-rate/FPR pair)
  - measured _GOLDEN_SHIP_FINDINGS re-baseline for the eight new fixtures
affects:
  - tests/test_known_bad_corpus.py
  - tests/test_causal_verb_golden.py
  - tests/test_frame_val.py
  - tests/test_dsx.py
tech-stack:
  added: []
  patterns:
    - "known-bad fixture cloned from the clean minimal-reference good-corpus template; only the analysis: block carries the encoded defect"
    - "inference.primary_procedure omitted for correlation/agreement fixtures so the frequentist admissibility ontology (no correlation family) draws no spurious DSX-ADM-020 / DSX-PRE-030"
    - "HIGH verify/ship stratum as a severity-tier x point-set DIMENSION on the single calibration classifier, read LIVE, never from the golden ledger (D-09)"
key-files:
  created:
    - examples/known-bad/correlation-pearson-ordinal-scale-ANALYSIS-SPEC.yaml (+POSTMORTEM +NARRATIVE)
    - examples/known-bad/correlation-for-agreement-estimand-ANALYSIS-SPEC.yaml (+POSTMORTEM +NARRATIVE)
    - examples/known-bad/icc-incomplete-triple-ANALYSIS-SPEC.yaml (+POSTMORTEM +NARRATIVE)
    - examples/known-bad/weighted-kappa-missing-weights-ANALYSIS-SPEC.yaml (+POSTMORTEM +NARRATIVE)
    - examples/known-bad/kappa-missing-companions-ANALYSIS-SPEC.yaml (+POSTMORTEM +NARRATIVE)
    - examples/good-corpus/valid-correlation-linear-ANALYSIS-SPEC.yaml (+NARRATIVE)
    - examples/good-corpus/valid-icc-reliability-ANALYSIS-SPEC.yaml (+NARRATIVE)
    - examples/good-corpus/valid-weighted-kappa-ANALYSIS-SPEC.yaml (+NARRATIVE)
  modified:
    - tests/test_known_bad_corpus.py
    - tests/test_causal_verb_golden.py
    - tests/test_frame_val.py
    - tests/test_dsx.py
decisions:
  - "primary_procedure omitted on correlation/agreement fixtures: the frequentist admissibility ontology has no correlation/agreement family, so it is the honest way to keep the ship set to exactly {DSX-STA-05x}"
  - "the five fixtures' HIGH own-codes live in a new _HIGH_TARGET_DEFECT_CODES map, read by _own_target_codes for ship-completeness recognition — not in _TARGET_DEFECT_CODES (CRITICAL-only) nor as non-empty _EXPECTED_CAUGHT_DEFECTS entries"
metrics:
  duration: ~50m
  completed: 2026-09-02
  tasks: 3
  commits: 3
  files_created: 24
  files_modified: 4
status: complete
---

# Phase 20 Plan A: Known-bad calibration re-baseline + live HIGH verify/ship stratum — Summary

Delivered REQ-P20-01: five dedicated PRESENT known-bad fixtures for the five Phase-18
codes that fire nowhere in `examples/` today, three valid good-corpus negative
controls that make the FPR a real negative control on those codes (denominator
12 -> 15), and the load-bearing extension of the single calibration harness with a
live HIGH verify/ship stratum reported as a third readout beside the (miss-rate, FPR)
pair. Zero finding codes minted; the only committed number that moved is
`_GOLDEN_SHIP_FINDINGS`.

## What shipped, per task

**Task 1 (commit 23e21e9)** — five PRESENT known-bad fixtures (SPEC + POSTMORTEM +
NARRATIVE each), one per Phase-18 code, each cloning the clean minimal-reference
good-corpus template and swapping only the `analysis:` block. Each declares only the
fields for its one code (mutually exclusive on `analysis.test`), omits
`analysis.outcome_type` (no DSX-STA-041 leak), and omits `inference.primary_procedure`.
Added the five MEASURED `_GOLDEN_SHIP_FINDINGS` keys, the five empty
`_EXPECTED_CAUGHT_DEFECTS` keys, the new `_HIGH_TARGET_DEFECT_CODES` declaration map,
and wired `_own_target_codes` to read it so each fixture's own HIGH code is recognised
by the ship-completeness guard.

**Task 2 (commit 849897a)** — three VALID good-corpus negative controls
(SPEC + NARRATIVE each), one per routing family, each reaching its DSX-STA-05x branch
and correctly staying silent (measured `frozenset()`). FPR denominator grows 12 -> 15.
Added the `test_fpr_noise_allowlist_is_disjoint_from_the_dsx_sta_family` guard so no
future editor can launder a real DSX-STA false positive as tempdir noise (D-05).

**Task 3 (commit d57e401)** — the live HIGH verify/ship stratum (D-03).
`_classify_target_defect` gained a trailing `severity` parameter defaulting to
`"CRITICAL"` (every existing call byte-for-byte unchanged); the stratified test now
reports the HIGH-tier PRESENT catch as a third readout computed LIVE via
`self._gate_findings` filtered to HIGH and `_classify_target_defect(..., severity="HIGH")`,
never lifted from the golden ledger (D-09). The anchor `_headline((2,5),(1,4),(3,10)) ==
(0.25,0.3)` and `_ABSENT_PARTITION_FLOOR == 3` are re-asserted unmoved, and the pair is
proven byte-identical before/after the stratum (D-06). Added
`test_high_stratum_target_codes_fire_and_are_named`.

## Measured golden sets (the re-baseline reality — re-verifiable)

Each measured live with the module's own fresh-tempdir `_ship_findings` idiom
(CRITICAL/HIGH set at `dsx gate ship`), never guessed:

| Fixture | Measured ship set |
|---------|-------------------|
| correlation-pearson-ordinal-scale | `{DSX-STA-050}` |
| correlation-for-agreement-estimand | `{DSX-STA-051}` |
| icc-incomplete-triple | `{DSX-STA-060}` |
| weighted-kappa-missing-weights | `{DSX-STA-061}` |
| kappa-missing-companions | `{DSX-STA-062}` |
| valid-correlation-linear | `frozenset()` |
| valid-icc-reliability | `frozenset()` |
| valid-weighted-kappa | `frozenset()` |

FPR denominator: `examples/good-corpus/*-ANALYSIS-SPEC.yaml` grew 12 -> 15; FPR stays
honest at 0/15 (the three new controls each measured `frozenset()`).

## Deviations from Plan

### Auto-fixed / design adjustments

**1. [Rule 3 — Blocking] `inference.primary_procedure` omitted on all eight new
correlation/agreement specs.**
- **Found during:** Task 1 (live measurement of the first fixture).
- **Issue:** The plan expected the ship set to be exactly `{DSX-STA-05x}`, but the
  frequentist admissibility ontology (`references/families.yaml`) carries NO
  correlation/agreement family. Declaring `primary_procedure: pearson_correlation`
  drew a spurious `DSX-ADM-020` (unresolved procedure), and leaving the cloned
  `primary_procedure: welch_t` drew `DSX-PRE-030` (executed `analysis.test` differs
  from declared branch).
- **Fix:** Omit `inference.primary_procedure` entirely. This makes admissibility
  resolve `not_declared` (clean) and the prereg branch `None` (DSX-PRE-030
  early-returns). The executed routing lives in `analysis.test`, which is what the
  DSX-STA-05x gate reads. Trusted the measurement over the plan's expectation, per the
  measurement-integrity rule; documented in every fixture's `inference:` comment.
- **Commits:** 23e21e9, 849897a.

**2. [Rule 3 — Blocking] `_HIGH_TARGET_DEFECT_CODES` created in Task 1, and
`_own_target_codes` extended to read it.**
- **Found during:** Task 1 (the ship-completeness invariant
  `test_ship_gate_findings_are_all_documented_incidental_corpus_gaps` runs in Task 1's
  verify).
- **Issue:** The new fixtures fire their HIGH code at ship. The ship-completeness guard
  requires every ship-blocking code to be either incidental or one of the fixture's
  own codes (`_own_target_codes`). With empty `_EXPECTED_CAUGHT_DEFECTS` and no
  `_TARGET_DEFECT_CODES` entry (both required by the plan), `_own_target_codes` would
  be empty and the HIGH code would read as an undocumented over-block.
- **Fix:** Front-loaded the plan's Task-3 `_HIGH_TARGET_DEFECT_CODES` map into Task 1
  and added a `high_map` source to `_own_target_codes`. This is the plan's own intent
  ("the HIGH catch lives in the new HIGH map"): the HIGH map is a declaration of
  intent (like `_TARGET_DEFECT_CODES`), never the measured ledger, so D-09 is
  preserved. Task 3 then consumes the existing map for the stratum.
- **Commit:** 23e21e9 (map + wiring); d57e401 (stratum consumer).

**3. [Rule 3 — Blocking] Two glob-based corpus-matrix tests updated for the new
fixtures.**
- **Found during:** final full-suite regression run after Task 3.
- **Issue:** `tests/test_frame_val.py::_EXPECTED_VAL_CODES` and
  `tests/test_dsx.py::test_every_committed_spec_declares_a_valid_estimand_type`
  discover the known-bad corpus by glob and each maintain a matrix/count that any
  fixture addition must update.
- **Fix:** Added the five new fixtures to `_EXPECTED_VAL_CODES`, each measured `set()`
  via `dsx.frame.val.check` (they clone the clean validity_frame); updated the
  committed-spec estimand-type count 14 -> 19. Neither file conflicts with any sibling
  plan's single-writer set (20-B: canonical specs / finding-codes.md / generator;
  Wave-1 C/D: their own test modules and `test-selection.md` / `stats.py`).
- **Commit:** d57e401.

**4. [commit granularity] Good-corpus controls committed in the Task-2 commit, not
mixed into Task 1.** The two golden sections live in one single-writer file
(`test_causal_verb_golden.py`) and `test_golden_keys_match_the_examples_tree_on_disk`
globs `examples/**`, so to keep each per-task commit self-consistent the good controls
were stashed out of the tree during the Task-1 commit and restored for Task 2.

## Invariants honoured (verified live)

- Each of the five known-bad fixtures fires EXACTLY its one DSX-STA-05x code (no
  DSX-STA-041 leak, no second Phase-18/19 code); clears plan/execute at exit 0; passes
  `dsx validate`; carries a POSTMORTEM naming its code and a NARRATIVE sibling. No
  `ATTRIBUTION.yaml` created (none is ABSENT — D-04/D-13-a).
- Headline stays the (miss-rate, FPR) pair; HIGH catch is a third readout beside it;
  `_headline((2,5),(1,4),(3,10)) == (0.25,0.3)` and `_ABSENT_PARTITION_FLOOR == 3`
  unmoved (D-06). The HIGH stratum reads LIVE, never the golden ledger (D-09 — the
  method source contains no `_GOLDEN_SHIP_FINDINGS` identifier).
- Classification keys on finding CODE identity only; no numeric-magnitude / effect-size
  band introduced (D-08).
- Zero `report.add` sites added; no edit to `dsx/`, `scripts/`, `references/`,
  `examples/good-ANALYSIS-SPEC.yaml`, or `examples/bad-ANALYSIS-SPEC.yaml`
  (`git diff --name-only` over those paths is empty). Catalogue stays 275.

## Verification results

- Task 1 verify: `python3 -m unittest tests.test_known_bad_corpus tests.test_causal_verb_golden` — OK; inline audit printed "five Phase-18 fixtures each fire exactly their target HIGH code".
- Task 2 verify: both modules OK; inline audit printed "three valid controls silent on the fifteen; denominator 15; noise-allowlist disjoint from DSX-STA".
- Task 3 verify: `tests.test_known_bad_corpus` OK; inline audit printed "severity param default CRITICAL; anchor+floor unmoved; HIGH stratum live, five fixtures, no golden self-reference".
- Full suite: `python3 -m unittest discover -s tests -q` — Ran 1457 tests, OK (1455 baseline + the two new calibration tests). Pre-existing DeprecationWarning in `tests/test_time_to_event_fallthrough.py` (a Wave-1 file, out of scope).

## Self-Check: PASSED

All eight new ANALYSIS-SPEC fixtures exist on disk; all three task commits
(23e21e9, 849897a, d57e401) exist in the branch history.
