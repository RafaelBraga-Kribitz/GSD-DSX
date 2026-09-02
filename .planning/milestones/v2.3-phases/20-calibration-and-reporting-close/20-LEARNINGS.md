---
phase: 20
phase_name: "Calibration and reporting close"
project: "gsd-dsx"
generated: "2026-09-02"
counts:
  decisions: 9
  lessons: 7
  patterns: 7
  surprises: 6
missing_artifacts:
  - "UAT.md"
  - "RESEARCH.md"
---

# Phase 20 Learnings: Calibration and reporting close

## Decisions

### D-03 (LOAD-BEARING) — extend the single calibration harness with a live HIGH verify/ship stratum, do not re-run or duplicate it

All 15 codes minted in Phases 18–19 are severity HIGH, and the `stats` check registers only at verify/ship (`dsx/cli.py:120–130`), where the gate blocks at HIGH; plan/execute block only at CRITICAL. The existing calibration `tests/test_known_bad_corpus.py::test_stratified_catch_rate_and_fpr_report` (line 1557) is CRITICAL-only in both partitions by two independent structural barriers: the PRESENT loop iterates only `_CRITICAL_THRESHOLD_POINTS = ("plan","execute")` (line 1607), and `_classify_target_defect` compares expected codes against CRITICAL-severity findings only (299/313); the ABSENT-partition union is likewise CRITICAL-only (1638–1640). Re-running the harness as-is is therefore provably invariant to the 15 new codes.

