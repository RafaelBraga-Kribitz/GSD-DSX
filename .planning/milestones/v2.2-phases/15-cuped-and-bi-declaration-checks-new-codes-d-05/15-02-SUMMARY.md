---
phase: 15-cuped-and-bi-declaration-checks-new-codes-d-05
plan: 02
status: complete
requirements: [REQ-P15-04]
---

# 15-02 SUMMARY — DSX-MET-021 changing-denominator check (REQ-P15-04 PARTIAL, loud)

## What shipped
- **`dsx/checks/metrics.py`** — added `_check_cohort_denominator_shift(spec, report)`, dispatched
  unconditionally from `check()` immediately after `_check_denominator_drift`. Mints **DSX-MET-021**
  (HIGH) when a `results.cohort_comparisons[]` entry's bucket `sampling_rate` spread (or, as a fallback,
  `treatment_share` spread) exceeds the declared-or-0.10-default tolerance AND `reweighted is not True`.
  Reads **only** `results.cohort_comparisons`, never `results.period_comparisons`; imports no
  pandas/scipy/numpy; sums no per-unit data (declaration-only, D-01). Fixed plain-string message
  `metric pooled across buckets sampled at different rates with no reweighting declared`;
  `where="spec.results.cohort_comparisons"`. Docstring carries `Citation:` (Crook 2009 KDD Pitfall 4) +
  `Structural criterion:` lines.
- **`tests/test_cohort_denominator.py`** (new, `# D-05: DSX-MET-021`) — 7 stdlib-only tests: firing on
  rate spread and on the treatment_share fallback, silence under reweighted:true / equal rates /
  within-tolerance, the declared-tolerance pass/fail split, and the **MET-020/MET-021 disjointness in
  both directions** (trap #1), plus only-MET-021-reachable (no silent survivorship mint).

## Gate evidence (all re-run by the orchestrator, brief §5)
- `python -m unittest tests.test_cohort_denominator` → 7 OK.
- AST verify: exactly one `report.add` (`DSX-MET-021`, `HIGH`, fixed literal message); body references
  `cohort_comparisons`, not `period_comparisons` (docstring excluded by node identity); no
  pandas/scipy/numpy import; dispatch call present.
- Survivorship code NOT minted (brief.md §6.5, D-13 entry condition); REQ-P15-04 ships PARTIAL — the
  REQUIREMENTS.md reword is the orchestrator's S4-4 close-out. No tracking file touched. Catalogue left
  intentionally stale until 15-06.
