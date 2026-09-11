---
id: SEED-004
status: dormant
planted: 2026-09-11
planted_during: v2.6.1 liabilities pass (after the v2.6.0 ship) — operator direction that no known liability is carried unrecorded
trigger_when: a milestone's scope runs more than one `dsx gate` at a time against ONE project root (parallel executors gating the same spec in the same directory, a CI matrix sharing a checkout), OR `dsx explain` is observed grouping two runs' records under one invocation header
scope: small — one module (`dsx/decisions.py`) plus its single caller in `dsx/cli.py`; stdlib only; a design decision (the identifier must stay deterministic), not a quick patch
---

# SEED-004: Serialise concurrent `DECISIONS.jsonl` writers

## What is true today (verified 2026-09-11 against the code)

- `dsx/decisions.py::next_invocation_id` (`:218-238`) derives `INV-NNNN` by counting the
  invocation records already in the file; `dsx/cli.py::_write_decision_trail` (`:336`, the
  call at `:377`) then appends the header as a separate step. Nothing serialises the two.
- The limitation is recorded, not hidden: the module docstring's "Concurrency (WR-02)" note
  (`:42-48`) and the function docstring (`:224-234`) both say concurrent gate runs against
  one root are unsupported and that serialising them is the operator's responsibility.
  Origin: Phase 06 review finding WR-02; Plan 06-11 Task 3 adopted "record it" and
  explicitly deferred a lock
  (`.planning/milestones/v2.0.0-phases/06-contract-extension-decision-record-paradigm-manifest/06-11-PLAN.md:353-370`).
- Consequence when violated: two racing `dsx gate` processes derive the same identifier,
  both append a header carrying it, and `dsx explain` — which groups purely on identifier
  equality — interleaves the two runs under one header. No record is lost (`append()` is
  flush-and-fsync per record; `read_all()` is tolerant), but attribution is.
- No caller in this repository does this today: the parallel-subagent rule gives each
  executor its own worktree (`.claude/CLAUDE.md`), the ceremony loop is a single process,
  and the test suite uses a fresh `tempfile.TemporaryDirectory()` per gate call.

## Why this is a seed and not a fix now

The identifier is deterministic by contract — never a uuid, never a clock read
(`dsx/decisions.py:219-220`) — so the easy "make ids unique" escapes are ruled out, and any
lock is platform-split in the stdlib (`msvcrt.locking` on Windows, `fcntl.flock` elsewhere).
Building it with no caller that races would add a code path no test exercises for real.
Recorded here so it is met as a known item, not re-discovered as a surprise.

## Candidate designs (for the phase that triggers this)

| id | Design | In practice | Cost |
|---|---|---|---|
| CL-01 | Advisory file lock around count-then-append | A context manager in `decisions.py` opens `DECISIONS.jsonl.lock`, takes an exclusive advisory lock (`msvcrt.locking` / `fcntl.flock`), and is held across `next_invocation_id()` and the header append in `_write_decision_trail`; released in `finally`. | Platform split to test on both. Advisory locks die with the process, so the lock file's mere existence must never be read as "held". Cheap to undo. |
| CL-02 | Append, then verify and repair on collision | Append with `O_APPEND`, re-read, and if the header's identifier is not unique, recount and rewrite. | Puts a rewrite path into an append-only log and conflicts with the "a line that finished writing survives" durability contract (`:32-41`). Expensive to undo. |
| CL-03 | Keep it unsupported; make the violation loud | `dsx explain` detects duplicate invocation identifiers and reports them as a trail-integrity problem instead of silently grouping. | Enables nothing; only makes the failure visible. Cheapest; can ship alongside CL-01. |

Recommendation for the triggering phase: CL-01 plus CL-03. Dropped: CL-02, because it
rewrites an append-only log.

## Test obligations when promoted

- Two subprocess `dsx gate` runs launched against one temp root at the same time must get
  distinct identifiers and unbroken `dsx explain` grouping — the race made real, not
  simulated.
- Lock release after a simulated crash (child killed mid-write): the next run must not
  hang.
- The trail stays a side channel: if the lock cannot be taken, the trail is not written and
  the gate still runs and exits on its findings (the "never fail the gate over the trail"
  rule that `dsx/cli.py` enforces around `append_decision`).

## Breadcrumbs

- `dsx/decisions.py:42-48, 218-238` — the recorded limitation
- `dsx/cli.py:336` — `_write_decision_trail`, the only writer
- `.planning/milestones/v2.0.0-phases/06-contract-extension-decision-record-paradigm-manifest/06-11-PLAN.md:353-370`
  — WR-02 adoption and the deferred remedy
