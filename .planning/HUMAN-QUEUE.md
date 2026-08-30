# HUMAN-QUEUE — items only you can answer

Milestone **v2.3 Test Catalog**. The loop keeps working around these; it only
blocks at the close-out stage (S5-2) if any remain.

**How to answer:** the operator is usually remote and cannot run local commands.
Answer in the session; an interactive Claude session records the verdict in the
proper GSD artifact (UAT file, SECURITY.md) and checks the item off here.

**What reaches this queue** (brief §4 — everything else the loop decides itself via
a persona round and records loudly):

1. A D-05 primary-source read — citation authenticity. The loop may prepare the
   evidence pack; it may not sign it.
2. An irreversible destructive operation (file deletion, history rewrite, force-moving
   a published tag).
3. A change to milestone scope (dropping or rewording a requirement).
4. A security sign-off (`SECURITY.md` approval line).
5. An outward-facing ship action (merge to `main`, release tag, opening a PR).

## Open

Both D-05 packs are now filed: the Phase 18 pack (HQ-16, 11 citations) and the
Phase 19 pack (HQ-17, 16 citations across REQ-P19-01…07). Expect ~27 citation reads
across the two — the largest D-05 round of any milestone so far; the granularity ruling
that keeps it bounded is: **one human read per new gate CODE, bibliographic citation
per catalog ENTRY.** Nothing blocks on these until close-out (S5-2).

### HQ-16 — Phase 18 D-05 citation evidence pack (filed early by design; non-blocking)

**Status: ASSEMBLED 2026-08-29 (S0-3), awaiting the human read. DO NOT SIGN — the
loop prepared this pack; D-05 authenticity is a human opening each primary source
and confirming the exact result at the exact locator.** Filed ahead of Phase 18 so
the operator reads while Phase 17 builds. Nothing waits on this until close-out (S5-2).

**What "confirmed by the loop" means below (READ ONCE):** bibliographic metadata
(authors / title / venue / year / volume / pages / DOI-or-PMID) and the candidate
formulation were corroborated by the loop across **multiple independent sources** on
2026-08-29. That is **not** a D-05 read — it only turns the operator's read into a
fast confirm-at-locator instead of a hunt. **What the human must still do:** open
each primary source and confirm the exact result at the exact page/equation, and —
where a numeric reference VALUE will become a test fixture — confirm that value at
the source. Code→citation binding and D-06 numbering are **Phase 17/18 persona
decisions, not settled here** — this pack only qualifies the citations.

**Granularity (per the scope §2.4 ruling):** the human reads that bind are keyed to
the two new Phase 18 **gate codes** — correlation scale/kind-match (REQ-P18-03) and
agreement declaration-completeness (REQ-P18-04) — plus the effect-size **band
sources** (REQ-P18-05) and the **one worked numeric value** (Krippendorff α). The
per-row bibliographic citations for the correlation catalog entries not named here
(Spearman 1904, Kendall 1938, point-biserial/Tate 1954, phi/Cramér 1946) are
row-level and do **not** each require a separate human read; they are confirmed at
the Phase 18 row-bibliography pass.

---

#### Group A — Pearson CI convention (REQ-P18-01 correlation row) — confidence: **HIGH**

**A1 — Fisher (1921), Fisher-z transformation for the Pearson correlation CI**

| Field | Value |
|---|---|
| Primary source | Fisher, R. A. (1921). *On the "probable error" of a coefficient of correlation deduced from a small sample.* **Metron, 1, 3–32.** |
| Candidate formulation the row will cite | The variance-stabilising transform **z = ½·ln((1+r)/(1−r)) = arctanh(r)**, approximately normal with **Var(z) ≈ 1/(n−3)**; the Pearson CI is formed on z and back-transformed with tanh. This is the "Fisher-z CI convention" REQ-P18-01 attaches to the Pearson row. |
| **Confirmed by the loop** | Locator (Metron vol. 1, pp. 3–32, 1921); that this is the origin of the z / arctanh transform and the 1/(n−3) variance; corroborated across multiple independent restatements. |
| **UNVERIFIED — for the human read** | The exact page carrying the transform and the 1/(n−3) variance within pp. 3–32 (Metron pagination is not in the corroborating snippets). |

---

#### Group B — Kappa-family agreement rows (REQ-P18-02; B2 also backs the REQ-P18-04 weighted-weights gate)

**B1 — Cohen (1960), Cohen's kappa — confidence: HIGH**

| Field | Value |
|---|---|
| Primary source | Cohen, J. (1960). *A coefficient of agreement for nominal scales.* **Educational and Psychological Measurement, 20(1), 37–46.** DOI **10.1177/001316446002000104**. |
| Candidate formulation | **κ = (p_o − p_e) / (1 − p_e)**, p_o observed agreement, p_e chance agreement from the marginals. |
| **Confirmed by the loop** | Locator (EPM 20(1):37–46, DOI); that this is kappa's primary source; the chance-corrected formula (corroborated widely). |
| **UNVERIFIED — for the human** | The exact page/equation of the κ definition within 37–46. |

**B2 — Cohen (1968), weighted kappa — confidence: HIGH**

| Field | Value |
|---|---|
| Primary source | Cohen, J. (1968). *Weighted kappa: nominal scale agreement with provision for scaled disagreement or partial credit.* **Psychological Bulletin, 70(4), 213–220.** |
| Candidate formulation | **κ_w** with an explicit, analyst-**declared** disagreement-weight matrix (linear or quadratic weights are conventions, not defaults). Backs REQ-P18-04's "weighted kappa without **declared** weights blocks." |
| **Confirmed by the loop** | Locator (Psych. Bull. 70(4):213–220); that κ_w originates here and requires a weight scheme supplied by the analyst. |
| **UNVERIFIED — for the human** | Exact page/equation; that the paper frames the weights as analyst-supplied (not auto-chosen) in the form the gate rationale will cite. |

