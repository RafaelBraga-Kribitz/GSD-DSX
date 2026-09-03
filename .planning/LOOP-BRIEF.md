# LOOP-BRIEF — autonomous milestone ceremony

**Current milestone: v2.4 Visual Excellence** (Phases 21–24, 16 requirements).
Branch `gsd/v2.4.0-visual-excellence`. Opened 2026-09-02 by operator direction.

**Purpose:** This file is the standing contract for the **scheduled headless
firings** that drive the current milestone to completion. The work backlog lives in
`LOOP-LEDGER.md`; items only a human can answer live in `HUMAN-QUEUE.md`.

**Predecessors — all driven end-to-end by this same brief:** v2.3 Test Catalog
SHIPPED 2026-09-02 (tag `v2.3.0`, 4 phases / 11 plans, audit `passed`, 27 D-05
citations independently re-verified — 7 corrected); v2.2 Analytic Surface
SHIPPED 2026-08-29 (tag `v2.2.0`); v2.0.0 DSX Validity Frame SHIPPED 2026-08-28
(tag `v2.1.0`). Ledgers and queues archived under `.planning/milestones/v2.3-*`,
`v2.2-*`, `v2.0.0-*`.

**Scope source:** `.planning/research/V2.3-V2.4-SCOPE.md` §3 (2026-08-29) —
research provenance, per-source citations, license audit findings, and the
critique register. The scope was researched at v2.3's open and re-verified
against the live tree at v2.4's own open (2026-09-02): `dsx/checks/viz.py`
untouched since before v2.3; catalogue confirmed at 275. **This milestone does
not need a fresh scoping round; it needs execution.**

**Definition of done:** every item in LOOP-LEDGER.md checked; milestone audit run and
`passed` (not gaps-accepted); `/gsd-complete-milestone` archived; branch merged to
`main` **by explicit name** and tagged `v2.4.0`; HUMAN-QUEUE.md empty or every
remaining item explicitly accepted by the operator.

**Why this project's standard is high — read once, then hold it.** This repository is
a portfolio artifact: it is expected to be read by technically capable, sceptical data
scientists and statisticians who will check the claims. That makes the *defensible*
route the required one, not the ambitious one. Concretely, and non-negotiably:
a citation is confirmed at its locator or it does not ship; a gate is re-run by the
orchestrator rather than trusted from a subagent's report; a number in a readout is
measured, never estimated into existence; and an honest "this is unverified" or "this
class is structurally uncatchable" is worth more than a claim that merely looks
complete. Prefer the smaller, provable claim every time.

## 0. Execution model — READ THIS FIRST, every single firing

You are one firing of a **scheduled headless run** — a fresh `claude -p` process
launched by `scripts/run-ceremony-firing.ps1` from a Windows Scheduled Task that
polls every 15 minutes. **You start with zero memory of every prior firing.** The
only things that persist between firings are files committed to this git
repository — principally this brief, `LOOP-LEDGER.md`, `HUMAN-QUEUE.md`, and GSD's
own per-phase state files.

This is deliberate: a fresh process per unit is the fix for context degradation
across a multi-day ceremony. Do not try to defeat the isolation: no
`ScheduleWakeup`, no `CronCreate`, no session-persistence tools — the next firing
is guaranteed by the OS scheduler, not by anything you do. Your job each firing is
narrow: **read state from disk, do bounded work, write state back to disk, stop.**

You are running on the operator's local machine, in their real working tree, with
the full GSD framework installed at `~/.claude/` — that is why this runs locally
rather than in a cloud sandbox.

**Every firing, in order, before touching any ledger item:**
1. Read this file (`LOOP-BRIEF.md`) in full.
2. Read `LOOP-LEDGER.md` in full — the Log section is your only memory.
3. Read `HUMAN-QUEUE.md` in full — an item answered since the last firing may
   unblock work.
4. Run `git log --oneline -15` and `git status` — the ledger is a claim, the repo
   is the fact; if they disagree, trust the repo and correct the ledger first.

## 1. One firing = as many units as the context window (and the pacing cap) allow

Work units **back to back**, but stop at whichever ceiling comes first: the
context window, or the pacing cap below. For each unit: take the **first
unblocked unit** in stage order, execute it **to completion** (including its
gate), update the ledger, commit + push, then start the next if the ceilings
allow. A unit is one ledger checkbox, not a whole stage.

**Pacing cap — spread usage across the 5-hour window, don't burst it.** Target
**at most ~12 minutes of continuous active work per firing**, then stop at the
nearest safe unit boundary. This is a tunable estimate; if the operator corrects
it via a Log line, treat that as ground truth.

