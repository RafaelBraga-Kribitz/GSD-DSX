# Phase 22: Catalog spine, uncertainty family, selection heuristic — Context

**Milestone v2.4 Visual Excellence · S2-1 discuss · 2026-09-03 (autonomous firing).**
Phase 22 is the milestone's centre of gravity — it carries the D-05 citation load and
builds directly on Phase 21's reconciled 50-mark vocabulary (the every-mark-has-a-home
invariant guarantees the catalog's DSX-admissible rows are a closed, orphan-free set).
Requirements: REQ-P22-01 … REQ-P22-05 (5). **The HQ-27 D-05 pack is ANSWERED with four
binding operator decisions D-1…D-4** (`.planning/v2.4-D05-EVIDENCE-PACK.md`); this discuss
applies them as hard constraints, never re-opens them.

## Binding inputs (not decided here — recorded so execute honours them)

- **D-1 — perceptual rank axis.** The Cleveland–McGill (1984) ordering is **6 ranks over
  10 tasks WITH TIES**, not a 7-item strict order (p.536 for the list, p.537 for the tie
  caveat; Heer & Bostock p.206 independently declines `length > angle`). REQ-P22-05's
  structural-criterion test asserts `rank(a) <= rank(b)`, **never** a strict `<` across
  tied members. `density` is absent from the 1984 paper; `curvature`/`shading` are tied,
  not dropped. Shipping form: rank1 position_common · rank2 position_nonaligned · rank3
  {length, direction/slope, angle} · rank4 area · rank5 {volume, curvature} · rank6
  {shading, colour_saturation}.
- **D-2 — uncertainty vocabulary = Wilke's actual §5.6 ten marks**, each with a real
  locator: error bars · graded error bars · 2D error bars · confidence strips · eyes ·
  half-eyes · quantile dot plot · confidence band · graded confidence band · fitted draws.
  "fan chart" and "gradient CI band" do **not** exist in Wilke and must not ship. "eye"
  (violin+error bar) ≠ "half-eye" (ridgeline+error bar). Frequentist/Bayesian paradigm
  symmetry is genuinely supported (§16.2).
- **D-3 — FT Visual Vocabulary is NOT MIT for its content.** Attribute the nine-category
  function axis (link ft.com/vocabulary); write **all** descriptions ourselves; never
  vendor the poster PDF or copy its per-chart blurbs; drop any "exhaustive" claim resting
  on the FT (the poster disclaims exhaustiveness itself). The nine categories are confirmed
  exactly: Deviation · Correlation · Ranking · Distribution · Change over Time · Magnitude ·
  Part-to-whole · Spatial · Flow.
- **D-4 — `dual_axis_line` refusal** cites **"Muth 2018 (Datawrapper), as amended July
  2026"**, records the amendment, and scopes its reason string to a **general audience**
  (Datawrapper's carve-out is expert/finance users). Already applied in Phase 21's
  `BANNED_TYPES`; Phase 22's catalog refusal row must match verbatim.
- **Cross-cutting finding (binding on citation wording):** the "spine" sources are **one
  design lineage, not three independent authorities** — Ribecca authored **both** the
  Graphic Continuum and the Data Visualisation Catalogue, and the FT poster credits the
  Graphic Continuum as its inspiration. The catalog must **not** claim triangulation across
  FT/GC/DVC as independent corroboration. Genuine independence comes from Munzner's task
  taxonomy and Cleveland–McGill's encoding work (the catalog's *other* two axes).

## Phase Boundary

Ship (1) a merged, citable chart **catalog** as a new reference doc, (2) the **uncertainty
function family** entering the live vocabulary, (3) **faceting** as an orthogonal
declaration (not a chart type), (4) the **5-layer question→chart heuristic** as edits to
the existing taxonomy files, and (5) **gate extensions** with D-05 citations. Constraints
inherited from the milestone: stdlib-only gate path, no pandas/scipy/numpy on the gate
path (D-01/D-02); additive codes only against the **re-measured live 275 baseline** (D-06);
the perceptual tie-break is a **pure ordering assertion, no computation** (REQ-P22-05 +
D-1). The catalog is a **reference artifact**, not itself a gate check.

