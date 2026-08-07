"""The ANALYSIS-SPEC contract — closed vocabularies and structural validation.

This is the pivot the whole capability turns on. An agent's job is to *fill* this
spec (judgement, flexible, stochastic). Code's job is to check the spec is
internally coherent and that produced artifacts satisfy it (deterministic).

Every vocabulary below is closed. A value outside it is a finding, not a warning
in prose — which is what makes agent output checkable instead of merely plausible.
"""

from __future__ import annotations

from typing import Any, Iterable

from .findings import Report

SPEC_VERSION = 1

# ── Closed vocabularies ──────────────────────────────────────────────────────

QUESTION_TYPES = {
    "descriptive": "What happened? Summarises observed data. No inference beyond the sample.",
    "diagnostic": "Why did it happen? Decomposition and attribution within observed data.",
    "predictive": "What will happen? Out-of-sample forecast or classification.",
    "causal": "What is the effect of X on Y? Requires an identification strategy.",
    "prescriptive": "What should we do? Requires a causal estimate plus a decision rule.",
}

DESIGN_KINDS = {"experiment", "quasi_experiment", "observational", "timeseries", "none"}

IDENTIFICATION_STRATEGIES = {
    "randomized_experiment": {"strength": "strong", "needs": []},
    "difference_in_differences": {
        "strength": "moderate",
        "needs": ["parallel_trends_evidence"],
    },
    "instrumental_variable": {
        "strength": "moderate",
        "needs": ["instrument", "exclusion_restriction_argument"],
    },
    "regression_discontinuity": {"strength": "moderate", "needs": ["running_variable", "cutoff"]},
    "synthetic_control": {"strength": "moderate", "needs": ["donor_pool", "pre_period_fit"]},
    "matching": {"strength": "weak", "needs": ["covariates", "sensitivity_analysis"]},
    "regression_adjustment": {"strength": "weak", "needs": ["covariates", "sensitivity_analysis"]},
    "front_door": {"strength": "moderate", "needs": ["mediator"]},
    "none": {"strength": "none", "needs": []},
}

CLAIM_TYPES = {"descriptive", "association", "predictive", "causal"}

# Verbs that assert causation. Used to catch a causal claim mislabelled as
# association — the single most common analytical overreach.
CAUSAL_VERBS = (
    "causes", "caused", "causing", "drives", "drove", "driving", "leads to", "led to",
    "results in", "resulted in", "increases", "decreases", "improves", "improved",
    "reduces", "reduced", "boosts", "boosted", "lifts", "lifted", "impact of",
    "effect of", "because of", "due to", "thanks to", "responsible for",
    "attributable to", "uplift from", "generates", "generated",
)

MULTIPLICITY_CORRECTIONS = {"bonferroni", "holm", "benjamini_hochberg", "bh", "fdr", "none"}

PEEKING_POLICIES = {
    "fixed_horizon": "One analysis at the pre-declared sample size. No interim looks.",
    "sequential_obf": "Interim looks against O'Brien-Fleming boundaries.",
    "sequential_pocock": "Interim looks against constant Pocock boundaries.",
    "always_valid": (
        "Error rate is controlled continuously via anytime-valid inference "
        "(mSPRT / confidence sequences)."
    ),
    "uncontrolled_continuous": (
        "Interim looks continue with no sequential correction and no anytime-valid method — "
        "the error rate is not controlled."
    ),
}

ML_TASKS = {
    "binary_classification",
    "multiclass_classification",
    "regression",
    "ranking",
    "forecasting",
    "clustering",
    "survival",
}

SPLIT_STRATEGIES = {"random", "stratified", "temporal", "grouped", "grouped_temporal", "nested_cv"}

# Metrics that mislead on imbalanced targets. Keyed to the recommended replacement.
IMBALANCE_UNSAFE_METRICS = {
    "accuracy": "pr_auc or balanced_accuracy",
    "roc_auc": "pr_auc (ROC-AUC is optimistic when positives are rare)",
    "error_rate": "pr_auc or balanced_accuracy",
}

