# Phase 20: Calibration and reporting close — Context

**Milestone v2.3 Test Catalog · S4-1 discuss (light) · 2026-09-02.** The **terminal**
phase (4 requirements, REQ-P20-01 … REQ-P20-04). Phases 17 (foundation), 18
(correlation / agreement) and 19 (RM / trend / categorical / resampling / post-hoc)
are CLOSED. Across 18–19 the milestone minted **15** new blocking codes —
DSX-STA-050/051/060/061/062 (Phase 18) + DSX-STA-070/080/081/090/100/110/111/120/121/122
(Phase 19). Catalogue is at **275**. Phase 20 is the Phase-12-precedented calibration
close: it lands known-bad fixtures for every new blocking code, re-measures the
**stratified catch rate + false-positive rate**, and adds the doc/code agreement test
that structurally prevents the Boschloo divergence class from recurring. **Phase 20
mints zero codes — catalogue stays 275 (D-01).**

## Phase Boundary

Declaration-only surface, exactly as 17–19: every artifact reads DECLARED strings /
structures; nothing computes on data. Phase 20 adds **fixtures (data), tests
(assertions), and a doc-binding parser** — none of which is a `report.add(...)` call
site, so no code is minted (D-01). Both canonical fixtures are **extended, not
replaced** (D-08 corpus discipline); frozen catalogue snapshots stay byte-frozen; new
codes were already added to the D-05 allowlist by exact name during 18–19. Any
effect-size band stays a **labeled convention, never a blocking threshold** (D-08);
the calibration counts finding **CODE** catch/FPR, never a band boundary.

## Persona round (LOOP-BRIEF §4)

Architect (`dsx-analysis-architect`) + Statistician (`dsx-statistician`), both opus/high,
concurrent — the two relevant personas for a calibration + doc-binding phase. The
**Auditor lens (measurement integrity / no-self-reference)** was **folded into the
Statistician's charge**, recorded loudly, rather than spawned as a third agent (the
"light" scope + pacing): its output is D-05 and the D-09 self-reference guard in D-03.
Tie-break **rigour > reliability > flexibility**. The round was run by the orchestrator
(opus/high) as tightly-scoped parallel spawns fed the S0–S3-verified ground truth (the
15 new codes, the Phase-12 calibration precedent, the `recommend_test` ↔ `test-selection.md`
seam) — adjudicated, not blind-explored. Both personas performed live file spot-checks and
returned `file:line` locators; the first Statistician spawn produced no file reads and was
discarded and re-run (recorded in the ledger Log).

> **The round surfaced a load-bearing discovery that reshapes the phase (D-03).** It is
> recorded first because every other decision depends on it.

## Decisions

### D-03 (LOAD-BEARING) — the 15 new codes are HIGH / verify-ship-only, so the existing calibration is a provable NO-OP on them; the deliverable is to EXTEND the harness with a live HIGH stratum, not re-run it

Both personas confirmed live, on three independent legs:

1. All 15 new codes are severity **HIGH** (`dsx/checks/stats.py` firing sites 924–1357),
   and the `stats` check is registered **only** at verify/ship (`dsx/cli.py:120–130`),
   where the gate blocks at HIGH; plan/execute block at CRITICAL.
2. The existing calibration `tests/test_known_bad_corpus.py::test_stratified_catch_rate_and_fpr_report`
   (line 1557) is **CRITICAL-only in both partitions**, by two independent structural
   barriers: the PRESENT loop iterates only `_CRITICAL_THRESHOLD_POINTS = ("plan","execute")`
   (line 1607), and `_classify_target_defect` compares expected codes against
   **CRITICAL-severity findings only** (299/313). The ABSENT-partition union is likewise
   CRITICAL-only (1638–1640).
3. Consequence: re-running the current harness returns a number **provably invariant** to
   the 15 — they add zero cells to the plan/execute CRITICAL partition. Reporting that as
   "re-baselined to cover the 15 new codes" would be **a null result wearing a coverage
   star** (Statistician). The claim the evidence licenses ("the 15 fire at verify/ship")
   is *not* the claim REQ-P20-01 asks for ("the stratified calibration measures them").

