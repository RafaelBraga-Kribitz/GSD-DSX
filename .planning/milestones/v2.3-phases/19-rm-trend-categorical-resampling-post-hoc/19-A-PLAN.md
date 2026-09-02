---
phase: 19-rm-trend-categorical-resampling-post-hoc
plan: A
type: tdd
wave: 1
depends_on: []
files_modified:
  - dsx/spec.py
  - dsx/checks/stats.py
  - references/test-selection.md
  - references/finding-codes.md
  - tests/test_declared_rm_trend_routing.py
  - tests/test_declared_resampling_posthoc_routing.py
  - tests/test_p19_categorical_rows.py
autonomous: true
requirements: [REQ-P19-01, REQ-P19-02, REQ-P19-03, REQ-P19-04, REQ-P19-05, REQ-P19-06, REQ-P19-07]
tags: [statistics, routing-table, rm-anova, trend, categorical, resampling, post-hoc, proportion-count, finding-codes, declaration-gate, anti-two-stage]

must_haves:
  truths:
    - "Seven recommend_* pure functions exist in dsx/checks/stats.py — recommend_rm, recommend_trend, recommend_resampling, recommend_posthoc, recommend_variance_role, recommend_power, recommend_proportion_ci — each DATALESS: its inspect.signature carries only declared-context string parameters, with NO data/n/distribution/paired flag (REQ-P18-06 anti-two-stage carried forward); each returns the acceptable-test/interval SET per declared context and never selects a DEPRECATED row (Yates, SNK, unprotected-LSD-k>3, Vuong) as a default"
    - "dsx/spec.py carries the eight new declared sub-vocabularies SPHERICITY_CORRECTIONS, DOSE_SCORE_SCHEMES, AUTOCORRELATION_HANDLINGS, RESAMPLING_METHODS, VARIANCE_TESTS, VARIANCE_TEST_ROLES, POWER_REPORTING_TYPES, PROPORTION_CI_METHODS plus the POSTHOC_FAMILY_MAP routing dict, all closed and additive, registered in _VOCABULARIES for dsx vocab discovery"
    - "the six scalar closed-vocab fields (sphericity_correction, autocorrelation_handling, variance_test, variance_test_role, power_reporting_type, proportion_ci_method) are registered in _MEMBERSHIP_FIELDS so a mis-slotted value is loud via the existing DSX-STA-040 for free — zero new code for the recognition half"
    - "references/test-selection.md carries the RM, Trend, Categorical, Resampling, Post-hoc, and Proportion/count sections keyed on DECLARED fields, INCLUDING the DEPRECATED Yates row (status: deprecated, use N-1 chi-square, Campbell 2007), the log-linear pointer row, the Fisher-Freeman-Halton honesty footnote, the CMH surfaced-stratification row, the DEPRECATED SNK / unprotected-LSD-k>3 rows (Hayter 1986), the ZIP/hurdle pointer row, and the Vuong DEPRECATED row (misuse-only, Wilson 2015, NO replacement endorsed)"
    - "REQ-P19-03 (categorical) mints ZERO finding codes — it is rows + one DEPRECATED row + pointer row + honesty footnote only; the live catalogue declared total stays exactly 265 at the Wave-1 merge (rows/recommend/vocab add no report.add sites)"
    - "no numeric statistic is hard-coded anywhere: catalog-only / not-in-hand items ship as named rows with explicit confirm-at-source language and no fabricated boundary (Greenhouse-Geisser epsilon, Hamed-Rao lag threshold, Davidson-MacKinnon 19/99-vs-399/1499, Brown-Cai-DasGupta n<=40, Campbell smallest-expected-count>=1, Hayter numeric alpha, McCullagh-Nelder section number)"
  artifacts:
    - dsx/spec.py
    - dsx/checks/stats.py
    - references/test-selection.md
    - references/finding-codes.md
    - tests/test_declared_rm_trend_routing.py
    - tests/test_declared_resampling_posthoc_routing.py
    - tests/test_p19_categorical_rows.py
  key_links:
    - "each recommend_* dataless signature <-> its inspect.signature assertion in the two no-autoswitch routing test modules — a future contributor adding a data/n/distribution parameter turns the anti-two-stage proof red (REQ-P18-06 doctrine, extended to the six new families)"
    - "the eight new sub-vocabs + POSTHOC_FAMILY_MAP in spec.py <-> the recommend_* acceptable sets in stats.py <-> the test-selection.md rows — one source of truth per family, kept in doc/code lockstep in the same commit (standing v2.3 rule)"
    - "the six scalar membership fields in _MEMBERSHIP_FIELDS <-> the existing DSX-STA-040 single call site (stats.py:544-555) — a mis-slotted routing value is loud for free, no new code minted in Wave 1"
    - "the DEPRECATED/pointer rows in test-selection.md <-> NO code path (references/test-selection.md is parsed by no code, verified: only dsx/frame/prereg.py names the concept in prose) — a status:deprecated row mints nothing and blocks nothing this phase (active deprecation enforcement is a named D-13 deferral)"
    - "the Wave-1 seam to 19-C: 19-A defines the declared-field NAMES and vocabs that 19-C's ten gates read; freezing the names here (before 19-C writes the fixtures against them) is the whole reason for the rows-then-gates order (D-08)"
---

