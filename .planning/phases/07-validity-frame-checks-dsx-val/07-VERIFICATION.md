---
phase: 07-validity-frame-checks-dsx-val
verified: 2026-08-20T00:00:00Z
status: passed
score: 5/5 roadmap success criteria verified; 8/9 requirements MET, 1/9 PARTIAL by deliberate scope decision (not a gap)
behavior_unverified: 0
overrides_applied: 0
re_verification: true
re_verification_context:
  previous_status: human_needed
  previous_score: "8/9 requirements MET, 1/9 PARTIAL (documented deferral, not a gap)"
  gaps_closed:
    - "Human item (a): whether Chan & Perry (2017) (Google technical report) clears D-05's vendor-blog/marketing exclusion for the weak-identification-mmm post-mortem citation — closed. 07-UAT.md test 6 (result: pass) is the human's recorded verdict: primary PDF spot-checked (authors, year, title, venue, both URLs, all four section numbers/titles confirmed), and the human explicitly recorded a qualification (the report is admissible on structure — abstract, numbered sections, reference list — as 'primary OR peer-reviewed', not requiring peer review specifically) rather than silently accepting it."
    - "Human item (b): whether the two D-05 honesty disclosures (five-field estimand decomposition; CONSTRAINT_SOURCES partition) read as adequate, honest prose — closed. 07-UAT.md test 2 (estimand decomposition, result: pass) and test 5 (CONSTRAINT_SOURCES four-way partition and identification citation, result: pass, 'User verified all three sites') are the human's recorded verdicts."
    - "Gap G-07-4 (Kish 1965 citation contradiction, severity major, found at first UAT pass) closed by plan 07-08 under remedy reading_b: section 8.2/page 258 kept as a confirmed locator in dsx/frame/val.py (two sites) and dsx/mathx.py, disclosure narrowed to state only the design-effect *formula's* section number is unverified, brief.md section 7 reworded to match. TestKishCitationCoherence (3 tests) added and independently re-run in this verification: 3/3 pass."
  gaps_remaining: []
  regressions: []
gaps: []
human_verification: []
---

# Phase 7: Validity frame checks (`DSX-VAL-*`) Verification Report

**Phase Goal:** The paradigm-independent content of the `validity_frame:` block is adjudicated —
a missing/unfalsifiable estimand, a unit triad guaranteeing pseudo-replication, dependence with no
method family, weak identification dressed as strong, a sampling frame that cannot carry the claim
population, a missingness mechanism the implied method cannot survive, and a measurement construct
with no operationalisation each block before the data is touched.
**Verified:** 2026-08-20
**Status:** passed
**Re-verification:** Yes — supersedes 07-VERIFICATION.md dated 2026-08-12T17:53:31Z (`human_needed`)

## What Changed Since the Prior Verdict

The prior verification (2026-08-12) found all mechanical checks passing but withheld a `passed`
verdict on two genuinely borderline human-judgment items, and reported REQ-P7-02 provisionally
because a citation self-contradiction (G-07-4) was still open. Since then:

1. **G-07-4 closed** (plan 07-08, 2026-08-14). Read `dsx/frame/val.py:78-85` and `:671-677`,
   `dsx/mathx.py:461-468`, and `brief.md` section 7 directly — all four Kish (1965) sites now
   state "section 8.2 was confirmed for the design-effect definition; no section number was
   confirmed for the design-effect formula itself" consistently. Independently re-ran
   `TestKishCitationCoherence`: 3/3 pass.
2. **UAT completed** (`07-UAT.md` frontmatter: `status: complete`, 38/38 passed, 0 issues, 0 open
   gaps). Both prior `human_needed` items are recorded as human-adjudicated `pass` verdicts in the
   UAT log, not silently dropped:
   - UAT test 6 (coverage_id D4, source_plan 07-07) is the human's verdict on the Chan & Perry
     (2017) admissibility question, with an explicit qualification recorded ("primary OR
     peer-reviewed" reading, disclosed as a Google Research technical report rather than a vendor
     blog).
   - UAT tests 2 and 5 are the human's verdicts on the two D-05 honesty disclosures (estimand
     decomposition; `CONSTRAINT_SOURCES` partition), both `pass`.

   I read `07-UAT.md` in full rather than trusting its `Summary` block, and confirmed each of
   these three entries individually names the exact file/lines the prior verification flagged and
   records a `pass`, not a placeholder or an auto-classification standing in for a human read.
