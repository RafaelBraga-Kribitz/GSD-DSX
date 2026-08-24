# HUMAN-QUEUE — items only you can answer

The loop keeps working around these; it only blocks at stage S4 if any remain.
Answer by typing into the loop session, e.g. `HQ-1: test 1 pass, test 2 pass, ...`
The loop records your verdict in the proper GSD artifact (UAT file, SECURITY.md)
and checks the item off here.

## Open

### HQ-1 — Phase 11 UAT: four D-05 citation/wording reads (11-UAT.md, open since 2026-08-22)

Project rule D-05 requires a **human** to read the source; the loop will attach an
evidence pack here (S0-9) so each check takes minutes:

1. Read all 14 `references/families.yaml` citations against their real sources.
2. Confirm `DSX-ADM-010`'s finding wording does not overstate ranking strength.
3. Read the corrected Fisher/Boschloo row in `references/test-selection.md`.
4. Read the two D-29 citation locators folded into `brief.md` §7.

Answering this flips REQ-P11-01..06 from partial to satisfied.

**Evidence pack** — assembled 2026-08-24 by the loop (S0-9), from three parallel
web-verification passes over every source the four checks touch. This is *evidence
only*: D-05 requires **you** to read the primary source, so nothing below is a
sign-off. The loop did **not** edit `references/families.yaml`, `test-selection.md`
or `brief.md` — where a source disagrees with its claimed citation, the discrepancy
is surfaced here for your decision, not silently "corrected".

**Read this first (5-line summary):**
1. Every source the four checks name **exists** and, at article level, almost all
   match their claimed citation string exactly.
2. Check 4's hardest claim — the Cameron & Miller (2015) manuscript numbering that
   **jumps from Section VIII to Section XI** — is CONFIRMED by a direct read of the
   open manuscript (no Section IX/X headings exist; the paper's own intro even calls
   the conclusion "Section IX" while the heading reads "XI").
3. Check 2 holds: the `DSX-ADM-010` finding prints the ontology's own `strength`
   token **verbatim** and only ever says "prefers" / "ranks another family above it",
   never "dominates" — so it cannot overstate strength beyond the ontology field.
4. **Three discrepancies need your eyes before checks 1 and 3 can pass** — see the
   "⚠ Discrepancies" block after the Check-1 table.
5. Full agent detail is in the loop transcript under `.planning/loop-logs/`; the
   distilled evidence is below.

---

#### Check 1 — 14 `families.yaml` entries, citation vs. real source

Each of the 14 `families:` entries maps to one of 8 distinct sources (some families
share a source). "Claimed status" is the file's own `locator_status`. "Agent verdict"
is the web-assembled evidence — **not** a D-05 sign-off.

