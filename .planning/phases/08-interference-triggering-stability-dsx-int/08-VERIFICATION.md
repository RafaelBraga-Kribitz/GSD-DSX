---
phase: 08-interference-triggering-stability-dsx-int
verified: 2026-08-13T00:00:00Z
status: gaps_found
score: 5/7 must-haves verified
behavior_unverified: 0
overrides_applied: 0
gaps:
  - truth: "A declared interference risk other than none, with no admissible mitigation and no residual note, is blocked at dsx gate plan (REQ-P8-01/REQ-P8-02; phase goal clause 1)."
    status: failed
    reason: >
      An out-of-vocabulary interference.mitigation value silently bypasses both DSX-INT-010
      and DSX-INT-011. Reproduced independently against the committed tree: copying
      examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml and changing line 145
      from `mitigation: none` to `mitigation: buget_isolation` (misspelling of the valid
      `budget_isolation`), with residual_note left blank, produces only
      DSX-SPEC-082/HIGH and DSX-MET-040/HIGH, and `dsx gate plan` exits 0 (PASS). The
      unmodified fixture, by contrast, correctly exits 1 naming DSX-INT-010/CRITICAL.
      Root cause: `_check_interference_unaddressed` (dsx/frame/interference.py:172) only
      treats a mitigation as "absent" when it normalizes to the literal string "none";
      `_check_interference_mitigation_admissibility` (dsx/frame/interference.py:277)
      independently short-circuits on any mitigation that is not a recognised member of
      INTERFERENCE_MITIGATIONS. Neither check treats "declared but not a real mitigation"
      as equivalent to "no mitigation" for purposes of judging the risk unaddressed.
      DSX-SPEC-082 (vocabulary violation) is HIGH, below `GATE_THRESHOLDS["plan"] ==
      "CRITICAL"` (dsx/cli.py), so the gate passes. A single typo is strictly safer,
      gate-wise, than honestly writing `mitigation: none`. This is documented in
      08-REVIEW.md as CR-01 (critical) and remains unfixed in the current tree — the fix
      proposed there (treat "not admissible-in-principle" as equivalent to "absent" in
      `_check_interference_unaddressed`) has not been applied, and no regression test
      exists (`git grep -n "INTERFERENCE_MITIGATIONS" tests/test_frame_interference.py`
      shows only a set-subset assertion, no out-of-vocabulary-mitigation test).
    artifacts:
      - path: "dsx/frame/interference.py"
        issue: "_check_interference_unaddressed (line 172) and _check_interference_mitigation_admissibility (line 277) both treat an unrecognised mitigation string as equivalent to a validly-declared, admissible-in-principle mitigation for their own judgment purposes, rather than as equivalent to absence."
    missing:
      - "Apply 08-REVIEW.md CR-01's fix: mitigation_absent = normalized_mitigation == \"none\" or normalized_mitigation not in INTERFERENCE_MITIGATIONS in _check_interference_unaddressed, so DSX-INT-010 still fires when the declared mitigation is out-of-vocabulary and the risk is otherwise unaddressed."
      - "Add a regression test asserting DSX-INT-010 fires for a real, declared risk with an out-of-vocabulary mitigation string and a blank/placeholder residual_note (e.g. test_out_of_vocabulary_mitigation_with_blank_residual_still_fires_int_010)."
      - "Confirm DSX-SPEC-082 continues to fire independently on the same input (it currently does, correctly, and should keep doing so — the two findings describe different facts, not a double-report of one defect)."
deferred: []
human_verification: []
---

# Phase 8: Interference, triggering, stability Verification Report

**Phase Goal:** The largest uncovered risk class for a 60%-experiment workload is adjudicated —
declared interference with no mitigation and no residual note, shared-budget and marketplace
patterns treated as distinct risks, triggered-versus-eligible analysis populations with no
dilution adjustment, and unassessed novelty/primacy over the declared stability window.

