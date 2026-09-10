---
phase: 29
phase_name: Evidence case — subgroup harm under a prescriptive recommendation
milestone: v2.6
unit: S5-1 (discuss + persona round)
status: SETTLED — design frozen (D-29-00..05); LIVE MISS to be MEASURED at S5-3 (execute measures first, D-13); D-05 citation resolved (HQ-40 row 40e, Gail & Simon 1985 CONFIRMED); one REQ half-met pending research (REQ-P29-02 documented public failure case — S5-2 deliverable)
box_checked: true
requirements: [REQ-P29-01, REQ-P29-02, REQ-P29-03]
d05_burden: 1 remaining (Gail & Simon 1985 CONFIRMED at HQ-40 row 40e 2026-09-07; the documented public failure case is a phase-research read, not yet found — S5-2)
codes_minted: 0 (DSX-COH-041 reserved here; authored — if the miss is live AND the case source is found — at S5-3, not S5-1)
---

# Phase 29 — CONTEXT (subgroup harm under a prescriptive recommendation)

This records S5-1's discuss. Per the §4 persona round below (Architect
`dsx-analysis-architect` + Statistician `dsx-statistician`, opus, parallel, each
grounded independently in the check code), the harness-polarity correction (D-29-00),
the segment-floor declaration (D-29-01), the case shape (D-29-02), the disposition
vocabulary + severity (D-29-03), the reserved code (D-29-04) and the D-05 honesty
boundary (D-29-05) are SETTLED and FROZEN now. The **LIVE MISS is not yet measured** —
that is S5-3's first act (execute measures first, D-13). A no-miss outcome at S5-3 is a
valid recorded terminal (no-mint close), never a licence to re-shape this design.

The Gail & Simon (1985) citation is already resolved (HQ-40 row 40e ANSWERED
2026-09-07 — read directly at PubMed, PMID 4027319), so the enforcement definition is
not parked on a human. **One requirement is only half-met pending research:** REQ-P29-02
needs, in addition to the citation, *one documented public case where an average benefit
masked subgroup harm, found with a primary source*. That case is an S5-2 research
deliverable; "not found" is a valid recorded outcome that keeps item 9 on the backlog
with the half-met condition stated.

Three states are used: **SETTLED/FROZEN** (design + rule, frozen now), **MEASURED**
(the four-point verdict, produced at S5-3), **RESERVED** (the code slot + veto window,
activated only on a confirmed live miss AND a confirmed case source).

## D-29-00 — Harness-polarity correction: this fixture is a pre-mint LIVE MISS that becomes a post-mint TARGET, not a Phase-27/28 permanent miss (SETTLED — the load-bearing finding of this discuss)

**State this loudly for S5-2; it diverges from the mirrored Phase-27/28 pattern and is
FORCED by REQ-P29-03, not chosen.**

Phase 27 (`feature_provenance`) and Phase 28 (`supported_by`) minted checks that are
**declaration-gated on an opt-in pointer the honest fixture omits**, so each fixture
stays a *permanent* miss (`kind: miss`, `absent_code`, "attribution not detection"). The
minted check never fires on the honest fixture.

Phase 29 is structurally different. REQ-P29-03 fixes the check as **"missing row →
CRITICAL"**: the check fires on the *absence* of a `decision.subgroup_harm[]` row given
the *presence* of an opposing segment. The opposing segment is already declared in
`results.segments[]` (the same input `_check_simpsons_paradox` reads, `metrics.py:298`) —
there is **no opt-in pointer to omit**. Therefore, once `DSX-COH-041` ships, it **fires
CRITICAL on the honest fixture** — the defect is genuinely *detected*, not merely
*attributed*. You cannot make this check pointer-gated without defeating the requirement.

**Consequence for the harness (flag to S5-2, do not over-freeze):** the Phase-29 fixture
wires as a **TARGET**, not a `kind: miss` sidecar — `_EXPECTED_CAUGHT_DEFECTS[slug]`
carries `DSX-COH-041` (target map at the CRITICAL threshold points plan/verify/ship),
like a normal caught known-bad, **not** `frozenset()` + an `absent_code` sidecar. The
`absent_code`/`promotes_backlog_item` miss machinery (Phase 27/28) does **not** apply to
a defect the minted check catches; §6.5 item 9 is promoted by minting the code and the
Phase-30 §6.5 row rewrite records it as PROMOTED — DETECTED (present partition), not an
attribution-only miss.

