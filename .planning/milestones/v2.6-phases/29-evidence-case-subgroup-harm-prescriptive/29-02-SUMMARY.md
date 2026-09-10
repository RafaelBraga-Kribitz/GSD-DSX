---
phase: 29-evidence-case-subgroup-harm-prescriptive
plan: 02
subsystem: known-bad corpus / coherence-discipline harness
tags: [corpus-fixture, target, DSX-COH-041, subgroup-harm, prescriptive, kind-target]
requires:
  - "Plan 29-01: DSX-COH-041 minted (catalogue 279), _check_subgroup_harm_disposition, decision-schema keys, four count pins"
  - "29-MEASUREMENT.md: VERDICT LIVE MISS (D-13 entry condition)"
provides:
  - "examples/known-bad/subgroup-harm-without-disposition-* (4 files) — the corpus's first kind: target fixture"
  - "harness TARGET wiring for DSX-COH-041 at plan/verify/ship"
  - "kind: target taught to the ATTRIBUTION sidecar vocabulary + falsifiability parser"
affects:
  - "spec count 44 -> 45; golden ship set; val-code map; brief §6.5 item 9 (PROMOTED — DETECTED)"
tech-stack:
  added: []
  patterns: ["point-scoped _TARGET_DEFECT_CODES bare-string shape (chart-truncated-axis-bar / prescriptive-churn-recommendation precedent)", "kind: target sidecar (D-29-00 inverse of Phase 27/28 kind: miss)"]
key-files:
  created:
    - examples/known-bad/subgroup-harm-without-disposition-ANALYSIS-SPEC.yaml
    - examples/known-bad/subgroup-harm-without-disposition-entrypoint.py
    - examples/known-bad/subgroup-harm-without-disposition-POSTMORTEM.md
    - examples/known-bad/subgroup-harm-without-disposition-ATTRIBUTION.yaml
  modified:
    - tests/test_known_bad_corpus.py
    - tests/test_frame_val.py
    - tests/test_causal_verb_golden.py
    - tests/test_dsx.py
    - brief.md
decisions:
  - "Followed the plan's recorded_authoring_choices: DSX-COH-041 lives point-scoped in _TARGET_DEFECT_CODES (plan/verify/ship); _EXPECTED_CAUGHT_DEFECTS[slug] = frozenset() (key-parity only) — the CONTEXT D-29-00 line's frozenset({DSX-COH-041}) cannot hold because coherence is absent from execute."
  - "Golden ship set re-measured live = frozenset({DSX-COH-041}); DSX-STA-011 MEDIUM is a swap-invariant incidental below the CRITICAL/HIGH stratum, so no _PER_FIXTURE_INCIDENTAL_CODES entry was added."
metrics:
  completed: 2026-09-08
status: complete
---

# Phase 29 Plan 02: Subgroup-harm TARGET fixture promotion Summary

Promoted the S5-3 measurement spike into the committed known-bad corpus as the corpus's
first `kind: target` fixture: on the confirmed LIVE MISS branch, DSX-COH-041 (minted in
wave 1) now catches the honestly-declared, undispositioned opposing minority segment
CRITICAL at plan/verify/ship — the load-bearing INVERSE of the Phase-27/28
attribution-only misses.

## Pre-flight

29-MEASUREMENT.md first content line confirmed `VERDICT: LIVE MISS` — this plan runs
(Branch B). Interpreter used for the full suite and every gate:
`C:/Users/Benutzer1/AppData/Local/Programs/Python/Python312/python.exe` (CPython 3.12.10).

## Files created / modified

