---
phase: 20-calibration-and-reporting-close
plan: C
type: execute
wave: 1
depends_on: []
files_modified:
  - tests/test_no_shapiro_autoswitch.py
  - tests/test_time_to_event_fallthrough.py
autonomous: true
requirements: [REQ-P20-03]
tags: [statistics, no-autoswitch, anti-two-stage, routing-table, fallthrough, structural-guard, declaration-gate]

must_haves:
  truths:
    - "the no-autoswitch structural proof covers EVERY new routing category: tests/test_no_shapiro_autoswitch.py enumerates every public recommend_* function in dsx.checks.stats via inspect and asserts each one EXCEPT recommend_test is DATALESS — its inspect.signature carries only declared-context string parameters, with NO parameter named data/n/n_groups/paired/normal/equal_variance/n_per_group/distribution/overdispersed — so a future contributor who re-introduces a data-then-pick (two-stage) parameter on any of the eight new-category routers (recommend_association/rm/trend/resampling/posthoc/variance_role/power/proportion_ci) turns the proof red (REQ-P18-06 doctrine, extended to every new category)"
    - "the existing normality-autoswitch guarantees still hold verbatim after Phases 18-19 appended six sections to references/test-selection.md: the fixed assumption order (independence -> equal variance -> normality), the UNCONDITIONAL Welch recommendation with no branch on a computed variance test, and normality declared as a small-n property (matters at small n only / irrelevant above ~200) are all re-asserted green"
    - "the decision-surface scan (dsx/ and skills/, never tests/, never the untracked academic paper) fires NO normality-test CALL (scipy.stats/shapiro(/normaltest(/anderson(/kstest() — the gate + skill decision surface never runs a normality test to pick a test"
    - "the fallthrough-position regression is green after ALL Phase-18/19 row additions: recommend_test reaches log_rank for a time_to_event outcome by UNCONDITIONAL terminal fallthrough (no equality guard on the time_to_event literal, log_rank is the last return in recommend_test), and the decision-table time-to-event row remains the TERMINAL outcome-type row in references/test-selection.md — no Phase-18/19 addition displaced it"
    - "this plan mints ZERO finding codes and modifies no production code: it extends two structural-guard test modules only; catalogue stays 275, dsx/ and references/ are byte-frozen by this plan"
  artifacts:
    - tests/test_no_shapiro_autoswitch.py
    - tests/test_time_to_event_fallthrough.py
  key_links:
    - "each new-category recommend_* dataless inspect.signature <-> the enumeration assertion in tests/test_no_shapiro_autoswitch.py — the anti-two-stage proof is now category-complete AND future-proof (it enumerates recommend_* dynamically, so a NEW category added without a dataless router is caught automatically)"
    - "references/test-selection.md's assumption-order prose + decision-table terminal time-to-event row <-> the two guard modules that read them CRLF-safely (r'\\r?\\n') — this plan is a READER of test-selection.md (Wave-1 plan D is its sole writer); the prose C reads (ranked assumptions, the terminal outcome row) is not the decision-table CELL D would repair, so C's assertions are stable under any D repair"
    - "recommend_test's terminal log_rank fallthrough <-> test_time_to_event_fallthrough.py's behavioural + source-scan + terminal-position legs — the fallthrough position is the seam Phases 18-19 could have broken by inserting an outcome row after time-to-event; pinning it here is the whole point of the Wave-1 structural guard"
---

<objective>
Deliver REQ-P20-03: the no-autoswitch structural proof made CATEGORY-COMPLETE (every new routing family added in Phases 17-19 is proven dataless / anti-two-stage), and the fallthrough-position regression confirmed green after all Phase-18/19 row additions. Both are pure structural guards over EXISTING code — this plan mints zero codes and edits no production file.

Purpose: this is a Wave-1 structural guard (D-07 rigour tie-break). It surfaces any latent anti-two-stage or fallthrough-position regression BEFORE Wave 2 re-measures the calibration against the settled state (Phase-12 "measure last"). The no-autoswitch doctrine (REQ-P18-06: a router that takes data can inspect-then-pick; a dataless router mechanically cannot) was proven per-family as the families shipped; Phase 20 unifies it into a single category-complete, future-proof enumeration in the canonical no-autoswitch module, and pins the time-to-event terminal fallthrough that the six Phase-18/19 sections could have displaced.