VARIANCE_ADJUSTMENTS = {"cluster_robust", "delta_method", "bootstrap_cluster", "mixed_effects"}

METRIC_TYPES = {"ratio", "count", "sum", "average", "rate", "percentile", "index"}

# Data-input types (DDVF) → admissible chart marks in dsx vocabulary.
DATA_INPUT_TYPES = {
    "bivariate-simple",
    "bivariate-dual",
    "trivariate",
    "categorical-value",
    "categorical-multi",
    "time-series",
    "interval-range",
    "grouped-categorical",
    "composition",
    "hierarchical",
    "matrix",
    "event-time",
}

# Admissible chart types per data_input_type (dsx mark names, underscored).
CHART_CAPABILITIES: dict[str, frozenset[str]] = {
    "bivariate-simple": frozenset({"line", "scatter", "area", "bar", "column", "horizontal_bar"}),
    "bivariate-dual": frozenset({"line", "area", "bar", "horizontal_bar", "grouped_bar", "multi_line"}),
    "trivariate": frozenset({"scatter", "bubble", "heatmap", "hexbin"}),
    "categorical-value": frozenset(
        {"bar", "horizontal_bar", "pie", "donut", "waffle", "dot_plot", "bullet"}
    ),
    "categorical-multi": frozenset(
        {"grouped_bar", "stacked_bar", "horizontal_bar", "bar", "slope", "dot_plot"}
    ),
    "time-series": frozenset(
        {"line", "area", "stacked_area", "sparkline", "slope", "bar", "stream"}
    ),
    "interval-range": frozenset({"box", "violin", "dot_plot", "bar", "horizontal_bar", "bullet"}),
    "grouped-categorical": frozenset(
        {"grouped_bar", "stacked_bar", "horizontal_bar", "bar", "dot_plot", "heatmap"}
    ),
    "composition": frozenset(
        {"stacked_bar", "pie", "donut", "treemap", "waffle", "stacked_area"}
    ),
    "hierarchical": frozenset({"treemap", "sunburst", "icicle", "circle_pack"}),
    "matrix": frozenset({"heatmap", "chord"}),
    "event-time": frozenset({"line", "scatter", "timeline", "funnel", "gantt"}),
}

RENDERERS = {"matplotlib", "plotly", "altair", "ggplot", "glyph", "other"}

SERIES_ROLES = {"component", "scenario"}

# ── Validity-frame / inference vocabularies (Phase 6, REQ-P6-06) ────────────
# Every one is a name->description dict, no exceptions (D-04). No new vocabulary is
# defined for dependence.method_family_required — it is typed against the existing
# VARIANCE_ADJUSTMENTS set above (M-09).

IDENTIFICATION_STRENGTHS = {
    "strong": "The identification strategy rules out confounding by design (e.g. randomization).",
    "moderate": (
        "The identification strategy relies on an assumption that is plausible but not "
        "verifiable from the data alone."
    ),
    "weak": "The identification strategy relies on covariate adjustment with no design-based support.",
}

CONSTRAINT_SOURCES = {
    "none": "No external constraint informs the estimate beyond the observed data.",
    "informative_priors": "A prior distribution encodes external information about the parameter.",
    "penalisation": (
        "A penalty term (e.g. ridge, lasso) shrinks the estimate toward a null or reference value."
    ),
    "design_restriction": (
        "The study design itself restricts the parameter space "
        "(e.g. a capped effect by construction)."
    ),
    "hierarchical_pooling": (
        "Partial pooling across groups in a hierarchical model constrains group-level estimates."
    ),
}

DEPENDENCE_STRUCTURES = {
    "none": "Observations are independent; no dependence structure is declared.",
    "clustered": "Observations are grouped into clusters that share unobserved factors.",
    "repeated_measures": "The same unit is observed multiple times.",
    "temporal": "Observations are ordered in time and adjacent observations are correlated.",
    "spatial": "Observations are located in space and nearby observations are correlated.",
    "hierarchical": "Observations are nested within multiple levels of grouping.",
}

