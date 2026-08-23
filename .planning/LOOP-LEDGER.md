# LOOP-LEDGER — v2.0.0 completion backlog

Source of truth for the autonomous loop. One checkbox = one wakeup unit.
Check a box ONLY with its gate evidence pasted in the log. Derived from
`.planning/v2.0.0-MILESTONE-AUDIT.md` (2026-08-23, gaps_found, 49/75).

## S0 — Hygiene and open gates

- [ ] S0-1 Execute Phase 11.1.1 plan 06 (malformed-.ipynb traceback fix; already written and gate-passed). Gate: the seven malformed inputs exit as gate findings, not raw tracebacks; suite green.
- [ ] S0-2 Execute Phase 11.1.1 plan 07 (README malformed-notebook claim correction; already written). Gate: README claim matches actual behaviour.
- [ ] S0-3 Write Phase 11.1.1 plan 08 (Option B from UAT: unscannable entrypoint must surface in `dsx check code` / `dsx explain`, not silently pass) via `/gsd-plan-phase 11.1.1 --gaps`, then execute it. Gate: unscannable entrypoint produces a visible finding + decision record.
- [ ] S0-4 Re-run `/gsd-secure-phase 11.1.1`. Gate: SECURITY.md `verified`, threats_open 0 (T-11.1.1-06 redisposition to "accept" goes to HUMAN-QUEUE HQ-2). Human sign-off line → HQ-2.
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
