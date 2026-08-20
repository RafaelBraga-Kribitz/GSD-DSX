"""Shared test helper: seed a plan-time decision-trail header (Phase 10).

From Phase 10, the decision trail is a gate input at verify and ship
(``dsx/frame/prereg.py::_check_content_lock``): a missing plan-gate-point
header aborts the run at exit 2. Any test that reaches ``dsx gate verify`` or
``dsx gate ship`` against a root with no prior ``dsx gate plan`` run needs a
plan-time header on file first, and this is the one place that fact is
encoded — every test module seeds it the same way, from the same real
primitives a genuine ``dsx gate plan`` run writes with, so the helper cannot
drift from the code under test.

The leading underscore keeps this module outside ``unittest discover``'s
``test*.py`` pattern, so it is importable by the test modules without being
collected as a suite of its own.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dsx.decisions import InvocationHeader, append, decisions_path, frame_digest  # noqa: E402
from dsx.loader import load  # noqa: E402


def seed_plan_header(root: "str | Path", spec_path: "str | Path") -> None:
    """Append a plan-gate-point ``InvocationHeader`` for the spec at
    ``spec_path`` into ``root``'s decision trail.

    Loads the specification with the real ``dsx.loader.load``, computes the
    real ``dsx.decisions.frame_digest`` over it, and appends the real
    ``dsx.decisions.InvocationHeader`` via the real ``dsx.decisions.append`` —
    so this writes exactly the bytes a genuine ``dsx gate plan`` run would
    write, never a stand-in shape that could drift from the writer it stands
    in for.

    ``invocation_id`` and ``dsx_version`` are not read anywhere on
    ``prereg``'s trail-reconciliation path; any string is acceptable for
    both.
    """
    spec = load(str(spec_path))
    append(
        decisions_path(root),
        InvocationHeader(
            invocation_id="INV-SEED",
            gate_point="plan",
            dsx_version="test-seed",
            frame_digest=frame_digest(spec),
        ),
    )