## Ground truth read this firing (assumptions mode)

Live structures read in full, catalogue count **re-measured three ways (not assumed)**:

- **Catalogue = 275 codes** — `references/finding-codes.md` Total line = 275; CRLF-safe
  unique `DSX-[A-Z]+-[0-9]+` grep = 275; `gen-finding-catalogue.py --check` = "current"
  (the 2 declared-twice VAL warnings are pre-existing, unrelated to VIZ). **D-06 baseline
  confirmed = 275.**
- **VIZ family codes (20):** 001, 010–014, 020, 021, 030, 040, 050–052, 060–064, 070, 080.
  Banded scheme. **Next-free in the 07x uncertainty band: 071–079** (070 = the existing
  `_check_uncertainty`, HIGH, "estimates without uncertainty"). Next-free elsewhere:
  002–009, 015–019, 022–029, 031–039, 041–049, 053–059, 065–069, 081+.
- **Live mark universe = 50 admissible marks** (Phase 21's closed set):
  `RELATIONSHIP_CHARTS` (36) ∪ `CHART_CAPABILITIES` (48) ∪ `EXTRA_MARKS` (10) minus the 5
  banned. Closed and orphan-free by `TestEveryMarkHasAHome` — this is the catalog's
  DSX-admissible spine.
- **`BANNED_TYPES` = 5 refusal records** `{reason, code, citation}` (Phase 21):
  3d_bar/3d_line/3d_pie/radar/dual_axis_line, all `code=DSX-VIZ-001`. `radar`'s citation is
  still the PROVISIONAL placeholder in `viz.py`; HQ-27 **replaced** it with Duan et al. 2023
  (J Clin Epidemiol 156:85–94) — execute must swap the string.
- **`_check_uncertainty`** (`viz.py:423`) already treats uncertainty as a **property**
  (`shows_estimates` + `shows_uncertainty` → DSX-VIZ-070). This is the *verification*
  surface; it is complementary to, not replaced by, the new *selection* surface below.
- **No `references/chart-catalog.md` exists** — REQ-P22-01 creates it. Existing reference
  docs to edit for REQ-P22-04: `references/question-taxonomy.md`, `references/chart-selection.md`.

## Persona round (LOOP-BRIEF §4)

**Architect** (`dsx-analysis-architect`) + **Statistician** (`dsx-statistician`) +
**Auditor** (`gsd-security-auditor` / `dsx-ml-integrity-auditor` lens), all opus/high, run
**inline** by the orchestrator against the re-measured ground truth (Phase-17/21 precedent:
a single artifact that must complete in one firing without mid-unit compaction — tightly
scoped inline deliberation over blind-exploring subagent spawns, and no subagent touches a
single-writer tracking file). Unlike Phase 21, the **Statistician IS engaged**: the
uncertainty family carries genuine statistical content (frequentist/Bayesian paradigm
symmetry, D-12a) and the perceptual-rank axis is an encoding-accuracy claim. Tie-break
**rigour > reliability > flexibility**. The round converged on GA-1…GA-3 below.

## Decisions (loud, vetoable — LOOP-BRIEF §4; veto window filed HQ-30, silence = accept)

<!-- Machine-readable decision index (format bridge for the context-coverage gate;
     decision CONTENT is in the authoritative ### bodies below). -->

- **GA-1 — catalog entry-set derivation & count (REQ-P22-01):** apply the ROADMAP's fixed
  method (synonym-merged union of the five named taxonomies minus principled exclusions —
  *do not re-litigate*); composition = **50 DSX-admissible marks + 10 uncertainty marks +
  the refusal rows + spine-attested reference-only rows**, sized to land the total in the
  **75–90 band** (target ~80). The DSX-admissible + uncertainty core (60) is frozen; the
  reference-only rows are the tunable remainder. Per-row 3-axis + citation enumeration is
  **execute (S2-3) work, plan-checker-verifiable**, not frozen here.
- **GA-2 — uncertainty vocabulary shape (REQ-P22-02):** an **11th `RELATIONSHIP_CHARTS`
  key `"uncertainty"`** carrying Wilke's 10 §5.6 marks — **not** new input-type ids. The
  property-based `DSX-VIZ-070` is retained as the complementary verification surface.
- **GA-3 — D-06 numbering (REQ-P22-05):** new gate codes take the **next-free 07x band**
  (`DSX-VIZ-071`, and `-072` if a second uncertainty check is warranted), assigned by the
  D-06 next-free rule against the **re-measured 275 baseline**; the exact count is pinned at
  plan (S2-2). REQ-P22-05's perceptual tie-break, faceting routing, and catalog↔vocabulary
  conformance are **repo-integrity tests off the gate path → zero code**.

### GA-1 — the merged catalog's entry set and count (REQ-P22-01)

**The derivation method is fixed by the ROADMAP scope boundary and is not re-opened:** the
catalog is the *"union of five named taxonomies (FT VV spine, Wilke, Graphic Continuum,
DVC, Datawrapper) after synonym merge and principled exclusions (3D, gauges, word clouds,
dual-axis — each cross-referenced to its banning code)."* This discuss **applies** it.

**Layered composition (Architect, count-anchored to the re-measured live tree):**

| Layer | Source | Count | Frozen? |
|---|---|---|---|
| DSX-admissible marks | Phase 21's closed 50-mark universe | 50 | yes |
| Uncertainty family | Wilke §5.6 (D-2), via the new `"uncertainty"` relationship | 10 | yes |
| Refusal rows | principled exclusions, each → its banning code + citation | ≥5 | see below |
| Spine-attested reference-only | FT/Wilke-ch.5/DVC types not (yet) in DSX's admissible set, own descriptions (D-3) | tunable | no |

Core (admissible + uncertainty) = **60**, below the band floor by design — the requirement
author set the 75–90 band *expecting* spine chart types beyond DSX's gate vocabulary (FT
has 66 distinct, DVC 60). Reaching the band by adding **reference-only rows** is faithful to
REQ-P22-01's intent, **not** a scope change: those rows are catalog reference entries
(attributed axis, our descriptions), explicitly flagged *reference-only, not in the DSX
admissible set*, so they never silently widen what the gate admits. Target ~80 ⇒ ~15
reference-only rows; the exact set is chosen at execute to fill genuine **function-coverage
gaps** across the nine FT categories, and the plan-checker verifies `75 ≤ total ≤ 90`.

