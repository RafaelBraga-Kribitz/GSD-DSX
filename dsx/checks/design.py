"""Experiment and causal-identification checks. Codes DSX-EXP-* and DSX-CAU-*.

These are the checks that compute rather than opine. When the spec declares a
baseline, an MDE, an alpha and a power target, the required sample size is not a
matter of judgement — it is arithmetic, and so is the verdict on whether the
planned sample meets it.
"""

from __future__ import annotations

from ..findings import Report
from ..mathx import (
    inflation_from_peeking,
    mde_two_proportions,
    power_two_proportions,
    sample_size_two_proportions,
    srm_test,
)
from ..spec import (
    IDENTIFICATION_STRATEGIES,
    as_number,
    get,
    is_blank,
    items,
    normalize,
    section,
)

SRM_ALPHA = 0.001  # deliberately strict: SRM is a bug signal, not a hypothesis test
MIN_EXPERIMENT_DAYS = 7


def check(spec: dict, *, strict: bool = False) -> Report:
    report = Report(check="design")
    design = section(spec, "design")
    kind = normalize(design.get("kind", "")) if design else ""
    qtype = normalize(spec.get("question_type", ""))

    if qtype in ("causal", "prescriptive") and not design:
        report.add(
            "DSX-CAU-001",
            "CRITICAL",
            f"question_type is '{qtype}' but no design block is declared",
            detail=(
                "A causal question without a declared design cannot be answered — only "
                "guessed at. The design block is what separates the two."
            ),
            remedy="Add a design: block naming kind and identification strategy.",
            where="spec.design",
        )
        return report

    # Run the experiment battery whenever the spec carries experiment machinery,
    # not only when it says "experiment". Mislabelling a randomized test as
    # observational must not be a way to dodge the power and SRM checks.
    experiment_markers = (
        "randomization_unit", "planned_n_per_arm", "arms", "expected_allocation",
        "baseline_rate", "mde", "guardrail_metrics", "duration_days",
    )
    looks_like_experiment = kind == "experiment" or any(
        not is_blank(design.get(marker)) for marker in experiment_markers
    )
    if looks_like_experiment:
        if kind and kind != "experiment":
            report.add(
                "DSX-EXP-000",
                "MEDIUM",
                f"design.kind is '{kind}' but the spec declares experiment machinery",
                detail=(
                    "Present: "
                    + ", ".join(m for m in experiment_markers if not is_blank(design.get(m)))
                    + ". Experiment checks are being applied regardless."
                ),
                remedy="Set design.kind to experiment, or remove the fields that do not apply.",
                where="spec.design.kind",
            )
        _check_experiment_power(design, spec, report)
        _check_allocation(design, spec, report)
        _check_units(design, report)
        _check_duration(design, report)
        _check_guardrails(design, report)
    _check_multiplicity(design, spec, report, strict=strict)
    _check_peeking(design, spec, report)
    _check_identification(design, spec, report)
    return report


# ── Power ────────────────────────────────────────────────────────────────────


