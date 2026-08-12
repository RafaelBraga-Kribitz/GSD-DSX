---
phase: 07-validity-frame-checks-dsx-val
plan: 05
subsystem: infra
tags: [python, stdlib, unittest, dependence, identification, priors, gate, citation-discipline]

# Dependency graph
requires:
  - phase: 07-validity-frame-checks-dsx-val (plan 04)
    provides: "dsx/frame/val.py's check(spec) dispatcher and DecisionRecord emission pattern, four private helpers shipped"
  - phase: 07-validity-frame-checks-dsx-val (plan 01)
    provides: "dsx.spec.DEPENDENCE_ADMISSIBLE_METHODS, IDENTIFICATION_STRENGTHS, CONSTRAINT_SOURCES vocabularies"
provides:
  - "dsx/frame/val.py — _check_dependence (DSX-VAL-030, CRITICAL) and _check_identification (DSX-VAL-040 CRITICAL / DSX-VAL-041 HIGH)"
  - "dsx/frame/val.py — _PARAMETER_SCALE_CONSTRAINT_SOURCES module constant, the project-defined constraint-source partition"
  - "templates/ANALYSIS-SPEC.yaml repaired: identification.strength changed weak -> strong so dsx init keeps clearing dsx gate plan"
  - "tests/test_known_bad_corpus.py: DSX-VAL-041 added to _INCIDENTAL_GAP_CODES with a cause comment; bayesian fixture itself untouched"
  - "TestValGateSeverity — gate-level proof that DSX-VAL-040 blocks from plan onward and DSX-VAL-041 prints at plan without blocking, then blocks at verify/ship"
affects: [07-06, 07-07]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Each new judgment point (dependence, identification) emits its own gated DecisionRecord in check(), matching plans 07-03/07-04's 'one record per judgment point' precedent; the identification record's choice text distinguishes which of the two mutually-exclusive outcomes (DSX-VAL-040 vs DSX-VAL-041 vs neither) was reached, per REQ-P7-05's repudiation mitigation"
    - "A project-defined vocabulary partition (which CONSTRAINT_SOURCES members carry parameter-scale information) is declared as its own module constant with a comment deriving each classification from the source vocabulary's own description text, then the same project-defined disclosure is repeated verbatim in the consuming function's docstring — so the honesty disclosure survives being read in isolation from either location"
    - "Gate-level severity-split proof exercises the real cli.main() entry point in-process (io.StringIO + redirect_stdout/stderr, matching tests/test_dsx.py's TestCLI._run idiom) against temporary specs cloned from the good fixture with only one sub-block overridden, rather than asserting behaviour at the unit-check level alone — this is what actually proves the roadmap's 'printed but non-blocking at plan, blocking at verify/ship' wording, since dsx/findings.py::emit() routes passing output to stdout and blocking output to stderr, and a naive test checking only the exit code would pass even if the finding were silently dropped"

key-files:
  created: []
  modified:
    - dsx/frame/val.py
    - tests/test_frame_val.py
    - templates/ANALYSIS-SPEC.yaml
    - tests/test_known_bad_corpus.py
    - references/finding-codes.md