**Verified:** 2026-08-13
**Status:** gaps_found
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | A declared interference risk with no mitigation and no residual note is blocked at `dsx gate plan`, citing SUTVA (REQ-P8-01) | ✗ FAILED | The unmutated fixture correctly blocks (`DSX-INT-010`, exit 1). But an out-of-vocabulary `mitigation` string (e.g. a one-letter typo of `budget_isolation`) bypasses both `DSX-INT-010` and `DSX-INT-011` — `dsx gate plan` exits 0. Reproduced independently, matches 08-REVIEW.md CR-01. See Gaps below. |
| 2 | Shared-budget and marketplace interference are distinct risks with distinct admissible mitigations (REQ-P8-02) | ✓ VERIFIED | `shared_budget` + `cluster_randomisation` → `DSX-INT-011`/CRITICAL, `dsx gate plan` exits 1. `marketplace` + `cluster_randomisation` → no `DSX-INT-*` finding, `dsx gate plan` exits 0 (other unrelated findings only). Confirmed by direct CLI invocation against mutated temp copies of the fixture. `_RISK_MITIGATION_MAP` key set equals `INTERFERENCE_RISKS` (`tests/test_frame_interference.py::TestRiskMitigationMap`). |
| 3 | `DSX-INT-030` blocks eligible-population analysis of an additive metric with no dilution adjustment, and a test asserts `delta_diluted = delta_triggered × trigger_rate` against the Deng & Hu (2015) published counterexample (REQ-P8-03) | ✓ VERIFIED | `examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml` exits 1 at `dsx gate plan`, naming `DSX-INT-030`/CRITICAL (reproduced directly). `dsx.mathx.diluted_effect` exists, is cited to Formula (1), raises `ValueError` outside `[0,1]`, admits both endpoints, and `tests.test_dsx -k dilut` (5 tests) is green. `diluted_effect` is never called from `dsx/frame/` or `dsx/checks/` (`git grep -n "diluted_effect(" dsx/` shows only the definition). |
| 4 | Ratio-metric dilution is explicitly out of scope, with a falsifiable entry condition, not the paper's availability (REQ-P8-04) | ✓ VERIFIED | `DSX-INT-030` does not fire on ratio/rate-typed metrics under otherwise-firing conditions (`test_ratio_scope_boundary_ratio_metric_produces_no_finding`, `test_ratio_scope_boundary_rate_metric_produces_no_finding`). `brief.md` §6.5 carries the corrected row naming the per-user-data requirement of Formula (3) rather than paper availability (brief.md:376). A documentation-content test guards the row (`tests/test_known_bad_corpus.py::test_brief_states_the_ratio_metric_dilution_entry_condition_as_a_falsifiable_blocker`, passes). ROADMAP success criterion 4 and REQ-P8-04 both carry the corrected wording (`.planning/ROADMAP.md:307-313`, `.planning/REQUIREMENTS.md:111`). |
| 5 | An unassessed novelty/primacy effect over the declared stability window is flagged at verify/ship (HIGH), not plan, with the assessment method cited (REQ-P8-05) | ✓ VERIFIED | Mutated copy of `examples/good-ANALYSIS-SPEC.yaml` with `novelty_primacy_assessed: false`: `dsx gate plan` exits 0 (HIGH below CRITICAL threshold), `dsx gate verify` exits 1 naming `DSX-INT-040`/HIGH — reproduced directly. Citation to Sadeghi et al. (2021) is in the check's docstring. `DSX-EXP-030`/`031` unchanged (not in `files_modified` of any Phase 8 plan). Finding detail explicitly states disjointness from `DSX-EXP-030` (`tests/test_frame_interference.py::test_stability_detail_names_dsx_exp_030_and_states_disjointness`). |
| 6 | No `DSX-INT-*` check reads `inference.paradigm` (REQ-P8-06) | ✓ VERIFIED | `tests/test_frame_boundary.py::TestFrameParadigmReadBoundary` (8 tests, all pass) includes `dsx/frame/interference.py` in its AST + text scan, both for direct subscript chains and string-literal dotted paths. `git grep -n "paradigm" dsx/frame/interference.py` shows no reads. |
| 7 | The known-bad corpus's structural guarantees hold after the D-15 rewrite (per-fixture target-defect map replacing the family-prefix allow-list) | ✓ VERIFIED | `_TARGET_DEFECT_CODES` and `_EXPECTED_CAUGHT_DEFECTS` are combined by `_effective_target_map()`. Independently mutation-tested: removing the `interference-shared-budget` entry from `_TARGET_DEFECT_CODES`, or the `bayesian-continuous-monitoring` entry from `_EXPECTED_CAUGHT_DEFECTS`, each turns `tests.test_known_bad_corpus` red (2 and 4 failures respectively) with a message correctly naming the newly-undocumented code. Both maps are load-bearing, restored to original state after the check. |

