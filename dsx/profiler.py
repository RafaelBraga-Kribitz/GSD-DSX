"""CSV profiler — produce a hermetic DATA-PROFILE.yaml from a local extract.

Gates never call this. Agents (or humans) run ``dsx profile``; the gate then
compares ANALYSIS-SPEC assertions against the written profile. Stdlib only.
"""

from __future__ import annotations

import csv
import hashlib
import math
import re
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any, Iterable

from .findings import CheckError

PROFILE_VERSION = 1
COMPUTED_BY = "dsx-profile"

_DATE_RE = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})(?:[ T](\d{2}):(\d{2})(?::(\d{2}))?)?"
)
_INT_RE = re.compile(r"^[+-]?\d+$")
_FLOAT_RE = re.compile(r"^[+-]?(\d+\.\d*|\.\d+)([eE][+-]?\d+)?$")
_NULLISH = {"", "null", "none", "na", "n/a", "nan", "#n/a"}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _is_null(value: str) -> bool:
    return value.strip().lower() in _NULLISH


def _infer_dtype(samples: Iterable[str]) -> str:
    seen = set()
    for raw in samples:
        if _is_null(raw):
            continue
        text = raw.strip()
        if _DATE_RE.match(text):
            seen.add("date")
        elif _INT_RE.match(text):
            seen.add("integer")
        elif _FLOAT_RE.match(text):
            seen.add("float")
        else:
            seen.add("string")
        if len(seen) > 1 and "string" in seen:
            return "mixed"
    if not seen:
        return "string"
    if seen == {"integer", "float"}:
        return "float"
    if len(seen) == 1:
        return next(iter(seen))
    return "mixed"


def _parse_date(value: str) -> date | None:
    match = _DATE_RE.match(value.strip())
    if not match:
        return None
    year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
    try:
        return date(year, month, day)
    except ValueError:
        return None


def profile_csv(
    path: "str | Path",
    *,
    primary_key: "list[str] | None" = None,
    time_column: "str | None" = None,
    sentinels: "list[Any] | None" = None,
) -> dict[str, Any]:
    """Compute a DATA-PROFILE mapping from a CSV file."""
    csv_path = Path(path)
    if not csv_path.exists():
        raise CheckError(f"CSV not found: {csv_path}")
    if csv_path.suffix.lower() not in {".csv", ".tsv", ".txt"}:
        raise CheckError(
            f"dsx profile currently supports CSV only (got {csv_path.suffix!r}). "
            "Export the extract to CSV, or write a measured_export profile by hand."
        )

    sentinel_set = {str(s) for s in (sentinels or [])}
    source_hash = file_sha256(csv_path)

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        sample = handle.read(8192)
        handle.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",\t|;")
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(handle, dialect=dialect)
        if not reader.fieldnames:
            raise CheckError(f"{csv_path}: CSV has no header row")

        columns = list(reader.fieldnames)
        null_counts: dict[str, int] = {c: 0 for c in columns}
        uniques: dict[str, set[str]] = {c: set() for c in columns}
        samples: dict[str, list[str]] = {c: [] for c in columns}
        sentinel_hits: Counter[str] = Counter()
        pk_combos: set[tuple[str, ...]] = set()
        pk_dupes = 0
        dates: list[date] = []
        row_count = 0
        pk = list(primary_key or [])
        for missing in pk:
            if missing not in columns:
                raise CheckError(f"primary key column {missing!r} not in CSV header")
        if time_column and time_column not in columns:
            raise CheckError(f"time column {time_column!r} not in CSV header")

        for row in reader:
            row_count += 1
            if pk:
                key = tuple(str(row.get(col, "")).strip() for col in pk)
                if key in pk_combos:
                    pk_dupes += 1
                else:
                    pk_combos.add(key)
            for col in columns:
                raw = row.get(col)
                text = "" if raw is None else str(raw)
                if _is_null(text):
                    null_counts[col] += 1
                    continue
                stripped = text.strip()
                uniques[col].add(stripped)
                if len(samples[col]) < 50:
                    samples[col].append(stripped)
                if stripped in sentinel_set or (
                    _FLOAT_RE.match(stripped) and stripped in sentinel_set
                ):
                    sentinel_hits[stripped] += 1
                # Also match numeric sentinel forms like -1.0 vs -1
                for sent in list(sentinel_set):
                    try:
                        if math.isclose(float(stripped), float(sent)):
                            sentinel_hits[sent] += 1
                    except ValueError:
                        pass
            if time_column:
                parsed = _parse_date(str(row.get(time_column, "")))
                if parsed is not None:
                    dates.append(parsed)

    col_stats: dict[str, Any] = {}
    for col in columns:
        n_non_null = row_count - null_counts[col]
        col_stats[col] = {
            "null_rate": round(null_counts[col] / row_count, 6) if row_count else 0.0,
            "n_unique": len(uniques[col]),
            "dtype": _infer_dtype(samples[col]),
        }

    duplicate_rate = 0.0
    primary_key_unique = True
    if pk and row_count:
        duplicate_rate = round(pk_dupes / row_count, 6)
        primary_key_unique = pk_dupes == 0

    time_block: dict[str, Any] = {
        "column": time_column,
        "min": None,
        "max": None,
        "max_gap_days": None,
    }
    if dates:
        dates.sort()
        time_block["min"] = dates[0].isoformat()
        time_block["max"] = dates[-1].isoformat()
        max_gap = 0
        for earlier, later in zip(dates, dates[1:]):
            gap = (later - earlier).days
            if gap > max_gap:
                max_gap = gap
        time_block["max_gap_days"] = max_gap

    found_sentinels = sorted({s for s, n in sentinel_hits.items() if n > 0})

    return {
        "profile_version": PROFILE_VERSION,
        "computed_by": COMPUTED_BY,
        "source_path": str(csv_path).replace("\\", "/"),
        "source_hash": source_hash,
        "row_count": row_count,
        "columns": col_stats,
        "primary_key": pk,
        "primary_key_unique": primary_key_unique,
        "duplicate_rate": duplicate_rate,
        "time": time_block,
        "sentinels_found": found_sentinels,
    }