Output: two extended structural-guard test modules — tests/test_no_shapiro_autoswitch.py (adds the every-new-category dataless enumeration; re-affirms the assumption-order / Welch-unconditional / normality-declared assertions still hold after the 18-19 section additions) and tests/test_time_to_event_fallthrough.py (adds the fallthrough-POSITION regression: log_rank is recommend_test's terminal unconditional fallthrough AND the decision-table time-to-event row is the terminal outcome-type row).
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
@tests/test_no_shapiro_autoswitch.py
@tests/test_time_to_event_fallthrough.py
</context>

<tasks>

<task type="auto">
  <name>Task 1: Extend tests/test_no_shapiro_autoswitch.py so the no-autoswitch proof covers EVERY new routing category</name>
  <read_first>
    - tests/test_no_shapiro_autoswitch.py in full (the two existing classes: TestSelectionOrderTest reads references/test-selection.md's "in order of how much they matter" section CRLF-safely and asserts the assumption order + Welch-unconditional + normality-declared; DecisionSurfaceScanTest scans dsx/ and skills/ for _NORMALITY_CALL_TOKENS) — the exact idiom, imports, and CRLF discipline (r"\r?\n", replace("\r\n","\n")) to preserve
    - dsx/checks/stats.py lines 109-206 (recommend_test — the ONE legacy router that legitimately takes declared shape args normal/equal_variance/n_per_group; it is EXCLUDED from the dataless proof and instead covered by the existing Welch-unconditional/normality-declared assertions) and lines 213-471 (the eight new-category routers recommend_association/rm/trend/resampling/posthoc/variance_role/power/proportion_ci — each takes exactly one declared-context string parameter; confirm every signature live before pinning)
    - .planning/phases/19-rm-trend-categorical-resampling-post-hoc/19-A-PLAN.md (the two 19-A no-autoswitch routing modules and their inspect.signature banned-parameter idiom — this plan CONSOLIDATES that proof into a single category-complete enumeration, it does not duplicate their per-module fixtures)
    - 20-CONTEXT.md D-08 (bands stay conventions; the calibration/routing keys on declared vocabulary/CODE identity only, never a computed statistic — the anti-two-stage invariant this proof enforces mechanically)
  </read_first>
  <files>tests/test_no_shapiro_autoswitch.py</files>
  <action>Add a new test class NoAutoswitchEveryNewCategoryTest to tests/test_no_shapiro_autoswitch.py that ENUMERATES every public routing function in dsx.checks.stats by introspection: import dsx.checks.stats, collect every attribute whose name starts with "recommend_" that is a function, and split it into the legacy declared-shape router (recommend_test) and the new-category routers (all the rest). Assert three things. First, anti-vacuity: the enumerated new-category set is non-empty and is a SUPERSET of the eight known names recommend_association, recommend_rm, recommend_trend, recommend_resampling, recommend_posthoc, recommend_variance_role, recommend_power, recommend_proportion_ci (so a future rename cannot silently empty the proof). Second, the dataless proof: for EACH new-category router, inspect.signature(fn).parameters contains NO parameter whose name is in the banned set {data, n, n_groups, paired, normal, equal_variance, n_per_group, distribution, overdispersed} — that banned set IS the data-then-pick surface the two-stage anti-pattern needs, and its absence is the mechanical proof no new category can inspect-then-switch. Third, the exclusion is explicit and justified: assert recommend_test IS present in the enumeration (so the split is real) and document in the test docstring that recommend_test is intentionally covered by the Welch-unconditional/normality-declared assertions below rather than the dataless proof, because it legitimately consumes DECLARED shape fields. Do NOT weaken, delete, or renumber the two existing classes; the assumption-order, Welch-unconditional, and normality-declared assertions must remain and must still pass now that Phases 18-19 have appended the Association / Repeated measures / Trend / Categorical / Resampling / Post-hoc / Variance-power / Proportion-count sections to references/test-selection.md (the setUp already scopes the order assertions to the "in order of how much they matter" section, so the appended sections do not perturb them — confirm this holds). Keep everything stdlib-only and CRLF-safe (r"\r?\n", never a bare \n). This test mints nothing and edits no production file; do NOT edit dsx/, references/, examples/, or any tracking file.</action>
  <verify>
    <automated>python3 -m unittest tests.test_no_shapiro_autoswitch -v && python3 -c "import inspect; import dsx.checks.stats as S; recs=[n for n in dir(S) if n.startswith('recommend_') and callable(getattr(S,n))]; assert set(recs) >= {'recommend_test','recommend_association','recommend_rm','recommend_trend','recommend_resampling','recommend_posthoc','recommend_variance_role','recommend_power','recommend_proportion_ci'}, recs; banned={'data','n','n_groups','paired','normal','equal_variance','n_per_group','distribution','overdispersed'}; newcats=[n for n in recs if n!='recommend_test']; bad=[n for n in newcats if banned & set(inspect.signature(getattr(S,n)).parameters)]; assert not bad, ('data/n flag on new-category router(s): '+str(bad)); print('every new category dataless; recommend_test excluded and covered by the Welch assertions')"</automated>
  </verify>
  <acceptance_criteria>
    - tests.test_no_shapiro_autoswitch is fully green and the inline check prints "every new category dataless; recommend_test excluded ...": every recommend_* except recommend_test has a signature free of any data/n/distribution parameter, and the enumeration covers all eight new-category routers.
    - The three pre-existing behaviours are preserved and still green after the 18-19 section additions: the fixed assumption order (independence -> equal variance -> normality), the unconditional Welch recommendation, and normality-declared-as-small-n; plus the decision-surface scan finds no normality-test CALL in dsx/ or skills/.
    - The enumeration is dynamic (dir()-based) so a future NEW category added without a dataless router is caught automatically; the anti-vacuity assertion prevents a rename from emptying the proof.
    - No edit to dsx/, references/, examples/, or any tracking file; zero codes minted.
  </acceptance_criteria>
  <done>tests/test_no_shapiro_autoswitch.py proves every new-category recommend_* is dataless (anti-two-stage, REQ-P18-06 extended to every category), retains the normality-autoswitch guarantees green after the 18-19 row additions, and mints nothing.</done>
</task>

<task type="auto">
  <name>Task 2: Extend tests/test_time_to_event_fallthrough.py with the fallthrough-POSITION regression, green after all Phase-18/19 row additions</name>
  <read_first>
    - tests/test_time_to_event_fallthrough.py in full (the behavioural leg drives stats.recommend_test over n_groups x paired and asserts log_rank; the source-scan leg asserts no _TIME_TO_EVENT_GUARD equality guard exists — the whitespace-tolerant, CRLF-safe regex idiom to preserve)
    - dsx/checks/stats.py lines 198-206 (the ordinal branch and the TERMINAL `return _rec("log_rank", ...)` — log_rank is the unconditional fallthrough reached because time_to_event is the only OUTCOME_TYPE with no explicit `if outcome == ...` branch; this is the position the guard pins)
    - references/test-selection.md lines 6-32 (the "## Decision table" section: the 15 data rows 10-24, the time-to-event row 24 as the LAST outcome row, then the [^1] footnote at 26) — the terminal-row position this regression asserts survived the Phase-18/19 additions (which appended NEW sections AFTER the decision table, never a new decision-table outcome row)
    - 20-CONTEXT.md (Phase 20 mints zero codes; this is a structural guard only)
  </read_first>
  <files>tests/test_time_to_event_fallthrough.py</files>
  <action>Extend tests/test_time_to_event_fallthrough.py, preserving both existing legs, by adding the fallthrough-POSITION regression the requirement names. Add a test that asserts, on the CODE side, that log_rank is recommend_test's TERMINAL unconditional fallthrough: read inspect.getsource(stats.recommend_test), collect every line containing a return of a recommendation (the `return _rec(` sites), and assert the LAST such return names log_rank — so a future contributor who appends a new outcome branch AFTER the log_rank fallthrough (which would shadow time_to_event's route) turns this red. Add a second test that asserts, on the DOC side, that the decision-table time-to-event row is the TERMINAL outcome-type row in references/test-selection.md: parse the "## Decision table" block CRLF-safely (split on r"\r?\n"), take the pipe-delimited data rows between the header separator and the [^1] footnote, and assert the FINAL data row's Outcome cell normalizes to time-to-event / time_to_event — proving no Phase-18/19 addition inserted an outcome row after it (the six new sections were appended as SEPARATE sections after the table, not as new table rows). Keep the behavioural leg (every n_groups x paired routes time_to_event to log_rank) and the source-scan leg (no equality guard on the time_to_event literal) intact and green. Stdlib-only, CRLF-safe (whitespace-tolerant regexes, never line-anchored on a bare \n). This module mints no finding code, so it carries NO `# D-05:` marker (as its header already states). Do NOT edit dsx/, references/, examples/, or any tracking file — this plan is a READER of test-selection.md; Wave-1 plan D is its sole writer.</action>
  <verify>
    <automated>python3 -m unittest tests.test_time_to_event_fallthrough -v && python3 -c "import inspect,re,pathlib; import dsx.checks.stats as S; src=inspect.getsource(S.recommend_test); returns=[l for l in src.splitlines() if 'return _rec(' in l]; assert returns and 'log_rank' in returns[-1], ('terminal recommend_test fallthrough is not log_rank: '+repr(returns[-1] if returns else None)); t=pathlib.Path('references/test-selection.md').read_text(encoding='utf-8'); block=t.split('## Decision table',1)[1].split('[^1]',1)[0]; rows=[r for r in re.split(r'\r?\n',block) if r.strip().startswith('|') and '---' not in r]; data=[r for r in rows if 'Outcome' not in r]; last=data[-1].split('|')[1].strip().lower(); assert 'time' in last and 'event' in last, ('terminal decision-table outcome row is not time-to-event: '+repr(last)); print('fallthrough terminal on both code and doc sides')"</automated>
  </verify>
  <acceptance_criteria>
    - tests.test_time_to_event_fallthrough is fully green and the inline check prints "fallthrough terminal on both code and doc sides": recommend_test's last `return _rec(` names log_rank, and the decision table's final data row's Outcome cell is time-to-event.
    - The behavioural leg (all n_groups x paired route to log_rank) and the source-scan leg (no time_to_event equality guard) remain intact and green.
    - The doc-side parse is CRLF-safe (r"\r?\n") and scoped to the "## Decision table" block up to the [^1] footnote, so the appended Phase-18/19 sections are outside the scanned region by construction.
    - No edit to dsx/, references/, examples/, or any tracking file; zero codes minted.
  </acceptance_criteria>
  <done>tests/test_time_to_event_fallthrough.py pins the time-to-event terminal fallthrough on both the code side (log_rank is recommend_test's last return) and the doc side (time-to-event is the decision table's terminal outcome row), green after all Phase-18/19 row additions.</done>
</task>

</tasks>

<single_writer_proof>
Phase 20 is a two-wave, file-disjoint, single-writer split (D-07). This is a Wave-1 structural-guard plan. Every file this plan WRITES is owned by exactly one plan in Wave 1:

| File | Wave-1 writer | Other writers | Concurrent write? |
|------|---------------|---------------|-------------------|
| tests/test_no_shapiro_autoswitch.py | 20-C | none | No |
| tests/test_time_to_event_fallthrough.py | 20-C | none | No |
| references/test-selection.md | 20-D (sole writer, conditional repair only) | — | No — 20-C only READS it |
| dsx/checks/stats.py | 20-D (sole writer, conditional repair only) | — | No — 20-C only READS it |

20-C is a pure READER of references/test-selection.md and dsx/checks/stats.py; the sole Wave-1 WRITER of both is 20-D, and only if its cross-check surfaces a divergence (expected: none, 18-19 closed green). The prose 20-C reads — the ranked-assumptions section and the decision-table terminal outcome row — is not the decision-table CELL 20-D would repair, so 20-C's assertions are stable under any 20-D repair. Reader/writer across two plans in the same wave is not a write conflict: the writes are disjoint. Tracking files (REQUIREMENTS/STATE/ROADMAP) stay orchestrator-serial.
</single_writer_proof>

<threat_model>
**register_authored_at_plan_time: true** — authored at planning time (S4-2). /gsd-secure-phase 20 reads this flag. ASVS L1, block_on: high. This plan adds only structural-guard test assertions over existing code; no data path, no new I/O surface, no new dependency, no report.add site; there is no high-severity open threat.

## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| recommend_* signatures <-> the no-autoswitch enumeration | The anti-two-stage contract: a router that takes data can inspect-then-pick. The inspect.signature enumeration is the boundary control — a data/n parameter on any new-category router turns the proof red. |
| references/test-selection.md decision table <-> the fallthrough-position guard | The terminal time-to-event row / log_rank fallthrough must not be displaced by a future row addition; the position assertion is the boundary control. |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-20-C-01 | Tampering (data-then-pick) | a new-category recommend_* gaining a data/n/distribution parameter, reintroducing two-stage selection | low | mitigate | The dynamic inspect.signature enumeration fails red on any banned parameter across every recommend_* except recommend_test (REQ-P18-06 doctrine, category-complete). |
| T-20-C-02 | Tampering (silent scope loss) | the enumeration silently emptying (rename/refactor) so the proof passes vacuously | low | mitigate | The anti-vacuity assertion requires the enumerated set to be a superset of the eight known new-category names and to include recommend_test. |
| T-20-C-03 | Tampering (fallthrough displacement) | a new outcome branch appended after log_rank, or a new decision-table row after the time-to-event row, silently rerouting time_to_event | low | mitigate | Terminal-position assertions on both the code side (last `return _rec(` is log_rank) and the doc side (final decision-table outcome row is time-to-event). |
| T-20-C-04 | Tampering (normality autoswitch returns) | a normality-test CALL creeping onto the gate/skill decision surface | low | mitigate | The existing DecisionSurfaceScanTest over dsx/ and skills/ is preserved and re-run green (no scipy.stats/shapiro/normaltest/anderson/kstest call). |
| T-20-C-SC | Tampering | npm/pip/cargo installs (supply chain) | low | accept | Zero packages installed; Python stdlib only (unittest, inspect, re, pathlib). No Package Legitimacy Audit owed (vacuously satisfied). |
</threat_model>

<verification>
- After Task 1 commit: `python3 -m unittest tests.test_no_shapiro_autoswitch -v` fully green; the inline enumeration check proves every new-category recommend_* is dataless and recommend_test is excluded; the assumption-order / Welch-unconditional / normality-declared / decision-surface-scan assertions remain green after the 18-19 section additions.
- After Task 2 commit: `python3 -m unittest tests.test_time_to_event_fallthrough -v` fully green; the terminal-fallthrough position is pinned on both the code and doc sides.
- Wave-1 completeness (this plan's contribution to REQ-P20-03): the no-autoswitch test covers every new category AND the fallthrough-position regression is green after all row additions.
</verification>

<success_criteria>
- The no-autoswitch structural proof is CATEGORY-COMPLETE and future-proof: every recommend_* except recommend_test is proven dataless by a dynamic enumeration, so any new category or reintroduced data-then-pick parameter turns it red (REQ-P20-03, first clause).
- The fallthrough-position regression is green after all Phase-18/19 row additions: log_rank is recommend_test's terminal unconditional fallthrough and the decision-table time-to-event row is the terminal outcome row (REQ-P20-03, second clause).
- The pre-existing normality-autoswitch guarantees (assumption order, unconditional Welch, normality-declared, decision-surface scan) are all preserved and green.
- Zero finding codes minted; dsx/ and references/ untouched by this plan; catalogue stays 275.
</success_criteria>

<output>
Create `.planning/phases/20-calibration-and-reporting-close/20-C-SUMMARY.md` when done.
</output>
