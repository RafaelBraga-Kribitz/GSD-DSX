---
phase: 11-frequentist-admissibility-adjudicator-dsx-adm
plan: 04
subsystem: infra
tags: [dsx, ontology, yaml, citations, admissibility, estimand]

# Dependency graph
requires:
  - phase: 11-01
    provides: "REQ-P11-01 amended to 14 families; references/test-selection.md D-27 citation fix; two D-29 locators folded into brief.md §7"
  - phase: 11-02
    provides: "ESTIMAND_TYPES closed vocabulary in dsx/spec.py and validity_frame.estimand.type populated on all nine committed specs"
provides:
  - "references/families.yaml — 14 cited frequentist family entries, 19-token cited assumption vocabulary, 4 cited ranking rules, all parsed only by dsx.loader.load()"
  - "tests/test_families_yaml.py — 28 tests pinning the file's schema, written before the data file existed"
affects: [11-05, 11-06, 11-07, 11-08]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Data files consumed by dsx.loader.load() use flat block sequences of double-quoted single-line scalars only — no block scalars, anchors, or merge keys — to sidestep the two parsers' documented divergence (D-08)."
    - "A raw-text acceptance check that greps the whole file for forbidden literal characters (&, <<:) means even prose in header comments describing the schema rule must avoid reproducing those characters verbatim."

key-files:
  created:
    - references/families.yaml
    - tests/test_families_yaml.py

key-decisions:
  - "Entries 1, 4 and 5 (the three two_proportion_z variants) all cite Agresti (2013), Categorical Data Analysis, 3rd edition, as the normal-approximation source, reusing the same unverified citation already established for the large_sample_normal_approximation assumption token — no new locator was introduced for the estimator itself."
  - "Entry 13 (linear_regression_block_bootstrap, temporal dependence) cites Cameron and Miller (2015) with no section number, matching the existing unverified-section-locator precedent already recorded in dsx/spec.py's DEPENDENCE_ADMISSIBLE_METHODS comment for the temporal/spatial pairing."
  - "Entries 11, 12 and 13 additionally name the NIST Statistical Reference Datasets collection (SRD 140) in notes as a further available reference-value source, without asserting any specific SRD 140 dataset or numeric value — permitted but not required by the plan."
  - "The header comment's schema-rule bullet was rewritten to describe anchors and merge keys in prose rather than reproducing the literal '&' and '<<:' characters, because the acceptance check's raw-text scan is a whole-file substring match with no comment carve-out — even a comment naming the forbidden character would fail it."

requirements-completed: [REQ-P11-01, REQ-P11-02, REQ-P11-06]

coverage:
  - id: D1
    description: "references/families.yaml parses through dsx.loader.load() and holds exactly 14 families, a 19-token assumption vocabulary, and 4 ranking rules, byte-for-byte identical whether parsed via PyYAML or the bundled fallback"
    requirement: "REQ-P11-01"
    verification:
      - kind: unit
        ref: "tests/test_families_yaml.py#TestFamiliesYamlParsesOnBothLoaderPaths"
        status: pass
      - kind: unit
        ref: "tests/test_families_yaml.py#TestFamiliesYamlSchema"
        status: pass
    human_judgment: false
  - id: D2
    description: "Every family and ranking rule carries a non-blank citation and an honest locator_status (verified/unverified with notes naming the gap); no entry declares a Bayesian inference method"
    requirement: "REQ-P11-06"
    verification:
      - kind: unit
        ref: "tests/test_families_yaml.py#TestFamiliesYamlSchema.test_every_family_locator_status_is_valid_and_notes_present_when_unverified"
        status: pass
      - kind: unit
        ref: "tests/test_families_yaml.py#TestFamiliesYamlSchema.test_every_family_notes_is_nonblank_verified_or_not"
        status: pass
    human_judgment: true
    rationale: "No parser can check whether a citation string actually names a real, correctly-quoted source — this plan's own threat model (T-11-13, T-11-14) requires a human-check verify step reading each citation against its source before the phase closes. Automated tests prove every entry HAS a citation and an honest locator_status; they cannot prove the citation is genuine."
  - id: D3
    description: "Every family's estimand and dependence values are members of the shipped ESTIMAND_TYPES/DEPENDENCE_STRUCTURES vocabularies, and each of the six frequentist committed specs resolves its declared procedure to exactly one family inside its own (estimand, dependence) group"
    requirement: "REQ-P11-02"
    verification:
      - kind: unit
        ref: "tests/test_families_yaml.py#TestFamiliesYamlSchema.test_every_estimand_is_a_member_of_estimand_types"
        status: pass
      - kind: unit
        ref: "tests/test_families_yaml.py#TestFamiliesYamlTraceability.test_every_committed_frequentist_spec_resolves_its_declared_procedure"
        status: pass
    human_judgment: false