**Refusal rows and the drift guard (Auditor, decisive).** The catalog's "principled
exclusions" must be **backed by live `BANNED_TYPES` entries** — a catalog row that claims a
refusal the gate does not enforce is exactly the drift surface Phase 21's doctrine forbids.
The 5 already-banned (3D×3, radar, dual_axis_line) are backed. **Gauges and word clouds are
named exclusions in the ROADMAP but are NOT yet in `BANNED_TYPES`** — so execute adds
`gauge` and `word_cloud` to `BANNED_TYPES` as `{reason, code, citation}` records with
`code=DSX-VIZ-001` (reusing the existing type-ban code → **zero new code**), citing HQ-27's
signed Tier-3 sources: **Few 2006 §3.2/§6.2.1.1** for gauges (grounds = wasted space /
missing context / unlabeled scale — *not* "arbitrary maximum", which HQ-27 marks as DSX's
own reasoning) and **Jacob Harris, Nieman Lab 2011** for word clouds (framed as
editorial/practice rationale, not a perceptual-encoding finding, per HQ-27). Refusal rows
then number **7**.

**Independence caveat carried into the citation column (per the cross-cutting finding).**
Where a reference-only row is attested only by the Ribecca lineage (GC and/or DVC and/or the
FT poster), the citation names them as **one lineage**, never as independent triangulation.
Counts are the HQ-27-corrected ones: DVC = 60 (not 77), FT = 66 distinct / 74 named (not
72), GC ≈ 90 *author-stated* (its primary page contradicts itself on group count). DVC URLs
are **resolved and stored at build time**, never auto-generated from names (`treemap.html`
has no underscore).

