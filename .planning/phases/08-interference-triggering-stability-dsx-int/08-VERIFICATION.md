---
phase: 08-interference-triggering-stability-dsx-int
verified: 2026-08-13T00:00:00Z
status: gaps_found
score: 5/6 must-haves verified
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: gaps_found
  previous_score: 5/7
  gaps_closed:
    - "An out-of-vocabulary triggering.analysis_population value (e.g. eligable) bypassing DSX-INT-030 — closed by plan 08-09. Independently reproduced: typo'd population now fires DSX-INT-030/CRITICAL; honestly-declared triggered, and absent, populations still produce no finding."
  gaps_remaining:
    - "A declared interference risk other than none, with no admissible mitigation and no residual note, is blocked at dsx gate plan no matter which INTERFERENCE_* field carries the typo (REQ-P8-01/REQ-P8-02; phase goal clause 1) — STILL FAILS on a third path plan 08-08 did not close: an out-of-vocabulary risk paired with a real, recognised, non-none mitigation (e.g. risk=shared_buget, mitigation=geo_split) produces zero DSX-INT-* findings and dsx gate plan exits 0. 08-08 fixed only the 'typo'd risk + no mitigation' sub-case."
  regressions: []
gaps:
  - truth: "A declared interference risk other than none, with no admissible mitigation and no residual note, is blocked at dsx gate plan no matter which INTERFERENCE_* field carries the typo, in every mitigation-declaration state (REQ-P8-01/REQ-P8-02; phase goal clause 1). This is 08-VERIFICATION.md's first failed truth, restated to cover the sub-case plan 08-08 left open."
    status: failed
    reason: >
      Plan 08-08 fixed _check_interference_unaddressed's risk guard so an out-of-vocabulary
      risk no longer short-circuits to "nothing to adjudicate" — but only when the
      mitigation side is also absent/none/unrecognised, because DSX-INT-010 only fires when
      mitigation_absent is True. When the typo'd risk is paired with a real, recognised,
      non-none mitigation, mitigation_absent is False, so DSX-INT-010 stays silent by its
      own construction — and _check_interference_mitigation_admissibility's risk guard
      (dsx/frame/interference.py:313, `if normalized_risk == "none" or normalized_risk not
      in INTERFERENCE_RISKS: return`) was deliberately left unedited by 08-08 (confirmed via
      git diff and the plan's own prohibitions list), so it returns before reaching its
      admissibility judgment for any unrecognised risk, mitigation notwithstanding.
      Independently reproduced (not taken on the code review's word) at both levels:
      unit level — interference.check() on a causal spec with risk="shared_buget",
      mitigation="geo_split", residual_note="" returns an empty finding set, while the
      same spec with risk="shared_budget" (correctly spelled) returns {'DSX-INT-011'};
      gate level — mutating the committed
      examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml to
      risk: shared_buget / mitigation: geo_split / residual_note: "" and running
      `dsx gate plan --json` against it produces block: false, CRITICAL: 0, exit 0, with
      only DSX-SPEC-082/HIGH in the finding list — no DSX-INT-010 and no DSX-INT-011.
      The rationale on record in 08-08-PLAN.md (T-8-18) and 08-08-SUMMARY.md for leaving
      _check_interference_mitigation_admissibility's risk guard untouched — that judging an
      out-of-vocabulary risk there "would make DSX-INT-011 double-report what DSX-INT-010
      now reports" — is independently falsified: a 390-combination sweep across
      INTERFERENCE_RISKS members, near-miss typos, out-of-vocabulary strings, blanks and
      None, crossed with INTERFERENCE_MITIGATIONS members, near-miss typos and blanks, and
      three residual_note shapes, run against the shipped DSX-INT-010 predicate plus a
      minimally-patched DSX-INT-011 predicate (only the `normalized_risk not in
      INTERFERENCE_RISKS` clause removed, letting `_RISK_MITIGATION_MAP.get(normalized_risk,
      frozenset())` degrade to an empty admissible set the way the DSX-INT-010 guard's own
      `.get(normalized_risk, ())` already does), produced zero combinations where both codes
      fired at once — disjointness holds on the mitigation dimension alone (absent/none/
      unrecognised vs. present/recognised/non-none), independent of risk-vocabulary
      membership. The disjointness invariant (DSX-INT-010 and DSX-INT-011 never both fire)
      does hold today, but only because the risk-typo-plus-real-mitigation input triggers
      neither check, not because the checks correctly disjointly partition it.
    artifacts:
      - path: "dsx/frame/interference.py"
        issue: "Line 311-314, _check_interference_mitigation_admissibility: `if normalized_risk == \"none\" or normalized_risk not in INTERFERENCE_RISKS: return` returns before the admissibility judgment for any risk string outside INTERFERENCE_RISKS, regardless of whether a real, recognised, non-none mitigation was declared. This guard was explicitly scoped out of plan 08-08 (08-08-PLAN.md prohibitions: '_check_interference_mitigation_admissibility is not edited') on a rationale this round's independent reproduction disproves."
    missing:
      - "Drop the `or normalized_risk not in INTERFERENCE_RISKS` clause from _check_interference_mitigation_admissibility's guard, keeping only `if normalized_risk == \"none\": return`, so an unrecognised risk falls through to the judgment point exactly as DSX-INT-010's guard now does — `_RISK_MITIGATION_MAP.get(normalized_risk, frozenset())` already degrades correctly to an empty admissible set for a risk it does not contain, matching the `admissible_listed` pattern _check_interference_unaddressed already uses."
      - "Update _check_interference_mitigation_admissibility's docstring, which currently states DSX-INT-011 'requires a real, recognised risk' — no longer true after the fix."
      - "Correct _check_interference_unaddressed's own disjointness paragraph, which currently attributes DSX-INT-011's early return for an unrecognised risk to '_RISK_MITIGATION_MAP has no admissibility cell for a risk it does not contain' — today the guard returns via an explicit `not in INTERFERENCE_RISKS` check, never reaching the map; after the fix the attribution becomes accurate for a different reason and should be restated."
      - "Add a unit-level regression test pairing an out-of-vocabulary risk (e.g. risk=\"shared_buget\") with a real, recognised, INTERFERENCE_RISKS-inadmissible mitigation (e.g. mitigation=\"geo_split\") and asserting DSX-INT-011 fires — the sub-case none of plan 08-08's or plan 08-09's new tests cover, because both existing out-of-vocabulary-risk tests use the default mitigation=\"none\"."
      - "Add a gate-level regression test mutating the committed shared-budget fixture to risk: shared_buget / mitigation: geo_split (a real, recognised, but channel-mismatched mitigation) and asserting dsx gate plan exits 1, naming DSX-INT-011 and DSX-SPEC-082 via the structured --json finding list."
      - "Re-run the disjointness proof (unit + gate level, in-vocabulary and out-of-vocabulary risk, absent/none/real mitigation) after the fix, the same shape 08-08/08-09 already used for their own sub-cases."
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
**Re-verification:** Yes — after 08-08/08-09 gap-closure round

## What changed since the last report

The previous verification (`9201a7c`, in git history) scored 5/7 and listed two gaps:
gap 1, an out-of-vocabulary `interference.risk` bypassing DSX-INT-010; gap 2, an
out-of-vocabulary `triggering.analysis_population` bypassing DSX-INT-030. Plans 08-08 and
08-09 executed against those two gaps respectively, touching only
`dsx/frame/interference.py` and `tests/test_frame_interference.py`.

**Gap 2 (triggering population) is genuinely closed.** Independently reproduced, not taken
on the summary's word: `interference.check()` on a causal spec with a `count`-type metric,
`triggering.analysis_population: "eligable"` (typo) and `dilution_adjusted: false` now fires
`DSX-INT-030`/CRITICAL; the same spec with `analysis_population: "triggered"` or the field
absent entirely still produces no finding. `dsx gate plan --json` against a mutated copy of
the committed `triggering-dilution-ANALYSIS-SPEC.yaml` fixture (`eligible` → `eligable`)
exits 1 naming `DSX-INT-030`/CRITICAL and `DSX-SPEC-082`/HIGH, where it exited 0 before this
round.

**Gap 1 (interference risk) is only partially closed — a new critical finding from the
deep code review (`08-REVIEW.md` CR-01) survives independent reproduction.** Plan 08-08's
fix to `_check_interference_unaddressed` correctly closes the sub-case where an
out-of-vocabulary risk is paired with an absent/`none`/unrecognised mitigation. It does
**not** close the sub-case where the same out-of-vocabulary risk is paired with a real,
recognised, non-`none` mitigation, because that input routes to
`_check_interference_mitigation_admissibility` (`DSX-INT-011`) instead of
`_check_interference_unaddressed` (`DSX-INT-010`) — and `DSX-INT-011`'s own risk guard was
deliberately left unedited by plan 08-08, on a "would double-report" rationale this round's
independent reproduction (a 390-combination sweep, separate from the reviewer's 400) shows
to be false. See the `gaps` entry above for full reproduction detail and the disjointness
sweep. `dsx gate plan` still exits `0` for this input.

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | A declared interference risk other than `none`, with no admissible mitigation and no residual note, is blocked at `dsx gate plan` regardless of which `INTERFERENCE_*` field carries the typo (REQ-P8-01/REQ-P8-02; phase goal clause 1) | ✗ FAILED | `risk="shared_buget"` + `mitigation="geo_split"` (real, recognised, inadmissible) + blank `residual_note` produces zero findings from `interference.check()` and `dsx gate plan --json` exits 0 with only `DSX-SPEC-082`/HIGH. Reproduced independently at both levels; see gaps section. |
| 2 | Shared-budget and marketplace interference resolve to distinct declared risks with distinct admissible mitigations — a marketplace-only mitigation applied to a shared-budget risk still exits 1 (REQ-P8-02, phase goal clause 2, roadmap SC2) | ✓ VERIFIED | `tests.test_frame_interference.TestRiskMitigationMap.test_cluster_randomisation_admissible_for_marketplace_not_shared_budget` passes. Independently reproduced: `shared_budget`+`cluster_randomisation` → `{'DSX-INT-011'}`; `marketplace`+`cluster_randomisation` → `set()`. |
| 3 | `DSX-INT-030` blocks eligible-population analysis of an additive metric with no dilution adjustment declared, no matter how `triggering.analysis_population` is spelled (REQ-P8-03, phase goal clause 3, roadmap SC3) | ✓ VERIFIED | Gap 2 closed this round. Independently reproduced: `analysis_population="eligable"` fires `DSX-INT-030`/CRITICAL; `"triggered"` and absent both produce no finding. `dsx gate plan` on a mutated fixture: exit 1 with `DSX-INT-030` + `DSX-SPEC-082`, where it exited 0 before this round. |
| 4 | A ratio metric under triggering is explicitly out of scope — `DSX-INT-030` does not fire on it, and `brief.md` §6.5 carries the corrected per-unit-data entry condition (REQ-P8-04, phase goal clause 4, roadmap SC4) | ✓ VERIFIED | Not touched by this round's diff (confined to `dsx/frame/interference.py` and `tests/test_frame_interference.py`, neither of which regresses this). Regression-checked: `python3 -m unittest tests.test_dsx -k dilut` (5 tests, OK), `tests.test_frame_interference -k ratio_scope` (2 tests, OK). REQUIREMENTS.md already records REQ-P8-04 Complete from plan 08-06. |
| 5 | An unassessed novelty/primacy effect over the declared stability window is flagged at verify/ship with the assessment method cited, and no `dsx/frame/interference.py` code path reads `inference.paradigm` (REQ-P8-05, REQ-P8-06, phase goal clause 5, roadmap SC5) | ✓ VERIFIED | Not touched by this round's diff. Regression-checked: `tests.test_frame_interference.TestStabilityAssessment` (11 tests, OK), `tests.test_frame_boundary.TestFrameParadigmReadBoundary` (6 tests, OK — see Note below). REQUIREMENTS.md already records REQ-P8-05 Complete from plan 08-06. |
| 6 | `DSX-INT-010` and `DSX-INT-011` never both fire on the same interference sub-block (disjointness invariant, requested explicitly for this round) | ✓ VERIFIED (as currently implemented) | 270-combination sweep across `INTERFERENCE_RISKS` members, typo'd near-misses, blanks/None, crossed with `INTERFERENCE_MITIGATIONS` members, typo'd near-misses, blanks, and three `residual_note` shapes, run against the shipped code: zero combinations produce both codes. Holds today, but note truth 1's gap: for the specific bypass input, the invariant holds only because *neither* check fires, not because the checks correctly and disjointly partition the input. |

**Score:** 5/6 truths verified (1 failed, 0 present-behavior-unverified)

**Note on truth 5's test count:** `08-08-SUMMARY.md` documents a pre-existing discrepancy —
the original `08-VERIFICATION.md` and the plan's acceptance criteria both stated
`TestFrameParadigmReadBoundary` runs 8 tests; the actual, unchanged count is 6. Independently
confirmed (`python3 -m unittest tests.test_frame_boundary.TestFrameParadigmReadBoundary -v`
→ `Ran 6 tests ... OK`). This is a stale count in the prior verifier's own report, not a
regression from this round's diff (that file is untouched by commits `eb8ae4c`, `cf4da61`,
`a864d6f`, `ef9fc65`, `12d5c56`) — informational only, does not affect truth 5's status.

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `dsx/frame/interference.py`, `_check_interference_unaddressed`'s risk guard | Short-circuits on the literal `none` alone (08-08 scope) | ✓ VERIFIED | Line 187: `if normalized_risk == "none": return`. Confirmed present, wired, and behaviorally correct for its own sub-case. |
| `dsx/frame/interference.py`, `_check_interference_mitigation_admissibility`'s risk guard | Deliberately unedited per 08-08's prohibitions | ✓ VERIFIED (unedited) — ⚠️ but this is the root of the remaining gap | Line 313: `if normalized_risk == "none" or normalized_risk not in INTERFERENCE_RISKS: return`, byte-identical to before this round. Present exactly as the plan required — the plan's scoping decision itself is what truth 1 fails on. |
| `dsx/frame/interference.py`, `_check_triggering_dilution`'s population guard | Distinguishes `triggered`/absent from `eligible`/out-of-vocabulary (08-09 scope) | ✓ VERIFIED | Line 430: `if normalized_population == "triggered" or not normalized_population: return`. Confirmed present, wired, behaviorally correct. |
| `tests/test_frame_interference.py`, `_gate_findings(spec_path, point)` helper | Structured `--json` finding-list helper, closing WR-01 | ✓ VERIFIED | Present, used by 6 call sites (`grep -c _gate_findings` → 6), including the rewritten mitigation-field gate test with a documented mutation proof. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|-----|-----|--------|---------|
| `_check_interference_unaddressed` | `dsx.spec.INTERFERENCE_RISKS` | Risk-guard membership treatment | ✓ WIRED | Out-of-vocabulary risk now adjudicated instead of short-circuited, for the no-mitigation sub-case. |
| `_check_interference_unaddressed` | `_check_interference_mitigation_admissibility` | Disjointness by construction | ⚠️ PARTIAL | Disjoint today (truth 6), but only because the mismatched sub-case (typo'd risk + real mitigation) reaches neither check's judgment point — see truth 1. |
| `_check_triggering_dilution` | `dsx.spec.ANALYSIS_POPULATIONS` | Population-guard membership treatment | ✓ WIRED | Out-of-vocabulary population now adjudicated. Vocabulary pinned to exactly `{eligible, triggered}` by a dedicated contract test. |
| Gate-level tests | `_gate_findings` | Structured JSON assertions | ✓ WIRED | Both new regression tests (08-08, 08-09) and the tightened WR-01 tests read `by_code` dicts, not rendered text. |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Full test suite | `python3 -m unittest discover -s tests` | `Ran 536 tests ... OK (skipped=2)` | ✓ PASS |
| Project check script | `sh scripts/check.sh` | `all checks passed` | ✓ PASS |
| Finding catalogue | `python3 scripts/gen-finding-catalogue.py --check` | `finding catalogue is current` | ✓ PASS |
| CR-01 bypass reproduction (unit level) | `interference.check()` on `risk="shared_buget", mitigation="geo_split", residual_note=""` | `findings: []` (empty) | ✗ FAIL (confirms gap) |
| CR-01 bypass reproduction (gate level) | `dsx gate plan --spec <mutated fixture> --json` | `exit 0`, `CRITICAL: 0`, only `DSX-SPEC-082`/HIGH | ✗ FAIL (confirms gap) |
| Disjointness sweep (current code) | 270-combo Python sweep over `interference.check()` | 0 combinations fire both `DSX-INT-010` and `DSX-INT-011` | ✓ PASS |
| "Double-report" rationale falsification | 390-combo sweep, DSX-INT-011 with risk-vocabulary guard removed | 0 combinations produce both findings | Rationale FALSE — confirms `08-REVIEW.md` CR-01's claim independently |
| Gap 2 closure (unit level) | `interference.check()` on typo'd/triggered/absent `analysis_population` | typo → `DSX-INT-030`; triggered/absent → no finding | ✓ PASS |
| Gap 2 closure (gate level) | `dsx gate plan --json` on mutated triggering-dilution fixture | exit 1, `DSX-INT-030` + `DSX-SPEC-082` | ✓ PASS |

### Requirements Coverage

| Requirement | Source Plan(s) | Description | Status | Evidence |
|-------------|-----------------|--------------|--------|----------|
| REQ-P8-01 | 08-03, 08-07, 08-08 | A declared interference risk other than `none` without a mitigation or residual note is blocked | ✗ BLOCKED | CR-01's surviving bypass (typo'd risk + real mitigation) means this is not true in every case. REQUIREMENTS.md correctly still shows this Pending. |
| REQ-P8-02 | 08-03, 08-07, 08-08 | Shared-budget and marketplace treated as distinct risks with distinct admissible mitigations | ✗ BLOCKED (jointly with REQ-P8-01, same guard) | The distinctness map itself is correct (truth 2, VERIFIED) but the requirement text also implies the risk-declaration side is adjudicated, which CR-01 defeats for out-of-vocabulary risk + real mitigation. REQUIREMENTS.md correctly still shows this Pending. |
| REQ-P8-03 | 08-01, 08-02, 08-04, 08-09 | `DSX-INT-030` blocks eligible-population analysis of additive metrics with no dilution adjustment | ✓ SATISFIED | Gap 2 closed this round, independently reproduced (truth 3). REQUIREMENTS.md should move this from Pending to Complete. |
| REQ-P8-04 | 08-01, 08-04, 08-06 | Ratio-metric dilution explicitly out of scope, entry condition corrected | ✓ SATISFIED | Unchanged this round; REQUIREMENTS.md already shows Complete. |
| REQ-P8-05 | 08-02, 08-05, 08-06 | Unassessed novelty/primacy flagged with cited method | ✓ SATISFIED | Unchanged this round; REQUIREMENTS.md already shows Complete. |
| REQ-P8-06 | 08-03 | No `DSX-INT-*` check reads `inference.paradigm` | ✓ SATISFIED | `TestFrameParadigmReadBoundary` — 6/6 pass, includes `dsx/frame/interference.py` in its scan. REQUIREMENTS.md correctly still shows this Pending pending an orchestrator update — recommend moving to Complete since this specific requirement is unaffected by the REQ-P8-01/02 gap. |

No orphaned requirements — all six IDs (`REQ-P8-01` through `REQ-P8-06`) are claimed by at least one plan's `requirements` frontmatter field and cross-reference cleanly against `.planning/REQUIREMENTS.md` lines 108-113.

### Anti-Patterns Found

None. Both files this round's diff touches (`dsx/frame/interference.py`, `tests/test_frame_interference.py`) were scanned for debt markers (`TBD`, `FIXME`, `XXX`, `TODO`, `HACK`, `PLACEHOLDER`) — zero matches. No stub returns, no hardcoded-empty data flowing to a gate decision, no console-log-only implementations.

### Gaps Summary

One gap remains, carried forward and narrowed from the previous round's gap 1. Plan 08-08
closed the "out-of-vocabulary risk + no mitigation" sub-case of the CRITICAL-threshold
bypass on `interference.risk`, but the sibling function it deliberately left untouched,
`_check_interference_mitigation_admissibility`, still returns before its judgment point for
*any* unrecognised risk — including one paired with a real, recognised, channel-mismatched
mitigation. That means a spec author can still clear `dsx gate plan` with zero `DSX-INT-*`
findings by misspelling `risk` while declaring an otherwise-real mitigation, which is exactly
the "typo is cheaper than an honest declaration" failure mode this whole finding family
exists to close. The rationale recorded in `08-08-PLAN.md`/`08-08-SUMMARY.md` for leaving
that guard alone — that touching it would cause double-reporting — was tested directly this
round (390-combination sweep) and found to be false: disjointness between `DSX-INT-010` and
`DSX-INT-011` rests entirely on the mitigation-presence dimension, not on risk-vocabulary
membership, so removing the guard's `not in INTERFERENCE_RISKS` clause would not cause any
double-fire. Phase goal clause 1 ("declared interference with no mitigation and no residual
note ... is adjudicated") is therefore not yet fully true — a third, untested path around it
still exists. The `gaps` entry above gives the precise fix and the five items still missing
for a future closure round to verify against, worded to match the shape 08-08/08-09's own
acceptance criteria used, so a next round can reproduce this exact finding rather than
re-derive it.

---

_Verified: 2026-08-13_
_Verifier: Claude (gsd-verifier)_