def _check_experiment_power(design: dict, spec: dict, report: Report) -> None:
    baseline = as_number(design.get("baseline_rate"))
    mde = as_number(design.get("mde"))
    alpha = as_number(design.get("alpha"))
    power_target = as_number(design.get("power"))
    planned = as_number(design.get("planned_n_per_arm"))

    missing = [
        name
        for name, value in (
            ("baseline_rate", baseline),
            ("mde", mde),
            ("alpha", alpha),
            ("power", power_target),
            ("planned_n_per_arm", planned),
        )
        if value is None
    ]
    if missing:
        report.add(
            "DSX-EXP-001",
            "CRITICAL",
            "Experiment design is missing power-calculation inputs",
            detail="Missing: " + ", ".join(missing),
            remedy=(
                "Declare all five. Without them the experiment's sample size is unjustified "
                "and a null result is uninterpretable — you cannot tell 'no effect' from "
                "'no power'."
            ),
            where="spec.design",
            missing=missing,
        )
        return

    if not 0.0 < baseline < 1.0:
        report.add(
            "DSX-EXP-002",
            "HIGH",
            f"baseline_rate {baseline} is not a proportion in (0, 1)",
            detail="Power for a proportion metric requires a baseline rate, not a count.",
            remedy="Express baseline_rate as a proportion, e.g. 0.31 for 31%.",
            where="spec.design.baseline_rate",
        )
        return
    if alpha <= 0 or alpha >= 0.5:
        report.add(
            "DSX-EXP-003", "HIGH", f"alpha {alpha} is outside a sane range",
            remedy="Use 0.05 unless you have a stated reason.", where="spec.design.alpha",
        )
        return
    if not 0.0 < power_target < 1.0:
        report.add(
            "DSX-EXP-004", "HIGH", f"power {power_target} is not in (0, 1)",
            remedy="Use 0.80 as the floor; 0.90 when the decision is expensive to reverse.",
            where="spec.design.power",
        )
        return

    try:
        required = sample_size_two_proportions(baseline, mde, alpha, power_target)
        achieved = power_two_proportions(baseline, mde, int(planned), alpha)
        detectable = mde_two_proportions(baseline, int(planned), alpha, power_target)
    except ValueError as exc:
        report.add(
            "DSX-EXP-005", "HIGH", "Power calculation could not be completed",
            detail=str(exc),
            remedy="Check that baseline_rate + mde stays inside (0, 1).",
            where="spec.design",
        )
        return

    report.context.update(
        {
            "required_n_per_arm": required,
            "planned_n_per_arm": int(planned),
            "achieved_power": round(achieved, 4),
            "detectable_mde_at_planned_n": round(detectable, 5),
        }
    )

    if planned < required:
        shortfall = (required - planned) / required
        report.add(
            "DSX-EXP-006",
            "CRITICAL",
            f"Experiment is underpowered: {int(planned):,} per arm vs {required:,} required",
            detail=(
                f"At baseline={baseline:.4g}, MDE={mde:.4g}, alpha={alpha:.4g}, the target "
                f"power of {power_target:.2f} needs {required:,} per arm. The plan is "
                f"{shortfall:.0%} short, delivering only {achieved:.2f} power. The smallest "
                f"effect actually detectable at {int(planned):,} per arm is {detectable:.4g}, "
                f"which is {detectable / mde:.1f}x the declared MDE."
            ),
            remedy=(
                f"Raise planned_n_per_arm to {required:,}, raise the MDE to {detectable:.4g}, "
                "or extend the run until the sample is reached. Do not proceed and reinterpret "
                "a null as evidence of no effect."
            ),
            where="spec.design.planned_n_per_arm",
            required_n_per_arm=required,
            planned_n_per_arm=int(planned),
            achieved_power=round(achieved, 4),
        )
    else:
        report.ok(
            f"power: {int(planned):,}/arm >= {required:,} required "
            f"(achieved power {achieved:.2f})"
        )

    practical = as_number(get(spec, "decision.minimum_practical_effect"))
    if practical is not None and mde > practical:
        report.add(
            "DSX-EXP-007",
            "HIGH",
            f"MDE ({mde:.4g}) exceeds the minimum effect the business cares about ({practical:.4g})",
            detail=(
                "The experiment is only powered to detect effects larger than the smallest "
                "effect that would change the decision. Effects in between will read as null."
            ),
            remedy=(
                f"Power the test for {practical:.4g} instead — that needs "
                f"{sample_size_two_proportions(baseline, practical, alpha, power_target):,} "
                "per arm."
            ),
            where="spec.design.mde",
        )


# ── Allocation / SRM ─────────────────────────────────────────────────────────


