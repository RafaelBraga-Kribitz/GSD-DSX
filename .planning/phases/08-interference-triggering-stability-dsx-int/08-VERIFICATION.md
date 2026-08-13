---
phase: 08-interference-triggering-stability-dsx-int
verified: 2026-08-13T00:00:00Z
status: gaps_found
score: 5/7 must-haves verified
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: gaps_found
  previous_score: 5/7
  gaps_closed:
    - "An out-of-vocabulary interference.mitigation value (e.g. buget_isolation) no longer bypasses DSX-INT-010/DSX-INT-011 — closed by plan 08-07."
  gaps_remaining:
    - "An out-of-vocabulary interference.risk value (e.g. shared_buget) still bypasses DSX-INT-010 and DSX-INT-011 entirely — same failure class, adjacent field, never fixed."
  regressions: []
  new_gaps_found_this_round:
    - "An out-of-vocabulary triggering.analysis_population value (e.g. eligable) bypasses DSX-INT-030 — pre-existing since plan 08-04, not caught by the original verification, found by the post-fix deep review."
gaps:
  - truth: "A declared interference risk other than none, with no admissible mitigation and no residual note, is blocked at dsx gate plan no matter which INTERFERENCE_* field carries the typo (REQ-P8-01/REQ-P8-02; phase goal clause 1)."
    status: failed
    reason: >
      Plan 08-07 fixed exactly one of the two identically-shaped guards in
      _check_interference_unaddressed. The mitigation guard now treats an
      out-of-vocabulary string as absent (verified: mutating
      examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml line 145 from
      `mitigation: none` to `mitigation: buget_isolation` makes `dsx gate plan` exit 1,
      naming DSX-INT-010/CRITICAL and DSX-SPEC-082/HIGH together). But the risk guard,
      twelve lines above the fixed one in the same function
      (dsx/frame/interference.py:178), was not touched. Reproduced independently against
      the committed tree: mutating the same fixture's line 137 from `risk: shared_budget`
      to `risk: shared_buget` (mitigation left at `none`, residual_note left blank) makes
      `dsx gate plan` exit 0 — only DSX-SPEC-082/HIGH and DSX-MET-040/HIGH fire, both
      below the CRITICAL plan threshold. This is the exact bypass 08-07 closed for
      `mitigation`, unpatched on `risk`. git log confirms this guard predates 08-07
      (introduced in feat(08-03), commit d9fdae7) — it is a pre-existing defect the
      post-fix deep review found by re-checking the module, not a regression the fix
      introduced. Documented as CR-01 in the current 08-REVIEW.md (the re-review round).
    artifacts:
      - path: "dsx/frame/interference.py"
        issue: "Line 178, in _check_interference_unaddressed: `if normalized_risk == \"none\" or normalized_risk not in INTERFERENCE_RISKS: return` treats any out-of-vocabulary interference.risk string identically to the honestly-declared none case, exempting a misspelled-but-declared risk from adjudication. The mirrored guard in _check_interference_mitigation_admissibility (line 296) has the same shape and is correctly left alone — it has no admissibility cell for an unrecognised risk."
    missing:
      - "Apply the same vocabulary-membership-as-declaration treatment already used for mitigation to the risk guard: only normalized_risk == \"none\" should short-circuit the judgment; an out-of-vocabulary, non-blank risk string should fall through, with _RISK_MITIGATION_MAP.get(normalized_risk, ()) naturally degrading to no admissible mitigations for it."
      - "Add a unit-level regression test asserting DSX-INT-010 fires for a spec with risk=\"shared_buget\" (out-of-vocabulary), mitigation: none, and a blank residual_note."
      - "Add a gate-level regression test mutating interference.risk on the committed shared-budget fixture to an out-of-vocabulary near-miss and asserting dsx gate plan exits 1, naming both DSX-INT-010 and DSX-SPEC-082."
      - "Confirm via git diff, as an acceptance criterion, that _check_interference_mitigation_admissibility's risk guard (line 296) is unchanged by the fix, preserving DSX-INT-010/DSX-INT-011 disjointness for the out-of-vocabulary-risk case the same way it is preserved for the out-of-vocabulary-mitigation case."
  - truth: "DSX-INT-030 blocks eligible-population analysis of an additive metric with no dilution adjustment declared, no matter how triggering.analysis_population is spelled (REQ-P8-03; phase goal clause 3)."
    status: failed
    reason: >
      _check_triggering_dilution (dsx/frame/interference.py:408) only enters its judgment
      branch when `normalized_population` is the exact string "eligible"; any other value
      — including a one-character misspelling — returns before DSX-INT-030 can fire.
      Reproduced independently against the committed tree: mutating
      examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml line 150 from
      `analysis_population: eligible` to `analysis_population: eligable` makes
      `dsx gate plan` exit 0 (only DSX-SPEC-082/HIGH and DSX-MET-040/HIGH fire). The
      unmutated fixture correctly exits 1 naming DSX-INT-030/CRITICAL. git log confirms
      this guard predates plan 08-07 (introduced in feat(08-04), commit 36ff448); 08-07
      touched the same function only to fix the metric-type derivation (WR-03), not this
      guard. This is a pre-existing defect the deep review found while re-checking the
      module the fix touched, not a regression from the fix itself. The formula
      infrastructure this truth also covers (dsx.mathx.diluted_effect, the
      delta_diluted = delta_triggered x trigger_rate identity, the ratio-metric scope
      boundary) is unaffected and still verified — see truth 4 below and the spot-checks
      table. Documented as CR-02 in the current 08-REVIEW.md.
    artifacts:
      - path: "dsx/frame/interference.py"
        issue: "Line 408, in _check_triggering_dilution: `if normalized_population != \"eligible\": return` treats any out-of-vocabulary triggering.analysis_population string identically to an honestly-declared triggered population, silently exempting a misspelled eligible declaration from the dilution check."
    missing:
      - "Distinguish an honestly-declared triggered population (and a genuinely absent/blank value) from an out-of-vocabulary string in the population guard, so a misspelling of eligible is adjudicated rather than silently skipped, mirroring the fix already applied to the mitigation field."
      - "Add a unit-level regression test asserting DSX-INT-030 fires for analysis_population=\"eligable\" with an otherwise-firing additive metric and dilution_adjusted: false."
      - "Add a gate-level regression test mutating triggering.analysis_population on the committed triggering-dilution fixture to an out-of-vocabulary near-miss and asserting dsx gate plan exits 1."
      - "Update the docstring's stated firing condition and the DecisionRecord.rule text, both of which currently describe the condition as the value 'is eligible', so the decision trail matches the corrected code."
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
**Re-verification:** Yes — after 08-07 gap closure

