# Roadmap: gsd-dsx

**Shipped:** v2.0.0 DSX Validity Frame — Phases 6–12 (2026-08-28); v1.1.0–v1.5.0 — Phases 1–5
**Queued:** v2.2 Analytic Surface — Phases 13–16 (entry condition met, not started)

> **Milestone name vs. release tag.** The DSX Validity Frame is named **v2.0.0**
> throughout planning (its archives are `v2.0.0-ROADMAP.md`, `v2.0.0-REQUIREMENTS.md`,
> `v2.0.0-MILESTONE-AUDIT.md`), but it ships under the git tag **`v2.1.0`**. The
> `v2.0.0` tag was already published on origin (2026-08-10) against an earlier,
> partial merge of this same branch, and moving a published ref would silently break
> anyone who had already fetched it — so the completed milestone got the next free
> tag instead. The follow-on **Analytic Surface** milestone was correspondingly
> renamed from v2.1 to **v2.2** so it does not collide with that release tag.

## Milestones

- ✅ **v1.1.0–v1.5.0** — Phases 1–5 (shipped incrementally; ten quality dimensions gated where decidable)
- ✅ **v2.0.0 DSX Validity Frame** — Phases 6–12 (shipped 2026-08-28)

## Phases

<details>
<summary>✅ v1.1.0–v1.5.0 (Phases 1–5) — SHIPPED</summary>

- [x] Phase 1: DQ + Evidence + Coherence (v1.1.0)
- [x] Phase 2: Viz proof + plot construction (v1.2.0)
- [x] Phase 3: Storytelling + code reality (v1.3.0)
- [x] Phase 4: Analytical logic depth + stats extensions (v1.4.0)
- [x] Phase 5: Chart review + suppressions (v1.5.0)

</details>

<details>
<summary>✅ v2.0.0 DSX Validity Frame (Phases 6–12) — SHIPPED 2026-08-28</summary>

Full phase detail archived at `.planning/milestones/v2.0.0-ROADMAP.md`.

- [x] Phase 6: Contract extension, decision record, paradigm manifest (M1) — 13/13 plans — completed 2026-08-10
- [x] Phase 7: Validity frame checks (`DSX-VAL-*`) (M2a) — 8/8 plans — completed 2026-08-20
- [x] Phase 8: Interference, triggering, stability (`DSX-INT-*`) (M2b) — 10/10 plans — completed 2026-08-14
- [x] Phase 9: Monitoring discipline, symmetric (`DSX-PAR-*`) (M2c) — 7/7 plans — completed 2026-08-13
- [x] Phase 10: Pre-registered inference plan (`DSX-PRE-*`) (M3) — 6/6 plans — completed 2026-08-20
- [x] Phase 11: Frequentist admissibility adjudicator (`DSX-ADM-*`) (M4) — 8/8 plans — completed 2026-08-28
- [x] Phase 11.1: Generated-pipeline reality (INSERTED) — 8/8 plans — completed 2026-08-21
- [x] Phase 11.1.1: Detection-code hardening (INSERTED) — 7/7 plans — completed 2026-08-22
- [x] Phase 11.2: Prescriptive claim layer (INSERTED) — 8/8 plans — completed 2026-08-26
- [x] Phase 11.3: Reporting completeness and missing-data discipline (INSERTED) — 7/7 plans — completed 2026-08-27
- [x] Phase 12: Calibration (M5, terminal) — 7/7 plans — completed 2026-08-27

</details>

## Queued milestone — v2.2 Analytic Surface (Phases 13–16)

**Status:** Queued. Not started. Not part of the v2.0.0 53-requirement map.
**Entry condition (D-13):** Phase 12 closed. Recorded in `brief.md` §6.5.
**Research:** `.planning/research/SURFACE.md` (2026-08-26). Comparison-repo READMEs are not D-05 sources.
**Does not reopen:** Phases 7–12, D-01…D-14, the v2.0.0 finding-code families.

Skill-only files that invent no new finding codes (Phases 13–14) may be *drafted* after Phase 6 in parallel. They do not gate v2.0.0. Vocabulary members and new `DSX-*` codes (Phase 15) wait for Phase 12.

Every Phase 15 check that ships is still subject to **D-05**: a primary-source citation naming the exact formulation, and a test against a published reference value (or a named structural criterion). If velocity pressure arrives, cut checks, never this.