def _check_allocation(design: dict, spec: dict, report: Report) -> None:
    results = section(spec, "results")
    observed = results.get("observed_n")
    if not isinstance(observed, list) or len(observed) < 2:
        return
    counts = [int(c) for c in observed if isinstance(c, (int, float))]
    if len(counts) != len(observed):
        return

    expected = design.get("expected_allocation")
    if not isinstance(expected, list) or len(expected) != len(counts):
        expected = [1.0] * len(counts)

    try:
        statistic, p_value, df = srm_test(counts, [float(e) for e in expected])
    except ValueError as exc:
        report.add("DSX-EXP-010", "MEDIUM", "SRM test could not be run", detail=str(exc),
                   where="spec.results.observed_n")
        return

    total = sum(counts)
    actual_share = [c / total for c in counts]
    report.context["srm"] = {"chi2": round(statistic, 4), "p": p_value, "df": df}

    if p_value < SRM_ALPHA:
        report.add(
            "DSX-EXP-011",
            "CRITICAL",
            f"Sample ratio mismatch: chi2={statistic:.2f}, p={p_value:.2e}",
            detail=(
                f"Observed split {['{:.4f}'.format(s) for s in actual_share]} against expected "
                f"{expected}. A p below {SRM_ALPHA} means the assignment mechanism is broken — "
                "bot filtering, redirect loss, logging drop or a bucketing bug. Any treatment "
                "effect estimated from this data is confounded by whatever caused the imbalance."
            ),
            remedy=(
                "Do not read the results. Find the assignment defect first, then re-run. "
                "SRM is never a statistical fluctuation you can adjust away."
            ),
            where="spec.results.observed_n",
            chi2=round(statistic, 4),
            p_value=p_value,
        )
    else:
        report.ok(f"no sample ratio mismatch (p={p_value:.3f})")


def _check_units(design: dict, report: Report) -> None:
    randomization = normalize(design.get("randomization_unit", ""))
    analysis = normalize(design.get("analysis_unit", ""))
    if not randomization or not analysis:
        report.add(
            "DSX-EXP-020",
            "HIGH",
            "randomization_unit and analysis_unit must both be declared",
            detail=(
                "When they differ and nothing corrects for it, standard errors are understated "
                "and false positives multiply."
            ),
            remedy="Declare both, even when they are the same.",
            where="spec.design",
        )
        return

    if randomization == analysis:
        report.ok(f"randomization unit == analysis unit ({randomization})")
        return

    adjustment = design.get("variance_adjustment")
    if is_blank(adjustment):
        report.add(
            "DSX-EXP-021",
            "CRITICAL",
            f"Unit mismatch: randomized on '{randomization}', analysed on '{analysis}'",
            detail=(
                "Observations within a randomization unit are correlated. Treating the finer "
                "analysis unit as independent understates variance, inflates the test "
                "statistic, and produces significant results from noise."
            ),
            remedy=(
                "Set design.variance_adjustment to cluster_robust (cluster on "
                f"'{randomization}'), delta_method, or bootstrap_cluster — or aggregate the "
                f"metric to the '{randomization}' level before testing."
            ),
            where="spec.design.analysis_unit",
        )
    else:
        report.ok(f"unit mismatch handled via {normalize(adjustment)}")


def _check_duration(design: dict, report: Report) -> None:
    days = as_number(design.get("duration_days"))
    if days is None:
        return
    if days < MIN_EXPERIMENT_DAYS:
        report.add(
            "DSX-EXP-030",
            "MEDIUM",
            f"Experiment runs for {days:g} days, under the {MIN_EXPERIMENT_DAYS}-day floor",
            detail=(
                "Runs shorter than a full week are dominated by novelty effects and by "
                "whichever weekdays happened to be included."
            ),
            remedy="Run at least one full week, in whole-week multiples.",
            where="spec.design.duration_days",
        )
    elif days % 7 != 0:
        report.add(
            "DSX-EXP-031",
            "LOW",
            f"Experiment duration of {days:g} days is not a whole number of weeks",
            detail="Partial weeks over-weight the weekdays they include.",
            remedy="Round to a multiple of 7 days.",
            where="spec.design.duration_days",
        )
    else:
        report.ok(f"duration {days:g} days ({days / 7:g} whole weeks)")


