---
phase: 16-re-run-verification-off-the-gate-path
plan: 02
status: complete
requirements: [REQ-P16-01]
---

# 16-02 SUMMARY — dsx-reproduce skill + REPRO-REPORT.md template + capability register

## What shipped
- **`templates/REPRO-REPORT.md`** (new) — the report contract. First fenced ```yaml block is a
  FLAT `key: value` mapping with a `status:` field (vocabulary `reproduced | mismatch | skipped |
  unable`) and one `<metric>: <number>` line per headline metric. `#` lines are parser-ignored
  guidance. Header states `status` is NOT a trusted verdict and documents the SKIPPED/UNABLE
  honest opt-out (D-11). Byte-compatible with the CRLF-safe `_check_reproduce_report` parser (D-04).
- **`skills/dsx-reproduce/SKILL.md`** (new) — mirrors the dsx-chart-audit house style. Re-runs
  `reproducibility.entrypoint` OFF the gate path via Bash (the only sanctioned execution site, D-01),
  captures fresh headline numbers, writes REPRO-REPORT.md, sets `status: skipped`/`unable` on a
  missing interpreter (D-11), and stamps `reproducibility.reproduce_report` (opt-in trigger, never
  entrypoint-presence, D-02). States it edits no dsx/ module and asks the gate to trust no verdict line.
- **`capabilities/dsx/capability.json`** — appended `dsx-reproduce` to `skills[]` (now 14); `hooks`
  stays `[]`, no other key changed.

## Gate evidence (all re-run by the orchestrator, brief §5)
- Task 1: template's first fenced yaml block parses under the 16-01 CRLF-safe extractor → `{status: reproduced, activation_rate: 0.024, retention_d7: 0.016}`; `status` present + numeric metric present.
- Task 2: `name: dsx-reproduce` ×1, `reproduce_report` ×2, `skipped|unable` ×1, `REPRO-REPORT.md` ×6.
- Task 3: capability.json valid JSON; `dsx-reproduce` ∈ skills; `hooks == []`.
- Zero dsx/ edits in this plan; catalogue stays at 258 (`--check` exit 0) — no code minted here.
