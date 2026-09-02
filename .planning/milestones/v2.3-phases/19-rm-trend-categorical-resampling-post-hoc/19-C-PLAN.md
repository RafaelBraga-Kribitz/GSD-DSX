---
phase: 19-rm-trend-categorical-resampling-post-hoc
plan: C
type: tdd
wave: 2
depends_on: [19-A]
files_modified:
  - dsx/checks/stats.py
  - scripts/gen-finding-catalogue.py
  - references/finding-codes.md
  - references/test-selection.md
  - tests/test_finding_catalogue_invariant.py
  - examples/bad-ANALYSIS-SPEC.yaml
  - tests/test_rm_sphericity_gate.py
  - tests/test_trend_gate.py
  - tests/test_resampling_gate.py
  - tests/test_posthoc_gate.py
  - tests/test_variance_role_gate.py
  - tests/test_power_reporting_gate.py
  - tests/test_proportion_count_gate.py
autonomous: true
requirements: [REQ-P19-01, REQ-P19-02, REQ-P19-04, REQ-P19-05, REQ-P19-06, REQ-P19-07]
tags: [statistics, declaration-gate, finding-codes, rm-anova, trend, resampling, post-hoc, variance-pretest, power-reporting, proportion-count, d05-allowlist, fixtures]

must_haves:
  truths:
    - "dsx/checks/stats.py carries a _check_declared_advanced_stats(analysis, spec, report) dispatcher wired at BOTH check() call sites (the not-tests early-return near line 231 AND the post-loop return near line 247), so a pure declaration-only Phase-19 spec with no results.tests is still gated"
    - "the ten codes are emitted by SEVEN per-family _check_declared_* helpers (rm_sphericity/trend/resampling/posthoc/variance_role/power_reporting/proportion_count), each carrying its own attributable D-05 Citation: and Structural criterion: docstring, because gen-finding-catalogue.py resolves docstrings per nearest-enclosing FunctionDef"
    - "DSX-STA-070 fires only on declared analysis.sphericity_correction == mauchly_conditional and NEVER on the mere presence of repeated measures; DSX-STA-080 fires on a declared cochran_armitage trend with blank dose_scores; DSX-STA-081 fires on a declared mann_kendall/sens_slope trend with is_blank(autocorrelation_handling) and is SILENT on a declared none/independent (is_blank predicate, not membership)"
    - "DSX-STA-090 fires on a declared analysis.resampling block with an incomplete {method, seed, B, unit} quadruple, naming the missing member, ONE code not four; DSX-STA-100 fires when declared analysis.posthoc is not in POSTHOC_FAMILY_MAP for the declared analysis.omnibus family; DSX-STA-110 fires on a declared analysis.variance_test with role blank OR precondition_to_location and is SILENT on scale_estimand; DSX-STA-111 fires only on analysis.power_reporting_type in {observed, post_hoc}"
    - "DSX-STA-120 fires on analysis.proportion_ci_method == wald (n-independent, no hard-coded n<=40); DSX-STA-121 fires on declared analysis.exposure with blank analysis.offset; DSX-STA-122 fires on declared analysis.nnt with blank analysis.nnt_ci"
    - "the finding catalogue is exactly the frozen Phase-12 snapshot (256, byte-unchanged) + four pre-existing mints + five Phase-18 codes + exactly the ten new Phase-19 codes; declared total is 275; references/finding-codes.md is regenerated in the same commit as the ten report.add sites"
    - "all ten codes are named by exact code in _D05_ALLOWLIST_CODES in scripts/gen-finding-catalogue.py (the DSX-STA- family prefix is NOT allowlisted), so gen-finding-catalogue.py --check enforces each one's Citation:/Structural criterion:/# D-05 marker and exits 0"
    - "examples/good-ANALYSIS-SPEC.yaml fires NONE of the ten (unedited, research-confirmed silent); examples/bad-ANALYSIS-SPEC.yaml (extended, not replaced) fires all ten; the phase12 fixture stays byte-frozen at 256"
  artifacts:
    - dsx/checks/stats.py
    - scripts/gen-finding-catalogue.py
    - references/finding-codes.md
    - references/test-selection.md
    - tests/test_finding_catalogue_invariant.py
    - examples/bad-ANALYSIS-SPEC.yaml
    - tests/test_rm_sphericity_gate.py
    - tests/test_trend_gate.py
    - tests/test_resampling_gate.py
    - tests/test_posthoc_gate.py
    - tests/test_variance_role_gate.py
    - tests/test_power_reporting_gate.py
    - tests/test_proportion_count_gate.py
  key_links:
    - "the ten report.add sites <-> the regenerated references/finding-codes.md (same commit) <-> gen-finding-catalogue.py --check as the drift gate; the ten codes in _D05_ALLOWLIST_CODES <-> check_d05 citation enforcement (an omission silently skips the D-05 gate because DSX-STA- is not an allowlisted prefix)"
    - "the seven per-family helpers <-> _resolve_docstrings' per-FunctionDef resolution (scripts/gen-finding-catalogue.py:303-342) — a monolith would launder seven distinct citation obligations under one docstring; the split keeps each attributable"
    - "_check_declared_advanced_stats wired at BOTH check() call sites (231 and 247) <-> a pure declaration-only spec with no results.tests still gets gated (19-RESEARCH.md Pattern 2)"
    - "the ten gate trigger fields (bound in 19-A's field_bindings) <-> the extended bad fixture's analysis block firing all ten <-> good's untouched analysis block firing none"
    - "the _EXPECTED_TOTAL/_MINTED_CODES/_SNAPSHOT_TOTAL triple in test_finding_catalogue_invariant.py moves as a set (265->275, +10, snapshot stays 256) — bumping one leg without the other fails the set-identity test"
