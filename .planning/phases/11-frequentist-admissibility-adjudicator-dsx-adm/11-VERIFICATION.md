---
phase: 11-frequentist-admissibility-adjudicator-dsx-adm
verified: 2026-08-22T00:00:00Z
status: human_needed
score: 5/5 must-haves verified
behavior_unverified: 0
overrides_applied: 0
human_verification:
  - test: "Read each of families.yaml's 14 family entries' `citation:` string against its real source (T-11-13/T-11-14)."
    expected: "The cited work exists, actually supports the named estimator family, and `locator_status` (verified/unverified) matches whether the specific locator (chapter/section/page) was actually confirmed."
    why_human: "No parser can confirm a citation string names a real, correctly-quoted source that supports the claim attached to it — this is the D-05 judgement automated tests cannot make. Explicitly noted as still-open by 11-04-SUMMARY.md ('has not yet been performed and remains open before the phase closes') and by 11-VALIDATION.md's Manual-Only Verifications table (unchecked)."
  - test: "Read each `DSX-ADM-010` finding's rendered message against its cited ranking rule's source and confirm the wording does not overstate the ordering's strength (e.g. the CV3-over-CV1 cluster-robust ordering is worded as a hedged reliability preference, never a domination)."
    expected: "Uniform-domination language (Boschloo-over-Fisher) is used only where the source states a uniform result; hedged/default-preference orderings (Welch-over-Student, CV3-over-CV1, interacted-over-unadjusted) are worded as preferences, not dominations."
    why_human: "Only a reader can tell a uniform domination from a hedged reliability ordering apart in prose; a test can assert the `strength` field is one of the three enum values, not that the rendered sentence honestly reflects the source at that strength (11-VALIDATION.md Manual-Only Verifications table, still unchecked)."
  - test: "Read the corrected `proportion | 2 | no` row and its Boschloo/Lydersen footnote in `references/test-selection.md` and confirm it reads correctly to a practitioner and states the Lydersen section-9 locator at the strength the source supports."
    expected: "The row no longer prescribes Fisher's exact as the small-cell fallback and the citation reads as an accurate, non-overstated summary."
    why_human: "11-01-PLAN.md Task 2's own `<human-check>` requires this; 11-01-SUMMARY.md records `human_judgment: true` for this item without recording that the read was performed."
  - test: "Read the two D-29 locators folded into `brief.md` section 7 (Kohavi, Tang & Xu Chapter 22; Cameron & Miller Section VI) against their sources and confirm each is stated at the strength the evidence supports, including the Cameron & Miller Section VIII-to-XI typeset-numbering caveat."
    expected: "The Kohavi locator reads as verified; the Cameron & Miller locator reads as manuscript-verified with the numbering caveat intact and unambiguous."
    why_human: "11-01-PLAN.md Task 3's own `<human-check>` requires this; 11-01-SUMMARY.md records `human_judgment: true` without recording that the read was performed."
---

# Phase 11: Frequentist admissibility adjudicator (`DSX-ADM-*`) Verification Report

**Phase Goal:** Given a coherent frame, the tool names which frequentist procedures are admissible and what each one costs in assumptions — and refuses rather than guesses when the frame is underdetermined.
**Verified:** 2026-08-22
**Status:** human_needed
**Re-verification:** No — initial verification

## Summary

All five ROADMAP success criteria and every specifically-requested acceptance check were re-run directly against the live tree — not taken from any SUMMARY.md claim — and all passed. The full test suite (1,014 tests), the known-bad corpus regression suite, the two import-boundary scanners, and the build-time citation gate are all green. I additionally reproduced the two-sided D-05 citation enforcement (both the run-time drop and the build-time `--check` failure) against a temporary copy of the tree with a blanked citation, and confirmed empirically — not just by reading the code — that `DSX-ADM-010` fires only on a cited pairwise-domination rule and never on a Manski-fallback-only or tiebreak-only separation. No blocking gaps were found. The phase does, however, carry four still-open human-judgment citation/wording checks that the plans themselves declared but never recorded as performed — these route the phase to `human_needed` rather than `passed`, per the standard rule that a clean automated pass with an open human-check item is not a clean pass.