key-decisions:
  - "DSX-VAL-030's decision record is computed in check() by re-deriving the same admissible-set membership test _check_dependence uses internally (structure normalized, checked against DEPENDENCE_ADMISSIBLE_METHODS, method family checked for blank/inadmissible) rather than having the helper return a boolean — this duplicates a small amount of logic but matches the existing pattern from _check_unit_triad/_check_unit_drift exactly, keeping the module's style consistent rather than introducing a new return-value convention for only these two helpers."
  - "The identification decision record's choice string names which specific code fired (DSX-VAL-040 or DSX-VAL-041) rather than only 'blocked'/'passed', because the two codes are opposite-severity findings on the same sub-block and a decision-trail reader needs to know which one without cross-referencing the findings list separately — this is the 'rule text distinguishes which of the two outcomes was reached' requirement from the plan's action block, applied to choice as well as rule for clarity."
  - "_PARAMETER_SCALE_CONSTRAINT_SOURCES lives in dsx/frame/val.py, not dsx/spec.py, per the plan's explicit instruction: unlike the dependence map (which Phase 11 keys its own admissibility file on), no later phase keys anything on this partition, so it stays a local judgment in the check module rather than shared infrastructure."
  - "The corpus repair added only DSX-VAL-041 to _INCIDENTAL_GAP_CODES, not the DSX-VAL- prefix to _TARGET_CODE_FAMILIES, exactly as the plan directs — plan 07-07 is where a single specific code (not the whole family) gets added to _TARGET_CODE_FAMILIES when it lands the fixture whose encoded defect that code is."
  - "TestValGateSeverity's Behaviour 5 (every shipped validity-frame code reachable from a profile) is implemented by intersecting dsx.cli.CHECKS with dsx.cli.GATE_PROFILES on the single 'val' check name, not by enumerating individual DSX-VAL-* codes — since every code in this module fires through the one check(spec) dispatcher, proving 'val' is reachable from a profile proves every code is, and the assertion keeps holding without editing as plan 07-06 adds three more codes (matching the plan's explicit instruction to derive this from registered checks and profile tuples rather than a hand-written code list)."

requirements-completed: [REQ-P7-04, REQ-P7-05]

