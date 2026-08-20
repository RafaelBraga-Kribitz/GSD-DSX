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

from ..decisions import DecisionRecord, decisions_path, frame_digest, read_all
from ..findings import CheckError, Report
from ..spec import PREREG_FACTS, as_number, get, is_blank, normalize

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


def _check_rule_resolves(spec: dict, resolution: "_Resolution", report: Report) -> None:
    """Emit DSX-PRE-010 when the declared fallback rule does not resolve to a branch.

    Fires when ``resolution.reason`` is set — the rule named a fact outside the closed
    ``PREREG_FACTS`` registry, or named a registry fact the spec does not declare as a
    number. Clears, with no finding, when the rule resolves cleanly, including the
    inert no-arrow-prose case, where ``resolution.reason`` is always ``None``.

    Citation: Gelman, A. and Loken, E. (2014), "The Statistical Crisis in Science",
    American Scientist volume 102 issue 6 pages 460-465, page 460, unnumbered section
    "How to Test a Hypothesis" — the passage distinguishing a classical test prechosen
    from a set of possible tests, with preregistered phi, from a test computed from the
    data in an environment where a different test would have been performed given
    different data, T(y; phi(y)). The article carries no numbered sections, tables or
    theorems, so page plus unnumbered heading is the most precise locator that exists;
    naming a section number would be the fabricated locator brief D-05 exists to
    prevent.
    Structural criterion: a declared rule must resolve to exactly one branch against the
    declared observed facts; this function fires when it resolves to none, which
    happens in exactly two ways — the named fact is outside PREREG_FACTS, or the spec
    does not declare it as a number — and no threshold, effect size or statistic is
    computed anywhere on this path (brief D-02). Falsifier: any rule naming a registry
    fact that the spec declares as a number still resolves and never fires (proved by
    TestRuleResolutionFindings test 4). The one available number — Simmons et al.
    (2011) Table 1's 60.7% false-positive rate for the combination of four researcher
    degrees of freedom — quantifies a different quantity entirely, so it is not
    asserted here as a Reference value.
    """
    fired = resolution.reason is not None

    inputs = ["inference.fallback_rule"]
    if fired:
        inference = spec.get("inference")
        if isinstance(inference, dict):
            parsed = _parse_fallback_rule(inference.get("fallback_rule"))
            if parsed is not None:
                path = PREREG_FACTS.get(parsed.fact)
                if path:
                    inputs.append(path)

        report.add(
            "DSX-PRE-010",
            "CRITICAL",
            "Declared fallback rule does not resolve to a branch",
            detail=resolution.reason,
            remedy=(
                "Declare the fact the rule names in the closed prereg fact registry "
                f"({', '.join(sorted(PREREG_FACTS))}), or rewrite the rule to "
                "reference one of those registry facts."
            ),
            where="inference.fallback_rule",
        )

    report.context.setdefault("decisions", []).append(
        DecisionRecord(
            id="",
            invocation_id="",
            layer="deterministic",
            choice=(
                f"DSX-PRE-010 {'fired' if fired else 'clear'}: "
                f"{resolution.reason or 'rule resolves to exactly one branch, or is inert prose'}"
            ),
            inputs=inputs,
            rule=(
                "DSX-PRE-010 fires when the declared fallback rule's resolution "
                "carries a reason — the named fact is outside PREREG_FACTS, or is a "
                "registry fact the spec does not declare as a number."
            ),
            citation="Gelman & Loken (2014), The Statistical Crisis in Science, page 460",
            counterfactual=(
                "Declaring the named fact as a number at its registry path, or "
                "rewriting the rule to reference a registry fact, would have "
                "cleared DSX-PRE-010."
                if fired
                else "Naming a fact outside PREREG_FACTS, or a registry fact the "
                "spec does not declare as a number, would have fired DSX-PRE-010."
            ),
        ).to_dict()
    )