<objective>
Deliver the Phase-19 ROUTING SURFACE: the seven dataless recommend_* pure functions (RM, trend, resampling, post-hoc, variance-role, power, proportion/count), the eight closed declared sub-vocabularies plus the POSTHOC_FAMILY_MAP those functions and the Wave-2 gates read, the human-readable test-selection.md mirror for all six families (INCLUDING every DEPRECATED row, pointer row, honesty footnote, and the CMH surfaced-stratification row), and the no-autoswitch structural proofs — all keyed on DECLARED fields only, all in doc/code lockstep, and all minting ZERO finding codes so the catalogue STAYS at 265 at the Wave-1 merge.

Purpose: this is Wave 1 of the D-08 single-writer rows-then-gates split. It freezes the declared-field names and vocabularies BEFORE 19-C (Wave 2) writes the ten gates and the fixtures against them. REQ-P19-03 (categorical) is delivered IN FULL here — rows only, zero codes, the absent D-06 decade being the deliberate tell. The six other requirements get their ROWS + recommend_* here; their GATES land in 19-C. Every recommend_* signature is dataless — that IS the mechanical anti-two-stage proof (REQ-P18-06 doctrine), a stronger guarantee than a prose promise.

Output: seven recommend_* functions + trigger/route constants + six _MEMBERSHIP_FIELDS additions in dsx/checks/stats.py; eight sub-vocabs + POSTHOC_FAMILY_MAP + _VOCABULARIES registration in dsx/spec.py; six new sections in references/test-selection.md (RM / Trend / Categorical / Resampling / Post-hoc / Proportion-count) with all DEPRECATED, pointer, footnote, and surfaced rows; a no-op regeneration of references/finding-codes.md that STAYS 265; and three test modules (two no-autoswitch routing modules + one REQ-P19-03 doc-presence module).
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
@dsx/checks/stats.py
@dsx/spec.py
@references/test-selection.md
@tests/test_finding_catalogue_invariant.py
</context>

<field_bindings>
This plan RESOLVES the ten declared-field NAME bindings D-03 explicitly delegated to plan-time (19-RESEARCH.md Open Questions OQ-1..OQ-8). The SHAPES are fixed by D-03; the NAMES below are this plan's binding decisions. 19-C's gates and fixtures read exactly these names.

- OQ-1 (070 sphericity): field `analysis.sphericity_correction`, vocab SPHERICITY_CORRECTIONS = {unconditional_gg, unconditional_hf, mauchly_conditional, none}; the Wave-2 gate fires only on `mauchly_conditional` (the two-stage/Mauchly-conditional token). Scalar -> _MEMBERSHIP_FIELDS.
- OQ-2 (080 dose scores): field `analysis.dose_scores` (presence) + optional `analysis.dose_score_scheme`, vocab DOSE_SCORE_SCHEMES = {equally_spaced, midrank, custom}. The scheme is DSX-STA-040-guarded; the gate trigger is presence only.
- OQ-3 (081 autocorrelation): field `analysis.autocorrelation_handling`, vocab AUTOCORRELATION_HANDLINGS = {none, independent, hamed_rao, prewhitening, yue_pilon}; the Wave-2 gate keys on is_blank, NOT membership — a declared `none`/`independent` is non-blank and SATISFIES. Scalar -> _MEMBERSHIP_FIELDS.
- OQ-4 (090 resampling — the load-bearing unit call): nested block `analysis.resampling: {method, seed, B, unit}`, vocab RESAMPLING_METHODS = {permutation, percentile_bootstrap, bca}. BOUND: a DEDICATED `analysis.resampling.unit` field (the resampling exchangeability unit — cluster/block vs iid FOR THE RESAMPLE), NOT a reuse of design.randomization_unit / validity_frame.units (which live under design:/validity_frame:, describe assignment not the resample, and would let the gate pass on a unit that does not describe the resampling). The nested method is validated inside the gate helper, not the flat _MEMBERSHIP_FIELDS loop.
- OQ-5 (100 post-hoc): fields `analysis.omnibus` (declared omnibus test) + `analysis.posthoc` (declared post-hoc) + POSTHOC_FAMILY_MAP (omnibus-family -> acceptable-post-hoc frozenset), structured like _ASSOCIATION_ROUTES. BOUND: an EXPLICIT `analysis.omnibus` field, NOT a reuse of `analysis.test` (which may hold the post-hoc in a post-hoc-focused spec). Deprecated post-hocs (SNK, unprotected-LSD-k>3) are NEVER a member of any acceptable set.
- OQ-6 (110 variance role + estimand exemption): field `analysis.variance_test`, vocab VARIANCE_TESTS = {levene, brown_forsythe, bartlett, fligner_killeen}; field `analysis.variance_test_role`, vocab VARIANCE_TEST_ROLES = {precondition_to_location, scale_estimand}. BOUND: the exemption rides on the DECLARED ROLE field. Do NOT add a scale/dispersion member to ESTIMAND_KINDS this phase — spec.py:398-423 has six members and none denotes scale; reading the exemption off estimand_kind today would exempt nothing, and adding a member is scope creep (the smaller provable claim). Both scalar -> _MEMBERSHIP_FIELDS.
- OQ-7 (111/120/121/122): field `analysis.power_reporting_type`, vocab POWER_REPORTING_TYPES = {a_priori, design, observed, post_hoc, mde_sensitivity} (Wave-2 gate fires on {observed, post_hoc} only); field `analysis.proportion_ci_method`, vocab PROPORTION_CI_METHODS = {wilson, clopper_pearson, jeffreys, wald, agresti_coull} (gate fires on wald, n-independent); flat presence fields `analysis.exposure` + `analysis.offset` (121); flat presence fields `analysis.nnt` + `analysis.nnt_ci` (122). The two scalar vocab fields -> _MEMBERSHIP_FIELDS.
- OQ-8 (CMH surfaced, non-gated P19-03): fields `analysis.cmh_strata` + `analysis.interval_method`, presence-surfaced only, NO gate this phase (the CMH-stratifier gate is a named D-13 deferral).

