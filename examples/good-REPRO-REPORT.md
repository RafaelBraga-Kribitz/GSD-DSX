# Reproduce report — onboarding-activation exemplar

This report records a fresh re-run of the analysis figures off the deterministic gate
path (`examples/analysis/charts.py`; the gate never runs the generator). The
deterministic gate reads **only the machine block below** — never this prose — so the
block is kept accurate.

The `status:` field is not a PASS/FAIL verdict the gate trusts. The gate independently
checks whether the reported numbers overlap `results.tests`; `status` only distinguishes
an honest skip from a real run. Every number below was actually observed.

## Machine-readable result

The first fenced block is the one the gate parses. It is a flat `key: value` mapping
(no nesting), read by a stdlib regex. Lines beginning with `#` are ignored.

```yaml
# status: one of  reproduced | mismatch | skipped | unable
status: reproduced
# lead metric (results.tests[0]) first; each value is the FRESH re-run number.
activation_rate: 0.024
retention_d7: 0.016
```

- `status: reproduced` — the figure generator ran and the lead number (activation
  uplift 0.024) overlaps the declared `results.tests[0].effect`.

## Notes

Determinism is structural, not incidental: re-running `examples/analysis/charts.py`
reproduces the sealed SVG bytes for all three figures. The recipe is the Phase-23 style
layer — `dsx_plotstyle.save_deterministic` fixes `svg.hashsalt`, bakes glyphs as paths
(`svg.fonttype: path`), and suppresses the render timestamp (`metadata Date: None`);
the dsx-urban style pins the same salt and fonttype (GA-3). Verified this run: two
consecutive renders produced byte-identical SVGs (`dsx seal` reported identical
`sha256:` digests both times), and those digests match `spec.visuals[].svg_sha256`.

- Renderer: matplotlib 3.11.1 (pinned in `good-FIGURE-MANIFEST.yaml`).
- Data snapshot: `warehouse.fct_signups`, 2026-06-01..06-14 (the readout window).
- Deviation from the declared environment: none.
