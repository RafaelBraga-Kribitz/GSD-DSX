---
phase: 20-calibration-and-reporting-close
plan: D
type: execute
wave: 1
depends_on: []
files_modified:
  - tests/test_doc_code_agreement.py
  - references/test-selection.md
  - dsx/checks/stats.py
autonomous: true
requirements: [REQ-P20-04]
tags: [doc-code-agreement, cross-check, decision-table, recommend-test, boschloo, set-membership, skip-list, structural-guard, lockstep]

must_haves:
  truths:
    - "a NEW read-only cross-check test tests/test_doc_code_agreement.py binds references/test-selection.md to the routing code with a TWO-TIER binding, so the Boschloo divergence CLASS (a doc cell that disagrees with the engine) is structurally prevented on every mirror table, caught at build/CI time by the test failing red — not repaired after the fact (D-02, the --check model)"
    - "Tier 1 STRICT cell-equality: every Decision-table data row (proportion/continuous/count/ordinal/time-to-event, rows 10-24) parses to (outcome_type, n_groups, paired, normal/equal_variance/overdispersed) and the parsed primary Test cell EQUALS recommend_test(...)['test']; any in-cell alternative (Cox, ordinal logistic) is asserted a MEMBER of recommend_test(...)['alternatives']; and for the proportion/2/no cell the Boschloo fallback is asserted present in ['alternatives'] (the exact cell the Boschloo divergence lived in)"
    - "Tier 2 honest SET-MEMBERSHIP: each of the six recommend_* mirror tables (Association/agreement, Repeated measures, Trend, Resampling, Post-hoc, Proportion-and-count) has every declared coefficient/test asserted a MEMBER of that engine's acceptable set for the row's declared key (recommend_association/rm/trend/resampling/proportion_ci returns, POSTHOC_FAMILY_MAP via recommend_posthoc) — membership, never single-cell equality, because these tables are legitimately set-valued (Spearman-vs-Kendall) and equality would be a false model"
    - "a VISIBLE, enumerated skip-list makes every un-bound row a DECLARED exclusion: pointer / DEPRECATED / catalog-only / surfaced / footnote / annotation rows, the whole Categorical section (mints zero codes — rows-only), and the Variance-pretest-and-power-reporting section (gate-only, keyed on declared roles, not an acceptable-set mirror) are named on the skip-list, and the test asserts every table row is either bound or explicitly skipped — so it can NEVER pass by silently failing to parse a row"
    - "the parser is CRLF-safe (r'\\r?\\n') and normalises the doc's presentation forms to code tokens: 2 / 3+ / any (groups), no / yes / — (paired), the Distribution phrases (normal or n >= 200 / skewed and n < 200 / normal, equal variance / normal, unequal variance / skewed / variance ~ mean / variance > mean / censored), bold **...**, the [^1] footnote marker, and hyphen/space test-label spelling (two-proportion z -> two_proportion_z, Welch t -> welch_t, Kruskal-Wallis -> kruskal_wallis, log-rank -> log_rank, negative binomial -> negative_binomial_regression)"
    - "this plan mints ZERO finding codes; references/test-selection.md and dsx/checks/stats.py are 20-D's SOLE-writer repair targets and are expected UNTOUCHED (18-19 closed green, the Boschloo cell already agrees) — if and only if the cross-check surfaces a divergence does 20-D repair it in doc/code lockstep (same commit); catalogue stays 275"
  artifacts:
    - tests/test_doc_code_agreement.py
    - references/test-selection.md
    - dsx/checks/stats.py
  key_links:
    - "the Decision-table cells <-> recommend_test(outcome_type, n_groups, paired, normal, equal_variance, n_per_group, overdispersed) — recommend_test is pure and total, so strict cell-equality is a fully provable claim; the proportion/2/no cell's Boschloo fallback <-> recommend_test('proportion',2,paired=False)['alternatives'] (dsx/checks/stats.py:139-144) is the exact seam the Boschloo divergence class lived in"
    - "each mirror-table declared token <-> its engine's acceptable set: recommend_association/rm/trend/resampling/proportion_ci return dicts carrying a frozenset, and recommend_posthoc returns POSTHOC_FAMILY_MAP[family] — the SAME acceptable-set semantics the runtime gates use, so membership is the honest ceiling each set-valued table's structure supports"
    - "the enumerated skip-list <-> every unparsed row: a declared exclusion per pointer/DEPRECATED/catalog-only/surfaced/footnote row plus the Categorical + Variance-power sections, asserted exhaustive so no row is silently dropped (the anti-false-pass control)"
    - "the cross-check failing red at build time <-> the D-01 decision that NO runtime doc/code-divergence finding code is minted — divergence is a CI failure, not a spec-audit finding; this is why REQ-P20-04 is a test, not a new gate"
