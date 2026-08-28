---
status: complete
phase: 07-validity-frame-checks-dsx-val
source: [07-01-SUMMARY.md, 07-02-SUMMARY.md, 07-03-SUMMARY.md, 07-04-SUMMARY.md, 07-05-SUMMARY.md, 07-06-SUMMARY.md, 07-07-SUMMARY.md, 07-08-SUMMARY.md]
started: 2026-08-12T00:00:00Z
updated: 2026-08-14T00:00:00Z
---

## Current Test
<!-- OVERWRITE each test - shows where we are -->

[testing complete]

## Tests

### 1. Citation honesty — dependence-method map and design_effect()
expected: Citation locators in the DEPENDENCE_ADMISSIBLE_METHODS comment and the design_effect() docstring are honest — verified locators stated as verified, unverified locators explicitly flagged rather than invented, and Conley (1999) recorded as a deliberate non-citation
result: pass
coverage_id: D4
source_plan: 07-01
reason: human_judgment
read:
  - "dsx/spec.py:215-232 — the comment block above DEPENDENCE_ADMISSIBLE_METHODS"
  - "dsx/mathx.py:430-460 — the design_effect() docstring"
rationale: "Citation-accuracy and honesty-labelling review is a human judgment call per this plan's threat model (T-7-07) and prohibitions; automated tests can confirm the UNVERIFIED string is present but cannot confirm the underlying bibliographic claims are accurate."

### 2. Citation honesty — estimand decomposition disclosed as project-defined
expected: Citation text and the estimand-decomposition/unverified-locator honesty disclosures in the docstrings and DecisionRecord are accurate and not laundered from a plausible-sounding but uncited source
result: pass
coverage_id: D7
source_plan: 07-03
reason: human_judgment
read:
  - "dsx/frame/val.py:~560-600 — the _check_estimand_completeness docstring"
rationale: "Citation-accuracy review is a human judgment call per this plan's threat model (T-7-07) and prohibitions; automated tests confirm the Citation:/Structural criterion: regex markers are present but cannot confirm the underlying bibliographic claims are accurate."

### 3. Build plumbing shipped with the first DSX-VAL finding
expected: Build plumbing lands in the same commit as the first DSX-VAL finding: DSX-VAL removed from paradigm.py's _NOT_SHIPPED, val registered in CHECKS and the plan/verify/ship (not execute) gate profiles, DSX-VAL PREFIX_GROUPS entry and D-05 allow-list prefix added, references/finding-codes.md regenerated
result: pass
coverage_id: D5
note: "Coverage block malformed (verification[0] missing status:). All clauses re-verified directly during UAT: _NOT_SHIPPED has no DSX-VAL entry; cli.py:79 registers val; GATE_PROFILES has val in plan/verify/ship and not execute; PREFIX_GROUPS + _D05_ALLOWLIST_PREFIXES both carry DSX-VAL-; catalogue --check exits 0; git log -S confirms commit 3633222 carries both val.py and the plumbing."
source_plan: 07-03
reason: validation_failed
requirement: REQ-P7-01
read:
  - "Already re-run by this session: full suite 419 passed / 378 subtests passed;"
  - "python scripts/gen-finding-catalogue.py --check -> exit 0 ('finding catalogue is current')"

### 4. Citation honesty — unit-triad citation (Kish / Cochrane / Hernan & Robins)
expected: Citation text (Kish 1965, Cochrane Handbook v6.5, Hernan & Robins 2020) and the UNVERIFIED-locator/fixed-illustration honesty disclosures in both new docstrings are accurate and not laundered from a plausible-sounding but uncited source
result: pass
retested_at: 2026-08-14
retest_note: "User confirmed the reworded citation against the four live passages read back from HEAD and against 07-DISCUSSION-LOG.md:102-103. The section-8.2/UNVERIFIED contradiction is gone; all four sites name the same locator set."
retest_of: "issue (2026-08-12) — see prior_report below"
prior_report: "Citation contradiction (defect found). val.py:79 states 'section 8.2, page 258' while val.py:83-84 says the section number is UNVERIFIED and 'do not invent one'. mathx.py omits the section number and is self-consistent. D-05 violation."
prior_severity: major
remediated_by: 07-08-PLAN.md (gap G-07-4, commits adc1ad2 + cb074c4)
coverage_id: D6
source_plan: 07-04
reason: human_judgment
read:
  - "dsx/frame/val.py:78-85 — the _UNIT_TRIAD_CITATION constant (reworded)"
  - "dsx/frame/val.py:671-677 — the _check_unit_triad docstring Citation: paragraph (reworded)"
  - "dsx/mathx.py:461-468 — the design_effect docstring Citation: paragraph (now names section 8.2)"
  - "brief.md section 7 — the Kish sentence (reworded to match)"
rationale: "Citation-accuracy review is a human judgment call per this plan's threat model (T-7-04) and prohibitions; automated tests confirm the Citation:/Reference value:/Structural criterion: regex markers and the '# D-05: <CODE>' test markers are present, but cannot confirm the underlying bibliographic claims are accurate."

