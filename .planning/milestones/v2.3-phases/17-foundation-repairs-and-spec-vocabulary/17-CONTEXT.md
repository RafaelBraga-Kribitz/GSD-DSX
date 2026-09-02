# Phase 17: Foundation — repairs and spec vocabulary — Context

**Milestone v2.3 Test Catalog · S1-1 discuss · 2026-08-29.** The foundation phase.
Everything Phases 18–20 read is decided here: the `estimand_kind` routing vocabulary,
the D-12a paradigm-disposition table for every downstream gate, and the D-06 code-range
pre-allocation that later phases draw from. Requirements: REQ-P17-01 … REQ-P17-05 (5).
Phase 17 **mints zero new codes** (REQ-P17-05); it fixes the live Boschloo divergence,
adds a declared vocabulary, and writes down the decisions the later phases execute against.

## Phase Boundary

Foundation repairs + one new **declared, non-blocking** vocabulary + two recorded
decision tables (dispositions, range pre-allocation). Nothing here computes on data or
touches the gate path with pandas/scipy/numpy (D-01/D-02). The catalogue stays byte-frozen
at **260 codes** (the S0-2 re-measured baseline); the set-identity diff is the phase-end
gate (REQ-P17-05). `estimand_kind` is additive to the `analysis:` block, absence allowed,
never blocking on its own (D-10 style). Both canonical fixtures are **extended, not
replaced** (D-08).

## Persona round (LOOP-BRIEF §4)

Architect (`dsx-analysis-architect`) + Statistician (`dsx-statistician`), both opus/high,
concurrent — the two relevant personas for a statistical, vocabulary-and-disposition
spec-shape phase (the Auditor lens is not engaged: no security/leakage surface in a
declared-vocabulary discuss). Tie-break **rigour > reliability > flexibility**. The round
was run inline by the orchestrator (opus/high) as tightly-scoped parallel spawns fed the
S0-verified ground truth, rather than blind-exploring — the unit is a single artifact that
must complete in one firing without mid-unit compaction (brief §1).

The round **converged unanimously** on: adding a 6th `estimand_kind` member
(`nominal_association`), the shape of the disposition table, the observed-power ban shipping
(not deferred) with its Bayesian sibling named-and-deferred, and the decade-per-category
range scheme. It **split on one call — whether to rename `estimand_kind` off the "estimand"
stem** — resolved by the orchestrator below (keep the name; answer the concern structurally).

### The decision, stated plainly

- **`estimand_kind`** — a closed **6-member** vocabulary on the `analysis:` block:
  `linear_association`, `monotone_association`, `nominal_association`, `agreement`,
  `method_comparison`, `ordered_trend`. Declared-only, absence non-blocking, read by
  `recommend_test` and the Phase-18 correlation gate. Ships with a closed-vocab membership
  guard so a mis-slotted value is a loud decidable error, not a silent no-op.
- **D-12a disposition table** recorded for all nine Phase 18/19 gate checks (below): eight
  ship paradigm-neutral / self-scoping; the observed-power ban ships with its Bayesian
  sibling (post-hoc Bayes-factor "power") **named and D-13-deferred**.
- **D-06 range pre-allocation** — one DSX-STA decade per thematic category, 050–129, 130s
  reserve; monotone, collision-free, keyed to the re-measured live count (260).
- Catalogue stays **260** (zero new codes this phase); Boschloo doc/code reconciled and
  pinned; `time_to_event` fallthrough position pinned by regression test.

## Decisions (loud, vetoable — LOOP-BRIEF §4; veto window filed as HQ-18, silence = accept)

**D-01 — `estimand_kind` vocabulary name and members (REQ-P17-02).** Field name kept as
`estimand_kind` on the `analysis:` block. Closed 6-member name→description set:

