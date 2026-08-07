---
phase: 06-contract-extension-decision-record-paradigm-manifest
plan: 06
subsystem: contract
tags: [dsx-spec, validity-frame, inference, decision-record, tdd, d-05, closed-vocabulary]

requires:
  - phase: 06-01
    provides: "loader _NULL fix (literal 'none' parses as a string) and the ten new closed vocabularies + _VOCABULARIES registry in dsx/spec.py"
  - phase: 06-02
    provides: "dsx/decisions.py substrate — DecisionRecord, collect_from_report(); this plan is its first caller"
  - phase: 06-03
    provides: "D-05 enforcement wired into scripts/gen-finding-catalogue.py --check, covering DSX-SPEC-08x and DSX-PAR- prefixes"
  - phase: 06-05
    provides: "examples/good-ANALYSIS-SPEC.yaml (clean validity_frame/inference), examples/bad-ANALYSIS-SPEC.yaml (six missing sub-blocks, two membership defects), templates/ANALYSIS-SPEC.yaml scaffold — all pre-shaped for this plan's validators"
provides:
  - "_validate_validity_frame_shape() and _validate_inference_shape() in dsx/spec.py, wired into validate_structure()'s existing call chain"
  - "Five new finding codes: DSX-SPEC-080/081/082/085/086, each D-05-compliant (Citation + Structural criterion + linked test)"
  - "Both validators emit layer=deterministic DecisionRecord entries onto report.context['decisions'] — the first real caller of dsx/decisions.py"
  - "references/finding-codes.md regenerated; gen-finding-catalogue.py --check passes both halves (staleness + D-05) for the whole tree, not just at phase end"
affects: [06-07, 06-08, 06-09, 06-10, 07, 08, 09, 10]

tech-stack:
  added: []
  patterns:
    - "Case-insensitive vocabulary membership via a normalized-key set comparison ({normalize(k) for k in vocab}), not exact-key membership — keeps a single comparison path across both lowercase-snake_case vocabularies and MISSINGNESS_MECHANISMS' case-sensitive MCAR/MAR/MNAR acronyms (R-02)"
    - "In-function DecisionRecord import (not module-level) to keep dsx/spec.py's import surface unchanged for the fifteen dsx/checks/*.py consumers that import from it"
    - "Aggregate-vs-per-item finding granularity: one CRITICAL for total block absence, one CRITICAL per missing sub-block once the block exists (D-11) — the plan's explicit correction to the RESEARCH.md sketch's single aggregate call"

key-files:
  created: []
  modified:
    - dsx/spec.py
    - tests/test_dsx.py
    - references/finding-codes.md

key-decisions:
  - "Membership comparison for validity_frame sub-fields normalizes both the declared value AND the vocabulary keys before comparing, rather than normalizing only the value — MISSINGNESS_MECHANISMS is deliberately case-sensitive (MCAR/MAR/MNAR per R-02) while every other vocabulary in dsx/spec.py is already lowercase, so exact-key membership against normalize(value) silently broke the good fixture's missingness.mechanism: MAR (Rule 1 auto-fix, found via full-suite regression, not a plan-specified behaviour)"
  - "Requiredness gating predicate is exactly the one the plan text mandates: question_type in ('causal', 'prescriptive') or design.kind == 'experiment' — reusing dsx/checks/design.py::_check_identification's existing causal-requiredness predicate rather than deriving a new one, per the plan's explicit instruction and the flagged-assumption note it carries forward unresolved"
  - "The requiredness DecisionRecord is emitted unconditionally on every validate_structure() call (even when validity_frame is absent or malformed) because the requiredness computation itself — which sub-blocks are required — happens regardless of whether the block exists; the inference DecisionRecord is emitted only when the inference: block is present as a non-empty dict, since 'no block' has no paradigm choice to record"
  - "Deng, Lu & Chen (2016) citation's exact section/theorem locator is flagged unverified rather than invented — author/year/title/venue match brief.md section 7's locked anchor, but sub-paper granularity exceeds what could be confirmed at authoring time; escalated per the plan's explicit 'stop and escalate rather than invent' instruction (D-05, T-6-07)"