3. Independently re-ran the full suite (`python -m unittest discover -s tests`) — **543 tests, OK**
   (up from 419 at the prior verification; the increase is Phases 8 and 9, executed since) — and
   re-ran the specific `TestValCitationObligations`, `TestValFixtureMatrix`,
   `TestFrameParadigmReadBoundary`, `TestValGateIntegration`, `TestValExpUnitsDisjointness`, and
   `TestValGateSeverity` classes directly: all pass.
4. `07-SECURITY.md` now exists (`status: verified`, `threats_open: 0`) — closes the milestone
   audit's `GAP-PROC-01` finding that Phase 7 had no security pass.

**Conclusion: both previously open human-judgment items are genuinely closed by a human, not
assumed closed.** No regressions found. Status moves from `human_needed` to `passed`.

## Success Criteria (ROADMAP.md, Phase 7 section)

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | `weak-identification-mmm` exits 1 at `dsx gate plan` naming `DSX-VAL-040`; a strong-identification spec with a parameter-scale constraint surfaces `DSX-VAL-041` at HIGH — printed but non-blocking at plan, blocking at verify/ship — both citing Gelman, Simpson & Betancourt (2017) | VERIFIED | Reran directly: `dsx gate plan --spec examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml` → exit 1, `[CRITICAL] DSX-VAL-040` printed. `dsx gate execute` on the same fixture → exit 0. `TestValGateSeverity` (5/5) and `TestValGateIntegration` (3/3) reran, all pass. |
| 2 | A finer-`observation`-than-`assignment` spec with no method family exits 1 under `DSX-VAL-020`, quantified via `DEFF = 1 + (m-1)·ICC`, with a test asserting the published worked value | VERIFIED | `dsx.mathx.design_effect(29.8, 0.02) == 1.576` — Cochrane worked example, docstring citation now internally consistent (G-07-4 closed). `TestValUnits` reran as part of the full suite pass. |
| 3 | `DSX-VAL-020` and `DSX-EXP-021` never both fire on the same defect; `dsx gate` on existing `DSX-EXP-020/021` fixtures is unchanged | VERIFIED | `TestValExpUnitsDisjointness` (6/6) reran directly, including `test_design_checks_py_content_is_unmodified_since_phase_start` — `dsx/checks/design.py` still pinned to its phase-start sha256. |
| 4 | Estimand incompleteness/non-falsifiability, dependence-without-method-family, sampling frame vs claim population, missingness vs implied method, measurement/operationalisation each block their own bad fixture and pass the extended good fixture, each with a citation + reference value or structural criterion + linked test | VERIFIED | `TestValFixtureMatrix` (5/5) reran directly — good fixture's `DSX-VAL-*` code set pinned to empty, every corpus fixture pinned to a measured set. `TestValCitationObligations` (3/3) reran — AST-derived, confirms all ten codes carry `Citation:` + `Reference value:`/`Structural criterion:` lines and a `# D-05: <CODE>` test marker. |
| 5 | A test asserts no `dsx/frame/val.py` code path reads `inference.paradigm` (D-11), failing the suite if one is introduced | VERIFIED, with a disclosed, non-blocking detector blind spot | `TestFrameParadigmReadBoundary` (7/7, includes the Phase 8 interference-module extension) reran directly. `grep -oE "DSX-VAL-[0-9]{3}" dsx/frame/val.py` and a full read confirm no `inference.paradigm` read exists today. The chained `.get().get()` detector blind spot flagged at the prior verification is still open (confirmed unchanged by direct read of the detector functions) — carried forward as tech debt (see "Findings Carried Forward" below), not exploited in the current tree, and does not change this criterion's truth value today. |

**Score:** 5/5 roadmap success criteria verified.

### Requirements Coverage (REQUIREMENTS.md:96-104)