### 5. Citation honesty — identification citation and the four-against-one partition
expected: Both identification codes' docstrings and the _PARAMETER_SCALE_CONSTRAINT_SOURCES module constant's comment carry the D-05 honesty disclosure verbatim in substance: no published source partitions CONSTRAINT_SOURCES into carries/does-not-carry parameter-scale information; Gelman, Simpson & Betancourt (2017) support the premise and section 1.2's taxonomy covers two of the four members, but publish no such four-way partition and design_restriction has no counterpart in their paper at all. Cited by section number AND title together (section 3.3, section 1.2), with an explicit UNVERIFIED flag on whether the typeset MDPI version's section numbers match the arXiv version.
result: pass
coverage_id: D3
source_plan: 07-05
note: "User verified all three sites. Section numbers are hedged by pairing number with title, and the UNVERIFIED flag is scoped to arXiv-vs-MDPI version renumbering rather than to an unconfirmed locator — deliberate defensive citation, not a test-4-style contradiction."
reason: human_judgment
read:
  - "dsx/frame/val.py:103-115 — the _IDENTIFICATION_CITATION constant"
  - "dsx/frame/val.py:141-160 — the _PARAMETER_SCALE_CONSTRAINT_SOURCES constant and its comment"
  - "dsx/frame/val.py:~900-960 — the _check_identification docstring"
rationale: "Citation-accuracy review (whether Gelman, Simpson & Betancourt's paper, section numbers and section titles are correctly attributed, and whether the constraint-source classification derivation is a fair reading of CONSTRAINT_SOURCES' own description text) is a human judgment call per this plan's prohibitions and threat T-7-07; automated tests confirm the Citation:/Structural criterion: regex markers, the '# D-05: DSX-VAL-040'/'DSX-VAL-041' test markers, and the literal strings 'project-defined'/'UNVERIFIED' are present, but cannot confirm the underlying bibliographic and derivational claims are accurate."

### 6. Citation honesty — weak-identification-mmm post-mortem source (Chan & Perry 2017)
expected: The post-mortem's source is a real, verified, primary/peer-reviewed publication describing weak identification in a marketing-mix model, and the two project-defined partitions plus the unverified citation locators are honestly disclosed rather than presented as published results
result: pass
coverage_id: D4
source_plan: 07-07
note: "User spot-checked the primary PDF: authors, year, title, venue and both URLs confirmed; the three quoted strings match verbatim; all four section numbers and titles (4.1.1, 4.1.2, 4.2, 4.3.2) exist as cited. Absence of an UNVERIFIED flag is justified because the document was actually read rather than inferred. Qualification recorded: the expected wording 'primary/peer-reviewed' was read as primary OR peer-reviewed. What shipped is a Google Research technical report, disclosed as such and argued admissible on structure (abstract, numbered sections, reference list) versus the inadmissible vendor-blog class. A stricter reading requiring peer review as well would not be satisfied; the disclosure makes the call transparent either way."
reason: human_judgment
read:
  - "examples/known-bad/weak-identification-mmm-POSTMORTEM.md — the 'Source' section"
rationale: "Whether a citation is genuinely admissible under D-05, and whether a docstring's honesty disclosure reads as adequate, are judgment calls this plan's own human-check step assigns to a human reader — see the 'Human Judgment Items' section below for exactly which files and passages to read."

### 7. [07-01/D1] DEPENDENCE_ADMISSIBLE_METHODS map — five structures, every value a VARIANCE_ADJUSTMENTS subset, 'none' absent,...
expected: DEPENDENCE_ADMISSIBLE_METHODS map — five structures, every value a VARIANCE_ADJUSTMENTS subset, 'none' absent, delta_method admissible nowhere, excluded from describe_vocabulary()
result: pass
source: automated
coverage_id: D1
source_plan: 07-01
requirement: REQ-P7-04
verification:
  - unit: "tests/test_dsx.py::TestDependenceAdmissibleMethods (5 tests)" (pass)

### 8. [07-01/D2] Falsifier placeholder/refusal detector and discrimination classifier — blank, angle-bracket placeholder, refus...
expected: Falsifier placeholder/refusal detector and discrimination classifier — blank, angle-bracket placeholder, refusal token, prose-without-predicate, numeric-token-only, and the 'none identified' non-refusal edge case, plus a DoS timing guard
result: pass
source: automated
coverage_id: D2
source_plan: 07-01
requirement: REQ-P7-01
verification:
  - unit: "tests/test_dsx.py::TestFalsifierLexicon (8 tests)" (pass)

### 9. [07-01/D3] design_effect() matches the Cochrane Handbook's published worked example (1.576) and raises ValueError on both...
expected: design_effect() matches the Cochrane Handbook's published worked example (1.576) and raises ValueError on both out-of-range boundary inputs
result: pass
source: automated
coverage_id: D3
source_plan: 07-01
requirement: REQ-P7-02
verification:
  - unit: "tests/test_dsx.py::TestMath::test_design_effect_* (5 tests)" (pass)

### 10. [07-02/D1] brief.md section 7 lists every source a Phase 7 docstring will cite (six new sources), pins the Lohr and Littl...
expected: brief.md section 7 lists every source a Phase 7 docstring will cite (six new sources), pins the Lohr and Little and Rubin editions, and labels four locators unverified
result: pass
source: automated
coverage_id: D1
source_plan: 07-02
requirement: REQ-P7-05
verification:
  - unit: "scripts/check_brief_refs.py" (pass)

