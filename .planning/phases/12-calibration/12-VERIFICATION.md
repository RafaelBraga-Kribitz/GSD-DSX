---
phase: 12-calibration
verified: 2026-08-27T00:00:00Z
status: human_needed
score: 5/5 must-haves verified
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: none
  previous_score: n/a
human_verification:
  - test: "D-05 primary-source citation read for garden-of-forking-paths-p-hacking (documented p-hacking / garden-of-forking-paths case) — verbatim quote at locator, assembled the way HQ-1/HQ-4/HQ-5 packs were."
    expected: "A verbatim primary-source quote at a citable locator confirms the case is a real, documented p-hacking archetype (not a reverse-engineered fixture)."
    why_human: "Primary-source reading against an external publication is the project's human bar (12-CONTEXT <deferred> D-05 pre-registration); grep cannot confirm a real-world citation is faithfully quoted."
  - test: "D-05 primary-source citation read for retracted-fabricated-field-experiment (retracted paper with published post-mortem) — verbatim quote at locator."
    expected: "A verbatim quote from the retraction notice / published post-mortem at a citable locator confirms the case is a real retracted-with-postmortem archetype."
    why_human: "Same as above — external-source fidelity is a human read, pre-registered for the Phase-12 UAT/ship round (mirrors 11.2/11.3 D-05 handling)."
  - test: "D-05 primary-source citation read for operator-known-answer-selective-exclusion (operator's own prior work whose answer is now known) — verbatim quote / provenance at locator."
    expected: "Provenance confirms the case is genuinely operator-known-answer, sourced-before-counted (D-02), not manufactured to trip a §6.5 threshold."
    why_human: "Provenance of the operator's own prior work is a human attestation; not programmatically checkable. Owed at UAT/ship per 12-07-SUMMARY §'D-05 note'."
---

# Phase 12: Calibration Verification Report

**Phase Goal:** There is a number. Measured catch rate and false-positive rate across a full-size known-bad corpus, a paradigm split across the operator's own frame history, and every gated-backlog entry condition either evaluated against measured evidence or removed.
**Verified:** 2026-08-27
**Status:** human_needed (5/5 requirements technically MET and test-backed; only the pre-registered D-05 human citation reads remain — non-blocking, mirrors 11.2/11.3)
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths (ROADMAP Success Criteria + REQ-P12-01..05)

| # | Truth (Success Criterion) | Status | Evidence |
|---|---|---|---|
| SC1 / REQ-P12-01 | Known-bad corpus extended to full size across the three missing coverage classes (retracted+postmortem, p-hacking, operator-known-answer), sourced-before-counted, class-presence predicate (no hardcoded slug list) | ✓ VERIFIED | 3 new spec+postmortem pairs on disk; `test_corpus_includes_full_coverage_classes` (`tests/test_known_bad_corpus.py:862`) GREEN — asserts class presence over glob-discovered slugs, never a count/slug-list. Full suite 1221 OK. |
| SC3 / REQ-P12-02 | Every miss/promotion case carries a machine-readable `<slug>-ATTRIBUTION.yaml` sidecar (frame_digest-safe, union-validated, live-falsifiable across all four gate points); per-family friction RAW+NET; catalogue stays 256 | ✓ VERIFIED | Sidecars present for all 3 miss cases. `test_attribution_sidecars_reference_valid_codes_and_items` (`:1363`) + `test_attribution_tags_are_falsifiable_against_live_gate` (`:1438`, checks absent_code fires NOWHERE CRITICAL across plan/execute/verify/ship) GREEN. Friction: `test_net_is_raw_minus_own_and_both_are_surfaced` (`:1935`), `test_relabeling_incidental_to_own_shrinks_net_but_not_raw` (`:1957`), `test_friction_uses_the_same_live_findings_as_golden` (`:1627`) GREEN. Catalogue: `test_finding_catalogue_stays_at_256_codes` GREEN; `references/finding-codes.md:16` = "Total: 256 codes." |
| SC2 / REQ-P12-03 | Harness reports catch rate + FPR as reproducible numbers, stratified PRESENT vs ABSENT, headline (miss-rate, FPR); good-side FPR control corpus ≥10 clean specs | ✓ VERIFIED | `test_stratified_catch_rate_and_fpr_report` (`:1496`) GREEN — headline (miss-rate 1.0 = 3/3, FPR 0.0 = 0/12), ABSENT partition floored at 3 (`_ABSENT_PARTITION_FLOOR`). Invariance proof `test_headline_is_invariant_to_adding_a_target_present_case` (`:1915`, TestStratifiedHeadlineHelpers) GREEN. 12 clean good-corpus specs in `examples/good-corpus/` (6 freq / 6 Bayesian); `test_false_positive_findings_excludes_documented_tempdir_noise` (`:1880`) GREEN. Readout recorded + Statistician-reviewed (`12-READOUT.md`). |
| SC4 / REQ-P12-04 | `dsx stats --paradigm` exits 0 and reports the frequentist/Bayesian split over the operator's own frame history; distinct-frame dedup; D-13 fixture-floor exclusion (CR-01 hardened to absolute boundary) | ✓ VERIFIED | Live: `dsx stats --paradigm --root .planning` → "no operator history yet … (examples/ and templates/ excluded)", exit 0. `test_always_exits_zero`, `test_dedup_is_by_distinct_frame_digest`, `test_never_sources_the_known_bad_floor`, `test_root_pointed_at_the_floor_still_excludes_it` (CR-01 pin), `test_excluded_component_match_is_case_folded`, `test_block_on_flag_is_rejected` — all GREEN (`tests/test_cli_stats.py`). |
| SC5 / REQ-P12-05 | §6.5 re-evaluated against measured evidence: carry 8, remove 1; item-6 ratio-metric relocated (not deleted) to Removed/out-of-scope with pinned substrings intact; REV-002 filed, SELF-001-safe | ✓ VERIFIED | `.planning/REVERSALS.md:82` REV-002 present; "New evidence" field explicitly refuses to launder the D-01/D-02 determinism doctrine as novelty (SELF-001-safe, D-17). `brief.md:430` "Removed / permanently out of scope (D-14)" subsection holds the relocated item-6 row; `test_brief_states_the_ratio_metric_dilution_entry_condition_as_a_falsifiable_blocker` (`:1284`) GREEN — pins "Ratio-metric dilution for trigger analysis", "Formula (3)", "per-unit trigger and outcome data reaching the gate". |