INTERFERENCE_RISKS = {
    "none": "Treatment of one unit does not plausibly affect another unit's outcome.",
    "shared_budget": (
        "Units compete for a shared, capacity-limited resource (e.g. a paid-media budget)."
    ),
    "marketplace": (
        "Units interact through a two-sided market where one side's treatment shifts the "
        "other side's outcomes."
    ),
    "geo_spillover": "Treatment effects in one geography leak into a nearby untreated geography.",
    "social_graph": (
        "Units are connected by a social or referral graph through which treatment can propagate."
    ),
    "shared_inventory": "Units draw from a shared, finite inventory of a physical or virtual good.",
}

INTERFERENCE_MITIGATIONS = {
    "none": "No mitigation is applied; interference risk, if any, is unaddressed.",
    "geo_split": "Randomization is performed at the geography level to contain spillover.",
    "cluster_randomisation": "Randomization is performed at the cluster level rather than the individual level.",
    "time_split": "Treatment and control are separated in time rather than concurrently.",
    "budget_isolation": "Each arm draws from a separate, non-competing budget.",
    "modelled": "Interference is estimated and adjusted for statistically rather than designed away.",
}

# Exactly four members, no "none" member (locked decision R-02): missingness is never
# absent, only unassessed. Do not re-add a "none" member.
MISSINGNESS_MECHANISMS = {
    "MCAR": (
        "Missing completely at random — missingness is independent of both observed and "
        "unobserved data."
    ),
    "MAR": "Missing at random — missingness depends only on observed data.",
    "MNAR": "Missing not at random — missingness depends on the unobserved value itself.",
    "not_assessed": "The missingness mechanism has not been evaluated.",
}

ANALYSIS_POPULATIONS = {
    "eligible": "The population that met eligibility criteria, regardless of subsequent engagement.",
    "triggered": "The subset of the eligible population that actually triggered the analyzed event.",
}

DECLARATION_POINTS = {
    "pre_data": "The inference plan was declared before the data was observed.",
    "post_data": (
        "The inference plan was declared after the data was observed — an unverifiable "
        "operator self-declaration (Phase 10 REQ-P10-02 documents this limit)."
    ),
}

PARADIGMS = {
    "frequentist": "Inference based on the sampling distribution of a statistic under repeated sampling.",
    "bayesian": "Inference based on a posterior distribution combining a prior with the observed data.",
}

# No description ranks one reason above another (D-12 symmetry).
PARADIGM_JUSTIFICATIONS = {
    "prior_information_available": "Credible external information exists to form an informative prior.",
    "sequential_monitoring_required": (
        "The analysis requires continuous or repeated looks at accumulating data."
    ),
    "decision_theoretic_loss_specified": (
        "A decision rule with an explicit loss function drives the analysis."
    ),
    "small_sample_informative_prior": (
        "The sample is too small for frequentist asymptotics to apply reliably."
    ),
    "regulatory_requirement": "A regulatory or compliance requirement mandates the paradigm.",
    "team_convention": "The paradigm follows the team's established analytical convention.",
    "vendor_constraint": "The paradigm is constrained by a third-party tool or vendor.",
}

