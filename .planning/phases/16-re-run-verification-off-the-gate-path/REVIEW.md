# Phase 16 — Code Review (S3-4)

**Reviewer:** orchestrator-direct (opus/high, LOOP-BRIEF §3 — code review tier).
**Method:** bounded diff, read every changed source, re-ran every gate here (§5 — not
subagent-trusted). Diff range `ec216b2..0bd6a75` (the four feature commits 16-01..04).
**Verdict: PASS — 0 blocking, 1 auto-fix applied and re-gated.**

## Scope of change (16 files, +745/−34)

| Area | Files | Notes |
|---|---|---|
| Gate check | `dsx/checks/repro.py` (+109) | `_check_reproduce_report` (DSX-REP-060/061), strict-only |
| Mint | `references/finding-codes.md` | 256→258, two HIGH rows, exact HQ-11 text |
| Skill | `skills/dsx-reproduce/SKILL.md` | new; `capabilities/dsx/capability.json` registers 14th skill |
| Template | `templates/REPRO-REPORT.md` | machine YAML block + status vocabulary (D-11) |
| Corpus (D-10) | 3 × `examples/known-bad/*-ATTRIBUTION.yaml`, `tests/test_known_bad_corpus.py` (+53) | additive `protocol_adherence` |
| Tests | `tests/test_reproduce_report.py` (new, 7), `tests/test_no_entrypoint_execution.py` (new, 3), `tests/test_finding_catalogue_invariant.py` (D-08 rebaseline) | |
| Artifacts | 4 × `16-0{1..4}-SUMMARY.md` | |

## The one finding — CONFIRMED, fixed (cross-phase test regression)

**F1 (blocking-until-fixed, correctness/test-coverage).** `tests/test_phase14_onboarding.py`
`test_req04_all_dsx_skills_carry_triggers` hard-coded `assertEqual(len(DSX_SKILLS), 13)`.
`DSX_SKILLS` is a live glob over `skills/dsx-*`; Phase 16 legitimately added the 14th DSX
skill (`dsx-reproduce`, REQ-P16-01, capability-registered), so the anti-vacuity/drop-detection
anchor was stale and the **full suite failed** (`14 != 13`). S3-3 ran only *targeted* tests and
never executed `scripts/check.sh`, so it did not surface this — precisely the cross-phase
regression S3-4 exists to catch.

- **Root cause, not symptom:** the failure short-circuited on the *count* assert (line 113),
  before the `Triggers:` assert (line 116). `dsx-reproduce`'s SKILL.md carries a `Triggers:`
  clause (`grep -c` = 1), so REQ-P14-04's actual invariant (every DSX skill carries Triggers)
  already held for all 14 — only the numeric anchor needed to move.
- **Fix (faithful, one-token semantics):** bumped the anchor 13→14 with a comment recording
  the Phase-16 growth; updated the module comment and the coverage-map docstring for internal
  consistency. Not a requirement change — REQ-P14-04's invariant is *strengthened* (now enforced
  across 14 skills) and Phase 14's other tests are untouched.
- **Re-gate:** `test_phase14_onboarding` 11 OK; full `scripts/check.sh` **all checks passed
  (Ran 1254 tests OK)**; capability manifest conformant at **14 skills**.

No `dsx/` gate code was involved in the fix (test-only), so gate-path purity is unaffected.

## Load-bearing re-runs (all real commands, §5)

- **Gate-path purity (D-01, REQ-P16-02):** only `dsx/checks/repro.py` changed under `dsx/`
  (`git diff --name-only ec216b2..0bd6a75 -- dsx/ scripts/`); `scripts/` clean. `repro.py`
  imports only `math`, `re`, `pathlib`, `..findings`, `..spec` — no pandas/scipy/numpy/csv,
  no subprocess/runpy/os.system/exec. The lone "numpy" token is inside DSX-REP-001's *remedy
  string*, not an import.
- **No entrypoint execution (REQ-P16-04, D-09):** `test_no_entrypoint_execution` 3 OK — static
  AST scan over `dsx/checks/`+`dsx/frame/` (asserted non-empty, incl. `code.py`+`repro.py`),
  positive control flags synthetic `subprocess.run`/`runpy.run_path`/`os.system`/`exec`,
  negative control does not flag `ast.*`/`re.compile`.
- **Reproduce-report behaviour (REQ-P16-02, D-02/D-04/D-11):** `test_reproduce_report` 7 OK —
  060 fires strict-only when declared-but-missing; 061 fires when numbers disagree *and* is not
  suppressed by a `status: reproduced` verdict (gate trusts numbers, not verdict); silent on
  absent field, on numeric overlap, and on honest `status: skipped/unable`. Good D-08 fixture
  stays silent (back-compat).
- **Codes both HIGH (D-05):** mint diff shows `DSX-REP-060`/`061` = HIGH (verify/ship block at
  HIGH — a MEDIUM code could not exit 1).
- **Catalogue additive (D-08):** `gen-finding-catalogue.py --check` exit 0; invariant 2 OK —
  `_EXPECTED_TOTAL=258`, separate `_SNAPSHOT_TOTAL=256`, set-identity vs `snapshot ∪ {060,061}`;
  `tests/fixtures/finding-codes-phase12.md` **byte-unchanged** over the feature commits.
- **protocol_adherence additive (REQ-P16-03, D-10):** `test_known_bad_corpus` 45 OK; diff is
  **0 deletions** (purely additive); closed vocab `{adhered,skipped,not_applicable}` on all 3
  sidecars; field proven **not** in `_headline.__code__.co_varnames`; `_headline` pinned to
  `(0.25, 0.3)`; the standalone headline anchor test present and unedited; ≥1 skipped case.
- **Citation authenticity:** the only new cited codes are 060/061 (self-minted, present in the
  catalogue); no dangling references introduced.

## Full gate
`sh scripts/check.sh` → **all checks passed** — Ran **1254** tests OK (1243→+11: reproduce_report 7
+ no_entrypoint_execution 3 + protocol_adherence 1); finding catalogue current; capability
conformant (14 skills); gate contract good/bad/missing; determinism identical.
