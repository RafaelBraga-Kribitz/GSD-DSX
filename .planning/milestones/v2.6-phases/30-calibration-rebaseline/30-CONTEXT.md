# Phase 30 — Calibration re-baseline (terminal) — CONTEXT

**Milestone:** v2.6 Exploration Depth and Backlog Evidence (terminal phase).
**Requirements:** REQ-P30-01, REQ-P30-02, REQ-P30-03. **Discuss unit:** S6-1 (ledger).
Ran inline at opus/high (brief §3; the Phase 24 / S4-1 calibration precedent — a
single-writer tracking-adjacent artifact, no mid-unit compaction, no subagent touches
a tracking file). Persona round inline per brief §4 (Architect + Statistician engaged;
Auditor **not** engaged — zero mint, off-gate-path measurement, no new code path or
input-handling surface; Advisor **not** engaged — no external-tooling / licensing gray
area this phase). The mode choice is itself GA-1 below, recorded loudly with its
rationale.

**One-line frame.** Phase 30 **measures**, it does not design. The three v2.6 evidence
cases are already built, wired into the corpus harness, and gate-verified (Phases
27/28/29, all COMPLETE). Phase 30 re-runs the stratified calibration over the grown
corpus, records the re-baselined headline pair + strata + friction in a `30-READOUT.md`
with an adversarial Statistician review, refreshes the two stale calibration records
(brief §6.5 backdrop + the literature deferred table), and confirms every
milestone-audit prerequisite. **Zero codes.** The corpus fixtures and every gate module
stay byte-frozen — the phase's only edits are the readout, the two doc records, and (if
S6-2 finds a genuine gap) an audit-prerequisite test.

## 0. Ground truth (read live this firing, not assumed)