### Phase 13: Task playbooks that fill the spec (skill-only)

**Goal**: Steal the Unified Framework's *what to do* for marketing work — cohort, funnel, root-cause, segmentation — as skills that fill `ANALYSIS-SPEC.yaml`, not as notebooks. EDA produces a hypothesis register. Narrative uses What / So What / Now What. Scope-analysis routes three engagement modes onto the ceremony tiers already in `docs/gsd-tiers.md`. The executor prefers `scripts/*.py` over a notebook as the entrypoint.

**Depends on**: Phase 12 to *open* the milestone. Drafting may begin after Phase 6.
**Blocks**: nothing in v2.0.0. Soft-blocks Phase 15's cohort/funnel spec fields — those fields should have a skill that fills them.

**Requirements**: REQ-P13-01, REQ-P13-02, REQ-P13-03, REQ-P13-04, REQ-P13-05, REQ-P13-06

**Ordering constraints**: REQ-P13-06 (no new finding codes) is the scope bound for the whole phase. A skill that "needs" a new code is a Phase 15 item, not a Phase 13 exception.

**Success Criteria** (what must be TRUE):

  1. Skills `dsx-cohort`, `dsx-funnel`, `dsx-root-cause` and `dsx-segment` exist, are registered in `capabilities/dsx/capability.json`, and each writes the relevant `ANALYSIS-SPEC.yaml` fields, pointing at existing gates (metric semantics, multiplicity, chart matrix) rather than inventing parallel advice.

  2. `dsx-explore-data` writes a hypothesis register that maps into `assumptions[]` and/or `results.tests`.

  3. `dsx-narrate` requires an explicit What / So What / Now What shape in the narrative deliverable.

  4. `dsx-scope-analysis` routes lookup → ceremony Tier 0, ad-hoc → Tier 1, full pipeline → Tier 2, matching `docs/gsd-tiers.md`.

  5. The executor fragment prefers `scripts/*.py` over a notebook as `reproducibility.entrypoint`.

  6. The finding catalogue after this phase contains no new `DSX-*` prefixes and no new codes relative to the Phase 12 catalogue — asserted by a catalogue diff, not by review.

**Plans**: TBD (not opened until Phase 12 closes)

### Phase 14: Compounding and data onboarding

**Goal**: Steal the Data Science Plugin's compounding loop and DAAF's data-onboarding skill. Later sessions search dated learnings before framing. A portable `DATA-DICTIONARY.md` sits next to `DATA-PROFILE.yaml`. Research-domain narratives may disclose AI assistance. A CSV-first conversation can start without knowing GSD phase names.

**Depends on**: Phase 12 to open. Soft-depends on Phase 13 for slash aliases covering the new task skills as well as the original eight.
**Blocks**: nothing in v2.0.0.

**Requirements**: REQ-P14-01, REQ-P14-02, REQ-P14-03, REQ-P14-04, REQ-P14-05, REQ-P14-06

**Ordering constraints**: REQ-P14-05 is conditional — if GSD Core exposes no overlay hooks, the requirement is satisfied by a documented skip in the operating guide, not by inventing a hook channel.

**Success Criteria** (what must be TRUE):

  1. `docs/dsx/learnings/` holds dated YAML-frontmatter files. The plan-pre path searches them before framing, the same loop as the plugin's `/ds:plan`.

  2. A `DATA-DICTIONARY.md` is produced next to `DATA-PROFILE.yaml` so later sessions do not re-guess grain and join keys.

  3. When `dsx.domain` is `research`, the narrate skill offers an optional AI-assistance disclosure block (GUIDE-LLM as a template, not a third-party dependency). Marketing-domain default remains unchanged.

  4. Slash-command aliases exist for the DSX skills so a CSV-first conversation has a start as simple as Claude Data Analysis, without a `data_storage/` special folder.

  5. Either a file-drop hook runs `dsx profile`, or the operating guide documents that GSD Core exposes no overlay hooks and the skip is the accepted satisfaction of REQ-P14-05.

  6. No new blocking finding codes ship in this phase.

**Plans**: TBD (not opened until Phase 12 closes)

### Phase 15: CUPED and BI declaration checks (new codes, D-05)

