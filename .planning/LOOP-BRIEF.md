# LOOP-BRIEF — v2.0.0 completion ceremony (autonomous)

**Purpose:** This file is the standing contract for the **cloud routine** that
finishes milestone v2.0.0 (DSX Validity Frame). The work backlog lives in
`LOOP-LEDGER.md`; items only a human can answer live in `HUMAN-QUEUE.md`.

**Hard deadline:** 2026-09-01 end of day (buffer day 2026-09-02).
**Definition of done:** every item in LOOP-LEDGER.md checked; milestone audit re-run
and `passed` (not gaps-accepted); `/gsd-complete-milestone` archived; branch pushed;
HUMAN-QUEUE.md empty or every remaining item explicitly accepted by the human.

## 0. Execution model — READ THIS FIRST, every single firing

You are one firing of a **recurring cloud routine** (Claude Code cloud session,
created via `/schedule`). **You start with zero memory of every prior firing.**
There is no conversation history to recall, no earlier turn to refer back to, no
"as I noted before." The only things that persist between firings are files
committed to this git repository — principally this brief, `LOOP-LEDGER.md`,
`HUMAN-QUEUE.md`, and GSD's own per-phase state files (`STATE.md`, `PLAN.md`,
`*-SUMMARY.md`, etc.).

This is deliberate, not a limitation to work around: it is the fix for the
problem that running one continuous session across a 10-day ceremony degrades
model performance. Do not try to defeat it — do not attempt to call
`ScheduleWakeup`, `CronCreate`, or any session-persistence tool from inside a
routine firing; those belong to interactive terminal sessions, not this one, and
calling them here does nothing useful. Your job each firing is narrow: **read
state from disk, do one bounded unit of work, write state back to disk, stop.**
The next firing is guaranteed by the cloud scheduler, not by anything you do.

**Every firing, in order, before touching any ledger item:**
1. Read this file (`LOOP-BRIEF.md`) in full.
2. Read `LOOP-LEDGER.md` in full — including the Log section, which is your only
   memory of what happened in every prior firing.
3. Read `HUMAN-QUEUE.md` in full — an item moved to "Answered" since your last
   firing may unblock work.
4. Run `git log --oneline -15` and `git status` to see what actually landed —
   the ledger is a claim, the repo is the fact; if they disagree, trust the repo
   and correct the ledger before proceeding.

## 1. One firing = one unit

Pick the **first unblocked unit** in stage order, execute it **to completion**
(including its gate), update the ledger, commit + push, then **stop**. Do not
start a second heavy unit in the same firing — let the scheduler bring the next
one. A unit is one ledger checkbox (one skill invocation or one bounded fix
batch), not a whole stage.

**If a unit is too large to finish in one firing** (a long `gsd-execute-phase`
run that is still going when you are running low on turn budget): do not force
it to completion by cutting corners. Stop cleanly at a safe boundary, leave the
ledger checkbox unchecked, add a one-line log entry noting exactly where you
stopped and which GSD state file records the sub-progress (GSD's own
`STATE.md`/`PLAN.md` tracking is resumable — that is what makes this safe), and
push whatever is committed. The next firing will read that log line, see the
GSD-native state is mid-phase, and resume the same unit rather than restarting
it — it does not need you to have remembered anything, only to have written it
down.

## 2. Cadence

Cadence is fixed by the cloud routine's cron schedule, not self-paced — there is
no `ScheduleWakeup` available inside a routine firing. The routine fires every
4 hours (6×/day). Most firings will do exactly one unit and stop; a firing that
finds every remaining unit blocked on `HUMAN-QUEUE.md` should say so in the log
and stop immediately rather than spin.

- Rate-limit / usage-window error on any tool call: do not retry in a loop. Log
  it plainly (`YYYY-MM-DDTHH:MMZ | <unit> | rate-limited, deferred | -`) and stop
  the firing — the next scheduled firing will pick the same unit back up.
- Soft budget: at most ~2 phase-scale units per calendar day even though the
  cadence allows more firings — the schedule in §7 has slack; do not burn quota
  running ahead of it. A firing that finds today's soft budget already spent
  (check the Log for today's date) should log `budget reached for today, no-op`
  and stop.

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

**No one is watching this session in real time — never wait on `AskUserQuestion`
or any interactive confirmation.** This is a headless cloud firing; a GSD skill
that would normally pause for one (audit gaps/tech-debt routing,
`gsd-cleanup`'s dry-run approval, etc.) must instead be driven with the safe
default: continue past advisory/non-blocking prompts, but never past a prompt
that exists because a quality gate actually failed — that case is a blocker
(§5) or a HUMAN-QUEUE item (the four categories above), not a default-through.
If a skill invocation truly cannot proceed without a live answer, treat it as a
blocker for this unit: log it, leave the checkbox unchecked, and move to the
next unblocked unit rather than stalling the firing.

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

The git-committed `LOOP-LEDGER.md` Log is the primary and durable reporting
channel — it is the only thing guaranteed to survive between firings, so treat
every log line as if it were the sole record a human will ever see of this
firing. Format: `YYYY-MM-DDTHH:MMZ | unit | outcome | evidence pointer`.

If a `PushNotification` tool is available in this session, use it once per
UTC day (only on the first firing after 00:00Z, checked against the Log) to
summarize: stage, units done, persona decisions made, HUMAN-QUEUE items
waiting, schedule risk, and the literal git state (branch, ahead-of-origin
count, unpushed yes/no). Do not depend on this — if the tool is absent, skip
it silently and rely on the Log; the human can read `LOOP-LEDGER.md` directly
or run `RemoteTrigger get_run_log` on this routine from an interactive session.

## 9. Stopping

There is no loop-control tool to call from inside a firing — the routine is
managed from outside (the human, or an interactive session on their behalf),
not by you. When the Definition of Done at the top is met:

1. Do the final housekeeping (push everything, confirm nothing unpushed).
2. Append a Log line: `... | MILESTONE COMPLETE — recommend disabling this routine | <link or note>`.
3. If `PushNotification` is available, send one final summary.
4. Stop. Every firing after this point should be a two-second no-op: read the
   Log, see the completion line with no newer work below it, log
   `... | already complete, no-op | -`, and stop — do not re-open finished
   stages looking for more to do.

If every remaining unit is blocked on `HUMAN-QUEUE.md` (not the Definition of
Done, just genuinely stuck): log that plainly, send the notification if
available, and stop the same way. The next firing checks `HUMAN-QUEUE.md`
fresh — if it is still all-open, it does the same and stops again; this is a
correct, low-cost holding pattern, not a bug.
