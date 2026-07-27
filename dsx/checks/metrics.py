"""Metric and BI-semantics checks. Codes DSX-MET-* and DSX-SQL-*.

Most "the numbers don't match" incidents are not data problems. They are
definition problems — two teams computing the same word with different
denominators, grains or filters. These checks force the definition into the open
and then verify the arithmetic that follows from it.
"""

from __future__ import annotations

import re

from ..findings import Report
from ..spec import as_number, get, is_blank, items, normalize, section

DEFAULT_RECONCILIATION_TOLERANCE = 0.01  # 1% relative difference


def check(spec: dict) -> Report:
    report = Report(check="metrics")
    metrics = items(spec, "metrics")
    registry = {normalize(m.get("name", "")): m for m in metrics if m.get("name")}

    _check_registry_coverage(spec, registry, report)
    _check_definition_collisions(metrics, report)
    _check_reconciliation(metrics, report)
    _check_denominator_drift(spec, report)
    _check_simpsons_paradox(spec, report)
    _check_time_semantics(metrics, report)
    for index, metric in enumerate(metrics):
        _lint_sql(metric, f"spec.metrics[{index}]", report)
    return report


# ── Registry ─────────────────────────────────────────────────────────────────


def _check_registry_coverage(spec: dict, registry: dict, report: Report) -> None:
    referenced: set[str] = set()
    for test in items(section(spec, "results"), "tests"):
        if test.get("metric"):
            referenced.add(normalize(test["metric"]))
    family = get(spec, "design.multiplicity.family")
    if isinstance(family, list):
        referenced.update(normalize(f) for f in family if isinstance(f, str))
    guardrails = get(spec, "design.guardrail_metrics")
    if isinstance(guardrails, list):
        referenced.update(normalize(g) for g in guardrails if isinstance(g, str))

    unknown = sorted(referenced - set(registry))
    if unknown:
        report.add(
            "DSX-MET-001",
            "HIGH",
            f"{len(unknown)} metric(s) are used but never defined",
            detail=(
                "Referenced without a definition: "
                + ", ".join(unknown)
                + ". Defined: "
                + (", ".join(sorted(registry)) or "(none)")
            ),
            remedy="Add each to spec.metrics with definition, grain, numerator and denominator.",
            where="spec.metrics",
            unknown=unknown,
        )
    elif referenced:
        report.ok(f"all {len(referenced)} referenced metrics are defined")


def _check_definition_collisions(metrics: list[dict], report: Report) -> None:
    by_definition: dict[str, list[str]] = {}
    for metric in metrics:
        definition = normalize(metric.get("definition", ""))
        name = metric.get("name")
        if not definition or not name:
            continue
        by_definition.setdefault(definition, []).append(str(name))

    for definition, names in by_definition.items():
        if len(names) > 1:
            report.add(
                "DSX-MET-002",
                "MEDIUM",
                f"{len(names)} metrics share one definition: {', '.join(names)}",
                detail=(
                    "Identical definitions under different names guarantee that two dashboards "
                    "will diverge the moment one is edited."
                ),
                remedy="Keep one canonical name and alias the rest, or differentiate the definitions.",
                where="spec.metrics",
            )


# ── Reconciliation ───────────────────────────────────────────────────────────


def _check_reconciliation(metrics: list[dict], report: Report) -> None:
    for index, metric in enumerate(metrics):
        where = f"spec.metrics[{index}].reconciliation"
        recon = metric.get("reconciliation")
        if not isinstance(recon, dict):
            continue
        sources = recon.get("sources")
        if not isinstance(sources, list) or len(sources) < 2:
            continue

        tolerance = as_number(recon.get("tolerance"))
        if tolerance is None:
            tolerance = DEFAULT_RECONCILIATION_TOLERANCE

        values: list[tuple[str, float]] = []
        for source in sources:
            if not isinstance(source, dict):
                continue
            value = as_number(source.get("value"))
            if value is not None:
                values.append((str(source.get("name", "?")), value))

        if len(values) < 2:
            report.add(
                "DSX-MET-010", "MEDIUM",
                f"Reconciliation for {metric.get('name')!r} declares sources but no values",
                remedy="Record the measured value from each source so the gap can be computed.",
                where=where,
            )
            continue

        reference_name, reference = values[0]
        worst_name, worst_gap = reference_name, 0.0
        for name, value in values[1:]:
            denominator = abs(reference) if reference else max(abs(value), 1e-12)
            gap = abs(value - reference) / denominator
            if gap > worst_gap:
                worst_name, worst_gap = name, gap

        if worst_gap > tolerance:
            report.add(
                "DSX-MET-011",
                "HIGH",
                f"Metric {metric.get('name')!r} differs {worst_gap:.2%} across sources",
                detail=(
                    f"'{reference_name}'={reference:,.6g} vs '{worst_name}' differs by "
                    f"{worst_gap:.2%}, above the declared tolerance of {tolerance:.2%}. "
                    "Values: " + "; ".join(f"{n}={v:,.6g}" for n, v in values)
                ),
                remedy=(
                    "Reconcile before publishing. Work the usual order: time zone and date "
                    "boundary, filters and exclusions, join fan-out, late-arriving rows, then "
                    "deduplication rules."
                ),
                where=where,
                gap=round(worst_gap, 6),
                tolerance=tolerance,
            )
        else:
            report.ok(f"{metric.get('name')} reconciles within {tolerance:.2%}")


