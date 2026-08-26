# HUMAN-QUEUE — items only you can answer

The loop keeps working around these; it only blocks at stage S4 if any remain.
Answer by typing into the loop session, e.g. `HQ-1: test 1 pass, test 2 pass, ...`
The loop records your verdict in the proper GSD artifact (UAT file, SECURITY.md)
and checks the item off here.

## Open

### HQ-4 — Phase 11.2 formal D-05 UAT round: four primary-source citation reads (added 2026-08-26, S1-4)

Phase 11.2's technical verification **passed** (11.2-VERIFICATION.md: 5/5 ROADMAP
success criteria, 7/7 requirements, 0 gaps, 0 behavior_unverified). Status is
`human_needed` **solely** because of the D-05 primary-source reads below — the
citation *selections* were already approved in HQ-3 (answered), but the verbatim
quote-at-locator read (the project's D-05 bar) is a human check owed before 11.2
*ships*. **Non-blocking for S1-5** (secure-phase + validate-phase run on the
technically-verified phase); it blocks only the phase's formal UAT/ship sign-off,
drained at S4-2. Evidence packs will be assembled the way HQ-1's were.

| # | Read | Anchors requirement | Expected |
|---|------|--------------------|----------|
| 1 | Hernán, M.A. (2018) "The C-Word," *AJPH* 108(5):616-619 — exact quotable sentence + page for the causal-verb / prescriptive-language structural criterion. | REQ-P11.2-03 / -02 | Locator matches; D-16 unverified-locator flag cleared. |
| 2 | Simmons, Nelson & Simonsohn (2011) p.1361/1365; Gelman & Loken (2014); Wagenmakers et al. (2012) support the DSX-PRE-040/041 **firing** half; Nosek et al. (2018) supports the **clearing** half ONLY (must not anchor the firing half — 10-CONTEXT D-14). | REQ-P11.2-05 | Firing/clearing anchors each confirmed; flags cleared. |
| 3 | The structural-criterion citation for DSX-COH-040 (revisit_when completeness) and the prescriptive-severity companion for REQ-P11.2-02 (Manski, per HQ-3). | REQ-P11.2-04 / -02 | Both confirmed or replaced; flags cleared. |
| 4 | Veto window: the D-06 codes minted this phase (DSX-COH-040 CRITICAL, DSX-PRE-040 HIGH, DSX-PRE-041 HIGH) and the REQ-P11.2-02 severity amendment (flat HIGH → CRITICAL-none/HIGH-weak). | D-06 / D-03 | No veto raised; the irreversible decisions stand. |

Also for the veto window (loud §4 persona decisions from S1-4 code review, vetoable
here): CR-01 purpose-gate denylist; WR-01 exempting prescriptive from DSX-CLM-011
(flagship golden re-baselined, still blocks on DSX-CLM-020); WR-02 requiring a
metric/threshold separate from the time anchor (inverted the bare-duration test).
See 11.2-REVIEW.md "Resolution" for full rationale.

**Phase 11.2 security sign-off (added 2026-08-26, S1-5).** `/gsd-secure-phase 11.2`
ran State B and reached `status: verified`, `threats_open: 0` (14/14 threats closed —
`gsd-security-auditor` opus verdict SECURED, orchestrator independently re-gated: 4
HIGH blockers re-verified by grep + 332 targeted tests OK + full suite 1147 OK). The
technical gate is closed; per brief §4 category 4 the **human phase security sign-off
line** on `11.2-SECURITY.md` is owed here before ship (non-blocking for S1-5/downstream).
Also in this window: the four ACCEPT dispositions AR-11.2-04/-06/-07/-SC (design-time
D-12 residuals decided in the S1-1 persona round, not fresh redispositions). See
`11.2-SECURITY.md` "Accepted Risks Log" + "Sign-Off". Answer e.g.
`HQ-4 security: approved` (or veto any specific item).

## Will be added by the loop when reached

- End-of-phase UAT rounds for Phases 11.2, 11.3, 12 (batched, with evidence packs).
- `/gsd-cleanup` file-deletion approval (S4-6).
- Any persona decision you veto from a daily summary.

## Answered

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