**Goal**: The only v2.2 phase that extends the gate catalogue. *(Amended 2026-08-29 — Phase 16 S3-1 discuss, decisions D-06/D-07: **Phase 16 also extends the catalogue**, minting `DSX-REP-060`/`DSX-REP-061` for the REQ-P16-02 reproduce-report gate check. This corrects the "only" claim; it drops or rewords no requirement. Rationale + veto window: `.planning/phases/16-re-run-verification-off-the-gate-path/16-CONTEXT.md` D-06 and HUMAN-QUEUE HQ-11.)* CUPED becomes a closed-vocabulary member with a pre-experiment covariate check. Thin spec fields for cohort grain and funnel steps catch survivorship and changing denominators as findings. Research-domain work may use an APA table template; marketing-domain stays with narrative + sealed figure + claim evidence. Shapiro–Wilk auto-switch is forbidden.

**Depends on**: Phase 12 (hard — D-13). Soft-depends on Phase 13 so the new fields have a skill that fills them. Does **not** wait on Phase 11's `families.yaml` — `cuped` is added to the existing `VARIANCE_ADJUSTMENTS` set in `dsx/spec.py`, not as a parallel vocabulary (same reasoning as M-09).
**Blocks**: nothing in v2.0.0.

**Requirements**: REQ-P15-01, REQ-P15-02, REQ-P15-03, REQ-P15-04, REQ-P15-05, REQ-P15-06, REQ-P15-07

**Ordering constraints**: REQ-P15-01 before REQ-P15-02 (`cuped` must be a legal vocabulary member before a check can require it). REQ-P15-06 (no Shapiro–Wilk auto-switch) is a negative assertion tested against skills and gate code. A cohort or funnel finding whose D-05 citation is not in hand at implement time is left in `brief.md` §6.5 rather than invented.

**Success Criteria** (what must be TRUE):

  1. `VARIANCE_ADJUSTMENTS` includes `cuped` and `dsx vocab` dumps it. The pre-existing four members (`cluster_robust`, `delta_method`, `bootstrap_cluster`, `mixed_effects`) still round-trip. D-08 fixtures are extended, not replaced.

  2. A spec declaring CUPED with a post-treatment covariate exits `1` at `dsx gate plan`. A spec declaring pre-experiment covariates passes that check. The finding docstring cites Deng, Xu, Kohavi and Walker (2013), WSDM, naming the exact formulation, plus a test against a published worked value. The Unified playbook snippet is not the citation.

  3. `ANALYSIS-SPEC.yaml` accepts thin fields for cohort grain and funnel steps, and the extended good fixture still passes every gate at every threshold.

  4. Survivorship-bias and changing-denominator defects each block their own bad fixture, every new code carrying a D-05 citation. A code without a citation does not ship.

  5. A research-domain optional APA table template exists. Marketing-domain ship still requires narrative + sealed figure + claim evidence. No skill or gate auto-switches a test on Shapiro–Wilk — asserted by test against `references/test-selection.md`'s order (independence, then variance, then normality).

  6. `scripts/gen-finding-catalogue.py --check` exits 0 on the new codes, and both canonical fixtures still satisfy D-08.

**Plans**: TBD (not opened until Phase 12 closes)

### Phase 16: Re-run verification (off the gate path)

**Goal**: Steal DAAF's "reproduced" verdict without putting pandas on the gate. A skill re-runs `reproducibility.entrypoint` and writes `REPRO-REPORT.md`. The gate checks that the report exists and that named numbers overlap. Phase 12 corpus tags gain `protocol_adherence` so "the agent skipped the skill" is countable. Catch rate and false-positive rate remain the calibration numbers.

**Depends on**: Phase 12 (hard — extends calibration tags; the reproduce skill itself does not need the harness, but the tag schema must not fork).
**Blocks**: nothing in v2.0.0.

**Requirements**: REQ-P16-01, REQ-P16-02, REQ-P16-03, REQ-P16-04

**Ordering constraints**: REQ-P16-02 must not execute analysis code on the gate path (D-01/D-02). If a future contributor "simplifies" by calling the entrypoint from `dsx gate`, the phase is failed, not done.