TREND / VARIANCE FIELD DECISION (deviation from the research recommendation, bound here to resolve a collision the research left implicit): the Wave-2 gates 080/081 read a DEDICATED `analysis.trend_test` field (a string OR a list of strings — a defective spec may declare more than one trend analysis), and gate 110 reads the DEDICATED `analysis.variance_test` field above — NOT the single-valued top-level `analysis.test` the research sketched. Rationale, three-fold: (1) `analysis.test` is single-valued, but 080 (cochran_armitage), 081 (mann_kendall/sens_slope) and 110 (a variance test) are three mutually-exclusive triggers — keying all three on `analysis.test` makes the D-08 merge gate "the bad fixture fires all ten" UNSATISFIABLE in a single audit; (2) it dodges 19-RESEARCH.md Pitfall 1 (a trend/variance token in `analysis.test` trips a spurious DSX-STA-041 from the untouched _check_declared_test); (3) it is semantically precise for 110 — the pretest scenario has the LOCATION test as `analysis.test` and the variance test as a declared companion, so reading the variance test off `analysis.test` would misread the scale-estimand case. This is exactly the D-03/OQ planner-binding authority; the SHAPE ("a declared Cochran-Armitage trend with blank dose scores", etc.) is preserved. The trend_test membership is validated inside the Wave-2 helper (list-capable), not the flat loop.
</field_bindings>

<tasks>

<task type="auto">
  <name>Task 1: The eight declared sub-vocabularies + POSTHOC_FAMILY_MAP in dsx/spec.py, registered in _VOCABULARIES</name>
  <read_first>
    - dsx/spec.py lines 398-454 (ESTIMAND_KINDS confirmed six members with NONE denoting scale — OQ-6 Pitfall 6; and the Phase-18 additive-vocab precedent ICC_MODELS/ICC_TYPES/ICC_DEFINITIONS/KAPPA_WEIGHT_TOKENS/OPERAND_SCALES with their comment style and the "registered in stats.py _MEMBERSHIP_FIELDS" note)
    - dsx/spec.py lines 620-659 (the _VOCABULARIES registry — the tuple shape and the Phase-18 registration block at 654-658 to mirror; confirm the current end-of-list line before appending)
    - dsx/checks/stats.py lines 49-73 (_ASSOCIATION_ROUTES — the routing-dict shape POSTHOC_FAMILY_MAP mirrors: a declared-key -> acceptable-frozenset lookup)
    - 19-CONTEXT.md D-03 (the reuse-vs-add table) and D-01 (the exact trigger tokens); 19-RESEARCH.md Open Questions OQ-1..OQ-8 (the recommended vocab members) and the field_bindings block above (the bound names)
  </read_first>
  <files>dsx/spec.py</files>
  <action>In dsx/spec.py, after the Phase-18 correlation/agreement sub-vocab block (near OPERAND_SCALES, line 454), add a new "Phase 19 RM/trend/resampling/post-hoc/variance/power/proportion declared sub-vocabularies (REQ-P19-01/02/04/05/06/07)" comment section and define eight closed sets and one routing dict, all with the exact members from the field_bindings block: SPHERICITY_CORRECTIONS = {unconditional_gg, unconditional_hf, mauchly_conditional, none}; DOSE_SCORE_SCHEMES = {equally_spaced, midrank, custom}; AUTOCORRELATION_HANDLINGS = {none, independent, hamed_rao, prewhitening, yue_pilon}; RESAMPLING_METHODS = {permutation, percentile_bootstrap, bca}; VARIANCE_TESTS = {levene, brown_forsythe, bartlett, fligner_killeen}; VARIANCE_TEST_ROLES = {precondition_to_location, scale_estimand}; POWER_REPORTING_TYPES = {a_priori, design, observed, post_hoc, mde_sensitivity}; PROPORTION_CI_METHODS = {wilson, clopper_pearson, jeffreys, wald, agresti_coull}; and POSTHOC_FAMILY_MAP as a dict from a declared omnibus test (or omnibus family) to the frozenset of acceptable post-hoc procedures — at minimum welch_anova -> {games_howell, dunnett_t3}, anova -> {tukey_hsd, tukey_kramer, dunnett, scheffe}, kruskal_wallis -> {dunn, nemenyi}, friedman -> {nemenyi, conover}. Each constant gets a short comment naming its D-05 citation basis WITHOUT any fabricated numeric boundary (Greenhouse-Geisser 1959 for the sphericity tokens; Hamed-Rao 1998 for the autocorrelation handlings, noting the lag threshold is NOT encoded; Davidson-MacKinnon 2000 / Efron 1987 for the resampling methods, noting B's value is never checked and the BCa acronym is Efron-Tibshirani 1993 not the 1987 text; Zimmerman 2004 two-group-scoped for the variance-test roles with the principled-extension flag; Hoenig-Heisey 2001 / Lakens 2022 for the power-reporting types, noting MDE is the catalog's paraphrase not attributed to Lakens; Brown-Cai-DasGupta 2001 for the proportion-CI methods, noting the n<=40 cutoff is NOT hard-coded; Hayter 1986 / Games-Howell 1976 for POSTHOC_FAMILY_MAP). Add a comment on AUTOCORRELATION_HANDLINGS stating `none`/`independent` are MEMBERS whose PRESENCE satisfies the Wave-2 gate (the gate keys on is_blank, not membership). Register the eight closed sets in the _VOCABULARIES list (lines 620-659) following the Phase-18 tuple shape, with a dated Phase-19 comment; POSTHOC_FAMILY_MAP is a routing dict, not a describe-vocabulary set, so it is NOT added to _VOCABULARIES. Do NOT add any member to ESTIMAND_KINDS (OQ-6: no scale estimand_kind this phase). Do NOT edit dsx/checks/stats.py, references/, or any tracking file in this task.</action>
  <verify>
    <automated>python3 -c "from dsx import spec; assert spec.SPHERICITY_CORRECTIONS=={'unconditional_gg','unconditional_hf','mauchly_conditional','none'}; assert 'bca' in spec.RESAMPLING_METHODS and 'permutation' in spec.RESAMPLING_METHODS; assert spec.VARIANCE_TESTS=={'levene','brown_forsythe','bartlett','fligner_killeen'}; assert spec.VARIANCE_TEST_ROLES=={'precondition_to_location','scale_estimand'}; assert {'observed','post_hoc','mde_sensitivity'}<=set(spec.POWER_REPORTING_TYPES); assert spec.PROPORTION_CI_METHODS=={'wilson','clopper_pearson','jeffreys','wald','agresti_coull'}; assert {'none','independent'}<=set(spec.AUTOCORRELATION_HANDLINGS); assert 'games_howell' in spec.POSTHOC_FAMILY_MAP.get('welch_anova',frozenset()); assert 'scale' not in ' '.join(spec.ESTIMAND_KINDS); print('spec vocabs OK')"</automated>
  </verify>
  <acceptance_criteria>
    - The inline check prints "spec vocabs OK" and exits 0: all eight closed sets import with their exact members, POSTHOC_FAMILY_MAP routes welch_anova to a set containing games_howell, and ESTIMAND_KINDS gained no scale member.
    - The eight closed sets are registered in _VOCABULARIES (confirmable via a dsx vocab dump); POSTHOC_FAMILY_MAP is NOT registered (it is a routing dict).
    - No numeric boundary is hard-coded in any comment (Greenhouse-Geisser epsilon, Hamed-Rao lag, Davidson-MacKinnon B floors, Brown-Cai-DasGupta n cutoff, Hayter alpha) — the confirm-at-source / not-in-hand dispositions are named in prose only.
    - No edit to dsx/checks/stats.py, references/, or any tracking file.
  </acceptance_criteria>
  <done>The eight Phase-19 sub-vocabs and POSTHOC_FAMILY_MAP exist in dsx/spec.py with the bound members, the eight closed sets are registered in _VOCABULARIES, and ESTIMAND_KINDS is unchanged (no scale member).</done>
