# Phase 18: Correlation, association and agreement — Context

**Milestone v2.3 Test Catalog · S2-1 discuss · 2026-09-01.** The first catalog phase.
Phase 17 (foundation) is CLOSED: the `estimand_kind` 6-member vocabulary, the D-12a
paradigm dispositions, and the D-06 code-range pre-allocation are all committed and now
binding. Phase 18 spends the two pre-allocated correlation/agreement decades (050–059,
060–069), adds the correlation and agreement/reliability rows keyed on DECLARED
`estimand_kind`, and grows the effect-size **convention** vocabulary. Requirements:
REQ-P18-01 … REQ-P18-06 (6). Five new blocking codes mint here (catalogue 260 → 265).

## Phase Boundary

Declaration-only routing surface. Nothing here computes on data or touches the gate path
with pandas/scipy/numpy (D-01/D-02): every new check compares DECLARED strings/structures
in `ANALYSIS-SPEC.yaml`. The two new gates key on `estimand_kind` (already membership-guarded
by the existing DSX-STA-040) and on the declared test/agreement declarations — never on data
inspection (the anti-two-stage invariant, REQ-P18-06). Both canonical fixtures are **extended,
not replaced** (D-08). Effect-size bands ship as **labeled conventions, never blocking
thresholds** (REQ-P18-05). Codes are permanent (D-06): the numbering below is load-bearing.

## Persona round (LOOP-BRIEF §4)

Architect (`dsx-analysis-architect`) + Statistician (`dsx-statistician`), both opus/high,
concurrent — the two relevant personas for a statistical, routing-and-gate spec-shape phase.
The Auditor lens is **not** engaged: the two gates are declaration-only string comparisons
with no data path, no leakage surface and no security surface (same reasoning as 17-CONTEXT.md).
Tie-break **rigour > reliability > flexibility**. The round was run by the orchestrator
(opus/high) as tightly-scoped parallel spawns fed the S0/S1-verified ground truth (the live
`recommend_test`/gate structure, the Phase-17 D-01/D-06 bindings, and the operator-answered
HQ-16 D-05 pack), rather than blind-exploring — the unit is a single decision artifact that
must complete in one firing without mid-unit compaction (brief §1).

The round **converged unanimously** on: the 5-code split (two correlation + three agreement,
all HIGH), the dataless `recommend_association` routing shape as the mechanical anti-two-stage
proof, the p_pos/p_neg companion correction, the report-only effect-size KIND registry that
keeps conventions out of the blocking magnitude guard, and the pin-vs-catalog-only D-05
dispositions. It surfaced two additive-scope riders (ICC combination-coherence; a coefficient
typo guard) that the orchestrator **deferred** with falsifiable entry conditions below —
smaller provable claim over larger unrequested surface.

### The decision, stated plainly

- **Five new codes, all HIGH/blocking**, from the Phase-17 pre-allocated ranges:
  **DSX-STA-050** (Pearson/linear correlation declared against a declared-ordinal operand),
  **DSX-STA-051** (a correlation coefficient declared for an `agreement`/`method_comparison`
  estimand — routes to kappa/ICC/Bland-Altman), **DSX-STA-060** (ICC without the full declared
  (model, type, definition) triple), **DSX-STA-061** (weighted kappa without declared weights),
  **DSX-STA-062** (kappa without its declared p_pos/p_neg companions).
- **Routing shape:** a new dataless pure function `recommend_association(estimand_kind)` +
  a new gate `_check_declared_association`, both beside the untouched `recommend_test`; a new
  Association/agreement section in `references/test-selection.md`. The dataless signature *is*
  the anti-two-stage proof (REQ-P18-06).
- **Effect-size growth is report-only:** the new agreement/correlation kinds are *recognised*
  (no false DSX-STA-012 nag) but the blocking magnitude guard (DSX-STA-011 via
  `mathx.interpret_effect`) keeps its domain at `{d, h, r}`. Bands ship as labeled conventions
  in the ungated APA template — conventions never block, enforced structurally.
- **D-05 dispositions honored:** Krippendorff α = **0.7598 (ordinal)** pinned (HQ-16 correction);
  kappa (Landis-Koch) bands pinned-and-convention-labelled; ICC (Koo-Li) bands and Kendall's W
  bands **catalog-only** (values unconfirmed / no citation exists); dCor, partial correlation,
  Cronbach→omega are catalog/pointer rows only.