---

<objective>
Deliver the Phase-19 GATE SURFACE: the ten new HIGH declaration-only finding codes (DSX-STA-070/080/081/090/100/110/111/120/121/122), split into SEVEN per-family _check_declared_* helpers dispatched from a single _check_declared_advanced_stats wired at BOTH check() call sites; the _D05_ALLOWLIST_CODES additions by exact name; the finding-codes.md regen to 275 and the invariant-test triple bump; the ten gate-code doc entries in test-selection.md (gate-lockstep); and the extended bad fixture that fires all ten while good stays silent. Catalogue 265 -> 275.

Purpose: this is Wave 2 of the D-08 rows-then-gates split — the gates read the declared-field NAMES 19-A froze in Wave 1. The seven-helper split is not cosmetic: gen-finding-catalogue.py resolves each code's D-05 citation from its nearest-enclosing function's docstring, so a monolith emitting all ten would satisfy the build with ONE shared docstring, laundering seven genuinely distinct citation obligations. Every predicate compares DECLARED strings/structures against a closed vocabulary or a presence check — never data (the anti-two-stage invariant).

Output: _check_declared_advanced_stats + seven per-family helpers emitting the ten codes in dsx/checks/stats.py, wired at both check() sites; the ten codes in scripts/gen-finding-catalogue.py's _D05_ALLOWLIST_CODES; references/finding-codes.md regenerated to 275; the ten gate-code doc entries in references/test-selection.md; the invariant-test triple moved to 275; the extended examples/bad-ANALYSIS-SPEC.yaml; and seven new gate test modules carrying the # D-05 markers.
</objective>

<execution_context>
@$HOME/.claude/gsd-core/workflows/execute-plan.md
@$HOME/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/19-rm-trend-categorical-resampling-post-hoc/19-CONTEXT.md
@.planning/phases/19-rm-trend-categorical-resampling-post-hoc/19-RESEARCH.md
@.planning/phases/19-rm-trend-categorical-resampling-post-hoc/19-VALIDATION.md
@.planning/phases/19-rm-trend-categorical-resampling-post-hoc/19-A-PLAN.md
@dsx/checks/stats.py
@dsx/spec.py
@scripts/gen-finding-catalogue.py
@tests/test_finding_catalogue_invariant.py
@examples/bad-ANALYSIS-SPEC.yaml
@examples/good-ANALYSIS-SPEC.yaml
</context>

<dependency_note>
This plan is Wave 2 and depends_on 19-A. Before executing, RE-VERIFY the live line numbers 19-RESEARCH.md pins (they were read immediately after Phase 18 closed and 19-A now sits on top): the two check() call sites (currently stats.py:230-231 and :246-247 — 19-A added no new call site, but confirm the exact lines), the _D05_ALLOWLIST_CODES block (gen-finding-catalogue.py:168-178, the Phase-18 comment precedent at 157-167), and the invariant-test triple (test_finding_catalogue_invariant.py: _EXPECTED_TOTAL line 36, _SNAPSHOT_TOTAL line 42, _MINTED_CODES 43-46, method test_finding_catalogue_stays_at_265_codes line 59). The declared-field NAMES and vocabs this plan reads are the ones 19-A bound in its field_bindings block (already imported into stats.py by 19-A) — this plan writes only the gate helpers and the check() wiring, never the recommend_* functions, the vocabs, or the import block.
</dependency_note>

<gate_predicates>
The exact firing predicate per code (all HIGH; all keyed on DECLARED fields; is_blank short-circuit then normalized equality/membership; absence of the trigger field is non-blocking, D-10):

- DSX-STA-070 (helper _check_declared_rm_sphericity): normalize(analysis.sphericity_correction) == "mauchly_conditional". NEVER keys on the presence of repeated measures (D-06 — else it false-blocks the legitimate mixed-model/GEE route, which has no sphericity step).
- DSX-STA-080 (helper _check_declared_trend): "cochran_armitage" in the declared trend_test set AND is_blank(analysis.dose_scores).
- DSX-STA-081 (helper _check_declared_trend): any of {"mann_kendall","sens_slope"} in the declared trend_test set AND is_blank(analysis.autocorrelation_handling). is_blank predicate, NOT membership — a declared "none"/"independent" is non-blank and SATISFIES (Pitfall 5). The trend_test field is str OR list; collect its non-blank normalized tokens into a set (list-capable).
- DSX-STA-090 (helper _check_declared_resampling): analysis.resampling present (a dict, or analysis.resampling.method present) AND any of {method, seed, B, unit} is_blank -> ONE code whose message NAMES the missing member(s). Never checks B's value.
- DSX-STA-100 (helper _check_declared_posthoc): not is_blank(analysis.omnibus) AND not is_blank(analysis.posthoc) AND normalize(analysis.posthoc) not in POSTHOC_FAMILY_MAP.get(normalize(analysis.omnibus), frozenset()). Membership against the acceptable family-map, like DSX-STA-041's alternatives.
- DSX-STA-110 (helper _check_declared_variance_role): normalize(analysis.variance_test) in VARIANCE_TESTS AND (is_blank(analysis.variance_test_role) OR normalize(analysis.variance_test_role) == "precondition_to_location"). SILENT on scale_estimand (the scale test IS the correct primary analysis when scale is the estimand). Undeclared role -> block for declaration-incompleteness. Keys on the DECLARED role, never on the presence of Levene/BF/Bartlett/Fligner (D-06).
- DSX-STA-111 (helper _check_declared_power_reporting): normalize(analysis.power_reporting_type) in {"observed","post_hoc"}. {a_priori, design, mde_sensitivity} do NOT fire (narrow — D-06; broadening is a D-13 deferral).
- DSX-STA-120 (helper _check_declared_proportion_count): normalize(analysis.proportion_ci_method) == "wald". n-independent; the n<=40 cutoff is NOT hard-coded.
- DSX-STA-121 (helper _check_declared_proportion_count): not is_blank(analysis.exposure) AND is_blank(analysis.offset).
- DSX-STA-122 (helper _check_declared_proportion_count): not is_blank(analysis.nnt) AND is_blank(analysis.nnt_ci).
</gate_predicates>