| Member | Routes (Phase 18/19 rows) | Estimand character |
|---|---|---|
| `linear_association` | Pearson, point-biserial | signed, slope-like; Pearson r incl. dichotomous-continuous |
| `monotone_association` | Spearman, Kendall tau-b | signed, rank-monotone |
| `nominal_association` | phi (2×2), Cramér's V (r×c) | **unsigned**, chi-square-based departure-from-independence |
| `agreement` | Cohen/weighted/Fleiss kappa, Krippendorff α, ICC | dimensionless chance-corrected agreement index |
| `method_comparison` | Bland-Altman | bias + limits-of-agreement, in measurement units |
| `ordered_trend` | Cochran-Armitage, Jonckheere-Terpstra, Mann-Kendall + Sen | trend across an ordered factor |

- **Why 6, not the requirement's minimum 5 (both personas, unanimous, rigour tier).**
  REQ-P17-02 says "covering **at least**" the five — the addition is within the requirement's
  own grant, additive, not a rewording (so a persona decision recorded loudly, not a scope
  escalation). The Statistician's carve is load-bearing: **Cramér's V / phi on unordered
  r×c is an unsigned dependence measure with no slope and no direction — it is not a Pearson
  r.** Folding it into `linear_association` (a signed, slope-like quantity) mis-carves the
  estimand space and would let the Phase-18 correlation scale/kind gate wave through a
  nominal×nominal "correlation." `point-biserial` and continuous Pearson stay in
  `linear_association` (both are genuinely Pearson r on {0,1}-coded / continuous data).
- **Why keep the name `estimand_kind` (orchestrator, resolving the split).** The Architect
  voted to rename off the "estimand" stem (proposed `relationship_kind`) on the rigour ground
  that `estimand_type`/`estimand_kind` are English synonyms authors will mis-slot. Rejected
  as drafted for two reasons: (1) `relationship_kind` is itself a misnomer — `agreement` and
  `method_comparison` are precisely **not** relationships/associations (that distinction is the
  whole point of the Phase-18 gate that blocks correlation-for-an-agreement-estimand); (2) the
  name is inherited scope — REQ-P17-02, the Phase 18/19 requirements, and both D-05 packs
  (HQ-16/HQ-17) all say `estimand_kind`, so a rename is cross-file churn for a worse label.
  The mis-slot concern is answered **structurally, not by a rotting note**: the two axes live
  on different blocks (`analysis.estimand_kind` vs `validity_frame.estimand.type`) and never
  read from the same site (`recommend_test` reads the former; the admissibility adjudicator
  reads the latter), and **both ship closed-vocab membership guards** — the member sets are
  disjoint, so a swapped value (`estimand_kind: difference_in_means`, or
  `estimand.type: linear_association`) fails membership loudly (DSX-SPEC-082-style decidable
  error), never a silent no-op. That converts "silent structural mis-slotting" into a caught
  error, which is the rigorous resolution without the churn or the worse name. A loud
  orthogonality note ships in the code comment and the `dsx vocab` description regardless:
  **type = the causal quantity for admissibility; kind = the association/agreement form for
  test routing.** Absence stays non-blocking (D-10): `estimand_kind` is a routing hint, never
  a gate on its own.

**D-02 — D-12a paradigm-disposition table (REQ-P17-03).** Every gate planned for Phases
18–19, classified paradigm-neutral (ships), self-scoping (fires only on a declared
frequentist procedure that has no Bayesian counterpart — ships, no sibling to pair), or
paradigm-specific (ships paired, or defers with a falsifiable D-13 entry condition):