**Score:** 5/5 requirements verified, each backed by a named passing test. 0 present-but-behavior-unverified.

### Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `examples/known-bad/garden-of-forking-paths-p-hacking-*` | spec+postmortem+ATTRIBUTION | ✓ VERIFIED | 3 files present; absent_code `DSX-EXP-051`, promotes item 1, live-confirmed silent. |
| `examples/known-bad/operator-known-answer-selective-exclusion-*` | spec+postmortem+ATTRIBUTION | ✓ VERIFIED | 3 files present; absent_code `DSX-VAL-080`, promotes item 1; §S3-3 flag resolved (silent at every severity). |
| `examples/known-bad/retracted-fabricated-field-experiment-*` | spec+postmortem+ATTRIBUTION | ✓ VERIFIED | 3 files present; absent_code `DSX-REP-020`, promotes item 7; IN-02 "nearest-anchor" polarity by-design-disclosed in sidecar rationale. |
| `examples/good-corpus/` (12 clean specs) | ≥10 clean FPR denominator | ✓ VERIFIED | 12 specs (6 freq / 6 Bayesian × proportion/continuous/count); all CRITICAL=0, HIGH=0 under `dsx audit` (12-REVIEW confirmed). |
| `dsx/cli.py` `cmd_stats` + `stats` subparser | pure return-0 reader, no GATE_PROFILES entry | ✓ VERIFIED | Subparser wired; not in CHECKS/GATE_PROFILES (diff-confirmed); `--block-on` rejected. |
| `tests/test_finding_catalogue_invariant.py` | catalogue stays 256 | ✓ VERIFIED | `test_finding_catalogue_stays_at_256_codes` GREEN. |
| `.planning/REVERSALS.md` REV-002 | D-14 reversal, SELF-001-safe | ✓ VERIFIED | Present at `:82`; honest reclassification framing. |
| `12-READOUT.md` | recorded, Statistician-reviewed | ✓ VERIFIED | status: recorded; RECORD-WITH-AMENDMENTS (F1–F6 folded/corrected). |

### Key Link Verification