# Single registry behind describe_vocabulary() (D-05, REQ-P6-06): the object each shape
# validator imports is the exact object dumped here — one place to add a vocabulary, not two.
# Deliberately excludes SPEC_VERSION, CAUSAL_VERBS, REQUIRED_TOP_LEVEL and
# IMBALANCE_UNSAFE_METRICS — they are not vocabularies. chart_capabilities stays
# special-cased in describe_vocabulary() below, exactly as before.
_VOCABULARIES: "list[tuple[str, Any]]" = [
    ("question_types", QUESTION_TYPES),
    ("design_kinds", DESIGN_KINDS),
    ("identification_strategies", IDENTIFICATION_STRATEGIES),
    ("claim_types", CLAIM_TYPES),
    ("multiplicity_corrections", MULTIPLICITY_CORRECTIONS),
    ("peeking_policies", PEEKING_POLICIES),
    ("ml_tasks", ML_TASKS),
    ("split_strategies", SPLIT_STRATEGIES),
    ("variance_adjustments", VARIANCE_ADJUSTMENTS),
    ("metric_types", METRIC_TYPES),
    ("data_input_types", DATA_INPUT_TYPES),
    ("renderers", RENDERERS),
    ("series_roles", SERIES_ROLES),
    # New this phase (REQ-P6-06) — every one a name->description dict per D-04:
    ("identification_strengths", IDENTIFICATION_STRENGTHS),
    ("constraint_sources", CONSTRAINT_SOURCES),
    ("dependence_structures", DEPENDENCE_STRUCTURES),
    ("interference_risks", INTERFERENCE_RISKS),
    ("interference_mitigations", INTERFERENCE_MITIGATIONS),
    ("missingness_mechanisms", MISSINGNESS_MECHANISMS),
    ("analysis_populations", ANALYSIS_POPULATIONS),
    ("declaration_points", DECLARATION_POINTS),
    ("paradigms", PARADIGMS),
    ("paradigm_justifications", PARADIGM_JUSTIFICATIONS),
]


# ── Access helpers ───────────────────────────────────────────────────────────


def get(spec: Any, path: str, default: Any = None) -> Any:
    """Read a dotted path out of a nested mapping. Never raises on a missing key."""
    node: Any = spec
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node if node is not None else default


def section(spec: dict, name: str) -> dict:
    value = spec.get(name)
    return value if isinstance(value, dict) else {}


def items(spec: dict, name: str) -> list[dict]:
    """Return a list section, keeping only mapping entries."""
    value = spec.get(name)
    if not isinstance(value, list):
        return []
    return [v for v in value if isinstance(v, dict)]


def is_blank(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict, tuple, set)):
        return len(value) == 0
    return False


def as_number(value: Any) -> "float | None":
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        text = value.strip().rstrip("%")
        try:
            number = float(text)
        except ValueError:
            return None
        return number / 100.0 if value.strip().endswith("%") else number
    return None


def normalize(value: Any) -> str:
    return str(value).strip().lower().replace("-", "_").replace(" ", "_")


# ── Structural validation ────────────────────────────────────────────────────

REQUIRED_TOP_LEVEL = ("spec_version", "title", "question_type", "decision")


def validate_structure(spec: dict) -> Report:
    """Shape and vocabulary validation. Semantic coherence lives in checks/.

    Codes DSX-SPEC-*.
    """
    report = Report(check="spec-structure")

    for key in REQUIRED_TOP_LEVEL:
        if is_blank(spec.get(key)):
            report.add(
                "DSX-SPEC-001",
                "CRITICAL",
                f"ANALYSIS-SPEC is missing required field '{key}'",
                detail=f"Present top-level keys: {', '.join(sorted(spec)) or '(none)'}",
                remedy=f"Add '{key}' to ANALYSIS-SPEC.yaml. See templates/ANALYSIS-SPEC.yaml.",
                where=f"spec.{key}",
            )
    if not report.findings:
        report.ok("required top-level fields present")

    version = spec.get("spec_version")
    if version is not None and version != SPEC_VERSION:
        report.add(
            "DSX-SPEC-002",
            "HIGH",
            f"Unsupported spec_version {version!r}",
            detail=f"This dsx build validates spec_version {SPEC_VERSION}.",
            remedy=f"Set spec_version: {SPEC_VERSION} and reconcile any renamed fields.",
            where="spec.spec_version",
        )

    qtype = normalize(spec.get("question_type", ""))
    if qtype and qtype not in QUESTION_TYPES:
        report.add(
            "DSX-SPEC-003",
            "CRITICAL",
            f"question_type {spec.get('question_type')!r} is not a recognised type",
            detail="Allowed: " + ", ".join(sorted(QUESTION_TYPES)),
            remedy="Pick the type matching the decision being supported, not the method used.",
            where="spec.question_type",
        )
    elif qtype:
        report.ok(f"question_type={qtype}")

    _validate_decision(spec, report)
    _validate_metrics(spec, report)
    _validate_data(spec, report)
    _validate_design_shape(spec, report)
    _validate_model_shape(spec, report)
    _validate_claims_shape(spec, report)

    from .suppressions import validate_suppressions

    report.extend(validate_suppressions(spec))

    return report