---

<objective>
Deliver REQ-P20-04: a read-only doc/code AGREEMENT cross-check test (not a generated mirror) in a new disjoint file tests/test_doc_code_agreement.py, binding references/test-selection.md to the routing engines with the D-02 two-tier binding — strict cell-equality of the Decision table to recommend_test (including the Boschloo fallback), honest set-membership of the six recommend_* mirror tables to their engines, and a visible enumerated skip-list so no row is silently unparsed. This structurally prevents the Boschloo divergence CLASS on every mirror table, caught red at build/CI time.

Purpose: this is a Wave-1 structural guard (D-07 rigour tie-break) — it SURFACES any latent doc-code divergence before Wave 2 re-measures the calibration against the settled state. references/test-selection.md is ~280 lines of irreducible hand-written prose a generator cannot emit (D-02), so a generated mirror does not transfer; a cross-check test is the honest mechanism. Per D-01 NO runtime doc/code-divergence finding code is minted — divergence is a CI failure (the --check model), not a spec-audit finding. 20-D is the SOLE writer of references/test-selection.md and dsx/checks/stats.py for any repair a surfaced divergence requires, but 18-19 closed green and the Boschloo cell already agrees, so the expected outcome is: the cross-check passes with NO repair, and both files stay byte-frozen.

Output: a new tests/test_doc_code_agreement.py carrying Tier-1 strict cell-equality (decision table <-> recommend_test + Boschloo), Tier-2 set-membership (six mirror tables <-> engines), a module-level enumerated skip-list with an exhaustiveness assertion, and a CRLF-safe normalising parser. references/test-selection.md and dsx/checks/stats.py remain untouched unless a divergence is surfaced.
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
@references/test-selection.md
</context>

<parser_bindings>
This plan RESOLVES the doc-cell -> code-token normalisation bindings D-02 delegated to plan time. The SHAPES are fixed by D-02; the exact bindings below are this plan's decisions, all verified live against references/test-selection.md and dsx/checks/stats.py.

Decision-table rows (references/test-selection.md lines 10-24, 15 data rows) -> recommend_test:
- Groups cell: "2" -> n_groups=2; "3+" -> n_groups=3; "any" -> n_groups=1.
- Paired cell: "no" -> False; "yes" -> True; "—" (em dash) -> False.
- Distribution cell -> (normal, equal_variance, overdispersed, n_per_group): "normal or n >= 200" -> normal=True, n_per_group=200; "skewed and n < 200" -> normal=False; "normal differences" -> normal=True; "skewed differences" -> normal=False; "normal, equal variance" -> normal=True, equal_variance=True; "normal, unequal variance" -> normal=True, equal_variance=False; "skewed" -> normal=False; "variance ~ mean" -> overdispersed=False; "variance > mean" -> overdispersed=True; "—" / "censored" -> all None (defaults).
- Test cell -> primary token (strip the [^1] footnote marker, bold **...**, and any parenthetical "(... fallback ...)" first): "two-proportion z" -> two_proportion_z; "McNemar" -> mcnemar; "chi-square" -> chi_square; "Welch t" -> welch_t; "Mann-Whitney" -> mann_whitney; "paired t" -> paired_t; "Wilcoxon signed-rank" -> wilcoxon_signed_rank; "ANOVA" -> anova; "Welch ANOVA" -> welch_anova; "Kruskal-Wallis" -> kruskal_wallis; "Poisson regression" -> poisson_regression; "negative binomial" -> negative_binomial_regression; "log-rank" -> log_rank. An "or"/comma-joined cell ("Kruskal-Wallis or ordinal logistic", "log-rank, Cox") -> primary is the FIRST token (equality-bound), the remainder are membership-bound against recommend_test(...)['alternatives'] (ordinal_logistic_regression; cox_proportional_hazards).
- Proportion/2/no row (line 10): additionally assert normalize contains "boschloo" among recommend_test('proportion',2,paired=False)['alternatives'] (dsx/checks/stats.py:139-144 emits "boschloo_exact (any expected cell < 5)").

