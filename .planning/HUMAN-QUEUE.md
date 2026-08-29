# HUMAN-QUEUE — items only you can answer

Milestone **v2.3 Test Catalog**. The loop keeps working around these; it only
blocks at the close-out stage (S5-2) if any remain.

**How to answer:** the operator is usually remote and cannot run local commands.
Answer in the session; an interactive Claude session records the verdict in the
proper GSD artifact (UAT file, SECURITY.md) and checks the item off here.

**What reaches this queue** (brief §4 — everything else the loop decides itself via
a persona round and records loudly):

1. A D-05 primary-source read — citation authenticity. The loop may prepare the
   evidence pack; it may not sign it.
2. An irreversible destructive operation (file deletion, history rewrite, force-moving
   a published tag).
3. A change to milestone scope (dropping or rewording a requirement).
4. A security sign-off (`SECURITY.md` approval line).
5. An outward-facing ship action (merge to `main`, release tag, opening a PR).

## Open

(none yet — the loop's S0-3 and S0-4 will file the Phase 18 and Phase 19 D-05
citation evidence packs here early, so the operator can read them asynchronously
while Phase 17 builds. Expect ~15–20 citation reads across the two packs — the
largest D-05 round of any milestone so far; the granularity ruling that keeps it
bounded is: one human read per new CODE, bibliographic citation per catalog ENTRY.)

## Will be added by the loop when reached

- S0-3: Phase 18 D-05 evidence pack (correlation/agreement codes + effect-size
  band sources).
- S0-4: Phase 19 D-05 evidence pack (RM/trend/categorical/resampling/post-hoc/
  negative-gate codes).
- Phase 17/18/19/20 end-of-phase security sign-off + UAT rounds (batched per
  phase; non-blocking until S5-2).
- D-06 numbering veto windows for the new codes (from the Phase 17 pre-allocated
  ranges; silence = accept).
- The S5-6 ship decisions: merge to `main` and the `v2.3.0` release tag.
- Any persona decision the operator vetoes from a daily summary.

## Standing framework notes (not queue items — nothing to answer, just remember)

**`/gsd-audit-uat`'s automated CLI under-reports human-verification items — TWO
defects.** (1) `gsd-core/bin/lib/uat.cjs::parseVerificationItems` only recognizes
a level-2 `## Human Verification` heading while the verifier template writes
level-3 `### Human Verification Required` (found v2.0.0). (2) `uat.cjs:78`
filters on `f.includes('-VERIFICATION')` while this repo's files are named
`VERIFICATION.md`, so the CLI never opens them and returns a false All Clear
(found v2.2 S5-1). **At S5-1, never accept the CLI's "all clear" — hand-check
every phase's VERIFICATION.md.**

**`/gsd-pr-branch` does not survive a long ceremony branch.** Its per-commit
cherry-pick chain hit recurring modify/delete conflicts on v2.0.0's 707-commit
branch and was abandoned mid-run. Ship by direct 3-way merge.

**Ship by EXPLICIT branch name — never the framework's auto-detect.** This repo
carries stale `gsd/*` branches from prior milestones; `/gsd-complete-milestone`'s
`handle_branches` picks the alphabetically-first `gsd/*` branch, which is wrong
here (found and bypassed at v2.2 ship). `git merge --no-ff gsd/v2.3.0-test-catalog`
by name, verified on a throwaway branch first.

**Release tags: never force-move a published one.** v2.0.0 shipped as tag
`v2.1.0` for this reason; v2.2 shipped as `v2.2.0`. The next free tag for this
milestone is `v2.3.0`.

**`/gsd-complete-milestone` output needs hand-verification.** At v2.2 close its
generated accomplishment bullets were truncated mid-sentence and the archived
REQUIREMENTS.md carried all rows forward still unchecked despite the passed
audit — both had to be hand-corrected. Also: it is NOT headless-safe
(interactive prompts + `git rm REQUIREMENTS.md`) — interactive session only.

**Run the full suite from a clean tree — a stray root `DECISIONS.jsonl`
false-fails two `explain` tests.** `tests/test_dsx.py::test_explain_missing_spec_exits_zero_not_two`
and `tests/test_explain_self_reported.py::test_returns_zero_when_spec_cannot_be_loaded`
run from repo-root CWD without isolation; any repo-root `dsx gate`/`dsx explain`
leaves a gitignored ledger that breaks them. If exactly these two fail:
`rm -f DECISIONS.jsonl examples/DECISIONS.jsonl examples/known-bad/DECISIONS.jsonl templates/DECISIONS.jsonl`
and re-run before treating it as real.

**Usage-limit backoff is the wrapper's job (operator-directed 2026-08-29).**
`scripts/run-ceremony-firing.ps1` detects limit hits in the transcript, writes
`.planning/loop-logs/.backoff-until`, skips polls until the weekly reset
(Wednesday 10:00 América/São_Paulo = 13:00 UTC; 60 minutes for a 5-hour-window
hit), then resumes by itself. Firings: log one line, stop, never retry-loop,
never touch the backoff file.

## Answered

(v2.0.0's items HQ-1…HQ-7 and v2.2's items HQ-8…HQ-15 are archived at
`.planning/milestones/v2.0.0-HUMAN-QUEUE*.md` and
`.planning/milestones/v2.2-HUMAN-QUEUE.md`. Numbering continues from HQ-16.)
