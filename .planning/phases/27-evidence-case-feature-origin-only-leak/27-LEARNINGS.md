---
phase: 27
phase_name: "Evidence case — feature-origin-only leak"
project: "gsd-dsx"
generated: "2026-09-10"
counts:
  decisions: 8
  lessons: 7
  patterns: 6
  surprises: 5
missing_artifacts:
  - "UAT.md"
---

# Phase 27 Learnings: Evidence case — feature-origin-only leak

## Decisions

### D-27-00 — Split the discuss into a citation-independent measurement portion and a citation-dependent mint portion
The S3-1 discuss was split: the case-shape design and the pass/fail rule (D-27-01/02) were settled and measured immediately, while the mint (Kaufman citation, docstring, active `DSX-ML-*` code) stayed PARKED on HQ-40 row 40b's human read. A persona round (AUDITOR + ARCHITECT, both YES) established that Kaufman attaches strictly to the docstring of a net-new check, not to the design/measurement path, so the block could be refined to its true object.

**Rationale:** Every check on the ml gate path is a spec-declaration check reading `model.*`/`results.*` — none inspect actual data — so the feature-origin defect is structurally invisible to the whole path regardless of citation status; measurement could proceed without waiting on the human read.
**Source:** 27-CONTEXT.md

### D-27-01 — Freeze the corpus case shape before any measurement (churn fixture, `account_health_index`)
The case shape — a churn-style fixture with an innocuously-named leaky column `account_health_index` that matches none of the 10 `LEAKAGE_PATTERNS`, recomputed nightly from activity that includes the outcome window, with every other declaration (temporal split, `preprocessing_fit_on: train_only`, both `train_score` and `test_score`, complete selection ledger, beaten baseline) honest — was frozen before measurement began.

**Rationale:** Once measurement begins, the shape is frozen; a no-miss outcome must be a valid recorded terminal, never a license to re-shape the case (the D-13 prohibition on post-hoc case tailoring).
**Source:** 27-CONTEXT.md

### D-27-02 — Pass/fail rule requires a swap-still-fires counterfactual to disqualify "incidental" codes
A code only counts as an incidental (non-catching) fire if it would still fire when the leaky column is swapped for an honestly-available one. If swapping stops the code firing, that code is a genuine catch (NO MINT). This rule is applied by literal code (a real swap-and-rerun), never by narrative relabeling.

**Rationale:** Prevents the failure mode of declaring a code "incidental" by assertion just to manufacture a live-miss result.
**Source:** 27-CONTEXT.md

### D-27-03 — DSX-ML-034 placed in the leakage-features family (03x), not the global-next slot
The live catalogue was re-measured at mint time (`grep 'DSX-ML-\d+' references/finding-codes.md`) to confirm 034–039 was a free gap in the 03x family; the global-next `DSX-ML-093` was considered and rejected because it would file a leakage check under the selection-ledger sub-family (090–092), wrong by family placement.

**Rationale:** Code numbering should reflect the check's semantic family, not just the next available global integer.
**Source:** 27-CONTEXT.md

### Kaufman citation recorded as "secondary-corroborated, primary PDF paywalled," never a first-hand read
After nine failed open attempts on the ACM primary PDF (logged verbatim in HQ-40), the operator judged secondary corroboration across three independent indexes sufficient to unblock the mint. The binding instruction: both the `# D-05: DSX-ML-034` marker and the check docstring must describe the citation this way and must not claim a first-hand PDF read or invent a locator.

**Rationale:** The loop's own D-13 measurement already proved the code gap independent of the citation; the citation only needed to be honestly sourced, not exhaustively verified, to unblock authorship.
**Source:** 27-CONTEXT.md

### `promotes_backlog_item` id corrected to the harness-frozen string, not the phase-name string
27-CONTEXT.md's §S3-1-CLOSE consequence 2 had instructed `6.5-item-7-feature-origin-only-leak`, but the frozen `_SECTION_65_ITEM_IDS` list in the committed harness fixes item 7's id as `6.5-item-7-feature-provenance`. The research stage caught this and the sidecar was written with the harness-valid id.

