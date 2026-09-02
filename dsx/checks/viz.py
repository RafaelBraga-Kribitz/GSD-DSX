"""Data-visualization checks. Codes DSX-VIZ-*.

A chart is an argument. These checks enforce the two things that make it an
honest one: the encoding has to match the relationship being shown, and the
geometry has to be proportional to the numbers. Both are decidable from a
declared chart spec — no rendering required, so the check runs in a gate.
"""

from __future__ import annotations

from ..findings import Report
from ..input_types import canonical_id
from ..input_types import get as input_type_record
from ..spec import CHART_CAPABILITIES, DATA_INPUT_TYPES, as_number, is_blank, items, normalize

# Relationship → admissible chart types. The first entry is the default choice.
RELATIONSHIP_CHARTS: dict[str, tuple[str, ...]] = {
    "comparison": ("bar", "horizontal_bar", "dot_plot", "bullet", "butterfly"),
    "trend": ("line", "area", "sparkline", "slope"),
    "part_to_whole": ("stacked_bar", "treemap", "waffle", "pie"),
    "distribution": ("histogram", "box", "violin", "density", "ecdf", "strip", "kde",
                     "population_pyramid"),
    "correlation": ("scatter", "hexbin", "heatmap"),
    "deviation": ("diverging_bar", "waterfall", "dumbbell"),
    "ranking": ("horizontal_bar", "dot_plot", "slope", "bump"),
    "flow": ("sankey", "chord", "funnel"),
    "geographic": ("choropleth", "symbol_map", "cartogram"),
    "composition_over_time": ("stacked_area", "stacked_bar", "stream"),
}

# Chart families whose visual encoding is length from a baseline. Truncating the
# axis breaks the proportionality the reader is decoding.
LENGTH_ENCODED = {"bar", "horizontal_bar", "stacked_bar", "area", "stacked_area", "waterfall",
                  "diverging_bar", "column", "histogram", "waffle", "funnel", "stream",
                  "grouped_bar"}

# A banned mark is a first-class refusal record, never a silent absence
# (REQ-P21-02). Each is {reason, code, citation}: `reason` is the distortion
# the ban prevents, `code` is the finding _check_banned emits (DSX-VIZ-001 for
# all five — a cross-reference to an existing code, not a new one), and
# `citation` points at the perception-doctrine source (HQ-27 Tier-3, drained at
# S5-2). The radar citation is the least-certain of the five — no exact Tier-3
# source is pre-mapped to it — and is flagged for operator confirmation in
# HUMAN-QUEUE HQ-27.
BANNED_TYPES: dict[str, dict[str, str]] = {
    "3d_bar": {
        "reason": "3D bars distort length with perspective and occlude the back rows.",
        "code": "DSX-VIZ-001",
        "citation": "Munzner 2014 ch.6 (no unjustified 3D); Tufte 1983 (chartjunk) — HQ-27 T2-6/T3-3",
    },
    "3d_pie": {
        "reason": "3D pie exaggerates the slices nearest the viewer.",
        "code": "DSX-VIZ-001",
        "citation": "Munzner 2014 ch.6 (no unjustified 3D); Tufte 1983 (chartjunk) — HQ-27 T2-6/T3-3",
    },
    "3d_line": {
        "reason": "3D lines make position unreadable without adding information.",
        "code": "DSX-VIZ-001",
        "citation": "Munzner 2014 ch.6 (no unjustified 3D); Tufte 1983 (chartjunk) — HQ-27 T2-6/T3-3",
    },
    "radar": {
        "reason": "Radar area scales with the square of the value and depends on axis order.",
        "code": "DSX-VIZ-001",
        "citation": "Tufte 1983 / Munzner 2014 proportional-encoding doctrine — PROVISIONAL, "
                    "no exact Tier-3 source pre-mapped; flagged for HQ-27 S5-2 confirmation",
    },
    "dual_axis_line": {
        "reason": "Two y-scales let any pair of series be made to look correlated.",
        "code": "DSX-VIZ-001",
        "citation": "Muth 2018 (Datawrapper) — HQ-27 T3-4; see also DSX-VIZ-030 (_check_dual_axis)",
    },
}

MAX_PIE_SLICES = 5
MAX_CATEGORICAL_COLORS = 7

COMPARISON_TOKENS = (
    "higher", "lower", "vs", "versus", "fell", "grew", "more", "less", "above",
    "below", "increase", "decrease", "up", "down", "gain", "loss", "clear",
    "exceed", "miss", "lead", "lag", "ahead", "behind", "difference", "gap",
)


