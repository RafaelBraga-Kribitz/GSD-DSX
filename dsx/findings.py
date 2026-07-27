"""Finding / Report primitives — the single output contract for every dsx check.

Every check in this package returns Findings. Nothing prints ad-hoc. This is what
makes the whole system deterministic and machine-checkable: one severity ladder,
one exit-code mapping, one JSON shape.

Exit-code contract (consumed by GSD `command-exit-zero` gates):
    0  -> no finding at or above the blocking threshold  (gate passes)
    1  -> at least one finding at/above threshold         (gate blocks)
    2  -> the check itself could not run                  (gate errors -> onError)
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field, asdict
from enum import IntEnum
from typing import Any, Iterable, Sequence

EXIT_PASS = 0
EXIT_BLOCK = 1
EXIT_ERROR = 2


class Severity(IntEnum):
    """Ordered severity ladder. Higher is worse. Comparable with `>=`."""

    INFO = 10
    LOW = 20
    MEDIUM = 30
    HIGH = 40
    CRITICAL = 50

    @classmethod
    def parse(cls, value: "str | Severity") -> "Severity":
        if isinstance(value, Severity):
            return value
        key = str(value).strip().upper()
        if key not in cls.__members__:
            raise ValueError(
                f"unknown severity {value!r}; expected one of {', '.join(cls.__members__)}"
            )
        return cls[key]

    @property
    def label(self) -> str:
        return self.name


@dataclass(frozen=True)
class Finding:
    """One machine-checkable defect.

    Attributes:
        code:     stable identifier, e.g. ``DSX-EXP-003``. Never renumber a shipped code.
        severity: position on the ladder.
        title:    one-line statement of what is wrong.
        detail:   the evidence — actual numbers, not adjectives.
        remedy:   the concrete next action that clears the finding.
        where:    file / spec path the finding attaches to.
        data:     structured evidence for downstream tooling.
    """

    code: str
    severity: Severity
    title: str
    detail: str = ""
    remedy: str = ""
    where: str = ""
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["severity"] = self.severity.label
        return out

    def render(self) -> str:
        head = f"[{self.severity.label}] {self.code}  {self.title}"
        lines = [head]
        if self.where:
            lines.append(f"    where:  {self.where}")
        if self.detail:
            lines.append(f"    detail: {self.detail}")
        if self.remedy:
            lines.append(f"    fix:    {self.remedy}")
        return "\n".join(lines)


@dataclass
class Report:
    """Collected findings for one check run."""

    check: str
    findings: list[Finding] = field(default_factory=list)
    passed_checks: list[str] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)

    # ---- accumulation -----------------------------------------------------

    def add(
        self,
        code: str,
        severity: "str | Severity",
        title: str,
        detail: str = "",
        remedy: str = "",
        where: str = "",
        **data: Any,
    ) -> Finding:
        finding = Finding(
            code=code,
            severity=Severity.parse(severity),
            title=title,
            detail=detail,
            remedy=remedy,
            where=where,
            data=data,
        )
        self.findings.append(finding)
        return finding

    def ok(self, name: str) -> None:
        """Record a check that ran and passed. Makes the report auditable."""
        self.passed_checks.append(name)

    def extend(self, other: "Report") -> None:
        self.findings.extend(other.findings)
        self.passed_checks.extend(other.passed_checks)

    # ---- querying ---------------------------------------------------------

    @property
    def max_severity(self) -> "Severity | None":
        return max((f.severity for f in self.findings), default=None)

    def at_or_above(self, threshold: Severity) -> list[Finding]:
        return [f for f in self.findings if f.severity >= threshold]

    def blocks(self, threshold: Severity) -> bool:
        return bool(self.at_or_above(threshold))

    def counts(self) -> dict[str, int]:
        out = {s.label: 0 for s in Severity}
        for f in self.findings:
            out[f.severity.label] += 1
        return out

    # ---- rendering --------------------------------------------------------

    def to_dict(self, threshold: Severity) -> dict[str, Any]:
        return {
            "check": self.check,
            "block": self.blocks(threshold),
            "threshold": threshold.label,
            "counts": self.counts(),
            "passed_checks": self.passed_checks,
            "findings": [f.to_dict() for f in self.findings],
            "context": self.context,
        }

    def render(self, threshold: Severity, verbose: bool = False) -> str:
        lines: list[str] = []
        ordered = sorted(self.findings, key=lambda f: (-f.severity, f.code))
        for finding in ordered:
            lines.append(finding.render())
        counts = self.counts()
        summary = " ".join(
            f"{label}={counts[label]}" for label in ("CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO")
        )
        if verbose and self.passed_checks:
            lines.append("")
            lines.append("passed: " + ", ".join(sorted(set(self.passed_checks))))
        lines.append("")
        verdict = "BLOCK" if self.blocks(threshold) else "PASS"
        lines.append(
            f"{self.check}: {verdict} (blocking at {threshold.label}) — {summary}"
        )
        return "\n".join(lines)

    def exit_code(self, threshold: Severity) -> int:
        return EXIT_BLOCK if self.blocks(threshold) else EXIT_PASS


def emit(report: Report, threshold: Severity, as_json: bool, verbose: bool = False) -> int:
    """Print the report on the correct stream and return the process exit code.

    Blocking output goes to stderr so GSD surfaces it in the gate message tail;
    passing output goes to stdout so it stays out of the way.
    """
    code = report.exit_code(threshold)
    text = (
        json.dumps(report.to_dict(threshold), indent=2, sort_keys=True)
        if as_json
        else report.render(threshold, verbose=verbose)
    )
    stream = sys.stderr if code != EXIT_PASS else sys.stdout
    print(text, file=stream)
    return code


def merge(check: str, reports: Iterable[Report]) -> Report:
    merged = Report(check=check)
    for r in reports:
        merged.extend(r)
        merged.context.setdefault(r.check, r.context)
    return merged


def require(condition: bool, message: str) -> None:
    """Guard for check preconditions. Raises CheckError -> exit 2."""
    if not condition:
        raise CheckError(message)


class CheckError(RuntimeError):
    """The check could not be evaluated. Distinct from 'the check found a defect'."""


def unique(values: Sequence[Any]) -> list[Any]:
    seen: set[Any] = set()
    out: list[Any] = []
    for v in values:
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out