- **Live catalogue = 279 codes** (`references/finding-codes.md:16` — "**Total: 279
  codes.**"; `DSX-COH-041` present, `grep -c` = 1). This is the post-Phase-29 count
  (S5-3/S5-4/S5-5 each re-ran `gen-finding-catalogue.py --check` EXIT 0 @ 279).
  **Re-measure live at S6-2/S6-3 — do not assume 279 has held** (D-06 note §2). Phase
  30 target: **set-identity 279 → 279, added={} removed={}.**
- **Corpus has grown to 42 known-bad + 15 good-control ANALYSIS-SPECs** (live count
  this firing: `examples/known-bad/*-ANALYSIS-SPEC.yaml` = 42, was **39** as of
  2026-09-06 per V2.6-SCOPE; the **+3** are exactly the v2.6 evidence cases;
  `examples/good-corpus/*-ANALYSIS-SPEC.yaml` = 15). **The FPR denominator therefore
  moves 12 → 15** vs the Phase-12 readout (three good-control specs added since).
- **6 attribution sidecars: 5 `kind: miss` + 1 `kind: target`** (live
  `grep "^kind:" examples/known-bad/*-ATTRIBUTION.yaml`):
  - **miss** — `feature-origin-only-leak` (`absent_code: DSX-ML-034`, promotes item 7,
    **new this milestone**); `garden-of-forking-paths-p-hacking`;
    `magnitude-without-computed-effect` (`absent_code: DSX-CLM-034`, promotes item 8,
    **new this milestone**); `operator-known-answer-selective-exclusion`;
    `retracted-fabricated-field-experiment`.
  - **target** — `subgroup-harm-without-disposition` (`DSX-COH-041`, promotes item 9,
    **new this milestone** — the corpus's first `kind: target`, PRESENT/DETECTED).
- **Miss-partition floor = 3** (`tests/test_known_bad_corpus.py:1032`,
  `_ABSENT_PARTITION_FLOOR = 3`). Measured misses now = **5 ≥ 3** → floor holds
  comfortably (was met exactly at 3 in Phase 12; the two v2.6 misses raise it to 5).
- **The measurement machinery already exists and is the reproducer of record.**
  `tests/test_known_bad_corpus.py` holds the live functions the calibration uses —
  `_gate_findings` (a real `dsx gate <point>` in a fresh tempdir), `_effective_target_map`,
  `_classify_target_defect`, `_headline`, `_friction`, `_false_positive_findings`,
  `_ABSENT_PARTITION_FLOOR` — and its `test_stratified_catch_rate_and_fpr_report` is the
  durable gate that asserts the partitions and the floor. The Phase-12 pattern extracts
  the printed numbers **read-only, off the gate path** via a committed
  `_measure_readout.py` companion (`.planning/milestones/v2.0.0-phases/12-calibration/_measure_readout.py`
  is the template) — the unittest, not the companion, is the reproducer.
- **Frozen surfaces (must stay byte-identical this phase):** `dsx/checks/dq.py`,
  `dsx/cli.py`, `dsx/checks/viz.py` and the chart corpus (v2.5.0-closed), every corpus
  fixture under `examples/known-bad/` and `examples/good-corpus/` (Phases 27/28/29 wired
  them; Phase 30 **reads** them), and the finding catalogue (zero mint). Package version
  stays 2.0.0 (gate-read `repro_lock.dsx_version`; out of scope per REQUIREMENTS).
- **The two stale calibration records Phase 30 must refresh (both carry Phase-12
  numbers):**
  - `brief.md §6.5` calibration backdrop (`brief.md:439–445`) still reads "**(miss-rate
    1.0, FPR 0.0)** — zero false positives over the **twelve-spec** good-control corpus
    (plan 12-05, 0/12) … a **3/3** miss". The item-7/8/9 entry rows (`:376–378`) and the
    re-evaluation bullets (`:421–437`) were already rewritten by the Phase-27/28/29
    executors (items 7 & 8 **Satisfied** as attributed misses; item 9 **promoted** as a
    PRESENT/DETECTED catch) — Phase 30 **verifies those against the measured re-baseline
    and refreshes the stale backdrop paragraph**, dated, with a short "Phase 30
    re-evaluation" note.
  - `docs/literature/the-ai-data-scientist.md` — the "What is deferred" table
    (`:81–88`) still lists items 7/8/9 as "No such case / paper-shaped instances fire /
    Neither in hand", and the mapping-table row 15 (`:43`) still reads "39 known-bad
    specs, 15 good-control specs"; rows 7/8/9/12 status cells still say **deferred**.
    Phase 30 moves items 7/8/9 out of the deferred table (Satisfied, code + fixture
    named), updates the corpus counts (39 → 42 known-bad; good-control stays 15), and
    flips the affected status cells.

## 1. Gray areas settled (persona round — loud, not silent)

### GA-1 — Persona-round mode and the readout deliverable shape

**Decision.** (a) Run the S6-1 persona round **inline** (Architect + Statistician),
matching the Phase 24 calibration precedent, and (b) produce a committed
`30-READOUT.md` mirroring `12-READOUT.md` (headline pair → stratified PRESENT/ABSENT →
FPR → per-family friction → limits → **adversarial Statistician review**), whose
**durable reproducer is the existing `test_stratified_catch_rate_and_fpr_report`**, with
the numbers extracted by a read-only `_measure_readout.py` companion. The heavy
adversarial Statistician review is part of the **readout** (S6-3/S6-4), **not** the
discuss — exactly the 12-READOUT precedent, where the review folded into the readout and
no measured number changed.

**Persona round.**
- **Architect (dsx-analysis-architect):** the calibration re-baseline is *measurement of
  an already-built corpus*, not a design. The classification of every case is already
  fixed by the harness maps the evidence phases committed; the discuss's job is to name
  the deliverable and confirm the method, not to re-decide the corpus. Spawning two opus
  personas to re-derive facts the reproducing unittest already asserts adds wall-clock
  and mid-unit-compaction risk for no design decision they would actually make. →
  **inline + `30-READOUT.md`.**
- **Statistician (dsx-statistician):** the load-bearing judgement in a calibration
  readout is *framing*, not arithmetic — how to read a 1.0 miss-rate (a construction
  invariant, not a sampled rate; F3 in the 12-READOUT review), what a one-sided upper
  bound on the FPR means, whether the floor is honestly met. That judgement belongs in
  the **adversarial readout review** (against measured numbers at S6-3/S6-4), where it
  can bite on real output, not in a pre-measurement discuss where there is nothing yet to
  review. Deferring it *preserves* the rigour rather than spending it early. →
  **inline discuss; adversarial review at the readout, RECORD-WITH-AMENDMENTS gate.**

**Tiebreak (rigour > reliability > flexibility):** unanimous **(a)**. Rigour is *not*
sacrificed by running inline: (i) every "ground truth" fact in §0 was read live this
firing; (ii) the calibration arithmetic is self-gating — the reproducing unittest asserts
the partitions and the floor, so no persona vote can make a wrong number pass; (iii) the
adversarial Statistician review is preserved in full, deferred to the point where it has
measured output to attack. This is the smaller, provable claim (brief: "prefer the
smaller, provable claim every time").

**Rejected — (b) spawn two parallel opus personas at discuss:** the pattern the v2.6
evidence phases used, correct *there* because each phase **designed** a new check and
each persona re-grounded the check code independently. Phase 30 designs nothing; the
independent re-grounding that matters is the reproducing unittest + the adversarial
readout review, both retained. Recorded loudly so the departure from the 25–29 spawn
convention is visible, not silent — and it is a persona-round process choice within brief
§4 latitude, **not** a HUMAN-QUEUE escalation.

### GA-2 — Classification of the three v2.6 evidence cases (the load-bearing calibration decision)

**Decision: the classification is already FORCED by the committed harness wiring —
Phase 30 CONFIRMS it live, it does not re-decide it.** Re-decoding a frozen corpus at the
terminal phase would be a D-13 violation (reshaping to a preferred outcome). The forced
classification:

| v2.6 case | Partition | Wiring (committed, Phases 27/28/29) | Promotes |
|---|---|---|---|
| `feature-origin-only-leak` | **ABSENT / miss** | `kind: miss`, `absent_code: DSX-ML-034`, `_EXPECTED_CAUGHT_DEFECTS`=∅, `_EXPECTED_VAL_CODES`=∅ | §6.5 item 7 |
| `magnitude-without-computed-effect` | **ABSENT / miss** | `kind: miss`, `absent_code: DSX-CLM-034`, `_EXPECTED_CAUGHT_DEFECTS`=∅ | §6.5 item 8 |
| `subgroup-harm-without-disposition` | **PRESENT / target** | `kind: target`, `_TARGET_DEFECT_CODES`={plan/verify/ship: DSX-COH-041}, `_GOLDEN_SHIP_FINDINGS`⊇{DSX-COH-041} | §6.5 item 9 |

**Consequences to confirm at measurement (S6-3), not to argue now:**
- **Miss partition = 5** (2 new + the 3 Phase-12 misses) **≥ floor 3** → floor holds;
  the invariance proof (injecting a synthetic target-present case leaves the headline
  byte-identical, D-10) stays green.
- **Headline miss-rate stays a construction invariant** (D-10 / 12-READOUT F3): the
  ABSENT partition is *curated* to be misses (each sidecar `kind: miss`), so miss-rate =
  1.0 = 5/5 by construction — it carries **no** sampling information about a miss
  propensity. The evidential content is the **per-case `fires_at_any_severity: false`
  confirmations** for the two NEW misses (DSX-ML-034 and DSX-CLM-034 genuinely silent at
  every severity across all four gate points, mirroring the Phase-27/28 measurements) —
  *not* the aggregate 1.0. The readout states this explicitly, as 12-READOUT §1 did.
- **PRESENT partition gains one target cell**: DSX-COH-041 must fire CRITICAL at
  plan/verify/ship on `subgroup-harm-without-disposition` (the honest inverse of the two
  misses). This is the honest catch metric; the corpus now demonstrates *both* a real
  closed catch minted from the paper's own §6 idea **and** two attributed misses.
- **FPR re-measured over 15 good-control specs** (denom 12 → 15); re-state the one-sided
  95% upper confidence bound on 0/15 (Clopper-Pearson `1 − 0.05^(1/15) ≈ 0.181`;
  rule-of-three ≈ 3/15 = 0.20) — do **not** quote it as a point estimate of a near-zero
  rate.

### GA-3 — The two required doc rewrites (REQ-P30-01, under the D-13 measured-evidence rule)

**Decision.** Both rewrites are **D-13-honest**: each item is promoted with its code and
fixture **named** and its measured LIVE-MISS / TARGET evidence cited, or carried with the
measured reason — never a promotion on an estimate.

1. **`brief.md §6.5`:** the item-7/8/9 entry rows (`:376–378`) and re-evaluation bullets
   (`:421–437`) are already rewritten by the evidence-phase executors — Phase 30
   **verifies they match the measured re-baseline** (items 7 & 8 as attributed misses
   promoting the backlog; item 9 as a PRESENT/DETECTED catch) and **refreshes the stale
   calibration-backdrop paragraph** (`:439–445`) to the Phase-30 numbers: the re-measured
   headline pair, FPR over **/15**, and the **5-miss** partition, with a dated "Phase 30
   re-evaluation" note so the durable record shows the terminal re-baseline (the paragraph
   currently still reads the Phase-12 "twelve-spec / 3-miss / miss-rate 1.0" backdrop).
2. **`docs/literature/the-ai-data-scientist.md`:** move items 7/8/9 **out of** the "What
   is deferred" table (`:81–88`) into a Satisfied disposition (code + fixture named, one
   line each: item 7 → `DSX-ML-034` / `feature-origin-only-leak` miss; item 8 →
   `DSX-CLM-034` / `magnitude-without-computed-effect` miss; item 9 → `DSX-COH-041` /
   `subgroup-harm-without-disposition` target); update the mapping-table corpus counts
   (row 15, `:43`: 39 → **42** known-bad; good-control stays **15**; and the count is now
   dated to the Phase-30 re-baseline); and flip the affected status cells (rows 7, 8:
   "provenance list deferred" / "residual deferred" → present as an attributed miss; row
   9 / row 12: subgroup-harm "gate deferred" → present as a catch via `DSX-COH-041`).