**Score:** 5/7 truths verified (2 present-and-partially-working but one contains a real bypass).
Note: truth 7 is a supporting-infrastructure truth added by the verifier (D-15 was the phase's
largest structural item per 08-CONTEXT.md); truths 1-6 map directly to REQ-P8-01…06.

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `dsx/frame/interference.py` | New module, four codes, admissibility map, additive partition | ✓ VERIFIED (with defect) | Exists, all four codes present, wired into `check()`. Contains the CR-01 bypass described above. |
| `dsx/mathx.py::diluted_effect` | Pure function, cited, range-validated | ✓ VERIFIED | Present, tested, never called from gate path. |
| `dsx/spec.py::needs_causal_block` | Extracted shared gating condition | ✓ VERIFIED | `git grep -n "def needs_causal_block" dsx/spec.py` present; used identically by `_validate_validity_frame_shape` and `interference.check()`. |
| `tests/test_frame_interference.py` | New test module | ✓ VERIFIED | 52 tests, all pass; covers admissibility, dilution, stability, malformed-shape hardening. Does **not** cover the out-of-vocabulary-mitigation bypass. |
| `examples/known-bad/triggering-dilution-*` | New fixture pair | ✓ VERIFIED | Both files exist; spec exits 1 at plan naming `DSX-INT-030`; postmortem names the code. |
| `references/finding-codes.md` | Catalogue entry for all four codes | ✓ VERIFIED | `DSX-INT-010/011/030/040` all listed under an interference heading; `gen-finding-catalogue.py --check` exits 0. |
| `brief.md` §6.5 row | Corrected ratio-metric entry condition | ✓ VERIFIED | Present at brief.md:376, guarded by a documentation-content test. |
| `.planning/ROADMAP.md` / `.planning/REQUIREMENTS.md` | Amended success criteria 3/4 and REQ-P8-04 | ✓ VERIFIED | Both carry the corrected D-10/D-12 wording; no retired-phrasing test regressed. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|-----|-----|--------|---------|
| `_RISK_MITIGATION_MAP` | `dsx.spec.INTERFERENCE_RISKS` | key-set equality test | ✓ WIRED | `test_map_keys_equal_risks_and_values_subset_of_mitigations` passes. |
| `dsx/cli.py::GATE_PROFILES` | `interference.check` | `CHECKS["interference"]`, registered in plan/verify/ship, absent from execute | ✓ WIRED | `test_interference_registered_in_plan_verify_ship_absent_from_execute` passes; confirmed live via direct CLI runs at all four gate points. |
| `_ADDITIVE_METRIC_TYPES`/`_RATIO_METRIC_TYPES` | `dsx.spec.METRIC_TYPES` | subset/disjoint reference | ✓ WIRED | `test_additive_and_ratio_metric_type_partitions_are_subsets_disjoint_and_proper` passes. |
| `_check_interference_unaddressed` | `_check_interference_mitigation_admissibility` | disjointness (never both fire) | ✓ WIRED for in-vocabulary inputs | `test_inadmissible_mitigation_fires_int_011_not_int_010` passes for valid-vocabulary mitigations. Disjointness is preserved for the out-of-vocabulary case too, but only because **neither** fires (the CR-01 gap) — not the intended form of disjointness. |
| `tests/test_known_bad_corpus.py::_TARGET_DEFECT_CODES` | `tests/test_known_bad_corpus.py::_EXPECTED_CAUGHT_DEFECTS` | `_effective_target_map()` | ✓ WIRED | Both maps independently load-bearing; mutation-verified by this report. |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Unmodified shared-budget fixture blocks plan | `python3 -m dsx gate plan --spec examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml` | exit 1, `DSX-INT-010`/CRITICAL | ✓ PASS |
| Misspelled mitigation bypasses plan gate | same spec, `mitigation: buget_isolation` | exit 0, only `DSX-SPEC-082`/HIGH, `DSX-MET-040`/HIGH | ✗ FAIL (CR-01) |
| shared_budget + cluster_randomisation blocks | mutated temp copy | exit 1, `DSX-INT-011`/CRITICAL | ✓ PASS |
| marketplace + cluster_randomisation clears | mutated temp copy | exit 0, no `DSX-INT-*` | ✓ PASS |
| triggering-dilution fixture blocks plan | `python3 -m dsx gate plan --spec examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml` | exit 1, `DSX-INT-030`/CRITICAL | ✓ PASS |
| unassessed novelty/primacy: plan vs verify | mutated `good-ANALYSIS-SPEC.yaml`, `novelty_primacy_assessed: false` | plan exit 0, verify exit 1 naming `DSX-INT-040`/HIGH | ✓ PASS |
| weak-identification-mmm blocks verify/ship on DSX-INT-030 | `dsx gate verify`/`dsx gate ship` against that fixture | both exit 1, `DSX-INT-030`/CRITICAL present | ✓ PASS (functionally true; see WR-01 below for the missing mechanical assertion of this) |
| Full suite | `python3 -m unittest discover -s tests` | 518 tests, OK (skipped=2) | ✓ PASS |
| Full project check | `sh scripts/check.sh` | all checks passed | ✓ PASS |
| Corpus map mutation check | remove one entry from each of the two live `_TARGET_DEFECT_CODES`/`_EXPECTED_CAUGHT_DEFECTS` maps | both mutations turn `test_known_bad_corpus` red; both restored | ✓ PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| REQ-P8-01 | 08-03 | Declared interference risk with no mitigation/residual note blocked, SUTVA-cited | ✗ BLOCKED | CR-01: bypassed by an out-of-vocabulary mitigation string. |
| REQ-P8-02 | 08-03 | Shared-budget vs marketplace distinct risks/mitigations | ✓ SATISFIED | Directly reproduced. |
| REQ-P8-03 | 08-01, 08-04 | `DSX-INT-030` + `diluted_effect` formula | ✓ SATISFIED | Directly reproduced; fixture blocks; math kernel function correct and cited. |
| REQ-P8-04 | 08-01, 08-04, 08-06 | Ratio-metric dilution out of scope, falsifiable entry condition | ✓ SATISFIED | Scope boundary tested; brief.md/ROADMAP/REQUIREMENTS all corrected and consistent. |
| REQ-P8-05 | 08-03 (fixtures), 08-05 | Unassessed novelty/primacy flagged, method cited | ✓ SATISFIED | Directly reproduced (plan/verify split). |
| REQ-P8-06 | all | No `DSX-INT-*` reads `inference.paradigm` | ✓ SATISFIED | Boundary scanner includes the module and passes. |

