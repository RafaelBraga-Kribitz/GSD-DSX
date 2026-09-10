---
phase: 28-evidence-case-magnitude-no-test-computed
verified: 2026-09-08T00:00:00Z
status: passed
verdict: PASSED
score: 3/3 requirements MET (REQ-P28-01/02/03); DSX-CLM-034 minted honestly under a human-confirmed D-05 (Wilkinson & TFSI 1999, read in full primary text — HQ-40 row 40c); corpus fixture a measured LIVE MISS; 3 review findings dispositioned (2 fixed WR-01/IN-02, 1 accepted+tracked residual IN-01)
behavior_unverified: 0
overrides_applied: 0
re_verification: false
gaps: []
human_verification:
  - "End-of-phase security sign-off (S4-5 /gsd-secure-phase 28) — batched to HUMAN-QUEUE, non-blocking until S7-2 per brief §6."
  - "End-of-phase UAT round (S4-5 /gsd-validate-phase 28) — batched, non-blocking until S7-2."
---

# Phase 28: Evidence case — magnitude no test computed — Verification Report

**Phase Goal:** Build and MEASURE a known-bad corpus case whose readout asserts a
magnitude for which no reported test computed the effect — using the collision/mislabel
construction (the claim's 27%/18% are the REAL reported numbers of OTHER metrics, so the
existing `DSX-CLM-033` union-membership check clears while no test computed the CLAIMED
metric) — then, because the case was a measured LIVE MISS at all four gate points, mint
the declaration-only traceability check `DSX-CLM-034` (`claims[].supported_by` → cited
test) under the Wilkinson & TFSI (1999) motivating principle, and wire the fixture into
every corpus harness map as a MISS (with the swap-invariant `DSX-COH-001` recorded as a
point-scoped incidental via the new `_PER_FIXTURE_INCIDENTAL_CODES` map, D-28-06) backed
by an ATTRIBUTION sidecar that promotes brief §6.5 item 8.

**Verified:** 2026-09-08 (orchestrator, all gates re-run on real Python 3.12.10 —
`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`; not trusted
from a subagent report).

**Status:** passed — 3/3 requirements MET.

## Verdict

`passed`. All three phase requirements are met. The `gsd-code-reviewer` (opus) returned
**0 BLOCKER / 0 HIGH / 1 MEDIUM / 2 LOW** and confirmed all seven load-bearing
invariants PASS on mechanical verification (`28-REVIEW.md`). The one MEDIUM (WR-01) and
the sibling LOW (IN-02) were stale-documentation drift in the catalogue-invariant test
and are **fixed**; the remaining LOW (IN-01) is a latent, no-live-trigger asymmetry whose
correct resolution is a genuine opposed design judgment — **accepted and tracked**, not
settled by a rushed solo behavior change on a minted check. No requirement is provisional.
The D-13 "measured miss before any check is designed" rule was satisfied at the prior
firings (`28-MEASUREMENT.md`, `VERDICT: LIVE MISS`); the fixture remains a MISS after this
phase's fix.

## Requirement verdicts

