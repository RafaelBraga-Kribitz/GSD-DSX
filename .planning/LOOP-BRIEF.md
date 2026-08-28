# LOOP-BRIEF — v2.0.0 completion ceremony (autonomous)

**Purpose:** This file is the standing contract for the **scheduled headless
firings** that finish milestone v2.0.0 (DSX Validity Frame). The work backlog
lives in `LOOP-LEDGER.md`; items only a human can answer live in
`HUMAN-QUEUE.md`.

**Hard deadline:** 2026-09-01 end of day (buffer day 2026-09-02).
**Definition of done:** every item in LOOP-LEDGER.md checked; milestone audit re-run
and `passed` (not gaps-accepted); `/gsd-complete-milestone` archived; branch pushed;
HUMAN-QUEUE.md empty or every remaining item explicitly accepted by the human.

## 0. Execution model — READ THIS FIRST, every single firing

You are one firing of a **scheduled headless run** — a fresh `claude -p` process
launched by `scripts/run-ceremony-firing.ps1` from a Windows Scheduled Task every
four hours. **You start with zero memory of every prior firing.** There is no
conversation history to recall, no earlier turn to refer back to, no "as I noted
before." The only things that persist between firings are files committed to this
git repository — principally this brief, `LOOP-LEDGER.md`, `HUMAN-QUEUE.md`, and
GSD's own per-phase state files (`STATE.md`, `PLAN.md`, `*-SUMMARY.md`, etc.).

This is deliberate, not a limitation to work around: it is the fix for the
problem that running one continuous session across a 10-day ceremony degrades
model performance as the context window fills. A fresh process per unit means the
context never accumulates in the first place — which is why this design does not
need, and must not use, `/clear`. Do not try to defeat the isolation: do not call
`ScheduleWakeup`, `CronCreate`, or any session-persistence tool from inside a
firing; those belong to interactive terminal sessions, not this one, and calling
them here does nothing useful. Your job each firing is narrow: **read state from
disk, do one bounded unit of work, write state back to disk, stop.** The next
firing is guaranteed by the operating system's scheduler, not by anything you do.

You are running on the operator's local machine, in their real working tree, with
the full GSD framework installed at `~/.claude/` (71 `gsd-*` skills, `gsd-core/`,
`gsd-tools.cjs`). That is why this runs locally rather than in a cloud sandbox —
a fresh cloud checkout of this repository contains the DSX product code but not
the GSD framework that drives the ceremony, so the skills would not resolve.

**Every firing, in order, before touching any ledger item:**
1. Read this file (`LOOP-BRIEF.md`) in full.
2. Read `LOOP-LEDGER.md` in full — including the Log section, which is your only
   memory of what happened in every prior firing.
3. Read `HUMAN-QUEUE.md` in full — an item moved to "Answered" since your last
   firing may unblock work.
4. Run `git log --oneline -15` and `git status` to see what actually landed —
   the ledger is a claim, the repo is the fact; if they disagree, trust the repo
   and correct the ledger before proceeding.

## 1. One firing = as many units as the context window (and the pacing cap) allow

Work units **back to back**, but stop at whichever of two ceilings comes first:
the context window, or the pacing cap below. Do not stop after one unit just
because it's convenient — a fresh firing costs a re-read of this brief, the
ledger and the git log before it can do anything, and paying that overhead for
a single unit wastes most of the run.

For each unit: take the **first unblocked unit** in stage order, execute it **to
completion** (including its gate), update the ledger, commit + push. Then, if
both ceilings below still allow it, immediately start the next one. A unit is
one ledger checkbox (one skill invocation or one bounded fix batch), not a
whole stage.

**Pacing cap — spread usage across the full 5-hour window, don't burst it.**
Measured behaviour: firings that just chase the context ceiling burn a whole
5-hour usage window's budget in roughly 3.5 hours, then sit blocked for the
remaining 1.5 hours until the window rolls over — net throughput lost to idle
waiting, not gained by finishing sooner. Target **at most ~12 minutes of
continuous active work per firing** (model generation + tool calls, not the
git/file-read bookkeeping at the top), then stop at the nearest safe unit
boundary even if context headroom remains. This is a starting estimate, not a
measured constant — nothing today reports real token/usage figures back into
this loop. If a human operator tells you (via a Log line or a brief update)
that the account is still exhausting its window early or, conversely, sitting
idle with headroom to spare, treat that as ground truth and adjust this number
in your own Log entry for the next firing to read — do not silently ignore
a correction like that.

**When to stop.** Stop at the first of these, whichever comes first:

- The ~12-minute pacing cap above is reached. Finish the unit you are on if
  it is close to its own safe boundary; otherwise stop at that boundary now.