**Decision:** parameterize `_classify_target_defect` with a trailing `severity` argument defaulting to `"CRITICAL"` (every existing call unchanged byte-for-byte), and add a HIGH point-set `("verify","ship")` stratum reported as a THIRD readout beside the existing (miss-rate, FPR) pair — never a second sibling calibration test (that would be exactly the divergent-drift failure `_effective_target_map`'s docstring at 472–473 warns against). The HIGH stratum must read findings LIVE via `self._gate_findings(path, "verify"/"ship")` filtering HIGH — never from `_GOLDEN_SHIP_FINDINGS` / `_INCIDENTAL_GAP_CODES` / any stored expected-map (the D-09 no-self-reference rule folded into this decision).

**Rationale:** one honest calibration source, a stratification dimension (severity-tier × point-set) added, not two sources with competing headlines; reading the golden ledger as "what fired" would make the catch rate tautological.

**Source:** 20-CONTEXT.md (D-03); 20-A-PLAN.md Task 3.

---

### D-01 — zero-mint; catalogue stays 275

Phase 20 ships fixtures, tests, and a doc-binding parser — no `report.add` call site — so no finding code is minted. The deliberate tell (mirroring REQ-P19-03's absent 06x decade): zero `report.add` sites in Phase-20 artifacts, the pre-allocated `DSX-STA` range stops at 122 with 123–129 unused and the 130s reserve untouched, and `python scripts/gen-finding-catalogue.py --check` stays green at Total: 275.

**Rationale:** a runtime "doc/code divergence" finding code is explicitly not wanted — divergence must be caught at build/CI time by a test failing red (the `--check` model), not laundered into a spec-audit finding.

**Source:** 20-CONTEXT.md (D-01).

---

### D-02 — REQ-P20-04 mechanism: read-only cross-check test, not a generated mirror; two-tier binding + visible skip-list

`references/test-selection.md` (303 lines) is ~280 lines of irreducible hand-written prose (the Boschloo footnote, "Notes that change the answer," the ranked-assumptions section, six routing tables governed by different engines) — the `gen-finding-catalogue.py` generated-mirror precedent works for `finding-codes.md` because that file is 100% mechanical, but does not transfer to a document humans read as one piece.

**Decision:** a new disjoint file `tests/test_doc_code_agreement.py` with a two-tier binding — Tier 1 strict cell-equality of Decision-table rows 8–24 to `recommend_test` (plus a Boschloo-fallback assertion for the proportion/2/no cell against `stats.py:139–144`), Tier 2 set-membership of the six `recommend_*` mirror tables against their engines' acceptable sets, and a visible enumerated skip-list so every un-parsed row is a declared exclusion.

**Rationale:** `recommend_test` is pure and total so cell-equality is a fully provable claim on the decision table; the mirror tables are legitimately set-valued (e.g. Spearman-vs-Kendall), so single-cell equality there would be a false model — membership is the honest ceiling their structure supports. The skip-list prevents the test from passing by silently failing to parse a row.

**Source:** 20-CONTEXT.md (D-02); 20-D-PLAN.md.

---

### D-04 — fixture stratification: all 15 codes are PRESENT-caught; none is ABSENT; the 5 Phase-18 codes are the real fixture gap

Verified live: the 10 Phase-19 codes already fire on `examples/bad-ANALYSIS-SPEC.yaml` at ship; the 5 Phase-18 codes (050/051/060/061/062) fire nowhere in `examples/` today. Each has an unambiguous declared-field trigger (`stats.py:924/942/979/1008/1035`), and the triggers are mutually exclusive on `analysis.test` (`pearson_correlation` vs `icc` vs `weighted_kappa` vs `cohens_kappa`).

**Decision:** the 5 Phase-18 codes get PRESENT known-bad fixtures; none of the 15 is declared ABSENT. `_ABSENT_PARTITION_FLOOR` stays 3 (`test_known_bad_corpus.py:452–454, 680`).

**Rationale:** declaring any of the 15 ABSENT would be a false "uncatchable" claim (they have live-firing unit tests) and would launder a HIGH-firing code through the CRITICAL-only miss-union (see D-13-a below).

**Source:** 20-CONTEXT.md (D-04).

---

### D-05 — FPR is currently silent, not clean, on the 15 → add valid negative controls

`_false_positive_findings` counts CRITICAL+HIGH blocking codes (`test_known_bad_corpus.py:696`), so a genuinely-firing one of the 15 on a good spec would be counted — but the 12 pre-existing good-corpus control specs are all outcome-comparison specs that never declare `estimand_kind=correlation/agreement` or `test=icc/pearson_correlation/kappa`, so none routes into any of the 15's branches. FPR = 0/12 was therefore silent, not a real negative control for these codes.

**Decision:** add ≥1 valid good-corpus control per routing family (a valid `icc` with a complete triple, a `weighted_kappa` with recognised weights + `p_pos`/`p_neg`, a correctly-scaled correlation), keeping the denominator ≥10 (line 1587) and growing it; also add a guard asserting `_FPR_TEMPDIR_NOISE_CODES` stays disjoint from the DSX-STA family so no future editor can silently absorb a real false positive as noise.

**Rationale:** a 0/N false-positive rate is only meaningful if N includes cases that actually exercise the branches being measured.

**Source:** 20-CONTEXT.md (D-05).

---

### D-06 — re-baseline semantics: exactly one committed number moves

The only committed number that moves is `_GOLDEN_SHIP_FINDINGS` (`test_causal_verb_golden.py:82–198`) — it gains a measured key per new known-bad fixture. The synthetic anchor `_headline((2,5),(1,4),(3,10)) == (0.25, 0.3)` (line 1490, `TestStratifiedHeadlineHelpers`) and `_ABSENT_PARTITION_FLOOR = 3` (line 680) must NOT move. The headline stays the pair (miss-rate, FPR); the HIGH-tier PRESENT catch stratum is a third readout reported beside the pair, never folded into it, so target-present-invariance (adding a caught PRESENT case cannot move the pair, 1676–1682) is preserved by construction.

**Rationale:** re-baselining must be additive and provably non-perturbing to the pre-existing calibration contract — otherwise a re-baseline could silently mask a regression in the existing CRITICAL partition.

**Source:** 20-CONTEXT.md (D-06).

---

### D-07 — two-wave, file-disjoint, single-writer split (rigour tie-break, not a conflict resolution)

Four file-disjoint plans, one per requirement (A=REQ-P20-01, B=REQ-P20-02, C=REQ-P20-03, D=REQ-P20-04). Wave 1 = structural guards (C + D), so any latent doc↔code divergence surfaces and is repaired first; Wave 2 = calibration (A + B), measured against the settled state (Phase-12 "measure last" discipline).

**Rationale:** the file sets are already disjoint (not a single-writer conflict), so the wave split is chosen purely on the rigour > reliability > flexibility tie-break — measuring calibration against a state where structural guards have already run and repaired anything they found is more rigorous than measuring against an unverified state.

**Source:** 20-CONTEXT.md (D-07); confirmed in every plan's `<single_writer_proof>` block (20-A-PLAN.md, 20-B-PLAN.md, 20-C-PLAN.md, 20-D-PLAN.md).

---

### D-08 — effect-size bands stay conventions, never blocking thresholds

No Phase-20 artifact converts any band (Cohen d/h/r, Landis-Koch kappa, Koo-Li ICC, Kendall W) into a blocking threshold. The 15 codes read declared vocabulary/presence only, never a computed statistic (`stats.py:915`); the calibration keys entirely on `f["code"]`.

**Rationale:** the HIGH-tier stratum and all Phase-20 tests classify on finding CODE identity only, introducing no numeric-magnitude comparison — preserving the declaration-only surface discipline carried since Phase 17.

**Source:** 20-CONTEXT.md (D-08).

---

### D-13-a — the falsifiability-guard miss-union is CRITICAL-only; named deferral, not exploited this phase

`test_attribution_tags_are_falsifiable_against_live_gate` builds its miss-union from CRITICAL severity only (`test_known_bad_corpus.py:1534–1547`), so a HIGH code tagged "miss" would pass `assertNotIn(absent_code, all_critical)` even though it fires at HIGH — a latent laundering risk. Not exploited this phase because all 15 new codes are PRESENT (D-04).

**Rationale (why deferred, not fixed):** named loudly rather than silently left as a gap — any future HIGH code that ever legitimately needs an ABSENT declaration requires the miss-partition severity filter to be widened first; there is no current need since D-04 guarantees no ABSENT declaration this phase.

**Source:** 20-CONTEXT.md ("Named deferrals" section, D-13-a); reaffirmed in 20-A-PLAN.md must_haves ("no new fixture relies on an ABSENT HIGH declaration").

---

## Lessons

### `inference.primary_procedure` must be omitted on correlation/agreement fixtures to keep the ship set to exactly one code

**What was learned:** the plan expected each of the five new known-bad fixtures to fire exactly `{DSX-STA-05x}` at ship, but the frequentist admissibility ontology (`references/families.yaml`) has no correlation/agreement family. Declaring `primary_procedure: pearson_correlation` drew a spurious `DSX-ADM-020` (unresolved procedure); leaving the cloned template's `primary_procedure: welch_t` drew `DSX-PRE-030` (executed `analysis.test` differs from declared branch). Omitting `inference.primary_procedure` entirely makes admissibility resolve `not_declared` (clean) and the prereg branch `None` (DSX-PRE-030 early-returns), leaving the executed routing to live purely in `analysis.test` — which is what the DSX-STA-05x gate actually reads.

**Context:** discovered during Task 1's live measurement of the first fixture, not predicted at plan time; the fix was trusted over the plan's original expectation per the project's measurement-integrity rule, and documented in every fixture's `inference:` comment.

**Source:** 20-A-SUMMARY.md (Deviation 1).

---

### The ship-completeness guard forced `_HIGH_TARGET_DEFECT_CODES` to be created a full task earlier than planned

**What was learned:** the plan assigned the new `_HIGH_TARGET_DEFECT_CODES` map to Task 3, but Task 1's own verify step runs `test_ship_gate_findings_are_all_documented_incidental_corpus_gaps`, which requires every ship-blocking code to be either incidental or one of the fixture's own codes via `_own_target_codes`. With empty `_EXPECTED_CAUGHT_DEFECTS` and no `_TARGET_DEFECT_CODES` entry (both required by D-04/D-08), `_own_target_codes` would have been empty and each new fixture's HIGH code would have read as an undocumented over-block.

**Context:** front-loading the map into Task 1 (with `_own_target_codes` extended to read it as a `high_map` source) kept D-09 intact, since the map remains a declaration of intent (like `_TARGET_DEFECT_CODES`), never the measured ledger — Task 3 then simply consumes the pre-existing map for the live stratum.

**Source:** 20-A-SUMMARY.md (Deviation 2).

---

### Glob-based corpus-matrix tests outside the plan's declared file set still needed updating when new fixtures were added

**What was learned:** `tests/test_frame_val.py::_EXPECTED_VAL_CODES` and `tests/test_dsx.py::test_every_committed_spec_declares_a_valid_estimand_type` discover the known-bad corpus by glob over `examples/` and each maintain a matrix/count that any fixture addition silently invalidates. These files were not in 20-A-PLAN.md's declared `files_modified` list.

**Context:** surfaced only in the final full-suite regression run after Task 3, not by any task-scoped verify command; fixed by adding the five new fixtures to `_EXPECTED_VAL_CODES` (each measured `set()`) and bumping the committed-spec estimand-type count 14 → 19. Confirmed non-conflicting with every other plan's single-writer file set before committing.

**Source:** 20-A-SUMMARY.md (Deviation 3).

---

### A `[^1]`-based split truncates the Decision table at row 10, not row 24 — the marker is in-cell, not just a footnote definition

**What was learned:** both 20-C's Task 2 verify command and 20-D's Tier-1 plan text bound the Decision-table block with `...split('[^1]',1)[0]`. This is wrong: `[^1]` also appears in-cell inside the proportion/2/no row ("...expected cell < 5)`[^1]`" on line 10), so splitting on the first occurrence truncates the table there instead of at the footnote definition (line 26) — meaning the intended "15 rows parsed" / "terminal row = time-to-event" assertions would silently pass on a 1-row table (or fail outright), not prove what they claimed to prove.

**Context:** caught by the orchestrator during 20-C's execution (brief §5, "re-run, don't trust"); the fix bounds the block at the next `##` heading instead (`re.split(r'\r?\n##\s', after, 1)[0]`, since footnote lines don't start with `|` and are already excluded). The correction was explicitly carried forward into 20-D's Tier-1 firing to avoid the same trap recurring.

**Source:** 20-C-SUMMARY.md ("Plan-defect caught and corrected"); 20-D-SUMMARY.md ("Plan-defect carried and corrected").

---

### A dead local variable (`dist_key`) survived into the delivered test module — same class of wart as prior-phase findings

**What was learned:** in `tests/test_doc_code_agreement.py::test_decision_table_cell_equality_and_boschloo`, `dist_key = "censored" if dist in DASHES else dist` was assigned but never read — an early-draft artifact left over once the censored/time-to-event row was instead handled by an explicit `if dist in DASHES: kwargs = {}` branch.

**Context:** flagged as LOW-1 in code review and fixed in the same unit (S4-4); behaviour-neutral (the 15-row cell-equality assertion was byte-identical after removal). The review note explicitly classifies this as "the same class as the S3-4 dead-import and S1-4 missing-`Any` findings" — a recurring low-severity pattern of unused locals surviving test authoring across phases.

**Source:** 20-REVIEW.md (LOW-1).

---

### Single-writer files with glob-based invariants force artificial commit-splitting discipline

**What was learned:** the three good-corpus negative controls (Task 2) and the five known-bad fixtures (Task 1) both needed entries in the same single-writer file `tests/test_causal_verb_golden.py`, and `test_golden_keys_match_the_examples_tree_on_disk` globs `examples/**` — meaning any fixture present on disk without a matching golden-ledger entry fails the whole suite, not just the fixture's own test.

**Context:** to keep each per-task commit self-consistent (a hard project convention), the good-corpus controls were stashed out of the working tree during the Task-1 commit and restored for Task 2, rather than committing all eight fixtures' golden entries together.

**Source:** 20-A-SUMMARY.md (Deviation 4, "commit granularity").

---

### A blind persona spawn without file reads is worthless and must be discarded, not salvaged

**What was learned:** during the S4-1 persona round, the first Statistician (`dsx-statistician`) spawn produced no file reads at all and was discarded and re-run — its output could not be trusted as "verified live" per the phase's evidentiary standard (both personas were required to return `file:line` locators from actual spot-checks, not adjudicated blind).

**Context:** recorded explicitly in the ledger Log per 20-CONTEXT.md's persona-round note; the corrected re-run is what produced the load-bearing D-03 discovery.

**Source:** 20-CONTEXT.md ("Persona round" section).

---

## Patterns

### Clean-template fixture cloning for known-bad corpora

Every new known-bad fixture (and every new good-corpus control) is authored by cloning a verified clean minimal-reference spec (`examples/good-corpus/freq-continuous-aov-ANALYSIS-SPEC.yaml`) byte-for-byte — keeping its `decision.replay`, `metrics[].source`, `reproducibility.entrypoint` + `repro_lock`, `narrative.path`, `validity_frame`, and `inference` blocks — and replacing ONLY the `analysis:` block (plus pointing `claims[].evidence`/`narrative.path` at a fixture-specific NARRATIVE.md sibling) with the one declaration that carries the target defect (or, for a control, the valid form that reaches but doesn't trip the branch).

**When to use:** whenever a new known-bad or good-corpus fixture must be added to prove a single, attributable finding-code catch or silence, without risking contamination from unrelated findings elsewhere in the spec.

**Source:** 20-A-PLAN.md (`<fixture_bindings>`); 20-A-SUMMARY.md.

---

### Severity-parameterized classifier extension that preserves every existing call byte-for-byte

`_classify_target_defect` gained a trailing `severity` parameter defaulting to `"CRITICAL"`, so every pre-existing call site (which passes no severity) is untouched, while a new call path can pass `severity="HIGH"` to add an entirely new stratum without duplicating the classifier or its surrounding harness.

**When to use:** extending a calibration/classification function to cover a new dimension (here: severity tier) when the existing behavior must remain provably unperturbed — prefer a defaulted parameter over a parallel/sibling function, since a sibling risks becoming a second source of truth that drifts from the original (the exact failure `_effective_target_map`'s docstring warns against).

**Source:** 20-CONTEXT.md (D-03); 20-A-PLAN.md Task 3; 20-A-SUMMARY.md; 20-REVIEW.md (adversarial probe 2).

---

### Live-read-only measurement stratum (no-self-reference / D-09 pattern)

The HIGH-tier PRESENT catch is derived exclusively from `self._gate_findings(path, point)` filtered to HIGH at measurement time — the golden ledger (`_GOLDEN_SHIP_FINDINGS`) and any other stored expected-map are referenced only in prose/comments explaining they are deliberately NOT read, never as an executable read inside the measuring method. A companion positive test (`test_high_stratum_target_codes_fire_and_are_named`) additionally asserts each code fires live AND is named in its fixture's POSTMORTEM AND is disjoint from `_INCIDENTAL_GAP_CODES`.

**When to use:** any time a calibration/coverage metric could tautologically "prove" itself by reading the same declaration it's supposed to be independently verifying — enforce that the measurement path and the declaration-of-intent path are structurally distinct, and add a source-scan assertion (grep the method's own source for the forbidden identifier) as a guard against future regression.

**Source:** 20-CONTEXT.md (D-03/D-09); 20-A-PLAN.md; 20-SECURITY.md (T-20-A-01); 20-REVIEW.md (adversarial probe 1).

---

### Read-only doc↔code cross-check with an exhaustiveness net (bound count + skip-list) instead of a generated mirror

`tests/test_doc_code_agreement.py` binds a hand-written prose document to routing engines via two tiers (strict cell-equality where the engine is pure/total; honest set-membership where the doc table is legitimately set-valued), backed by an explicit, enumerated `SKIP_SECTIONS`/`SKIP_ROW_MARKERS` list and an exhaustiveness assertion that every pipe-delimited row in the file is either bound or explicitly skip-listed (`bound == 31` out of `total_data_rows == 57`, with 26 skip-listed). A negative control (a deliberately-wrong primary, `welch_t` vs the engine's `welch_anova`) confirms the assertion actually fails on divergence rather than passing leniently.

**When to use:** whenever a document that is too prose-heavy to regenerate mechanically must still be kept provably in sync with the code it describes — prefer this over a generated-mirror approach (which only works for 100%-mechanical references), and always pair the binding with an exhaustiveness/anti-vacuity check so a parser bug (dropped or mis-scoped row) cannot produce a false green.

**Source:** 20-CONTEXT.md (D-02); 20-D-PLAN.md; 20-D-SUMMARY.md; 20-REVIEW.md (adversarial probe 3); 20-SECURITY.md (T-20-D-02).

---

### Zero-mint close proven by byte-frozen production diff, not by absence of complaints

The zero-mint claim is proven, not asserted, via `git diff <plan-start-commit>..HEAD -- dsx scripts references` returning empty, combined with `python scripts/gen-finding-catalogue.py --check` exiting 0 at Total 275, a byte-frozen Phase-12 snapshot assertion (`tests/fixtures/finding-codes-phase12.md` at 256, and a subset-of-current-catalogue check), and a constructed (not hard-coded) numeric-range check that the 123-onward reserve band is absent from the catalogue.

**When to use:** any terminal/close phase whose success criterion is "nothing changed in production" — pin the specific commit range and diff it against the exact directories that must stay frozen, rather than trusting a description of what wasn't touched; construct reserve-band checks programmatically so the guard doesn't rot as new codes are added elsewhere.

**Source:** 20-B-PLAN.md; 20-B-SUMMARY.md; 20-VERIFICATION.md (Orchestrator gate evidence); 20-SECURITY.md (T-20-B-01, T-20-B-03).

---

### Dynamic `dir()`-based enumeration with an anti-vacuity superset assertion for future-proof structural guards

`NoAutoswitchEveryNewCategoryTest` enumerates every `recommend_*` function in `dsx.checks.stats` by introspection (`dir()` + `callable`) rather than hard-coding a list, then asserts the enumerated set is a superset of the currently-known eight new-category routers AND includes `recommend_test` (the one deliberately-excluded legacy router) — so a future rename or a newly-added router that lacks a dataless signature is caught automatically, and a rename cannot silently empty the proof into a vacuous pass.

**When to use:** any "prove every X has property P" structural guard where X is an open-ended, growing set (new routing categories, new finding families, new plugin types) — enumerate dynamically and pin a non-vacuity floor, rather than hand-listing members that will drift out of date.

**Source:** 20-C-PLAN.md Task 1; 20-C-SUMMARY.md; 20-REVIEW.md (adversarial probe 4); 20-SECURITY.md (T-20-C-02).

---

### Terminal-fallthrough position pinning on both the code side and the doc side

To guard against a future contributor silently displacing the `time_to_event` → `log_rank` unconditional fallthrough, the regression pins TWO independent positions: on the code side, that the LAST `return _rec(` line in `inspect.getsource(recommend_test)` names `log_rank`; on the doc side, that the FINAL data row of the `## Decision table` block (correctly scoped to end at the next `##` heading, not the in-cell `[^1]` marker) has Outcome = time-to-event. Either a new branch appended after the fallthrough or a new decision-table row appended after the terminal row turns the corresponding assertion red.

**When to use:** whenever correctness depends on an element being LAST in an ordered sequence (a fallthrough branch, a terminal row, a default case) rather than merely present — pin the position explicitly on every side (source and documentation) that encodes the ordering, since a positional regression can pass a naive "is it present somewhere" check.

**Source:** 20-C-PLAN.md Task 2; 20-C-SUMMARY.md; 20-SECURITY.md (T-20-C-03).

---

## Surprises

### The pre-existing calibration test was a provable no-op on all 15 new codes — a null result that would have worn a coverage star

The existing `test_stratified_catch_rate_and_fpr_report` was CRITICAL-only in both partitions (the PRESENT loop iterates only `("plan","execute")`, and `_classify_target_defect` filters to CRITICAL-severity findings only), while every one of the 15 new codes is HIGH and fires only at verify/ship. Re-running the unmodified harness would return a number provably invariant to the 15 new codes — the Statistician's persona framed reporting that as "re-baselined to cover the fifteen" as "a null result wearing a coverage star."

**Impact:** reshaped the entire phase — it became the LOAD-BEARING discovery (D-03) that the deliverable had to be a structural extension of the harness (a new severity/point-set stratum), not merely re-running or adding fixtures to the existing test.

**Source:** 20-CONTEXT.md (D-03); 20-SECURITY.md (T-20-A-02).

---

### The false-positive rate on the 15 new codes was silently meaningless, not genuinely clean

FPR = 0/12 looked like a clean negative-control result, but none of the 12 pre-existing good-corpus specs declared `estimand_kind=correlation/agreement` or a correlation/ICC/kappa test — so none of them ever reached any of the 15 codes' branches. The "0" was measuring an unreached code path, not an actual absence of false positives.

**Impact:** required authoring three new good-corpus fixtures specifically designed to reach each routing family's branch and correctly stay silent, growing the FPR denominator 12 → 15, before the FPR figure could honestly be called a negative control on the 15.

**Source:** 20-CONTEXT.md (D-05).

---

### An in-cell footnote marker masquerading as a footnote-definition boundary would have silently truncated the Decision table to one row

Both 20-C's and 20-D's initial parsing approach used `split('[^1]', 1)[0]` to bound the Decision-table block, not anticipating that the same `[^1]` marker also appears inline inside the proportion/2/no row's cell text (not just at the footnote's definition further down the file). This would have truncated the "15 decision rows" and "terminal row is time-to-event" assertions down to effectively one row, silently weakening the very proofs the phase was built to deliver.

**Impact:** caught structurally by the orchestrator during 20-C's execution before it could propagate; the fix (bound at the next `##` heading instead) was explicitly carried forward into 20-D to prevent the same defect recurring in a second plan reading the same document.

**Source:** 20-C-SUMMARY.md; 20-D-SUMMARY.md.

---

### Declaring a correlation/agreement test in `inference.primary_procedure` triggers findings from an unrelated ontology that has no concept of correlation

The frequentist admissibility ontology (`references/families.yaml`) has no correlation/agreement family at all, so declaring `primary_procedure: pearson_correlation` didn't get silently ignored — it produced a spurious `DSX-ADM-020` (unresolved procedure), and leaving a stale non-matching value produced a spurious `DSX-PRE-030` (executed test differs from declared branch). This was not knowable from reading `stats.py`'s DSX-STA firing predicates alone.

**Impact:** every one of the eight new correlation/agreement fixtures (5 known-bad + 3 good-corpus controls) had to omit `inference.primary_procedure` entirely to keep the measured ship set to exactly the intended single code — a cross-ontology interaction the plan's fixture-authoring guidance hadn't anticipated.

**Source:** 20-A-SUMMARY.md (Deviation 1); 20-REVIEW.md (adversarial probe 6).

---

### The doc/code cross-check found zero divergence — the Boschloo-class risk was already closed, not merely assumed closed

Despite building a structural mechanism specifically to catch drift between `references/test-selection.md` and the routing engines (the class of bug the Boschloo divergence exemplified), the Tier-1 and Tier-2 cross-check surfaced no divergence at all: all 15 decision rows and all 16 mirror rows agreed with the engines, and `references/test-selection.md` / `dsx/checks/stats.py` stayed byte-frozen through the whole plan.

**Impact:** confirms 18–19 closed genuinely green rather than merely reporting green — but also means the mechanism's true discriminating power was only proven indirectly, via the deliberately-wrong negative control (`welch_t` vs the engine's `welch_anova`) rather than by catching a real, pre-existing bug.

**Source:** 20-D-SUMMARY.md ("Divergence disposition"); 20-VERIFICATION.md (REQ-P20-04).

---

### A persona spawn can produce zero evidence and still return a confident-sounding output — the process must actively discard, not merely discount, blind runs

The first Statistician (`dsx-statistician`) spawn in the S4-1 persona round produced no file reads at all, meaning none of its claims could have been grounded in the live codebase. Rather than weighting its output lower, the process discarded it outright and re-ran the spawn.

**Impact:** the discarded run is explicitly logged in the ledger as a named event, not silently dropped — establishing that ungrounded agent output is treated as zero-value rather than low-value evidence in this project's decision process.

**Source:** 20-CONTEXT.md ("Persona round" section).
