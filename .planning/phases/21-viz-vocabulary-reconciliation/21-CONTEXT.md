# Phase 21: Viz vocabulary reconciliation — Context

**Milestone v2.4 Visual Excellence · S1-1 discuss · 2026-09-03 (autonomous firing).**
The foundation phase. The Phase 22 catalog spine is built directly on the mark
vocabulary this phase reconciles, so Phase 21 **hard-blocks Phase 22**. Requirements:
REQ-P21-01 … REQ-P21-03 (3). Phase 21 **mints zero new codes** (REQ-P21-03,
set-identity diff vs the S0-2 re-measured 275 baseline); it adds one repo-integrity
test, homes the orphaned marks into the capability matrix, and turns the five banned
types into first-class refusal entries.

## Phase Boundary

Reconcile the existing chart-mark vocabulary so every non-banned mark is reachable,
and make banned marks explicitly refused rather than silently absent. **No new gate
code, no computation on data, no pandas/scipy/numpy on the gate path** (D-01/D-02).
The every-mark-has-a-home invariant is a **repo-integrity test** (`tests/`), not a
`dsx run` gate check — it asserts a property of the vocabulary data structures, off
the gate path, in the same family as `test_finding_catalogue_invariant.py`. The
catalogue stays byte-frozen at **275 codes**; the set-identity diff is the phase-end
gate (REQ-P21-03).

## Ground truth read this firing (assumptions mode)

Live structures read in full, with their consumers traced:

- **`RELATIONSHIP_CHARTS`** (`dsx/checks/viz.py:17-28`) — 10 relationships → admissible
  marks, first entry = default. The **recommendation surface**. Consumed by
  `_check_relationship_match` (DSX-VIZ-010/011/012) and `input_types.py:100` (narrowing).
- **`CHART_CAPABILITIES`** (`dsx/spec.py:296-325`) — 15 `data_input_type` families →
  admissible marks. The **admissibility surface** on the gate path
  (`_check_input_type_matrix`, DSX-VIZ-013). Consumed also by `input_types.py:94`,
  `gen-input-types.py:143`, `spec.py:1647` (vocab dump), `test_input_types.py:32`.
- **`EXTRA_MARKS`** (`scripts/gen-input-types.py:77-86`) — per-IT-id addendum:
  `admissible(IT) = CHART_CAPABILITIES[family(IT)] ∪ EXTRA_MARKS[IT]`. **This is a real
  capability-reachability path** — the input-type matrix admits these marks. `IT011 →
  {population_pyramid, butterfly}` is the load-bearing entry for this phase.
- **`BANNED_TYPES`** (`dsx/checks/viz.py:36-42`) — flat `dict[str,str]` (mark →
  distortion reason). Consumed at **exactly two sites**: `viz.py:81` (`in` membership)
  and `viz.py:86` (`BANNED_TYPES[chart_type]` read as a string). No serializer, no
  `dsx vocab` dump, and no test iterates its values — verified by repo-wide grep.
- Property sets: **`LENGTH_ENCODED`** (viz.py:32), **`DENSITY_MARKS`** `{density, kde,
  violin}` (smells.py:12), **`STACKED_MARKS`** (smells.py:13). These name marks and
  trigger property checks; they are **not** home families.

## Persona round (LOOP-BRIEF §4)

**Architect** (`dsx-analysis-architect`) + **Auditor** (`dsx-ml-integrity-auditor` /
`gsd-security-auditor` lens), both opus/high, run **inline** by the orchestrator against
the S0-verified ground truth — the Phase-17 precedent: a single artifact that must
complete in one firing without mid-unit compaction (brief §1), so tightly-scoped
inline deliberation beats blind-exploring subagent spawns. The **Statistician is not
engaged** — a structural-vocabulary discuss has no statistical content (same reasoning
as Phase 17, different second lens: here the "never silently absent" property and the
zero-new-codes set-identity guard are integrity concerns, so the Auditor lens replaces
the Statistician).

Tie-break **rigour > reliability > flexibility**. The round **converged** on both named
decisions and surfaced one finding that goes beyond the S0-2 recheck (below).