No orphaned requirements: `grep -E "Phase 8" .planning/REQUIREMENTS.md` maps only REQ-P8-01…06,
and all six are claimed across the six plans' `requirements:` frontmatter.

**Note on REQUIREMENTS.md checkbox state:** `.planning/REQUIREMENTS.md:108-113` still shows all
six `REQ-P8-*` items as unchecked `[ ]`, and its separate tracking table (lines ~204-209) shows
`REQ-P8-04`/`REQ-P8-05` as "Complete" but `REQ-P8-01/02/03/06` as "Pending" — an inconsistency
with the SUMMARY.md claims of full completion. This mirrors the same unchecked pattern already
present for Phase 7's REQ-P7-* entries, so it appears to be a standing convention (checkboxes are
flipped at a later milestone step, not at phase-verification time) rather than a Phase-8-specific
gap. Flagged for awareness, not scored as a failure.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `dsx/frame/interference.py` | 172 | Silent gate bypass: unrecognised mitigation treated as "not absent" | 🛑 Blocker | REQ-P8-01/02, phase goal clause 1 — see Gaps |
| `tests/test_dsx.py` | 162-170 | Tautological test (`assertNotEqual(-18.0, -26.0)`) that never calls `mathx.diluted_effect`, despite its name/docstring claiming to test the function's scope boundary | ⚠️ Warning | Weakens confidence in REQ-P8-04's math-kernel verification, though the literal plan `must_haves` wording ("asserts the published naive value and published true effect are different numbers") is technically satisfied. Matches 08-REVIEW.md WR-02. |
| `dsx/frame/interference.py` | 404-405 | `metric.get("type", "")` treats explicit `type: null` differently from an absent key — the former silently skips both the finding path and the documented decision-record path (reproduced independently: no finding, no decision record) | ℹ️ Info/Warning | Decision-trail completeness gap only; no finding fires either way (correct outcome, incomplete audit trail). Matches 08-REVIEW.md WR-03. |
| `tests/test_known_bad_corpus.py` | 134-138 | `_TARGET_DEFECT_CODES` has no on-disk key-completeness guard symmetrical to `_EXPECTED_CAUGHT_DEFECTS`'s `test_expected_caught_defects_keys_match_the_corpus_on_disk` | ℹ️ Info/Warning | A renamed/removed fixture would silently drop a point-scoped guarantee. Matches 08-REVIEW.md WR-04. No `TBD`/`FIXME`/`XXX` markers found in any Phase 8 file. |

