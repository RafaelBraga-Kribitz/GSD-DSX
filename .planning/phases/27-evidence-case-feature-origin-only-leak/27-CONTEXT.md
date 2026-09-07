---
phase: 27
phase_name: Evidence case — feature-origin-only leak
milestone: v2.6
unit: S3-1 (discuss + persona round)
status: partial — citation-independent design SETTLED; mint PARKED on HQ-40 Kaufman read
box_checked: false
requirements: [REQ-P27-01, REQ-P27-02, REQ-P27-03]
d05_burden: 1 (Kaufman 2012 TKDD — HQ-40 row 40b, UNVERIFIED)
codes_minted: 0
---

# Phase 27 — CONTEXT (feature-origin-only leak)

This document records the **citation-independent** portion of S3-1's discuss. Per the
persona round below, S3-1 is split: the case-shape design and the pass/fail rule are
SETTLED and FROZEN now; the mint (its D-05 Kaufman citation, docstring, and the active
`DSX-ML-*` code) stays PARKED on HQ-40 row 40b's human read. **The S3-1 checkbox stays
UNCHECKED** — see §5.

Three explicit states are used throughout: **SETTLED** (design + rule, frozen now),
**MEASURED** (the four-point verdict, produced by the next firing at S3-3), **PARKED**
(mint + citation, blocked on Kaufman).

## D-27-00 — Extract the citation-independent D-13 measurement spike ahead of the Kaufman read

**Decision (persona round, both YES; adopted by the orchestrator):** Phase 27's D-13
measurement is executed ahead of HQ-40 row 40b's human read. The S3-1 discuss is split
into a citation-independent design+measurement portion (proceeds now) and a
citation-dependent mint portion (stays blocked on Kaufman).

**Panel (brief §4; opus, parallel, grounded — no re-exploration):**
- **AUDITOR** (`dsx-ml-integrity-auditor`) → **YES.** Verified at `dsx/checks/ml.py`:
  *every* check on the ml gate path is a spec-**declaration** check reading `model.*`
  / `results.*` off the parsed spec — none open the warehouse extract, inspect actual
  feature values, or execute the entrypoint. The feature-origin defect (a column whose
  train-time value ≠ its prediction-moment value) lives in the **data**, not the spec,
  so it is structurally invisible to the whole path. Measurement dependency graph =
  {frozen fixture, existing gate} → measured codes; **Kaufman is nowhere in it** (ml.py
  cites Saito–Rehmsmeier at -043, Varma–Simon at -052/-053, Cawley–Talbot at -090/-092,
  **not** Kaufman). Kaufman attaches strictly downstream, to the docstring of a
  net-new check.
- **ARCHITECT** (`dsx-analysis-architect`) → **YES.** The Kaufman citation attaches to
  exactly one artifact — the docstring of the minted check produced at S3-3. Nothing in
  the S3-1 discuss *carries* the citation. The ledger's own block qualifier — "blocked
  until Kaufman *for the citation the code would carry*" — scopes the block to the
  mint's citation, not the design/measurement. Splitting **refines** the block to its
  true object; under the freeze discipline (§ guardrails) it *strengthens* D-13.

**Tie-break:** not needed — unanimous. (Had it been needed: rigour > reliability >
flexibility.)

**Classification (brief §4):** this is a re-scope of the *block*, not of a requirement.
REQ-P27-01/02/03 are unchanged. It is therefore a persona-round decision recorded
loudly with a **veto window** (silence = accept), **not** a HUMAN-QUEUE escalation.

## D-27-01 — The corpus case's exact shape (SETTLED, FROZEN before any measurement)

A churn-style known-bad fixture. **Once measurement begins this shape is frozen; a
no-miss outcome is a valid recorded terminal (no-mint close), never a licence to
re-shape the case — that is the D-13 prohibition.**

- **Entrypoint** reads a pre-joined warehouse extract. It splits **temporally**, fits
  the pipeline on the **training fold only**, and contains **no** cleaning step, **no**
  scaler-before-split, **no** test-sees-target idiom. Nothing in the code is a visible
  fit-call defect.
- **The leaky column:** `account_health_index` — an innocuous name matching **none** of
  the 10 `LEAKAGE_PATTERNS` (verified: cancel/churn, refund/chargeback/reversal,
  closed/resolved/settled, final/total/lifetime/ltv/cumulative, after/post,
  outcome/label/target/y_true/ground_truth, days/weeks/months_to_event, next_period,
  score/probability/pred, reason/cause_code). It is **recomputed nightly from activity
  that includes the outcome window**, so its value at training time is not the value
  that would exist at the declared prediction moment.
- **Honest declarations (all true):** `preprocessing_fit_on: train_only`; a temporal
  split; a `prediction_time_definition`; a `baseline` the model beats; a complete
  selection ledger; a plausible score. **`train_score` AND `test_score` are both
  declared honestly** — the fixture must NOT omit `train_score` (DSX-ML-060/061 return
  early when it is absent, `ml.py:1093`; omitting it to dodge them would be reshaping).
- Every declaration is honest. The defect is attributable **only** through feature
  origin — the exact §6.5 item 7 entry condition.

**Predicted outcome (NOT a substitute for measurement):** a live miss. A
name-pattern-plus-declaration gate cannot see data provenance. But D-13 forbids
assuming — the entry condition is decided by the *measured* four-point verdict, not by
this prediction.

## D-27-02 — Pass/fail rule for "live miss" (SETTLED, FROZEN, pre-registered)

Measured at **all four gate points** (plan / execute / verify / ship), from a **fresh
temp directory**, recorded **verbatim** before any interpretation.

