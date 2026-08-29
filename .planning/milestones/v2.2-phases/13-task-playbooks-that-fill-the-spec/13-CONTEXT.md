# Phase 13: Task playbooks that fill the spec (skill-only) — Context

**Gathered:** 2026-08-28 (assumptions mode; headless ceremony — AskUserQuestion gates replaced by an Architect-led 2-persona round per LOOP-BRIEF §4)
**Status:** Ready for planning
**Order:** 1st of 4 in v2.2 execution order (13 → 14 → 16 → 15)

<domain>
## Phase Boundary

Phase 13 is a **skill-only, prompt-guidance** phase. It steals the Unified Framework's *what to
do* for marketing work — cohort, funnel, root-cause, segmentation — as **skills that fill
`ANALYSIS-SPEC.yaml`**, not as notebooks or new gates. Its entire product is markdown and one
JSON edit: four new `skills/<name>/SKILL.md` playbooks, three edits to existing skills/fragments,
and a scope-bound test. **It mints ZERO new `DSX-*` finding codes and touches nothing on the
deterministic `dsx gate` path.**

Scope anchor (ROADMAP.md §"Phase 13", REQ-P13-01..06):

- REQ-P13-01 — Skills `dsx-cohort`, `dsx-funnel`, `dsx-root-cause`, `dsx-segment` exist, are
  registered in `capabilities/dsx/capability.json`, and each fills the relevant
  `ANALYSIS-SPEC.yaml` fields **pointing at existing gates (metric semantics, multiplicity, chart
  matrix) rather than inventing parallel advice**.
- REQ-P13-02 — `dsx-explore-data` writes a **hypothesis register** that maps into `assumptions[]`
  and/or `results.tests`.
- REQ-P13-03 — `dsx-narrate` uses an explicit **What / So What / Now What** shape in the narrative
  deliverable.
- REQ-P13-04 — `dsx-scope-analysis` routes **lookup → Tier 0, ad-hoc → Tier 1, full pipeline →
  Tier 2**, matching `docs/gsd-tiers.md`.
- REQ-P13-05 — The **executor fragment** prefers `scripts/*.py` over a notebook as
  `reproducibility.entrypoint`.
- REQ-P13-06 — **No new `DSX-*` finding codes ship** — asserted by a **catalogue diff** against
  the Phase 12 catalogue (the whole-phase scope bound; a skill that "needs" a new code is a Phase
  15 item, not a Phase 13 exception).