| Requirement | Description | Status | Evidence |
|---|---|---|---|
| REQ-P7-01 | Estimand missing any of `quantity`/`population`/`contrast`/`time_window`/`falsifier` blocked; a non-discriminating falsifier blocked | MET | `_check_estimand_completeness` (`DSX-VAL-010`), `_check_estimand_falsifiability` (`DSX-VAL-011`). Confirmed present in `dsx/frame/val.py`; covering tests pass in the full suite. |
| REQ-P7-02 | Analysis unit finer than assignment unit blocked, DEFF quantified via `1 + (m-1)·ICC`, published worked value tested | MET | `_check_unit_triad` (`DSX-VAL-020`); worked value 1.576 confirmed by direct call. Citation self-consistency (G-07-4) confirmed closed this session (`TestKishCitationCoherence` 3/3, direct read of all four Kish sites). |
| REQ-P7-03 | `DSX-VAL-020`/`DSX-EXP-021` disjoint; EXP-021 unchanged; VAL-020 covers only `observation` vs `assignment` | MET | See SC3 above. |
| REQ-P7-04 | Declared dependence structure with no matching method family blocked, using `VARIANCE_ADJUSTMENTS` | MET | `_check_dependence` (`DSX-VAL-030`) confirmed present; `DEPENDENCE_ADMISSIBLE_METHODS` confirmed a `VARIANCE_ADJUSTMENTS` subset map by direct read. |
| REQ-P7-05 | `DSX-VAL-040` blocks weak+`constraint_source: none`; `DSX-VAL-041` flags strong+parameter-scale constraint; both cite Gelman, Simpson & Betancourt (2017) | MET | See SC1 above, plus the committed `weak-identification-mmm` fixture. Chan & Perry (2017) citation-admissibility judgment (UAT test 6) closed by human `pass` verdict. |
| REQ-P7-06 | Sampling frame that cannot represent claim population blocked, with exclusions and selection risk declared | MET | `_check_sampling_frame` (`DSX-VAL-050`) confirmed present; presence/consistency check per D-06 (disclosed, not a text comparison). |
| REQ-P7-07 | Missingness mechanism inconsistent with implied method blocked, against the Rubin MCAR/MAR/MNAR framing | MET | `_check_missingness` (`DSX-VAL-060`) confirmed present; `missingness.rate` proven never read (dedicated test in the full suite). |
| REQ-P7-08 | Measurement construct with no operationalisation, **or** whose known gaps contradict the claim population, blocked | **PARTIAL, by design — not a gap** | First clause MET: `_check_measurement` (`DSX-VAL-070`) confirmed present, blocks a blank operationalisation. Second clause confirmed still unadjudicated by direct read (`grep -n "known_gaps" dsx/frame/val.py dsx/spec.py` → no matches) — this is decision D-06 (07-CONTEXT.md:143-158), a recorded, human-made scope deferral, and the roadmap's own SC4 wording does not require the second clause. Reported PARTIAL, not silently folded into MET, consistent with the prior verification's own instruction. |
| REQ-P7-09 | No `DSX-VAL-*` check reads `inference.paradigm`, asserted by test | MET (see SC5 caveat) | `TestFrameParadigmReadBoundary` reran, 7/7 pass. |

**No orphaned requirements.** All nine `REQ-P7-*` IDs appear in exactly one plan's `requirements:`
frontmatter (checked directly: 07-01 → 01/02/04; 07-02 → 02/05; 07-03 → 01/09; 07-04 → 02/03;
07-05 → 04/05; 07-06 → 06/07/08; 07-07 → 05; 07-08 → 02) and REQUIREMENTS.md lists exactly these
nine for Phase 7, no more, no fewer.

## The Ten Finding Codes — reconfirmed present

`grep -oE "DSX-VAL-[0-9]{3}" dsx/frame/val.py | sort -u` (rerun this session):
`DSX-VAL-010, 011, 020, 021, 030, 040, 041, 050, 060, 070` — all ten present, matching
`references/finding-codes.md`.

## Behavioral Spot-Checks (rerun independently this session)

| Behavior | Command | Result | Status |
|---|---|---|---|
| Full suite | `python -m unittest discover -s tests` | 543 tests, OK (2 skipped) | PASS |
| Kish citation coherence | `python -m unittest tests.test_frame_val.TestKishCitationCoherence -v` | 3/3 OK | PASS |
| Citation obligations + fixture matrix + D-11 boundary + gate integration/severity + EXP/VAL disjointness | `python -m unittest tests.test_frame_val.TestValCitationObligations tests.test_frame_val.TestValFixtureMatrix tests.test_frame_boundary.TestFrameParadigmReadBoundary tests.test_frame_val.TestValGateIntegration tests.test_frame_val.TestValExpUnitsDisjointness tests.test_frame_val.TestValGateSeverity -v` | 34/34 OK | PASS |
| weak-identification-mmm blocks plan, clears execute | `dsx gate plan` / `dsx gate execute --spec .../weak-identification-mmm-ANALYSIS-SPEC.yaml` | exit 1 (`DSX-VAL-040` CRITICAL) / exit 0 | PASS |
| Finding catalogue currency | `python scripts/gen-finding-catalogue.py --check` | exit 0 (warns on pre-existing `DSX-VAL-021`/`DSX-VAL-060` two-severity rendering, non-fatal) | PASS |

