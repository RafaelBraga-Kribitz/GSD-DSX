---
phase: 28-evidence-case-magnitude-no-test-computed
plan: 02
subsystem: known-bad corpus + gate harness
tags: [corpus, miss, attribution, harness, D-28-06]
requires: [28-01]
provides:
  - examples/known-bad/magnitude-without-computed-effect-* (4 files)
  - _PER_FIXTURE_INCIDENTAL_CODES (point-scoped incidental map, D-28-06)
  - brief §6.5 item 8 (satisfied)
affects: [tests/test_known_bad_corpus.py, tests/test_frame_val.py, tests/test_causal_verb_golden.py, tests/test_dsx.py, tests/test_frame_interference.py, brief.md]
tech_stack:
  added: []
  patterns: [point-scoped-per-fixture-incidental, declaration-gated-miss-attribution]
key_files:
  created:
    - examples/known-bad/magnitude-without-computed-effect-ANALYSIS-SPEC.yaml
    - examples/known-bad/magnitude-without-computed-effect-entrypoint.py
    - examples/known-bad/magnitude-without-computed-effect-POSTMORTEM.md
    - examples/known-bad/magnitude-without-computed-effect-ATTRIBUTION.yaml
  modified:
    - tests/test_known_bad_corpus.py
    - tests/test_frame_val.py
    - tests/test_causal_verb_golden.py
    - tests/test_dsx.py
    - tests/test_frame_interference.py
    - brief.md
decisions:
  - Encoded DSX-COH-001 as a point-scoped per-fixture incidental (D-28-06 Option A), not global, not own-target.
  - Registered the descriptive/observational fixture in _NON_CAUSAL_KNOWN_BAD (Rule 3 blocking fix).
metrics:
  duration: ~35m
  completed: 2026-09-08
  tasks: 3
  files: 10
status: complete
requirements-completed: [REQ-P28-01, REQ-P28-03]
---

# Phase 28 Plan 02: Promote magnitude-without-computed-effect into the known-bad corpus — Summary

Promoted the measured LIVE-MISS spike into a permanent, self-testing known-bad corpus fixture
(`magnitude-without-computed-effect-*`), authored a falsifiable ATTRIBUTION sidecar naming the
declaration-gated `DSX-CLM-034` as the absent code, completed the three glob-discovered harness maps
plus the D-28-06 point-scoped `_PER_FIXTURE_INCIDENTAL_CODES` encoding of the swap-invariant
`DSX-COH-001` residual, moved the spec count 43→44, rewrote brief §6.5 item 8 as satisfied, and
re-synced the installer overlay. The fixture stays an honest MISS: it declares no claim-to-cited-test
pointer, so `DSX-CLM-034` fires nowhere and the golden ship set is `{DSX-COH-001}` only.

## What was built

**Task 1 — spike promotion.** Copied the spike spec + entrypoint under the corpus basename; changed
only `spec_id` → `magnitude-without-computed-effect` and `reproducibility.entrypoint`; stripped the
spike header and added a corpus header naming REQ-P28-01/02/03 and the frozen D-28-01 collision. The
`supported_by` token appears nowhere in the promoted spec (its absence is what keeps the fixture a
MISS). Body left byte-equal to the spike (evidence/narrative still point at the committed spike
NARRATIVE, so the measured incidental set is unchanged).

**Task 2 — POSTMORTEM + ATTRIBUTION.** POSTMORTEM reproduces the four-point measured gate table
verbatim and both swap-still-fires counterfactuals, names `DSX-COH-001` as the documented incidental
and `DSX-CLM-034` as the attributing code, and carries the required `DSX-<LETTERS>-<digits>` token.
ATTRIBUTION: `absent_code: DSX-CLM-034`, `promotes_backlog_item: "6.5-item-8-magnitude-without-computed-effect"`
(the frozen `_SECTION_65_ITEM_IDS` member at :853), `kind: miss`, `protocol_adherence: skipped`.