def _check_guardrails(design: dict, report: Report) -> None:
    guardrails = design.get("guardrail_metrics")
    if is_blank(guardrails):
        report.add(
            "DSX-EXP-040",
            "MEDIUM",
            "No guardrail metrics declared for the experiment",
            detail=(
                "A treatment can move the primary metric while damaging latency, error rate, "
                "margin or a downstream funnel step. Without guardrails that damage ships."
            ),
            remedy="Declare design.guardrail_metrics — at minimum one health and one revenue metric.",
            where="spec.design.guardrail_metrics",
        )
    else:
        report.ok(f"{len(guardrails) if isinstance(guardrails, list) else 1} guardrail metric(s)")


# ── Multiplicity and peeking ─────────────────────────────────────────────────


def _check_multiplicity(
    design: dict, spec: dict, report: Report, *, strict: bool = False
) -> None:
    family = get(design, "multiplicity.family")
    correction = get(design, "multiplicity.correction")
    tests = items(section(spec, "results"), "tests") if section(spec, "results") else []
    n_tests = len(family) if isinstance(family, list) else 0
    if not n_tests and tests:
        n_tests = len(tests)

    if n_tests <= 1:
        if n_tests == 1:
            report.ok("single hypothesis — no correction needed")
    elif is_blank(correction) or normalize(correction) == "none":
        report.add(
            "DSX-EXP-050",
            "HIGH",
            f"{n_tests} hypotheses tested with no multiplicity correction",
            detail=(
                f"At alpha=0.05 the chance of at least one false positive across {n_tests} "
                f"independent tests is {1 - 0.95 ** n_tests:.0%}, not 5%."
            ),
            remedy=(
                "Set design.multiplicity.correction to benjamini_hochberg (discovery work, "
                "controls FDR) or holm (confirmatory work, controls FWER). Alternatively "
                "designate one primary metric and label the rest exploratory."
            ),
            where="spec.design.multiplicity.correction",
            n_tests=n_tests,
            naive_family_error=round(1 - 0.95**n_tests, 4),
        )
    else:
        report.ok(f"{n_tests} hypotheses corrected via {normalize(correction)}")

    _check_exploratory_looks(design, spec, report, strict=strict)


def _check_exploratory_looks(
    design: dict, spec: dict, report: Report, *, strict: bool
) -> None:
    family = get(design, "multiplicity.family")
    if not isinstance(family, list) or not family:
        return
    family_n = len(family)
    results = section(spec, "results")
    looked = as_number(results.get("comparisons_looked_at")) if results else None
    tests = items(results, "tests") if results else []

    if looked is not None and looked > family_n:
        report.add(
            "DSX-EXP-051",
            "HIGH",
            f"comparisons_looked_at={int(looked)} exceeds multiplicity family size {family_n}",
            detail=(
                "Segment cuts and exploratory comparisons inflate the family-wise error "
                "beyond what the declared correction covers."
            ),
            remedy=(
                "Expand design.multiplicity.family to every cut examined, or stop examining "
                "undeclared cuts, or label extras exploratory and do not claim significance."
            ),
            where="spec.results.comparisons_looked_at",
            looked_at=int(looked),
            family_size=family_n,
        )
    elif looked is not None:
        report.ok(f"comparisons_looked_at={int(looked)} within family size {family_n}")

    if strict and len(tests) >= 2 and looked is None:
        report.add(
            "DSX-EXP-052",
            "MEDIUM",
            "Multiple tests with a declared family but comparisons_looked_at is missing",
            detail=(
                "Without a count of cuts actually examined, the multiplicity family cannot "
                "be audited against exploratory work."
            ),
            remedy="Set results.comparisons_looked_at to the number of comparisons examined.",
            where="spec.results.comparisons_looked_at",
        )


