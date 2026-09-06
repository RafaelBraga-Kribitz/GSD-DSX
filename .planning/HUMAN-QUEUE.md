# HUMAN-QUEUE — items only you can answer

Milestone **v2.6 Exploration Depth and Backlog Evidence**. The loop keeps working
around these; it only blocks at the close-out stage (S7-2) if any remain.

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

(none yet — S0-3 will file the v2.6 D-05 citation evidence pack as HQ-40.)

## Will be added by the loop when reached

- S0-3: the v2.6 D-05 citation evidence pack (Hyndman & Fan 1996 quantile type;
  Kaufman et al. 2012 legitimacy condition; Wilkinson & TFSI 1999 / APA JARS–Quant
  2018; Gail & Simon 1985 qualitative interaction). Non-blocking for Phases 25–26;
  blocks S3-1, S4-1 and S5-1 for the rows each phase's code would cite.
- Phase 25/26/27/28/29/30 end-of-phase security sign-off + UAT rounds (batched per
  phase; non-blocking until S7-2).
- D-06 numbering veto windows for any code Phases 27–29 mint, and for any number
  reserved in `_SECTION_65_BACKLOG_CODES` for a miss sidecar (from a freshly
  re-measured live catalogue count; silence = accept).
- Phase 29's documented subgroup-harm case source, if research finds one whose
  authenticity needs a human read.
- The S7-6 ship decisions: merge to `main` and the `v2.6.0` release tag, together
  with the S7-5 interactive-complete step, after S7-4's audit PASSES.
- Any persona decision the operator vetoes from a daily summary.

## Standing framework notes (not queue items — nothing to answer, just remember)

**`/gsd-audit-uat`'s automated CLI under-reports human-verification items —
multiple documented defects.** (1) `gsd-core/bin/lib/uat.cjs::parseVerificationItems`
only recognizes a level-2 `## Human Verification` heading while the verifier
template writes level-3 `### Human Verification Required` (found v2.0.0).
(2) `uat.cjs:78` filters on `f.includes('-VERIFICATION')`, which matches this
project's `NN-VERIFICATION.md` naming but not a bare `VERIFICATION.md` — check
which convention the current milestone's phases use before trusting the CLI's
file discovery. (3) The frontmatter-status gate only emits a verification file
when `status ∈ {human_needed, gaps_found}`; a phase whose VERIFICATION.md
carries `verdict: PASSED` with no `status:` key resolves to `status:unknown`
and is silently dropped (found v2.3 S5-1). **At S7-1, never accept the CLI's
"all clear" — hand-check every phase's verification file directly.**