| Gate (req) | Check | Disposition | Ships |
|---|---|---|---|
| REQ-P18-03 | correlation scale/kind match | **paradigm-neutral** — measurement-scale + estimand-kind definition, holds under any paradigm | as-is |
| REQ-P18-04 | agreement declaration completeness (ICC (model,type,definition) triple; weighted-kappa declared weights; kappa companions per Feinstein-Cicchetti 1990) | **paradigm-neutral** — declaration completeness, interpretable under any paradigm | as-is |
| REQ-P19-01 | two-stage sphericity (Mauchly-then-correct) blocks; unconditional Greenhouse-Geisser required | **neutral doctrine / self-scoping** — the banned object is a two-stage pretest with no Bayesian counterpart; a Bayesian RM/covariance model has no Mauchly step | as-is |
| REQ-P19-02 | trend declared dose-scores / declared autocorrelation handling (Hamed-Rao 1998) | **paradigm-neutral** — a Bayesian trend model needs dose scores + autocorrelation handling too | as-is |
| REQ-P19-04 | resampling seed + B + unit + method quadruple | **paradigm-neutral** — reproducibility declaration; Bayesian bootstrap needs it equally | as-is |
| REQ-P19-05 | post-hoc matches declared omnibus family | **neutral coherence / self-scoping** — a declaration-matching consistency check | as-is |
| REQ-P19-06a | variance-test-as-precondition-to-location-choice blocks (Zimmerman 2004); scale-as-declared-estimand stays open | **paradigm-neutral (no-autoswitch doctrine) / self-scoping** | as-is |
| REQ-P19-06b | observed / post-hoc power in a readout blocks (Hoenig-Heisey 2001) | **paradigm-neutral / self-scoping** — rationale led by **power ≡ monotone f(p)**, uninformative under any paradigm; **Bayesian sibling named + D-13-deferred** (below) | as-is |
| REQ-P19-07 | Wald-interval-for-proportion blocks (Brown-Cai-DasGupta 2001); count-with-exposure-no-offset blocks | **paradigm-neutral** — recommended replacements span paradigms (Wilson is frequentist, **Jeffreys is Bayesian**); the offset is a rate-model necessity under any paradigm | as-is |

- **The observed-power ban's Bayesian sibling — explicitly dispositioned (REQ-P17-03's named
  requirement).** Sibling = a **post-hoc Bayes factor, or a posterior-based "probability of
  replication," presented as evidence of design adequacy / "power."** Same fallacy in Bayesian
  clothing (a post-hoc adequacy statistic computed from the same data that produced the
  result). Disposition: **D-13-deferred** with a falsifiable entry condition — *the sibling
  gate enters when the catalog gains a Bayesian post-hoc reporting surface for the gate to
  attach to.* This is **not** the asymmetric ban D-12 forbids: there is no Bayesian
  post-hoc-adequacy reporting surface in the catalog today to leave un-banned, so no live
  asymmetry exists; the sibling is named with a concrete trigger, not omitted. The sanctioned
  substitute — **MDE / sensitivity power analysis (Lakens 2022)** — is paradigm-neutral and
  ships as a positive catalog row.
- **Two rigour riders carried into Phase 19 (Statistician, adopted):**
  - **P19-06a citation scope.** Zimmerman 2004 tested **Levene-then-t in the two-group case**;
    the P19-06a gate spans k-group ANOVA (Brown-Forsythe/Bartlett are k-group variance tests).
    Citing Zimmerman alone for a k-group gate is citation-overreach. This is **already flagged
    in HQ-17 F1** — Phase 19 must either add a k-group authority or scope the cited claim to
    the two-group case with an explicit principled-extension flag. Recorded so Phase 19's D-05
    bar is bound to it.
  - **P19-01 alternative route.** The unconditional-GG requirement and its two-stage block fire
    only on a **declared frequentist RM-ANOVA plan**. The **mixed-model and GEE pointer rows**
    (REQ-P19-01) are the sanctioned alternative route to sphericity-robustness and are **not**
    touched by the gate — confirm at Phase 19 execute that the gate keys on the declared
    two-stage procedure, not on the presence of repeated measures.

**D-03 — D-06 code-range pre-allocation (REQ-P17-04; keyed to the re-measured live count
260).** All new gate codes are statistical → **DSX-STA-***. Current DSX-STA runs 001–043 in
tens sub-blocks (000s reporting-contract, 010s practical-sig, 020s null-acceptance, 030s
multiplicity, 040s declared-test-match). Pre-allocation, **one decade per thematic category**
(Architect's rider: anchor the block's meaning to the theme, not the mutable REQ-ID — codes
are permanent under D-06 while requirement IDs churn):

