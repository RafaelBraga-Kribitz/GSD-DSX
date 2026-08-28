# HUMAN-QUEUE archive — answered items

Per LOOP-BRIEF.md §5: answered HUMAN-QUEUE items are moved here once nothing downstream
still double-checks them inline, so the live `HUMAN-QUEUE.md` (re-read in full every
firing) stays lean. Full verbatim records below; the live file keeps one-line pointers.

Moved 2026-08-28T03:55Z (S4-6 operator-hold firing): HQ-1..HQ-6 + the ⚠Z Zimmerman fix.

### HQ-1 — Phase 11 UAT: four D-05 citation/wording reads (answered 2026-08-26)

**Operator verdict (verbatim):**
`HQ-1: check2 pass, check3 pass (accept ⚠L as noted), check4 pass (accept ⚠LR as noted, ⚠J informational); check1 partial — ⚠Z flagged for manual research`

**Recorded in:** `.planning/phases/11-frequentist-admissibility-adjudicator-dsx-adm/11-UAT.md`

| Check | Result | Operator decision |
|---|---|---|
| 1 — 14 `families.yaml` citations | **Partial / blocked** | ⚠Z (HIGH): Zimmerman (2004) *Journal of General Psychology* 131(2):142-160 for `no_variance_pretesting` — **flag for manual research**. Thirteen families accepted at article level. Follow-up citation-fix unit required for families #6/#7/#8 and `ranking_rules` once confirmed. |
| 2 — `DSX-ADM-010` wording | **Pass** | Accept as noted. Wording prints ontology `strength` verbatim; cannot overstate beyond the field. |
| 3 — `test-selection.md` Fisher/Boschloo row | **Pass** | Accept as noted. Boschloo over Fisher for small cells (D-27 confirmed). ⚠L accepted: domination in Lydersen §5.4/§6.4, not §9. |
| 4 — `brief.md` §7 D-29 locators | **Pass** | Accept as noted. Kohavi Ch.22 identity confirmed (page range second-hand). Cameron & Miller VIII→XI jump confirmed by direct manuscript read. ⚠LR accepted (Ch.3 locator wrong; taxonomy in Ch.1 — follow-up fix). ⚠J informational only (Johari arXiv byline — no action). |

**Evidence pack:** assembled 2026-08-24 (S0-9). Full agent tables remain in git history pre-2026-08-26 (`HUMAN-QUEUE.md` open item) and in loop transcripts under `.planning/loop-logs/`.

**Requirement impact:** REQ-P11-02..06 may advance (checks 2–4 signed). REQ-P11-01 stays **partial** until ⚠Z is resolved and Check 1 passes.

### HQ-2 — Phase 11.1.1 security sign-off (answered 2026-08-26)

**Operator verdict (verbatim):** `HQ-2: (a) approved, (b) accept confirmed`

**Recorded in:** `.planning/phases/11.1.1-detection-code-hardening-inserted/11.1.1-SECURITY.md`, Sign-Off section.

| Item | Result | Detail |
|---|---|---|
| (a) Phase sign-off line | **Approved** | Phase 11.1.1 is now both technically verified (`status: verified`, `threats_open: 0`) and human-approved. |
| (b) T-11.1.1-06 redisposition | **Confirmed accept** | AR-11.1.1-04 stands as `accept`, not `mitigate` — no further engineering time expected on that input's performance (medium severity, below the `high` block threshold, never counted toward `threats_open`). |

**Requirement impact:** Phase 11.1.1 fully closed — both the technical gate and the human approval line. Unblocks S0-4 in `LOOP-LEDGER.md`.

### HQ-3 — Phase 11.2 discuss: D-05 citation reads (answered 2026-08-26)

**Operator verdict (verbatim):** `HQ-3: cite1 approved as structural criterion (no Levin requirement), cite2 use Manski (Law of Decreasing Credibility), cite3 re-anchor approved`

