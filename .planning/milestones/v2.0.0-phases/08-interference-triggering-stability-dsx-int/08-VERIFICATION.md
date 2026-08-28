---
phase: 08-interference-triggering-stability-dsx-int
verified: 2026-08-14T00:00:00Z
status: passed
score: 6/6 must-haves verified
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: gaps_found
  previous_score: 5/6
  gaps_closed:
    - "A declared interference risk other than none, with no admissible mitigation and no residual note, is blocked at dsx gate plan no matter which INTERFERENCE_* field carries the typo, in every mitigation-declaration state (REQ-P8-01/REQ-P8-02; phase goal clause 1) — closed by plan 08-10. Independently reproduced at both levels: unit level, `interference.check()` on risk=\"shared_buget\" (typo), mitigation=\"geo_split\" (real, recognised, channel-inadmissible), residual_note=\"\" now returns exactly `{'DSX-INT-011'}` at CRITICAL (previously the empty set); gate level, a mutated copy of `examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml` with the same risk/mitigation pair run through `dsx gate plan --json` now exits 1 with `DSX-INT-011`/CRITICAL and `DSX-SPEC-082`/HIGH both present and `DSX-INT-010` absent (previously exit 0, no `DSX-INT-*` finding)."
  gaps_remaining: []
  regressions: []
deferred: []
human_verification: []
---

# Phase 8: Interference, triggering, stability Verification Report

**Phase Goal:** The largest uncovered risk class for a 60%-experiment workload is adjudicated —
declared interference with no mitigation and no residual note, shared-budget and marketplace
patterns treated as distinct risks, triggered-versus-eligible analysis populations with no
dilution adjustment, and unassessed novelty/primacy over the declared stability window.

**Verified:** 2026-08-14
**Status:** passed
**Re-verification:** Yes — after plan 08-10's gap-closure round

## What changed since the last report

The previous verification (`08-VERIFICATION.md`, scored 2026-08-13) found 5/6 truths verified
and one failed truth: an out-of-vocabulary `interference.risk` (e.g. `shared_buget`) paired with
a real, recognised, channel-inadmissible mitigation (e.g. `geo_split`) produced zero
`DSX-INT-*` findings and let `dsx gate plan` exit 0, because
`_check_interference_mitigation_admissibility`'s risk guard (`DSX-INT-011`) still
short-circuited on `normalized_risk not in INTERFERENCE_RISKS` — a clause plan 08-08
deliberately left in place on a "would double-report" rationale the prior verifier's own
390-combination sweep had already falsified.

Plan 08-10 shipped in three atomic commits (`38ba7be` test/RED, `5d95091` fix/GREEN, `243dc11`
test/gate-level proof), dropping the `or normalized_risk not in INTERFERENCE_RISKS` clause from
that guard, keeping only the `normalized_risk == "none"` short-circuit, and relying on the
pre-existing `_RISK_MITIGATION_MAP.get(normalized_risk, frozenset())` fallback to degrade to an
empty admissible set for any risk the map has no cell for — the same shape plan 08-08 already
used for `DSX-INT-010`'s guard. Three prose sites (the admissibility docstring's firing
condition and disjointness paragraphs, its `DecisionRecord.rule` text, and
`_check_interference_unaddressed`'s disjointness paragraph) were corrected to match the new
routing. Two permanent regression tests and two permanent disjointness grids (unit + gate
level) were added.