**Rationale:** The frozen harness is the fact; a document-vs-code discrepancy is resolved in favor of the committed code, not the planning doc, and the doc records the correction rather than silently overriding it.
**Source:** 27-RESEARCH.md, 27-CONTEXT.md (§S3-2-RESEARCH-CORRECTIONS)

### DSX-ML-034 ships in the catalogue, kept OUT of `_SECTION_65_BACKLOG_CODES`
Because DSX-ML-034 is minted (shipped), it must not appear in the backlog-reserved set — the harness's disjointness assertion (`_SECTION_65_BACKLOG_CODES ∩ catalogue == ∅`) would fail otherwise. It goes only in `_D05_ALLOWLIST_CODES` and the generated catalogue row.

**Rationale:** The "reserved in backlog" wording in the earlier PARKED-state notes described the pre-mint RESERVE-INACTIVE era and was superseded once minting happened; the sidecar still names DSX-ML-034 as the shipped `absent_code`.
**Source:** 27-CONTEXT.md, 27-RESEARCH.md

### WR-01 fix: broaden the HIGH branch so omitted/null/off-vocabulary `available_at` is never more permissive than an honest `unknown`
Code review found the original branch chain silently cleared any `available_at` value that wasn't one of the four recognized tokens — a missing key, a null, or a typo'd value all produced zero findings, while an analyst who honestly wrote `unknown` was flagged HIGH. The fix routed unattested values (missing, blank, null, or off-vocabulary) through the same waiver-suppressible HIGH path as `unknown`, while keeping the HIGH-first/CRITICAL-second `report.add` order so the catalogue row still renders CRITICAL.

**Rationale:** An analyst should never be able to evade the attribution check simply by leaving a field blank or misspelling it; honesty should not be penalized relative to omission.
**Source:** 27-REVIEW.md, 27-VERIFICATION.md

---

## Lessons

### A live miss can be a "positive clearance," not merely an absence of coverage
The `ml` check at `plan`/`execute` didn't fail to run on the leaky spec — it ran fully and explicitly cleared the leaky column: "7 features screened, no leakage patterns matched." This distinction (positive clearance vs. a check simply not firing) matters for correctly characterizing what kind of gap the entry condition documents.

**Context:** The measurement table showed exit 0 at `plan`/`execute` with the `ml` check's own passed-checks list naming the leaky column as clean.
**Source:** 27-MEASUREMENT.md

### Declaration-only checks buy attribution, not detection — a spec that lies or omits still passes
This is a standing, explicitly acknowledged limit on the whole `model.feature_provenance[]` mechanism: DSX-ML-034 only fires on a self-incriminating declaration. A spec that never declares the block, or declares it falsely, sails through untouched. This was treated as an accepted design boundary, not a defect, throughout planning and review.

**Context:** Repeated in the PARKED design notes, the research doc's check-placement section, and confirmed candid (not a crippled-to-fake-a-miss design) by code review.
**Source:** 27-CONTEXT.md, 27-REVIEW.md

### Doc-vs-harness discrepancies surface cheaper in a dedicated research pass than at execution time
The S3-2 research stage read the frozen harness and found two authoring-detail conflicts with the prior context doc (`promotes_backlog_item` id; backlog-set placement) before any code was written, and recorded them as binding corrections rather than letting execution trip on them.

**Context:** Both corrections were verified against committed code, not assumed, and neither touched the frozen case shape or pass/fail rule (guardrail 1 stayed intact).
**Source:** 27-RESEARCH.md, 27-CONTEXT.md

### Minting one finding code at two severities collides with a one-code-one-row catalogue generator
DSX-ML-034 needed two literal-severity `report.add` sites (CRITICAL for `after_prediction`, HIGH for unwaived `unknown`), but the catalogue generator dedupes by code and keeps only the last-seen row. The plan had to explicitly arrange source order so the committed row rendered CRITICAL, then verify by regenerating and grepping the rendered severity.

**Context:** No existing catalogue code had previously been emitted at two severities — this was a novel case flagged as an open risk in research and resolved during execution.
**Source:** 27-RESEARCH.md, 27-01-SUMMARY.md