**Watch item S5-2 MUST verify, not assume:** converting item 9 to a *present* (caught)
case means it does **not** add to the ABSENT partition. `_ABSENT_PARTITION_FLOOR = 3`
(`tests/test_known_bad_corpus.py:993`, asserted `:2071/:2129/:2174`) must still hold from
the pre-existing misses (Phase 27 `feature-origin-only-leak`, Phase 28
`magnitude-without-computed-effect`, plus earlier misses). A NEW target fixture subtracts
nothing from the existing miss set, so the floor is expected to hold — but S5-2 measures
it, does not assume it.

**D-13 is unaffected.** The **pre-mint** four-point measurement (S5-3, against a gate
with no `DSX-COH-041`) is still a clean LIVE MISS — that is what licenses the mint.
D-29-00 only fixes what the fixture *becomes* after the mint.

## D-29-01 — The segment floor's declaration (SETTLED)

**Field:** `decision.subgroup_harm_floor` — a non-negative **integer** absolute n, in the
`decision` block, co-located with `subgroup_harm[]` (both are decision-level obligations,
both sit in the DSX-COH 04x tier, cf. 040). Exact field name (`subgroup_harm_floor` vs
`subgroup_harm_floor_n`) finalised at S5-2 against the REQ-P29-03 text; the semantics
below are frozen.

**Semantics (declaration only — computes nothing; `dq.py` and the assertion vocabulary
stay byte-frozen):** a `results.segments[]` entry whose declared `effect` opposes
`results.overall_effect` (sign test **reused verbatim** from `metrics.py:311-314`,
`_sign(v) = (v>0)-(v<0)`, never recomputed) **and** whose declared `n ≥
decision.subgroup_harm_floor` requires a matching `decision.subgroup_harm[]` row. This is
the DSX-COH-040 mould ("enforced as a declaration").

**Default when absent = 0 (both personas, unanimous).** No escape by omission: to *not*
disposition an opposing segment, the analyst must **affirmatively declare a floor above
that segment's n** — a single auditable integer a reviewer can challenge, a
pre-registered "this cut is too small to act on." Omitting the floor makes the check
**maximally strict** (every declared opposing segment demands a disposition). A declared
floor may only **raise** the bar (tighten), never lower it — the D-28-03 "may tighten,
never loosen" precedent, applied to a floor.

**Rejected (recorded; S5-2 may revisit): declaration-gated-silent** (absent floor → check
silent), the strict Phase-27/28 mirror. Rejected as primary because it reproduces the
very gap §6.5 item 9 closes (escape by omitting the floor). That bound is *forced* for
DSX-CLM-034/DSX-ML-034 (they cannot detect without the pointer); it is **not** forced
here (DSX-COH-041 detects from `results.segments` alone), so the stronger default is
available and taken. Corpus-safety of default 0 is **verified, not assumed**: the trigger
requires `question_type == prescriptive`; every good-corpus spec is `causal` and the
existing known-bad `prescriptive-churn-recommendation` fixture is `descriptive` with no
`results.segments` → DSX-COH-041 is silent on every current corpus member except the new
fixture.

## D-29-02 — The four-segment case shape (SETTLED, FROZEN before any measurement)

**Slug:** `subgroup-harm-without-disposition` (house style "X-without-Y", cf.
`magnitude-without-computed-effect`; deliberately distinct from the existing
`prescriptive-churn-recommendation` fixture, whose targets are DSX-COH-001/010 —
verified `examples/known-bad/prescriptive-churn-recommendation-ANALYSIS-SPEC.yaml`).