def _validate_decision(spec: dict, report: Report) -> None:
    decision = section(spec, "decision")
    if not decision:
        return  # absence already reported by the required-field loop

    if is_blank(decision.get("decision_rule")):
        report.add(
            "DSX-SPEC-010",
            "CRITICAL",
            "decision.decision_rule is missing",
            detail=(
                "Without a pre-declared rule mapping results to actions, any result can be "
                "rationalised after the fact. This is the primary defence against HARKing."
            ),
            remedy=(
                "State the rule before looking at results, e.g. "
                "'If the 95% CI lower bound on uplift exceeds 0, roll out; otherwise hold.'"
            ),
            where="spec.decision.decision_rule",
        )
    else:
        report.ok("decision rule declared")

    if is_blank(decision.get("owner")):
        report.add(
            "DSX-SPEC-011",
            "MEDIUM",
            "decision.owner is missing",
            detail="An analysis with no named decision-maker has no consumer.",
            remedy="Name the person or role who will act on this result.",
            where="spec.decision.owner",
        )

    if is_blank(decision.get("action_if_null")):
        report.add(
            "DSX-SPEC-012",
            "HIGH",
            "decision.action_if_null is missing",
            detail=(
                "The null outcome is the more likely one. If it has no pre-declared action, "
                "a null result will be reframed as 'directionally positive'."
            ),
            remedy="State what happens when the effect is not detected.",
            where="spec.decision.action_if_null",
        )


def _validate_metrics(spec: dict, report: Report) -> None:
    metrics = items(spec, "metrics")
    if not metrics:
        report.add(
            "DSX-SPEC-020",
            "CRITICAL",
            "No metrics declared",
            detail="Every analysis needs at least one metric with an unambiguous definition.",
            remedy="Add a metrics: block. Each entry needs name, definition, grain and type.",
            where="spec.metrics",
        )
        return

    seen: dict[str, int] = {}
    for index, metric in enumerate(metrics):
        where = f"spec.metrics[{index}]"
        name = metric.get("name")
        if is_blank(name):
            report.add(
                "DSX-SPEC-021", "CRITICAL", "Metric is missing 'name'",
                remedy="Give every metric a stable snake_case name.", where=where,
            )
            continue
        key = normalize(name)
        if key in seen:
            report.add(
                "DSX-SPEC-022",
                "CRITICAL",
                f"Duplicate metric name {name!r}",
                detail=f"Also declared at spec.metrics[{seen[key]}].",
                remedy="One name, one definition. Rename or merge the duplicate.",
                where=where,
            )
        seen[key] = index

        if is_blank(metric.get("definition")):
            report.add(
                "DSX-SPEC-023",
                "HIGH",
                f"Metric {name!r} has no definition",
                detail="An undefined metric cannot be reconciled across sources.",
                remedy="Write the definition as a computable expression, not a label.",
                where=where,
            )
        if is_blank(metric.get("grain")):
            report.add(
                "DSX-SPEC-024",
                "HIGH",
                f"Metric {name!r} has no grain",
                detail="Grain determines whether a sum double-counts. It is not optional.",
                remedy="Declare the entity one row represents, e.g. user, session, order.",
                where=where,
            )

        mtype = normalize(metric.get("type", ""))
        if mtype and mtype not in METRIC_TYPES:
            report.add(
                "DSX-SPEC-025",
                "MEDIUM",
                f"Metric {name!r} has unrecognised type {metric.get('type')!r}",
                detail="Allowed: " + ", ".join(sorted(METRIC_TYPES)),
                remedy="Use a listed type so downstream checks know how to treat it.",
                where=where,
            )
        if mtype in ("ratio", "rate") and (
            is_blank(metric.get("numerator")) or is_blank(metric.get("denominator"))
        ):
            report.add(
                "DSX-SPEC-026",
                "HIGH",
                f"Ratio metric {name!r} does not declare both numerator and denominator",
                detail=(
                    "Most metric disputes are denominator disputes. An undeclared denominator "
                    "silently changes when a filter changes."
                ),
                remedy="Declare numerator and denominator explicitly, including filters.",
                where=where,
            )

    report.ok(f"{len(metrics)} metric(s) declared")