def check(spec: dict) -> Report:
    report = Report(check="viz")
    visuals = items(spec, "visuals")
    if not visuals:
        return report

    for index, visual in enumerate(visuals):
        where = f"spec.visuals[{index}]"
        label = visual.get("name") or f"visual {index}"
        chart_type = normalize(visual.get("type", ""))

        _check_banned(chart_type, label, where, report)
        _check_relationship_match(visual, chart_type, label, where, report)
        _check_input_type_matrix(visual, chart_type, label, where, report)
        _check_axis_truncation(visual, chart_type, label, where, report)
        _check_dual_axis(visual, label, where, report)
        _check_slice_count(visual, chart_type, label, where, report)
        _check_color(visual, label, where, report)
        _check_labelling(visual, label, where, report)
        _check_uncertainty(visual, label, where, report)
        _check_ordering(visual, chart_type, label, where, report)

    report.ok(f"{len(visuals)} visual(s) audited")
    return report


def _check_banned(chart_type: str, label: str, where: str, report: Report) -> None:
    if chart_type in BANNED_TYPES:
        report.add(
            "DSX-VIZ-001",
            "HIGH",
            f"'{label}' uses {chart_type}, which distorts the data",
            detail=BANNED_TYPES[chart_type]["reason"],
            remedy="Use a 2D length- or position-encoded chart instead.",
            where=f"{where}.type",
        )


def _check_relationship_match(
    visual: dict, chart_type: str, label: str, where: str, report: Report
) -> None:
    relationship = normalize(visual.get("relationship", ""))
    if not relationship:
        report.add(
            "DSX-VIZ-010",
            "MEDIUM",
            f"'{label}' does not declare the relationship it shows",
            detail="Allowed: " + ", ".join(sorted(RELATIONSHIP_CHARTS)),
            remedy="Declare the relationship first; the chart type follows from it.",
            where=f"{where}.relationship",
        )
        return
    admissible = RELATIONSHIP_CHARTS.get(relationship)
    if admissible is None:
        report.add(
            "DSX-VIZ-011", "MEDIUM",
            f"'{label}' declares unrecognised relationship {visual.get('relationship')!r}",
            detail="Allowed: " + ", ".join(sorted(RELATIONSHIP_CHARTS)),
            remedy="Pick the relationship the reader is meant to extract.",
            where=f"{where}.relationship",
        )
        return
    if chart_type and chart_type not in admissible:
        report.add(
            "DSX-VIZ-012",
            "HIGH",
            f"'{label}' shows a {relationship} relationship with a {chart_type} chart",
            detail=(
                f"A {relationship} relationship reads correctly from: {', '.join(admissible)}. "
                f"A {chart_type} encodes a different comparison, so the reader decodes the "
                "wrong quantity."
            ),
            remedy=f"Use {admissible[0]} unless you have a specific reason for another.",
            where=f"{where}.type",
        )
    elif chart_type:
        report.ok(f"'{label}': {chart_type} suits a {relationship} relationship")


def _check_input_type_matrix(
    visual: dict, chart_type: str, label: str, where: str, report: Report
) -> None:
    raw = visual.get("data_input_type")
    if is_blank(raw):
        if chart_type:
            report.add(
                "DSX-VIZ-014",
                "MEDIUM",
                f"'{label}' has no data_input_type",
                detail=(
                    "The input-type × chart matrix catches marks that look plausible for "
                    "the relationship but wrong for the column signature."
                ),
                remedy="Declare data_input_type from `dsx vocab` (see references/data-input-types.md).",
                where=f"{where}.data_input_type",
            )
        return
    # An IT id from the IT001-IT040 inventory is accepted alongside the coarse
    # family names, and is the more precise declaration of the two.
    it_id = canonical_id(str(raw))
    if it_id:
        dit = it_id
        admissible = frozenset(input_type_record(it_id)["admissible"])
    else:
        dit = normalize(str(raw)).replace("_", "-")
        if dit not in DATA_INPUT_TYPES:
            report.add(
                "DSX-VIZ-013",
                "HIGH",
                f"'{label}' chart type conflicts with data_input_type",
                detail=(
                    f"Unrecognised data_input_type {raw!r}. Allowed: "
                    + ", ".join(sorted(DATA_INPUT_TYPES))
                    + "; or an inventory id IT001-IT040 (see `dsx charts --list`)."
                ),
                remedy="Pick a closed data_input_type id.",
                where=f"{where}.data_input_type",
            )
            return
        admissible = CHART_CAPABILITIES.get(dit, frozenset())
    if not chart_type:
        return
    # Accept both underscored and hyphenated mark aliases
    aliases = {chart_type, chart_type.replace("_", "-"), chart_type.replace("-", "_")}
    if not aliases & set(admissible) and chart_type not in admissible:
        report.add(
            "DSX-VIZ-013",
            "HIGH",
            f"'{label}' chart type conflicts with data_input_type",
            detail=(
                f"type {chart_type!r} is not admissible for data_input_type {dit}. "
                f"Admissible marks: {', '.join(sorted(admissible))}."
            ),
            remedy=f"Change type to one of {', '.join(sorted(admissible)[:4])}…, or fix data_input_type.",
            where=f"{where}.type",
        )
    else:
        report.ok(f"'{label}': {chart_type} admitted by {dit}")


