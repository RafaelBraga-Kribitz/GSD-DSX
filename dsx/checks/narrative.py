"""Narrative deliverable gates. Codes DSX-NAR-*.

Holds the decision-maker's document to the claims and forbidden-wording register.
Stdlib only; optional phase-local FORBIDDEN-CLAIMS.yaml merges with a universal pack.
"""

from __future__ import annotations

import re
from pathlib import Path

from ..findings import Report
from ..loader import loads as load_yaml
from ..pct_base import normalize_ws, relative_percent_without_base
from ..spec import is_blank, items, section

UNIVERSAL_FORBIDDEN: list[tuple[str, str]] = [
    ("data_proves", r"(?i)\b(the )?data (proves|shows that|demonstrates that)\b"),
    ("high_confidence", r"(?i)with high confidence"),
    ("virtually_all_scenarios", r"(?i)under virtually all scenarios"),
]

FORBIDDEN_FILENAMES = ("FORBIDDEN-CLAIMS.yaml", "FORBIDDEN-CLAIMS.yml")


def check(
    spec: dict,
    phase_dir: "str | None" = None,
    *,
    gate_point: "str | None" = None,
) -> Report:
    report = Report(check="narrative")
    claims = items(spec, "claims")
    narrative = section(spec, "narrative")
    path_raw = narrative.get("path") if narrative else None
    roots = _roots(phase_dir)

    if claims and is_blank(path_raw) and gate_point == "ship":
        report.add(
            "DSX-NAR-001",
            "HIGH",
            "Claims declared but narrative.path is missing",
            detail=(
                "At ship, every claim must appear in a named narrative deliverable. "
                "Without narrative.path there is nowhere to verify claim⊆deliverable."
            ),
            remedy="Set narrative.path (e.g. NARRATIVE.md) and write the file.",
            where="spec.narrative.path",
        )

    if not is_blank(path_raw):
        resolved = _resolve_file(str(path_raw), roots)
        if resolved is None:
            report.add(
                "DSX-NAR-010",
                "HIGH",
                f"narrative.path {path_raw!r} does not exist",
                detail=f"Looked under: {', '.join(str(r) for r in roots)}",
                remedy="Create the file or fix the path.",
                where="spec.narrative.path",
            )
        else:
            body = resolved.read_text(encoding="utf-8")
            norm_body = normalize_ws(body)
            for index, claim in enumerate(claims):
                text = str(claim.get("text") or "")
                if not text.strip():
                    continue
                if normalize_ws(text) not in norm_body:
                    report.add(
                        "DSX-NAR-020",
                        "HIGH",
                        f"Claim text missing from narrative: claims[{index}]",
                        detail=(
                            f"“{normalize_ws(text)[:140]}” must appear (whitespace-normalised) "
                            f"in {path_raw}."
                        ),
                        remedy="Paste the claim wording into the narrative, or edit the claim.",
                        where=f"spec.claims[{index}].text",
                    )
            _scan_forbidden(body, "narrative", str(path_raw), report, roots)
            if relative_percent_without_base(body):
                report.add(
                    "DSX-NAR-040",
                    "MEDIUM",
                    "Narrative contains a relative % without a nearby base",
                    detail=(
                        "Readers assume the larger base. State from/to, n=, or of N users "
                        "next to the percentage."
                    ),
                    remedy="Add base language, or set base_n / from_value+to_value on the claim.",
                    where=f"narrative:{path_raw}",
                )
            else:
                report.ok(f"narrative {path_raw} scanned")

    for index, claim in enumerate(claims):
        text = str(claim.get("text") or "")
        if text.strip():
            _scan_forbidden(text, "claim", f"spec.claims[{index}].text", report, roots)

    dashboard = section(spec, "dashboard")
    dash_path = dashboard.get("path") if dashboard else None
    if not is_blank(dash_path):
        if _resolve_file(str(dash_path), roots) is None:
            report.add(
                "DSX-NAR-050",
                "HIGH",
                f"dashboard.path {dash_path!r} does not exist",
                detail="Optional BI surface was declared; the path must resolve at ship.",
                remedy="Create the dashboard README or remove dashboard.path.",
                where="spec.dashboard.path",
            )
        else:
            report.ok(f"dashboard path present: {dash_path}")

    return report


def _roots(phase_dir: "str | None") -> list[Path]:
    roots: list[Path] = []
    if phase_dir:
        roots.append(Path(phase_dir))
    roots.append(Path.cwd())
    return roots


def _resolve_file(rel: str, roots: list[Path]) -> Path | None:
    for root in roots:
        candidate = root / rel
        if candidate.is_file():
            return candidate
    alt = Path(rel)
    if alt.is_file():
        return alt
    return None


def _load_forbidden(roots: list[Path]) -> list[tuple[str, str]]:
    patterns = list(UNIVERSAL_FORBIDDEN)
    seen_ids = {pid for pid, _ in patterns}
    for root in roots:
        for name in FORBIDDEN_FILENAMES:
            path = root / name
            if not path.is_file():
                continue
            try:
                data = load_yaml(path.read_text(encoding="utf-8"), suffix=path.suffix)
            except Exception:
                continue
            for entry in data.get("patterns") or []:
                if not isinstance(entry, dict):
                    continue
                pid = str(entry.get("id") or "")
                regex = entry.get("regex")
                if not pid or not isinstance(regex, str) or pid in seen_ids:
                    continue
                patterns.append((pid, regex))
                seen_ids.add(pid)
            break
    return patterns


def _scan_forbidden(
    text: str,
    kind: str,
    where: str,
    report: Report,
    roots: list[Path],
) -> None:
    for pid, pattern in _load_forbidden(roots):
        try:
            if re.search(pattern, text):
                report.add(
                    "DSX-NAR-030",
                    "CRITICAL",
                    f"Forbidden wording ({pid}) in {kind}",
                    detail=f"Matched pattern {pid!r} in {where}.",
                    remedy=(
                        "Rewrite without overclaim verbs. Negated corrections are fine; "
                        "assertive 'data proves' is not."
                    ),
                    where=where,
                    pattern_id=pid,
                )
        except re.error:
            continue
