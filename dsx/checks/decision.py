"""Decision replay against results.tests. Codes DSX-DEC-*.

Structured thresholds in decision.replay are evaluated numerically — the gate
never parses English decision_rule prose.
"""

from __future__ import annotations

import json

from ..findings import Report
from ..spec import as_number, get, is_blank, items, normalize, section


def check(spec: dict, *, gate_point: "str | None" = None) -> Report:
    report = Report(check="decision")
    decision = section(spec, "decision")
    replay = decision.get("replay") if decision else None
    design = section(spec, "design")
    kind = normalize(str(design.get("kind", "")))
    qtype = normalize(str(spec.get("question_type", "")))
    tests = items(section(spec, "results"), "tests")

    needs_replay = bool(tests) and (
        kind == "experiment" or qtype in {"causal", "prescriptive"}
    )

    if needs_replay and not isinstance(replay, dict):
        if gate_point == "ship":
            report.add(
                "DSX-DEC-001",
                "HIGH",
                "decision.replay missing or incomplete",
                detail=(
                    "Experiments and causal/prescriptive questions need structured "
                    "thresholds so the pre-declared rule can be re-applied to the numbers."
                ),
                remedy=(
                    "Add decision.replay with metric, ci_lower_min (and/or effect_min / "
                    "ci_upper_max), on_pass, and on_fail."
                ),
                where="spec.decision.replay",
            )
        return report

    if not isinstance(replay, dict):
        return report

    if is_blank(replay.get("on_pass")) or is_blank(replay.get("on_fail")):
        report.add(
            "DSX-DEC-001",
            "HIGH",
            "decision.replay missing or incomplete",
            detail="Labels document which action the thresholds imply.",
            remedy="Set on_pass and on_fail to short action labels.",
            where="spec.decision.replay",
        )

    metric_name = normalize(str(replay.get("metric", "")))
    if not metric_name:
        report.add(
            "DSX-DEC-010",
            "HIGH",
            "decision.replay.metric missing from results.tests",
            remedy="Point replay.metric at a results.tests[].metric name.",
            where="spec.decision.replay.metric",
        )
        return report

    matched = None
    for test in tests:
        if normalize(str(test.get("metric", ""))) == metric_name:
            matched = test
            break
    if matched is None:
        report.add(
            "DSX-DEC-010",
            "HIGH",
            "decision.replay.metric missing from results.tests",
            detail=(
                f"Looked for {replay.get('metric')!r}. Declared tests: "
                + (", ".join(str(t.get("metric")) for t in tests) or "(none)")
            ),
            remedy="Fix the metric name, or add the matching results.tests entry.",
            where="spec.decision.replay.metric",
        )
        return report

    verdict, payload = _evaluate_replay(replay, matched, spec)
    detail = json.dumps(payload, sort_keys=True)

    if verdict == "fail":
        report.add(
            "DSX-DEC-020",
            "HIGH",
            f"Decision replay FAIL for metric {metric_name!r}",
            detail=detail,
            remedy=(
                "Do not ship a pass/rollout action. Follow action_if_null / on_fail, "
                "or revise thresholds only with an explicit amendment."
            ),
            where="spec.decision.replay",
            verdict="fail",
        )
    else:
        alpha = as_number(get(spec, "design.alpha")) or 0.05
        p = as_number(matched.get("p_value"))
        if p is not None and p >= alpha:
            report.add(
                "DSX-DEC-021",
                "HIGH",
                f"Decision replay PASS but primary p={p:.4g} ≥ alpha={alpha}",
                detail=detail,
                remedy=(
                    "A threshold pass with a non-significant primary test is incoherent — "
                    "check CI construction, alpha, or whether the metric is the right primary."
                ),
                where="spec.decision.replay",
                verdict="pass",
            )
        else:
            report.ok(f"decision replay PASS for {metric_name}: {detail}")

    return report


def _evaluate_replay(
    replay: dict, test: dict, spec: dict
) -> tuple[str, dict]:
    ci = test.get("ci")
    lo = hi = None
    if isinstance(ci, (list, tuple)) and len(ci) == 2:
        lo, hi = as_number(ci[0]), as_number(ci[1])
    effect = as_number(test.get("effect"))
    p = as_number(test.get("p_value"))

    reasons: list[str] = []
    ci_lower_min = as_number(replay.get("ci_lower_min"))
    if ci_lower_min is not None:
        if lo is None or lo <= ci_lower_min:
            reasons.append(f"ci[0]={lo} not > ci_lower_min={ci_lower_min}")

    ci_upper_max = as_number(replay.get("ci_upper_max"))
    if ci_upper_max is not None:
        if hi is None or hi >= ci_upper_max:
            reasons.append(f"ci[1]={hi} not < ci_upper_max={ci_upper_max}")

    effect_min = as_number(replay.get("effect_min"))
    if effect_min is not None:
        if effect is None or abs(effect) < effect_min:
            reasons.append(f"|effect|={effect} < effect_min={effect_min}")

    # If no numeric thresholds declared, treat as incomplete fail.
    if (
        ci_lower_min is None
        and ci_upper_max is None
        and effect_min is None
    ):
        reasons.append("no ci_lower_min / ci_upper_max / effect_min declared")

    payload = {
        "verdict": "fail" if reasons else "pass",
        "metric": replay.get("metric"),
        "ci": [lo, hi],
        "effect": effect,
        "p_value": p,
        "ci_lower_min": ci_lower_min,
        "ci_upper_max": ci_upper_max,
        "effect_min": effect_min,
        "reasons": reasons,
        "on_pass": replay.get("on_pass"),
        "on_fail": replay.get("on_fail"),
    }
    return payload["verdict"], payload
