---
phase: 07-validity-frame-checks-dsx-val
verified: 2026-08-12T17:53:31Z
status: human_needed
score: 8/9 requirements MET, 1/9 PARTIAL (documented deferral, not a gap)
behavior_unverified: 0
overrides_applied: 0
re_verification: false
human_verification:
  - test: "Judge whether Chan, D. & Perry, M. (2017), 'Challenges and Opportunities in Media Mix Modeling' (Google Inc. technical report) clears D-05's vendor-blog/marketing exclusion for the weak-identification-mmm post-mortem's citation."
    expected: "A human sign-off that an industry (non-peer-reviewed) technical report from a company with a commercial interest in advertising is or is not admissible under the project's citation-admissibility rule."
    why_human: "This is an explicit judgment call the project's own rules assign to a human (07-CONTEXT.md 'Vendor blogs and Medium posts are inadmissible in either direction' + the verification brief's own instruction to 'assess honestly ... this is a borderline call the human should see'). I traced every quoted passage and page/section number against the primary PDF (fetched live) and found them all verbatim-accurate — the citation is not fabricated or laundered — but whether a Google Research technical report meets the admissibility bar is not something a grep or test can settle."
  - test: "Confirm the two D-05 honesty disclosures (five-field estimand decomposition; CONSTRAINT_SOURCES partition) read as adequate, honest prose, not just structurally present."
    expected: "A human reads dsx/frame/val.py's _check_estimand_completeness and _check_identification docstrings and agrees the 'project-defined, not a published result' framing is not misleading."
    why_human: "TestValCitationObligations mechanically proves a Citation: line and a Reference value:/Structural criterion: line exist on every finding-emitting function — it cannot judge whether the prose is honest. Quoted verbatim below for a direct read."
---

# Phase 7: Validity frame checks (`DSX-VAL-*`) Verification Report

**Phase Goal:** The paradigm-independent content of the `validity_frame:` block is adjudicated — a
missing/unfalsifiable estimand, a unit triad guaranteeing pseudo-replication, dependence with no
method family, weak identification dressed as strong, an unrepresentative sampling frame, an
unsurvivable missingness mechanism, and an unoperationalised measurement construct each block
before the data is touched.
**Verified:** 2026-08-12T17:53:31Z
**Status:** human_needed (all mechanical checks pass; one genuinely borderline citation-admissibility
judgment and one honesty-disclosure prose read are handed to a human, exactly as the plan itself
flagged them — not because anything failed)
**Re-verification:** No — initial verification

## Summary

