# Phase 19: RM, trend, categorical, resampling, post-hoc — Research

**Researched:** 2026-09-02
**Domain:** Sixth extension of an existing declaration-only Python gate library
(`dsx`) — no new statistics computed, no new package, no data path. The task:
add per-family dataless `recommend_*` routing, ten new HIGH `_check_declared_*`
gate codes across six pre-allocated `DSX-STA-*` decades, several additive
membership-guarded sub-vocabularies, and new rows (including one DEPRECATED and
several pointer rows) in `references/test-selection.md` — mirroring the Phase-18
machinery verbatim. Catalogue **265 → 275**.
**Confidence:** HIGH on every claim tagged `[VERIFIED: live tree]` — every
locator, line number, function name, and mechanism below was read directly from
the live repository this session (branch `gsd/v2.3.0-test-catalog`), not recalled
from training data and not copied from a stale prior-phase document. MEDIUM /
`[ASSUMED]` on the declared-field NAMES for the ten gates — 19-CONTEXT.md D-03
fixes the field SHAPES but explicitly binds the exact names "at plan-time for
S3-2." Those are this session's concrete, reasoned recommendations, itemised in
Open Questions, and are NOT yet committed anywhere in the tree.

## Summary

Phase 19 touches the same file set Phase 18 did, all of which exist and were
re-read this session: `dsx/checks/stats.py` (the gates + `recommend_*`),
`dsx/spec.py` (new sub-vocabs + `_VOCABULARIES` registration),
`references/test-selection.md` (the human doc mirror, extended with RM / trend /
categorical / resampling / post-hoc / proportion-count rows), the generated
`references/finding-codes.md` (regenerated, never hand-edited, 265 → 275),
`scripts/gen-finding-catalogue.py` (`_D05_ALLOWLIST_CODES` += the ten codes by
exact name), `tests/test_finding_catalogue_invariant.py` (three pinned numbers
move as a set), the two canonical fixtures (`examples/good-`/`bad-ANALYSIS-SPEC.yaml`,
extended not replaced), and several new test files. Nothing computes a number
from data: every one of the ten new predicates compares DECLARED strings /
presence in `ANALYSIS-SPEC.yaml`'s `analysis:` block against a closed vocabulary
or a presence check — the identical idiom Phase 18 established and this session
re-verified is live and unchanged.

Five things this research resolves that 19-CONTEXT.md's own locator list leaves
at sub-implementation granularity, and that materially shape how the S3-2 plans
must be written (the HOW gaps):

1. **The ten new codes are invisible to the D-05 citation build gate unless
   named by exact code in `_D05_ALLOWLIST_CODES`.** `[VERIFIED: live tree]`
   `scripts/gen-finding-catalogue.py:87-89` — `_D05_ALLOWLIST_PREFIXES` does NOT
   contain `"DSX-STA-"`, and `check_d05()` (`:360-390`) only inspects a code if
   it matches a hyphen-terminated prefix OR is named in `_D05_ALLOWLIST_CODES`
   (`:168-178`). `DSX-STA-*` is a ~40-code legacy family carrying no citation, so
   a prefix add would fail the build red on every one. All ten Phase-19 codes
   MUST be appended by exact name to `_D05_ALLOWLIST_CODES`, following the file's
   own dated-comment precedent (the Phase-18 block at `:157-167` added
   DSX-STA-050…062 exactly this way). Without it, `--check` stays green even if a
   gate ships with no `Citation:` line — silently defeating the D-05 obligation.

2. **`check_d05`'s docstring resolution is per nearest-enclosing-function
   (`_resolve_docstrings`, `:303-342`), so the ten gates must be split into
   per-family `_check_declared_*` helpers.** A monolith emitting all ten codes
   would satisfy the gate with ONE shared docstring, laundering seven genuinely
   distinct citation obligations (Greenhouse-Geisser; Cochran-Armitage /
   Hamed-Rao; Davidson-MacKinnon / Efron; Hayter / Games-Howell; Zimmerman;
   Hoenig-Heisey / Lakens; Brown-Cai-DasGupta / Newcombe / McCullagh-Nelder) into
   one pass. Recommended split: seven helpers by family, each carrying its own
   attributable `Citation:` + `Structural criterion:` docstring — the exact
   pattern Phase 18 used when it split `_check_declared_association` into
   `_check_correlation_scale_kind` + `_check_agreement_completeness`
   (`stats.py:651` / `:707`).

3. **19-B is NOT needed. Wave 1 is 19-A alone.** `[VERIFIED: live tree]`
   `dsx/mathx.py`'s report-only band surface already carries every convention
   Phase 19 could touch: `KAPPA_BANDS` (`:354`), `REPORT_ONLY_EFFECT_KINDS`
   (`:341`, already includes `kendalls_w`), and `CONVENTION_CATALOG` (`:383`,
   already carries `kendalls_w` as catalog-only, no numeric band). None of
   REQ-P19-01…07's requirement text names an effect-size band, a magnitude
   convention, or `mathx.py` — band growth was REQ-P18-05, explicitly a Phase-18
   concern (19-CONTEXT.md D-08 confirms "Phase 19's requirements ask for no new
   mathx.py band growth"). All ten gates are declared-field PRESENCE checks (D-07:
   nothing numeric is hard-coded), so no report-only band needs a home. **Verdict:
   no 19-B; Wave 1 = 19-A only.** Evidence and the one falsifiable trigger that
   would revive 19-B are in "The 19-B Verdict" below.

4. **The declared-field NAMES are unbound; the SHAPES are fixed (D-03).** For
   each of the ten gates this research gives a concrete recommended field name
   and vocab, flagged as a recommendation not a locked contract, plus the
   reuse-vs-add decision and (where a sub-vocab is added) registration in both
   `_MEMBERSHIP_FIELDS` (`stats.py:40-44`) and `_VOCABULARIES` (`spec.py:620-659`)
   so a mis-slotted value fires the existing DSX-STA-040 for free — the mechanism
   verified still live at `stats.py:544-555`. The load-bearing shape calls
   (resampling `unit` reuse-vs-dedicated; post-hoc family-map; variance-test role
   + the estimand_kind scale exemption; the `none`-satisfies semantics for 081)
   are resolved as reasoned recommendations in Open Questions.

5. **Both canonical fixtures already stay silent on all ten predicates — verified
   empirically.** `[VERIFIED: live tree]` `examples/good-ANALYSIS-SPEC.yaml`
   declares `analysis.test: two_proportion_z` and `examples/bad-ANALYSIS-SPEC.yaml`
   declares `analysis.test: welch_t`; neither carries any sphericity, dose-scores,
   autocorrelation, resampling, post-hoc, variance-role, power-reporting, Wald-CI,
   exposure/offset, or NNT field. None of the ten predicates can fire against
   either file as it stands. D-08's "extend, not replace" means 19-C ADDS fields
   to `bad` so it exercises all ten, and leaves `good` silent — confirm with
   `dsx audit --spec`, don't assume an edit is owed to `good`.