<tasks>

<task type="tdd" tdd="true">
  <name>Task 1 (RED then GREEN): the seven per-family gate helpers + the dispatcher wired at both check() sites, emitting the ten codes</name>
  <read_first>
    - dsx/checks/stats.py lines 219-248 (check() and the TWO declaration-gate call sites at 230-231 and 246-247 — the dispatcher is added beside _check_declared_association at BOTH; RE-VERIFY the exact current lines) and lines 633-797 (the Phase-18 _check_declared_association dispatcher + _check_correlation_scale_kind + _check_agreement_completeness split — the EXACT precedent to mirror: a thin dispatcher calling per-predicate-group helpers, each with its own D-05 docstring; note the is_blank short-circuit, the isinstance-before-normalize discipline, and the report.add signature)
    - dsx/checks/stats.py lines 9-29 (the import block — 19-A already imported the eight vocabs + POSTHOC_FAMILY_MAP; confirm they are present and do NOT re-import) and lines 557-560 (the _check_declared_test outcome_type early-return — 19-RESEARCH.md Pitfall 1: a gate-test fixture declaring outcome_type + test both non-blank trips DSX-STA-041; the unit fixtures avoid this)
    - dsx/findings.py Report.add / Report.ok signatures
    - scripts/gen-finding-catalogue.py lines 303-342 (_resolve_docstrings, per nearest-enclosing FunctionDef — WHY seven helpers) and 360-390 (check_d05 requires a Citation: line, a Reference value:/Structural criterion: line, and a # D-05: <CODE> test marker per allowlisted code) and 345-357 (_collect_test_markers reads # D-05: <CODE> comments under tests/)
    - 19-CONTEXT.md D-01/D-06/D-07 (the predicates, the over-block guards, the citation dispositions); 19-A-PLAN.md field_bindings (the exact field names/vocabs); 19-VALIDATION.md the per-REQ gate oracles
  </read_first>
  <files>dsx/checks/stats.py, tests/test_rm_sphericity_gate.py, tests/test_trend_gate.py, tests/test_resampling_gate.py, tests/test_posthoc_gate.py, tests/test_variance_role_gate.py, tests/test_power_reporting_gate.py, tests/test_proportion_count_gate.py</files>
  <behavior>
    RED first — author all seven gate test modules so each fails against the current tree (the helpers do not exist), then implement to GREEN. Each module drives the specific helper (or stats.check on a minimal analysis dict) and asserts the codes list EXHAUSTIVELY so a stray DSX-STA-041/040 cannot hide behind an `in` check (Pitfall 1: omit analysis.outcome_type in the fixture, or call the helper directly; name the choice in the test docstring). Each module carries a `# D-05: <CODE>` comment for EVERY code it exercises so check_d05 can resolve the marker.
    - test_rm_sphericity_gate.py (REQ-P19-01, DSX-STA-070): fires on {sphericity_correction: mauchly_conditional}; SILENT on unconditional_gg, on absent sphericity_correction, and — the over-block guard — on a spec that merely declares repeated measures without the two-stage token.
    - test_trend_gate.py (REQ-P19-02, DSX-STA-080/081): 080 fires on {trend_test: cochran_armitage} with blank dose_scores, silent when dose_scores present; 081 fires on {trend_test: mann_kendall} (and sens_slope) with blank autocorrelation_handling, and is SILENT on {trend_test: mann_kendall, autocorrelation_handling: none} (the is_blank tell — a declared none satisfies); a list trend_test [cochran_armitage, mann_kendall] with both companions blank fires BOTH 080 and 081.
    - test_resampling_gate.py (REQ-P19-04, DSX-STA-090): fires ONCE on an incomplete {method, seed, B, unit} block naming the missing member; silent on the complete quadruple; a block missing two members still fires exactly one code (not four).
    - test_posthoc_gate.py (REQ-P19-05, DSX-STA-100): fires on {omnibus: kruskal_wallis, posthoc: tukey_hsd} (post-hoc not in the map for that omnibus family); silent on a matched pair {omnibus: welch_anova, posthoc: games_howell}; a declared deprecated post-hoc (snk) is never a member of any acceptable set.
    - test_variance_role_gate.py (REQ-P19-06a, DSX-STA-110): fires on {variance_test: levene, variance_test_role: precondition_to_location} and on {variance_test: levene} with blank role (declaration-incompleteness); SILENT on {variance_test: levene, variance_test_role: scale_estimand}; never keys on the presence of Levene alone without a role read.
    - test_power_reporting_gate.py (REQ-P19-06b, DSX-STA-111): fires on {power_reporting_type: observed} and {power_reporting_type: post_hoc}; SILENT on a_priori, design, and mde_sensitivity (narrow).
    - test_proportion_count_gate.py (REQ-P19-07, DSX-STA-120/121/122): 120 fires on {proportion_ci_method: wald} (and silent on wilson/jeffreys, n-independent); 121 fires on {exposure: person_years} with blank offset (silent when offset present); 122 fires on {nnt: 12} with blank nnt_ci (silent when nnt_ci present).
  </behavior>
  <action>In dsx/checks/stats.py, after _check_agreement_completeness (near line 797), add _check_declared_advanced_stats(analysis, spec, report) as a thin dispatcher modelled EXACTLY on _check_declared_association (line 633): early-return on empty analysis, then call the seven per-family helpers in order. Write the seven helpers, each with its own docstring carrying a Citation: line and a Structural criterion: line so gen-finding-catalogue.py resolves each code's D-05 obligation to the right function: _check_declared_rm_sphericity (DSX-STA-070; Citation: Greenhouse-Geisser 1959 Psychometrika 24(2):95-112, PIN bib locator only, epsilon is computed from data never a fixture, NOT the reversed 1958 Annals paper; Maxwell-Delaney 2004 ch.11-12 catalog-paraphrase); _check_declared_trend (DSX-STA-080/081; Citation: Cochran 1954 / Armitage 1955 for 080, Hamed-Rao 1998 J.Hydrology 204(1-4):182-196 for 081, PIN bib locator, do NOT hard-code the autocorrelation lag threshold); _check_declared_resampling (DSX-STA-090; Citation: Davidson-MacKinnon 2000 Econometric Reviews 19(1):55-68 catalog-only never check B's value, Efron 1987 JASA 82(397):171-185 PIN bib, do NOT attribute the BCa acronym to the 1987 text); _check_declared_posthoc (DSX-STA-100; Citation: Hayter 1986 JASA 81(396):1000-1004 catalog-only NOT the 1984 Annals no numeric alpha, Games-Howell 1976 J.Educational Statistics 1(2):113-125 PIN bib period-correct); _check_declared_variance_role (DSX-STA-110; Citation: Zimmerman 2004 BJMSP 57(1):173-181 PIN bib, finding catalog-only two-group scoped with the principled-extension flag that the mechanism is invariant to group count and the empirical k-group magnitude is UNVERIFIED, Bancroft 1944 not-in-hand backlog); _check_declared_power_reporting (DSX-STA-111; Citation: Hoenig-Heisey 2001 Amer.Statistician 55(1):19-24 PIN the identity scope catalog-only fire NARROWLY, Lakens 2022 Collabra:Psychology 8(1):33267 PIN bib, MDE is the catalog's paraphrase not attributed to Lakens); _check_declared_proportion_count (DSX-STA-120/121/122; Citation: Brown-Cai-DasGupta 2001 Statistical Science 16(2):101-133 PIN bib n<=40 NOT hard-coded n-independent for 120, McCullagh-Nelder 1989 Ch.6 Log-Linear Models chapter-granular do NOT pin section 6.2 for 121, and for 122 the internal completeness doctrine — a point NNT ships with its interval because its sampling distribution is discontinuous — with Altman-Deeks-Sackett 1998 BMJ 317:1309-1312 named as a row-bibliography confirm-at-execute item NOT an owed gate-code read). Implement each firing predicate EXACTLY as the gate_predicates block states, with an is_blank short-circuit and exact normalized equality/membership only; DSX-STA-090 emits ONE code naming the missing quadruple member(s); DSX-STA-100 membership-tests against POSTHOC_FAMILY_MAP; all ten are severity HIGH via report.add. Wire the dispatcher: add `_check_declared_advanced_stats(analysis, spec, report)` immediately after the `_check_declared_association(...)` line at BOTH check() call sites (the not-tests early-return branch AND the post-loop return — Pattern 2); a declaration-only Phase-19 spec hits the early-return branch, so BOTH sites are mandatory or the gates silently skip. Do NOT touch the recommend_* functions, the vocabs, _MEMBERSHIP_FIELDS, PARAMETRIC_TESTS/NONPARAMETRIC_TESTS, dsx/spec.py, dsx/mathx.py, or any tracking file. Do NOT regenerate finding-codes.md or edit the allowlist in this task (Task 2 owns catalogue infra). Run the seven RED modules first (they must fail), implement to GREEN.</action>
  <verify>
    <automated>python3 -m unittest tests.test_rm_sphericity_gate tests.test_trend_gate tests.test_resampling_gate tests.test_posthoc_gate tests.test_variance_role_gate tests.test_power_reporting_gate tests.test_proportion_count_gate -v && python3 -c "from dsx.checks import stats; import inspect; src=inspect.getsource(stats.check); assert src.count('_check_declared_advanced_stats(')>=2, 'dispatcher not wired at both call sites'; print('dispatcher wired at both sites')"</automated>
  </verify>
  <acceptance_criteria>
    - All seven gate test modules are GREEN: each code fires on its exact declared trigger and is silent otherwise, with the over-block guards proven (070 never fires on repeated-measures presence; 081 silent on a declared none; 110 silent on scale_estimand; 111 silent on a_priori/design/mde_sensitivity).
    - DSX-STA-090 emits exactly ONE code for an incomplete quadruple (asserted by an exhaustive codes-count check), naming the missing member; DSX-STA-100 uses POSTHOC_FAMILY_MAP membership.
    - _check_declared_advanced_stats appears at BOTH check() call sites (the inline getsource count >= 2); a declaration-only spec with no results.tests reaches the gates.
    - The seven helpers are separate functions, each with a Citation: and Structural criterion: docstring line; each gate test module carries a `# D-05: <CODE>` marker for every code it exercises.
    - Pitfall 1 is handled: no gate test lets a stray DSX-STA-041/040 pass its assertion (codes asserted exhaustively; the handling is named in each test docstring).
    - No edit to recommend_*, vocabs, spec.py, mathx.py, finding-codes.md, the allowlist, or any tracking file.
  </acceptance_criteria>
  <done>The seven per-family helpers emit the ten HIGH codes with the exact D-01/D-06 predicates and the over-block guards; the dispatcher is wired at both check() sites; each helper carries its own D-05 citation docstring and each code has a # D-05 test marker; all seven gate modules pass.</done>
</task>

<task type="auto">
  <name>Task 2: The D-05 allowlist additions, the finding-codes.md regen to 275, and the invariant-test triple bump</name>
  <read_first>
    - scripts/gen-finding-catalogue.py lines 87-89 (_D05_ALLOWLIST_PREFIXES — confirm DSX-STA- is NOT present, which is why the by-exact-name addition is mandatory; 19-RESEARCH.md Pitfall 3) and lines 157-178 (the Phase-18 dated-comment precedent block and the _D05_ALLOWLIST_CODES frozenset the ten codes append to; the exact addition is sketched in 19-RESEARCH.md as commented lines to uncomment/adapt)
    - tests/test_finding_catalogue_invariant.py lines 32-46 (_EXPECTED_TOTAL=265 line 36, _SNAPSHOT_TOTAL=256 line 42 byte-frozen, _MINTED_CODES 43-46) and lines 58-105 (the method test_finding_catalogue_stays_at_265_codes line 59 and the several 265-mentioning docstrings/assert messages) and lines 108-143 (the set-identity test's expected_set and its 265-mentioning prose) — 19-RESEARCH.md Pitfall 4 lists every line to move
    - references/finding-codes.md line 16 (**Total: 265 codes.** -> 275 after regen) — the file is generated, NEVER hand-edited
    - 19-CONTEXT.md D-08 (catalogue 265->275; the ten codes by exact name); 19-RESEARCH.md Pitfalls 3 and 4
  </read_first>
  <files>scripts/gen-finding-catalogue.py, references/finding-codes.md, tests/test_finding_catalogue_invariant.py</files>
  <action>In scripts/gen-finding-catalogue.py add the ten codes DSX-STA-070, DSX-STA-080, DSX-STA-081, DSX-STA-090, DSX-STA-100, DSX-STA-110, DSX-STA-111, DSX-STA-120, DSX-STA-121, DSX-STA-122 by EXACT NAME to the _D05_ALLOWLIST_CODES frozenset (lines 168-178), with a dated Phase-19 (REQ-P19-01/02/04/05/06/07, 2026-09-02) comment block after the Phase-18 block, matching that block's precedent style and stating why the exact-code path is used (DSX-STA- is a ~40-code legacy family with no citation; a prefix add would fail the build on all of them). Do NOT add DSX-STA- to _D05_ALLOWLIST_PREFIXES. Regenerate references/finding-codes.md by running `python3 scripts/gen-finding-catalogue.py --write` (the ten new report.add sites from Task 1 raise the total to 275) and stage the regenerated file IN THIS SAME COMMIT (never hand-edit it). In tests/test_finding_catalogue_invariant.py move the triple as a SET (Pitfall 4): _EXPECTED_TOTAL 265 -> 275; add the ten Phase-19 codes to _MINTED_CODES; _SNAPSHOT_TOTAL STAYS 256 and tests/fixtures/finding-codes-phase12.md is NEVER mutated; rename the method test_finding_catalogue_stays_at_265_codes -> test_finding_catalogue_stays_at_275_codes; update the 265-mentioning docstrings and assert messages in both test methods to 275 and name the Phase-19 mint (keep all prose CRLF-safe). Do NOT edit dsx/, examples/, references/test-selection.md, or any tracking file in this task.</action>
  <verify>
    <automated>python3 scripts/gen-finding-catalogue.py --check && python3 -m unittest tests.test_finding_catalogue_invariant -v && python3 -c "import pathlib; g=pathlib.Path('scripts/gen-finding-catalogue.py').read_text(encoding='utf-8'); assert all(c in g for c in ('DSX-STA-070','DSX-STA-080','DSX-STA-081','DSX-STA-090','DSX-STA-100','DSX-STA-110','DSX-STA-111','DSX-STA-120','DSX-STA-121','DSX-STA-122')); c=pathlib.Path('references/finding-codes.md').read_text(encoding='utf-8'); assert '275 codes' in ' '.join(c.split()); print('allowlist + regen + invariant at 275 OK')"</automated>
  </verify>
  <acceptance_criteria>
    - scripts/gen-finding-catalogue.py --check exits 0: every one of the ten codes has a Citation: line, a Structural criterion: line, and a # D-05 marker (proves the Task-1 docstrings and the allowlist agree); the check would go RED if any of the ten lost its citation.
    - All ten codes are in _D05_ALLOWLIST_CODES by exact name; DSX-STA- is NOT in _D05_ALLOWLIST_PREFIXES.
    - references/finding-codes.md declares 275 and was regenerated (not hand-edited) in the same commit as the report.add sites.
    - tests/test_finding_catalogue_invariant.py is GREEN at declared total 275 with set-identity holding (frozen 256 snapshot + four prior + five Phase-18 + exactly the ten Phase-19 codes; no drift); _SNAPSHOT_TOTAL still 256 and the phase12 fixture byte-unchanged; the method is renamed to _275_codes.
    - No edit to dsx/, examples/, test-selection.md, or any tracking file.
  </acceptance_criteria>
  <done>The ten codes are citation-enforced via _D05_ALLOWLIST_CODES; finding-codes.md is regenerated to 275 in-commit; the invariant triple is moved as a set (275, +10, snapshot frozen at 256) and the test is green with set-identity.</done>
</task>

<task type="auto">
  <name>Task 3: The ten gate-code doc entries in test-selection.md, and the fixture discipline (bad fires all ten, good silent)</name>
  <read_first>
    - references/test-selection.md the six Phase-19 sections 19-A appended (RM/Trend/Categorical/Resampling/Post-hoc/Proportion-count) — the gate-code descriptive entries attach to these sections in lockstep with the code (add a bolded "**X gate (DSX-STA-0NN).**" paragraph per code, mirroring the Association section's "**Scale gate (DSX-STA-050).**" / "**Kind gate (DSX-STA-051).**" style at lines 83-94)
    - examples/bad-ANALYSIS-SPEC.yaml lines 85-89 (the analysis block to EXTEND — outcome_type/estimand_kind/n_groups/test:welch_t already present and already firing other codes) and examples/good-ANALYSIS-SPEC.yaml lines 154-163 (the analysis block — declares only standard fields, verified to carry NONE of the ten Phase-19 trigger fields, so it stays silent unedited)
    - tests/test_known_bad_corpus.py header lines 6-8 (the corpus invariant is structural/compositional — no test asserts an exact code set on the main bad fixture; each code-specific assertion lands with the phase that ships its code — so extending bad with the ten new triggers is safe) and tests/test_good_fixture_phase15.py (the good-fixture silence gate)
    - 19-CONTEXT.md D-08 (bad extended to fire all ten, good stays silent, extend-not-replace); 19-A-PLAN.md field_bindings (the exact trigger field names); 19-VALIDATION.md the D-08 fixture-discipline row
  </read_first>
  <files>references/test-selection.md, examples/bad-ANALYSIS-SPEC.yaml</files>
  <action>In references/test-selection.md add, under the matching 19-A section, one bolded gate-code entry per code, in gate-lockstep with the Task-1 report.add sites: the two-stage-sphericity gate (DSX-STA-070) under Repeated measures; the Cochran-Armitage-without-dose-scores (DSX-STA-080) and Mann-Kendall-without-autocorrelation-handling (DSX-STA-081, noting a declared none/independent satisfies) gates under Trend; the incomplete-resampling-quadruple gate (DSX-STA-090) under Resampling; the post-hoc-family-mismatch gate (DSX-STA-100) under Post-hoc; the variance-test-as-location-pretest gate (DSX-STA-110, noting the scale_estimand exemption and the Zimmerman two-group-scoped principled-extension flag) under a new variance/power subsection; the observed/post-hoc-power-in-a-readout gate (DSX-STA-111, narrow) beside it; and the Wald-interval (DSX-STA-120), exposure-without-offset (DSX-STA-121), and NNT-without-CI (DSX-STA-122) gates under Proportion and count extras. Each entry names its declared trigger field, its remedy, and its citation with NO fabricated numeric boundary. Then EXTEND examples/bad-ANALYSIS-SPEC.yaml's analysis block (do NOT replace the file; keep every existing defect) so it fires all ten, using the composable dedicated fields 19-A bound (each on its own field so all ten fire in one audit): add sphericity_correction: mauchly_conditional (070); trend_test as the list [cochran_armitage, mann_kendall] with dose_scores and autocorrelation_handling both absent (080 + 081); a resampling block with method: bca and seed present but B and unit absent (090, incomplete quadruple); omnibus: kruskal_wallis with posthoc: tukey_hsd (100, family mismatch); variance_test: levene with variance_test_role: precondition_to_location (110); power_reporting_type: observed (111); proportion_ci_method: wald (120); exposure: person_years with offset absent (121); nnt: 12 with nnt_ci absent (122). Choose values that are in-vocabulary so DSX-STA-040 does not fire on the new fields (only the ten intended gates fire from these additions). Do NOT edit examples/good-ANALYSIS-SPEC.yaml (verified silent, no edit owed — extend-not-replace is a safety rail, not a mandate to touch good). Do NOT edit dsx/, scripts/, tests/, or any tracking file in this task. After editing, prove the fixture discipline via a direct audit (see verify): bad fires all ten, good fires none.</action>
  <verify>
    <automated>python3 -m unittest tests.test_known_bad_corpus tests.test_good_fixture_phase15 -v && python3 -c "from dsx.loader import load; from dsx.checks import stats; TEN={'DSX-STA-070','DSX-STA-080','DSX-STA-081','DSX-STA-090','DSX-STA-100','DSX-STA-110','DSX-STA-111','DSX-STA-120','DSX-STA-121','DSX-STA-122'}; bad={f.code for f in stats.check(load('examples/bad-ANALYSIS-SPEC.yaml')).findings}; good={f.code for f in stats.check(load('examples/good-ANALYSIS-SPEC.yaml')).findings}; missing=TEN-bad; assert not missing, ('bad missing: '+str(sorted(missing))); leaked=TEN&good; assert not leaked, ('good leaked: '+str(sorted(leaked))); import re,pathlib; t=pathlib.Path('references/test-selection.md').read_text(encoding='utf-8'); assert all(('DSX-STA-0'+n) in t for n in ('70','80','81','90')) and all(('DSX-STA-1'+n) in t for n in ('00','10','11')) and all(('DSX-STA-1'+n) in t for n in ('20','21','22')); print('bad fires all ten; good silent; gate-code doc entries present')"</automated>
  </verify>
  <acceptance_criteria>
    - The direct audit prints "bad fires all ten; good silent; gate-code doc entries present": examples/bad-ANALYSIS-SPEC.yaml fires ALL ten Phase-19 codes in one stats.check pass, examples/good-ANALYSIS-SPEC.yaml fires NONE of them (and good is unedited).
    - tests/test_known_bad_corpus.py and tests/test_good_fixture_phase15.py are GREEN (the corpus invariant is structural, so the ten additions do not break it; any catch-rate re-baseline is REQ-P20-01, a Phase-20 concern, not this plan).
    - Every gate-code doc entry (all ten DSX-STA-0NN) is present in references/test-selection.md in lockstep with its report.add site.
    - The new bad-fixture fields are in-vocabulary so the additions fire ONLY the ten intended gates and not a spurious DSX-STA-040.
    - No edit to examples/good-ANALYSIS-SPEC.yaml, dsx/, scripts/, tests/, or any tracking file.
  </acceptance_criteria>
  <done>The ten gate-code doc entries ship in test-selection.md in gate-lockstep; the bad fixture is extended (not replaced) to fire all ten in one audit; good stays silent and unedited; the corpus and good-fixture gates remain green.</done>
</task>

</tasks>

<single_writer_proof>
Phase 19 is a two-wave, sequential, single-writer split (D-08); 19-C is Wave 2, depends_on 19-A, and runs only after Wave 1 merges — no shared file is written concurrently. Every shared file has EXACTLY ONE writer per wave:

| File | Wave 1 writer (19-A) | Wave 2 writer (19-C) | Concurrent write? |
|------|----------------------|----------------------|-------------------|
| dsx/checks/stats.py | 19-A (recommend_* + trigger consts + imports + 6 _MEMBERSHIP_FIELDS entries) | 19-C (7 gate helpers + dispatcher + wiring at check() 231/247) | No — different waves, different regions |
| dsx/spec.py | 19-A (8 sub-vocabs + POSTHOC_FAMILY_MAP + _VOCABULARIES) | — (not written) | No |
| references/test-selection.md | 19-A (recommend_* mirror rows + DEPRECATED/pointer/footnote/CMH) | 19-C (the ten gate-code doc entries, gate-lockstep) | No — different waves |
| references/finding-codes.md | 19-A (regen, no-op, stays 265) | 19-C (regen -> 275) | No — different waves |
| scripts/gen-finding-catalogue.py | — (19-A only RUNS it) | 19-C (_D05_ALLOWLIST_CODES += 10 by exact name) | No |
| tests/test_finding_catalogue_invariant.py | — (19-A only RE-RUNS it at 265) | 19-C (bump 265->275, +10, method rename) | No |
| examples/bad-ANALYSIS-SPEC.yaml | — | 19-C (extend to fire all ten) | No |
| examples/good-ANALYSIS-SPEC.yaml | — | — (verified silent, NOT edited) | No |

CORRECTION to 19-CONTEXT.md D-08's table (surfaced for the orchestrator): D-08 places `_D05_ALLOWLIST_CODES` in `dsx/spec.py`; it actually lives in `scripts/gen-finding-catalogue.py:168-178` (verified live; 19-RESEARCH.md §Diagram corrects this). Under the corrected allocation `dsx/spec.py` is a Wave-1 (19-A) write only and `scripts/gen-finding-catalogue.py` is a Wave-2 (19-C) write only — the single-writer-per-wave invariant holds. The seam: 19-C READS what 19-A wrote in stats.py (recommend_*, imported vocabs, _MEMBERSHIP_FIELDS) and spec.py (vocabs) but WRITES only new regions (the gate helpers + the check() wiring) — a read-after-write across sequential waves, never a concurrent write.
</single_writer_proof>

<threat_model>
**register_authored_at_plan_time: true** — this STRIDE register was authored at planning time (S3-2). /gsd-secure-phase 19 reads this flag. ASVS L1, block_on: high. This phase adds only declaration-only string/structure comparison gates with no data path, no new I/O surface, and no new dependency; there is no high-severity open threat.

## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| analyst-authored ANALYSIS-SPEC.yaml -> dsx loader -> stats.check | Untrusted declared strings/structures cross here. Wave 2 adds ten closed-vocabulary/presence gates on the analysis block; no data is read, no computation on values. |
| report.add call sites -> scripts/gen-finding-catalogue.py -> references/finding-codes.md | Generated docs must not drift from enforced behaviour; regen + --check is the boundary control. |
| the ten codes -> the D-05 citation build gate | A code inspected for a citation only if named in _D05_ALLOWLIST_CODES (DSX-STA- is not an allowlisted prefix); an omission silently ships an uncited gate. |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-19-C-01 | Repudiation | a new code ships uncited because the DSX-STA- family prefix is not in the D-05 allowlist | high | mitigate | All ten codes added by EXACT NAME to _D05_ALLOWLIST_CODES (Task 2); scripts/gen-finding-catalogue.py --check enforces the Citation:/Structural criterion:/# D-05 marker discipline per code and is the Task-2 gate. |
| T-19-C-02 | Tampering (citation laundering) | a monolithic gate emitting all ten codes under one shared docstring, satisfying the D-05 gate while seven distinct citation obligations go unmet | high | mitigate | Seven per-family helpers, each with its own attributable Citation: docstring (Pattern 1); _resolve_docstrings binds each code to its enclosing function. |
| T-19-C-03 | Tampering | a closed-vocabulary gate implemented as substring/fuzzy match, or DSX-STA-081 written as membership instead of is_blank (false-blocking a declared none) | medium | mitigate | Exact normalize(value) equality/membership only; DSX-STA-081 keys on is_blank (Pitfall 5), proven silent on a declared none by its unit test. |
| T-19-C-04 | Tampering (over-block) | DSX-STA-070 firing on repeated-measures presence, or DSX-STA-110 firing on Levene presence without a role read, false-blocking a legitimate route | medium | mitigate | 070 keys on the declared two-stage token only; 110 keys on the declared role (scale_estimand exempt); both over-block guards are asserted by their unit tests (D-06). |
| T-19-C-05 | Tampering (docs drift from behaviour) | regenerated finding-codes.md committed out of sync with the ten report.add sites, or a stale invariant total | medium | mitigate | finding-codes.md regenerated via --write in the same commit as the report.add sites; the invariant triple moves as a set (265->275, +10, snapshot frozen); --check is the drift gate. |
| T-19-C-06 | Tampering (false authority) | a fabricated numeric locator/boundary for a D-07 not-in-hand item printed into a gate docstring or a doc entry | low | mitigate | Gates check declared-field PRESENCE only; no numeric ships (Hamed-Rao lag, Brown-Cai-DasGupta n<=40, Campbell expected-count, McCullagh-Nelder section, Hayter alpha, Greenhouse-Geisser epsilon, Davidson-MacKinnon B); catalog-only dispositions carry explicit not-in-hand language. |
| T-19-C-SC | Tampering | npm/pip/cargo installs (supply chain) | low | accept | Zero packages installed; Python stdlib only (unittest, ast, re). No Package Legitimacy Audit owed (vacuously satisfied). |
</threat_model>

<verification>
- After Task 1 commit: the seven gate test modules are green; the dispatcher is wired at both check() call sites; each helper carries its own D-05 docstring and each code a # D-05 marker.
- After Task 2 commit: `python3 scripts/gen-finding-catalogue.py --check` exits 0 at 275; `python3 -m unittest tests.test_finding_catalogue_invariant -v` green at 275 with set-identity; the ten codes are in the allowlist by exact name.
- After Task 3 commit: the direct audit shows bad firing all ten and good firing none (good unedited); test_known_bad_corpus and test_good_fixture_phase15 green; the ten gate-code doc entries present in test-selection.md.
- Wave-2 merge gate (orchestrator, after 19-C merges): `python3 -m unittest discover -s tests -q` fully green; catalogue declared total asserts == 275; the D-05 citation build passes (all ten in the allowlist); good stays silent; bad fires all ten; `dsx validate` + `dsx gate plan` exit 0.
</verification>

<success_criteria>
- The ten HIGH codes fire on their exact declared predicates with the D-06 over-block guards (070 declared two-stage only; 081 is_blank not membership; 110 declared role with scale_estimand exempt; 111 narrow); split into seven per-family helpers each with an attributable D-05 citation (REQ-P19-01/02/04/05/06/07 gate half).
- The dispatcher is wired at BOTH check() call sites; a declaration-only spec is gated.
- The catalogue is exactly 275 (set-identity: frozen 256 + four prior + five Phase-18 + the ten Phase-19 codes); finding-codes.md regenerated in-commit; --check green; all ten citation-enforced via _D05_ALLOWLIST_CODES by exact name.
- The bad fixture (extended, not replaced) fires all ten; good stays silent and unedited; the phase12 snapshot is byte-frozen at 256.
- The ten gate-code doc entries ship in test-selection.md in gate-lockstep; no numeric boundary or fabricated locator is printed (D-07).
</success_criteria>

<output>
Create `.planning/phases/19-rm-trend-categorical-resampling-post-hoc/19-C-SUMMARY.md` when done.
</output>