**No fixture, check, or catalogue edit** — these are record files. Exact line targets are
an S6-2 plan-research item (the files may shift by a few lines before S6-3 runs).

### GA-4 — REQ-P30-02 audit prerequisites: verify-not-build

**Decision.** REQ-P30-02 is a **verification** requirement, not a build: on the final
tree, on the **real 3.12.10 interpreter** from a clean tree, confirm — `gen-finding-catalogue.py
--check` exit 0 (catalogue current @ the live count); all frozen snapshots / count-pin
tests unmutated (`test_finding_catalogue_invariant`, `test_phase20_zero_mint_close`,
`test_p19_categorical_rows`, the example-profile digests); the doc/code agreement tests
green (`test_doc_code_agreement`, `test_selection_heuristic_docs`, and any doc↔code
agreement test touching the literature record); `node install.mjs --check` passes;
`scripts/check.sh` green; full suite green. **Author nothing new unless S6-2 research
finds a genuine gap** (e.g. no test asserts the literature record's corpus counts track
the live corpus). If a gap is found, Phase 30 closes exactly that gap and no more — no
speculative test. The known interpreter/tree hazards apply (stray root `DECISIONS.jsonl`
false-fails two `explain` tests; a bare `python3` stub reports the matplotlib determinism
test as skipped — use the real interpreter).

