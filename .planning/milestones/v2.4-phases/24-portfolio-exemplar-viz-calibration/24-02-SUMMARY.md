# 24-02 SUMMARY — First bad-CHART-choice fixtures + MEDIUM-stratum re-baseline (REQ-P24-02)

**Plan:** 24-02 (Wave 1) · **Requirement:** REQ-P24-02 · **Status:** DONE
**Gate:** `python -m unittest tests.test_known_bad_corpus` → **47 tests OK**; full suite **1507 OK / 47.5s** from a clean tree; zero mint (`gen-finding-catalogue.py --check` exit 0 @276).

## What was built (GA-2)

The FIRST bad-**chart**-choice fixtures in `examples/known-bad/`. Every earlier fixture encodes a bad
*analysis* choice; these four encode a bad *visual* choice on top of an otherwise clean, gate-passing
analysis. Each fixture is a **copy of a proven-clean `examples/good-corpus/*` control + exactly ONE bad
`visuals[]` entry** (the plan's recipe / Risks P4/P5), so it passes `dsx validate` and exits 0 at
`plan`+`execute`, and the only off-clean finding is the intended one.

**Fixture recipe measured, not estimated.** Before authoring, the base specs were run through the real
corpus harness (`_gate_findings`: fresh tempdir + `_seed_entrypoint` + `seed_plan_header`) to confirm they
produce zero findings; then each authored fixture was re-measured through the same harness. Recipe for the
three banned types: banned `type` → `DSX-VIZ-001` HIGH (the target); OMIT `relationship` (accept
`DSX-VIZ-010` MEDIUM, avoid `DSX-VIZ-012` HIGH); OMIT `data_input_type` (accept `DSX-VIZ-014` MEDIUM, avoid
`DSX-VIZ-013` HIGH); declare `units`/`takeaway`(magnitude)/`source` (avoid `DSX-VIZ-061/063/064`); OMIT
`artifact_path`/`svg_sha256` (avoid `DSX-FIG-001`).

**Task 1 — three banned-type HIGH fixtures** (each → the EXISTING `DSX-VIZ-001`, zero new code, D-06):
- `chart-gauge-single-kpi` (base `freq-count-installs`) — `type: gauge`
- `chart-word-cloud-text` (base `freq-count-referrals`) — `type: word_cloud`
- `chart-radar-multimetric` (base `freq-continuous-aov`) — `type: radar` (pre-existing banned-type control)

Measured through the harness: exit 0 at plan/execute; exit 1 at verify/ship with `DSX-VIZ-001` the sole
HIGH (incidental `DSX-VIZ-010`/`DSX-VIZ-014` MEDIUM only). Each POSTMORTEM names `DSX-VIZ-001` and explains
why the chart is substantively bad, citing the perception-doctrine source recorded in `viz.py` BANNED_TYPES
(Few 2006 §3.2/§6.2.1.1 gauge; Jacob Harris 2011 word cloud; Duan et al. 2023 radar).

**Task 2 — the MEDIUM `DSX-VIZ-071` fixture** `chart-uncertainty-mark-misuse` (base `freq-continuous-timeontask`):
`relationship: uncertainty`, `type: error_bars`, `uncertainty_mark: gradient_band` (NOT a member of
`RELATIONSHIP_CHARTS["uncertainty"]` — the trap: `confidence_band`/`graded_confidence_band` are real members,
`gradient_band` is not; HQ-27 D-2), `data_input_type: interval-range` (admits `error_bars` per spec.py:318 →
no `DSX-VIZ-013`), `shows_estimates`/`shows_uncertainty` true (→ no `DSX-VIZ-070`). Measured: exit 0 at the
default HIGH threshold (fires only `DSX-VIZ-071` MEDIUM); exit 1 under `--block-on MEDIUM` with `DSX-VIZ-071`
among the MEDIUM findings. NOT registered as a `kind: miss` ABSENT case; DSX-VIZ-071 severity unchanged
(Risk P1/T-24-02-03).

**Task 3 — the MEDIUM stratum (`tests/test_known_bad_corpus.py`).** Added `_MEDIUM_TARGET_DEFECT_CODES`;
threaded a `block_on` argument through `_gate_findings` (appends `--block-on <level>`; default `None` keeps
the CRITICAL/HIGH strata byte-for-byte unchanged); extended `test_stratified_catch_rate_and_fpr_report` with
a MEDIUM readout computed LIVE (`_gate_findings(..., block_on="MEDIUM")` + `_classify_target_defect(...,
severity="MEDIUM")`) reported **BESIDE** the headline, plus a headline-invariance re-assertion proving the
(miss-rate, FPR) pair is byte-identical before/after the MEDIUM stratum runs (T-24-02-02). The 3 banned
fixtures joined `_HIGH_TARGET_DEFECT_CODES` and are picked up live by the HIGH stratum and
`test_high_stratum_target_codes_fire_and_are_named`. All 4 keyed in `_EXPECTED_CAUGHT_DEFECTS` (empty
frozensets — their catches live in the HIGH/MEDIUM strata, not the CRITICAL partition).

## Deviation (recorded loudly) — three tree-wide registries beyond the plan's `files_modified`

The plan named only `tests/test_known_bad_corpus.py`, but three OTHER tests iterate **every committed spec**
and require a per-fixture entry for any new one. Each was updated with **measured** values (never guessed),
matching each registry's own decision-trail discipline:
- `tests/test_dsx.py::test_every_committed_spec_declares_a_valid_estimand_type` — hardcoded count pin
  bumped **19 → 23** (each fixture is a copy of a clean control that already declares a valid estimand.type).
- `tests/test_frame_val.py::_EXPECTED_VAL_CODES` — 4 entries, all `set()` (measured `dsx.frame.val.check()`
  = empty; the defect lives in `visuals:`, not `validity_frame`).
- `tests/test_causal_verb_golden.py::_GOLDEN_SHIP_FINDINGS` — 4 entries; measured CRITICAL/HIGH ship set =
  `{DSX-VIZ-001}` for the three banned, `frozenset()` for the uncertainty fixture (VIZ-071 is MEDIUM).

## Gate evidence (orchestrator-run, clean tree)

- `python -m unittest tests.test_known_bad_corpus` → **Ran 47 tests OK** (all strata + total-equality +
  incidental-gap + friction guards green, incl. the new MEDIUM stratum).
- `scripts/gen-finding-catalogue.py --check` → **exit 0 @ 276** — zero mint (D-06); no `dsx/` gate code
  touched (`git diff dsx/` empty).
- Full suite **1507 passed, 2344 subtests passed / 47.5s** from a clean tree (stray `DECISIONS.jsonl` swept
  per standing note). Top-level count unchanged (no new test *method*); the 4 fixtures add subtests.

## Files

New (8): `examples/known-bad/chart-{gauge-single-kpi,word-cloud-text,radar-multimetric,uncertainty-mark-misuse}-{ANALYSIS-SPEC.yaml,POSTMORTEM.md}`.
Modified (4): `tests/test_known_bad_corpus.py` (planned) + `tests/test_dsx.py`, `tests/test_frame_val.py`,
`tests/test_causal_verb_golden.py` (registry deviations above).

## Boundary

S4-3 is one checkbox spanning 3 plans / 2 waves; **24-01 and 24-02 (Wave 1) are now done, 24-03 (Wave 2,
verify-not-build, depends on both) remains → the S4-3 box stays UNCHECKED.** Next unit = S4-3 continue (24-03).