## Goal Achievement

### Observable Truths (ROADMAP Success Criteria)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | `references/families.yaml` holds 14 estimator families as data keyed on estimand × family × inference method × dependence handling, parsed by the existing `dsx.loader.load()` with no new parser, and named tests resolve as aliases into families rather than being enumerated as a test catalogue. | ✓ VERIFIED | Read `references/families.yaml` directly: exactly 14 entries under `families:`, all four axes present per entry. `tests/test_families_yaml.py` (28/28 pass) proves the dual-loader-path equality and the 14-count. `dsx/frame/admissibility.py::resolve_declared_procedure()` resolves by exact `normalize()`-equality lookup against each family's own `aliases:` list — confirmed by reading the function and by a live call (`fishers_exact` alias → `fishers_exact` family) and by `TestFamiliesYamlTraceability` (6+ committed specs resolve). No test enumeration/catalogue exists in the module. |
| 2 | `dsx recommend-test` returns a ranked admissible set naming, per entry, the assumptions bought and the assumptions charged — the existing subcommand extended, not replaced, with its v1.5.0 behaviour on existing specs unchanged. | ✓ VERIFIED | Ran `dsx recommend-test proportion --groups 2` from both a temp directory and the repo root: byte-identical stdout, keys exactly `['test','rationale','alternatives','effect_size']`. Ran the same command with `--spec examples/good-ANALYSIS-SPEC.yaml`: identical four original keys plus one additive `admissibility` key holding `admissible_families()`'s dict, `admissible[0].id == 'two_proportion_z_cluster_robust'` with `buys`/`charges` lists present. |
| 3 | A deliberately underdetermined frame returns `no_admissible_procedure` and exits 1 under the escalating code at CRITICAL rather than falling back to the nearest-sounding family, and an unrecognised alias escalates rather than resolving. | ✓ VERIFIED | Direct call: a spec with blank `estimand.type` produces `DSX-ADM-020` at CRITICAL, `DecisionRecord.escalate=True`, no `CheckError` raised. A spec declaring an unrecognised procedure label (`not_a_real_test_xyz`) also produces `DSX-ADM-020` — confirming no nearest-match fallback. `dsx gate plan --spec examples/bad-ANALYSIS-SPEC.yaml` (which declares no `dependence.structure`) exits 1, matching the documented single committed exception. |
| 4 | A `families.yaml` entry with no citation fails the build via the Phase 6 catalogue check, and the adjudicator refuses to rank an uncited family — D-05 binds the ontology data exactly as it binds check code. | ✓ VERIFIED | Reproduced both halves independently in a scratch copy of the tree: blanking `two_proportion_z`'s citation made `python scripts/gen-finding-catalogue.py --check` exit 1 with `D-24: families entry 'two_proportion_z' has a missing or blank citation`; separately, `load_ontology()` against the same blanked file loaded 13 families (not 14) with `dropped_uncited == ('two_proportion_z',)` and did not raise. `_D05_ALLOWLIST_PREFIXES` contains `"DSX-ADM-"` and `check_d05()` returns `[]` on the real tree, confirmed live. |
| 5 | Every family entry traces to a fixture or corpus case that needed it, and a test asserts no `families.yaml` entry declares a Bayesian inference method — the axis space is capped to v1's frequentist scope, with Bayesian admissibility left in the gated backlog. | ✓ VERIFIED | `TestFamiliesYamlTraceability.test_every_family_traceability_resolves` (pass) confirms every `traceability:` value resolves to an existing spec path, ranking rule id, or one of the three named operating contexts. `TestFamiliesYamlSchema.test_every_inference_method_is_exactly_frequentist` (pass) asserts every entry's `inference_method` is exactly `"frequentist"`. Direct grep of `references/families.yaml` for `bayesian`: zero occurrences. |

