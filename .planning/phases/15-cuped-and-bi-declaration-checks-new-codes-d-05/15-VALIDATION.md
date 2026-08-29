---
phase: 15
slug: cuped-and-bi-declaration-checks-new-codes-d-05
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-08-29
validated: 2026-08-29
---

# Phase 15 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> **State B run** (no prior VALIDATION.md): reconstructed from the six plans + SUMMARY files.
> Phase 15 is a **code phase** — unlike Phases 13/14/16 (doc/skill phases whose requirements
> needed crystallising from S-hand-reads), every requirement here already shipped a dedicated
> behavioural test at execution time (S4-3): `test_cuped_vocab` (REQ-P15-01), `test_cuped`
> (REQ-P15-02), `test_good_fixture_phase15` (REQ-P15-03), `test_cohort_denominator`
> (REQ-P15-04), `test_apa_template` (REQ-P15-05), `test_no_shapiro_autoswitch` (REQ-P15-06),
> and the rebaselined `test_finding_catalogue_invariant` (REQ-P15-07). This firing added one
> phase-scoped **coverage anchor** (`tests/test_phase15_bi_checks.py`, 20 tests) — the way S3-5
> did with `tests/test_phase16_reproduce.py` even though behavioural tests already existed — so
> a silent regression (a deleted guard, a downgraded severity, a stripped citation, a dropped
> vocabulary member, a data library pulled onto the declaration gate) names itself against a
> single requirement→behaviour map. Gap analysis: **0 gaps** → no `gsd-nyquist-auditor`
> spawned. REQ-P15-04 is **COVERED (PARTIAL)** as recorded and consented at S4-1 (survivorship
> half unshipped per answered HQ-8; the changing-denominator half fully shipped + tested).
> Every command below was re-run by the orchestrator this firing (brief §5).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python stdlib `unittest` (no pytest / no third-party test framework in the repo) |
| **Config file** | none — `python -m unittest discover -s tests -q` (see `scripts/check.sh`) |
| **Quick run command** | `python -m unittest tests.test_phase15_bi_checks tests.test_cuped tests.test_cohort_denominator tests.test_cuped_vocab tests.test_good_fixture_phase15 tests.test_apa_template tests.test_no_shapiro_autoswitch tests.test_finding_catalogue_invariant -v` |
| **Full suite command** | `python -m unittest discover -s tests -q` (1312 tests as of 2026-08-29) |
| **Phase gate** | `sh scripts/check.sh` (full suite + `gen-finding-catalogue.py --check` + capability manifest + gate-contract good/bad/missing exit codes + determinism) |
| **Estimated runtime** | ~35 seconds (full suite: `Ran 1312 tests in ~35s`) |

**Clean-tree note:** run the full suite from a tree with no gitignored `DECISIONS.jsonl` at the
repo root (a fresh checkout, or `scripts/check.sh`, which runs the suite before its own gate
steps regenerate the ledger). Two pre-existing `explain` tests do not isolate the repo-root CWD
and false-fail on a stray root ledger; see the security doc's environmental note + HUMAN-QUEUE.

---

## Sampling Rate

- **After every task commit:** Run `python -m unittest tests.test_phase15_bi_checks -v`, plus `python scripts/gen-finding-catalogue.py --check` whenever the catalogue or a cited code changes.
- **After every plan wave:** Run `python -m unittest discover -s tests -q` (full suite).
- **Before `/gsd-verify-work`:** `sh scripts/check.sh` must be green.
- **Max feedback latency:** ~35 seconds.

---

## Per-Task Verification Map

*State B reconstruction: every requirement maps to a named test that runs green.*

