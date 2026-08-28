---
phase: 12-calibration
plan: 01
subsystem: known-bad-corpus
tags: [corpus, calibration, coverage, attribution, tdd]
requires:
  - "tests/test_known_bad_corpus.py::_slugs glob discovery"
  - "tests/test_causal_verb_golden.py::_ship_findings fresh-tempdir helper"
  - "brief.md §6.5 gated backlog (nine rows)"
provides:
  - "three known-bad coverage classes present by class-presence predicate (D-01)"
  - "per-slug ATTRIBUTION.yaml sidecar file kind (D-06/D-07)"
  - "lockstep golden entries for three new specs"
affects:
  - "plan 12-03 (sidecar sibling-integrity + falsifiability tests)"
  - "plan 12-05/12-06 (rate/FPR/friction harness reads this corpus)"
  - "plan 12-07 (§6.5 re-evaluation counts sidecars)"
tech-stack:
  added: []
  patterns:
    - "class-presence coverage predicate over glob-discovered slugs (D-01)"
    - "catch-attribution carried in a frame_digest-safe sidecar (D-06, 11.2 D-08 placement)"
    - "whole-examples-tree lockstep registration across every glob harness (RESEARCH Pitfall 2)"
key-files:
  created:
    - "examples/known-bad/garden-of-forking-paths-p-hacking-ANALYSIS-SPEC.yaml + -POSTMORTEM.md + -ATTRIBUTION.yaml"
    - "examples/known-bad/retracted-fabricated-field-experiment-ANALYSIS-SPEC.yaml + -POSTMORTEM.md + -ATTRIBUTION.yaml"
    - "examples/known-bad/operator-known-answer-selective-exclusion-ANALYSIS-SPEC.yaml + -POSTMORTEM.md + -ATTRIBUTION.yaml"
  modified:
    - "tests/test_known_bad_corpus.py (coverage predicate + incidental allowlist + expected-caught keys)"
    - "tests/test_causal_verb_golden.py (three measured golden entries)"
    - "tests/test_frame_val.py (three _EXPECTED_VAL_CODES entries)"
    - "tests/test_frame_interference.py (non-causal exclusion set)"
    - "tests/test_dsx.py (committed-spec count 11 -> 14)"
decisions:
  - "All three coverage cases are genuine MISSES: the real-world defect is invisible to a declaration-only gate; each carries a sidecar naming the absent code and the §6.5 row it promotes."
  - "operator-known-answer framed descriptive/observational (faithful to Reinhart-Rogoff's stylised-fact claim), so it is a non-causal known-bad fixture."
metrics:
  duration: "~25 min"
  completed: "2026-08-27"
requirements-completed: [REQ-P12-01, REQ-P12-02]
status: complete
---

# Phase 12 Plan 01: Known-bad corpus coverage classes + catch-attribution sidecars Summary

Extended the known-bad corpus to full size by class-coverage (D-01) and instrumented each new miss with a frame_digest-safe catch-attribution sidecar in the same change (REQ-P12-02 ordering), using a class-presence coverage predicate rather than a fixed count, with every new spec's ship finding-set measured live and pinned in lockstep across all glob harnesses.

## What was built

- **Coverage predicate (TDD):** `test_corpus_includes_full_coverage_classes` asserts class-presence over glob-discovered slugs for three markers — `retract`, `p-hack`/`phack`, `operator-known` — no hardcoded slug list, no target count (D-01/D-02). Committed RED (failed on the 8-pair corpus), then GREEN.
- **Three real coverage-class cases**, each a genuine MISS whose defect a declaration-only gate structurally cannot catch:
  - `garden-of-forking-paths-p-hacking` (p-hacking class) — undisclosed specification search reported as a single comparison.
  - `retracted-fabricated-field-experiment` (retracted class) — a well-powered design resting on fabricated data.
  - `operator-known-answer-selective-exclusion` (operator-known class) — undisclosed selective exclusion + weighting; descriptive/observational.
- **Three ATTRIBUTION.yaml sidecars** (D-06/D-07 schema: `absent_code`, `promotes_backlog_item`, `kind`, `rationale`) living only in the sidecar, never in the spec — confirmed no attribution keys appear in any spec, so `frame_digest` is unperturbed (11.2 D-08 placement, cited correctly — not 11.3 D-08).
- **Lockstep golden + harness registration:** one measured `_GOLDEN_SHIP_FINDINGS` entry per new spec, plus registration in every whole-examples-tree glob harness (see Deviations).

## Coverage cases, sources, and attribution

| Slug | Class | Primary source (locators flagged UNVERIFIED, D-05 read pre-registered for UAT) | promotes_backlog_item | absent_code |
|------|-------|-------------------------------------------------------------------------------|-----------------------|-------------|
| garden-of-forking-paths-p-hacking | p-hacking | Gelman & Loken (2014) American Scientist 102(6):460; Simmons, Nelson & Simonsohn (2011) Psych Science 22(11):1359-66; Wansink (2016) blog + van der Zee, Anaya & Brown (2017) BMC Nutrition 3:54 | §6.5 item 1 (prior justification & sensitivity / frequentist specification sensitivity) | DSX-EXP-051 |
| retracted-fabricated-field-experiment | retracted | LaCour & Green (2014) Science 346(6215):1366-69 [RETRACTED]; Broockman, Kalla & Aronow (2015) "Irregularities in LaCour (2014)"; retraction notice Science 348(6239):1100 | §6.5 item 7 (feature/data provenance) | DSX-REP-020 |
| operator-known-answer-selective-exclusion | operator-known | Reinhart & Rogoff (2010) AER 100(2):573-78; Herndon, Ash & Pollin (2014) Cambridge J Econ 38(2):257-79 | §6.5 item 1 (prior justification & sensitivity / frequentist specification sensitivity) | DSX-VAL-080 |