duration: ~30min (interrupted by an API connection loss after the third task commit; resumed to write this SUMMARY, no other work redone)
completed: 2026-08-20
status: complete
---

# Phase 11 Plan 04: Frequentist Estimator Ontology (families.yaml) Summary

**Shipped `references/families.yaml` — 14 cited frequentist family entries, a 19-token cited assumption vocabulary, and 4 cited pairwise ranking rules — parsed only by `dsx.loader.load()` and proven to round-trip identically on both its PyYAML and bundled-fallback paths, with `tests/test_families_yaml.py` (28 tests) written first and left unmodified once the data made it pass.**

## Performance

- **Duration:** ~30 min of active work across two agent runs (an API connection loss interrupted the first run after the third task commit; nothing was redone on resume — only this SUMMARY was written)
- **Tasks:** 3
- **Files modified:** 2 (1 created test file, 1 created data file)

## Accomplishments

- `tests/test_families_yaml.py` written first and confirmed RED (28/28 failing with `SpecParseError: spec file not found`) before any data existed.
- `references/families.yaml` header, 19-entry cited assumption vocabulary, and 4 cited ranking rules (`welch_over_students`, `boschloo_over_fishers_exact`, `cv3_wild_bootstrap_over_cv1`, `interacted_adjustment_over_unadjusted`) written and proven to round-trip identically through both `dsx.loader.load()` paths before `families:` existed.
- All 14 family entries added; `tests/test_families_yaml.py` turned green on the first run with **zero test edits** — no assertion written in task 1 was relaxed to make task 3 pass.
- Full suite: 692 tests (664 baseline + 28 new), `OK`. `python scripts/gen-finding-catalogue.py --check` exits 0 with the same 7 pre-existing "declared twice" warnings. `dsx gate plan`/`dsx gate ship` on `examples/good-ANALYSIS-SPEC.yaml` both still exit 0 — no gate exit code moved.

## Task Commits

Each task followed the RED → GREEN TDD cycle:

1. **Task 1: Write tests/test_families_yaml.py and confirm it fails** — `6a7f893` (test)
2. **Task 2: Write header, 19-token assumption vocabulary, 4 ranking rules** — `4bf4568` (feat)
3. **Task 3: Write the 14 family entries and turn the test suite green** — `9e6233c` (feat)