def _check_procedure_reconciliation(spec: dict, resolution: "_Resolution", report: Report) -> None:
    """Emit DSX-PRE-030 when the executed procedure differs from the declared branch.

    Returns early, emitting nothing, when ``resolution.branch`` is ``None`` — an
    unresolved rule is DSX-PRE-010's territory, and one defect must not produce two
    codes — or when the executed side, ``analysis.test``, is blank: there is no
    executed side to reconcile against, and a missing ``analysis:`` block (e.g. the
    committed ``weak-identification-mmm`` known-bad fixture, which declares
    ``primary_procedure`` and has no ``analysis:`` block at all) must not read as a
    switch. Otherwise compares ``normalize(resolution.branch)`` against
    ``normalize(executed)`` and fires on any inequality.

    The declared fallback rule is the preregistered test-selection function, phi; the
    executed procedure is that function evaluated on the data, phi(y).

    Citation: Gelman, A. and Loken, E. (2014), "The Statistical Crisis in Science",
    American Scientist volume 102 issue 6 pages 460-465, page 463, unnumbered section
    "Menstrual Cycles and Voting": "For a p-value to be interpreted as evidence, it
    requires a strong claim that the same analysis would have been performed had the
    data been different." Same no-numbered-structure locator flag as
    ``_check_rule_resolves``. Secondary citation: Simmons, J. P., Nelson, L. D. and
    Simonsohn, U. (2011), "False-Positive Psychology", Psychological Science volume 22
    issue 11 pages 1359-1366, DOI 10.1177/0956797611417632, page 1365, "General
    Discussion", "Nonsolutions", "Correcting alpha levels" — read from the
    publisher-typeset PDF, no scanning risk.
    Structural criterion: branch identity, never procedure merit — the check resolves
    the declared fallback rule to exactly one branch against the declared observed
    facts and blocks on any inequality between that branch label and the executed
    procedure label, reading no admissibility, power or conservatism ordering on the
    gate path (brief D-02); falsified by any fixture whose substituted procedure is
    strictly more conservative and passes.
    """
    if resolution.branch is None:
        return

    executed = get(spec, "analysis.test")
    if is_blank(executed):
        return

    fired = normalize(resolution.branch) != normalize(executed)

    if fired:
        report.add(
            "DSX-PRE-030",
            "CRITICAL",
            "Executed procedure differs from the declared branch",
            detail=(
                f"The declared fallback rule resolves to branch {resolution.branch!r} "
                f"(source: inference.{resolution.source}), but the executed procedure "
                f"at analysis.test is {executed!r} — a different label."
            ),
            remedy=(
                "Either run the procedure the declared rule selects, or amend the "
                "declared plan and record why the amendment happened before the data "
                "was seen. A more conservative substituted procedure still blocks: "
                "the substitution is itself a new researcher degree of freedom "
                "(Simmons, Nelson & Simonsohn 2011, p. 1365), so its merit is not the "
                "question and this check does not evaluate it. Honest caveat: "
                "analysis.test is scaffolded in templates/ANALYSIS-SPEC.yaml and is "
                "therefore a plan-time declaration too — 'executed' is a convention "
                "imposed by this gate point, not a property of the field, the same "
                "class of limit as declared_at."
            ),
            where="analysis.test",
        )

    report.context.setdefault("decisions", []).append(
        DecisionRecord(
            id="",
            invocation_id="",
            layer="deterministic",
            choice=(
                f"DSX-PRE-030 {'fired' if fired else 'clear'}: "
                f"declared={resolution.branch!r} ({resolution.source}), "
                f"executed={executed!r}"
            ),
            inputs=[
                "inference.fallback_rule"
                if resolution.source == "fallback_rule"
                else "inference.primary_procedure",
                "analysis.test",
            ],
            rule=(
                "DSX-PRE-030 fires when normalize(resolution.branch) != "
                "normalize(analysis.test), for a resolved branch and a non-blank "
                "executed procedure."
            ),
            citation=(
                "Gelman & Loken (2014), page 463; Simmons, Nelson & Simonsohn "
                "(2011), page 1365"
            ),
            counterfactual=(
                "Running the procedure the declared rule selects would have "
                "cleared DSX-PRE-030."
                if fired
                else "Executing a different procedure than the declared branch "
                "would have fired DSX-PRE-030, regardless of its relative merit."
            ),
        ).to_dict()
    )


def _recorded_plan_digests(root: "str | None") -> "set[str]":
    """Return every ``frame_digest`` recorded at a ``plan``-gate-point invocation
    header in ``root``'s decision trail.

    Guards for ``root is None`` by returning an empty set rather than constructing a
    path from it — ``decisions_path(None)`` would raise ``TypeError`` from ``Path()``
    before this function ever got a chance to degrade gracefully. Otherwise builds the
    trail path with ``decisions_path(root)`` and reads it with ``read_all``, which
    never raises for any on-disk state (missing, unreadable, or corrupt all degrade to
    ``[]``) — this function adds no ``try``/``except`` of its own, because doing so
    would suggest ``read_all`` could raise, which its own contract says it never does.

    Collects ``frame_digest`` from every record whose ``record_type`` is
    ``"invocation"`` and whose ``gate_point`` is ``"plan"`` — the filter is on gate
    point, not merely on the file existing, so a trail holding only
    ``execute``/``verify``/``ship`` headers still yields an empty set. Uses ``.get()``
    access throughout, because ``read_all`` is a tolerant reader and may hand back a
    dict missing any key.
    """
    if root is None:
        return set()

    records = read_all(decisions_path(root))
    digests: "set[str]" = set()
    for record in records:
        if not isinstance(record, dict):
            continue
        if record.get("record_type") != "invocation":
            continue
        if record.get("gate_point") != "plan":
            continue
        digest = record.get("frame_digest")
        if digest:
            digests.add(digest)
    return digests