- The harness warns you that context is running low or that auto-compaction is
  approaching (`context_guard_mode: warn` is enabled for this project). **Treat
  the first such warning as your stop signal** — finish the unit you are on,
  then stop. Do not keep going to squeeze in one more.
- You judge, honestly, that your remaining context is not enough to finish the
  next unit *and* its gate. Starting a unit you cannot finish well is worse than
  leaving it for a firing that can.
- Every remaining unit is blocked on `HUMAN-QUEUE.md`.

Never let auto-compaction happen mid-unit and then carry on as if nothing
changed. Compaction replaces what you actually read with a summary of it, and
this project's gates depend on exact line numbers, exact test counts and exact
citation text. A gate signed off from a summary is not a gate.

**Before stopping, always:** commit and push, append your Log line(s), and — if
you are stopping mid-unit rather than at a clean boundary — run
`Skill(skill="gsd-pause-work")` to write a proper handoff, then reference that
handoff file in your Log line so the next firing finds it immediately.

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

Cadence is set by the Scheduled Task, not self-paced — there is no
`ScheduleWakeup` available to a headless firing. **The task polls every 15
minutes.** That is not the work rhythm; it is a retry rhythm. A firing already in
progress holds a lock file, so a poll that lands while one is running exits in
about a second without doing anything. Work therefore runs effectively
back-to-back: whenever the machine is free, the next poll picks the work up
within a quarter of an hour instead of leaving hours on the floor.

This design is deliberate and was arrived at by measurement. On a 4-hour interval
with one unit per firing, the machine worked 22 minutes out of every 240 — a 9%
duty cycle — and 27 open units at that rate could not have finished inside the
milestone deadline. Short polling plus multi-unit firings (§1) is what closes
that gap. Do not "pace yourself" against some imagined budget: there is no daily
unit cap, and there deliberately isn't one.

Firings missed to sleep or shutdown are simply skipped; the next poll picks up
the same work, so a missed window costs time but never correctness. A firing that
finds every remaining unit blocked on `HUMAN-QUEUE.md` should say so in the log
and stop immediately rather than spin.

- Rate-limit / usage-window error on any tool call: do not retry in a loop. Log
  it plainly (`YYYY-MM-DDTHH:MMZ | <unit> | rate-limited, deferred | -`) and stop
  the firing. Polling every 15 minutes means the work resumes as soon as capacity
  returns, with no intervention. **This is the only pacing mechanism.** Being
  rate-limited occasionally is the expected, correct steady state for a run that
  is using its capacity properly — it is not a fault and needs no report beyond
  the Log line.

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

- **Keep the hot-path files lean — every word here is re-read on every firing.**
  `LOOP-BRIEF.md`, `LOOP-LEDGER.md` and `HUMAN-QUEUE.md` are read in full at the
  start of every single firing (§0). Measured on 2026-08-26: the ledger alone had
  grown to ~19,000 words purely from verbose per-unit evidence essays inlined on
  checkbox lines — paid again, in full, on every firing, whether or not that unit
  was relevant to what this firing is doing. Full evidence still matters for audit;
  it just does not belong in the file every firing must re-read to get oriented.
  Concretely:
  - When you check off a ledger item, write **one line** on the checkbox itself
    (what happened, gate result, pointer to commits) — not the full essay. If the
    evidence is long, put the full essay in `.planning/LOOP-LEDGER-ARCHIVE.md`
    under a `## <unit-id>` heading and leave `(full evidence: LOOP-LEDGER-ARCHIVE.md#<unit-id>)`
    on the checkbox line instead.
  - Keep the Log section to roughly the **most recent 15–20 entries**. When it grows
    past that, move the oldest entries into `LOOP-LEDGER-ARCHIVE.md` under
    `## Log (archived)`, oldest first, and leave a one-line pointer at the top of
    the active Log section noting the cutoff. Never delete history — move it.
  - Same principle for `HUMAN-QUEUE.md`'s `## Answered` section: once an item has
    been answered for more than a few firings and nothing downstream still needs
    to double-check it inline, move its full record to
    `.planning/HUMAN-QUEUE-ARCHIVE.md` and leave a one-line pointer.
  - Do this trimming as its own light unit when you notice a file has grown past
    a couple hundred lines — it pays for itself on every subsequent firing.
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
it silently and rely on the Log; the human can read `LOOP-LEDGER.md` directly,
or read the raw per-firing transcript under `.planning/loop-logs/`.

## 9. Stopping

There is no loop-control tool to call from inside a firing — the Scheduled Task is
managed from outside (the human, or an interactive session on their behalf), not
by you. When the Definition of Done at the top is met:

1. Do the final housekeeping (push everything, confirm nothing unpushed).
2. Append a Log line: `... | MILESTONE COMPLETE — stop the task with: Unregister-ScheduledTask -TaskName "GSD-DSX-v2-Ceremony" -Confirm:$false | <note>`.
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