def _check_axis_truncation(
    visual: dict, chart_type: str, label: str, where: str, report: Report
) -> None:
    if chart_type not in LENGTH_ENCODED:
        return
    starts_at_zero = visual.get("y_axis_starts_at_zero")
    axis_min = as_number(visual.get("y_axis_min"))
    truncated = starts_at_zero is False or (axis_min is not None and axis_min > 0)
    if truncated:
        report.add(
            "DSX-VIZ-020",
            "CRITICAL",
            f"'{label}' is a {chart_type} chart with a truncated y-axis",
            detail=(
                "Bars and areas encode value as length from the baseline. Starting the axis "
                f"above zero (y_axis_min={axis_min}) makes a small difference look large — the "
                "geometry no longer matches the numbers."
            ),
            remedy=(
                "Set the baseline to zero. If the interesting variation is small, plot the "
                "difference or the percentage change directly, on a chart whose encoding is "
                "position rather than length (dot plot, line)."
            ),
            where=f"{where}.y_axis_min",
        )
    elif starts_at_zero is None:
        report.add(
            "DSX-VIZ-021", "LOW", f"'{label}' does not declare its y-axis baseline",
            remedy="Declare y_axis_starts_at_zero so the check can run.",
            where=f"{where}.y_axis_starts_at_zero",
        )
    else:
        report.ok(f"'{label}': zero baseline on a length-encoded chart")


def _check_dual_axis(visual: dict, label: str, where: str, report: Report) -> None:
    if not visual.get("dual_axis"):
        return
    report.add(
        "DSX-VIZ-030",
        "HIGH",
        f"'{label}' uses two y-axes",
        detail=(
            "The relative scaling of the two axes is arbitrary, so any two series can be made "
            "to appear to move together or apart. Readers reliably infer a relationship that "
            "the chart does not establish."
        ),
        remedy=(
            "Use two aligned panels sharing an x-axis, index both series to a common base, or "
            "plot the ratio explicitly if that is the quantity of interest."
        ),
        where=f"{where}.dual_axis",
    )


def _check_slice_count(
    visual: dict, chart_type: str, label: str, where: str, report: Report
) -> None:
    if chart_type not in ("pie", "donut", "waffle", "treemap"):
        return
    slices = as_number(visual.get("category_count"))
    if slices is None:
        return
    if slices > MAX_PIE_SLICES:
        report.add(
            "DSX-VIZ-040",
            "MEDIUM",
            f"'{label}' is a {chart_type} with {int(slices)} categories",
            detail=(
                f"Angle is a weak encoding; beyond about {MAX_PIE_SLICES} slices readers cannot "
                "rank them reliably, and adjacent small slices become indistinguishable."
            ),
            remedy="Use a sorted horizontal bar chart, or group the tail into 'Other'.",
            where=f"{where}.category_count",
        )
    else:
        report.ok(f"'{label}': {int(slices)} categories within the readable limit")


def _check_color(visual: dict, label: str, where: str, report: Report) -> None:
    colors = as_number(visual.get("color_count"))
    if colors is not None and colors > MAX_CATEGORICAL_COLORS:
        report.add(
            "DSX-VIZ-050",
            "MEDIUM",
            f"'{label}' encodes {int(colors)} categories in colour",
            detail=(
                f"Beyond {MAX_CATEGORICAL_COLORS} hues, categories stop being distinguishable "
                "and the legend becomes a lookup task."
            ),
            remedy="Highlight the two or three that matter, grey the rest, or use small multiples.",
            where=f"{where}.color_count",
        )

    palette = normalize(visual.get("palette", ""))
    if palette in ("red_green", "redgreen", "traffic_light") and not visual.get(
        "redundant_encoding"
    ):
        report.add(
            "DSX-VIZ-051",
            "HIGH",
            f"'{label}' relies on red/green as its only distinction",
            detail=(
                "Roughly 8% of men and 0.5% of women cannot separate these hues, so for those "
                "readers the chart carries no information at all."
            ),
            remedy=(
                "Add a redundant encoding — shape, position, direct labels — or switch to a "
                "colourblind-safe diverging palette such as blue/orange."
            ),
            where=f"{where}.palette",
        )

    if normalize(visual.get("scale_type", "")) == "rainbow":
        report.add(
            "DSX-VIZ-052",
            "MEDIUM",
            f"'{label}' uses a rainbow colour scale for a continuous variable",
            detail="Rainbow scales are not perceptually uniform; they invent boundaries where the data is smooth.",
            remedy="Use a perceptually uniform sequential scale (viridis, cividis, magma).",
            where=f"{where}.scale_type",
        )