## Decisions (loud, vetoable — LOOP-BRIEF §4; veto window filed as HQ-28, silence = accept)

<!-- Machine-readable decision index (added S1-2 as a format bridge for the
     context-coverage gate; decision CONTENT is unchanged — see the detailed
     ### D-01 / ### D-02 sections below, which remain authoritative). -->

- **D-01 — every-mark-has-a-home invariant scope (REQ-P21-01):** one repo-integrity
  test off the gate path, two directional clauses over the mark universe
  (`RELATIONSHIP_CHARTS` ∪ `CHART_CAPABILITIES` ∪ `EXTRA_MARKS` ∪ smells sets, minus
  `BANNED_TYPES`); capability home = membership in `CHART_CAPABILITIES` or `EXTRA_MARKS`
  (gate-faithful); relationship home = membership in `RELATIONSHIP_CHARTS`, else the
  frozen `CAPABILITY_ONLY` allowlist; homes the 12 orphans.
- **D-02 — refusal-entry representation (REQ-P21-02):** enrich `BANNED_TYPES` in place
  from `dict[str,str]` to `{reason, code, citation}`; `code` = `DSX-VIZ-001` for all
  five; `_check_banned` reads `["reason"]` at its one call site; citations point at the
  HQ-27 Tier-3 pack (non-blocking, drained at S5-2).

### D-01 — the every-mark-has-a-home invariant's exact scope (REQ-P21-01)

The invariant is **two directional clauses over a precisely-bounded mark universe**,
implemented as one repo-integrity test off the gate path.

**Mark universe** = the union of marks named in `RELATIONSHIP_CHARTS` values,
`CHART_CAPABILITIES` values, `EXTRA_MARKS` values, `LENGTH_ENCODED`, `DENSITY_MARKS`,
and `STACKED_MARKS`, **minus `BANNED_TYPES`** (banned marks are exempt from homing and
are covered by REQ-P21-02's refusal invariant instead).

**Capability home** = admitted by ≥1 input-type's *effective* admissible set =
membership in some `CHART_CAPABILITIES` value **or** some `EXTRA_MARKS` value. This is
the **gate-faithful** definition: it is exactly what `_check_input_type_matrix`
(DSX-VIZ-013) admits from, so the invariant tests the property the gate enforces, not a
narrower proxy. It also avoids over-widening a base family for a mark that is only
sensible for one specific IT shape.

**Relationship home** = membership in some `RELATIONSHIP_CHARTS` value.

- **Clause 1 (capability-completeness, hard).** Every mark in the universe has a
  capability home. This is the clause that fixes the DSX-VIZ-013 friction the ROADMAP
  names ("marks the catalog will reference but no family admits"). It homes the 9
  relationship-listed capability-orphans + `kde`.
- **Clause 2 (relationship-completeness, hard, with an explicit exempt allowlist).**
  Every mark in the universe **either** has a relationship home **or** is on a
  frozen `CAPABILITY_ONLY` allowlist. `RELATIONSHIP_CHARTS` is a *curated recommendation
  surface*, deliberately not exhaustive — several admissible marks have no natural fit
  among the 10 relationships (`big_number`, `candlestick`, `column_range`). Forcing them
  in would corrupt the per-relationship defaults. The allowlist makes them **loud and
  frozen**, not silently absent (REQ-P21-02's spirit applied to the recommendation side).

**Why the two-clause + allowlist shape, not a naive symmetric "both homes for all"
(Architect + Auditor, rigour tier).** A strict symmetric reading of "reachable through a
relationship AND a capability" exposes **~14 capability-only marks** that REQ-P21-01's
enumerated 12 never named (see the finding below). Homing all of them into
`RELATIONSHIP_CHARTS` would (a) exceed REQ-P21-01's grant — a scope expansion, not the
enumerated 12 — and (b) over-widen the recommendation defaults with marks like
`big_number` that fit no relationship. Silently ignoring them would violate the "never
silently absent" doctrine. The frozen allowlist is the rigorous middle: the invariant is
**provably complete** (every universe mark is accounted for by a home or an explicit
exemption), the 12 are homed as required, and no unscoped expansion happens. A mark added
later to `CHART_CAPABILITIES` without a relationship home **and** without an allowlist
entry fails the invariant — catching the exact drift class.

**The finding that extends S0-2 (recorded loudly per the brief's "state the correction
explicitly" rule):**

1. **`population_pyramid` and `butterfly` are not "double orphans."** S0-2 labeled them
   so under a strict `CHART_CAPABILITIES`-only reading. Under the gate-faithful reading
   adopted here, they are **capability-homed via `EXTRA_MARKS[IT011]`** and are
   **relationship-orphans only**. Their homing work is therefore **relationship-only**
   (add a relationship home); do **not** touch `CHART_CAPABILITIES` for them.
2. **~14 capability-only marks lack a relationship home** — `column`, `grouped_bar`,
   `multi_line`, `bubble`, `donut`, `sunburst`, `icicle`, `circle_pack`, `timeline`,
   `gantt`, `big_number`, `candlestick`, `ohlc_bar`, `column_range`. Not in REQ-P21-01's
   12; surfaced by clause 2. These become the frozen `CAPABILITY_ONLY` allowlist, **not**
   homed into relationships this phase. Whether any (e.g. `column → comparison`,
   `grouped_bar → comparison`) *should* be promoted is a **Phase 22 catalog decision**
   (relationship-per-entry is assigned there, with citations) — carried as a caveat, not
   pre-empted here.

**Homing guidance for the plan (S1-2/S1-3) — proposed, plan-checker-verifiable, not
frozen.** Home each orphan to the family/relationship whose *data signature* it matches;
prefer the narrowest home that removes the friction (`EXTRA_MARKS[specific IT]` for a
mark sensible only for one shape; base `CHART_CAPABILITIES` family for a broadly-admissible
signature):

| Mark | Has (existing) | Add | Rationale |
|---|---|---|---|
| histogram | rel: distribution | cap: interval-range | univariate continuous distribution; sits with box/violin |
| density | rel: distribution | cap: interval-range | smoothed univariate distribution |
| ecdf | rel: distribution | cap: interval-range | cumulative univariate distribution |
| strip | rel: distribution | cap: interval-range | raw univariate points |
| diverging_bar | rel: deviation | cap: categorical-value | signed value per category from a baseline |
| waterfall | rel: deviation | cap: composition *(alt: categorical-value)* | cumulative bridge of contributions to a total |
| dumbbell | rel: deviation | cap: categorical-multi | two values per category (before/after) |
| bump | rel: ranking | cap: categorical-multi *(alt: time-series)* | rank series across ordered steps |
| sankey | rel: flow | cap: matrix | weighted edge list / adjacency; sibling of chord |
| kde | — | rel: distribution + cap: interval-range | density estimate of one continuous var (needs both) |
| population_pyramid | cap: IT011 extra | rel: distribution *(alt: comparison)* | mirrored age-band distributions |
| butterfly | cap: IT011 extra | rel: comparison | back-to-back category comparison (tornado) |

Homing widens admissibility to **fix false positives** (e.g. `interval-range`+`histogram`
today wrongly fires DSX-VIZ-013); it introduces **no false negatives** (each mark is
genuinely admissible for its assigned signature) and **no new code**.

### D-02 — refusal-entry representation (REQ-P21-02): enrich `BANNED_TYPES` in place

**Chosen: annotate `BANNED_TYPES` in place** — promote it from `dict[str, str]` to
`dict[str, dict[str, str]]`, each value a record `{reason, code, citation}`:
`reason` = the existing distortion string; `code` = the banning finding code
(**`DSX-VIZ-001`** for all five — that is the code `_check_banned` emits); `citation` =
the D-05 perception source. `_check_banned` changes at exactly one line
(`detail=BANNED_TYPES[chart_type]["reason"]`); the `in` membership check (viz.py:81) is
unchanged (dict keys). Blast radius = one call site, verified.

**Rejected: a separate parallel `REFUSAL_ENTRIES` sub-map (Auditor, decisive).** A second
map keyed on the same marks introduces a **drift surface** — a mark could be banned but
undocumented, or documented but not banned, which is precisely the "silently absent"
failure REQ-P21-02 exists to prevent. A single enriched registry makes "every banned mark
is a complete refusal entry" a **structural property of one keyset**, not a second
invariant to police. Rigour tier: one source of truth > two synchronized maps.

**Rejected: a `NamedTuple`/dataclass record (Architect, minor).** Typed and immutable, but
introduces a new type on the gate path for five entries against a codebase whose
vocabularies are plain dicts (D-04 house style). A nested `dict[str, dict[str, str]]`
matches the idiom with lower churn. The invariant test (D-01) additionally asserts each
refusal record is non-empty on all three fields — the completeness guarantee lands in the
test, where it belongs, not in a type.

**Zero new codes holds (REQ-P21-03).** The refusal entries cross-reference the **existing**
`DSX-VIZ-001`; the `citation` field is new *metadata*, not a new check. `dual_axis_line`
carries `code: DSX-VIZ-001` (the type ban that `_check_banned` fires); its `dual_axis: true`
property is separately caught by `DSX-VIZ-030` — noted as a "see also" in the record's
reason, not a second banning code.

**D-05 handling for the refusal citations.** The perception citations are HQ-27's **Tier-3
refusal-doctrine** sources (Few / Harris / Tufte / Muth 2018), currently *prepared but
unsigned*. S1-3 **builds** the structure and populates the citation pointers from the
prepared pack; the authoritative locator-signature is **batched to HQ-27 (Tier 3) and
drained at S5-2 — non-blocking for Phase 21 ship**, because REQ-P21-02 adds **no new
blocking gate code** (DSX-VIZ-001 already fires) and the cited rationale is already-live
and uncontested (the `reason` strings shipped long ago). S1-3 must annotate HQ-27's Tier-3
batch with the specific banned-type → source mapping so the human read has concrete targets.

## What Phase 21 execute (S1-3) is now bound to

1. **Home the 12** per D-01's guidance table: add the 9 + `kde` to a `CHART_CAPABILITIES`
   family (or `EXTRA_MARKS[IT]`); add `kde` + `population_pyramid` + `butterfly` to a
   `RELATIONSHIP_CHARTS` value. Do **not** touch `CHART_CAPABILITIES` for
   `population_pyramid`/`butterfly` (already homed via `EXTRA_MARKS[IT011]`).
2. **The every-mark-has-a-home invariant test** (`tests/`, off the gate path): both
   clauses of D-01, plus the frozen `CAPABILITY_ONLY` allowlist (the ~14), plus the
   refusal-record completeness assertion (D-02). It reads `RELATIONSHIP_CHARTS`,
   `CHART_CAPABILITIES`, `EXTRA_MARKS`, the smells sets, and `BANNED_TYPES`.
3. **Enrich `BANNED_TYPES` in place** to `{reason, code, citation}` records (D-02); update
   `_check_banned` at its one call site; annotate HQ-27 Tier-3 with the per-mark citation
   targets.
4. **Phase-end:** catalogue set-identity diff proves **275 → 275**, zero new codes
   (REQ-P21-03), asserted by the same diff mechanism S0-2 used three ways.

## Open questions / carried caveats

- **HQ-28 (veto window, non-blocking):** D-01's two-clause + `CAPABILITY_ONLY` allowlist
  shape and the gate-faithful capability-home definition; D-02's enrich-in-place refusal
  record. Silence = accept; nothing blocks on it.
- **Carried to Phase 22 (catalog spine):** whether any `CAPABILITY_ONLY` mark
  (`column`, `grouped_bar`, …) should be promoted to a relationship home — decided there
  with per-entry relationship citations, not pre-empted in Phase 21.
- **HQ-27 Tier-3** (refusal-doctrine citations) now has a concrete landing site (Phase 21
  refusal entries); non-blocking for Phase 21 ship, drained at S5-2.
- No D-05 read is *owed by Phase 21 to unblock its own build*: homing uses existing family
  semantics (interval-range = univariate distribution, etc.), already citable from shipped
  references; the refusal citations are batched, not blocking (above).