**B3 — Fleiss (1971), Fleiss kappa (m raters) — confidence: HIGH**

| Field | Value |
|---|---|
| Primary source | Fleiss, J. L. (1971). *Measuring nominal scale agreement among many raters.* **Psychological Bulletin, 76(5), 378–382.** DOI **10.1037/h0031619**. |
| Candidate formulation | Generalises kappa to a fixed number of raters per subject where the raters need not be the same across subjects; large-sample SEs derived, numerical example given. |
| **Confirmed by the loop** | Locator (Psych. Bull. 76(5):378–382, DOI); that this is the many-raters generalisation. |
| **UNVERIFIED — for the human** | Exact page/equation of the estimator and its SE. |

**B4 — Hayes & Krippendorff (2007), Krippendorff's α + WORKED VALUE — confidence: HIGH on locator, the VALUE is the live D-05 question**

| Field | Value |
|---|---|
| Primary source | Hayes, A. F. & Krippendorff, K. (2007). *Answering the call for a standard reliability measure for coding data.* **Communication Methods and Measures, 1(1), 77–89.** DOI **10.1080/19312450709336664**. |
| Candidate WORKED VALUE (would become the α fixture) | **α = 0.743** on the paper's worked example. ⚠️ **Trap the read must resolve:** Krippendorff's *textbook* reports **0.734** for the same data, which is a **known typographical error**; the macro/paper value **0.743** is the correct one. The fixture must adopt the value the operator confirms at the primary source, not the book. |
| **Confirmed by the loop** | Locator (CM&M 1(1):77–89, DOI); that this is α's standard reference; that a 0.743-vs-0.734 discrepancy exists and 0.743 is the corrected value (corroborated across independent sources). |
| **UNVERIFIED — for the human (this is the load-bearing read)** | The **exact worked-example dataset and the exact α at its locator** in the paper — because this becomes a pinned numeric fixture (scope §2.3: Krippendorff configs ship catalog-only until a published numeric reference value is adopted). Per brief §5, if the value cannot be confirmed at the source, the α fixture ships **catalog-only** rather than pinned to an unverified number. |

---

#### Group C — ICC (model, type, definition) triple (REQ-P18-02 + REQ-P18-04 gate) — confidence: HIGH

**C1 — Shrout & Fleiss (1979)**

| Field | Value |
|---|---|
| Primary source | Shrout, P. E. & Fleiss, J. L. (1979). *Intraclass correlations: uses in assessing rater reliability.* **Psychological Bulletin, 86(2), 420–428.** |
| Candidate formulation | The **six ICC forms** — ICC(1,1), ICC(2,1), ICC(3,1) and their k-averaged forms — indexed by the **model** (one-way random / two-way random / two-way mixed) and whether one rater or a mean of k is the unit. Backs REQ-P18-04's "ICC without the full declared (model, type, definition) triple blocks." |
| **Confirmed by the loop** | Locator (Psych. Bull. 86(2):420–428); the six-form taxonomy and the model/unit indexing. |
| **UNVERIFIED — for the human** | Exact page/equation for each form's definition. |

**C2 — McGraw & Wong (1996)**

| Field | Value |
|---|---|
| Primary source | McGraw, K. O. & Wong, S. P. (1996). *Forming inferences about some intraclass correlation coefficients.* **Psychological Methods, 1(1), 30–46.** |
| Candidate formulation | Supplies the **"consistency" vs "absolute agreement"** distinction (the "definition" axis of the triple) and the single-vs-average-measures axis — the modern (model, type, definition) vocabulary REQ-P18-04's gate reads. |
| **Confirmed by the loop** | Locator (Psych. Methods 1(1):30–46); the consistency/absolute-agreement and single/average framing. ⚠️ The loop notes a **published correction to this article exists** (a same-year erratum on some of its formulae). |
| **UNVERIFIED — for the human** | Exact page/table for the definition axis; **and** whether the specific form(s) the gate's rationale leans on are among those touched by the erratum — confirm against the corrected version, not the original. |

---

#### Group D — Method comparison (REQ-P18-01/02 row + REQ-P18-03 routing target) — confidence: HIGH

**D1 — Bland & Altman (1986)**

| Field | Value |
|---|---|
| Primary source | Bland, J. M. & Altman, D. G. (1986). *Statistical methods for assessing agreement between two methods of clinical measurement.* **The Lancet, 1(8476), 307–310.** |
| Candidate formulation | **Limits of agreement = mean difference ± 1.96·SD(differences)**, plotted as difference vs mean. This is the method REQ-P18-03 routes a declared `method_comparison` estimand **to** (and away from a bare correlation). |
| **Confirmed by the loop** | Locator (Lancet 1(8476):307–310, 1986); the limits-of-agreement definition and the difference-vs-mean plot. |
| **UNVERIFIED — for the human** | Exact page of the ±1.96·SD statement within 307–310. |

---

#### Group E — Kappa companion-reporting gate (REQ-P18-04) — confidence: HIGH

**E1 — Feinstein & Cicchetti (1990)**

| Field | Value |
|---|---|
| Primary source | Feinstein, A. R. & Cicchetti, D. V. (1990). *High agreement but low kappa: I. The problems of two paradoxes.* **Journal of Clinical Epidemiology, 43(6), 543–549.** PMID **2348207**. (Companion: Cicchetti & Feinstein 1990, *II. Resolving the paradoxes*, JCE 43(6):551–558.) |
| Candidate formulation the gate cites | The two paradoxes — high p_o can yield low κ under marginal imbalance; κ rises with asymmetric imbalance — which is **why** REQ-P18-04 blocks a kappa reported **without** its declared companions (raw agreement p_o **and** the prevalence / marginal context). Declaration-completeness, not a numeric threshold. |
| **Confirmed by the loop** | Locator (JCE 43(6):543–549, PMID); the two-paradoxes result and its companion paper. |
| **UNVERIFIED — for the human** | Exact page of each paradox statement; that the paper's own recommendation is "report p_o and marginals alongside κ" in the form the gate rationale cites. |