## 2. D-06 numbering note (loud, veto window — NOT escalated per brief §4)

Phase 30 **mints zero new finding codes.** The re-baseline routes entirely to existing
codes; the readout, the two record rewrites, and the audit-prerequisite verifications are
off-gate-path repo-integrity work. Target at S6-4: **set-identity 279 → 279, added={}
removed={}**, `gen-finding-catalogue.py --check` exit 0. **Re-measure the live count at
S6-2 plan time** (do not assume 279 has held since S5-5). Recorded loudly with the
standard silence = accept veto window; **not** escalated (D-06 numeric/zero-mint
assignments are persona-round decisions, brief §4).

## 3. Standing inputs carried in (not re-litigated)

- **The profiler is a producer, not a gate (D-01/D-02).** No computation on the gate
  path; Phase 30's measurement runs **off the gate path** in a read-only companion, and
  the reproducing gate is a unittest that shells `dsx gate` in a tempdir — it never adds
  gate-path computation.
- **The headline is the pair (miss-rate, FPR), never catch-rate alone (D-10).** Every
  target-present fixture carries a firing code, so a single catch-rate headline is a
  regression-pin dressed as detection; the ABSENT partition is floored and an invariance
  proof guards it. Carry this framing verbatim into the readout.
- **Miss-rate is a construction invariant of a curated partition (12-READOUT F3),** and
  a curated corpus is **not** a random sample — the rates describe behaviour on these
  archetypes, not a base rate. Report the FPR upper bound; report **no** interval on the
  miss-rate.