| Requirement | Observable behaviour | Test Type | Named passing test(s) | Status |
|-------------|----------------------|-----------|-----------------------|--------|
| REQ-P15-01 | `cuped` is a legal `VARIANCE_ADJUSTMENTS` member (four legacy members survive, set is exactly five); `CUPED_COVARIATE_TIMINGS` is the two-valued covariate-timing vocabulary, registered once in `_VOCABULARIES` and dumped by `dsx vocab` | unit | `tests.test_cuped_vocab` (4 — legacy round-trip, two-valued timing, vocab dump); anchors `tests.test_phase15_bi_checks.test_req01_*` | ✅ green |
| REQ-P15-02 | A non-`pre_experiment` CUPED covariate blocks at `dsx gate plan` via `DSX-EXP-070` (CRITICAL); the check reads `covariate_timing` only, imports no CUPED math, and cites Deng et al. 2013 WSDM | unit | `tests.test_cuped` (8 — firing on post/absent/unrecognised, silent on pre/non-cuped, `run_checks` exit 0→1 flip, no-math-import purity, ρ²=0.25 identity); anchors `…test_req02_exp070_registered_critical`, `…test_req02_cuped_check_is_declaration_only`, `…test_req02_cuped_check_cites_wsdm_primary_source` | ✅ green |
| REQ-P15-03 | The extended good fixture (cohort_grain, `pre_experiment` CUPED, well-behaved cohort_comparisons, monotone funnel steps) stays silent (EXP-070/MET-021 absent, exit 0) at every gate threshold; new keys never enter `validity_frame` | unit | `tests.test_good_fixture_phase15` (3 — silence at all four gate points, `validity_frame` placement, additive round-trip) | ✅ green |
| REQ-P15-04 | A changing-denominator cohort declaration (unreweighted rate / treatment-share spread) blocks via `DSX-MET-021` (HIGH), respects declared tolerance, is provably disjoint from `DSX-MET-020` both directions, and cites Crook et al. 2009 KDD §6. Survivorship half **not shipped** (Brown 1992 does-not-transfer, HQ-8) | unit | `tests.test_cohort_denominator` (7 — fires on rate/share spread, silent when reweighted/equal, tolerance-respecting, disjoint both ways, only-MET-021-reachable); anchors `…test_req04_met021_registered_high`, `…test_req04_met020_and_met021_read_disjoint_surfaces`, `…test_req04_cohort_check_cites_kdd_primary_source`, `…test_req04_survivorship_code_not_minted` | ✅ green (PARTIAL, consented) |
| REQ-P15-05 | `templates/APA-TABLE-research.md` ships as an optional, research-domain deliverable that relaxes no marketing-domain ship requirement (NAR/FIG/CLM intact) | unit | `tests.test_apa_template` (3 — presence, optional + research-domain framing, no gate-code edit); anchor `…test_req05_apa_template_ships` | ✅ green |
| REQ-P15-06 | No normality-test (Shapiro-Wilk) auto-switch on the `dsx/`+`skills/` decision surface; the fixed independence→variance→normality order + unconditional Welch stand | unit | `tests.test_no_shapiro_autoswitch` (4 — 0 normality-test calls, non-empty named scan set, order pinned) | ✅ green |
| REQ-P15-07 | The catalogue extends additively to 260 (set-identity vs the frozen Phase-12 snapshot ∪ {REP-060, REP-061, EXP-070, MET-021}); `_SNAPSHOT_TOTAL` stays 256; the frozen anchor is byte-unchanged; `gen-finding-catalogue.py --check` exits 0 | unit | `tests.test_finding_catalogue_invariant` (2 — count 260 + set-identity); anchors `…test_req07_both_new_codes_in_catalogue`, `…test_req07_frozen_phase12_snapshot_present` | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

The one new module (`tests/test_phase15_bi_checks.py`) was created during this validation run to
crystallise REQ-P15-01..07 into a single phase-scoped coverage anchor. The behavioural guards
were created in execution (S4-3). All are present in the tree; `wave_0_complete: true`.

