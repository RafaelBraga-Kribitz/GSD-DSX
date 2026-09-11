---
phase: 29-evidence-case-subgroup-harm-prescriptive
plan: 01
subsystem: dsx/checks/coherence + finding-catalogue
tags: [D-13, live-miss, mint, DSX-COH-041, subgroup-harm, prescriptive, D-05, tdd]
requires:
  - "29-CONTEXT.md D-29-00..05 — frozen before the measurement began (guardrail 1)"
  - "29-RESEARCH.md — Obermeyer et al. 2019 confirmed at its locator (the REQ-P29-02 case source)"
provides:
  - "29-MEASUREMENT.md: VERDICT LIVE MISS — validate and all four gate points exit 0 on the frozen D-29-02 spike; DSX-MET-030/031 silent at 1-of-4 opposing; the swap counterfactual toggles nothing"
  - "dsx/checks/coherence.py::_check_subgroup_harm_disposition — DSX-COH-041, one code, two literal severities (missing disposition row CRITICAL / accept without rationale HIGH), dispatched from coherence.check() at :54"
  - "templates/ANALYSIS-SPEC.yaml: additive commented-optional decision.subgroup_harm[] and decision.subgroup_harm_floor"
  - "tests/test_subgroup_harm_disposition.py carrying the `# D-05: DSX-COH-041` marker (Gail & Simon 1985 as motivating definition only)"
  - "catalogue 278 -> 279 with the four count pins moved in lockstep; DSX-COH-041 in _D05_ALLOWLIST_CODES by exact code"
affects:
  - "Plan 29-02 (spike promoted to examples/known-bad/ as the corpus's first kind: target fixture); brief §6.5 item 9"
tech-stack:
  added: []
  patterns:
    - "measure-first D-13 spike under the phase's spike/ directory (Phase 27/28 precedent), promoted only after the verdict"
    - "a D-05 obligation lands in a brand-new sub-check, never folded into a legacy uncited docstring"
    - "exact-code _D05_ALLOWLIST_CODES entry, never a family prefix"
key-files:
  created:
    - 29-MEASUREMENT.md (this directory)
    - spike/subgroup-harm-without-disposition-{ANALYSIS-SPEC.yaml,entrypoint.py,NARRATIVE.md,MEASURE.py}
    - tests/test_subgroup_harm_disposition.py
  modified:
    - dsx/checks/coherence.py
    - templates/ANALYSIS-SPEC.yaml
    - scripts/gen-finding-catalogue.py
    - references/finding-codes.md
    - tests/test_finding_catalogue_invariant.py
    - tests/test_phase20_zero_mint_close.py
    - tests/test_p19_categorical_rows.py
    - tests/test_gen_finding_catalogue.py
decisions:
  - "Field name finalised as decision.subgroup_harm_floor and function name as _check_subgroup_harm_disposition (the plan's recorded_authoring_choices)"
  - "No dsx/cli.py edit: the coherence family already registers at plan/verify/ship and is absent from execute, so the new sub-check inherits that registration"
requirements-completed: [REQ-P29-01, REQ-P29-03]
metrics:
  completed: 2026-09-08
status: complete
---

# Phase 29 Plan 01: D-13 measurement + DSX-COH-041 mint — Summary

> Provenance. This summary was written on 2026-09-11, after the v2.6.0 ship, from the
> plan's own measurement record (`29-MEASUREMENT.md`, including its Task 4 Branch B
> closure) and the two commits that carried the work — `ff279d2` (measurement,
> 2026-09-08) and `b41eee2` (mint, 2026-09-08). The executing firings wrote the
> measurement record but never the summary file the plan's `<output>` asked for; the
> gap was found in the post-ship liability review. Nothing below is reconstructed from
> memory: every number was re-checked against the record or the tree on 2026-09-11.

Measured the brief §6.5 item 9 case live first (D-13), found it a LIVE MISS, and only then
minted `DSX-COH-041`: a declaration-only disposition obligation for an honestly-declared
minority segment that opposes a positive aggregate under a prescriptive recommendation.

## Task 1 — the D-13 act (commit `ff279d2`)

- Frozen D-29-02 spike authored under `spike/` (not `examples/known-bad/`): a
  prescriptive retention-rollout recommendation, `results.overall_effect: 0.032`, four
  declared segments — A n=4000 +5.0pp, B n=3000 +4.0pp, C n=2000 +3.0pp, D n=1000 −6.0pp —
  `decision.subgroup_harm_floor: 500`, and **no** `decision.subgroup_harm[]` row. That
  omission is the sole defect; segment D was not shaved toward a trivial n or effect.
- Gate protocol run from a fresh `tempfile.TemporaryDirectory()` per point on CPython
  3.12.10 (`subgroup-harm-without-disposition-MEASURE.py` is the driver): validate, plan,
  execute, verify, ship all **exit 0**; no CRITICAL or HIGH finding at any point.
