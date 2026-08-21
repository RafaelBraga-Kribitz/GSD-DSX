---
id: SEED-001
status: dormant
planted: 2026-08-21
planted_during: v2.0.0 Phase 11.1.1 (Detection-code hardening)
trigger_when: v2.0.0 Phase 12 complete, OR a new milestone whose scope includes exploration / agent skills / DATA-PROFILE
scope: small (quick task) — skills/dsx-explore-data, templates/EDA.md, capabilities/dsx/fragments/executor.md; NOT dsx/checks, NOT new DSX-* codes in v2.0.0
---

# SEED-001: Deepen dsx-explore-data into a reusable EDA protocol

Structured `EDA.md`, stop-and-rescope rule, question-type branches after the trust steps, optional correlation-funnel and conversion-funnel routines; keep computation off the gate path (D-01/D-02).

## Why This Matters

The current skill is a strong data-trust checklist (steps 1–4: shape, completeness, time, distributions) but steps 5–6 do not drive insight — they name vague verbs ("correlations", "the headline number") that different agents will implement differently. Two runs do not produce comparable `EDA.md` files, and nothing downstream is forced to consume them. `funnel_correlation_py` (C:\Users\Benutzer1\Dev\funnel_correlation_py) is a good optional hypothesis-ranker for binary targets, but it must not become a gate: gates adjudicate declarations, they do not compute statistics (D-02), and the gate path stays stdlib-only (D-01).

## When to Surface

**Trigger:** v2.0.0 Phase 12 (calibration) has shipped, OR a new milestone whose scope includes exploration, agent skills, or DATA-PROFILE.

Do not promote into v2.0.0: Phase 12 measures the catch rate of gates, and EDA skill text is not a gate. A skill-deepening quick task may run earlier (after 11.1.1 is idle) without touching the roadmap — see EDA_enhancement_BRIEF.md for the quick-task recipe.

## Scope Estimate

**Small — a GSD quick task, not a phase.** Files in scope: `skills/dsx-explore-data/SKILL.md` (keep steps 1–4 as trust core; add stop-and-rescope, question-type branches, structured EDA.md outline, optional funnel routines), new `templates/EDA.md`, a pointer in `capabilities/dsx/fragments/executor.md`, and syncing the user-level skill copy (`~/.claude/skills/dsx-explore-data/SKILL.md`, including the split-first paragraph it currently lacks). Explicitly out of scope: `dsx/checks/`, `dsx/profiler.py`, new `DSX-*` finding codes, pandas/numpy imports in `dsx/`.

## Breadcrumbs

- `skills/dsx-explore-data/SKILL.md` — the protocol to deepen (repo copy is source of truth)
- `references/data-quality-assertions.md` — documents which judgements stay agent-side
- `brief.md` — decisions D-01 (gate path stdlib-only) and D-02 (gates adjudicate declarations, not statistics)
- `capabilities/dsx/fragments/executor.md` — already carries the join-grain rule; should point at the EDA.md contract
- `EDA_enhancement_BRIEF.md` — full evaluation, locked decisions, and the quick-task recipe
- `C:\Users\Benutzer1\Dev\funnel_correlation_py` — reference implementation only (binarize → Pearson → tornado); never vendored into `dsx/`

## Notes

Locked decisions carried from the brief: correlation funnel is optional (skip-with-reason), after steps 1–4 only, training rows only on predictive work, exploratory label with `comparisons_looked_at` incremented, never a causal claim, never a sealed figure. Distinguish correlation funnel from conversion funnel (ordered step drop-off — a separate optional routine). Missingness maps onto the existing `validity_frame.missingness` vocabulary (MCAR / MAR / MNAR / not_assessed); do not invent a parallel vocabulary. EDA.md stays ungated in this pass.
