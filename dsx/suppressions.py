"""ADR/SPEC-backed finding suppressions.

Optional ``suppressions[]`` on ANALYSIS-SPEC removes matching findings from the
blocking set *after* checks run. Suppressions are not soft opinions — each row
must name a real ``DSX-*`` code, a non-blank reason, and an authority pointer
(SPEC, ADR, or ticket). Unknown codes abort the run (exit 2).
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any

from .findings import CheckError, Finding, Report, Severity
from .spec import is_blank, items

_CODE_RE = re.compile(r"^DSX-[A-Z]+-\d{3}$")
_DSX_ROOT = Path(__file__).resolve().parent
_KNOWN: set[str] | None = None


def known_codes() -> set[str]:
    """Codes emitted by ``report.add(...)`` under ``dsx/`` (cached)."""
    global _KNOWN
    if _KNOWN is not None:
        return _KNOWN
    found: set[str] = set()
    for path in list(_DSX_ROOT.rglob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if not (isinstance(func, ast.Attribute) and func.attr == "add"):
                continue
            if not node.args:
                continue
            arg0 = node.args[0]
            if isinstance(arg0, ast.Constant) and isinstance(arg0.value, str):
                if arg0.value.startswith("DSX-"):
                    found.add(arg0.value)
    # SQL rule tuples in metrics.py
    metrics = _DSX_ROOT / "checks" / "metrics.py"
    if metrics.exists():
        text = metrics.read_text(encoding="utf-8")
        for match in re.finditer(r'"(DSX-(?:SQL|MET)-\d{3})"', text):
            found.add(match.group(1))
    _KNOWN = found
    return found


def validate_suppressions(spec: dict) -> Report:
    """Structural checks on ``suppressions[]``. Codes DSX-SPEC-070…072."""
    report = Report(check="suppressions")
    rows = items(spec, "suppressions")
    if not rows:
        report.ok("no suppressions declared")
        return report

    known = known_codes()
    for index, row in enumerate(rows):
        where = f"spec.suppressions[{index}]"
        if not isinstance(row, dict):
            report.add(
                "DSX-SPEC-070",
                "HIGH",
                "suppression entry is not a mapping",
                detail=f"Got {type(row).__name__}.",
                remedy="Each suppressions[] item needs code, reason, and authority.",
                where=where,
            )
            continue

        code = str(row.get("code") or "").strip()
        reason = row.get("reason")
        authority = row.get("authority")

        if is_blank(code):
            report.add(
                "DSX-SPEC-070",
                "HIGH",
                "suppression is missing code",
                detail="A suppression without a finding code cannot be audited.",
                remedy="Set code: to a DSX-* identifier from references/finding-codes.md.",
                where=f"{where}.code",
            )
        elif not _CODE_RE.match(code):
            report.add(
                "DSX-SPEC-071",
                "HIGH",
                f"suppression code {code!r} has invalid shape",
                detail="Expected DSX-<FAMILY>-NNN (three digits).",
                remedy="Use a catalogue code, e.g. DSX-VIZ-030.",
                where=f"{where}.code",
            )
        elif code not in known:
            # Unknown codes are operational errors — raise at apply time; also flag.
            report.add(
                "DSX-SPEC-072",
                "CRITICAL",
                f"suppression references unknown code {code!r}",
                detail="Suppressions may only name codes this dsx build can emit.",
                remedy="Fix the typo or remove the row. See references/finding-codes.md.",
                where=f"{where}.code",
            )

        if is_blank(reason):
            report.add(
                "DSX-SPEC-070",
                "HIGH",
                f"suppression of {code or '?'} is missing reason",
                detail="A blank reason is how silent waivers sneak in.",
                remedy="Write why this finding is accepted (SPEC/ADR constraint).",
                where=f"{where}.reason",
            )
        if is_blank(authority):
            report.add(
                "DSX-SPEC-070",
                "HIGH",
                f"suppression of {code or '?'} is missing authority",
                detail="Authority must point at a SPEC, ADR, or ticket.",
                remedy="Set authority: to a path or URL a reviewer can open.",
                where=f"{where}.authority",
            )

    if not any(f.code.startswith("DSX-SPEC-07") for f in report.findings):
        report.ok(f"{len(rows)} suppression(s) well-formed")
    return report


def _visual_index_by_chart_id(spec: dict, chart_id: str) -> tuple[int | None, str | None]:
    for index, visual in enumerate(items(spec, "visuals")):
        if str(visual.get("chart_id") or "").strip() == chart_id:
            return index, str(visual.get("name") or "") or None
    return None, None


def _matches(finding: Finding, row: dict, spec: dict) -> bool:
    code = str(row.get("code") or "").strip()
    if finding.code != code:
        return False
    chart_id = str(row.get("chart_id") or "").strip()
    if not chart_id:
        return True
    index, name = _visual_index_by_chart_id(spec, chart_id)
    if index is not None and finding.where.startswith(f"spec.visuals[{index}]"):
        return True
    if chart_id and chart_id in finding.where:
        return True
    if name and name in finding.title:
        return True
    return False


def apply_suppressions(spec: dict, report: Report) -> Report:
    """Drop findings matched by valid suppressions; record context for the report.

    Raises ``CheckError`` (exit 2) when a suppression names an unknown code.
    """
    rows = items(spec, "suppressions")
    if not rows:
        return report

    known = known_codes()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            continue
        code = str(row.get("code") or "").strip()
        if code and code not in known:
            raise CheckError(
                f"spec.suppressions[{index}].code {code!r} is not a known DSX finding code"
            )
        if code and not _CODE_RE.match(code):
            raise CheckError(
                f"spec.suppressions[{index}].code {code!r} has invalid shape"
            )

    # Structural defects (missing reason/authority) stay as findings — do not
    # apply those rows.
    usable: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        code = str(row.get("code") or "").strip()
        if (
            code
            and _CODE_RE.match(code)
            and code in known
            and not is_blank(row.get("reason"))
            and not is_blank(row.get("authority"))
        ):
            usable.append(row)

    kept: list[Finding] = []
    suppressed: list[dict[str, str]] = []
    for finding in report.findings:
        matched = next((row for row in usable if _matches(finding, row, spec)), None)
        if matched is None:
            kept.append(finding)
            continue
        suppressed.append(
            {
                "code": finding.code,
                "title": finding.title,
                "reason": str(matched.get("reason")).strip(),
                "authority": str(matched.get("authority")).strip(),
                "chart_id": str(matched.get("chart_id") or "").strip(),
            }
        )

    out = Report(check=report.check, findings=kept, passed_checks=list(report.passed_checks))
    out.context.update(report.context)
    if suppressed:
        out.context["suppressions_applied"] = suppressed
        out.ok(f"applied {len(suppressed)} suppression(s)")
    return out