patterns-established:
  - "A structural shape validator computes its requiredness/decision inputs once at the top of the function and records a DecisionRecord immediately, before any early-return branches for absent/malformed input — so the decision trail captures the rule that was applied even when the input failed the rule"

requirements-completed: [REQ-P6-02, REQ-P6-03, REQ-P6-04]

coverage:
  - id: D1
    description: "validity_frame requiredness gated by question_type/design.kind per R-01: block absence yields one itemised CRITICAL DSX-SPEC-080, a present-but-incomplete block yields one CRITICAL DSX-SPEC-081 per missing sub-block (not an aggregate), and a descriptive/non-experimental spec omitting the four causal-only sub-blocks passes clean"
    requirement: "REQ-P6-03"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestSpecStructure (test_causal_spec_with_no_validity_frame_key_reports_one_critical_itemising_ten, test_descriptive_spec_with_no_validity_frame_key_names_only_six, test_causal_spec_missing_three_sub_blocks_reports_three_findings, test_descriptive_spec_with_only_six_always_required_produces_no_findings, test_descriptive_experiment_design_still_requires_interference, test_malformed_validity_frame_shapes_degrade_to_dsx_spec_080_not_a_crash)"
        status: pass
    human_judgment: false
  - id: D2
    description: "validity_frame's ten sub-blocks are shape-validated against their closed vocabularies (eight vocabulary-typed fields across identification/dependence/interference/triggering/missingness); a blank or absent field is not a membership error"
    requirement: "REQ-P6-02"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestSpecStructure::test_out_of_vocabulary_sub_field_reports_high_with_allowed_members, test_good_fixture_produces_none_of_the_three_validity_frame_codes"
        status: pass
    human_judgment: false
  - id: D3
    description: "inference: block's three vocabulary-typed fields (paradigm, paradigm_justification, declared_at) are validated; declaring the field M-02 removed (stopping_rule) produces a redirect to design.peeking_policy rather than silence; _INFERENCE_FIELDS pins the exact six REQ-P6-04 field names"
    requirement: "REQ-P6-04"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestSpecStructure (test_absent_inference_block_produces_no_finding, test_inference_fields_constant_matches_req_p6_04, test_inference_vocabulary_violations_report_three_high_findings, test_removed_stopping_rule_field_redirects_to_peeking_policy, test_good_fixture_produces_none_of_the_inference_codes)"
        status: pass
    human_judgment: false
  - id: D4
    description: "Both validators append one layer=deterministic DecisionRecord each onto report.context['decisions'], with empty id/invocation_id placeholders left for CLI assignment, collectible via dsx.decisions.collect_from_report through a merged report; no dsx/checks/*.py module appends to a decisions list (D-13 boundary, source-level guard test)"
    requirement: "REQ-P6-02"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestSpecStructure (test_structural_adjudications_emit_deterministic_decision_records, test_collect_from_report_returns_both_decisions_in_order, test_no_check_module_appends_to_a_decisions_list)"
        status: pass
    human_judgment: false
  - id: D5
    description: "Every new DSX-SPEC-08x code satisfies both halves of D-05 (Citation + Structural criterion line, plus a linked # D-05: test marker) and the regenerated references/finding-codes.md passes gen-finding-catalogue.py --check (staleness + D-05) for the whole tree"
    requirement: "REQ-P6-11"
    verification:
      - kind: unit
        ref: "python3 scripts/gen-finding-catalogue.py --check exits 0; check_d05() returns []"
        status: pass
    human_judgment: false

duration: 20min
completed: 2026-08-08
status: complete
---

# Phase 6 Plan 06: Validity-frame and inference structural shape validators Summary

**`_validate_validity_frame_shape()` and `_validate_inference_shape()` land in `dsx/spec.py`, making `validity_frame:` requiredness and both blocks' closed vocabularies enforceable at `dsx gate plan` — the contract becomes a gate, not documentation, and both validators emit the project's first real `dsx/decisions.py` decision records.**