coverage:
  - id: D1
    description: "DSX-VAL-030 (CRITICAL): fires when validity_frame.dependence.structure names a member of DEPENDENCE_ADMISSIBLE_METHODS and method_family_required is blank or inadmissible for that structure; skips a blank structure, structure 'none' (declared independence), an out-of-vocabulary structure, and an absent/malformed dependence sub-block; detail names the full admissible set for the declared structure at the point of failure; every structure in the admissible map is exercised by test"
    requirement: "REQ-P7-04"
    verification:
      - kind: unit
        ref: "tests/test_frame_val.py::TestValDependenceIdentification::test_dependence_structure_with_blank_method_family_fires_critical_val_030, test_dependence_structure_with_admissible_method_family_produces_no_val_030, test_dependence_structure_with_inadmissible_method_family_names_the_admissible_set, test_dependence_structure_none_with_blank_method_family_produces_no_val_030, test_absent_dependence_subblock_produces_no_val_030, test_out_of_vocabulary_dependence_structure_produces_no_val_030, test_every_dependence_admissible_map_structure_is_exercised_at_least_once, test_malformed_dependence_subblock_produces_no_finding_and_does_not_raise, test_dependence_judgment_point_appends_exactly_one_decision_record"
        status: pass
    human_judgment: false
  - id: D2
    description: "DSX-VAL-040 (CRITICAL): fires when identification.strength is weak and constraint_source is none. DSX-VAL-041 (HIGH): fires when strength is strong and constraint_source is a member of the project-defined _PARAMETER_SCALE_CONSTRAINT_SOURCES set (informative_priors, penalisation, design_restriction, hierarchical_pooling). The two codes are mutually exclusive by construction; weak+real-constraint, strong+none, moderate (any constraint), out-of-vocabulary values, and blank values all produce neither code."
    requirement: "REQ-P7-05"
    verification:
      - kind: unit
        ref: "tests/test_frame_val.py::TestValDependenceIdentification::test_weak_identification_with_no_constraint_fires_critical_val_040_and_no_val_041, test_weak_identification_with_a_real_constraint_produces_neither_identification_code, test_strong_identification_with_informative_priors_fires_high_val_041_and_no_val_040, test_strong_identification_with_each_parameter_scale_constraint_fires_val_041, test_strong_identification_with_constraint_source_none_produces_neither_identification_code, test_moderate_identification_produces_neither_identification_code_with_any_constraint, test_out_of_vocabulary_identification_strength_or_constraint_produces_neither_code, test_blank_identification_strength_or_constraint_source_produces_neither_code, test_malformed_identification_subblock_produces_no_finding_and_does_not_raise, test_identification_judgment_point_appends_one_decision_record_distinguishing_outcomes"
        status: pass
    human_judgment: false
  - id: D3
    description: "Both identification codes' docstrings and the _PARAMETER_SCALE_CONSTRAINT_SOURCES module constant's comment carry the D-05 honesty disclosure verbatim in substance: no published source partitions CONSTRAINT_SOURCES into carries/does-not-carry parameter-scale information; Gelman, Simpson & Betancourt (2017) support the premise and section 1.2's taxonomy covers two of the four members, but publish no such four-way partition and design_restriction has no counterpart in their paper at all. Cited by section number AND title together (section 3.3, section 1.2), with an explicit UNVERIFIED flag on whether the typeset MDPI version's section numbers match the arXiv version."
    verification:
      - kind: unit
        ref: "python3 -c \"import dsx.frame.val as v; d=v._check_identification.__doc__; assert 'project-defined' in d and 'UNVERIFIED' in d\" (exit 0, part of Task 2 acceptance criteria)"
        status: pass
    human_judgment: true
    rationale: "Citation-accuracy review (whether Gelman, Simpson & Betancourt's paper, section numbers and section titles are correctly attributed, and whether the constraint-source classification derivation is a fair reading of CONSTRAINT_SOURCES' own description text) is a human judgment call per this plan's prohibitions and threat T-7-07; automated tests confirm the Citation:/Structural criterion: regex markers, the '# D-05: DSX-VAL-040'/'DSX-VAL-041' test markers, and the literal strings 'project-defined'/'UNVERIFIED' are present, but cannot confirm the underlying bibliographic and derivational claims are accurate."
  - id: D4
    description: "templates/ANALYSIS-SPEC.yaml's identification.strength changed from weak to strong (constraint_source stays none) so the scaffold no longer trips its own DSX-VAL-040; dsx init's copy still clears dsx gate plan; dsx gate ship on the raw template still fails (scaffold-must-be-edited proof intact)"
    requirement: "REQ-P7-05"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestCLI::test_template_validity_frame_and_inference_pass_gate_plan, test_template_validates_structurally_as_a_scaffold, test_template_validity_frame_and_inference_pass_dsx_validate; tests/test_dsx.py::TestFalsifierLexicon::test_template_angle_bracket_falsifier_is_not_discriminating; tests/test_dsx.py::TestLoader::test_bundled_parser_handles_the_template_subset; tests/test_dsx.py::TestSpecStructure::test_template_validity_frame_and_inference_round_trip, test_template_vocabulary_placeholders_are_legal_members"
        status: pass
    human_judgment: false
  - id: D5
    description: "The bayesian-continuous-monitoring known-bad fixture's incidental DSX-VAL-041 finding (strength: strong + constraint_source: informative_priors, both true declarations) is documented in tests/test_known_bad_corpus.py's _INCIDENTAL_GAP_CODES with a cause comment, and the fixture file itself is unedited; the corpus's positive gate guarantee (clears plan/execute) and ship-gate documentation guarantee both continue to hold; DSX-VAL- is not added to _TARGET_CODE_FAMILIES"
    requirement: "REQ-P7-05"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py::TestKnownBadCorpus::test_every_spec_passes_the_critical_threshold_gate_points, test_ship_gate_findings_are_all_documented_incidental_corpus_gaps, test_incidental_allowlist_names_no_target_family_code"
        status: pass
    human_judgment: false
  - id: D6
    description: "Gate-level proof of the roadmap's severity wording: DSX-VAL-040 blocks dsx gate plan; DSX-VAL-041 exits 0 at dsx gate plan while still printed on stdout, then blocks dsx gate verify and dsx gate ship with the code visible on stderr; neither validity-frame code appears at dsx gate execute (val is not in that profile); the reachability proof is derived from GATE_PROFILES/CHECKS intersection, not a hand-written code list"
    requirement: "REQ-P7-05"
    verification:
      - kind: unit
        ref: "tests/test_frame_val.py::TestValGateSeverity::test_weak_no_constraint_spec_blocks_gate_plan_naming_val_040, test_strong_informative_priors_spec_passes_gate_plan_but_still_prints_val_041, test_strong_informative_priors_spec_blocks_gate_verify_and_gate_ship_naming_val_041, test_neither_identification_spec_produces_a_validity_frame_finding_at_gate_execute, test_val_check_is_reachable_from_at_least_one_gate_profile"
        status: pass
    human_judgment: false