### REQ-P28-01 — MET
A known-bad corpus case exists as four artifacts under `examples/known-bad/`:
`magnitude-without-computed-effect-{ANALYSIS-SPEC.yaml,entrypoint.py,POSTMORTEM.md,
ATTRIBUTION.yaml}`. Its magnitude claim (an `association` churn claim "27% vs 18%") names
figures no `results.tests[]` entry computed for the claimed metric — the two reported
tests carry effect sizes and intervals for OTHER metrics (`revenue_per_user` 0.27,
`activation_rate` 0.18), so the claimed 27/18 clear `DSX-CLM-033`'s all-tests union
membership via the ×100 percent/proportion scale bridge while no test measured the
claimed metric. Every existing claims/narrative/stats check passes at the default
threshold (`DSX-CLM-070` cleared by a declared base; `DSX-STA-011/012` cleared by the
reported tests' effect sizes). Measured live before any check was designed: `28-MEASUREMENT.md`
records `VERDICT: LIVE MISS`, independently re-run by the orchestrator on real 3.12.10
(validate=0; plan/verify/ship=1 CRITICAL `DSX-COH-001` only; execute=0; `DSX-CLM-033`
silent at verify/ship; honest-swap no-toggle; break-swap makes `DSX-CLM-033` fire —
proving it metric-blind, so its silence IS the miss). Enforced by
`tests/test_known_bad_corpus.py` inside the passing 1615-test suite.

### REQ-P28-02 — MET
Because the case is a measured live miss, the declaration-level cross-reference
`claims[].supported_by` (naming the `results.tests[]` entry a claim rests on, additive to
the template with a `claims[].rounding` sig-figs field) and its declaration-only check
`_check_supported_by_traceability` (DSX-CLM-034, HIGH, `dsx/checks/claims.py:477`) were
minted and wired into the per-claim dispatch (`claims.py:84`). It early-returns on an
absent `supported_by` (attribution, not detection), then fires HIGH when a claim
magnitude does not trace to the cited test's reported numbers (effect, the ×100 pp/%
bridge `DSX-CLM-033` already uses, or a CI bound) to `claims[].rounding` significant
figures (default 2); its reconciliation window is never looser than `DSX-CLM-033`'s. It
is a text-to-declared-number overlap, never a recomputation. D-05 honesty: the docstring
and the `# D-05: DSX-CLM-034` marker cite Wilkinson & TFSI (1999) as the MOTIVATING
PRINCIPLE only and explicitly disclaim any numeric-overlap mandate — the citation was
read in full primary text and CONFIRMED at its locator by the operator (HQ-40 row 40c;
JARS–Quant 2018 dropped as weaker/wrong-edition). D-06 assigned the next-free `DSX-CLM-034`.
Pinned by `tests/test_claims_supported_by.py` (7 tests, `# D-05:` marker at line 11);
DSX-CLM-034 is in `_D05_ALLOWLIST_CODES` by exact code.

### REQ-P28-03 — MET
Corpus harness entries are complete and internally consistent (all enforced by the
passing suite): `_EXPECTED_CAUGHT_DEFECTS[slug]` = `frozenset()`, `_EXPECTED_VAL_CODES` =
`set()`, golden ship ledger `_GOLDEN_SHIP_FINDINGS` = `{DSX-COH-001}` with DSX-CLM-034
deliberately ABSENT (the target defect is missed; DSX-COH-001 is the swap-invariant
incidental), spec count moved 43→44 (`tests/test_dsx.py`), catalogue set-identity 277→278.
The measured incidental `DSX-COH-001` — which is another slug's legitimate target and so
fits neither the global `_INCIDENTAL_GAP_CODES` nor any own-target map — is recorded in
the new point-scoped `_PER_FIXTURE_INCIDENTAL_CODES` (D-28-06), read ONLY by the two
completeness tests, never by `_own_target_codes`/`_effective_target_map`/`_classify_target_defect`'s
target logic; its anti-laundering guard requires every per-fixture incidental to be
another slug's declared target (strictly narrower than the global list), and the defaulted
`incidental=` parameter leaves every existing call site byte-identical. The ATTRIBUTION
sidecar names `absent_code: DSX-CLM-034`, `promotes_backlog_item:
"6.5-item-8-magnitude-without-computed-effect"` (a member of `_SECTION_65_ITEM_IDS`), and
`kind: miss`; the fixture declares no `supported_by` on the magnitude claim, so the mint
correctly stays silent (honest miss). Brief §6.5 item 8 was rewritten with the measured
evidence (the scope's literal "no test at all" shape recorded as the `DSX-CLM-033` no-mint
control).

## Code review disposition (`28-REVIEW.md` — 0 BLOCKER / 0 HIGH / 1 MEDIUM / 2 LOW)

