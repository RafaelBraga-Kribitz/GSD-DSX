# Phase 29: Evidence case — subgroup harm under a prescriptive recommendation — Research

**Researched:** 2026-09-08
**Domain:** dsx coherence-discipline check (`dsx/checks/coherence.py`, `DSX-COH-*`) + D-13
measure-first corpus-fixture mint (conditional on a live miss AND a found case source) +
finding-catalogue/harness TARGET wiring. Plus the REQ-P29-02 **documented public failure case**
research deliverable.
**Confidence:** HIGH on the case citation (confirmed at its locator this session via two
independent authoritative indexes + PDF retrieval — see honesty flag); HIGH on the plan-input
locators (the catalogue total, the free code slot, the absent-partition floor and the spec count
re-measured live this firing; the CONTEXT's persona-verified code map is inherited on a tree that
is byte-frozen since the S5-1 commit).

> Scope: this is the S5-2 *plan-input* research. `29-CONTEXT.md`'s design (D-29-00..05) is FROZEN
> and is NOT re-opened here (guardrail 1: freeze-before-measure). This file delivers the one thing
> S5-2's research sub-stage owes — REQ-P29-02's documented public case — and re-confirms the
> counts/locators the plan will pin. **The LIVE MISS is UNMEASURED as of this research** (D-13,
> S5-3's first act); nothing here assumes the four-point verdict, and the plan the next firing
> writes must be correct under EITHER measured outcome (live miss → conditional mint; catch →
> no-mint close). No vocabulary ships, no `DSX-COH-041` is authored here.

---

## 1. REQ-P29-02 — the documented public failure case (the distinctive S5-2 deliverable)

REQ-P29-02 has **two** source obligations, tracked separately:

1. **The enforcement-criteria primary source** (Gail & Simon 1985, the qualitative-interaction
   definition, *enforced as a declaration, never computed*) — **ALREADY CONFIRMED** by the human
   read, HQ-40 row 40e (2026-09-07, PubMed PMID 4027319, *Biometrics* 41(2):361–372, read
   directly). This is a D-05 read and is closed. Not re-opened here.
2. **One documented public case where an average benefit masked subgroup harm, found by phase
   research with a primary source** — this was **UNFOUND** at S5-1 (recorded as the half-met
   condition). It is **research, not a D-05 read** (the S5-1 record and CONTEXT §4 classification
   are explicit: the named D-05 source is already confirmed; this second half is phase research).
   **This firing FINDS it.**

### FOUND — Obermeyer, Powers, Vogeli & Mullainathan (2019)

**Full citation (Crossref publisher metadata, confirmed at its locator this session):**
> Obermeyer, Z., Powers, B., Vogeli, C., & Mullainathan, S. (2019). *Dissecting racial bias in an
> algorithm used to manage the health of populations.* **Science, 366(6464), 447–453.**
> DOI: **10.1126/science.aax2342**. PubMed: **PMID 31649194**.

**Why it is the REQ-P29-02 case — the phenomenon is the requirement, verbatim from the abstract**
(Semantic Scholar authoritative abstract, quoted exactly):

- **The masking aggregate benefit:** *"despite health care cost appearing to be an effective proxy
  for health by some measures of predictive accuracy, large racial biases arise."* The algorithm
  looked good on an aggregate accuracy metric — that is the "average benefit" that masked the harm.
- **The subgroup harm:** *"At a given risk score, Black patients are considerably sicker than White
  patients, as evidenced by signs of uncontrolled illnesses."* A minority subgroup is materially
  harmed under a system whose aggregate metric looked fine.
- **The operationalisable magnitude:** *"Remedying this disparity would increase the percentage of
  Black patients receiving additional help from 17.7 to 46.5%."* Not noise — a decision-changing
  harm on a real minority subgroup, exactly the shape §6.5 item 9 and the frozen fixture
  (D-29-02: one minority segment, material n, opposite direction) mirror.
- **The generalisable lesson the paper itself draws:** *"the choice of convenient, seemingly
  effective proxies for ground truth can be an important source of algorithmic bias in many
  contexts"* — i.e. an aggregate metric that looks good can mask systematic subgroup harm. This is
  precisely the failure DSX-COH-041 is motivated to force disclosure of.

**Mapping to the check's phenomenon (honest, with the boundary stated):**
- **What matches (the requirement):** a deployed, decision-driving system with a **positive
  aggregate signal** that **masked a material harm concentrated in one minority subgroup**, publicly
  documented in a peer-reviewed primary source. That is REQ-P29-02's phrase — "an average benefit
  masked subgroup harm" — instantiated in the real world.
- **What differs (do not overclaim — mirrors the project's D-05 honesty discipline):** Obermeyer is
  a **label-bias / allocation-fairness** case (the target proxy — cost — was itself biased), **not**
  a Gail & Simon *qualitative interaction* (an opposite-sign *treatment* effect in a randomized
  contrast). The frozen fixture (D-29-02) is built as the qualitative-interaction shape (a
  minority segment whose *effect* opposes the positive overall). So Obermeyer is the documented
  public case of the **broader phenomenon the whole check exists to force disclosure of**; Gail &
  Simon (1985) supplies the **enforcement definition** for *when a segment counts as harmed*. The
  two sources play the two distinct roles REQ-P29-02 asks for; neither is asked to do the other's
  job. Recording both, with this boundary explicit, is the defensible read for a sceptical
  reviewer.

**Locator-confirmation method + honesty flag (binding on how the record may be phrased):**
- Bibliographic metadata (title, four authors, *Science* 366(6464):447–453, 2019, DOI) confirmed
  against **Crossref** — the publisher's own authoritative metadata service.
- The abstract text quoted above confirmed **verbatim** against **Semantic Scholar's** authoritative
  paper record (independent of Crossref).
- The full open-access PDF (UC eScholarship, item `6h92v832`, 543.8 KB) was **retrieved** but is a
  binary/compressed-stream PDF that could not be rendered to text in this environment (no
  poppler/pdftoppm; the small extraction model saw only PDF object code). **No full-body read is
  claimed.** The confirmation rests on the publisher metadata (Crossref) + the verbatim abstract
  (Semantic Scholar) — an *authoritative abstract-grade* confirmation, stronger than HQ-40 40b's
  secondary-index corroboration but weaker than a full-text read. Any downstream mention (a plan
  note, a §6.5 row, a docstring aside) must say "abstract + authoritative metadata confirmed," not
  imply the body was read.
- **Not a D-05 human read, and does not become one.** REQ-P29-02's *enforcement* source (Gail &
  Simon) is the D-05 read and is already closed; this documented-case half is phase research and is
  satisfiable by the loop (S5-1/CONTEXT §4 classification). No new HUMAN-QUEUE item is owed for it.

**Consequence for the requirement:** REQ-P29-02 moves from **half-met** (source confirmed, case
unfound) toward **fully met** — both halves now have a confirmed primary source. It remains
formally *contingent* only on S5-3's live-miss measurement (per REQ-P29-03's "if … source is
confirmed" clause and the frozen guardrails); the *case-source* condition of the mint is now
**satisfied**. Item 9 no longer carries the "documented public failure case UNFOUND" condition.

**Structural analogs (from prior knowledge, NOT independently confirmed at a locator this firing —
recorded as corroboration only, explicitly not the designated case):**
- **National JTPA Study** (Bloom, Orr, et al., mid-1990s evaluation): job-training had a
  positive/neutral *average* impact but a **negative** impact for male out-of-school youth — a
  genuine opposite-sign subgroup harm under a program a positive aggregate would recommend scaling.
  This is the closer *qualitative-interaction* structural match to the fixture, but its primary
  source (the multi-volume evaluation report / *J. Human Resources* articles) was not opened this
  firing, so it is not designated — offered only to show Obermeyer is not a lone data point.
- **Gail & Simon (1985)** themselves illustrate qualitative interaction on breast-cancer trial
  (NSABP) subgroup data — the citation already confirmed at HQ-40 40e doubles as a documented
  clinical instance of the phenomenon.

Designating **one** confirmed case (Obermeyer) satisfies REQ-P29-02's "one documented public case";
the analogs are supporting context, not additional claims to defend.

---

## 2. Plan-input locator + count map (re-confirmed live this firing)

The CONTEXT (S5-1) carries a thorough, twice-persona-verified code map (the clear-table
D-29-02, the trigger predicate, the harness wiring D-29-00). The tree is byte-frozen since the
S5-1 commit (`356d550`; `git diff` on `dsx/` empty), so those locators stand. The plan will **pin**
these counts — re-measured live this firing, not trusted from the CONTEXT:

| Pin the plan asserts | Value (re-measured 2026-09-08) | Evidence |
|---|---|---|
| Catalogue total (pre-mint) | **278** | `references/finding-codes.md:16` "**Total: 278 codes.**" |
| `DSX-COH-041` currently free | **yes** | `grep -c DSX-COH-041 references/finding-codes.md` → **0** |
| Absent-partition floor holds | **3** | `tests/test_known_bad_corpus.py:993` `_ABSENT_PARTITION_FLOOR = 3`, asserted `:2071/:2129/:2174` |
| Corpus spec count (pre-add) | **44** | `tests/test_dsx.py:588` `self.assertEqual(len(paths), 44, …)` |

**Conditional deltas the plan encodes (all gated on S5-3's live miss AND the now-found case
source):** catalogue `278 → 279` (`_EXPECTED_TOTAL` + a `finding-codes.md` row +
`_D05_ALLOWLIST_CODES` exact-code entry); spec count `44 → 45`; `_EXPECTED_CAUGHT_DEFECTS[slug] =
frozenset({DSX-COH-041})` and `_TARGET_DEFECT_CODES[slug]` at plan/verify/ship (**TARGET, not a
`kind: miss` sidecar** — D-29-00's load-bearing correction); `_ABSENT_PARTITION_FLOOR` **stays 3**
(a new *present/target* fixture subtracts nothing from the existing miss set — S5-3 verifies, does
not assume). Registration at plan/verify/ship (`cli.py:117,123,128`), NOT execute. The new check
`_check_subgroup_harm_disposition` in `coherence.py`, guarded on populated results (Simpson's
`len(segments) < 2: return` + `overall_effect is None` early-return moulds).

**The miss seam (re-stated, not re-derived):** MET-030/031 (`metrics.py:296-349`) are structurally
silent at 1-of-4 opposing (030 needs all-oppose, 031 needs ≥half; `1==4` and `1>=2` both False),
and `results.segments` is consumed by exactly one function in `dsx/` (`_check_simpsons_paradox`) —
`subgroup_harm` appears nowhere — so the gap is genuinely uncovered pre-mint. S5-3 MEASURES this
at four points from a fresh tempdir before any check is authored (D-13).

---

## 3. D-05 honesty carried into the plan (from D-29-05, restated for the planner)

The plan must instruct S5-3's docstring + `# D-05:` marker to cite **Gail & Simon (1985) as the
MOTIVATING DEFINITION only** (opposite-sign-across-subsets = when a segment counts as harmed),
never as authority for the enforcement mechanic (their paper is a likelihood-ratio *test*; the
check computes nothing on the gate path — D-02). Bounded-catch honesty: DSX-COH-041 buys
**attribution over honestly-declared segments, not detection of hidden harm** — a spec that omits
the harmed segment, lies about the sign, or declares a gamed floor still passes. Obermeyer is the
real-world *motivation* for forcing the disclosure; it is **not** cited as an enforcement authority
either.

---

## 4. What this research does NOT do

- Does **not** re-open the frozen design (D-29-00..05 stand; guardrail 1).
- Does **not** measure the live miss (S5-3's first act, D-13) — no four-point verdict is assumed.
- Does **not** ship any vocabulary, author `DSX-COH-041`, or touch `dsx/` (byte-frozen this unit).
- Does **not** write the plan itself — that is the remainder of S5-2 (next firing): decompose into
  plans, run `/gsd-plan-phase 29`, and pass the plan-checker gate (orchestrator re-verifies the
  gate itself). The S5-2 box stays **UNCHECKED** until that gate passes.

**S5-2 progress after this firing:** research sub-stage **DONE** — REQ-P29-02's documented public
case FOUND and confirmed at its locator (Obermeyer et al. 2019, Science 366(6464):447–453). Plan
authoring + plan-checker gate remain. **Next: author the Phase 29 plan(s) and gate them.**
