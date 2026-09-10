---
phase: 29-evidence-case-subgroup-harm-prescriptive
verified: 2026-09-08T00:00:00Z
status: passed
verdict: PASSED
score: 3/3 requirements MET (REQ-P29-01/02/03); DSX-COH-041 minted honestly under a human-confirmed D-05 (Gail & Simon 1985, HQ-40 row 40e); corpus fixture a measured LIVE MISS promoted to the corpus's FIRST kind:target TARGET (DSX-COH-041 PRESENT/firing); 4 review findings dispositioned (3 fixed HG-01/MD-01/MD-02 strict tightenings, 1 accepted residual LW-01)
behavior_unverified: 0
overrides_applied: 0
re_verification: false
gaps: []
human_verification:
  - "End-of-phase security sign-off (S5-5 /gsd-secure-phase 29) — batched to HUMAN-QUEUE, non-blocking until S7-2 per brief §6."
  - "End-of-phase UAT round (S5-5 /gsd-validate-phase 29) — batched, non-blocking until S7-2."
---

# Phase 29: Evidence case — subgroup harm under a prescriptive recommendation — Verification Report

**Phase Goal:** Build and MEASURE a known-bad corpus case in which a prescriptive
recommendation with a positive overall effect declares `results.segments[]` where one
minority segment opposes the recommendation's direction at n above a declared floor with
no disposition — a shape `DSX-MET-030/031` structurally cannot fire on (fewer than half
the segments oppose) — then, because the case was a measured LIVE MISS at all four gate
points, mint the declaration-only check `_check_subgroup_harm_disposition` (`DSX-COH-041`)
under the Gail & Simon (1985) motivating definition of qualitative interaction, and promote
the corpus's FIRST `kind: target` fixture in which the newly-minted code is PRESENT and
fires (the load-bearing inverse of the Phase-27/28 permanent misses, D-29-00), backed by an
ATTRIBUTION sidecar that promotes brief §6.5 item 9.

**Verified:** 2026-09-08 (orchestrator, all gates re-run on real Python 3.12.10 —
`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`; not trusted from a
subagent report).

**Status:** passed — 3/3 requirements MET.

## Verdict

`passed`. All three phase requirements are met. The `gsd-code-reviewer` (opus) returned
**0 BLOCKER / 1 HIGH / 2 MEDIUM / 1 LOW** and confirmed five of six load-bearing invariants
hold outright (`29-REVIEW.md`); the sixth (check correctness) surfaced three silent-evasion
gaps in the freshly-minted check. All three (HG-01, MD-01, MD-02) are **fixed** — each a
strict tightening that aligns the code with the FROZEN design (MD-01/MD-02 with the SETTLED
D-29-01 "no escape by omission"; HG-01 with the D-29-03 discuss recommendation the plan
under-specified) and leaves the shipped TARGET fixture and all gate evidence unchanged. The
one LOW (LW-01, catalogue last-seen-dedup renders the two-severity code as HIGH) is the
established repo-wide DSX-COH-030 convention — **accepted** as a documented residual, out of
Phase-29 scope. No requirement is provisional. The D-13 "measured miss before any check is
designed" rule was satisfied at the prior firings (`29-MEASUREMENT.md`, `VERDICT: LIVE
MISS`); after this phase's fixes the fixture is still a caught TARGET (DSX-COH-041 fires).

## Requirement verdicts

### REQ-P29-01 — MET
A known-bad corpus case exists as four artifacts under `examples/known-bad/`:
`subgroup-harm-without-disposition-{ANALYSIS-SPEC.yaml,entrypoint.py,POSTMORTEM.md,
ATTRIBUTION.yaml}`. It is a genuinely prescriptive recommendation with a declared positive
`results.overall_effect` (+3.2pp, n-weighted 320/10000) and four declared `results.segments[]`
(A +5.0pp/n4000, B +4.0pp/n3000, C +3.0pp/n2000, D **−6.0pp/n1000**): a single minority
segment D opposes the recommendation's direction at n=1000, well above the declared
`decision.subgroup_harm_floor: 500`, with no `decision.subgroup_harm[]` disposition — the
sole defect. Only 1 of 4 segments opposes, so `DSX-MET-030` (needs ALL opposing,
`metrics.py:316`) and `DSX-MET-031` (needs ≥half, `:334`) structurally cannot fire.
Measured live before any check was designed: `29-MEASUREMENT.md` records `VERDICT: LIVE
MISS`, independently re-run by the orchestrator on real 3.12.10 (the DEFECT fixture exits 0
at validate/plan/execute/verify/ship, CRITICAL=[] HIGH=[] at every point; the D→+0.06 swap
counterfactual toggles nothing, so no existing code was a latent catch; only `DSX-STA-011`
MEDIUM fires as a swap-invariant orthogonal aggregate-effect-size note). Enforced by
`tests/test_known_bad_corpus.py` inside the passing 1627-test suite.

### REQ-P29-02 — MET
The primary enforcement source — **Gail & Simon (1985), Biometrics 41(2):361-372, PMID
4027319**, the qualitative/crossover-interaction definition (treatment effects of opposite
sign across subsets) — was read at its locator and CONFIRMED by the operator (HQ-40 row
40e). It is cited as the MOTIVATING DEFINITION only, never as authority for the enforcement
mechanic (D-02: the check computes no statistic; Gail & Simon's paper is a likelihood-ratio
TEST the code does not run). One documented public case where an average benefit masked
subgroup harm was found by phase research with a primary source: **Obermeyer, Powers, Vogeli
& Mullainathan (2019), "Dissecting racial bias in an algorithm used to manage the health of
populations," Science 366(6464):447-453, DOI 10.1126/science.aax2342** (`29-RESEARCH.md`),
confirmed at its locator this milestone via Crossref (publisher metadata) + Semantic Scholar
(verbatim abstract) — at **abstract + metadata grade**, with the honest boundary recorded
that the paper body was not read here and that Obermeyer is a label-bias/allocation-fairness
case (a real-world instance of the broader "average benefit masks subgroup harm" phenomenon),
NOT itself a Gail & Simon opposite-sign contrast. The two sources fill REQ-P29-02's two
distinct roles (enforcement definition vs documented public case), neither doing the other's
job. Pinned by `tests/test_subgroup_harm_disposition.py` (`# D-05: DSX-COH-041` marker at
lines 10/81); DSX-COH-041 is in `_D05_ALLOWLIST_CODES` by exact code.

