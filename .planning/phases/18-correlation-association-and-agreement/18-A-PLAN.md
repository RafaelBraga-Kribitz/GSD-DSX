---
phase: 18-correlation-association-and-agreement
plan: A
type: tdd
wave: 1
depends_on: []
files_modified:
  - dsx/checks/stats.py
  - dsx/spec.py
  - references/test-selection.md
  - references/finding-codes.md
  - scripts/gen-finding-catalogue.py
  - tests/test_declared_association_routing.py
  - tests/test_correlation_scale_kind_gate.py
  - tests/test_agreement_completeness_gate.py
  - tests/test_finding_catalogue_invariant.py
autonomous: true
requirements: [REQ-P18-01, REQ-P18-02, REQ-P18-03, REQ-P18-04, REQ-P18-06]
tags: [statistics, routing-table, correlation, agreement, finding-codes, declaration-gate, anti-two-stage]

must_haves:
  truths:
    - "recommend_association(estimand_kind) is dataless: its signature carries exactly one parameter estimand_kind, with no data/n/distribution flag (REQ-P18-06 anti-two-stage), and it returns the acceptable-coefficient SET per kind — linear_association -> {pearson_correlation, point_biserial}; monotone_association -> {spearman_correlation, kendall_tau_b}; nominal_association -> {phi, cramers_v}"
    - "DSX-STA-050 fires only when declared test == pearson_correlation AND declared operand_scale == ordinal; declared point_biserial and any declared-dichotomous operand never fire it (D-03 whitelist), and absence of operand_scale is non-blocking"
    - "DSX-STA-051 fires when the declared test is in the correlation family {pearson_correlation, spearman_correlation, kendall_tau_b, point_biserial, phi, cramers_v} AND declared estimand_kind is in {agreement, method_comparison}"
    - "DSX-STA-060 fires when ICC is declared (analysis.icc is a non-blank dict, or test == icc) AND any of model/type/definition is blank or out of its closed vocabulary; presence + membership only, combination-coherence is NOT built (deferred as candidate DSX-STA-063)"
    - "DSX-STA-061 fires when test == weighted_kappa AND weights is blank, or is neither a recognised string in {linear, quadratic} nor a non-empty explicit matrix; the guard branches on isinstance before any normalize (never stringifies a matrix)"
    - "DSX-STA-062 fires when test is in {cohens_kappa, weighted_kappa, fleiss_kappa} AND either p_pos or p_neg is missing; BOTH companions are required (D-04, the HQ-16-corrected p_pos-AND-p_neg reading, not raw-agreement+prevalence)"
    - "the finding catalogue is exactly the frozen Phase-12 snapshot (256, byte-unchanged) + the four pre-existing v2.2 mints + exactly the five new Phase-18 codes; declared total is 265; the regenerated references/finding-codes.md is committed in the same commit as the report.add call sites"
    - "both examples/good-ANALYSIS-SPEC.yaml and examples/bad-ANALYSIS-SPEC.yaml fire none of the five new codes, and neither fixture is edited (research-confirmed silence, D-08 extend-not-replace is a safety rail not a mandate)"
    - "the five codes are enforced by the D-05 citation build gate because they are named by exact code in _D05_ALLOWLIST_CODES (the DSX-STA- prefix is NOT allowlisted); scripts/gen-finding-catalogue.py --check exits 0 and would go non-zero if any of the five lost its citation line"
  artifacts:
    - dsx/checks/stats.py
    - dsx/spec.py
    - references/test-selection.md
    - references/finding-codes.md
    - scripts/gen-finding-catalogue.py
    - tests/test_declared_association_routing.py
    - tests/test_correlation_scale_kind_gate.py
    - tests/test_agreement_completeness_gate.py
    - tests/test_finding_catalogue_invariant.py
  key_links:
    - "recommend_association's dataless signature <-> test_declared_association_routing.py inspect.signature assertion — a future contributor adding a data/n/distribution parameter turns the anti-two-stage proof red (REQ-P18-06)"
    - "the five report.add(DSX-STA-050/051/060/061/062) sites <-> the regenerated references/finding-codes.md — same commit; scripts/gen-finding-catalogue.py --check is the drift gate"
    - "the five codes in _D05_ALLOWLIST_CODES <-> check_d05 citation enforcement — an omission silently skips the D-05 build gate because the DSX-STA- prefix is not allowlisted"
    - "_check_declared_association wired at BOTH check() call sites (the not-tests early return and the post-loop return) <-> a pure declaration-only correlation/agreement spec with no results.tests still gets gated"
    - "stats.py DSX-STA-012 branch <-> mathx.REPORT_ONLY_EFFECT_KINDS (owned by Plan 18-B) — the one cross-plan seam, resolved at the Wave-1 merge (see the coupling note in the objective)"
---

