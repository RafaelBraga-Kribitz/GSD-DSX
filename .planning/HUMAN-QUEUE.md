# HUMAN-QUEUE — items only you can answer

The loop keeps working around these; it only blocks at stage S4 if any remain.
Answer by typing into the loop session, e.g. `HQ-1: test 1 pass, test 2 pass, ...`
The loop records your verdict in the proper GSD artifact (UAT file, SECURITY.md)
and checks the item off here.

## Open

(none currently — HQ-1, HQ-2 and HQ-3 are all answered; see below)

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

