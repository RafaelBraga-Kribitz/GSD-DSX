---
phase: 14-compounding-and-data-onboarding
plan: 03
requirements: [REQ-P14-03]
status: complete
---

# 14-03 SUMMARY — Research-domain AI-assistance disclosure (opt-in, guarded)

**Requirement:** REQ-P14-03 (D-04). When `dsx.domain == research`, `dsx-narrate` offers
an optional AI-assistance disclosure block; the marketing-domain default is unchanged.

## What was done

- **Created `templates/DISCLOSURE-research.md`** — GUIDE-LLM-derived template authored
  in-repo. States explicitly GUIDE-LLM is a **template/structure, not a third-party
  dependency** (nothing installed/imported). One stable level-2 disclosure heading
  (`## AI-assistance disclosure`) with the four GUIDE-LLM sub-parts: AI-assisted steps,
  human-reviewed decisions, data handling, reproducibility. States the file is
  research-only, optional, and **ungated** (no `dsx` check reads it → mints no code).
- **Edited `skills/dsx-narrate/SKILL.md`** — added a `<disclosure>` step after
  `</structure>`: reads `dsx.domain` via `gsd-tools.cjs config-get dsx.domain`; **only**
  on the literal `research` value offers to append the block from the template; **opt-in
  with skip-with-reason**. States non-research values — including `auto` and
  `marketing_science` — take today's path **byte-unchanged** (no new section, no
  reordering, no disclosure heading, by construction of the guard). Inherits the
  What/So What/Now What layer's rule: mints no new narrative code, adds no
  heading-scanner gate. `description:`/`allowed-tools:` untouched; five `<structure>`
  sections not reordered.

## Gate evidence

Both Task verify blocks re-run by the orchestrator: **T1 PASS, T2 PASS**. (Caught and
fixed one authoring slip: an early draft of the disclosure step contained the literal
`dsx/checks/` string, which would have tripped the plan's `! grep dsx/checks/`
assertion — reworded to "no gate check anywhere on the deterministic path" before
gating.) `description:` confirmed unchanged. `git status --porcelain -- dsx/` empty.
Golden property holds structurally: `dsx.domain != research` emits no disclosure heading
by construction. Zero-mint certified phase-wide by 14-05.

## Prohibitions held

- No path under `dsx/` modified. No DSX-NAR mint, no heading-scanner gate.
- Marketing/auto and every non-research value byte-unchanged (conditional guard on the
  literal `research` value; five structure sections not reordered).
- Catalogue stays 256 (proved phase-wide by 14-05 set-identity diff).
