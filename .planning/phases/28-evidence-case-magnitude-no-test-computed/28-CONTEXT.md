---
phase: 28
phase_name: Evidence case — magnitude no test computed
milestone: v2.6
unit: S4-1 (discuss + persona round)
status: SETTLED — design frozen (D-28-00..05); LIVE MISS to be MEASURED at S4-3 (execute measures first, D-13); D-05 citation resolved (HQ-40, Wilkinson & TFSI 1999 alone)
box_checked: true
requirements: [REQ-P28-01, REQ-P28-02, REQ-P28-03]
d05_burden: 1 (Wilkinson & TFSI 1999 — HQ-40 rows 40c/40d ANSWERED 2026-09-07: cite 40c alone, DROP JARS 40d)
codes_minted: 0 (DSX-CLM-034 reserved here; authored — if the miss is live — at S4-3, not S4-1)
---

# Phase 28 — CONTEXT (a magnitude no reported test computed)

This records S4-1's discuss. Per the §4 persona round below (Statistician + Architect,
opus, parallel, grounded in the check code), the case-shape design (D-28-01), the
pass/fail rule (D-28-02), the rounding tolerance (D-28-03) and the reserved code
(D-28-04) are SETTLED and FROZEN now. The **LIVE MISS is not yet measured** — that is
S4-3's first act (execute measures first, D-13). A no-miss outcome at S4-3 is a valid
recorded terminal (no-mint close), never a licence to re-shape this design.

Unlike Phase 27, the D-05 citation is already resolved (HQ-40 rows 40c/40d ANSWERED:
Wilkinson & TFSI 1999 alone, JARS dropped), so nothing here is PARKED on a human read.

Three states are used: **SETTLED/FROZEN** (design + rule, frozen now), **MEASURED**
(the four-point verdict, produced at S4-3), **RESERVED** (the code slot + veto window,
activated only on a confirmed live miss).

## D-28-00 — D-13 CORRECTION: the scope's literal case is CAUGHT by `DSX-CLM-033`; freeze the collision construction instead (SETTLED)

**The load-bearing finding of this discuss.** The V2.6-SCOPE.md §Phase 28 starting
proposal was a claim asserting "a magnitude on metric C that appears in **no** test."
Both personas, reading the code independently, found that case is **caught already** by
the existing `DSX-CLM-033` (CRITICAL, "Claim numbers do not overlap results.tests"):

- `DSX-CLM-033` = `_check_numeric_overlap` (`dsx/checks/claims.py:343-401`), dispatched
  per-claim (`claims.py:83`). It extracts the claim's %/pp/decimal literals
  (`_extract_claim_magnitudes`, `claims.py:404-436` — bare integers are **not**
  extracted, `:423-429`) and builds `reference` from the **union over ALL tests** of
  `{effect, effect×100, each CI bound, bound×100}` plus the claim's own `ci`
  (`claims.py:353-375`). A claim number fires CRITICAL **only if it matches no reference
  number** under `_close_enough` = rel ≤ 5% OR abs ≤ 5e-4 (`claims.py:381-383,439-443`).
- Therefore a claim quoting 27% / 18% for a metric **no test reports** → both numbers
  match nothing in the union → **`DSX-CLM-033` FIRES CRITICAL**. That case is a **NO-MINT
  close** (D-13), consistent with the brief's own item-8 prior ("carried; likely none —
  the paper-shaped instances already fire the per-test finding").