## What changed since the last report

Plan 08-07 closed the one gap the previous verification found: an out-of-vocabulary
`interference.mitigation` value (a misspelling such as `buget_isolation` for
`budget_isolation`) no longer clears `dsx gate plan` for a declared, unmitigated
interference risk. I reproduced that fix independently and it holds.

But the fix was narrow. `dsx/frame/interference.py` has the identical guard shape — "if this
declared value is not a recognised vocabulary member, treat the whole judgment as
not-applicable" — on two other fields in the same module: `interference.risk` and
`triggering.analysis_population`. Neither was touched by plan 08-07, and both bypass a
CRITICAL-severity gate check with a one-character misspelling, exactly the way `mitigation`
did before the fix. I reproduced both independently against the committed tree (commands and
output below). Git history shows both guards predate plan 08-07 — they are pre-existing
defects the deep code review surfaced while re-checking the module the fix touched, not
regressions the fix introduced.

Net effect: the phase goal's first clause ("declared interference with no mitigation and no
residual note") and third clause ("triggered-versus-eligible analysis populations with no
dilution adjustment") are each still defeatable by a typo on the committed corpus, so I am
scoring both as not yet achieved.

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | A declared interference risk with no mitigation and no residual note is blocked at `dsx gate plan`, citing SUTVA, regardless of which field carries a typo (REQ-P8-01) | ✗ FAILED | Mitigation-field bypass closed by 08-07 (verified). Risk-field bypass still open: mutating `risk: shared_budget` to `risk: shared_buget` on the committed fixture makes the gate exit 0 with no `DSX-INT-*` finding at all. See Gaps. |
| 2 | Shared-budget and marketplace interference are distinct risks with distinct admissible mitigations (REQ-P8-02) | ✓ VERIFIED | Re-confirmed independently: `shared_budget` + `cluster_randomisation` → `DSX-INT-011`/CRITICAL, exit 1. `marketplace` + `cluster_randomisation` → no `DSX-INT-*` finding, exit 0. No collateral change from 08-07's edits to the same module. |
| 3 | `DSX-INT-030` blocks eligible-population analysis of an additive metric with no dilution adjustment, no matter how the population field is spelled, and a test asserts `delta_diluted = delta_triggered × trigger_rate` against the Deng & Hu (2015) counterexample (REQ-P8-03) | ✗ FAILED | The formula and its test are correct and re-confirmed green (`tests.test_dsx -k dilut`, 5/5 pass). But the population-field bypass (see Gaps) means the check that is supposed to fire when a real dilution problem is declared can be silenced by a one-character misspelling of `eligible`, defeating the operational guarantee this truth asserts. |
| 4 | Ratio-metric dilution is explicitly out of scope, with a falsifiable entry condition, not the paper's availability (REQ-P8-04) | ✓ VERIFIED | Re-confirmed: `test_ratio_scope_boundary_ratio_metric_produces_no_finding` and `test_ratio_scope_boundary_rate_metric_produces_no_finding` both pass. `brief.md` §6.5's corrected entry-condition row is unaffected by 08-07 (that plan did not touch `brief.md`). |
| 5 | An unassessed novelty/primacy effect over the declared stability window is flagged at verify/ship (HIGH), not plan, with the assessment method cited (REQ-P8-05) | ✓ VERIFIED | Re-confirmed with a fresh mutation of `examples/good-ANALYSIS-SPEC.yaml` (`novelty_primacy_assessed: false`): `dsx gate plan` exits 0, `dsx gate verify` exits 1 naming `DSX-INT-040`. `dsx/frame/interference.py`'s stability check was not touched by 08-07. |
| 6 | No `DSX-INT-*` check reads `inference.paradigm` (REQ-P8-06) | ✓ VERIFIED | Re-ran `tests/test_frame_boundary.py::TestFrameParadigmReadBoundary` (8 tests) — all pass, including the interference-module-specific test, after 08-07's edits. |
| 7 | The known-bad corpus's structural guarantees (per-fixture target-defect map) hold after 08-07's additions | ✓ VERIFIED | `python3 -m unittest tests.test_frame_interference tests.test_known_bad_corpus` — 77 tests, all pass, including the two new corpus guards 08-07 added (`test_weak_identification_mmm_fixture_blocks_verify_and_ship_naming_int_030`, `test_target_defect_codes_keys_are_a_subset_of_the_corpus_on_disk`). |