| DSX-STA range | Theme | Motivating req |
|---|---|---|
| 050–059 | correlation scale / kind match | REQ-P18-03 |
| 060–069 | agreement declaration completeness | REQ-P18-04 |
| 070–079 | RM sphericity / two-stage block | REQ-P19-01 |
| 080–089 | trend declared-field gates | REQ-P19-02 |
| 090–099 | resampling declaration quadruple | REQ-P19-04 |
| 100–109 | post-hoc ↔ omnibus-family match | REQ-P19-05 |
| 110–119 | negative gates (variance-as-precondition; observed-power) | REQ-P19-06 |
| 120–129 | proportion / count extras | REQ-P19-07 |
| 130–139 | reserve (Phase 20 calibration / overflow) | — |

- **Why decades, not tight packing (both personas, ACCEPT).** Address space is not scarce;
  predictability and parity with the existing tens sub-blocks (000s–040s) outweigh density.
  The densest foreseen block is 110–119 (variance-precondition + observed-power + the
  named-but-deferred sibling ≈ 3–4 codes) — comfortably ≤ 10. Phase 17 assigns **no** code
  from these ranges (REQ-P17-05); it reserves them so Phases 18/19 draw the next-free slot
  within the owning decade and no two phases collide.
- The **`time_to_event` fallthrough guard** (REQ-P17-04) is a Phase-17 *execute* task (S1-3):
  a regression test pins `recommend_test`'s unconditional final `return _rec("log_rank", …)`
  (stats.py:128-129) so a new outcome-type row cannot silently change routing. Not a code, so
  no range. Recorded here as the discuss binding for the plan.

**D-04 — Boschloo reconciliation shape (REQ-P17-01), confirmed for the plan.** The live
divergence (S0-2): doc says Boschloo (`references/test-selection.md:10` + footnote `[^1]`
Lydersen-Fagerland-Laake 2009), code emits `fisher_exact` (`stats.py:65`) and
`boschloo_exact` is absent from `NONPARAMETRIC_TESTS` (`stats.py:23-26`). Direction of the
fix — **reconcile to the doc** (`recommend_test`'s small-expected-cell fallback emits
`boschloo_exact`; `boschloo_exact` joins `NONPARAMETRIC_TESTS`), because the doc side carries
the cited authority (Lydersen-Fagerland-Laake 2009 §9: Boschloo dominates Fisher on power
while holding size) and Boschloo is the more powerful exact test. A **pinned regression test**
locks doc and code so this divergence class cannot recur silently — the structural, permanent
prevention (the general doc/code agreement test is REQ-P20-04; this is its Boschloo-specific
down payment). Adds **no new code** — `boschloo_exact` is a test-name string in the routing
table, not a DSX-STA finding code.

## What Phase 17 execute (S1-3) is now bound to

1. Boschloo reconciliation + pinned regression test (D-04).
2. `estimand_kind` 6-member closed vocab on `analysis:`, additive to `ANALYSIS-SPEC.yaml`,
   membership guard, `dsx vocab` dump, orthogonality note vs `estimand_type` (D-01); both
   canonical fixtures **extended** with an `estimand_kind` line (D-08), neither replaced.
3. `time_to_event` fallthrough-position regression test (D-03).
4. D-06 range note committed (this file's D-03 table is that note).
5. Phase-end: catalogue set-identity diff proves **260 → 260**, zero new codes (REQ-P17-05).

## Open questions / carried caveats

- **HQ-18 (veto window, non-blocking):** the D-01 6th member (`nominal_association`) and the
  D-03 range pre-allocation. Silence = accept; nothing blocks on it.
- **HQ-17 F1 (Zimmerman two-group scope)** binds Phase 19's P19-06a citation — recorded in
  D-02.
- No D-05 read is owed *by Phase 17*: the Boschloo citation (Lydersen-Fagerland-Laake 2009)
  is an existing, already-shipped doc footnote, not a new gate citation.