**Decision (orchestrator, rigour):** the load-bearing REQ-P20-01 deliverable is to
**extend the single calibration test with a HIGH verify/ship stratum** alongside the
existing CRITICAL plan/execute partition — parameterize `_classify_target_defect` by a
`severity` argument that **defaults to `"CRITICAL"`** (every existing call unchanged
byte-for-byte) and iterate a HIGH point-set `("verify","ship")` for the new stratum.
**Do NOT add a Phase-20 sibling calibration test** — a second source with its own
headline is exactly the divergent-drift failure the module was rewritten to prevent
(`_effective_target_map` docstring 472–473). One honest calibration source, a
stratification *dimension* (severity-tier × point-set) added, not two sources.

The HIGH stratum **must read findings LIVE** via `self._gate_findings(path, "verify"/"ship")`
filtering HIGH — **never** from `_GOLDEN_SHIP_FINDINGS` / `_INCIDENTAL_GAP_CODES` / any
stored expected-map (the **D-09 no-self-reference rule**). The tempting shortcut of reading
`_GOLDEN_SHIP_FINDINGS` (which already lists which of the 15 fire on the monolith) as "what
fired" is a D-09 violation and is prohibited.

### D-01 — zero-mint; catalogue stays 275

Phase 20 ships fixtures + tests + a doc-binding parser — **no `report.add` call site**, so
no finding code is minted. The **deliberate tell** (mirroring REQ-P19-03's absent 06x
decade): zero `report.add` sites in Phase-20 artifacts, the pre-allocated `DSX-STA` range
stops at **122** with **123–129 unused and the 130s reserve untouched**, and
`python scripts/gen-finding-catalogue.py --check` stays green at **Total: 275**. A runtime
"doc/code divergence" code is explicitly *not* wanted — divergence is caught at build/CI
time by the agreement test failing red (the `--check` model), not at spec-audit time.

### D-02 — REQ-P20-04 mechanism: CROSS-CHECK TEST (not generated mirror), dual binding + visible skip-list

`references/test-selection.md` (303 lines) is ~280 lines of **irreducible hand-written
prose** a generator cannot emit — the Boschloo footnote `[^1]` (26–32), "Notes that change
the answer" (34–52), the ranked-assumptions section (54–64), and six *other* routing tables
governed by different engines. The `gen-finding-catalogue.py` generated-mirror precedent
works for `finding-codes.md` because that file is 100% mechanical; it does **not** transfer
to a document humans read as one piece. **Decision: a read-only cross-check test** in a new
disjoint file `tests/test_doc_code_agreement.py`, with a **two-tier binding**:

- **Strict cell-equality** of Decision-table rows 8–24 to `recommend_test`: parse each
  `(Outcome, Groups, Paired, Distribution) → Test` cell, map to
  `recommend_test(outcome_type, n_groups, paired, normal, equal_variance, n_per_group)`,
  and assert the parsed Test cell **equals** the returned `["test"]`. For the proportion/2/no
  cell (line 10) additionally assert the Boschloo fallback appears in the returned
  `["alternatives"]` (`stats.py:139–144`). `recommend_test` is pure and total, so
  cell-equality is a fully provable claim — and this is the exact cell the Boschloo
  divergence lived in.
- **Set-membership** binding of the six `recommend_*` mirror tables (Association / RM / Trend
  / Resampling / Post-hoc / Proportion-count) to their engines: assert each declared
  coefficient/test is a **member of** that engine's acceptable set for the row's key — the
  exact semantics the runtime gates already use. Asserting single-cell equality on set-valued
  tables would be a false model (over-blocking legitimate Spearman-vs-Kendall choices);
  membership is the **honest ceiling** their structure supports.
- **Visible skip-list**: pointer / DEPRECATED / catalog-only / footnote / annotation rows are
  placed on an explicit, enumerated skip-list — so every un-parsed row is a *declared*
  exclusion and the test can never pass by silently failing to parse. Parser normalization
  tolerates `2`/`3+`/`—`/`normal or n ≥ 200`/bold/`[^1]` and matches with `\r?\n` (CRLF rule).

This closes the divergence **class** on every mirror table (not just the one Boschloo
instance) while never claiming more rigour than each table's structure can prove — the
doctrine's "smaller provable claim; honest membership beats false completeness."