**Note on D-05:** this is the operator's approval of the persona round's citation *selections* — which sources anchor which requirement. It is not yet the D-05 primary-source read itself; that full evidence pack (verbatim quotes side-by-side with each locator) is still assembled the way HQ-1's was, once the checks land in code and the formal 11.2 UAT round opens. Recorded here now so that round can consume a decided citation set instead of re-litigating it.

| Item | Result | Detail |
|---|---|---|
| Cite 1 (REQ-P11.2-03) | **Approved** | Hernán, M.A. (2018), "The C-Word," *AJPH* 108(5):616-619, DOI 10.2105/AJPH.2018.304337 — sole structural criterion for causal-verb widening. Levin 1993 companion **not required**. |
| Cite 2 (REQ-P11.2-02) | **Manski selected** | Manski, Law of Decreasing Credibility (already in the Phase 11 citation spine) backs the decision-theoretic severity claim, over the offered Hernán & Robins Ch.1 alternative. |
| Cite 3 (REQ-P11.2-05) | **Re-anchor approved** | Firing half re-anchored to Simmons, Nelson & Simonsohn 2011 (60.7% false-positive rate, Table 1 p.1361) + Gelman & Loken 2014 + Wagenmakers et al. 2012. Nosek et al. 2018 retained **only** for the clearing half, per the persona round's reasoning that using it to fire on amendments would cite the paper against its own thesis (Phase 10's D-14 already relies on Nosek to argue declared deviations are legal). |

**Requirement impact:** REQ-P11.2-02, -03, -05 have a decided citation set. D-05's primary-source read itself remains outstanding and non-blocking — tracked for the formal Phase 11.2 UAT round, not reopened here.

### HQ-4 — Phase 11.2 formal D-05 UAT round + security sign-off (answered 2026-08-27)

**Operator verdict (verbatim):** `HQ-4: approve all citations + accept dispositions; security approved`

**D-05 reads — evidence gathered by the operator's own web verification** (not a mechanical
persona-round pack, an independent check against real sources) before asking: Hernán 2018 "The
C-Word" confirmed exact (*AJPH* 108(5):616-619, DOI 10.2105/AJPH.2018.304337), argument matches
(causal content is set by intent, not verb form). The reused Simmons/Nelson/Simonsohn 2011 +
Gelman & Loken 2014 set (already approved in HQ-3) independently re-confirmed real (*Psych Sci*
22(11):1359-1366; *American Scientist* 2014).

**Recorded in:** `.planning/phases/11.2-prescriptive-claim-layer/11.2-SECURITY.md`, Sign-Off section.

| Item | Result | Detail |
|---|---|---|
| 4 citation reads | **Approved** | REQ-P11.2-02/-03/-04/-05's D-05 bar met. |
| Veto window (CR-01, WR-01, WR-02) | **Accepted as decided** | Code-review dispositions from 11.2-REVIEW.md stand unchanged. |
| Security sign-off | **Approved** | Phase 11.2 now technically verified AND human-approved. 4 ACCEPT dispositions (AR-11.2-04/-06/-07/-SC) confirmed. |

**Requirement impact:** Phase 11.2 fully closed for ship — technical gate, D-05 bar, and human security sign-off all satisfied.

### HQ-5 — Phase 11.3 D-05 citation reads + D-06 code veto + security sign-off (answered 2026-08-27)

**Operator verdict (verbatim):** `HQ-5: approve all citations + accept codes/dispositions; security approved`

**D-05 reads — independently web-verified before asking:** Rubin 1987's total-variance formula
(anchoring the DSX-VAL-060 CRITICAL branch) confirmed — the book is real (Wiley 1987) and the
formula matches (found as T=Ū+B+B/m, algebraically identical to the cited T=W̄+(1+1/m)·B).
Simmons/Nelson/Simonsohn 2011 (anchoring DSX-VAL-080) is the same confirmed source as HQ-4's.

**Recorded in:** `.planning/phases/11.3-reporting-completeness/11.3-SECURITY.md`, Sign-Off section.

