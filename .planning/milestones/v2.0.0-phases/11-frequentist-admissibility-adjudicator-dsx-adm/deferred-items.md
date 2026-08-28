# Deferred items — Phase 11

Out-of-scope discoveries logged during plan execution, per the executor's scope
boundary rule. Not fixed here; recorded for a later phase or a dedicated cleanup.

## From 11-01 (2026-08-20)

- **`python scripts/gen-finding-catalogue.py --check` prints more "declared twice
  with different text" warnings than 11-01-PLAN.md's `<verification>` section
  names.** The plan expects four (`DSX-SPEC-070` twice, `DSX-VAL-021`,
  `DSX-VAL-060`). The actual run also prints `DSX-COH-030` and `DSX-PAR-002`.
  Both `python -m unittest discover -s tests` (640 tests, OK) and the catalogue
  `--check` itself (exits 0, "finding catalogue is current") still pass — this is
  a drift in the plan's baseline description, not a build failure, and 11-01
  touches no code that could cause it. Not investigated further because it is
  out of scope for a documentation-only plan; whoever next edits
  `dsx/frame/*.py` or `scripts/gen-finding-catalogue.py` should re-baseline the
  expected warning count.