**Score:** 5/7 truths verified. Truths 1 and 3 both fail on the same defect class — a
declared-but-misspelled vocabulary value silently exempting the spec from a CRITICAL-severity
check — now on the `risk` and `analysis_population` fields respectively, after 08-07 closed it
on `mitigation`.

### Reproductions run for this re-verification (real command output)

```
=== BASELINE interference-shared-budget (unmutated) ===
exit: 1   DSX-INT-010 in output: True

=== MITIGATION TYPO (buget_isolation), residual_note blank ===
exit: 1   DSX-INT-010 in output: True   DSX-SPEC-082 in output: True   <- 08-07 fix confirmed working

=== RISK TYPO (shared_buget), mitigation: none, residual_note blank ===
exit: 0   Any DSX-INT-* in output: False   DSX-SPEC-082 in output: True   <- still open

=== BASELINE triggering-dilution (unmutated) ===
exit: 1   DSX-INT-030 in output: True

=== ANALYSIS_POPULATION TYPO (eligable) ===
exit: 0   DSX-INT-030 in output: False   <- still open

=== marketplace + cluster_randomisation ===
exit: 0   DSX-INT-011 in output: False   (unchanged from prior verification — no regression)

=== shared_budget + cluster_randomisation ===
exit: 1   DSX-INT-011 in output: True   DSX-INT-010 in output: False   (unchanged — no regression)

=== novelty_primacy_assessed:false, gate plan ===
exit: 0   DSX-INT-040 in output: True   (HIGH, non-blocking at plan — unchanged)

=== novelty_primacy_assessed:false, gate verify ===
exit: 1   DSX-INT-040 in output: True   (unchanged)
```