This round independently reproduced the fix rather than trusting `08-10-SUMMARY.md`'s account
of it — see Behavioral Spot-Checks below for the reproduction commands and raw output.

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | A declared interference risk other than `none`, with no admissible mitigation and no residual note, is blocked at `dsx gate plan` regardless of which `INTERFERENCE_*` field carries the typo, in every mitigation-declaration state (REQ-P8-01/REQ-P8-02; phase goal clause 1) | ✓ VERIFIED | Independently reproduced, not taken on the summary's word. Unit level: `interference.check()` on `_causal_spec(risk="shared_buget", mitigation="geo_split")` (blank residual note) returns exactly `{'DSX-INT-011'}` at `Severity.CRITICAL`, `where=spec.validity_frame.interference.mitigation`, `DSX-INT-010` absent. Gate level: a mutated temp copy of the committed shared-budget fixture with the same pair, run through the real `dsx gate plan --json` CLI, exits `1` with findings `DSX-SPEC-082`/HIGH (`where=...interference.risk`), `DSX-INT-011`/CRITICAL, plus three unrelated non-CRITICAL findings (`DSX-EXP-040`, `DSX-MET-040`, `DSX-PAR-001`) — `DSX-INT-010` absent. Also swept the two adjacent cells: `risk="shared_buget", mitigation="budget_isolation"` (the mitigation that *would* be admissible for the correctly-spelled risk) now fires `DSX-INT-011` too, where it fired nothing before this round; `risk="shared_buget", mitigation="none"` still fires only `DSX-INT-010`, unchanged. |
| 2 | Shared-budget and marketplace interference resolve to distinct declared risks with distinct admissible mitigations — a marketplace-only mitigation applied to a shared-budget risk still exits 1 (REQ-P8-02, phase goal clause 2, roadmap SC2) | ✓ VERIFIED (regression-checked) | `tests.test_frame_interference.TestRiskMitigationMap` (2/2 pass). Independently reproduced: `shared_budget`+`cluster_randomisation` (i.e. `geo_split`-class inadmissible) → `{'DSX-INT-011'}`; `marketplace`+`cluster_randomisation` → `set()`. No regression from plan 08-10's diff — `_RISK_MITIGATION_MAP` itself is untouched. |
| 3 | `DSX-INT-030` blocks eligible-population analysis of an additive metric with no dilution adjustment declared, no matter how `triggering.analysis_population` is spelled (REQ-P8-03, phase goal clause 3, roadmap SC3) | ✓ VERIFIED (regression-checked) | `_check_triggering_dilution` is not in plan 08-10's `files_modified` and its diff (`git diff --stat de1ec9a HEAD -- dsx/frame/interference.py`) touches only the two named helper functions. `tests.test_frame_interference -k analysis_population` (3/3 pass), including the out-of-vocabulary and vocabulary-pin tests. |
| 4 | A ratio metric under triggering is explicitly out of scope — `DSX-INT-030` does not fire on it, and `brief.md` §6.5 carries the corrected per-unit-data entry condition (REQ-P8-04, phase goal clause 4, roadmap SC4) | ✓ VERIFIED (regression-checked) | Not touched by plan 08-10's diff. `tests.test_frame_interference -k ratio_scope` (2/2 pass). REQUIREMENTS.md already records REQ-P8-04 Complete. |
| 5 | An unassessed novelty/primacy effect over the declared stability window is flagged at verify/ship with the assessment method cited, and no `dsx/frame/interference.py` code path reads `inference.paradigm` (REQ-P8-05, REQ-P8-06, phase goal clause 5, roadmap SC5) | ✓ VERIFIED (regression-checked) | Not touched by plan 08-10's diff. `tests.test_frame_interference.TestStabilityAssessment` (11/11 pass), `tests.test_frame_boundary.TestFrameParadigmReadBoundary` (6/6 pass, including the AST/text scan that covers `dsx/frame/interference.py`). REQUIREMENTS.md already records REQ-P8-05 Complete. |
| 6 | `DSX-INT-010` and `DSX-INT-011` never both fire on the same interference sub-block (disjointness invariant), and the invariant holds for the correct reason — the mitigation dimension alone, not risk-vocabulary membership | ✓ VERIFIED | Previously this held only as an accident of the bypass (neither check reached its judgment point for the mismatched cell). Now it holds because both checks correctly and disjointly partition the input on the mitigation dimension. `test_int_010_and_int_011_are_disjoint_across_the_risk_and_mitigation_grid` (unit-level, passes) and `test_int_010_and_int_011_never_both_fire_across_the_gate_level_risk_and_mitigation_grid` (gate-level, passes) both green. Independently reproduced the 8-cell gate-level grid table from `08-10-SUMMARY.md` — matches. |

