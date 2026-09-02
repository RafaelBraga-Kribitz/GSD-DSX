---
phase: 20-calibration-and-reporting-close
plan: A
type: execute
wave: 2
depends_on: [20-C, 20-D]
files_modified:
  - examples/known-bad/correlation-pearson-ordinal-scale-ANALYSIS-SPEC.yaml
  - examples/known-bad/correlation-pearson-ordinal-scale-POSTMORTEM.md
  - examples/known-bad/correlation-pearson-ordinal-scale-NARRATIVE.md
  - examples/known-bad/correlation-for-agreement-estimand-ANALYSIS-SPEC.yaml
  - examples/known-bad/correlation-for-agreement-estimand-POSTMORTEM.md
  - examples/known-bad/correlation-for-agreement-estimand-NARRATIVE.md
  - examples/known-bad/icc-incomplete-triple-ANALYSIS-SPEC.yaml
  - examples/known-bad/icc-incomplete-triple-POSTMORTEM.md
  - examples/known-bad/icc-incomplete-triple-NARRATIVE.md
  - examples/known-bad/weighted-kappa-missing-weights-ANALYSIS-SPEC.yaml
  - examples/known-bad/weighted-kappa-missing-weights-POSTMORTEM.md
  - examples/known-bad/weighted-kappa-missing-weights-NARRATIVE.md
  - examples/known-bad/kappa-missing-companions-ANALYSIS-SPEC.yaml
  - examples/known-bad/kappa-missing-companions-POSTMORTEM.md
  - examples/known-bad/kappa-missing-companions-NARRATIVE.md
  - examples/good-corpus/valid-correlation-linear-ANALYSIS-SPEC.yaml
  - examples/good-corpus/valid-correlation-linear-NARRATIVE.md
  - examples/good-corpus/valid-icc-reliability-ANALYSIS-SPEC.yaml
  - examples/good-corpus/valid-icc-reliability-NARRATIVE.md
  - examples/good-corpus/valid-weighted-kappa-ANALYSIS-SPEC.yaml
  - examples/good-corpus/valid-weighted-kappa-NARRATIVE.md
  - tests/test_known_bad_corpus.py
  - tests/test_causal_verb_golden.py
autonomous: true
requirements: [REQ-P20-01]
tags: [calibration, catch-rate, fpr, known-bad-corpus, high-stratum, negative-controls, re-baseline, measurement-integrity, fixtures]

must_haves:
  truths:
    - "five dedicated PRESENT known-bad fixtures fire the five Phase-18 codes that fire NOWHERE in examples/ today — DSX-STA-050 (Pearson r against a declared-ordinal operand), DSX-STA-051 (a correlation coefficient declared for an agreement estimand), DSX-STA-060 (ICC without a complete (model,type,definition) triple), DSX-STA-061 (weighted kappa without recognised weights), DSX-STA-062 (a kappa missing its p_pos/p_neg companions) — each fixture firing EXACTLY its one HIGH target at verify/ship (mutually exclusive on analysis.test), clearing plan/execute at exit 0 (no CRITICAL), passing dsx validate, and carrying a POSTMORTEM naming its code; NONE is declared ABSENT (D-04)"
    - "the single stratified calibration harness is EXTENDED, not duplicated, with a live HIGH verify/ship stratum (D-03): _classify_target_defect gains a severity parameter defaulting to \"CRITICAL\" (every existing call byte-for-byte unchanged), a new _HIGH_TARGET_DEFECT_CODES map declares which new fixture demonstrates which HIGH code at verify/ship, and test_stratified_catch_rate_and_fpr_report reports the HIGH-tier PRESENT catch rate as a THIRD readout computed LIVE via self._gate_findings filtering HIGH — never lifted from _GOLDEN_SHIP_FINDINGS / _INCIDENTAL_GAP_CODES / any stored expected-map (the D-09 no-self-reference rule)"
    - "the headline stays the pair (miss-rate, FPR): the HIGH-tier PRESENT catch is reported BESIDE the pair, never folded into _headline, so target-present-invariance holds by construction; the synthetic anchor _headline((2,5),(1,4),(3,10)) == (0.25, 0.3) and the floor _ABSENT_PARTITION_FLOOR == 3 are UNMOVED (D-06); the only committed number that moves is _GOLDEN_SHIP_FINDINGS, which gains one MEASURED key per new fixture"
    - "at least one VALID good-corpus negative control per routing family (a correctly-scaled correlation, a complete-triple ICC, a weighted kappa with recognised weights + p_pos/p_neg) genuinely EXERCISES each of the five codes' branches and correctly stays silent — so the FPR is a real negative control on the fifteen, not the prior silence; the FPR denominator stays >= 10 and grows (12 -> 15); a guard asserts _FPR_TEMPDIR_NOISE_CODES is DISJOINT from the DSX-STA statistical-validity family (D-05)"
    - "the HIGH-tier stratum classifies on finding CODE identity only, introduces no numeric-magnitude comparison, and reads no effect-size band as a threshold (D-08); every new fixture is added to _EXPECTED_CAUGHT_DEFECTS with an empty frozenset() (its HIGH catch lives in the new HIGH map, not the CRITICAL both-points map) so the keys-match invariant stays green"
    - "this plan mints ZERO finding codes — no report.add site is added anywhere; the catalogue stays 275 and the D-13-a deferral (the CRITICAL-only miss-union) is NOT exploited: no new fixture relies on an ABSENT HIGH declaration"
  artifacts:
    - examples/known-bad/correlation-pearson-ordinal-scale-ANALYSIS-SPEC.yaml
    - examples/known-bad/correlation-for-agreement-estimand-ANALYSIS-SPEC.yaml
    - examples/known-bad/icc-incomplete-triple-ANALYSIS-SPEC.yaml
    - examples/known-bad/weighted-kappa-missing-weights-ANALYSIS-SPEC.yaml
    - examples/known-bad/kappa-missing-companions-ANALYSIS-SPEC.yaml
    - examples/good-corpus/valid-correlation-linear-ANALYSIS-SPEC.yaml
    - examples/good-corpus/valid-icc-reliability-ANALYSIS-SPEC.yaml
    - examples/good-corpus/valid-weighted-kappa-ANALYSIS-SPEC.yaml
    - tests/test_known_bad_corpus.py
    - tests/test_causal_verb_golden.py
  key_links:
    - "each new known-bad fixture's declared analysis-block trigger <-> the Phase-18 firing site it exercises (DSX-STA-050 stats.py:924; 051 stats.py:942; 060 stats.py:979; 061 stats.py:1008; 062 stats.py:1035) <-> its measured _GOLDEN_SHIP_FINDINGS key (test_golden_keys_match_the_examples_tree_on_disk forces every new fixture to carry a measured entry, so the re-baseline can never be guessed)"
    - "_HIGH_TARGET_DEFECT_CODES (the intent: which fixture targets which HIGH code) <-> self._gate_findings(path, verify/ship) filtering HIGH (the live measurement) — the target map is a declaration like _TARGET_DEFECT_CODES, never the measured ledger _GOLDEN_SHIP_FINDINGS; using the ledger as 'what fired' is the D-09 violation this stratum is built to avoid"
    - "the severity parameter on _classify_target_defect (default CRITICAL) <-> every existing call site unchanged <-> the HIGH stratum's severity=\"HIGH\" call — one honest calibration source, a stratification DIMENSION (severity-tier x point-set) added, not a second sibling test with its own headline (the divergent-drift failure _effective_target_map's docstring warns against)"
    - "the three valid good-corpus controls (exercise-and-stay-silent) <-> the FPR denominator (>=10, grows to 15) <-> the _FPR_TEMPDIR_NOISE_CODES-disjoint-from-DSX-STA guard — the silence on the fifteen becomes a measured negative control instead of the branch never being reached"
    - "the pair anchor (0.25,0.3) + floor 3 UNMOVED <-> the third readout reported beside the pair — the D-06 re-baseline invariant that adding a caught PRESENT case cannot move the (miss-rate, FPR) pair"