**Score:** 5/5 truths verified (0 present-but-behavior-unverified)

### Additional Directly-Requested Checks

| Check | Method | Result |
|---|---|---|
| `DSX-ADM-010` fires only via a cited pairwise-domination rule, never via Manski-fallback-only or tiebreak-only separation | Ranked the full `difference_in_proportions`/`none` candidate set (`boschloo_exact` → `fishers_exact` [cited rule] → `two_proportion_z` [Manski] → `two_proportion_z_always_valid` [tiebreak]); declared each of the Manski- and tiebreak-dominated procedures directly and called `check()` | Both the Manski-dominated (`two_proportion_z`) and tiebreak-dominated (`two_proportion_z_always_valid`) declarations produced **zero** findings; only declaring the cited-rule-dominated `fishers_exact` produced `DSX-ADM-010`, naming `boschloo_over_fishers_exact` |
| `dsx/frame/admissibility.py` never reads `inference.paradigm` directly | `grep -n "paradigm" dsx/frame/admissibility.py` — only docstring prose referencing the externally-computed boolean and the module name `dsx/frame/paradigm.py`, no code read | `tests.test_frame_boundary` (10/10 pass, includes `TestFrameParadigmReadBoundary.test_real_frame_modules_read_no_declared_paradigm`) — mechanically confirms |
| Two-sided D-05 citation enforcement is wired (`load_ontology()` run-time drop + `check_families_citations()` build-time failure) | Reproduced both against a scratch copy of the tree with one citation blanked | Both fire independently: build gate exits 1 with `D-24:`; loader drops the entry (14→13) without raising |
| `dsx recommend-test`'s byte-identity regression against v1.5.0 output actually holds | Ran the no-flag command from a temp dir and from repo root via subprocess, diffed stdout | Byte-identical, same 4 keys in the same order, independent of working directory |
| Known-bad corpus and full test suite are green | `python -m unittest discover -s tests`; `python -m unittest tests.test_known_bad_corpus` | 1,014/1,014 and 30/30 pass respectively; `git status` confirmed clean of any leftover test artifacts afterward |

### Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `references/families.yaml` | 14-family, 19-token, 4-rule cited ontology, parsed by `dsx.loader.load()` | ✓ VERIFIED | Read in full; matches schema exactly (D-06/D-07/D-08 constraints hold — no `---`, `&`, `<<:`, block scalars). |
| `dsx/frame/admissibility.py` | Ontology loader, alias resolver, ranker, `admissible_families()`, `check()` emitting `DSX-ADM-010`/`DSX-ADM-020` | ✓ VERIFIED | Read in full (954 lines); all documented functions/dataclasses present and match plan-declared signatures. |
| `dsx/frame/paradigm.py` | `applies_to_frequentist_admissibility(spec)`; `_NOT_SHIPPED` emptied | ✓ VERIFIED | Function present at line 457, correct widening logic; `_NOT_SHIPPED == {}` confirmed live. |
| `scripts/gen-finding-catalogue.py` | `check_families_citations()`, `D-24:` wiring, `"DSX-ADM-"` in `_D05_ALLOWLIST_PREFIXES` | ✓ VERIFIED | All three present and functioning; empirically fires on a synthetic uncited entry. |
| `dsx/cli.py` | `CHECKS["admissibility"]`, `GATE_PROFILES` at plan/verify/ship (not execute), `run_checks` dispatch branch, `--spec`/`--phase-dir` on `recommend-test` | ✓ VERIFIED | All present at the documented locations; gate exit codes for the full committed corpus confirmed unchanged. |
| `references/finding-codes.md` | `DSX-ADM` group with both codes | ✓ VERIFIED | Confirmed present via grep. |

### Key Link Verification

