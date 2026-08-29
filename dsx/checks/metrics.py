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

RECONCILIATION_CLASS_TOLERANCES = {
    "financial": 0.005,
    "user": 0.02,
    "behavioral": 0.05,
    "default": DEFAULT_RECONCILIATION_TOLERANCE,
}


def check(spec: dict) -> Report:
    report = Report(check="metrics")
    metrics = items(spec, "metrics")
    registry = {normalize(m.get("name", "")): m for m in metrics if m.get("name")}

    _check_registry_coverage(spec, registry, report)
    _check_definition_collisions(metrics, report)
    _check_reconciliation(metrics, report)
    _check_denominator_drift(spec, report)
    _check_cohort_denominator_shift(spec, report)
    _check_simpsons_paradox(spec, report)
    _check_time_semantics(metrics, report)
    _check_warehouse_sql(metrics, report)
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

        recon_class = normalize(str(recon.get("class") or "default")) or "default"
        if recon.get("class") is not None and recon_class not in RECONCILIATION_CLASS_TOLERANCES:
            report.add(
                "DSX-MET-012",
                "MEDIUM",
                f"Unknown reconciliation class {recon.get('class')!r} for {metric.get('name')!r}",
                detail=(
                    "Known classes: "
                    + ", ".join(sorted(RECONCILIATION_CLASS_TOLERANCES))
                    + "."
                ),
                remedy="Use financial | user | behavioral | default, or set an explicit tolerance.",
                where=f"{where}.class",
            )
            class_default = DEFAULT_RECONCILIATION_TOLERANCE
        else:
            class_default = RECONCILIATION_CLASS_TOLERANCES.get(
                recon_class, DEFAULT_RECONCILIATION_TOLERANCE
            )

        tolerance = as_number(recon.get("tolerance"))
        if tolerance is None:
            tolerance = class_default

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
                    f"{worst_gap:.2%}, above the declared tolerance of {tolerance:.2%}"
                    f" (class={recon_class}). "
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
                recon_class=recon_class,
            )
        else:
            report.ok(f"{metric.get('name')} reconciles within {tolerance:.2%} ({recon_class})")


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


def _check_cohort_denominator_shift(spec: dict, report: Report) -> None:
    """Changing-denominator / bucket mix-shift on a declared cohort comparison.

    Citation: Crook, Frasca, Kohavi & Longbotham (2009), "Seven Pitfalls to Avoid
    when Running Controlled Experiments on the Web", KDD '09, pp. 1105-1114,
    DOI 10.1145/1557019.1557139, Section 6 "Pitfall 4" (Table 1, Simpson's paradox
    from combining metrics over subpopulations sampled at different rates). This is
    DISTINCT from ratio-metric dilution (Deng & Hu 2015, Formula (3)), which is
    permanently out of scope for the declaration gate (brief.md:450), and from
    INT-030 triggered-vs-eligible dilution: this check reads declared allocation
    shares only and sums no per-unit data.

    Structural criterion: fires DSX-MET-021 (HIGH) when a declared
    results.cohort_comparisons entry's bucket sampling_rate spread (or, as a
    fallback, treatment_share spread) exceeds the declared-or-0.10-default
    tolerance AND `reweighted` is not the literal boolean True. It reads
    results.cohort_comparisons, never results.period_comparisons.
    """
    comparisons = items(section(spec, "results"), "cohort_comparisons")
    for index, comparison in enumerate(comparisons):
        if not isinstance(comparison, dict):
            continue
        where = f"spec.results.cohort_comparisons[{index}]"
        buckets = comparison.get("buckets")
        if not isinstance(buckets, list):
            continue
        axis = "sampling_rate"
        values = [
            v
            for v in (as_number(b.get("sampling_rate")) for b in buckets if isinstance(b, dict))
            if v is not None
        ]
        if len(values) < 2:
            axis = "treatment_share"
            values = [
                v
                for v in (
                    as_number(b.get("treatment_share")) for b in buckets if isinstance(b, dict)
                )
                if v is not None
            ]
        if len(values) < 2:
            continue  # nothing declared to compare
        spread = max(values) - min(values)
        tolerance = as_number(comparison.get("sampling_tolerance"))
        if tolerance is None:
            tolerance = 0.10
        reweighted = comparison.get("reweighted")
        metric_name = comparison.get("metric", "metric")
        if spread > tolerance and reweighted is not True:
            report.add(
                "DSX-MET-021",
                "HIGH",
                "metric pooled across buckets sampled at different rates with no reweighting declared",
                detail=(
                    f"{metric_name!r}: bucket {axis} values {values} span {spread:.4g}, above the "
                    f"declared-or-default tolerance of {tolerance:.4g}, with no reweighting declared. "
                    "Pooling across buckets sampled at different rates makes the aggregate a mix "
                    "artifact, not a performance change."
                ),
                remedy=(
                    "Declare reweighted: true after reweighting each bucket to a fixed allocation, "
                    "compare within stable-allocation epochs, or hold the sampling rate constant."
                ),
                where=where,
                spread=round(spread, 4),
                tolerance=tolerance,
            )
        else:
            report.ok(f"cohort allocation stable for {metric_name}")


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
                    "DSX-MET-041",
                    "MEDIUM",
                    f"Time-grained metric {metric.get('name')!r} declares no timezone",
                    detail=(
                        "Daily aggregates computed in UTC and in local time disagree for every "
                        "event near midnight — usually a few percent, always unexplained."
                    ),
                    remedy="Declare the timezone the date boundary is evaluated in.",
                    where=f"spec.metrics[{index}].timezone",
                )