def _check_denominator_drift(spec: dict, report: Report) -> None:
    comparisons = items(section(spec, "results"), "period_comparisons")
    for index, comparison in enumerate(comparisons):
        where = f"spec.results.period_comparisons[{index}]"
        base_denominator = as_number(comparison.get("base_denominator"))
        comp_denominator = as_number(comparison.get("comparison_denominator"))
        if base_denominator is None or comp_denominator is None or base_denominator == 0:
            continue
        drift = abs(comp_denominator - base_denominator) / abs(base_denominator)
        threshold = as_number(comparison.get("denominator_tolerance")) or 0.10
        if drift > threshold:
            report.add(
                "DSX-MET-020",
                "HIGH",
                f"Denominator for {comparison.get('metric', 'metric')!r} moved {drift:.1%} between periods",
                detail=(
                    f"{base_denominator:,.6g} -> {comp_denominator:,.6g}. A ratio whose "
                    "denominator shifts this much is not measuring the same population, so the "
                    "period-over-period change is partly composition, not performance."
                ),
                remedy=(
                    "Decompose the change into denominator and numerator contributions, or "
                    "compare on a fixed cohort."
                ),
                where=where,
                drift=round(drift, 4),
            )
        else:
            report.ok(f"denominator stable for {comparison.get('metric', 'metric')}")


# ── Simpson's paradox ────────────────────────────────────────────────────────


def _check_simpsons_paradox(spec: dict, report: Report) -> None:
    results = section(spec, "results")
    overall = as_number(results.get("overall_effect"))
    segments = items(results, "segments")
    if overall is None or len(segments) < 2:
        return

    effects: list[tuple[str, float]] = []
    for segment in segments:
        value = as_number(segment.get("effect"))
        if value is not None:
            effects.append((str(segment.get("name", "?")), value))
    if len(effects) < 2:
        return

    overall_sign = _sign(overall)
    if overall_sign == 0:
        return
    opposing = [(name, value) for name, value in effects if _sign(value) == -overall_sign]

    if len(opposing) == len(effects):
        report.add(
            "DSX-MET-030",
            "CRITICAL",
            "Simpson's paradox: every segment moves opposite to the aggregate",
            detail=(
                f"Aggregate effect {overall:+.6g}, while all {len(effects)} segments show the "
                "opposite sign: "
                + "; ".join(f"{n}={v:+.6g}" for n, v in effects)
                + ". The aggregate is being driven by changing segment mix, not by the effect."
            ),
            remedy=(
                "Report the segment-level effects as the headline. If an aggregate is needed, "
                "standardize the mix or weight segments to a fixed population."
            ),
            where="spec.results.segments",
            overall=overall,
        )
    elif opposing and len(opposing) >= len(effects) / 2:
        report.add(
            "DSX-MET-031",
            "HIGH",
            f"{len(opposing)} of {len(effects)} segments move against the aggregate",
            detail=(
                "Aggregate "
                f"{overall:+.6g}; opposing segments: "
                + "; ".join(f"{n}={v:+.6g}" for n, v in opposing)
                + ". The headline number does not describe most of the population."
            ),
            remedy="Lead with the heterogeneity. A single average here hides the actual finding.",
            where="spec.results.segments",
        )
    else:
        report.ok("segment effects are directionally consistent with the aggregate")


def _sign(value: float) -> int:
    return (value > 0) - (value < 0)


