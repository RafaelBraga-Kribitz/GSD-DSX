# LOOP-BRIEF — autonomous milestone ceremony

**Current milestone: v2.6 Exploration Depth and Backlog Evidence** (Phases 25–30,
18 requirements). Branch `gsd/v2.6.0-exploration-depth`. Opened 2026-09-06 by
operator direction (HQ-39): scope = the EDA brief's gated half (SEED-002) plus the
per-skill read contracts (SEED-001 E-26), then the three corpus evidence cases the
project's engagement with *The AI Data Scientist* left on the gated backlog
(brief §6.5 items 7, 8, 9), then a terminal calibration re-baseline.

**Purpose:** This file is the standing contract for the **scheduled headless
firings** that drive the current milestone to completion. The work backlog lives in
`LOOP-LEDGER.md`; items only a human can answer live in `HUMAN-QUEUE.md`.

**Predecessors — all driven end-to-end by this same brief unless noted:** v2.4 Visual
Excellence SHIPPED 2026-09-03 (tag `v2.4.0`, 4 phases / 11 plans, audit `passed`);
v2.4.1 and v2.5.0 SHIPPED 2026-09-06 interactively (metric-direction fix; every
`DSX-VIZ-*` code given a fixture, installer self-test fixed, literature record); v2.3
Test Catalog SHIPPED 2026-09-02 (tag `v2.3.0`); v2.2 SHIPPED 2026-08-29 (`v2.2.0`);
v2.0.0 SHIPPED 2026-08-28 (`v2.1.0`). Ledgers and queues archived under
`.planning/milestones/v2.4-*`, `v2.3-*`, `v2.2-*`, `v2.0.0-*`.

**Scope source:** `.planning/research/V2.6-SCOPE.md` (2026-09-06) and
`.planning/REQUIREMENTS.md` (REQ-P25-01 … REQ-P30-03). The scope was written
against the live tree the same day the milestone opened (profiler keys, explore-skill
step numbers, corpus counts 39 known-bad / 15 good-control, catalogue 276, §6.5 rows
7–9 verbatim). S0-2 re-verifies it before any planning. **This milestone needs
execution, not a fresh scoping round.**

**Definition of done:** every item in LOOP-LEDGER.md checked; milestone audit run and
`passed` (not gaps-accepted); `/gsd-complete-milestone` archived; branch merged to
`main` **by explicit name** and tagged `v2.6.0`; HUMAN-QUEUE.md empty or every
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

**The one rule that shapes this whole milestone (D-13, restated for Phases 27–29):**
each evidence phase begins by BUILDING the corpus case and MEASURING it live at all
four gate points. A case the existing gate already catches means the §6.5 entry
condition is **not** met: the phase records that, with the measured codes, and mints
nothing — that outcome satisfies the requirement. Never widen, weaken or re-shape a
case to manufacture a miss; a promoted item must be earned by a real, documented gap.

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
rather than in a cloud sandbox. The pause switch `.planning/loop-logs/.paused` is
the operator's; never create or delete it.

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
operator's in-progress work, not yours to finalize or destroy. Operator-local
untracked files (`.claude/*`, `.vscode/`, `graphify-out/`, `references/The AI Data
Scientist.md`, a leftover `.claude/worktrees/*`) are always left untouched.

## 2. Cadence and the usage-limit backoff

The Scheduled Task polls every 15 minutes — a retry rhythm, not a work rhythm; a
lock file makes overlapping polls exit in a second, so work runs effectively
back-to-back whenever the machine is free. Firings missed to sleep/shutdown are
simply skipped; a missed window costs time, never correctness.

**Usage limits: the wrapper owns limit pacing — you own nothing about it except
honesty.** Proven in production across v2.3 and v2.4: the weekly-reset backoff
self-healed, and the periodic early-release probe (every 30 minutes during a hold)
caught and self-recovered from separate 5-hour-window hits, each resolved in
minutes.

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
family — verify the live catalogue count first, do not assume 276"), recorded
loudly with a veto window, NOT escalated. A reserved-but-unminted number for a
miss sidecar's `absent_code` is the same kind of decision, recorded the same way.

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
- Windows CRLF: any line-start/end regex uses `\r?\n`. The real Python is
  `C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`; a bare
  `python3` on this machine can resolve to a package-less stub that reports the
  matplotlib determinism test as skipped — run the full suite on the real one.
- After every commit, push. Every daily summary ends with the literal git state.
- Gate failure: one repair attempt, then record the blocker and move to the next
  non-dependent unit. Never loop on a failing gate.
- Never skip verification, security, or Nyquist gates to save time. If schedule
  is at risk, shrink scope via a recorded, consented re-scope — rigour is not the
  variable.