def _check_peeking(design: dict, spec: dict, report: Report) -> None:
    policy = normalize(design.get("peeking_policy", "")) if design else ""
    looks = as_number(get(spec, "results.interim_looks"))
    if looks is None:
        return
    looks = int(looks)

    if policy in ("", "fixed_horizon") and looks > 1:
        alpha = as_number(design.get("alpha"))
        if alpha is None:
            alpha = 0.05
        inflated = inflation_from_peeking(looks, alpha)
        report.add(
            "DSX-EXP-060",
            "CRITICAL",
            f"{looks} interim looks were taken under a fixed-horizon design",
            detail=(
                f"Repeatedly testing the same accumulating data inflates the true type-I error "
                f"from {alpha:.2f} to roughly {inflated:.2f}. "
                "Any 'significant' reading here is not significant at the stated level."
            ),
            remedy=(
                "Either report only the final pre-declared analysis, or switch the design to "
                "sequential_obf / always_valid and re-evaluate against the corrected boundary."
            ),
            where="spec.results.interim_looks",
            interim_looks=looks,
            inflated_alpha=round(inflated, 4),
        )
    elif looks > 1:
        report.ok(f"{looks} interim looks under policy '{policy}'")


# ── Causal identification ────────────────────────────────────────────────────


def _check_identification(design: dict, spec: dict, report: Report) -> None:
    qtype = normalize(spec.get("question_type", ""))
    if qtype not in ("causal", "prescriptive"):
        return
    if not design:
        return

    kind = normalize(design.get("kind", ""))
    strategy = normalize(design.get("identification", "")) if design.get("identification") else ""

    if kind == "experiment" and not strategy:
        strategy = "randomized_experiment"

    if not strategy or strategy == "none":
        report.add(
            "DSX-CAU-010",
            "CRITICAL",
            f"Causal question with no identification strategy (design.kind={kind or 'unset'})",
            detail=(
                "Correlation in observational data identifies nothing on its own. Without a "
                "strategy that rules out confounding, no estimate here supports a causal claim."
            ),
            remedy=(
                "Declare design.identification as one of: "
                + ", ".join(sorted(k for k in IDENTIFICATION_STRATEGIES if k != "none"))
                + ". If none applies, change question_type to 'diagnostic' and reword every "
                "claim as association."
            ),
            where="spec.design.identification",
        )
        return

    meta = IDENTIFICATION_STRATEGIES.get(strategy, {})
    needs = list(meta.get("needs", []))
    missing = [need for need in needs if is_blank(design.get(need))]
    if missing:
        report.add(
            "DSX-CAU-011",
            "HIGH",
            f"Identification strategy '{strategy}' is missing its required assumptions",
            detail=(
                f"Missing: {', '.join(missing)}. Each is a condition the strategy needs in "
                "order to identify anything; undeclared, it is untested."
            ),
            remedy=(
                "Declare each missing field under design: and state the evidence supporting it. "
                "For matching and regression adjustment, a sensitivity analysis quantifying how "
                "strong an unmeasured confounder would have to be is mandatory."
            ),
            where="spec.design",
            strategy=strategy,
            missing=missing,
        )
    else:
        report.ok(f"identification '{strategy}' with all required assumptions declared")

    if meta.get("strength") == "weak":
        report.add(
            "DSX-CAU-012",
            "MEDIUM",
            f"Identification strategy '{strategy}' provides weak causal support",
            detail=(
                "Matching and regression adjustment identify causal effects only under "
                "conditional ignorability — an assumption the data cannot verify."
            ),
            remedy=(
                "State the assumption explicitly in the deliverable, report the sensitivity "
                "analysis alongside the point estimate, and prefer hedged wording."
            ),
            where="spec.design.identification",
        )