| From | To | Via | Status | Details |
|---|---|---|---|---|
| `references/families.yaml` `aliases:` | `dsx/frame/admissibility.py::alias_index()` | No separate alias section — alias only exists on its owning family | ✓ WIRED | Confirmed by reading `alias_index()` and by a live resolution call. |
| `dsx/frame/paradigm.py::applies_to_frequentist_admissibility` | `dsx/cli.py::run_checks`'s admissibility branch | Computed inline, passed as a keyword boolean | ✓ WIRED | `dsx/cli.py:225` calls `paradigm.applies_to_frequentist_admissibility(spec)` and passes it as `applies_to_frame=`. |
| `dsx/frame/admissibility.py::admissible_families()` | `dsx/cli.py::cmd_recommend` | Direct call, JSON-serialisable dict merged additively | ✓ WIRED | Confirmed by subprocess test — `admissibility` key present and correctly populated only when `--spec`/`--phase-dir` given. |
| `dsx/frame/admissibility.py`'s `report.add("DSX-ADM-010"/"DSX-ADM-020", ...)` docstrings/test markers | `scripts/gen-finding-catalogue.py`'s `_D05_ALLOWLIST_PREFIXES` | Inclusion-list entry turns convention into enforcement | ✓ WIRED | `check_d05()` returns `[]` on the real tree with `"DSX-ADM-"` present; confirmed live. |

### Behavioral Spot-Checks (see "Additional Directly-Requested Checks" table above for full detail)

| Behavior | Command | Result | Status |
|---|---|---|---|
| DSX-ADM-010 fires only on cited domination | Direct Python calls to `check()` against Manski-only, tiebreak-only, and cited-rule scenarios | Only the cited-rule scenario fired | ✓ PASS |
| Two-sided D-05 enforcement | Scratch-tree blanked citation, both `--check` and `load_ontology()` | Both independently caught it | ✓ PASS |
| Byte-identical `recommend-test` v1.5.0 output | Subprocess diff, temp dir vs. repo root | Identical | ✓ PASS |
| Bayesian spec draws no `DSX-ADM-*` finding | Direct call against `bayesian-continuous-monitoring` fixture | Zero findings | ✓ PASS |
| Full corpus gate exit codes unchanged | `dsx gate {plan,execute,verify,ship}` across good/template/known-bad/bad fixtures | All match documented expectations | ✓ PASS |

### Probe Execution

