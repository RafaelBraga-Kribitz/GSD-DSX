---
name: dsx-reproduce
description: "Re-run reproducibility.entrypoint OFF the gate path, compare the fresh headline numbers to declared results.tests, and write REPRO-REPORT.md with a machine-readable number block + status. Use to substantiate (or honestly decline) the reproduced verdict the gate then checks. Triggers: 'reproduce this analysis', 're-run the entrypoint', 'did the numbers reproduce' — routes intent without GSD phase names."
argument-hint: "[--phase-dir <path>] [--spec <path>]"
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
---

<objective>
Produce a schema-valid REPRO-REPORT.md whose machine block substantiates — or
honestly declines — the reproduced verdict, then opt the spec in
(`reproducibility.reproduce_report`) so the deterministic gate evaluates it. The
skill is the ONLY sanctioned place the entrypoint runs; the gate re-runs nothing.
</objective>

<process>

1. Resolve `PHASE_DIR` from `--phase-dir` (or the current GSD phase) and locate the
   ANALYSIS-SPEC (`--spec` or `$PHASE_DIR/ANALYSIS-SPEC.yaml`). Read
   `reproducibility.entrypoint` and `results.tests` — the entrypoint tells you what to
   run; `results.tests` gives the declared headline numbers (lead metric = `tests[0]`).

2. **Re-run the entrypoint OFF the gate path**, in this skill's runtime only, via Bash:
   ```bash
   ${DSX_PYTHON:-python3} <entrypoint>        # or the command the entrypoint names
   ```
   This is the only place the entrypoint is executed. No dsx gate module runs it.

3. Capture the fresh headline number for each metric in `results.tests` (lead metric
   first). Read them from the run's own output — never invent one.

4. Fill `templates/REPRO-REPORT.md`. Write the fenced `yaml` block with one
   `<metric>: <fresh number>` line per headline metric (lead metric first), and set:
   - `status: reproduced` when the lead fresh number overlaps declared
     `results.tests[0]` (within a rounding tolerance),
   - `status: mismatch` when it does not.
   Write the report to `$PHASE_DIR/REPRO-REPORT.md`.

5. **If the interpreter is absent or the entrypoint cannot run**, write the report with
   `status: skipped` (or `status: unable`) and **no fabricated numbers**. This is the
   honest opt-out: the gate honours it without exiting 1 (D-11). Never write a number
   you did not observe to force a green gate.

6. Stamp `reproducibility.reproduce_report: REPRO-REPORT.md` into the ANALYSIS-SPEC (the
   opt-in path string) so `dsx gate verify`/`ship` then evaluates DSX-REP-060/061. This
   is the trigger the gate reads — gate behaviour is NEVER keyed on entrypoint-presence.

7. Surface the `status` and the per-metric comparison (declared vs fresh) to the user.

This skill **never edits any `dsx/` gate module** and **never asks the gate to trust a
PASS/FAIL line** — the gate re-derives overlap from the numbers alone. Producing the
report here (execution) and checking it there (declaration) sit on opposite sides of the
gate-path-purity boundary the phase defends.

</process>

<references>
@templates/REPRO-REPORT.md
@references/finding-codes.md
</references>