_WAREHOUSE_SOURCE_RE = re.compile(
    r"(?i)^(warehouse\.|dbt\.)|[A-Za-z_][\w]*\.[A-Za-z_][\w]*\.[A-Za-z_][\w]*"
)


def _check_warehouse_sql(metrics: list[dict], report: Report) -> None:
    for index, metric in enumerate(metrics):
        source = str(metric.get("source") or "")
        if not source or not _WAREHOUSE_SOURCE_RE.search(source):
            continue
        sql = metric.get("sql")
        if isinstance(sql, str) and sql.strip():
            continue
        report.add(
            "DSX-MET-040",
            "HIGH",
            f"Warehouse-like source {source!r} has no sql definition",
            detail=(
                "Sources matching warehouse., dbt., or catalog.schema.table need the SQL "
                "that produces the metric — otherwise two teams invent two queries."
            ),
            remedy="Add metrics[].sql for this source, or point source at a documented view.",
            where=f"spec.metrics[{index}].sql",
        )


# ── SQL lint ─────────────────────────────────────────────────────────────────

# Pattern-based rules applied after comment strip. Codes SQL-007/011/012 need
# extra logic in `_lint_sql`; string literals below keep the catalogue complete.
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
    (
        "DSX-SQL-008",
        r"(?:=|!=|<>)\s*NULL\b",
        "HIGH",
        "= NULL / != NULL is always unknown in SQL; use IS NULL / IS NOT NULL.",
        "Replace with IS NULL or IS NOT NULL.",
    ),
    (
        "DSX-SQL-009",
        r"\bSELECT\s+\*",
        "MEDIUM",
        "SELECT * couples the metric to every column change and hides grain.",
        "List the columns the metric actually needs.",
    ),
    (
        "DSX-SQL-013",
        r"\bCOUNT\s*\(\s*DISTINCT\s*\*\s*\)",
        "MEDIUM",
        "COUNT(DISTINCT *) is invalid or meaningless in most engines.",
        "Count a specific key: COUNT(DISTINCT id).",
    ),
    (
        "DSX-SQL-014",
        r"\bSUM\s*\(\s*[A-Za-z_][A-Za-z0-9_.]*\s*/\s*[A-Za-z_]",
        "HIGH",
        "SUM of per-row ratios is not a ratio of sums.",
        "Compute SUM(numerator) / NULLIF(SUM(denominator), 0) instead.",
    ),
]

