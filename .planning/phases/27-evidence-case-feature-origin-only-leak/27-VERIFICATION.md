---
phase: 27-evidence-case-feature-origin-only-leak
verified: 2026-09-07T00:00:00Z
status: passed
verdict: PASSED
score: 3/3 requirements MET (REQ-P27-01/02/03); DSX-ML-034 minted honestly under a secondary-corroborated D-05; corpus fixture a measured LIVE MISS; 3 review findings dispositioned (1 fixed WR-01, 2 accepted residuals)
behavior_unverified: 0
overrides_applied: 0
re_verification: false
gaps: []
human_verification:
  - "End-of-phase security sign-off (S3-5 /gsd-secure-phase 27) — batched to HUMAN-QUEUE, non-blocking until S7-2 per brief §6."
  - "End-of-phase UAT round (S3-5 /gsd-validate-phase 27) — batched, non-blocking until S7-2."
---

# Phase 27: Evidence case — feature-origin-only leak — Verification Report

**Phase Goal:** Build and MEASURE a known-bad corpus case whose leak is attributable
only through feature origin — an innocuous column name matching none of
`LEAKAGE_PATTERNS`, a leaking column arriving pre-joined so no fit/cleaning idiom is
visible, and every `model.*`/`results.*` declaration honest — then, because the case
was a measured LIVE MISS at all four gate points, mint the declaration-only check
`DSX-ML-034` (feature provenance) under the Kaufman et al. (2012) legitimacy
formulation, and wire the fixture into every corpus harness map as a MISS backed by an
ATTRIBUTION sidecar that promotes brief §6.5 item 7.

**Verified:** 2026-09-07 (orchestrator, all gates re-run on real Python 3.12.10 —
`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`; not trusted
from a subagent report).

**Status:** passed — 3/3 requirements MET.

## Verdict

`passed`. All three phase requirements are met. The `gsd-code-reviewer` (opus) returned
**0 BLOCKER / 0 HIGH / 1 MEDIUM / 2 LOW** and confirmed all six load-bearing invariants
HOLD (`27-REVIEW.md`). The one MEDIUM (WR-01) was a genuine robustness gap and is
**fixed**; the two LOW/info findings are accepted with recorded rationale. No
requirement is provisional. The D-13 "measured miss before any check is designed" rule
was satisfied at the prior firing (`27-MEASUREMENT.md`); the fixture remains a MISS
after this phase's fix.

## Requirement verdicts

### REQ-P27-01 — MET
A known-bad corpus case exists as four artifacts under `examples/known-bad/`:
`feature-origin-only-leak-ANALYSIS-SPEC.yaml`, `-entrypoint.py`, `-POSTMORTEM.md`,
`-ATTRIBUTION.yaml`. Its leak (`account_health_index`, recomputed nightly from
activity that includes the outcome window) is attributable only through feature
origin: the name clears all ten `LEAKAGE_PATTERNS`, the column arrives pre-joined so
no fit/cleaning idiom is visible to the entrypoint scan, and every declared field is
honest (no declaration contradicts). Enforced by `tests/test_known_bad_corpus.py`
(fixture present + entrypoint runnable) inside the passing 1599-test suite.

### REQ-P27-02 — MET
Because the case is a measured live miss, the optional `model.feature_provenance[]`
declaration (`{feature, source, available_at, derived_from}`, plus an additive
`waiver`) and its declaration-only check `_check_feature_provenance` (DSX-ML-034,
`dsx/checks/ml.py`) were minted and wired into the `check()` dispatch. It fires
CRITICAL for `available_at: after_prediction` and HIGH for an unwaived `unknown`;
after the S3-4 fix it also fires HIGH (waiver-suppressible) for any unattested value —
missing, blank, or off-vocabulary — so an omitted `available_at` is never more
permissive than an honest `unknown`. `before_prediction`/`at_prediction` clear.
Pinned by `tests/test_ml_feature_provenance.py` (9 tests: the six frozen §S3-1-CLOSE
behaviours + three WR-01 regressions). D-05 honesty preserved: the docstring and the
`# D-05:` marker state the Kaufman citation is secondary-corroborated with the primary
ACM PDF paywalled, asserting no page/section locator.

