"""CSV profiler — produce a hermetic DATA-PROFILE.yaml from a local extract.

Gates never call this. Agents (or humans) run ``dsx profile``; the gate then
compares ANALYSIS-SPEC assertions against the written profile. Stdlib only.
"""

from __future__ import annotations

import csv
import hashlib
import math
import re
import statistics
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


def _extract_hour(value: str) -> "int | None":
    """Return the hour of a timestamp token, or None when no time token is present.

    Additive companion to `_parse_date` (25-RESEARCH.md Pitfall 2): it re-matches
    `_DATE_RE` and reads the optional hour group (group 4). A date-only value or an
    unparseable string carries no clock evidence, so it returns None — never 0. This is
    kept deliberately separate from `_parse_date` and the frozen `dates` accumulator so
    time.min/time.max/time.max_gap_days stay byte-for-byte unchanged.
    """
    match = _DATE_RE.match(value.strip())
    if not match or match.group(4) is None:
        return None
    return int(match.group(4))


def _numeric_block(values: "list[float]") -> dict[str, Any]:
    """D-02 numeric column block: min/q1/median/q3/max/mean/sd/n_zero/n_negative/n.

    Quantiles use statistics.quantiles(..., n=4, method="inclusive") (Hyndman & Fan
    type 7, pinned per 25-RESEARCH.md). mean/sd use statistics.mean/statistics.stdev
    (exact-Fraction accumulation, order-independent) — never fmean, never a hand-rolled
    float loop. Undefined statistics are Python None so `_scalar` renders them as
    YAML `null`, never 0 or NaN.
    """
    n = len(values)
    n_zero = sum(1 for v in values if v == 0)
    n_negative = sum(1 for v in values if v < 0)
    if n == 0:
        return {
            "min": None, "q1": None, "median": None, "q3": None, "max": None,
            "mean": None, "sd": None, "n_zero": 0, "n_negative": 0, "n": 0,
        }
    ordered = sorted(values)
    if n == 1:
        v = ordered[0]
        return {
            "min": v, "q1": v, "median": v, "q3": v, "max": v,
            "mean": v, "sd": None, "n_zero": n_zero, "n_negative": n_negative, "n": 1,
        }
    q1, median, q3 = statistics.quantiles(ordered, n=4, method="inclusive")
    return {
        "min": ordered[0], "q1": q1, "median": median, "q3": q3, "max": ordered[-1],
        "mean": statistics.mean(ordered), "sd": statistics.stdev(ordered),
        "n_zero": n_zero, "n_negative": n_negative, "n": n,
    }


def _categorical_block(counts: "Counter[str]") -> dict[str, Any]:
    """D-02 categorical column block: share_top1/share_top10/rare_share/n_singleton.

    Tie-break is frozen: count desc, then level string asc — computed via an explicit
    `sorted(..., key=lambda kv: (-count, level))`, never `Counter.most_common()` (whose
    tie order is CSV row order / first-insertion order, not the frozen rule). Levels are
    exact raw stripped strings — no trim beyond the existing strip, no case-fold, no
    collation.
    """
    n = sum(counts.values())
    if n == 0:
        return {"share_top1": None, "share_top10": None, "rare_share": None, "n_singleton": 0}
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    share_top1 = ranked[0][1] / n
    top10 = ranked[:10]
    share_top10 = 1.0 if len(ranked) < 10 else sum(c for _, c in top10) / n
    rare = sum(c for _, c in ranked if c < 10 or c / n < 0.001)
    n_singleton = sum(1 for _, c in ranked if c == 1)
    return {
        "share_top1": share_top1, "share_top10": share_top10,
        "rare_share": rare / n, "n_singleton": n_singleton,
    }


