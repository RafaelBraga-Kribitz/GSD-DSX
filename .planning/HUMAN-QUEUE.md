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
**Evidence pack:** (loop fills in at S0-9)

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
