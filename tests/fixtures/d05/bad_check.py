"""Deliberately violating D-05 fixture. Codes DSX-PAR-999 (fixture-only).

This module exists solely so `check_d05()` in `scripts/gen-finding-catalogue.py`
has a real, committed case to prove enforcement against (ROADMAP Success
Criterion 4, REQ-P6-11). It is scanned by `ast.parse` only — nothing here is
ever imported or executed, so no import of `dsx` is needed (matches
`dsx/checks/design.py`'s module-docstring convention without its imports).

Not named with a `test` prefix: `unittest discover`'s default `test*.py`
pattern must never collect this file as a test module.

`DSX-PAR-999` and `DSX-SPEC-089` are fixture-only codes. They live here, under
`tests/fixtures/`, and must never appear under `dsx/` — `collect()` and
`dsx/suppressions.py::known_codes()` both walk `dsx/` only, so neither ever
sees them.
"""

from __future__ import annotations


def violating_check(report):
    """Emits DSX-PAR-999: a citation with no reference value or structural criterion.

    Citation: Example, A. (2020), "A Study of Something", Table 1.
    """
    report.add("DSX-PAR-999", "HIGH", "deliberately missing reference value")


def compliant_check(report):
    """Emits DSX-SPEC-089: both required docstring lines present.

    Citation: Example, A. (2020), "A Study of Something Else", Table 2.
    Structural criterion: field is present and non-blank.
    """
    report.add("DSX-SPEC-089", "HIGH", "deliberately compliant fixture case")