Created (untracked, under `examples/known-bad/`):
- `subgroup-harm-without-disposition-ANALYSIS-SPEC.yaml` — promoted from the 29-01 spike; spike banner stripped and replaced with a corpus header naming REQ-P29-01/02/03, the FROZEN D-29-02 defect, the post-mint CAUGHT polarity, and the Gail & Simon / Obermeyer sources at their honest grade. `spec_id` and `reproducibility.entrypoint` already at the corpus basename; every other block byte-equal to the spike (no `decision.subgroup_harm[]` row; segment D unchanged at −6.0pp / n=1000).
- `subgroup-harm-without-disposition-entrypoint.py` — promoted; head comment retitled from "spike" to "fixture" (basename only); body is the byte-equal static no-op read by the code scan, never executed.
- `subgroup-harm-without-disposition-POSTMORTEM.md` — authored new; reproduces the pre-mint LIVE MISS table (all exit 0) and the post-mint CAUGHT table (measured), records MET-030/031 silent at 1-of-4, records the swap-still-fires counterfactual, names DSX-COH-041 as the catch, states the bounded-catch limit and the D-29-05 source honesty.
- `subgroup-harm-without-disposition-ATTRIBUTION.yaml` — authored new; the corpus's first `kind: target` sidecar: `absent_code: DSX-COH-041`, `promotes_backlog_item: "6.5-item-9-subgroup-harm-declaration"`, `protocol_adherence: skipped`, rationale.

Modified (tracked):
- `tests/test_known_bad_corpus.py` — added `_TARGET_DEFECT_CODES["subgroup-harm-without-disposition"] = {"plan"/"verify"/"ship": "DSX-COH-041"}` and `_EXPECTED_CAUGHT_DEFECTS["subgroup-harm-without-disposition"] = frozenset()`; extended the closed-vocabulary assertion to `("miss", "caught", "target")` with an updated message; updated the falsifiability docstring + non-miss branch comment to name `target`. `_ABSENT_PARTITION_FLOOR` (3), `_SECTION_65_BACKLOG_CODES`, and the `!= "miss"` guard left unedited.
- `tests/test_frame_val.py` — added `_EXPECTED_VAL_CODES["subgroup-harm-without-disposition-ANALYSIS-SPEC.yaml"] = set()` (measured empty via val.check).
- `tests/test_causal_verb_golden.py` — added `_GOLDEN_SHIP_FINDINGS[".../subgroup-harm-without-disposition-ANALYSIS-SPEC.yaml"] = frozenset({"DSX-COH-041"})` (measured live).
- `tests/test_dsx.py` — spec count `44 -> 45` (with a comment row for the new fixture).
- `brief.md` — §6.5 item 9 table row rewritten to "Satisfied (Phase 29)" with the measured evidence (LIVE MISS pre-mint; DSX-COH-041 minted to CATCH; Obermeyer + Gail & Simon at honest grade); the item-9 disposition bullet updated from "carried" to "promoted"; the calibration line "items 1/3/7/9" corrected to "items 1/3/7" (item 9 is now a PRESENT/DETECTED target, not an ABSENT miss).

## Measured `_GOLDEN_SHIP_FINDINGS` value (verbatim)

`frozenset({"DSX-COH-041"})` — re-measured live at `dsx gate ship` against a fresh
`tempfile.TemporaryDirectory()`. DSX-COH-041 IS present (fires CRITICAL at ship). The
only other ship finding, DSX-STA-011 (MEDIUM, aggregate effect-size advisory,
swap-invariant), sits below the CRITICAL/HIGH stratum this set records; DSX-PAR-001 is
INFO. No undocumented incidental — no STOP condition; the fixture is a catch, consistent
with the frozen D-29-00 design.

### Full post-mint gate measurement (fresh tempdir per point, CPython 3.12.10)

| Gate point | Exit | CRITICAL/HIGH |
|---|---|---|
| validate | 0 | — |
| plan | 1 | DSX-COH-041 |
| execute | 0 | — |
| verify | 1 | DSX-COH-041 |
| ship | 1 | DSX-COH-041 |

Swap-still-fires (segment D flipped to +0.06): all points exit 0, DSX-COH-041 gone
everywhere (the real catch toggles off); DSX-STA-011 MEDIUM persists at verify/ship
(swap-invariant, non-blocking). Confirms DSX-COH-041 is this fixture's catch, not an
artefact.