### REQ-P29-03 — MET
Because REQ-P29-01 is a measured live miss and REQ-P29-02's source is confirmed, the optional
`decision.subgroup_harm[]` declaration (`{segment, effect, ci, n, disposition: accept |
exclude | mitigate, rationale}`, additive to the template) and its declaration-only check
`_check_subgroup_harm_disposition` (`DSX-COH-041`, `dsx/checks/coherence.py:223`) were minted
and dispatched from the coherence family `check()`. It fires when a prescriptive question
declares an opposite-sign segment at n ≥ `decision.subgroup_harm_floor` (default 0; sign test
reused verbatim from `metrics.py`, never recomputed) that carries no matching
`decision.subgroup_harm[]` row **or** a row with no valid disposition → CRITICAL; a matching
`accept` row with a blank rationale → HIGH (one code, two severities per REQ-P29-03,
per-segment mutually exclusive). D-06 assigned the next-free `DSX-COH-041` in the 04x
decision-obligation tier (veto window opened, silence = accept). Corpus harness entries are
complete and internally consistent (all enforced by the passing suite): this fixture is a
post-mint **TARGET**, not a Phase-27/28 permanent miss (D-29-00 — the missing-row CRITICAL
fires on the honestly-declared opposing segment), so `_TARGET_DEFECT_CODES[slug]` =
`{plan/verify/ship: DSX-COH-041}`, `_EXPECTED_CAUGHT_DEFECTS[slug]` = `frozenset()`,
`_EXPECTED_VAL_CODES` = `set()`, and the golden ship ledger `_GOLDEN_SHIP_FINDINGS[slug]` =
`frozenset({DSX-COH-041})` (PRESENT — it fires live, re-measured, not statically pinned). The
ATTRIBUTION closed vocabulary was extended to `("miss", "caught", "target")` and the
ATTRIBUTION sidecar is the corpus's FIRST `kind: target`, naming `promotes_backlog_item:
6.5-item-9-subgroup-harm-declaration` (a member of `_SECTION_65_ITEM_IDS`); DSX-COH-041 is
OUT of `_SECTION_65_BACKLOG_CODES` (a real mint). Spec count moved 44→45; catalogue
set-identity 278→279 (minted at Wave 1). Brief §6.5 item 9 was rewritten with the measured
evidence. `_ABSENT_PARTITION_FLOOR` stays 3 (untouched).

## Code review disposition (`29-REVIEW.md` — 0 BLOCKER / 1 HIGH / 2 MEDIUM / 1 LOW)

- **HG-01 (HIGH, `dsx/checks/coherence.py`) — FIXED.** Once a `subgroup_harm[]` row named
  the segment, the only remaining emit required `disposition == "accept"` + blank rationale,
  so a content-free `- segment: D` (no or unrecognised disposition) fell through both
  branches and silenced the CRITICAL entirely — the "force disclosure" guarantee defeated by
  a declaration that discloses nothing. The plan (S5-2) enumerated only the two REQ-P29-03
  severities and **under-specified**, neither carrying nor explicitly rejecting the discuss
  round's own D-29-03 recommendation ("unknown `disposition` / row missing a required key →
  CRITICAL"). Fixed by validating the disposition against the closed vocabulary
  `{accept, exclude, mitigate}`; an invalid/missing disposition on a matching row now fires
  CRITICAL — implementing D-29-03's recommendation, a strict tightening (D-13-safe: catches
  more gaming, reshapes no fixture) that leaves the shipped TARGET fixture unchanged (it
  declares no `subgroup_harm` row → still the `row is None` CRITICAL). Still one code / two
  severities. Same class as the Phase-27 WR-01 fix → applied solo with a loud recorded
  rationale, no persona fork. Locked by three new unit tests.
- **MD-01 (MEDIUM, `dsx/checks/coherence.py:258`) — FIXED.** The borrowed `len(segments) < 2`
  guard contradicts the SETTLED D-29-01 per-segment semantics (each opposing segment is
  judged against `overall_effect` alone; the ≥2-to-compare rationale of `_check_simpsons_paradox`
  does not transfer). Changed to `not segments`. Locked by `test_lone_opposing_segment_critical`.
- **MD-02 (MEDIUM, `dsx/checks/coherence.py:277-280`) — FIXED.** A declared opposing segment
  omitting `n` escaped even the strict default floor 0, contradicting the SETTLED D-29-01 "no
  escape by omission / maximally strict". A missing `n` now reads as 0. Locked by
  `test_opposing_segment_missing_n_fires_at_default_floor` (fires at default floor 0; still
  ruled out by an affirmatively-declared floor above 0 — the floor mechanism intact).
- **LW-01 (LOW, `references/finding-codes.md:357`) — ACCEPTED (documented residual).** The
  catalogue renders DSX-COH-041 as `HIGH` via the last-seen-dedup convention though its
  load-bearing severity is CRITICAL. This is the established repo-wide DSX-COH-030 convention
  (pinned in `test_gen_finding_catalogue.py`); changing it is a cross-cutting generator
  behavior change touching every two-severity code and risks the catalogue byte-determinism
  invariant — out of Phase-29 scope. Both severities are proven to fire live by the unit tests.

## Gate evidence (orchestrator-re-run, real 3.12.10)

- Full suite: **1627 tests OK** (`unittest discover -s tests`), 1622 + 5 new S5-4 regressions.
- Catalogue: `gen-finding-catalogue.py --check` exit 0, "finding catalogue is current";
  set-identity **279** (behavior-only change, mints nothing); `references/finding-codes.md`
  byte-unchanged by the S5-4 fixes; DSX-COH-041 renders **HIGH** (last-seen dedup — see
  LW-01; both severities fire live). All count pins at 279.
- `dsx/checks/dq.py` and `dsx/cli.py`: byte-frozen across the phase (empty diff) — the
  profiler-is-a-producer rule holds; the mint lives in `coherence.py`, registered through the
  existing coherence family dispatch with no `cli.py` edit.
- DSX-COH-041 is in `_D05_ALLOWLIST_CODES` (`gen-finding-catalogue.py`) and OUT of
  `_SECTION_65_BACKLOG_CODES` (minted, not reserved).
- TARGET polarity intact: the promoted fixture fires DSX-COH-041 at plan/verify/ship
  (`test_known_bad_corpus` green in-suite); golden set present, `_EXPECTED_CAUGHT_DEFECTS`
  empty, `kind: target` vocab routed correctly at every `kind`-switch.
- `node install.mjs --check`: self-test passed (6/6 agents, 14/14 skills, 5 gates).
- S5-4 working-tree change scope: `dsx/checks/coherence.py` +
  `tests/test_subgroup_harm_disposition.py` + `tests/test_gen_finding_catalogue.py` (the
  `_CANONICAL_DECLARATIONS` pin gained the third DSX-COH-041 declaration deliberately). No
  `scripts/`, `references/`, `templates/`, `examples/` touched.

## Human verification (batched, non-blocking until S7-2)

1. Security sign-off (S5-5 `/gsd-secure-phase 29`) — SECURITY.md approval line.
2. UAT round (S5-5 `/gsd-validate-phase 29`).

Both filed to HUMAN-QUEUE per brief §6; neither blocks any earlier unit.