## Performance

- **Duration:** ~20 min
- **Completed:** 2026-08-08
- **Tasks:** 3 (all `tdd="true"`)
- **Files modified:** 3 (`dsx/spec.py`, `tests/test_dsx.py`, `references/finding-codes.md`)

## Accomplishments

- `_validate_validity_frame_shape()`: requiredness gated by `question_type`/`design.kind` per locked decision R-01 (six always-required sub-blocks, four causal-only). Block absence → one itemised `DSX-SPEC-080` (CRITICAL). Block present but incomplete → one `DSX-SPEC-081` (CRITICAL) **per missing sub-block**, per D-11's explicit correction to the RESEARCH.md sketch's aggregate-call approach. A non-dict `validity_frame` (string, list, empty dict, `None`) degrades to `DSX-SPEC-080` rather than raising (T-6-12).
- Eight sub-field vocabulary memberships checked independently of requiredness across `identification`, `dependence`, `interference`, `triggering`, `missingness` — `DSX-SPEC-082` (HIGH), `detail` listing sorted allowed members.
- `_validate_inference_shape()`: the optional `inference:` block's three vocabulary-typed fields (`paradigm`, `paradigm_justification`, `declared_at`) validated against `DSX-SPEC-085` (HIGH); declaring the field M-02 removed (`stopping_rule`) redirects to `design.peeking_policy` via `DSX-SPEC-086` (HIGH) rather than silent acceptance. `_INFERENCE_FIELDS` pins the exact six REQ-P6-04 field names.
- Both functions append one `layer=deterministic` `DecisionRecord` each onto `report.context["decisions"]` with empty `id`/`invocation_id` placeholders (CLI assigns at write time, per D-19) — the first real caller of `dsx/decisions.py`'s substrate. `DecisionRecord` is imported inside each function body, keeping `dsx/spec.py`'s module-level import surface unchanged for the fifteen `dsx/checks/*.py` consumers.
- D-05 compliance: each function's docstring carries multiple `Citation:` lines (Hernán & Robins 2020 for estimand/identification; Little & Rubin 2019 for missingness; Imbens & Rubin 2015 §1.6 for interference/SUTVA in the frame validator; Deng, Lu & Chen 2016 in the inference validator) and a `Structural criterion:` line stating each is a presence-and-membership test, not a numeric one.
- `references/finding-codes.md` regenerated via `gen-finding-catalogue.py --write`; `--check` now passes both the staleness half and the D-05 half for all five new codes against the real tree.
- No `dsx/checks/` module touched (`git diff --stat dsx/checks/` empty at every commit) — proven mechanically by a new source-scanning guard test (`test_no_check_module_appends_to_a_decisions_list`), not just by convention.

## Task Commits

TDD RED/GREEN, but the three tasks' RED tests were authored together in one commit and Tasks 1+2's GREEN implementation landed together in one commit (see Deviations below for why):

1. **RED (Tasks 1–3 combined):** `46c216d` test(06-06): add failing tests for validity_frame/inference shape and decision records
2. **GREEN (Tasks 1–2):** `7ded314` feat(06-06): validity_frame and inference structural shape validators
3. **GREEN (Task 3, catalogue only):** `c37ba3f` feat(06-06): regenerate finding catalogue for the five new DSX-SPEC-08x codes

**Plan metadata:** pending (final `docs(06-06)` commit follows this summary)

## Files Created/Modified