**Construction — minimal-perturbation clone.** There is **no good `prescriptive` fixture
to clone** (verified: every `examples/good-corpus/` spec is `question_type: causal`), so
clone a causal+experiment good spec that already clears the full frame (SRM, stats,
`revisit_when` via experiment, assumptions, structured `decision.replay`), then:
(i) `question_type: causal → prescriptive`; (ii) retype the claim to `prescriptive`
(recommend the rollout); (iii) inject `results.segments[]` = **3 positive + 1 minority
opposing, all n above the declared floor**, positive `results.overall_effect`;
(iv) declare `decision.subgroup_harm_floor`; (v) **omit `decision.subgroup_harm[]`** — the
sole defect. Bumping causal→prescriptive adds no new frame surface (`needs_causal_block`
is already True for causal; revisit_when/assumptions/replay already cleared by the
experiment base). This is the deliberate **structural opposite** of
`prescriptive-churn-recommendation` (which keeps the question *descriptive* to make a
prescriptive *claim* an overreach → DSX-COH-001): here the question is genuinely
prescriptive and the claim clears the ceiling on the merits, so the only residual is the
undispositioned harm.

**Concrete numbers the Statistician sanity-checked (S5-2 may refine; the SHAPE is
frozen):** N = 10,000; metric = retention lift in pp (higher better); floor declared 500.

| Segment | n | effect | opposes overall? |
|---|---|---|---|
| A (high-value) | 4,000 | +5.0pp | no |
| B (mid) | 3,000 | +4.0pp | no |
| C (established) | 2,000 | +3.0pp | no |
| D (minority) | 1,000 | −6.0pp | **yes** |

n-weighted overall = (4000·5 + 3000·4 + 2000·3 + 1000·(−6)) / 10000 = **+3.2pp** (positive
→ "roll the bundle out to all at-risk accounts"). MET check: opposing 1 of 4 → `1==4`
False (030 silent), `1>=2` False (031 silent) — **the miss**, confirmed by the
arithmetic, not asserted. D is a material, decision-changing harm (−6pp on 10% of the
book, n=1000 ≫ the 500 floor), not noise — do **not** shave D toward n=2 or −0.1pp to
"clean it up" (that manufactures a trivial miss, D-13).

**Clear-table — every existing check the fixture must clear HONESTLY (persona-verified
locators; mirror 28-CONTEXT D-28-02):**

| Check | Locator | Clears because |
|---|---|---|
| DSX-COH-001 CRITICAL | `coherence.py:58-83` | claim `prescriptive` (4) ≤ question `prescriptive` (4) |
| DSX-COH-010 CRITICAL | `coherence.py:86-111` | fires only descriptive/diagnostic; prescriptive returns early — decision-rule verbs licensed |
| DSX-COH-020 CRITICAL | `coherence.py:114-146` | experiment: `minimum_practical_effect` + `action_if_null` declared |
| DSX-COH-030 / 031 | `coherence.py:197-253` | ≥1 assumption, each `checked: true` or waived (strict at verify/ship) |
| DSX-COH-040 CRITICAL | `coherence.py:149-194` | `revisit_when` discriminating + time-anchored |
| **DSX-MET-030 / 031** | `metrics.py:296-349` | **1 of 4 opposing: 1≠4 (030 silent), 1<2 (031 silent) — THE MISS** |
| decision-replay (`decision` family) | `decision.py:15-126`, registered verify/ship `cli.py:123,128` | structured `decision.replay` matches the prose rule on the **positive aggregate**; primary test significant so DSX-DEC-020/021 stay silent (`decision.py:92-122`) |
| stats DSX-STA-* | `stats.py` | primary test reports effect + 2-bound CI + p + `effect_size_kind` + `standardized_effect` + interpretation |
| claims DSX-CLM-011 / 020 | `claims.py` | prescriptive claim carries identification (randomization) |
| val / interference DSX-VAL-* / INT-* | `val.py`, `interference.py` | full clean causal frame inherited from the clone base |
| prereg DSX-PRE-* | `prereg.py` | declared `spec_id` or the DSX-PRE-020 suppression the sibling fixture already uses |
| narrative DSX-NAR-* | `narrative.py` | claim verbatim + base-n language in the body |

`results.overall_effect` MUST be declared (else MET *and* the new check return early,
`metrics.py:300`). Grep-confirmed: `results.segments` is consumed by **exactly one**
function in `dsx/` (`_check_simpsons_paradox`); `subgroup`/`subgroup_harm` appears nowhere
in `dsx/` — the gap is not covered elsewhere.

