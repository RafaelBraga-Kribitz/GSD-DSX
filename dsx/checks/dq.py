"""Data-quality gates. Codes DSX-DQ-*.

Gates stay hermetic: they compare ANALYSIS-SPEC ``data[].assertions`` against a
written DATA-PROFILE.yaml. They never open the warehouse or the CSV. Prefer
producing the profile with ``dsx profile`` so ``computed_by`` and ``source_hash``
are honest.
"""

from __future__ import annotations

from pathlib import Path

from ..findings import Report
from ..loader import SpecParseError, load
from ..spec import as_number, is_blank, items, normalize, section


def check(spec: dict, phase_dir: "str | None" = None) -> Report:
    report = Report(check="dq")
    datasets = items(spec, "data")
    if not datasets:
        report.ok("no data sources declared")
        return report

    roots = _resolve_roots(phase_dir)
    checked = 0
    for index, dataset in enumerate(datasets):
        assertions = dataset.get("assertions")
        if not isinstance(assertions, dict) or not assertions:
            continue
        checked += 1
        where = f"spec.data[{index}]"
        profile_path = dataset.get("profile_path")
        if is_blank(profile_path):
            report.add(
                "DSX-DQ-001",
                "CRITICAL",
                "Data assertions declared but profile is missing or unreadable",
                detail=(
                    f"Dataset {dataset.get('name', index)!r} has assertions with no "
                    "profile_path. Gates cannot verify what was never measured."
                ),
                remedy=(
                    "Run `dsx profile <csv> --out DATA-PROFILE.yaml` (or write a "
                    "measured_export profile) and set data[].profile_path."
                ),
                where=where,
            )
            continue

        profile_file = _find_file(str(profile_path), roots)
        if profile_file is None:
            report.add(
                "DSX-DQ-001",
                "CRITICAL",
                "Data assertions declared but profile is missing or unreadable",
                detail=f"Profile file {profile_path!r} not found under: {', '.join(str(r) for r in roots)}",
                remedy="Create the profile next to the spec, or fix profile_path.",
                where=f"{where}.profile_path",
            )
            continue

        try:
            profile = load(profile_file)
        except SpecParseError as exc:
            report.add(
                "DSX-DQ-001",
                "CRITICAL",
                "Data assertions declared but profile is missing or unreadable",
                detail=str(exc),
                remedy="Fix the YAML or regenerate with `dsx profile`.",
                where=f"{where}.profile_path",
            )
            continue

        _check_row_count(assertions, profile, where, report)
        _check_primary_key(assertions, profile, where, report)
        _check_null_rates(assertions, profile, where, report)
        _check_time_gaps(assertions, profile, where, report)
        _check_sentinels(assertions, profile, where, report)
        _check_manual_honesty(dataset, profile, where, report)

    if checked == 0:
        report.ok("no data assertions to enforce")
    else:
        report.ok(f"{checked} data source(s) checked against profile(s)")
    return report


def _resolve_roots(phase_dir: "str | None") -> list[Path]:
    roots: list[Path] = []
    if phase_dir:
        roots.append(Path(phase_dir))
    roots.append(Path.cwd())
    return roots


def _find_file(relative: str, roots: list[Path]) -> Path | None:
    candidate = Path(relative)
    if candidate.is_absolute() and candidate.exists():
        return candidate
    for root in roots:
        path = root / relative
        if path.exists():
            return path
    if candidate.exists():
        return candidate
    return None


def _check_row_count(
    assertions: dict, profile: dict, where: str, report: Report
) -> None:
    row_assert = assertions.get("row_count")
    if not isinstance(row_assert, dict):
        # Allow bare equals number
        equals = as_number(row_assert) if row_assert is not None else None
        if equals is None:
            return
        row_assert = {"equals": equals, "tol": 0.01}

    observed = as_number(profile.get("row_count"))
    if observed is None:
        report.add(
            "DSX-DQ-010",
            "CRITICAL",
            "Row count fails the declared assertion",
            detail="Profile is missing row_count.",
            remedy="Regenerate the profile with `dsx profile`.",
            where=f"{where}.profile_path",
        )
        return

    tol = as_number(row_assert.get("tol"))
    if tol is None:
        tol = 0.01
    equals = as_number(row_assert.get("equals"))
    minimum = as_number(row_assert.get("min"))
    maximum = as_number(row_assert.get("max"))

    if equals is not None:
        if equals == 0:
            ok = observed == 0
            band = "exactly 0"
        else:
            lo, hi = equals * (1 - tol), equals * (1 + tol)
            ok = lo <= observed <= hi
            band = f"{lo:.0f}–{hi:.0f} (±{tol:.0%} of {equals:g})"
        if not ok:
            report.add(
                "DSX-DQ-010",
                "CRITICAL",
                "Row count fails the declared assertion",
                detail=f"Row count {observed:g} outside asserted band {band}. Profile row_count={observed:g}; assertion equals={equals:g}, tol={tol}.",
                remedy="Refresh the extract, update the assertion, or fix the upstream filter.",
                where=f"{where}.assertions.row_count",
                observed=observed,
                expected=equals,
            )
            return

    if minimum is not None and observed < minimum:
        report.add(
            "DSX-DQ-010",
            "CRITICAL",
            "Row count fails the declared assertion",
            detail=f"Row count {observed:g} below minimum {minimum:g}.",
            where=f"{where}.assertions.row_count",
            remedy="Refresh the extract or lower the assertion only with a known_gaps note.",
        )
        return
    if maximum is not None and observed > maximum:
        report.add(
            "DSX-DQ-010",
            "CRITICAL",
            "Row count fails the declared assertion",
            detail=f"Row count {observed:g} above maximum {maximum:g}.",
            where=f"{where}.assertions.row_count",
            remedy="Investigate fan-out / double-loads, or raise the assertion deliberately.",
        )
        return
    report.ok(f"row_count {observed:g} within assertions")