```
$ python3 -m unittest discover -s tests
Ran 531 tests in 6.301s
OK (skipped=2)

$ sh scripts/check.sh
...
all checks passed
```

### Regression check on git history (are the new bypasses 08-07 regressions?)

```
$ git log --oneline --all -- dsx/frame/interference.py | tail -6
d9fdae7 feat(08-03): ship DSX-INT-010/011 and the interference gate module
36ff448 feat(08-04): ship DSX-INT-030 with the additive metric partition
fd6ea0e feat(08-05): ship DSX-INT-040 with the disjointness statement against DSX-EXP-030
e174a52 fix(08-05): harden the finished four-code module against malformed sub-block shapes
f669607 fix(08-07): treat an unrecognised interference.mitigation as absent for DSX-INT-010
7c5cfec fix(08-07): close WR-02, WR-03 and IN-02; record IN-01 as deferred
```

The `risk` guard (line 178) traces to `feat(08-03)` (commit `d9fdae7`), five commits before
08-07. The `analysis_population` guard (line 408) traces to `feat(08-04)` (commit `36ff448`),
also before 08-07. **Both bypasses are pre-existing defects that 08-07 did not introduce.**
08-07 fixed the `mitigation` field's copy of this same guard shape and, in the same commit,
fixed an unrelated metric-type derivation in the same function that surrounds the
`analysis_population` guard — which is what put a reviewer's eyes back on that function and
surfaced the adjacent, untouched defect. The original 08-VERIFICATION.md did not catch either
bypass because its reproduction of CR-01 tested the `mitigation` field specifically, not every
field sharing the same vocabulary-membership guard pattern.

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `dsx/frame/interference.py` | Vocabulary-membership-as-absence applied consistently across `risk`, `mitigation`, `analysis_population` | ⚠️ PARTIAL | Applied to `mitigation` only (08-07). `risk` (line 178) and `analysis_population` (line 408) still use the pre-existing "out-of-vocabulary is not-applicable" shape. |
| `tests/test_frame_interference.py` | Regression tests for every out-of-vocabulary bypass class | ⚠️ PARTIAL | 3 new tests from 08-07 cover the `mitigation` bypass and the null-metric-type decision-trail gap. No test exists for the `risk` or `analysis_population` out-of-vocabulary bypasses. |
| `tests/test_known_bad_corpus.py` | Positive gate-level guarantees for DSX-INT-030 verify/ship, on-disk map guard | ✓ VERIFIED | Both new tests present and pass (77/77 in the two interference-related test modules). |
| `tests/test_dsx.py` | Non-tautological dilution scope-boundary test | ✓ VERIFIED | Rewritten test asserts the real partition constants and the docstring's published reference pair; confirmed it can fail (turns red when `ratio` is added to the additive partition, per 08-REVIEW.md's own mutation check). |
| `examples/bad-ANALYSIS-SPEC.yaml` | DSX-INT-010 attribution comment | ✓ VERIFIED | `DSX-INT-010` string present in the file; `dsx gate plan` still exits 1 naming it. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|-----|-----|--------|---------|
| `_check_interference_unaddressed` (mitigation branch) | `dsx.spec.INTERFERENCE_MITIGATIONS` | vocabulary-membership term | ✓ WIRED | Confirmed by direct reproduction — out-of-vocabulary mitigation now fires DSX-INT-010. |
| `_check_interference_unaddressed` (risk branch) | `dsx.spec.INTERFERENCE_RISKS` | vocabulary-membership term | ✗ NOT_WIRED | The risk branch still short-circuits on out-of-vocabulary membership instead of adjudicating it. |
| `_check_triggering_dilution` (population branch) | `dsx.spec.ANALYSIS_POPULATIONS` (implicit two-member vocabulary: `eligible`/`triggered`) | vocabulary-membership term | ✗ NOT_WIRED | The population branch treats any string other than the literal `"eligible"` as equivalent to `"triggered"`, including out-of-vocabulary values, so DSX-INT-030 never adjudicates a misspelled `eligible`. |
| `_check_interference_unaddressed` | `_check_interference_mitigation_admissibility` | disjointness (never both fire) | ✓ WIRED | Still holds for all tested input classes, including the out-of-vocabulary-mitigation case, confirmed by direct reproduction (mitigation typo fires DSX-INT-010 only, not DSX-INT-011). |
| `_RISK_MITIGATION_MAP` | `dsx.spec.INTERFERENCE_RISKS` | key-set equality | ✓ WIRED | Re-confirmed via direct CLI reproduction: shared_budget+cluster_randomisation and marketplace+cluster_randomisation resolve to distinct, correct outcomes. |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Mitigation-typo bypass is closed | `dsx gate plan` on shared-budget fixture with `mitigation: buget_isolation` | exit 1, DSX-INT-010 + DSX-SPEC-082 | ✓ PASS |
| Risk-typo bypass is still open | `dsx gate plan` on shared-budget fixture with `risk: shared_buget` | exit 0, no DSX-INT-* | ✗ FAIL (gap) |
| Population-typo bypass is still open | `dsx gate plan` on triggering-dilution fixture with `analysis_population: eligable` | exit 0, no DSX-INT-030 | ✗ FAIL (gap) |
| Shared-budget/marketplace distinctness unaffected | `dsx gate plan` on shared_budget vs marketplace + cluster_randomisation | exit 1 vs exit 0 respectively | ✓ PASS |
| Novelty/primacy severity split unaffected | `dsx gate plan` vs `dsx gate verify` on unassessed novelty/primacy | exit 0 vs exit 1, DSX-INT-040 at verify only | ✓ PASS |
| Full suite green | `python3 -m unittest discover -s tests` | 531 tests, OK (skipped=2) | ✓ PASS |
| Project check script green | `sh scripts/check.sh` | all checks passed | ✓ PASS |