- **WR-01 (MEDIUM, `tests/test_finding_catalogue_invariant.py`) — FIXED.** The
  catalogue-count invariant test was named `test_finding_catalogue_stays_at_277_codes`
  with a docstring and failure message asserting 277, while its assertions correctly use
  `_EXPECTED_TOTAL = 278` — a green test whose name lies about the enforced invariant, a
  direct violation of the phase's own "count pins moved to 278 in lockstep" discipline.
  Fixed by renaming the method to `test_finding_catalogue_stays_at_278_codes` and updating
  the docstring and failure-message prose to read 278 and to name DSX-ML-034 (Phase 27)
  and DSX-CLM-034 (Phase 28) in the mint chain, matching `_MINTED_CODES`. Test-doc only —
  no assertion or behavior change; the full suite is still 1615 OK.
- **IN-02 (LOW, `tests/test_finding_catalogue_invariant.py`) — FIXED** in the same edit.
  The set-identity test's docstring enumerated the sanctioned mints ending at Phase 22's
  DSX-VIZ-071 and never named DSX-ML-034 / DSX-CLM-034 though `_MINTED_CODES` includes both;
  the enumeration was extended to match.
- **IN-01 (LOW, `dsx/checks/claims.py`) — ACCEPTED (documented, tracked residual).**
  DSX-CLM-034 folds a claim's own declared `claim.ci` into `claim_numbers` (via the shared
  `_extract_claim_magnitudes`) but not into `reference`, unlike `DSX-CLM-033`, which
  appends `claim.ci` to its own `reference` so a self-declared interval is self-consistent.
  A future honest spec that both declares `supported_by` AND its own `claim.ci` diverging
  from the cited test's CI would then false-fire HIGH. This is latent, not live: no shipped
  spec reaches the path (the promoted fixture declares no `supported_by`, so the check
  early-returns at `claims.py:514`; the committed good/bad specs pair no `supported_by`
  with a divergent `claim.ci`). The correct resolution is a genuine opposed design
  judgment — `DSX-CLM-033` treats a self-declared CI as legitimate self-consistency, while
  `DSX-CLM-034`'s stricter "trace to THIS cited test" purpose arguably requires a declared
  CI to come from the cited test — so it is deferred to a recorded decision (a persona
  round) rather than settled by a rushed solo behavior change on a minted check at the
  pacing boundary. **Tracked** for a future decision (candidate: Phase 30 or a follow-on).

## Gate evidence (orchestrator-re-run, real 3.12.10)

- Full suite: **1615 tests OK** (`unittest discover -s tests`), unchanged from S4-3 — the
  WR-01/IN-02 fixes are docstring/method-name only.
- Catalogue: `gen-finding-catalogue.py --check` exit 0, "finding catalogue is current";
  set-identity **277→278** (one `DSX-CLM-034 | HIGH` row); `references/finding-codes.md`
  byte-unchanged by the S4-4 fix; DSX-CLM-034 renders **HIGH** (headline disposition
  preserved). All count pins at 278.
- `dsx/checks/dq.py`: byte-frozen across the phase (`git diff --stat caa9e4f..HEAD --
  dsx/checks/dq.py` empty) — the profiler-is-a-producer rule holds; the mint lives in
  `claims.py`.
- DSX-CLM-034 is in `_D05_ALLOWLIST_CODES` (`gen-finding-catalogue.py`) and OUT of
  `_SECTION_65_BACKLOG_CODES` (minted, not reserved).
- `node install.mjs --check`: self-test passed (6/6 agents, 14/14 skills, 5 gates).
- S4-4 working-tree change scope: `tests/test_finding_catalogue_invariant.py` only (no
  `dsx/`, `scripts/`, `references/`, `templates/`, `examples/` touched).

## Human verification (batched, non-blocking until S7-2)

1. Security sign-off (S4-5 `/gsd-secure-phase 28`) — SECURITY.md approval line.
2. UAT round (S4-5 `/gsd-validate-phase 28`).

Both filed to HUMAN-QUEUE per brief §6; neither blocks any earlier unit.