**Verified baseline (orchestrator re-ran, 2026-08-28):** the current catalogue is **256 codes**
(`references/finding-codes.md:16` "Total: 256 codes." and an independent distinct-`DSX-*` grep both
= 256); `python scripts/gen-finding-catalogue.py --check` exits **0** ("finding catalogue is
current"); the pre-existing `DSX-VAL-060 declared twice` warning is shipped-tree noise the S0-2
recheck already flagged and does not change `len(rows)`. The Phase-12 count, the shipped v2.0.0
total, and the current total are the **same 256** — no discrepancy to reconcile.

**Not in scope:** any new detection check; any `report.add("DSX-…")` under `dsx/`; any change to
`CHECKS`/`GATE_PROFILES` (`dsx/cli.py:64-131`); any Python under `skills/` or `capabilities/`; a
heading-scanner narrative gate (REQ-P13-03 is template-only); a notebook-blocking entrypoint gate
(REQ-P13-05 is fragment guidance); tier auto-mutation from inside the scope skill (REQ-P13-04 is
advisory). Phase 16 owns `dsx-reproduce`; Phase 15 owns the new codes and vocabulary. These are
named in Deferred Ideas.

**Pre-requisite for planning (S1-2), not a scope change.** `init phase-op --phase 13` currently
returns `phase_found:false` / `expected_phase_dir:null` because the v2.2 phases still sit under
`.planning/ROADMAP.md:52` "## Queued milestone — v2.2 Analytic Surface" while the active
`## Milestones` (`:15`) and `## Phases` (`:20`) sections still describe v2.0.0. Before
`/gsd-plan-phase 13` can resolve the phase, S1-2 must **promote the v2.2 section into the active
milestone/phase structure** (same class of structural repoint as the S0-1 STATE reconcile — the 23
requirements are unchanged, so it is not a §4 scope escalation). The expected phase dir by
convention is `.planning/phases/13-task-playbooks-that-fill-the-spec/` (`<num>-<slug>`, unpadded, per
the archived v2.0.0 dirs).
</domain>

<decisions>
## Implementation Decisions

Every decision below was settled by an **Architect-led 2-persona round** (Architect
`dsx-analysis-architect` = lead, on spec shape / field-filling contracts / tier routing; Auditor
`dsx-ml-integrity-auditor` = adversary, on the no-new-codes bound, gate-path purity and
parallel-advice hazard; both opus/high, concurrent), tie-break **rigour > reliability >
flexibility**. They are loud and **vetoable via the daily summary** (LOOP-BRIEF §4); none is a
HUMAN-QUEUE escalation because none mints a D-06 finding code, changes a numbered requirement, or is
destructive. Phase 13 mints no irreversible artifact — it adds no code and no vocabulary member.

### Skill packaging and registration

- **D-01 (packaging):** The four playbooks are **pure prompt-guidance skills** — one
  `skills/<name>/SKILL.md` each (`dsx-cohort`, `dsx-funnel`, `dsx-root-cause`, `dsx-segment`),
  plus a four-line append to the `capability.json` `"skills"` array (`capability.json:35-45`).
  **No** `steps`/`contributions`/`gates`/`agents` entry: only `dsx-scope-analysis` is loop-wired
  (`capability.json:126-134`); the other eight registered skills appear **only** in the flat
  `"skills"` array and are invoked by name — matching that is the whole point of an on-demand "reach
  for it when the question is a cohort/funnel/root-cause/segment question" playbook. Loop-wiring an
  advisory playbook would fire it unconditionally at a loop point — an unrequested behaviour change.
  Frontmatter mirrors the house shape (`name`/`description`/`argument-hint`/`allowed-tools`,
  `skills/dsx-define-metrics/SKILL.md:1-13`). **No Python** is added under `skills/` or
  `capabilities/` (both trees are Python-free today; the catalogue generator only walks `dsx/**/*.py`,
  `gen-finding-catalogue.py:226-243`, so markdown/JSON here is structurally incapable of minting a
  code).

### The field→gate contract (REQ-P13-01, "route, don't reinvent")

- **D-02 (field-filling contract):** Each playbook is expressed as *which existing spec field it
  writes* and *which already-shipped gate reads that field* — zero parallel advice. Locked contract:

  | Skill | Writes these existing `ANALYSIS-SPEC.yaml` fields | Existing gate each field points at |
  |---|---|---|
  | **dsx-cohort** | retention-ratio `metrics[]`; a `data_input_type: matrix` cohort visual; `decision.revisit_when` | metric semantics `DSX-SPEC-020..026` (`spec.py:892-971`) + `DSX-MET-*`; chart matrix `dsx charts`→`DSX-VIZ-013` (`spec.py:290-319`, `cli.py:1060-1063`); coherence `DSX-COH-040` on `revisit_when` (`spec.py:755-777`) |
  | **dsx-funnel** | step-conversion `metrics[]`; an `event-time` visual with the `funnel` mark | chart matrix (`funnel` admitted only under `event-time`, `spec.py:311-312`, else `DSX-VIZ-013`); `DSX-MET-*`; the existing conversion-funnel ordering routine (`dsx-explore-data/SKILL.md:552-559`) |
  | **dsx-root-cause** | `question_type: diagnostic` (`spec.py:22-28`); `results.segments {name,effect,n}` | Simpson/mix `DSX-MET-030` CRITICAL / `DSX-MET-031` HIGH; causal guard keeps a *diagnostic* label under `DSX-CAU-*`/`DSX-COH-001/010`; mirrors EDA branch 5B decomposition (`dsx-explore-data/SKILL.md:356-386`) |
  | **dsx-segment** | `design.multiplicity.family[]` + `correction`; `results.segments`; `results.comparisons_looked_at` | multiplicity `DSX-SPEC-043` (`spec.py:1046-1055`) + `DSX-EXP-050/051/052/053` (`design.py:362-412`); Simpson `DSX-MET-030/031` |

  **Enforcement (the anti-parallel-advice rule):** a playbook **may** name a gate + its finding
  code and tell the analyst to run `dsx gate/check`; it **may not** state a numeric threshold,
  correction method, or admissible-chart rule of its own — those live in the deterministic check.
  The catch is a plan-checker/review step (S1-4) asserting every threshold/number in the four
  `SKILL.md` files is either absent or immediately attributed to a `DSX-*` code — mirroring how the
  existing executor fragment cites `DSX-MET-040` rather than restating the SQL rule
  (`fragments/executor.md:34-35`).

### Hypothesis register (REQ-P13-02)

- **D-03 (carrier = both existing carriers, keyed by shape):** `dsx-explore-data` resolves the
  "assumptions[] and/or results.tests" by a **deterministic router**, not a new schema:
  - a hypothesis that is an *untested belief the analysis rests on* → `assumptions[]`
    `{assumption, rationale, impact_if_wrong, checked, waiver}`, adjudicated by `DSX-COH-030`
    (present-when-causal/prescriptive) and `DSX-COH-031` (each row `checked:true` XOR `waiver`)
    (`finding-codes.md:332-333`);
  - a hypothesis *promoted to a confirmatory test* → declared in `design.multiplicity.family[]` at
    scope time, filled in `results.tests[]` at execute, adjudicated by `DSX-EXP-050..053`
    (`design.py:362-412`).

  The "register" itself is the **existing `EDA.md` findings/comparisons ledgers**
  (`dsx-explore-data/SKILL.md:664-751`); REQ-P13-02 is the *mapping rule*, and it reuses the
  candidate→confirmatory promotion path the skill already ships ("promoted only by a spec amendment
  adding the test to `design.multiplicity.family`; never promotes a candidate into
  `decision.replay`", `:586-599`). Mints nothing.

### What / So What / Now What (REQ-P13-03)

- **D-04 (template-only, no `DSX-NAR` mint):** The narrative gate has **no section/shape check** to
  ride — `dsx/checks/narrative.py` emits only `DSX-NAR-001`/`-010` (path), a claim⊆deliverable
  check, and the forbidden-wording scan (`:17-61`); the current `dsx-narrate/SKILL.md` has no
  "So What"/"Now What" wording (grep = 0). So the three-part shape is a **skill-template
  requirement**, mapped onto the five parts the skill already prescribes
  (`dsx-narrate/SKILL.md:26-35`): **What** = the answer (§1); **So What** = what it means / the
  action the pre-declared rule implies (§2); **Now What** = what would change it (§4), which for
  prescriptive/experiment readouts cites the gate-read `decision.revisit_when` (already enforced by
  `DSX-COH-040`) and the non-empty `limitations[]` (already enforced by `DSX-CLM-080`,
  `finding-codes.md:223`). The shape gets as much teeth as the *existing* codes allow and mints
  none. **Do not** add a heading-scanner `DSX-NAR-0xx` — it would move the catalogue off 256 and
  fail S1-5.

### Tier routing (REQ-P13-04)

- **D-05 (advisory, not a config mutation):** `dsx-scope-analysis` **classifies** the engagement,
  **recommends** the tier, and **emits the exact command** (`pwsh scripts/gsd-tier.ps1 -Tier N`) —
  it does **not** call `config-set` itself. Fixed mapping, cross-checked to `docs/gsd-tiers.md:39-56`:
  **lookup → Tier 0 exploratory** (`dsx.enforce=false`, throwaway); **ad-hoc → Tier 1 published
  artifact** (`dsx.enforce=true`, DS gates on); **full pipeline → Tier 2 code others run**
  (full ceremony, `mode=interactive`). Rationale: `gsd-tier.ps1` flips global `workflow.*`,
  `granularity`, `model_profile` and `mode` in one shot (`docs/gsd-tiers.md:27-56`); a spec-scoping
  skill silently switching the whole project to `interactive`/`quality` mid-loop is an unauditable
  side effect outside its remit. Rigour forbids the side effect; the deterministic mapping still
  matches the doc.

### Executor entrypoint preference (REQ-P13-05)

- **D-06 (one fragment bullet, riding two shipped checks):** Add a prose bullet to
  `capabilities/dsx/fragments/executor.md` preferring a `scripts/*.py` entrypoint over a notebook,
  citing the two checks that already make a script strictly preferable: `DSX-REP-040` fires HIGH on
  an `.ipynb` entrypoint unless `runs_clean_top_to_bottom`, and its own remedy is "move the logic
  into a module the notebook imports" (`dsx/checks/repro.py:176-197`); and the `DSX-CODE` fit-order
  scan reads notebook JSON line offsets "which a user cannot usefully open" versus scanning `.py`
  source directly (`dsx/checks/code.py:5-13`). The deterministic gate stays **suffix-neutral**
  (`code.py` reads `.py` and `.ipynb` identically, `:4-24`) — no code minted, no gate behaviour
  changed. **Reproducibility rationale to state (advisory, not a leakage claim):** a linear `.py`
  makes `reproducibility.entrypoint` a faithful record of execution *order*, removing the out-of-order
  cell-counter ambiguity a saved `.ipynb` can encode — this is *ordering fidelity*, **not** leakage
  detection, and must not be sold as making code leak-free.

### The scope-bound gate (REQ-P13-06 → S1-5)

- **D-07 (assert by set-diff, not by count alone):** The ledger's S1-5 wording is "assert by diff,
  not by review", and a diff is a **set comparison**, strictly stronger than a count. The existing
  count invariant (`tests/test_finding_catalogue_invariant.py`, `_EXPECTED_TOTAL = 256`, two
  CRLF-safe independent readings) catches any pure *addition* (it raises `len(rows)` above 256) but
  leaves a **swap hole**: a mint-one/drop-one that preserves cardinality passes it. So S1-5 rides
  **both**: (a) `gen-finding-catalogue.py --check` exit 0 + the count invariant stay green, **and**
  (b) a **set-identity diff** against a frozen Phase-12 code-set snapshot committed under
  `tests/fixtures/` (a byte-copy of the *generated* `references/finding-codes.md`, not hand-edited,
  to avoid formatting false-fails), asserting `current_code_set == phase12_code_set`. Regex must be
  CRLF-tolerant (`\r?\n`, repo checks out CRLF). This is the orchestrator tie-break under
  **rigour > reliability**: the stronger assertion is the required one. Whether (b) is a new test
  file or an extension of the existing D-18 invariant test is a planner choice.

### Finding-code footprint

- **D-08 (zero mint; naming caveat):** Phase 13 mints **ZERO** `DSX-*` codes; the catalogue stays
  256, unchanged. Registration, field-filling, hypothesis routing, the narrate shape, tier routing
  and the entrypoint preference are all prompt/JSON/markdown — none registers a check.
  **Naming caveat to hold:** `DSX-COH-*` is **"Coherence", not "Cohort"** (`finding-codes.md:323-334`).
  `dsx-cohort` routes to the *coherence* `revisit_when` check `DSX-COH-040`; its `SKILL.md` must **not**
  imply a `DSX-COH*` "cohort" code family exists (that phrasing would read as minting a family).
  State it as: cohort points at the existing coherence `revisit_when` check.

### Claude's Discretion (planner)

- Exact `SKILL.md` prose and section ordering within each of the four playbooks; the precise
  `argument-hint` strings.
- Whether the hypothesis register gets its own `templates/` heading or rides the existing `EDA.md`
  ledgers (D-03).
- Whether the REQ-P13-06 set-diff (D-07b) is a new test file or an extension of the existing D-18
  catalogue-invariant test (`tests/test_finding_catalogue_invariant.py`).
- Whether tier auto-apply is ever offered — and if so, only behind an **explicit operator opt-in
  flag**, never as an ungated side effect of writing a spec (D-05).

### Folded Todos

None checked at discuss time — resolve `todo.match-phase 13` during planning (S1-2).
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents (researcher, planner) MUST read these before planning or implementing.**

- `.planning/ROADMAP.md` — §"Phase 13" (goal, 6 success criteria, the REQ-P13-06 scope-bound
  ordering constraint, `:63-88`); and the active-milestone reconciliation the plan step must do
  first (`:15`, `:20`, `:52`).
- `.planning/REQUIREMENTS.md` — REQ-P13-01..06 (`:331-336`).
- `capabilities/dsx/capability.json` — `"skills"` array (`:35-45`, the four-name append target);
  `steps`/`contributions` (`:125-192`, proof the eight non-scope skills are unwired); `dsx.causal_guard`
  (`:72-76`); the "entrypoint fit order" phrase (`:6`).
- `dsx/spec.py` — `question_type` (`:22-28`); `CHART_CAPABILITIES` incl. `matrix`/`event-time`+`funnel`
  (`:290-319`); `revisit_when_is_discriminating` (`:755-777`); metric structural checks (`:892-971`);
  `DSX-SPEC-043` multiplicity (`:1046-1055`).
- `dsx/checks/` — `repro.py:147-197` (`DSX-REP-030/031/040`); `design.py:362-412` (`DSX-EXP-050..053`)
  + causal `DSX-CAU-*` (`:41`, `:550-593`); `code.py:4-24` (suffix-neutral scan + notebook-JSON caveat);
  `narrative.py:17-61` (no shape check to ride); `metrics.py` (`DSX-MET-*`); `viz.py:67-180` (`DSX-VIZ-013`).
- `dsx/cli.py` — `CHECKS` (`:64-85`) and `GATE_PROFILES` (`:115-131`) — **must remain untouched**;
  `cmd_charts` (`:504`, `:1060-1063`).
- `docs/gsd-tiers.md:39-56` — the Tier 0/1/2 table + `gsd-tier.ps1` (the REQ-P13-04 routing target).
- `skills/dsx-explore-data/SKILL.md` — 5B diagnostic (`:356-386`), conversion-funnel routine (`:552-559`),
  candidate→confirmatory handshake (`:586-599`), the `EDA.md` ledgers = the register (`:664-751`).
- `skills/dsx-narrate/SKILL.md:26-64`; `skills/dsx-define-metrics/SKILL.md:1-13` (frontmatter shape).
- `references/finding-codes.md:16` (Total: 256 — the REQ-P13-06 baseline).
- `scripts/gen-finding-catalogue.py` (`collect` `:226-243`, `render` `:263`, `--check` `:435-453`) and
  `tests/test_finding_catalogue_invariant.py` (`_EXPECTED_TOTAL=256`, D-18 mechanism) — the S1-5 gate.
- `.planning/milestones/v2.0.0-phases/12-calibration/12-CONTEXT.md:197-202` — Phase-12 **D-18**
  catalogue-invariant test = the REQ-P13-06 reusable asset.
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **Frontmatter template** for all four new `SKILL.md`: `skills/dsx-define-metrics/SKILL.md:1-13`
  (`name`/`description`/`argument-hint`/`allowed-tools`).
- **Candidate→confirmatory promotion path** to reuse verbatim for the hypothesis register:
  `dsx-explore-data/SKILL.md:586-599`.
- **Diagnostic decomposition body** `dsx-root-cause` should mirror (not re-write):
  `dsx-explore-data/SKILL.md:356-386` (5B).
- **Conversion-funnel integrity routine** `dsx-funnel` should route to, not duplicate:
  `dsx-explore-data/SKILL.md:552-559`.
- **`dsx charts` matrix + `DSX-VIZ-013`** as the chart gate the cohort/funnel visuals consult:
  `dsx/cli.py:1060-1063`, `dsx/spec.py:290-319`.
- **Catalogue-invariant test** to reuse/extend for REQ-P13-06: the Phase-12 D-18 test
  (`tests/test_finding_catalogue_invariant.py`; design in `12-CONTEXT.md:197-202`).

### Established Patterns
- **Route-and-cite, never restate** (11.x house style): the executor fragment cites `DSX-MET-040`
  rather than repeating the SQL rule (`fragments/executor.md:34-35`). The four playbooks follow this
  — name the field + the code, defer the number to the deterministic check.
- **Gate-path purity by construction:** the catalogue generator walks only `dsx/**/*.py`
  (`gen-finding-catalogue.py:226-229`); markdown skills and JSON registry entries cannot mint a code.
  The deterministic path lives entirely in `dsx/` — Phase 13 stays out of it.
- **Prompt-guidance vs gate:** REQ-P13-03 (narrate shape) and REQ-P13-05 (entrypoint preference) are
  additive prompt edits precisely because the relevant gates (`narrative.py`, `code.py`) have no
  matching check to ride and are deliberately shape-/suffix-neutral.

### Integration Points
- **`skills/dsx-{cohort,funnel,root-cause,segment}/SKILL.md`** — four new files.
- **`capabilities/dsx/capability.json`** — one four-line `"skills"` append (`:35-45`); nothing else.
- **`skills/dsx-explore-data/SKILL.md`** — hypothesis-register mapping rule (D-03).
- **`skills/dsx-narrate/SKILL.md`** — the three-part template shape (D-04).
- **`skills/dsx-scope-analysis/SKILL.md`** (and possibly `capabilities/dsx/fragments/scope-analysis.md`)
  — the advisory tier-routing table (D-05).
- **`capabilities/dsx/fragments/executor.md`** — one entrypoint-preference bullet (D-06).
- **`tests/`** — the REQ-P13-06 count invariant (green) + the new set-identity diff snapshot (D-07).
- **`dsx/cli.py:64-131`, `dsx/checks/*`** — **read-only**; Phase 13 must not edit these.
</code_context>

<specifics>
## Specific Ideas

- REQ-P13-06 is the phase's centre of gravity: every other requirement was shaped to be deliverable
  *without* a new code. The single genuine rigour decision (D-07) is that "diff" means set-identity,
  not count — a count invariant passes a mint-one/drop-one swap, which is exactly the laundering the
  house style exists to block. The frozen snapshot must be a generated byte-copy, not hand-authored.
- The four playbooks are routers, not authors: the D-02 table is the acceptance test for
  "no parallel advice" — a `SKILL.md` section carrying a threshold with no field→code cell is the
  smell the S1-4 review greps for.
</specifics>

<deferred>
## Deferred Ideas

- **`dsx-reproduce`** — Phase 16's skill, not Phase 13 (the S0-2 recheck listed it among the absent
  target skills; it belongs to the re-run-verification phase).
- **New codes / vocabulary members (`cuped`, cohort/funnel declaration checks)** — Phase 15 only,
  under D-05/D-06. A Phase 13 skill that "needs" one is out of scope by REQ-P13-06.
- **Tier auto-apply** from inside `dsx-scope-analysis` — only if a later phase adds an explicit
  operator opt-in flag; never an ungated `config-set` side effect (D-05).
- **A narrative shape gate (`DSX-NAR` section check)** — would require minting a code; deferred to a
  future milestone that opens the catalogue, if ever wanted (D-04).
- **Carried v2.2 seeds:** `SEED-001` (deepen `dsx-explore-data` EDA protocol) and `SEED-002` (grow
  `data-profile` hermetic EDA artifacts) touch `dsx-explore-data` and may inform D-03's register
  shape, but are dormant future work, not Phase 13 scope.

### Reviewed Todos (not folded)
None — resolve `todo.match-phase 13` at planning (S1-2).

### D-05 pre-registration note
Phase 13 mints no code and therefore owes **no** D-05 primary-source read. The milestone's only
D-05 obligations remain Phase 15's (filed early as HUMAN-QUEUE HQ-8).
</deferred>
</content>
</invoke>