| # | family id | Source cited | Claimed status | Agent verdict (article-level) |
|---|---|---|---|---|
| 1 | two_proportion_z | Agresti (2013) 3rd ed | unverified | Book confirmed (Wiley, 3rd ed, 2013); no chapter claimed — matches "unverified" |
| 2 | fishers_exact | Lydersen et al. (2009) §9 | verified | Article EXACT (28(7):1159-1175, DOI 10.1002/sim.3531); §9 line confirmed — see ⚠L |
| 3 | boschloo_exact | Lydersen et al. (2009) §9 | verified | Same as #2; the *domination* sentence is in §5.4/§6.4, not §9 — see ⚠L |
| 4 | two_proportion_z_always_valid | Agresti (2013) 3rd ed | unverified | As #1 |
| 5 | two_proportion_z_cluster_robust | Agresti (2013) 3rd ed | unverified | As #1 (clustering charged via Cameron & Miller tokens) |
| 6 | students_t | Delacre et al. (2017)+2022 Corr.; Zimmerman (2004) | unverified | Delacre EXACT; **Zimmerman citation could not be located — see ⚠Z** |
| 7 | welch_t | Delacre et al. (2017)+2022 Corr.; Zimmerman (2004) | unverified | As #6 |
| 8 | welch_t_cluster_robust | Delacre; Zimmerman; Cameron & Miller (2015) §II | unverified | Delacre EXACT; Cameron & Miller §II CONFIRMED; **Zimmerman — see ⚠Z** |
| 9 | linear_regression_unadjusted | Freedman (2008) | unverified | Real venue found: *Adv. Appl. Math.* 40(2):180-193, DOI 10.1016/j.aam.2006.12.003 |
| 10 | linear_regression_interacted_adjustment | Lin (2013) | unverified | Real venue found: *Ann. Appl. Stat.* 7(1):295-318, DOI 10.1214/12-AOAS583, arXiv:1208.2301 |
| 11 | linear_regression_cv1 | Cameron & Miller (2015) §II | verified | Article EXACT (50(2):317-372, DOI 10.3368/jhr.50.2.317); §II heading CONFIRMED |
| 12 | linear_regression_cv3_wild_bootstrap | MacKinnon, Nielsen & Webb (2023) §9 | unverified | Article EXACT (232(2):272-299, DOI 10.1016/j.jeconom.2022.04.001); §9 = "Conclusion: A Summary Guide", plausible — published §-numbers unread (paywall) |
| 13 | linear_regression_block_bootstrap | Cameron & Miller (2015) | unverified | Article EXACT; temporal-case locator genuinely unconfirmed, matches "unverified" |
| 14 | ratio_of_means_delta_method | Deng, Knoblich & Lu (2018) | verified | DOI 10.1145/3219819.3219919 + arXiv:1803.06336 CONFIRMED |

**Assumption-token sources these families charge** (in `assumption_vocabulary`), all
confirmed at article level unless flagged: Hernán & Robins (2020) *What If* — §3.2
exchangeability / §3.3 positivity / §3.4 consistency CONFIRMED by direct PDF read;
Rubin (1980) JASA 75(371):591-593 CONFIRMED (note: the correct DOI is
`10.1080/01621459.1980.10477517`; the adjacent `...12` is Basu's paper, do not
conflate); Rubin (1976) *Biometrika* 63(3):581-592 CONFIRMED; Imbens & Rubin (2015)
book CONFIRMED (SUTVA in Ch.1 not independently reached — paywall); MacKinnon et al.
(2023) §4 "Asymptotic Inference" covers few-treated-clusters, plausible; Little &
Rubin — **see ⚠LR**; Johari et al. (2022) — **see ⚠J**.

**⚠ Discrepancies (resolve before signing Check 1 / Check 3):**