| Item | Result | Detail |
|---|---|---|
| 2 citation reads | **Approved** | REQ-P11.3-03/-04's D-05 bar met. |
| D-06 veto window (8 new codes) | **Accepted** | `DSX-EXP-053`, `DSX-STA-012`, `DSX-VAL-080`, `DSX-SPEC-083`, `DSX-CRV-010/011/012/013` stand — D-06 irreversible. Missingness-rate DEFER and Phase-12-backlog routing also accepted. |
| Security sign-off | **Approved** | Phase 11.3 now technically verified AND human-approved. 2 ACCEPT dispositions (AR-11.3-02, AR-11.3-SC) confirmed. |

**Requirement impact:** Phase 11.3 fully closed for ship.

### HQ-6 — Phase 12 (Calibration) UAT round + §4 veto + security sign-off (answered 2026-08-27)

**Operator verdict (verbatim):** `HQ-6: approve all citations + accept dispositions; security approved`

**D-05 reads — independently web-verified before asking, all three of this milestone's most
sensitive corpus-case citations:** (1) garden-of-forking-paths — Simmons/Nelson/Simonsohn 2011 +
Gelman & Loken 2014, both confirmed above; (2) LaCour & Green 2014 fabrication — confirmed
retracted by *Science*, retraction notice at exactly 348(6239):1100 as cited, fraud uncovered by
Broockman/Kalla/Aronow as cited; (3) Reinhart & Rogoff 2010 + the Herndon/Ash/Pollin 2014
critique — confirmed real, published in *Cambridge Journal of Economics* as cited, the canonical
operator-known-answer case that fell apart under independent replication.

**Recorded in:** `.planning/phases/12-calibration/12-SECURITY.md`, Sign-Off section.

| Item | Result | Detail |
|---|---|---|
| 3 citation reads | **Approved** | REQ-P12-01's D-05 bar met — the corpus's most sensitive cases confirmed genuine, not invented. |
| §4 veto window | **Accepted** | CR-01 (absolute D-13 boundary fix), IN-01/IN-02 (by-design), plus carried-forward items (sidecar format, missingness/paradigm DEFERs, §6.5 carry/relocate) all stand. |
| Security sign-off | **Approved** | Phase 12 — the milestone's terminal phase — now technically verified AND human-approved. AR-12-SC confirmed. |

**Requirement impact:** Phase 12 fully closed for ship. All three shipped phases (11.2, 11.3, 12) now have both their D-05 bar and human security sign-off satisfied.

### ⚠Z Zimmerman citation fix — HQ-1 follow-up (answered 2026-08-27)

**Operator verdict (verbatim):** `Correct to the British Journal locator`

The operator independently verified, via three sources (Wiley Online Library, PubMed, Semantic
Scholar), that Zimmerman, D.W. (2004), "A note on preliminary tests of equality of variances,"
*British Journal of Mathematical and Statistical Psychology* 57(1):173-181, DOI
10.1348/000711004849222, is real and its finding (a preliminary variance test fails to protect
the significance level, usually making it worse) matches exactly what `families.yaml` cites it
for. No matching article exists at the previously-cited *Journal of General Psychology*
131(2):142-160 locator.

**Ledger unit — EXECUTED at S4-1b (commit dc65fc6, 2026-08-28):** `references/families.yaml`
was edited for families `students_t`, `welch_t`, `welch_t_cluster_robust` (#6/#7/#8 per
11-UAT.md's numbering) and `ranking_rules` — the *Journal of General Psychology* locator
replaced with the *British Journal of Mathematical and Statistical Psychology* one above, the
D-05 catalogue gate re-run green (`gen-finding-catalogue.py --check` exit 0), and `locator_status`
reconciled (the Zimmerman-only `no_variance_pretesting` token → `verified`; the 4 co-cited
multi-source entries kept `unverified` under their unchanged project caveats — honesty call at S4-1b).

**Requirement impact:** the fix unit executed and its gate passed; REQ-P11-01 is now **satisfied**
— the last open item from Phase 11's original UAT round is closed.

