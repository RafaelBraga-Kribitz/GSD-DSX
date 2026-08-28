# HUMAN-QUEUE — items only you can answer

The loop keeps working around these; it only blocks at stage S4 if any remain.
Answer by typing into the loop session, e.g. `HQ-1: test 1 pass, test 2 pass, ...`
The loop records your verdict in the proper GSD artifact (UAT file, SECURITY.md)
and checks the item off here.

## Open

### HQ-7 — S4-6 final ship: PR / merge-to-main / release-tag decisions (filed 2026-08-28, S4-6 prep)

This is the milestone's **terminal** human gate. Everything else is done: audit
`passed` (S4-4), milestone archived (S4-5), branch pushed (0/0 vs origin), queue
was otherwise empty. The only open ledger box is **S4-6**, whose two halves the
loop cannot finish alone:

- **`/gsd-cleanup` — no action needed (verified no-op this firing).** v2.0.0 already
  has its `.planning/milestones/v2.0.0-phases/` archive (S4-5), `.planning/phases/`
  is empty, and there are **zero** stale local branches (no `: gone]` upstreams). So
  the promised "cleanup file-deletion approval" is moot — there is nothing to delete.
- **`/gsd-ship` — needs you.** Its remaining actions are outward-facing / semi-irreversible
  and the branch state is tangled; a headless firing must not blind-fire them.

**Ground-truth git state (measured this firing, 2026-08-28T03:32Z):**

| Fact | Value |
|---|---|
| Branch vs `origin/main` | **663 commits ahead, DIVERGED** (origin/main is not an ancestor — no clean fast-forward) |
| Code delta (non-`.planning`) | 117 files, +34,555 / −1,768 — the real DSX validity-frame product |
| `.planning` delta | 308 files, +111,062 / −892 — ceremony artifacts (would bloat a raw PR) |
| Existing PR for this branch | **PR #1 — already MERGED 2026-08-10** ("v2.0.0: validity frame, deterministic chart selection, installer correctness") |
| `git tag v2.0.0` | points at **old `cb94015`** (2026-08-10, unrelated "Merge v2.0.0"), already on origin, **NOT an ancestor of HEAD** |
| Local `main` | 1 behind `origin/main` |
| `gh` | authenticated (RafaelBraga-Kribitz; `repo`,`workflow` scopes) — a PR *could* be created |

**Three decisions (answer any/all, e.g. `HQ-7: pr=a, merge=merge-commit, tag=new v2.0.1`):**

1. **PR shape.** (a) `/gsd-pr-branch` to filter out the 308 `.planning/` files, then open a code-only PR (~117 files) for review; (b) `/gsd-ship` full milestone PR including planning artifacts; (c) direct-merge, no new PR; (d) none — treat PR #1 as the ship of record and skip.
2. **Merge to `main`.** Whether and how to land the 663-commit diverged branch — merge commit vs rebase vs squash. (Outward/semi-irreversible → your call.)
3. **Release tag `v2.0.0`.** (a) leave the existing published tag at `cb94015` untouched and cut a **new** tag (e.g. `v2.0.1`) at the shipped commit; (b) force-move the published `v2.0.0` tag to the shipped commit — **history rewrite of a published ref, irreversible** (brief §4 cat. 2); (c) no tag.

**Loop's recommendation (advisory — the outward/irreversible parts are yours):**
1(a) filtered PR via `/gsd-pr-branch` (keeps the review diff to real code), 2 operator-driven
merge, 3(a) a **new** tag rather than force-moving the published `v2.0.0` — least-destructive,
avoids rewriting a release ref already on origin. Rationale: rigour > reliability > flexibility.

**How to act:** answer here, or (per LOOP-OPERATOR.md §5) drive `/gsd-pr-branch` + `/gsd-ship`
in an interactive session (pause the Scheduled Task first — two writers on this branch conflict).
Once shipped, a firing checks S4-6 and logs `MILESTONE COMPLETE`.

_(HQ-1 through HQ-6 + the ⚠Z Zimmerman fix are all answered — see below.)_

## Standing framework notes (not queue items — nothing to answer, just remember)

**`/gsd-audit-uat`'s automated CLI under-reports human-verification items.**
Found 2026-08-27 during S4-1: the CLI returns a false "All Clear" because
`gsd-core/bin/lib/uat.cjs::parseVerificationItems` only recognizes a level-2
`## Human Verification` heading, while the `gsd-verifier` template actually
writes a level-3 `### Human Verification Required` heading. This is a
framework-internal defect (not a bug in this repo's own code) — recorded,
not patched here. **At S4-4 and any future milestone audit, do not accept a
CLI "all clear" as evidence of no outstanding UAT** — cross-check each
phase's VERIFICATION.md by hand, the way the S4-1 sweep did.

## Will be added by the loop when reached

- End-of-phase UAT rounds for Phases 11.2, 11.3, 12 (batched, with evidence packs). — DONE (HQ-4/5/6, all answered).
- ~~`/gsd-cleanup` file-deletion approval (S4-6).~~ — REACHED 2026-08-28: cleanup is a verified no-op (nothing to archive, no stale branches), so no deletion approval is needed. The live S4-6 ship decisions are in HQ-7 (Open) instead.
- Any persona decision you veto from a daily summary.

## Answered

Full verbatim records for every item answered through 2026-08-27 moved to
`.planning/HUMAN-QUEUE-ARCHIVE.md` (§5 hot-path trim — this file is re-read in full
on every firing). Nothing downstream still double-checks these inline: every consuming
unit (S4-1b ⚠Z fix, S4-2 queue drain, S4-4 milestone audit) is complete. Pointers:

- HQ-1 — Phase 11 UAT: four D-05 citation/wording reads (answered 2026-08-26) — `HUMAN-QUEUE-ARCHIVE.md`
- HQ-2 — Phase 11.1.1 security sign-off (answered 2026-08-26) — `HUMAN-QUEUE-ARCHIVE.md`
- HQ-3 — Phase 11.2 discuss: D-05 citation reads (answered 2026-08-26) — `HUMAN-QUEUE-ARCHIVE.md`
- HQ-4 — Phase 11.2 formal D-05 UAT round + security sign-off (answered 2026-08-27) — `HUMAN-QUEUE-ARCHIVE.md`
- HQ-5 — Phase 11.3 D-05 citation reads + D-06 code veto + security sign-off (answered 2026-08-27) — `HUMAN-QUEUE-ARCHIVE.md`
- HQ-6 — Phase 12 (Calibration) UAT round + §4 veto + security sign-off (answered 2026-08-27) — `HUMAN-QUEUE-ARCHIVE.md`
- ⚠Z Zimmerman citation fix — HQ-1 follow-up (answered 2026-08-27; executed at S4-1b, commit dc65fc6) — `HUMAN-QUEUE-ARCHIVE.md`
