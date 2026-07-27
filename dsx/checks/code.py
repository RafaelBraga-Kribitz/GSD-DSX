"""Entrypoint fit-before-split scans. Codes DSX-CODE-*.

Stdlib-only: `.py` as text; `.ipynb` via json cell source concat in line order.
Missing / non-text entrypoints are skipped (repro covers missing paths).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from ..findings import Report
from ..spec import is_blank, section

SPLIT_MARKERS = (
    "train_test_split",
    "TimeSeriesSplit",
    "GroupKFold",
    "StratifiedKFold",
    "StratifiedGroupKFold",
    "KFold(",
    "ShuffleSplit",
    "GroupShuffleSplit",
    "TimeSeriesSplit(",
)

FIT_LEAK_MARKERS = (
    r"\.fit\s*\(",
    r"\.fit_transform\s*\(",
    r"\.partial_fit\s*\(",
)

SCALER_FULL_RE = re.compile(
    r"(?i)StandardScaler\s*\(\s*\)\s*\.\s*fit_transform\s*\(\s*(X|df|features)\b"
)

RESAMPLE_BEFORE_RE = re.compile(
    r"(?i)\b(SMOTE|RandomOverSampler|RandomUnderSampler|ADASYN)\b"
)

PIPELINE_FIT_TRAIN_RE = re.compile(
    r"(?i)Pipeline\s*\(.*\)\s*\.\s*fit\s*\(\s*X_train\b"
)


def check(spec: dict, phase_dir: "str | None" = None) -> Report:
    report = Report(check="code")
    repro = section(spec, "reproducibility")
    entry = repro.get("entrypoint")
    if is_blank(entry):
        return report

    path = _resolve_entrypoint(str(entry), phase_dir)
    if path is None:
        return report

    source = _read_source(path)
    if source is None:
        return report

    lines = source.splitlines()
    first_split = _first_line_matching(lines, SPLIT_MARKERS)
    first_fit = _first_fit_leak_line(lines)
    has_model = bool(section(spec, "model"))

    if first_fit is not None and (first_split is None or first_fit < first_split):
        # Allow Pipeline(...).fit(X_train after a split — only when split precedes.
        report.add(
            "DSX-CODE-001",
            "CRITICAL",
            "Fit/transform appears before the first train/test split marker",
            detail=(
                f"Line {first_fit + 1} fits or fit_transforms before any split marker "
                f"({'none' if first_split is None else f'line {first_split + 1}'}). "
                "Fitting on the full frame leaks test statistics into training."
            ),
            remedy=(
                "Split first, then fit only on the training fold "
                "(or use a Pipeline fitted on X_train after the split)."
            ),
            where=f"entrypoint:{entry}",
            fit_line=first_fit + 1,
        )

    for index, line in enumerate(lines):
        if SCALER_FULL_RE.search(line):
            prior = "\n".join(lines[:index])
            if "X_train" not in prior and "x_train" not in prior.lower():
                report.add(
                    "DSX-CODE-002",
                    "HIGH",
                    "StandardScaler().fit_transform on full frame with no prior X_train",
                    detail=f"Line {index + 1}: {line.strip()[:120]}",
                    remedy="Fit the scaler on X_train only, then transform X_train and X_test.",
                    where=f"entrypoint:{entry}",
                )
                break

    for index, line in enumerate(lines):
        if RESAMPLE_BEFORE_RE.search(line):
            if first_split is None or index < first_split:
                report.add(
                    "DSX-CODE-003",
                    "HIGH",
                    "Resampler (SMOTE / RandomOverSampler / …) before split",
                    detail=f"Line {index + 1}: {line.strip()[:120]}",
                    remedy="Split first; resample only the training fold.",
                    where=f"entrypoint:{entry}",
                )
                break

    if has_model and path.suffix.lower() in {".py", ".ipynb"} and first_split is None:
        report.add(
            "DSX-CODE-010",
            "MEDIUM",
            "model: block present but entrypoint has no declared split marker",
            detail=(
                "Expected train_test_split / TimeSeriesSplit / GroupKFold (or similar) "
                "in the entrypoint when a model is declared."
            ),
            remedy="Split in code and name the method, or document an external split.",
            where=f"entrypoint:{entry}",
        )
    elif first_split is not None:
        report.ok(f"entrypoint split marker at line {first_split + 1}")

    return report


def _resolve_entrypoint(entry: str, phase_dir: "str | None") -> Path | None:
    candidates: list[Path] = []
    if phase_dir:
        candidates.append(Path(phase_dir) / entry)
    candidates.append(Path(entry))
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def _read_source(path: Path) -> str | None:
    suffix = path.suffix.lower()
    if suffix == ".py":
        try:
            return path.read_text(encoding="utf-8")
        except OSError:
            return None
    if suffix == ".ipynb":
        try:
            nb = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        chunks: list[str] = []
        for cell in nb.get("cells") or []:
            if cell.get("cell_type") not in {"code", "markdown"}:
                continue
            src = cell.get("source") or ""
            if isinstance(src, list):
                chunks.append("".join(src))
            else:
                chunks.append(str(src))
        return "\n".join(chunks)
    return None


def _first_line_matching(lines: list[str], markers: tuple[str, ...]) -> int | None:
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if re.match(r"^(from|import)\b", stripped):
            continue
        for marker in markers:
            if marker in line:
                return index
    return None


def _first_fit_leak_line(lines: list[str]) -> int | None:
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if re.match(r"^(from|import)\b", stripped):
            continue
        # Pipeline.fit(X_train) after a split is allowed — still counts as fit;
        # CODE-001 only fires when fit precedes split.
        if PIPELINE_FIT_TRAIN_RE.search(line):
            return index
        for pattern in FIT_LEAK_MARKERS:
            if re.search(pattern, line):
                if "fit(" in line or "fit_transform" in line or "partial_fit" in line:
                    return index
    return None
