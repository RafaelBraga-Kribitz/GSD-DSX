---
quick_id: 260821-d6h
status: complete
date: 2026-08-21
commit: 40e015d
---

# Quick Task 260821-d6h — Summary

Deepened `dsx-explore-data` from a data-trust checklist into a protocol that drives
analytical insight. Agent protocol only: `dsx/` is byte-identical, no new finding codes,
no gate reads `EDA.md`, 807 tests green.

## What changed

**`skills/dsx-explore-data/SKILL.md`** — rewritten. The trust core (steps 1–4) is kept and
sub-stepped: grain-and-dependence with the rows-per-unit measurement that determines
`dependence.structure`; join fan-out matrix; a missingness decision table mapping onto the
existing `MCAR/MAR/MNAR/not_assessed` vocabulary; time integrity (staleness, edge periods,
hour fingerprint → `tz_verdict`); classical-vs-robust summaries; concentration; a
four-class outlier taxonomy with one action each; a pathology and impossible-pairs sweep;
and a base-rate producer. Then six question-type branches, each ending in a
`meets | falls_short | re-scope` verdict; segments rewritten around a computed split
ranking and a candidate handshake; a second-order look that attacks the headline with a
closed six-mechanism artifact menu; spec reconciliation as a `confirms / fills /
contradicts` table; three registers (findings, searched-not-found, comparisons); a single
spec-write moment followed by `dsx validate`; a rerun contract; and lifecycle rules.

**`templates/EDA.md`** — new. YAML front-matter contract (the facts downstream steps read)
plus the fixed headings in protocol order, with a CRLF-tolerance authoring note.

**`capabilities/dsx/fragments/executor.md`** — one rule: read `EDA.md` front-matter when
present; its comparisons count seeds `results.comparisons_looked_at`.

**`~/.claude/skills/dsx-explore-data/SKILL.md`** — synced; the user copy previously lacked
even the split-first paragraph.

**`SEED-001`** — records the six deferred enhancements (E-26..E-31) with entry conditions.

## Design provenance

A 10-agent workflow: six dimension researchers (Tukey insight, question-type depth,
data-shape versatility, LLM-agent failure modes, DSX contract integration, external state
of the art) → synthesis into catalog E-01..E-33 → three adversarial critics (constraints,
protocol integrity, completeness). 25 defects were reported; each correction was verified
against the live repo before acceptance, including:

- `DSX-VAL-020`'s real clearing condition is `dependence.method_family_required`
  (`dsx/frame/val.py:270+`) — the grain step now names it.
- `comparisons_looked_at` / `interim_looks` are adjudicated at `dsx/checks/design.py:407+`
  / `:446+`, so the ledger counts at **first computation**; a rerun that re-counted would
  spuriously fire multiplicity and make a fixed-horizon experiment look like peeking.
- ANALYSIS-SPEC has no "pre-declared cuts" field — promotion is a spec amendment adding the
  test to `design.multiplicity.family`.
- `dsx power` is two-proportion arithmetic only; ICC and `outcome_sd` are recorded for
  agent-side design arithmetic, not claimed as CLI inputs.
- Range-shaped data errors have no assertion type and the profiler records no numeric
  min/max — they go to `known_gaps`, not a new assertion key.
- The week-1/week-2 effect ratio is readout-stage; EDA records its inputs instead of
  spending the least-powered possible interim look.
- Differential attrition (per-arm outcome completeness) added — the largest uncovered
  validity threat for a ~60%-experiment workload.

Every judgement fork was closed: all applicable artifact mechanisms are computed rather
than two being chosen; the decomposition dimension is picked by rule with a two-dimension
cap; the outlier categorical search is bounded and ordered.

## Verification

- `python -m unittest discover -s tests` → 807 tests, OK.
- `git diff --stat -- dsx/` → empty.
- The only `DSX-` code the skill names is the pre-existing `DSX-VAL-020`.
- Repo and user skill copies diff clean.