- `dsx/spec.py` — added `_VALIDITY_FRAME_ALWAYS_REQUIRED`, `_VALIDITY_FRAME_CAUSAL_REQUIRED`, `_VALIDITY_FRAME_MEMBERSHIP`, `_validate_validity_frame_shape()`, `_INFERENCE_FIELDS`, `_INFERENCE_MEMBERSHIP`, `_INFERENCE_REMOVED_FIELD`, `_validate_inference_shape()`; both wired into `validate_structure()`'s call chain after `_validate_claims_shape()`
- `tests/test_dsx.py` — 21 new test methods in `TestSpecStructure` (pure insertion after `test_no_shipped_spec_declares_removed_stopping_rule_field`, before the `# ── design ──` divider) plus `import re` for the D-13 guard test; `git diff -U0` confirms no touch inside the original lines 804-839 range
- `references/finding-codes.md` — regenerated; five new rows under `## Contract structure — DSX-SPEC-*`

## Decisions Made

- **Case-insensitive membership via normalized vocabulary keys, not normalized-value-only comparison.** The good fixture (06-05) declares `missingness.mechanism: MAR`, matching `MISSINGNESS_MECHANISMS`' deliberately case-sensitive acronym keys (`MCAR`/`MAR`/`MNAR`, R-02). My first implementation normalized only the declared value (`normalize(value) not in vocab`), which lowercases `MAR` to `mar` and fails exact membership against the uppercase keys — this broke the good fixture and an existing `TestCLI` integration test (`test_mixed_project_phase_dirs_behave_correctly`) on the first full-suite run. Fixed by comparing `normalize(value)` against `{normalize(k) for k in vocab}` instead of `vocab` directly — one comparison path for both case-sensitive and case-insensitive vocabularies, no per-field special case. **(Rule 1 — bug, caught by the full-suite run before commit, not by a plan-specified test.)**
- **R-01's requiredness predicate reused verbatim from `_check_identification`**, per the plan's explicit instruction: `question_type in ("causal", "prescriptive") or design.kind == "experiment"`. The plan itself flags this predicate as the one part of R-01 not pinned by the locked decision (a `predictive` question with a causal decision rule could slip past the causal-only four) — carried forward as-is, not re-litigated here.
- **Decision-record emission timing:** the requiredness record is emitted before the presence/shape branches in `_validate_validity_frame_shape` (so it fires even when `validity_frame` is absent or malformed — the rule was still applied, just against absent input), while the inference record is emitted only after confirming `inference:` is a non-empty dict (nothing was decided if there's no block to read a paradigm from).
- **Deng, Lu & Chen (2016) citation locator flagged, not fabricated.** The plan requires "the exact section or theorem" and explicitly instructs escalation over invention when this can't be verified. Author/year/title/venue (IEEE DSAA 2016, "Continuous Monitoring of A/B Tests without Pain: Optional Stopping in Bayesian Testing") match brief.md section 7's locked reference-source anchor with high confidence; the specific section/theorem number inside the paper could not be confirmed at authoring time and is stated as such in the docstring and here. **Escalating for human confirmation before this citation is treated as fully verified** — this is the one open item from this plan. The two textbook citations (Hernán & Robins Ch. 1/3; Little & Rubin Ch. 1; Imbens & Rubin Ch. 1 §1.6) are given at chapter/section granularity with higher confidence, since their tables of contents are stable, widely-referenced structures.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Membership check silently broke case-sensitive MISSINGNESS_MECHANISMS**
- **Found during:** Task 1/2 GREEN, first full-suite run (`python3 -m unittest discover -s tests`)
- **Issue:** `normalize(value) not in vocab` lowercases the declared value but not the vocabulary's own keys. `MISSINGNESS_MECHANISMS` intentionally uses uppercase acronym keys (`MCAR`, `MAR`, `MNAR`) per locked decision R-02, unlike every other vocabulary in `dsx/spec.py` (all lowercase snake_case, where this bug is invisible because `normalize(key) == key`). This produced a spurious `DSX-SPEC-082` on the good fixture's `missingness.mechanism: MAR` and broke a pre-existing `TestCLI` integration test that exercises the same fixture through `dsx gate verify`.
- **Fix:** Compare `normalize(value)` against `{normalize(k) for k in vocab}` (the vocabulary's own keys, also normalized) instead of `vocab` directly. Purely additive robustness — a no-op for the other seven membership fields, all of which are already lowercase.
- **Files modified:** `dsx/spec.py`
- **Verification:** Full suite green (228 tests, 2 pre-existing skips); `dsx gate ship --spec examples/good-ANALYSIS-SPEC.yaml` exits 0.
- **Committed in:** `7ded314` (fixed before commit; caught during GREEN, never landed broken)

### Process deviation (not a Rule 1-4 auto-fix — documented per 06-03's precedent)

**Per-task commit granularity collapsed across Tasks 1–3's RED phase, and Tasks 1–2's GREEN phase.** The plan specifies three separate `tdd="true"` tasks, each implying its own RED→GREEN pair. Because the three tasks are additive extensions of the same `validate_structure()` call chain in the same file, and Task 3's decision-record emission is naturally co-located with the validator logic it instruments (not a separable later pass), I authored all 21 new tests in one RED commit and implemented the two validators (including their decision-record emission) in one GREEN commit, leaving Task 3 with only the catalogue-regeneration step as its own commit. Every acceptance-criteria script from all three tasks was run and passed individually before committing. No production behavior differs from what per-task granularity would have produced; only commit-message granularity is coarser than the plan's literal task boundaries. This mirrors 06-03's own documented TDD-granularity deviation (Task 2's fixture-proof tests).

---

**Total deviations:** 1 auto-fixed (Rule 1 — bug), 1 process deviation (commit granularity, no behavioral impact)
**Impact on plan:** The Rule 1 fix was necessary for the good fixture to pass at `verify`/`ship` as R-01/D-11 require; it is a correctness fix, not scope creep. The commit-granularity deviation changes commit-message boundaries only — every acceptance criterion from all three tasks passes.

## Issues Encountered

None beyond the Rule 1 fix above, caught and resolved before any commit landed with the bug.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- `validity_frame:` requiredness and both new blocks' vocabularies are now live at `dsx gate plan` (CRITICAL) through `ship` (HIGH) — the milestone's core value ("a statistically invalid analysis must fail at the gate, before the data is touched") is enforced for the frame layer for the first time.
- `examples/bad-ANALYSIS-SPEC.yaml` now blocks at `plan` with six `DSX-SPEC-081` findings plus its pre-existing defects; `examples/good-ANALYSIS-SPEC.yaml` and `templates/ANALYSIS-SPEC.yaml` both stay clean through all four gate points.
- `dsx/decisions.py` has its first real producer — `report.context["decisions"]` now carries real `DecisionRecord` dicts from a live gate run, ready for plan 06-09's CLI-side `id`/`invocation_id` assignment and file write.
- The D-05 catalogue gate (`gen-finding-catalogue.py --check`) now enforces citation/structural-criterion/test-linkage for all five new codes against the real tree, not just a fixture — any future uncited `DSX-SPEC-08x` or `DSX-PAR-*` code will fail the build immediately.
- **Open item for a human to confirm:** the Deng, Lu & Chen (2016) citation's exact section/theorem locator inside `_validate_inference_shape`'s docstring is flagged as unverified (see Decisions Made above) — author/title/venue/year are correct and match `brief.md`, but the specific section number was not confirmed against the source paper.
- No blockers for 06-07 onward. `git diff --stat dsx/checks/ dsx/cli.py` is empty at every commit in this plan, exactly as scoped (D-13).

---
*Phase: 06-contract-extension-decision-record-paradigm-manifest*
*Completed: 2026-08-08*

## Self-Check: PASSED

- FOUND: dsx/spec.py
- FOUND: tests/test_dsx.py
- FOUND: references/finding-codes.md
- FOUND: .planning/phases/06-contract-extension-decision-record-paradigm-manifest/06-06-SUMMARY.md
- FOUND commit: 46c216d (test(06-06): failing tests for validity_frame/inference shape and decision records)
- FOUND commit: 7ded314 (feat(06-06): validity_frame and inference structural shape validators)
- FOUND commit: c37ba3f (feat(06-06): regenerate finding catalogue for the five new DSX-SPEC-08x codes)