**The only honest LIVE-MISS seam** (both personas, independently): the claimed
magnitude's numbers are **real reported numbers of the WRONG metrics** — they coincide
(within `DSX-CLM-033`'s 5% window) with the reported effects / CI bounds of the tests
that *were* computed, so `DSX-CLM-033` clears with its **full logic exercised** (union
membership, not a skip), while **no test computed the claimed metric**. This is the
mislabelled-magnitude defect — an analyst quotes "churn at 27% vs 18%" where 27/18 are
in fact the effects of *other* metrics (a copy-from-the-wrong-row error), the single
commonest real-world magnitude defect. Nothing is hidden to dodge a check; only the
metric→number binding is absent, which `DSX-CLM-033` structurally never verifies (it is
metric-blind and reads no `supported_by`).

**This is a REFINEMENT driven by the measured behaviour of the existing check, NOT a
manufacture of a miss (D-13).** The collision case documents a *real* gap — `DSX-CLM-033`
checks number-membership globally, not per-metric binding — and is the realistic form
of item 8's defect. The scope's literal wording is preserved as the explicit **NO-MINT
control** shape: if S4-3 measures that shape, `DSX-CLM-033` catches it and the phase
closes clean.

## D-28-01 — The corpus case's exact shape (SETTLED, FROZEN before any measurement)

A churn-style, **descriptive / observational** known-bad fixture (descriptive question +
`design.kind: observational` keeps the causal-identification and `decision.replay`
obligations off the spec, so the miss stays clean; the Architect verified structured
`decision.replay` is required at ship only for experiment/causal/prescriptive designs
with tests). **Frozen now; a no-miss outcome at S4-3 is a valid terminal, never a
licence to re-shape.**

- **`results.tests[]` — two tests on OTHER metrics**, each clearing the stats reporting
  contract on the merits (`dsx/checks/stats.py:505-548,621-663`):
  - **A** `metric: revenue_per_user` — `effect`, two-bound `ci`, `p_value`,
    `effect_size_kind: d` (∈ `EFFECT_SIZE_KINDS={d,h,r}`, `dsx/mathx.py:296`),
    non-negligible `standardized_effect`, non-null `interpretation`.
  - **B** `metric: activation_rate` — same complete reporting shape.
- **One magnitude claim, typed `association`/descriptive** (no causal verbs → CLM-011/
  020/021 silent, `claims.py:104-149`):
  `"Customers holding fewer than two products churn at 27% against 18% for the rest of
  the book, over the 2026-Q2 window."` The claimed metric is **churn (metric C), which
  NO test computes.** The literals **27 and 18 coincide** (within `DSX-CLM-033`'s
  tolerance) with the reported numbers of tests A / B — the collision that clears
  `DSX-CLM-033` on its full logic (D-28-00). `base_n` declared; absolute percentages.
- **The corpus fixture declares NO `claims[].supported_by`.** This is the Phase-27
  precedent (the feature-origin fixture declared no `feature_provenance` block): the
  minted `DSX-CLM-034` is **declaration-gated**, so it stays **silent** on the fixture →
  the fixture remains an **honest MISS**. `DSX-CLM-034` buys **attribution, not
  detection** — a spec that omits the pointer still passes (the standing README "a frame
  that lies passes" limit). A separate positive-firing unit test (S4-2/S4-3) proves the
  check bites when `supported_by` *is* declared but does not cover the number.
- Every declaration is honest. The defect — a claimed magnitude no test computed —
  is attributable only through the missing claim→test traceability, the exact §6.5
  item 8 entry condition.

**Predicted outcome (NOT a substitute for measurement):** a live miss under the
collision construction. But D-13 forbids assuming — the entry condition is decided by
the *measured* four-point verdict at S4-3, not by this prediction.

## D-28-02 — Pass/fail rule for "live miss" (SETTLED, FROZEN, pre-registered)

Measured at **all four gate points** (plan / execute / verify / ship), from a **fresh
temp directory**, recorded **verbatim** before any interpretation (the
`tests/test_known_bad_corpus.py::_gate_findings` protocol). Note `claims` registers only
at **verify and ship** (`dsx/cli.py:123,128`), threshold HIGH (`:138-139`); `DSX-CLM-033`
is CRITICAL, so it blocks wherever it fires.

- **CAUGHT ⇒ NO MINT, CLOSE PHASE (a valid success):** any existing check fires **on the
  merits of the target defect** — flags that the claimed churn magnitude is not backed
  by any computed test, by any mechanism. Chief risk: `DSX-CLM-033` fires (the collision
  did not clear it). Record the measured codes, write the no-mint record, close the phase.
- **LIVE MISS ⇒ ENTRY CONDITION MET:** all four points return a ship/pass verdict on the
  merits, and — after subtracting *documented incidental corpus-gap codes* — nothing
  flags the uncomputed-magnitude defect.
- **"Documented incidental corpus-gap code" — the swap-still-fires counterfactual
  (applied by literal code, never narrative), same rule as Phase 27:** a blocking code
  counts as *incidental* **only if** it would still fire when the claim's collision
  numbers are swapped for numbers that genuinely appear in the cited test — i.e. it
  concerns a *different* property (a schema nit, fixture plumbing, a missing-optional
  warning). If the swap **stops** the code firing, that code **is a catch** ⇒ NO MINT.
- **Existing checks that MUST clear on the merits (persona-verified locators — clear
  HONESTLY, never by omission):**

| Check | Locator | Clears honestly because |
|---|---|---|
| `DSX-CLM-033` CRITICAL | `claims.py:343-401` | union membership: 27,18 present via test A/B (±5%, ×100 bridge) — **the load-bearing clearance (D-28-00)** |
| `DSX-CLM-070` HIGH | `claims.py:532-550`, `dsx/pct_base.py:56-72` | `base_n` declared → `claim_supplies_base` True |
| `DSX-NAR-040` MEDIUM | `narrative.py:82-93` | narrative body carries base language ("of 5,000 customers"/"n=5,000") — `base_n` does **not** help the body scan |
| `DSX-NAR-020` HIGH | `narrative.py:65-80` | claim text present (whitespace-normalised) in `narrative.path` |
| `DSX-STA-011/012` MEDIUM | `stats.py:621-663`, `mathx.py:296` | `effect_size_kind: d` recognised + non-negligible `standardized_effect` — STA-012 clears **on the merits, not by omitting the field** |
| `DSX-STA-002/003`, `020/021` | `stats.py:523-546,667-675` | each test reports effect + 2-bound CI; significant, non-null interpretation |
| `DSX-CLM-080` HIGH | `claims.py:553-573` | declare a one-line `limitations[]` |
| `DSX-CLM-050` MEDIUM | `claims.py:472-493` | avoid GENERALISATION_TERMS; state `population` |
| `DSX-CLM-030/031` | `claims.py:246-…` | `evidence:` points at the **committed** narrative |

## D-28-03 — Rounding-tolerance rule (SETTLED)

REQ-P28-02 fixes the **field**: `claims[].rounding` = number of significant figures,
**default 2** when absent. The comparison for the minted check: a claim literal `L`
reconciles with a cited-test number `T` iff they agree to `rounding` significant
figures, **applying the same percent/proportion ×100 scale bridge `DSX-CLM-033` already
uses** (`claims.py:360-368`) so a claim quoted in points reconciles with a test effect
declared as a proportion. `rounding` may *tighten* per claim, never loosen.

**Plan-gate carry (S4-2, recorded, not over-frozen):** the Statistician flagged that a
sig-figs tolerance can be *tighter* than `DSX-CLM-033`'s rel-5%/abs-5e-4 window — which
is intended (`DSX-CLM-034` is stricter, against the *cited* test only). S4-2 must confirm
the two never double-code the **same** number against the **same** test on the shipped
fixture; they cannot on the corpus fixture (it declares no `supported_by`, so
`DSX-CLM-034` is silent there), and the positive-firing unit test measures both codes
live rather than assuming.

## D-28-04 — Reserved code `DSX-CLM-034` (D-06, RESERVED; veto window OPEN now)

**Reserved: `DSX-CLM-034`.** Live catalogue re-measured this firing (do not assume):
`references/finding-codes.md` **Total: 277** (Phase 27's `DSX-ML-034` landed); the
`DSX-CLM` family occupies 001, 01x (causal-verb), 02x (identification), **03x
evidence-pointer/overlap** (030 no-pointer, 031 unresolved, 032 anchor-absent, **033
CRITICAL numeric-overlap-with-results.tests**), 04x (predictive), 050, 060, 070, 080;
`grep -c DSX-CLM-034 references/finding-codes.md` → **0** (free). A claim→cited-test
numeric-traceability check is the direct refinement of 033 (union → cited test) and a
traceability sibling of 030–032, so it belongs in **03x**; the next-free-**in-family**
slot is **`DSX-CLM-034`** (033 → 040 leaves 034–039 open). Both personas reached 034
independently. The global-next `DSX-CLM-090`+ was rejected — wrong family placement.
(No collision with Phase 27's `DSX-ML-034`: different family prefix.)

**RESERVED, not minted:** `DSX-CLM-034` is a *slot*, activated as the sidecar's
`absent_code` (kept OUT of `_SECTION_65_BACKLOG_CODES` once shipped; `promotes_backlog_item:
6.5-item-8-magnitude-without-computed-effect` — the frozen `_SECTION_65_ITEM_IDS` member
at `tests/test_known_bad_corpus.py:853`, verified this firing, NOT the phase slug) **only
if** S4-3 measures a live miss. **D-06 veto window opens now; silence = accept** (brief §4;
the generic "D-06 numbering veto windows" line already stands in HUMAN-QUEUE — this
records the specific number).

## D-28-05 — D-05 citation honesty: Wilkinson & TFSI (1999) is the MOTIVATING PRINCIPLE, not the mechanism (SETTLED)

HQ-40 rows 40c/40d ANSWERED (2026-09-07): cite **Wilkinson, L. & the Task Force on
Statistical Inference (1999), American Psychologist 54(8):594–604 ALONE**; JARS-Quant
(40d) DROPPED (weaker/hedged wording, and only the 2024 web table was reachable).
Wilkinson was read in full primary text and states the rule unconditionally ("Always
present effect sizes for primary outcomes"; "Always provide some effect-size estimate
when reporting a p value"; "Interval estimates should be given for any effect sizes
involving principal outcomes").

**Honesty constraint (binding on the S4-3 docstring + `# D-05:` marker), per the
Statistician:** Wilkinson mandates *reporting* effect sizes and intervals for primary
outcomes. The minted check enforces a **declaration-level traceability corollary** — a
claim's headline magnitude must trace to the *specific cited test* (a text-to-declared-
number overlap, the `DSX-REP-061` precedent, never a recomputation). The docstring MUST
cite Wilkinson & TFSI (1999) as the **principle that motivates** the check and state
plainly that the check enforces the traceability corollary, **not** the literal
"report an effect size" rule. Do not claim Wilkinson mandates the overlap mechanic.

**Bounded-catch honesty (record in the docstring too):** even `DSX-CLM-034` catches the
collision case only via the **stray** number (e.g. the `18` that sits outside the cited
test), not via metric-identity — a claim whose *both* numbers happened to sit in the one
cited test would still pass. The check closes "a claim number absent from the cited
test," not "the cited test measures the wrong metric." This bounds the D-13 claim
honestly, mirroring Phase 27's "buys attribution, not a catch."

## Declaration vocabulary + severity direction (PLAN INPUTS for S4-2 — recorded, not over-frozen)

The S4-1 unit settles the four items above; the exact check internals are refined at
S4-2 (plan) against the REQ-P28-02 text and confirmed by the S4-3 live measurement.
Recommended by the round:

- **`claims[].supported_by`** — a **string** = the `metric` value of the `results.tests[]`
  entry the claim rests on (a list tolerated → union of those tests' numbers). Additive,
  opt-in, consistent with the frozen claims schema's existing optional keys
  (`templates/ANALYSIS-SPEC.yaml:299-308`). Absent → the check is silent (the DSX-ML-034 /
  DSX-REP-06x declaration-gated pattern).
- **`claims[].rounding`** — int significant figures, default 2 (D-28-03).
- **Severity (recommendation, S4-2 to finalise against REQ-P28-02's exact text):** the
  round leans **HIGH**, sitting `DSX-CLM-034` in the 030–032 traceability tier (all HIGH)
  and reserving CRITICAL for `DSX-CLM-033`'s fabrication-grade "matches nothing anywhere"
  — a legible severity ladder, non-overlapping with 033 by construction (034 is
  `supported_by`-gated; 033 reads no `supported_by`). At verify/ship the threshold is
  HIGH, so HIGH loses no enforcement. The scope proposed a two-tier HIGH/CRITICAL; S4-2
  reconciles the final severity and confirms non-overlap by live measurement, not by
  argument.
- **Harness wiring names (for S4-2):** fixture slug `magnitude-without-computed-effect`
  (distinct from the existing `chart-takeaway-without-magnitude` fixture, verified);
  `_EXPECTED_CAUGHT_DEFECTS[...] = frozenset()`; `_EXPECTED_VAL_CODES[...] = set()`;
  golden ship ledger entry = **measured-live**, never guessed; spec count
  `tests/test_dsx.py` 43 → 44; catalogue `_EXPECTED_TOTAL` 277 → 278 + `references/
  finding-codes.md` row + `_D05_ALLOWLIST_CODES` entry (all conditional on a live miss).

## Guardrails (non-negotiable — from both personas, mirroring Phase 27)

1. **FREEZE-BEFORE-MEASURE.** D-28-00/01/02/03 are frozen by this document *before* the
   S4-3 measurement. A no-miss outcome is a valid recorded terminal; it is **not** a
   licence to widen/weaken/re-shape the case. Any post-measurement edit to the frozen
   design voids the phase.
2. **NOTHING MINTED PRE-MEASUREMENT.** No `supported_by`/`rounding` vocabulary is shipped,
   no `DSX-CLM-034` check/docstring is authored, and the code is RESERVED-INACTIVE until
   S4-3 confirms a live miss. (The D-05 read is already resolved, so — unlike Phase 27 —
   nothing is parked on a human.)
3. **HARD STOP AT THE MINT BOUNDARY.** S4-3's first deliverable is the recorded four-point
   verdict. On a confirmed live miss, author the vocabulary + check + Wilkinson docstring
   + `DSX-CLM-034`; on a catch, write the no-mint record and close.
4. **HONEST MEASUREMENT.** Fresh isolated tempdir; existing gate unmodified; record every
   measured code (including incidental fires) verbatim at each of the four points before
   interpreting; apply the swap-still-fires counterfactual by literal code.

## §5 — What this unit did NOT do

S4-1 settles and freezes the **design** (D-28-00..05) from the §4 persona round; the D-05
citation is resolved. It did **not**: build the fixture, run any measurement, ship any
vocabulary, mint any code, or write the check. **The LIVE MISS is unmeasured** — that is
S4-3's first act (execute measures first, D-13). The S4-1 box is CHECKED because its
deliverable — the settled, frozen CONTEXT with the four required settlements (claim text +
test roster; existing checks to clear; rounding tolerance; reserved number) — is complete
and the citation block is cleared.

**Next: S4-2** (plan the mint conditional on the live miss; plan-checker must pass) →
**S4-3** (measure first at the four gate points; if live miss → author vocabulary + check
+ Wilkinson docstring + `DSX-CLM-034` + harness + sidecar; else the no-mint record) →
**S4-4** review → **S4-5** secure/validate.

## §4 persona round record (Statistician + Architect, opus, parallel, grounded)

- **STATISTICIAN** → the scope's literal "appears in no test" case is CAUGHT by
  `DSX-CLM-033` (union set-membership, `claims.py:343-401`); the only honest live-miss is
  the collision/mislabel construction; reuse `DSX-CLM-033`'s scale semantics for the
  comparison; Wilkinson is the motivating principle, not the mechanism; the minted check
  catches via the stray number, not metric-identity (bounded honesty). Verdict:
  mint-plausible under the collision shape, no-mint under the literal shape — the S4-3
  measurement decides.
- **ARCHITECT** → `DSX-CLM-033` is union-scoped and `supported_by`-blind, so `DSX-CLM-034`
  (per-cited-test, declaration-gated, DSX-REP-061 mould) is genuinely distinct;
  `DSX-CLM-034` is next-free-in-03x-family; additive `supported_by`(string)+`rounding`(int
  sig-figs) vocabulary; fixture is a MISS with no `supported_by` (attribution not
  detection); severity HIGH in the traceability tier. Verdict: LIVE-MISS-plausible → mint
  path, conditional on the S4-3 measurement; NO MINT record-only if `DSX-CLM-033` fires.
- **Tie-break (rigour > reliability > flexibility):** the two agreed on every load-bearing
  point (collision construction, `DSX-CLM-034`, declaration-gated fixture, Wilkinson-as-
  principle). The one divergence — comparison tolerance (Statistician: reuse 033's
  rel-5%/abs-5e-4; Architect: sig-figs per REQ-P28-02) and severity (Statistician: two-tier
  HIGH/CRITICAL per scope; Architect: single HIGH) — resolved by **rigour**: keep the
  REQ-P28-02 sig-figs *field* (the requirement is binding) with the ×100 scale bridge, and
  lean HIGH for a legible ladder non-overlapping with 033; both flagged to S4-2 for final
  reconciliation against the requirement text and the live measurement, not decided by
  argument alone.
- **Classification (brief §4):** these are persona-round decisions recorded loudly with a
  veto window (the D-06 number), NOT HUMAN-QUEUE escalations. REQ-P28-01/02/03 unchanged;
  the D-28-00 shift from the scope's literal wording to the collision construction is a
  refinement of the *case*, driven by the measured behaviour of an existing check, within
  the same requirement — not a scope change.