Tier-2 mirror tables (six) -> engines, membership only:
- "## Association / agreement" (### Correlation, ### Agreement/reliability): declared coefficient rows keyed on estimand_kind (linear_association / monotone_association / nominal_association) -> recommend_association(estimand_kind)['tests']; agreement rows route to kappa/ICC/Bland-Altman and are membership-checked against recommend_association where it raises for out-of-scope kinds, so the agreement/method_comparison sub-rows are SKIP-listed as "routes outside recommend_association's association scope" (they are the DSX-STA-051 negative space, not a recommend_association return).
- "## Repeated measures" -> recommend_rm(measure_kind)['tests'] keyed on continuous / ranks(ordinal) / binary.
- "## Trend" -> recommend_trend(trend_context)['tests'] keyed on the declared trend context (ordered dose / ordered groups / temporal).
- "## Resampling" -> recommend_resampling(purpose) acceptable-set keyed on interval / hypothesis-test purpose.
- "## Post-hoc" -> recommend_posthoc(omnibus) acceptable set (== POSTHOC_FAMILY_MAP[family]) keyed on the declared omnibus (welch_anova / anova / kruskal_wallis / friedman).
- "## Proportion and count extras" -> recommend_proportion_ci(context) acceptable-set for the single-proportion row.
- READ each engine's return dict live to identify the frozenset key (tests / intervals / methods) before binding; bind to that key, do not assume a name.

Enumerated skip-list (declared exclusions — every row not membership/equality-bound MUST be named here): the "## Categorical" section in full (mints zero codes; N-1 chi-square / GOF / G-test rows + the Yates DEPRECATED row + CMH surfaced row + log-linear pointer + Fisher-Freeman-Halton footnote — no recommend_* mirror set exists for it); the "## Variance pretest and power reporting" section in full (gate-only, keyed on declared roles, not an acceptable-set mirror); every pointer / DEPRECATED / catalog-only / surfaced row and every honesty footnote inside the six bound tables (LMM/GEE pointers, distance-correlation/partial-correlation catalog-only, Cronbach->McDonald pointer, ICC/Kendall-W catalog-only bands, Kappa-companion annotation, SNK/unprotected-LSD DEPRECATED, ZIP/hurdle pointer, Vuong DEPRECATED, RD/OR surfaced-not-gated); and the "## Notes that change the answer" + "## Assumptions" prose sections (not tables). The test asserts every pipe-delimited table row in the file is either bound (Tier 1 or Tier 2) or matched by an enumerated skip-list entry.
</parser_bindings>

<tasks>

<task type="auto">
  <name>Task 1: Tier-1 strict cell-equality — the Decision table bound to recommend_test, including the Boschloo fallback</name>
  <read_first>
    - references/test-selection.md lines 6-32 (the "## Decision table": header row 8, separator row 9, 15 data rows 10-24, the [^1] Boschloo footnote 26-32) — the exact cell text, em dashes, bold, and the "(Boschloo's exact test if any expected cell < 5)[^1]" fallback in row 10
    - dsx/checks/stats.py lines 109-210 (recommend_test's full branch structure and the _rec return shape {test, rationale, alternatives, effect_size}; lines 134-146 the proportion branch with "boschloo_exact (any expected cell < 5)" in alternatives; lines 148-206 the continuous/count/ordinal/time-to-event branches the Distribution mapping targets) — RE-VERIFY these live line numbers before pinning
    - the <parser_bindings> block above (the exact Groups/Paired/Distribution/Test normalisation for every one of the 15 rows)
    - 20-CONTEXT.md D-02 (strict cell-equality for the decision table; Boschloo in alternatives for the proportion/2/no cell; the visible skip-list; CRLF r"\r?\n") and D-01 (no divergence code minted — a divergence is a red build, and 20-D repairs in lockstep only if surfaced)
  </read_first>
  <files>tests/test_doc_code_agreement.py, references/test-selection.md, dsx/checks/stats.py</files>
  <action>Create tests/test_doc_code_agreement.py (stdlib-only: unittest, re, pathlib, importing dsx.checks.stats). Write a CRLF-safe parser (split on r"\r?\n") that locates the "## Decision table" block, takes the pipe-delimited data rows between the header separator and the [^1] footnote, and for each row parses the six cells and normalises them to recommend_test arguments exactly per the <parser_bindings> block (Groups 2/3+/any, Paired no/yes/em-dash, the Distribution phrases, and the Test-label spelling map; strip [^1], bold, and parenthetical fallbacks from the Test cell). For each row call recommend_test(outcome_type, n_groups, paired=paired, normal=normal, equal_variance=equal_variance, n_per_group=n_per_group, overdispersed=overdispersed) and assert its ["test"] EQUALS the parsed primary Test token (strict cell-equality). For any in-cell alternative token (the second half of an "or"/comma cell, e.g. ordinal logistic, Cox) assert it is a MEMBER of the returned ["alternatives"] (normalised). For the proportion/2/no row specifically, additionally assert a normalised "boschloo" token appears in recommend_test('proportion', 2, paired=False)["alternatives"] — the exact cell the Boschloo divergence class lived in. Include an anti-vacuity assertion that exactly 15 decision-table data rows were parsed and bound (so a parser that silently drops rows fails). Author the module so it runs green against the current tree WITHOUT modifying references/test-selection.md or dsx/checks/stats.py — those two files are 20-D's SOLE-writer repair targets and must stay byte-frozen UNLESS this cross-check surfaces a genuine divergence; if (and only if) a decision-table cell does not equal the engine, repair the divergence in doc/code LOCKSTEP in the same commit (fix whichever side is wrong; per the standing v2.3 rule the doc table and recommend_test move together), and record the repair in the SUMMARY. Expected outcome: no divergence, no repair. Do NOT mint any finding code, do NOT add a report.add site, do NOT edit examples/ or any tracking file.</action>
  <verify>
    <automated>python3 -m unittest tests.test_doc_code_agreement -v && python3 -c "import re,pathlib; from dsx.checks import stats; t=pathlib.Path('references/test-selection.md').read_text(encoding='utf-8'); block=t.split('## Decision table',1)[1].split('[^1]',1)[0]; rows=[r for r in re.split(r'\r?\n',block) if r.strip().startswith('|') and '---' not in r and 'Outcome' not in r]; assert len(rows)==15, ('expected 15 decision rows, parsed '+str(len(rows))); alt=[a.lower().replace(' ','_') for a in stats.recommend_test('proportion',2,paired=False)['alternatives']]; assert any('boschloo' in a for a in alt), ('Boschloo fallback missing from proportion/2/no alternatives: '+str(alt)); assert stats.recommend_test('proportion',2,paired=False)['test']=='two_proportion_z' and stats.recommend_test('time_to_event',1)['test']=='log_rank'; print('decision table cell-equality + Boschloo fallback bound')"</automated>
  </verify>
  <acceptance_criteria>
    - tests.test_doc_code_agreement is green and the inline check prints "decision table cell-equality + Boschloo fallback bound": all 15 decision-table rows parse and each parsed Test cell equals recommend_test(...)['test']; the proportion/2/no cell's Boschloo fallback is a member of ['alternatives'].
    - The parser is CRLF-safe and the anti-vacuity assertion pins exactly 15 bound rows, so a silently-dropped row fails the test.
    - references/test-selection.md and dsx/checks/stats.py are UNCHANGED (no divergence surfaced) — or, if a divergence was surfaced, it is repaired in doc/code lockstep in the same commit and named in the SUMMARY.
    - No finding code minted, no report.add site added, no edit to examples/ or any tracking file.
  </acceptance_criteria>
  <done>tests/test_doc_code_agreement.py strictly binds every Decision-table cell to recommend_test and asserts the Boschloo fallback in alternatives; the Boschloo divergence instance is structurally pinned; no doc/code repair was needed (or was applied in lockstep if surfaced).</done>
</task>

<task type="auto">
  <name>Task 2: Tier-2 honest set-membership — the six recommend_* mirror tables bound to their engines, with the exhaustive visible skip-list</name>
  <read_first>
    - references/test-selection.md lines 65-303 (the six mirror sections: Association/agreement 65-128, Repeated measures 130-157, Trend 159-178, Categorical 180-203 [SKIP — zero codes], Resampling 205-222, Post-hoc 224-246, Variance-pretest-and-power 248-277 [SKIP — gate-only], Proportion-and-count 279-303) — note every pointer/DEPRECATED/catalog-only/surfaced row and every honesty footnote that the skip-list must name
    - dsx/checks/stats.py lines 213-471 (recommend_association 213-, recommend_rm 337-, recommend_trend 355-, recommend_variance_role 371-, recommend_resampling 389-, recommend_posthoc 406-, recommend_power 427-, recommend_proportion_ci 450-) and dsx/spec.py POSTHOC_FAMILY_MAP — READ each return dict live to identify the frozenset key (tests / intervals / methods) before binding
    - the <parser_bindings> block above (the exact section->engine map and the full enumerated skip-list)
    - 20-CONTEXT.md D-02 (set-membership is the honest ceiling for the set-valued mirror tables — single-cell equality would over-block a legitimate Spearman-vs-Kendall choice; the visible enumerated skip-list so no row is silently unparsed)
  </read_first>
  <files>tests/test_doc_code_agreement.py</files>
  <action>Extend tests/test_doc_code_agreement.py with the Tier-2 set-membership binding. For each of the six mirror sections named in <parser_bindings> (Association/agreement, Repeated measures, Trend, Resampling, Post-hoc, Proportion-and-count), parse its markdown table rows CRLF-safely, extract the declared key column and the acceptable-coefficient/test column, normalise each declared coefficient/test token to its code spelling, and assert it is a MEMBER of the corresponding engine's acceptable set for the row's declared key — recommend_association/rm/trend/resampling/proportion_ci returns (bind to the frozenset key you read live) and recommend_posthoc(omnibus) (== POSTHOC_FAMILY_MAP[family]). Use membership (token in acceptable_set), never single-cell equality, because these tables are legitimately set-valued. Add a module-level, explicitly-enumerated SKIP_LIST naming every row deliberately not bound: the entire "## Categorical" and "## Variance pretest and power reporting" sections, and every pointer / DEPRECATED / catalog-only / surfaced row and honesty footnote inside the bound tables (LMM/GEE pointers, distance/partial correlation catalog-only, Cronbach->McDonald pointer, ICC/Kendall-W band annotations, the kappa-companion annotation, SNK/unprotected-LSD DEPRECATED, ZIP/hurdle pointer, Vuong DEPRECATED, RD/OR surfaced-not-gated) — each entry carrying a one-line reason in a comment. Then add an EXHAUSTIVENESS assertion: iterate EVERY pipe-delimited table row in references/test-selection.md and assert each is either bound (by Tier 1 or Tier 2) or matched by a SKIP_LIST entry — so the test can never pass by silently failing to parse a row (D-02's anti-false-pass control). Keep it stdlib-only and CRLF-safe. Do NOT mint any code; do NOT edit references/test-selection.md or dsx/checks/stats.py unless Tier 2 surfaces a genuine membership divergence, in which case repair in doc/code lockstep (same commit) as 20-D's sole-writer prerogative and record it. Do NOT edit examples/ or any tracking file.</action>
  <verify>
    <automated>python3 -m unittest tests.test_doc_code_agreement -v && python3 -c "import re,pathlib; from dsx.checks import stats; assert 'games_howell' in {x.lower().replace(' ','_') for x in stats.recommend_posthoc('welch_anova')['tests']}; assert 'wilson' in {x.lower().replace(' ','_') for x in stats.recommend_proportion_ci('single proportion')['intervals']} or 'wilson' in {x.lower().replace(' ','_') for x in list(stats.recommend_proportion_ci('single proportion').values())[0]}; t=pathlib.Path('references/test-selection.md').read_text(encoding='utf-8'); allrows=[r for r in re.split(r'\r?\n',t) if r.strip().startswith('|') and '---' not in r]; assert len(allrows) > 25, ('too few table rows scanned: '+str(len(allrows))); print('six mirror tables membership-bound; skip-list exhaustive; all table rows accounted for')"</automated>
  </verify>
  <acceptance_criteria>
    - tests.test_doc_code_agreement is green (Tier 1 + Tier 2 together) and the inline check prints "six mirror tables membership-bound; skip-list exhaustive; all table rows accounted for".
    - Every declared coefficient/test in the six mirror tables is a MEMBER of its engine's acceptable set for the row's key (recommend_association/rm/trend/resampling/proportion_ci and POSTHOC_FAMILY_MAP via recommend_posthoc); membership, not equality.
    - The enumerated SKIP_LIST names the Categorical and Variance-power sections and every pointer/DEPRECATED/catalog-only/surfaced/footnote row; the exhaustiveness assertion proves every pipe-delimited table row in the file is either bound or explicitly skipped (no silent unparsed row).
    - references/test-selection.md and dsx/checks/stats.py are UNCHANGED (no membership divergence) — or repaired in lockstep and named in the SUMMARY if one was surfaced.
    - No finding code minted; no edit to examples/ or any tracking file.
  </acceptance_criteria>
  <done>tests/test_doc_code_agreement.py binds all six recommend_* mirror tables by honest set-membership with a visible exhaustive skip-list; the doc/code divergence CLASS is structurally prevented on every mirror table; no lockstep repair was needed (or was applied if surfaced).</done>
</task>

</tasks>

<single_writer_proof>
Phase 20 is a two-wave, file-disjoint, single-writer split (D-07). This is a Wave-1 structural-guard plan. Every file this plan may WRITE is owned by exactly one plan across all four:

| File | Writer | Other plans | Concurrent write? |
|------|--------|-------------|-------------------|
| tests/test_doc_code_agreement.py | 20-D (new file) | none | No |
| references/test-selection.md | 20-D (SOLE writer, conditional lockstep repair) | 20-C reads only; 20-A/20-B do not touch it | No |
| dsx/checks/stats.py | 20-D (SOLE writer, conditional lockstep repair) | 20-C reads only; 20-A/20-B do not touch it | No |

20-D is the ONLY plan in the phase that may write references/test-selection.md or dsx/checks/stats.py, and only to repair a divergence the cross-check surfaces (expected: none — 18-19 closed green, the Boschloo cell already agrees, so both stay byte-frozen). 20-C (same wave) only READS references/test-selection.md; a reader/writer pair across two plans is not a write conflict. Wave 2 (20-A calibration, 20-B catalogue-close) touches neither file. Tracking files stay orchestrator-serial.
</single_writer_proof>

<threat_model>
**register_authored_at_plan_time: true** — authored at planning time (S4-2). /gsd-secure-phase 20 reads this flag. ASVS L1, block_on: high. This plan adds a read-only cross-check test over declared strings/structures; no data path, no new I/O surface, no new dependency, no report.add site; there is no high-severity open threat.

## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| references/test-selection.md prose <-> the routing engines | The doc mirror must not drift from recommend_test / recommend_*; the cross-check test is the boundary control, failing red at build/CI time (the D-01 --check model, not a runtime finding code). |
| doc cell presentation forms <-> code tokens | A lenient parser that mis-normalises could pass a real divergence; exact normalisation + the 15-row and exhaustiveness anti-vacuity assertions are the control. |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-20-D-01 | Tampering (docs drift from behaviour) | a decision-table cell drifting from recommend_test (the Boschloo divergence class) | high | mitigate | Tier-1 strict cell-equality binds all 15 rows to recommend_test and asserts the Boschloo fallback in alternatives; any drift fails the build red. Doc/code repaired in lockstep in the same commit if surfaced (standing v2.3 rule). |
| T-20-D-02 | Tampering (false pass) | the cross-check passing because a row silently failed to parse | high | mitigate | The 15-row anti-vacuity assertion (Tier 1) and the exhaustiveness assertion (every pipe-delimited row is bound or explicitly skip-listed) make an unparsed row a hard failure. |
| T-20-D-03 | Tampering (over-strong claim) | asserting single-cell equality on a legitimately set-valued mirror table, over-blocking a valid Spearman-vs-Kendall choice | medium | mitigate | Tier 2 uses honest set-MEMBERSHIP against the engine's acceptable set — the same semantics the runtime gates use — never equality. |
| T-20-D-04 | Tampering (false authority) | a lenient normaliser mapping an unrelated doc token to a code token, masking a divergence | low | mitigate | Explicit, enumerated normalisation maps (Groups/Paired/Distribution/Test-label); an unmapped token raises rather than silently passing. |
| T-20-D-SC | Tampering | npm/pip/cargo installs (supply chain) | low | accept | Zero packages installed; Python stdlib only (unittest, re, pathlib). No Package Legitimacy Audit owed (vacuously satisfied). |
</threat_model>

<verification>
- After Task 1 commit: `python3 -m unittest tests.test_doc_code_agreement -v` green; all 15 decision-table rows bound to recommend_test by strict cell-equality; the Boschloo fallback asserted in the proportion/2/no alternatives.
- After Task 2 commit: `python3 -m unittest tests.test_doc_code_agreement -v` green (both tiers); the six mirror tables membership-bound; the enumerated skip-list + exhaustiveness assertion prove every table row is accounted for.
- Divergence disposition: references/test-selection.md and dsx/checks/stats.py are byte-unchanged (no divergence surfaced), OR any surfaced divergence is repaired in doc/code lockstep in the same commit and named in the SUMMARY.
- Wave-1 completeness (REQ-P20-04): the cross-check binds test-selection.md to the routing engines with the two-tier binding + visible skip-list, structurally preventing the Boschloo divergence class; catalogue stays 275; zero codes minted.
</verification>

<success_criteria>
- A new read-only tests/test_doc_code_agreement.py binds references/test-selection.md to recommend_test (strict cell-equality of all 15 decision rows + the Boschloo fallback) and to the six recommend_* mirror tables (honest set-membership), with a visible enumerated skip-list and an exhaustiveness assertion so no row is silently unparsed (REQ-P20-04, D-02).
- The Boschloo divergence CLASS is structurally prevented on every mirror table, caught red at build/CI time — not repaired after the fact (D-01, the --check model; no runtime divergence code minted).
- references/test-selection.md and dsx/checks/stats.py stay byte-frozen (no divergence surfaced), or any surfaced divergence is repaired in doc/code lockstep in the same commit (20-D sole writer).
- Zero finding codes minted; catalogue stays 275; CRLF-safe throughout.
</success_criteria>

<output>
Create `.planning/phases/20-calibration-and-reporting-close/20-D-SUMMARY.md` when done.
</output>