---

#### Group F — Effect-size interpretation bands (REQ-P18-05) — ship as **CONVENTIONS, never blocking thresholds**

**F1 — Landis & Koch (1977), kappa benchmark bands — confidence: HIGH on bands, ONE locator caveat**

| Field | Value |
|---|---|
| Primary source | Landis, J. R. & Koch, G. G. (1977). *The measurement of observer agreement for categorical data.* **Biometrics, 33(1), 159–174.** PMID **843571**. |
| Candidate bands (label as convention) | < 0 poor · 0.00–0.20 slight · 0.21–0.40 fair · 0.41–0.60 moderate · 0.61–0.80 substantial · **0.81–1.00 almost perfect** (corroborated across multiple sources). |
| **Confirmed by the loop** | Locator; the six band labels and boundaries. ⚠️ **Locator caveat:** a **second** Landis & Koch 1977 Biometrics paper exists — *An application of hierarchical kappa-type statistics…*, **33(2):363–374** — which is **not** the benchmark source. Cite the **159–174** paper for the bands. |
| **UNVERIFIED — for the human** | That the benchmark table is in 159–174 (not 363–374) and the exact edge conventions (inclusive/exclusive) as the paper words them. |

**F2 — Koo & Li (2016), ICC interpretation bands — confidence: HIGH on locator, band VALUES unconfirmed**

| Field | Value |
|---|---|
| Primary source | Koo, T. K. & Li, M. Y. (2016). *A guideline of selecting and reporting intraclass correlation coefficients for reliability research.* **Journal of Chiropractic Medicine, 15(2), 155–163.** DOI **10.1016/j.jcm.2016.02.012**, PMID **27330520**. |
| Candidate bands (label as convention) | < 0.5 poor · 0.5–0.75 moderate · 0.75–0.90 good · > 0.90 excellent. **Loop flag:** the corroborating search confirmed the paper and locator but did **not** confirm these exact boundary values — treat the numbers as candidate-only until read. |
| **Confirmed by the loop** | Locator (J. Chiropr. Med. 15(2):155–163, DOI, PMID); that the paper gives interpretive ICC ranges. |
| **UNVERIFIED — for the human** | The **exact boundary values and labels** at the source (the loop did not confirm them); and that Koo & Li present them as guidance, not thresholds. |

---

**Not in this pack (flagged, not an omission):** the REQ-P18-03 correlation
scale/kind-match gate's own *doctrinal* citation (measurement scale ⇒ Pearson needs
interval/ratio + linear; ordinal ⇒ Spearman/Kendall) is a Phase 18 discuss binding
decision, not one of the 11 named here. The remaining correlation-row bibliographic
citations (Spearman/Kendall/point-biserial/phi) are row-level per the granularity
ruling and are confirmed at the Phase 18 row-bibliography pass.

**Operator action:** read the sources at the locators above and reply in a session
with, per group (or per citation where you want finer grain): confirmed-at-locator
(with any locator corrections) or not-confirmed. Two are load-bearing beyond
metadata: **B4 (Krippendorff α = 0.743 worked value)** and **F1/F2 (the band
boundaries)** — a fixture or a band that cannot be confirmed at its source ships
**catalog-only / convention-labelled**, per brief §5, rather than pinned to an
unverified number. An interactive session records the verdict and checks HQ-16 off.
Until then, Phase 18 (S2) treats any code whose citation is not confirmed as **not
in hand** (the S2-1 D-05 bar).

### HQ-17 — Phase 19 D-05 citation evidence pack (filed early by design; non-blocking)

**Status: ASSEMBLED 2026-08-29 (S0-4), awaiting the human read. DO NOT SIGN — same
standard as HQ-16: the loop corroborated bibliographic metadata + the candidate
formulation across multiple independent sources; D-05 authenticity is a human opening
each primary source and confirming the exact result at the exact locator.** Filed ahead
of Phase 19 (S3) so the operator reads while Phases 17–18 build. Nothing waits on this
until close-out (S5-2).

**"Confirmed by the loop" means exactly what it means in HQ-16:** bibliographic metadata
(authors / title / venue / volume / issue / pages / DOI-or-PMID) and the candidate
formulation were corroborated across **≥2 independent sources** on 2026-08-29
(Crossref / publisher page / DOI resolver / PubMed / citation index / textbook
restatement). That is **not** a D-05 read — it only turns the operator's read into a
fast confirm-at-locator. **What the human must still do:** open each primary source,
confirm the exact result at the exact page/equation, and — where a numeric value would
become a test fixture or a section number would become a citation string — confirm it at
the source. Code→citation binding and D-06 numbering are Phase 17/19 persona decisions,
not settled here.

**Granularity (per scope §2.4 — one human read per new gate CODE):** the reads that bind
are keyed to the Phase 19 gate codes (REQ-P19-01…07). Row-level bibliographic citations
for catalog entries that carry no gate (Friedman, Cochran's Q, Page's L,
Jonckheere-Terpstra, Dunn, Nemenyi, Scheffé, Tukey/Kramer, Dunnett, Clopper-Pearson,
Woolf, etc.) are confirmed at the Phase 19 row-bibliography pass and do **not** each
require a separate human read.

---

#### Group A — RM sphericity (REQ-P19-01 gate: two-stage Mauchly-then-correct blocks) — confidence: **HIGH**

**A1 — Greenhouse & Geisser (1959), the ε (epsilon) sphericity correction**