- **`dsx/checks/dq.py`, `dsx/cli.py`, `dsx/checks/viz.py` and every corpus fixture stay
  byte-frozen.** Phase 30 measures the corpus; it does not reshape it. Reshaping a frozen
  case to move a number is a D-13 violation and a finding in itself (D-14).
- **Ship discipline is S7, not S6.** Phase 30 is the last *build/measure* phase; the
  merge-to-`main` + `v2.6.0` tag are S7-6 (explicit-name direct merge; never the
  framework's alphabetical `gsd/*` auto-detect — six stale `gsd/*` branches would be
  picked instead).

## 4. Pre-staged for S6-2 (plan-checker-verifiable)

| REQ | Deliverable | Reuse anchor | Open plan-research question |
|---|---|---|---|
| P30-01 | `30-READOUT.md` (headline pair + stratified PRESENT/ABSENT + FPR /15 + per-family friction + limits + adversarial Statistician review) measured LIVE over the 42+15 corpus; read-only `_measure_readout.py` companion; durable reproducer = `test_stratified_catch_rate_and_fpr_report` | `12-READOUT.md`; `.../12-calibration/_measure_readout.py`; `tests/test_known_bad_corpus.py` live functions | Does `_measure_readout.py` copy forward cleanly against the current harness API (`_classify_target_defect`, `_effective_target_map`, `_headline` signatures, the `kind: target` path added in Phase 29)? |
| P30-01 | Refresh `brief.md §6.5` calibration backdrop (`:439–445`) to the measured Phase-30 numbers + a dated re-evaluation note; verify item-7/8/9 rows/bullets match the re-baseline | `brief.md:376–378, 421–445` (executor-written) | Exact current line spans for the backdrop paragraph and the re-evaluation list (may shift; grep-anchor, don't hard-code) |
| P30-01 | Update `docs/literature/the-ai-data-scientist.md`: items 7/8/9 out of the deferred table (Satisfied, code+fixture named); row-15 corpus counts 39→42; status cells rows 7/8/9/12 | `docs/literature/the-ai-data-scientist.md:43, 81–88` | Is there a doc/code agreement test that pins the literature record's corpus counts or deferred-item list? (if yes it must move in lockstep; if no, is that the REQ-P30-02 gap to close?) |
| P30-02 | Verify: catalogue current @ live count, frozen snapshots/count-pins unmutated, doc/code agreement green, `node install.mjs --check`, `scripts/check.sh`, full suite — all on real 3.12.10 from a clean tree | `gen-finding-catalogue.py --check`; `test_finding_catalogue_invariant`; `test_doc_code_agreement`; `test_selection_heuristic_docs`; `install.mjs --check` | Does any existing test assert the literature record tracks the live corpus, or is that an uncovered agreement gap to close (and only that)? |
| P30-03 | Zero mint: set-identity **279 → 279** (re-measured live), added={} removed={} | `gen-finding-catalogue.py --check`; §2 D-06 note | Confirm 279 still holds at plan time (do not assume) |

**Next = S6-2 (Phase 30 plan; plan-checker must pass; opus/high per brief §3). The
adversarial Statistician readout review lands at S6-3/S6-4 per GA-1, against measured
numbers.**