## Decisions (loud, vetoable — LOOP-BRIEF §4; veto window filed as HQ-20, silence = accept)

**D-01 — Routing integration shape (REQ-P18-01/02/06).** A **hybrid**, not a fold-in and not
gate-only. Add a thin **dataless** pure function `recommend_association(estimand_kind: str) ->
{tests, effect_size, citation}` returning the *acceptable-coefficient SET* per `estimand_kind`
(`linear_association` → {pearson_correlation, point_biserial}; `monotone_association` →
{spearman_correlation, kendall_tau_b}; `nominal_association` → {phi, cramers_v}), plus a new gate
function `_check_declared_association(analysis, spec, report)` sitting beside `_check_declared_test`.
`recommend_test` is left **untouched**. A new "Association / agreement" section is added to
`references/test-selection.md` as the doc mirror (lockstep with the code, standing v2.3 rule).

- **Why hybrid, not fold-in (both personas, unanimous, rigour tier).** `recommend_test`'s
  signature already carries data-shape flags (`normal=`, `n_per_group=`, `overdispersed=`) and
  raises `ValueError` on an unknown `outcome_type`. Correlation/agreement have **no**
  `outcome_type`; folding them in would either pollute the closed `OUTCOME_TYPES` vocab or bolt a
  branch onto a switch keyed on a field they don't have — both endanger the working
  040/041/042/043 path. Gate-only was also rejected: it abandons the module's "derived, not
  chosen — `dsx recommend-test` returns the same table the gate checks" doctrine and leaves the
  new doc section with no programmatic mirror.
- **Why the dataless signature is the load-bearing point (REQ-P18-06).** `recommend_association`
  takes *no* data, *no* n, *no* distribution flag — it is a mechanically-verifiable string→set
  lookup, a **stronger** anti-two-stage guarantee than a branch of a function that already
  accepts data-shape arguments. The no-autoswitch test (P18-06) guards exactly this signature.