def _check_time_semantics(metrics: list[dict], report: Report) -> None:
    for index, metric in enumerate(metrics):
        if is_blank(metric.get("timezone")) and not is_blank(metric.get("grain")):
            grain = normalize(str(metric.get("grain")))
            if any(token in grain for token in ("day", "date", "week", "month", "hour")):
                report.add(
                    "DSX-MET-040",
                    "MEDIUM",
                    f"Time-grained metric {metric.get('name')!r} declares no timezone",
                    detail=(
                        "Daily aggregates computed in UTC and in local time disagree for every "
                        "event near midnight — usually a few percent, always unexplained."
                    ),
                    remedy="Declare the timezone the date boundary is evaluated in.",
                    where=f"spec.metrics[{index}].timezone",
                )


# ── SQL lint ─────────────────────────────────────────────────────────────────

_SQL_RULES: list[tuple[str, str, str, str, str]] = [
    (
        "DSX-SQL-001",
        r"\bNOT\s+IN\s*\(\s*SELECT",
        "HIGH",
        "NOT IN against a subquery returns no rows when the subquery yields any NULL.",
        "Use NOT EXISTS, or add an IS NOT NULL filter inside the subquery.",
    ),
    (
        "DSX-SQL-002",
        r"\bCOUNT\s*\(\s*\*\s*\)",
        "MEDIUM",
        "COUNT(*) after a LEFT JOIN counts non-matching rows as 1, inflating the result.",
        "Count the specific key column, e.g. COUNT(DISTINCT o.order_id).",
    ),
    (
        "DSX-SQL-003",
        r"\bUNION\b(?!\s+ALL)",
        "LOW",
        "Bare UNION silently deduplicates rows and costs a sort.",
        "Use UNION ALL unless deduplication is intended, and say so if it is.",
    ),
    (
        "DSX-SQL-004",
        r"\bAVG\s*\(\s*[A-Za-z_][A-Za-z0-9_.]*\s*/\s*[A-Za-z_]",
        "HIGH",
        "Averaging a per-row ratio gives an unweighted average of averages.",
        "Compute SUM(numerator) / SUM(denominator) instead.",
    ),
    (
        "DSX-SQL-005",
        r"\bBETWEEN\b[^\n]*\b(timestamp|_at|datetime)\b",
        "MEDIUM",
        "BETWEEN on a timestamp excludes everything after 00:00:00 on the end date.",
        "Use >= start AND < end + 1 day (half-open interval).",
    ),
    (
        "DSX-SQL-006",
        r"\bSELECT\s+DISTINCT\b",
        "LOW",
        "SELECT DISTINCT often patches a join fan-out rather than fixing it.",
        "Confirm the join grain; deduplicate at the source CTE if fan-out is the cause.",
    ),
]

_AGGREGATE_RE = re.compile(r"\b(SUM|COUNT|AVG)\s*\(", re.IGNORECASE)
_JOIN_RE = re.compile(r"\bJOIN\b", re.IGNORECASE)
_DISTINCT_RE = re.compile(r"\bDISTINCT\b", re.IGNORECASE)


def _lint_sql(metric: dict, where: str, report: Report) -> None:
    sql = metric.get("sql")
    if not isinstance(sql, str) or not sql.strip():
        return
    name = metric.get("name", "metric")
    stripped = re.sub(r"--[^\n]*", " ", sql)
    stripped = re.sub(r"/\*.*?\*/", " ", stripped, flags=re.DOTALL)

    for code, pattern, severity, detail, remedy in _SQL_RULES:
        if re.search(pattern, stripped, re.IGNORECASE):
            report.add(code, severity, f"SQL for {name!r}: {detail.split('.')[0]}",
                       detail=detail, remedy=remedy, where=f"{where}.sql")

    joins = len(_JOIN_RE.findall(stripped))
    if joins >= 2 and _AGGREGATE_RE.search(stripped) and not _DISTINCT_RE.search(stripped):
        report.add(
            "DSX-SQL-010",
            "HIGH",
            f"SQL for {name!r} aggregates across {joins} joins with no fan-out guard",
            detail=(
                "Each one-to-many join multiplies rows before aggregation, so sums and counts "
                "are inflated by the fan-out factor. This is the single most common cause of "
                "metrics that disagree between two dashboards."
            ),
            remedy=(
                "Aggregate to the target grain in a CTE before joining, or verify each join is "
                "one-to-one against the declared grain."
            ),
            where=f"{where}.sql",
            joins=joins,
        )
    elif joins:
        report.ok(f"{name}: SQL join grain reviewed")