**Why reference-only rows rather than promoting all spine types into the gate vocabulary
(Architect + Auditor, rigour tier).** Promoting ~15 new marks into `RELATIONSHIP_CHARTS` /
`CHART_CAPABILITIES` would (a) balloon Phase 21's every-mark-has-a-home invariant with marks
that have no verified data-signature home, and (b) widen what the gate admits on the
strength of a *reference catalog* rather than a decided admissibility rule. Keeping them
reference-only is the honest smaller claim: the catalog documents them; the gate does not
silently start accepting them. Any later promotion is its own decided change.

### GA-2 — uncertainty vocabulary shape: 11th relationship key (REQ-P22-02)

**Chosen: add an 11th `RELATIONSHIP_CHARTS` key `"uncertainty"`** whose admissible-mark
tuple is Wilke's 10 §5.6 marks (D-2). Rippled across `viz.py` (the relationship tuple +
`_check_relationship_match` coverage), `input_types.py` narrowing, the skills/references
that enumerate relationships, and the catalog's function axis.

**Why (Architect + Statistician).** Uncertainty is the one function *"every poster taxonomy
lacks and a rigour project most needs"* (ROADMAP goal); Wilke's own directory (ch.5) lists
**Uncertainty as a peer top-level category**, so an 11th key is the paradigm-faithful
modeling. It gives every one of the 10 marks a **relationship home**, keeping Phase 21's
invariant satisfiable without exemptions. And it expresses **D-12a paradigm symmetry as one
function**: the Statistician confirms the §5.6 marks map symmetrically across the divide
Wilke draws in §16.2 — frequentist confidence intervals (error bars, graded error bars,
confidence strips, confidence band) and Bayesian posteriors (eyes, half-eyes, quantile dot
plots, graded confidence band, fitted draws) are **both** first-class, so the family is
D-12a-clean by construction rather than by a bolted-on check.

**Rejected: new input-type ids (Architect, decisive against).** Admitting the uncertainty
marks via `CHART_CAPABILITIES`/`EXTRA_MARKS` on new data-signature ids would scatter the
family across data families, lose the "uncertainty is a function" framing the milestone is
built to add, force more input-type churn, and make the frequentist/Bayesian symmetry an
emergent property of several families rather than a stated one. Lower rigour on the exact
axis the phase exists to strengthen.

**The property surface is retained, not replaced (Statistician).** `DSX-VIZ-070`
(`shows_estimates` without `shows_uncertainty`) answers *"did you show uncertainty at
all?"* — a verification concern. The new `"uncertainty"` relationship answers *"which mark
communicates it?"* — a selection concern. They are complementary surfaces over one D-05
source (Wilke ch.16 / §5.6); neither subsumes the other, and keeping both avoids a
false either/or.

### GA-3 — D-06 numbering for the new gate codes (REQ-P22-05)

**New gate codes take the next-free number in the 07x uncertainty band**, by the D-06
next-free rule verified against the **re-measured live 275 baseline** (not assumed):

- **`DSX-VIZ-071`** — reserved for the uncertainty-vocabulary gate extension (a declared
  uncertainty mark must be a recognised §5.6 family member). D-05 citation: **Wilke §5.6**
  (the mark set) + **§16.2** (the frequentist/Bayesian paradigm).
- **`DSX-VIZ-072`** — reserved *contingently*, only if plan (S2-2) finds a second distinct
  uncertainty check is warranted (e.g. paradigm-mismatch detection). Same citation basis.

