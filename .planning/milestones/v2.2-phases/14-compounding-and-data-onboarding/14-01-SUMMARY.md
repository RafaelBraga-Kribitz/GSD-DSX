---
phase: 14-compounding-and-data-onboarding
plan: 01
requirements: [REQ-P14-01]
status: complete
---

# 14-01 SUMMARY — Compounding loop: search dated learnings before framing

**Requirement:** REQ-P14-01 (D-02). Steal the Data Science Plugin's compounding loop —
later sessions search dated learnings before framing.

## What was done

- **Created `docs/dsx/learnings/README.md`** — the schema authority. Fixes the closed
  frontmatter key set in order (`date, title, domain, question_type, tags, metrics,
  phase, source_spec, outcome, supersedes?`), the `YYYY-MM-DD-<slug>.md` filename
  convention (plain sort = chronological), the What/So What/Now What body shape, names
  `gsd-extract-learnings` as the producer of future dated files, states the files are
  written+read+**ungated** (no `dsx` check reads them → mints no code), and carries the
  CRLF authoring note.
- **Created `docs/dsx/learnings/2026-08-28-join-fanout-inflates-additive-metrics.md`** —
  one real dated exemplar carrying every required key (`domain: business_intelligence`,
  `question_type: diagnostic`, `metrics: [revenue]`, `phase: 14`, `source_spec: none`).
  Body is a genuine house finding (no fabricated dataset numbers): a join fan-out ≠ 1.0
  silently inflates additive metrics; fix the grain, don't divide the number down;
  confirm `fanout == 1.0` on every declared one-to-one join before framing.
- **Edited `skills/dsx-scope-analysis/SKILL.md`** — added `<process>` step 0 "Search
  dated learnings before framing" ahead of Scaffold/architect: greps the fixed keys,
  cites `README.md` as authority, records `searched dated learnings: none found` for
  the empty case, names `gsd-extract-learnings` as producer, reuses already-granted
  Grep/Glob/Read (no new grant, no CLI, no gate). `description:` and `allowed-tools:`
  untouched.
- **Edited `capabilities/dsx/fragments/researcher.md`** — one clause on the existing
  "Has this been analysed before?" bullet pointing at `docs/dsx/learnings/`.

## Gate evidence

All three Task verify blocks re-run by the orchestrator: **T1 PASS, T2 PASS, T3 PASS**.
`git status --porcelain -- dsx/` empty (no gate-path edit). No new `DSX-*` code (all
edits are markdown; the catalogue generator walks only `dsx/**/*.py`). Zero-mint
certified phase-wide by 14-05.

## Prohibitions held

- No path under `dsx/` modified. No gate check added for the learnings directory.
- No new tool grant, no `dsx` CLI subcommand.
- Catalogue stays 256 (proved phase-wide by 14-05 set-identity diff).