### D-04 — fixture stratification: all 15 are PRESENT-caught; NONE is ABSENT; the 5 Phase-18 codes are the real fixture gap

Verified live: the 10 Phase-19 codes already fire on `examples/bad-ANALYSIS-SPEC.yaml` at
ship (`test_causal_verb_golden.py:100–101`); the 5 Phase-18 codes
(050/051/060/061/062) fire **nowhere** in `examples/` today — `estimand_kind` is inert at
`bad-ANALYSIS-SPEC.yaml:87` (the defect there is a wrong test family). All 15 have dedicated
unit-firing tests + `# D-05:` markers. Each of the 5 has an unambiguous declared-field
trigger (`stats.py:924/942/979/1008/1035`), and the triggers are **mutually exclusive on
`analysis.test`** (`pearson_correlation` vs `icc` vs `weighted_kappa` vs `cohens_kappa`), so
they cannot all fire from one `analysis` block → **~3–5 dedicated known-bad fixtures**, one
per routing family.

**Decision:** the 5 Phase-18 codes get **PRESENT** known-bad fixtures (add firing context);
**none of the 15 is declared ABSENT.** Declaring any ABSENT would be a **false "uncatchable"
claim** (they have live-firing unit tests) — the opposite of the honest-omission the standing
rule protects — and would *launder* a HIGH-firing code through the CRITICAL-only miss-union
(see D-13-a). `_ABSENT_PARTITION_FLOOR` stays **3** (the three coverage-class misses;
`test_known_bad_corpus.py:452–454, 680`). REQ-P20-01 is therefore mostly **confirm-coverage +
re-measure**, with the genuinely-new work being: the HIGH-tier harness stratum (D-03), the 5
Phase-18 corpus fixtures, and the re-baseline.

### D-05 — FPR is currently SILENT, not clean, on the 15 → add valid negative controls

Verified: `_false_positive_findings` counts CRITICAL+HIGH blocking codes
(`test_known_bad_corpus.py:696`), so a genuinely-firing one of the 15 on a good spec *is*
counted. But the 12 good-corpus control specs are outcome-comparison specs — **none** declares
`estimand_kind=correlation/agreement` or `test=icc/pearson_correlation/kappa`, so none routes
into any of the 15's branches. FPR = 0/12 is therefore **silent**, not a real negative control
for these codes.

**Decision:** add **≥1 valid good-corpus control per routing family** (a valid `icc` with a
complete (model,type,definition) triple; a `weighted_kappa` with recognised weights +
`p_pos`/`p_neg`; a correctly-scaled correlation), so the FPR genuinely exercises the 15's
silence. This keeps the denominator **≥10** (line 1587) and *grows* resolution. Also add a
guard asserting `_FPR_TEMPDIR_NOISE_CODES` (the tempdir-noise allowlist) stays **disjoint from
the DSX-STA statistical-validity family**, so no future editor can silently absorb a real
new-code false positive as "noise."

### D-06 — re-baseline semantics: exactly one committed number moves

The only committed *number* that moves is `_GOLDEN_SHIP_FINDINGS`
(`test_causal_verb_golden.py:82–198`) — it gains a measured key per new known-bad fixture
(`test_golden_keys_match_the_examples_tree_on_disk:253` forces every new fixture to carry a
measured entry). The calibration headline pins **no** corpus literal — it is computed live and
asserted only for internal consistency (1660–1673). **Must NOT move:** the synthetic anchor
`_headline((2,5),(1,4),(3,10)) == (0.25, 0.3)` (line 1490 / `TestStratifiedHeadlineHelpers`)
and `_ABSENT_PARTITION_FLOOR = 3` (line 680). The headline stays the pair **(miss-rate, FPR)**;
the HIGH-tier PRESENT catch stratum is a **third readout reported beside** the pair (never
folded into it), so target-present-invariance (adding a caught PRESENT case cannot move the
pair, 1676–1682) is preserved by construction.

### D-07 — wave / single-writer split (planner binds the final assignment at S4-2)

Four file-disjoint plans, one per requirement:
- **A (REQ-P20-01):** `examples/known-bad/*` (new fixtures + sidecars), the 5 Phase-18
  good-corpus controls (D-05), `tests/test_known_bad_corpus.py` (HIGH stratum + re-baseline).
