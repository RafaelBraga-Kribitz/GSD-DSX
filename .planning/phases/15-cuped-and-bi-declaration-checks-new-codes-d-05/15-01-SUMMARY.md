---
phase: 15-cuped-and-bi-declaration-checks-new-codes-d-05
plan: 01
status: complete
requirements: [REQ-P15-01]
---

# 15-01 SUMMARY — CUPED vocabulary keystone (trap-12), no mint

## What shipped
- **`dsx/spec.py`** — added `cuped` to `VARIANCE_ADJUSTMENTS` (now five members: cluster_robust,
  delta_method, bootstrap_cluster, mixed_effects, cuped), so `design.variance_adjustment: cuped` no
  longer draws a stray DSX-SPEC-044 (MEDIUM). Added the closed two-member vocabulary
  `CUPED_COVARIATE_TIMINGS = {"pre_experiment", "post_treatment"}` and registered
  `("cuped_covariate_timings", CUPED_COVARIATE_TIMINGS)` in `_VOCABULARIES` so `dsx vocab` dumps it.
  Augmented the M-09 comment at `dependence.method_family_required` noting the shared set now includes
  `cuped` — NOT a defect to fork.
- **`tests/test_cuped_vocab.py`** (new) — 4 stdlib-only tests: cuped is a variance adjustment, the four
  legacy members round-trip (additive, exactly five), `dsx vocab` dumps cuped, and the timing vocabulary
  is exactly two-valued.

## Gate evidence (all re-run by the orchestrator, brief §5)
- Task-1 verify: `VARIANCE_ADJUSTMENTS`/`CUPED_COVARIATE_TIMINGS`/`describe_vocabulary()` assertions pass;
  `git status --porcelain -- references/finding-codes.md dsx/cli.py` empty (no mint, no gate-threshold edit).
- Task-2 verify: `python -m unittest tests.test_cuped_vocab` → 4 OK; required method names present.
- No finding code minted; catalogue untouched by this plan (regenerated once in 15-06). Wave 1, strictly
  before the 15-04 CUPED check that imports `CUPED_COVARIATE_TIMINGS` (trap #12).
