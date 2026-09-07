# LOOP-LEDGER-ARCHIVE — v2.6 Exploration Depth and Backlog Evidence

Long-form evidence for ledger units, offloaded from `LOOP-LEDGER.md` to keep the
hot-path Log lean (brief §5). One `## <unit-id>` section per unit that needs more
than a pointer. The Log line in `LOOP-LEDGER.md` is the index into this file.

Previous milestones' archives: `.planning/milestones/v2.4-LOOP-LEDGER-ARCHIVE.md`,
`v2.3-LOOP-LEDGER-ARCHIVE.md`, `v2.2-LOOP-LEDGER-ARCHIVE.md`,
`v2.0.0-LOOP-LEDGER-ARCHIVE.md`.

---

## S1-3 — Phase 25 execute (plan 25-01 slice; 2026-09-07)

Plan 25-01 (wave 1 of 4) executed by a `gsd-executor` subagent (sonnet, per brief §3
routing for plan execution) and **verified by the orchestrator re-running every gate**
on the real interpreter (`Python 3.12.10`), per the brief's "gate re-run by the
orchestrator, not trusted from a subagent's report" mandate.

**Reconciliation (repo is the fact):** HEAD `a100f00` on `gsd/v2.6.0-exploration-depth`,
6 atomic commits (`d78a738`→`a100f00`), **no stray `gsd/*` branch created** (the
`worktree-agent-a9a54fddf75afc02f` leftover is pre-existing operator-local, untouched).
Only operator-local untracked files in the tree.

**Gates re-run by orchestrator (not the subagent's numbers):**
- `tests.test_profiler_hermetic` (all classes) → 14 tests OK.
- Independent reference-value check via a direct `statistics` call:
  `quantiles([1..10], n=4, method='inclusive')` = q1 3.25 / median 5.5 / q3 7.75;
  `mean` 5.5; `stdev` `3.0276503540974917` — matches the pinned test literals exactly.
- Full suite `unittest discover -s tests -q` → **1542 tests OK** (only pre-existing
  catalogue "declared twice" warnings; the two explain tests did NOT false-fail, so the
  stray-`DECISIONS.jsonl` remedy was not triggered).

**Code correctness confirmed by read** (`dsx/profiler.py`): `_numeric_block` uses
`statistics.quantiles(ordered, n=4, method="inclusive")` (H&F type-7), `statistics.mean`,
`statistics.stdev`, `None` for undefined stats (n=0 all-null; n=1 sd=None); numeric/
categorical assigned as the LAST write under each `columns[<col>]` (D-01 byte-stability).
`_categorical_block` uses the explicit `sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))`
(count desc, level string asc) — the frozen rule, never `Counter.most_common()`.

**Executor deviation, reviewed and accepted:** the executor corrected a hand-arithmetic
error in `test_top10_tie_boundary` (original `(109+5)/119` → correct `(99+5)/109`). The
fixture is 109 rows (a15,b14,c13,d12,e11,f10,g9,h8,i7,n5,m5); `104/109` is arithmetically
correct. This was a legitimate test-value fix, not code masking.

**FINDING for S1-4 (test-efficacy, NOT a correctness bug — carry forward):**
`test_top10_tie_boundary_count_desc_then_string_asc` is **non-discriminating**. Because
`m` and `n` both have count 5, `share_top10 = 104/109` is invariant to which one occupies
rank 10 — so the assertion (and its docstring's claim that `Counter.most_common()` "would
wrongly include n") cannot actually distinguish the frozen tie-break from a buggy one. The
string-asc tie-break among *equal-count* levels is fundamentally unobservable in any
sum-over-top-N aggregate; the block exposes no level list. This is a **plan/test design
flaw** (the plan specified equal counts), faithfully built by the executor. The production
code IS correct (explicit `sorted((-count, level))`, verified by read) and determinism is
independently guaranteed (`TestProfilerDeterminism` + order-invariant sums). **S1-4 code
review should either correct the misleading docstring to state honestly that the test
proves the top-10 *sum* (not the string-asc tie-break, which is unobservable here), or add
a discriminating check via an exposed ranking — without adding a new profile key (D-01
byte-stability forbids it).** Not an S1-3 blocker: 25-01's automated gate passes and the
code is correct.

**Stop rationale:** S1-3 is a large 4-plan unit (brief §1 "unit too large for one firing →
stop cleanly at a safe boundary, write down where you stopped"). The executor alone ran
~10 min wall-clock; with orchestrator verification (full suite 61s) the firing is at the
~12-min pacing cap. Stopped at the committed+verified 25-01 plan boundary. Resume: execute
plan 25-02 (wave 2, depends 25-01; time-block + unit-block) via a fresh `gsd-executor`,
then 25-03, then 25-04, then S1-3 checks and S1-4 begins. No `gsd-pause-work` handoff
needed — no in-flight context (fresh subagent per plan; `25-01-SUMMARY.md` on disk; GSD
STATE/PLAN tracking resumable).

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