- [x] `tests/test_phase15_bi_checks.py` — phase-scoped structural coverage anchor for REQ-P15-01..07 (20 tests; CRLF-safe, stdlib-only)
- [x] `tests/test_cuped_vocab.py` — `cuped` vocabulary keystone (REQ-P15-01, 4 tests)
- [x] `tests/test_cuped.py` — `DSX-EXP-070` CUPED gate check + off-path arithmetic (REQ-P15-02, 8 tests)
- [x] `tests/test_good_fixture_phase15.py` — extended good fixture silent everywhere (REQ-P15-03, 3 tests)
- [x] `tests/test_cohort_denominator.py` — `DSX-MET-021` changing-denominator, disjoint from MET-020 (REQ-P15-04, 7 tests)
- [x] `tests/test_apa_template.py` — APA research-table template (REQ-P15-05, 3 tests)
- [x] `tests/test_no_shapiro_autoswitch.py` — no normality auto-switch guard (REQ-P15-06, 4 tests)
- [x] `tests/test_finding_catalogue_invariant.py` — additive 260 + set-identity (REQ-P15-07, 2 tests)

*If none: "Existing infrastructure covers all phase requirements."*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Citation authenticity: that Deng et al. 2013 WSDM states the pre-experiment-covariate requirement, and Crook et al. 2009 KDD §6 states the changing-allocation pooling defect, at the cited locators | REQ-P15-02, REQ-P15-04 | D-05 authenticity is a human reading the primary source; no unit test can open a paper. The *code behaviour* that enforces each rule IS fully tested above. | Already answered at **HQ-8** (operator read all three sources directly: CUPED confirmed at locator; changing-denominator confirmed at locator; survivorship does-not-transfer → unshipped). No new D-05 read owed by Phase 15. |
| Survivorship non-promotion: that `brief.md` §6.5 still carries the survivorship-bias item as an open, unpromoted entry with a falsifiable D-13 entry condition | REQ-P15-04 | Whether a future source transfers is a judgement, not a test. The negative fact (no survivorship code shipped) IS tested (`test_req04_survivorship_code_not_minted`). | Confirm at S5-2 that `brief.md` §6.5 retains the survivorship entry; REQ-P15-04 wording reflects the consented PARTIAL satisfaction (queued at S4-1, single-writer). |

*These manual-only items do **not** reduce Nyquist compliance: every requirement's deterministic
behaviour is covered by green automated tests above. Only the D-05 primary-source reads (already
answered at HQ-8) and the §6.5 non-promotion judgement — reads no unit test can perform — are
manual, exactly as with the D-05 reads in earlier phases. `nyquist_compliant: true` stands.*

---

## Validation Audit 2026-08-29

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

State B reconstruction: all 7 requirements classified **COVERED** (REQ-P15-04 PARTIAL, consented)
— each maps to a named test that runs green. **No `gsd-nyquist-auditor` spawned and no gap-filling
tests generated (0 gaps).** The single new test module (`tests/test_phase15_bi_checks.py`) was
authored to crystallise REQ-P15-01..07 into one coverage anchor, not to fill a gap the auditor
found. Independent re-gate this firing:

- New anchor `tests.test_phase15_bi_checks` → **Ran 20 tests … OK**.
- Behavioural modules: `tests.test_cuped` → **8 OK**; `tests.test_cohort_denominator` → **7 OK**; `tests.test_cuped_vocab` → **4 OK**; `tests.test_good_fixture_phase15` → **3 OK**; `tests.test_apa_template` → **3 OK**; `tests.test_no_shapiro_autoswitch` → **4 OK**.
- Catalogue invariant `tests.test_finding_catalogue_invariant` → **Ran 2 tests … OK** (260 count + set-identity vs snapshot ∪ {REP-060, REP-061, EXP-070, MET-021}); `python scripts/gen-finding-catalogue.py --check` → **exit 0**.
- Full corpus gate `sh scripts/check.sh` → **all checks passed** (`Ran 1312 tests … OK` on a clean tree, catalogue current at 260, capability manifest conformant — 14 skills, gate contract good/bad/missing, determinism identical).

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references (none — 0 gaps)
- [x] No watch-mode flags
- [x] Feedback latency < 35s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** validated 2026-08-29 — `nyquist_compliant: true`, 0 gaps, 7/7 requirements COVERED by green automated tests (REQ-P15-04 PARTIAL, consented at S4-1 via answered HQ-8); independent re-gate green (`Ran 1312 tests … OK`).