**Plan metadata:** (this commit, made by execute-plan.md's git_commit_metadata step)

## Files Created/Modified

- `tests/test_families_yaml.py` — four `unittest.TestCase` classes (`TestFamiliesYamlParsesOnBothLoaderPaths`, `TestFamiliesYamlSchema`, `TestFamiliesYamlRankingRules`, `TestFamiliesYamlTraceability`), 28 tests total, loading the file only through `dsx.loader.load()`.
- `references/families.yaml` — the ontology: header + `vocabulary_is_not_exhaustive: true`, 19-token `assumption_vocabulary`, 4-entry `ranking_rules`, 14-entry `families`.

## Locator Status Split

Across the 14 family entries: **4 verified, 10 unverified** (every unverified entry carries a non-blank `notes` naming what was not confirmed, per D-09):

- **Verified (4):** `fishers_exact` and `boschloo_exact` (both cite Lydersen, Fagerland and Laake 2009 §9, author/year/journal/volume/issue/pages/section all confirmed); `linear_regression_cv1` (Cameron and Miller 2015 §II, subject to the D-29 manuscript-numbering caveat); `ratio_of_means_delta_method` (Deng, Knoblich and Lu 2018, verified at article level via DOI/arXiv — but see the reference-value gap below).
- **Unverified (10):** `two_proportion_z`, `two_proportion_z_always_valid`, `two_proportion_z_cluster_robust` (Agresti 2013, no chapter locator confirmed); `students_t`, `welch_t`, `welch_t_cluster_robust` (Delacre, Lakens and Leys 2017 tables superseded by the 2022 Correction, no numeric value used from either); `linear_regression_unadjusted` (Freedman 2008, journal/volume/pages not confirmed); `linear_regression_interacted_adjustment` (Lin 2013, same reason); `linear_regression_cv3_wild_bootstrap` (MacKinnon, Nielsen and Webb 2023 §9, section number unconfirmed); `linear_regression_block_bootstrap` (Cameron and Miller 2015, temporal-dependence section locator unconfirmed, matching existing `dsx/spec.py` precedent).

The 19-token `assumption_vocabulary` and the 4 `ranking_rules` carry their own, separately-tracked `locator_status` values (not counted in the 4/10 split above, which is family-entries-only).

## No Verified Published Reference Value

Per D-28/D-05, `entry 14 (ratio_of_means_delta_method)` — the delta-method / ratio-metrics family — has a **verified citation** (Deng, Knoblich and Lu 2018, DOI 10.1145/3219819.3219919, also arXiv:1803.06336, confirmed at article level) but **no verified published reference value**. Its `notes` field states this plainly as a recorded gap, not an oversight, matching the identical statement already carried by the `ratio_denominator_nonzero_and_finite` assumption token. This is one of the four clusters `11-CONTEXT.md`'s `<specifics>` names as citation-only with no verified reference value (quantile treatment effects, count/rate models, survey-weighted estimation, delta method) — the other three were not built as families in this roster at all, so only the delta method's gap is live in the shipped file.

Two families (`students_t`, `welch_t`) do have a verified NIST reference value: NIST/SEMATECH e-Handbook of Statistical Methods, Handbook 151, section 1.3.5.3, the AUTO83B.DAT two-sample t-test worked example, cited by handbook and section number with a URL and no DOI (D-28), per `11-CONTEXT.md`'s confirmed specifics.

## Decisions Made

- Reused the `large_sample_normal_approximation` token's own Agresti (2013) citation as the estimator-level citation for all three `two_proportion_z` variants (entries 1, 4, 5), rather than inventing a separate locator — matches the plan's literal instruction to use "the two-proportion normal-approximation source" for those three.
- `linear_regression_block_bootstrap` (temporal) cites Cameron and Miller (2015) with no section number, deliberately matching the existing unverified-locator precedent already recorded in `dsx/spec.py`'s `DEPENDENCE_ADMISSIBLE_METHODS` comment rather than inventing a new section number for the temporal case.
- The three deliberate roster divergences from `11-RESEARCH.md`'s 12-family recommendation, as instructed by the plan's task 3 action text and restated here for auditability:
  1. The cluster-robust regression pair (`linear_regression_cv1`, `linear_regression_cv3_wild_bootstrap`) sits under `clustered` dependence, not `temporal` — Cameron & Miller and MacKinnon, Nielsen & Webb are about clusters. `linear_regression_block_bootstrap` is the sole `temporal` entry, keeping `weak-identification-mmm`'s candidate set a set of one.
  2. `linear_regression_cluster_robust` was not written as a separate family; `linear_regression_cv1` is that family under its precise name.
  3. Two entries were added beyond the research roster to reach the 14 `REQ-P11-01` (as amended by plan 11-01) requires: entry 4 (`two_proportion_z_always_valid`) for D-01's sequential-monitoring cluster, and entry 14 (`ratio_of_means_delta_method`) for D-01's ratio-metrics cluster.
- The header comment's schema-rule line describing "no anchor, no merge key" was rewritten to avoid literally containing the characters `&` and `<<:`, because the acceptance check `assert '&' not in t and '<<:' not in t` is a whole-file substring match with no exemption for comment prose naming the forbidden characters. Caught during task 2's verification run, fixed before commit — not a deviation from the schema itself, only from how the rule was described in a comment.

## Deviations from Plan

None beyond the two items above, both already anticipated and pre-authorized by the plan's own text: the header-comment literal-character fix (a self-correction during task 2's own verification loop, not a Rule 1-4 deviation) and the three roster divergences from `11-RESEARCH.md` (explicitly instructed by task 3's action block, not an unplanned departure).

**Process note, not a content deviation:** this execution run was interrupted by an API connection loss after the third task commit (`9e6233c`) completed and the working tree was already clean. On resume, all three commits, the 692-test-passing state, and the `gen-finding-catalogue.py --check` result were independently re-verified before writing this SUMMARY — nothing was redone or re-executed.

## Issues Encountered

None beyond the header-comment fix described above, resolved within task 2 before its commit.

## Next Phase Readiness

- `references/families.yaml` is ready for `dsx/frame/admissibility.py` (plan 11-05) to read via `dsx.loader.load()` and build its alias index and candidate-family lookup against.
- All four D-13 citable orderings are present with both sides of each pair in the roster, so `DSX-ADM-010`'s "which rule fired" message has a dominated alternative to name for every rule.
- The human-check verify step this plan's threat model (T-11-13, T-11-14) requires — reading each citation against its actual source — has not yet been performed and remains open before the phase closes; automated tests prove structural honesty (every entry has a citation and a locator_status) but cannot prove citation authenticity.
- No blockers for plan 11-05.

---
*Phase: 11-frequentist-admissibility-adjudicator-dsx-adm*
*Completed: 2026-08-20*

## Self-Check: PASSED

- FOUND: `references/families.yaml`
- FOUND: `tests/test_families_yaml.py`
- FOUND: `6a7f893` (test: failing schema tests)
- FOUND: `4bf4568` (feat: header, vocabulary, ranking rules)
- FOUND: `9e6233c` (feat: 14 family entries, tests green)
- All commits verified present in `git log --oneline`.
