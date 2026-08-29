# Phase 15 — Verification (S4-4)

**Verdict: PASSED — 7/7 requirements (REQ-P15-01 … REQ-P15-07), goal-backward.**
Orchestrator-direct (opus/high, §3); each requirement mapped to a re-run gate or a
read locator, never trusted from a summary (§5). REQ-P15-04 ships **PARTIAL** as
recorded and consented at S4-1 (survivorship half unshipped per answered HQ-8).

Headline gate: `sh scripts/check.sh` → **all checks passed, Ran 1292 tests OK**.

| REQ | What it demands | Evidence (re-run here) | Verdict |
|---|---|---|---|
| P15-01 | `cuped` is a legal vocabulary member; covariate-timing vocab exists | `cuped` ∈ `VARIANCE_ADJUSTMENTS` (`spec.py:264`); `CUPED_COVARIATE_TIMINGS={pre_experiment,post_treatment}` registered in `_VOCABULARIES`; `test_cuped_vocab` green (in the 76-OK focused run). No mint in 15-01. | COVERED |
| P15-02 | A post-treatment CUPED covariate blocks at `dsx gate plan` | **Gate-path flip proven:** post-treatment spec → `dsx gate plan` exit **1**, DSX-EXP-070 (CRITICAL); good (pre_experiment) → exit 0. Absent timing also fires. `test_cuped` green. Cites Deng et al. 2013 WSDM (HQ-8-confirmed). | COVERED |
| P15-03 | BI declaration checks exercised via extended good fixture; silent everywhere | Good fixture extended (cohort_grain, cuped block, cohort_comparisons reweighted:true, monotone funnel_steps); EXP-070/MET-021 silent at plan+verify; `test_good_fixture_phase15` green. | COVERED |
| P15-04 | Changing-denominator defect blocks its own bad fixture (survivorship = PARTIAL) | DSX-MET-021 (HIGH) fires on declared bucket mix-shift w/o reweighting; disjoint from MET-020 both directions; `test_cohort_denominator` green. Survivorship **not** minted (HQ-8 does-not-transfer, `brief.md` §6.5). Cites Crook et al. 2009 KDD §6. | COVERED (PARTIAL, consented) |
| P15-05 | APA research-table template shipped | `templates/APA-TABLE-research.md` present; `test_apa_template` green. No mint. | COVERED |
| P15-06 | No Shapiro auto-switch on the decision surface | `test_no_shapiro_autoswitch` green — grep of `dsx/`+`skills/` decision surface = 0 normality-test auto-switch calls. No mint. | COVERED |
| P15-07 | Catalogue extends additively; both canonical fixtures satisfy D-08 | `test_finding_catalogue_invariant` 2 OK (count 260 + set-identity vs snapshot∪{REP-060,REP-061,EXP-070,MET-021}); `_SNAPSHOT_TOTAL`=256, frozen anchor byte-unchanged; `gen-finding-catalogue.py --check` exit 0. | COVERED |

## Automated coverage note

REQ-P15-01..07 are covered by the 6 new Phase-15 test modules
(`test_cuped_vocab`, `test_cuped`, `test_cohort_denominator`, `test_apa_template`,
`test_no_shapiro_autoswitch`, `test_good_fixture_phase15`) plus the rebaselined
`test_finding_catalogue_invariant` — all green in the full suite. A standing
Phase-15 structural test (analogous to `test_phase13/14/16_*`) can be crystallised at
S4-5 alongside secure+validate if that unit judges it adds coverage; the underlying
behaviours are already automated here.

## HUMAN-QUEUE

- **D-05 (citation authenticity):** owed reads already answered at HQ-8 (CUPED
  confirmed; changing-denominator confirmed; survivorship does-not-transfer → unshipped).
  No new D-05 read owed by S4-4.
- **D-06 (numbering veto):** HQ-13 filed at S4-1; finalised this unit to the exact
  shipped catalogue text (`DSX-MET-021` shipped lower-case "metric pooled…"). Non-blocking.
- Phase-15 end-of-phase security sign-off + UAT is filed at S4-5 (secure+validate),
  per the S1-5/S2-5/S3-5 pattern.
