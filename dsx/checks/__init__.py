"""Check modules. Each exposes ``check(spec) -> Report`` and owns a code prefix.

    design      DSX-EXP-*, DSX-CAU-*   experiment power, SRM, units, identification
    stats       DSX-STA-*              test selection, assumptions, reporting contract
    ml          DSX-ML-*               leakage, splits, metric choice, baselines
    metrics     DSX-MET-*, DSX-SQL-*   definitions, reconciliation, Simpson's, SQL lint
    claims      DSX-CLM-*              causal language, evidence, generalisation
    viz         DSX-VIZ-*              encoding correctness, proportionality, uncertainty
    repro       DSX-REP-*              seeds, environment, data identity, entrypoint
    dq          DSX-DQ-*               profile assertions vs DATA-PROFILE artifact
    coherence   DSX-COH-*              question ↔ claim ↔ decision agreement
"""

from . import claims, coherence, design, dq, metrics, ml, repro, stats, viz

__all__ = [
    "claims",
    "coherence",
    "design",
    "dq",
    "metrics",
    "ml",
    "repro",
    "stats",
    "viz",
]