---

<objective>
Deliver REQ-P20-01: known-bad test-choice fixtures for every new blocking code, the stratified catch rate and false-positive rate re-measured, and the calibration re-baselined (Phase-12 discipline). The load-bearing deliverable (D-03) is EXTENDING the single calibration harness with a live HIGH verify/ship stratum — the fifteen new codes are all HIGH / verify-ship-only, so the existing CRITICAL plan/execute partition is a provable no-op on them, and "re-baselined to cover the fifteen" is UNSUPPORTED without the HIGH stratum.

Purpose: this is Wave 2 (D-07), measured against the settled post-C/post-D state (Phase-12 "measure last"). The ten Phase-19 codes already fire on examples/bad-ANALYSIS-SPEC.yaml at ship; the genuinely-new fixture work is the FIVE Phase-18 codes (050/051/060/061/062), which fire nowhere in examples/ today — each gets a dedicated PRESENT known-bad fixture (none is declared ABSENT, D-04). The FPR is currently silent-not-clean on the fifteen (D-05): the twelve control specs never declare correlation/agreement, so their branches are never reached — three valid controls fix that. The re-baseline moves exactly one committed number, _GOLDEN_SHIP_FINDINGS (D-06); the pair anchor (0.25,0.3) and floor 3 do not move; effect-size bands stay conventions (D-08).

Output: five dedicated PRESENT known-bad fixtures (+ POSTMORTEM + NARRATIVE siblings) firing the five Phase-18 codes; three valid good-corpus negative controls (+ NARRATIVE siblings); the HIGH verify/ship stratum in tests/test_known_bad_corpus.py (severity-parameterised _classify_target_defect, _HIGH_TARGET_DEFECT_CODES, the live third readout, the FPR-disjointness guard); and the _GOLDEN_SHIP_FINDINGS re-baseline in tests/test_causal_verb_golden.py. Zero codes minted; catalogue stays 275.
</objective>

<execution_context>
@$HOME/.claude/gsd-core/workflows/execute-plan.md
@$HOME/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/20-calibration-and-reporting-close/20-CONTEXT.md
@dsx/checks/stats.py
@tests/test_known_bad_corpus.py
@tests/test_causal_verb_golden.py
@examples/good-corpus/freq-continuous-aov-ANALYSIS-SPEC.yaml
</context>

<fixture_bindings>
The five Phase-18 codes and their exact declared-field triggers (verified live at dsx/checks/stats.py:905-1050). Each fixture declares ONLY the fields needed to fire its ONE code, so the five are mutually exclusive on analysis.test and each catch is attributable:

- DSX-STA-050 (correlation-pearson-ordinal-scale): analysis.test = pearson_correlation AND analysis.operand_scale = ordinal; estimand_kind stays a NON-agreement kind (e.g. linear_association) so DSX-STA-051 does not also fire.
- DSX-STA-051 (correlation-for-agreement-estimand): analysis.test = pearson_correlation (a CORRELATION_FAMILY member) AND analysis.estimand_kind = agreement; operand_scale is NOT ordinal so DSX-STA-050 does not also fire.
- DSX-STA-060 (icc-incomplete-triple): analysis.test = icc (or an analysis.icc dict) with an INCOMPLETE / out-of-vocab (model, type, definition) triple (omit one member).
- DSX-STA-061 (weighted-kappa-missing-weights): analysis.test = weighted_kappa with NO recognised analysis.weights (omit weights) BUT WITH valid analysis.p_pos and analysis.p_neg present, so ONLY 061 fires (062 is satisfied by the companions).
- DSX-STA-062 (kappa-missing-companions): analysis.test = cohens_kappa (a kappa-family test that is NOT weighted_kappa, so 061 is out of scope) with analysis.p_pos and/or analysis.p_neg BLANK.

Anti-DSX-STA-041 discipline (19-RESEARCH Pitfall 1): each correlation/agreement fixture OMITS analysis.outcome_type (declaring outcome_type + a non-comparison test trips DSX-STA-041 from _check_declared_test); the _check_declared_test outcome_type early-return then leaves DSX-STA-041 silent, so ONLY the intended DSX-STA-05x fires.

Minimal-reference cleanliness: model each fixture on examples/good-corpus/freq-continuous-aov-ANALYSIS-SPEC.yaml (a full clean spec that fires frozenset() at ship). Keep its clean decision/replay, metrics-with-source, reproducibility (entrypoint: examples/good-corpus/_control_readout.py — cwd-resolvable, shared, no new entrypoint), repro_lock, narrative, validity_frame and inference blocks; point claims[].evidence and narrative.path at the fixture's own cwd-resolvable NARRATIVE.md sibling; and REPLACE only the analysis block (and the results.tests interpretation) with the correlation/agreement declaration carrying the one defect above. The measured ship set is then {the one DSX-STA-05x code} and the fixture clears plan/execute at exit 0. MEASURE the golden set live; never guess it.
</fixture_bindings>

<tasks>