All ten `DSX-VAL-*` codes exist, fire correctly on constructed and real fixtures, and are reachable
from the plan/verify/ship gate profiles (not execute). I independently reran every measured command
in the brief — 419 tests OK, catalogue check exit 0, all four gate-exit-code claims, and the
`dsx/checks/design.py` diff-since-baseline is empty — and additionally fetched and text-extracted the
primary PDF the new fixture's post-mortem cites, confirming every quoted passage and section/page
number verbatim. `dsx/frame/val.py`'s two honesty disclosures (project-defined estimand decomposition;
project-defined `CONSTRAINT_SOURCES` partition) are present and read as intended. One requirement
(REQ-P7-08's second clause) is honestly and deliberately unadjudicated by design (D-06) — reported
PARTIAL, not silently folded into MET. The corpus test's narrowing (`_EXPECTED_PLAN_BLOCKERS`) is a
genuine strengthening, not a weakening: it converts a lost blanket assertion into a stronger
per-fixture requirement and still fails loudly on an undocumented fixture. The one open item is a
citation-admissibility judgment call the project's own rules assign to a human.

## Success Criteria (ROADMAP.md:210-234)

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | `weak-identification-mmm` exits 1 at `dsx gate plan` naming `DSX-VAL-040`; a strong-identification spec with a parameter-scale constraint surfaces `DSX-VAL-041` at HIGH — printed but non-blocking at plan, blocking at verify/ship — both citing Gelman, Simpson & Betancourt (2017) | MET | `dsx gate plan --spec examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml` → exit 1, `[CRITICAL] DSX-VAL-040` (reproduced). `tests.test_frame_val.TestValGateSeverity` (5/5 pass, reran) exercises the real `cli.main()`: weak/none blocks plan naming VAL-040; strong/informative_priors exits 0 at plan while VAL-041 is on stdout; the same spec blocks verify and ship naming VAL-041 on stderr. `_IDENTIFICATION_CITATION` in `dsx/frame/val.py:103-113` cites Gelman, Simpson & Betancourt (2017) for both codes. |
| 2 | A finer-`observation`-than-`assignment` spec with no method family exits 1 under `DSX-VAL-020`, quantified via `DEFF = 1 + (m-1)·ICC`, with a test asserting the published worked value | MET | `dsx.mathx.design_effect(29.8, 0.02) == 1.576` (reran directly). `tests/test_dsx.py::test_design_effect_matches_cochrane_worked_example` asserts it. `TestValUnits` (15/15 pass, reran) includes `test_units_020_detail_carries_the_deff_formula_and_illustration_wording`. |
| 3 | `DSX-VAL-020` and `DSX-EXP-021` never both fire on the same defect; `dsx gate` on existing v1.5.0 `DSX-EXP-020/021` fixtures is unchanged | MET | `dsx gate plan --spec examples/bad-ANALYSIS-SPEC.yaml` (reran) names `DSX-EXP-021`, not `DSX-VAL-020`. `TestValExpUnitsDisjointness` (6/6 pass, reran) proves this by construction (editing one block never changes the other check's fired set) plus a whole-repo scan, plus a pinned sha256 of `dsx/checks/design.py`. `git diff 36e3873..HEAD -- dsx/checks/design.py` (reran) is empty — the file is byte-identical to the phase-start baseline. |
| 4 | Estimand incompleteness/non-falsifiability, dependence-without-method-family, sampling frame vs claim population, missingness vs implied method, measurement/operationalisation each block their own bad fixture and pass the extended good fixture, each with a citation + reference value or structural criterion + linked test | MET | `TestValEstimand`, `TestValDependenceIdentification`, `TestValSamplingMissingnessMeasurement`, `TestValUnits` (68/68 pass, reran together). `TestValFixtureMatrix` (5/5, reran) pins the good fixture's `DSX-VAL-*` code set to the empty set and every corpus fixture to a measured, dated set. `TestValCitationObligations` (3/3, reran) AST-derives every `report.add()` call site and asserts a `Citation:` + `Reference value:`/`Structural criterion:` docstring line and a `# D-05: <CODE>` test marker for each — all ten codes present (grep confirms markers for `010`/`011`/`020`/`021`/`030`/`040`/`041`/`050`/`060`/`070`). |
| 5 | A test asserts no `dsx/frame/val.py` code path reads `inference.paradigm` (D-11), failing the suite if one is introduced | MET, with a documented detector blind spot (WARNING, not blocking) | `tests.test_frame_boundary.TestFrameParadigmReadBoundary` (7/7 pass, reran) — text detector + AST detector, both proven to fire against synthetic violations and to permit a legitimate field read; the real module scans clean. `grep -n "paradigm" dsx/frame/val.py` and a full read of the file (below) confirm no such read exists today. **Caveat, disclosed honestly by the executor in 07-03-SUMMARY.md and not hidden**: during development, the deliberate-violation drill found the chained-call form `spec.get("inference", {}).get("paradigm")` is NOT caught by either detector — only the idiomatic `get(spec, "inference.paradigm")` form is. `val.py` uses neither form today (confirmed by full read), so the current codebase is clean, but the test's coverage has a known gap that would let a future chained-`.get()` regression through silently. This is a real, if narrow, hole in the SC5 guarantee's future-proofing — flagged as a WARNING for a follow-up, not a BLOCKER against this phase's present state. |

## Requirements Coverage (REQUIREMENTS.md:96-104)

| Requirement | Description | Status | Evidence |
|---|---|---|---|
| REQ-P7-01 | Estimand missing any of `quantity`/`population`/`contrast`/`time_window`/`falsifier` blocked; a non-discriminating falsifier blocked | MET | `_check_estimand_completeness` (`DSX-VAL-010`, CRITICAL), `_check_estimand_falsifiability` (`DSX-VAL-011`, HIGH). `TestValEstimand` reran, all pass. |
| REQ-P7-02 | Analysis unit finer than assignment unit blocked, DEFF quantified via `1 + (m-1)·ICC`, published worked value tested | MET | `_check_unit_triad` (`DSX-VAL-020`). Worked value 1.576 confirmed by direct call and by test. |
| REQ-P7-03 | `DSX-VAL-020`/`DSX-EXP-021` disjoint; EXP-021 unchanged; VAL-020 covers only `observation` vs `assignment` | MET | See SC3 above. |
| REQ-P7-04 | Declared dependence structure with no matching method family blocked, using `VARIANCE_ADJUSTMENTS` | MET | `_check_dependence` (`DSX-VAL-030`) tests `dsx.spec.DEPENDENCE_ADMISSIBLE_METHODS`, a five-key map of `VARIANCE_ADJUSTMENTS` subsets (confirmed by direct read: `delta_method` in no entry). |
| REQ-P7-05 | `DSX-VAL-040` blocks weak+`constraint_source: none`; `DSX-VAL-041` flags strong+parameter-scale constraint; both cite Gelman, Simpson & Betancourt (2017) | MET | See SC1 above, plus the committed `weak-identification-mmm` fixture proving REQ-P7-05 end to end against a real, not synthetic, spec. |
| REQ-P7-06 | Sampling frame that cannot represent claim population blocked, with exclusions and selection risk declared | MET | `_check_sampling_frame` (`DSX-VAL-050`, HIGH) — presence/consistency only, deliberately not a text comparison against claim population (D-06, disclosed). |
| REQ-P7-07 | Missingness mechanism inconsistent with implied method blocked, against the Rubin MCAR/MAR/MNAR framing | MET, with honest naming caveat already handled | `_check_missingness` (`DSX-VAL-060`) implements a project-assembled (not printed) mechanism×method table per D-07; the docstring explicitly disclaims it as "the Rubin validity table," matching REQUIREMENTS.md's own footnote that the phrase names a concept, not a citable artifact. `missingness.rate` is proven never read (dedicated test). |
| REQ-P7-08 | Measurement construct with no operationalisation, **or** whose known gaps contradict the claim population, blocked | **PARTIAL** | First clause MET: `_check_measurement` (`DSX-VAL-070`, HIGH) blocks a construct with a blank operationalisation. **Second clause is deliberately unadjudicated** — confirmed by full read of `dsx/frame/val.py`: `known_gaps` is never referenced anywhere in the module (`grep -n "known_gaps" dsx/frame/val.py dsx/spec.py` → no matches), and the comment directly above `_check_measurement` states this in full: *"Unadjudicated (D-06, REQ-P7-08's second clause): a measurement whose known gaps contradict the claim population is not adjudicated by this check, or by any check in this phase. This is decision D-06's text-comparison deferral rather than an oversight, and the known-gaps field is therefore read by no check in this phase."* This is an honest, load-bearing, human-recorded scope decision (D-06, 07-CONTEXT.md:143-158) — the roadmap's own SC4 wording only requires the first clause — not a hidden gap. Reported PARTIAL per this verification's own instruction rather than silently counted MET. |
| REQ-P7-09 | No `DSX-VAL-*` check reads `inference.paradigm`, asserted by test | MET (see SC5 caveat above) | |

## The Ten Finding Codes

| Code | Exists | Reachable from a profile | `Citation:` line | `Reference value:`/`Structural criterion:` line | `# D-05: <CODE>` test marker |
|---|---|---|---|---|---|
| `DSX-VAL-010` | yes | yes (`val` in plan/verify/ship) | yes | Structural criterion | `tests/test_frame_val.py:66` |
| `DSX-VAL-011` | yes | yes | yes | Structural criterion | `tests/test_frame_val.py:92` |
| `DSX-VAL-020` | yes | yes | yes | Reference value (1.576) | `tests/test_frame_val.py:171`, `tests/test_dsx.py:131` |
| `DSX-VAL-021` | yes | yes | yes | Structural criterion | `tests/test_frame_val.py:243` |
| `DSX-VAL-030` | yes | yes | yes | Structural criterion | `tests/test_frame_val.py:311` |
| `DSX-VAL-040` | yes | yes | yes | Structural criterion | `tests/test_frame_val.py:421` |
| `DSX-VAL-041` | yes | yes | yes | Structural criterion | `tests/test_frame_val.py:450` |
| `DSX-VAL-050` | yes | yes | yes | Structural criterion | `tests/test_frame_val.py:630` |
| `DSX-VAL-060` | yes | yes | yes | Structural criterion | `tests/test_frame_val.py:758` |
| `DSX-VAL-070` | yes | yes | yes | Structural criterion | `tests/test_frame_val.py:711` |

All ten mechanically confirmed via `TestValCitationObligations` (AST-derived — never a hand-written
list) and directly via `grep -rn "# D-05: DSX-VAL-0" tests/`, both rerun. All ten appear in
`references/finding-codes.md:361-370`.

**One catalogue imprecision, not a Phase 7 regression:** `DSX-VAL-060` has two `report.add()` call
sites (HIGH and CRITICAL branches, split deliberately so `gen-finding-catalogue.py`'s literal-string
AST extractor can see the severity — see 07-06-SUMMARY.md's Rule-1 fix). The rendered catalogue shows
only one severity (CRITICAL) for the code; this is the same pre-existing "declared twice with
different text" pattern already carried by `DSX-COH-030` and `DSX-SPEC-070` (both predate Phase 7,
confirmed by warning text appearing in every plan's baseline `--check` run since 07-01). Cosmetic only
— `--check` still exits 0 and both severities are correctly emitted at runtime (confirmed:
`_MISSINGNESS_METHOD_VALIDITY`'s two branches call `report.add("DSX-VAL-060", "HIGH", ...)` and
`report.add("DSX-VAL-060", "CRITICAL", ...)` as separate literal call sites).

## Honesty Disclosures — the highest-value check in this phase

### 1. Five-field estimand decomposition — disclosed as project-defined

Quoted verbatim from `dsx/frame/val.py::_check_estimand_completeness` (lines 570-578):

> "Honesty disclosure (D-05's whole point): the five-field estimand decomposition this module uses
> (quantity, population, contrast, time_window, falsifier) is project-defined. The addendum and Hernan
> and Robins (2016) each name four of the five attributes checked here, but neither treats
> `falsifier` as an estimand attribute at all, and `time_window` appears in the addendum as a
> sub-specification of the estimand rather than as one of its named attributes. No cited source
> states this five-field decomposition as written; it is this project's own grouping, adopted for
> decidability, not asserted as a published result."

**Verdict: present and adequate.** This is exactly the disclosure the phase promised — it does not
merely footnote the gap, it names precisely which two of the five fields (`falsifier`, `time_window`)
have no source backing and why. Routed to human verification only for a final prose-adequacy read,
not because anything is missing.

### 2. `CONSTRAINT_SOURCES` partition for `DSX-VAL-041` — disclosed as project-defined

Quoted verbatim from `dsx/frame/val.py::_check_identification` (lines 917-924):

> "Honesty disclosure (D-05's whole point): no published source partitions CONSTRAINT_SOURCES into
> members that carry parameter-scale information and members that do not. Gelman, Simpson &
> Betancourt support the underlying premise, and their section 1.2 gives a prior taxonomy that lines
> up with two of the four members classified here (structural priors -> hierarchical_pooling;
> regularizing priors -> penalisation), but they publish no such partition, and design_restriction has
> no counterpart in their paper at all. This partition is project-defined."

**Verdict: present and adequate**, repeated a second time in the module-constant comment
(`dsx/frame/val.py:132-140`) so it survives being read in isolation from the docstring — exactly the
"survives being read in isolation" design goal 07-CONTEXT.md set for this disclosure.

## Unverified Locators — flagged, not invented

**Kish (1965) section number for the DEFF formula.** `dsx/frame/val.py:78-85`
(`_UNIT_TRIAD_CITATION`): *"The section number inside Kish for the design-effect formula itself is
UNVERIFIED — only the page numbers above were confirmed; do not invent one."* Confirmed present,
correctly hedged (page 258 stated as confirmed, no section number invented).

**Gelman, Simpson & Betancourt (2017) typeset-vs-arXiv section numbering.**
`dsx/frame/val.py:103-113` (`_IDENTIFICATION_CITATION`): *"Whether the typeset MDPI journal version
uses the same section numbers as the arXiv final version is UNVERIFIED — cited by section number and
title together so the locator survives either."* Confirmed present, and the citation is indeed given
by both number (3.3, 1.2) and title, matching its own stated mitigation.

A third instance exists beyond the two named in the brief: `_DEPENDENCE_CITATION`
(`dsx/frame/val.py:92-101`) flags the Cameron & Miller (2015) section locator and the Gelman & Hill
(2007) chapter locator as both UNVERIFIED, in the same honest form.

## Adversarial Check: the weak-identification-mmm fixture's citation

`examples/known-bad/weak-identification-mmm-POSTMORTEM.md` cites Chan, D. & Perry, M. (2017),
"Challenges and Opportunities in Media Mix Modeling," Google Inc.

**Fabrication/laundering check — PASSED.** I fetched the primary PDF live
(`storage.googleapis.com/gweb-research2023-media/pubtools/3803.pdf`, HTTP 200, 807,776 bytes) and
extracted its text with `pdftotext`. Every element checked against the primary document:

- Title page: "Challenges And Opportunities In Media Mix Modeling", authors "David Chan and Michael
  Perry", affiliation "Google Inc." — matches the citation exactly.
- Section 4.1.1 quote ("A typical MMM dataset, consisting of three years of national weekly data is
  only 156 data points") — found **verbatim**, on the page immediately preceding the printed footer
  "6" — matches the post-mortem's claimed page 6.
- Section 4.1.2 ("Correlated input variables") — found on the same physical page (6), content
  ("bad attribution of sales to the ad channel," two response surfaces with different slopes fitting
  correlated data equally well) matches the post-mortem's paraphrase.
- Section 4.2 ("Selection bias") — "Selection bias from MMMs perhaps represents the largest hurdle to
  MMMs providing valid estimates of advertising effectiveness" found verbatim, on the page matching
  the post-mortem's claimed pages 8-9.
- Section 4.3.2 ("Model uncertainty") — "Each model achieves an R2 value of either 0.98 or 0.99" and
  "differ in their sales predictions by up to 50%" both found verbatim, on the page matching the
  post-mortem's claimed pages 10-11.

No quote was paraphrased-then-presented-as-verbatim, no section/page number was invented, and no
number was misattributed. This citation is genuinely, independently verified — not merely asserted.

**Admissibility judgment — BORDERLINE, routed to human, my own read leans admissible.** The project's
own rule (07-CONTEXT.md) is: *"Vendor blogs and Medium posts are inadmissible in either direction."*
Chan & Perry (2017) is not literally a vendor blog, Medium post, or tool-marketing page — it is a
Google Research technical report with an abstract, numbered sections, and (per the extracted text) a
references list, hosted under Google's research publication imprint rather than its marketing or
product-documentation properties. Two points that push toward admissible: (1) the paper's actual
content argues *against* over-trusting MMM point estimates (the opposite incentive a marketing piece
would have), and (2) it is a widely-cited reference in the applied marketing-analytics/econometrics
literature, not a novel or fringe source. One point of genuine caution the human should weigh: Google
sells advertising and has since shipped MMM tooling (e.g., Meridian), so a Google-authored critique of
MMM reliability is not fully disinterested even though this specific paper predates that tooling and
argues for more caution, not a particular product. **This is exactly the kind of call the phase's own
plan (07-07-SUMMARY.md "Human Judgment Items") assigned to a human rather than a test — I am
surfacing it plainly, not rubber-stamping it, and not blocking on it because the letter of the named
exclusion list (vendor blogs / Medium / tool marketing) is not met.**

## Silent-Weakening Check: `tests/test_known_bad_corpus.py`

**Narrowing confirmed to be a genuine strengthening, not a weakening.** Read the full file
(394 lines). `_EXPECTED_PLAN_BLOCKERS = {"weak-identification-mmm-ANALYSIS-SPEC.yaml": "DSX-VAL-040"}`
is the sole named exception. `test_every_spec_passes_the_critical_threshold_gate_points`:

- For any fixture **not** in `_EXPECTED_PLAN_BLOCKERS`: unchanged blanket assertion — `exit == 0` at
  both `plan` and `execute`.
- For the **listed** fixture at `plan`: **must** exit 1 **and** its mapped code (`DSX-VAL-040`) must be
  among the CRITICAL findings — a strictly stronger, positive requirement than the assertion it
  replaces for this one fixture, not merely a relaxed one.
- For the listed fixture at `execute`: the original blanket `exit == 0` assertion still applies
  unchanged (the `val` check is not in the execute gate profile).
- **A fixture with no recorded expectation is not silently exempted.** If a future fixture blocks
  `plan` without an entry in `_EXPECTED_PLAN_BLOCKERS`, `expected_blocker` is `None`, the `else`
  branch runs, and `self.assertEqual(code, 0, ...)` fails loudly with the blocking codes printed in
  the failure message — exactly the "fail the suite loudly rather than pass unexamined" behavior
  required. Confirmed by direct code read (`tests/test_known_bad_corpus.py:219-251`), and
  independently reran (`python3 -m unittest tests.test_known_bad_corpus -v` → 13/13 OK).
- `test_incidental_allowlist_names_no_target_family_code` additionally proves no allow-listed
  incidental code can share a prefix with a target-family code (`_TARGET_CODE_FAMILIES` now includes
  the exact string `"DSX-VAL-040"`, not the bare `"DSX-VAL-"` prefix — confirmed by read, this is
  deliberate: it keeps the pre-existing `DSX-VAL-041` incidental-gap entry on the bayesian fixture
  legal while still forbidding `DSX-VAL-040` from ever being allow-listed as incidental).

## Reproduced Measurements (all rerun independently, not taken on trust)

| Command | Claimed | Reproduced |
|---|---|---|
| `python3 -m unittest discover -s tests` | 419 tests OK (2 skipped) | Reran: **419 tests OK (2 skipped)** — matches |
| `python3 scripts/gen-finding-catalogue.py --check` | exit 0 | Reran: **exit 0** — matches |
| `gate plan --spec examples/good-ANALYSIS-SPEC.yaml`; `gate ship` same | 0; 0 | Reran: **0; 0** — matches |
| `gate plan --spec examples/bad-ANALYSIS-SPEC.yaml` | 1 | Reran: **1**, names `DSX-EXP-021` (not `DSX-VAL-020`) plus a new, additive `DSX-VAL-011` finding |
| `gate plan --spec templates/ANALYSIS-SPEC.yaml` | 0 | Reran: **0** — matches |
| `gate plan --spec .../weak-identification-mmm-ANALYSIS-SPEC.yaml` | 1, naming `DSX-VAL-040` | Reran: **1**, `[CRITICAL] DSX-VAL-040` — matches |
| `gate execute` same fixture | 0 | Reran: **0** — matches |
| `git diff 36e3873..HEAD -- dsx/checks/design.py` | empty | Reran: **0 lines** — matches |
| `python3 scripts/check_brief_refs.py` | (not in original list; ran anyway) | **All checks passed, exit 0** |

## Anti-Pattern Scan

`grep -n -E "TODO|FIXME|XXX|TBD|HACK|PLACEHOLDER|not yet implemented|coming soon"` across
`dsx/frame/val.py`, `tests/test_frame_val.py`, the new fixture and its post-mortem: no debt markers.
The one `PLACEHOLDER` hit in `tests/test_frame_val.py:44` is a test constant name
(`_TEMPLATE_PLACEHOLDER_FALSIFIER`) exercising the placeholder-detection logic itself, not a stub.
No blockers found.

## Findings Nobody Flagged

1. **The D-11 boundary test has a known, disclosed blind spot** (chained `.get().get()` form) — see
   SC5 above. Not exploited today (confirmed by full read of `val.py`), but worth a follow-up ticket
   so a future contributor doesn't reintroduce a paradigm read through the one door the detector
   doesn't watch.
2. **`DSX-VAL-060`'s two-severity catalogue rendering is cosmetically incomplete** (shows CRITICAL
   only) — pre-existing pattern shared with two other legacy codes, not a Phase 7 regression, and
   `--check` still exits 0. Noted for completeness, not actionable.
3. **REQ-P7-08's second clause is genuinely, honestly unadjudicated** — this is the one place this
   verification declines to call the requirement fully MET. It is a recorded, deliberate scope
   decision (D-06) rather than an oversight, and the roadmap's own Success Criterion 4 does not
   require the second clause — but REQUIREMENTS.md does, so the honest report is PARTIAL.

---

## GAPS FOUND

No BLOCKER-level gaps. Two items require a human decision before this phase can be called fully
closed:

1. **[WARNING — human decision requested]** Citation-admissibility judgment on Chan & Perry (2017) for
   the weak-identification-mmm post-mortem. My independent verification found the citation accurate,
   unfabricated, and internally consistent down to the page and section number — but whether a
   Google-authored industry technical report clears the project's vendor-source exclusion is a
   judgment call the project's own rules assign to a human, not a verifier. See "Adversarial Check"
   above for the full reasoning; my own reading leans admissible.
2. **[WARNING — human decision requested]** Prose-adequacy read of the two D-05 honesty disclosures
   (quoted verbatim above). Structurally present and, in my own reading, honest and specific — routed
   to human sign-off because "does this read as honest, not misleading" is exactly the kind of
   judgment this project's threat model (T-7-07) assigns to a human.
3. **[WARNING, not requiring a decision to proceed]** REQ-P7-08's second clause (measurement whose
   known gaps contradict the claim population) is deliberately unadjudicated by design (D-06). This is
   documented, intentional, and does not block the roadmap's own Success Criterion 4 — reported here
   as PARTIAL per this verification's own instruction, not as a defect to fix.
4. **[WARNING, minor, non-blocking]** The D-11 paradigm-read boundary test has a disclosed detection
   gap for the chained `.get().get()` access form. Not exploited in the current codebase; worth a
   follow-up hardening ticket.

Every mechanical, testable claim in the phase's SUMMARY.md files reproduced exactly as documented. The
phase goal — the paradigm-independent content of the validity frame is adjudicated before the data is
touched — is achieved in the codebase, not merely claimed. The two items above are exactly the sort of
borderline judgment calls this project's own working agreements ask to be surfaced to a human rather
than silently resolved by an agent, and neither reflects a defect in the shipped code.

---

*Verified: 2026-08-12T17:53:31Z*
*Verifier: Claude (gsd-verifier)*