**When to stop.** First of: the ~12-minute cap; a context-low warning (treat the
first warning as the stop signal — finish the current unit, then stop); your
honest judgment that remaining context cannot finish the next unit AND its gate;
every remaining unit blocked on `HUMAN-QUEUE.md`.

Never let auto-compaction happen mid-unit and carry on — gates here depend on
exact line numbers, test counts and citation text; a gate signed off from a
summary is not a gate.

**Before stopping, always:** commit and push, append your Log line(s); if
stopping mid-unit, run `Skill(skill="gsd-pause-work")` and reference the handoff
in the Log line. If a unit is too large for one firing, stop cleanly at a safe
boundary — GSD's own STATE/PLAN tracking is resumable; write down exactly where
you stopped.

**If you find uncommitted changes in the working tree at the start of a firing**
that don't match the ledger's claimed state (e.g. an interactive session's
in-progress close-out work): do NOT commit them and do NOT discard them. Leave
them exactly as found, note it in your Log line, and hold — this is the
operator's in-progress work, not yours to finalize or destroy. (Observed for
real at v2.3's close: a firing correctly detected and held rather than
interfering with a concurrent interactive `/gsd-complete-milestone` run.)

## 2. Cadence and the usage-limit backoff

The Scheduled Task polls every 15 minutes — a retry rhythm, not a work rhythm; a
lock file makes overlapping polls exit in a second, so work runs effectively
back-to-back whenever the machine is free. Firings missed to sleep/shutdown are
simply skipped; a missed window costs time, never correctness.

**Usage limits: the wrapper owns limit pacing — you own nothing about it except
honesty.** Proven in production across v2.3 (2026-08-30 through 2026-09-02): the
weekly-reset backoff self-healed once, and the periodic early-release probe
(every 30 minutes during a hold) caught and self-recovered from four separate
5-hour-window hits, each resolved in 2–7 minutes.

- Inside a firing: on a rate-limit / usage-window error on any tool call, do NOT
  retry in a loop. Append one Log line
  (`YYYY-MM-DDTHH:MMZ | <unit> | rate-limited, deferred | -`), commit+push if
  anything changed, and stop the firing. Being limited occasionally is the
  expected steady state of a run using its capacity properly — it is not a fault.
- Never edit or delete `.planning/loop-logs/.backoff-until` or
  `.backoff-last-probe` yourself; they are the wrapper's files.

A firing that finds every remaining unit blocked on `HUMAN-QUEUE.md` says so in
the Log once and stops; later firings in the same all-blocked state do a TRUE
no-op (no duplicate hold lines).

## 3. Model and effort routing

GSD's `model_profile: adaptive` routes GSD subagents — do not override it. For
direct `Agent` spawns and effort choices:

| Work | Model | Effort |
|---|---|---|
| Mechanical doc fixes (traceability rows, frontmatter, progress tables) | haiku | low |
| Plan execution, test writing, fix application | profile default (sonnet-class) | medium |
| Discuss persona rounds, planning, plan-check, verification, code review | opus | high |
| Milestone audit, adversarial statistical review, catch-rate/FPR readouts | fable (Agent model override) or opus | high/max |

Rule: never spend opus/fable on checklist work; never let a sonnet-class agent
make an irreversible design decision alone.

## 4. Expert persona protocol (answer your own questions)

For every gray-area decision, run an internal advisor round instead of asking the
human. Panel (spawn only the relevant 2–3): **Architect** (`dsx-analysis-architect`),
**Statistician** (`dsx-statistician`), **Auditor** (`gsd-security-auditor` /
`dsx-ml-integrity-auditor`), **Advisor** (`gsd-advisor-researcher`). Each persona
proposes, questions itself, answers, votes; the orchestrator picks, breaking ties
by **rigour > reliability > flexibility**; decision + rationale recorded in the
phase CONTEXT.md and one ledger line. Loud, never silent.

Escalate to HUMAN-QUEUE.md **only** for:
1. A D-05 human source read (personas may prepare evidence packs, never sign them).
2. An irreversible destructive operation.
3. A change to milestone scope (dropping or rewording a requirement).
4. A security sign-off (`SECURITY.md` approval line).
5. An outward-facing ship action (merge to `main`, release tag, opening a PR).

