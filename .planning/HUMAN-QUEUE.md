# HUMAN-QUEUE — items only you can answer

The loop keeps working around these; it only blocks at stage S4 if any remain.
Answer by typing into the loop session, e.g. `HQ-1: test 1 pass, test 2 pass, ...`
The loop records your verdict in the proper GSD artifact (UAT file, SECURITY.md)
and checks the item off here.

## Open

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

### HQ-3 — Phase 11.2 discuss: D-05 citation reads for the prescriptive claim layer (opened 2026-08-24)

**Non-blocking.** The loop keeps building Phase 11.2; these reads are needed before 11.2 *ships*
(verify/ship), not before it plans/executes. A fuller evidence pack (verbatim quotes side-by-side
with each claimed locator) will be assembled the way HQ-1 was, once the checks land in code. This
item records the citation *selections* the 2026-08-24 persona round made so you can start reading.

Project rule D-05 requires **you** to read the primary source; the persona round prepared the
evidence, it did not sign. Three reads:

1. **Causal-verb widening (REQ-P11.2-03) — Hernán, M.A. (2018), "The C-Word: Scientific Euphemisms
   Do Not Improve Causal Inference From Observational Data," *American Journal of Public Health*
   108(5):616-619, DOI 10.2105/AJPH.2018.304337.** Confirm the paper states that a claim's causal
   content is set by intent, not verb form (euphemistic/nominalised verbs face the same
   identification standard) — the `Structural criterion:` for flagging bare/gerund action forms.
   Confirm the exact quotable sentence + page.

2. **Prescriptive severity (REQ-P11.2-02) — companion needed.** Hernán 2018 covers *language
   honesty*, not the *decision-theoretic severity of recommending an action*. Approve one of:
   **Manski, Law of Decreasing Credibility** (already in the Phase 11 citation spine) or
   **Hernán & Robins, *Causal Inference: What If*, Ch.1** — for "an intervention requires
   identification, not merely an association."

3. **Amendment discipline (REQ-P11.2-05) — RE-ANCHOR AWAY FROM Nosek.** The ROADMAP's candidate
   **Nosek et al. 2018 "The preregistration revolution," *PNAS* 115(11):2600-2606** is the **wrong
   anchor for the FIRING half** — Phase 10's `10-CONTEXT.md` D-14 already uses Nosek to argue
   *declared deviations are legal*, so citing it to fire HIGH on amendments would cite the paper
   against its own thesis. The persona round re-anchored the firing half to **Simmons, Nelson &
   Simonsohn 2011** (researcher degrees of freedom; published reference value **60.7%** false-positive
   rate, Table 1 p.1361), **Gelman & Loken 2014** (garden of forking paths; already the Phase-10
   anchor), and **Wagenmakers et al. 2012** ("the data may be used only once" — the temporal
   criterion). **Nosek 2018 is retained only for the CLEARING half** (a declared amendment stays
   legal). Please confirm this re-anchor, or veto it.

Optional: approve **Levin 1993** (lexical causatives) as the verb-classification companion, or accept
Hernán 2018 alone as the structural criterion for D-05.

Answer e.g. `HQ-3: cite1 pass, cite2 use Manski, cite3 re-anchor accepted, Levin optional-skip` — or
raise any item. The loop records your verdict when it assembles the 11.2 UAT.

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