| Field | Value |
|---|---|
| Primary source | Greenhouse, S. W. & Geisser, S. (1959). *On methods in the analysis of profile data.* **Psychometrika, 24(2), 95–112.** DOI **10.1007/BF02289823**. |
| Candidate formulation the gate cites | The ε adjustment to the F-test degrees of freedom for departures from sphericity — the "always correct" (unconditional Greenhouse-Geisser) analog of always-Welch that REQ-P19-01 requires and against which the two-stage Mauchly-then-correct procedure blocks. |
| **Confirmed by the loop** | Locator (Psychometrika 24(2):95–112, DOI) corroborated across 4 independent sources (Crossref, Springer, RePEc, Cambridge Core); that this is the origin of the applied ε correction. |
| **UNVERIFIED — for the human** | The exact equation/page defining ε (function of the covariance-matrix eigenvalues). ⚠️ **Locator trap:** a same-authors, author-order-**reversed** paper exists — Geisser, S. & Greenhouse, S. W. (1958), *An extension of Box's results…*, **Annals of Mathematical Statistics 29(3):885–891** — which did the underlying derivation but is **not** the paper to cite for the applied ε correction. Confirm the catalog cites the **1959 Psychometrika** paper. |

**A2 — Maxwell & Delaney (2004), the "routinely correct" doctrine — confidence: HIGH on identity, TEXTBOOK (no DOI)**

| Field | Value |
|---|---|
| Primary source | Maxwell, S. E. & Delaney, H. D. (2004). *Designing Experiments and Analyzing Data: A Model Comparison Perspective* (**2nd ed.**). Mahwah, NJ: Lawrence Erlbaum. ISBN **0-8058-3718-3**. **Textbook — no DOI/PMID.** Chapters **11–12** (within-subjects / repeated-measures designs). |
| Candidate formulation the gate cites | The argument for routinely applying the ε correction rather than a preliminary sphericity test (Mauchly) — the doctrinal backing for REQ-P19-01's unconditional-GG requirement and its two-stage-blocks gate. |
| **Confirmed by the loop** | Publisher / 2nd ed. / 2004 / ISBN corroborated across 4+ sources; that ch. 11–12 cover within-subjects designs (independent course-notes for "M&D ch. 11/12"); the "Mauchly underpowered → just correct" position attributed to this edition by a secondary stats reference. |
| **UNVERIFIED — for the human** | Exact page(s) in ch. 11–12 for the "always correct" argument (no DOI to anchor a textbook). ⚠️ **Two edition traps:** (a) some retailer records attach **Ken Kelley** as a co-author to the 2nd-ed ISBN — Kelley is a **3rd-edition** addition; the 2004 title page is Maxwell & Delaney only. (b) The **3rd edition renumbers** this content to later chapters — the "ch. 11–12" locator is **edition-locked to the 2nd (2004)** and will not match a 3rd-ed copy. |

---

#### Group B — Trend tests (REQ-P19-02 gates: declared dose scores / declared autocorrelation handling) — confidence: **HIGH**

**B1 — Hamed & Rao (1998), modified Mann-Kendall variance correction**

| Field | Value |
|---|---|
| Primary source | Hamed, K. H. & Rao, A. R. (1998). *A modified Mann-Kendall trend test for autocorrelated data.* **Journal of Hydrology, 204(1–4), 182–196.** DOI **10.1016/S0022-1694(97)00125-X**. (No PMID — not PubMed-indexed; expected.) |
| Candidate formulation the gate cites | A corrected (effective-sample-size-deflated) variance for the Mann-Kendall S-statistic under serial correlation — the backing for REQ-P19-02's "declared autocorrelation handling required" on Mann-Kendall + Sen's-slope rows. |
| **Confirmed by the loop** | Locator (J. Hydrology 204(1–4):182–196, DOI) corroborated across 4 sources (Crossref, ScienceDirect, ADS, SCIRP); the variance-correction-via-effective-sample-size approach. |
| **UNVERIFIED — for the human** | The exact equation/page for the variance-correction factor and the autocorrelation-significance threshold that decides which lags enter the correction (the load-bearing procedural detail behind the declared-field gate). Double-check the combined "issue 1–4" against the paginated print issue. |

**B2 — Cochran (1954), Cochran half of Cochran-Armitage**

| Field | Value |
|---|---|
| Primary source | Cochran, W. G. (1954). *Some methods for strengthening the common χ² tests.* **Biometrics, 10(4), 417–451.** DOI **10.2307/3001616**. |
| Candidate formulation | The linear-trend-in-proportions partition of chi-square that, with Armitage 1955, is the Cochran-Armitage trend test REQ-P19-02 requires declared dose scores for. |
| **Confirmed by the loop** | Locator (Biometrics 10(4):417–451, DOI) corroborated across 4 sources (Crossref, Google Scholar, SCIRP, secondary restatements). |
| **UNVERIFIED — for the human** | ⚠️ **Title-glyph trap:** the authoritative title carries the literal "χ²" glyph — confirm the catalog's stored string doesn't silently diverge (ASCII "chi-squared"/"chi-square" variants abound). This paper covers **several** "strengthening" methods; pin the exact sub-section/page for the **trend** method vs the combining-2×2 methods. |

**B3 — Armitage (1955), Armitage half of Cochran-Armitage**

| Field | Value |
|---|---|
| Primary source | Armitage, P. (1955). *Tests for linear trends in proportions and frequencies.* **Biometrics, 11(3), 375–386.** DOI **10.2307/3001775**. |
| Candidate formulation | The linear-trend test statistic across an ordered series of proportions (extends Cochran 1954). |
| **Confirmed by the loop** | Locator (Biometrics 11(3):375–386, DOI) corroborated across 4 sources (Crossref, PsycINFO, Google Scholar, Semantic Scholar). |
| **UNVERIFIED — for the human** | ⚠️ **Title-number trap:** the authoritative title is **plural** "Trends"; at least one aggregator renders singular "Trend" — confirm against JSTOR. (A hosted-PDF fetch of this paper returned a hallucinated wrong title/pages — disregard any automated re-fetch of that copy; read JSTOR/print.) |