duration: ~6min
completed: 2026-08-12
status: complete
---

# Phase 7 Plan 5: DSX-VAL-030/040/041 Dependence and Identification Checks Summary

**`dsx/frame/val.py` gains the dependence check (`DSX-VAL-030`, CRITICAL — a declared dependence structure with no admissible method family, naming the full admissible set at the point of failure) and the identification pair (`DSX-VAL-040` CRITICAL for weak identification with no constraint, `DSX-VAL-041` HIGH for strong identification also carrying a project-defined parameter-scale constraint), landing in the same commits as repairs to the template and the bayesian corpus fixture's documentation that the new checks would otherwise have broken, plus a gate-level proof that the roadmap's severity-split wording — `DSX-VAL-041` printed but non-blocking at plan, blocking at verify/ship — actually holds through the real CLI.**

## Performance

- **Duration:** ~6 min (git commit span 17:22:43–17:28:48 on 2026-08-12; does not include the reading/design time before the first commit)
- **Tasks:** 3
- **Files modified:** 5 (`dsx/frame/val.py`, `tests/test_frame_val.py`, `templates/ANALYSIS-SPEC.yaml`, `tests/test_known_bad_corpus.py`, `references/finding-codes.md`)

## Accomplishments

- `DSX-VAL-030` (CRITICAL): fires when `validity_frame.dependence.structure` is a member of `dsx.spec.DEPENDENCE_ADMISSIBLE_METHODS` (`clustered`, `repeated_measures`, `temporal`, `spatial`, `hierarchical`) and `method_family_required` is either blank or does not belong to that structure's admissible set. Skips a blank structure, structure `none` (declared independence — the nothing-to-validate case), and an out-of-vocabulary structure (`DSX-SPEC-082`'s territory, avoiding a double report). The finding's `detail` distinguishes "nothing declared" from "declared but does not address it" and names the full admissible set in both cases — the one place an author sees the map's contents at the point of failure. Docstring cites Cameron & Miller (2015) for `clustered`/`repeated_measures`/`temporal`/`spatial` and Gelman & Hill (2007) for `hierarchical`, with an explicit UNVERIFIED locator disclosure for both (author/year/title/venue confirmed, internal section/chapter locators not).
- `DSX-VAL-040`/`DSX-VAL-041` (CRITICAL/HIGH): a new module constant `_PARAMETER_SCALE_CONSTRAINT_SOURCES` classifies four of `CONSTRAINT_SOURCES`' five members (`informative_priors`, `penalisation`, `design_restriction`, `hierarchical_pooling` — `none` deliberately absent) as carrying parameter-scale information, derived from each member's own description text in `dsx.spec.CONSTRAINT_SOURCES`. `DSX-VAL-040` fires when `identification.strength` is `weak` and `constraint_source` is `none` — an estimate nothing anchors. `DSX-VAL-041` fires when `strength` is `strong` and `constraint_source` is a member of the new constant — a design that rules out confounding also carrying a scale-informing constraint, a tension to reconcile rather than an assertion of error, which is why it is HIGH rather than CRITICAL. The two codes are mutually exclusive by construction (one requires `weak`, the other `strong`). Both the constant's comment and the docstring state plainly, twice, that this four-against-one partition is **project-defined** — no published source draws it; Gelman, Simpson & Betancourt (2017) support the underlying premise and their section 1.2 taxonomy covers two of the four members, but they publish no such partition and `design_restriction` has no counterpart in their paper at all. Cited by section number **and** title together (section 3.3, section 1.2) so the locator survives either the arXiv preprint or the typeset MDPI journal version, with an explicit UNVERIFIED flag on whether the two versions' section numbers match.
- `templates/ANALYSIS-SPEC.yaml`'s `identification.strength` changed from `weak` to `strong` (the previous value was the literal `DSX-VAL-040` trigger, since `constraint_source` stays `none`); the `evidence` placeholder now asks for the design-based support a strong claim implies, and a comment states the value is an example to replace. `dsx init`'s scaffold copy still clears `dsx gate plan`; `dsx gate ship` on the raw template still fails (scaffold-must-be-edited proof intact).
- `tests/test_known_bad_corpus.py`'s `_INCIDENTAL_GAP_CODES` gains `DSX-VAL-041` with an inline cause comment: the bayesian-continuous-monitoring fixture's `strength: strong` + `constraint_source: informative_priors` is a true, honest declaration (it is a Bayesian analysis and does use informative priors), and the finding is a correct secondary observation about a fixture built to demonstrate a different defect (uncontrolled continuous monitoring), not the encoded defect itself. The fixture file is untouched, per D-14's resolution recorded in this plan. `DSX-VAL-` is deliberately **not** added to `_TARGET_CODE_FAMILIES` — plan 07-07 adds a single specific code there when it lands the fixture whose encoded defect that code is.
- `TestValGateSeverity` (Task 3, REQ-P7-05): exercises the real `dsx.cli.main()` entry point in-process against temporary specs cloned from the good fixture with only `identification` overridden. Proves a weak/`none` spec blocks `dsx gate plan` naming `DSX-VAL-040`; a strong/`informative_priors` spec exits 0 at `dsx gate plan` while `DSX-VAL-041` is still visible on stdout (the behaviour most likely to be gotten wrong — asserting only the exit code would pass even if the finding were silently dropped); the same spec blocks `dsx gate verify` and `dsx gate ship`, naming `DSX-VAL-041` on stderr; neither spec produces a validity-frame finding at `dsx gate execute` (`val` is not in that profile); and `val` (the single dispatcher for every `DSX-VAL-*` code) is reachable from at least one gate profile, derived by intersecting `dsx.cli.CHECKS` with `dsx.cli.GATE_PROFILES` rather than a hand-written code list.
- `references/finding-codes.md` regenerated after each production-code task; now carries `DSX-VAL-030`, `DSX-VAL-040` and `DSX-VAL-041` in the "Validity frame" section.

