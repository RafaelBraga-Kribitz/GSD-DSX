# Phase 19: RM, trend, categorical, resampling, post-hoc — Context

**Milestone v2.3 Test Catalog · S3-1 discuss · 2026-09-02.** The largest catalog phase
(7 requirements, REQ-P19-01 … REQ-P19-07). Phases 17 (foundation) and 18 (correlation /
agreement) are CLOSED: the `estimand_kind` 6-member vocabulary, the D-12a paradigm
dispositions for **every** Phase 19 gate, the D-06 code-range pre-allocation (070–129 for
the Phase 19 decades), and the operator-answered HQ-17 D-05 pack (16 citations) are all
committed and now binding. Phase 19 spends six pre-allocated decades, adds the RM / trend /
categorical / resampling / post-hoc / proportion-count rows keyed on DECLARED fields, and
mints **ten** new blocking codes. Catalogue **265 → 275**.

## Phase Boundary

Declaration-only routing surface, exactly as Phases 17–18 (D-01/D-02): every new check
compares DECLARED strings/structures in `ANALYSIS-SPEC.yaml`; nothing computes on data or
touches the gate path with pandas/scipy/numpy. Every gate keys on a declared field —
never on data inspection (the anti-two-stage invariant, extended per REQ-P18-06 doctrine
to this category). Both canonical fixtures are **extended, not replaced** (D-08). Any
effect-size bands ship as **labeled conventions, never blocking thresholds**. Codes are
permanent (D-06): the numbering below is load-bearing. **REQ-P19-03 (categorical) mints
zero gate codes** — it is rows + one DEPRECATED row + pointer rows (see D-01).

## Persona round (LOOP-BRIEF §4)

Architect (`dsx-analysis-architect`) + Statistician (`dsx-statistician`), both opus/high,
concurrent — the two relevant personas for a statistical, routing-and-gate spec-shape phase.
The Auditor lens is **not** engaged: the ten gates are declaration-only string/structure
comparisons with no data path, no leakage surface and no security surface (same reasoning as
17/18-CONTEXT.md). Tie-break **rigour > reliability > flexibility**. The round was run by the
orchestrator (opus/high) as tightly-scoped parallel spawns fed the S0/S1/S2-verified ground
truth (the Phase-17 D-06 ranges + D-12a dispositions, the Phase-18 routing/gate/lockstep
pattern, and the operator-answered HQ-17 D-05 pack), rather than blind-exploring — the unit is
a single decision artifact that must complete in one firing without mid-unit compaction (brief §1).