**Success Criteria** (what must be TRUE):

  1. Skill `dsx-reproduce` re-runs `reproducibility.entrypoint`, compares declared `results.tests` to a fresh run, and writes `REPRO-REPORT.md`.

  2. `dsx gate` at verify/ship checks that `REPRO-REPORT.md` exists (when the skill is in use) and that named numbers overlap `results.tests`. It does not import pandas, scipy, or the entrypoint. A missing interpreter on a reproduce *skill* run is not a gate exit `1`.

  3. Phase 12 corpus cases that remain after v2.0.0 carry a `protocol_adherence` field so skipped-skill failures are countable. This extends REQ-P12-02; it does not replace catch rate or false-positive rate.

  4. A test asserts no `dsx/checks/` or `dsx/frame/` module executes the analysis entrypoint.

**Plans**: TBD (not opened until Phase 12 closes)

---

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. DQ + Evidence + Coherence | v1.1.0 | — | Complete | v1.1.0 |
| 2. Viz proof + plot construction | v1.2.0 | — | Complete | v1.2.0 |
| 3. Storytelling + code reality | v1.3.0 | — | Complete | v1.3.0 |
| 4. Analytical logic depth + stats extensions | v1.4.0 | — | Complete | v1.4.0 |
| 5. Chart review + suppressions | v1.5.0 | — | Complete | v1.5.0 |
| 6. Contract extension, decision record, paradigm manifest | v2.0.0 | 13/13 | Complete | 2026-08-10 |
| 7. Validity frame checks (`DSX-VAL-*`) | v2.0.0 | 8/8 | Complete | 2026-08-20 |
| 8. Interference, triggering, stability (`DSX-INT-*`) | v2.0.0 | 10/10 | Complete | 2026-08-14 |
| 9. Monitoring discipline, symmetric (`DSX-PAR-*`) | v2.0.0 | 7/7 | Complete | 2026-08-13 |
| 10. Pre-registered inference plan (`DSX-PRE-*`) | v2.0.0 | 6/6 | Complete | 2026-08-20 |
| 11. Frequentist admissibility adjudicator (`DSX-ADM-*`) | v2.0.0 | 8/8 | Complete | 2026-08-28 |
| 11.1 Generated-pipeline reality | v2.0.0 | 8/8 | Complete | 2026-08-21 |
| 11.1.1 Detection-code hardening | v2.0.0 | 7/7 | Complete | 2026-08-22 |
| 11.2 Prescriptive claim layer | v2.0.0 | 8/8 | Complete | 2026-08-26 |
| 11.3 Reporting completeness | v2.0.0 | 7/7 | Complete | 2026-08-27 |
| 12. Calibration | v2.0.0 | 7/7 | Complete | 2026-08-27 |

**v2.0.0 totals:** 11 phases, 89 plans, 208 tasks. Milestone audit `passed` (`.planning/milestones/v2.0.0-MILESTONE-AUDIT.md`); all 11 phases verified and Nyquist-validated; cross-phase integration INTEGRATED.

Queued (v2.2 Analytic Surface — not v2.0.0 work):

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 13. Task playbooks that fill the spec | 0/TBD | Queued | entry condition met — Phase 12 closed |
| 14. Compounding and data onboarding | 0/TBD | Queued | entry condition met — Phase 12 closed |
| 15. CUPED and BI declaration checks | 0/TBD | Queued | entry condition met — Phase 12 closed |
| 16. Re-run verification (off the gate path) | 0/TBD | Queued | entry condition met — Phase 12 closed |

## Next

v2.0.0 is shipped and archived — full internal dependency graph and the 53-requirement
coverage table are preserved at `.planning/milestones/v2.0.0-ROADMAP.md`. Two dormant
seeds carry forward (deepen `dsx-explore-data` into a reusable EDA protocol; grow
DATA-PROFILE into hermetic EDA artifacts) — see `.planning/STATE.md` Deferred Items.

**v2.2 Analytic Surface's entry condition (D-13: Phase 12 closed) is now satisfied.**
Start it with `/gsd-new-milestone`, or open the queued Phase 13/14 skill-only drafts
directly — see `.planning/REQUIREMENTS.md` "Queued — Milestone v2.2" for requirements
and `brief.md` §6.5 for the entry condition record. Dependency shape (unchanged by
v2.0.0's completion):

```
Phase 12 (M5) ──> Phase 13 ──> Phase 14
                      │
                      └──> Phase 15 (soft: fields those skills fill)
Phase 12 (M5) ──> Phase 16 (extends corpus tags; does not replace calibration numbers)
```
