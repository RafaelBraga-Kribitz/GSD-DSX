"""dsx — deterministic guardrails for data-science, analytics and BI work.

The design premise: an agent's judgement belongs in *filling* the analysis
contract; code's judgement belongs in *checking* it. Everything in this package
is pure, dependency-free and returns findings with stable codes, so the same spec
always produces the same verdict.
"""

__version__ = "1.4.0"
__all__ = ["__version__"]