The round **converged** on: ten new HIGH codes across six decades; REQ-P19-03 minting none
(the absent decade is the deliberate tell); the DEPRECATED-row mechanism as doc-only routing-off;
the Zimmerman two-group scope-and-flag; the declared-field shapes; and the pin-vs-catalog-only
D-05 dispositions. It **split on one call — whether CMH-with-declared-stratification is a gate**
(Statistician: yes, a Simpson's-paradox completeness gate; Architect: no, a non-blocking row) —
resolved by the orchestrator below (row-only this phase; the stratifier concern named as a
falsifiable D-13 deferral).

### The decision, stated plainly

- **Ten new codes, all HIGH/blocking**, from the Phase-17 pre-allocated ranges:
  **DSX-STA-070** (two-stage sphericity), **080** (Cochran-Armitage without dose scores),
  **081** (Mann-Kendall without autocorrelation handling), **090** (resampling incomplete
  quadruple), **100** (post-hoc ≠ omnibus family), **110** (variance test as location-choice
  pretest), **111** (observed power in a readout), **120** (Wald interval for a proportion),
  **121** (exposure/time-at-risk with no offset), **122** (NNT without a CI). Catalogue 265 → 275.
- **Routing shape:** extend the Phase-18 pattern — dataless pure `recommend_*` functions +
  `_check_declared_*` gates sitting beside the untouched `recommend_test`, wired into `check()`;
  new rows in `references/test-selection.md` in lockstep; `references/finding-codes.md`
  regenerated in the same commit; new codes added to `_D05_ALLOWLIST_CODES` **by exact name**.
- **REQ-P19-03 categorical mints zero codes:** rows (N-1 chi-square, CMH, G-test, exact GOF)
  + one DEPRECATED row (Yates) + pointer row (log-linear) + one D-13 honesty footnote
  (Fisher-Freeman-Halton). The missing categorical decade corroborates this.
- **Zimmerman 2004 scoped to two-group + a principled-extension flag** for the k-group span;
  no unverified k-group authority pinned (Bancroft 1944 is a confirm-then-add backlog item).
- **D-05 dispositions honored:** almost nothing pins (the gates check declared-field PRESENCE,
  not computed statistics); pins are bibliographic locators + the Campbell / Hoenig-Heisey
  algebraic identities + the Newcombe A/B disambiguation. Everything else ships catalog-only /
  chapter-granular / not-in-hand per HQ-17.

## Decisions (loud, vetoable — LOOP-BRIEF §4; veto window filed as HQ-22, silence = accept)

**D-01 — The ten new codes and their D-06 numbering (REQ-P19-01/02/04/05/06/07).** All HIGH
(the "recognised-but-contradictory / incomplete declaration" class — the same class as the
HIGH DSX-STA-041/050/051/060/061/062; REQ language "blocks / must / mandatory" pins HIGH).
One code per explicit "Gate:/blocks" clause, split (not merged) because each failure mode has
a distinct remedy, distinct citation and distinct declared-field predicate under permanent D-06
numbering. Assigned next-free slot in the owning pre-allocated decade:

| Code | Sev | Range/theme | Fires when (DECLARED fields only; `is_blank` short-circuit then normalized membership) |
|---|---|---|---|
| `DSX-STA-070` | HIGH | 070–079 (P19-01) | a **two-stage sphericity procedure** (Mauchly-then-correct-if-significant) is DECLARED on an RM-ANOVA plan → route to unconditional Greenhouse-Geisser. Keys on the declared two-stage procedure, **not** the presence of repeated measures (D-06) |
| `DSX-STA-080` | HIGH | 080–089 (P19-02) | declared `test == cochran_armitage` **and** declared dose/scores field blank → trend undefined without monotone scores |
| `DSX-STA-081` | HIGH | 080–089 (P19-02) | declared `test ∈ {mann_kendall, sens_slope}` **and** declared autocorrelation-handling field blank (a declared `none`/`assessed: independent` **satisfies** the gate — force the declaration, never a correction; D-06) |
| `DSX-STA-090` | HIGH | 090–099 (P19-04) | a declared resampling procedure with an **incomplete** {seed, B, resampling-unit, method} quadruple (message names the missing member; one code, not four) |
| `DSX-STA-100` | HIGH | 100–109 (P19-05) | declared post-hoc **family ≠** declared omnibus family (declaration-matching only; membership tested against the acceptable family-map, like DSX-STA-041's `alternatives`) |
| `DSX-STA-110` | HIGH | 110–119 (P19-06a) | a variance/scale test declared with **role = precondition to a location-test choice** AND scale is **not** the declared estimand → block (Zimmerman; D-06). Undeclared role → block for declaration-incompleteness, not the Zimmerman reason |
| `DSX-STA-111` | HIGH | 110–119 (P19-06b) | **observed/post-hoc power** declared in a **readout** (power-reporting type ∈ {observed, post_hoc}) → block; a-priori/design and MDE-sensitivity types do not fire (narrow; D-06) |
| `DSX-STA-120` | HIGH | 120–129 (P19-07) | declared proportion-CI method == `wald` → route to Wilson/Jeffreys/Agresti-Coull (n-independent; the n≤40 cutoff is **not** hard-coded) |
| `DSX-STA-121` | HIGH | 120–129 (P19-07) | declared exposure/time-at-risk present **and** declared offset blank → count model needs the log-exposure offset |
| `DSX-STA-122` | HIGH | 120–129 (P19-07) | declared `nnt` row present **and** no declared CI / interval-method companion → NNT ships with its interval (completeness; D-06) |

Total new = **10**. Catalogue **265 → 275**. 071–079 / 082–089 / 091–099 / 101–109 / 112–119 /
123–129 stay free for later codes and the deferred riders below. This is a **D-06 persona
decision recorded loudly with a veto window (HQ-22), not a scope escalation** (brief §4).

**D-02 — Routing integration shape (REQ-P19-01/02/04/05/06/07).** Extend the Phase-18 hybrid
pattern verbatim: thin **dataless** pure `recommend_*` functions per family (returning the
acceptable-test/interval SET per declared context) + `_check_declared_*` gate functions sitting
**beside** the untouched `recommend_test`, wired into `check()` at both call sites. New rows
(incl. DEPRECATED + pointer rows) added to `references/test-selection.md` as the doc mirror,
lockstep with the code in the same commit. The dataless signatures are the mechanical
anti-two-stage proof (they take no data, no n, no distribution flag) — the no-autoswitch test
guards exactly those signatures, extended to the new families (REQ-P18-06 doctrine carried forward).

**D-03 — Declared-field shapes for the new gates (plan-time binds the exact field names;
shapes fixed here).** Reuse an existing declared field where one plausibly exists, else add an
additive, membership-guarded sub-vocab in `dsx/spec.py` `_VOCABULARIES` (a mis-slotted value
then fires the existing DSX-STA-040 for free — the Phase-18 mechanism). Absence non-blocking (D-10):

| Gate | Reads | Reuse / Add |
|---|---|---|
| 070 | RM sphericity-correction procedure ∈ {unconditional_gg, unconditional_hf, **two_stage/mauchly_conditional**, none} | Add sub-vocab |
| 080 | dose/scores declaration (presence; optional scheme ∈ {equally_spaced, midrank, custom}) | Add field (+ optional scheme sub-vocab) |
| 081 | autocorrelation-handling ∈ {none/independent, hamed_rao, prewhitening, …} — a declared `none` **satisfies** | Add sub-vocab |
| 090 | resampling **method** ∈ {permutation, percentile_bootstrap, bca}; **seed**; **B**; **resampling-unit** (the load-bearing member — cluster/block vs iid) | Reuse the analysis/randomization unit for resampling-unit; add method sub-vocab + seed/B presence |
| 100 | post-hoc family + omnibus family (+ the acceptable family-map) | Reuse the omnibus/test field if present; add post-hoc-family sub-vocab + family-map |
| 110 | variance-test **role** ∈ {precondition_to_location, scale_estimand}; the declared `estimand_kind` | Reuse Phase-18 `estimand_kind` for the scale exemption; add variance-test-role sub-vocab |
| 111 | power-reporting type ∈ {a_priori/design, **observed/post_hoc**, mde_sensitivity} | Add sub-vocab (mde_sensitivity is the Lakens-2022 sanctioned substitute row) |
| 120 | proportion-CI method ∈ {wilson, clopper_pearson, jeffreys, **wald**, agresti_coull} | Add sub-vocab |
| 121 | exposure/time-at-risk (presence) + offset (presence) | Add two presence fields |
| 122 | nnt (presence) + nnt-CI/interval-method (presence) | Add two presence fields |
| — (non-gated, P19-03) | CMH stratification; RD/RR/OR interval method (Newcombe/Woolf) | Add as surfaced declared fields, non-blocking (D-10) |

**D-04 — DEPRECATED routing-off row mechanism (REQ-P19-03/05/07).** Yates (P19-03), SNK +
unprotected-LSD-at-k>3 (P19-05), Vuong-for-zero-inflation (P19-07) ship as **doc-only rows in
`references/test-selection.md` flagged `status: deprecated` (routing-off), minting no code and
adding no blocking behaviour.** The pure `recommend_*` functions never select a deprecated row
as a default; **declaring one does not block** in Phase 19 (no gate keys on them — P19-03 has
no gate; P19-05's gate is family-match; P19-07's gates are Wald/offset/NNT). Structural
distinction: a **pointer row** (mixed-model/GEE, log-linear, ZIP/hurdle) is routing-neutral,
points **outward** to an out-of-detailed-scope method ("this route exists"); a **DEPRECATED
row** is routing-off, points at an **in-scope** method that should not be used, carrying a
"use X instead" redirect + the *why* citation (Yates→N-1 chi-square Campbell 2007;
SNK/LSD-k>3→protected post-hoc Hayter 1986 JASA 81(396):1000-1004; Vuong→misuse-finding **only**,
no replacement endorsed, Wilson 2015). Active deprecation enforcement (a
"declared-deprecated-method blocks" gate) is a **named D-13 deferral**, not shipped (below).

**D-05 — P19-06a Zimmerman two-group scope resolution (REQ-P19-06a; both personas, rigour tier,
load-bearing citation-integrity call).** Zimmerman 2004 (BJMSP 57(1):173–181) tested
**Levene-then-t in the two-group case only**; the DSX-STA-110 gate spans k-group ANOVA
(Brown-Forsythe/Bartlett/Fligner-Killeen are k-group scale tests). Citing Zimmerman alone for a
k-group gate is the citation-overreach this portfolio forbids above all. **Resolution: scope the
*cited empirical result* to two-group and attach an explicit principled-extension flag to the
k-group span** — `principled-extension: two-group→k-group; mechanism = a location test
conditioned on a data-dependent variance pretest distorts Type I error; mechanism is invariant
to group count; empirical k-group magnitude UNVERIFIED`. The gate does **not** need Zimmerman's
magnitude — the predicate is "variance test declared as a location-choice pretest → block," and
the *mechanism* (conditional inference after a preliminary test) is paradigm-general/textbook
(preliminary-test bias, tracing to **Bancroft 1944**, Annals Math Stat 15(2):190–204). Bancroft
1944 ships **not-in-hand / backlog**: recommended as the general k-group pretest-bias authority
**only after source-confirmation** (a candidate for a future D-05 addendum), never pinned
unverified. Rigour favours honest scoping + a flag over an unread citation.

**D-06 — Gate-predicate rulings (both personas; the over-block guards are the point).**
- **Two-stage sphericity (070)** keys on the DECLARED "Mauchly-then-correct-if-significant"
  procedure → block; it must **not** fire on the mere presence of repeated measures, else it
  false-blocks the legitimate mixed-model/GEE route (which never invokes a sphericity step). This
  is the P19-01 rider from Phase-17 D-02, confirmed.
- **Variance-precondition (110)** reads the DECLARED **role**: role = pretest/precondition to
  choose a location test → block (Zimmerman); role = scale/dispersion **is** the estimand →
  allow (the scale test is the correct primary analysis); role undeclared → block for
  declaration-incompleteness. Keys on the declared estimand-role, **not** on the presence of
  Levene/BF/Bartlett/Fligner — the Phase-18 point-biserial-whitelist lesson (don't false-block
  the legitimate case).
- **Observed power (111)** fires **narrowly**: blocks observed/post-hoc power declared in a
  readout as evidence about a result; routes design/sensitivity uses to the Lakens MDE-sensitivity
  row. Hoenig-Heisey's coverage of *all* post-hoc power uses is UNCONFIRMED at source, so a broad
  fire would over-block a legitimate "use this pilot's observed effect to plan the next study"
  declaration. **Broaden is a D-13 deferral** (enters when H&H is confirmed to cover all uses).
- **NNT (122) is a GATE** (completeness): a bare point NNT is active false precision — its
  sampling distribution is discontinuous (when the ARR CI crosses zero the NNT CI splits into
  NNTB/NNTH across an infinite discontinuity), so an interval is mandatory. Ships on the
  **internal completeness doctrine** (a point estimate ships with its interval — the same
  self-scoping class as the resampling quadruple and the ICC triple), exactly as Phase-18's
  DSX-STA-050 shipped on internal scale definitions. Altman-Deeks-Sackett 1998 (BMJ 317:1309–1312)
  is the **row-bibliography** citation confirmed at the Phase-19 execute row-bibliography pass —
  it is **not** a gate-code D-05 read owed at S3-1 (the gate mechanism does not need it). RD/RR/OR
  interval-method is a surfaced field, **not** gated (mandatory-CI symmetry is a D-13 deferral).
- **CMH-with-declared-stratification is NOT a gate this phase (orchestrator adjudication of the
  one persona split).** The Statistician's Simpson's-paradox reading (declaring CMH while pooling
  across un-named strata is a real error) is statistically correct, but REQ-P19-03 is the **only**
  requirement with **no "Gate:" clause and no pre-allocated decade**, and the same requirement
  family wrote an explicit gate clause for the exposure/offset case (REQ-P19-07) — the author
  deliberately did not for CMH. Minting a CMH gate would need a code from outside the theme-decade
  scheme (breaking committed D-06 discipline) and adds unrequested scope. CMH ships as a **row**
  surfacing a non-blocking declared stratification field; the stratifier concern is a **named D-13
  deferral** (below), not a silent drop (tie-break: the smaller provable claim + the honest named
  deferral over an unrequested gate that breaks the numbering).

**D-07 — D-05 dispositions: pin vs catalog-only (REQ-P19-01…07; both personas). Frame: the gates
check declared-field PRESENCE, not computed statistics — so almost nothing pins.** Pins are
confirmed bibliographic locators, algebraic identities, and the Newcombe A/B disambiguation;
everything doctrinal / chapter-level / house-convention ships catalog-only. The load-bearing
DO-NOT-HARD-CODE flags are called out:

| Citation | Disposition | Load-bearing flag |
|---|---|---|
| Greenhouse-Geisser 1959 Psychometrika 24(2):95–112 | PIN bib locator | ε is computed from data — never a fixture. NOT the reversed 1958 Annals paper. |
| Maxwell-Delaney 2004 ch.11–12 | CHAPTER-GRANULAR, catalog paraphrase | Access blocked → "GG over preliminary Mauchly" framed as the catalog's paraphrase, not a confirmed quote. |
| Hamed-Rao 1998 J.Hydrology 204(1–4):182–196 | PIN bib locator | **Do NOT hard-code the autocorrelation-significance lag threshold** — gate checks "handling declared," not the corrected variance. |
| Campbell 2007 Stat Med 26(19):3661–3675 | PIN the algebra χ²₍N−1₎ = χ²_Pearson×(N−1)/N, df unchanged; attribution "revalidated, not invented" (Egon Pearson originated N−1) | **Do NOT hard-code the smallest-expected-count ≥1 boundary** — confirm-at-source; not-in-hand. |
| Davidson-MacKinnon 2000 Econometric Reviews 19(1):55–68 | CATALOG-ONLY cited convention | Gate checks the seed+B+unit+method QUADRUPLE presence ONLY, never B's value. **Do NOT conflate 19/99 (exactness floor) with 399/1499 (recommended min)** — 19/99-as-floor under-powers. |
| Efron 1987 JASA 82(397):171–185 (BCa) | PIN bib locator; "house default" = house convention | **Do NOT attribute the acronym "BCa" to the 1987 text** (Efron-Tibshirani 1993). |
| Games-Howell 1976 J.Educational Statistics 1(2):113–125 | PIN bib locator, period-correct journal name | Don't anachronize ("...and Behavioral" is post-1994). "House default after Welch" is a later convention. |
| Hayter 1986 JASA 81(396):1000–1004 | CATALOG-ONLY + confirm-at-source (k=3 vs k≥4 boundary) | NOT the 1984 Annals paper. **Do NOT hard-code a numeric inflated-α.** |
| Zimmerman 2004 BJMSP 57(1):173–181 | PIN bib locator; finding catalog-only, two-group scoped | See D-05 (principled-extension flag; Bancroft 1944 backlog). |
| Hoenig-Heisey 2001 Amer.Statistician 55(1):19–24 | PIN the identity (observed power ≡ monotone f(p)); scope catalog-only | Gate breadth pending source-confirmation → fire NARROWLY (D-06). |
| Lakens 2022 Collabra:Psychology 8(1):33267 (CC-BY) | PIN bib locator; may quote his actual term "minimal statistically detectable effect" | **"MDE"/"minimum detectable effect" is the catalog's paraphrase — do NOT attribute it to Lakens.** |
| Brown-Cai-DasGupta 2001 Statistical Science 16(2):101–133 | PIN bib locator; Wilson/Jeffreys/Agresti-Coull recs catalog-only | **Do NOT hard-code the n≤40 cutoff (secondary-source only). Gate fires on "Wald declared," n-independent.** |
| Newcombe 1998 | **PIN both locators + the disambiguation**: Paper B = Stat Med 17(8):873–890 (SIM779, PMID 9595617) = **RD**; Paper A = 857–872 (SIM777) = single-proportion | Citation-lint MUST assert the full DOI to prevent A/B cross-wiring. Highest-value pin in the set. |
| McCullagh-Nelder 1989 offset | CHAPTER-GRANULAR "Ch.6 Log-Linear Models" | **Do NOT pin §6.2 (unconfirmed).** §6.3.2 pp.204–209 (MASS `ships` example) best-supported but prose unread → chapter only. Count-data gate needs no page. |
| Wilson 2015 Economics Letters 127:51–53 | PIN bib locator; misuse finding catalog-only | **DEPRECATED row states the misuse ONLY (null on the parameter-space boundary violates Vuong's interior-point prerequisite); claims NO replacement test.** |
| Altman-Deeks-Sackett 1998 BMJ 317:1309–1312 (NNT CI) | ROW-BIBLIOGRAPHY, confirm-at-execute (not a gate-code D-05 read) | DSX-STA-122 ships on internal completeness doctrine; Altman confirmed at the row-bibliography pass before it is printed (D-06). |

**D-08 — Single-writer wave split (REQ-P19 all; S3-2 plan preview; the load-bearing
architectural question the ledger says the discuss MUST confirm).** Phase 19 mints far more
codes than Phase 18 and they all append to the **same** single-writer files (`stats.py`,
`references/test-selection.md`, `references/finding-codes.md`), which have **no theme-disjoint
file-level decomposition** — themes cannot parallelize, they can only serialize across waves.
Recommended split: **two sequential waves, rows-then-gates**, with a conditional file-disjoint
bands plan parallel in Wave 1:

- **Wave 1 (parallel, file-disjoint):**
  - **19-A — rows / routing / vocab / doc.** Writers: `dsx/checks/stats.py` (all `recommend_*`
    pure functions, **no gate wiring**); `dsx/spec.py` (all new sub-vocabs); `references/test-selection.md`
    (all rows incl. DEPRECATED + pointer rows, doc-lockstep with the recommend functions);
    `references/finding-codes.md` regen (**stays 265** — rows/recommend/vocab mint no codes);
    the no-autoswitch tests for the new dataless signatures.
  - **19-B — bands (CONDITIONAL).** Writers: `dsx/mathx.py` (any report-only bands) +
    `templates/APA-TABLE-research.md` + band tests. File-disjoint (one semantic coupling: 19-A
    imports a frozenset from 19-B), exactly the 18-A/18-B shape. **Exists only if the row
    inventory surfaces a NEW report-only band that needs a home** (e.g. an RM/Friedman
    convention). Default expectation: Phase 19's requirements ask for **no** new mathx.py band
    growth (that was REQ-P18-05), so Wave 1 is likely **19-A alone** — the bands inventory is a
    plan-step call at S3-2.
- **Wave 2 (serial, single plan — created from live HEAD after Wave 1 merges):**
  - **19-C — gates + fixtures.** Writers: `dsx/checks/stats.py` (the 10 `_check_*` gate functions
    + wire into `check()` at both call sites); `dsx/spec.py` (`_D05_ALLOWLIST_CODES` += all 10
    codes **by exact name**); `references/finding-codes.md` regen (**→ 275**);
    `references/test-selection.md` (gate-code entries, gate-lockstep same commit);
    `examples/good-ANALYSIS-SPEC.yaml` + `examples/bad-ANALYSIS-SPEC.yaml` (extended per D-08 —
    bad exercises all 10, good stays silent); the gate tests.

Single-writer proof — every shared file has **exactly one writer per wave**, and the waves are
sequential so `stats.py` (19-A then 19-C) is never concurrent:

| File | Wave 1 writer | Wave 2 writer |
|---|---|---|
| `dsx/checks/stats.py` | 19-A only | 19-C only |
| `dsx/spec.py` | 19-A only | 19-C only |
| `references/test-selection.md` | 19-A only | 19-C only |
| `references/finding-codes.md` | 19-A only | 19-C only |
| `examples/*.yaml` | — | 19-C only |
| `dsx/mathx.py` | 19-B only | — |
| `templates/APA-TABLE-research.md` | 19-B only | — |

Merge gates: Wave 1 asserts catalogue == **265** (unchanged), all `recommend_*` dataless
(no-autoswitch green), doc-lockstep holds; Wave 2 asserts catalogue == **275**, the D-05 citation
build passes (all 10 codes in the allowlist), the good fixture stays silent, the bad fixture
fires all 10, and `dsx validate` + `dsx gate plan` exit 0. **Fallback** (recorded, the planner's
call): a scaled one-wave 18-A/18-B shape (gates inside 19-A) is legal (single-writer still holds)
if the orchestrator judges 19-A↔19-C coordination overhead higher than the mega-plan risk;
rows-then-gates is preferred for the intermediate 265-checkpoint and because it freezes the
declared-field names before the fixtures are written against them. The final wave/plan
granularity is the S3-2 planner's binding; the plan-checker validates single-writer disjointness.

## What Phase 19 plan/execute (S3-2 / S3-3) is now bound to

1. Extend the Phase-18 routing pattern: dataless `recommend_*` + `_check_declared_*` gates beside
   `recommend_test`; new rows (incl. DEPRECATED + pointer) in `test-selection.md` in lockstep;
   `finding-codes.md` regen in the gate commit; new codes in `_D05_ALLOWLIST_CODES` by exact name (D-02).
2. Ten HIGH codes DSX-STA-070/080/081/090/100/110/111/120/121/122 with the exact declared-field
   predicates in D-01, the over-block guards in D-06 (070 keys on the declared two-stage procedure;
   110 on the declared role; 111 narrow; 081 accepts a declared `none`).
3. REQ-P19-03 categorical = rows + DEPRECATED (Yates) + pointer (log-linear) + Fisher-Freeman-Halton
   honesty footnote — **zero new codes** (D-01/D-04).
4. Zimmerman scoped to two-group + the principled-extension flag on the k-group span; Bancroft 1944
   not-in-hand backlog (D-05).
5. D-05 dispositions per D-07: pin bibliographic locators + the Campbell/Hoenig-Heisey identities +
   the Newcombe A/B disambiguation; everything else catalog-only / chapter-granular; no hard-coded
   numeric (DM 19/99-vs-399/1499, BCD n≤40, Campbell expected-count, M&N §6.2, Hamed-Rao lag threshold,
   Hayter α).
6. Catalogue set-diff proves 265 → 275 with exactly the ten new codes; both canonical fixtures stay
   silent on them (D-08); the no-autoswitch test covers every new family (REQ-P18-06 doctrine).
7. Single-writer wave split per D-08 (two-wave rows-then-gates + conditional 19-B; planner confirms
   at S3-2; plan-checker validates disjointness).

## Open questions / carried caveats

- **HQ-22 (veto window, non-blocking):** the D-01 code numbering (070/080/081/090/100/110/111/120/121/122).
  Silence = accept; nothing blocks on it.
- **Deferred riders (named D-13 entry conditions, not silent gaps):**
  1. **CMH-stratifier gate** — enters when a fixture demonstrates a CMH declaration pooling across
     un-named strata passing, OR the operator requests it (draws a code from the 130s reserve or a
     newly-allocated categorical decade).
  2. **Active deprecation enforcement** ("declared-deprecated-method blocks") — enters when the
     operator requests it or a production spec is observed declaring a deprecated method.
  3. **Observed-power broadening** ("all post-hoc power uses") — enters when Hoenig-Heisey is confirmed
     at source to cover all uses; ships narrow now.
  4. **Bancroft 1944 k-group Zimmerman authority** — enters when confirmed at source (a future D-05
     addendum candidate); ships now as the D-05 principled-extension flag.
  5. **NNT/RD/RR/OR mandatory-CI symmetry** — enters if the operator wants RD/RR/OR gated for a missing
     CI; ships NNT-only now (in-decade 120–129).
  6. **P19-06b Bayesian sibling** (post-hoc Bayes-factor "power") — **stands** as named + D-13-deferred
     (Phase-17 D-02); enters when the catalog gains a Bayesian post-hoc reporting surface.
  7. **Fisher-Freeman-Halton** honesty footnote — ships as the D-13-conditioned footnote/row ("no
     practical unconditional r×c test exists"), NOT a gate; enters when a validated practical
     unconditional r×c test with an implementation appears.
- **Row-bibliography D-05 confirm-at-execute items (not gate-code reads owed at S3-1):** the NNT CI
  citation (Altman-Deeks-Sackett 1998) and the row-level bibliographic citations for the non-gated
  rows (Friedman, Cochran's Q, Page's L, Jonckheere-Terpstra, Dunn, Nemenyi, Scheffé, Tukey/Kramer,
  Dunnett, Clopper-Pearson, Woolf, G-test, log-linear) are confirmed at the Phase-19 row-bibliography
  pass, per the granularity ruling (one human read per gate CODE; bibliographic citation per catalog
  ENTRY). Every gate CODE's citation (070–121) is in the operator-answered HQ-17 pack; 122 rests on
  internal completeness doctrine.
- **No new D-05 read is owed by Phase 19 to unblock S3-1:** HQ-17 (16 citations, REQ-P19-01…07) is
  answered. The Bancroft 1944 k-group enrichment and the Altman 1998 NNT row citation are the only
  not-in-hand items, and neither blocks a shipping gate CODE.