**Primary recommendation:** implement Phase 19 as a two-wave, single-writer,
rows-then-gates split with 19-B dropped (Wave 1 = 19-A alone, Wave 2 = 19-C).
19-A writes all seven `recommend_*` pure functions, all new sub-vocabs, all
`test-selection.md` rows (incl. the DEPRECATED Yates row + pointer rows), the
`finding-codes.md` regen that STAYS 265, and the no-autoswitch tests — asserting
catalogue == 265 at merge. 19-C writes the ten `_check_declared_*` gates split
into seven per-family helpers, wires a single dispatcher into `check()` at BOTH
call sites (`stats.py:231` and `:247`), adds the ten codes by exact name to
`_D05_ALLOWLIST_CODES`, regenerates `finding-codes.md` → 275, extends the `bad`
fixture to fire all ten while `good` stays silent, and adds the gate tests.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Seven dataless `recommend_*` routing lookups (RM, trend, resampling, post-hoc, variance-role, power, proportion/count) | Backend / gate library (`dsx/checks/stats.py`) | Docs (`references/test-selection.md`) | Pure functions taking a declared string only; the doc rows are the human mirror kept in lockstep by convention (no generator — REQ-P20-04 is the future mechanism), exactly as `recommend_association` + its Association section do today |
| Ten `_check_declared_*` gate codes (070/080/081/090/100/110/111/120/121/122) | Backend / gate library (`dsx/checks/stats.py`) | — | Declaration-only string/presence comparison against `analysis:`; same tier as `_check_declared_test` (`:528`) and `_check_declared_association` (`:633`) |
| New closed sub-vocabularies (sphericity correction, dose-score scheme, autocorrelation handling, resampling method, post-hoc family-map, variance-test role, power-reporting type, proportion-CI method) | Backend / spec contract (`dsx/spec.py`) | CLI (`dsx vocab`, discretionary) | `dsx.spec` is the sole `_VOCABULARIES` registry; `dsx.checks.stats` imports from it, never the reverse (the enforced import-direction boundary Phase 18 followed for ICC_MODELS etc.) |
| D-05 citation / reference-value build gate for the ten codes | Build script (`scripts/gen-finding-catalogue.py`) | Test suite (`tests/test_finding_catalogue_invariant.py`) | The allowlist + per-function docstring-resolution mechanism lives in the generator; the invariant test only re-reads its output |
| DEPRECATED (Yates) + pointer (log-linear, mixed-model/GEE, ZIP/hurdle) rows | Docs only (`references/test-selection.md`) | — | `[VERIFIED: live tree]` no code path parses `test-selection.md` (only `dsx/frame/prereg.py` references the *concept* "test-selection function" in prose docstrings); a `status: deprecated` row mints no code and adds no behaviour |
| Report-only convention bands | **N/A this phase** | — | `dsx/mathx.py` already carries every band Phase 19 could touch (Kendall's W is catalog-only); no `mathx.py` growth — see The 19-B Verdict |

## User Constraints

<user_constraints>

### Locked Decisions (19-CONTEXT.md `## Decisions` D-01…D-08, verbatim intent — see 19-CONTEXT.md for exact wording)

- **D-01** — Ten new HIGH/blocking codes from the Phase-17 pre-allocated decades,
  one per explicit "Gate:/blocks" clause (split, not merged, because each failure
  mode has a distinct remedy, citation and declared-field predicate):
  `DSX-STA-070` (a DECLARED two-stage sphericity procedure — Mauchly-then-correct-
  if-significant — on an RM-ANOVA plan → route to unconditional Greenhouse-Geisser;
  keys on the declared procedure, NOT the presence of repeated measures);
  `DSX-STA-080` (`test == cochran_armitage` AND dose/scores field blank);
  `DSX-STA-081` (`test ∈ {mann_kendall, sens_slope}` AND autocorrelation-handling
  field blank — a declared `none`/`assessed: independent` SATISFIES);
  `DSX-STA-090` (a declared resampling procedure with an incomplete
  {seed, B, resampling-unit, method} quadruple — one code, message names the
  missing member); `DSX-STA-100` (declared post-hoc family ≠ declared omnibus
  family — membership against an acceptable family-map); `DSX-STA-110` (a
  variance/scale test declared with role = precondition to a location-test choice
  AND scale is not the declared estimand → block; undeclared role → block for
  declaration-incompleteness); `DSX-STA-111` (observed/post-hoc power declared in
  a readout → block; a-priori/design and MDE-sensitivity do NOT fire — narrow);
  `DSX-STA-120` (proportion-CI method == `wald` → route to Wilson/Jeffreys/
  Agresti-Coull; the n≤40 cutoff is NOT hard-coded); `DSX-STA-121` (exposure/
  time-at-risk present AND offset blank); `DSX-STA-122` (NNT present AND no CI /
  interval-method companion). Total new = 10; catalogue 265 → 275.
- **D-02** — Routing integration shape: extend the Phase-18 hybrid pattern
  verbatim — thin dataless `recommend_*` functions per family (returning the
  acceptable-test/interval SET per declared context) + `_check_declared_*` gates
  beside the untouched `recommend_test`, wired into `check()` at BOTH call sites;
  new rows (incl. DEPRECATED + pointer) in `test-selection.md` in lockstep;
  `finding-codes.md` regen in the gate commit; new codes in `_D05_ALLOWLIST_CODES`
  by exact name. The dataless signatures are the mechanical anti-two-stage proof
  (no data, no n, no distribution flag); the no-autoswitch test guards them
  (REQ-P18-06 doctrine carried forward).
- **D-03** — Declared-field shapes for the new gates (plan-time binds the exact
  field NAMES; shapes fixed here). Reuse an existing declared field where one
  plausibly exists, else add an additive, membership-guarded sub-vocab in
  `dsx/spec.py` `_VOCABULARIES` (a mis-slotted value then fires the existing
  DSX-STA-040 for free). Absence non-blocking (D-10). The per-gate reads and
  reuse/add dispositions are the D-03 table (reproduced in the Phase Requirements
  section below and resolved to concrete names in Open Questions).
- **D-04** — DEPRECATED routing-off row mechanism: Yates (P19-03), SNK +
  unprotected-LSD-at-k>3 (P19-05), Vuong-for-zero-inflation (P19-07) ship as
  doc-only rows in `test-selection.md` flagged `status: deprecated`, minting no
  code and adding no blocking behaviour. `recommend_*` never selects a deprecated
  row as a default; declaring one does not block this phase. A pointer row
  (mixed-model/GEE, log-linear, ZIP/hurdle) is routing-neutral, points OUTWARD to
  an out-of-detailed-scope method; a DEPRECATED row points at an IN-scope method
  that should not be used, carrying "use X instead" + the why-citation (Yates→N-1
  chi-square Campbell 2007; SNK/LSD-k>3→protected post-hoc Hayter 1986 JASA
  81(396):1000-1004; Vuong→misuse-finding only, no replacement, Wilson 2015).
  Active deprecation enforcement is a named D-13 deferral.
- **D-05** — P19-06a Zimmerman two-group scope: scope the CITED empirical result
  to two-group and attach an explicit principled-extension flag to the k-group
  span (`mechanism = a location test conditioned on a data-dependent variance
  pretest distorts Type I error; invariant to group count; empirical k-group
  magnitude UNVERIFIED`). The gate does not need Zimmerman's magnitude — the
  predicate is "variance test declared as a location-choice pretest → block."
  Bancroft 1944 ships not-in-hand / backlog (a future D-05 addendum candidate),
  never pinned unverified.
- **D-06** — Gate-predicate over-block guards: 070 keys on the DECLARED two-stage
  procedure, not the presence of repeated measures (else it false-blocks the
  legitimate mixed-model/GEE route); 110 reads the DECLARED role (pretest → block;
  scale-is-the-estimand → allow; undeclared → block for incompleteness), not the
  presence of Levene/BF/Bartlett/Fligner; 111 fires narrowly (observed/post-hoc
  power in a readout only; design/sensitivity route to the Lakens MDE-sensitivity
  row); 122 is a GATE on the internal completeness doctrine (a bare point NNT is
  active false precision — its interval is mandatory); CMH-with-declared-
  stratification is NOT a gate this phase (a named D-13 deferral, not a silent
  drop).
- **D-07** — D-05 dispositions: the gates check declared-field PRESENCE, not
  computed statistics, so almost nothing pins. Pins are bibliographic locators +
  the Campbell / Hoenig-Heisey algebraic identities + the Newcombe A/B
  disambiguation; everything doctrinal / chapter-level / house-convention ships
  catalog-only. The DO-NOT-HARD-CODE flags are enumerated (see the Anti-Patterns
  and Common Pitfalls sections): Davidson-MacKinnon 19/99-vs-399/1499,
  Brown-Cai-DasGupta n≤40, Campbell smallest-expected-count≥1, McCullagh-Nelder
  §6.2, Hamed-Rao lag threshold, Hayter numeric α, Greenhouse-Geisser ε. Every
  gate CODE's citation (070–121) is in the operator-answered HQ-17 pack; 122 rests
  on internal completeness doctrine (Altman 1998 is a row-bibliography
  confirm-at-execute, NOT a gate-code D-05 read owed at S3-1).
- **D-08** — Single-writer wave split, two sequential waves rows-then-gates, with
  a CONDITIONAL file-disjoint 19-B in Wave 1. Wave 1 = 19-A (all `recommend_*` +
  all sub-vocabs + all rows incl. DEPRECATED/pointer + `finding-codes.md` regen
  STAYS 265 + no-autoswitch tests) ∥ 19-B (mathx bands + APA template — exists
  ONLY if the row inventory surfaces a NEW report-only band). Wave 2 = 19-C (the
  ten gates + wire into `check()` at both call sites + `_D05_ALLOWLIST_CODES` +=
  10 by name + `finding-codes.md` regen → 275 + fixtures extended + gate tests).
  Merge gates: Wave 1 asserts catalogue == 265, dataless-recommend green,
  doc-lockstep holds; Wave 2 asserts catalogue == 275, the D-05 build passes (all
  10 in the allowlist), good stays silent, bad fires all 10, `dsx validate` +
  `dsx gate plan` exit 0. Fallback: a one-wave 18-A/18-B shape (gates inside 19-A)
  is legal (single-writer still holds); rows-then-gates is preferred for the
  265-checkpoint and to freeze the declared-field names before the fixtures are
  written against them.

### Claude's Discretion

19-CONTEXT.md carries no separate "Claude's Discretion" heading — the phase is
bound by D-01…D-08. The residual mechanics D-03 defers ("plan-time binds the
exact field names") are exactly what this research resolves as concrete, reasoned
recommendations (Open Questions), not as pre-decided. Also left to the planner,
confirmed this session: whether to register the new sub-vocabs in `_VOCABULARIES`
so `dsx vocab` dumps them (Phase 18 registered its five for house-style
consistency at `spec.py:654-658` — recommendation: register, low cost); whether
to add `dsx recommend-rm`/`recommend-posthoc`/etc. CLI subcommands (not required
by any REQ — recommendation: defer, the no-autoswitch proof is the signature, not
the CLI); and the seven-helper split granularity (recommended, see Pattern 1).

### Deferred Ideas (OUT OF SCOPE for Phase 19)

- **REQ-P19-03 categorical mints ZERO gate codes.** It is rows (N-1 chi-square,
  CMH with declared stratification, G-test, exact multinomial GOF) + one
  DEPRECATED Yates row + a log-linear pointer row + a Fisher-Freeman-Halton
  honesty footnote. The absent categorical decade is the deliberate tell — do NOT
  mint a categorical code.
- **HQ-22 veto window (non-blocking):** the D-01 numbering. Silence = accept;
  nothing blocks on it.
- **Named D-13 deferrals (entry conditions stated, not silent gaps):**
  CMH-stratifier gate; active deprecation enforcement; observed-power broadening
  (enters when Hoenig-Heisey is source-confirmed to cover all uses); Bancroft 1944
  k-group Zimmerman authority; NNT/RD/RR/OR mandatory-CI symmetry (ships NNT-only
  now); P19-06b Bayesian post-hoc "power" sibling; Fisher-Freeman-Halton practical
  r×c test. Do not build any of these this phase.
- **No mathx.py band growth** (see The 19-B Verdict) — do not add any effect-size
  band; Kendall's W is already catalog-only from Phase 18.

</user_constraints>

<phase_requirements>

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| REQ-P19-01 | RM rows (unconditional Greenhouse-Geisser RM-ANOVA, Friedman, Cochran's Q, Page's L; mixed-model/GEE pointer rows). Gate: DECLARED two-stage sphericity procedure blocks (DSX-STA-070) | Field-shape recommended (`analysis.sphericity_correction` sub-vocab `{unconditional_gg, unconditional_hf, mauchly_conditional, none}`, gate fires on `mauchly_conditional`); over-block guard confirmed (keys on the declared procedure, never on repeated-measures presence — D-06); Greenhouse-Geisser 1959 pins bib locator only, ε never hard-coded (D-07). See Open Questions OQ-1 |
| REQ-P19-02 | Trend rows (Cochran-Armitage with declared dose scores; Jonckheere-Terpstra; Mann-Kendall + Sen's slope with declared autocorrelation handling). Two declared-field gates (DSX-STA-080/081) | 080: `test == cochran_armitage AND is_blank(analysis.dose_scores)`; 081: `test ∈ {mann_kendall, sens_slope} AND is_blank(analysis.autocorrelation_handling)` — a declared `none` SATISFIES (is_blank check, NOT membership). Hamed-Rao 1998 lag threshold NOT hard-coded (D-07). See Open Questions OQ-2/OQ-3 |
| REQ-P19-03 | Categorical rows (N-1 chi-square replacing Yates; CMH with declared stratification; Fisher-Freeman-Halton + honesty footnote; G-test; exact multinomial GOF). **Zero gate codes** | DEPRECATED Yates row (`status: deprecated`, Campbell 2007) + log-linear pointer row + CMH non-blocking surfaced stratification field + FFH footnote. `[VERIFIED: live tree]` no code parses `test-selection.md`, so a deprecated/pointer row mints nothing. Campbell smallest-expected-count≥1 NOT hard-coded. See Pattern 3 |
| REQ-P19-04 | Resampling rows (permutation, percentile bootstrap, BCa house default). Gate: incomplete {seed, B, unit, method} quadruple (DSX-STA-090, one code, names the missing member) | Recommended nested `analysis.resampling: {method, seed, B, unit}` + sub-vocab `RESAMPLING_METHODS = {permutation, percentile_bootstrap, bca}`. The `unit` reuse-vs-dedicated call resolved in OQ-4. Davidson-MacKinnon 19/99-vs-399/1499 NOT conflated, B's value NEVER checked (D-07); Efron 1987 "BCa" acronym not attributed to the 1987 text |
| REQ-P19-05 | Post-hoc rows (Games-Howell house default after Welch ANOVA; Tukey/Kramer; Dunnett+T3; Dunn; Nemenyi; Scheffé; DEPRECATED SNK + unprotected-LSD-k>3). Gate: post-hoc family ≠ omnibus family (DSX-STA-100) | Recommended `analysis.posthoc` + reuse the declared omnibus (an explicit `analysis.omnibus` field recommended over reusing `analysis.test`) + a `POSTHOC_FAMILY_MAP` (omnibus-family → acceptable post-hoc frozenset), membership like DSX-STA-041's `alternatives`. Hayter 1986 numeric α NOT hard-coded; k=3-vs-k≥4 confirm-at-source. See OQ-5 |
| REQ-P19-06 | (a) variance test declared as location-choice pretest blocks (DSX-STA-110, Zimmerman two-group scoped); (b) observed/post-hoc power in a readout blocks (DSX-STA-111, narrow) | 110: `analysis.test ∈ VARIANCE_TESTS AND (role blank OR role == precondition_to_location)` where role sub-vocab `{precondition_to_location, scale_estimand}`; the estimand_kind scale-exemption reuse resolved in OQ-6. 111: `analysis.power_reporting_type ∈ {observed, post_hoc}` fires; `{a_priori, design, mde_sensitivity}` do not. Hoenig-Heisey identity pinned, scope catalog-only, fire NARROWLY (D-06) |
| REQ-P19-07 | Proportion/count extras (Wilson house default, Clopper-Pearson, exact binomial, RD/RR/OR named interval methods, NNT with mandatory CI; ZIP/hurdle pointer; Vuong DEPRECATED). Gates: Wald blocks (120); exposure with no offset blocks (121); NNT with no CI blocks (122) | 120: `analysis.proportion_ci_method == wald` (sub-vocab `{wilson, clopper_pearson, jeffreys, wald, agresti_coull}`, n-independent, n≤40 NOT hard-coded — Brown-Cai-DasGupta 2001). 121: `not is_blank(analysis.exposure) AND is_blank(analysis.offset)` (McCullagh-Nelder §6.2 NOT pinned). 122: `not is_blank(analysis.nnt) AND is_blank(analysis.nnt_ci)` — internal completeness doctrine, Altman 1998 confirm-at-execute. Newcombe A/B disambiguation pins both DOIs. See OQ-7 |

</phase_requirements>

## The 19-B Verdict: NO — Wave 1 is 19-A alone

**Definite call: Phase 19 does NOT need a 19-B plan. Wave 1 = 19-A only.**

Evidence, all `[VERIFIED: live tree]` this session:

1. **`dsx/mathx.py`'s report-only band surface already covers every convention
   Phase 19 could conceivably touch.** The surface is: `EFFECT_SIZE_KINDS =
   frozenset({"d","h","r"})` (`:296`, the frozen blocking domain);
   `REPORT_ONLY_EFFECT_KINDS` (`:341-343`) already contains `kappa, icc,
   kendalls_w, phi, cramers_v, tau_b, rho`; `KAPPA_BANDS` (`:354-361`);
   `KRIPPENDORFF_REFERENCE` (`:373-378`); and `CONVENTION_CATALOG` (`:383-406`)
   which already carries `kendalls_w` as catalog-only with NO numeric band. The
   one band a Friedman / RM readout would want — Kendall's W — is therefore
   already present, recognised, and correctly catalog-only. Phase 19 adds nothing.

2. **No REQ-P19 requirement text names an effect-size band, a magnitude
   convention, or `mathx.py`.** `[VERIFIED: live tree]` `.planning/REQUIREMENTS.md:72-105`
   — REQ-P19-01…07 speak only of rows, declared-field gates, DEPRECATED/pointer
   rows, and citations. Effect-size vocabulary growth in `mathx.py` was REQ-P18-05
   (`.planning/REQUIREMENTS.md`, the Phase-18 block), and 19-CONTEXT.md D-08 states
   the default expectation explicitly: "Phase 19's requirements ask for no new
   mathx.py band growth (that was REQ-P18-05)."

3. **All ten gates are declared-field PRESENCE / membership checks (D-07), so
   nothing numeric — no band, no threshold — is introduced.** A band lives in
   `mathx.py` only when a code adjudicates a magnitude; none of the ten does.

**Consequence for the wave split:** the conditional 19-B (`dsx/mathx.py` +
`templates/APA-TABLE-research.md` + band tests) has no reason to exist. Wave 1 is
19-A alone; `dsx/mathx.py` and `templates/APA-TABLE-research.md` are UNTOUCHED
this phase, and the single-writer table collapses to: Wave 1 writer = 19-A for
`stats.py`/`spec.py`/`test-selection.md`/`finding-codes.md`; Wave 2 writer = 19-C
for the same four + `examples/*.yaml`.

**The one falsifiable trigger that would revive 19-B** (record it, do not build
it): if the S3-2 row inventory surfaces a REQ-P19 row that ships a PINNED numeric
magnitude band with a confirmed source (e.g. an RM/Friedman-specific convention
with a real citation in hand), that band would need a `mathx.py` home and 19-B
returns. This research found no such row in REQ-P19-01…07; Kendall's W — the only
candidate — is already catalog-only (no numeric band) from Phase 18.

## Standard Stack

Not applicable in the conventional sense — this phase installs no package and
uses no library beyond the Python 3 standard library, matching D-01/D-02's
gate-path constraint. `[VERIFIED: live tree]` this session: `python3
scripts/gen-finding-catalogue.py --check` prints "finding catalogue is current"
(the three legacy "declared twice" warnings — DSX-VAL-021, DSX-VAL-060, and
DSX-SPEC-070 — are pre-existing, none Phase-19, and do not fail the gate). The
project uses stdlib `unittest` exclusively; no `pytest` is installed or used
anywhere — do NOT write `pytest`-only syntax into any new test file. Per the
binding ground truth: Python 3.14.6, `tests/test_finding_catalogue_invariant.py`
`_EXPECTED_TOTAL = 265` / `_SNAPSHOT_TOTAL = 256` at baseline.

## Package Legitimacy Audit

Not applicable. This phase installs zero external packages. No `npm view` /
`pip index versions` / registry check is needed; the Package Legitimacy Gate is
vacuously satisfied.

## Architecture Patterns

### System Architecture Diagram

```
ANALYSIS-SPEC.yaml (analyst-authored, or a fixture)
        |
        v
dsx/checks/stats.py::check(spec)
        |
        |-- (not results.tests) early-return branch  [stats.py:227-232]
        |         |-- _check_declared_test(analysis, spec, report)          [UNTOUCHED — line 230]
        |         |-- _check_declared_association(analysis, spec, report)    [Phase 18 — line 231]
        |         `-- _check_declared_advanced_stats(analysis, spec, report) [NEW — add beside, ~line 231]
        |
        `-- post-loop return branch                   [stats.py:245-248]
                  |-- _check_declared_test(section(spec,"analysis"), ...)          [UNTOUCHED — line 246]
                  |-- _check_declared_association(section(spec,"analysis"), ...)   [Phase 18 — line 247]
                  `-- _check_declared_advanced_stats(section(spec,"analysis"), ...) [NEW — add beside, ~line 247]

_check_declared_advanced_stats(analysis, spec, report)   [NEW dispatcher, mirrors _check_declared_association:633]
        |-- _check_declared_rm_sphericity(analysis, report)        -> DSX-STA-070   (Greenhouse-Geisser 1959)
        |-- _check_declared_trend(analysis, report)                -> DSX-STA-080/081 (Cochran-Armitage; Hamed-Rao 1998)
        |-- _check_declared_resampling(analysis, report)           -> DSX-STA-090     (Davidson-MacKinnon 2000; Efron 1987)
        |-- _check_declared_posthoc(analysis, report)              -> DSX-STA-100     (Hayter 1986; Games-Howell 1976)
        |-- _check_declared_variance_role(analysis, report)        -> DSX-STA-110     (Zimmerman 2004, two-group scoped)
        |-- _check_declared_power_reporting(analysis, report)      -> DSX-STA-111     (Hoenig-Heisey 2001; Lakens 2022)
        `-- _check_declared_proportion_count(analysis, report)     -> DSX-STA-120/121/122
                                                                     (Brown-Cai-DasGupta 2001; McCullagh-Nelder 1989; internal completeness)

recommend_rm / recommend_trend / recommend_resampling / recommend_posthoc /
recommend_variance_role / recommend_power / recommend_proportion_ci  [NEW pure, dataless]
        read the new dsx.spec sub-vocabs; return the acceptable SET per declared context;
        the no-autoswitch test asserts each signature takes NO data/n/distribution flag

dsx/spec.py
        |-- SPHERICITY_CORRECTIONS / DOSE_SCORE_SCHEMES / AUTOCORRELATION_HANDLINGS /
        |   RESAMPLING_METHODS / VARIANCE_TEST_ROLES / POWER_REPORTING_TYPES /
        |   PROPORTION_CI_METHODS   [NEW sets, after OPERAND_SCALES:454]
        |-- POSTHOC_FAMILY_MAP      [NEW dict, omnibus-family -> acceptable posthoc frozenset]
        `-- _VOCABULARIES += the membership sub-vocabs   [after :658, for dsx vocab + DSX-STA-040 reuse]

dsx/mathx.py                       -- UNTOUCHED (no 19-B; Kendall's W already catalog-only)
templates/APA-TABLE-research.md    -- UNTOUCHED (no 19-B)

references/test-selection.md   -- NEW sections: RM, Trend, Categorical (+ DEPRECATED Yates row +
                                  log-linear pointer + FFH footnote), Resampling, Post-hoc
                                  (+ DEPRECATED SNK/LSD rows), Proportion/count (+ Vuong DEPRECATED +
                                  ZIP/hurdle pointer). Human doc mirror, parsed by NO code path.

references/finding-codes.md    -- REGENERATED (never hand-edited): 265 (Wave 1) -> 275 (Wave 2)
                                  via scripts/gen-finding-catalogue.py --write

scripts/gen-finding-catalogue.py -- _D05_ALLOWLIST_CODES += the ten codes by exact name
                                    (NOT a prefix add — DSX-STA-* has ~40 uncited legacy codes) [:168-178]

tests/test_finding_catalogue_invariant.py -- _EXPECTED_TOTAL 265->275 [:36]; _MINTED_CODES += ten [:43-46];
                                             _SNAPSHOT_TOTAL stays 256 [:42, byte-frozen]; method name + docstrings
```

### Recommended Project Structure

```
dsx/
├── spec.py                    # 7 new sub-vocab sets + POSTHOC_FAMILY_MAP after
│                               # OPERAND_SCALES (:454); registration in _VOCABULARIES (:658)
├── checks/
│   └── stats.py                # 7 recommend_* pure fns; _check_declared_advanced_stats
│                               # dispatching 7 per-family helpers; wired at BOTH check()
│                               # call sites (lines 231 and 247)
references/
├── test-selection.md          # new RM/Trend/Categorical/Resampling/Post-hoc/Proportion sections
└── finding-codes.md           # regenerated, 265 -> 275
scripts/
└── gen-finding-catalogue.py   # _D05_ALLOWLIST_CODES += the ten codes
examples/
├── good-ANALYSIS-SPEC.yaml    # verified silent on all ten; stays silent (19-C)
└── bad-ANALYSIS-SPEC.yaml     # verified silent; 19-C extends to fire all ten
tests/
├── test_declared_rm_trend_routing.py         # NEW — REQ-P19-01/02/06 no-autoswitch
├── test_declared_resampling_posthoc_routing.py # NEW — REQ-P19-04/05 no-autoswitch
├── test_rm_sphericity_gate.py                # NEW — DSX-STA-070
├── test_trend_gate.py                        # NEW — DSX-STA-080/081
├── test_resampling_gate.py                   # NEW — DSX-STA-090
├── test_posthoc_gate.py                      # NEW — DSX-STA-100
├── test_variance_role_gate.py                # NEW — DSX-STA-110
├── test_power_reporting_gate.py              # NEW — DSX-STA-111
├── test_proportion_count_gate.py             # NEW — DSX-STA-120/121/122
└── test_finding_catalogue_invariant.py       # EXTENDED — 265 -> 275, +10 minted
```

### Pattern 1: Split the ten gates into seven per-family helpers so D-05's docstring resolution stays honest

**What:** `scripts/gen-finding-catalogue.py::_resolve_docstrings` (`[VERIFIED:
live tree]` `:303-342`) maps each `report.add(...)` call site to the docstring of
its NEAREST enclosing `FunctionDef`, via a synthesized child→parent map (no native
`ast` parent pointer). If all ten codes sit in one function, they share one
docstring for D-05 — a single `Citation:` line satisfies the gate for all ten.

**When to use:** whenever one gate emits codes drawing on genuinely different
citations. Here that is seven distinct citation clusters. Phase 18 set the
precedent exactly: `_check_declared_association` (`stats.py:633`) is a thin
dispatcher that calls `_check_correlation_scale_kind` (`:651`, carrying the
Fisher/estimand-scale citation) and `_check_agreement_completeness` (`:707`,
carrying Shrout-Fleiss + McGraw-Wong + Feinstein-Cicchetti — multiple citations
in ONE docstring, which the gate accepts). Multi-citation-per-helper is fine; the
split is by REMEDY FAMILY, not one-helper-per-code.

**Recommended shape (sketch, not final — field names are recommendations, OQ):**
```python
# Source: dsx/checks/stats.py (this repository), sketch for Phase 19. Sits beside
# _check_declared_association; dispatcher wired at BOTH check() call sites (231, 247).

def _check_declared_advanced_stats(analysis: dict, spec: dict, report: Report) -> None:
    """Dispatch the seven declaration-only Phase-19 gate families.

    Sits beside _check_declared_test / _check_declared_association (D-02's "hybrid,
    not fold-in"): every predicate keys on DECLARED analysis: fields, never on data
    (the anti-two-stage invariant, REQ-P18-06 doctrine). Split into per-family
    helpers so each carries its own attributable D-05 docstring (Pattern 1).
    """
    if not analysis:
        return
    _check_declared_rm_sphericity(analysis, report)
    _check_declared_trend(analysis, report)
    _check_declared_resampling(analysis, report)
    _check_declared_posthoc(analysis, report)
    _check_declared_variance_role(analysis, report)
    _check_declared_power_reporting(analysis, report)
    _check_declared_proportion_count(analysis, report)


def _check_declared_rm_sphericity(analysis: dict, report: Report) -> None:
    """DSX-STA-070: a DECLARED two-stage sphericity procedure on an RM-ANOVA plan.

    Citation: Greenhouse, S.W. & Geisser, S. (1959), Psychometrika 24(2):95-112
    [PIN the bib locator only — ε is computed from data, NEVER a fixture; and this
    is NOT the reversed 1958 Annals paper]. Maxwell & Delaney (2004) ch.11-12 ships
    catalog-paraphrase (access blocked, D-07). Structural criterion: declaration-only
    string comparison against analysis.sphericity_correction; fires ONLY on the
    declared two-stage/Mauchly-conditional token, NEVER on the mere presence of
    repeated measures (D-06 — else it false-blocks the legitimate mixed-model/GEE
    route, which never invokes a sphericity step). Absent field is non-blocking.
    """
    if normalize(analysis.get("sphericity_correction", "")) == "mauchly_conditional":
        report.add("DSX-STA-070", "HIGH", ...)
        # D-05: DSX-STA-070

def _check_declared_trend(analysis: dict, report: Report) -> None:
    """DSX-STA-080/081: declared trend tests missing a required companion field.

    Citation: Cochran (1954) / Armitage (1955) [dose-response trend, 080];
    Hamed, K.H. & Rao, A.R. (1998), J. Hydrology 204(1-4):182-196 [autocorrelation-
    corrected Mann-Kendall, 081 — PIN bib locator; do NOT hard-code the
    autocorrelation-significance lag threshold: the gate checks "handling declared,"
    not the corrected variance]. Structural criterion: presence checks only. 080:
    test == cochran_armitage AND dose_scores blank. 081: test in {mann_kendall,
    sens_slope} AND autocorrelation_handling blank — a DECLARED `none`/`independent`
    is non-blank and SATISFIES (force the declaration, never a correction; D-06).
    """
    declared = normalize(analysis.get("test", ""))
    if declared == "cochran_armitage" and is_blank(analysis.get("dose_scores")):
        report.add("DSX-STA-080", "HIGH", ...)  # D-05: DSX-STA-080
    if declared in ("mann_kendall", "sens_slope") and is_blank(analysis.get("autocorrelation_handling")):
        report.add("DSX-STA-081", "HIGH", ...)  # D-05: DSX-STA-081
```
The `090` quadruple helper names the single missing member in its message (one
code, not four); `100` derives the omnibus family from the declared omnibus and
membership-tests the declared post-hoc against `POSTHOC_FAMILY_MAP`; `110` reads
the declared role; `111` fires only for `{observed, post_hoc}`; `120/121/122` are
three presence/membership predicates in one proportion-count helper. Field names
are this session's recommendation — see Open Questions.

### Pattern 2: Wire the new dispatcher at BOTH of `check()`'s existing call sites

**What:** `[VERIFIED: live tree]` `dsx/checks/stats.py::check()` calls the
declaration gates from TWO places: the `if not tests:` early-return branch
(`:227-232`, call sites at `:230` `_check_declared_test` and `:231`
`_check_declared_association`) and the post-loop return (`:245-248`, call sites at
`:246` and `:247`). A pure declaration-only Phase-19 spec (an RM/trend/resampling
plan with no computed `results.tests` yet) hits the early-return branch — so
`_check_declared_advanced_stats` MUST be added at BOTH sites (beside line 231 AND
beside line 247), not just one, or a declaration-only spec silently skips every
Phase-19 gate.

### Pattern 3: The DEPRECATED / pointer row mechanism is doc-only and mints nothing

**What:** `[VERIFIED: live tree]` `references/test-selection.md` is a pure human
mirror. No code path parses it — the only `dsx/` reference to "test-selection" is
`dsx/frame/prereg.py` naming the *concept* ("the declared fallback rule is the
preregistered test-selection function") in prose docstrings (`:3`, `:308`), never
reading the file. The catalogue generator (`gen-finding-catalogue.py::collect`,
`:250-267`) walks `dsx/**/*.py` `report.add(...)` AST call sites ONLY — it never
touches `test-selection.md`. Therefore a row flagged `status: deprecated` (Yates,
SNK, unprotected-LSD-k>3, Vuong) or a `status: pointer` row (log-linear,
mixed-model/GEE, ZIP/hurdle) adds ZERO codes and ZERO behaviour. The existing
Association section already uses a `Status` column for catalog-only rows
(`test-selection.md:96-101`), so the mechanism is a natural extension, not a new
construct.

**How to structure it:** add a `Status` (or `status:`) column to the new tables;
a DEPRECATED row carries "use X instead" + the why-citation (Campbell 2007 for
Yates→N-1; Hayter 1986 for SNK/LSD→protected post-hoc; Wilson 2015 for Vuong,
misuse-finding only, NO replacement endorsed). The `recommend_*` pure functions
must never return a deprecated row as a default (the acceptable SET excludes it).

### Anti-Patterns to Avoid

- **Adding `"DSX-STA-"` to `_D05_ALLOWLIST_PREFIXES`.** `[VERIFIED: live tree]`
  `:87-89` — the family has ~40 legacy codes with no `Citation:` docstring line
  and no `# D-05:` marker; a prefix add fails the build red on all of them. Use
  the exact-code path (`_D05_ALLOWLIST_CODES`, `:168-178`), the precedent every
  prior in-family addition used (DSX-EXP-070, DSX-MET-021, DSX-COH-040, and the
  Phase-18 DSX-STA-050…062 block at `:157-167`).
- **A single monolithic gate function emitting all ten codes.** Passes `check_d05`
  with one shared docstring, laundering seven distinct citation obligations
  (Pattern 1 / Pitfall 2).
- **Hand-editing `references/finding-codes.md`.** Its header says "Do not edit by
  hand." Run `python3 scripts/gen-finding-catalogue.py --write` after the code
  lands and commit the regen in the SAME commit as the `report.add` calls.
- **Firing DSX-STA-070 on the presence of repeated measures.** D-06: it keys on
  the DECLARED two-stage procedure ONLY, else it false-blocks the mixed-model/GEE
  route (which never has a sphericity step). Same lesson as Phase-18's
  point-biserial whitelist — don't false-block the legitimate case.
- **Firing DSX-STA-110 on the presence of Levene/BF/Bartlett/Fligner.** D-06: it
  keys on the declared ROLE (`precondition_to_location` → block; `scale_estimand`
  → allow; blank → block for incompleteness). A scale test IS the correct primary
  analysis when scale is the estimand.
- **Broadening DSX-STA-111 beyond `{observed, post_hoc}`.** Hoenig-Heisey's
  coverage of all post-hoc power uses is UNCONFIRMED at source; a broad fire
  over-blocks a legitimate "use this pilot's observed effect to plan the next
  study" declaration. Broadening is a D-13 deferral.
- **Hard-coding any numeric statistic (D-07).** The gates check declared-field
  PRESENCE, never a computed value. Do NOT hard-code: Greenhouse-Geisser ε;
  Hamed-Rao lag threshold; Davidson-MacKinnon B floors (do NOT conflate 19/99 with
  399/1499, and NEVER check B's value); Brown-Cai-DasGupta n≤40; Campbell
  smallest-expected-count≥1; McCullagh-Nelder §6.2 page; Hayter numeric inflated-α.
- **Adding the new test names to `PARAMETRIC_TESTS` / `NONPARAMETRIC_TESTS`.**
  `[VERIFIED: live tree]` `stats.py:76-84` — these two sets exist ONLY to gate
  DSX-STA-042/043 inside `_check_declared_test`, orthogonal to the new gates.
  Adding `cochran_armitage`/`mann_kendall`/`games_howell`/etc. would trip
  DSX-STA-042 (unassessed normality/variance/independence) on a trend/RM
  declaration. Leave both sets unchanged.
- **Minting a categorical (P19-03) code.** The absent decade is deliberate — rows
  + one DEPRECATED Yates row + pointer + footnote, ZERO codes.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Catalogue gained/lost a code | A bespoke diff | `gen-finding-catalogue.py --check` + `test_finding_catalogue_invariant.py`'s set-identity test, extended with the ten codes | Already exists, already wired into the gate sequence, already does set-identity not just count |
| A new code carries a citation | A review checklist | `check_d05()` + `_D05_ALLOWLIST_CODES` | Already a build-time gate; the only missing step is naming the ten codes in the allowlist |
| Mis-slotted routing value is loud | A bespoke validator | Register each new membership sub-vocab in `_MEMBERSHIP_FIELDS` (`stats.py:40-44`) — DSX-STA-040 fires for free (`:544-555`) | The recognition half of every gate costs ZERO new code; Phase 18 did exactly this for `operand_scale` |
| A "no autoswitch" proof for the new families | A prose note | `inspect.signature(recommend_*)` structural assertions, modelled on the Phase-18 `recommend_association` signature test (`18-RESEARCH.md:838-862`) | The dataless signature IS the proof; a signature-inspecting test cannot silently rot |
| DEPRECATED/pointer routing-off | A new gate/parser | A `status:` cell in `test-selection.md` (doc-only, parsed by no code path) | Active deprecation enforcement is an explicit D-13 deferral; a doc row mints nothing |

**Key insight:** every mechanism Phase 19 needs already exists and was exercised
by Phase 18 — the membership-guard idiom, the exact-code D-05 allowlist, the
catalogue set-identity invariant, the doc/code lockstep, the two-call-site
wiring, and the per-family docstring split. The work is composition plus ten
declared-field-name bindings (Open Questions) — not new machinery.

## Common Pitfalls

### Pitfall 1: The untouched `_check_declared_test` fires a false DSX-STA-041 against a new gate-test fixture
**What goes wrong:** `_check_declared_test` runs whenever both `analysis.test` and
`analysis.outcome_type` are declared and non-blank (`[VERIFIED: live tree]`
`stats.py:557-560`), and it has no awareness of the Phase-19 tests. A fixture
declaring `analysis: {outcome_type: continuous, test: mann_kendall}` to exercise
DSX-STA-081 ALSO trips the old gate: `recommend_test("continuous", 2, ...)`
derives `welch_t`/`mann_whitney`, `mann_kendall` is not in that acceptable set, and
DSX-STA-041 fires unrelated.
**Why it happens:** `recommend_test`/`_check_declared_test` and the new gates are
deliberately independent (D-02's "hybrid, not fold-in"); nothing suppresses one
for the other.
**How to avoid:** the same three options Phase 18 documented — (a) omit
`analysis.outcome_type` in the gate fixture (the early-return at `stats.py:559-560`
skips the test-recommendation, though the `_MEMBERSHIP_FIELDS` loop still runs, which
is fine), or (b) call the specific `_check_declared_*` helper directly as a unit,
or (c) pick an `outcome_type`/`test` combo `recommend_test` accepts. Name the
choice in the test docstring. Also assert `codes` exhaustively so a stray
DSX-STA-041 does not hide behind a `DSX-STA-081 in codes` membership check.

### Pitfall 2: D-05's docstring resolution is per enclosing function, not per code
Restated as a pitfall: a single dispatcher body emitting all ten codes passes
`check_d05()` with one shared, generic docstring — the build stays green while
seven distinct citation obligations go unmet in substance. Split into the seven
per-family helpers (Pattern 1). Each helper's docstring needs a `Citation:` line,
a `Structural criterion:`/`Reference value:` line, and a matching `# D-05: <CODE>`
marker under `tests/` for EVERY code it emits.

### Pitfall 3: The ten new codes are silently uncovered by the D-05 build gate unless named in `_D05_ALLOWLIST_CODES`
**What goes wrong:** `[VERIFIED: live tree]` `:87-89` — `DSX-STA-` is not a
prefix; unless the ten codes are added by exact name to `_D05_ALLOWLIST_CODES`
(`:168-178`), `check_d05()` never inspects them and `--check` passes even with no
`Citation:` line.
**How to avoid:** add all ten — `DSX-STA-070`, `-080`, `-081`, `-090`, `-100`,
`-110`, `-111`, `-120`, `-121`, `-122` — to `_D05_ALLOWLIST_CODES`, with a dated
Phase-19 comment block after the Phase-18 block (`:157-167`), following that
block's precedent style.
**Warning sign:** `gen-finding-catalogue.py --check` exits 0 even though a new
`report.add("DSX-STA-070", ...)` has no `Citation:` docstring line.

### Pitfall 4: The `_EXPECTED_TOTAL` / `_MINTED_CODES` / `_SNAPSHOT_TOTAL` triple in the invariant test
**What goes wrong:** bumping only `_EXPECTED_TOTAL` (265→275) without adding the
ten codes to `_MINTED_CODES` (or vice versa) fails the set-identity test, or lets
a cardinality-preserving swap slip through.
**How to avoid:** `[VERIFIED: live tree]` update the triple together —
`_EXPECTED_TOTAL = 275` (line 36), `_MINTED_CODES` unions the ten Phase-19 codes
(lines 43-46, currently holds the four pre-existing + the five Phase-18 codes),
`_SNAPSHOT_TOTAL` stays 256 (line 42) and `tests/fixtures/finding-codes-phase12.md`
stays byte-frozen — NEVER mutate it. Also rename the method
`test_finding_catalogue_stays_at_265_codes` (line 59) → `_275_codes`, and update
the several `265`-mentioning docstrings/assert messages (lines 33-35, 60-70,
84-90, 108-143). The regex `_TOTAL_RE`/`_ROW_RE` (lines 50/55) are CRLF-safe
(`\|\s*` non-line-anchored) — no change needed, but keep any new prose CRLF-safe.

### Pitfall 5: The `none`-satisfies semantics for DSX-STA-081 is an `is_blank` check, NOT a membership check
**What goes wrong:** if the gate is written as `normalize(autocorrelation_handling)
not in AUTOCORRELATION_HANDLINGS` it would fire on a blank field (correct) but the
membership framing invites a future contributor to "tighten" it into rejecting a
declared `none`. D-01/D-06 are explicit: a DECLARED `none`/`independent` SATISFIES
the gate (it forces the declaration, never a correction).
**How to avoid:** the FIRING predicate is `is_blank(analysis.get(
"autocorrelation_handling"))` — presence, not value. Register
`AUTOCORRELATION_HANDLINGS` (with `none`/`independent` as members) in
`_MEMBERSHIP_FIELDS` so a TYPO'd handling value fires DSX-STA-040 separately, but
DSX-STA-081 itself keys on blankness. `none` is non-blank, so it never fires 081.
**Warning sign:** a fixture declaring `autocorrelation_handling: none` fires
DSX-STA-081 — the tell that the gate used membership instead of `is_blank`.

### Pitfall 6: DSX-STA-110's estimand_kind scale-exemption has no scale member in the current vocabulary
**What goes wrong:** D-03 says "reuse Phase-18 `estimand_kind` for the scale
exemption," but `[VERIFIED: live tree]` `ESTIMAND_KINDS` (`spec.py:398-423`) has
SIX members — `linear_association, monotone_association, nominal_association,
agreement, method_comparison, ordered_trend` — and NONE denotes scale/dispersion.
Reading the exemption off `estimand_kind` today would never exempt anything, and
ADDING a `dispersion_comparison` member is scope creep (D-03 says reuse, not grow;
CMH-gate precedent — the smaller provable claim).
**How to avoid:** carry the exemption on the DECLARED role field itself:
`variance_test_role == scale_estimand` means scale IS the estimand → allow;
`precondition_to_location` → block; blank → block for incompleteness. Keep an
`estimand_kind`-based exemption as an inert secondary path (harmless no-op today,
auto-activates if a future phase adds a scale member). Flag the "add a scale
estimand_kind member?" question as OQ-6 for the planner — recommend NOT adding it
this phase.
**Warning sign:** the gate imports `ESTIMAND_KINDS` and branches on a member name
that does not exist in the vocabulary.

### Pitfall 7: DSX-STA-122 rests on internal completeness doctrine, not an external D-05 read
**What goes wrong:** treating Altman-Deeks-Sackett 1998 (BMJ 317:1309-1312) as an
owed gate-code D-05 read at S3-1 stalls the plan on a citation the gate mechanism
does not need. D-06: 122 ships on the internal completeness doctrine (a point
estimate ships with its interval — the same self-scoping class as the resampling
quadruple and, in Phase 18, DSX-STA-062's structural criterion). Altman is a
ROW-BIBLIOGRAPHY citation confirmed at the execute row-bibliography pass, before
the NNT row prints.
**How to avoid:** the `_check_declared_proportion_count` docstring's `Citation:`
line for 122 names the internal completeness doctrine (mirroring how Phase-18's
`_check_agreement_completeness` cited a `Structural criterion:` for its
presence-only codes); the `# D-05: DSX-STA-122` marker + a `Structural criterion:`
line still satisfy the build gate. Do NOT block S3-1 waiting on Altman.

## Code Examples

### The two `check()` call sites the new dispatcher wires into (verified this session, `dsx/checks/stats.py`)
```python
# Source: dsx/checks/stats.py:227-248 — CURRENT state, confirmed by direct read.
    if not tests:
        analysis = section(spec, "analysis")
        if analysis:
            _check_declared_test(analysis, spec, report)          # line 230
            _check_declared_association(analysis, spec, report)   # line 231
            # NEW: _check_declared_advanced_stats(analysis, spec, report)
        return report

    pvalues: list[float] = []
    for index, test in enumerate(tests):
        ...
    _check_correction_applied(spec, pvalues, alpha, report)
    _check_declared_test(section(spec, "analysis"), spec, report)          # line 246
    _check_declared_association(section(spec, "analysis"), spec, report)   # line 247
    # NEW: _check_declared_advanced_stats(section(spec, "analysis"), spec, report)
    return report
```

### The existing membership-guard the recognition half reuses for free (verified this session, `dsx/checks/stats.py`)
```python
# Source: dsx/checks/stats.py:40-44 and 544-555 — CURRENT state.
_MEMBERSHIP_FIELDS: "tuple[tuple[str, Any], ...]" = (
    ("outcome_type", OUTCOME_TYPES),
    ("estimand_kind", ESTIMAND_KINDS),
    ("operand_scale", OPERAND_SCALES),
    # NEW (Phase 19): ("sphericity_correction", SPHERICITY_CORRECTIONS),
    #                 ("autocorrelation_handling", AUTOCORRELATION_HANDLINGS),
    #                 ("power_reporting_type", POWER_REPORTING_TYPES),
    #                 ("proportion_ci_method", PROPORTION_CI_METHODS),
    #                 ("variance_test_role", VARIANCE_TEST_ROLES), ...
)
# for field_name, vocabulary in _MEMBERSHIP_FIELDS:  (loop at :544)
#     ... if value not in vocabulary: report.add("DSX-STA-040", "MEDIUM", ...)
```
Registering each new closed sub-vocab here makes a mis-slotted value loud via the
existing DSX-STA-040, zero new code — exactly how `operand_scale` was added in
Phase 18. (Nested-block sub-vocabs like the resampling `method` are validated
inside their own gate helper, not this flat loop; see OQ-4.)

### The exact allowlist block to extend (verified this session, `scripts/gen-finding-catalogue.py`)
```python
# Source: scripts/gen-finding-catalogue.py:168-178 — CURRENT state.
_D05_ALLOWLIST_CODES = frozenset(
    {
        "DSX-SPEC-080", "DSX-SPEC-081", "DSX-SPEC-082", "DSX-SPEC-085", "DSX-SPEC-086",
        "DSX-CODE-020", "DSX-CODE-021", "DSX-CODE-030", "DSX-CODE-031",
        "DSX-ML-023", "DSX-ML-024", "DSX-ML-043", "DSX-ML-052", "DSX-ML-053",
        "DSX-ML-090", "DSX-ML-091", "DSX-ML-092",
        "DSX-COH-040",
        "DSX-EXP-070", "DSX-MET-021",
        "DSX-STA-050", "DSX-STA-051", "DSX-STA-060", "DSX-STA-061", "DSX-STA-062",
        # Phase 19 (REQ-P19-01/02/04/05/06/07, 2026-09-02) adds the ten codes here, by
        # exact code and NOT via _D05_ALLOWLIST_PREFIXES (DSX-STA-* is a ~40-code legacy
        # family with no citation; a prefix add would fail the build on all of them —
        # 19-RESEARCH.md Pitfall 3). Each lives in a per-family helper carrying its own
        # attributable D-05 docstring (19-RESEARCH.md Pattern 1).
        # "DSX-STA-070", "DSX-STA-080", "DSX-STA-081", "DSX-STA-090", "DSX-STA-100",
        # "DSX-STA-110", "DSX-STA-111", "DSX-STA-120", "DSX-STA-121", "DSX-STA-122",
    }
)
```

### The invariant-test triple to move (verified this session, `tests/test_finding_catalogue_invariant.py`)
```python
# Source: tests/test_finding_catalogue_invariant.py:36-46 — CURRENT state.
_EXPECTED_TOTAL = 265   # -> 275
_SNAPSHOT_TOTAL = 256   # UNCHANGED — never mutate the byte-frozen snapshot
_MINTED_CODES = {
    "DSX-REP-060", "DSX-REP-061", "DSX-EXP-070", "DSX-MET-021",
    "DSX-STA-050", "DSX-STA-051", "DSX-STA-060", "DSX-STA-061", "DSX-STA-062",
    # -> add the ten Phase-19 codes: DSX-STA-070/080/081/090/100/110/111/120/121/122
}
```

### The mathx.py band surface that stays UNTOUCHED (verified this session — the 19-B evidence)
```python
# Source: dsx/mathx.py:296, 341-343, 383-393 — CURRENT state.
EFFECT_SIZE_KINDS = frozenset({"d", "h", "r"})                      # frozen blocking domain
REPORT_ONLY_EFFECT_KINDS = frozenset(
    {"kappa", "icc", "kendalls_w", "phi", "cramers_v", "tau_b", "rho"}  # kendalls_w already here
)
CONVENTION_CATALOG = {
    "kendalls_w": ("Kendall's W magnitude bands — catalog-only: no band citation "
                   "exists anywhere in the repo or the HQ-16 pack, so NO numeric "
                   "boundary is asserted. A D-05 read is owed before any Kendall's W band ships."),
    ...
}
```
Kendall's W — the only band a Friedman/RM readout would want — is already
recognised and catalog-only. No REQ-P19 requirement asks for a numeric band, so
`mathx.py` is untouched and 19-B does not exist.

## State of the Art

Not applicable — this phase extends an internal declaration-only contract; the
statistical methods (RM-ANOVA, Cochran-Armitage, Mann-Kendall/Sen, permutation/
bootstrap/BCa, Games-Howell/Tukey/Dunnett/Dunn/Nemenyi/Scheffé, Levene/BF/Bartlett/
Fligner, Wilson/Clopper-Pearson/Jeffreys/Agresti-Coull, NNT) are decades-old and
stable. No external ecosystem version to track. The one current-state caveat: the
Greenhouse-Geisser citation must be the 1959 Psychometrika 24(2):95-112 paper, NOT
the reversed 1958 Annals paper (D-07); and Efron's "BCa" acronym is Efron-Tibshirani
1993, not the 1987 JASA text (D-07) — both are citation-text disciplines, not gate
mechanics.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | `analysis.sphericity_correction` (sub-vocab `{unconditional_gg, unconditional_hf, mauchly_conditional, none}`, gate fires on `mauchly_conditional`) is the correct field-shape for DSX-STA-070 | OQ-1 | Low — shape is fixed by D-03; only the NAME/token is a proposal. A rename is a mechanical edit, not a re-architecture |
| A2 | `analysis.dose_scores` (presence) + optional `analysis.dose_score_scheme` sub-vocab for DSX-STA-080; `analysis.autocorrelation_handling` (sub-vocab incl. `none`/`independent`) for DSX-STA-081, keyed on `is_blank` not membership | OQ-2/OQ-3, Pitfall 5 | Medium — the `none`-satisfies semantics is load-bearing (D-06); getting the predicate wrong (membership instead of is_blank) would false-block a legitimate declared `none` |
| A3 | Nested `analysis.resampling: {method, seed, B, unit}` with a DEDICATED `unit` field (not reusing `design.randomization_unit`) is the correct shape for DSX-STA-090 | OQ-4 | Medium — CONTEXT D-03 leans "reuse the analysis/randomization unit," but those live under `design`/`validity_frame.units`, not `analysis`; the resampling exchangeability unit is semantically distinct. A wrong reuse could let the gate pass on a design-level unit that doesn't describe the resampling |
| A4 | `analysis.omnibus` (declared omnibus test) + `analysis.posthoc` + a `POSTHOC_FAMILY_MAP` is the correct shape for DSX-STA-100, rather than reusing `analysis.test` as the omnibus | OQ-5 | Medium — `analysis.test` may hold the post-hoc rather than the omnibus in a post-hoc-focused spec; an explicit `omnibus` field disambiguates. Reusing `analysis.test` risks reading the wrong operand |
| A5 | The DSX-STA-110 scale exemption rides on `variance_test_role == scale_estimand`, not on an `estimand_kind` scale member (which does not exist), and no scale member should be added this phase | OQ-6, Pitfall 6 | Medium — D-03 says "reuse estimand_kind"; this session reads that as an inert secondary path since no scale member exists, and recommends against adding one (scope). If the planner adds a member, the gate gains a second exemption path |
| A6 | `analysis.power_reporting_type` sub-vocab `{a_priori, design, observed, post_hoc, mde_sensitivity}` lives on `analysis:` (not `results:`) for DSX-STA-111 | OQ-7 | Low — the gate path reads `analysis`; a `results.`-placed field would be unreachable by the current dispatcher without a second read |
| A7 | Flat `analysis.proportion_ci_method` (sub-vocab), `analysis.exposure`+`analysis.offset` (presence), `analysis.nnt`+`analysis.nnt_ci` (presence) for DSX-STA-120/121/122 | OQ-7 | Low — presence/membership shapes are unambiguous; only names are proposals |

## Open Questions

> All ten are declared-field NAME bindings D-03 explicitly defers to "a plan-time
> binding for S3-2." The SHAPES are fixed by D-03; these are concrete, reasoned
> NAME/vocab recommendations for the planner to confirm or override — NOT
> already-decided contracts.

1. **DSX-STA-070 sphericity field.** Recommend `analysis.sphericity_correction`,
   sub-vocab `SPHERICITY_CORRECTIONS = {"unconditional_gg", "unconditional_hf",
   "mauchly_conditional", "none"}`, registered in `_MEMBERSHIP_FIELDS`. Gate fires
   iff `normalize(...) == "mauchly_conditional"`. The token name for the two-stage
   procedure is the only real choice (`mauchly_conditional` vs `two_stage`);
   recommend `mauchly_conditional` (names the mechanism). **Planner confirms.**

2. **DSX-STA-080 dose-scores field.** Recommend `analysis.dose_scores` (presence)
   + optional `analysis.dose_score_scheme` sub-vocab `{equally_spaced, midrank,
   custom}`. Gate: `test == cochran_armitage AND is_blank(dose_scores)`. The scheme
   is optional and DSX-STA-040-guarded; the trigger is presence only.

3. **DSX-STA-081 autocorrelation field.** Recommend `analysis.autocorrelation_handling`,
   sub-vocab `{none, independent, hamed_rao, prewhitening, yue_pilon}`, registered
   in `_MEMBERSHIP_FIELDS`. **Gate keys on `is_blank`, NOT membership** (Pitfall 5):
   a declared `none`/`independent` is non-blank and SATISFIES.

4. **DSX-STA-090 resampling quadruple + the `unit` reuse call (load-bearing).**
   Recommend a nested `analysis.resampling: {method, seed, B, unit}` block +
   `RESAMPLING_METHODS = {"permutation", "percentile_bootstrap", "bca"}`. Gate: if
   the block (or `method`) is present, check each of {method, seed, B, unit}
   non-blank; one code, message names the first/only missing member. **The `unit`
   call:** CONTEXT D-03 suggests reusing the analysis/randomization unit, but those
   live under `design.randomization_unit`/`validity_frame.units`, not `analysis:`,
   and the resampling exchangeability unit (cluster/block vs iid FOR THE RESAMPLE)
   is a distinct concept. **Recommend a DEDICATED `analysis.resampling.unit`
   presence field** (the quadruple self-describes the resampling procedure); a
   fallback cross-read of `design.randomization_unit` is defensible but risks the
   gate passing on a unit that doesn't describe the resample. **Planner binds.**

5. **DSX-STA-100 post-hoc family-map.** Recommend `analysis.posthoc` (declared
   post-hoc) + an explicit `analysis.omnibus` (declared omnibus test) + a
   `POSTHOC_FAMILY_MAP: dict[str, frozenset[str]]` (omnibus-family → acceptable
   post-hoc set), structured like `_ASSOCIATION_ROUTES` (`stats.py:57-73`). Gate:
   both present AND `posthoc ∉ POSTHOC_FAMILY_MAP[omnibus_family]` → block,
   membership like DSX-STA-041's `alternatives`. Recommend an explicit `omnibus`
   field over reusing `analysis.test` (which may hold the post-hoc in a post-hoc
   spec). Deprecated post-hocs (SNK, unprotected-LSD-k>3) are NEVER in an
   acceptable set (D-04). **Planner binds the field names + the family-map contents.**

6. **DSX-STA-110 role field + the estimand_kind exemption.** Recommend
   `analysis.variance_test_role` sub-vocab `{precondition_to_location,
   scale_estimand}` + a `VARIANCE_TESTS = {levene, brown_forsythe, bartlett,
   fligner_killeen}` trigger set. Gate: `test ∈ VARIANCE_TESTS AND (is_blank(role)
   OR role == precondition_to_location)` → block. **The estimand_kind scale
   exemption has no vocabulary member to hang on today** (Pitfall 6): recommend the
   role field carry the exemption and do NOT add a `dispersion` estimand_kind
   member this phase (scope). **Planner confirms: role-only, or add a scale member?**

7. **DSX-STA-111/120/121/122 fields.** Recommend `analysis.power_reporting_type`
   sub-vocab `{a_priori, design, observed, post_hoc, mde_sensitivity}` (111 fires
   on `{observed, post_hoc}` only); `analysis.proportion_ci_method` sub-vocab
   `{wilson, clopper_pearson, jeffreys, wald, agresti_coull}` (120 fires on `wald`);
   flat `analysis.exposure` + `analysis.offset` presence (121 fires on exposure
   present + offset blank); flat `analysis.nnt` + `analysis.nnt_ci` presence (122
   fires on nnt present + nnt_ci blank). All membership sub-vocabs register in
   `_MEMBERSHIP_FIELDS`. **Planner confirms names.**

8. **CMH stratification surfaced field (non-gated, P19-03).** D-03 lists CMH
   stratification + RD/RR/OR interval method as surfaced declared fields,
   non-blocking (D-10). Recommend `analysis.cmh_strata` and `analysis.interval_method`
   as presence-surfaced fields with NO gate. The CMH-stratifier gate is a named
   D-13 deferral. **No gate this phase — confirm the surfaced field names only.**

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3 | Everything | Yes | 3.14.6 (binding ground truth) | — |
| `unittest` (stdlib) | Test execution | Yes | stdlib | — |
| `pytest` | Not used | No | — | N/A — project is stdlib `unittest` only; never write pytest syntax |
| `scripts/gen-finding-catalogue.py` | Catalogue regen + D-05 build gate | Yes — ran `--check` this session, prints "finding catalogue is current" at 265 | — | — |

No missing dependencies block this phase.

## Validation Architecture

> Seed for 19-VALIDATION.md. `.planning/config.json` nyquist_validation is not
> `false`, so this section is included.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Python stdlib `unittest` |
| Config file | none — `python3 -m unittest discover -s tests` |
| Quick run command | `python3 -m unittest tests.<module_name> -v` |
| Full suite command | `python3 -m unittest discover -s tests -q` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| REQ-P19-01 | `recommend_rm(...)` dataless; DSX-STA-070 fires on `mauchly_conditional`, silent on `unconditional_gg`/absent; never fires on repeated-measures presence | unit + structural | `python3 -m unittest tests.test_rm_sphericity_gate -v` | Wave 0 — new |
| REQ-P19-02 | DSX-STA-080 fires on `cochran_armitage` + blank dose_scores; DSX-STA-081 fires on `mann_kendall`/`sens_slope` + blank handling, SILENT on declared `none` | unit | `python3 -m unittest tests.test_trend_gate -v` | Wave 0 — new |
| REQ-P19-03 | DEPRECATED Yates row + log-linear pointer + CMH surfaced field + FFH footnote present in `test-selection.md`; ZERO new codes minted | doc-presence + catalogue count | `python3 -m unittest tests.test_finding_catalogue_invariant -v` (stays 265 at Wave 1) + substring asserts | Wave 0 — new asserts |
| REQ-P19-04 | DSX-STA-090 fires on incomplete {method,seed,B,unit}, message names the missing member; silent on the complete quadruple | unit | `python3 -m unittest tests.test_resampling_gate -v` | Wave 0 — new |
| REQ-P19-05 | DSX-STA-100 fires on post-hoc ∉ omnibus family-map; silent on a matched pair; deprecated post-hocs never accepted | unit | `python3 -m unittest tests.test_posthoc_gate -v` | Wave 0 — new |
| REQ-P19-06 | DSX-STA-110 fires on variance test + (blank OR precondition role), silent on `scale_estimand`; DSX-STA-111 fires on `{observed,post_hoc}` only | unit | `python3 -m unittest tests.test_variance_role_gate -v` / `tests.test_power_reporting_gate -v` | Wave 0 — new |
| REQ-P19-07 | DSX-STA-120 fires on `wald` (n-independent); DSX-STA-121 on exposure+blank offset; DSX-STA-122 on nnt+blank nnt_ci | unit | `python3 -m unittest tests.test_proportion_count_gate -v` | Wave 0 — new |
| No-autoswitch (REQ-P18-06 doctrine) | Each `recommend_*` signature takes NO data/n/distribution flag | structural (`inspect.signature`) | `python3 -m unittest tests.test_declared_rm_trend_routing -v` etc. | Wave 0 — new |
| Catalogue mint proof | Live set = frozen snapshot ∪ four ∪ five Phase-18 ∪ ten Phase-19; total 275 | unit | `python3 -m unittest tests.test_finding_catalogue_invariant -v` | Extended |
| D-05 citation build gate (ten codes) | Each of the ten has a `Citation:` line, a `Structural criterion:`/`Reference value:` line, and a `# D-05: <CODE>` marker | build script | `python3 scripts/gen-finding-catalogue.py --check` | Extended — `_D05_ALLOWLIST_CODES` addition required |
| Fixture discipline | `good` fires none of the ten; `bad` fires all ten (19-C) | integration | `dsx audit --spec examples/good-ANALYSIS-SPEC.yaml` / same for `bad` | good pre-existing (verify silent); bad extended |

### Sampling Rate
- **Per task commit:** the single new test module the task touched, plus
  `python3 -m unittest tests.test_finding_catalogue_invariant -v` on any task that
  adds a `report.add(...)` call site.
- **Per wave merge:** `python3 -m unittest discover -s tests -q`. Wave 1 asserts
  catalogue == 265; Wave 2 asserts == 275.
- **Phase gate:** `scripts/gen-finding-catalogue.py --check` (catches a missing
  `_D05_ALLOWLIST_CODES` entry AND a stale `finding-codes.md`) + the good/bad
  fixture smoke test, before `/gsd-verify-work`.

### Wave 0 Gaps
- [ ] `tests/test_declared_rm_trend_routing.py` — no-autoswitch for `recommend_rm`/`recommend_trend`/`recommend_variance_role`
- [ ] `tests/test_declared_resampling_posthoc_routing.py` — no-autoswitch for `recommend_resampling`/`recommend_posthoc`/`recommend_power`/`recommend_proportion_ci`
- [ ] `tests/test_rm_sphericity_gate.py`, `test_trend_gate.py`, `test_resampling_gate.py`, `test_posthoc_gate.py`, `test_variance_role_gate.py`, `test_power_reporting_gate.py`, `test_proportion_count_gate.py` — the seven gate helpers
- [ ] `tests/test_finding_catalogue_invariant.py` extension — 265→275, +10 minted, method rename, docstrings
- [ ] `scripts/gen-finding-catalogue.py` `_D05_ALLOWLIST_CODES` addition — build-gate prerequisite for the D-05 checks to mean anything
- [ ] No framework install — stdlib `unittest` confirmed working (baseline `--check` green this session)

## Security Domain

`security_enforcement` is enabled in `.planning/config.json` (Phase 17/18
assessment), so this section is required even though the threat surface is thin —
matching the 19-CONTEXT.md persona round's decision NOT to engage the Auditor lens
(declaration-only, no data path, no leakage/security surface).

### Applicable ASVS Categories
| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | No auth surface in this local CLI/library |
| V3 Session Management | No | No session concept |
| V4 Access Control | No | File-based CLI, no access-control surface |
| V5 Input Validation | Yes, extended | Seven+ new closed-vocabulary/presence guards added, following the exact-normalize-equality idiom (`normalize(value) not in vocab`, no fuzzy/prefix match); presence gates use `is_blank` |
| V6 Cryptography | No | No cryptographic operation |

### Known Threat Patterns for this stack
| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| A closed-vocabulary check implemented as substring/fuzzy match, letting an adjacent value pass | Tampering (of the validation contract) | Exact `normalize(value) not in vocab` equality only; presence gates use `is_blank`, never truthiness on a structured value |
| DSX-STA-081 written as membership instead of `is_blank`, false-blocking a declared `none` | Denial of validation | `is_blank` predicate (Pitfall 5); `none`/`independent` are non-blank and satisfy |
| A new gate silently exempted from the D-05 build gate because `DSX-STA-` is not a prefix | Repudiation (a code ships uncited, build reports nothing) | Add the ten codes by exact name to `_D05_ALLOWLIST_CODES` (Pitfall 3) |
| Regenerated `finding-codes.md` committed out of sync with the real `report.add` sites | Tampering (docs drift from behaviour) | `gen-finding-catalogue.py --check` as a build gate |
| A fabricated numeric locator/boundary for a D-07 not-in-hand item (Hamed-Rao lag, BCD n≤40, Campbell count, M&N §6.2, Hayter α, GG ε) | Tampering (false authority) | Presence-only gates; ship these as named catalog-only rows with "confirm-at-source"/"not-in-hand" language, never a numeric boundary |

This phase introduces no new attack surface (no network call, no new
deserialization beyond the existing YAML loader used unchanged, no new file write
path beyond the existing catalogue-regen, no subprocess, no secret).

## Sources

### Primary (HIGH confidence — read directly from the live tree this session)
- `dsx/checks/stats.py` — full read (797 lines): `_MEMBERSHIP_FIELDS` (40-44),
  `CORRELATION_FAMILY`/`_ASSOCIATION_ROUTES` (49-73), `PARAMETRIC_TESTS`/
  `NONPARAMETRIC_TESTS` (76-84), `recommend_test` (90-191), `recommend_association`
  (194-213), `check()` with both dispatch call sites (219-248, `_check_declared_advanced_stats`
  insertion points at 231 and 247), `_check_declared_test` (528-630, incl. the
  membership loop 544-555 and the outcome_type early-return 557-560),
  `_check_declared_association`/`_check_correlation_scale_kind`/`_check_agreement_completeness`
  (633-797) — the exact split precedent Phase 19 mirrors
- `dsx/spec.py` — targeted reads: ICC/kappa/operand sub-vocabs (438-454, the
  Phase-18 additive-vocab precedent + comment style), `_VOCABULARIES` registry
  (620-659), `ESTIMAND_KINDS` confirmed six members (398-423, no scale member —
  Pitfall 6)
- `dsx/mathx.py` — targeted read (290-428): `EFFECT_SIZE_KINDS` (296),
  `REPORT_ONLY_EFFECT_KINDS` (341, `kendalls_w` present), `KAPPA_BANDS` (354),
  `KRIPPENDORFF_REFERENCE` (373), `CONVENTION_CATALOG` (383, `kendalls_w`
  catalog-only), `label_convention_band` (409) — the 19-B evidence
- `scripts/gen-finding-catalogue.py` — full read (484 lines):
  `_D05_ALLOWLIST_PREFIXES` (87-89, no `DSX-STA-`), `_D05_ALLOWLIST_CODES` (168-178,
  the Phase-18 block precedent at 157-167), `check_d05` (360-390),
  `_resolve_docstrings` per-enclosing-function (303-342), `collect` walking
  `dsx/**/*.py` only (250-267)
- `tests/test_finding_catalogue_invariant.py` — full read (148 lines):
  `_EXPECTED_TOTAL` (36), `_SNAPSHOT_TOTAL` (42, byte-frozen 256), `_MINTED_CODES`
  (43-46), both test bodies, method name `_stays_at_265_codes` (59), CRLF-safe
  regexes (50/55)
- `references/test-selection.md` — structure read: Decision table (6-24),
  Association/agreement section (65-126), the `Status`-column pointer-rows table
  (96-101) that Phase-19's DEPRECATED/pointer rows extend
- `examples/good-ANALYSIS-SPEC.yaml` (`analysis.test: two_proportion_z`) and
  `examples/bad-ANALYSIS-SPEC.yaml` (`analysis.test: welch_t`) — both read in full;
  confirmed silent on all ten Phase-19 predicates
- `dsx/frame/prereg.py` — grep confirmed "test-selection" appears only in prose
  docstrings (3, 308), NOT as a file parse — DEPRECATED rows are doc-only
- `.planning/REQUIREMENTS.md` — REQ-P19-01…07 read in full (72-105)
- `.planning/phases/19-.../19-CONTEXT.md` — read in full (D-01…D-08, HQ-22, D-13
  deferrals)
- `.planning/phases/18-.../18-RESEARCH.md` — read in full as the structural
  template
- Live shell: `python3 scripts/gen-finding-catalogue.py --check` → "finding
  catalogue is current" (baseline 265; three legacy declared-twice warnings, none
  Phase-19)

### Secondary (MEDIUM confidence)
- None — no web research performed. Every claim is checked against the live tree.
  The row-level statistical citations (Greenhouse-Geisser, Cochran-Armitage,
  Hamed-Rao, Davidson-MacKinnon, Efron, Games-Howell, Hayter, Zimmerman,
  Hoenig-Heisey, Lakens, Brown-Cai-DasGupta, Newcombe, McCullagh-Nelder, Campbell,
  Wilson) are the operator-answered HQ-17 pack referenced in 19-CONTEXT.md D-07;
  this research verifies WHERE and HOW the code consumes them, not the underlying
  literature.

### Tertiary (LOW confidence)
- None.

## Metadata

**Confidence breakdown:**
- Live-tree locators (paths, line numbers, function names, constants): HIGH —
  every one read directly this session on branch `gsd/v2.3.0-test-catalog`.
- D-05 build-gate mechanism + the `_D05_ALLOWLIST_CODES` requirement + the
  per-function docstring split: HIGH — mechanism fully read; the Phase-18 block is
  an unambiguous precedent.
- The 19-B verdict (no new band): HIGH — the mathx.py surface and the REQ-P19 text
  were both read directly; Kendall's W is provably already catalog-only.
- Declared-field NAME recommendations (the ten gates): MEDIUM — SHAPES are fixed
  by D-03; NAMES are this session's reasoned proposals, flagged as Open Questions
  for the planner to bind, not asserted as settled. The resampling-`unit` reuse
  call (OQ-4) and the estimand_kind scale-exemption (OQ-6) are the two
  highest-judgment items.
- Statistical citations: inherited from 19-CONTEXT.md's operator-answered HQ-17
  pack — not independently re-verified (out of scope; this session verifies
  code/doc mechanics).

**Research date:** 2026-09-02
**Valid until:** a point-in-time read of the tree immediately after Phase 18
closed (`ef907f8` head this session). Re-verify the exact line numbers in
`dsx/checks/stats.py`, `dsx/spec.py`, `scripts/gen-finding-catalogue.py`, and
`tests/test_finding_catalogue_invariant.py` immediately before executing if any
further commit lands on `gsd/v2.3.0-test-catalog` touching them between this
research and Phase 19 execute.