### 11. [07-02/D2] the unsourced 3.45 design-effect worked example in .planning/research/FEATURES.md is replaced with the Cochran...
expected: the unsourced 3.45 design-effect worked example in .planning/research/FEATURES.md is replaced with the Cochrane Handbook's own published value (1.576), and the retired value survives only inside an explicit D-10 correction note
result: pass
source: automated
coverage_id: D2
source_plan: 07-02
requirement: REQ-P7-02
verification:
  - unit: "tests.test_known_bad_corpus (python3 -m unittest tests.test_known_bad_corpus -v)" (pass)
  - other: "python3 -c \'... assert 'Worked published example' not in t or '1.576' in t.split(...)[1][:600]\'" (pass)

### 12. [07-03/D1] dsx/frame/val.py: check(spec) -> Report(check='val'), degrading to an empty report on an absent or non-dict va...
expected: dsx/frame/val.py: check(spec) -> Report(check='val'), degrading to an empty report on an absent or non-dict validity_frame block with no traceback
result: pass
source: automated
coverage_id: D1
source_plan: 07-03
requirement: REQ-P7-01
verification:
  - unit: "tests/test_frame_val.py::TestValEstimand::test_check_returns_report_named_val, test_missing_validity_frame_key_produces_no_findings_and_does_not_raise, test_non_dict_validity_frame_and_estimand_degrade_to_no_findings" (pass)

### 13. [07-03/D2] DSX-VAL-010 (CRITICAL): fires exactly once, naming every blank of quantity/population/contrast/time_window in ...
expected: DSX-VAL-010 (CRITICAL): fires exactly once, naming every blank of quantity/population/contrast/time_window in detail, with where=spec.validity_frame.estimand; falsifier is excluded from this check entirely
result: pass
source: automated
coverage_id: D2
source_plan: 07-03
requirement: REQ-P7-01
verification:
  - unit: "tests/test_frame_val.py::TestValEstimand::test_blank_quantity_produces_exactly_one_critical_val_010, test_three_blank_fields_produce_one_val_010_naming_all_three, test_complete_discriminating_estimand_produces_no_findings" (pass)

### 14. [07-03/D3] DSX-VAL-011 (HIGH): fires on blank falsifier, angle-bracket placeholder, refusal token, and non-discriminating...
expected: DSX-VAL-011 (HIGH): fires on blank falsifier, angle-bracket placeholder, refusal token, and non-discriminating prose; does not fire on the good fixture's real falsifier; a blank falsifier fires only DSX-VAL-011, never DSX-VAL-010 too
result: pass
source: automated
coverage_id: D3
source_plan: 07-03
requirement: REQ-P7-01
verification:
  - unit: "tests/test_frame_val.py::TestValEstimand::test_blank_falsifier_produces_exactly_one_high_val_011_and_no_val_010, test_angle_bracket_placeholder_falsifier_produces_val_011, test_refusal_token_falsifier_produces_val_011, test_non_discriminating_prose_falsifier_produces_val_011, test_good_fixture_falsifier_produces_no_val_011" (pass)

### 15. [07-03/D4] One deterministic decision record per estimand judgment, layer=deterministic, empty id/invocation_id, non-empt...
expected: One deterministic decision record per estimand judgment, layer=deterministic, empty id/invocation_id, non-empty counterfactual
result: pass
source: automated
coverage_id: D4
source_plan: 07-03
requirement: REQ-P7-01
verification:
  - unit: "tests/test_frame_val.py::TestValEstimand::test_estimand_judgment_point_appends_exactly_one_decision_record" (pass)

### 16. [07-03/D6] No code path in dsx/frame/val.py reads the declared inference paradigm; the boundary test proves both its own ...
expected: No code path in dsx/frame/val.py reads the declared inference paradigm; the boundary test proves both its own detectors fire against synthetic violations and the real module scans clean
result: pass
source: automated
coverage_id: D6
source_plan: 07-03
requirement: REQ-P7-09
verification:
  - unit: "tests/test_frame_boundary.py::TestFrameParadigmReadBoundary (5 tests)" (pass)

### 17. [07-04/D1] DSX-VAL-020 (CRITICAL): fires when validity_frame.units.observation is finer than units.assignment (D-08 plain...
expected: DSX-VAL-020 (CRITICAL): fires when validity_frame.units.observation is finer than units.assignment (D-08 plain string inequality) and dependence.method_family_required is blank; does not fire when either unit is blank, when the two units match, or when a method family is declared; detail quantifies the consequence via dsx.mathx.design_effect's Cochrane worked value (1.576), explicitly labelled a fixed illustration
result: pass
source: automated
coverage_id: D1
source_plan: 07-04
requirement: REQ-P7-02
verification:
  - unit: "tests/test_frame_val.py::TestValUnits::test_finer_observation_with_no_method_family_fires_critical_units_020, test_finer_observation_with_declared_method_family_produces_no_units_020, test_matching_observation_and_assignment_produces_no_units_020_regardless_of_method, test_blank_observation_or_blank_assignment_produces_no_units_020, test_same_unit_named_two_ways_fires_units_020_with_alignment_remedy, test_units_020_detail_carries_the_deff_formula_and_illustration_wording, test_malformed_units_subblock_produces_no_finding_and_does_not_raise, test_unit_triad_judgment_point_appends_exactly_one_decision_record" (pass)