### Requirements Coverage

| Requirement | Source Plan(s) | Description | Status | Evidence |
|---|---|---|---|---|
| REQ-P8-01 | 08-03, 08-07 | Declared interference risk with no mitigation/residual note is blocked | ✗ BLOCKED | Mitigation-field bypass closed; risk-field bypass open (typo defeats the CRITICAL gate). |
| REQ-P8-02 | 08-03, 08-07 | Shared-budget and marketplace are distinct risks with distinct admissible mitigations | ✓ SATISFIED | Distinctness itself re-confirmed unaffected; note this requirement shares plan 08-07 with REQ-P8-01 but the risk-field bypass is a different sub-claim (typo tolerance, not risk/mitigation mapping). |
| REQ-P8-03 | 08-01, 08-02, 08-04 | DSX-INT-030 blocks eligible-population analysis of additive metric with no dilution adjustment | ✗ BLOCKED | Dilution formula and ratio-scope boundary correct; the population-field typo bypass defeats the check's operational guarantee. |
| REQ-P8-04 | 08-01, 08-04, 08-06 | Ratio-metric dilution explicitly out of scope with falsifiable entry condition | ✓ SATISFIED | Re-confirmed, unaffected by 08-07. |
| REQ-P8-05 | 08-02, 08-05, 08-06 | Unassessed novelty/primacy flagged at verify/ship, not plan, with method cited | ✓ SATISFIED | Re-confirmed, unaffected by 08-07. |
| REQ-P8-06 | 08-03 | No DSX-INT-* check reads inference.paradigm | ✓ SATISFIED | Re-confirmed, unaffected by 08-07. |

