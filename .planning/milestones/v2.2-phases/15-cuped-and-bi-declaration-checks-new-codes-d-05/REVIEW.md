# Phase 15 — Code Review (S4-4)

**Verdict: PASS — 1 auto-fix, 0 blocking, 1 non-blocking nit.**
Reviewer: orchestrator-direct (opus/high, brief §3), loud op-decision consistent with
S1-4/S2-4/S3-4 — the diff is a bounded gate-path + test + catalogue phase and every
gate was re-run here, never trusted from a subagent report (brief §5).

Scope reviewed: the 6 Phase-15 feature commits `a75fc9e..4704722`
(`6ccb155`,`e6c1ee8`,`0ffeb7f`,`2173030`,`47b5e41`,`4704722`) — 21 files,
+981/−32: 4 gate-path modules (`dsx/spec.py`, `dsx/checks/design.py`,
`dsx/checks/metrics.py`, `dsx/mathx.py`), the catalogue + generator, one fixture,
one template, 7 test modules.

## Auto-fix applied (1)

**AF-1 — cross-phase byte anchor went stale (REQ-P7-03 guard).**
`tests/test_frame_val.py::test_design_checks_py_content_is_unmodified_since_phase_start`
pins a CRLF-normalised SHA-256 of `dsx/checks/design.py`. Plan 15-04 legitimately
added `_check_cuped` (DSX-EXP-070) to that file but the 15-04 feature commit did not
update the anchor in the same commit — so the full suite (deferred from S4-3 to this
unit) failed `a4f296c2… != f18056a6…`. This is exactly the cross-phase staleness the
S3-4 auto-fix handled, and exactly what this guard exists to force into the open.

Faithful fix (the anchor's own documented escape hatch — used three times before:
S0-6a and twice in Phase 11.3): recomputed the hash **independently** (§5) to
`a4f296c2b7ca879a96248d0bcc736b571df8e462802b9332317b2bad6e80c271`, updated the
constant, and added a dated rationale comment. **REQ-P7-03's behavioural invariant is
untouched** — the three VAL/EXP disjointness tests all passed pre-fix; DSX-EXP-070 is
disjoint from DSX-EXP-021/DSX-VAL-020 and fires only on `variance_adjustment==cuped`,
so it cannot make the two units' codes co-fire. Test-only change, no `dsx/` touch.

## Non-blocking nit (1, left as-is)

**N1 — dangling comment fragment in `dsx/spec.py`.** The Phase-15 edit to the M-09
reuse comment (above `_VALIDITY_FRAME_CAUSAL_REQUIRED`) leaves the sentence "…NOT a
defect to 'fix' by forking the set. The" broken across a blank comment line before
"`estimand.type` row …". Purely cosmetic — comment only, no behaviour — so left
untouched rather than re-touch a gate-path file for prose. Recorded for a future
tidy-up if `spec.py` is edited for a real reason.

## Load-bearing checks (all re-run here, real commands — §5)

- **Full suite:** `sh scripts/check.sh` → **all checks passed, Ran 1292 tests OK**
  (1263 at S3-5 end → +29 for the 6 new Phase-15 test modules); catalogue current,
  capability conformant (14 skills), gate contract good/bad/missing, determinism
  identical.
- **Gate-path purity:** the Phase-15 additions to `design.py`/`metrics.py`/`mathx.py`/
  `spec.py` add **no** `pandas`/`scipy`/`numpy` import (diff-scoped grep = clean);
  `_check_cohort_denominator_shift` uses only the existing stdlib-backed spec helpers
  (`as_number`,`get`,`is_blank`,`items`,`normalize`,`section`).
- **Both mints, single clean declaration:** `DSX-EXP-070` (CRITICAL) and
  `DSX-MET-021` (HIGH) each appear exactly once in `references/finding-codes.md`;
  neither is in the pre-existing S0-2 double-declare warning set.
- **MET-020 / MET-021 disjoint (both directions):** MET-021 reads only
  `results.cohort_comparisons` (allocation/sampling-rate spread); MET-020 reads only
  `results.period_comparisons` (count magnitude). Constructed mix-shift fires MET-021
  and does **not** drag in MET-020; good fixture (reweighted:true, equal rates) is
  silent on MET-021.
- **Gate-path flip (behaviour, not just tests):** good fixture at `dsx gate plan` →
  **exit 0**; a post-treatment-covariate CUPED variant → **exit 1** with DSX-EXP-070
  (CRITICAL blocks at plan). Absent `covariate_timing` also fires; `pre_experiment` is
  silent. EXP-070/MET-021 are silent on the good fixture at plan **and** verify.
  (The good fixture exiting 1 at verify/ship is **pre-existing** — the same at commit
  `a75fc9e`, before Phase 15 — the example intentionally lacks the verify/ship
  attestations; Phase 15 adds no new firing to it.)
- **D-08 additive rebaseline:** invariant `test_finding_catalogue_invariant` 2 OK
  (count 260 + set-identity = Phase-12 snapshot ∪ {REP-060,REP-061,EXP-070,MET-021});
  `_SNAPSHOT_TOTAL` stays 256; `tests/fixtures/finding-codes-phase12.md` byte-unchanged.
  `_D05_ALLOWLIST_CODES` extended by **exact code** (not prefix) for both mints, with
  rationale; `--check` exit 0 @260.
- **D-05 bar honoured:** both shipping codes cite operator-confirmed HQ-8 sources
  (EXP-070 → Deng et al. 2013 WSDM; MET-021 → Crook et al. 2009 KDD §6). Survivorship
  code **not** minted (HQ-8 "does not transfer" → stays `brief.md` §6.5); REQ-P15-04
  ships PARTIAL, as recorded at S4-1.

## Files

`REVIEW.md`, `VERIFICATION.md` (this dir); fix in `tests/test_frame_val.py`.