### 18. [07-04/D2] templates/ANALYSIS-SPEC.yaml's three unit placeholders unified to one string, so dsx init's scaffold copy stil...
expected: templates/ANALYSIS-SPEC.yaml's three unit placeholders unified to one string, so dsx init's scaffold copy still clears dsx gate plan after DSX-VAL-020 ships; ship still fails (scaffold proof intact)
result: pass
source: automated
coverage_id: D2
source_plan: 07-04
requirement: REQ-P7-02
verification:
  - unit: "tests/test_dsx.py::TestCLI::test_template_validity_frame_and_inference_pass_gate_plan, test_template_validates_structurally_as_a_scaffold; tests/test_dsx.py::TestSpecStructure::test_template_validity_frame_and_inference_round_trip, test_template_vocabulary_placeholders_are_legal_members" (pass)

### 19. [07-04/D3] examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml repaired (structure=clustered, cluster_var=us...
expected: examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml repaired (structure=clustered, cluster_var=user, method_family_required=cluster_robust) so it blocks only on its own encoded interference defect, not on pseudo-replication
result: pass
source: automated
coverage_id: D3
source_plan: 07-04
requirement: REQ-P7-02
verification:
  - unit: "tests/test_known_bad_corpus.py::TestKnownBadCorpus::test_every_spec_passes_the_critical_threshold_gate_points, test_ship_gate_findings_are_all_documented_incidental_corpus_gaps, test_incidental_allowlist_names_no_target_family_code" (pass)

### 20. [07-04/D4] DSX-VAL-021 (HIGH): fires once per disagreeing pair (validity_frame.units.assignment vs design.randomization_u...
expected: DSX-VAL-021 (HIGH): fires once per disagreeing pair (validity_frame.units.assignment vs design.randomization_unit; validity_frame.units.analysis vs design.analysis_unit) with normalised comparison; skips whenever either side of a pair is blank; never fires on either canonical fixture or any known-bad corpus fixture
result: pass
source: automated
coverage_id: D4
source_plan: 07-04
requirement: REQ-P7-03
verification:
  - unit: "tests/test_frame_val.py::TestValUnits::test_assignment_vs_randomization_unit_disagreement_fires_high_units_021, test_analysis_vs_design_analysis_unit_disagreement_fires_units_021, test_both_pairs_agreeing_produces_no_units_021, test_blank_design_randomization_unit_produces_no_units_021, test_blank_validity_frame_assignment_produces_no_units_021, test_units_021_normalises_case_and_whitespace_before_comparing, test_units_021_never_fires_on_the_canonical_or_corpus_fixtures" (pass)

