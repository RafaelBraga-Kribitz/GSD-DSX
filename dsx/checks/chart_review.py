"""CHART-REVIEW.md structural conformance. Codes DSX-CRV-*.

Validates the adversarial chart-audit report artifact
(``references/chart-review-schema.md``) against its own contract — deterministically,
reading structure only (frontmatter ``schema`` tag, the forbidden ten-point-scale
substring, the terminal sentinel, and the ``DSX-``/``UNMAPPED`` token on finding
lines). D-13 (11.3-CONTEXT.md): this module must NEVER read ``final_assessment``,
any ``scores.*``, the agent-transcribed ``gates.A/B/C/D`` values, or the verdict
prose of ``## Executive Verdict`` / ``## Final Assessment`` / ``## Per-Exhibit
Disposition`` — those are exactly the stochastic agent judgements this family
exists to never gate on. Reuses no ``DSX-FIG-*`` code (D-12): the schema's own
Gate-D proxy wildcards ``DSX-FIG-*`` at CRITICAL/HIGH, so a malformed report
minting a DSX-FIG-* code would be swept into the very gate it reports on.
"""

from __future__ import annotations

from pathlib import Path

from ..findings import Report
from ..loader import SpecParseError, loads as load_yaml

CHART_REVIEW_NAMES = ("CHART-REVIEW.md", "good-CHART-REVIEW.md")
REQUIRED_SCHEMA = "dsx-chart-review-v1"
TERMINAL_SENTINEL = "## CHART AUDIT COMPLETE"
FORBIDDEN_SCALE_SUBSTRING = "X/10"
_FINDING_HEADINGS = ("## Critical Issues", "## Moderate Issues", "## Minor Issues")


def check(
    spec: dict,
    phase_dir: "str | None" = None,
    *,
    strict: bool = False,
) -> Report:
    """Validate CHART-REVIEW.md's structural conformance.

    ``spec`` is accepted and unused — every other checks-layer artifact reader
    (``figures.check(spec, phase_dir, *, strict=...)``) takes it for
    ``run_checks()`` calling-convention uniformity even when the artifact being
    read carries no spec-derived fields of its own (RESEARCH Open Question 2).
    ``strict`` is likewise accepted for the same uniformity and currently
    unused: every DSX-CRV-* rule already blocks identically at verify and ship
    (T-11.3-11/D-01): a missing, truncated or undecodable CHART-REVIEW.md
    degrades to an ok/empty report rather than raising, mirroring
    ``figures.check`` and ``dsx/frame/val.py::check``.
    """
    report = Report(check="chart_review")
    roots = _resolve_roots(phase_dir)
    path = _find_chart_review(roots)
    if path is None:
        report.ok("no CHART-REVIEW.md found")
        return report

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        report.ok(f"CHART-REVIEW.md at {path} could not be read ({exc}) — skipped")
        return report

    frontmatter, body = _split_frontmatter(text)

    _check_schema_tag(frontmatter, report, path)
    _check_forbidden_scale(text, report, path)
    _check_terminal_sentinel(text, report, path)
    _check_finding_tokens(body, report, path)

    return report


def _resolve_roots(phase_dir: "str | None") -> list[Path]:
    roots: list[Path] = []
    if phase_dir:
        roots.append(Path(phase_dir))
    roots.append(Path.cwd())
    return roots


def _find_chart_review(roots: list[Path]) -> "Path | None":
    for root in roots:
        for name in CHART_REVIEW_NAMES:
            candidate = root / name
            if candidate.is_file():
                return candidate
    return None