def dump_profile_yaml(profile: dict[str, Any]) -> str:
    """Serialize a profile mapping to a YAML subset (stdlib only)."""
    return _dump(profile) + "\n"


def _dump(value: Any, indent: int = 0) -> str:
    pad = "  " * indent
    if isinstance(value, dict):
        if not value:
            return "{}"
        lines = []
        for key, item in value.items():
            key_s = str(key)
            if isinstance(item, dict):
                if not item:
                    lines.append(f"{pad}{key_s}: {{}}")
                else:
                    lines.append(f"{pad}{key_s}:")
                    lines.append(_dump(item, indent + 1))
            elif isinstance(item, list):
                if not item:
                    lines.append(f"{pad}{key_s}: []")
                elif all(not isinstance(x, (dict, list)) for x in item):
                    rendered = ", ".join(_scalar(x) for x in item)
                    lines.append(f"{pad}{key_s}: [{rendered}]")
                else:
                    lines.append(f"{pad}{key_s}:")
                    for elem in item:
                        if isinstance(elem, dict):
                            lines.append(f"{pad}  -")
                            # indent dict under list item
                            nested = _dump(elem, indent + 2)
                            lines.append(nested)
                        else:
                            lines.append(f"{pad}  - {_scalar(elem)}")
            else:
                lines.append(f"{pad}{key_s}: {_scalar(item)}")
        return "\n".join(lines)
    if isinstance(value, list):
        if not value:
            return "[]"
        return "\n".join(f"{pad}- {_scalar(item)}" for item in value)
    return f"{pad}{_scalar(value)}"


def _scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return "null"
        text = f"{value:.6f}".rstrip("0").rstrip(".")
        return text if text else "0"
    text = str(value)
    if text == "" or any(c in text for c in ":#{}[]&*!|>%@`'\",\n") or text.strip() != text:
        escaped = text.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return text


def write_profile(profile: dict[str, Any], out_path: "str | Path") -> Path:
    target = Path(out_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(dump_profile_yaml(profile), encoding="utf-8")
    return target