**`check.decision-coverage-plan` false-blocks on this project's CONTEXT.md
decision-bullet style (found v2.3 S1-2).** The plan-phase decision-coverage
gate's regexes expect `- **D-NN:** …` (colon-immediate) or an em-dash inside
the bold; this project's discuss rounds write `- **D-06 range
pre-allocation** — one …` (title inside the bold, separator after the closing
`**`), matching none of the regexes → `total:0, reason:"could-not-parse"`. This
is a parser format-mismatch, **not** an uncovered decision — the
`gsd-plan-checker`'s Dimension-7 (Context Compliance) substantively verifies the
same property. **At every phase plan gate, do NOT treat a could-not-parse/
total:0 result as a real coverage gap** — confirm via the plan-checker Dim-7
pass instead.

**`init.manager`'s `verification_status` can read "missing" for a genuinely
verified phase (found v2.3 close-out; confirmed again at v2.4's).** Same class of
naming-convention blind spot as the audit-uat issues, on a different code path. If
it happens again, read the actual verification file directly before treating it as
a real gap.

**`/gsd-pr-branch` does not survive a long ceremony branch.** Its per-commit
cherry-pick chain hit recurring modify/delete conflicts on v2.0.0's 707-commit
branch and was abandoned mid-run. Ship by direct 3-way merge.

**Ship by EXPLICIT branch name — never the framework's auto-detect.** This repo
now carries six stale `gsd/*` branches from prior milestones (`v1.1.0-milestone`,
`v2.0.0-dsx-validity-frame`, `v2.0.0-milestone`, `v2.2.0-analytic-surface`,
`v2.3.0-test-catalog`, `v2.4.0-visual-excellence`); `/gsd-complete-milestone`'s
`handle_branches` picks the alphabetically-first `gsd/*` branch, which is always
wrong here (found and bypassed at v2.2, v2.3 and v2.4 ship).
`git merge --no-ff gsd/v2.6.0-exploration-depth` by name, verified on a throwaway
branch first.

**`gsd-tools query commit` (used by GSD planner/researcher/executor subagents)
auto-creates the wrong branch mid-run — recurring, budget for it.** Confirmed
three times in v2.4: when a `gsd-*` subagent commits via `gsd-tools query commit`,
it can create + switch to a stray branch (v2.4's was `gsd/v2.4-visual-excellence`,
**no `.0`**) and land the commit there instead of the canonical branch; the
subagent's own return then confidently **misreports** the branch/push state.
**After ANY subagent that may commit, the orchestrator must reconcile against the
repo, not the report:** `git rev-parse --abbrev-ref HEAD` + `git branch -vv`; if a
stray branch holds the work, it is a linear descendant of canonical →
`git checkout` canonical → `git merge --ff-only <stray>` (no commit lost) →
`git branch -d`/`-D` the stray → push; verify tree-hash identity /
`git merge-base --is-ancestor` before deleting. This is exactly why the loop uses
plain `git commit` for orchestrator-authored files, and why the `gsd/*` count must
be re-asserted (6 stale + 1 active) every planning firing.

**Release tags: never force-move a published one.** v2.0.0 shipped as tag
`v2.1.0` for this reason; v2.2 as `v2.2.0`; v2.3 as `v2.3.0`; v2.4 as `v2.4.0`;
`v2.4.1` and `v2.5.0` were interactive releases. The next free tag for this
milestone is `v2.6.0`.

**`/gsd-complete-milestone` output needs hand-verification — recurring at every
close so far.** At v2.2's, v2.3's and v2.4's close, its generated accomplishment
bullets were truncated mid-sentence or captured YAML frontmatter instead of
prose, STATE.md's generated body contradicted its own frontmatter, and the
archived REQUIREMENTS.md carried all rows forward still unchecked despite the
passed audit — all needed hand-correction each time. Budget for this as a standing
cost, not a surprise. Also: it is NOT headless-safe (interactive prompts +
`git rm REQUIREMENTS.md`) — interactive session only.

**Run the full suite from a clean tree, on the real interpreter.** A stray root
`DECISIONS.jsonl` false-fails two `explain` tests
(`tests/test_dsx.py::test_explain_missing_spec_exits_zero_not_two`,
`tests/test_explain_self_reported.py::test_returns_zero_when_spec_cannot_be_loaded`);
if exactly these two fail: `rm -f DECISIONS.jsonl examples/DECISIONS.jsonl
examples/known-bad/DECISIONS.jsonl templates/DECISIONS.jsonl` and re-run. A bare
`python3` on this machine can resolve to a package-less stub (Python 3.14.6) that
reports the matplotlib determinism test as *skipped*; the real interpreter is
`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`.

**`node install.mjs --check` is now a real gate (fixed in v2.5.0).** Before
2026-09-06 its self-test ran `gate ship` alone and had failed on every fresh install
since Phase 10, and the installer shipped the gitignored `examples/DECISIONS.jsonl`
into the overlay; both fixed. Installed skill/agent copies had silently drifted
from the repo for two weeks. Every phase that touches `skills/`, `agents/`,
`templates/` or `references/` ends with `node install.mjs` and a passing `--check`.

**Usage-limit backoff is the wrapper's job — proven working in production.**
`scripts/run-ceremony-firing.ps1` detects limit hits, writes
`.planning/loop-logs/.backoff-until`, and re-probes every 30 minutes during a
hold with one trivial `claude -p` call to catch an early release rather than
blindly waiting the full window. Firings: log one line, stop, never retry-loop,
never touch the backoff/probe-marker files. The pause switch
`.planning/loop-logs/.paused` is the operator's; the loop never creates or removes it.

**A firing that finds uncommitted, ledger-inconsistent changes at start should
hold, not act.** Confirmed working at v2.3's close: a firing found an
interactive session's in-progress `/gsd-complete-milestone` work uncommitted in
the tree and correctly left it untouched (neither committed nor discarded),
logging the observation instead. This is the correct behavior, not a bug to fix.

## Answered

### HQ-39 — v2.6 scope: open the milestone with both halves (answered 2026-09-06 — operator direction; reverses HQ-38)

**Operator verdict: "Both: EDA depth + paper evidence."** Asked after the operator
directed that the ceremony run rather than stay paused. Three options were offered
in the decision-block shape: both halves (~6 phases), EDA depth only (~3), paper
evidence only (~4). The operator chose both. Consequences, all recorded:

- **SEED-002 promoted** (Phase 25) — this reverses **HQ-38**, answered hours earlier
  the same day, which had held the seed on its unmet D-13 entry condition. The
  reversal is by operator direction with a stated reason (the portfolio work starting
  now should consume hash-bound numbers from its first phase rather than produce the
  evidence first); the seed carries both decisions in order.
- **SEED-001 E-26 promoted** (Phase 26), its entry condition likewise overridden by
  direction; E-27 … E-31 unchanged.
- **§6.5 items 7, 8, 9 get their corpus cases built and measured** (Phases 27–29)
  under the brief's D-13 rule: a case the gate already catches closes its phase with
  no mint. Nothing is promoted by this answer; only the evidence is commissioned.
- Terminal calibration re-baseline (Phase 30). Ships as `v2.6.0`.

Recorded in `.planning/research/V2.6-SCOPE.md`, `REQUIREMENTS.md`, the seeds, and
STATE.md. The v2.4 queue (HQ-27 … HQ-38) is archived at
`.planning/milestones/v2.4-HUMAN-QUEUE.md`; numbering continues from HQ-40.