<task type="auto">
  <name>Task 1: The five Phase-18 PRESENT known-bad fixtures (+ POSTMORTEM + NARRATIVE), their _EXPECTED_CAUGHT_DEFECTS empty keys, and their measured golden keys</name>
  <read_first>
    - examples/good-corpus/freq-continuous-aov-ANALYSIS-SPEC.yaml in full (the clean minimal-reference template: the exact block structure that fires frozenset() at ship — decision.replay, metrics[].source, reproducibility.entrypoint + repro_lock, narrative.path, validity_frame, inference — to clone verbatim except the analysis block)
    - dsx/checks/stats.py lines 905-1050 (_check_correlation_scale_kind DSX-STA-050 at 924 / DSX-STA-051 at 942, and _check_agreement_completeness DSX-STA-060 at 979 / DSX-STA-061 at 1008 / DSX-STA-062 at 1035 — the EXACT declared-field predicates and the CORRELATION_FAMILY / ICC vocab / KAPPA_WEIGHT_TOKENS the fixtures must match) and lines 557-560 (the _check_declared_test outcome_type early-return — why omitting outcome_type avoids DSX-STA-041)
    - tests/test_known_bad_corpus.py lines 843-910 (the corpus sibling / three-pairs / loads / dsx-validate invariants each new fixture must satisfy) and lines 923-956 (test_every_spec_blocks_only_on_its_target_defect_at_critical_threshold_points — the new fixtures are NOT in _effective_target_map, so they MUST clear plan/execute at exit 0) and lines 409-455 (_EXPECTED_CAUGHT_DEFECTS: every fixture needs a key, empty frozenset() for a fixture with no CRITICAL target) and lines 1129-1141 (test_expected_caught_defects_keys_match_the_corpus_on_disk — the equality this keeps green)
    - tests/test_causal_verb_golden.py lines 82-198 (_GOLDEN_SHIP_FINDINGS) and 253-266 (test_golden_keys_match_the_examples_tree_on_disk — every new examples/** spec needs a measured golden key) and 223-246 (_ship_findings — the fresh-tempdir measurement idiom to reproduce when measuring each new key)
    - 20-CONTEXT.md D-04 (all fifteen PRESENT-caught, none ABSENT; the five Phase-18 codes are the real fixture gap; the mutually-exclusive-on-analysis.test triggers) and D-13-a (the CRITICAL-only miss-union is NOT exploited: no fixture relies on an ABSENT HIGH declaration)
  </read_first>
  <files>examples/known-bad/correlation-pearson-ordinal-scale-ANALYSIS-SPEC.yaml, examples/known-bad/correlation-pearson-ordinal-scale-POSTMORTEM.md, examples/known-bad/correlation-pearson-ordinal-scale-NARRATIVE.md, examples/known-bad/correlation-for-agreement-estimand-ANALYSIS-SPEC.yaml, examples/known-bad/correlation-for-agreement-estimand-POSTMORTEM.md, examples/known-bad/correlation-for-agreement-estimand-NARRATIVE.md, examples/known-bad/icc-incomplete-triple-ANALYSIS-SPEC.yaml, examples/known-bad/icc-incomplete-triple-POSTMORTEM.md, examples/known-bad/icc-incomplete-triple-NARRATIVE.md, examples/known-bad/weighted-kappa-missing-weights-ANALYSIS-SPEC.yaml, examples/known-bad/weighted-kappa-missing-weights-POSTMORTEM.md, examples/known-bad/weighted-kappa-missing-weights-NARRATIVE.md, examples/known-bad/kappa-missing-companions-ANALYSIS-SPEC.yaml, examples/known-bad/kappa-missing-companions-POSTMORTEM.md, examples/known-bad/kappa-missing-companions-NARRATIVE.md, tests/test_known_bad_corpus.py, tests/test_causal_verb_golden.py</files>
  <action>Author the five dedicated PRESENT known-bad fixtures per the <fixture_bindings> block, one per Phase-18 code. For each: (1) clone the good-corpus clean template, keeping every clean block verbatim, add a cwd-resolvable NARRATIVE.md sibling (doubling as claims[].evidence and narrative.path), and REPLACE the analysis block with the correlation/agreement declaration carrying exactly the one DSX-STA-05x trigger — OMITTING analysis.outcome_type to keep DSX-STA-041 silent; (2) write a POSTMORTEM.md sibling that NAMES the target DSX-STA-05x code (the corpus requires a sibling postmortem naming a finding code) and explains the encoded routing defect and its remedy in prose, with no fabricated numeric boundary. Then keep the corpus and golden suites green: in tests/test_known_bad_corpus.py add each of the five new slugs to _EXPECTED_CAUGHT_DEFECTS with an empty frozenset() (its HIGH catch lives in the Task-3 HIGH map, NOT the CRITICAL both-points map — comment this by design, mirroring the coverage-class MISS entries at 442-455); do NOT add any of them to _TARGET_DEFECT_CODES (a subset map, CRITICAL-only). In tests/test_causal_verb_golden.py add each new fixture's MEASURED ship CRITICAL/HIGH set to _GOLDEN_SHIP_FINDINGS — measure it live with the module's own fresh-tempdir _ship_findings idiom (each should be exactly {its DSX-STA-05x code}; commit the measured reality, never a guess), so test_golden_keys_match_the_examples_tree_on_disk stays green. Do NOT edit dsx/, scripts/, references/, examples/bad-ANALYSIS-SPEC.yaml, examples/good-ANALYSIS-SPEC.yaml, or any tracking file; add NO report.add site (zero mint); create NO ATTRIBUTION.yaml sidecar for any new fixture (none is ABSENT — D-04/D-13-a). CRLF-safe throughout.</action>
  <verify>
    <automated>python3 -m unittest tests.test_known_bad_corpus tests.test_causal_verb_golden -v && python3 -c "import pathlib; from dsx.loader import load; from dsx.checks import stats; T={'correlation-pearson-ordinal-scale':'DSX-STA-050','correlation-for-agreement-estimand':'DSX-STA-051','icc-incomplete-triple':'DSX-STA-060','weighted-kappa-missing-weights':'DSX-STA-061','kappa-missing-companions':'DSX-STA-062'}; F={'DSX-STA-050','DSX-STA-051','DSX-STA-060','DSX-STA-061','DSX-STA-062','DSX-STA-070','DSX-STA-080','DSX-STA-081','DSX-STA-090','DSX-STA-100','DSX-STA-110','DSX-STA-111','DSX-STA-120','DSX-STA-121','DSX-STA-122'}; fired={s:{f.code for f in stats.check(load('examples/known-bad/'+s+'-ANALYSIS-SPEC.yaml')).findings} for s in T}; assert all(pathlib.Path('examples/known-bad/'+s+'-POSTMORTEM.md').is_file() for s in T), 'a POSTMORTEM sibling is missing'; assert all(c in fired[s] for s,c in T.items()), ('a fixture misses its target: '+str({s:c for s,c in T.items() if c not in fired[s]})); assert all(not ((F-{c}) & fired[s]) for s,c in T.items()), ('a fixture fires other Phase-18/19 codes: '+str({s:sorted((F-{c})&fired[s]) for s,c in T.items() if (F-{c})&fired[s]})); print('five Phase-18 fixtures each fire exactly their target HIGH code')"</automated>
  </verify>
  <acceptance_criteria>
    - tests.test_known_bad_corpus and tests.test_causal_verb_golden are fully green: sibling/three-pairs/loads/dsx-validate invariants hold, the five new fixtures clear plan/execute at exit 0, every new fixture has an _EXPECTED_CAUGHT_DEFECTS empty key, and every new examples/** spec has a measured golden key (keys match disk).
    - The inline audit prints "five Phase-18 fixtures each fire exactly their target HIGH code": each fixture fires its one DSX-STA-05x and NONE of the other fourteen (mutually exclusive on analysis.test; no DSX-STA-041 leak).
    - Each new known-bad fixture has a POSTMORTEM naming its code and a NARRATIVE sibling; no ATTRIBUTION.yaml is created (none is ABSENT).
    - No edit to dsx/, scripts/, references/, examples/bad-ANALYSIS-SPEC.yaml, examples/good-ANALYSIS-SPEC.yaml, or any tracking file; zero report.add sites added.
  </acceptance_criteria>
  <done>Five dedicated PRESENT known-bad fixtures fire the five Phase-18 codes (each exactly its own, clearing plan/execute), carry POSTMORTEM + NARRATIVE siblings and empty _EXPECTED_CAUGHT_DEFECTS keys, and each carries a measured _GOLDEN_SHIP_FINDINGS key; the corpus and golden suites are green; zero codes minted.</done>
</task>

<task type="auto">
  <name>Task 2: The three valid good-corpus negative controls (+ NARRATIVE) and the _FPR_TEMPDIR_NOISE_CODES disjointness guard</name>
  <read_first>
    - examples/good-corpus/freq-continuous-aov-ANALYSIS-SPEC.yaml (the clean control template again — the controls clone it and swap ONLY the analysis block to a VALID correlation/agreement declaration that reaches the DSX-STA-05x branch and correctly stays silent)
    - dsx/checks/stats.py lines 905-1050 (the silence conditions: DSX-STA-050 does NOT fire when operand_scale is not ordinal; 051 does NOT fire for a non-agreement estimand; 060 does NOT fire with a COMPLETE in-vocab (model,type,definition) triple; 061 does NOT fire with recognised weights (linear/quadratic or a matrix); 062 does NOT fire with both p_pos and p_neg present) — the controls declare the VALID form of each
    - tests/test_known_bad_corpus.py lines 642-698 (GOOD_CORPUS_DIR, _FPR_TEMPDIR_NOISE_CODES at 666-671, _false_positive_findings at 683-698 — counts CRITICAL/HIGH minus tempdir-noise, so a control that fires a HIGH DSX-STA-05x WOULD be a false positive; the controls must fire NONE of the fifteen) and lines 1585-1598 (the FPR denominator loop and the >=10 floor)
    - tests/test_causal_verb_golden.py lines 108-134 (the good-corpus control golden entries — each frozenset(); the new controls follow the same minimal-reference route and measure frozenset())
    - 20-CONTEXT.md D-05 (add >=1 valid control per routing family; denominator stays >=10 and grows; guard _FPR_TEMPDIR_NOISE_CODES disjoint from the DSX-STA family)
  </read_first>
  <files>examples/good-corpus/valid-correlation-linear-ANALYSIS-SPEC.yaml, examples/good-corpus/valid-correlation-linear-NARRATIVE.md, examples/good-corpus/valid-icc-reliability-ANALYSIS-SPEC.yaml, examples/good-corpus/valid-icc-reliability-NARRATIVE.md, examples/good-corpus/valid-weighted-kappa-ANALYSIS-SPEC.yaml, examples/good-corpus/valid-weighted-kappa-NARRATIVE.md, tests/test_known_bad_corpus.py, tests/test_causal_verb_golden.py</files>
  <action>Author three VALID good-corpus negative controls, one per routing family, each cloning the clean control template with a cwd-resolvable NARRATIVE.md sibling and swapping ONLY the analysis block to a correctly-declared correlation/agreement analysis that REACHES a DSX-STA-05x branch and correctly stays silent: valid-correlation-linear declares estimand_kind: linear_association + test: pearson_correlation + operand_scale: interval (reaches 050/051's branch, both silent); valid-icc-reliability declares test: icc (or an analysis.icc dict) with a COMPLETE in-vocab (model, type, definition) triple (reaches 060's branch, silent); valid-weighted-kappa declares test: weighted_kappa with recognised analysis.weights (linear or quadratic) AND analysis.p_pos + analysis.p_neg present (reaches 061/062's branches, both silent). OMIT analysis.outcome_type as in Task 1 so DSX-STA-041 stays silent. In tests/test_causal_verb_golden.py add each control's measured ship set to _GOLDEN_SHIP_FINDINGS (measure live; each should be frozenset()). In tests/test_known_bad_corpus.py add a NEW guard test asserting _FPR_TEMPDIR_NOISE_CODES is DISJOINT from the DSX-STA statistical-validity family (no key in _FPR_TEMPDIR_NOISE_CODES starts with "DSX-STA-"), so no future editor can absorb a real new-code false positive as tempdir noise. Do NOT edit dsx/, scripts/, references/, examples/bad-ANALYSIS-SPEC.yaml, examples/good-ANALYSIS-SPEC.yaml, or any tracking file; add NO report.add site. CRLF-safe.</action>
  <verify>
    <automated>python3 -m unittest tests.test_known_bad_corpus tests.test_causal_verb_golden -v && python3 -c "import pathlib; from dsx.loader import load; from dsx.checks import stats; F={'DSX-STA-050','DSX-STA-051','DSX-STA-060','DSX-STA-061','DSX-STA-062','DSX-STA-070','DSX-STA-080','DSX-STA-081','DSX-STA-090','DSX-STA-100','DSX-STA-110','DSX-STA-111','DSX-STA-120','DSX-STA-121','DSX-STA-122'}; C=['valid-correlation-linear','valid-icc-reliability','valid-weighted-kappa']; fired={s:{f.code for f in stats.check(load('examples/good-corpus/'+s+'-ANALYSIS-SPEC.yaml')).findings} for s in C}; assert all(not (F & fired[s]) for s in C), ('a control leaked a Phase-18/19 code (false positive): '+str({s:sorted(F&fired[s]) for s in C if F&fired[s]})); n=len(list(pathlib.Path('examples/good-corpus').glob('*-ANALYSIS-SPEC.yaml'))); assert n>=10, ('FPR denominator below floor: '+str(n)); import tests.test_known_bad_corpus as TB; assert not any(x.startswith('DSX-STA-') for x in TB._FPR_TEMPDIR_NOISE_CODES), 'a DSX-STA code is in the tempdir-noise allowlist'; print('three valid controls silent on the fifteen; denominator '+str(n)+'; noise-allowlist disjoint from DSX-STA')"</automated>
  </verify>
  <acceptance_criteria>
    - tests.test_known_bad_corpus and tests.test_causal_verb_golden are green; the new FPR-disjointness guard passes.
    - The inline audit prints "three valid controls silent on the fifteen; denominator 15; noise-allowlist disjoint from DSX-STA": each control reaches a DSX-STA-05x branch and fires NONE of the fifteen; the FPR denominator is >=10 (15) and grew from 12.
    - Each control fires frozenset() at ship (measured golden entry), so the FPR stays honest at 0.
    - No edit to dsx/, scripts/, references/, examples/bad-ANALYSIS-SPEC.yaml, examples/good-ANALYSIS-SPEC.yaml, or any tracking file; zero report.add sites.
  </acceptance_criteria>
  <done>Three valid good-corpus negative controls exercise each routing family's branch and correctly stay silent, growing the FPR denominator to 15 (>=10); the _FPR_TEMPDIR_NOISE_CODES-disjoint-from-DSX-STA guard is in place; suites green; zero codes minted.</done>
</task>

<task type="auto">
  <name>Task 3: Extend the single calibration harness with the live HIGH verify/ship stratum and the third readout</name>
  <read_first>
    - tests/test_known_bad_corpus.py lines 264-319 (_classify_target_defect — the severity parameter goes here; line 299 `critical = [f["code"] for f in findings if f.get("severity") == "CRITICAL"]` becomes severity-parameterised) and lines 1557-1686 (test_stratified_catch_rate_and_fpr_report — the PRESENT/ABSENT/FPR partitions, the _headline pair, the invariance proof; the HIGH stratum is ADDED here as a third readout beside the pair) and lines 1488-1497 (the local anchor re-pin _headline((2,5),(1,4),(3,10)) == (0.25,0.3) and the D-10 "reported beside, never inside" discipline) and lines 673-714 (_ABSENT_PARTITION_FLOOR == 3 and _headline — both UNMOVED) and lines 1750-1804 (test_target_defect_codes_fire_and_are_named — the CRITICAL analog whose HIGH-stratum sibling this task adds)
    - 20-CONTEXT.md D-03 (the load-bearing decision: extend the harness with a live HIGH stratum; severity defaults to CRITICAL; iterate the HIGH point-set (verify,ship); read LIVE, never from _GOLDEN_SHIP_FINDINGS / _INCIDENTAL_GAP_CODES / any stored expected-map — the D-09 rule), D-06 (only _GOLDEN_SHIP_FINDINGS moves; the anchor (0.25,0.3) and floor 3 do not; the HIGH catch is a THIRD readout beside the pair, never folded in), D-08 (classify on finding CODE identity only, no numeric-magnitude comparison), D-09 (no self-reference)
    - tests/test_causal_verb_golden.py lines 82-198 (the measured HIGH sets for the five new fixtures Task 1 committed — the HIGH stratum re-derives its catch LIVE and MUST NOT read these; this is the tempting shortcut D-09 forbids)
  </read_first>
  <files>tests/test_known_bad_corpus.py</files>
  <action>Extend the SINGLE calibration harness (do NOT add a sibling calibration test — D-03). First, parameterise _classify_target_defect with a trailing severity parameter defaulting to "CRITICAL" and change its findings filter (line 299) to key on that severity, so every existing call (which passes no severity) is byte-for-byte unchanged. Add a module-level _HIGH_TARGET_DEFECT_CODES map declaring which new fixture demonstrates which HIGH code at the HIGH point-set — the five slugs from Task 1 each mapped to {"verify": "DSX-STA-05x", "ship": "DSX-STA-05x"} — with a docstring stating this is the DECLARATION of intent (like _TARGET_DEFECT_CODES), never the measured ledger, and that the catch is measured LIVE. In test_stratified_catch_rate_and_fpr_report, AFTER the existing (miss-rate, FPR) headline and its invariance proof, add a HIGH-tier PRESENT stratum: iterate _HIGH_TARGET_DEFECT_CODES over the HIGH point-set ("verify","ship"), and for each expected cell call self._gate_findings(path, point) LIVE and _classify_target_defect(slug, point, code, findings, _HIGH_TARGET_DEFECT_CODES, severity="HIGH"), counting caught; assert the HIGH denominator is > 0 (non-empty) and report high_present_caught / high_present_denom as a THIRD readout BESIDE the pair. Assert the HIGH stratum did not touch the pair: re-assert the local anchor _headline((2,5),(1,4),(3,10)) == (0.25, 0.3) and _ABSENT_PARTITION_FLOOR == 3 unchanged, and that the pair computed with and without the HIGH stratum present is identical (target-present-invariance). Document in the method that the HIGH catch is derived only from self._gate_findings filtered to HIGH and is NEVER read from _GOLDEN_SHIP_FINDINGS / _INCIDENTAL_GAP_CODES / any stored expected-map (D-09). Add a HIGH-stratum sibling of test_target_defect_codes_fire_and_are_named: for each entry in _HIGH_TARGET_DEFECT_CODES assert its code FIRES live HIGH at its mapped verify/ship point AND is NAMED in that slug's POSTMORTEM, and assert the HIGH target codes are disjoint from _INCIDENTAL_GAP_CODES (no laundering). Do NOT move the anchor, the floor, or _headline; do NOT fold the HIGH catch into the pair; do NOT read a computed statistic or an effect-size band (D-08 — CODE identity only). Do NOT edit dsx/, scripts/, references/, examples/, or any tracking file; add NO report.add site.</action>
  <verify>
    <automated>python3 -m unittest tests.test_known_bad_corpus -v && python3 -c "import inspect; import tests.test_known_bad_corpus as T; assert 'severity' in inspect.signature(T._classify_target_defect).parameters, 'severity parameter missing'; assert inspect.signature(T._classify_target_defect).parameters['severity'].default=='CRITICAL', 'severity default is not CRITICAL'; assert T._headline((2,5),(1,4),(3,10))==(0.25,0.3), 'anchor moved'; assert T._ABSENT_PARTITION_FLOOR==3, 'floor moved'; hm=T._HIGH_TARGET_DEFECT_CODES; assert set(hm)=={'correlation-pearson-ordinal-scale','correlation-for-agreement-estimand','icc-incomplete-triple','weighted-kappa-missing-weights','kappa-missing-companions'}, sorted(hm); import inspect as I; src=I.getsource(T.test_stratified_catch_rate_and_fpr_report) if hasattr(T,'test_stratified_catch_rate_and_fpr_report') else I.getsource(T.TestKnownBadCorpus.test_stratified_catch_rate_and_fpr_report); assert '_GOLDEN_SHIP_FINDINGS' not in src, 'HIGH stratum must not read the golden ledger (D-09)'; assert 'severity=\"HIGH\"' in src or \"severity='HIGH'\" in src, 'HIGH stratum severity call missing'; print('severity param default CRITICAL; anchor+floor unmoved; HIGH stratum live, five fixtures, no golden self-reference')"</automated>
  </verify>
  <acceptance_criteria>
    - tests.test_known_bad_corpus is fully green and the inline check prints "severity param default CRITICAL; anchor+floor unmoved; HIGH stratum live, five fixtures, no golden self-reference".
    - _classify_target_defect has a severity parameter defaulting to "CRITICAL"; every existing call is unchanged; the HIGH stratum calls it with severity="HIGH".
    - The HIGH-tier PRESENT catch is reported as a THIRD readout beside the (miss-rate, FPR) pair with a non-empty denominator; the anchor _headline((2,5),(1,4),(3,10)) == (0.25,0.3) and _ABSENT_PARTITION_FLOOR == 3 are UNMOVED; the pair is invariant to the HIGH stratum's presence.
    - The HIGH catch is derived only from live self._gate_findings filtered to HIGH — _GOLDEN_SHIP_FINDINGS / _INCIDENTAL_GAP_CODES are not read in the stratum (D-09); the HIGH "fire and are named" guard passes and the HIGH targets are disjoint from _INCIDENTAL_GAP_CODES.
    - No edit to dsx/, scripts/, references/, examples/, or any tracking file; zero report.add sites; no numeric-magnitude / effect-size-band comparison introduced (D-08).
  </acceptance_criteria>
  <done>The single calibration harness carries a live HIGH verify/ship stratum measuring the five Phase-18 fixtures' catch as a third readout beside the (miss-rate, FPR) pair; _classify_target_defect is severity-parameterised (default CRITICAL); the anchor and floor are unmoved; the HIGH catch is read live, never from the golden ledger (D-09); zero codes minted.</done>
</task>

</tasks>

<single_writer_proof>
Phase 20 is a two-wave, file-disjoint, single-writer split (D-07). This is a Wave-2 calibration plan (depends_on 20-C, 20-D — measured against the settled post-structural-guard state). Every file this plan writes is owned by exactly one plan; the Wave-2 writer partition with 20-B is disjoint:

| File | Wave-2 writer | 20-B (Wave 2) writes? | Concurrent write? |
|------|---------------|-----------------------|-------------------|
| examples/known-bad/* (5 new fixtures + POSTMORTEM + NARRATIVE) | 20-A | No | No |
| examples/good-corpus/* (3 new controls + NARRATIVE) | 20-A | No | No |
| tests/test_known_bad_corpus.py | 20-A | No | No |
| tests/test_causal_verb_golden.py | 20-A | No | No |
| examples/good-ANALYSIS-SPEC.yaml | — | 20-B | No — 20-A never touches it |
| references/finding-codes.md | — | 20-B | No — 20-A never touches it |

Cross-plan read-only invariant (documented, not a write conflict): 20-A's tests/test_causal_verb_golden.py pins the good-ANALYSIS-SPEC.yaml golden entry to its existing four-code baseline and 20-A does NOT change that entry (20-A only ADDS entries for its eight new fixtures). 20-B (Wave 2) extends examples/good-ANALYSIS-SPEC.yaml with silent, in-vocabulary, non-triggering new-family declarations and its own gate PRESERVES good's finding set at the four-code baseline — so at merge, 20-A's unchanged golden entry still matches 20-B's extended fixture. File writes are disjoint (20-A writes the golden test; 20-B writes the fixture); the preservation invariant is enforced by 20-B's own gate. Wave-1 files (references/test-selection.md, dsx/checks/stats.py, the two guard test modules) are untouched by 20-A. Tracking files stay orchestrator-serial.
</single_writer_proof>

<threat_model>
**register_authored_at_plan_time: true** — authored at planning time (S4-2). /gsd-secure-phase 20 reads this flag. ASVS L1, block_on: high. This plan adds only fixtures (declared data) and calibration test assertions; no data path, no new I/O surface, no new dependency, no report.add site; there is no high-severity open threat.

## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| analyst-authored ANALYSIS-SPEC.yaml -> dsx loader -> stats.check | The new known-bad fixtures cross declared correlation/agreement strings; the gate reads DECLARED fields only (no data path). |
| the HIGH-tier catch declaration <-> the live gate measurement | The self-reference boundary (D-09): the catch rate must be measured live, never lifted from the golden ledger; reading _GOLDEN_SHIP_FINDINGS as "what fired" is the tampering this stratum is built to prevent. |
| good-control corpus <-> the FPR denominator | A control that fires a real HIGH code is a false positive; the controls must reach each branch and stay silent, and the noise allowlist must stay disjoint from DSX-STA. |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-20-A-01 | Tampering (self-reference) | the HIGH stratum reading _GOLDEN_SHIP_FINDINGS (which already lists which of the fifteen fire) as "what fired" — a tautological catch rate | high | mitigate | The stratum derives its catch only from live self._gate_findings filtered to HIGH; the verify gate asserts _GOLDEN_SHIP_FINDINGS is not referenced in the method (D-09). |
| T-20-A-02 | Tampering (null result wearing a coverage star) | reporting a re-run of the CRITICAL-only harness as "re-baselined to cover the fifteen" when it is provably invariant to them | high | mitigate | The load-bearing HIGH verify/ship stratum (D-03) measures the fifteen where they actually fire; the CRITICAL partition is unchanged and the HIGH catch is a separate, non-empty readout. |
| T-20-A-03 | Tampering (headline drift) | folding the HIGH catch into _headline, moving the (miss-rate, FPR) pair or the anchor/floor | medium | mitigate | The HIGH catch is reported BESIDE the pair; the anchor (0.25,0.3) and floor 3 are re-asserted unmoved and the pair is proven invariant to the stratum's presence (D-06). |
| T-20-A-04 | Tampering (false negative control) | a good-corpus control that never reaches a DSX-STA-05x branch (silent-not-clean) or a real false positive laundered as tempdir noise | medium | mitigate | Each control declares the VALID form that reaches its branch and stays silent; the _FPR_TEMPDIR_NOISE_CODES-disjoint-from-DSX-STA guard blocks laundering (D-05). |
| T-20-A-05 | Tampering (spurious catch) | a new fixture firing DSX-STA-041 or a second Phase-18 code, misattributing the catch | low | mitigate | Each fixture omits analysis.outcome_type (no DSX-STA-041) and declares only its one trigger; the audit asserts exactly one of the fifteen fires per fixture. |
| T-20-A-SC | Tampering | npm/pip/cargo installs (supply chain) | low | accept | Zero packages installed; Python stdlib only (unittest, json, tempfile, pathlib). No Package Legitimacy Audit owed (vacuously satisfied). |
</threat_model>

<verification>
- After Task 1 commit: the corpus + golden suites are green; the five Phase-18 fixtures each fire exactly their target HIGH code, clear plan/execute, carry POSTMORTEM + NARRATIVE siblings and empty _EXPECTED_CAUGHT_DEFECTS keys, and each carries a measured golden key.
- After Task 2 commit: the three valid controls fire none of the fifteen; the FPR denominator is 15 (>=10) and grew; the noise allowlist is disjoint from DSX-STA.
- After Task 3 commit: `python3 -m unittest tests.test_known_bad_corpus -v` green; _classify_target_defect is severity-parameterised (default CRITICAL); the HIGH verify/ship stratum reports a live third readout beside the pair; the anchor (0.25,0.3) and floor 3 are unmoved; the HIGH catch is not read from the golden ledger.
- REQ-P20-01 completeness: known-bad fixtures exist for every new blocking code (the five Phase-18 via new fixtures; the ten Phase-19 already fire on bad-ANALYSIS-SPEC.yaml at ship), the stratified catch rate + FPR are re-measured (CRITICAL pair + HIGH third readout + grown FPR), and the calibration is re-baselined moving only _GOLDEN_SHIP_FINDINGS; catalogue stays 275; zero codes minted.
</verification>

<success_criteria>
- Five dedicated PRESENT known-bad fixtures fire the five Phase-18 codes (each exactly its own, clearing plan/execute, passing dsx validate); none is declared ABSENT (D-04); the D-13-a CRITICAL-only miss-union is not exploited.
- The single calibration harness is EXTENDED with a live HIGH verify/ship stratum (D-03): severity-parameterised _classify_target_defect (default CRITICAL), _HIGH_TARGET_DEFECT_CODES, the third readout read LIVE and never from _GOLDEN_SHIP_FINDINGS (D-09).
- The headline stays the (miss-rate, FPR) pair; the HIGH catch is reported beside it; the anchor (0.25,0.3) and floor 3 are unmoved; the only committed number that moved is _GOLDEN_SHIP_FINDINGS (D-06).
- Three valid good-corpus negative controls exercise each routing family and stay silent; the FPR denominator is >=10 and grew to 15; the noise allowlist is disjoint from DSX-STA (D-05).
- Effect-size bands stay conventions; the calibration keys on finding CODE identity only (D-08); zero codes minted; catalogue stays 275.
</success_criteria>

<output>
Create `.planning/phases/20-calibration-and-reporting-close/20-A-SUMMARY.md` when done.
</output>