### REQ-P27-03 — MET
Corpus harness entries are complete and internally consistent (all enforced by the
passing suite): `_EXPECTED_CAUGHT_DEFECTS` = `frozenset()`, `_EXPECTED_VAL_CODES` =
`set()`, golden ship ledger `_GOLDEN_SHIP_FINDINGS` = `{CLM-031, COH-031, MET-040,
NAR-001}` with DSX-ML-034 deliberately ABSENT, spec count moved 42→43
(`tests/test_dsx.py`), catalogue set-identity 276→277. The ATTRIBUTION sidecar names
`absent_code: DSX-ML-034` and `promotes_backlog_item: "6.5-item-7-feature-provenance"`
(a member of `_SECTION_65_ITEM_IDS`); the sidecar is an honest miss attribution
because DSX-ML-034 is declaration-only and this honest spec declares no
`feature_provenance` block, so the code correctly stays silent at every gate point.
Brief §6.5 item 7 was rewritten with the measured evidence.

## Code review disposition (`27-REVIEW.md` — 0 BLOCKER / 0 HIGH / 1 MEDIUM / 2 LOW)

- **WR-01 (MEDIUM, `dsx/checks/ml.py`) — FIXED.** The branch chain had no terminal
  route for a missing/null/typo'd `available_at`, silently clearing it — an omitted
  availability was more permissive than an honest `unknown` (which fires HIGH), a
  one-token bypass and a mismatch with the docstring's "membership test against a
  closed vocabulary" claim. Fixed by broadening the HIGH branch to fire on any
  unattested value (unknown, blank, or off-vocabulary), waiver-suppressible, while
  preserving the HIGH-first / CRITICAL-second `report.add` lexical order so the
  catalogue row stays CRITICAL. Safe: the `feature_provenance` block is new this
  phase, so no shipped spec or fixture carries it and the broadening cannot
  false-positive on existing work (the MISS fixture has no block → early return, still
  a miss). Locked by three new regression tests; the deliberate declaration-text drift
  updated in `_CANONICAL_DECLARATIONS` (`tests/test_gen_finding_catalogue.py`) with
  its reason recorded.
- **L-01 (LOW) — ACCEPTED (documented residual).** A bare `waiver: true` silences the
  HIGH finding with no rationale. The waiver is a by-design escape hatch mirroring the
  standing "a frame that lies passes" limit; a structured-rationale requirement exceeds
  REQ-P27-02's declared field vocabulary (`{feature, source, available_at,
  derived_from}`) and is a separate, later decision.
- **L-02 (LOW, comment inaccuracy "nested one level deeper") — FIXED** as part of the
  WR-01 edit; the source-order note now correctly describes the branches as sibling
  `elif`s at the same nesting level.

## Gate evidence (orchestrator-re-run, real 3.12.10)

- Full suite: **1599 tests OK** (`unittest discover -s tests`), up from 1596 at S3-3
  by the three new WR-01 regression tests.
- Catalogue: `gen-finding-catalogue.py --check` exit 0, "finding catalogue is current";
  set-identity **276→277** (one DSX-ML-034 row); `references/finding-codes.md`
  byte-unchanged by the S3-4 fix; DSX-ML-034 renders **CRITICAL** (headline
  disposition preserved).
- `dsx/checks/dq.py`: byte-frozen across the phase (`git diff --stat dd930af..HEAD --
  dsx/checks/dq.py` empty) — the profiler-is-a-producer rule holds; the mint lives in
  `ml.py`.
- DSX-ML-034 is in `_D05_ALLOWLIST_CODES` (`gen-finding-catalogue.py`) and OUT of
  `_SECTION_65_BACKLOG_CODES` (minted, not reserved).
- `node install.mjs --check`: self-test passed (6/6 agents, 14/14 skills, 5 gates).

## Human verification (batched, non-blocking until S7-2)

1. Security sign-off (S3-5 `/gsd-secure-phase 27`) — SECURITY.md approval line.
2. UAT round (S3-5 `/gsd-validate-phase 27`).

Both filed to HUMAN-QUEUE per brief §6; neither blocks any earlier unit.