No `scripts/*/tests/probe-*.sh` convention exists in this repository and none is declared by any of the 8 plans or their SUMMARYs — SKIPPED (no probe convention in this project; the phase's own `<verify>` blocks and `11-VALIDATION.md` use `python -m unittest`/direct Python assertions instead, which are covered above).

### Requirements Coverage

| Requirement | Source Plan(s) | Description | Status | Evidence |
|---|---|---|---|---|
| REQ-P11-01 | 11-01, 11-02, 11-04 | `families.yaml` holds 14 families (amended from 25–35, D-02), keyed on 4 axes, parsed by existing loader | ✓ SATISFIED | See Truth 1 above. |
| REQ-P11-02 | 11-04, 11-05 | Named tests resolve as aliases into families, not enumerated as a catalogue | ✓ SATISFIED | See Truth 1 and the domination check above. |
| REQ-P11-03 | 11-06 | Admissibility function returns ranked admissible set naming assumptions bought/charged | ✓ SATISFIED | Confirmed via `admissible_families()` output and `rank_admissible()` reading/testing. |
| REQ-P11-04 | 11-02, 11-03, 11-06, 11-07 | Underdetermined frame returns `no_admissible_procedure` and escalates | ✓ SATISFIED | See Truth 3. |
| REQ-P11-05 | 11-03, 11-07 | Adjudicator extends existing `dsx recommend-test` rather than replacing it | ✓ SATISFIED | See Truth 2 and the byte-identity check. |
| REQ-P11-06 | 11-01, 11-04, 11-08 | D-05 applies to `families.yaml` as it does to checks, enforced by M1 catalogue check | ✓ SATISFIED | See Truth 4. |

**Note on tracking artifacts (not a functional gap):** `.planning/REQUIREMENTS.md`'s REQ-P11-01 through REQ-P11-06 checkboxes remain unticked (`[ ]`) and the traceability table still reads "Pending" for all six, even though every requirement is functionally satisfied in the live codebase as shown above. Per this project's CLAUDE.md ("Shared tracking files ... are single-writer only" and "Do not mark requirements complete until the verifying gate has actually passed"), flipping these is expected to happen as a downstream step after this verification report lands — I have not flipped them myself, consistent with the verifier's single-writer boundary, and note it here so the orchestrator can act on it.

**No orphaned requirements:** REQUIREMENTS.md maps exactly REQ-P11-01 through REQ-P11-06 to Phase 11; all six are claimed and covered by at least one of the 8 plans.

### Anti-Patterns Found

None. Grepped every phase-11-modified source file (`dsx/frame/admissibility.py`, `dsx/frame/paradigm.py`, `scripts/gen-finding-catalogue.py`, `dsx/cli.py`, `references/families.yaml`, and the 5 new/extended test modules) for `TBD`, `FIXME`, `XXX`, `TODO`, `HACK`, `PLACEHOLDER` — zero matches.

### Deferred Items (informational, not gaps)

`.planning/phases/11-frequentist-admissibility-adjudicator-dsx-adm/deferred-items.md` records one item: the `gen-finding-catalogue.py --check` warning count discrepancy (4 named in early plan text vs. 7 actual, both pre-existing and unrelated to this phase's own work). This is explicitly named in this verification's briefing as expected and not a defect; confirmed still 7, still pre-existing, `--check` still exits 0. Not treated as a gap.

### Post-Verification Correction (orchestrator note)

The code review (`11-REVIEW.md`, run in parallel with this verification) found and the
orchestrator fixed one CRITICAL bug (`CR-01`, commit `d49666c`) after this verification
pass completed: `dsx recommend-test --spec <bayesian-spec>` bypassed the frequentist-only
scoping predicate that every other path (`dsx gate`/`dsx check`/`dsx audit`) correctly
applies, producing a spurious refusal. This verification's own checks did not catch it
because Truth 2 and the byte-identity check both exercised `recommend-test` only against
the frequentist `good-ANALYSIS-SPEC.yaml`, and the separate Bayesian-spec check (the
"Bayesian spec draws no `DSX-ADM-*` finding" row above) exercised `admissibility.check()`
directly, not `cmd_recommend`. The fix does not change behavior on any frequentist spec
(including `good-ANALYSIS-SPEC.yaml`), so none of the PASS results above are invalidated —
confirmed by re-running the full suite after the fix (1,017 tests, up from 1,014, all
green) and by the fix's own regression test. Two further WARNING-level review findings
(`WR-01`, `WR-03`) were also fixed in the same commit; see `11-REVIEW.md`'s `resolution`
frontmatter for the full disposition of all six review findings.

### Gaps Summary

No blocking gaps were found. Every ROADMAP success criterion, every specifically-requested acceptance check, the full test suite, the known-bad corpus regression suite, and both import-boundary scanners all pass on direct re-execution against the live tree.

The phase is routed to `human_needed` rather than `passed` solely because of four still-open, explicitly plan-declared human-judgment items (see `human_verification` above): the T-11-13/T-11-14 citation-authenticity read over all 14 `families.yaml` entries (explicitly named in this verification's briefing as carried forward to phase closure, not a blocker to this verification's PASS/FAIL determination), the `DSX-ADM-010` ranking-strength wording read, and the two `<human-check>` items from plan 11-01 (the D-27 `test-selection.md` wording and the D-29 `brief.md` locator-strength reads) whose SUMMARY.md entries record `human_judgment: true` without recording that the read was actually performed. None of these are functional defects — they are the honest citation/wording judgement this project's D-05 discipline exists to protect, and no automated check can close them.

---

_Verified: 2026-08-22_
_Verifier: Claude (gsd-verifier)_