## Task Commits

Each task was committed atomically:

1. **Task 1: Ship DSX-VAL-030, the dependence check** - `b54b7b5` (feat)
2. **Task 2: Ship DSX-VAL-040 and DSX-VAL-041, and land the template and corpus repairs in the same commit** - `917fa14` (feat)
3. **Task 3: Prove the severity split behaves as the roadmap specifies at each gate point** - `a50c945` (test)

**Plan metadata:** committed alongside this SUMMARY (worktree mode — orchestrator finalizes STATE.md/ROADMAP.md after merge)

_Note: per this plan's `tdd="true"` task structure (matching plans 07-01/07-03/07-04's precedent), each task's `<action>` describes adding the check/repair/test code as one unit rather than a separate RED-then-GREEN pair, so Tasks 1 and 2 landed as single verified-green `feat` commits and Task 3 as a single `test` commit. See "TDD Gate Compliance" below._

## Files Created/Modified

- `dsx/frame/val.py` - Added `_check_dependence()` (`DSX-VAL-030`) and `_check_identification()` (`DSX-VAL-040`/`DSX-VAL-041`), each wired into `check()`'s dispatcher with its own gated `DecisionRecord`; added `_DEPENDENCE_CITATION`, `_IDENTIFICATION_CITATION` and `_PARAMETER_SCALE_CONSTRAINT_SOURCES` module constants; imported `CONSTRAINT_SOURCES`, `DEPENDENCE_ADMISSIBLE_METHODS`, `IDENTIFICATION_STRENGTHS` from `dsx.spec`; updated the module docstring's code-count description
- `tests/test_frame_val.py` - `TestValDependenceIdentification` (19 tests: 9 for `DSX-VAL-030` including the D-05 marker and a test method containing "dependence", 10 for `DSX-VAL-040`/`DSX-VAL-041` including both D-05 markers); `TestValGateSeverity` (5 tests: the plan-blocks, plan-prints-but-passes, verify/ship-blocks, execute-silent and profile-reachability behaviours, with a test method containing "identification"); imports `cli`, `io`, `json`, `tempfile`, `redirect_stderr`/`redirect_stdout`, `load`
- `templates/ANALYSIS-SPEC.yaml` - `identification.strength` changed `weak` → `strong`; `evidence` placeholder reworded; example-to-replace comment added; vocabulary hint comments on those lines left unchanged
- `tests/test_known_bad_corpus.py` - `DSX-VAL-041` added to `_INCIDENTAL_GAP_CODES` with a cause comment; `_TARGET_CODE_FAMILIES` unchanged
- `references/finding-codes.md` - Regenerated twice (once per new-code task); now lists `DSX-VAL-030` (CRITICAL), `DSX-VAL-040` (CRITICAL) and `DSX-VAL-041` (HIGH)