All three are `kind: miss`. Each absent_code was **measured** to never fire at any gate point (plan/execute/verify/ship), satisfying D-08's miss-falsifiability polarity in advance of plan 12-03's dedicated test.

## Measured golden ship finding-sets (fresh-tempdir `_ship_findings`, 2026-08-27)

- garden-of-forking-paths-p-hacking: `{DSX-CLM-031, DSX-COH-031, DSX-DEC-001, DSX-MET-040, DSX-NAR-001, DSX-REP-030, DSX-REP-050}`
- retracted-fabricated-field-experiment: same set as above
- operator-known-answer-selective-exclusion: `{DSX-CLM-031, DSX-MET-040, DSX-NAR-001, DSX-REP-030, DSX-REP-050}` (descriptive → no DEC-001/COH-031)

Every code is a shared corpus-completeness incidental gap, never the encoded defect.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking issue] Registered new fixtures in every whole-examples-tree glob harness**
- **Found during:** Task 1/2 (running `scripts/check.sh`).
- **Issue:** Adding glob-discovered corpus fixtures hard-fails not only the golden test but every whole-tree harness that requires per-fixture registration (RESEARCH Pitfall 2, generalized). Four beyond the golden test: `_INCIDENTAL_GAP_CODES` (DSX-DEC-001/DSX-REP-050 fire because the new specs declare `results.tests`), `_EXPECTED_CAUGHT_DEFECTS` (equality test requires every slug keyed — misses catch nothing → `frozenset()`), `tests/test_frame_val.py::_EXPECTED_VAL_CODES` (empty set each, measured), `tests/test_frame_interference.py::_NON_CAUSAL_KNOWN_BAD` (the descriptive operator-known fixture), and `tests/test_dsx.py` committed-spec count (11→14).
- **Fix:** Added measured/empty registrations in each; all values measured via `dsx.frame.val.check()` / live gate runs, never guessed.
- **Files modified:** tests/test_known_bad_corpus.py, tests/test_frame_val.py, tests/test_frame_interference.py, tests/test_dsx.py.
- **Commits:** 2a37ebf (corpus harness), dd58d84 (frame_val/interference/dsx).
- **Scope note:** test_frame_val.py, test_frame_interference.py and test_dsx.py are outside the plan's declared `files_modified`, but their edits are mechanically required by the in-scope `examples/known-bad/` additions and are lockstep registrations only (no logic change).

**2. [Rule 1 - Spec quality] Reframed two specs to the proportion-outcome path**
- **Found during:** Task 1 GREEN (measuring finding-sets).
- **Issue:** Continuous-outcome experiments have no clean path in the current schema (no continuous sibling exists; checks assume a proportion baseline_rate), so the first drafts fired accidental spec-quality findings (DSX-EXP-002 invalid baseline_rate, DSX-EXP-021 unit mismatch, DSX-INT-030 additive dilution, DSX-CAU-011/ADM-020). Reframed the retracted case as a proportion "share who durably warmed" and the operator-known case as a descriptive group-mean contrast so each fires only its intended incidental set (plan requirement: "only fire its intended defect").
- **Commit:** 2a37ebf.

## Zero codes minted (D-18)

`git diff --stat` over the whole plan confirms **no change** to `dsx/findings.py`, `dsx/cli.py` (GATE_PROFILES / CHECKS), or `references/finding-codes.md`. Sidecars only REFERENCE existing shipped catalogue codes. The catalogue stays 256.

## Verification

- Task 1: `python -m unittest tests.test_known_bad_corpus.TestKnownBadCorpus.test_corpus_includes_full_coverage_classes ...holds_at_least_three_pairs ...every_spec_has_a_sibling_postmortem_and_vice_versa` → **3 tests OK**.
- Task 2: `python -m unittest tests.test_causal_verb_golden` → **6 tests OK**.
- Full corpus module: `python -m unittest tests.test_known_bad_corpus` → **31 tests OK**.
- Full repo gate: `bash scripts/check.sh` → **all checks passed (1200 tests)**.

## Known Stubs

None. All three cases are honestly-sourced real cases; no fixture was reverse-engineered to hit a threshold (D-02 source-before-count).

## Self-Check: PASSED

- Created files verified present: 3 specs, 3 postmortems, 3 sidecars under examples/known-bad/.
- Commits verified: 0935d98 (RED), 2a37ebf (GREEN), 919a803 (sidecars+golden), dd58d84 (harness registration).
- Protected files verified untouched via `git diff --stat 0935d98~1 HEAD -- dsx/findings.py dsx/cli.py references/finding-codes.md` (empty).
