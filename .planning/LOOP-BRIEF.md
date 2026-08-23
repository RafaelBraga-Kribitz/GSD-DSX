# LOOP-BRIEF — v2.0.0 completion ceremony (autonomous)

**Purpose:** This file is the standing contract for the `/loop` session that finishes
milestone v2.0.0 (DSX Validity Frame). Re-read it at every wakeup. The work backlog
lives in `LOOP-LEDGER.md`; items only a human can answer live in `HUMAN-QUEUE.md`.

**Hard deadline:** 2026-09-01 end of day (buffer day 2026-09-02).
**Definition of done:** every item in LOOP-LEDGER.md checked; milestone audit re-run
and `passed` (not gaps-accepted); `/gsd-complete-milestone` archived; branch pushed;
HUMAN-QUEUE.md empty or every remaining item explicitly accepted by the human.

## 1. One wakeup = one unit

Each wakeup: read this brief, read LOOP-LEDGER.md, pick the **first unblocked unit**
in stage order, execute it **to completion** (including its gate), update the ledger,
commit + push, then schedule the next wakeup. Never start a second heavy unit in the
same wakeup. A unit is one ledger checkbox (one skill invocation or one bounded fix
batch), not a whole stage.

## 2. Cadence and quota (Claude Pro Max 5x)

- After completing a heavy unit: schedule wakeup in **1800s**.
- After a light unit (doc fix, ledger bookkeeping): **900s**.
- Rate-limit / 5-hour-window error: do NOT retry. Schedule **3600s noop** wakeups
  until capacity returns. Log the pause in the ledger.
- Waiting only on HUMAN-QUEUE answers: **3600s noop** wakeups; send one
  PushNotification per day summarizing what is waiting.
- Soft budget: at most ~2 phase-scale units per calendar day. The schedule in §7
  has slack; do not burn the weekly quota trying to run ahead of it.

## 3. Model and effort routing

GSD's `model_profile: adaptive` already routes GSD subagents — do not override it.
For direct `Agent` spawns and effort choices, use this table:

| Work | Model | Effort |
|---|---|---|
| Mechanical doc fixes (traceability rows, frontmatter, progress tables) | haiku | low |
| Plan execution, test writing, fix application | profile default (sonnet-class) | medium |
| Discuss persona rounds, planning, plan-check, verification, code review | opus | high |
| Milestone audit, adversarial statistical review, Phase 12 catch-rate / false-positive-rate readout | fable (Agent model override) or opus | high/max |

Rule: never spend opus/fable on work a checklist could do; never let a sonnet-class
agent make an irreversible design decision alone.

## 4. Expert persona protocol (answer your own questions)

For every gray-area decision, run an internal advisor round instead of asking the
human. Panel (spawn only the relevant 2–3):

- **Architect** — `dsx-analysis-architect`: spec shape, decision rules, contracts.
- **Statistician** — `dsx-statistician`: validity, missingness design, calibration
  metrics, multiplicity.
- **Auditor** — `gsd-security-auditor` / `dsx-ml-integrity-auditor`: threats,
  leakage, evaluation defects.
- **Advisor** — `gsd-advisor-researcher`: option comparison for tooling/approach.

Round shape: each persona proposes options, raises its own questions, answers them,
and votes. The orchestrator picks, breaking ties by **rigour > reliability >
flexibility**. Record the decision and rationale in the phase CONTEXT.md (or
REVERSALS.md if it reverses anything) and one line in the ledger. Decisions are
loud, never silent: every persona-decided item also appears in the daily summary.

Escalate to HUMAN-QUEUE.md **only** when the item is one of:
1. A D-05 human source read (citation authenticity — the project's bar is a human
   reading the source; personas may prepare the evidence pack but not sign it).
2. An irreversible destructive operation (file deletion, history rewrite).
3. A change to milestone scope (dropping or rewording a requirement).
4. A security sign-off (`SECURITY.md` approval line).

Numeric finding-code assignments (D-06, irreversible) are decided by persona round
using "next free number in family, catalogue-consistent", recorded loudly as above —
NOT escalated. The human may veto via the daily summary before the phase ships.

## 5. Non-negotiable ground rules

- Never mark a ledger item done without its verifying gate actually passing
  (run the test / read the file / run the command — paste evidence into the ledger).
- Tracking files (REQUIREMENTS.md, STATE.md, ROADMAP.md) are single-writer:
  orchestrator only, never subagents.
- Windows CRLF: any line-start/end regex uses `\r?\n`.
- After every commit, push. Every daily summary ends with branch / commits ahead /
  unpushed state.
- Gate failure: one repair attempt, then record the blocker in the ledger and
  HUMAN-QUEUE if human-shaped, and move to the next non-dependent unit. Never loop
  on a failing gate.
- Never skip verification, security, or Nyquist validation gates to save time. If
  the deadline is at risk, shrink new-feature scope via a recorded re-scope in
  HUMAN-QUEUE (consent required) — rigour is not the variable.

## 6. Stages (execute in order; units within a stage may be reordered if unblocked)

- **S0 — Hygiene and open gates.** Close everything the 2026-08-23 milestone audit
  found on already-executed phases before any new scope. Details in ledger.
- **S1 — Phase 11.2** (prescriptive claim layer): full ceremony —
  `/gsd-discuss-phase` (assumptions mode + persona rounds) → `/gsd-plan-phase` →
  `/gsd-execute-phase` → code review + fix → verify → `/gsd-secure-phase` →
  `/gsd-validate-phase`. Human-verification items go to HUMAN-QUEUE, work continues.
  Prefer `/gsd-autonomous --only 11.2` as the carrier where it runs cleanly.
- **S2 — Phase 11.3** (reporting completeness): same ceremony. The missingness-rate
  reconciliation design (naive spec fires on the good fixture) is decided by a
  Statistician-led persona round: tolerance + re-baseline vs entry-condition
  deferral — decide with evidence from the fixture, record it.
- **S3 — Phase 12** (calibration, terminal): full known-bad corpus with
  catch-attribution tags, measured catch rate and false-positive rate,
  `dsx stats --paradigm`, backlog re-evaluation. The readout is reviewed by the
  Statistician persona at high effort before verification.
- **S4 — Close-out:** `/gsd-audit-uat` sweep → drain HUMAN-QUEUE (this is the one
  place the loop may block on the human) → `/gsd-extract-learnings` →
  `/gsd-audit-milestone` (must reach `passed`) → `/gsd-complete-milestone` →
  `/gsd-cleanup` (deletion approval via HUMAN-QUEUE) → `/gsd-ship`.

## 7. Target schedule (slack included)

| Dates | Stage |
|---|---|
| Aug 23–24 | S0 |
| Aug 25–26 | S1 (Phase 11.2) |
| Aug 27–28 | S2 (Phase 11.3) |
| Aug 29–30 | S3 (Phase 12) |
| Aug 31 | S4 close-out |
| Sep 1–2 | Buffer / human-queue drain |

If a stage has not started by its window's end, log a schedule-risk line in the
daily summary and apply §5's re-scope rule rather than gate-skipping.

## 8. Reporting

Every wakeup appends one ledger log line (UTC timestamp via `date`, unit, outcome,
evidence pointer). Once per day send a PushNotification: stage, units done,
persona decisions made, HUMAN-QUEUE items waiting, schedule risk, and the literal
git state (branch, ahead-of-origin count, unpushed yes/no).

## 9. Stopping

Stop the loop (ScheduleWakeup stop) when the Definition of Done at the top is met,
or when every remaining unit is blocked on HUMAN-QUEUE — in that case send a final
notification listing exactly what the human must answer to finish.