def _validate_data(spec: dict, report: Report) -> None:
    sources = items(spec, "data")
    if not sources:
        report.add(
            "DSX-SPEC-030",
            "HIGH",
            "No data sources declared",
            detail="Reproducibility starts with naming what was read.",
            remedy="Add a data: block with name, source, period and row count per source.",
            where="spec.data",
        )
        return
    for index, source in enumerate(sources):
        where = f"spec.data[{index}]"
        if is_blank(source.get("name")):
            report.add("DSX-SPEC-031", "HIGH", "Data source is missing 'name'", where=where,
                       remedy="Name each source so findings can point at one.")
        if is_blank(source.get("source")):
            report.add(
                "DSX-SPEC-032", "MEDIUM",
                f"Data source {source.get('name', index)!r} has no 'source' locator",
                remedy="Record the table, file path or endpoint the data came from.",
                where=where,
            )
        if is_blank(source.get("period")):
            report.add(
                "DSX-SPEC-033", "MEDIUM",
                f"Data source {source.get('name', index)!r} has no 'period'",
                detail="Without a period the analysis cannot be re-run on the same window.",
                remedy="Record the date range as start..end.",
                where=where,
            )
    report.ok(f"{len(sources)} data source(s) declared")


def _validate_design_shape(spec: dict, report: Report) -> None:
    design = section(spec, "design")
    if not design:
        return
    kind = normalize(design.get("kind", ""))
    if kind and kind not in DESIGN_KINDS:
        report.add(
            "DSX-SPEC-040",
            "HIGH",
            f"design.kind {design.get('kind')!r} is not recognised",
            detail="Allowed: " + ", ".join(sorted(DESIGN_KINDS)),
            remedy="Pick the design actually used; 'observational' is the honest default.",
            where="spec.design.kind",
        )

    strategy = normalize(design.get("identification", "")) if design.get("identification") else ""
    if strategy and strategy not in IDENTIFICATION_STRATEGIES:
        report.add(
            "DSX-SPEC-041",
            "HIGH",
            f"design.identification {design.get('identification')!r} is not recognised",
            detail="Allowed: " + ", ".join(sorted(IDENTIFICATION_STRATEGIES)),
            remedy="Name the strategy that licenses a causal reading, or set 'none'.",
            where="spec.design.identification",
        )

    policy = normalize(design.get("peeking_policy", "")) if design.get("peeking_policy") else ""
    if policy and policy not in PEEKING_POLICIES:
        report.add(
            "DSX-SPEC-042",
            "HIGH",
            f"design.peeking_policy {design.get('peeking_policy')!r} is not recognised",
            detail="Allowed: " + ", ".join(sorted(PEEKING_POLICIES)),
            remedy="Declare how interim looks are handled before the test starts.",
            where="spec.design.peeking_policy",
        )

    correction = get(design, "multiplicity.correction")
    if correction and normalize(correction) not in MULTIPLICITY_CORRECTIONS:
        report.add(
            "DSX-SPEC-043",
            "HIGH",
            f"multiplicity.correction {correction!r} is not recognised",
            detail="Allowed: " + ", ".join(sorted(MULTIPLICITY_CORRECTIONS)),
            remedy="Use benjamini_hochberg for discovery, holm when every false positive is costly.",
            where="spec.design.multiplicity.correction",
        )

    adjustment = design.get("variance_adjustment")
    if adjustment and normalize(adjustment) not in VARIANCE_ADJUSTMENTS:
        report.add(
            "DSX-SPEC-044",
            "MEDIUM",
            f"design.variance_adjustment {adjustment!r} is not recognised",
            detail="Allowed: " + ", ".join(sorted(VARIANCE_ADJUSTMENTS)),
            remedy="Use cluster_robust or delta_method when the analysis unit is finer than the randomization unit.",
            where="spec.design.variance_adjustment",
        )