<objective>
Add the correlation and agreement/reliability routing surface and the two new declaration-only gates that key on the DECLARED estimand_kind and the declared test/agreement fields — never on data. This plan delivers the dataless routing function recommend_association, the gate _check_declared_association emitting five new HIGH finding codes (DSX-STA-050/051/060/061/062), the closed sub-vocabularies those codes read, the doc mirror in references/test-selection.md, and the regenerated finding catalogue at 265 codes — all in lockstep.

Purpose: this is the first catalog phase's correlation/agreement half. Every new check compares declared strings/structures in ANALYSIS-SPEC.yaml against closed vocabularies or acceptable-coefficient sets (the anti-two-stage invariant, REQ-P18-06). The dataless signature of recommend_association is itself the load-bearing proof that nothing here inspects data then picks.

Output: recommend_association + _check_declared_association (dispatching to _check_correlation_scale_kind for 050/051 and _check_agreement_completeness for 060/061/062) in dsx/checks/stats.py; new spec vocabularies in dsx/spec.py; the Association/agreement section in references/test-selection.md; the regenerated references/finding-codes.md (260 -> 265); the five codes named in scripts/gen-finding-catalogue.py's _D05_ALLOWLIST_CODES; three new test modules and one extended invariant test.

Cross-plan coupling (the ONE semantic seam, per 18-CONTEXT.md D-08): the DSX-STA-012 branch in dsx/checks/stats.py must consult a report-only effect-size registry (REPORT_ONLY_EFFECT_KINDS) that Plan 18-B creates in dsx/mathx.py. This plan owns the stats.py side of that seam; Plan 18-B owns the mathx.py registry and the test that pins the behaviour. To keep this plan importable and green in isolation, the seam reads the registry via a module-attribute access with a defensive empty default (Task 3), so its absence is inert until 18-B merges. Files stay disjoint (this plan never writes dsx/mathx.py, templates/APA-TABLE-research.md, or tests/test_effect_size_kind.py); the seam resolves at the Wave-1 merge.

Planner field-shape decisions (18-RESEARCH.md Open Questions OQ-1/2/3, explicitly delegated to this plan, resolved here — accepting the research recommendations): (1) the declared operand scale is a new field analysis.operand_scale with closed vocabulary {continuous, ordinal, dichotomous, nominal}, registered in the existing _MEMBERSHIP_FIELDS loop so a mis-slotted value is loud via DSX-STA-040 for free; the ordinal-vs-dichotomous split is what encodes D-03's ">2 levels" (a 2-level operand is declared dichotomous and is whitelisted). (2) the ICC triple nests under analysis.icc: {model, type, definition}. (3) the kappa companions are flat: analysis.weights, analysis.p_pos, analysis.p_neg.
</objective>

<execution_context>
@$HOME/.claude/gsd-core/workflows/execute-plan.md
@$HOME/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/18-correlation-association-and-agreement/18-CONTEXT.md
@.planning/phases/18-correlation-association-and-agreement/18-RESEARCH.md
@.planning/phases/18-correlation-association-and-agreement/18-VALIDATION.md
@dsx/checks/stats.py
@dsx/spec.py
@scripts/gen-finding-catalogue.py
@tests/test_finding_catalogue_invariant.py
@tests/test_no_shapiro_autoswitch.py
@references/test-selection.md
</context>