D-06 numeric code assignments are persona-round decisions ("next free number in
family — verify the live catalogue count first, do not assume 275"), recorded
loudly with a veto window, NOT escalated.

**No one is watching — never wait on `AskUserQuestion` or interactive prompts.**
Drive skills with the safe default: continue past advisory prompts, never past a
prompt that exists because a quality gate failed (that is a blocker or a
HUMAN-QUEUE item).

## 5. Non-negotiable ground rules

- **Keep the hot-path files lean** — this brief, the ledger and the queue are
  re-read every firing. One line per checked-off checkbox (evidence pointer, not
  essay); long evidence goes to `LOOP-LEDGER-ARCHIVE.md` under `## <unit-id>`;
  keep the Log to the most recent ~15–20 entries (archive older, never delete);
  same for the queue's Answered section. Trim as a light unit when a file passes
  a couple hundred lines.
- Never mark a ledger item done without its verifying gate actually passing —
  paste real evidence.
- Tracking files (REQUIREMENTS.md, STATE.md, ROADMAP.md) are single-writer:
  orchestrator only, never subagents.
- Windows CRLF: any line-start/end regex uses `\r?\n`.
- After every commit, push. Every daily summary ends with the literal git state.
- Gate failure: one repair attempt, then record the blocker and move to the next
  non-dependent unit. Never loop on a failing gate.
- Never skip verification, security, or Nyquist gates to save time. If schedule
  is at risk, shrink scope via a recorded, consented re-scope — rigour is not the
  variable.
- **v2.4-specific standing rules:** every new gate check needs D-05 (citation +
  published reference value); license audit is a plan-review item for the style
  layer, never an afterthought (no GPL ports of bbplot, no embedding the
  unlicensed Economist styleguide PDF — cite, never vendor); the catalog's
  perceptual tie-break ordering is asserted as a structural criterion against
  the published Cleveland–McGill ranking, never computed; the SVG determinism
  recipe is proven by a double-render hash-equality test kept OFF the gate path.

## 6. Stages (execute in stage order)

The authoritative stage/unit list is `LOOP-LEDGER.md`. Orientation summary:

- **S0 — Bootstrap.** Verify state pointing; re-verify the inherited scope
  against the live tree (viz.py vocabulary, live catalogue count); file the
  Phase 22 D-05 citation evidence pack EARLY so the operator reads
  asynchronously while Phase 21 builds.
- **S1 — Phase 21** (viz vocabulary reconciliation) — full ceremony: discuss →
  plan → execute → review/verify → secure/validate. Hard-blocks S2.
- **S2 — Phase 22** (catalog spine, uncertainty family, selection heuristic) —
  same ceremony. Carries the milestone's D-05 load.
- **S3 — Phase 23** (style and snippet layer) — same ceremony. Light D-05 load;
  license audit is its own plan-review item.
- **S4 — Phase 24** (portfolio exemplar and viz calibration) — same ceremony;
  terminal by design, exercises both v2.3 and v2.4.
- **S5 — Close-out:** `/gsd-audit-uat` (hand-checked — known CLI under-reporting
  defects) → drain HUMAN-QUEUE → `/gsd-extract-learnings` →
  `/gsd-audit-milestone` (must reach `passed`) → `/gsd-complete-milestone`
  (interactive session — NOT headless-safe) → ship by **explicit named** direct
  merge + `v2.4.0` tag (never the framework's alphabetical branch auto-detect;
  this repo now has five stale `gsd/*` branches it would pick instead).

Phases run in numeric order this milestone (21 → 22 → 23 → 24): 21 is the
foundation the catalog spine builds on, 24 is terminal and consumes both v2.3
and v2.4's surfaces.

## 7. Pacing

No fixed per-stage calendar. Work the ledger in order; log a schedule-risk line
when a phase visibly overruns its neighbours. The usage-limit backoff (§2) is
proven working; expect occasional short holds, not multi-day stalls.

## 8. Reporting

The git-committed `LOOP-LEDGER.md` Log is the primary, durable reporting channel.
Format: `YYYY-MM-DDTHH:MMZ | unit | outcome | evidence pointer`. If a
`PushNotification` tool is available, one summary per UTC day (first firing after
00:00Z): stage, units done, persona decisions, HUMAN-QUEUE items waiting,
schedule risk, literal git state. If absent, skip silently.

## 9. Stopping

When the Definition of Done is met: push everything, append
`... | MILESTONE COMPLETE — stop the task with: Unregister-ScheduledTask -TaskName "GSD-DSX-v2-Ceremony" -Confirm:$false | <note>`,
send the notification if available, and stop. Every later firing: two-second
no-op (read Log, see completion, log `already complete, no-op`, stop).

If every remaining unit is blocked on HUMAN-QUEUE (not done, just stuck): log it
once plainly and stop; later firings in the same state do a true no-op.