- **CAUGHT ⇒ NO MINT, CLOSE PHASE (a valid success):** any existing check at any of the
  four points fires **on the merits of the target defect** — flags the
  temporal/outcome-window leak in the innocuous column by any mechanism (name match,
  fit-call, temporal-split, or other). §6.5 entry condition **not** met. Record the
  measured codes and write the no-mint record. This closes the phase and moots Kaufman.
- **LIVE MISS ⇒ ENTRY CONDITION MET:** all four points return a ship/pass verdict on the
  honest-but-leaky spec, and — after subtracting *documented incidental corpus-gap
  codes* — nothing flags the target leak.
- **"Documented incidental corpus-gap code" — the swap-still-fires counterfactual
  (applied by literal code, never narrative):** a blocking code counts as *incidental*
  (does not defeat a live miss) **only if** it would still fire when `account_health_index`
  is swapped for an honestly-available column — i.e. it concerns a *different* property
  (a schema nit, fixture plumbing, a missing-optional warning). If swapping the column
  **stops** the code firing, that code **is a catch** ⇒ NO MINT. It must **never** mean
  relabelling a code that flags the leaky column as "incidental" to force a miss.
- **Incidental-fire watch list (auditor — clear only HONESTLY, never by hiding):**
  - `DSX-ML-060/061` (train/test gap): a leak present uniformly across folds inflates
    train and test symmetrically → clears; but honest numbers showing test > train past
    threshold fire **061** = a documented catch. Do not omit `train_score`.
  - `DSX-ML-053` (margin-over-baseline < fold-score spread): a stable leak → small
    spread, large margin → clears. Do not fudge `fold_scores`.
  - `DSX-ML-080` (probability/threshold decision with no declared calibration): orthogonal
    to the leak; clear it by honestly declaring `calibration_method`/`calibration_error`,
    not by hiding probability use.

## D-27-03 — Reserved sidecar `absent_code` (D-06, RESERVE-INACTIVE; veto window OPEN now)

**Reserved: `DSX-ML-034`.** Live catalogue re-measured this firing (do not assume):
`grep 'DSX-ML-\d+' references/finding-codes.md` → the leakage/features sub-family
occupies **030–033** (a gap at **034–039**); the global family tops at **092**. A
`feature_provenance` / feature-availability check belongs to the **leakage-features
family (03x)**, so the next-free-**in-family** slot is `DSX-ML-034`. The global-next
`DSX-ML-093` was considered and **rejected** — it would file a leakage check under the
selection-ledger sub-family (090–092), wrong by family placement.

**RESERVE-INACTIVE:** `DSX-ML-034` is a *slot*, not a minted code. It is activated as the
sidecar's `absent_code` (reserved in `_SECTION_65_BACKLOG_CODES`, `promotes_backlog_item:
6.5-item-7-…`) **only if** the measurement confirms a live miss **and** the Kaufman read
clears the mint. **D-06 veto window opens now; silence = accept** (brief §4; the generic
"D-06 numbering veto windows" line already stands in HUMAN-QUEUE — this records the
specific number).

## PARKED — mint (blocked on HQ-40 row 40b, NOT written active pre-read)

None of the following is authored or minted before the human read (guardrail 2):

- The **D-05 Kaufman citation** and its docstring text — UNVERIFIED (HQ-40 40b).
- **`model.feature_provenance[]` field vocabulary — DRAFT-only:** `{feature, source,
  available_at, derived_from}`, with `available_at` on the closed vocabulary
  `before_prediction | at_prediction | after_prediction | unknown`; a declaration-only
  check firing CRITICAL when a feature is declared `after_prediction` and HIGH when
  `unknown` without a waiver. This buys **attribution, not detection** — a spec that
  lies still passes (the README's standing "a frame that lies passes" limit). Adopted
  **only if** the measurement confirms a live miss.
- The **active `DSX-ML-034` mint** (§ D-27-03).

## Guardrails (non-negotiable — from both personas)

1. **FREEZE-BEFORE-MEASURE.** D-27-01 (case shape) and D-27-02 (pass/fail rule) are
   frozen by this document *before* the first measurement. A no-miss outcome is a valid
   recorded terminal; it is **not** a licence to widen/weaken/re-shape the case. Any
   post-measurement edit to D-27-01/02 voids the phase.
2. **NOTHING KAUFMAN-ACTIVE PRE-READ.** No citation, docstring, or active `DSX-ML-*`
   code/check is written or minted before HQ-40 row 40b. `feature_provenance` = DRAFT;
   `absent_code` = RESERVED-INACTIVE.
3. **HARD STOP AT THE MINT BOUNDARY.** The S3-3 deliverable is the recorded four-point
   verdict. On a confirmed live miss, stop — do not author the check or its Kaufman
   docstring until the read completes.
4. **HONEST PARTIAL STATE.** S3-1 stays UNCHECKED (§5). Fresh isolated tempdir; existing
   gate unmodified; record every measured code (including incidental fires) verbatim at
   each of the four points before interpreting.

## §5 — What this unit did NOT do (honest partial state)

The **S3-1 box stays UNCHECKED.** S3-1 cannot reach checked on design alone: completion
requires either a **no-mint close** (measurement shows the case is caught) or the
**Kaufman read clearing the mint**. This firing settled the citation-independent design
(D-27-01/02), recorded the split decision (D-27-00) and the reserved slot (D-27-03), and
parked the mint. It did **not**: build the fixture, run any measurement, mint any code,
or sign the D-05 citation.

**Next firing (S3-3 measurement spike):** build the D-27-01 fixture and MEASURE it live
at the four gate points from a fresh tempdir, recording verbatim; apply the D-27-02 rule.
If caught → no-mint close (Phase 27 done, Kaufman moot). If a live miss → stop at the
mint boundary and hold for HQ-40 row 40b.