<artifacts_produced>
Symbols and files this plan creates or extends (five new finding codes minted; the effect-size band frozenset EFFECT_SIZE_KINDS is NOT widened here — that firewall is Plan 18-B's, and this plan only reads it):

- `recommend_association(estimand_kind: str)` — NEW dataless pure function in `dsx/checks/stats.py`; string -> {tests, effect_size, citation} lookup over the three association estimand kinds; raises ValueError for a kind with no association route (e.g. agreement/method_comparison/ordered_trend).
- `_ASSOCIATION_ROUTES`, `CORRELATION_FAMILY` — NEW module-level lookup constants in `dsx/checks/stats.py`.
- `_check_declared_association(analysis, spec, report)` — NEW gate dispatcher in `dsx/checks/stats.py`, wired at BOTH existing `_check_declared_test` call sites in `check()`.
- `_check_correlation_scale_kind(analysis, report)` — NEW private helper emitting DSX-STA-050 and DSX-STA-051, with its own D-05 citation docstring.
- `_check_agreement_completeness(analysis, report)` — NEW private helper emitting DSX-STA-060, DSX-STA-061, DSX-STA-062, with its own D-05 citation docstring.
- Finding codes **DSX-STA-050, DSX-STA-051, DSX-STA-060, DSX-STA-061, DSX-STA-062** — all HIGH; minted via `report.add(...)`.
- `ICC_MODELS`, `ICC_TYPES`, `ICC_DEFINITIONS`, `KAPPA_WEIGHT_TOKENS`, `OPERAND_SCALES` — NEW closed vocabularies in `dsx/spec.py`, registered in `_VOCABULARIES`.
- `operand_scale` entry added to `_MEMBERSHIP_FIELDS` in `dsx/checks/stats.py` (reuses DSX-STA-040 for recognition; zero new code for that half).
- DSX-STA-012 report-only seam in `dsx/checks/stats.py` (consults `mathx.REPORT_ONLY_EFFECT_KINDS`; see the cross-plan coupling note).
- Association / agreement section in `references/test-selection.md` (doc mirror of recommend_association; correlation + agreement rows + catalog-only pointer rows).
- Regenerated `references/finding-codes.md` (260 -> 265).
- The five codes added by exact name to `_D05_ALLOWLIST_CODES` in `scripts/gen-finding-catalogue.py`.
- `tests/test_declared_association_routing.py` (NEW), `tests/test_correlation_scale_kind_gate.py` (NEW), `tests/test_agreement_completeness_gate.py` (NEW), `tests/test_finding_catalogue_invariant.py` (EXTENDED).

Residual assumptions recorded (no silent drops): the three field shapes above are this plan's decisions per OQ-1/2/3, not committed contracts; if a future spec author prefers a different nesting, the vocabularies and predicates rename without re-architecting. The DSX-STA-012 seam behaviour is validated at the Wave-1 merge, not in this plan's isolated run.
</artifacts_produced>

<tasks>

<task type="auto">
  <name>Task 1: Declared-field vocabularies, the Association/agreement doc mirror, and the D-05 citation allowlist</name>
  <read_first>
    - dsx/spec.py lines 398-423 (ESTIMAND_KINDS — the six-member vocabulary the gate reads; confirm the three association kinds and their prose-named coefficients) and lines 588-633 (the _VOCABULARIES registry shape and the describe_vocabulary tail) and lines 634-690 (section/is_blank/normalize helpers the gate will use)
    - dsx/checks/stats.py lines 17-27 (OUTCOME_TYPES and _MEMBERSHIP_FIELDS — the existing membership-guard loop that operand_scale joins; note _MEMBERSHIP_FIELDS lives in stats.py, the vocab constant will live in spec.py)
    - scripts/gen-finding-catalogue.py lines 805-819 (the _D05_ALLOWLIST_CODES frozenset — the five new codes are already sketched in 18-RESEARCH.md as the exact addition to make; confirm the exact current line and the DSX-EXP-070/DSX-MET-021/DSX-COH-040 precedent comment style) and lines 87-89 (_D05_ALLOWLIST_PREFIXES — confirm DSX-STA- is NOT present, which is why the by-exact-name addition is mandatory)
    - references/test-selection.md (full file — confirm there is no correlation/agreement section yet; this section is appended as the doc mirror)
    - 18-CONTEXT.md D-01/D-02/D-05/D-07 (the acceptable-coefficient sets, the five codes' predicates, the ICC admissible values, the pin-vs-catalog-only dispositions); 18-RESEARCH.md § "Recommended shape" and Open Questions OQ-1/2/3; 18-VALIDATION.md Per-Task Verification Map rows REQ-P18-01/02
  </read_first>
  <files>dsx/spec.py, references/test-selection.md, scripts/gen-finding-catalogue.py</files>
  <action>In dsx/spec.py add five closed vocabularies as module-level constants near ESTIMAND_KINDS: ICC_MODELS = {one_way_random, two_way_random, two_way_mixed}; ICC_TYPES = {single, average}; ICC_DEFINITIONS = {consistency, absolute_agreement}; KAPPA_WEIGHT_TOKENS = {linear, quadratic}; OPERAND_SCALES = {continuous, ordinal, dichotomous, nominal}. Give each a short docstring/comment naming the admitting citation basis per 18-CONTEXT.md D-05 (Shrout and Fleiss 1979 / McGraw and Wong 1996 corrected for the ICC triple) and, for OPERAND_SCALES, note that the ordinal-vs-dichotomous split is what encodes D-03's ">2 levels" whitelist. Register all five in the _VOCABULARIES list (the same list dsx vocab dumps) following the existing tuple shape, so a spec author can discover them; ESTIMAND_KINDS stays a name->description dict, the new ones may be plain sets — match whatever _VOCABULARIES already accepts. In references/test-selection.md append a new "## Association / agreement" section that is the human-readable mirror of recommend_association: a correlation subsection with rows for linear_association (Pearson r, with the Fisher-z confidence-interval convention; point-biserial as Pearson r on a {0,1} dichotomy), monotone_association (Spearman rho, Kendall tau-b), nominal_association (phi for 2x2, Cramer's V for r x c), each keyed on the DECLARED estimand_kind and naming its effect size and primary citation; plus distance correlation and partial correlation as explicitly labelled catalog-only pointer rows (D-13 entry conditions unmet, no routing target). Then an agreement/reliability subsection with rows for Cohen's kappa, weighted kappa (declared weights), Fleiss kappa, Krippendorff alpha, the ICC declared as the (model, type, definition) triple, Bland-Altman for method_comparison, and a Cronbach-alpha -> McDonald-omega pointer row carrying the deprecation citation. Write catalog-only and not-in-hand items as named presence rows with no invented numeric boundary and no fabricated locator (D-07). In scripts/gen-finding-catalogue.py add the five codes DSX-STA-050, DSX-STA-051, DSX-STA-060, DSX-STA-061, DSX-STA-062 by exact name to _D05_ALLOWLIST_CODES, with a dated Phase-18 comment matching the DSX-EXP-070/DSX-MET-021/DSX-COH-040 precedent; do NOT add DSX-STA- to _D05_ALLOWLIST_PREFIXES (that would fail the build on ~40 uncited legacy codes). Do NOT regenerate finding-codes.md in this task (no report.add sites exist yet) and do NOT edit dsx/checks/stats.py in this task. Do NOT edit REQUIREMENTS.md, STATE.md, or ROADMAP.md.</action>
  <verify>
    <automated>python3 -c "from dsx import spec; assert {'one_way_random','two_way_random','two_way_mixed'}<=set(spec.ICC_MODELS); assert {'single','average'}<=set(spec.ICC_TYPES); assert {'consistency','absolute_agreement'}<=set(spec.ICC_DEFINITIONS); assert {'linear','quadratic'}<=set(spec.KAPPA_WEIGHT_TOKENS); assert {'continuous','ordinal','dichotomous','nominal'}<=set(spec.OPERAND_SCALES); import pathlib,re; t=pathlib.Path('references/test-selection.md').read_text(encoding='utf-8'); assert re.search(r'Association\s*/\s*agreement',t) and 'Krippendorff' in t and 'Bland-Altman' in t and 'Kendall' in t and 'McDonald' in t; g=pathlib.Path('scripts/gen-finding-catalogue.py').read_text(encoding='utf-8'); assert all(c in g for c in ('DSX-STA-050','DSX-STA-051','DSX-STA-060','DSX-STA-061','DSX-STA-062')); print('vocab+doc+allowlist OK')"</automated>
  </verify>
  <acceptance_criteria>
    - The inline check prints "vocab+doc+allowlist OK" and exits 0: the five spec vocabularies import with the exact admissible members from 18-CONTEXT.md D-05; references/test-selection.md contains an Association/agreement section naming Krippendorff, Bland-Altman, Kendall, and McDonald (the Cronbach->omega pointer); all five codes appear by exact name in scripts/gen-finding-catalogue.py.
    - scripts/gen-finding-catalogue.py --check still exits 0 at the pre-Phase-18 baseline of 260 codes (the allowlist entries are inert until the report.add sites exist — no new code is minted by this task).
    - The five vocabularies are registered in _VOCABULARIES (confirmable via a dsx vocab dump listing them); DSX-STA- is NOT added to _D05_ALLOWLIST_PREFIXES.
    - No edit to dsx/checks/stats.py, references/finding-codes.md, or any tracking file in this task.
  </acceptance_criteria>
  <done>The five spec vocabularies exist with their D-05 admissible members and are registered in _VOCABULARIES; references/test-selection.md carries the Association/agreement doc mirror with correlation, agreement, and catalog-only pointer rows; the five codes are named in _D05_ALLOWLIST_CODES by exact name; gen-finding-catalogue.py --check still passes at 260.</done>
</task>

<task type="tdd" tdd="true">
  <name>Task 2 (RED then GREEN then REFACTOR): recommend_association + the five-code declaration gate, wired into check(), catalogue regenerated in-commit</name>
  <read_first>
    - dsx/checks/stats.py lines 9-16 (the import block, especially `from ..spec import ... is_blank, normalize, section` and `from ..mathx import EFFECT_SIZE_KINDS, ...`) and lines 44-70 (recommend_test's signature — the model to sit beside, NOT to fold into) and the two _check_declared_test call sites (18-RESEARCH.md Pattern 2 pins them at the not-tests early-return branch near line 162 and the post-loop return near line 177 — RE-VERIFY the exact current line numbers before editing, per 18-RESEARCH.md "Valid until")
    - dsx/checks/stats.py lines 460-490 (_check_declared_test — read enough to understand Pitfall 1: it fires DSX-STA-041 whenever outcome_type AND test are both declared and non-blank, with no estimand_kind awareness; the new gate tests must avoid a false 041)
    - dsx/spec.py the new ICC_MODELS/ICC_TYPES/ICC_DEFINITIONS/KAPPA_WEIGHT_TOKENS/OPERAND_SCALES (from Task 1) and is_blank/normalize/section signatures
    - dsx/findings.py Report.add / Report.ok signatures (18-RESEARCH.md confirms them at lines 91-129)
    - tests/test_finding_catalogue_invariant.py lines 34-42 (_EXPECTED_TOTAL=260, _SNAPSHOT_TOTAL=256, _MINTED_CODES) — only _EXPECTED_TOTAL and _MINTED_CODES move; _SNAPSHOT_TOTAL and tests/fixtures/finding-codes-phase12.md are byte-frozen (the test file's own "D-08 trap #3")
    - tests/test_no_shapiro_autoswitch.py and 18-RESEARCH.md § "The no-autoswitch structural proof" (the inspect.signature model for REQ-P18-06)
    - 18-CONTEXT.md D-01/D-02/D-03/D-04/D-05; 18-RESEARCH.md § "Recommended shape (sketch, not yet written)", Pitfalls 1/2/3/4/5, and § "The exact invariant-test locators to bump"; 18-VALIDATION.md Per-Task Verification Map rows REQ-P18-01/03/04/06 + Catalogue mint proof + D-05 citation build gate
  </read_first>
  <files>dsx/checks/stats.py, references/finding-codes.md, tests/test_declared_association_routing.py, tests/test_correlation_scale_kind_gate.py, tests/test_agreement_completeness_gate.py, tests/test_finding_catalogue_invariant.py</files>
  <behavior>
    RED first — author these tests so each fails against the current tree, then implement to GREEN:
    - test_declared_association_routing.py (REQ-P18-01/06): recommend_association's signature is exactly the single parameter estimand_kind (inspect.signature list equals ["estimand_kind"]) — the anti-two-stage proof; recommend_association("linear_association")["tests"] == {pearson_correlation, point_biserial}; ("monotone_association") == {spearman_correlation, kendall_tau_b}; ("nominal_association") == {phi, cramers_v}; recommend_association("agreement") raises ValueError (no association route). Plus a doc-presence assertion reading references/test-selection.md for the catalog-only pointer rows (distance correlation, partial correlation, Cronbach->McDonald omega) named for REQ-P18-01/02.
    - test_correlation_scale_kind_gate.py (REQ-P18-03): DSX-STA-050 fires for {test: pearson_correlation, operand_scale: ordinal}; DSX-STA-050 does NOT fire for {test: point_biserial, operand_scale: ordinal} nor for {test: pearson_correlation, operand_scale: dichotomous} (the D-03 whitelist) nor when operand_scale is absent; DSX-STA-051 fires for any correlation-family test with estimand_kind in {agreement, method_comparison}, and does not fire for estimand_kind in the association kinds. Check the codes list EXHAUSTIVELY (Pitfall 1: assert DSX-STA-041 is NOT among the findings — omit outcome_type from the fixture dict, or drive _check_declared_association directly).
    - test_agreement_completeness_gate.py (REQ-P18-04): DSX-STA-060 fires when analysis.icc is declared with a missing or out-of-vocab model/type/definition, and is SILENT on a complete valid triple; DSX-STA-061 fires for {test: weighted_kappa} with blank weights and with an unrecognised string, ACCEPTS weights == "linear"/"quadratic" and ACCEPTS a non-empty explicit matrix (a nested list) without firing (Pitfall 5 — isinstance branch, never normalize on a list); DSX-STA-062 fires when either p_pos OR p_neg is missing for any of {cohens_kappa, weighted_kappa, fleiss_kappa}, and is silent when BOTH are present (D-04). Each new report.add site carries a `# D-05: <CODE>` test marker in the test module so check_d05 can resolve it.
    - test_finding_catalogue_invariant.py extension: _EXPECTED_TOTAL 260 -> 265; _MINTED_CODES gains the five Phase-18 codes; _SNAPSHOT_TOTAL stays 256 and the phase12 fixture is untouched.
  </behavior>
  <action>Implement in dsx/checks/stats.py exactly as 18-RESEARCH.md's "Recommended shape" sketches, adapted to the Task-1 vocabularies. Add module-level CORRELATION_FAMILY = {pearson_correlation, spearman_correlation, kendall_tau_b, point_biserial, phi, cramers_v} and _ASSOCIATION_ROUTES mapping the three association estimand kinds to (acceptable-coefficient frozenset, effect_size token, citation label). Write recommend_association(estimand_kind: str) as a dataless normalize-then-lookup returning {tests, effect_size, citation}, raising ValueError for a kind absent from _ASSOCIATION_ROUTES — its signature must carry ONLY estimand_kind (this is the REQ-P18-06 proof; do not add any data/n/flag parameter). Write _check_declared_association(analysis, spec, report) that early-returns on empty analysis then calls two private helpers. _check_correlation_scale_kind(analysis, report) emits DSX-STA-050 when normalize(analysis.test) == pearson_correlation AND normalize(analysis.operand_scale) == ordinal (the ordinal-vs-dichotomous split IS the >2-levels whitelist; point_biserial and dichotomous never reach this branch), and DSX-STA-051 when normalize(analysis.test) is in CORRELATION_FAMILY AND normalize(analysis.estimand_kind) is in {agreement, method_comparison}; give this helper its own docstring carrying a Citation: line for the correlation-scale doctrine and the P18-03 not-in-hand disposition (rest on the internal Phase-17 estimand_kind/scale definitions; no fabricated external locator — D-07) and a Structural criterion: line stating it is declaration-only. _check_agreement_completeness(analysis, report) emits DSX-STA-060 (walk analysis.icc's model/type/definition against ICC_MODELS/ICC_TYPES/ICC_DEFINITIONS with an is_blank short-circuit, presence + membership only, emit once), DSX-STA-061 (isinstance branch on analysis.weights per Pitfall 5: a string is checked against KAPPA_WEIGHT_TOKENS, a non-empty list/tuple is accepted as an explicit matrix, anything else fires), and DSX-STA-062 (fires when is_blank(analysis.p_pos) OR is_blank(analysis.p_neg) for a kappa-family test); give this helper its own docstring with the Shrout-Fleiss 1979 / McGraw-Wong 1996 corrected citation for the ICC triple and the Feinstein-Cicchetti 1990 Part I (paradoxes) + Part II (the p_pos/p_neg recommendation) citation for DSX-STA-062. All five are severity HIGH. Add "operand_scale", OPERAND_SCALES to _MEMBERSHIP_FIELDS (imported from spec) so a mis-slotted operand_scale is loud via DSX-STA-040 for free. Add the _check_declared_association(analysis, spec, report) call immediately beside _check_declared_test at BOTH call sites in check() (the not-tests early-return branch AND the post-loop return — Pattern 2). Then regenerate references/finding-codes.md by running scripts/gen-finding-catalogue.py --write and stage it IN THIS SAME COMMIT as the report.add sites (D-08 doc/code/catalogue lockstep). Run the RED tests first (they must fail against the current tree), implement to GREEN, then a REFACTOR pass only if the two helpers share extractable normalize/lookup logic. Do NOT touch dsx/mathx.py, the DSX-STA-011/012 branch (Task 3 owns the 012 seam), examples/*.yaml, or any tracking file.</action>
  <verify>
    <automated>python3 -m unittest tests.test_declared_association_routing tests.test_correlation_scale_kind_gate tests.test_agreement_completeness_gate tests.test_finding_catalogue_invariant -v && python3 scripts/gen-finding-catalogue.py --check</automated>
  </verify>
  <acceptance_criteria>
    - All four test modules are GREEN, and scripts/gen-finding-catalogue.py --check exits 0 (proves each of the five codes carries a Citation:/Structural criterion: docstring line and a # D-05: marker, AND that references/finding-codes.md is in sync with the report.add sites).
    - tests/test_finding_catalogue_invariant.py is green at declared total 265 with set-identity holding (frozen 256 snapshot + four prior mints + exactly the five new codes; no added/removed drift); _SNAPSHOT_TOTAL is still 256 and tests/fixtures/finding-codes-phase12.md is byte-unchanged.
    - inspect.signature(stats.recommend_association) lists exactly ["estimand_kind"] (REQ-P18-06); recommend_association returns the three acceptable-coefficient sets and raises ValueError for agreement.
    - The correlation-gate test asserts DSX-STA-041 is absent from the findings for the 050/051 fixtures (Pitfall 1 handled explicitly, and the handling is named in the test docstring).
    - The weighted-kappa test proves an explicit-matrix weights value (a nested list) does NOT fire DSX-STA-061 (Pitfall 5 isinstance branch).
    - references/finding-codes.md was regenerated (not hand-edited) and committed in the same commit as the report.add sites.
  </acceptance_criteria>
  <done>recommend_association is dataless and routes the three association kinds; _check_declared_association emits the five HIGH codes with the exact D-02 predicates, the D-03 whitelist, the Pitfall-5 weights branch, and the D-04 p_pos-AND-p_neg rule; both check() call sites are wired; the catalogue is regenerated to 265 in-commit; all four test modules and the D-05 build gate pass.</done>
</task>

<task type="auto">
  <name>Task 3: DSX-STA-012 report-only seam (cross-plan) and canonical-fixture silence proof</name>
  <read_first>
    - dsx/checks/stats.py lines 297-326 (the DSX-STA-011/012 practical-significance block — the exact `if kind in EFFECT_SIZE_KINDS: ... else: report.add("DSX-STA-012", ...)` shape) and line 14 (the current `from ..mathx import EFFECT_SIZE_KINDS, apply_correction, interpret_effect` NAME import — this is why the seam uses a module-attribute access with a default, NOT a new name import that would break this plan's isolated import when 18-B has not merged)
    - 18-CONTEXT.md D-06 (report-only registry; EFFECT_SIZE_KINDS stays {d,h,r}; DSX-STA-012 remedy branches) and 18-RESEARCH.md Pitfall 6 (the recommended control-flow: elif kind in the report-only registry -> report.ok naming the convention, else -> DSX-STA-012) and § "The exact DSX-STA-011/012 site Plan 18-B's remedy branch must extend"
    - 18-RESEARCH.md Anti-Patterns (do NOT edit examples/good-ANALYSIS-SPEC.yaml or examples/bad-ANALYSIS-SPEC.yaml reflexively — verified silence, no edit owed) and 18-VALIDATION.md rows "D-08 fixture silence"
    - the existing fixture-gate tests the silence proof re-runs: tests/test_good_fixture_phase15.py and tests/test_known_bad_corpus.py (read enough to confirm they audit examples/good-ANALYSIS-SPEC.yaml and the known-bad corpus through stats.check)
  </read_first>
  <files>dsx/checks/stats.py</files>
  <action>Modify only the DSX-STA-012 branch in dsx/checks/stats.py so a declared report-only effect-size kind is recognised without firing a blocking code. Add a module import `from .. import mathx` (leaving the existing name imports of EFFECT_SIZE_KINDS/apply_correction/interpret_effect in place) and, inside the p < alpha block, change the control flow to: if kind in EFFECT_SIZE_KINDS -> unchanged DSX-STA-011 path; elif kind in getattr(mathx, "REPORT_ONLY_EFFECT_KINDS", frozenset()) -> report.ok(...) with a message naming the convention (e.g. that effect_size_kind names a labeled convention band, not a gated threshold), so DSX-STA-011 and DSX-STA-012 both stay silent; else -> the unchanged DSX-STA-012 firing for a genuinely unrecognised kind. The getattr-with-empty-default is deliberate: it keeps this plan importable and its own tests green in isolation (the report-only branch is simply inert until Plan 18-B lands mathx.REPORT_ONLY_EFFECT_KINDS), and it activates automatically once 18-B merges. Do NOT widen EFFECT_SIZE_KINDS, do NOT add REPORT_ONLY_EFFECT_KINDS to this file, do NOT edit dsx/mathx.py (Plan 18-B owns it), do NOT edit the examples fixtures. Then prove canonical-fixture silence: run the existing good/bad fixture gate tests and a direct audit of both canonical specs, and confirm none of the five new codes appears in either — record in the SUMMARY that no fixture edit was required (D-08 extend-not-replace is a safety rail, not a mandate; research-confirmed silence). Do NOT edit REQUIREMENTS.md, STATE.md, or ROADMAP.md.</action>
  <verify>
    <automated>python3 -m unittest tests.test_good_fixture_phase15 tests.test_known_bad_corpus -v && python3 -c "from dsx.cli import GATE_PROFILES, run_checks; from dsx.loader import load; import pathlib; R=pathlib.Path('.').resolve(); RES=str(R/'examples'); FIVE={'DSX-STA-050','DSX-STA-051','DSX-STA-060','DSX-STA-061','DSX-STA-062'}; hits={n: FIVE & {f.code for f in run_checks(load(str(R/'examples'/n)), GATE_PROFILES['ship'], None, gate_point='ship', resolve_root=RES).findings} for n in ('good-ANALYSIS-SPEC.yaml','bad-ANALYSIS-SPEC.yaml')}; assert not any(hits.values()), hits; from dsx import mathx; print('canonical fixtures silent on the five new codes; stats+mathx import ok')" && python3 -m unittest tests.test_effect_size_kind -v</automated>
  </verify>
  <acceptance_criteria>
    - dsx/checks/stats.py imports cleanly with 18-B NOT yet merged (the getattr default makes REPORT_ONLY_EFFECT_KINDS optional); the existing DSX-STA-011 and DSX-STA-012 tests in tests/test_effect_size_kind.py still pass (this plan does not change their isolated behaviour for d/h/r or for a genuinely unknown kind).
    - EFFECT_SIZE_KINDS is byte-unchanged in this plan (this plan never edits dsx/mathx.py); the only stats.py change is the elif report-only branch plus the module import.
    - Both canonical fixtures fire NONE of the five new codes (tests/test_good_fixture_phase15 and tests/test_known_bad_corpus green; a direct audit of examples/good-ANALYSIS-SPEC.yaml and examples/bad-ANALYSIS-SPEC.yaml shows no DSX-STA-050/051/060/061/062), and neither fixture file is edited.
    - The SUMMARY records the DSX-STA-012 report-only-firing behaviour (kappa fires neither 011 nor 012 + a report.ok) as a cross-plan seam validated at the Wave-1 merge with Plan 18-B, not in this plan's isolated run.
  </acceptance_criteria>
  <done>The DSX-STA-012 branch consults a report-only registry via a defensive module-attribute access (inert until 18-B merges, never widening EFFECT_SIZE_KINDS); both canonical fixtures are proven silent on all five new codes with no fixture edit; stats.py imports and passes in isolation.</done>
</task>

</tasks>

<threat_model>
**register_authored_at_plan_time: true** — this STRIDE register was authored at planning time (S2-2) per the security_contribution contract; /gsd-secure-phase 18 reads this flag. ASVS L1, block_on: high. This phase adds only declaration-only string/structure comparisons with no data path, no new I/O surface, and no new dependency; there is no high-severity open threat.

## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| analyst-authored ANALYSIS-SPEC.yaml -> dsx loader -> stats.check | Untrusted declared strings/structures cross here. This plan adds five closed-vocabulary/structural membership guards on the analysis block; no data is read, no computation on values. |
| report.add call sites -> scripts/gen-finding-catalogue.py -> references/finding-codes.md | Generated documentation must not drift from enforced behaviour; regeneration + --check is the boundary control. |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-18-A-01 | Tampering | a closed-vocabulary gate (050/051/060/062, operand_scale) implemented as substring/fuzzy match, letting a malformed or adjacent value silently pass | low | mitigate | Exact normalize(value)-equality membership for every field except weights; DSX-STA-040 reuse for operand_scale recognition; unit tests assert non-firing on valid members and firing on out-of-vocab. |
| T-18-A-02 | Tampering | type-confused membership on the weighted-kappa weights field (normalize()/str() on a matrix silently matching nothing but raising nothing) | low | mitigate | Explicit isinstance branch before any normalize (Pitfall 5): recognised string OR non-empty explicit matrix passes; anything else fires DSX-STA-061; a nested-list fixture proves no false positive. |
| T-18-A-03 | Repudiation | a new code ships with no verifiable citation because the DSX-STA- family prefix is not in the D-05 allowlist | low | mitigate | The five codes are added by exact name to _D05_ALLOWLIST_CODES; scripts/gen-finding-catalogue.py --check enforces the Citation:/Structural criterion:/# D-05 marker discipline and is run as the Task-2 gate. |
| T-18-A-04 | Tampering | regenerated references/finding-codes.md committed out of sync with the report.add sites | low | mitigate | finding-codes.md is regenerated (never hand-edited) via gen-finding-catalogue.py --write and committed in the same commit as the report.add sites; --check is the drift gate. |
| T-18-A-05 | Tampering (false authority) | a fabricated or approximated citation locator for a D-07 not-in-hand item (the P18-03 doctrinal scale citation) | low | mitigate | The DSX-STA-050 block rests on the internal Phase-17 estimand_kind/scale definitions; the external doctrinal citation is shipped as a named, presence-only disposition with explicit not-in-hand language — no invented page/section locator. |
| T-18-A-SC | Tampering | npm/pip/cargo installs (supply chain) | low | accept | Zero packages installed; Python stdlib only (unittest, inspect, re). No Package Legitimacy Audit owed. |
</threat_model>

<verification>
- After Task 1 commit: the inline vocab+doc+allowlist check exits 0; gen-finding-catalogue.py --check still passes at 260.
- After Task 2 commit: `python3 -m unittest tests.test_declared_association_routing tests.test_correlation_scale_kind_gate tests.test_agreement_completeness_gate tests.test_finding_catalogue_invariant -v` all green; `python3 scripts/gen-finding-catalogue.py --check` exit 0 at 265.
- After Task 3 commit: the good/bad fixture gate tests pass; both canonical specs are silent on the five new codes; stats.py imports with 18-B absent.
- Wave-1 merge gate (orchestrator, after 18-A and 18-B merge): `python3 -m unittest discover -s tests -q` fully green — this is where the DSX-STA-012 report-only seam with Plan 18-B is validated end-to-end.
- This plan's files_modified are disjoint from Plan 18-B's (this plan never writes dsx/mathx.py, templates/APA-TABLE-research.md, or tests/test_effect_size_kind.py), so the two run concurrently in Wave 1.
</verification>

<success_criteria>
- recommend_association is dataless (signature is exactly estimand_kind) and routes the three association kinds to their acceptable-coefficient sets (REQ-P18-01/06).
- The Association/agreement rows (correlation + agreement + catalog-only pointers) are present in references/test-selection.md (REQ-P18-01/02).
- DSX-STA-050/051 fire per the exact D-02 predicates with the D-03 whitelist (REQ-P18-03); DSX-STA-060/061/062 fire per the exact D-02 predicates with the Pitfall-5 weights branch and the D-04 p_pos-AND-p_neg rule (REQ-P18-04).
- The catalogue is exactly 265 (set-identity: frozen 256 + four prior mints + the five new codes); finding-codes.md regenerated in-commit; --check green; the five codes are citation-enforced via _D05_ALLOWLIST_CODES.
- Both canonical fixtures are silent on the five new codes with no fixture edit.
- EFFECT_SIZE_KINDS is untouched by this plan; the DSX-STA-012 report-only seam is in place, inert-until-18B, and validated at the Wave-1 merge.
</success_criteria>

<output>
Create `.planning/phases/18-correlation-association-and-agreement/18-A-SUMMARY.md` when done.
</output>
