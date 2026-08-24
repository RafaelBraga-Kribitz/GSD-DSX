# LOOP-LEDGER — v2.0.0 completion backlog

Source of truth for the autonomous loop. One checkbox = one wakeup unit.
Check a box ONLY with its gate evidence pasted in the log. Derived from
`.planning/v2.0.0-MILESTONE-AUDIT.md` (2026-08-23, gaps_found, 49/75).

## Reconciliation notes (repo is the fact; the ledger's audit source can be stale)

- **2026-08-23T15:15Z (firing 1):** The milestone audit (this ledger's source)
  claims at lines 213–224 that Phase 11.1.1 plans 06 and 07 are "written and
  gate-passed but NOT YET EXECUTED." **The repo contradicts this: both are
  executed and committed** — plan 06 (`745f4d4`, `53cd3ae`, `a6061a4`, `9931e53`),
  plan 07 (`79329a1`, `25dee19`, `2e132d3`), followed by `4b8318a docs(phase-11.1.1):
  complete phase execution` and `c9835fc ...evolve PROJECT.md after phase
  completion`. `11.1.1-VERIFICATION.md` scores the phase `passed` 6/6 with SC5
  re-verified live. The audit was misled by two pre-execution snapshots that were
  never refreshed: the phase's `.continue-here.md` (still says "execution NOT
  started" — the exact stale-handoff trap its own anti-pattern table names) and
  `11.1.1-SECURITY.md` (`status: draft`, written before 06/07 ran). **Consequence
  for the ledger:** S0-1 and S0-2 were already complete in the repo; verified
  empirically this firing and checked off. The security *gate* is still genuinely
  open (SECURITY.md register was never refreshed to close T-11.1.1-13(plan04) and
  T-11.1.1-08's factual half, and WR-02/plan 08 is real remaining work) — that is
  S0-3 and S0-4, not S0-1/S0-2. The first genuinely-unexecuted unit is **S0-3**.

## S0 — Hygiene and open gates

- [x] S0-1 Execute Phase 11.1.1 plan 06 (malformed-.ipynb traceback fix; already written and gate-passed). Gate: the seven malformed inputs exit as gate findings, not raw tracebacks; suite green. → **ALREADY EXECUTED (repo fact); gate re-run and PASSED this firing.** Probe over 11 malformed shapes + 20000-deep JSON: every one returns `None` (controlled "NOT scanned" finding), none raised; `{"cells": []}` boundary control still scans. `bash scripts/check.sh` → "all checks passed", 1028 tests OK, gate contract + determinism green. Commits: `53cd3ae fix(11.1.1-06): guard every JSON shape the notebook read can meet`, `745f4d4`, `a6061a4`. See Reconciliation notes above.
- [x] S0-2 Execute Phase 11.1.1 plan 07 (README malformed-notebook claim correction; already written). Gate: README claim matches actual behaviour. → **ALREADY EXECUTED (repo fact); gate re-checked this firing.** README.md lines 258–274 enumerate exactly the shapes the shipped `_read_source` guards (non-object doc, non-object cell, non-list/number/boolean `cells`, non-text source element, non-text/non-list source, too-deeply-nested) plus the empty-notebook boundary — one-to-one with the probe results. False generalisation removed (`grep -c "for example, the two characters" README.md` → 0); residual limits disclosed (`grep -c "not valid UTF-8" README.md` → 1). Commits: `79329a1`, `25dee19`, `2e132d3`.
- [x] S0-3 Write Phase 11.1.1 plan 08 (Option B from UAT: unscannable entrypoint must surface in `dsx check code` / `dsx explain`, not silently pass) via `/gsd-plan-phase 11.1.1 --gaps`, then execute it. Gate: unscannable entrypoint produces a visible finding + decision record. → **PLAN WRITTEN (2026-08-23T23:47Z) + EXECUTED (2026-08-24T01:01Z firing): WR-02 Option B CLOSED IN CODE.** Plan 08 executed by `gsd-executor` (sonnet-class per §3 routing); 3 atomic commits `ca2828c` (RED tests), `4c41513` (GREEN record_decision calls), `685954d` (docs/summary). **Gate re-run independently by the orchestrator, real evidence:** `bash scripts/check.sh` → final line `all checks passed`; full suite `python -m unittest discover -s tests -q` → `Ran 1031 tests ... OK`; target `TestPhase11_1Code` → `Ran 138 tests ... OK`; known-bad corpus → `Ran 30 tests ... OK`. Closure evidence: `grep -c "record_decision(" dsx/checks/code.py` → 4 (was 2); `grep -v '^#' dsx/checks/code.py | grep -c "scan_path:not-scanned"` → 2 (was 0); old test name renamed (`grep -c "def test_unscannable_entrypoint_also_produces_no_decision_record"` → 0). Scope held: `git diff --stat -- dsx/findings.py dsx/cli.py` empty (Option C NOT implemented); `git diff --stat 8aacd07..HEAD -- tests/test_known_bad_corpus.py examples/` empty (no corpus/fixture drift); `is_blank` (:537) still record-free (blank-boundary pin green). Summary: `11.1.1-08-SUMMARY.md`.
- [x] S0-4 Re-run `/gsd-secure-phase 11.1.1`. Gate: SECURITY.md `verified`, threats_open 0 (T-11.1.1-06 redisposition to "accept" goes to HUMAN-QUEUE HQ-2). Human sign-off line → HQ-2. → **DONE (2026-08-24 firing): SECURITY.md now `status: verified`, `threats_open: 0`.** Ran the secure-phase gate: State A, register authored at plan time, `threats_open: 3 > 0` so no short-circuit; Step-4 AskUserQuestion driven with the safe default "Verify all open threats" (headless per brief §4). Spawned `gsd-security-auditor` (opus, resolved model) — verdict **`## SECURED`**, all 3 blocking threats CLOSED in the live tree (T-11.1.1-13(plan04) by plan 06, T-11.1.1-08 factual half by plan 07, T-11.1.1-11/T-11.1.1-18/WR-02 by plan 08), 0 blocking open. The auditor surfaced-and-cleared the `dsx/cli.py` 77-line diff (unrelated Phase 11 admissibility work, not Option C). **Orchestrator independently re-ran the gate (never trusted the subagent claim):** full suite `Ran 1031 tests ... OK`, `TestPhase11_1Code` `Ran 138 ... OK`, known-bad corpus `Ran 30 ... OK`; `grep -c "record_decision(" dsx/checks/code.py`=4, non-comment `scan_path:not-scanned`=2, `git log 8aacd07..HEAD -- dsx/findings.py`=0 commits (Option C unimplemented); malformed-shape probe over 11 temp `.ipynb` files → all no-raise. T-11.1.1-06 redispositioned mitigate→accept (non-blocking, below `high`); its confirmation + the phase security sign-off line remain in HQ-2 (do NOT block the technical `verified`). Audit-trail row added 2026-08-24.
- [ ] S0-5 Run `/gsd-secure-phase 10` (never run; DECISIONS.jsonl became a gate input in Phase 10). Gate: 10-SECURITY.md exists, `verified` or threats queued.
- [ ] S0-6 Tech-debt batch via `/gsd-audit-fix` or direct fixes, one commit each:
      (a) `design.alpha: 0` falsy-or bug at dsx/checks/decision.py:106, dsx/checks/stats.py:143, dsx/frame/paradigm.py:225 + regression test for alpha=0;
      (b) `dsx/decisions.py::append` CRLF — open with `newline="\n"` + byte-level test;
      (c) canonical-declaration test pinning DSX-SPEC-070, DSX-VAL-021, DSX-VAL-060, DSX-COH-030, DSX-PAR-002 duplicate texts. Gate: full suite green (≥1,028 tests).
- [ ] S0-7 Process fixes (haiku-grade): REQUIREMENTS.md traceability rows for Phases 7/10/11.1 (verified-passed, still `Pending`); ROADMAP.md Progress table rows for Phases 10 and 11; 06-/09-VERIFICATION.md frontmatter-vs-body status contradictions. Gate: re-read files show consistency.
- [ ] S0-8 Nyquist validation backfill: `/gsd-validate-phase` for 6, 7, 9 (its VALIDATION.md still has literal placeholder braces), 10, 11.1, 11.1.1 — one unit per phase is allowed if heavy. Gate: each VALIDATION.md `validated`, `nyquist_compliant: true`.
- [ ] S0-9 Prepare the Phase 11 UAT evidence pack for the four open D-05 checks in 11-UAT.md (fetch/quote each source where accessible, side-by-side with the claimed citation) and file it as HQ-1. Gate: HUMAN-QUEUE.md HQ-1 contains a per-check evidence table. (The sign-off itself is human — do not close 11-UAT.md.)

## S1 — Phase 11.2: Prescriptive claim layer (7 requirements)

- [ ] S1-1 Discuss: persona round for numeric DSX code assignments (D-06) + any gray areas; CONTEXT.md written.
- [ ] S1-2 Plan (plan-checker must pass).
- [ ] S1-3 Execute all plans (`--no-transition`; worktrees per config).
- [ ] S1-4 Code review + auto-fix; verification `passed` (human items → HUMAN-QUEUE, continue).
- [ ] S1-5 `/gsd-secure-phase 11.2` verified + `/gsd-validate-phase 11.2` compliant.

## S2 — Phase 11.3: Reporting completeness and missing-data discipline (7 requirements)

- [ ] S2-1 Discuss: Statistician-led persona round settles the missingness-rate reconciliation design (tolerance + re-baseline vs entry-condition deferral — must not fire on the canonical good fixture) + numeric codes; CONTEXT.md written.
- [ ] S2-2 Plan (plan-checker must pass).
- [ ] S2-3 Execute all plans.
- [ ] S2-4 Code review + auto-fix; verification `passed`.
- [ ] S2-5 `/gsd-secure-phase 11.3` verified + `/gsd-validate-phase 11.3` compliant.

## S3 — Phase 12: Calibration (5 requirements, terminal)

- [ ] S3-1 Discuss: persona round on corpus composition and catch-attribution tagging (retrofit tags to the cases that landed untagged in Phases 10/11.1); CONTEXT.md written.
- [ ] S3-2 Plan (plan-checker must pass).
- [ ] S3-3 Execute: full known-bad corpus + attribution tags + `dsx stats --paradigm`.
- [ ] S3-4 Measure catch rate and false-positive rate; Statistician persona (fable/opus, high effort) adversarially reviews the readout before it is recorded.
- [ ] S3-5 Code review + auto-fix; verification `passed`; secure-phase + validate-phase both green; backlog re-evaluation recorded.

## S4 — Close-out

- [ ] S4-1 `/gsd-audit-uat` cross-phase sweep; queue any residue.
- [ ] S4-2 Drain HUMAN-QUEUE (the only permitted blocking wait; daily notification while waiting).
- [ ] S4-3 `/gsd-extract-learnings`.
- [ ] S4-4 `/gsd-audit-milestone` — must reach `passed`. If gaps_found: fix and re-run (one full cycle allowed before escalating).
- [ ] S4-5 `/gsd-complete-milestone` (archive verified to exist).
- [ ] S4-6 `/gsd-cleanup` (deletion approval via HUMAN-QUEUE) and `/gsd-ship`.

## Log

(append one line per wakeup: `YYYY-MM-DDTHH:MMZ | unit | outcome | evidence`)

2026-08-23T15:15Z | reconcile ledger vs repo | audit stale: plans 06/07 ALREADY executed+committed, phase VERIFICATION.md passed 6/6; audit misled by pre-exec `.continue-here.md` + `11.1.1-SECURITY.md` draft | Reconciliation note added to ledger head; commits 53cd3ae/2e132d3 etc.
2026-08-23T15:15Z | S0-1 | DONE — gate re-run PASSED (already executed) | probe: 11 malformed shapes + 20000-deep JSON all → None/no-raise, `{"cells":[]}` still scans; `bash scripts/check.sh` all checks passed, 1028 tests OK
2026-08-23T15:15Z | S0-2 | DONE — gate re-checked (already executed) | README.md:258–274 enumerates the 6 guarded shapes + empty-notebook boundary, matches probe 1:1; grep old-generalisation=0, "not valid UTF-8"=1
2026-08-23T15:15Z | firing-stop | one unit complete (S0-1+S0-2 reconciled/closed); next unblocked = S0-3 (write+execute plan 08 for WR-02, heavy) — deferred to next firing per §1 | committed+pushed to gsd/v2.0.0-dsx-validity-frame
2026-08-23T23:47Z | S0-3 (plan half) | plan 08 WRITTEN + plan-checker gate PASS; split at §1 safe boundary, execution deferred to next firing; S0-3 checkbox stays UNCHECKED (needs execute+suite gate) | `11.1.1-08-PLAN.md` (539 lines, type:tdd, gap_closure, wave 1, requirements:[]); gsd-planner + gsd-plan-checker run as INDEPENDENT contexts (role separation preserved). Checker verified live: early returns code.py:537(is_blank,OUT)/545(path is None,IN)/553(source is None,IN); 2 existing record_decision @717/824 unmoved; scan_path_input/python_input @580/583 are after the returns so new records build `scan_path:not-scanned:<reason>`+`python:{maj}.{min}` inline; replay wiring traced record_decision→report.context["decisions"]→collect_from_report→cli _write_decision_trail(:381)→dsx explain(:558); target test test_unscannable_entrypoint_also_produces_no_decision_record @tests/test_dsx.py:7316 (today asserts decisions is None) to be inverted; scope-boundary pin @:7290 kept; live counts TestPhase11_1Code=135, full suite=1028, plan gates ≥138/≥1031. Verdict text in plan-checker return (this firing).
2026-08-23T23:47Z | firing-stop | one unit's plan-half complete (S0-3 plan written+gate-passed); did NOT start a 2nd heavy unit per §1; next firing executes plan 08 | committed+pushed to gsd/v2.0.0-dsx-validity-frame
2026-08-24T01:01Z | S0-3 (execute) | DONE — plan 08 executed, WR-02 Option B CLOSED IN CODE. gsd-executor ran TDD RED→GREEN→docs; orchestrator re-ran the gate independently and pasted real evidence (never trusted the subagent claim). | commits ca2828c/4c41513/685954d; `bash scripts/check.sh`→"all checks passed"; full suite 1031 OK, TestPhase11_1Code 138 OK, known-bad 30 OK; record_decision(=4 (was 2), non-comment scan_path:not-scanned=2 (was 0), old test name=0; diff-stat findings.py/cli.py empty (Option C untouched), corpus/examples vs 8aacd07 empty
2026-08-24T01:01Z | firing-stop | one unit complete (S0-3 executed+gated); did NOT start a 2nd heavy unit per §1; next unblocked = S0-4 (`/gsd-secure-phase 11.1.1` — now unblocked since 06/07/08 all executed) | committing+pushing ledger to gsd/v2.0.0-dsx-validity-frame
2026-08-24T05:03Z | reconcile ledger vs repo | ledger and repo AGREE — S0-1/S0-2/S0-3 done+committed (`873bbc6`/`685954d`/`4c41513`/`ca2828c` all present); branch up to date with origin; no correction needed | `git log --oneline -15` + `git status` clean (only untracked non-ceremony files: `.claude/`, `.vscode/`, briefs)
2026-08-24T05:03Z | S0-4 | DONE — `/gsd-secure-phase 11.1.1` gate PASSED: SECURITY.md `status: verified`, `threats_open: 0`. State A, register-at-plan-time, threats_open 3>0 so no short-circuit; Step-4 driven with safe default "verify" (headless §4). `gsd-security-auditor` (opus) verdict **SECURED** — 3/3 blocking threats closed by plans 06/07/08; orchestrator re-ran the gate independently (never trusted the subagent). | suite 1031 OK / TestPhase11_1Code 138 OK / known-bad 30 OK; `record_decision(`=4, non-comment `scan_path:not-scanned`=2, `findings.py` 0 commits since 8aacd07; malformed probe 11 temp `.ipynb` → all no-raise. T-11.1.1-06→accept (non-blocking, below `high`). Human sign-off line + T-11.1.1-06 accept-confirm stay in HQ-2 (do NOT block technical `verified`). Audit-trail row added.
