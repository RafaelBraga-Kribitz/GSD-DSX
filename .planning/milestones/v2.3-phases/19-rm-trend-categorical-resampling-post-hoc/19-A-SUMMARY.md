---
phase: 19-rm-trend-categorical-resampling-post-hoc
plan: A
subsystem: statistics
tags: [rm-anova, trend, categorical, resampling, post-hoc, proportion-count, routing-table, finding-codes, closed-vocabulary, anti-two-stage]

# Dependency graph
requires:
  - phase: 18
    provides: "recommend_association dataless-routing model, _MEMBERSHIP_FIELDS/DSX-STA-040 recognition site, _VOCABULARIES registration precedent, REQ-P18-06 no-autoswitch doctrine"
provides:
  - "Eight closed Phase-19 declared sub-vocabularies + POSTHOC_FAMILY_MAP in dsx/spec.py, eight sets registered in _VOCABULARIES"
  - "Seven dataless recommend_* routing functions (rm, trend, resampling, posthoc, variance_role, power, proportion_ci) in dsx/checks/stats.py"
  - "Six scalar closed-vocab routing fields registered in _MEMBERSHIP_FIELDS (DSX-STA-040 recognition for free, zero new code)"
  - "Six new test-selection.md sections mirroring the recommend_* functions, with every DEPRECATED / pointer / footnote / CMH-surfaced row"
  - "Two no-autoswitch structural-proof modules + one REQ-P19-03 doc-presence module"
  - "Frozen declared-field NAMES + import seam for 19-C's Wave-2 gates"
affects: [19-C, wave-2 gates, DSX-STA-070, DSX-STA-080, DSX-STA-081, DSX-STA-090, DSX-STA-100, DSX-STA-110, DSX-STA-111, DSX-STA-120, DSX-STA-121, DSX-STA-122]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Dataless recommend_* routing function keyed on declared-context strings only (REQ-P18-06 anti-two-stage doctrine, extended to six new families)"
    - "inspect.signature structural proof as the mechanical anti-two-stage guarantee"
    - "doc/code lockstep: test-selection.md rows land in the same commit as the recommend_* they mirror"

key-files:
  created:
    - tests/test_declared_rm_trend_routing.py
    - tests/test_declared_resampling_posthoc_routing.py
    - tests/test_p19_categorical_rows.py
  modified:
    - dsx/spec.py
    - dsx/checks/stats.py
    - references/test-selection.md
    - references/finding-codes.md

key-decisions:
  - "Every recommend_* signature is dataless (no data/n/n_groups/paired/normal/distribution) — the mechanical anti-two-stage proof, asserted by inspect.signature in two structural-proof modules"
  - "No route names a DEPRECATED procedure by construction: recommend_rm never Mauchly-conditional, recommend_posthoc returns exactly POSTHOC_FAMILY_MAP[family] (never snk/unprotected_lsd), recommend_proportion_ci never wald, recommend_power never observed/post_hoc"
  - "REQ-P19-03 (categorical) delivered as documentation only — rows + one deprecated + one surfaced + one pointer + one footnote — minting ZERO finding codes; catalogue stays exactly 265"
  - "Six scalar fields join _MEMBERSHIP_FIELDS for DSX-STA-040 recognition for free; nested resampling.method and str-or-list trend_test are deferred to Wave-2 helpers; dose_score_scheme deliberately not registered"
  - "DOSE_SCORE_SCHEMES imported into stats.py despite being unused this wave — freezes the import seam so 19-C's dose gate never re-touches the single-writer import block"
  - "No numeric statistic or fabricated page locator printed (D-07): GG epsilon, Hamed-Rao lag, Davidson-MacKinnon B floors, Brown-Cai-DasGupta n cutoff, Campbell expected-count, Hayter alpha, McCullagh-Nelder section all named as confirm-at-source in prose only"

patterns-established:
  - "Pattern: closed-vocab sub-vocabularies registered additively in _VOCABULARIES; routing dicts (POSTHOC_FAMILY_MAP) deliberately excluded"
  - "Pattern: variance-role disposition token must not itself name the forbidden procedure (renamed drop_the_pretest_* -> use_welch_unconditionally so the no-pretest proof holds)"