### A "first shipped-code miss sidecar" makes the falsifiability test actually exercise the live gate
All three prior miss sidecars named unshipped backlog codes, which are trivially absent from a live run. DSX-ML-034 is the first case where a shipped, catalogued code is used as a `kind: miss` `absent_code` — the falsifiability test genuinely runs the gate and requires the code to stay silent CRITICAL on the fixture, which only holds because the fixture declares no `feature_provenance` block.

**Context:** Flagged as a distinct risk category in research (RISK 4) precisely because it changes the strength of what the falsifiability assertion proves.
**Source:** 27-RESEARCH.md, 27-REVIEW.md

### Full-suite and cross-file count pins can hide outside the set enumerated by research
Research named two catalogue count pins beyond the catalogue file itself; a third live-total pin in `tests/test_p19_categorical_rows.py`, self-documented as "kept in lockstep" with the invariant test, was not named anywhere and only surfaced when the full suite was run and failed at 277 != 276.

**Context:** Recorded as a Rule 3 blocking auto-fix during execution rather than a plan defect, since the pin's own comment mandated the lockstep move.
**Source:** 27-01-SUMMARY.md

### A docstring claim of "membership test" can diverge from what the code structurally performs
The DSX-ML-034 docstring asserted the check performs "a membership test... against that closed vocabulary," but the actual branch logic performed selected-member equality with no terminal `else` — meaning out-of-vocabulary values were silently dropped rather than flagged as unattested. Code review treated this gap between documented intent and actual control flow as load-bearing enough to warrant a MEDIUM finding, not just a wording nit.

**Context:** Surfaced only by a deep code review that read the full function in context rather than trusting the docstring or the SUMMARY files.
**Source:** 27-REVIEW.md

---

## Patterns

### FREEZE-BEFORE-MEASURE: lock case shape and pass/fail rule before the first live measurement
D-27-01 (case shape) and D-27-02 (pass/fail rule) were written and frozen in the context doc before any gate was run against the fixture. Any post-measurement edit to either would void the phase. A no-miss outcome is declared a valid, honest terminal state up front, removing the incentive to reshape a case after seeing an unfavorable result.

**When to use:** Any phase whose deliverable is contingent on a measured outcome (a corpus case that may or may not be "caught") — freeze the falsifiable design and the interpretation rule before running the measurement that will judge it.
**Source:** 27-CONTEXT.md