| From | To | Via | Status |
|---|---|---|---|
| attribution sidecar `absent_code` | live `_gate_findings` union (4 gate points) | falsifiability assertion (miss ⇒ fires nowhere CRITICAL) | ✓ WIRED (`test_attribution_tags_are_falsifiable_against_live_gate`) |
| friction column | same `_gate_findings` set as golden test | live-source proof | ✓ WIRED (`test_friction_uses_the_same_live_findings_as_golden`) |
| `dsx stats --paradigm` | operator `.planning/` trails only | D-13 exclusion on resolved absolute parts (CR-01 fix) | ✓ WIRED (`test_root_pointed_at_the_floor_still_excludes_it`) |
| REV-002 relocation | brief.md §6.5 pinned row | pin test on 3 substrings | ✓ WIRED (`test_brief_states_the_ratio_metric_dilution_entry_condition_as_a_falsifiable_blocker`) |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|---|---|---|---|
| Targeted REQ tests | `python -m unittest` (coverage-classes, sidecar-integrity, falsifiability, stratified-rate) | 4/4 OK (2.9s) | ✓ PASS |
| Headline/friction helpers + effect-size | `python -m unittest TestStratifiedHeadlineHelpers TestFrictionArithmetic test_effect_size_kind` | 14 OK | ✓ PASS |
| CLI stats + catalogue invariant | `python -m unittest tests.test_cli_stats tests.test_finding_catalogue_invariant` | 8 OK | ✓ PASS |
| `dsx stats --paradigm` live | `python -m dsx stats --paradigm --root .planning` | "no operator history yet … excluded", exit 0 | ✓ PASS |
| Full suite | `python -m unittest discover -s tests -q` | Ran 1221 tests — OK | ✓ PASS |
| Gate | `bash scripts/check.sh` | all checks passed; catalogue current (256); capability conformant; determinism OK | ✓ PASS |

### Requirements Coverage

| Requirement | Source Plan(s) | Status | Evidence |
|---|---|---|---|
| REQ-P12-01 | 12-01 | ✓ SATISFIED | Coverage-class predicate GREEN; 3 new pairs. |
| REQ-P12-02 | 12-01, 12-03, 12-06 | ✓ SATISFIED | Sidecar integrity + falsifiability + friction RAW/NET + catalogue-256 all GREEN. |
| REQ-P12-03 | 12-04, 12-05 | ✓ SATISFIED | Stratified rate + FPR (0/12) + headline invariance GREEN; readout recorded. |
| REQ-P12-04 | 12-02 | ✓ SATISFIED | `dsx stats --paradigm` exit 0 + dedup + D-13 exclusion (CR-01 hardened) GREEN. |
| REQ-P12-05 | 12-07 | ✓ SATISFIED | REV-002 (SELF-001-safe) + item-6 relocation pin GREEN; carry-8/remove-1. |

### Anti-Patterns Found

| File | Pattern | Severity | Impact |
|---|---|---|---|
| — | No unreferenced TBD/FIXME/XXX in phase-modified code | ℹ️ Info | Clean. Debt-marker gate passes. |
| `.planning/REVERSALS.md:116` | REV-002 "What did not change" describes item 4 as "`dsx stats --paradigm` measured below 15%", whereas the corrected READOUT §5 (Statistician F5) states the split is 0/0 **undefined/untestable**, not measured-below-threshold | ℹ️ Info | Disposition (carry item 4) is identical either way; wording-only inconsistency between REVERSALS.md and the corrected readout framing. Not a gap — item-4 carry is correct. Worth a one-line reconciliation at ship. |
| `retracted-fabricated-field-experiment-ATTRIBUTION.yaml` | `absent_code: DSX-REP-020` is "nearest-anchor" not strictly "would-have-caught" (IN-02) | ℹ️ Info | Adjudicated BY-DESIGN in 12-REVIEW + READOUT F2 (only this class is structurally uncatchable regardless of authoring); transparently disclosed in the sidecar's own rationale. |

### Human Verification Required

3 items — the pre-registered D-05 primary-source citation reads for the three new corpus cases (owed at the Phase-12 UAT/ship round per 12-CONTEXT `<deferred>` and recorded non-blocking in 12-07-SUMMARY §"D-05 note"). These mirror how 11.2/11.3 handled D-05: they do **not** reduce technical coverage — every requirement is already backed by a named passing test. See frontmatter `human_verification`.

### Gaps Summary

**0 gaps.** All five ROADMAP success criteria / REQ-P12-01..05 are delivered and backed by named passing tests. Full suite 1221 OK, `check.sh` all checks passed, catalogue invariant 256 (zero codes minted, D-18 honored). The prior code-review BLOCKER CR-01 (D-13 exclusion defeated when `--root` resolves at/inside the fixture tree) and WR-01 are FIXED (`4e8d1ff`) and independently re-confirmed here (default `--root .planning` safe; the CR-01 vector is now pinned by `test_root_pointed_at_the_floor_still_excludes_it`). REV-002 survives its own SELF-001 self-consistency convention. The only outstanding work is the pre-registered, non-blocking D-05 human citation reads → status `human_needed`, not `passed`.

---

_Verified: 2026-08-27_
_Verifier: Claude (gsd-verifier, opus/high, goal-backward)_