requirements-completed: [REQ-P19-01, REQ-P19-02, REQ-P19-03, REQ-P19-04, REQ-P19-05, REQ-P19-06, REQ-P19-07]

coverage:
  - id: D1
    description: "Eight closed Phase-19 sub-vocabs + POSTHOC_FAMILY_MAP in spec.py, eight sets registered in _VOCABULARIES, ESTIMAND_KINDS unchanged"
    requirement: "REQ-P19-01"
    verification:
      - kind: unit
        ref: "python3 -c '<spec vocab inline check>' -> 'spec vocabs OK'"
        status: pass
    human_judgment: false
  - id: D2
    description: "Seven dataless recommend_* routing functions excluding every deprecated procedure; six scalar membership fields; no-autoswitch structural proofs"
    requirement: "REQ-P19-04"
    verification:
      - kind: unit
        ref: "tests/test_declared_rm_trend_routing.py; tests/test_declared_resampling_posthoc_routing.py (29 tests)"
        status: pass
    human_judgment: false
  - id: D3
    description: "Six test-selection.md sections with all deprecated/pointer/footnote/CMH-surfaced rows; catalogue no-op regen stays 265; REQ-P19-03 doc-presence"
    requirement: "REQ-P19-03"
    verification:
      - kind: unit
        ref: "tests/test_p19_categorical_rows.py; tests/test_finding_catalogue_invariant.py; scripts/gen-finding-catalogue.py --check (exit 0)"
        status: pass
    human_judgment: false

# Metrics
duration: ~25min
completed: 2026-09-02
status: complete
---

# Phase 19 Plan A: RM/Trend/Categorical/Resampling/Post-hoc Routing Surface Summary

**Shipped the Phase-19 declaration-only routing surface — seven dataless recommend_* functions, eight closed sub-vocabularies + POSTHOC_FAMILY_MAP, and six human-readable test-selection.md sections with every deprecated/pointer/footnote row — all keyed on declared fields, all in doc/code lockstep, minting ZERO finding codes so the catalogue stays exactly 265.**

## Performance

- **Duration:** ~25 min
- **Tasks:** 3 of 3 (Task 2 executed as RED then GREEN)
- **Files modified:** 7 (3 created, 4 modified)
- **Commits:** 4 atomic (1 feat, 1 test/RED, 1 feat/GREEN, 1 feat)

## Accomplishments

- **Task 1 (af56283):** Added eight closed declared sub-vocabularies (SPHERICITY_CORRECTIONS, DOSE_SCORE_SCHEMES, AUTOCORRELATION_HANDLINGS, RESAMPLING_METHODS, VARIANCE_TESTS, VARIANCE_TEST_ROLES, POWER_REPORTING_TYPES, PROPORTION_CI_METHODS) plus the POSTHOC_FAMILY_MAP routing dict to dsx/spec.py; registered the eight sets in _VOCABULARIES; ESTIMAND_KINDS left unchanged (OQ-6, no scale member).
- **Task 2 RED (673a952):** Authored the two no-autoswitch structural-proof modules; confirmed 29 tests fail against the current tree (the seven functions do not exist — AttributeError).
- **Task 2 GREEN (0b7175a):** Implemented the seven dataless recommend_* functions modelled on recommend_association; extended the spec import block with all nine Phase-19 constants (freezes the Wave-2 import seam); registered the six scalar fields in _MEMBERSHIP_FIELDS; PARAMETRIC_TESTS/NONPARAMETRIC_TESTS left byte-unchanged.
- **Task 3 (ccf119e):** Appended six test-selection.md sections (Repeated measures, Trend, Categorical, Resampling, Post-hoc, Proportion and count extras), each mirroring its recommend_* function, with the DEPRECATED Yates row, log-linear pointer, CMH surfaced-stratification row, Fisher-Freeman-Halton honesty footnote, DEPRECATED SNK/unprotected-LSD rows, ZIP/hurdle pointer, and Vuong misuse-only row. Ran the catalogue regen (no-op diff, stays 265) and authored the REQ-P19-03 doc-presence test.