def _validate_model_shape(spec: dict, report: Report) -> None:
    model = section(spec, "model")
    if not model:
        return
    task = normalize(model.get("task", ""))
    if task and task not in ML_TASKS:
        report.add(
            "DSX-SPEC-050",
            "HIGH",
            f"model.task {model.get('task')!r} is not recognised",
            detail="Allowed: " + ", ".join(sorted(ML_TASKS)),
            remedy="Pick the learning task; it determines which metrics are admissible.",
            where="spec.model.task",
        )
    split = normalize(model.get("split", ""))
    if split and split not in SPLIT_STRATEGIES:
        report.add(
            "DSX-SPEC-051",
            "HIGH",
            f"model.split {model.get('split')!r} is not recognised",
            detail="Allowed: " + ", ".join(sorted(SPLIT_STRATEGIES)),
            remedy="Declare how train and test were separated.",
            where="spec.model.split",
        )
    if is_blank(model.get("target")):
        report.add(
            "DSX-SPEC-052", "HIGH", "model.target is missing",
            remedy="Name the column being predicted.", where="spec.model.target",
        )


def _validate_claims_shape(spec: dict, report: Report) -> None:
    claims = items(spec, "claims")
    if not claims:
        return
    for index, claim in enumerate(claims):
        where = f"spec.claims[{index}]"
        if is_blank(claim.get("text")):
            report.add("DSX-SPEC-060", "HIGH", "Claim has no text", where=where,
                       remedy="Write the claim as it will appear in the deliverable.")
        ctype = normalize(claim.get("type", ""))
        if not ctype:
            report.add(
                "DSX-SPEC-061",
                "HIGH",
                f"Claim {index} has no type",
                detail="Allowed: " + ", ".join(sorted(CLAIM_TYPES)),
                remedy="Label every claim descriptive, association, predictive or causal.",
                where=where,
            )
        elif ctype not in CLAIM_TYPES:
            report.add(
                "DSX-SPEC-062",
                "HIGH",
                f"Claim {index} has unrecognised type {claim.get('type')!r}",
                detail="Allowed: " + ", ".join(sorted(CLAIM_TYPES)),
                remedy="Use one of the four claim types.",
                where=where,
            )
    report.ok(f"{len(claims)} claim(s) declared")


def describe_vocabulary() -> "dict[str, Any]":
    """Machine-readable dump of every closed vocabulary — used by `dsx vocab`.

    Registry-driven (D-05): a dict-backed vocabulary dumps as a key-sorted dict of its
    descriptions; a set-backed vocabulary dumps as a sorted list. `chart_capabilities` stays
    special-cased — it is not a vocabulary, it is a capability matrix keyed by vocabulary.
    """
    out: "dict[str, Any]" = {}
    for name, obj in _VOCABULARIES:
        out[name] = {k: obj[k] for k in sorted(obj)} if isinstance(obj, dict) else sorted(obj)
    out["chart_capabilities"] = {
        key: sorted(values) for key, values in sorted(CHART_CAPABILITIES.items())
    }
    return out