## Decisions Made

See `key-decisions` in the frontmatter for the full list. In brief: the dependence and identification decision records duplicate a small amount of membership-test logic between the helper functions and `check()`'s record-emission code, matching the module's existing style from plan 07-04 rather than introducing a new return-value convention; the identification decision record's `choice` text names the specific code (`DSX-VAL-040`/`DSX-VAL-041`) that fired, not only "blocked"/"passed", since the two codes are opposite-severity findings on the same sub-block; `_PARAMETER_SCALE_CONSTRAINT_SOURCES` stays local to `dsx/frame/val.py` per the plan's explicit instruction (no later phase keys anything on it, unlike the dependence map); and the gate-profile reachability test derives its assertion from `CHECKS`/`GATE_PROFILES` intersection rather than a hand-written code list, so it keeps holding as plan 07-06 adds three more codes.

## Deviations from Plan

None — plan executed exactly as written. One correction was applied mid-authoring before any commit landed (not a deviation from shipped behaviour, since it was caught before the first commit): the initial gate-level test for the "prints at plan without blocking" behaviour checked `stderr` for `DSX-VAL-041`, but `dsx/findings.py::emit()` routes passing output (exit code 0) to stdout and blocking output to stderr — the test was corrected to check `stdout` for that specific assertion before Task 3's commit, and the `execute`-profile test checks the concatenation of both streams since it only needs to prove *absence*, not which stream. No production code was affected; this is a test-authoring correction, not a Rule 1–4 deviation, since it never reached a commit in the wrong state.

## Issues Encountered

- **Repeated from plan 07-04's SUMMARY, and confirmed to still apply:** the plan's own acceptance-criteria one-liners using `str(f[0].severity)=='CRITICAL'`/`=='HIGH'` do not hold in this environment's Python (3.14). Since Python 3.11, `IntEnum.__str__` prints the underlying int value, not the member name. All verification in this plan's tasks used the codebase's own idiom, `finding.severity == Severity.CRITICAL` / `Severity.HIGH`, which is what the acceptance criteria intended and what the rest of the test suite already uses — confirmed correct, no code defect. This was called out as a defect in the plan's one-liners (not in the shipped code) by the 07-04 SUMMARY and is repeated here per that SUMMARY's own note that it would recur in 07-05/07-06.
- **`gen-finding-catalogue.py`'s pre-existing double-declaration warnings** (`DSX-COH-030`, `DSX-SPEC-070` x3, `DSX-VAL-021`) are unchanged from the 07-04 baseline; no new double-declaration warning was introduced by this plan's two new report.add() call sites (`DSX-VAL-030` has one call site, `DSX-VAL-040`/`DSX-VAL-041` each have one call site, so no duplicate-title collision).

