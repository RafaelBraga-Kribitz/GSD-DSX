"""The frame package — cross-cutting validity-frame and paradigm checks.

Frame checks read across the whole spec (the estimand, the declared analysis
paradigm, the interference structure) rather than owning one narrow slice of
it the way a ``dsx/checks/*.py`` module does. Each frame family gets its own
code prefix and its own module, added as its phase ships:

    family                       prefix        phase
    paradigm manifest            DSX-PAR-*     Phase 6 (this phase — DSX-PAR-001)
    paradigm monitoring pair     DSX-PAR-*     Phase 9  (DSX-PAR-010/011, symmetric)
    validity frame               DSX-VAL-*     Phase 7
    interference / SUTVA         DSX-INT-*     Phase 8
    pre-registration             DSX-PRE-*     Phase 10
    admissibility                DSX-ADM-*     Phase 11

D-03a boundary (enforced mechanically by ``tests/test_frame_boundary.py``):
a module under ``dsx/frame/`` may import from ``dsx.findings``, ``dsx.spec``,
``dsx.loader``, ``dsx.decisions`` and ``dsx.mathx`` — and never from
``dsx.checks``. ``dsx.mathx`` is a pure-computation helper module (stdlib-only
numeric kernels, no I/O, no checks of its own) — permitted for the same
reason the other four are: it carries nothing upward into ``dsx/checks/``.
Phase 9's ``dsx/frame/paradigm.py::_check_monitoring_discipline`` is the
first frame module to import it, reusing ``inflation_from_peeking()`` rather
than coining a second table (REQ-P9-01). The rule exists so this package
stays an extractable, self-contained boundary: if a future extraction ever
pulls ``dsx/frame/`` into its own package, no upward import into
``dsx/checks/`` has to be untangled first — the forbidden direction is
strictly upward into ``dsx.checks``, never a pure computation helper like
``dsx.mathx``. The boundary is proven, not assumed — the test scans every
real ``dsx/frame/*.py`` module and is itself shown to fail against three
deliberately violating import forms.
"""

from __future__ import annotations
