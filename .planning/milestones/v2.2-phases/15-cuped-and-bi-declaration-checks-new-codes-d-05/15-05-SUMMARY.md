---
phase: 15-cuped-and-bi-declaration-checks-new-codes-d-05
plan: 05
status: complete
requirements: [REQ-P15-03]
---

# 15-05 SUMMARY — good-fixture extension, silent at every threshold (D-08), no mint

## What shipped
- **`examples/good-ANALYSIS-SPEC.yaml`** — extended additively (no existing field changed): a
  `cohort_grain: user_cohort` label on `activation_rate`; a `design.variance_adjustment: cuped` with a
  `cuped:` block declaring `covariate_timing: pre_experiment`; a well-behaved `results.cohort_comparisons[]`
  entry (equal `sampling_rate` 0.5/0.5 AND `reweighted: true` — belt-and-suspenders silence for MET-021);
  and a monotone `results.funnel_steps[]` (18512 ≥ 5817 ≥ 3402, documentation only). Every new key is
  top-level under results/metrics/design — none inside `validity_frame`, so `frame_digest` is unchanged (D-04).
- **`tests/test_good_fixture_phase15.py`** (new) — 3 tests: the extended fixture passes every gate at every
  threshold (plan/execute/verify/ship, exit_code 0); DSX-MET-021 and DSX-EXP-070 stay silent on it at
  ship (trap #2); and the new keys sit outside validity_frame (D-04 placement invariant).

## Gate evidence (all re-run by the orchestrator, brief §5)
- Fixture round-trips through the loader; the D-04 placement assertions pass.
- `python -m unittest tests.test_good_fixture_phase15` → 3 OK (silence + exit_code 0 at all four gate points).
- `python -m unittest tests.test_causal_verb_golden` → 6 OK (the good-fixture-consuming golden suite stays
  green — the fixture was extended, not replaced, D-08). No mint; no gate module edited.