def _check_content_lock(spec: dict, root: "str | None", report: Report) -> None:
    """Reconcile the plan-time content lock recorded in the decision trail against
    the verify-time bytes of the ``validity_frame:``/``inference:`` blocks
    (``DSX-PRE-020``), refusing to run at all when no plan-time header is recorded.

    Before Phase 10 the decision trail (``DECISIONS.jsonl``) was a write-only side
    channel: ``dsx gate`` appended to it, and only ``dsx explain`` ever rendered it
    back for a human — never gating on its contents. From here, the plan-time header,
    once written, is a gate input at verify and ship: the first record in this file
    that can change an exit code. The write path documented at
    ``dsx/cli.py::_write_decision_trail`` remains a side channel that can never itself
    change an exit code; the two statements are compatible because they describe
    different directions of the same file — writing stays unconditional and inert,
    reading (here) is conditional and can block. Plan 04 makes the matching edit on
    the writing side.

    Raises ``CheckError`` when the recorded-plan-digest set is empty: there is nothing
    for this gate point to reconcile the declared inference plan against, and a silent
    pass would be the failure the exit-code contract exists to prevent (CONTEXT D-09
    forbids softening the missing header into a pass or a non-blocking finding). The
    message names, in order: what happened (no plan-time frame lock recorded, naming
    the resolved trail path), why that stops the run (nothing to reconcile against),
    the ordinary fix (run ``dsx gate plan`` against this phase directory first), and
    the grandfather route named explicitly (a specification that legitimately predates
    the plan gate declares a ``suppressions[]`` entry citing the architecture decision
    record or specification that authorises it — an unknown code in that block aborts
    the run at exit 2 in the same way, keeping the M-07 grandfather path walkable and
    attributable).

    Once at least one plan header is on record, this function (Task 1) returns with
    no further check — Task 2, later in this same plan, extends it to compare the
    current ``frame_digest`` against the recorded set, honour the ``pre_data``/
    ``post_data`` distinction (D-10), and emit ``DSX-PRE-020``.
    """
    recorded = _recorded_plan_digests(root)
    if not recorded:
        trail_display = str(decisions_path(root)) if root is not None else (
            "<no phase directory>"
        )
        raise CheckError(
            "no plan-time frame lock is recorded in the decision trail at "
            f"{trail_display} — dsx gate plan has never run against this phase "
            "directory, so there is nothing for this gate point to reconcile the "
            "declared inference plan against, and a silent pass would be the "
            "failure the exit-code contract exists to prevent. Run `dsx gate plan` "
            "against this phase directory first. If this specification legitimately "
            "predates the plan gate, declare a `suppressions[]` entry citing the "
            "architecture decision record or specification that is its authority "
            "(the ADR/SPEC authority requirement); an unknown code in that block "
            "aborts the run at exit 2 in the same way."
        )


def check(spec: dict, root: "str | None" = None, *, reconcile_trail: bool = False) -> Report:
    """Emit the pre-registered inference plan findings (``DSX-PRE-*``).

    Degrades to an empty report, never a traceback, when ``spec`` is not a dict,
    matching ``interference.check``'s habit. Resolves the declared fallback rule once
    per run and dispatches to one private helper per adjudicated concept.

    ``reconcile_trail`` gates ``_check_content_lock`` — this function is only invoked
    when the caller opts into trail reconciliation, so the trail-dependent half stays
    inert outside a real gate invocation (a bare ``dsx check``/``dsx audit`` call
    passes no trail root and reconciles nothing). Plan 04 wires *when* a real caller
    passes ``reconcile_trail=True`` — a ``dsx gate`` invocation only, never
    ``validate``/``check``/``audit`` — via the ``gate_invocation`` keyword on
    ``run_checks`` and this family's ``GATE_PROFILES`` registration.
    """
    report = Report(check="prereg")

    if not isinstance(spec, dict):
        return report

    resolution = _resolve_branch(spec)
    _check_rule_resolves(spec, resolution, report)
    _check_procedure_reconciliation(spec, resolution, report)

    if reconcile_trail:
        _check_content_lock(spec, root, report)

    return report
