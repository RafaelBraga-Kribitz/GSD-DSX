# Chart generators for the known-good onboarding-activation exemplar (Phase 24, REQ-P24-01).
#
# This is the ONLY matplotlib importer in the repo and is deliberately NOT a gate
# module — it must never be imported on the hermetic gate path
# (tests/test_gate_path_hermetic.py keeps ``matplotlib`` in FORBIDDEN). It renders
# all three exemplar figures through the v2.4 style layer: the dsx-urban house style
# + templates/dsx_plotstyle.py (GA-2 finalise_figure with a MANDATORY source kw +
# save_deterministic, which writes byte-reproducible SVG and never hashes — dsx seal
# remains the single hashing authority). The point estimate and 95% CI are anchored
# to results.tests[0] in good-ANALYSIS-SPEC.yaml (effect 0.024, CI [0.0101, 0.0384]);
# no headline number is invented here.
#
# Re-rendering the two pre-existing figures intentionally changes their bytes; that is
# exactly why every seal in the spec is refreshed via ``dsx seal`` after this runs.

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless, deterministic — no display backend

import matplotlib.pyplot as plt

# Repo root is three levels up: examples/analysis/charts.py -> repo root.
REPO_ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = REPO_ROOT / "examples" / "figures"
STYLE = REPO_ROOT / "styles" / "dsx-urban.mplstyle"

# templates/ is not a package; import the analyst helper by path. Importing it also
# registers the vendored Lato font (register_fonts runs at import time) BEFORE any
# plt.style.use resolves font.family to it (Pitfall 1).
sys.path.insert(0, str(REPO_ROOT / "templates"))
from dsx_plotstyle import direct_label, finalise_figure, save_deterministic  # noqa: E402

# ── Ground truth (results.tests[0], good-ANALYSIS-SPEC.yaml) ──────────────────
BASELINE_RATE = 0.310          # design.baseline_rate (control activation)
UPLIFT = 0.024                 # results.tests[0].effect
TREATMENT_RATE = BASELINE_RATE + UPLIFT
CI_LOW, CI_HIGH = 0.0101, 0.0384   # results.tests[0].ci -> 1.0pp .. 3.8pp
DECISION_FLOOR = 0.010         # decision.decision_rule: CI lower bound > +1.0pp
SOURCE = "warehouse.fct_signups, 2026-06-01..06-14"

# Illustrative but deterministic daily series (control flat ~31%, treatment opens the
# gap on day 2 and holds it). The trend figure has always been illustrative — the two
# original SVGs were hand-made placeholders; the load-bearing numbers are the point
# estimate and CI, carried by the bar and uncertainty figures.
DAYS = list(range(1, 15))
CONTROL_DAILY = [0.305, 0.308, 0.310, 0.309, 0.311, 0.312, 0.310,
                 0.311, 0.313, 0.312, 0.311, 0.310, 0.312, 0.311]
TREATMENT_DAILY = [0.307, 0.318, 0.325, 0.329, 0.332, 0.333, 0.334,
                   0.335, 0.334, 0.336, 0.335, 0.334, 0.335, 0.334]


def _pct(ax) -> None:
    """Format the y-axis as whole-percent tick labels."""
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _pos: f"{v * 100:.0f}%"))


def render_activation_uplift() -> Path:
    """Point-estimate uplift bar: control vs treatment activation (y starts at zero)."""
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    ax.bar(["control", "treatment"], [BASELINE_RATE, TREATMENT_RATE])
    ax.set_ylim(0, 0.40)
    ax.set_ylabel("7-day activation")
    _pct(ax)
    finalise_figure(
        fig,
        title="Treatment activates 2.4pp higher than control",
        subtitle="7-day activation rate by arm",
        source=SOURCE,
    )
    fig.subplots_adjust(top=0.82, bottom=0.12)
    out = save_deterministic(fig, FIG_DIR / "activation_uplift.svg")
    plt.close(fig)
    return out


def render_daily_trend() -> Path:
    """Daily activation trend by arm; lines labelled directly (no legend)."""
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    ax.plot(DAYS, CONTROL_DAILY, label="control")
    ax.plot(DAYS, TREATMENT_DAILY, label="treatment")
    ax.set_xlabel("day since signup")
    ax.set_ylabel("7-day activation")
    ax.set_xlim(1, 15.6)
    _pct(ax)
    direct_label(ax)
    finalise_figure(
        fig,
        title="The gap opens on day 2 and holds — not a novelty effect",
        subtitle="Daily 7-day activation rate by arm",
        source=SOURCE,
    )
    fig.subplots_adjust(top=0.82, bottom=0.12, right=0.86)
    out = save_deterministic(fig, FIG_DIR / "daily_activation_trend.svg")
    plt.close(fig)
    return out


def render_uplift_ci() -> Path:
    """Uncertainty figure: the uplift point estimate with its real 95% CI error bars."""
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    yerr = [[UPLIFT - CI_LOW], [CI_HIGH - UPLIFT]]  # asymmetric = actual CI arms
    ax.errorbar(
        [0], [UPLIFT], yerr=yerr, fmt="o", capsize=6, markersize=8, linewidth=1.5,
    )
    ax.axhline(DECISION_FLOOR, linestyle="--", linewidth=1.0, color="#5c5859")
    ax.text(0.18, DECISION_FLOOR, "+1.0pp decision floor", va="bottom", ha="left",
            fontsize="small", color="#5c5859")
    ax.axhline(0.0, linewidth=0.8, color="#222222")
    ax.set_xlim(-0.6, 0.9)
    ax.set_xticks([0])
    ax.set_xticklabels(["activation uplift"])
    ax.set_ylim(0, 0.045)
    ax.set_ylabel("uplift (percentage points)")
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda v, _pos: f"{v * 100:.1f}")
    )
    finalise_figure(
        fig,
        title="The 2.4pp uplift's 95% CI is 1.0 to 3.8pp",
        subtitle="Activation uplift with 95% confidence interval",
        source=SOURCE,
        note="CI clears the +1.0pp decision floor",
    )
    fig.subplots_adjust(top=0.82, bottom=0.12)
    out = save_deterministic(fig, FIG_DIR / "activation_uplift_ci.svg")
    plt.close(fig)
    return out


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    plt.style.use(str(STYLE))
    paths = [render_activation_uplift(), render_daily_trend(), render_uplift_ci()]
    for p in paths:
        print(f"wrote {p.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