def _check_labelling(visual: dict, label: str, where: str, report: Report) -> None:
    takeaway = visual.get("takeaway")
    name = str(visual.get("name") or "")
    if is_blank(takeaway):
        report.add(
            "DSX-VIZ-060",
            "MEDIUM",
            f"'{label}' has no takeaway title",
            detail=(
                "A title naming the variables ('Revenue by region') asks the reader to find the "
                "point. A title stating it ('EMEA revenue fell 12% while every other region grew') "
                "delivers it."
            ),
            remedy="Write the title as the sentence you want remembered.",
            where=f"{where}.takeaway",
        )
        report.add(
            "DSX-VIZ-063",
            "HIGH",
            f"'{label}' takeaway is blank or identical to the chart name",
            detail="An empty takeaway is not an argument.",
            remedy="Write a takeaway sentence that states the finding.",
            where=f"{where}.takeaway",
        )
    else:
        takeaway_s = str(takeaway).strip()
        if name and takeaway_s.casefold() == name.strip().casefold():
            report.add(
                "DSX-VIZ-063",
                "HIGH",
                f"'{label}' takeaway is blank or identical to the chart name",
                detail=(
                    f"takeaway repeats name {name!r}. Variable labels are not findings."
                ),
                remedy="Rewrite the takeaway as the sentence you want remembered.",
                where=f"{where}.takeaway",
            )
        else:
            lowered = takeaway_s.casefold()
            has_digit = any(ch.isdigit() for ch in takeaway_s)
            has_token = any(tok in lowered for tok in COMPARISON_TOKENS) or (
                "%" in takeaway_s or "pp" in lowered
            )
            if not has_digit and not has_token:
                report.add(
                    "DSX-VIZ-064",
                    "MEDIUM",
                    f"'{label}' takeaway has no magnitude or comparison",
                    detail=(
                        "A strong takeaway usually contains a digit or a comparison word "
                        "(higher, fell, vs, …)."
                    ),
                    remedy="Add the magnitude or the comparison the reader should leave with.",
                    where=f"{where}.takeaway",
                )
            else:
                report.ok(f"'{label}' takeaway states a finding")

    if is_blank(visual.get("units")):
        report.add(
            "DSX-VIZ-061",
            "HIGH",
            f"'{label}' does not declare its units",
            detail="An unlabelled axis is unreadable — currency, percent and index all look alike.",
            remedy="Declare units and label the axis with them.",
            where=f"{where}.units",
        )
    if is_blank(visual.get("source")):
        report.add(
            "DSX-VIZ-062", "LOW", f"'{label}' has no source note",
            remedy="Cite the dataset and period so the chart survives being screenshotted.",
            where=f"{where}.source",
        )


def _check_uncertainty(visual: dict, label: str, where: str, report: Report) -> None:
    if not visual.get("shows_estimates"):
        return
    if visual.get("shows_uncertainty"):
        report.ok(f"'{label}' displays uncertainty alongside estimates")
        return
    report.add(
        "DSX-VIZ-070",
        "HIGH",
        f"'{label}' plots estimates without any uncertainty",
        detail=(
            "Point estimates drawn as solid bars or lines read as facts. Differences well "
            "inside the noise will be acted on."
        ),
        remedy="Add confidence intervals, error bars, or a shaded band. Say what they represent.",
        where=f"{where}.shows_uncertainty",
    )


def _check_ordering(
    visual: dict, chart_type: str, label: str, where: str, report: Report
) -> None:
    if chart_type not in ("bar", "horizontal_bar", "dot_plot"):
        return
    ordering = normalize(visual.get("category_order", ""))
    if not ordering:
        return
    if ordering in ("alphabetical", "arbitrary", "source_order"):
        report.add(
            "DSX-VIZ-080",
            "LOW",
            f"'{label}' orders categories {ordering}",
            detail="Alphabetical order encodes nothing; it hides the ranking the chart exists to show.",
            remedy="Sort by value, unless the categories have a natural order (time, size band).",
            where=f"{where}.category_order",
        )
    else:
        report.ok(f"'{label}' ordered by {ordering}")
