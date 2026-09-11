# Post-mortem: subgroup harm undisclosed under a prescriptive rollout recommendation

Paired spec: `subgroup-harm-without-disposition-ANALYSIS-SPEC.yaml`
Paired entrypoint: `subgroup-harm-without-disposition-entrypoint.py`
Attribution sidecar: `subgroup-harm-without-disposition-ATTRIBUTION.yaml` (the corpus's
first `kind: target`)

## What was concluded

A growth-analytics team ran a randomized experiment on a retention bundle and
recommended rolling it out to **100% of at-risk accounts**. The recommendation is
genuinely prescriptive (`question_type: prescriptive`, `design.kind: experiment`,
`identification: randomized_experiment`) and rests on a positive n-weighted
aggregate: +3.2 percentage points of 90-day retention lift (95% CI 2.4 to 4.0pp),
a fully-reported two-proportion z-test, and a structured `decision.replay` that
greenlights the rollout on that aggregate. The spec declares a segment breakdown —
four segments, all above the declared harm floor:

| Segment | n | effect | opposes overall (+3.2pp)? |
|---|---|---|---|
| A (high-value) | 4000 | +5.0pp | no |
| B (mid) | 3000 | +4.0pp | no |
| C (established) | 2000 | +3.0pp | no |
| **D (minority)** | **1000** | **−6.0pp** | **yes** |

It declares `decision.subgroup_harm_floor: 500` and then recommends rolling the bundle
out to everyone — including segment D, a material minority (n=1000, 10% of the book)
the experiment itself measured being **harmed** by 6.0pp, well above the declared 500
floor. No `decision.subgroup_harm[]` disposition row acknowledges, accepts, excludes,
or mitigates that harm.

## Why it was wrong