_AGGREGATE_RE = re.compile(r"\b(SUM|COUNT|AVG)\s*\(", re.IGNORECASE)
_JOIN_RE = re.compile(r"\bJOIN\b", re.IGNORECASE)
_DISTINCT_RE = re.compile(r"\bDISTINCT\b", re.IGNORECASE)
_DIVISION_RE = re.compile(r"(?<![=<>!])/(?![/=*])\s*(?:\w|\()")
_NULLIF_RE = re.compile(r"\bNULLIF\b", re.IGNORECASE)
_CROSS_JOIN_RE = re.compile(r"\bCROSS\s+JOIN\b", re.IGNORECASE)
_JOIN_CLAUSE_RE = re.compile(
    r"\b(?:(?:INNER|LEFT|RIGHT|FULL|LEFT\s+OUTER|RIGHT\s+OUTER|FULL\s+OUTER)\s+)?"
    r"JOIN\b",
    re.IGNORECASE,
)


def _lint_sql(metric: dict, where: str, report: Report) -> None:
    sql = metric.get("sql")
    if not isinstance(sql, str) or not sql.strip():
        return
    name = metric.get("name", "metric")
    stripped = re.sub(r"--[^\n]*", " ", sql)
    stripped = re.sub(r"/\*.*?\*/", " ", stripped, flags=re.DOTALL)

    for code, pattern, severity, detail, remedy in _SQL_RULES:
        if re.search(pattern, stripped, re.IGNORECASE):
            report.add(
                code,
                severity,
                f"SQL for {name!r}: {detail.split('.')[0]}",
                detail=detail,
                remedy=remedy,
                where=f"{where}.sql",
            )

    if _DIVISION_RE.search(stripped) and not _NULLIF_RE.search(stripped):
        report.add(
            "DSX-SQL-007",
            "HIGH",
            f"SQL for {name!r}: Division without nearby NULLIF",
            detail=(
                "Division in metric SQL without nearby NULLIF — divide-by-zero yields "
                "NULL or error."
            ),
            remedy="Wrap the denominator: NULLIF(denominator, 0).",
            where=f"{where}.sql",
        )

    if _CROSS_JOIN_RE.search(stripped):
        has_where = bool(re.search(r"\bWHERE\b", stripped, re.IGNORECASE))
        has_on = bool(re.search(r"\bON\b", stripped, re.IGNORECASE))
        if not has_where and not has_on:
            report.add(
                "DSX-SQL-011",
                "HIGH",
                f"SQL for {name!r}: CROSS JOIN without WHERE/ON",
                detail="CROSS JOIN without a restricting WHERE/ON explodes the row count.",
                remedy="Add a join predicate, or replace with an intentional filtered cross join.",
                where=f"{where}.sql",
            )

    for match in _JOIN_CLAUSE_RE.finditer(stripped):
        start = match.start()
        chunk = stripped[start : start + 180]
        if re.match(r"(?i)\bCROSS\s+JOIN\b", chunk):
            continue
        if re.search(r"(?i)\bNATURAL\s+", stripped[max(0, start - 12) : start + 20]):
            continue
        tail = stripped[match.end() :]
        next_boundary = re.search(
            r"\b(?:JOIN|WHERE|GROUP\s+BY|ORDER\s+BY|LIMIT|UNION|INTERSECT|EXCEPT)\b|;",
            tail,
            re.IGNORECASE,
        )
        region = tail[: next_boundary.start()] if next_boundary else tail[:200]
        if not re.search(r"\bON\b", region, re.IGNORECASE):
            if not re.search(r"\bUSING\s*\(", region, re.IGNORECASE):
                report.add(
                    "DSX-SQL-012",
                    "HIGH",
                    f"SQL for {name!r}: JOIN without ON",
                    detail="JOIN without ON (after comment strip) is an implicit cross product.",
                    remedy="Add an ON clause, or use CROSS JOIN deliberately with a filter.",
                    where=f"{where}.sql",
                )
                break

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