### Split a decision along its true dependency boundary rather than blocking the whole unit
Rather than blocking the entire S3-1 discuss on the Kaufman human read, the orchestrator identified exactly which artifact the citation attaches to (the mint's docstring) and let everything else proceed. This is a re-scope of the block's object, recorded loudly with a veto window rather than escalated as a new decision.

**When to use:** When a single external dependency (a human read, an API confirmation, etc.) threatens to block a multi-part unit, check whether the dependency truly gates every part or only a downstream artifact.
**Source:** 27-CONTEXT.md

### Incidental-fire watch list: pre-register expected swap-invariant fires and how to clear them honestly
Before measurement, the phase pre-registered which codes were expected to fire incidentally (DSX-ML-060/061 train/test gap, DSX-ML-053 margin-over-baseline, DSX-ML-080 calibration) and the honest way to clear each (real numbers, not omitted fields or fudged fold scores) — explicitly forbidding relabeling a code that flags the leak as "incidental" just to force a miss.

**When to use:** Any adversarial-fixture design where some check fires for reasons unrelated to the target defect — enumerate and pre-clear those fires before measuring, so post-hoc rationalization isn't needed.
**Source:** 27-CONTEXT.md

### Corpus fixture promotion: sibling-convention files wired into glob-discovered harness maps with key-parity enforcement
A known-bad fixture is promoted as a basename-matched set (ANALYSIS-SPEC.yaml, entrypoint.py, POSTMORTEM.md, optional ATTRIBUTION.yaml sidecar) and registered in several glob-discovered maps (`_EXPECTED_CAUGHT_DEFECTS`, `_EXPECTED_VAL_CODES`, `_GOLDEN_SHIP_FINDINGS`) whose key-parity tests fail loudly if any entry is missing.

**When to use:** Adding any new fixture to a corpus-style test harness that enforces fixture-to-map correspondence — follow the existing sibling naming/file convention exactly and expect several count pins to move together.
**Source:** 27-RESEARCH.md

### TDD RED/GREEN for a new declaration-only finding-code check, with the D-05 marker authored in the RED test
The unit test carrying the `# D-05: <code>` marker and the honesty phrase was authored first (and deliberately left failing/RED because the check didn't exist yet), then the check implementation was added to turn it GREEN, followed by a separate catalogue-regeneration task.

**When to use:** Minting any new finding code under a citation-honesty gate (D-05) — write the marker-bearing test before the check exists so the RED state proves the marker's honesty language predates the implementation.
**Source:** 27-01-PLAN.md, 27-01-SUMMARY.md

### Re-measure harness values live rather than transcribe them from a planning document
Golden ship sets and validity-frame codes for the promoted fixture were explicitly re-run against the live gate rather than copied from the measurement doc's predicted values; the plan instructed that a differing measured result must stop execution and be recorded, never silently overwritten.

**When to use:** Whenever a planning artifact predicts a value that a downstream execution step could instead measure directly — measure and compare, don't trust the earlier prediction as ground truth.
**Source:** 27-RESEARCH.md, 27-02-PLAN.md

---

## Surprises

### The leakage check positively cleared the leaky column rather than silently skipping it
At `plan`/`execute`, the `ml` check's passed-checks output explicitly read "7 features screened, no leakage patterns matched" — meaning the leaky `account_health_index` column was inspected and actively declared clean, not merely unexamined. This is a stronger (more concerning) form of miss than a check that simply doesn't run.

**Impact:** Strengthened the case that this is a genuine detection gap worth minting a check for, rather than a coverage gap that might be dismissed as "the check wasn't designed to look there."
**Source:** 27-MEASUREMENT.md

### A one-character omission was a bigger bypass than an honest "unknown" declaration
Code review found that leaving `available_at` off an entry, setting it to null, or typo'ing it (e.g., `after-pred`) produced zero findings, while writing the honest value `unknown` triggered a HIGH finding — inverting the incentive the check was designed to create.

**Impact:** Classified as a MEDIUM defect and fixed pre-ship (WR-01); without the fix, the mint would have shipped with a known one-token bypass of its central `unknown`→HIGH attribution.
**Source:** 27-REVIEW.md

### An unnamed third count pin (`test_p19_categorical_rows.py`) only surfaced at full-suite run
Research and the plan named two catalogue count pins that needed to move 276→277; a third, self-documented as lockstep-bound to the invariant test, was not enumerated anywhere and only failed when the full suite ran during execution.

**Impact:** Treated as a Rule 3 blocking auto-fix rather than a plan failure, since the pin's own in-file comment mandated the move — but it shows research's "every count pin" claim had a gap.
**Source:** 27-01-SUMMARY.md

### The two-severity emission tripped an unanticipated "divergent declaration" pin test
Research explicitly checked for a test asserting zero generator warnings on the one-code-two-severities collision and found none — but a different test, `test_divergent_code_set_is_exactly_the_pinned_five`, pinned the exact set of codes with divergent (severity, title) pairs and had to be updated to include DSX-ML-034, a mechanism research's search hadn't surfaced.

**Impact:** Another Rule 3 blocking auto-fix during execution; underscores that "no test asserts X" checks need to search for adjacent/differently-named tests covering the same invariant.
**Source:** 27-01-SUMMARY.md

### The phase's own docstring overstated the check's rigor relative to its actual code
The check's docstring described itself as performing "a membership test... against a closed vocabulary," language that implies out-of-vocabulary values are handled (rejected/flagged); the actual code performed selected-member equality with silent fallthrough for anything unrecognized — a gap between self-description and implementation that only a deep code review caught.

**Impact:** Contributed directly to the WR-01 finding and fix; the docstring's overclaim (not on citation honesty, but on the check's own logical completeness) was corrected as part of the same edit.
**Source:** 27-REVIEW.md