## Verification (real output)

- **Task 1:** `python3 -c '<spec vocab check>'` -> `spec vocabs OK`
- **Task 2:** `python3 -m unittest tests.test_declared_rm_trend_routing tests.test_declared_resampling_posthoc_routing -v` -> `Ran 29 tests ... OK`; inline dataless check -> `dataless routing OK`
- **Task 3:** `python3 scripts/gen-finding-catalogue.py --check` -> exit 0 (`finding catalogue is current`); `python3 -m unittest tests.test_p19_categorical_rows tests.test_finding_catalogue_invariant -v` -> `Ran 8 tests ... OK`; inline check -> `rows+deprecated+footnote present; catalogue stays 265`
- **Full suite:** `python3 -m unittest discover -s tests -q` -> `Ran 1402 tests ... OK`
- **Catalogue invariant:** declared total stayed exactly **265**; phase12 snapshot byte-unchanged; `--check` exit 0.

## Deviations from Plan

- **[Test-authoring self-correction, in-task] variance-role disposition token.** The first GREEN implementation used the disposition token `drop_the_pretest_use_welch_unconditionally`, which contains the substring `pretest` that the no-autoswitch proof asserts must be absent (the token must not name a pretest gate). Renamed the frozenset member to `use_welch_unconditionally`; the proof then held. This was a within-task RED→GREEN correction, not a plan deviation — the plan's intent (the precondition role never endorses a variance pretest as a location gate) is preserved exactly. Fixed in the same GREEN commit (0b7175a).
- **[D-07 reconciliation] Davidson-MacKinnon B floors.** The Task-3 action text asks for a prose note distinguishing "19/99 (an exactness floor)" from "399/1499 (a recommended minimum)", while the ceremony's hard constraint 8 and the plan must_haves list "Davidson-MacKinnon 19/99-vs-399/1499" as a numeric statistic that must NOT be hard-coded. Resolved by writing the conceptual distinction (an exactness floor is not a recommended-minimum B; both confirm-at-source, neither printed nor gated) WITHOUT printing the specific numeric floors — honoring constraint 8 while preserving the two-concepts-not-one intent. The gate never checks B's value regardless.

Otherwise the plan executed as written.

## Notes for 19-C (Wave 2)

- The declared-field NAMES are frozen: 19-C's ten gates and the extended bad fixture read exactly the names bound in this plan's field_bindings block (analysis.sphericity_correction, analysis.dose_scores/dose_score_scheme, analysis.autocorrelation_handling, analysis.resampling.{method,seed,B,unit}, analysis.omnibus/posthoc, analysis.variance_test/variance_test_role, analysis.power_reporting_type, analysis.proportion_ci_method, analysis.exposure/offset, analysis.nnt/nnt_ci, analysis.cmh_strata/interval_method, analysis.trend_test).
- The import seam in dsx/checks/stats.py is frozen — all nine Phase-19 spec constants (including the currently-unused DOSE_SCORE_SCHEMES) are already imported, so 19-C's gate helpers need not re-touch the single-writer import block.
- The nested analysis.resampling.method and the str-or-list analysis.trend_test are intentionally NOT in the flat _MEMBERSHIP_FIELDS loop — validate them inside the Wave-2 gate helpers.
- 19-C owns all ten new codes (265 -> 275), the _D05_ALLOWLIST_CODES additions in scripts/gen-finding-catalogue.py, and the invariant-test bump.

## Self-Check: PASSED

- Files created exist: tests/test_declared_rm_trend_routing.py, tests/test_declared_resampling_posthoc_routing.py, tests/test_p19_categorical_rows.py — FOUND.
- Files modified: dsx/spec.py, dsx/checks/stats.py, references/test-selection.md, references/finding-codes.md — FOUND (finding-codes.md regen was a no-op diff, stays 265).
- Commits exist: af56283, 673a952, 0b7175a, ccf119e — FOUND in git log.
- Branch unchanged: gsd/v2.3.0-test-catalog.
- Catalogue declared total: 265, `--check` exit 0.