**Score:** 6/6 truths verified (0 present-behavior-unverified)

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `dsx/frame/interference.py`, `_check_interference_mitigation_admissibility`'s risk guard | Short-circuits on the literal `none` alone, matching `_check_interference_unaddressed`'s guard shape | ✓ VERIFIED | Line 330: `if normalized_risk == "none": return`. The `or normalized_risk not in INTERFERENCE_RISKS` clause is gone — confirmed by grep (`normalized_risk not in INTERFERENCE_RISKS` occurs 0 times in the file). |
| `dsx/frame/interference.py`, three prose sites (docstring firing-condition, docstring disjointness paragraph, `DecisionRecord.rule`) | Restated to match the corrected code | ✓ VERIFIED | Read all three (lines 280–326, 371–388). The `DecisionRecord.rule` text now reads `_RISK_MITIGATION_MAP.get(normalize(risk), frozenset())`, not a direct subscript. The disjointness paragraphs in both `_check_interference_unaddressed` (lines 154–167) and the admissibility function (lines 295–303) both ground disjointness in the mitigation dimension, not risk-vocabulary membership. |
| `tests/test_frame_interference.py`, unit-level regression test `test_out_of_vocabulary_risk_with_real_mitigation_still_fires_int_011` | Fails before the fix, passes after | ✓ VERIFIED | Present at line 162; passes independently under `python3 -m unittest tests.test_frame_interference -k with_real_mitigation`. |
| `tests/test_frame_interference.py`, gate-level regression test `test_out_of_vocabulary_risk_with_real_mitigation_variant_blocks_plan_naming_both_int_011_and_spec_082` | Fails before the fix, passes after | ✓ VERIFIED | Present in `TestInterferenceGateLevel`; passes independently. |
| `tests/test_frame_interference.py`, unit-level disjointness grid `test_int_010_and_int_011_are_disjoint_across_the_risk_and_mitigation_grid` | Executable proof, not a claim | ✓ VERIFIED | Present, passes. |
| `tests/test_frame_interference.py`, gate-level disjointness grid `test_int_010_and_int_011_never_both_fire_across_the_gate_level_risk_and_mitigation_grid` | Executable proof at the shipped path (real CLI, real exit code) | ✓ VERIFIED | Present at line 763, passes. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|-----|-----|--------|---------|
| `_check_interference_mitigation_admissibility` | `_RISK_MITIGATION_MAP` | `.get(normalized_risk, frozenset())` fallback | ✓ WIRED | Confirmed the fallback (not a direct subscript) is what makes dropping the vocabulary clause safe — an unrecognised risk degrades to an empty admissible set, so any recognised mitigation is unconditionally inadmissible for it. |
| `_check_interference_unaddressed` | `_check_interference_mitigation_admissibility` | Disjointness by construction | ✓ WIRED (upgraded from ⚠️ PARTIAL) | Previously scored PARTIAL because the mismatched cell reached neither check's judgment point. Now both checks reach their judgment point for every non-`none` risk, and the mitigation-presence dimension alone determines which one fires — verified by both disjointness grids. |
| `dsx/spec.py`'s `DSX-SPEC-082` | `DSX-INT-011` | Two independent findings about two different facts, from structured `--json` | ✓ WIRED | Reproduced directly: both codes present simultaneously in the same `--json` finding list on the same mutated fixture, `DSX-SPEC-082` at `where=...interference.risk`, `DSX-INT-011` at `where=...interference.mitigation`. |
| Gate-level tests | `_gate_findings` helper | Structured JSON assertions, not rendered text | ✓ WIRED | Both new tests (unit + gate) and the pre-existing WR-01-hardened tests read parsed `--json` finding lists, never substring-match rendered report text. |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Full test suite | `python3 -m unittest discover -s tests -q` | `Ran 540 tests ... OK (skipped=2)` | ✓ PASS |
| Project check script | `sh scripts/check.sh` | `all checks passed` | ✓ PASS |
| Unit-level bypass reproduction | `interference.check()` on `risk="shared_buget", mitigation="geo_split", residual_note=""` (built independently, not via the test factory) | `['DSX-INT-011']` (previously `[]`) | ✓ PASS (confirms gap closed) |
| Gate-level bypass reproduction | Live `dsx gate plan --json` via `cli.main(...)` on a temp-mutated copy of the committed shared-budget fixture | `exit 1`; findings include `DSX-SPEC-082`/HIGH, `DSX-INT-011`/CRITICAL, `DSX-EXP-040`/MEDIUM, `DSX-MET-040`/HIGH, `DSX-PAR-001`/INFO; `DSX-INT-010` absent | ✓ PASS (confirms gap closed; matches `08-10-SUMMARY.md`'s recorded table exactly) |
| Adjacent-cell sweep | `risk="shared_buget", mitigation="budget_isolation"` (the mitigation admissible for the *correctly-spelled* risk) | `['DSX-INT-011']` (previously `[]`) | ✓ PASS |
| No-regression cell | `risk="shared_budget", mitigation="budget_isolation"` (correct spelling, admissible mitigation) | `[]` | ✓ PASS |
| No-regression cell | `risk="none", mitigation="geo_split"` | `[]` | ✓ PASS |
| Fail-closed on non-string risk | `risk=3, mitigation="geo_split"` | `['DSX-INT-011']`, no exception raised | ✓ PASS |
| New regression tests (both) | `python3 -m unittest tests.test_frame_interference -k with_real_mitigation` | 2/2 pass | ✓ PASS |
| Unit disjointness grid | `python3 -m unittest tests.test_frame_interference -k disjoint` | 3/3 pass | ✓ PASS |
| Gate-level `TestInterferenceGateLevel` (whole class) | `python3 -m unittest tests.test_frame_interference.TestInterferenceGateLevel -v` | 7/7 pass | ✓ PASS |
| Truth 2 regression | `python3 -m unittest tests.test_frame_interference.TestRiskMitigationMap -v` | 2/2 pass | ✓ PASS |
| Truth 3 regression | `python3 -m unittest tests.test_frame_interference -k analysis_population -v` | 3/3 pass | ✓ PASS |
| Truth 4 regression | `python3 -m unittest tests.test_frame_interference -k ratio_scope -v` | 2/2 pass | ✓ PASS |
| Truth 5 regression | `python3 -m unittest tests.test_frame_interference.TestStabilityAssessment -v` | 11/11 pass | ✓ PASS |
| Truth 5/REQ-P8-06 regression | `python3 -m unittest tests.test_frame_boundary.TestFrameParadigmReadBoundary -v` | 6/6 pass | ✓ PASS |
| Known-bad corpus | `python3 -m unittest tests.test_known_bad_corpus -v` | 22/22 pass | ✓ PASS |
| Committed fixture untouched | `git status --short examples/ templates/` and all `08-0*-PLAN.md`/`08-0*-SUMMARY.md` | empty | ✓ PASS |
| Finding catalogue | `python3 scripts/gen-finding-catalogue.py --check` (via `scripts/check.sh`) | `finding catalogue is current` | ✓ PASS |

### DSX Verification Stance Note

Phase 8 is not an analytical phase — its own `<phase_note>` and `08-10-PLAN.md`'s
`<phase_note>` both confirm no `ANALYSIS-SPEC.yaml` exists for this phase, and the
orchestrator's `plan:post` gate check already confirmed this. The phase builds the gate tool
itself (`dsx/frame/interference.py`) rather than producing an analysis for the gate to check.
`dsx gate verify --phase-dir ... --report .../DATA-REVIEW.md` therefore has no applicable
target — there is no phase-owned `ANALYSIS-SPEC.yaml`/`DATA-REVIEW.md` to run it against. The
equivalent audit for a tooling phase is the deterministic test suite plus `scripts/check.sh`
plus the known-bad corpus, all of which are reproduced above.

### Requirements Coverage

| Requirement | Source Plan(s) | Description | Status | Evidence |
|-------------|-----------------|--------------|--------|----------|
| REQ-P8-01 | 08-03, 08-07, 08-08, 08-10 | A declared interference risk other than `none` without a mitigation or residual note is blocked | ✓ SATISFIED | The prior round's surviving bypass (typo'd risk + real mitigation) is closed and independently reproduced. REQUIREMENTS.md still shows this Pending — single-writer file, orchestrator's to update after this verification. |
| REQ-P8-02 | 08-03, 08-07, 08-08, 08-10 | Shared-budget and marketplace treated as distinct risks with distinct admissible mitigations | ✓ SATISFIED | Distinctness map (truth 2) plus the risk-declaration side now adjudicated for every mitigation-declaration state (truth 1). REQUIREMENTS.md still shows this Pending — orchestrator's to update. |
| REQ-P8-03 | 08-01, 08-02, 08-04, 08-09 | `DSX-INT-030` blocks eligible-population analysis of additive metrics with no dilution adjustment | ✓ SATISFIED | Closed in the prior round, regression-checked clean this round. REQUIREMENTS.md still shows this Pending — orchestrator's to update. |
| REQ-P8-04 | 08-01, 08-04, 08-06 | Ratio-metric dilution explicitly out of scope, entry condition corrected | ✓ SATISFIED | Unchanged; REQUIREMENTS.md already shows Complete. |
| REQ-P8-05 | 08-02, 08-05, 08-06 | Unassessed novelty/primacy flagged with cited method | ✓ SATISFIED | Unchanged; REQUIREMENTS.md already shows Complete. |
| REQ-P8-06 | 08-03 | No `DSX-INT-*` check reads `inference.paradigm` | ✓ SATISFIED | `TestFrameParadigmReadBoundary` 6/6 pass, scan includes `dsx/frame/interference.py` as modified by this round. REQUIREMENTS.md still shows this Pending — orchestrator's to update. |