---

#### Group C — Categorical: N−1 chi-square (REQ-P19-03; Yates ships DEPRECATED) — confidence: **HIGH on metadata, one attribution question**

**C1 — Campbell (2007), N−1 chi-square**

| Field | Value |
|---|---|
| Primary source | Campbell, I. (2007). *Chi-squared and Fisher–Irwin tests of two-by-two tables with small sample recommendations.* **Statistics in Medicine, 26(19), 3661–3675.** DOI **10.1002/sim.2832**. (No PMID surfaced; DOI is the persistent id.) |
| Candidate formulation | **χ²₍N−1₎ = χ²_Pearson × (N−1)/N**, df unchanged; recommended over Yates (which over-corrects) once the smallest expected count exceeds ~1 — the basis for making N−1 the default and shipping Yates DEPRECATED. |
| **Confirmed by the loop** | Full record corroborated across ≥3 sources (Crossref, MRC-CBU stats FAQ, academia.edu, MedCalc manual); the (N−1)/N multiplier with df unchanged (R-bloggers, UVM course page). |
| **UNVERIFIED — for the human (load-bearing framing)** | ⚠️ **Attribution:** multiple secondary sources say the N−1 statistic was **originally proposed by Egon Pearson**, and Campbell 2007 is the **simulation study that recommends reviving it** — so the citation should read "argued for / revalidated," **not** "invented." Confirm the exact applicability boundary (smallest expected count ≥ 1?) the catalog will encode, at the primary source. |

---

#### Group D — Resampling (REQ-P19-04 gate: seed + B + unit + method quadruple) — confidence: **HIGH**

**D1 — Davidson & MacKinnon (2000), how many bootstraps (B conventions)**

| Field | Value |
|---|---|
| Primary source | Davidson, R. & MacKinnon, J. G. (2000). *Bootstrap tests: how many bootstraps?* **Econometric Reviews, 19(1), 55–68.** DOI **10.1080/07474930008800459**. |
| Candidate formulation (ships as **cited convention**, the gate is declaration-completeness, not a threshold) | Choose B so that **α(B+1) is an integer**; practical minimum **B = 399 (α=.05) / B = 1499 (α=.01)** to keep finite-B power loss small. |
| **Confirmed by the loop** | Full record across 4+ sources (Crossref, Tandfonline, EconPapers, ResearchGate); the 399/1499 values and α(B+1)-integer rule read from the author-hosted PDF and corroborated by an independent search synthesis. |
| **UNVERIFIED — for the human (load-bearing if any B number is pinned)** | ⚠️ **Two distinct B pairs must not be conflated:** the **exactness floor** (smallest B with α(B+1) integer) is **19 / 99**; the **recommended practical minimum** is **399 / 1499**. If any catalog text pins a B floor, state which pair — treating 19/99 as the floor silently under-powers. Confirm page in the published pagination (the loop read an author working-paper mirror, not the journal offprint). |

**D2 — Efron (1987), BCa interval (house default)**

