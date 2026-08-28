---
id: SEED-002
status: dormant
planted: 2026-08-21
planted_during: v2.0.0 Phase 11.1.1 (Detection-code hardening)
trigger_when: v2.0.0 Phase 12 catch-rate published AND real phases produce EDA.md files that gates ignore
scope: medium — dsx profiler + gate surface; a milestone-level decision, not a quick task
---

# SEED-002: Grow DATA-PROFILE / dsx profile into hermetic EDA artifacts

Grow `DATA-PROFILE.yaml` / `dsx profile` so daily volume, structured missingness, and distribution summaries are hermetic artifacts gates can read. Do not do this before Phase 12.

## Why This Matters

`dsx profile` currently writes only the shallow slice (row count, null rates, unique counts, PK uniqueness, date min/max/gap, sentinels). The insight-producing numbers the explore protocol asks for — daily volume, structured-missingness tables, five-number summaries, categorical tails, base-rate drift — are not in the profile, so an agent can skip every insight step, run `dsx profile`, and still look compliant. Making those numbers hermetic artifacts is the only honest way for gates to ever notice EDA.

## When to Surface

**Trigger (entry condition D-13):** Phase 12 catch-rate is published AND real phases are producing `EDA.md` files that gates ignore. Both must hold — this changes fixtures that Phase 12 measures, so it must not land before calibration ships. The natural home is a v2.2-style milestone (exploratory protocol and profile depth), where extra DATA-PROFILE fields, an optional dsx CLI wrapping the correlation funnel *outside* the gate path, or a non-blocking EDA.md-exists check can be weighed. Revisit D-01/D-02 before any of those become blocking codes.

## Scope Estimate

**Medium.** Touches `dsx/profiler.py`, DATA-PROFILE schema, fixtures, and possibly new non-blocking checks. Explicitly deferred: not implemented in the SEED-001 quick task, not inserted into the 11.x chain.

## Breadcrumbs

- `dsx/profiler.py` — current shallow profile writer
- `references/data-quality-assertions.md` — the judgements that stay stochastic after the numbers exist
- `brief.md` — D-01/D-02 boundaries that any gated growth must renegotiate
- `EDA_enhancement_BRIEF.md` — verdict table and the "do not add in this pass" list
- [[deepen-dsx-explore-data-eda-protocol]] (SEED-001) — the agent-protocol half that runs first

## Notes

Optional companion to SEED-001. SEED-001 deepens the agent protocol without gates; this seed is the later, gated half. If SEED-001 never ships or EDA.md never gets produced in practice, this seed should be discarded rather than promoted.
