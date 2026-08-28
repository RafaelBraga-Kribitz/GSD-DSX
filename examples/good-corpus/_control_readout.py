"""Shared reproducibility entrypoint for the good-side control corpus.

Every clean control spec under ``examples/good-corpus/`` declares
``reproducibility.entrypoint: examples/good-corpus/_control_readout.py`` so the
gate's code-pointer check (DSX-REP-030/031) resolves against a committed,
repo-root-relative script. These specs are hand-authored calibration controls,
not live analyses, so this readout is intentionally a documented no-op: it names
where a real readout would live without fabricating numbers a control corpus
must not assert as measured.

The file exists to satisfy the reproducibility contract honestly — a named
entrypoint that resolves — while the corpus stays a pure declaration-level
control set (D-04, REQ-P12-03).
"""


def main() -> int:
    # Control-corpus specs carry no executable analysis; their numbers are
    # illustrative and pinned in each spec's results block. A real analysis would
    # recompute them here from its own extract.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