| Field | Value |
|---|---|
| Primary source | Efron, B. (1987). *Better bootstrap confidence intervals.* **Journal of the American Statistical Association, 82(397), 171–185** (published **with discussion**). DOI **10.1080/01621459.1987.10478410**. |
| Candidate formulation | The BCa interval — percentile interval adjusted by bias-correction z₀ and acceleration â, second-order accurate — the house-default resampling CI. |
| **Confirmed by the loop** | Record across ≥2 sources (Crossref, Tandfonline); that this 1987 paper is the credited BCa origin (Wikipedia + a method synthesis). |
| **UNVERIFIED — for the human** | ⚠️ **Page-range locator:** Crossref registers **171–185** (Efron's article); some sources cite **171–200** because discussion+rejoinder follow — the BCa equations live in **171–185**. Decide which range the catalog means. ⚠️ **Term trap:** the abbreviation "**BCa**" may have been popularized later (Efron & Tibshirani 1993), not coined in the 1987 text — don't quote "BCa" as Efron's own 1987 wording without checking. z₀/â equations not retrievable (JSTOR/Tandfonline 403). |

---

#### Group E — Post-hoc (REQ-P19-05 gate: declared post-hoc must match declared omnibus family) — confidence: **HIGH; one load-bearing locator disambiguation**

**E1 — Games & Howell (1976), Games-Howell (house default after Welch ANOVA)**

| Field | Value |
|---|---|
| Primary source | Games, P. A. & Howell, J. F. (1976). *Pairwise multiple comparison procedures with unequal n's and/or variances: a Monte Carlo study.* **Journal of Educational Statistics, 1(2), 113–125.** DOI **10.3102/10769986001002113**. |
| Candidate formulation | The Games-Howell pairwise procedure (per-pair Welch–Satterthwaite df + studentized range) for unequal variance/unequal n. |
| **Confirmed by the loop** | Full record across 3 sources (Crossref, ERIC EJ143952, SAGE); the unequal-variance/unequal-n Monte-Carlo context. |
| **UNVERIFIED — for the human** | ⚠️ **Venue-name trap:** in 1976 the journal was *Journal of Educational Statistics*; it was **renamed** *Journal of Educational **and Behavioral** Statistics* only **post-1994** — using the renamed title for the 1976 paper is an anachronism. Note "house default after Welch" is a **later convention**, not this Monte-Carlo paper's own single recommendation. |

**E2 — Hayter (1986), unprotected LSD fails at k>3 — LOAD-BEARING LOCATOR**

| Field | Value |
|---|---|
| Primary source (the one to cite) | Hayter, A. J. (1986). *The maximum familywise error rate of Fisher's least significant difference test.* **Journal of the American Statistical Association, 81(396), 1000–1004.** DOI **10.1080/01621459.1986.10478364**. |
| Candidate formulation | Fisher's **unprotected** LSD controls the familywise error rate only at exactly **k = 3** groups; its max FWER exceeds α for k ≥ 4 — the basis for shipping unprotected LSD at k>3 (and SNK) as DEPRECATED. |
| **Confirmed by the loop** | 1986 JASA record across 3 sources; the MFWER-exceeds-α result and the k=3-only protection (secondary summaries). |
| **UNVERIFIED — for the human (load-bearing)** | ⚠️ **Do NOT cite the wrong Hayter paper:** a **different** Hayter (**1984**), *A proof of the conjecture that the Tukey-Kramer procedure is conservative*, **Annals of Statistics 12(1)**, DOI 10.1214/aos/1176346392 — is a separate work on a **different** topic. There is **no** Hayter 1986 in *Annals*. Cite the **1986 JASA** paper. Confirm the exact k boundary (k=3 protected vs k≥4) as the paper words it. |

---

#### Group F — Negative gates (REQ-P19-06: two-stage variance-test blocks; observed power blocks) — confidence: **HIGH**

**F1 — Zimmerman (2004), preliminary variance test invalidates the location test**

| Field | Value |
|---|---|
| Primary source | Zimmerman, D. W. (2004). *A note on preliminary tests of equality of variances.* **British Journal of Mathematical and Statistical Psychology, 57(1), 173–181.** DOI **10.1348/000711004849222**, PMID **15171807**. |
| Candidate formulation the gate cites | Conditioning the location-test choice on a preliminary variance test fails to protect the Type I rate (usually makes it worse); unconditional separate-variance testing is preferred — the backing for the REQ-P19-06(a) block. |
| **Confirmed by the loop** | Full record across 4 sources (Crossref, Wiley/BPS, PubMed, search synthesis); the "two-stage fails, use separate-variance unconditionally" conclusion. |
| **UNVERIFIED — for the human (scope caveat)** | The paper's tested context is **Levene-then-t-test** (two-group t), not k-group ANOVA. If the catalog's gate blocks a general ANOVA-level variance-precondition, confirm the paper supports that generalization or cite it only for the t-test case. Any numeric Type-I-inflation figure must come from the paper's tables. |

**F2 — Hoenig & Heisey (2001), the observed-power fallacy**

| Field | Value |
|---|---|
| Primary source | Hoenig, J. M. & Heisey, D. M. (2001). *The abuse of power: the pervasive fallacy of power calculations for data analysis.* **The American Statistician, 55(1), 19–24.** DOI **10.1198/000313001300339897**. |
| Candidate formulation | Observed / post-hoc power is a monotone function of the p-value and conveys no new information — the basis for REQ-P19-06(b)'s "observed power in a readout blocks." |
| **Confirmed by the loop** | Full record across 4 sources (Crossref, Tandfonline, EconPapers, a free UBC-hosted PDF); the observed-power-fallacy framing. |
| **UNVERIFIED — for the human (scope)** | The exact p-value↔power monotone relation page/equation; whether the argument covers **all** post-hoc power uses or only interpreting one's own non-significant result — this sets how broadly the gate should fire. |

**F3 — Lakens (2022), sensitivity power analysis (the sanctioned MDE substitute)**

| Field | Value |
|---|---|
| Primary source | Lakens, D. (2022). *Sample size justification.* **Collabra: Psychology, 8(1), 33267.** DOI **10.1525/collabra.33267**. **CC BY 4.0 open access** (no access barrier for the read). |
| Candidate formulation | **Sensitivity power analysis** — the range of effects a design can detect given the achieved N (a sensitivity curve) — as the sanctioned substitute row for observed power. |
| **Confirmed by the loop** | Full record across 5 sources (Crossref, TU/e portal, UCPress, Semantic Scholar, author's companion text); that sensitivity power analysis is one of the six justification approaches presented. |
| **UNVERIFIED — for the human** | Whether Lakens uses "**minimum detectable effect (MDE)**" verbatim or whether that is the catalog's paraphrase of "sensitivity curve" — don't attribute "MDE" wording to him without checking. |

---

#### Group G — Proportion / count extras (REQ-P19-07 gates: Wald-for-proportion blocks; no-declared-offset blocks) — confidence: **HIGH; two load-bearing caveats**

**G1 — Brown, Cai & DasGupta (2001), Wald interval is bad**

| Field | Value |
|---|---|
| Primary source | Brown, L. D., Cai, T. T. & DasGupta, A. (2001). *Interval estimation for a binomial proportion.* **Statistical Science, 16(2), 101–133.** DOI **10.1214/ss/1009213286**. |
| Candidate formulation | The Wald proportion interval has erratic/chaotic coverage; recommend Wilson (house default) / Jeffreys for small n, Agresti-Coull for larger n — the basis for REQ-P19-07's "declared Wald interval for a proportion blocks." |
| **Confirmed by the loop** | Full record across ≥4 sources (Project Euclid, PMC2706447, Wharton faculty page, Google Scholar); the erratic-coverage result and the Wilson/Jeffreys/Agresti-Coull recommendation (abstract snippet). |
| **UNVERIFIED — for the human (load-bearing if pinned)** | ⚠️ A secondary source (PMC2706447) paraphrases the small/large-n cutoff as **"n ≤ 40"**; this exact number was **not** in the primary abstract snippet. If any catalog text hard-codes n=40, confirm it at the primary source's recommendation section. |

**G2 — Newcombe (1998), difference-between-proportions intervals — LOAD-BEARING TWO-PAPER DISAMBIGUATION**

| Field | Value |
|---|---|
| Primary source (the one to cite for RD/RR/OR) | Newcombe, R. G. (1998). *Interval estimation for the difference between independent proportions: comparison of eleven methods.* **Statistics in Medicine, 17(8), 873–890.** DOI **10.1002/(SICI)1097-0258(19980430)17:8<873::AID-SIM779>3.0.CO;2-I**, PMID **9595617**. |
| The companion paper (do NOT cross-wire) | Newcombe, R. G. (1998). *Two-sided confidence intervals for the single proportion: comparison of seven methods.* **Statistics in Medicine, 17(8), 857–872.** DOI ends **…<857::AID-SIM777>**, PMID **9595616** — the **single-proportion** paper, a different citation. |
| Candidate formulation | The Wilson-score-combination ("Newcombe hybrid-score") interval for a risk difference, easy to implement at any n — for the RD/RR/OR named-interval-method rows. |
| **Confirmed by the loop** | Both papers' records across ≥4 sources each (Wiley, PubMed, ResearchGate, Crossref, Wikidata). |
| **UNVERIFIED — for the human (load-bearing)** | ⚠️ The two DOIs differ only in **SIM777 vs SIM779** and the page digit (857 vs 873) — a one-character slip swaps them. **Cite Paper B (873–890, SIM779, PMID 9595617)** for RD intervals; any citation-lint should assert the full DOI, not "Newcombe 1998." Which of the 11 methods the catalog implements (the Wilson-score combination) should be pinned at the source. |

**G3 — McCullagh & Nelder (1989), offset for exposure/time-at-risk — SECTION LOCATOR UNCONFIRMED**

| Field | Value |
|---|---|
| Primary source | McCullagh, P. & Nelder, J. A. (1989). *Generalized Linear Models* (**2nd ed.**). London: Chapman & Hall. *Monographs on Statistics and Applied Probability*, vol. 37. ISBN **0-412-31760-5**. **Textbook — no DOI.** Ch. 6 "Log-Linear Models." |
| Candidate formulation | The log(exposure) **offset** (coefficient constrained to 1) that turns a Poisson count model into a rate model — the basis for REQ-P19-07's "declared exposure/time-at-risk with no declared offset blocks." |
| **Confirmed by the loop** | Book identity across ≥6 sources (Routledge, Amazon, Google Books, Internet Archive, SCIRP); that **Chapter 6** is "Log-Linear Models" and is the standard cite for the offset-for-rates technique. |
| **UNVERIFIED — for the human (this is the weakest link in the pack)** | ⚠️ The specific "**§6.2**" sub-section could **not** be corroborated. Secondary citations point at **"p. 206"** and **"§6.3.2"** — **neither confirms 6.2**. Per brief §5, until the human confirms the exact section, the citation ships at **chapter granularity ("Ch. 6, Log-Linear Models")**, not pinned to "§6.2." Confirm the exact section/page for the offset content in the 2nd-ed copy. |

**G4 — Wilson (2015), Vuong-for-zero-inflation is a misuse (DEPRECATED row)**

| Field | Value |
|---|---|
| Primary source | Wilson, P. (2015). *The misuse of the Vuong test for non-nested models to test for zero-inflation.* **Economics Letters, 127, 51–53.** DOI **10.1016/j.econlet.2014.12.029**. (Issue field returns "C" = Elsevier continuous-numbering, i.e. **no issue number** — not a data error.) |
| Candidate formulation | Vuong's non-nested test is invalid for comparing a zero-inflated model to its non-zero-inflated parent (they are effectively nested) — the basis for shipping Vuong-for-zero-inflation as DEPRECATED. |
| **Confirmed by the loop** | Full record across ≥5 sources (EconPapers, Crossref, Semantic Scholar, ScienceDirect index, Wolverhampton OA repository); the "quasi-nested → misuse" argument. |
| **UNVERIFIED — for the human** | Exact wording of the "misuse" argument and whether Wilson endorses a replacement test (relevant to whether the catalog cites an alternative alongside the deprecation) — a 3-page paper, low locator risk; the OA repository copy is readable. |

---

**Load-bearing beyond metadata (read these with extra care — a value or locator that
can't be confirmed at source ships catalog-only / chapter-granular / convention-labelled,
per brief §5):** (1) **G3 McCullagh & Nelder §6.2** — the section number is unconfirmed;
ships at chapter granularity until pinned. (2) **E2 Hayter** — cite the 1986 JASA paper,
NOT the 1984 Annals paper; confirm the k>3 boundary. (3) **G2 Newcombe** — cite Paper B
(873–890, SIM779), not Paper A. (4) **D1 Davidson & MacKinnon** — 399/1499 (recommended)
vs 19/99 (exactness floor); state which if any B is pinned. (5) **G1 Brown-Cai-DasGupta**
— the "n ≤ 40" cutoff is secondary-source only; verify before hard-coding. (6) **C1
Campbell** — cite as "argued for / revalidated," not "invented" (Egon Pearson originated
N−1). (7) **A1 Greenhouse-Geisser** — cite the 1959 Psychometrika paper, not the reversed-
author 1958 Annals paper.

**Operator action:** read the sources at the locators above and reply in a session with,
per group (or per citation): confirmed-at-locator (with any locator corrections) or
not-confirmed. An interactive session records the verdict and checks HQ-17 off. Until
then, Phase 19 (S3) treats any code whose citation is not confirmed as **not in hand**
(the S3-1 D-05 bar).

### HQ-18 — Phase 17 discuss decisions (veto window; NON-BLOCKING; silence = accept)

**Status: RECORDED 2026-08-29 (S1-1). Not a D-05/scope/ship escalation — a D-06-class
persona decision recorded loudly with a veto window per brief §4. Nothing blocks on it.**
Two decisions from `.planning/phases/17-foundation-repairs-and-spec-vocabulary/17-CONTEXT.md`
that the operator may veto from a daily summary:

1. **`estimand_kind` gains a 6th member `nominal_association`** (phi / Cramér's V on
   unordered r×c) beyond REQ-P17-02's named five. Additive, within the requirement's "at
   least" grant; both personas voted for it (Cramér's V is an unsigned dependence measure,
   not a signed Pearson r — folding it into `linear_association` would mis-carve the
   estimand space). Full 6-member set + rationale in 17-CONTEXT.md D-01.
2. **D-06 range pre-allocation** — one DSX-STA decade per theme, 050–129, 130s reserve
   (17-CONTEXT.md D-03). Codes are permanent (D-06); this reserves ranges so Phases 18/19
   draw collision-free. Phase 17 assigns none.

To veto either, reply in a session; otherwise silence accepts and Phase 18/19 build on them.

## Will be added by the loop when reached

- ~~S0-3: Phase 18 D-05 evidence pack~~ — **FILED as HQ-16 above (2026-08-29).**
- ~~S0-4: Phase 19 D-05 evidence pack~~ — **FILED as HQ-17 above (2026-08-29).**
- Phase 17/18/19/20 end-of-phase security sign-off + UAT rounds (batched per
  phase; non-blocking until S5-2).
- D-06 numbering veto windows for the new codes (from the Phase 17 pre-allocated
  ranges; silence = accept).
- The S5-6 ship decisions: merge to `main` and the `v2.3.0` release tag.
- Any persona decision the operator vetoes from a daily summary.

## Standing framework notes (not queue items — nothing to answer, just remember)

**`/gsd-audit-uat`'s automated CLI under-reports human-verification items — TWO
defects.** (1) `gsd-core/bin/lib/uat.cjs::parseVerificationItems` only recognizes
a level-2 `## Human Verification` heading while the verifier template writes
level-3 `### Human Verification Required` (found v2.0.0). (2) `uat.cjs:78`
filters on `f.includes('-VERIFICATION')` while this repo's files are named
`VERIFICATION.md`, so the CLI never opens them and returns a false All Clear
(found v2.2 S5-1). **At S5-1, never accept the CLI's "all clear" — hand-check
every phase's VERIFICATION.md.**

**`check.decision-coverage-plan` false-blocks on this project's CONTEXT.md
decision-bullet style (found v2.3 S1-2).** The §13a plan-phase decision-coverage
gate parses decisions with `gsd-core/bin/lib/decisions.cjs`, whose regexes expect
`- **D-NN:** …` (colon-immediate) or em-dash-*inside*-the-bold. The discuss-phase
persona rounds write `- **D-12a disposition table** recorded …` / `- **D-06 range
pre-allocation** — one …` (title inside the bold, separator *after* the closing
`**`), which matches none of the three regexes → `total:0, reason:"could-not-parse",
passed:false`. That is a parser format-mismatch, **not** an uncovered decision — the
gsd-plan-checker's Dimension-7 (Context Compliance) substantively verifies the same
property (every D-NN honored by a plan). **At every phase plan gate (P18/P19/P20 S*-2),
do NOT treat this could-not-parse/total:0 as a real coverage gap** — confirm coverage
via the plan-checker Dim-7 pass and proceed. (Fixing it would mean either widening the
parser or reformatting committed CONTEXT.md decision bullets to `- **D-NN:** …`; not
done — the substantive gate already covers it.)

**`/gsd-pr-branch` does not survive a long ceremony branch.** Its per-commit
cherry-pick chain hit recurring modify/delete conflicts on v2.0.0's 707-commit
branch and was abandoned mid-run. Ship by direct 3-way merge.

**Ship by EXPLICIT branch name — never the framework's auto-detect.** This repo
carries stale `gsd/*` branches from prior milestones; `/gsd-complete-milestone`'s
`handle_branches` picks the alphabetically-first `gsd/*` branch, which is wrong
here (found and bypassed at v2.2 ship). `git merge --no-ff gsd/v2.3.0-test-catalog`
by name, verified on a throwaway branch first.

**Release tags: never force-move a published one.** v2.0.0 shipped as tag
`v2.1.0` for this reason; v2.2 shipped as `v2.2.0`. The next free tag for this
milestone is `v2.3.0`.

**`/gsd-complete-milestone` output needs hand-verification.** At v2.2 close its
generated accomplishment bullets were truncated mid-sentence and the archived
REQUIREMENTS.md carried all rows forward still unchecked despite the passed
audit — both had to be hand-corrected. Also: it is NOT headless-safe
(interactive prompts + `git rm REQUIREMENTS.md`) — interactive session only.

**Run the full suite from a clean tree — a stray root `DECISIONS.jsonl`
false-fails two `explain` tests.** `tests/test_dsx.py::test_explain_missing_spec_exits_zero_not_two`
and `tests/test_explain_self_reported.py::test_returns_zero_when_spec_cannot_be_loaded`
run from repo-root CWD without isolation; any repo-root `dsx gate`/`dsx explain`
leaves a gitignored ledger that breaks them. If exactly these two fail:
`rm -f DECISIONS.jsonl examples/DECISIONS.jsonl examples/known-bad/DECISIONS.jsonl templates/DECISIONS.jsonl`
and re-run before treating it as real.

**Usage-limit backoff is the wrapper's job (operator-directed 2026-08-29).**
`scripts/run-ceremony-firing.ps1` detects limit hits in the transcript, writes
`.planning/loop-logs/.backoff-until`, skips polls until the weekly reset
(Wednesday 10:00 América/São_Paulo = 13:00 UTC; 60 minutes for a 5-hour-window
hit), then resumes by itself. Firings: log one line, stop, never retry-loop,
never touch the backoff file.

## Answered

(v2.0.0's items HQ-1…HQ-7 and v2.2's items HQ-8…HQ-15 are archived at
`.planning/milestones/v2.0.0-HUMAN-QUEUE*.md` and
`.planning/milestones/v2.2-HUMAN-QUEUE.md`. Numbering continues from HQ-16.)