- **⚠Z — Zimmerman (2004) citation looks misattributed (HIGH).** The file cites
  "Zimmerman, D.W. (2004), *Journal of General Psychology* 131(2):142-160" and marks
  the `no_variance_pretesting` token `verified`. The agent pulled the full 2004
  Crossref/ToC listing for that journal volume and found **no Zimmerman article**
  there (nearest by page range is Grabbe & Pratt, an unrelated topic). The paper that
  actually matches the attached claim (pre-testing for equal variance inflates the
  Type-I error of the following t-test) is most likely **Zimmerman, D.W. (2004), "A
  note on preliminary tests of equality of variances," *British Journal of
  Mathematical and Statistical Psychology* 57(1):173-181, DOI
  10.1348/000711004849222** (paywalled — agent could not read it directly). This is a
  claim of *absence*, which an agent cannot settle; **please confirm** whether the
  *Journal of General Psychology* locator is real. If it is not, the citation (and its
  `verified` status) needs correcting in `families.yaml`, `ranking_rules:` and three
  families (#6/#7/#8) — a follow-up fix unit, not part of this evidence pack.
- **⚠L — Lydersen §9 attribution is split (MEDIUM).** The "should practically never
  be used" sentence about Fisher's exact test **is** verbatim in Section 9 (p.1174) ✓.
  But the *uniform-power-domination* claim (Boschloo ≥ Fisher at every configuration)
  is stated in **§5.4 (p.1168) and §6.4 (p.1170-71)**, not §9, and the paper credits
  it to Boschloo (1970) [ref 21] as a rejection-region-containment argument (analytic),
  not an empirical "every parameter value checked" scan. The substance is real and in
  the paper; only the *section pointer for the domination half* is imprecise. Bears on
  Checks 1, 2 and 3 (all lean on Lydersen §9).
- **⚠LR — Little & Rubin Ch.3 locator (MEDIUM, adjacent).** The
  `missing_at_random_given_covariates` token cites "Little & Rubin, *Statistical
  Analysis with Missing Data*, Chapter 3, section 3.2 (mechanisms)". A recovered 3rd-ed
  (2019) table of contents shows **Ch.3 = "Complete-Case and Available-Case Analysis"**;
  the MCAR/MAR/MNAR mechanism taxonomy sits in Ch.1 (and ignorability in Ch.7). The
  ToC was a publisher preview, not a full read, and editions renumber — **please
  confirm** against your copy. (Same locator also appears in `brief.md` §7 for
  `DSX-VAL-060`, so it is adjacent to Check 4 too.)
- **⚠J — Johari et al. arXiv author list (LOW).** Published *Operations Research*
  70(3):1806-1821 (4 authors incl. Koomen) matches exactly; the arXiv companion
  1512.04922 (v3) still lists only 3 authors (no Koomen) and the older sub-title. The
  cite pairs them as "also arXiv:1512.04922" — accurate for the paper, minor mismatch
  on the preprint's byline.

---

#### Check 2 — `DSX-ADM-010` wording does not overstate ranking strength

The finding's rendered `detail` (`dsx/frame/admissibility.py:752-761`) is:
> "Ranking rule `<id>` (citation: `<citation>`) states that `<prefers>` is preferred
> over `<over>` when `<condition>` **-- strength: `<strength>`**." … "Prefer
> `<prefers>` when `<condition>` -- the declared procedure remains admissible, but
> this cited ordering **ranks another family above it**."

It never renders the word "dominates"; it prints the ontology's `strength` token
verbatim. So the sentence can be no stronger than the field. The four orderings:

| ranking_rule id | strength field (rendered verbatim) | Source | Honest? |
|---|---|---|---|
| boschloo_over_fishers_exact | `uniform_domination` | Lydersen et al. (2009) — real uniform-power result (⚠L on the §9 pointer) | Yes — the only uniform result, and it is genuine |
| welch_over_students | `default_preference` | Delacre (2017) — "Welch's t-test should always be used" (a default, not a domination) | Yes — worded as preference |
| cv3_wild_bootstrap_over_cv1 | `reliability_hedged` | MacKinnon et al. (2023); file note: "must never be reported as a domination" | Yes — hedged |
| interacted_adjustment_over_unadjusted | `default_preference` | Lin (2013) cannot-hurt + Freedman (2008) | Yes — preference |

Verdict for your read: the code cannot promote a hedged/preference ordering into a
domination — it echoes the field. The only judgement left to you is whether
`uniform_domination` is the honest label for Boschloo-over-Fisher; the Lydersen
evidence (⚠L) says the *claim* is real, only its section pointer is loose.

---

#### Check 3 — `references/test-selection.md` Fisher/Boschloo row + Lydersen footnote

Current text (verbatim):
> Row: "two-proportion z (**Boschloo's exact test** if any expected cell < 5)[^1]"
> [^1]: "The small-expected-cell fallback here is **Boschloo's unconditional exact
> test, not the traditional Fisher's exact test.** Lydersen, Fagerland and Laake
> (2009), *Statistics in Medicine* 28(7):1159-1175, section 9, states directly that
> the traditional Fisher's exact test should practically never be used … Boschloo's
> test never has less power than the traditional test it replaces, at every parameter
> value checked. Locator: section 9, verified."

Evidence: the correction is **present and correct** — the row prescribes Boschloo,
not Fisher, as the small-cell fallback (the D-27 fix landed). The Lydersen article and
the "practically never be used" §9 quote are confirmed. **Two caveats for your read,**
both from ⚠L: (a) the "at every parameter value checked" phrasing describes an
analytic rejection-region-containment result (credited to Boschloo 1970), not an
empirical scan; (b) the domination half is in §5.4/§6.4, while §9 carries the
"never use Fisher" recommendation — so "Locator: section 9, verified" is right for the
recommendation but loose for the domination claim.

---

#### Check 4 — `brief.md` §7, two D-29 locators

| Locator (brief §7) | Claimed strength | Agent evidence |
|---|---|---|
| Kohavi, Tang & Xu, *Trustworthy Online Controlled Experiments*, **Ch.22 "Leakage and Interference between Variants", pp.226-234, verified** | verified | Book + chapter number + **exact chapter title** CONFIRMED via Cambridge Core. Page range **226-234 second-hand only** — Ch.23 starts at p.235 per a search summary of the ToC, but the ToC PDF was not read directly (server 403/timeout). Human must open the book to sign the page range. |
| Cameron & Miller (2015), *JHR* 50(2):317-372, "Section VI *Few Clusters*" verified, "**manuscript jumps VIII→XI, typeset may differ; manuscript numbering is the verified object**" | manuscript-verified w/ numbering caveat | **CONFIRMED by direct manuscript read.** Headings: I, II Cluster-Robust Inference, III, IV What to Cluster Over?, V, VI Few Clusters, VII, VIII Empirical Example, **XI Concluding Thoughts** — no IX/X exist; the intro prose even says "Section IX" for the conclusion the heading calls "XI". §II/IV/VI match their claimed roles. The caveat is verified exactly as written. |

Both read at the strength the evidence supports: Kohavi's chapter identity is verified
but its page range is one confirmation short (second-hand); Cameron & Miller is
manuscript-verified with the numbering caveat intact and now independently corroborated.

---

**To answer:** e.g. `HQ-1: check1 pass (Zimmerman corrected / accepted as flagged),
check2 pass, check3 pass, check4 pass` — or raise any ⚠ item. The loop records your
verdict in `11-UAT.md` and, if you flag ⚠Z/⚠LR, opens a follow-up citation-fix unit.

### HQ-2 — Phase 11.1.1 security sign-off — NOW UNBLOCKED (2026-08-24), awaiting only your two confirmations

Plans 06/07/08 are all executed and S0-4 re-ran `/gsd-secure-phase 11.1.1`
(2026-08-24). The register is now `status: verified`, `threats_open: 0`: all three
blocking threats (T-11.1.1-13 plan04, T-11.1.1-08 factual half, WR-02) were verified
closed in the live tree by `gsd-security-auditor` (opus) and independently re-gated by
the loop (suite 1031 OK; `record_decision(`=4, `scan_path:not-scanned`=2, `findings.py`
untouched). Two human sign-offs remain — neither blocks the technical `verified`
status, but the phase is NOT human-approved until you answer both:
- **(a)** Approve the SECURITY.md phase sign-off line (`11.1.1-SECURITY.md`, Sign-Off
  section — currently reads "technical re-audit PASSED … two human sign-offs remain").
- **(b)** Confirm redisposing T-11.1.1-06 (2.525s vs 1.0s house budget on the 3.1MB
  pathological, analyst-authored input) from "mitigate" to "accept" (logged as
  AR-11.1.1-04). It is medium / below the `high` block threshold, so it never counted
  toward `threats_open` regardless.

Answer e.g. `HQ-2: (a) approved, (b) accept confirmed` — the loop will write your
verdict into `11.1.1-SECURITY.md` and check this item off.

## Will be added by the loop when reached

- End-of-phase UAT rounds for Phases 11.2, 11.3, 12 (batched, with evidence packs).
- `/gsd-cleanup` file-deletion approval (S4-6).
- Any persona decision you veto from a daily summary.

## Answered

(moved here with timestamp and where the verdict was recorded)
