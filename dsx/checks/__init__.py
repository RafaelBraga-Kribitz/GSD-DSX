"""Check modules. Each exposes ``check(spec) -> Report`` and owns a code prefix.

    design      DSX-EXP-*, DSX-CAU-*   experiment power, SRM, units, identification
    stats       DSX-STA-*              test selection, assumptions, reporting contract
    ml          DSX-ML-*               leakage, splits, metric choice, baselines
    metrics     DSX-MET-*, DSX-SQL-*   definitions, reconciliation, Simpson's, SQL lint
    claims      DSX-CLM-*              causal language, evidence, generalisation
    viz         DSX-VIZ-*              encoding correctness, proportionality, uncertainty
    repro       DSX-REP-*              seeds, environment, data identity, entrypoint, repro_lock
    dq          DSX-DQ-*               profile assertions vs DATA-PROFILE artifact
    coherence   DSX-COH-*              question ↔ claim ↔ decision agreement
    figures     DSX-FIG-*              artifact paths and svg_sha256 seals
    smells      DSX-SMELL-*            declaration-based plot-construction smells
    narrative   DSX-NAR-*              deliverable path, claim⊆narrative, forbidden wording
    code        DSX-CODE-*             fit-before-split entrypoint scan
    decision    DSX-DEC-*              structured decision.replay vs results.tests
"""

from . import (
    claims,
    code,
    coherence,
    decision,
    design,
    dq,
    figures,
    metrics,
    ml,
    narrative,
    repro,
    smells,
    stats,
    viz,
)

__all__ = [
    "claims",
    "code",
    "coherence",
    "decision",
    "design",
    "dq",
    "figures",
    "metrics",
    "ml",
    "narrative",
    "repro",
    "smells",
    "stats",
    "viz",
]