- **The gate membership-checks a SET, not one coefficient (Architect residual #4, adopted).**
  `monotone_association` legitimately admits *both* Spearman and Kendall; the gate tests the
  declared test against the acceptable set (like DSX-STA-041's `alternatives`), never forcing a
  single coefficient, so a legitimate Kendall-vs-Spearman choice is not over-blocked.

**D-02 — The five new codes and their D-06 numbering (REQ-P18-03/04).** All HIGH (they are the
"recognised-but-contradictory declaration" class — the same class as the existing HIGH
DSX-STA-041, not the MEDIUM DSX-STA-040 "unrecognised vocabulary" class; and REQ-P18-04's
"blocks at verify/ship" language pins HIGH, since MEDIUM does not block). Split rather than
merged because each failure mode has a **distinct remedy, distinct citation, and distinct
declared-field predicate**, and a merged code would emit the wrong remedy for half its firings
under permanent D-06 numbering. Assigned from the Phase-17 pre-allocated ranges, next-free slot
in the owning decade:

| Code | Sev | Range/theme | Fires when (DECLARED fields only; `is_blank` short-circuit then normalized membership) |
|---|---|---|---|
| `DSX-STA-050` | HIGH | 050–059 (P18-03) | declared linear-correlation test (`pearson_correlation`; not `point_biserial`) **and** a declared operand scale == `ordinal` with >2 levels → route to Spearman/Kendall (redeclare `monotone_association`) |
| `DSX-STA-051` | HIGH | 050–059 (P18-03) | declared primary test ∈ correlation family {pearson_correlation, spearman_correlation, kendall_tau_b, point_biserial, phi, cramers_v} **and** declared `estimand_kind` ∈ {`agreement`, `method_comparison`} → route to kappa/ICC/Bland-Altman |
| `DSX-STA-060` | HIGH | 060–069 (P18-04) | declared ICC (`test == icc` or `estimand_kind == agreement` with an ICC row) **and** any of `model` / `type` / `definition` blank or out-of-vocabulary (see D-05 for admissible values) |
| `DSX-STA-061` | HIGH | 060–069 (P18-04) | declared `test == weighted_kappa` **and** `weights` blank or ∉ {`linear`, `quadratic`, explicit matrix} |
| `DSX-STA-062` | HIGH | 060–069 (P18-04) | declared kappa (`test` ∈ {`cohens_kappa`, `weighted_kappa`, `fleiss_kappa`}) **and** declared `p_pos` OR `p_neg` companion missing (see D-04) |

050 and 051 are mutually exclusive by `estimand_kind` context, so no double-fire. 052–059 and
063–069 stay free for later correlation-scale / agreement codes (dCor/partial promotion under
D-13; Fleiss category-count; Krippendorff level-of-measurement; ICC combination-coherence — D-05).
This numbering is a **D-06 persona decision recorded loudly with a veto window (HQ-20), not a
scope escalation** (brief §4: numeric code assignments from the pre-allocated ranges are
persona-round decisions).

**D-03 — DSX-STA-050 point-biserial / dichotomous whitelist (REQ-P18-03; both personas,
non-negotiable rider, rigour tier).** A naive `test == pearson AND scale ∈ {ordinal, dichotomous}`
predicate would **false-block every legitimate point-biserial** — point-biserial *is* Pearson r
on a {0,1} dichotomy, and it lives in `linear_association` by Phase-17 D-01. So DSX-STA-050 fires
**only** when the declared operand scale is `ordinal` with **more than two levels**; declared
`point_biserial` and any declared-**dichotomous** (2-level) operand are whitelisted and never fire
050. The operand scale must be a **declared** field (anti-two-stage — never inferred from data,
absence non-blocking per D-10); the exact field shape is a plan-time binding for S2-2 — reuse an
existing declared measurement-scale field if `ANALYSIS-SPEC.yaml` already carries one, else add an
additive, membership-guarded one. Recorded so the planner writes the RED test with the whitelist
built in, not bolted on.

**D-04 — DSX-STA-062 companions are p_pos AND p_neg, not "raw agreement + prevalence"
(REQ-P18-04; both personas, blocking correction, rigour tier).** REQ-P18-04's parenthetical
paraphrases the kappa companions as "raw agreement + prevalence, per Feinstein & Cicchetti 1990."
The **operator-answered HQ-16 D-05 correction (2026-09-01, primary text read)** establishes that
the explicit reporting recommendation — "the omnibus κ should always be accompanied by separate
individual values of **p_pos and p_neg**" — lives in the companion **Part II** (Cicchetti &
Feinstein 1990, *J. Clin. Epidemiol.* 43(6):551–558), while Part I (43(6):543–549) states the two
paradoxes. Shipping the stale paraphrase would encode a **weaker, mis-attributed** gate — a
citation-integrity defect, which this portfolio's standard forbids above all else. Therefore
DSX-STA-062 requires the declared companions to be **p_pos AND p_neg** specifically, and the row
cites **both parts** (Part I for the paradoxes / *why*, Part II for the p_pos/p_neg recommendation).
This implements the requirement's **intent** (companion-reporting per Feinstein-Cicchetti) with the
operator's own corrected specifics — it is executing the answered D-05, not the loop rewording a
requirement on its own authority. The one-word requirement-parenthetical alignment
("prevalence" → "p_pos/p_neg") is offered to the operator **non-blocking in HQ-20** to prevent the
requirement and the gate from drifting (Statistician's flag); REQUIREMENTS.md is **not** edited
unilaterally this firing (a requirement reword is a §4-item-3 escalation; silence-accepts here
because the change is the operator's own answered correction).

**D-05 — ICC triple = presence + membership completeness only; combination-coherence deferred
(REQ-P18-04; orchestrator adjudication).** DSX-STA-060 fires on missing-or-out-of-vocabulary
sub-fields. Admissible declared values (Shrout & Fleiss 1979; McGraw & Wong 1996, corrected
edition — both confirmed at locator by HQ-16):

- `model` ∈ {`one_way_random`, `two_way_random`, `two_way_mixed`}
- `type` ∈ {`single`, `average`} (single vs average measures)
- `definition` ∈ {`consistency`, `absolute_agreement`}

The Statistician recommended an additional **coherence** rider (`one_way_random` ⇒ `definition`
must be `absolute_agreement`, since one-way-random has no rater effect to partial out for a
consistency ICC). Correct statistically, but it is a **different** gate (coherence, not
completeness) with its own citation burden and its own permanent code. REQ-P18-04 asks for
declaration **completeness**, which is provably presence + membership; coherence is additive
scope. **Deferred** to a falsifiable **D-13 entry condition**: *the ICC-combination-coherence
gate (candidate DSX-STA-063, in the 060–069 reserve) enters when a fixture demonstrates a
complete-but-incoherent triple passing DSX-STA-060.* Recorded so it is a named, triggered
deferral, not a silent omission (tie-break: the rigorous reading of "completeness" is
presence+membership; prefer the smaller provable claim).

**D-06 — Effect-size KIND handling: a report-only registry; the blocking band domain stays
`{d, h, r}` (REQ-P18-05; both personas, load-bearing firewall, rigour tier).** The existing
magnitude guard (DSX-STA-011 "negligible" / DSX-STA-012 "unrecognised kind" in `stats.py`) bands
`effect_size_kind` via `mathx.interpret_effect`, whose domain is `EFFECT_SIZE_KINDS =
frozenset({"d","h","r"})`. Do **NOT** add kappa / ICC / Kendall's W / phi / Cramér's V / tau-b /
rho to that frozenset. Two reasons it would be *wrong*: (1) it would make DSX-STA-011 adjudicate a
**convention** as a band boundary — violating REQ-P18-05's "never as blocking thresholds"; (2)
`interpret_effect` uses a flat `abs(value)` band, but **Cramér's V thresholds are df-dependent**
(Cohen's 0.1/0.3/0.5 hold only at df=1) and phi/W are unsigned with a different null — a single
flat band is statistically wrong. Instead, add a separate **report-only registry** that
DSX-STA-012 consults so a spec declaring `effect_size_kind: kappa` on a significant result is
*recognised* (no nonsensical "declare d/h/r" nag) but is **never banded by a blocking code**;
DSX-STA-012's remedy text branches (for report-only kinds: "magnitude is a labeled convention, not
a gated band"). The bands themselves live in `mathx.py` report-only tables and are wired only into
the **ungated** `templates/APA-TABLE-research.md` (which mints no finding code). This is REQ-P18-05's
"conventions never block" implemented structurally, not by discipline.

**D-07 — D-05 dispositions: pin vs catalog-only (REQ-P18-01/02/05; both personas).** A value is
pinned only if confirmed at source; otherwise catalog-only (brief §5):

| Item | Disposition | Basis |
|---|---|---|
| Krippendorff α = **0.7598 @ ordinal level** | **PIN** (reference value in the agreement fixture, never on the gate compute path) | HQ-16 B4 corrected, primary text read; MUST carry `level: ordinal` — the same data yields 0.4765/0.7574/0.6621 at nominal/interval/ratio |
| Kappa bands (Landis & Koch 1977, Biometrics 33(1):159–174) | **PIN values, label convention** | HQ-16 F1 values corroborated; edge-tie handling ships as a labeled convention choice, not claimed as the paper's exact wording |
| ICC bands (Koo & Li 2016) | **CATALOG-ONLY** (convention-labelled, never wired into any code) | HQ-16 F2: exact boundary VALUES unconfirmed at source → not a pinned band |
| Kendall's W bands | **CATALOG-ONLY, named only, no boundaries** | Statistician grep: **no band citation exists** anywhere in the repo or HQ-16 → a D-05 read is owed before any W band values ship |
| dCor, partial correlation | catalog/pointer rows only, **no numeric fixture** | REQ-P18-01 (D-13 entry conditions unmet) |
| Cronbach → McDonald ω | pointer/catalog-only with deprecation citations | REQ-P18-02 (a redirect row, not a routing target) |
| P18-03 doctrinal scale citation (scale ⇒ admissible correlation) | **block ships; external citation not-in-hand** | HQ-16 note: deliberately outside the pack, a Phase-18 binding. The block rests on the **internal** Phase-17 `estimand_kind`/scale definitions (self-scoping, paradigm-neutral); the external doctrinal citation is confirmed at the row-bibliography pass before it is printed — no fabricated locator |

**D-08 — Single-writer wave split (REQ-P18 all; S2-2 plan preview).** Two **file-disjoint**,
parallelizable plans, serialized only at the orchestrator's tracking-file merge:

- **Plan 18-A — routing + gates + doc/catalogue lockstep.** Writers: `dsx/checks/stats.py`
  (`recommend_association`, `_check_declared_association`, correlation/agreement token sets, wire
  into `check()`); `dsx/spec.py` (new closed sub-vocabs — ICC triple keys, kappa companion keys,
  coefficient tokens if any); `references/test-selection.md` (new Association section);
  `references/finding-codes.md` (**regenerated** via `scripts/gen-finding-catalogue.py`, not
  hand-edited — total 260 → **265**, in the SAME commit as the `report.add` calls); gate fixtures
  (D-08 extend-not-replace, both canonical fixtures stay silent); gate tests for
  050/051/060/061/062; the P18-06 no-autoswitch test guarding `recommend_association`'s dataless
  signature.
- **Plan 18-B — effect-size convention vocabulary (REQ-P18-05).** Writers: `dsx/mathx.py`
  (kappa/ICC/Kendall's-W report-only band tables + the report-only kind registry per D-06);
  `templates/APA-TABLE-research.md`; extend the existing effect-size / `interpret_effect` /
  DSX-STA-011/012 tests. Mints **no** DSX-STA code (bands are conventions), so it never touches
  `finding-codes.md` — no catalogue-regen contention with 18-A.
- File sets are disjoint → 18-A ∥ 18-B. The one coupling is **semantic**: 18-A's `stats.py`
  imports `EFFECT_SIZE_KINDS` from 18-B's `mathx.py`; that is single-source-of-truth by design and
  18-B owns the 011/012 test update. The hard doc+code+catalogue lockstep is satisfied *within*
  18-A.

## What Phase 18 plan/execute (S2-2 / S2-3) is now bound to

1. `recommend_association(estimand_kind)` (dataless) + `_check_declared_association` gate + the
   Association section in `references/test-selection.md`, in lockstep (D-01).
2. Five HIGH codes DSX-STA-050/051/060/061/062 with the exact declared-field predicates in D-02,
   the 050 point-biserial/dichotomous whitelist (D-03), and the 062 p_pos/p_neg companions (D-04).
3. ICC DSX-STA-060 = presence + membership over the enumerated (model, type, definition) values
   (D-05); combination-coherence deferred as candidate DSX-STA-063.
4. Report-only effect-size KIND registry; `EFFECT_SIZE_KINDS` stays `{d, h, r}`; DSX-STA-012 remedy
   branches; bands wired only into the ungated APA template (D-06).
5. D-05 dispositions per D-07: pin α=0.7598@ordinal and the Landis-Koch kappa bands; everything
   else (ICC bands, Kendall's W bands, dCor, partial, Cronbach→omega, the P18-03 doctrinal
   citation) ships catalog-only / not-in-hand until read.
6. Catalogue set-diff proves 260 → 265 with exactly the five new codes (no others); both canonical
   fixtures stay silent (D-08); the no-autoswitch test covers the new category (REQ-P18-06).

## Open questions / carried caveats

- **HQ-20 (veto window, non-blocking):** the D-02 code numbering (050/051/060/061/062) and the
  D-04 requirement-parenthetical alignment ("prevalence" → "p_pos/p_neg"). Silence = accept.
- **Coefficient-typo guard deferred (Architect residual #2 / Statistician).** A typo'd
  `analysis.test` coefficient (e.g. `"pearsons"`) matches no family and silently escapes all five
  new gates — the same tolerance the current design has for unknown test names (DSX-STA-041 only
  fires when it *can* derive a recommendation). Minting a whole test-name closed-vocab guard is a
  large permanent surface the requirements do not ask for. **Deferred, not adopted** — recorded as
  a candidate for a later phase / the 130s reserve, so it is a named decision, not a silent gap.
- **ICC combination-coherence deferred (D-05)** as candidate DSX-STA-063 with a falsifiable D-13
  entry condition.
- **D-05 not-in-hand for S2-3 (D-07):** ICC (Koo-Li) band values, Kendall's W bands (no citation
  exists), and the P18-03 doctrinal scale citation — all ship catalog-only / definition-backed
  until confirmed at locator. The McGraw & Wong 1996 erratum (HQ-16 C2) means any pinned ICC
  equation must be checked against the corrected version; the completeness gate is
  formula-independent so it ships regardless.
- No **new** D-05 read is owed *by Phase 18 to unblock S2-1*: HQ-16 is answered. The row-level
  bibliographic citations (Spearman/Kendall/point-biserial/phi; the P18-03 doctrinal scale
  citation) are confirmed at the Phase-18 row-bibliography pass during execute, per the granularity
  ruling (one human read per gate CODE; bibliographic citation per catalog ENTRY).
