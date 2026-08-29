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

The loop's S0-3 has filed the Phase 18 D-05 citation evidence pack below (HQ-16).
S0-4 will add the Phase 19 pack next. Expect ~15–20 citation reads across the two
packs — the largest D-05 round of any milestone so far; the granularity ruling
that keeps it bounded is: **one human read per new CODE, bibliographic citation
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

## Will be added by the loop when reached

- ~~S0-3: Phase 18 D-05 evidence pack~~ — **FILED as HQ-16 above (2026-08-29).**
- S0-4 (NEXT): Phase 19 D-05 evidence pack (RM/trend/categorical/resampling/post-hoc/
  negative-gate codes) — will be filed as HQ-17.
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