**Task 3 — harness + D-28-06 + brief + installer.**
- `_EXPECTED_CAUGHT_DEFECTS[magnitude-without-computed-effect] = frozenset()` (a MISS catches nothing).
- `_EXPECTED_VAL_CODES[...] = set()` (measured live: val check fires nothing).
- `_GOLDEN_SHIP_FINDINGS[...] = frozenset({"DSX-COH-001"})` (measured live; DSX-CLM-034 absent).
- **D-28-06 encoding (a)-(i):** new `_PER_FIXTURE_INCIDENTAL_CODES` map keyed
  `magnitude-without-computed-effect -> {plan/verify/ship: frozenset({DSX-COH-001})}`; new
  `_per_fixture_incidental_codes(slug)` flatten helper; `_classify_target_defect` gained a defaulted
  `incidental: frozenset[str] = frozenset()` param loosening only the no-expected branch (empty ⇒
  byte-identical to prior behaviour); the :1149 call passes the point-scoped incidental; the ship
  `allowed` set unions the flattened per-fixture incidental. Guards: self-target disjointness,
  justification-binding (every per-fixture incidental must be some OTHER slug's declared target),
  live non-inertness (DSX-COH-001 fires CRITICAL at ship), the DSX-CLM-034-stays-out severity trap,
  and synthetic controls of both the classifier and the two static guards.
- Spec count 43→44 (`tests/test_dsx.py`) with the running-tally comment.
- brief §6.5 item 8 rewritten as satisfied (LIVE MISS; DSX-CLM-034 minted under D-05).
- Installer overlay re-synced (`node install.mjs` + `--check` both exit 0).

DSX-COH-001 was deliberately kept OUT of the global `_INCIDENTAL_GAP_CODES` (it is
prescriptive-churn-recommendation's own target — globalising it would fail
`test_incidental_allowlist_names_no_slugs_own_target_code`) and out of any own-target map (that would
credit the MISS with a catch). DSX-CLM-034 was kept OUT of `_SECTION_65_BACKLOG_CODES` (it shipped to
the catalogue in Wave 1; the disjointness assertion forbids it there) and out of
`_PER_FIXTURE_INCIDENTAL_CODES`/own-target (so the ship-completeness test stays its live falsifier if
it ever ships HIGH on the fixture).

## Measured golden ship set (re-measured live, never guessed)

Live gate on the promoted fixture (real CPython 3.12.10, fresh tempdir per point, entrypoint + plan
header seeded exactly as the harness does) — matches 28-MEASUREMENT.md exactly:

| Gate point | Exit | CRITICAL | HIGH |
|---|---|---|---|
| `dsx validate`   | 0 | — | — |
| `dsx gate plan`    | 1 | DSX-COH-001 | — |
| `dsx gate execute` | 0 | — | — |
| `dsx gate verify`  | 1 | DSX-COH-001 | — |
| `dsx gate ship`    | 1 | DSX-COH-001 | — |

**Golden ship CRITICAL/HIGH set = `{DSX-COH-001}`. DSX-CLM-034 ABSENT.** The fixture is a MISS, as the
frozen design requires.

## Gate evidence (real interpreter)

- `python312 -m dsx.cli validate --spec examples/known-bad/magnitude-without-computed-effect-ANALYSIS-SPEC.yaml`
  → `spec: PASS ... CRITICAL=0 HIGH=0 ...` exit 0.
- `python312 -m unittest tests.test_known_bad_corpus tests.test_frame_val tests.test_causal_verb_golden tests.test_dsx -q`
  → `Ran 710 tests ... OK` exit 0.
- `python312 -m unittest discover -s tests -q` → `Ran 1615 tests ... OK` exit 0 (Wave 1 left 1606; this
  plan added 9 net — the D-28-06 guard/synthetic-control tests).
- `python312 scripts/gen-finding-catalogue.py --check` → `finding catalogue is current` exit 0
  (Total: 278, unchanged; this plan mints no code).
- `node install.mjs` → `Installed.` exit 0; `node install.mjs --check` → `self-test: passed` exit 0.
- `git status --porcelain .planning/REQUIREMENTS.md .planning/STATE.md .planning/ROADMAP.md` → prints
  nothing (single-writer files untouched).
- `git diff --stat -- dsx/checks/dq.py` → empty (byte-freeze held); no `dsx/` source edited at all.

## Deviations from Plan

**1. [Rule 3 — Blocking] Registered the fixture in `_NON_CAUSAL_KNOWN_BAD` (tests/test_frame_interference.py).**
- **Found during:** Task 3 full-suite run.
- **Issue:** `test_needs_causal_block_true_for_known_bad_and_canonical_fixtures` sweeps every known-bad
  fixture and asserts `needs_causal_block True`, excluding deliberately descriptive/observational
  fixtures by slug. Our fixture is descriptive/observational (FROZEN D-28-01), so it returned False.
- **Fix:** Added `magnitude-without-computed-effect-ANALYSIS-SPEC.yaml` to `_NON_CAUSAL_KNOWN_BAD` with
  an explanatory comment, exactly as `prescriptive-churn-recommendation` and
  `operator-known-answer-selective-exclusion` already are. Within the allowed `tests/` edit surface;
  a direct consequence of the frozen fixture shape, not a design change.
- **Files modified:** tests/test_frame_interference.py.

No other deviations. The frozen design (D-28-00..06), `dsx/` source, and the single-writer tracking
files were untouched.

## Known Stubs

None. The fixture is a deliberate, documented MISS (attribution, not detection) per the frozen
D-28-01 design; this is not a stub but the phase's whole point, and it is asserted behaviourally by
the golden-set, falsifiability, and D-28-06 guard tests.

## Self-Check: PASSED

- Created files exist: all four `examples/known-bad/magnitude-without-computed-effect-*` present.
- Golden ship set re-measured live = `{DSX-COH-001}`, DSX-CLM-034 absent (matches 28-MEASUREMENT.md).
- Full suite OK (1615 tests); catalogue --check exit 0 (Total 278); installer --check exit 0.
- Single-writer files untouched; dq.py byte-frozen; no git write commands were run.