No unreferenced `TBD`/`FIXME`/`XXX` debt markers found in files modified by this phase.

### TDD Gate (advisory)

Plans 08-01, 08-04 and 08-05 have GREEN commits with no matching RED commit in the visible git
log; 08-03 shows both. MVP mode is off for this project, so this is non-blocking, but is recorded
per the orchestrator's finding.

### Gaps Summary

One CRITICAL defect blocks phase-goal achievement: **DSX-INT-010 and DSX-INT-011 are both
silently defeated by an out-of-vocabulary `interference.mitigation` value.** This was reproduced
independently against the committed tree (not merely taken on the code review's word) — a
one-letter misspelling of `budget_isolation` turns a `dsx gate plan` exit-1 CRITICAL block into
an exit-0 PASS, for a spec that has a real, declared, functionally-unmitigated shared-budget
interference risk with a blank residual note. This is precisely the failure mode the phase goal's
first clause exists to close ("declared interference with no mitigation and no residual note ...
adjudicated") and precisely what REQ-P8-01/REQ-P8-02 require. The gap is both unfixed and
untested — 08-REVIEW.md documents it as CR-01 with a specific proposed fix and regression test,
neither of which has landed in the current tree.

Three further warning-level items (WR-02, WR-03, WR-04 from 08-REVIEW.md) were independently
reproduced and do not block the phase goal on their own — they are test-strength and
audit-completeness gaps, not runtime defects — but should be closed alongside CR-01 since a
gap-closure plan will already be touching this file and its test suite.

Everything else — REQ-P8-02 through REQ-P8-06, the D-09 math kernel, the D-15 corpus
restructure, the D-13/D-14 disjointness and boundary proofs, the brief.md/ROADMAP/REQUIREMENTS
amendments — was independently reproduced and verified working.

---

_Verified: 2026-08-13_
_Verifier: Claude (gsd-verifier)_