## User Setup Required

None - no external service configuration required. D-01 holds: only the Python 3.9+ standard library, plus already-shipped `dsx.spec` vocabularies, were used across all three tasks; no new dependency was added.

## Next Phase Readiness

- `dsx/frame/val.py`'s `check()` dispatcher now calls six private helpers (`_check_estimand_completeness`, `_check_estimand_falsifiability`, `_check_unit_triad`, `_check_unit_drift`, `_check_dependence`, `_check_identification`); plan 07-06 (sampling frame, missingness, measurement) adds the remaining three as one call each, per the established pattern.
- Verified before finishing: `python3 -m unittest discover -s tests` — 386 tests, OK (2 skipped, same 2 as baseline; 371 after Task 1, 381 after Task 2, 386 after Task 3, up from 371's baseline of 362 at the start of this plan); `python3 scripts/gen-finding-catalogue.py --check` — exit 0, "finding catalogue is current" (same pre-existing warnings as the 07-04 baseline, no new ones).
- `python3 -m dsx.cli gate plan|execute|verify|ship --spec examples/good-ANALYSIS-SPEC.yaml` all exit 0; `gate plan --spec templates/ANALYSIS-SPEC.yaml` exits 0 (the `dsx init` regression holds); `gate ship --spec templates/ANALYSIS-SPEC.yaml` exits 1 (scaffold proof intact).
- `python3 -m unittest tests.test_known_bad_corpus -v` — 13 tests, OK; the bayesian fixture's incidental `DSX-VAL-041` gap is documented and does not block `dsx gate plan`/`dsx gate execute` (the corpus's positive guarantee) nor go undocumented at `dsx gate ship`.
- `git status --short` is clean after each commit (no stray untracked files); `dsx/checks/design.py` and `examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml` were never staged in any of this plan's three commits, confirmed by `git status --short` showing only the five files named above across the whole plan, and by `TestValExpUnitsDisjointness::test_design_checks_py_content_is_unmodified_since_phase_start`'s pinned content hash still passing.
- No blockers for plan 07-06, this phase's other declared consumer of `dsx/frame/val.py`'s now-six-helper dispatcher. Plan 07-07 (the weak-identification-mmm known-bad fixture, D-15) can now rely on `DSX-VAL-040` actually shipping.

## TDD Gate Compliance

This plan's frontmatter sets `type: tdd`, and each task individually carries `tdd="true"`. Consistent with plans 07-01/07-03/07-04's precedent, Tasks 1 and 2's `<action>` describe adding the check/repair/test code as one unit rather than a separate RED-then-GREEN sequence, so each landed as a single verified-green `feat` commit rather than a `test(...)`/`feat(...)` pair. Task 3 is itself entirely a test addition (no new production code), so it committed as a single `test` commit. Every test in all three tasks was written against the plan's `<behavior>` blocks, run, and confirmed passing before its task's commit. No commit in this plan's git log matches a bare `^test\(07-05` immediately followed by production code in the same commit for Tasks 1/2, by task design.

---
*Phase: 07-validity-frame-checks-dsx-val*
*Completed: 2026-08-12*

## Self-Check: PASSED

- FOUND: dsx/frame/val.py
- FOUND: tests/test_frame_val.py
- FOUND: templates/ANALYSIS-SPEC.yaml
- FOUND: tests/test_known_bad_corpus.py
- FOUND: references/finding-codes.md
- FOUND: .planning/phases/07-validity-frame-checks-dsx-val/07-05-SUMMARY.md
- FOUND commit b54b7b5 (Task 1)
- FOUND commit 917fa14 (Task 2)
- FOUND commit a50c945 (Task 3)