def profile_csv(
    path: "str | Path",
    *,
    primary_key: "list[str] | None" = None,
    time_column: "str | None" = None,
    sentinels: "list[Any] | None" = None,
    unit: "str | None" = None,
    target: "str | None" = None,
) -> dict[str, Any]:
    """Compute a DATA-PROFILE mapping from a CSV file."""
    # An explicit empty flag value (`--unit ""` / `--target ""`) means "not declared":
    # coerce to None so the truthiness guards (column-existence, --target-requires-time)
    # and the identity guards (block emission) agree, instead of emitting a degenerate
    # all-null block. Non-empty names still validate against the header as before.
    unit = unit or None
    target = target or None
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
        numeric_values: dict[str, list[float]] = {c: [] for c in columns}
        categorical_counts: dict[str, Counter[str]] = {c: Counter() for c in columns}
        sentinel_hits: Counter[str] = Counter()
        pk_combos: set[tuple[str, ...]] = set()
        pk_dupes = 0
        dates: list[date] = []
        # Additive, separate accumulators (25-RESEARCH.md Pitfall 2): never appended to
        # the frozen `dates` list, so the three time.* keys stay byte-stable.
        hour_of_time_bearing_rows: list[int] = []
        day_counts: Counter[str] = Counter()
        iso_week_counts: Counter[tuple[int, int]] = Counter()
        row_count = 0
        pk = list(primary_key or [])
        for missing in pk:
            if missing not in columns:
                raise CheckError(f"primary key column {missing!r} not in CSV header")
        if time_column and time_column not in columns:
            raise CheckError(f"time column {time_column!r} not in CSV header")
        if unit and unit not in columns:
            raise CheckError(f"unit column {unit!r} not in CSV header")
        # D-03: --target hard-requires --time (the weekly base rate buckets by ISO week
        # of the time column); an unknown header raises CheckError, matching --pk/--time.
        if target and not time_column:
            raise CheckError("--target requires --time")
        if target and target not in columns:
            raise CheckError(f"target column {target!r} not in CSV header")
        unit_counts: Counter[str] = Counter()
        # D-02 target accumulators: raw stripped non-null target values (for overall +
        # the binary validation) and per-ISO-week binary values (for the weekly table).
        target_all: list[str] = []
        target_distinct: set[str] = set()
        target_week_raw: dict[tuple[int, int], list[str]] = {}

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
                if _INT_RE.match(stripped) or _FLOAT_RE.match(stripped):
                    numeric_values[col].append(float(stripped))
                categorical_counts[col][stripped] += 1
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
                raw_time = str(row.get(time_column, ""))
                parsed = _parse_date(raw_time)
                if parsed is not None:
                    dates.append(parsed)
                    day_counts[parsed.isoformat()] += 1
                    iso_year, iso_week = parsed.isocalendar()[:2]
                    iso_week_counts[(iso_year, iso_week)] += 1
                hour = _extract_hour(raw_time)
                if hour is not None:
                    hour_of_time_bearing_rows.append(hour)
            if unit:
                unit_raw = row.get(unit)
                unit_text = "" if unit_raw is None else str(unit_raw)
                if not _is_null(unit_text):
                    unit_counts[unit_text.strip()] += 1
            if target:
                target_raw = row.get(target)
                target_text = "" if target_raw is None else str(target_raw)
                if not _is_null(target_text):
                    target_stripped = target_text.strip()
                    target_all.append(target_stripped)
                    target_distinct.add(target_stripped)
                    # Bucket by (iso_year, iso_week) of the time column (target requires
                    # --time, so time_column is set here). isocalendar() is locale-free
                    # and deterministic; rows whose time cell does not parse are counted
                    # in `overall` (non-null target) but cannot enter a weekly bucket.
                    parsed_target_date = _parse_date(str(row.get(time_column, "")))
                    if parsed_target_date is not None:
                        wk = parsed_target_date.isocalendar()[:2]
                        target_week_raw.setdefault(wk, []).append(target_stripped)

    col_stats: dict[str, Any] = {}
    for col in columns:
        n_non_null = row_count - null_counts[col]
        dtype = _infer_dtype(samples[col])
        col_stats[col] = {
            "null_rate": round(null_counts[col] / row_count, 6) if row_count else 0.0,
            "n_unique": len(uniques[col]),
            "dtype": dtype,
        }
        # D-01: appended LAST, after null_rate/n_unique/dtype, so pre-existing
        # rendered bytes are identical (insertion-order YAML emitter).
        if dtype in ("integer", "float"):
            col_stats[col]["numeric"] = _numeric_block(numeric_values[col])
        elif dtype in ("string", "mixed"):
            col_stats[col]["categorical"] = _categorical_block(categorical_counts[col])

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

    # D-01/D-02: append the additive time keys AFTER max_gap_days, only when a time
    # column is declared — so a profile without --time keeps the frozen 4-key time block
    # byte-identical (the 25-01 pre-existing-key golden is the trip-wire). Every
    # undefined value is Python None (rendered as YAML `null`), never 0.
    if time_column:
        if day_counts:
            day_values = sorted(day_counts.values())
            time_block["rows_per_day"] = {
                "min": min(day_values),
                "median": statistics.median(day_values),
                "max": max(day_values),
            }
        else:
            time_block["rows_per_day"] = {"min": None, "median": None, "max": None}

        first_period_ratio: "float | None" = None
        last_period_ratio: "float | None" = None
        if len(iso_week_counts) >= 5:
            # Populated weeks sorted by (iso_year, iso_week); order-independent.
            ordered_weeks = [c for _, c in sorted(iso_week_counts.items(), key=lambda kv: kv[0])]
            first_period_ratio = ordered_weeks[0] / statistics.mean(ordered_weeks[1:5])
            last_period_ratio = ordered_weeks[-1] / statistics.mean(ordered_weeks[-5:-1])
        time_block["first_period_ratio"] = first_period_ratio
        time_block["last_period_ratio"] = last_period_ratio

        if hour_of_time_bearing_rows:
            zeros = sum(1 for h in hour_of_time_bearing_rows if h == 0)
            time_block["share_at_hour_00"] = zeros / len(hour_of_time_bearing_rows)
        else:
            time_block["share_at_hour_00"] = None

    found_sentinels = sorted({s for s, n in sentinel_hits.items() if n > 0})

    profile: dict[str, Any] = {
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

    # D-01: `unit` is a NEW top-level block appended AFTER sentinels_found, and omitted
    # entirely (never null) when no unit column is declared. rows_per_unit uses type-7
    # (inclusive) quantiles over per-unit row counts; <2 distinct units -> p50/p95 null,
    # max defined for >=1. largest_unit_share picks the winner via an explicit
    # (count desc, unit-string asc) tie-break (the tie-break does not change the value).
    if unit is not None:
        per_unit = sorted(unit_counts.values())
        if len(per_unit) >= 2:
            cuts = statistics.quantiles(per_unit, n=100, method="inclusive")
            p50: "float | None" = cuts[49]
            p95: "float | None" = cuts[94]
        else:
            p50 = None
            p95 = None
        max_unit = max(per_unit) if per_unit else None
        if per_unit and row_count:
            ranked = sorted(unit_counts.items(), key=lambda kv: (-kv[1], kv[0]))
            largest_unit_share: "float | None" = ranked[0][1] / row_count
        else:
            largest_unit_share = None
        profile["unit"] = {
            "rows_per_unit": {"p50": p50, "p95": p95, "max": max_unit},
            "largest_unit_share": largest_unit_share,
        }

    # D-01/D-02: `target` is a NEW top-level block appended AFTER the unit block (or after
    # sentinels_found when no unit is declared), and omitted entirely (never null) when no
    # target column is declared — so the 25-01/25-02 no-flag golden stays byte-identical.
    if target is not None:
        # D-03 / 25-RESEARCH.md Pitfall 4: closed check against the literal set {"0","1"}.
        # No reuse of any truthy/falsy coercion — yes/no/true/false must fail. The error
        # lists EVERY distinct offending value (sorted, deterministic) so it is actionable.
        offending = sorted(v for v in target_distinct if v not in {"0", "1"})
        if offending:
            raise CheckError(
                f"target column {target!r} must be binary {{0,1}}; "
                f"offending value(s): {', '.join(offending)}"
            )
        binary_all = [int(v) for v in target_all]
        overall: "float | None" = statistics.mean(binary_all) if binary_all else None
        # Weekly base-rate table, ordered by (iso_year, iso_week) — order-independent.
        weekly: list[dict[str, Any]] = []
        for wk in sorted(target_week_raw.keys()):
            vals = [int(v) for v in target_week_raw[wk]]
            weekly.append({
                "week": [wk[0], wk[1]],
                "n": len(vals),
                "base_rate": statistics.mean(vals) if vals else None,
            })
        populated = [w["base_rate"] for w in weekly if w["base_rate"] is not None]
        weekly_range = [min(populated), max(populated)] if populated else None
        # verdict = 'drifting' iff any week base_rate < 0.8*overall OR > 1.2*overall
        # (strict, multiplicative to dodge divide-by-zero); null when <2 populated weeks.
        # Baseline population note (accepted residual, review LOW #2): `overall` is the
        # base rate over ALL non-null-target rows, whereas the weekly rates cover only
        # rows whose time cell parsed into a week. When every target row has a parseable
        # timestamp (the shipped case) the two populations coincide; a material fraction
        # of untimed target rows would draw the baseline from a superset of the weekly
        # population. `verdict` is a coarse producer heuristic, never a gate input.
        if len(populated) >= 2 and overall is not None:
            lo, hi = 0.8 * overall, 1.2 * overall
            verdict: "str | None" = (
                "drifting" if any(r < lo or r > hi for r in populated) else "stable"
            )
        else:
            verdict = None
        profile["target"] = {
            "overall": overall,
            "weekly": weekly,
            "weekly_range": weekly_range,
            "verdict": verdict,
        }

    return profile


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