</task>

<task type="tdd" tdd="true">
  <name>Task 2 (RED then GREEN): the seven dataless recommend_* functions + _MEMBERSHIP_FIELDS additions, guarded by the two no-autoswitch structural proofs</name>
  <read_first>
    - dsx/checks/stats.py lines 9-29 (the import block from ..spec — the new sub-vocabs and POSTHOC_FAMILY_MAP must be added to this import), lines 40-73 (_MEMBERSHIP_FIELDS and _ASSOCIATION_ROUTES — the two shapes to extend/mirror), lines 194-213 (recommend_association — the EXACT dataless model to replicate: one declared-string parameter, returns {tests, ...}, raises ValueError for an out-of-route kind), lines 76-84 (PARAMETRIC_TESTS/NONPARAMETRIC_TESTS — DO NOT add any new test names here; that would trip DSX-STA-042 on a trend/RM declaration, 19-RESEARCH.md Anti-Patterns)
    - tests/test_no_shapiro_autoswitch.py (the inspect.signature structural-proof model) — RE-VERIFY the recommend_association signature test referenced in 19-RESEARCH.md as the template
    - dsx/spec.py the Task-1 constants and the is_blank/normalize/section helper signatures
    - 19-CONTEXT.md D-02 (dataless recommend_* beside recommend_test) and D-04 (recommend_* never selects a DEPRECATED row); 19-VALIDATION.md rows "No-autoswitch (REQ-P18-06 doctrine)" and the per-REQ routing oracles
  </read_first>
  <files>dsx/checks/stats.py, tests/test_declared_rm_trend_routing.py, tests/test_declared_resampling_posthoc_routing.py</files>
  <behavior>
    RED first — author both no-autoswitch modules so each fails against the current tree, then implement to GREEN:
    - test_declared_rm_trend_routing.py (REQ-P19-01/02/06 routing): inspect.signature(recommend_rm), (recommend_trend), and (recommend_variance_role) each list ONLY declared-context string parameters — assert there is NO parameter named or typed as data/n/n_groups/paired/normal/distribution (the anti-two-stage proof). recommend_rm returns an acceptable-test SET containing the unconditional-Greenhouse-Geisser RM-ANOVA route (and Friedman/Cochran-Q/Page-L for the rank cases) and NEVER a two-stage/Mauchly-conditional procedure. recommend_trend over a declared ordered-trend context returns a set containing cochran_armitage / jonckheere_terpstra / mann_kendall+sens_slope. recommend_variance_role returns the acceptable disposition SET keyed on the declared role and never endorses a variance pretest as a location-choice gate.
    - test_declared_resampling_posthoc_routing.py (REQ-P19-04/05/07 routing): inspect.signature(recommend_resampling), (recommend_posthoc), (recommend_power), (recommend_proportion_ci) each carry ONLY declared-context string parameters, no data/n flag. recommend_resampling returns a set drawn from RESAMPLING_METHODS with bca as the house default and never a bare/incomplete quadruple as "acceptable". recommend_posthoc(omnibus) returns POSTHOC_FAMILY_MAP[omnibus_family] and NEVER contains snk or unprotected_lsd (the DEPRECATED post-hocs, D-04). recommend_proportion_ci returns a set containing wilson (house default), clopper_pearson, jeffreys, agresti_coull and NEVER wald as an endorsed default.
  </behavior>
  <action>Add the Task-1 constants (SPHERICITY_CORRECTIONS, DOSE_SCORE_SCHEMES, AUTOCORRELATION_HANDLINGS, RESAMPLING_METHODS, VARIANCE_TESTS, VARIANCE_TEST_ROLES, POWER_REPORTING_TYPES, PROPORTION_CI_METHODS, POSTHOC_FAMILY_MAP) to the `from ..spec import (...)` block in dsx/checks/stats.py so BOTH this plan's recommend_* functions AND 19-C's gate helpers can read them without touching the import block again (freezes the import seam for Wave 2). Write seven pure dataless functions modelled EXACTLY on recommend_association (lines 194-213): recommend_rm, recommend_trend, recommend_resampling, recommend_posthoc, recommend_variance_role, recommend_power, recommend_proportion_ci. Each takes only declared-context string argument(s) — the load-bearing rule is NO data/n/n_groups/paired/normal/distribution parameter appears in any signature (that is the REQ-P18-06 proof) — normalizes its input, looks up the acceptable SET from the Task-1 vocabs / POSTHOC_FAMILY_MAP, and returns a dict carrying at least a `tests` (or `intervals`/`methods`) frozenset plus a citation label; raise ValueError for an out-of-route declared context, mirroring recommend_association. recommend_rm's acceptable set NEVER contains the two-stage/Mauchly-conditional procedure; recommend_posthoc's set is exactly POSTHOC_FAMILY_MAP[family] and NEVER contains snk or unprotected_lsd; recommend_proportion_ci NEVER endorses wald; recommend_resampling's house default is bca. Add the six SCALAR closed-vocab fields to _MEMBERSHIP_FIELDS (lines 40-44) as new tuples: ("sphericity_correction", SPHERICITY_CORRECTIONS), ("autocorrelation_handling", AUTOCORRELATION_HANDLINGS), ("variance_test", VARIANCE_TESTS), ("variance_test_role", VARIANCE_TEST_ROLES), ("power_reporting_type", POWER_REPORTING_TYPES), ("proportion_ci_method", PROPORTION_CI_METHODS) — so a mis-slotted value fires the existing DSX-STA-040 for free (do NOT register dose_score_scheme unless you also add its field; the resampling nested method and the str-or-list trend_test are validated in the Wave-2 helpers, not this flat loop). Do NOT add any test name to PARAMETRIC_TESTS/NONPARAMETRIC_TESTS. Do NOT write any _check_declared_* gate, do NOT wire anything into check(), do NOT add any report.add call site (Wave 2 owns all ten codes) — this task mints zero codes. Run the two RED modules first (they must fail: the functions do not exist), implement to GREEN. Do NOT edit references/, examples/, or any tracking file.</action>
  <verify>
    <automated>python3 -m unittest tests.test_declared_rm_trend_routing tests.test_declared_resampling_posthoc_routing -v && python3 -c "import inspect; from dsx.checks import stats; import dsx.checks.stats as S; [print(n, list(inspect.signature(getattr(S,n)).parameters)) for n in ('recommend_rm','recommend_trend','recommend_resampling','recommend_posthoc','recommend_variance_role','recommend_power','recommend_proportion_ci')]; banned={'data','n','n_groups','paired','normal','equal_variance','n_per_group','overdispersed','distribution'}; assert all(not (banned & set(inspect.signature(getattr(S,n)).parameters)) for n in ('recommend_rm','recommend_trend','recommend_resampling','recommend_posthoc','recommend_variance_role','recommend_power','recommend_proportion_ci')), 'a recommend_* took a data/n flag'; assert 'snk' not in S.recommend_posthoc('welch_anova')['tests'] and 'wald' not in S.recommend_proportion_ci('proportion')['tests']; print('dataless routing OK')"</automated>
  </verify>
  <acceptance_criteria>
    - Both no-autoswitch test modules are GREEN, and the inline check prints "dataless routing OK": every recommend_* signature is free of any data/n/distribution parameter (the REQ-P18-06 anti-two-stage proof extended to all six new families), recommend_posthoc never returns snk, recommend_proportion_ci never returns wald.
    - The six scalar fields are in _MEMBERSHIP_FIELDS; a mis-slotted value would fire DSX-STA-040 (confirmable by driving stats.check with an out-of-vocab sphericity_correction).
    - PARAMETRIC_TESTS and NONPARAMETRIC_TESTS are byte-unchanged; no test name added.
    - Zero report.add sites added; the catalogue is unaffected in this task.
  </acceptance_criteria>
  <done>The seven dataless recommend_* functions exist and route to acceptable sets that exclude every DEPRECATED procedure; both no-autoswitch structural proofs are green; the six scalar membership fields are registered; no code is minted and no gate is wired.</done>
