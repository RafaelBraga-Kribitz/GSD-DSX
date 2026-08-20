"""DSX-PRE-* — pre-registered inference plan reconciliation (Phase 10).

The declared fallback rule is the preregistered test-selection function, and the
executed procedure is the test-selection function evaluated on the data — Gelman and
Loken's distinction between a test prechosen from a set of possible tests and a test
computed from the data in an environment where a different test would have been
performed given different data. The declared fallback rule is phi; the executed
procedure is phi(y).

Citation: Gelman, A. and Loken, E. (2014), "The Statistical Crisis in Science",
American Scientist 102(6):460-465, page 460, unnumbered section "How to Test a
Hypothesis". The article carries no numbered sections, tables or theorems, so page
plus unnumbered heading is the most precise locator available. The Greek symbol the
paper uses for the selection function is rendered unreliably by optical character
recognition in both freely available scans, so it is taken from the authors'
unpublished 2013 Columbia working paper as a notation source only, never as the
published record. Do not tidy either of those two statements away in a later edit.
"""

from __future__ import annotations

import operator
import re
from dataclasses import dataclass

from ..findings import CheckError, Report
from ..spec import PREREG_FACTS, as_number, get, normalize

_ARROW = "->"

# Fully anchored, no nested quantifier (threat T-10-02: no catastrophic-backtracking
# exposure). The two-character operators are listed before their one-character
# prefixes so the alternation tries them first and never mis-splits `<=` as `<`.
_CONDITION_RE = re.compile(
    r"^\s*(?:if\s+)?(?P<fact>[A-Za-z_][A-Za-z0-9_]*)\s*"
    r"(?P<op><=|>=|==|!=|<|>)\s*"
    r"(?P<value>-?\d+(?:\.\d+)?)\s*$"
)

_OPS = {
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
    "==": operator.eq,
    "!=": operator.ne,
}

_EXPECTED_FORM = "<fact> <op> <number> -> <branch>"


@dataclass(frozen=True)
class _ParsedRule:
    fact: str
    op: str
    threshold: float
    branch: str


def _parse_fallback_rule(text: object) -> "_ParsedRule | None":
    """Parse a declared ``inference.fallback_rule`` string into a ``_ParsedRule``.

    Opt-in, discriminated by the literal arrow ``->`` (D-01): a string that is not a
    string at all, or a string containing no arrow, returns ``None`` — it is free
    prose, not a rule, and produces no finding and no error. Every ``fallback_rule``
    value committed to this repository today is English prose with no arrow, so this
    function is inert against all of them.

    Once an arrow is present the text is a rule and must parse. A left-hand side that
    does not match ``<fact> <op> <number>`` (an optional leading ``if``, a fact name,
    one of six comparison operators, and a numeric threshold), or an arrow with no
    branch label after it, raises ``CheckError`` — the only route to exit 2 (D-02).
    That raise aborts the whole gate run and prints no findings; this is an accepted
    consequence (D-03), not a defect to work around, so every message here names the
    offending text and the expected form, letting an operator tell an aborted run from
    a clean one.

    The branch label is the text after ``->`` up to the first comma, trimmed — the
    brief's own worked example carries a trailing annotation
    (``, 9999 reps, seed 42``) that is discarded, not parsed.
    """
    if not isinstance(text, str) or _ARROW not in text:
        return None

    # The repository checks out CRLF; normalise line endings before matching rather
    # than relying on \s alone at the anchors.
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lhs, _, rhs = normalized.partition(_ARROW)

    match = _CONDITION_RE.match(lhs)
    if match is None:
        raise CheckError(
            f"fallback_rule condition {lhs.strip()!r} does not match the expected "
            f"form {_EXPECTED_FORM!s}"
        )

    branch = rhs.split(",", 1)[0].strip()
    if not branch:
        raise CheckError(
            f"fallback_rule {text.strip()!r} has an arrow but no branch label; "
            f"expected form {_EXPECTED_FORM!s}"
        )

    return _ParsedRule(
        fact=match.group("fact"),
        op=match.group("op"),
        threshold=float(match.group("value")),
        branch=branch,
    )


# Format templates (not f-strings evaluated at module scope) — the two reasons a
# DSX-PRE-010 finding will later carry. The accepted-names list in _UNKNOWN_FACT is
# built from sorted(PREREG_FACTS) at module load time, so it can never drift from the
# registry.
_UNKNOWN_FACT = (
    "fallback_rule references fact {fact!r}, which is outside the closed prereg fact "
    "registry; accepted names are: " + ", ".join(sorted(PREREG_FACTS))
)

_UNDECLARED_FACT = (
    "fallback_rule references registry fact {fact!r} ({path}), which the spec does "
    "not declare as a number"
)


@dataclass(frozen=True)
class _Resolution:
    branch: "str | None"
    reason: "str | None"
    source: str


def _resolve_branch(spec: dict) -> _Resolution:
    """Resolve the declared ``inference.fallback_rule`` to exactly one branch.

    A single-condition grammar with an implicit else (the primary procedure) has
    exactly two outcomes and no way to select more than one — the "more than one
    branch" failure mode REQ-P10-01 names is structurally impossible here, rather
    than merely untested. The "zero branches" mode is exactly the two registry
    failures below: a fact name outside ``PREREG_FACTS``, or a registry fact the
    spec does not declare as a number.

    Degrades to an unresolved ``_Resolution`` with no reason — never a traceback —
    when ``spec`` is not a dict or ``inference`` is not a dict, matching
    ``interference.check``'s habit. A ``CheckError`` raised by
    ``_parse_fallback_rule`` propagates untouched: that is D-02's exit-2 route, and
    this function must not swallow it.

    Returns the branch label as authored, without normalising it — normalisation
    belongs at the comparison site in a later plan, so the finding text can quote
    the operator's own wording.

    This function never reads the declared inferential paradigm field (D-11, brief
    D-11): the branch a fallback rule selects does not depend on it.
    """
    if not isinstance(spec, dict):
        return _Resolution(branch=None, reason=None, source="unresolved")

    inference = spec.get("inference")
    if not isinstance(inference, dict):
        return _Resolution(branch=None, reason=None, source="unresolved")

    primary_procedure = inference.get("primary_procedure")

    parsed = _parse_fallback_rule(inference.get("fallback_rule"))
    if parsed is None:
        return _Resolution(
            branch=primary_procedure, reason=None, source="primary_procedure"
        )

    path = PREREG_FACTS.get(parsed.fact)
    if path is None:
        return _Resolution(
            branch=None,
            reason=_UNKNOWN_FACT.format(fact=parsed.fact),
            source="unresolved",
        )

    value = as_number(get(spec, path))
    if value is None:
        return _Resolution(
            branch=None,
            reason=_UNDECLARED_FACT.format(fact=parsed.fact, path=path),
            source="unresolved",
        )

    condition_true = _OPS[parsed.op](value, parsed.threshold)
    if condition_true:
        return _Resolution(branch=parsed.branch, reason=None, source="fallback_rule")
    return _Resolution(
        branch=primary_procedure, reason=None, source="primary_procedure"
    )