## D-29-03 — Disposition vocabulary + severity (SETTLED)

**`decision.subgroup_harm[]` = `{segment, effect, ci, n, disposition, rationale}`**,
`disposition ∈ {accept | exclude | mitigate}` (accept = proceed despite harm; exclude =
carve the segment out of the rollout; mitigate = apply a modified treatment). The `ci`
lives here (NOT on `results.segments[]`, which is `{name, effect, n}` — verified
`templates/ANALYSIS-SPEC.yaml:260`); it is the field that makes an `accept` credible, not
a trigger (see the trigger predicate below).

**One code, two severities (both personas — matches REQ-P29-03's singular "number"):**
- opposing segment ≥ floor with **no matching row** (matched by `segment` name) →
  **CRITICAL**;
- a matching **`accept` row with blank/missing `rationale`** → **HIGH**;
- (recommend, S5-2 to confirm against REQ-P29-03) an unknown `disposition` value or a row
  missing a required key → **CRITICAL** (no valid disposition = silence);
- `exclude` / `mitigate` without rationale → recommended, **not** required (self-justifying
  protective actions) — kept minimal per REQ-P29-03.

**Legibility.** The two firing conditions are per-segment mutually exclusive (row-absent →
CRITICAL, or `accept`-without-rationale → HIGH, never both), so the ladder stays readable.
Precedent inside the family: DSX-COH-030 is already one code at two severities (HIGH
non-strict / CRITICAL strict, `coherence.py:212-229`). Non-overlap with 001/010/020/040 is
by construction (each a distinct decision/claim obligation). On the corpus fixture the fire
is **CRITICAL** (missing row) → the CRITICAL falsifiability test
(`test_attribution_tags_are_falsifiable_against_live_gate`, harness `:1725`) is its live
falsifier (mirror D-28-06 guard 6). The HIGH branch (`accept`-without-rationale) needs a
**separate positive unit test** (a spec that declares an `accept` row with blank rationale).

## D-29-04 — Reserved code `DSX-COH-041` (D-06, RESERVED; veto window OPEN now)

**Reserved: `DSX-COH-041`.** Live catalogue re-measured this firing (do not assume):
`references/finding-codes.md` **Total: 278** (Phase 28's `DSX-CLM-034` landed); the
DSX-COH family occupies **001** (claim-type-exceeds-question), **010** (causal language
under wrong qtype), **020** (experiment block incomplete), **030/031** (assumptions),
**040** (decision.revisit_when missing) — verified `finding-codes.md:351-356`;
`grep -c DSX-COH-041` → **0** (free). The **04x tier is the decision-block-completeness
tier**: 040 is a required decision-level declaration for prescriptive/experiment
questions. `subgroup_harm[]` is the same *kind* of obligation — a required decision-level
declaration for prescriptive questions whenever a declared segment opposes — so it is a
direct **sibling of 040**; the next-free-**in-family/tier** slot is **`DSX-COH-041`**. This
follows Phase 28's own D-06 precedent (DSX-CLM-033 → 034 filled the 03x tier; the
global-next 090 was rejected as wrong placement).

**Tie-break recorded (rigour > reliability > flexibility).** The Architect voted
`DSX-COH-041` with the tier-placement argument above and explicitly rejected DSX-COH-050
(opens a new tier for a plain 04x decision obligation), DSX-COH-032 (03x is the
assumptions tier), and DSX-MET-04x (the obligation is decision-level and REQ-P29-03 fixes
DSX-COH-*). The Statistician named DSX-COH-050 only as "the natural next round number" and
**deferred final numbering to the D-06 veto window** — so there is no hard conflict; the
Architect's reasoned tier placement wins on rigour, and Phase 28's fill-the-tier precedent
confirms it.

**RESERVED, not minted:** `DSX-COH-041` is a *slot*, authored only if S5-3 measures a live
miss **and** REQ-P29-02's case source is found. **D-06 veto window opens now; silence =
accept** (brief §4; the generic "D-06 numbering veto windows" line already stands in
HUMAN-QUEUE — this records the specific number).

## D-29-05 — D-05 citation honesty: Gail & Simon (1985) is the MOTIVATING DEFINITION, not the mechanism (SETTLED)

HQ-40 row 40e ANSWERED (2026-09-07): Gail, M. & Simon, R. (1985), *Testing for qualitative
interactions between treatment effects and patient subsets*, **Biometrics 41(2):361–372,
PMID 4027319** — read directly at PubMed. Verbatim: "Qualitative or crossover interactions
are said to occur when one treatment is superior for some subsets of patients and the
alternative treatment is superior for other subsets." This is the opposite-sign-across-
subsets definition the check's "harmed segment" criterion needs.

**Honesty constraint (binding on the S5-3 docstring + `# D-05:` marker), per the
Statistician — mirrors Phase 28 D-28-05 exactly:**
- **MAY claim:** Gail & Simon (1985) is the **motivating definition** of a qualitative
  (crossover) interaction — treatment effects of opposite sign across subsets — which is
  what motivates *when a segment counts as harmed* (opposite sign to the recommendation's
  premised direction).
- **MUST NOT claim:** that Gail & Simon authorise or supply the **enforcement mechanic**.
  Their paper is a formal **likelihood-ratio test** for qualitative interaction. The minted
  check runs **no such test** — no statistic is computed on the gate path (D-02); no gate
  reads a computed interaction statistic. The check enforces only the **declaration** that
  opposite-sign-above-floor segments carry a disposition row. Do not cite Gail & Simon as
  authority for the declaration-enforcement mechanic, and do not imply the check performs
  or approximates their test.

**Bounded-catch honesty (record in the docstring too):** DSX-COH-041 buys **attribution
over honestly-declared segments, not detection of hidden harm**. It closes "you declared a
harmed segment above the floor and failed to disposition it," **not** "you have a harmed
subgroup." All of these still **pass** — the standing "a frame that lies passes" limit
(Phase 27 "buys attribution, not a catch"; Phase 28 "catches via the stray number, not
metric-identity"): a spec that **omits** the harmed segment from `results.segments[]`; a
spec that **lies about the sign**; a spec that declares a **gamed floor** above D's n
(auditable, but passes). Note the fixture-as-built (which honestly declares D) IS caught —
D-29-00's "target" and this bound are consistent: the honest fixture is detected; an
evasive spec is not.

## Trigger predicate (PLAN INPUT for S5-2 — from the Statistician's Q1, recorded not over-frozen)

Read from DECLARED fields only (the CI arm is written in to honour the scope's OR and to
future-proof if `results.segments[]` ever gains a `ci`, but on today's schema only the
`n ≥ floor` arm bites — `results.segments[]` has no `ci`, so a CI-*required* trigger could
never fire on the exact miss it targets; that circularity is why sign+floor is the trigger,
not sign+CI):

```
question_type == "prescriptive"
AND overall = results.overall_effect is not None AND _sign(overall) != 0
FOR each S in results.segments[] with numeric S.effect:
    harmed(S) := _sign(S.effect) == -_sign(overall)
                 AND ( S.n >= decision.subgroup_harm_floor          # bites today
                       OR (S has declared ci AND ci excludes zero) )  # latent OR-arm
    if harmed(S) and no decision.subgroup_harm[] row with segment == S.name:
        report CRITICAL (DSX-COH-041)
    elif matching row present and disposition == "accept" and rationale blank:
        report HIGH (DSX-COH-041)
```

Rationale (rigour): `n ≥ floor` fires on any opposing segment above the floor regardless of
interval width — the broader trigger is the *stricter* one, and it keeps the trigger to
pure structural reads of declared fields (D-02). "CI excludes zero" would let a large
opposing segment with a wide CI escape the disclosure obligation silently — the exact
failure mode guarded against. The CI earns its rigour one layer down, in
`decision.subgroup_harm[].ci`, as the justification an `accept` row needs.

## Declaration vocabulary + plan inputs for S5-2 (recorded, not over-frozen)

- **`decision.subgroup_harm[]`** — additive, opt-in list of `{segment, effect, ci, n,
  disposition, rationale}`; consistent with the frozen `decision` schema's existing
  optional keys (`templates/ANALYSIS-SPEC.yaml:34-66`). Absent + an opposing segment above
  floor ⇒ CRITICAL (this is the whole point — NOT declaration-gated-silent).
- **`decision.subgroup_harm_floor`** — int absolute n, default 0 (D-29-01).
- **New check** `_check_subgroup_harm_disposition` (name S5-2) in `dsx/checks/coherence.py`
  (registered at plan/verify/ship — `cli.py:117,123,128`; NOT execute); **guard on
  populated results** (mirror Simpson's `len(segments) < 2: return` and the
  `overall_effect is None` early-return) so real-workflow plan runs on empty results stay
  silent, and so the check fires on the *completed* fixture at plan exactly as DSX-COH-001
  does — hence the target-map keys plan/verify/ship.
- **Harness wiring (D-29-00 — TARGET, not miss):** `_EXPECTED_CAUGHT_DEFECTS[slug] =
  frozenset({DSX-COH-041})` at the CRITICAL threshold points; `_TARGET_DEFECT_CODES[slug]`
  = DSX-COH-041 at plan/verify/ship; **verify `_ABSENT_PARTITION_FLOOR = 3` still holds**;
  spec count `tests/test_dsx.py` 44 → 45; catalogue `_EXPECTED_TOTAL` 278 → 279 +
  `finding-codes.md` row + `_D05_ALLOWLIST_CODES` exact-code entry — **all conditional on a
  live miss AND a found case source.** §6.5 item 9 promotion recorded via the target + the
  Phase-30 row rewrite; item id `6.5-item-9-subgroup-harm-declaration` is a frozen
  `_SECTION_65_ITEM_IDS` member (verified `tests/test_known_bad_corpus.py:951`).
- **Incidental discipline (Phase 28 D-28-06 precedent):** apply the swap-still-fires
  counterfactual (flip D's effect to positive) by literal code at S5-3; any code that
  **still** fires is incidental (encode per `_PER_FIXTURE_INCIDENTAL_CODES` if it collides
  with another fixture's target), any code that **stops** firing is a real catch → NO MINT.
  Watch DSX-DEC-001 and DSX-COH-040/030/031 (declare a complete passing replay + a
  discriminating revisit_when + checked assumptions so they clear on the merits).

## Guardrails (non-negotiable — from both personas, mirroring Phase 27/28)

1. **FREEZE-BEFORE-MEASURE.** D-29-00..05 are frozen by this document *before* the S5-3
   measurement. A no-miss outcome is a valid recorded terminal; it is **not** a licence to
   widen/weaken/re-shape the case. Any post-measurement edit to the frozen design voids
   the phase.
2. **NOTHING MINTED PRE-MEASUREMENT.** No `subgroup_harm`/`subgroup_harm_floor` vocabulary
   ships, no `DSX-COH-041` check/docstring is authored; the code is RESERVED-INACTIVE until
   S5-3 confirms a live miss AND REQ-P29-02's case source is found. The Gail & Simon
   citation is resolved (HQ-40 40e); the documented public failure case is unfound (S5-2
   research deliverable) — do NOT treat it as found.
3. **HARD STOP AT THE MINT BOUNDARY.** S5-3's first deliverable is the recorded four-point
   verdict from a fresh tempdir. On a confirmed live miss **and** a found case source:
   author the vocabulary + DSX-COH-041 + Gail & Simon docstring (motivating definition,
   enforced as a declaration — never computed) + harness. On a catch, or a missing case
   source, write the no-mint record and close (item 9 stays on the backlog, half-met
   condition stated).
4. **HONEST MEASUREMENT.** Fresh isolated tempdir; existing gate byte-unmodified; every
   measured code (including incidental fires) recorded verbatim at each of the four points
   before interpreting; swap-still-fires applied by literal code.

## §5 — What this unit did NOT do

S5-1 settles and freezes the **design** (D-29-00..05) from the §4 persona round; the D-05
citation (Gail & Simon) is resolved. It did **not**: build the fixture, run any
measurement, find the REQ-P29-02 documented public failure case, ship any vocabulary, mint
any code, or write the check. **The LIVE MISS is unmeasured** — S5-3's first act (execute
measures first, D-13). The S5-1 box is CHECKED because its deliverable — the settled,
frozen CONTEXT with the four required settlements (segment floor declaration; four-segment
case shape; disposition vocabulary; reserved number) plus the D-05 honesty boundary and
the D-29-00 harness-polarity correction — is complete.

**Next: S5-2** (plan the mint conditional on the live miss AND a found case source;
**research must find or record-as-not-found the documented public failure case**;
plan-checker must pass; confirm `_ABSENT_PARTITION_FLOOR=3` and the target-map wiring) →
**S5-3** (measure first at the four gate points; if live miss AND case found → author
vocabulary + check + Gail & Simon docstring + DSX-COH-041 + harness as a TARGET; else the
no-mint record) → **S5-4** review → **S5-5** secure/validate.

## §4 persona round record (Architect + Statistician, opus, parallel, grounded independently)

- **ARCHITECT** (`dsx-analysis-architect`) → independently verified all four orchestrator
  facts by reading the code (MET-030/031 silent at 1-of-4; catalogue 278, DSX-COH-041 free;
  segments schema `{name,effect,n}`; existing prescriptive fixture distinct). Load-bearing
  original finding **D-29-00**: the fixture is a pre-mint LIVE MISS that becomes a post-mint
  TARGET (not a Phase-27/28 permanent miss) because REQ-P29-03's "missing-row CRITICAL"
  fires on the declared segment with no opt-in pointer to omit — wires as
  `_TARGET_DEFECT_CODES`, verify `_ABSENT_PARTITION_FLOOR`. Settled: floor
  `decision.subgroup_harm_floor` (int, default 0); slug `subgroup-harm-without-disposition`;
  prescriptive+experiment minimal-perturbation clone (no good prescriptive fixture exists);
  one two-severity code; `DSX-COH-041` (04x decision-obligation tier, sibling of 040).
  Predicts LIVE MISS → mint, conditional on S5-3.
- **STATISTICIAN** (`dsx-statistician`) → independently verified the Simpson gap is
  *structural* (a ≥half rule is definitionally blind to a harmed *minority* under a positive
  average — the real shape of subgroup harm), grep-confirmed no other check reads segments,
  and added two facts: `results.segments[]` has **no `ci`** (so a CI-required trigger is
  circular — the trigger must be sign + n≥floor) and `decision.replay` is segment-blind
  (`decision.py:70-89`, greenlights rollout on the +3.2pp aggregate — both "no secret catch"
  and the harm mechanism). Settled: sign+floor trigger; floor default 0 (un-gameable);
  faithful non-manufactured 4-seg/1-minority shape with checked numbers; CRITICAL/HIGH
  ladder; Gail & Simon = motivating definition only, never the mechanic; bounded-catch =
  attribution not detection. Named DSX-COH-050 as the "next round number" but deferred final
  numbering to the D-06 veto window.
- **Convergence + tie-break (rigour > reliability > flexibility):** the two agreed on every
  load-bearing point (structural gap, case shape, floor default 0, trigger sign+floor,
  CRITICAL/HIGH ladder, Gail & Simon honesty, bounded-catch limit, LIVE-MISS prediction).
  The one numbering divergence (Architect `DSX-COH-041` tier placement vs Statistician
  `DSX-COH-050` next-round-number, with the Statistician deferring to the veto window)
  resolved by **rigour** to `DSX-COH-041` (D-29-04), consistent with Phase 28's fill-the-tier
  D-06 precedent. The Statistician did not contest D-29-00.
- **Classification (brief §4):** these are persona-round decisions recorded loudly with a
  veto window (the D-06 number), NOT HUMAN-QUEUE escalations. REQ-P29-01/02/03 unchanged;
  D-29-00 (target vs permanent-miss) is a harness-polarity consequence *forced by
  REQ-P29-03*, not a scope change. The remaining human dependency is REQ-P29-02's documented
  public failure case, which is *research*, not a D-05 read of a named source (the named D-05
  source, Gail & Simon, is already confirmed) — S5-2 finds it or records not-found.