**Everything else in Phase 22 mints zero code (Auditor, rigour tier):**
- **REQ-P22-05 perceptual tie-break** is a **repo-integrity test off the gate path**
  (`tests/`, family of `test_viz_vocabulary_invariant.py`), asserting `rank(a) <= rank(b)`
  over the catalog's rank data (D-1) — a **pure ordering assertion, no computation**, so it
  is not a `report.add(...)` gate code.
- **Faceting (REQ-P22-03)** ships as an orthogonal `facet_by` **declaration** whose smell
  remedies **route to an existing** overplotting/density check as a remedy string — no new
  banning code.
- **Catalog↔vocabulary conformance** (every DSX-admissible mark has exactly one catalog
  row; every catalog row flagged DSX-admissible is in the live vocabulary) is a
  repo-integrity test — no code.

So Phase 22's blocking-code footprint is **1 (contingently 2)**: `DSX-VIZ-071` (+`-072`).
Recorded loudly with a veto window (HQ-30), **not** escalated (brief §4: D-06 numeric
assignments are persona-round decisions, silence = accept). The set-identity mint diff at
phase end proves `275 → 276` (or `277`), additive-only.

## What Phase 22 execute (S2-3) is bound to

1. **Create `references/chart-catalog.md`** — the merged catalog, 75–90 rows, each with the
   three axes (function = attributed FT nine-category axis + our description per D-3; data
   signature = DSX input-type shape; perceptual rank = the D-1 six-rank-with-ties ordering)
   and a per-row citation; DSX-admissible vs reference-only clearly flagged; refusal rows
   for the 7 excluded types cross-referencing their banning code.
2. **Add the `"uncertainty"` relationship** (11th key, Wilke's 10 marks) to
   `RELATIONSHIP_CHARTS`; ripple through `_check_relationship_match`, `input_types.py`,
   regenerate `input_types.json`, and the skills/references that enumerate relationships.
3. **Mint `DSX-VIZ-071`** (+`-072` iff plan warrants) for the uncertainty gate extension,
   each with its Wilke §5.6/§16.2 D-05 citation; regenerate `finding-codes.md`; prove the
   additive-only set-identity diff.
4. **Add `gauge` + `word_cloud`** to `BANNED_TYPES` as `{reason, code=DSX-VIZ-001, citation}`
   records (Few 2006 / Jacob Harris 2011, HQ-27-signed); swap `radar`'s PROVISIONAL citation
   for **Duan et al. 2023**.
5. **`facet_by`** orthogonal declaration + smell-remedy routing (no new chart type, no new
   code).
6. **5-layer heuristic** as route-and-cite edits to `references/question-taxonomy.md` /
   `chart-selection.md` + skill pointers — no parallel decision tree (REQ-P22-04).
7. **Repo-integrity tests** (off gate path): the perceptual tie-break structural criterion
   (`rank(a) <= rank(b)`, D-1) and catalog↔vocabulary conformance.

## Open questions / carried caveats

- **HQ-30 (veto window, non-blocking):** GA-1 (reference-only rows to reach band; +gauge/
  word_cloud refusals), GA-2 (11th relationship key), GA-3 (`DSX-VIZ-071`/`-072`
  reservation). Silence = accept; nothing blocks on it.
- **Pinned at plan (S2-2), not here:** the exact reference-only row set (function-coverage
  gaps) and the exact count (75–90); whether `DSX-VIZ-072` is warranted. The plan-checker
  verifies band-compliance and the additive-only mint.
- **D-05 status:** every citation this phase ships is drawn from the **signed** HQ-27 pack
  (D-1…D-4 + the Tier-3 corrections). No new primary-source read is owed to unblock the
  build. The 8 items HQ-27 lists as *still unverified* (Mackinlay 1986, R.L. Harris 1999
  index, Tufte's verbatim chartjunk sentence, Few 2013 ed., GC primary count, FT stance on
  axis reuse, Munzner "cardinality", one Duan phrasing) are **not** relied on by any
  shipping row — execute must not cite them.
- **Cross-cutting independence caveat** travels into every reference-only citation drawn
  from the Ribecca lineage: name the lineage, never claim triangulation.