- **v2.6-specific standing rules:**
  - **The profiler is a producer, not a gate (D-01/D-02).** `dsx profile` may
    compute anything stdlib can; no gate reads a new profile key this milestone.
    `dsx/checks/dq.py` and the `data[].assertions` vocabulary are frozen; growing
    them is a separate, later decision with its own D-06 mint. Phases 25, 26 and
    30 mint zero codes (set-identity 276 → 276, re-measured live).
  - **Existing profile keys and values are byte-stable.** The committed example
    profiles (`examples/good-DATA-PROFILE.yaml`, `examples/bad-DATA-PROFILE.yaml`)
    must regenerate identically on every existing key; new keys are additive. Two
    runs on the same extract are byte-identical.
  - **Every statistic the profiler emits is a declared definition with a cited
    source and a reference-value test** (the quantile method above all — name the
    Hyndman & Fan type that `statistics.quantiles` implements, verified at plan,
    not assumed). Hand-computed fixture CSVs are the reference values.
  - **Skill and template edits are mirrored by `node install.mjs`**, and
    `node install.mjs --check` must pass at the end of every phase that touches
    `skills/`, `agents/`, `templates/` or `references/` — the installed copies
    drifted silently for two weeks before 2026-09-06.
  - **Evidence phases (27–29) obey D-13 as stated at the top of this brief.** A
    corpus case is measured before any check is designed; a case caught by an
    existing code is recorded and closes the phase without a mint. Every new
    fixture needs its entries in `_EXPECTED_CAUGHT_DEFECTS`, the golden ship ledger
    (`tests/test_causal_verb_golden.py`), `_EXPECTED_VAL_CODES`
    (`tests/test_frame_val.py`), the spec count in `tests/test_dsx.py` (42 today),
    and — for a miss — an ATTRIBUTION sidecar whose `absent_code` is a catalogue
    code or a number reserved in `_SECTION_65_BACKLOG_CODES` and whose
    `promotes_backlog_item` is the matching `6.5-item-N-…` id.
  - **D-05 for any minted code:** citation + structural criterion in the docstring,
    a `# D-05:` test marker, and the exact code added to
    `_D05_ALLOWLIST_CODES` in `scripts/gen-finding-catalogue.py`. Candidate sources
    named in the scope document are UNVERIFIED until a human read closes the
    HUMAN-QUEUE item; the loop prepares the evidence pack at S0-3.

## 6. Stages (execute in stage order)

The authoritative stage/unit list is `LOOP-LEDGER.md`. Orientation summary:

- **S0 — Bootstrap.** Verify state pointing; re-verify the scope against the live
  tree (profiler keys, explore-skill step ids, corpus counts, catalogue count,
  §6.5 rows); file the D-05 citation evidence pack for the whole milestone EARLY
  so the operator reads asynchronously while Phase 25 builds.
- **S1 — Phase 25** (hermetic profile depth) — full ceremony: discuss → plan →
  execute → review/verify → secure/validate. Hard-blocks S2.
- **S2 — Phase 26** (per-skill read contracts) — same ceremony; skill-only, zero
  codes, installer sync is its own gate.
- **S3 — Phase 27** (evidence case: feature-origin-only leak) — same ceremony;
  D-13 measured-first rule.
- **S4 — Phase 28** (evidence case: magnitude no test computed) — same.
- **S5 — Phase 29** (evidence case: subgroup harm under a prescriptive
  recommendation) — same; carries the milestone's heaviest D-05 read.
- **S6 — Phase 30** (calibration re-baseline, terminal) — same ceremony; re-measures
  the headline pair and every stratum with the new cases classified.
- **S7 — Close-out:** `/gsd-audit-uat` (hand-checked — known CLI under-reporting
  defects) → drain HUMAN-QUEUE → `/gsd-extract-learnings` →
  `/gsd-audit-milestone` (must reach `passed`) → `/gsd-complete-milestone`
  (interactive session — NOT headless-safe) → ship by **explicit named** direct
  merge + `v2.6.0` tag (never the framework's alphabetical branch auto-detect;
  this repo now has six stale `gsd/*` branches it would pick instead).

Phases run in numeric order (25 → 26 → 27 → 28 → 29 → 30): 25 produces the keys 26
consumes; 27–29 are independent of each other but sequential on one branch; 30 is
terminal and re-baselines everything.

**Pre-agreed contingency:** if the D-05 queue for Phases 28–29 materially outruns
the ceremony cadence, split Phases 28–30 off as v2.7 by a recorded re-scope — the
profiler and read contracts need almost no human reads and should not be blocked
behind the evidence-case sources.

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