The n-weighted aggregate is real, but it is an average: the +5.0/+4.0/+3.0pp gains on
segments A, B and C mathematically swamp the −6.0pp loss on the smaller segment D, so
the book-level number looks like an unqualified win. Recommending a rollout to *all*
at-risk accounts on that average silently ships a −6.0pp retention harm to a declared,
identifiable minority. This is the qualitative (crossover) interaction Gail & Simon
(1985) *define* — one treatment superior for some subsets, the alternative superior for
others (Gail, M. & Simon, R. (1985), "Testing for qualitative interactions between
treatment effects and patient subsets," *Biometrics* 41(2):361–372, PMID 4027319). That
paper supplies the **motivating definition** of *when a segment counts as harmed*
(opposite sign to the recommendation's premised direction); it is a formal
likelihood-ratio test and is **not** the enforcement mechanic here — no statistic is
computed on the gate path (D-02). The gate enforces only the **declaration** that a
declared opposite-sign, above-floor segment carries a disposition row.

The real-world motivation for forcing that disclosure is Obermeyer et al. 2019
(Obermeyer, Z., Powers, B., Vogeli, C. & Mullainathan, S. (2019), "Dissecting racial
bias in an algorithm used to manage the health of populations," *Science*
366(6464):447–453, DOI 10.1126/science.aax2342, PMID 31649194): a deployed,
decision-driving system whose aggregate accuracy metric looked effective while it
concentrated material harm in one minority subgroup. That case is recorded here at
**abstract + authoritative metadata grade** (bibliographic metadata confirmed against
Crossref; the abstract confirmed verbatim against Semantic Scholar) — **the paper body
was not read**, and it is cited as motivation, not as an enforcement authority.
Obermeyer is a label-bias / allocation-fairness case (the target proxy was itself
biased), not a Gail & Simon qualitative-interaction contrast; it is the documented
public instance of the *broader phenomenon* the check exists to force disclosure of,
while Gail & Simon supplies the enforcement *definition*.

### The MET-030/031 structural seam (the miss, from the arithmetic)

`_check_simpsons_paradox` (`dsx/checks/metrics.py:296-349`) is the only function in
`dsx/` that reads `results.segments[]`. Its two emit gates, evaluated against this
fixture (overall sign +, opposing = [('D', −0.06)], count 1 of 4):

```text
DSX-MET-030 (metrics.py:316)  len(opposing) == len(effects):   1 == 4   -> False  (SILENT)
DSX-MET-031 (metrics.py:334)  len(opposing) >= len(effects)/2: 1 >= 2.0 -> False  (SILENT)
```

Both are **structurally silent at 1-of-4 opposing**, and the check's `else` branch
(`metrics.py:348-349`) actively emits a reassuring "segment effects are directionally
consistent with the aggregate" INFO. A `≥half` rule is definitionally blind to a harmed
**minority** under a positive average — the real shape of subgroup harm. This is the
structural gap brief §6.5 item 9 targets, confirmed by the arithmetic, not asserted.

## What the gate saw before the mint, and what it sees now

This is the D-29-02 / D-13 entry-condition test. On the **pre-mint** gate (no
`DSX-COH-041` shipped), measured from a fresh `tempfile.TemporaryDirectory()` per gate
point against the spike fixture (29-MEASUREMENT.md, `VERDICT: LIVE MISS`, measured
2026-09-08 on CPython 3.12.10):

| Gate point | Exit | CRITICAL | HIGH |
|---|---|---|---|
| `dsx validate` | 0 | — | — |
| `dsx gate plan` | 0 | — | — |
| `dsx gate execute` | 0 | — | — |
| `dsx gate verify` | 0 | — | — |
| `dsx gate ship` | 0 | — | — |

**No CRITICAL and no HIGH finding fired at any point.** The undispositioned opposing
minority — the sole defect — was caught by no shipped code. `DSX-MET-030`/`031` were
absent from the findings everywhere (`MET codes present: []`). That clean LIVE MISS is
what licensed the mint (D-13): plan 29-01 authored `_check_subgroup_harm_disposition` /
`DSX-COH-041` (catalogue 278 → 279).

After the mint, measured the same way against this committed fixture and entrypoint
(fresh tempdir per point; a plan-time decision header seeded first at verify/ship, as
the corpus harness does automatically):

| Gate point | Exit | CRITICAL | HIGH |
|---|---|---|---|
| `dsx validate` | 0 | — | — |
| `dsx gate plan` | 1 | `DSX-COH-041` | — |
| `dsx gate execute` | 0 | — | — |
| `dsx gate verify` | 1 | `DSX-COH-041` | — |
| `dsx gate ship` | 1 | `DSX-COH-041` | — |

`DSX-COH-041` fires **CRITICAL at plan/verify/ship** — the `coherence` check family is
registered at those three points and is absent from `execute`
(`dsx/cli.py::GATE_PROFILES`), so the fixture clears execute (exit 0) by construction.
This is the D-29-00 **target polarity** — the code is PRESENT/DETECTED everywhere it
fires, the load-bearing INVERSE of the Phase-27/28 attribution-only misses (where the
attributing code is ABSENT and lives in a `kind: miss` sidecar). `DSX-STA-011` (MEDIUM,
verify/ship) and `DSX-PAR-001` (INFO, every point) sit below the HIGH ship threshold
and never block.

### The swap-still-fires counterfactual (applied by literal code)

Flipping **only** segment D's declared effect from −0.06 (opposing) to +0.06 (aligned),
leaving `overall_effect` and every other field byte-identical, isolates D's opposition.
Under the swap, `opposing = []` (0 of 4), so `DSX-MET-030`/`031` stay silent as before —
and the post-mint gate now clears completely:

| Gate point | Exit | CRITICAL | HIGH | swap-invariant residual |
|---|---|---|---|---|
| `dsx gate plan` | 0 | — | — | — |
| `dsx gate execute` | 0 | — | — | — |
| `dsx gate verify` | 0 | — | — | `DSX-STA-011` (MEDIUM) |
| `dsx gate ship` | 0 | — | — | `DSX-STA-011` (MEDIUM) |

**`DSX-COH-041` is the code that TOGGLES.** It fires on the DEFECT (opposing D) and
**stops firing** the moment D is made to align — the signature of a real closed catch,
not a swap-invariant artefact. `DSX-STA-011` (a small Cohen's-`h` negligible-effect
advisory on the aggregate, MEDIUM) fires identically in both variants; it reads the
primary test's `standardized_effect`, a field the swap leaves untouched, so it is a
**swap-invariant incidental** orthogonal to the subgroup-harm defect and is not shaved
away (D-13). It never blocks (MEDIUM sits below the HIGH ship threshold).

## The code that catches it

- **`DSX-COH-041`** (CRITICAL) — `_check_subgroup_harm_disposition`
  (`dsx/checks/coherence.py`, minted in plan 29-01). Under a prescriptive question with a
  signed aggregate, it reads each `results.segments[]` entry, reuses the sign convention
  from `metrics.py` verbatim, and fires CRITICAL when a segment whose declared `effect`
  opposes `results.overall_effect` and whose `n ≥ decision.subgroup_harm_floor` has **no
  matching `decision.subgroup_harm[]` row**. Here segment D (−6.0pp, n=1000) opposes the
  +3.2pp aggregate above the declared 500 floor with no disposition row, so the code
  fires at plan/verify/ship.

## Bounded-catch limit (D-29-05 honesty)

`DSX-COH-041` buys **attribution over honestly-declared segments, not detection of
hidden harm**. It closes "you declared a harmed segment above the floor and failed to
disposition it," **not** "you have a harmed subgroup." A spec that *omits* segment D from
`results.segments[]`, one that *lies about the sign*, or one that declares a *gamed
floor* above D's n all still pass the gate — each is auditable but evasive, and the check
does not compute an interaction statistic to catch them (D-02). The fixture as built
honestly declares D, which is exactly why it is caught: the honest declaration is
detected; an evasive frame is not.