No orphaned requirements — all six IDs (`REQ-P8-01` through `REQ-P8-06`) are claimed by at
least one plan's `requirements` frontmatter field (cross-checked across all ten plan files,
08-01 through 08-10) and cross-reference cleanly against `.planning/REQUIREMENTS.md` lines
108–113. `.planning/REQUIREMENTS.md`'s status table (lines 204–209) has not yet been updated to
reflect this round's closure of REQ-P8-01, REQ-P8-02 and REQ-P8-06 — that file is
single-writer and owned by the orchestrator, not by this verifier or by plan 08-10's executor,
consistent with the project's parallel-subagent working agreement. This is a tracking-sync
item for the orchestrator, not a gap in the underlying code.

### Anti-Patterns Found

None blocking. Both files touched by plan 08-10 (`dsx/frame/interference.py`,
`tests/test_frame_interference.py`) were scanned for debt markers (`TBD`, `FIXME`, `XXX`,
`TODO`, `HACK`, `PLACEHOLDER`) — zero matches. No stub returns, no hardcoded-empty data
reaching a gate decision, no console-log-only implementations.

`08-REVIEW.md` (this round's code review) recorded two WARNING-level and one INFO-level
finding, none of which the reviewer classified as blocking and none of which this verifier's
independent read disputes:

- **WR-01** — `DSX-INT-011`'s remedy text for an out-of-vocabulary risk reads
  `Declare a mitigation admissible for 'shared_buget': (none admissible).` — self-contradictory
  wording (the empty admissible set makes the instruction impossible to follow), but
  operator-facing message text, explicitly out of this gap-closure plan's scope per its own
  prohibitions (`08-10-PLAN.md`: "No finding detail, remedy, title or where string is
  reworded"). Does not affect the fire/no-fire decision or the gate exit code — `DSX-SPEC-082`
  fires alongside it and names the real fix (correct the spelling).
- **WR-02** — `dsx/frame/paradigm.py:219`, `design.alpha: 0` silently replaced by the 0.05
  default via Python's `or` truthiness. Outside `dsx/frame/interference.py` entirely — not
  touched by this phase's diff, and only affects a reference-value display string in a
  different finding family (`DSX-PAR-010`), not this phase's fire/no-fire logic.
- **IN-01** — inconsistent empty-collection default style (`()` vs `frozenset()`) between two
  `_RISK_MITIGATION_MAP.get()` call sites. Style nit; both iterate identically via `sorted()`.

Both WARNINGs are real, correctly-scoped-out deferrals rather than defects hidden from this
report; neither blocks the phase goal, and neither is inside this phase's requirement set.

### Gaps Summary

None. The one gap carried forward from the prior verification round — an out-of-vocabulary
`interference.risk` paired with a real, recognised, channel-inadmissible mitigation bypassing
`DSX-INT-011` and clearing `dsx gate plan` with exit 0 — is closed. Independently reproduced at
both unit and gate level, against the actual code as it stands in the working tree (not against
`08-10-SUMMARY.md`'s claims). All five previously-VERIFIED truths were regression-checked and
none moved. The full test suite (540 tests), `scripts/check.sh`, and the known-bad corpus
(22 tests) all pass. No committed fixture, no prior plan file, and no prior summary was
modified by this round's diff (`git status --short` empty across all of them). The phase goal —
"the largest uncovered risk class for a 60%-experiment workload is adjudicated" — is now
observably true across every path this phase's own investigation surfaced, including the
out-of-vocabulary-risk-plus-real-mitigation bypass that took three rounds (plan 08-08, the
code review, and plan 08-10) to fully close.

The only open item is administrative: `.planning/REQUIREMENTS.md`'s status table still shows
REQ-P8-01, REQ-P8-02 and REQ-P8-06 as `Pending`. That file is single-writer and owned by the
orchestrator per this project's working agreements — the orchestrator should update those three
rows to `Complete` following this verification.

---

_Verified: 2026-08-14_
_Verifier: Claude (gsd-verifier)_