No orphaned requirements — all six REQ-P8 IDs are claimed by at least one plan in the phase
(`08-01` through `08-07`), matching `.planning/REQUIREMENTS.md`.

Note: the `REQ-P8-*` checkboxes in `.planning/REQUIREMENTS.md` remain unchecked
(`Pending`/`Complete` mix in the tracking table). Per this project's standing convention
(noted in the prior verification and confirmed unchanged here), that file is single-writer
and checkbox state is updated at a later milestone step, not at phase-verification time. Not
scored as a gap, and not edited by this report.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `dsx/frame/interference.py` | 178, 296 | Vocabulary-membership guard drops out-of-vocabulary risk values instead of adjudicating them | Blocker (scored as gap above) | Same class as the fixed mitigation bypass |
| `dsx/frame/interference.py` | 408 | Vocabulary-membership guard drops out-of-vocabulary analysis_population values instead of adjudicating them | Blocker (scored as gap above) | Same class as the fixed mitigation bypass |
| `tests/test_frame_interference.py` | ~491 | Gate-level test asserting `DSX-SPEC-082 in (out+err)` via text substring, while the same commit added the literal string `DSX-SPEC-082` to `DSX-INT-010`'s own `detail` text — the assertion is satisfied by prose regardless of whether DSX-SPEC-082 actually fired | Warning | Not a functional bypass — I independently confirmed via structured reproduction (above) that DSX-SPEC-082 genuinely does fire on the mutated input and genuinely does not fire on the unmutated baseline, so the underlying claim this weak test was meant to pin is true. But the test itself cannot currently catch a regression in that specific claim. Documented as WR-01 in 08-REVIEW.md; not independently re-scored as a phase-blocking gap here because the claim it should protect is otherwise verified, but it should be tightened in the same closure round as CR-01/CR-02 above. |
| `dsx/frame/interference.py` | 420 | `dilution_adjusted is not True` / `novelty_primacy_assessed is not True` identity comparisons fail closed on a quoted-string YAML boolean (e.g. `"true"`) | Info | Pre-existing, codebase-wide convention; deliberately deferred in 08-07 (IN-01) with documented rationale (fails by over-firing, never by silently passing) — not re-litigated here. |

No `TBD`/`FIXME`/`XXX` debt markers found in the files this phase modified beyond fixture
content that is itself deliberately testing placeholder detection (`examples/bad-ANALYSIS-SPEC.yaml`'s `owner: "TBD"` is a defect the file is designed to encode, not an implementation debt marker).

### Human Verification Required

None. All truths in this report were resolved by direct, reproducible command output.

### Gaps Summary

Two gaps, both instances of the same defect class the previous verification round found and
plan 08-07 partially closed: a value declared in a closed vocabulary field, but misspelled,
is treated as equivalent to "nothing declared" rather than "declared, but not a recognised
member" — which lets a typo clear a CRITICAL-threshold gate that an honest, correctly-spelled
declaration would not. Plan 08-07 fixed this for `interference.mitigation`. It remains open on
`interference.risk` (same function, twelve lines away, blocking REQ-P8-01/REQ-P8-02 and phase
goal clause 1) and on `triggering.analysis_population` (a different function the plan also
edited for an unrelated reason, blocking REQ-P8-03 and phase goal clause 3).

Both are pre-existing defects (traced via `git log` to commits `d9fdae7` and `36ff448`,
predating plan 08-07), not regressions the gap-closure plan introduced. The next gap-closure
round can apply the same fix shape 08-07 already used for `mitigation` to both remaining
fields, plus tighten the weak `DSX-SPEC-082` text-substring assertion (WR-01) noted above.

Truths 2, 4, 5, 6 and 7 — the risk/mitigation distinctness map, the ratio-metric scope
boundary, the novelty/primacy severity split, the paradigm-read boundary, and the corpus
restructure's guards — were all re-confirmed independently after 08-07's edits and show no
collateral damage.

---

_Verified: 2026-08-13_
_Verifier: Claude (gsd-verifier)_