## Gate results (raw)

- Full suite: `python312 -m unittest discover -s tests -q` -> `Ran 1622 tests` -> `OK` (exit 0).
- Targeted modules: `python312 -m unittest tests.test_known_bad_corpus tests.test_frame_val tests.test_causal_verb_golden tests.test_dsx -q` -> `Ran 710 tests` -> `OK` (exit 0).
- `python312 scripts/gen-finding-catalogue.py --check` -> `finding catalogue is current` (exit 0; catalogue at 279 from wave 1, untouched). Pre-existing benign "declared twice" warnings (DSX-CLM-020/021, DSX-COH-030/041, DSX-ML-034, DSX-PAR-002, DSX-SPEC-070, DSX-VAL-021/060) present in baseline; non-fatal.
- `python312 -m dsx.cli validate --spec examples/known-bad/subgroup-harm-without-disposition-ANALYSIS-SPEC.yaml` -> `spec: PASS ... CRITICAL=0 HIGH=0 MEDIUM=0 LOW=0 INFO=0` (exit 0).
- `node install.mjs` -> `capability installed` / `self-test passed` (exit 0); `node install.mjs --check` -> `self-test: passed` (exit 0). Overlay re-synced — all four fixture files confirmed present under `C:/Users/Benutzer1/.gsd/capabilities/dsx/examples/known-bad/`.

## Byte-freeze + single-writer confirmation

- `git diff --stat -- dsx/checks/dq.py` -> empty (byte-frozen).
- `git status --porcelain` over `.planning/REQUIREMENTS.md .planning/STATE.md .planning/ROADMAP.md references/finding-codes.md scripts/gen-finding-catalogue.py tests/test_finding_catalogue_invariant.py tests/test_phase20_zero_mint_close.py tests/test_p19_categorical_rows.py` -> empty (wave-1 + single-writer files untouched).
- `git status --porcelain dsx/` -> empty (no source edits).
- Full working-tree change set: `M brief.md`, `M tests/test_causal_verb_golden.py`, `M tests/test_dsx.py`, `M tests/test_frame_val.py`, `M tests/test_known_bad_corpus.py`, plus the four new untracked `examples/known-bad/subgroup-harm-without-disposition-*` files — exactly the plan's `files_modified` + `artifacts`.

## Deviations from Plan

None affecting the frozen design or scope. Two disclosures:

1. **[Plan-consistency, not a design change] Extra brief.md edits beyond the single §6.5 table row.** The plan's Task 3 names "the brief.md §6.5 item 9 row". I additionally updated (a) the item-9 disposition bullet further down (was "carried … neither is in the measured corpus", now stale/contradictory) and (b) the calibration line "items 1/3/7/9" -> "items 1/3/7". Reason: leaving those two would have left the brief internally contradicting its own §6.5 row (project working agreement: no un-corrected contradictions). No numbers in the calibration headline were changed; item 9 correctly moves out of the ABSENT-miss list because it is now a PRESENT/DETECTED target.

2. **[Interpreter substitution, per orchestrator instruction] Ran every gate on the full Python 3.12.10 path**, not the literal `python312` shorthand in the plan (which is not a command on this machine). `node install.mjs --check` self-reports `python3 (Python 3.14.6)` for its own env probe, but its self-test passed regardless — that probe is the installer's, not the gate interpreter.

## Write-only / no-git

Per the orchestrator's hard constraints, NO git command was run beyond read-only
`git status` / `git diff --stat` for verification. Nothing staged or committed; no
STATE.md / ROADMAP.md / REQUIREMENTS.md edits (single-writer — orchestrator owns them).
Every change is left in the working tree for the orchestrator to re-verify and commit.

## Self-Check: PASSED

- Created files exist: all four `examples/known-bad/subgroup-harm-without-disposition-*` confirmed on disk (git sees them as `??`).
- Golden set re-measured live, not guessed; DSX-COH-041 present.
- dq.py + wave-1 catalogue files + single-writer tracking files: diff/porcelain empty.