def _split_frontmatter(text: str) -> "tuple[dict, str]":
    """Split ``text`` into ``(frontmatter, body)``.

    Frontmatter is the YAML block between the first two ``---`` delimiter
    lines (``chart-review-schema.md:8-33``), parsed via ``dsx/loader.py``'s
    shared bundled/PyYAML loader rather than a new ad-hoc parser (RESEARCH
    "Don't Hand-Roll"). Absence of delimiters, a parse failure, or a
    non-mapping frontmatter block all degrade to ``({}, text)`` rather than
    raising — a chart_review.check() caller never sees an exception from this
    helper (D-01).
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            fm_text = "\n".join(lines[1:index])
            body = "\n".join(lines[index + 1 :])
            try:
                data = load_yaml(fm_text, suffix=".yaml")
            except SpecParseError:
                return {}, body
            if not isinstance(data, dict):
                return {}, body
            return data, body
    return {}, text


def _check_schema_tag(frontmatter: dict, report: Report, path: Path) -> None:
    """Emit DSX-CRV-010 when the frontmatter ``schema`` tag is not
    ``dsx-chart-review-v1``.

    Citation: references/chart-review-schema.md, "Orchestrator validation"
    section, rule 1 of 4 (chart-review-schema.md:84). The schema file is the
    contract itself, not an external judgement source (D-13) — a DSX-CRV-*
    code is never cited against a scores/gates/final_assessment field.

    Structural criterion: ``frontmatter.get("schema")`` equals the literal
    string ``"dsx-chart-review-v1"`` (chart-review-schema.md:12,84). A blank,
    absent or mismatched value fires; the value compared is the declared
    contract-identity tag, never any judgement content.
    """
    schema_tag = frontmatter.get("schema") if isinstance(frontmatter, dict) else None
    if schema_tag == REQUIRED_SCHEMA:
        report.ok(f"CHART-REVIEW.md schema tag is {REQUIRED_SCHEMA!r}")
        return
    report.add(
        "DSX-CRV-010",
        "HIGH",
        f"CHART-REVIEW.md frontmatter schema is {schema_tag!r}, not {REQUIRED_SCHEMA!r}",
        detail=(
            "The chart-review contract identity is broken: a report that does not "
            "declare dsx-chart-review-v1 cannot be trusted to follow the rest of "
            "the schema (body order, gate proxies, orchestrator validation rules)."
        ),
        remedy=f"Set frontmatter `schema: {REQUIRED_SCHEMA}`.",
        where=str(path),
    )


def _check_forbidden_scale(text: str, report: Report, path: Path) -> None:
    """Emit DSX-CRV-011 when the forbidden free-form ten-point-scale substring
    is present anywhere in CHART-REVIEW.md.

    Citation: references/chart-review-schema.md, "Orchestrator validation"
    section, rule 2 of 4 (chart-review-schema.md:85), restating the Scores
    contract at chart-review-schema.md:35 ("Scores are 1-4 only. Free-form
    `X/10` is forbidden.").

    Structural criterion: the literal substring "X/10" is present in the raw
    file text (chart-review-schema.md:35,85) — a plain `in` test, per RESEARCH
    "Don't Hand-Roll" (no regex, no markdown parsing). The schema states this
    rule against exactly that literal string; no numeric score value is
    computed or compared here.
    """
    if FORBIDDEN_SCALE_SUBSTRING not in text:
        report.ok("CHART-REVIEW.md carries no free-form X/10 scale")
        return
    report.add(
        "DSX-CRV-011",
        "MEDIUM",
        "CHART-REVIEW.md contains the forbidden free-form 'X/10' scale",
        detail=(
            "Scores must use the mandated 1-4 scale "
            "(chart-review-schema.md:35). A free-form X/10 note anywhere in "
            "the report signals the audit did not follow the contract."
        ),
        remedy="Replace the free-form X/10 note with a 1-4 score plus an evidence bullet.",
        where=str(path),
    )


def _check_terminal_sentinel(text: str, report: Report, path: Path) -> None:
    """Emit DSX-CRV-012 when CHART-REVIEW.md does not end with the terminal
    ``## CHART AUDIT COMPLETE`` sentinel.

    Citation: references/chart-review-schema.md, "Orchestrator validation"
    section, rule 3 of 4 (chart-review-schema.md:86), restating the fixed H2
    body order's final heading (chart-review-schema.md:80).

    Structural criterion: ``text.rstrip().endswith("## CHART AUDIT
    COMPLETE")`` — a plain string operation (RESEARCH "Don't Hand-Roll"), not
    a markdown-structure parse. Its absence means the audit may be truncated —
    literally "reporting completeness" — independent of anything the audit
    concluded.
    """
    if text.rstrip().endswith(TERMINAL_SENTINEL):
        report.ok("CHART-REVIEW.md ends with the terminal sentinel")
        return
    report.add(
        "DSX-CRV-012",
        "HIGH",
        "CHART-REVIEW.md does not end with the terminal '## CHART AUDIT COMPLETE' sentinel",
        detail=(
            "The fixed H2 body order (chart-review-schema.md:69-80) ends with this "
            "heading; its absence means the audit may be truncated or incomplete."
        ),
        remedy="Append `## CHART AUDIT COMPLETE` as the final line of the report.",
        where=str(path),
    )


def _check_finding_tokens(body: str, report: Report, path: Path) -> None:
    """Emit DSX-CRV-013 for every finding line under ``## Critical Issues`` /
    ``## Moderate Issues`` / ``## Minor Issues`` that carries neither a
    ``DSX-`` code nor ``UNMAPPED``.

    Citation: references/chart-review-schema.md, "Orchestrator validation"
    section, rule 4 of 4 (chart-review-schema.md:87), restating the Issues
    headings' own contract (chart-review-schema.md:75, "each line cites
    `DSX-*` or `UNMAPPED`").

    Structural criterion: for each bullet line (``- ...``) under one of the
    three Issues headings — skipping the literal placeholder line ``- None``
    — the line's text must contain the substring ``DSX-`` or ``UNMAPPED``. A
    plain substring test against the finding line's own text, never against
    the verdict prose sections this module never reads.
    """
    violations = _untokenised_finding_lines(body)
    if not violations:
        report.ok("CHART-REVIEW.md finding lines all carry a DSX- or UNMAPPED token")
        return
    for line_number, line_text in violations:
        report.add(
            "DSX-CRV-013",
            "MEDIUM",
            "CHART-REVIEW.md finding line carries neither a DSX- code nor UNMAPPED",
            detail=f"Line {line_number}: {line_text!r}",
            remedy="Cite the finding's DSX-* code, or UNMAPPED if none applies.",
            where=f"{path}:{line_number}",
        )


def _untokenised_finding_lines(body: str) -> "list[tuple[int, str]]":
    violations: list[tuple[int, str]] = []
    in_findings_section = False
    for offset, raw_line in enumerate(body.splitlines(), start=1):
        stripped = raw_line.strip()
        if stripped.startswith("## "):
            in_findings_section = stripped in _FINDING_HEADINGS
            continue
        if not in_findings_section or not stripped.startswith("- "):
            continue
        content = stripped[2:].strip()
        if content.lower() == "none":
            continue
        if "DSX-" in content or "UNMAPPED" in content:
            continue
        violations.append((offset, content))
    return violations
