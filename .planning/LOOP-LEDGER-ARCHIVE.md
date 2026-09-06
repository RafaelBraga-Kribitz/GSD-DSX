# LOOP-LEDGER-ARCHIVE — v2.6 Exploration Depth and Backlog Evidence

Long-form evidence for ledger units, offloaded from `LOOP-LEDGER.md` to keep the
hot-path Log lean (brief §5). One `## <unit-id>` section per unit that needs more
than a pointer. The Log line in `LOOP-LEDGER.md` is the index into this file.

Previous milestones' archives: `.planning/milestones/v2.4-LOOP-LEDGER-ARCHIVE.md`,
`v2.3-LOOP-LEDGER-ARCHIVE.md`, `v2.2-LOOP-LEDGER-ARCHIVE.md`,
`v2.0.0-LOOP-LEDGER-ARCHIVE.md`.

---

## milestone-open — 2026-09-06 (interactive session, operator direction)

Opened outside the loop, in the operator's interactive session, after the operator
fixed the scope from a three-option decision block ("Both: EDA depth + paper
evidence"). Recorded as HUMAN-QUEUE HQ-39, which reverses HQ-38 (SEED-002 hold)
from earlier the same day. Artifacts written: `.planning/research/V2.6-SCOPE.md`
(live-tree facts verified against `d2f0140`), `REQUIREMENTS.md` (18 requirements,
Phases 25–30), the v2.6 section of `ROADMAP.md`, the Current Milestone section of
`PROJECT.md`, STATE.md via `gsd-tools query state.milestone-switch`, this ledger,
the brief and the queue. The v2.4 ledger, its archive and its queue moved to
`.planning/milestones/v2.4-*` by `git mv`. `scripts/run-ceremony-firing.ps1`
`$Branch` repointed to `gsd/v2.6.0-exploration-depth`; the operator's pause flag
removed so the next scheduled poll fires S0-1.
