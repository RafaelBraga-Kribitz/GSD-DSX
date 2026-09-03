---
phase: 22-catalog-spine-uncertainty-heuristic
plan: 04
type: execute
wave: 4
status: complete
requirements:
  - REQ-P22-04
completed: 2026-09-03T04:39Z
---

# 22-04 SUMMARY — 5-layer selection heuristic (route-and-cite) + Pitfall-3 perceptual correction

Wave 4 of the S2-3 execute unit — the last of the four plans, so completing it
checks the S2-3 checkbox. Ships the agent- and human-facing front door to the
catalog and the gate: the five-layer question→chart heuristic as **route-and-cite
edits into the two existing reference files plus the visualize skill — never a
parallel decision tree** — and, in the same pass, corrects the one pre-HQ-27
error still living in `references/chart-selection.md` (the superseded strict
perceptual ordering that D-1 replaced).

Executed inline by the orchestrator (persona-lite, S1-3/22-03 precedent: the plan
left zero design judgment, all gates re-run by the orchestrator on the final tree,
STATE is single-writer). Zero new code minted — doc/skill/test edits only; the
catalogue stays at **276**.

## What shipped

- **`references/chart-selection.md`** — (1) **perceptual line corrected (Pitfall 3)**:
  the old strict arrow chain (`position → length → angle → area → colour saturation
  → volume`) is **removed** and replaced with Cleveland & McGill's **six ranks with
  ties** (rank 3 = length/direction/angle tied; rank 5 = volume/curvature tied;
  rank 6 = shading/colour saturation tied), with the p.536-list / p.537-tie-caveat
  citation and an explicit note that **"density" is absent from the 1984 paper**
  (D-1). (2) A new **"Selection heuristic"** section threading **L2–L5** as
  route-and-cite pointers (L2 relationship → FT nine categories + the 11th
  uncertainty function; L3 admissible mark → chart-catalog.md three axes + gate
  codes DSX-VIZ-012/013; L4 encoding channel → the corrected rank list; L5 show
  uncertainty → the ten Wilke §5.6 members + DSX-VIZ-070/071) — routes to finding
  codes, never restates a numeric threshold. (3) A new **uncertainty relationship
  row** in the selection table (default = error bars; avoid = a point estimate with
  no interval), attributing Wilke §5.6. (4) A top-of-file catalog pointer.
- **`references/question-taxonomy.md`** — a **"Selection heuristic — Layer 1
  (question → task)"** pointer that maps the five existing question types to the
  analytical task, citing **Munzner ch.3** (task taxonomy, Actions × Targets) and
  routing onward to chart-selection.md (L2–L5) and chart-catalog.md (the marks).
  Reuses the existing table; adds no parallel tree.
- **`skills/dsx-visualize/SKILL.md`** — `<method>` step 1 relationship enumeration
  **10 → 11** (adds `uncertainty`); step 6 routes the uncertainty-mark choice to the
  ten Wilke §5.6 members + DSX-VIZ-071 (vocabulary) / DSX-VIZ-070 (property); the
  `<references>` block now points at `@references/chart-catalog.md`.
- **`tests/test_selection_heuristic_docs.py`** (new) — stdlib unittest, 6 clauses,
  all green: (a) eleven relationships in the skill; (b) D-1 tie language + the
  Cleveland-&-McGill-1984 / p.536-p.537 citation present AND the superseded
  saturation→volume chain absent AND `density` never listed as a ranked channel;
  (c) both surfaces reference chart-catalog.md; (d) question-taxonomy.md cites
  Munzner and routes to chart-selection.md; (e) no parallel decision-tree file under
  `references/`; (f) no Abela / Graph-Selection-Matrix citation. CRLF-safe
  (whitespace-collapsed matching), off the gate path by construction.

## Decisions (loud)

- **No-parallel-tree guard = name-pattern, not a fixed filename allowlist.** The
  plan offered either. `references/` carries an operator-local untracked file
  (`The AI Data Scientist.md`); a fixed allowlist would either false-fail or force
  an operator filename into a committed test. The name-pattern guard
  (`decision-tree|selection-tree|chart-decision|decision-flow|flowchart`) encodes
  the structural intent (REQ-P22-04) robustly. Rigour > reliability.
- **`density` correction, not blanket removal.** The plan requires *stating* density
  is absent from the 1984 paper, so the file must name it; the test therefore forbids
  only density *as a ranked channel* (arrow-chain / tied-list adjacency), not the
  negation sentence — matching D-1 exactly.
- **Finding codes verified before citing.** DSX-VIZ-012/013/030/070/071 all confirmed
  live in `dsx/checks/viz.py` (012 = relationship↔mark, 013 = data-signature↔mark)
  before being written into guidance prose — no dangling code reference ships.
- **Heuristic citations limited to the HQ-27-signed set** (Munzner ch.3 + FT
  nine-category axis; Wilke §5.6 for uncertainty). Abela 2008 and Few's Graph
  Selection Matrix dropped entirely (Research Open Question 1, option (a)); no
  triangulation claim across the Ribecca lineage.

## Gates (orchestrator-run, final tree)

- Task 1 verify one-liner: `chart-selection corrected` ✓
- Task 2 verify one-liner: `skill lists 11 relationships; L1 pointer present` ✓
- Task 3 module: `python -m unittest tests.test_selection_heuristic_docs -v` — 6 OK ✓
- Per-wave gate — **full suite `python -m unittest discover -s tests` = 1495 OK**
  (1489 → 1495, +6 = the new doc-conformance module), clean tree (stray
  `DECISIONS.jsonl` cleared per the standing note); the same pre-existing
  declared-twice warnings, unchanged. Catalogue-invariant test green inside the
  suite → **mint unchanged at 276** (zero new code this wave).

## Result

REQ-P22-04 delivered (5-layer heuristic as route-and-cite edits, no parallel tree)
and the REQ-P22-05-adjacent Pitfall-3 perceptual correction folded in. All four
Phase-22 plans (22-01…22-04) are now executed → **S2-3 complete**. Next ledger
unit: **S2-4** (code review + verification of Phase 22, `passed`, incl. the
perceptual-ranking structural-criterion test).