## Findings Carried Forward (not phase blockers, not new)

1. **D-11 boundary detector blind spot** (chained `.get("inference", {}).get("paradigm")` form is
   not caught by either detector). Disclosed at the prior verification, independently confirmed
   unexploited in the current tree by both this session's read and the 2026-08-14 milestone audit.
   Non-blocking; worth a follow-up hardening ticket.
2. **`DSX-VAL-021`/`DSX-VAL-060` catalogue rendering shows one severity/title per code** (generator
   limitation — `scripts/gen-finding-catalogue.py`'s dedup keeps the last-seen call site and only
   warns, does not fail). Confirmed present this session (`--check` still prints both warnings).
   Cosmetic; `--check` exits 0; both severities emit correctly at runtime. Pre-existing pattern
   shared with `DSX-COH-030`/`DSX-SPEC-070`, and now separately documented as WR-02 in the phase's
   own 2026-08-20 code review.
3. **`dsx/frame/val.py::check()` hand-duplicates each `_check_*` function's blocking predicate to
   build `DecisionRecord.choice` strings** (WR-01 in `07-REVIEW.md`, dated 2026-08-20). All ~9
   duplicated predicates agree with their source function today (verified by the reviewer's trace,
   independently spot-checked here for the identification pair), but this is a genuine future-drift
   risk in Phase 07's own file. Non-blocking for this verification (nothing currently disagrees),
   flagged as a WARNING worth a follow-up ticket to consolidate the two code paths.
4. **REQ-P7-08's second clause is deliberately unadjudicated** (D-06) — see requirements table
   above. Documented scope decision, not a defect.

**Deliberately out of scope for this verification:** `07-REVIEW.md`'s CR-01 (the `DSX-PAR-001`
manifest and `DSX-PAR-002` in `dsx/frame/paradigm.py` disagreeing on an out-of-vocabulary
`inference.paradigm` value) is a real, reproduced defect, but it lives entirely in code that
predates or postdates Phase 7: `dsx/frame/paradigm.py`'s `check()` selection logic and
`_check_paradigm_justification` were both created in Phase 6 (`a746c9f`, "feat(06-07)"), and the
`DSX-PAR-010`/`011` monitoring pair that exposes the contradiction was added in Phase 9
(`df20ef6`, "feat(09-03)"). Phase 7's only touch to `dsx/frame/paradigm.py`, confirmed by
`git show --stat 3633222`, was a one-line removal of the `DSX-VAL-` entry from `_NOT_SHIPPED` —
build plumbing, not the manifest logic CR-01 describes. This defect belongs to Phase 6/9's
verification scope, not Phase 7's.

## Anti-Pattern Scan (rerun this session)

`grep -n -E "TODO|FIXME|XXX|TBD|HACK|PLACEHOLDER|not yet implemented|coming soon"` across
`dsx/frame/val.py`, `dsx/mathx.py`, `tests/test_frame_val.py`,
`examples/known-bad/weak-identification-mmm-POSTMORTEM.md`,
`examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml`, `brief.md`: only hit is
`tests/test_frame_val.py:44`'s `_TEMPLATE_PLACEHOLDER_FALSIFIER` test constant name, exercising
the placeholder-detection logic itself, not a stub. No debt markers. No blockers.

## Human Verification Required

None. Both items open at the prior verification are closed by recorded human `pass` verdicts in
`07-UAT.md` (tests 2, 5, and 6) — see "What Changed Since the Prior Verdict" above.

## Gaps Summary

No gaps. The phase goal — the paradigm-independent content of the `validity_frame:` block is
adjudicated before the data is touched — is achieved in the codebase and confirmed by independent
re-execution of every load-bearing test and CLI command, not by SUMMARY.md or UAT narrative alone.
The one PARTIAL requirement (REQ-P7-08's second clause) is a disclosed, human-made scope decision
(D-06) that the roadmap's own success criteria do not require, not an unresolved defect.

---

*Verified: 2026-08-20*
*Verifier: Claude (gsd-verifier)*