def _check_primary_key(
    assertions: dict, profile: dict, where: str, report: Report
) -> None:
    pk = assertions.get("primary_key")
    if not pk:
        return
    if profile.get("primary_key_unique") is False:
        rate = as_number(profile.get("duplicate_rate")) or 0.0
        report.add(
            "DSX-DQ-020",
            "CRITICAL",
            "Primary key is not unique in the profile",
            detail=(
                f"Asserted key {pk}; profile reports primary_key_unique=false "
                f"(duplicate_rate={rate})."
            ),
            remedy=(
                "Fix the grain before modelling or aggregating. Deduplicating without "
                "understanding the duplicate cause usually hides the finding."
            ),
            where=f"{where}.assertions.primary_key",
        )
    else:
        report.ok("primary key unique in profile")


def _check_null_rates(
    assertions: dict, profile: dict, where: str, report: Report
) -> None:
    limits = assertions.get("max_null_rate")
    if not isinstance(limits, dict) or not limits:
        return
    columns = profile.get("columns") or {}
    if not isinstance(columns, dict):
        return
    for col, limit_raw in limits.items():
        limit = as_number(limit_raw)
        if limit is None:
            continue
        stats = columns.get(col)
        if not isinstance(stats, dict):
            report.add(
                "DSX-DQ-030",
                "HIGH",
                "Column null rate exceeds the declared maximum",
                detail=f"Null-rate assertion for missing column {col!r} — profile has no stats for this column.",
                remedy="Fix the column name or regenerate the profile.",
                where=f"{where}.assertions.max_null_rate.{col}",
            )
            continue
        observed = as_number(stats.get("null_rate"))
        if observed is None:
            continue
        if observed > limit + 1e-12:
            report.add(
                "DSX-DQ-030",
                "HIGH",
                "Column null rate exceeds the declared maximum",
                detail=f"Null rate for {col!r} is {observed:.4f} > allowed {limit:.4f}. Profile columns.{col}.null_rate={observed}.",
                remedy="Impute with an explicit rule, drop the column, or raise the cap with a gap note.",
                where=f"{where}.assertions.max_null_rate.{col}",
            )
        else:
            report.ok(f"null_rate {col}={observed:.4f} ≤ {limit:.4f}")


def _check_time_gaps(
    assertions: dict, profile: dict, where: str, report: Report
) -> None:
    max_gap = as_number(assertions.get("max_gap_days"))
    if max_gap is None:
        return
    time_block = profile.get("time") or {}
    if not isinstance(time_block, dict):
        return
    observed = as_number(time_block.get("max_gap_days"))
    if observed is None:
        report.add(
            "DSX-DQ-040",
            "HIGH",
            "Time gap exceeds the declared maximum",
            detail="max_gap_days asserted but profile has no time.max_gap_days.",
            remedy="Re-run `dsx profile --time <column>` or remove the assertion.",
            where=f"{where}.assertions.max_gap_days",
        )
        return
    if observed > max_gap + 1e-12:
        report.add(
            "DSX-DQ-040",
            "HIGH",
            "Time gap exceeds the declared maximum",
            detail=(
                f"Time gap of {observed:g} days exceeds allowed {max_gap:g}. "
                f"Profile time column={time_block.get('column')!r}, "
                f"range {time_block.get('min')}..{time_block.get('max')}."
            ),
            remedy="Document the outage in known_gaps or fix the extract continuity.",
            where=f"{where}.assertions.max_gap_days",
        )
    else:
        report.ok(f"max time gap {observed:g}d ≤ {max_gap:g}d")


def _check_sentinels(
    assertions: dict, profile: dict, where: str, report: Report
) -> None:
    banned = assertions.get("banned_sentinels") or []
    if not banned:
        return
    found = profile.get("sentinels_found") or []
    if not isinstance(found, list):
        return
    banned_norm = {str(x) for x in banned}
    hits = [str(x) for x in found if str(x) in banned_norm]
    # Also match numeric equality for -1 vs -1.0
    for item in found:
        for ban in banned:
            try:
                if abs(float(item) - float(ban)) < 1e-12 and str(ban) not in hits:
                    hits.append(str(ban))
            except (TypeError, ValueError):
                continue
    if hits:
        report.add(
            "DSX-DQ-050",
            "HIGH",
            f"Banned sentinel value(s) present: {', '.join(hits)}",
            detail="Sentinels masquerade as real data and corrupt aggregates.",
            remedy="Map sentinels to null in the extract, or remove them from banned_sentinels with a gap note.",
            where=f"{where}.assertions.banned_sentinels",
        )
    else:
        report.ok("no banned sentinels found")


def _check_manual_honesty(
    dataset: dict, profile: dict, where: str, report: Report
) -> None:
    computed_by = normalize(str(profile.get("computed_by", "")))
    if computed_by != "manual":
        return
    if is_blank(dataset.get("known_gaps")):
        report.add(
            "DSX-DQ-060",
            "MEDIUM",
            "Manual profile without a known_gaps note",
            detail=(
                "computed_by: manual means the numbers were not produced by "
                "`dsx profile` or a measured export. Without known_gaps the reader "
                "cannot tell what was guessed."
            ),
            remedy=(
                "Prefer `dsx profile` or measured_export. If the profile must be "
                "manual, document how the numbers were obtained under data[].known_gaps."
            ),
            where=where,
        )
