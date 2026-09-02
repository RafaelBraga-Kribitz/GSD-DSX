---
phase: 20-calibration-and-reporting-close
plan: D
wave: 1
requirements: [REQ-P20-04]
status: complete
mints_codes: 0
catalogue_total: 275
divergence_surfaced: false
files_touched: [tests/test_doc_code_agreement.py]
---

# 20-D SUMMARY — doc/code AGREEMENT cross-check (read-only, D-02)

Wave-1 structural guard (D-07 rigour tie-break). Delivers **REQ-P20-04**. **Zero
finding codes minted; no production file touched** — a single new read-only test
module was created. Catalogue stays **275**. Executed inline on the ceremony branch
`gsd/v2.3.0-test-catalog` by the orchestrator (never `handle_branching`).

## What was built

`tests/test_doc_code_agreement.py` — a stdlib-only (`unittest`, `re`, `pathlib`),
CRLF-safe cross-check binding `references/test-selection.md` to the routing engines
with the D-02 two-tier binding:

- **Tier 1 — strict cell-equality.** All **15** `## Decision table` data rows parse
  to `recommend_test(outcome, n_groups, paired, normal, equal_variance, n_per_group,
  overdispersed)` arguments and the parsed primary Test cell **equals**
  `recommend_test(...)['test']`. Any in-cell alternative (`ordinal logistic`, `Cox`)
  is asserted a **member** of `['alternatives']`. For the proportion/2/no cell the
  **Boschloo fallback** is asserted present in `['alternatives']` — the exact cell the
  Boschloo divergence class lived in. Anti-vacuity: exactly 15 rows bound, Boschloo
  cell provably reached.
- **Tier 2 — honest set-membership.** Each of the six `recommend_*` mirror tables
  (Correlation, Repeated measures, Trend, Resampling, Post-hoc, single-proportion) has
  every declared coefficient/test asserted a **member** of that engine's acceptable
  `tests` set for the row's declared key — `recommend_association / recommend_rm /
  recommend_trend / recommend_resampling / recommend_posthoc / recommend_proportion_ci`.
  Membership (`⊆`), never single-cell equality, because these tables are legitimately
  set-valued (Spearman-vs-Kendall) and equality would be a false model.
- **Visible enumerated skip-list + exhaustiveness.** `SKIP_SECTIONS` (Categorical,
  Variance-pretest-and-power — no acceptable-set mirror) plus a 14-entry
  `SKIP_ROW_MARKERS` list, each carrying a one-line reason, name every un-bound row
  (agreement/method-comparison routes, catalog-only pointers, LMM/GEE, SNK/unprotected
  LSD, one-sample-count/RD/OR/NNT, ZIP-hurdle, Vuong). The `test_skiplist_exhaustive`
  net asserts **every** pipe-delimited data row in the file (57 scanned) is either bound
  (31) or explicitly skip-listed (26) — so the test can never pass by silently failing
  to parse a row.

## Parser bindings (this plan's decisions, verified live against the tree)

- Doc→code label map for the spellings whose `normalize()` form differs from the engine
  token: `negative binomial → negative_binomial_regression`, `ordinal logistic →
  ordinal_logistic_regression`, `cox → cox_proportional_hazards`, `scheffé → scheffe`,
  `wilson score → wilson`. Everything else normalises directly.
- Distribution phrasings, Groups (`2/3+/any`), Paired (`no/yes/`—), CRLF `\r?\n`, bold
  `**…**`, `[^1]` marker, and parenthetical `(…fallback…)` all normalised per the plan's
  `<parser_bindings>`.
- The six mirror tables bind to the `tests` frozenset key (confirmed uniform across all
  `recommend_*` returns — the prior firing's carryover note).

## Plan-defect carried and corrected (orchestrator, brief §5)

The 20-C firing flagged that both plans' `[^1]`-marker split truncates the decision
table at row 10 (the marker is in-cell in the proportion row, not only the footnote
definition). 20-D's parser bounds the block at the **next same-or-higher `#` heading**
(the `block()` helper), so footnote lines — which do not start with `|` — are excluded
structurally, and all 15 rows parse. The 15-row anti-vacuity assertion is the guard.

## Divergence disposition

**No divergence surfaced.** All 15 decision rows and all 16 mirror rows agree with the
engines; `references/test-selection.md` and `dsx/checks/stats.py` are **byte-frozen**
(`git diff --name-only` empty). No lockstep repair was needed. The standing v2.3 rule
(doc + `recommend_test` move together) held vacuously — 18/19 closed green and the
Boschloo cell already agrees.

## Gate (re-run by orchestrator from the working tree)

- `python -m unittest tests.test_doc_code_agreement -v` → **8 OK**.
- Robustness / negative control (diagnostic): φ glyph matched (`nominal_association` binds
  both `phi` + `cramers_v`, not under-bound); `bound=31`, `total_data_rows=57`; a
  deliberately-wrong primary (`welch_t` vs engine `welch_anova` at continuous/3+/unequal)
  **fails** the equality assertion — the cross-check is not a lenient pass.
- Full suite `python -m unittest discover -s tests -q` → **Ran 1455 tests OK**
  (20-C baseline 1447 + 8 new; the "declared twice" warnings are pre-existing legacy,
  none Phase-20; the two `explain` tests passed — no stray root `DECISIONS.jsonl`).
- `git diff --name-only` empty (production byte-frozen); `gen-finding-catalogue.py
  --check` = "finding catalogue is current"; 275 unique DSX codes — zero mints.

## S4-3 status after this plan

Wave 1 complete: **20-C ✅** (REQ-P20-03) **∥ 20-D ✅** (REQ-P20-04). **Wave 2 remains**:
20-A ∥ 20-B (the load-bearing D-03 calibration harness extension — live HIGH verify/ship
stratum — + the catch-rate/FPR re-baseline, D-04 PRESENT fixtures, D-05 good-corpus
controls). S4-3 stays IN PROGRESS (atomic checkbox — not checked until Wave 2 + the
Wave-2 merge gate land).