### 21. [07-04/D5] DSX-VAL-020 and DSX-EXP-021 (dsx/checks/design.py, unmodified) never both fire on one spec: proven against the...
expected: DSX-VAL-020 and DSX-EXP-021 (dsx/checks/design.py, unmodified) never both fire on one spec: proven against the current bad fixture, against a constructed unit-triad-only defect, across every fixture in the repository, and by construction (editing one block never changes the other check's code set); dsx/checks/design.py's content is pinned to a recorded sha256 hash
result: pass
source: automated
coverage_id: D5
source_plan: 07-04
requirement: REQ-P7-03
verification:
  - unit: "tests/test_frame_val.py::TestValExpUnitsDisjointness (6 tests)" (pass)

### 22. [07-05/D1] DSX-VAL-030 (CRITICAL): fires when validity_frame.dependence.structure names a member of DEPENDENCE_ADMISSIBLE...
expected: DSX-VAL-030 (CRITICAL): fires when validity_frame.dependence.structure names a member of DEPENDENCE_ADMISSIBLE_METHODS and method_family_required is blank or inadmissible for that structure; skips a blank structure, structure 'none' (declared independence), an out-of-vocabulary structure, and an absent/malformed dependence sub-block; detail names the full admissible set for the declared structure at the point of failure; every structure in the admissible map is exercised by test
result: pass
source: automated
coverage_id: D1
source_plan: 07-05
requirement: REQ-P7-04
verification:
  - unit: "tests/test_frame_val.py::TestValDependenceIdentification::test_dependence_structure_with_blank_method_family_fires_critical_val_030, test_dependence_structure_with_admissible_method_family_produces_no_val_030, test_dependence_structure_with_inadmissible_method_family_names_the_admissible_set, test_dependence_structure_none_with_blank_method_family_produces_no_val_030, test_absent_dependence_subblock_produces_no_val_030, test_out_of_vocabulary_dependence_structure_produces_no_val_030, test_every_dependence_admissible_map_structure_is_exercised_at_least_once, test_malformed_dependence_subblock_produces_no_finding_and_does_not_raise, test_dependence_judgment_point_appends_exactly_one_decision_record" (pass)

### 23. [07-05/D2] DSX-VAL-040 (CRITICAL): fires when identification.strength is weak and constraint_source is none. DSX-VAL-041 ...
expected: DSX-VAL-040 (CRITICAL): fires when identification.strength is weak and constraint_source is none. DSX-VAL-041 (HIGH): fires when strength is strong and constraint_source is a member of the project-defined _PARAMETER_SCALE_CONSTRAINT_SOURCES set (informative_priors, penalisation, design_restriction, hierarchical_pooling). The two codes are mutually exclusive by construction; weak+real-constraint, strong+none, moderate (any constraint), out-of-vocabulary values, and blank values all produce neither code.
result: pass
source: automated
coverage_id: D2
source_plan: 07-05
requirement: REQ-P7-05
verification:
  - unit: "tests/test_frame_val.py::TestValDependenceIdentification::test_weak_identification_with_no_constraint_fires_critical_val_040_and_no_val_041, test_weak_identification_with_a_real_constraint_produces_neither_identification_code, test_strong_identification_with_informative_priors_fires_high_val_041_and_no_val_040, test_strong_identification_with_each_parameter_scale_constraint_fires_val_041, test_strong_identification_with_constraint_source_none_produces_neither_identification_code, test_moderate_identification_produces_neither_identification_code_with_any_constraint, test_out_of_vocabulary_identification_strength_or_constraint_produces_neither_code, test_blank_identification_strength_or_constraint_source_produces_neither_code, test_malformed_identification_subblock_produces_no_finding_and_does_not_raise, test_identification_judgment_point_appends_one_decision_record_distinguishing_outcomes" (pass)

### 24. [07-05/D4] templates/ANALYSIS-SPEC.yaml's identification.strength changed from weak to strong (constraint_source stays no...
expected: templates/ANALYSIS-SPEC.yaml's identification.strength changed from weak to strong (constraint_source stays none) so the scaffold no longer trips its own DSX-VAL-040; dsx init's copy still clears dsx gate plan; dsx gate ship on the raw template still fails (scaffold-must-be-edited proof intact)
result: pass
source: automated
coverage_id: D4
source_plan: 07-05
requirement: REQ-P7-05
verification:
  - unit: "tests/test_dsx.py::TestCLI::test_template_validity_frame_and_inference_pass_gate_plan, test_template_validates_structurally_as_a_scaffold, test_template_validity_frame_and_inference_pass_dsx_validate; tests/test_dsx.py::TestFalsifierLexicon::test_template_angle_bracket_falsifier_is_not_discriminating; tests/test_dsx.py::TestLoader::test_bundled_parser_handles_the_template_subset; tests/test_dsx.py::TestSpecStructure::test_template_validity_frame_and_inference_round_trip, test_template_vocabulary_placeholders_are_legal_members" (pass)

### 25. [07-05/D5] The bayesian-continuous-monitoring known-bad fixture's incidental DSX-VAL-041 finding (strength: strong + cons...
expected: The bayesian-continuous-monitoring known-bad fixture's incidental DSX-VAL-041 finding (strength: strong + constraint_source: informative_priors, both true declarations) is documented in tests/test_known_bad_corpus.py's _INCIDENTAL_GAP_CODES with a cause comment, and the fixture file itself is unedited; the corpus's positive gate guarantee (clears plan/execute) and ship-gate documentation guarantee both continue to hold; DSX-VAL- is not added to _TARGET_CODE_FAMILIES
result: pass
source: automated
coverage_id: D5
source_plan: 07-05
requirement: REQ-P7-05
verification:
  - unit: "tests/test_known_bad_corpus.py::TestKnownBadCorpus::test_every_spec_passes_the_critical_threshold_gate_points, test_ship_gate_findings_are_all_documented_incidental_corpus_gaps, test_incidental_allowlist_names_no_target_family_code" (pass)

### 26. [07-05/D6] Gate-level proof of the roadmap's severity wording: DSX-VAL-040 blocks dsx gate plan; DSX-VAL-041 exits 0 at d...
expected: Gate-level proof of the roadmap's severity wording: DSX-VAL-040 blocks dsx gate plan; DSX-VAL-041 exits 0 at dsx gate plan while still printed on stdout, then blocks dsx gate verify and dsx gate ship with the code visible on stderr; neither validity-frame code appears at dsx gate execute (val is not in that profile); the reachability proof is derived from GATE_PROFILES/CHECKS intersection, not a hand-written code list
result: pass
source: automated
coverage_id: D6
source_plan: 07-05
requirement: REQ-P7-05
verification:
  - unit: "tests/test_frame_val.py::TestValGateSeverity::test_weak_no_constraint_spec_blocks_gate_plan_naming_val_040, test_strong_informative_priors_spec_passes_gate_plan_but_still_prints_val_041, test_strong_informative_priors_spec_blocks_gate_verify_and_gate_ship_naming_val_041, test_neither_identification_spec_produces_a_validity_frame_finding_at_gate_execute, test_val_check_is_reachable_from_at_least_one_gate_profile" (pass)

### 27. [07-06/D1] DSX-VAL-050 fires HIGH on a blank claim_population or a non-empty known_exclusions with a blank selection_risk...
expected: DSX-VAL-050 fires HIGH on a blank claim_population or a non-empty known_exclusions with a blank selection_risk; uses plain blankness only, never placeholder detection
result: pass
source: automated
coverage_id: D1
source_plan: 07-06
requirement: REQ-P7-06
verification:
  - unit: "tests/test_frame_val.py::TestValSamplingMissingnessMeasurement (D-05: DSX-VAL-050 block)" (pass)

### 28. [07-06/D2] DSX-VAL-070 fires HIGH on a declared construct with a blank operationalisation; a blank construct never fires
expected: DSX-VAL-070 fires HIGH on a declared construct with a blank operationalisation; a blank construct never fires
result: pass
source: automated
coverage_id: D2
source_plan: 07-06
requirement: REQ-P7-08
verification:
  - unit: "tests/test_frame_val.py::TestValSamplingMissingnessMeasurement (D-05: DSX-VAL-070 block)" (pass)

### 29. [07-06/D3] DSX-VAL-060 fires HIGH on MAR + complete_case/available_case, CRITICAL on MNAR + anything but an explicit mech...
expected: DSX-VAL-060 fires HIGH on MAR + complete_case/available_case, CRITICAL on MNAR + anything but an explicit mechanism model, and never on MCAR or not_assessed
result: pass
source: automated
coverage_id: D3
source_plan: 07-06
requirement: REQ-P7-07
verification:
  - unit: "tests/test_frame_val.py::TestValSamplingMissingnessMeasurement (D-05: DSX-VAL-060 block, 12 tests)" (pass)

### 30. [07-06/D4] missingness.rate is never read by the check at any value (zero, positive, absent, non-numeric)
expected: missingness.rate is never read by the check at any value (zero, positive, absent, non-numeric)
result: pass
source: automated
coverage_id: D4
source_plan: 07-06
requirement: REQ-P7-07
verification:
  - unit: "tests/test_frame_val.py::TestValSamplingMissingnessMeasurement::test_missingness_rate_is_never_read_by_the_check" (pass)

### 31. [07-06/D5] The good fixture and template are repaired in the same commit as DSX-VAL-060, and both still clear every gate ...
expected: The good fixture and template are repaired in the same commit as DSX-VAL-060, and both still clear every gate at every threshold
result: pass
source: automated
coverage_id: D5
source_plan: 07-06
verification:
  - integration: "dsx gate plan/execute/verify/ship --spec examples/good-ANALYSIS-SPEC.yaml (all exit 0); dsx gate plan --spec templates/ANALYSIS-SPEC.yaml exits 0; dsx gate ship --spec templates/ANALYSIS-SPEC.yaml exits 1 (unchanged, incidental gaps only)" (pass)

### 32. [07-06/D6] All three known-bad corpus fixtures still clear the critical-threshold gate points with no new allow-list entr...
expected: All three known-bad corpus fixtures still clear the critical-threshold gate points with no new allow-list entry for DSX-VAL-060
result: pass
source: automated
coverage_id: D6
source_plan: 07-06
verification:
  - unit: "tests/test_frame_val.py::TestValSamplingMissingnessMeasurement::test_missingness_known_bad_corpus_fixtures_never_fire_val_060; tests/test_known_bad_corpus.py (unchanged, git diff empty)" (pass)

### 33. [07-06/D7] A single fixture-matrix test pins the whole ten-code family's behaviour against every spec file in the reposit...
expected: A single fixture-matrix test pins the whole ten-code family's behaviour against every spec file in the repository, failing loudly on any undocumented fixture
result: pass
source: automated
coverage_id: D7
source_plan: 07-06
verification:
  - unit: "tests/test_frame_val.py::TestValFixtureMatrix (5 tests); deliberate-violation check performed manually and reverted before commit" (pass)

### 34. [07-07/D1] examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml exists, blocks dsx gate plan naming DSX-VAL-040,...
expected: examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml exists, blocks dsx gate plan naming DSX-VAL-040, and clears dsx gate execute
result: pass
source: automated
coverage_id: D1
source_plan: 07-07
requirement: REQ-P7-05
verification:
  - integration: "tests/test_frame_val.py#TestValGateIntegration.test_weak_identification_mmm_fixture_blocks_gate_plan_naming_val_040" (pass)
  - integration: "tests/test_frame_val.py#TestValGateIntegration.test_weak_identification_mmm_fixture_clears_gate_execute" (pass)

### 35. [07-07/D2] The corpus's blanket plan/execute gate-clearance assertion is narrowed by a named exception (_EXPECTED_PLAN_BL...
expected: The corpus's blanket plan/execute gate-clearance assertion is narrowed by a named exception (_EXPECTED_PLAN_BLOCKERS) that carries a positive counterpart, not deleted; glob discovery and the incidental-gap allow-list guard are preserved
result: pass
source: automated
coverage_id: D2
source_plan: 07-07
verification:
  - unit: "tests/test_known_bad_corpus.py#TestKnownBadCorpus.test_every_spec_passes_the_critical_threshold_gate_points" (pass)
  - unit: "tests/test_known_bad_corpus.py#TestKnownBadCorpus.test_ship_gate_findings_are_all_documented_incidental_corpus_gaps" (pass)
  - unit: "tests/test_known_bad_corpus.py#TestKnownBadCorpus.test_incidental_allowlist_names_no_target_family_code" (pass)

### 36. [07-07/D3] Every DSX-VAL-* code carries a Citation: line, a Reference value:/Structural criterion: line, and a test marke...
expected: Every DSX-VAL-* code carries a Citation: line, a Reference value:/Structural criterion: line, and a test marker, proven by an AST-parsed test rather than a hand-written list; every emitted code appears in the rendered catalogue
result: pass
source: automated
coverage_id: D3
source_plan: 07-07
requirement: REQ-P7-05
verification:
  - unit: "tests/test_frame_val.py#TestValCitationObligations.test_every_finding_emitting_function_has_citation_and_reference_value_lines" (pass)
  - unit: "tests/test_frame_val.py#TestValCitationObligations.test_every_emitted_code_has_a_test_marker_under_tests" (pass)
  - unit: "tests/test_frame_val.py#TestValCitationObligations.test_every_emitted_code_appears_in_the_rendered_catalogue" (pass)
  - other: "python3 scripts/gen-finding-catalogue.py --check" (pass)

### 37. [07-08/D1] TestKishCitationCoherence added to tests/test_frame_val.py (3 assertions, 2 module-level helpers) and observ...
expected: TestKishCitationCoherence added to tests/test_frame_val.py (3 assertions, 2 module-level helpers) and observed failing against the unfixed tree before any production file was touched
result: pass
source: automated
coverage_id: D1
source_plan: 07-08
requirement: REQ-P7-02
verification:
  - unit: "tests/test_frame_val.py::TestKishCitationCoherence (3 tests, all FAIL at commit adc1ad2)" (pass)
  - unit: "python3 -m unittest tests.test_frame_val.TestKishCitationCoherence -v (3/3 pass at commit cb074c4)" (pass)

### 38. [07-08/D2] Kish (1965) citation reconciled across val.py (two sites), mathx.py and brief.md — no new bibliographic claim
expected: Kish (1965) citation reconciled across dsx/frame/val.py (two sites), dsx/mathx.py and brief.md: section 8.2 kept as a confirmed locator, disclosure narrowed to flag only the design-effect formula's section number as unverified, no new bibliographic claim added
result: pass
coverage_id: D2
source_plan: 07-08
reason: human_judgment
requirement: REQ-P7-02
read:
  - "dsx/frame/val.py:78-85 and 671-677 — the two reworded Kish passages"
  - "dsx/mathx.py:461-468 — the design_effect Citation: paragraph"
  - "brief.md section 7 — the Kish sentence"
  - "07-DISCUSSION-LOG.md:102-103 and 07-CONTEXT.md:284/303-304 — the research ledger the wording must not exceed"
rationale: "Whether the reworded disclosure states only what 07-DISCUSSION-LOG.md:102-103 and 07-CONTEXT.md:284/303-304 record, and no more, is a citation-accuracy judgment call this plan's own threat model (T-7-18) and human-check step assign to a human reader — automated tests confirm the Citation:/Reference value:/Structural criterion: shapes and the locator-set/pages-only-claim invariants, but cannot confirm the underlying bibliographic claim is exactly what the research log supports."
note: "Presented as the residual delta over test 4's retest rather than a full re-read: the over-claim ('and no more') clause, checked against 07-CONTEXT.md:303-304's parenthetical. User confirmed the shipped wording restates the ledger fact positively without widening it."

## Summary

total: 38
passed: 38
issues: 0
pending: 0
skipped: 0
blocked: 0

## Notes

- 07-03 coverage entry D5 has a malformed `verification` block: the first entry
  (`kind: unit`) is missing its `status:` field, so `uat classify-coverage` reported
  `invalid_status` and could not auto-pass it. Per the fail-safe rule it is carried as a
  human checkpoint (test 3). Both of its refs were re-run in this session and pass.
- Full suite re-run at UAT start: 419 passed, 378 subtests passed (5.37s).
- `python scripts/gen-finding-catalogue.py --check` -> exit 0, "finding catalogue is current".
- No cold-start smoke test injected: no SUMMARY touches server/app/index/main entrypoints,
  database/, db/, seed(s)/, migrations/, startup*, docker-compose* or Dockerfile*.

**Session 2 (2026-08-14) — resumed after gap closure:**

- Gap G-07-4 reconciled to `resolved`: 07-08-PLAN.md carries `gap_ids: [G-07-4]` and has a
  matching 07-08-SUMMARY.md (status: complete). 1 gap resolved, 0 still open.
- 07-08-SUMMARY.md added to `source`. Its coverage block classified `mode: coverage`, 2 entries:
  D1 auto-passed (test 37), D2 human checkpoint (test 38).
- Test 4 reopened as a retest rather than left as `issue` — the defect it reported was fixed by
  07-08, and the fix needs the same human citation-accuracy judgment that found it.
- Re-run this session against live HEAD: `TestKishCitationCoherence` 3/3 pass;
  `gen-finding-catalogue.py --check` exit 0 ("finding catalogue is current"; the four
  "declared twice" warnings are pre-existing and name no Kish/DSX-VAL-020 code);
  `check_brief_refs.py` exit 0 (14/14 ok).
- `verify:pre` gates: `api-coverage.verify-pre` → `block: false` (no external-API integration
  detected). The `dsx` capability's `dsx-statistician` step hook is registered and active
  (`dsx.enforce` default true) but was skipped per its own `onError: skip` — `dsx audit
  --phase-dir` reports no ANALYSIS-SPEC for this phase, which is correct: Phase 07 builds the
  validity-frame checker, it does not produce a statistical analysis to review. No STATS-REVIEW.md
  is expected or produced.

## Gaps

- gap_id: G-07-4
  truth: "The unit-triad citation's Kish locator and its UNVERIFIED disclosure agree with each other and with the phase's own research ledger."
  status: resolved
  resolved_by: 07-08-PLAN.md
  resolved_at: 2026-08-14
  resolution_note: "Reading B implemented across all four sites. Re-verified this session: TestKishCitationCoherence 3/3 pass, gen-finding-catalogue.py --check exit 0, check_brief_refs.py exit 0. Human re-confirmation of the reworded citation text is UAT test 4 (retest) and test 38."
  reason: "User reported: Citation contradiction (defect found). val.py:79 states 'section 8.2, page 258' while val.py:83-84 says the section number is UNVERIFIED and 'do not invent one'. D-05 violation."
  severity: major
  test: 4
  artifacts:
    - path: "dsx/frame/val.py"
      issue: "_UNIT_TRIAD_CITATION (lines 78-85) and the _check_unit_triad docstring (lines 671-677) both state 'section 8.2, page 258 (design-effect definition)' and then assert 'only the page numbers above were confirmed; do not invent one'."
  missing:
    - "Reconcile the Kish locator with its disclosure in both val.py sites (lines 79-84 and 671-677)."
    - "Decide which of the two readings below the fix implements, and make mathx.py:440-445 consistent with the same decision."
  contested: |
    Two readings of the source evidence, unresolved at UAT time — the fix plan must pick one.

    Reading A (user's verdict at UAT): the two clauses are mutually exclusive. Remedy: drop
    'section 8.2' from val.py, cite page numbers only, matching mathx.py.

    Reading B (found in the phase's own research during UAT, after the verdict was given):
    07-DISCUSSION-LOG.md:102-103 records "Kish (1965) §8.2 p. 258 confirmed for the Deff
    definition and pp. 161-162 for the ICC, but no *section* number for the formula — flagged
    UNVERIFIED". 07-CONTEXT.md:303-304 repeats it: "a *section* number in Kish for the DEFF
    formula itself (page numbers only were confirmed)". On this reading §8.2 is a CONFIRMED
    locator for the design-effect *definition*, and the UNVERIFIED locator is a different one —
    a section for the *formula*. The citation is then correct and the defect is narrower: the
    disclosure clause "only the page numbers above were confirmed" is factually wrong, because
    §8.2 was confirmed. Remedy: keep 'section 8.2', reword the disclosure to say the section
    number for the formula itself is unverified while §8.2 covers the definition. Under this
    reading mathx.py is under-citing a confirmed locator rather than being the correct model.
  root_cause: "Diagnosed inline during UAT, not by a debug agent — the evidence was already in the phase's own artifacts. 07-DISCUSSION-LOG.md:102-103 and 07-CONTEXT.md:303-304 both record that Kish §8.2 p.258 WAS confirmed for the design-effect *definition*, and that what is unverified is a section number for the *formula*. The 07-CONTEXT.md:284 research-ledger row carries '§8.2 p. 258' and was copied into _UNIT_TRIAD_CITATION verbatim. The defect is that the disclosure sentence shipped alongside it — 'only the page numbers above were confirmed' — is broader than the ledger supports and contradicts the §8.2 it sits next to. mathx.py resolved the same tension the other way by dropping §8.2 entirely, so the two files now disagree about what was confirmed. No test detects this: TestValCitationObligations asserts only that a Citation: line exists."
  remedy_decision: reading_b   # Pinned by the user at UAT close, 2026-08-12.
  remedy_rationale: |
    Reading B chosen. The discussion log and context file already record that Kish (1965)
    section 8.2, page 258 was confirmed for the design-effect definition, and that only a
    section for the formula itself was never confirmed. Dropping section 8.2 would throw away
    a locator the phase already verified; matching mathx.py by deleting it would make the code
    less accurate than the ledger. Keep the confirmed locator, narrow the disclosure, then
    bring mathx.py up to the same wording.
  remedy_steps:
    - "dsx/frame/val.py: keep 'section 8.2, page 258 (design-effect definition)' in both
       _UNIT_TRIAD_CITATION (lines 78-85) and the _check_unit_triad docstring (lines 671-677)."
    - "dsx/frame/val.py: rewrite the UNVERIFIED sentence so it no longer says 'only the page
       numbers above were confirmed'. Scope it to: no section number was confirmed for the
       design-effect formula itself."
    - "dsx/mathx.py: add section 8.2 to the design_effect() citation (lines 440-445) and use
       the same scoped disclosure, so tests 1 and 4 no longer disagree."
    - "Add a regression test that fails if a citation names a Kish section AND also claims only
       page numbers were confirmed."
  debug_session: ""  # not needed; see root_cause