</task>

<task type="auto">
  <name>Task 3: The six test-selection.md sections (rows + DEPRECATED + pointer + footnote + CMH surfaced), the no-op finding-codes.md regen at 265, and the REQ-P19-03 doc-presence proof</name>
  <read_first>
    - references/test-selection.md lines 65-129 (the Association/agreement section and its Status-column pointer-row table at 96-101 — the exact mechanism the Phase-19 DEPRECATED/pointer/footnote rows extend; and the "catalog-only, named without numeric boundaries" convention at 120-122 to mirror)
    - references/finding-codes.md line 16 (**Total: 265 codes.** — this must be UNCHANGED after this task)
    - tests/test_finding_catalogue_invariant.py lines 36-46 and 58-105 (the 265 assertions — this test must STAY green at 265 through Wave 1; this task does NOT edit it, only re-runs it)
    - 19-CONTEXT.md D-01 (REQ-P19-03 mints zero codes), D-04 (the DEPRECATED routing-off mechanism and the pointer-vs-deprecated distinction with the exact why-citations: Yates->N-1 Campbell 2007; SNK/LSD-k>3->protected post-hoc Hayter 1986 JASA 81(396):1000-1004; Vuong->misuse-only Wilson 2015, NO replacement), D-06 (CMH is a row not a gate — the named D-13 deferral); 19-RESEARCH.md Pattern 3 (doc-only, minted-nothing) and the Deferred Ideas (Fisher-Freeman-Halton honesty footnote)
  </read_first>
  <files>references/test-selection.md, references/finding-codes.md, tests/test_p19_categorical_rows.py</files>
  <action>In references/test-selection.md append six new sections, each the human-readable mirror of the matching recommend_* function and each keyed on DECLARED fields (add a Status column where a section carries deprecated/pointer rows, mirroring the Association section's 96-101 table). (1) "## Repeated measures" — unconditional Greenhouse-Geisser one-way RM-ANOVA (the RM analog of always-Welch), Friedman, Cochran's Q, Page's L rows; mixed-model and GEE pointer rows (status: pointer, routing-neutral, point outward); note the two-stage sphericity procedure is what the Wave-2 DSX-STA-070 gate blocks, and that Greenhouse-Geisser 1959 Psychometrika 24(2):95-112 is cited as a bibliographic locator only with epsilon computed from data, never a printed boundary. (2) "## Trend" — Cochran-Armitage (declared dose scores required), Jonckheere-Terpstra, Mann-Kendall + Sen's slope (declared autocorrelation handling required, Hamed-Rao 1998, lag threshold NOT printed) rows. (3) "## Categorical" — N-1 chi-square as the default replacing Yates; the DEPRECATED Yates row (status: deprecated, "use N-1 chi-square instead", why-citation Campbell 2007 Stat Med 26(19):3661-3675, note the smallest-expected-count>=1 boundary is confirm-at-source not printed); CMH with a declared-stratification SURFACED row (status: surfaced, non-blocking — the CMH-stratifier gate is a named D-13 deferral); G-test and exact multinomial / chi-square GOF rows; a log-linear POINTER row (status: pointer, McCullagh-Nelder Ch.6, no section number pinned); and a Fisher-Freeman-Halton honesty FOOTNOTE stating no practical unconditional r x c test with a shipping implementation exists (a D-13 entry condition). This section mints ZERO codes. (4) "## Resampling" — permutation, percentile bootstrap, BCa (house default) rows; note the Wave-2 DSX-STA-090 gate requires the full {method, seed, resampling-unit, B} quadruple, that B's value is never checked, and that 19/99 (an exactness floor) must not be conflated with 399/1499 (a recommended minimum) — Davidson-MacKinnon 2000, no B value printed. (5) "## Post-hoc" — Games-Howell (house default after Welch ANOVA), Tukey/Kramer, Dunnett (+T3), Dunn, Nemenyi, Scheffe rows; DEPRECATED SNK and unprotected-LSD-at-k>3 rows (status: deprecated, "use a protected post-hoc instead", why-citation Hayter 1986 JASA 81(396):1000-1004, the k=3-vs-k>=4 boundary confirm-at-source, no numeric alpha printed); note the Wave-2 DSX-STA-100 gate matches the declared post-hoc family against the declared omnibus family. (6) "## Proportion and count extras" — Wilson (house default), Clopper-Pearson, one-sample exact binomial, RD/RR/OR with named interval methods (Newcombe for RD; Woolf for OR — surfaced, not gated), NNT with mandatory CI rows; a ZIP/hurdle POINTER row (status: pointer); a Vuong DEPRECATED row (status: deprecated, misuse-finding ONLY — the null on the parameter-space boundary violates Vuong's interior-point prerequisite — Wilson 2015 Economics Letters 127:51-53, NO replacement test endorsed); note the Wave-2 gates block a declared Wald interval (DSX-STA-120, n-independent, n<=40 not hard-coded, Brown-Cai-DasGupta 2001), a declared exposure with no offset (DSX-STA-121), and a declared NNT with no CI (DSX-STA-122). Ship every catalog-only / not-in-hand item as a named row with explicit confirm-at-source language and NO fabricated numeric boundary or page locator (D-07). Then run `python3 scripts/gen-finding-catalogue.py --write` to regenerate references/finding-codes.md — because this plan added zero report.add sites the regen is a NO-OP diff and the total STAYS 265; stage it so the doc/code/catalogue lockstep is explicit. Author tests/test_p19_categorical_rows.py (REQ-P19-03 doc-presence): CRLF-safe substring assertions over references/test-selection.md that the Yates DEPRECATED row, the log-linear pointer row, the CMH surfaced-stratification row, and the Fisher-Freeman-Halton footnote are all present, AND a re-assertion (importing the invariant module's constant or re-reading the Total line) that the catalogue declared total is exactly 265 — proving REQ-P19-03 minted nothing. Do NOT edit tests/test_finding_catalogue_invariant.py (it stays at 265 and is only re-run). Do NOT edit dsx/, examples/, or any tracking file.</action>
  <verify>
    <automated>python3 scripts/gen-finding-catalogue.py --check && python3 -m unittest tests.test_p19_categorical_rows tests.test_finding_catalogue_invariant -v && python3 -c "import re,pathlib; t=pathlib.Path('references/test-selection.md').read_text(encoding='utf-8'); assert re.search(r'Repeated measures',t) and 'Cochran-Armitage' in t and 'Games-Howell' in t and 'Wilson' in t; assert re.search(r'(?i)yates',t) and re.search(r'(?i)deprecated',t) and re.search(r'(?i)fisher.freeman.halton',t) and re.search(r'(?i)log-linear',t) and re.search(r'(?i)cmh|cochran.mantel.haenszel',t); c=pathlib.Path('references/finding-codes.md').read_text(encoding='utf-8'); assert '265 codes' in ' '.join(c.split()); print('rows+deprecated+footnote present; catalogue stays 265')"</automated>
  </verify>
  <acceptance_criteria>
    - The inline check prints "rows+deprecated+footnote present; catalogue stays 265" and exits 0: all six sections are present with their family rows, the Yates DEPRECATED row, the log-linear pointer, the CMH surfaced row, and the Fisher-Freeman-Halton footnote are all in test-selection.md, and finding-codes.md still declares 265.
    - scripts/gen-finding-catalogue.py --check exits 0 (the regen is a no-op diff; no code was minted); tests/test_finding_catalogue_invariant.py stays GREEN at 265 with set-identity holding (no drift); tests/fixtures/finding-codes-phase12.md is byte-unchanged.
    - tests/test_p19_categorical_rows.py is green and its assertions are CRLF-safe (repo checks out CRLF).
    - No numeric boundary or fabricated page locator is printed for any catalog-only / not-in-hand item (Campbell expected-count, Hayter alpha, McCullagh-Nelder section, Davidson-MacKinnon B, Brown-Cai-DasGupta n cutoff).
    - No edit to dsx/, examples/, tests/test_finding_catalogue_invariant.py, or any tracking file.
  </acceptance_criteria>
  <done>All six test-selection.md sections ship with their rows plus every DEPRECATED / pointer / footnote / surfaced row; REQ-P19-03 is delivered in full with ZERO codes; finding-codes.md regen is a no-op that stays 265; the invariant test stays green at 265; the REQ-P19-03 doc-presence module passes.</done>
</task>

</tasks>

<single_writer_proof>
Phase 19 is a two-wave, sequential, single-writer split (D-08). 19-C depends_on 19-A and runs in Wave 2 only after Wave 1 merges — so no shared file is ever written concurrently. Every shared file has EXACTLY ONE writer per wave:

| File | Wave 1 writer (19-A) | Wave 2 writer (19-C) | Concurrent write? |
|------|----------------------|----------------------|-------------------|
| dsx/checks/stats.py | 19-A (recommend_* + trigger consts + import block + 6 _MEMBERSHIP_FIELDS entries) | 19-C (the 7 gate helpers + dispatcher + wiring at check() lines 231/247) | No — different waves, different regions |
| dsx/spec.py | 19-A (8 sub-vocabs + POSTHOC_FAMILY_MAP + _VOCABULARIES) | — (not written) | No |
| references/test-selection.md | 19-A (recommend_* mirror rows + DEPRECATED/pointer/footnote/CMH surfaced) | 19-C (the ten gate-code doc entries, gate-lockstep) | No — different waves |
| references/finding-codes.md | 19-A (regen, no-op diff, stays 265) | 19-C (regen -> 275) | No — different waves |
| scripts/gen-finding-catalogue.py | — (19-A only RUNS --check/--write) | 19-C (_D05_ALLOWLIST_CODES += 10 by exact name) | No |
| tests/test_finding_catalogue_invariant.py | — (19-A only RE-RUNS it, stays 265) | 19-C (bump 265->275, +10 minted, method rename) | No |
| examples/bad-ANALYSIS-SPEC.yaml | — | 19-C (extend to fire all ten) | No |

CORRECTION to 19-CONTEXT.md D-08's single-writer table (surfaced for the orchestrator): D-08 places `_D05_ALLOWLIST_CODES` in `dsx/spec.py`; it actually lives in `scripts/gen-finding-catalogue.py:168-178` (verified live; 19-RESEARCH.md §Diagram corrects this). Consequence: `dsx/spec.py` is written by 19-A ONLY (not 19-C), and `scripts/gen-finding-catalogue.py` is written by 19-C ONLY. The single-writer-per-wave invariant holds under the corrected allocation. The seam: 19-C READS what 19-A wrote in stats.py (the recommend_* functions, the imported vocabs, the _MEMBERSHIP_FIELDS entries) and in spec.py (the vocabs) but WRITES only new regions (the gate helpers and the check() wiring) — a read-after-write across sequential waves, never a concurrent write.
</single_writer_proof>

<threat_model>
**register_authored_at_plan_time: true** — this STRIDE register was authored at planning time (S3-2). /gsd-secure-phase 19 reads this flag. ASVS L1, block_on: high. This phase adds only declaration-only string/structure comparisons and pure dataless routing lookups with no data path, no new I/O surface, and no new dependency; there is no high-severity open threat (matching the 19-CONTEXT.md persona round's decision not to engage the Auditor lens).

## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| analyst-authored ANALYSIS-SPEC.yaml -> dsx loader -> stats.check | Untrusted declared strings/structures cross here. Wave 1 adds six closed-vocabulary recognition guards (via DSX-STA-040 reuse) and seven pure dataless routing lookups; no data is read, no value is computed. |
| recommend_* acceptable sets <-> references/test-selection.md rows | The doc mirror must not drift from the routing functions; doc/code lockstep in the same commit is the boundary control. |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-19-A-01 | Tampering | a closed-vocabulary recognition guard implemented as substring/fuzzy match, letting an adjacent value pass | low | mitigate | The six new scalar fields join _MEMBERSHIP_FIELDS which uses exact normalize(value)-not-in-vocab equality only (stats.py:544-555); no fuzzy/prefix match. |
| T-19-A-02 | Tampering (of the routing contract) | a recommend_* function silently returning a DEPRECATED procedure (Yates/SNK/unprotected-LSD/Vuong) as an acceptable default | low | mitigate | The acceptable SETs exclude every deprecated procedure by construction; the no-autoswitch modules assert recommend_posthoc never returns snk and recommend_proportion_ci never returns wald. |
| T-19-A-03 | Tampering (data-then-pick) | a recommend_* function gaining a data/n/distribution parameter, reintroducing two-stage selection | low | mitigate | inspect.signature structural assertions in the two routing modules fail red on any data/n/distribution parameter (REQ-P18-06 doctrine); a signature-inspecting test cannot silently rot. |
| T-19-A-04 | Tampering (false authority) | a fabricated numeric locator/boundary for a D-07 not-in-hand item printed into test-selection.md | low | mitigate | Every catalog-only / not-in-hand item ships as a named row with explicit confirm-at-source language and NO numeric boundary (Greenhouse-Geisser epsilon, Hamed-Rao lag, Davidson-MacKinnon B, Brown-Cai-DasGupta n, Campbell expected-count, Hayter alpha, McCullagh-Nelder section). |
| T-19-A-05 | Tampering (docs drift from behaviour) | test-selection.md rows drifting from the recommend_* acceptable sets | low | mitigate | Rows and recommend_* land in the same commit (doc/code lockstep, standing v2.3 rule); finding-codes.md regen (--check) confirms the catalogue stayed 265. |
| T-19-A-SC | Tampering | npm/pip/cargo installs (supply chain) | low | accept | Zero packages installed; Python stdlib only (unittest, inspect, re). No Package Legitimacy Audit owed (vacuously satisfied). |
</threat_model>

<verification>
- After Task 1 commit: the spec-vocab inline check exits 0 (eight sets + POSTHOC_FAMILY_MAP present, no scale estimand_kind added).
- After Task 2 commit: `python3 -m unittest tests.test_declared_rm_trend_routing tests.test_declared_resampling_posthoc_routing -v` all green; every recommend_* signature is dataless; recommend_posthoc/recommend_proportion_ci exclude the deprecated defaults.
- After Task 3 commit: `python3 scripts/gen-finding-catalogue.py --check` exit 0 at 265; `python3 -m unittest tests.test_p19_categorical_rows tests.test_finding_catalogue_invariant -v` green; all six sections + DEPRECATED/pointer/footnote/CMH rows present.
- Wave-1 merge gate (orchestrator, after 19-A merges — no 19-B this phase): `python3 -m unittest discover -s tests -q` fully green; the catalogue declared total asserts == 265 (rows/recommend/vocab mint no codes); doc/code lockstep holds; the no-autoswitch proofs cover all six new families.
</verification>

<success_criteria>
- Seven dataless recommend_* functions route RM / trend / resampling / post-hoc / variance-role / power / proportion-count to acceptable sets that exclude every deprecated procedure (REQ-P19-01/02/04/05/06/07 routing half); every signature is data-free (REQ-P18-06 doctrine).
- Eight closed sub-vocabs + POSTHOC_FAMILY_MAP exist in spec.py, registered in _VOCABULARIES; six scalar fields join _MEMBERSHIP_FIELDS (DSX-STA-040 recognition for free); ESTIMAND_KINDS is unchanged (OQ-6).
- All six test-selection.md sections ship with the DEPRECATED Yates row, log-linear pointer, CMH surfaced row, Fisher-Freeman-Halton footnote, DEPRECATED SNK/LSD rows, ZIP/hurdle pointer, and Vuong DEPRECATED row; no numeric boundary or fabricated locator is printed (D-07).
- REQ-P19-03 is delivered in full with ZERO new codes; the catalogue stays exactly 265 at the Wave-1 merge; the invariant test is green at 265; the phase12 snapshot is byte-frozen.
- The declared-field names are frozen for 19-C (the rows-then-gates seam): 19-C's ten gates and the extended bad fixture read exactly the names bound in this plan's field_bindings block.
</success_criteria>

<output>
Create `.planning/phases/19-rm-trend-categorical-resampling-post-hoc/19-A-SUMMARY.md` when done.
</output>
