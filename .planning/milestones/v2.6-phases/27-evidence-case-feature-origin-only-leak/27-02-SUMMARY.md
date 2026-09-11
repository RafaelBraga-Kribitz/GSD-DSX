---
phase: 27-evidence-case-feature-origin-only-leak
plan: 02
subsystem: dsx known-bad corpus + harness wiring
tags: [corpus-fixture, feature-provenance, DSX-ML-034, miss-attribution, harness]
requires: [27-01]
provides:
  - examples/known-bad/feature-origin-only-leak-* (4 files)
  - feature-origin-only-leak keyed in _EXPECTED_CAUGHT_DEFECTS / _EXPECTED_VAL_CODES / _GOLDEN_SHIP_FINDINGS
  - spec count pin 43
affects: [brief.md §6.5 item 7]
tech-stack:
  added: []
  patterns: [glob-discovered corpus harness maps, declaration-only miss attribution]
key-files:
  created:
    - examples/known-bad/feature-origin-only-leak-ANALYSIS-SPEC.yaml
    - examples/known-bad/feature-origin-only-leak-entrypoint.py
    - examples/known-bad/feature-origin-only-leak-POSTMORTEM.md
    - examples/known-bad/feature-origin-only-leak-ATTRIBUTION.yaml
  modified:
    - tests/test_known_bad_corpus.py
    - tests/test_frame_val.py
    - tests/test_causal_verb_golden.py
    - tests/test_dsx.py
    - brief.md
decisions:
  - "Golden ship set MEASURED, not assumed: live gate re-run on the promoted fixture yields exactly {DSX-CLM-031, DSX-COH-031, DSX-MET-040, DSX-NAR-001}; DSX-ML-034 absent — the frozen MISS holds."
  - "DSX-ML-034 kept OUT of _SECTION_65_BACKLOG_CODES (shipped in Wave 1; disjointness assertion forbids it); promotes_backlog_item uses the harness-frozen id 6.5-item-7-feature-provenance."
  - "The promoted ANALYSIS-SPEC declares NO feature_provenance block and never names that token — its absence keeps DSX-ML-034 silent (attribution, not detection)."
metrics:
  duration: ~20m
  completed: 2026-09-07
status: complete
requirements-completed: [REQ-P27-01, REQ-P27-03]
---

# Phase 27 Plan 02: Feature-origin-only-leak corpus promotion Summary

Promoted the measured LIVE-MISS spike into a committed known-bad corpus fixture
(`feature-origin-only-leak`), authored its POSTMORTEM and a falsifiable ATTRIBUTION
sidecar naming DSX-ML-034 as the absent attributing code, wired the fixture into the
four glob-discovered harness maps + the spec-count pin, and rewrote brief §6.5 item 7
with the measured evidence — all without re-opening the frozen D-27-01/02 contract and
with `dsx/checks/dq.py` byte-frozen.

## Tasks

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Promote spike spec + entrypoint | d6cf0af | feature-origin-only-leak-ANALYSIS-SPEC.yaml, -entrypoint.py |
| 2 | Author POSTMORTEM + ATTRIBUTION sidecar | 2ae0a33 | feature-origin-only-leak-POSTMORTEM.md, -ATTRIBUTION.yaml |
| 3 | Wire 4 harness maps + spec count + brief + installer re-sync | 0f6a808 | tests/test_known_bad_corpus.py, tests/test_frame_val.py, tests/test_causal_verb_golden.py, tests/test_dsx.py, brief.md |

## What was built

- **Fixture (MISS):** the spike spec/entrypoint promoted under the corpus basename;
  `spec_id` → `feature-origin-only-leak`, `reproducibility.entrypoint` →
  `feature-origin-only-leak-entrypoint.py`, spike header replaced by a corpus header
  naming REQ-P27-01/02/03. No `feature_provenance` block, and the token appears nowhere
  in the spec. `dsx validate` exits 0.
- **POSTMORTEM:** records the four-point measured gate table verbatim (validate/plan/
  execute clean; verify/ship exit 1 on the four swap-invariant residuals), states it as
  the D-27-02 entry-condition test, records the swap-still-fires counterfactual, and
  names DSX-ML-034 as the attributing code.
- **ATTRIBUTION sidecar:** `absent_code: DSX-ML-034` (a shipped code — the first
  shipped-code miss sidecar), `promotes_backlog_item: 6.5-item-7-feature-provenance`,
  `kind: miss`, `protocol_adherence: skipped`.
- **Harness wiring:** `_EXPECTED_CAUGHT_DEFECTS["feature-origin-only-leak"] =
  frozenset()`; `_EXPECTED_VAL_CODES["…-ANALYSIS-SPEC.yaml"] = set()`;
  `_GOLDEN_SHIP_FINDINGS["…-ANALYSIS-SPEC.yaml"] = {DSX-CLM-031, DSX-COH-031,
  DSX-MET-040, DSX-NAR-001}` (live-measured); spec count 42 → 43.
- **brief §6.5 item 7:** rewritten to state the measured LIVE MISS and DSX-ML-034 mint.
- **Installer overlay** re-synced (`node install.mjs` then `--check`, self-test passed).

## Verification (all green)

- `dsx validate` on the promoted spec — exit 0.
- Targeted: `test_known_bad_corpus + test_frame_val + test_causal_verb_golden +
  test_dsx` — 701 tests OK.
- Full suite `python -m unittest discover -s tests -q` — 1596 tests OK.
- `scripts/gen-finding-catalogue.py --check` — exit 0 ("finding catalogue is current").
- `node install.mjs --check` — exit 0 (self-test passed).
- `git diff --stat -- dsx/checks/dq.py` — empty (byte-frozen).
- Direct golden re-measure: ship set `{DSX-CLM-031, DSX-COH-031, DSX-MET-040,
  DSX-NAR-001}`; DSX-ML-034 absent — frozen MISS reproduced.

## Deviations from Plan

None. The plan executed exactly as written. Notes:
- The plan's automated verify commands write `python312`; on this machine that is not a
  command — the real interpreter
  `C:/Users/Benutzer1/AppData/Local/Programs/Python/Python312/python.exe` (CPython
  3.12.10) was used for every run (environment grounding, not a plan deviation).
- The full-suite run and the catalogue `--check` emit benign
  `warning: DSX-ML-034 declared twice with different text` (and the same for other
  two-severity codes) on stderr — the two-severity emit from the Wave-1 check
  (27-RESEARCH §RISK 3). `--check` does not fail on it and no test asserts zero
  warnings; the committed catalogue is current.

## Branch / push state

Branch: `gsd/v2.6.0-exploration-depth` (no stray-branch switch occurred at any commit
step; plain `git commit` used throughout). Three commits ahead of origin, unpushed
(no push performed — orchestrator owns STATE/ROADMAP/REQUIREMENTS and the wave merge).

## Self-Check: PASSED
- Files created: all 4 `examples/known-bad/feature-origin-only-leak-*` FOUND.
- Commits: d6cf0af, 2ae0a33, 0f6a808 all present in `git log`.
