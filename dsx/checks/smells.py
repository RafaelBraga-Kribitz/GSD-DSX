"""Plot-construction smells. Codes DSX-SMELL-*.

Declaration-only subset of Chart_Audit smells B/G/I/J/K/M. Smells that need
notebook greps stay in references/viz-smells.md for the viz critic.
"""

from __future__ import annotations

from ..findings import Report
from ..spec import as_number, is_blank, items, normalize

DENSITY_MARKS = {"density", "kde", "violin"}
STACKED_MARKS = {"stacked_bar", "stacked_area", "stream"}


def check(spec: dict) -> Report:
    report = Report(check="smells")
    visuals = items(spec, "visuals")
    if not visuals:
        report.ok("no visuals to smell-check")
        return report

    run_ids: list[tuple[int, str]] = []
    for index, visual in enumerate(visuals):
        where = f"spec.visuals[{index}]"
        label = visual.get("name") or f"visual {index}"
        _check_dead_series(visual, label, where, report)
        _check_atoms_under_density(visual, label, where, report)
        _check_stacked_scenarios(visual, label, where, report)
        _check_category_coverage(visual, label, where, report)
        _check_self_correlation(visual, label, where, report)
        rid = visual.get("run_id")
        if not is_blank(rid):
            run_ids.append((index, str(rid).strip()))

    _check_run_id_consistency(run_ids, report)
    report.ok(f"{len(visuals)} visual(s) smell-checked")
    return report


def _check_dead_series(visual: dict, label: str, where: str, report: Report) -> None:
    std = as_number(visual.get("within_group_std"))
    if std is None:
        return
    if abs(std) <= 1e-12:
        report.add(
            "DSX-SMELL-002",
            "CRITICAL",
            f"'{label}' declares within_group_std ≈ 0",
            detail=(
                "Zero within-group variance usually means a scalar was broadcast "
                "into a series, or the wrong column was plotted."
            ),
            remedy="Recompute the series from raw rows; do not plot a constant as variation.",
            where=f"{where}.within_group_std",
        )


def _check_atoms_under_density(
    visual: dict, label: str, where: str, report: Report
) -> None:
    relationship = normalize(str(visual.get("relationship") or ""))
    chart_type = normalize(str(visual.get("type") or ""))
    if relationship != "distribution" or chart_type not in DENSITY_MARKS:
        return
    atomic = visual.get("atomicity") is True
    n_unique = as_number(visual.get("n_unique"))
    few = n_unique is not None and n_unique <= 5
    if atomic or few:
        report.add(
            "DSX-SMELL-007",
            "HIGH",
            f"'{label}' uses {chart_type} on atomic / low-cardinality data",
            detail=(
                "Density/KDE/violin invent continuity where the data are discrete atoms. "
                f"atomicity={visual.get('atomicity')!r}, n_unique={n_unique}."
            ),
            remedy="Use an ECDF, stem, or strip plot instead.",
            where=f"{where}.type",
        )


def _check_stacked_scenarios(
    visual: dict, label: str, where: str, report: Report
) -> None:
    chart_type = normalize(str(visual.get("type") or ""))
    role = normalize(str(visual.get("series_role") or ""))
    if chart_type in STACKED_MARKS and role == "scenario":
        report.add(
            "DSX-SMELL-009",
            "CRITICAL",
            f"'{label}' stacks scenario series",
            detail=(
                "Stacked geometry implies parts of one whole. Scenario / alternative "
                "series must overlay or sit in paired panels."
            ),
            remedy="Set series_role: component only for true parts, or change type to overlay/line.",
            where=f"{where}.series_role",
        )


def _check_category_coverage(
    visual: dict, label: str, where: str, report: Report
) -> None:
    expected = visual.get("expected_categories")
    if not isinstance(expected, list) or not expected:
        return
    count = as_number(visual.get("category_count"))
    if count is None:
        return
    if int(count) != len(expected):
        report.add(
            "DSX-SMELL-010",
            "HIGH",
            f"'{label}' category_count {int(count)} ≠ len(expected_categories)={len(expected)}",
            detail=f"expected_categories={expected!r}. Silent groupby/join drops are common here.",
            remedy="Reconcile plotted categories with the schema, or fix category_count.",
            where=f"{where}.category_count",
        )


def _check_self_correlation(
    visual: dict, label: str, where: str, report: Report
) -> None:
    if visual.get("ratio_of_x") is True:
        report.add(
            "DSX-SMELL-011",
            "HIGH",
            f"'{label}' plots a y that algebraically contains x",
            detail="ratio_of_x: true — this is self-correlation, not an empirical relationship.",
            remedy="Replot against an independent predictor, or show the residual.",
            where=f"{where}.ratio_of_x",
        )
        return
    encodings = visual.get("encodings")
    if not isinstance(encodings, dict):
        return
    x = str(encodings.get("x") or "").strip()
    y = str(encodings.get("y") or "").strip()
    if not x or not y:
        return
    # Patterns like a_over_b vs b, or y literally containing "/x"
    y_norm = y.replace(" ", "").lower()
    x_norm = x.replace(" ", "").lower()
    if y_norm.endswith("/" + x_norm) or y_norm.endswith("_per_" + x_norm):
        report.add(
            "DSX-SMELL-011",
            "HIGH",
            f"'{label}' plots a y that algebraically contains x",
            detail=f"encodings.x={x!r}, encodings.y={y!r}.",
            remedy="Set ratio_of_x deliberately or choose an independent x.",
            where=f"{where}.encodings",
        )


def _check_run_id_consistency(
    run_ids: list[tuple[int, str]], report: Report
) -> None:
    if len(run_ids) < 2:
        return
    unique = {rid for _, rid in run_ids}
    if len(unique) <= 1:
        report.ok(f"shared run_id across {len(run_ids)} visuals")
        return
    detail = ", ".join(f"visuals[{i}]={rid!r}" for i, rid in run_ids)
    report.add(
        "DSX-SMELL-013",
        "HIGH",
        "visuals[] declare disagreeing run_id values",
        detail=detail,
        remedy="Regenerate all figures from one readout, or clear run_id on drafts.",
        where="spec.visuals",
    )
