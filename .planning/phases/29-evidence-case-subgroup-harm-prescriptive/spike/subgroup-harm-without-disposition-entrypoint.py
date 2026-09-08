"""Reproducibility entrypoint for the subgroup-harm-without-disposition spike.

Read as TEXT by the gate's code-pointer / leakage scan (dsx/checks/code.py) and
NEVER executed on the gate path. Kept a documented no-op, exactly like the
good-corpus control readout it is cloned from (examples/good-corpus/
_control_readout.py): it names where a real readout would live without
fabricating numbers a measurement spike must not assert as measured.

This exists only so the reproducibility contract (DSX-REP-030/031) resolves
against a committed, seedable script during the D-13 measurement. The spike's
numbers are pinned illustratively in the spec's results block.
"""


def main() -> int:
    # No executable analysis: the spike's illustrative numbers are pinned in the
    # spec's results block. A real analysis would recompute them here from its
    # own extract.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
