# HUMAN-QUEUE — items only you can answer

Milestone **v2.4 Visual Excellence**. The loop keeps working around these; it only
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

### HQ-27 — Phase 22 D-05 citation evidence pack (filed S0-3, 2026-09-03)

**Type:** D-05 primary-source read (item 1). **Blocks:** S2-1 discuss for any
Phase 22 code whose Tier-1 source is unsigned; non-blocking for Phase 21.
**Full pack:** `.planning/v2.4-D05-EVIDENCE-PACK.md` (per-citation table: locator,
exact claim, confirmed-by-loop vs UNVERIFIED-for-human split). Prepared by the
loop; **NOT signed** — the loop may prepare, it may not sign.

Sources to confirm at their locators (granularity: one deep read per code-critical
source, one authenticity confirmation per per-entry source):

- **Tier 1 — mandatory deep read (code-critical):** T1-1 Cleveland & McGill 1984
  (JASA 79:531-554, the perceptual ranking the REQ-P22-05 tie-break asserts);
  T1-2 Heer & Bostock 2010 (CHI, the paired replication); T1-3 Wilke 2019 ch.16
  (the fan/quantile-dot/half-eye/gradient-CI uncertainty family, REQ-P22-02).
- **Tier 2 — authenticity confirm (per-entry spine + heuristic):** T2-1 FT Visual
  Vocabulary 2016 (MIT repo, the spine); T2-2 Wilke ch.5 directory; T2-3 Graphic
  Continuum; T2-4 Data Visualisation Catalogue (stable URLs); T2-5 Datawrapper
  cardinality bands; T2-6 Munzner 2014 (ch.2/3/6).
- **Tier 3 — refusal-entry doctrine (batch when refusal entries land):** Few,
  Harris, Tufte, Muth 2018.

**To sign:** confirm each row in the pack file (`SIGNED <initials> <date>`), then an
interactive session checks HQ-27 off here. ~9 core + 4 refusal = within the ~8–12
estimate.

## Will be added by the loop when reached

- ~~S0-3: Phase 22 D-05 evidence pack~~ — FILED 2026-09-03 as HQ-27 (see Open).
- Phase 21/22/23/24 end-of-phase security sign-off + UAT rounds (batched per
  phase; non-blocking until S5-2).
- D-06 numbering veto windows for any new codes Phase 22 mints (from a freshly
  re-measured live catalogue count; silence = accept).
- The Phase 23 license-audit confirmation (dsx-538/dsx-urban forked from
  permissively-licensed sources; dsx-econ/dsx-bbc reimplemented from published
  doctrine only, no GPL port, no unlicensed PDF embed).
- The S5-6 ship decisions: merge to `main` and the `v2.4.0` release tag.
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
and is silently dropped (found v2.3 S5-1). **At S5-1, never accept the CLI's
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
verified phase (found v2.3 close-out).** Same class of naming-convention blind
spot as the audit-uat issues, on a different code path. If it happens again,
read the actual verification file directly before treating it as a real gap.

**`/gsd-pr-branch` does not survive a long ceremony branch.** Its per-commit
cherry-pick chain hit recurring modify/delete conflicts on v2.0.0's 707-commit
branch and was abandoned mid-run. Ship by direct 3-way merge.

**Ship by EXPLICIT branch name — never the framework's auto-detect.** This repo
now carries five stale `gsd/*` branches from prior milestones; `/gsd-complete-
milestone`'s `handle_branches` picks the alphabetically-first `gsd/*` branch
(`gsd/v1.1.0-milestone`), which is always wrong here (found and bypassed at
v2.2 and v2.3 ship). `git merge --no-ff gsd/v2.4.0-visual-excellence` by name,
verified on a throwaway branch first.

**Release tags: never force-move a published one.** v2.0.0 shipped as tag
`v2.1.0` for this reason; v2.2 shipped as `v2.2.0`; v2.3 shipped as `v2.3.0`.
The next free tag for this milestone is `v2.4.0`.

**`/gsd-complete-milestone` output needs hand-verification — recurring at every
close so far.** At both v2.2's and v2.3's close, its generated accomplishment
bullets were truncated mid-sentence or captured YAML frontmatter instead of
prose, and the archived REQUIREMENTS.md carried all rows forward still
unchecked despite the passed audit — both needed hand-correction each time.
Budget for this as a standing cost, not a surprise. Also: it is NOT
headless-safe (interactive prompts + `git rm REQUIREMENTS.md`) — interactive
session only.

**Run the full suite from a clean tree — a stray root `DECISIONS.jsonl`
false-fails two `explain` tests.** `tests/test_dsx.py::test_explain_missing_spec_exits_zero_not_two`
and `tests/test_explain_self_reported.py::test_returns_zero_when_spec_cannot_be_loaded`
run from repo-root CWD without isolation; any repo-root `dsx gate`/`dsx explain`
leaves a gitignored ledger that breaks them. If exactly these two fail:
`rm -f DECISIONS.jsonl examples/DECISIONS.jsonl examples/known-bad/DECISIONS.jsonl templates/DECISIONS.jsonl`
and re-run before treating it as real.

**Usage-limit backoff is the wrapper's job — proven working in production.**
`scripts/run-ceremony-firing.ps1` detects limit hits, writes
`.planning/loop-logs/.backoff-until`, and re-probes every 30 minutes during a
hold with one trivial `claude -p` call to catch an early release rather than
blindly waiting the full window (fixed 2026-09-01 after a weekly-limit early
release was missed). Observed across v2.3's close: four separate 5-hour-window
hits each self-recovered in 2–7 minutes. Firings: log one line, stop, never
retry-loop, never touch the backoff/probe-marker files.

**A firing that finds uncommitted, ledger-inconsistent changes at start should
hold, not act.** Confirmed working at v2.3's close: a firing found an
interactive session's in-progress `/gsd-complete-milestone` work uncommitted in
the tree and correctly left it untouched (neither committed nor discarded),
logging the observation instead. This is the correct behavior, not a bug to fix.

## Answered

(v2.0.0's items HQ-1…HQ-7, v2.2's items HQ-8…HQ-15, and v2.3's items
HQ-16…HQ-26 are archived at `.planning/milestones/v2.0.0-HUMAN-QUEUE*.md`,
`.planning/milestones/v2.2-HUMAN-QUEUE.md`, and
`.planning/milestones/v2.3-HUMAN-QUEUE.md`. Numbering continues from HQ-27.)
