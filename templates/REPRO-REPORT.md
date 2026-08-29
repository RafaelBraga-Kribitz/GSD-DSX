# Reproduce report

This report records a **fresh re-run** of the analysis `reproducibility.entrypoint`,
performed by the `dsx-reproduce` skill **off the deterministic gate path** (the skill
runs the entrypoint; the gate never does). The deterministic gate reads **only the
machine block below** — never this prose — so keep the block accurate.

The `status:` field is **not** a PASS/FAIL verdict the gate trusts. The gate
independently checks whether the reported numbers overlap `results.tests`; `status`
only distinguishes an honest skip from a real run. A `status:` of `skipped` or
`unable` is the honest opt-out for a missing interpreter or an entrypoint that cannot
run — no fresh numbers are written, and the gate honours it **without exiting 1**
(it does not fabricate a reproduced verdict). Never write a number you did not
actually observe.

## Machine-readable result

The first fenced block below is the one the gate parses. Keep it a **flat**
`key: value` mapping (no nesting) so it is read by a stdlib regex, not a YAML library.
Lines beginning with `#` are ignored by the parser and may be used for guidance.

```yaml
# status: one of  reproduced | mismatch | skipped | unable
status: reproduced
# one line per headline metric from results.tests, keyed by metric name, lead
# metric (results.tests[0]) first; each value is the FRESH re-run number.
activation_rate: 0.024
retention_d7: 0.016
```

- `status: reproduced` — the entrypoint ran and the lead number overlaps the declared
  `results.tests[0]`.
- `status: mismatch` — the entrypoint ran but a headline number disagrees.
- `status: skipped` / `status: unable` — the entrypoint could not be run (e.g. a
  missing interpreter); no fresh numbers are reported and the gate does not exit 1.

## Notes

Record here anything a human should know about the re-run: interpreter version, data
snapshot, and any deviation from the declared environment. This prose is informational
only — the gate reads the machine block above.