- The structural seam confirmed by arithmetic before interpreting: `DSX-MET-030` needs
  every segment opposing (`1 == 4` is False) and `DSX-MET-031` needs at least half
  (`1 >= 2.0` is False), so both are silent at 1-of-4 — and the Simpson's check's `else`
  branch emits a reassuring "directionally consistent" INFO on the defect.
- Swap-still-fires counterfactual applied by literal code (segment D flipped to +0.06):
  nothing toggles at any point, so there is no existing catch to subtract. `DSX-STA-011`
  (MEDIUM, aggregate effect size) fires identically in both variants and never blocks.
- `29-MEASUREMENT.md` written with `VERDICT: LIVE MISS` as its first content line.

## Tasks 2–3 — RED then GREEN on the LIVE MISS branch (commit `b41eee2`)

- `tests/test_subgroup_harm_disposition.py`: seven test methods at the mint commit, one
  per behaviour bullet (missing-row CRITICAL, accept-blank-rationale HIGH, matching row
  with rationale silent, floor boundary with the just-touching `n == floor` case, sign
  gate, default floor zero, empty early return), carrying the standalone
  `# D-05: DSX-COH-041` marker and the Gail & Simon motivating-definition phrasing. RED
  before the check existed, GREEN after. (The S5-4 code review, commit `bf8f2cb`, later
  added five strict-tightening methods; the module has 12 today.)
- `dsx/checks/coherence.py::_check_subgroup_harm_disposition` (`:223`), dispatched from
  `coherence.check()` (`:54`): returns early unless `question_type` is prescriptive and
  `results.overall_effect` plus `results.segments[]` are present; reuses the `_sign`
  convention from `metrics.py`; a harmed segment (`_sign(effect) == -_sign(overall)` and
  `n >= decision.subgroup_harm_floor`, default 0) with no matching `decision.subgroup_harm[]`
  row fires `DSX-COH-041` CRITICAL, an `accept` row with a blank rationale fires HIGH, and
  a row with a rationale is silent. Both severities are string literals. The CI arm of the
  trigger is written in but latent — `results.segments[]` carries no `ci` field.
- Docstring satisfies the D-05 gate: a `Citation:` line (Gail, M. & Simon, R. (1985),
  Biometrics 41(2):361–372, PMID 4027319) as the **motivating definition** of a
  qualitative/crossover interaction only, a `Structural criterion:` line, and the
  bounded-catch statement — attribution over honestly-declared segments, not detection
  of hidden, mis-signed or omitted harm. No claim that Gail & Simon authorise the mechanic.
- `templates/ANALYSIS-SPEC.yaml`: `decision.subgroup_harm[]` (segment, effect, ci, n,
  disposition, rationale) and `decision.subgroup_harm_floor` added as commented-optional
  keys (`:58-67`); `dsx/spec.py` untouched.
- `scripts/gen-finding-catalogue.py`: `DSX-COH-041` added to `_D05_ALLOWLIST_CODES` by
  exact code (`:229`); catalogue regenerated — exactly one `DSX-COH-041` row after
  `DSX-COH-040`, `**Total: 279 codes.**`, byte-identical on a second `--write`.
- Four count pins moved 278 → 279 in lockstep: the catalogue Total, `_EXPECTED_TOTAL` in
  `tests/test_finding_catalogue_invariant.py`, `_declared_total(_CATALOGUE)` in
  `tests/test_phase20_zero_mint_close.py`, `_EXPECTED_TOTAL` in
  `tests/test_p19_categorical_rows.py`. The frozen 256 (Phase 12) and 275 baselines were
  not touched.

## Task 4 — Branch B closure

Recorded in `29-MEASUREMENT.md` ("Task 4 — Branch B closure"): the disposition tests GREEN,
`gen-finding-catalogue.py --check` exit 0 at 279, full suite OK (1622 tests at the time),
`dsx/checks/dq.py` byte-frozen, single-writer tracking files untouched. The phase handed
off to Plan 29-02 for promotion of the spike as a `kind: target` fixture (D-29-00).

## Deviations from plan

- The summary file itself was not produced by the executing firing (this document, dated
  above, closes that gap). No other deviation: the frozen D-29-02 case was not widened,
  nothing was minted before the verdict, and `dsx/checks/dq.py` was not modified.

## Verification (re-run 2026-09-11 on the current tree)

- `grep -c "    def test_" tests/test_subgroup_harm_disposition.py` → 12;
  `git show b41eee2:tests/test_subgroup_harm_disposition.py | grep -c "    def test_"` → 7.
- `references/finding-codes.md:16` → `**Total: 279 codes.**`; the three test pins read 279.
- `dsx/checks/coherence.py:54` dispatches `_check_subgroup_harm_disposition`, defined at `:223`.