- **B (REQ-P20-02):** `examples/good-ANALYSIS-SPEC.yaml` + `examples/bad-ANALYSIS-SPEC.yaml`
  extension for the 5 Phase-18 codes, `references/finding-codes.md` (regen — no-op at 275),
  `scripts/gen-finding-catalogue.py` (allowlist already satisfied → likely untouched).
- **C (REQ-P20-03):** `tests/test_no_shapiro_autoswitch.py`, `tests/test_time_to_event_fallthrough.py`.
- **D (REQ-P20-04):** `tests/test_doc_code_agreement.py` (**new**), and **sole writer** of any
  `references/test-selection.md` / `dsx/checks/stats.py` repair a surfaced divergence requires.

**Decision:** **two waves on the rigour tie-break** (not on a single-writer conflict — the file
sets are disjoint): **Wave 1 = structural guards (C + D)** so any latent doc↔code divergence D
surfaces is repaired first; **Wave 2 = calibration (A + B)** measured against the *settled*
state (Phase-12 "measure last" discipline). Every writable file is owned by exactly one plan
per wave; `test-selection.md` has multiple readers but one writer (D). Tracking files
(REQUIREMENTS/STATE/ROADMAP) stay orchestrator-serial. The planner (S4-2) is free to collapse
to one wave if it merges D before A's final re-baseline; two waves make the ordering structural
rather than procedural. Wave 1/2 file-disjointness is the single-writer proof.

### D-08 — effect-size bands stay conventions

No Phase-20 artifact converts any band (Cohen d/h/r, Landis-Koch kappa, Koo-Li ICC, Kendall W)
into a blocking threshold. The 15 codes read declared vocabulary/presence only and never a
computed statistic (`stats.py:915`, anti-two-stage note 892); the calibration keys entirely on
`f["code"]`. **Guard:** the HIGH-tier stratum classifies on finding **CODE identity only** and
introduces no numeric-magnitude comparison.

## Named deferrals (loud, not silent — D-13 class)

- **D-13-a — the falsifiability-guard miss-union is CRITICAL-only.**
  `test_attribution_tags_are_falsifiable_against_live_gate` builds its miss-union from CRITICAL
  severity only (`test_known_bad_corpus.py:1534–1547`), so a HIGH code tagged "miss" would pass
  `assertNotIn(absent_code, all_critical)` even though it fires at HIGH — a latent laundering
  risk. **Not exploited this phase** (all 15 are PRESENT, D-04). Named so it is not a silent
  gap: **any future HIGH code that ever legitimately needs an ABSENT declaration requires the
  miss-partition severity filter to be widened first.** Deferred, not fixed (no current need).

## Veto window

Filed to HUMAN-QUEUE as **HQ-24** (non-blocking; silence = accept). Phase 20 mints **no**
codes, so there is **no D-06 code-numbering veto**; the offered items are the two substantive
methodological choices: (1) REQ-P20-04 mechanism = cross-check test over generated mirror
(D-02), and (2) the load-bearing calibration extension = a live HIGH verify/ship stratum in the
existing harness rather than a re-run or a sibling test (D-03). To veto either, reply in a
session; otherwise Phase 20 plan (S4-2) builds on them.

## What S4-2 (plan) must carry forward

1. **D-03 is the load-bearing deliverable** — the HIGH verify/ship stratum, live-read, is not
   an optional refinement; without it "stratified catch rate re-measured" is UNSUPPORTED.
2. Dedicated PRESENT known-bad fixtures firing each of the **5 Phase-18 codes**, each with a
   measured `_GOLDEN_SHIP_FINDINGS` key.
3. **Valid good-corpus negative controls** per routing family (D-05); denominator stays ≥10.
4. REQ-P20-04 cross-check test with the two-tier binding + visible skip-list (D-02).
5. Zero-mint proof (catalogue 275, `--check` green); the anchor `(0.25, 0.3)` and floor `3`
   unmoved (D-06); bands stay conventions (D-08); the D-13-a deferral recorded, not closed.
6. Single-writer waves per D-07 (or a justified one-wave collapse with D merged before A's
   re-baseline).
