"""The ANALYSIS-SPEC contract — closed vocabularies and structural validation.

This is the pivot the whole capability turns on. An agent's job is to *fill* this
spec (judgement, flexible, stochastic). Code's job is to check the spec is
internally coherent and that produced artifacts satisfy it (deterministic).

Every vocabulary below is closed. A value outside it is a finding, not a warning
in prose — which is what makes agent output checkable instead of merely plausible.
"""

from __future__ import annotations

import re
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

CLAIM_TYPES = {"descriptive", "association", "predictive", "causal", "prescriptive"}

# Verbs that assert causation. Used to catch a causal claim mislabelled as
# association — the single most common analytical overreach.
#
# Structural criterion: a claim's or decision rule's causal content is set by
# communicative intent (is the sentence recommending an action believed to
# change an outcome?), not by surface verb morphology (finite vs. gerund vs.
# bare infinitive). Hernán, M. A. (2018), "The C-Word: Scientific Euphemisms
# Do Not Improve Causal Inference From Observational Data", American Journal
# of Public Health, 108(5):616-619, DOI 10.2105/AJPH.2018.304337. The exact
# quotable sentence/page locator within this paper is unverified at time of
# writing and is flagged for human confirmation (queued HQ-3, D-16); the
# author/year/title/venue anchor itself is not in doubt and matches this
# phase's D-05 provenance model.
#
# vocabulary_is_not_exhaustive: true — no published closed lexicon of
# "causal action verbs" exists; closure here is this project's editorial
# judgement, not anyone's published finding, and this file says so (the same
# model 11-CONTEXT D-10 established for the assumption vocabulary).
#
# Two tiers (D-04), NOT an epistemic softener — HEDGE_TERMS (claims.py:30-34)
# remains the sole epistemic softener:
#   - CAUSAL_VERBS_ALWAYS_HIT: finite verbs plus gerunds — unambiguously
#     verbal, fire on any \b-bounded occurrence regardless of context. A
#     gerund reaches the MEDIUM path only through the pre-existing
#     HEDGE_TERMS gate, exactly like any other verb hit here — it is never
#     itself a softener.
#   - CAUSAL_VERBS_PURPOSE_GATED: bare infinitives that double as nouns
#     ("increase", "decrease", "reduce") — ambiguous out of context (compare
#     "sales increase in Q4"), so they fire only inside a
#     purpose/recommendation construction ("to reduce churn", "in order to
#     increase..."), never as a bare substring.
CAUSAL_VERBS_ALWAYS_HIT = (
    "causes", "caused", "causing", "drives", "drove", "driving", "leads to", "led to",
    "results in", "resulted in", "increases", "decreases", "improves", "improved",
    "improving", "reduces", "reduced", "reducing", "boosts", "boosted", "boosting",
    "lifts", "lifted", "lifting", "impact of", "effect of", "because of", "due to",
    "thanks to", "responsible for", "attributable to", "uplift from", "generates",
    "generated", "generating", "increasing", "decreasing",
)

CAUSAL_VERBS_PURPOSE_GATED = ("reduce", "increase", "decrease")

# Compatibility alias for any consumer still importing the flat name (grep at
# plan 11.2-02 time found none outside dsx/checks/claims.py and
# dsx/checks/coherence.py, both of which now call causal_verb_matches()
# instead). Maps to the unambiguous always-hit tier only — the purpose-gated
# tier is deliberately NOT flattened in here, since a naive `verb in lowered`
# consumer of this alias would reintroduce the noun-homograph false positive
# the two-tier split exists to prevent.
CAUSAL_VERBS = CAUSAL_VERBS_ALWAYS_HIT

# Multiword purpose/recommendation markers that license a purpose-gated bare
# form. Unlike a bare "to" (handled separately below) these never introduce a
# raising/control complement, so they license the verb unconditionally.
_PURPOSE_MARKERS_MULTIWORD = ("in order to", "so as to", "aimed at", "designed to")

# Governing heads whose bare-infinitive "to <verb>" complement expresses
# tendency, aspect, failure or capacity — a raising/control infinitive, NOT a
# purpose adjunct (CR-01, 11.2 code review, §4 persona round). When one sits
# immediately before a bare "to <verb>", the purpose gate stays shut, so
# ordinary descriptive prose no longer fires DSX-CLM-011/DSX-COH-010:
# "usage tends to increase", "the pilot failed to reduce", "customers were
# quick to increase" are descriptions, not recommendations. Purpose "to"
# instead follows a noun object ("incentives to reduce churn"), a goal verb,
# or opens the clause ("To reduce churn, ...").
# INVARIANT — never add (a) a goal/intent head (aim, seek, intend, want, wish,
# plan, hope, propose, mean, strive, aspire) or (b) an achievement head that
# asserts the effect occurred (manage, prove, ensure, help): those license a
# genuine causal/purpose reading and denying them would open a false negative.
# The residual error therefore leans false-negative, the accepted direction at
# this CRITICAL blocking gate (Statistician vote); an omitted catenative leaks
# only a rare residual false positive, never a missed genuine recommendation.
_NON_PURPOSE_TO_PRECEDERS = frozenset({
    # tendency / aspect / state — a trend or phase, not a recommended effect
    "tend", "tends", "tended", "seem", "seems", "seemed",
    "appear", "appears", "appeared", "begin", "begins", "began", "begun",
    "start", "starts", "started", "continue", "continues", "continued",
    "cease", "ceases", "ceased", "remain", "remains", "remained",
    "happen", "happens", "happened", "used", "going", "about",
    # failure / resistance — the effect was not achieved
    "fail", "fails", "failed", "decline", "declines", "declined",
    "refuse", "refuses", "refused", "neglect", "neglects", "neglected",
    "struggle", "struggles", "struggled", "hesitate", "hesitates", "hesitated",
    # modal ability / propensity (raising adjectives) — capacity, not actuality
    "able", "unable", "likely", "unlikely", "apt", "prone", "bound",
    "ready", "willing", "reluctant", "eager", "keen", "hesitant",
    "quick", "quicker", "slow", "slower", "fast", "faster",
    "easy", "hard", "difficult", "impossible", "possible",
})

# Bounded, single-level quantifier only (mirrors _FALSIFIER_NUMBER_RE,
# spec.py:466-473, named threat T-7-03): a fixed-width window of at most 30
# characters between the marker and the verb. No `.*` chains, no nested
# quantifier groups.
_PURPOSE_GATE_WINDOW = r"[\s\w]{0,30}?"

_CAUSAL_VERBS_ALWAYS_HIT_RE: dict[str, re.Pattern[str]] = {
    verb: re.compile(rf"\b{re.escape(verb)}\b") for verb in CAUSAL_VERBS_ALWAYS_HIT
}

# Multiword marker + bounded window + bare verb — fires unconditionally.
_CAUSAL_VERBS_MULTIWORD_GATE_RE: dict[str, re.Pattern[str]] = {
    verb: re.compile(
        rf"\b(?:{'|'.join(re.escape(m) for m in _PURPOSE_MARKERS_MULTIWORD)})\b"
        rf"{_PURPOSE_GATE_WINDOW}\b{re.escape(verb)}\b"
    )
    for verb in CAUSAL_VERBS_PURPOSE_GATED
}

# Bare "to" + bounded window + bare verb. Each occurrence is validated against
# its governing head (see _bare_to_is_purpose) before it counts as a hit.
_CAUSAL_VERBS_BARE_TO_RE: dict[str, re.Pattern[str]] = {
    verb: re.compile(rf"\bto\b{_PURPOSE_GATE_WINDOW}\b{re.escape(verb)}\b")
    for verb in CAUSAL_VERBS_PURPOSE_GATED
}


def _bare_to_is_purpose(prefix: str) -> bool:
    """True when a bare "to" at the end of ``prefix`` reads as a purpose marker
    rather than a raising/control complement.

    Clause-initial "to" (no governing head) is a purpose adjunct. Otherwise the
    governing head must not be a ``_NON_PURPOSE_TO_PRECEDERS`` catenative or
    raising adjective. A trailing ``-ly`` adverb or a ``not``/``never`` negator
    is skipped first, so "failed repeatedly to reduce" and "chose not to
    reduce" resolve to their real head ("failed"/"chose").
    """
    words = re.findall(r"[a-z]+", prefix)
    while words and (words[-1] in {"not", "never"} or words[-1].endswith("ly")):
        words.pop()
    if not words:
        return True
    return words[-1] not in _NON_PURPOSE_TO_PRECEDERS


def causal_verb_matches(lowered: str) -> list[str]:
    """Return every causal-verb lexicon member found in ``lowered`` text.

    The single shared matcher for both consumers (dsx/checks/claims.py
    ``_check_causal_language`` and dsx/checks/coherence.py
    ``_check_decision_language``) so the two cannot drift (D-04). Always-hit
    members (finite verbs + gerunds) fire on any \\b-bounded occurrence.
    Purpose-gated members (bare infinitives / noun-homographs) fire only
    when preceded, within a small bounded window, by a purpose/
    recommendation marker — a false-positive-conservative context gate, not
    an epistemic softener.
    """
    hits = [
        verb
        for verb in CAUSAL_VERBS_ALWAYS_HIT
        if _CAUSAL_VERBS_ALWAYS_HIT_RE[verb].search(lowered)
    ]
    for verb in CAUSAL_VERBS_PURPOSE_GATED:
        if _CAUSAL_VERBS_MULTIWORD_GATE_RE[verb].search(lowered):
            hits.append(verb)
            continue
        # A bare "to <verb>" fires only when its governing head reads as
        # purpose, not as a raising/control complement (CR-01).
        if any(
            _bare_to_is_purpose(lowered[: m.start()])
            for m in _CAUSAL_VERBS_BARE_TO_RE[verb].finditer(lowered)
        ):
            hits.append(verb)
    return hits


# Substrings that mark an estimand falsifier as discriminating — it names a concrete,
# checkable observation that would prove the estimand wrong, not just a topic (D-05,
# REQ-P7-01). The first eight members are fixed by D-05; the remainder (the two bare
# comparison symbols) are the planner's discretion under D-05's explicit grant, chosen
# to widen the accepted set rather than narrow it, because the accepted risk in D-05
# runs toward false positives at the earliest and highest-friction gate.
FALSIFIER_DISCRIMINATORS = (
    "includes zero", "crosses", "below", "above", "exceeds", "does not exceed",
    "falls below", "fails to", "greater than", "less than", "<", ">",
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
    # Shapes present in the IT001-IT040 inventory that the twelve above do not
    # cover. See references/input-type-inventory.md.
    "single-value",
    "geospatial",
    "financial-ohlc",
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
    # A single number has no relationship to encode, so the honest marks are the
    # ones that do not imply one. Gauges are excluded deliberately: the arc is a
    # length-encoded channel with an arbitrary maximum.
    "single-value": frozenset({"big_number", "bullet", "sparkline"}),
    "geospatial": frozenset({"choropleth", "symbol_map", "cartogram", "hexbin"}),
    "financial-ohlc": frozenset({"candlestick", "ohlc_bar", "line", "column_range"}),
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

# Phase 11 (REQ-P11-01, REQ-P11-04): the estimand axis the frequentist admissibility
# adjudicator (dsx/frame/admissibility.py) keys on. Chosen over reusing
# analysis.outcome_type + n_groups + paired because that shape is unreachable from
# examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml, which has no
# analysis:/model: block at all. validity_frame.estimand is one of the six
# always-required sub-blocks, so this field is reachable from every spec that has
# passed the Phase 6 shape gate. Closed vocabulary compared by exact normalized
# membership only — no fuzzy string match on free prose (11-CONTEXT.md Claude's
# Discretion, binding constraint).
ESTIMAND_TYPES = {
    "difference_in_proportions": (
        "The estimand is a difference between two or more group proportions or rates."
    ),
    "difference_in_means": "The estimand is a difference between two or more group means.",
    "regression_coefficient": "The estimand is a coefficient from a fitted regression model.",
    "ratio_of_means": (
        "The estimand is a ratio of two quantities each estimated from the same units, "
        "such as a per-user revenue rate or any metric whose numerator and denominator "
        "are both random."
    ),
}

# Dependence structure -> admissible variance-adjustment method family (D-04, REQ-P7-04).
# Every method named below is drawn verbatim from VARIANCE_ADJUSTMENTS above — M-09
# forbids inventing a parallel vocabulary. "none" has no entry: a declared independence
# is the nothing-to-validate case, and the consuming check in plan 07-05 must handle it
# before indexing this map. delta_method appears in no entry — it addresses
# transformed-parameter variance, not correlated observations, so admitting it anywhere
# here would let a spec satisfy a dependence declaration with a method that does not
# address dependence.
#
# Citation: Cameron, A.C. and Miller, D.L. (2015), "A Practitioner's Guide to
# Cluster-Robust Inference", Journal of Human Resources 50(2):317-372 — covers the
# `clustered` and `repeated_measures` pairings directly.
# The same Cameron and Miller (2015) paper is cited for `temporal` and `spatial`; the
# exact section locator inside that paper for those two structures is UNVERIFIED —
# author, year, title, journal, volume, issue and page range were confirmed, the
# section number was not.
# Citation: Gelman, A. and Hill, J. (2007), Data Analysis Using Regression and
# Multilevel/Hierarchical Models, Cambridge University Press — covers `hierarchical`.
# The exact chapter locator inside it is UNVERIFIED, for the same reason as above.
# Conley, T.G. (1999) was considered as a second source for the `spatial` pairing and
# deliberately NOT cited: only training-knowledge attribution was available for it, and
# this project does not ship a citation it has not confirmed.
DEPENDENCE_ADMISSIBLE_METHODS: "dict[str, frozenset[str]]" = {
    "clustered": frozenset({"cluster_robust", "bootstrap_cluster", "mixed_effects"}),
    "repeated_measures": frozenset({"mixed_effects", "cluster_robust"}),
    "temporal": frozenset({"cluster_robust", "bootstrap_cluster", "mixed_effects"}),
    "spatial": frozenset({"cluster_robust", "bootstrap_cluster", "mixed_effects"}),
    "hierarchical": frozenset({"mixed_effects", "cluster_robust"}),
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

# The closed vocabulary the missingness.method_implied sub-field may hold (D-04,
# REQ-P11.3-03). Exactly seven locked members — do not shrink. multiple_imputation
# must stay (the good fixture declares it) and single_imputation must stay (else the
# DSX-VAL-060 CRITICAL block path in dsx/frame/val.py is unreachable). An unrecognised
# method is a decidable error (DSX-SPEC-082 HIGH via the _VALIDITY_FRAME_MEMBERSHIP
# loop), never a silent no-op. Whether a recognised method is LICENSED under the
# declared mechanism is a separate, content-layer judgment (dsx/frame/val.py's
# DSX-VAL-060) — this vocabulary only decides recognition, not licensing.
MISSINGNESS_METHODS = {
    "multiple_imputation": (
        "Missing values are imputed multiple times and the between-imputation "
        "variance is propagated into the standard errors (Rubin's rules)."
    ),
    "single_imputation": (
        "Each missing value is filled once and thereafter treated as if observed, "
        "which drops the missing-data variance component and understates uncertainty."
    ),
    "complete_case": "Only units with no missing values in the analysis are used.",
    "available_case": (
        "Each estimate uses whichever units have the values that estimate needs, "
        "so the effective sample differs across estimates."
    ),
    "mechanism_model": (
        "The missingness mechanism itself is modelled explicitly (e.g. a shared-parameter "
        "or joint model of the outcome and the missingness process)."
    ),
    "selection_model": (
        "Missingness is modelled as a selection process conditional on the (possibly "
        "unobserved) outcome."
    ),
    "pattern_mixture_model": (
        "The distribution is modelled separately within each missingness pattern and "
        "then mixed over the patterns."
    ),
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

# The closed namespace the fallback_rule mini-language (dsx/frame/prereg.py, Phase 10,
# REQ-P10-01) may reference. (a) This is deliberately closed: a rule naming a fact
# outside this dict is a decidable error (DSX-PRE-010), never a silent no-op (D-04).
# (b) It coins no new contract field — every value is a dotted path to a field that
# already exists and is already read by a shipped check: results.comparisons_looked_at
# is read by dsx/checks/design.py::_check_exploratory_looks; results.interim_looks and
# design.alpha are read by dsx/checks/design.py::_check_peeking. (Stable function-name
# references, not line numbers, so this comment cannot drift on the next design.py edit —
# D-03.) (c) results.observed_n is deliberately excluded — it is a list of per-arm
# counts, not a scalar, and no Phase 10 requirement needs list-to-scalar semantics.
# (d) brief.md's own worked example names a fact, `clusters`, that has never existed in
# any spec in this repository — the brief binds structurally (fact -> number -> compare),
# not at the token level.
PREREG_FACTS: "dict[str, str]" = {
    "alpha": "design.alpha",
    "comparisons_looked_at": "results.comparisons_looked_at",
    "interim_looks": "results.interim_looks",
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
# Deliberately excludes SPEC_VERSION, CAUSAL_VERBS, REQUIRED_TOP_LEVEL,
# IMBALANCE_UNSAFE_METRICS, DEPENDENCE_ADMISSIBLE_METHODS and FALSIFIER_DISCRIMINATORS —
# they are not vocabularies. chart_capabilities stays special-cased in
# describe_vocabulary() below, exactly as before.
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
    ("estimand_types", ESTIMAND_TYPES),
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


def is_blank_text(value: Any) -> bool:
    """Return True unless ``value`` is a string carrying non-whitespace text.

    Deliberately not ``is_blank``'s general semantics: this is the predicate
    for free-text declarations whose entire declared content is the text an
    operator wrote — a bare number or boolean carries no declared content, so
    every non-string type reads as blank here, even though ``is_blank`` itself
    reads a declared ``0`` or ``False`` as present. ``is_blank`` is read by
    138 call sites where a declared ``0`` or ``False`` is meaningful data, so
    the tightening lives in this separate helper rather than in ``is_blank``.
    ``references/paradigm-symmetry.md`` is the contract this predicate serves.
    """
    return not isinstance(value, str) or is_blank(value)


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


# ── Falsifier lexicon helpers (D-05, REQ-P7-01) ─────────────────────────────

# Whole-value equality after normalize(), never substring containment — that is what
# keeps "none identified" (the good fixture's sampling_frame.selection_risk value, a
# different field entirely) out of this set even though it starts with "none".
_FALSIFIER_REFUSALS = frozenset(
    {"n/a", "na", "tbd", "tba", "none", "unknown", "not assessed", "to be determined"}
)

# A whole value that opens with '<' and closes with '>' with no intervening '>' — the
# angle-bracket placeholder shape every template ships (e.g. "<the observation that
# would prove this wrong>"). Not multiline, not anchored on a line end, so the CRLF
# checkout cannot change the result.
_PLACEHOLDER_RE = re.compile(r"^<[^>]*>$")

# Re-homed from the numeric-token idiom at dsx/checks/claims.py:340-375 (the pattern is
# copied, not the import — D-03a forbids importing dsx.checks from dsx.spec). Bounded,
# non-nested quantifiers only: a nested quantifier here would expose the gate to a
# denial-of-service through catastrophic backtracking on adversarial free text
# (threat T-7-03).
_FALSIFIER_NUMBER_RE = re.compile(r"\d+(?:\.\d+)?\s*(?:%|pp)?")


def is_placeholder_or_refusal(value: Any) -> bool:
    """True when ``value`` is blank, an angle-bracket placeholder, or a refusal token.

    Layered beside ``is_blank()``, never a replacement for it — ``is_blank()`` stays
    unchanged because placeholder text still counts as present for the sampling-frame
    and measurement checks (plan 07-06), which must treat placeholder text as present
    so the template does not trip them.
    """
    if is_blank(value):
        return True
    if isinstance(value, str) and _PLACEHOLDER_RE.match(value.strip()):
        return True
    return normalize(value) in _FALSIFIER_REFUSALS


def falsifier_is_discriminating(value: Any) -> bool:
    """True when ``value`` names a concrete, checkable observation that would prove an
    estimand wrong — carries a comparison predicate (`FALSIFIER_DISCRIMINATORS`) or a
    numeric threshold, and is neither blank, a placeholder, nor a refusal token.
    """
    if is_placeholder_or_refusal(value):
        return False
    text = str(value).lower()
    if any(token in text for token in FALSIFIER_DISCRIMINATORS):
        return True
    return bool(_FALSIFIER_NUMBER_RE.search(str(value)))


# A bare number-of-units duration ("30 days", "8 weeks", "next quarter" is handled by
# the recurring-token set below since it carries no digit). Bounded, non-nested
# quantifiers only (mirrors _FALSIFIER_NUMBER_RE above, threat T-11.2-08 / T-7-03):
# no `.*` chains.
_WINDOW_DURATION_RE = re.compile(
    r"\b\d+\s*(?:day|days|week|weeks|month|months|quarter|quarters|year|years)\b"
)

# A date/deadline: an ISO calendar date (2026-07-15) or a fiscal-quarter date
# (2026-Q4 / 2026-q4). Bounded, non-nested quantifiers only.
_WINDOW_DATE_RE = re.compile(r"\b\d{4}-(?:\d{2}-\d{2}|q[1-4])\b", re.IGNORECASE)

# Named recurring checkpoints that anchor a re-visit in time without carrying a
# digit (e.g. "at the next quarterly review"). Substring match, same idiom as
# FALSIFIER_DISCRIMINATORS above — not a regex, so no backtracking surface at all.
_WINDOW_RECURRING_TOKENS = (
    "quarterly review", "annual review", "monthly review", "weekly review",
    "next review", "review cycle",
)


def _has_window_token(text: str) -> bool:
    """True when ``text`` carries a time anchor: a duration ("8 weeks"), a
    date/deadline (an ISO date or a fiscal-quarter date like "2026-Q4"), or a named
    recurring checkpoint ("quarterly review"). Bounded, non-nested quantifiers only
    (mirrors ``_FALSIFIER_NUMBER_RE``, threat T-11.2-08 / T-7-03) — no `.*` chains.
    """
    lowered = str(text).lower()
    if _WINDOW_DURATION_RE.search(lowered):
        return True
    if _WINDOW_DATE_RE.search(lowered):
        return True
    return any(token in lowered for token in _WINDOW_RECURRING_TOKENS)


def _strip_window_tokens(text: str) -> str:
    """Remove every time-anchor span from ``text``: the duration and
    date/deadline regexes and the recurring-checkpoint substrings, using the
    exact same patterns ``_has_window_token`` recognises so detection and
    stripping cannot diverge.

    Used only by ``revisit_when_is_discriminating`` so the discriminating
    metric/threshold test runs on what is LEFT once the time anchor is removed.
    Without it the anchor's own digits (the year "2026", the duration count
    "30") satisfy ``falsifier_is_discriminating``'s numeric branch, and a bare
    "revisit at the 2026-Q4 review" clears a check whose contract demands a
    named metric AND a threshold AND a time anchor as three separate things
    (WR-02, 11.2 code review, §4 persona round).
    """
    lowered = str(text).lower()
    lowered = _WINDOW_DURATION_RE.sub(" ", lowered)
    lowered = _WINDOW_DATE_RE.sub(" ", lowered)
    for token in _WINDOW_RECURRING_TOKENS:
        lowered = lowered.replace(token, " ")
    return lowered


def revisit_when_is_discriminating(value: Any) -> bool:
    """True when ``value`` carries a time anchor — a duration, date/deadline, or
    time-anchored recurring event — AND names a discriminating condition (a
    comparison predicate or numeric threshold) in the text that REMAINS once the
    time anchor is stripped out.

    A NEW sibling, not an extension of ``falsifier_is_discriminating`` itself: its two
    estimand callers (val.py:236, val.py:637) validate a logical falsifier with no
    time anchor, and the ``good`` fixture's estimand falsifier (good-ANALYSIS-SPEC.yaml,
    the ``validity_frame.estimand.falsifier`` field) carries none — extending the
    shared predicate would regress DSX-VAL-011 on that fixture (D-07, RESEARCH
    landmine b). ``falsifier_is_discriminating`` is called unchanged, never mutated;
    the residual test lives here so the estimand path is provably untouched.

    Known limit (WR-02): a threshold expressed in the same lexical shape as a
    window — e.g. an SLA "within 30 days" as the metric itself — is stripped
    with the anchor and reads as non-discriminating. This is genuinely ambiguous
    ("revisit in 30 days" is indistinguishable) and does not occur in the corpus;
    DSX-COH-040's remedy models the discriminating form with a comparison word.
    """
    return _has_window_token(str(value)) and falsifier_is_discriminating(
        _strip_window_tokens(value)
    )


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
    _validate_validity_frame_shape(spec, report)
    _validate_inference_shape(spec, report)

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
                remedy=(
                    "Label every claim descriptive, association, predictive, "
                    "causal or prescriptive."
                ),
                where=where,
            )
        elif ctype not in CLAIM_TYPES:
            report.add(
                "DSX-SPEC-062",
                "HIGH",
                f"Claim {index} has unrecognised type {claim.get('type')!r}",
                detail="Allowed: " + ", ".join(sorted(CLAIM_TYPES)),
                remedy=(
                    "Use one of the five claim types: descriptive, association, "
                    "predictive, causal or prescriptive."
                ),
                where=where,
            )
    report.ok(f"{len(claims)} claim(s) declared")


# ── validity_frame / inference structural validators (Phase 6, REQ-P6-02/03/04) ──
# Locked by decision R-01. Diverges deliberately from research/PITFALLS.md Pitfall 2,
# which placed `interference` in a conditional tier and `identification` in the
# causal-only tier: REQ-P6-03 and ROADMAP Success Criterion 2 are the binding sources
# and both put `interference` in the causal-only list below. Do not "fix" this back to
# match PITFALLS.md.
_VALIDITY_FRAME_ALWAYS_REQUIRED = (
    "estimand", "units", "measurement", "dependence", "sampling_frame", "missingness",
)
_VALIDITY_FRAME_CAUSAL_REQUIRED = ("identification", "interference", "triggering", "stability")

# (sub-block, sub-field, closed vocabulary). `dependence.method_family_required` reuses
# VARIANCE_ADJUSTMENTS verbatim (M-09) — no parallel set is defined for it. The
# `estimand.type` row (Phase 11, REQ-P11-01/04) is the adjudication axis the
# frequentist admissibility adjudicator (dsx/frame/admissibility.py) keys on; it is
# deliberately optional — the membership loop below `continue`s on a blank value
# before testing membership, so omitting it produces no finding.
_VALIDITY_FRAME_MEMBERSHIP: "tuple[tuple[str, str, Any], ...]" = (
    ("estimand", "type", ESTIMAND_TYPES),
    ("identification", "strength", IDENTIFICATION_STRENGTHS),
    ("identification", "constraint_source", CONSTRAINT_SOURCES),
    ("dependence", "structure", DEPENDENCE_STRUCTURES),
    ("dependence", "method_family_required", VARIANCE_ADJUSTMENTS),
    ("interference", "risk", INTERFERENCE_RISKS),
    ("interference", "mitigation", INTERFERENCE_MITIGATIONS),
    ("triggering", "analysis_population", ANALYSIS_POPULATIONS),
    ("missingness", "mechanism", MISSINGNESS_MECHANISMS),
    ("missingness", "method_implied", MISSINGNESS_METHODS),
)


def needs_causal_block(spec: dict) -> bool:
    """The single condition deciding whether the causal ``validity_frame`` sub-blocks
    (identification, interference, triggering, stability) apply — shared by the shape
    validator and the frame checks so the two can never disagree (D-16)."""
    return (
        normalize(spec.get("question_type", "")) in ("causal", "prescriptive")
        or normalize(get(spec, "design.kind", "")) == "experiment"
    )


# The closed key set for the validity_frame.exclusions sub-block (DSX-SPEC-083,
# REQ-P11.3-04). Born strict on exclusions ONLY: a declared row-exclusion rule
# carries exactly these four keys and nothing else, so a data-dependent row count
# (n_excluded) cannot be smuggled into a content-locked frame. This strictness is
# deliberately NOT retrofitted to the legacy tolerant validity_frame/inference
# blocks below (D-09) — those still parse unknown keys silently.
_EXCLUSIONS_ALLOWED_KEYS = {"rule", "action", "applied_before_split", "justification"}


def _validate_validity_frame_shape(spec: dict, report: Report) -> None:
    """Requiredness, aggregation and membership shape of the ``validity_frame:`` block.

    Codes DSX-SPEC-080 (block absent), DSX-SPEC-081 (required sub-block missing, one
    finding per sub-block per D-11) and DSX-SPEC-082 (sub-field outside its closed
    vocabulary).

    Citation: Hernan, M.A. & Robins, J.M. (2020), *Causal Inference: What If*, Chapter 1
    ("A Definition of Causal Effect") and Chapter 3 ("Observational Studies") — the
    estimand and identification-condition vocabulary the `estimand` and `identification`
    sub-blocks encode.
    Citation: Little, R.J.A. & Rubin, D.B. (2019), *Statistical Analysis with Missing
    Data*, 3rd ed., Chapter 1 ("Introduction") — the MCAR/MAR/MNAR missingness-mechanism
    taxonomy this validator's membership check enforces via MISSINGNESS_MECHANISMS.
    Citation: Imbens, G.W. & Rubin, D.B. (2015), *Causal Inference for Statistics,
    Social, and Biomedical Sciences*, Chapter 1, Section 1.6 ("The Stable Unit Treatment
    Value Assumption") — the interference/SUTVA vocabulary the `interference` sub-block
    encodes.
    Structural criterion: presence-and-membership test, not a numeric one. Requiredness
    is a set-membership check against a question_type/design.kind-gated list of exactly
    ten sub-block names; the aggregation rule (one finding per missing sub-block once the
    block itself is present) and the eight per-field vocabulary memberships are D-11 and
    D-04, respectively. No threshold, effect size or statistic is computed here.
    """
    from .decisions import DecisionRecord

    frame = spec.get("validity_frame")
    required = list(_VALIDITY_FRAME_ALWAYS_REQUIRED) + (
        list(_VALIDITY_FRAME_CAUSAL_REQUIRED) if needs_causal_block(spec) else []
    )

    report.context.setdefault("decisions", []).append(
        DecisionRecord(
            id="",
            invocation_id="",
            layer="deterministic",
            choice=f"validity_frame requires: {', '.join(required)}",
            inputs=["question_type", "design.kind"],
            rule=(
                "R-01: question_type in ('causal', 'prescriptive') or design.kind == "
                "'experiment' adds identification, interference, triggering and stability "
                "to the six always-required sub-blocks (estimand, units, measurement, "
                "dependence, sampling_frame, missingness)."
            ),
            citation="Hernan & Robins (2020), Causal Inference: What If, Ch. 1 and Ch. 3",
            counterfactual=(
                "If question_type were not 'causal'/'prescriptive' and design.kind were "
                "not 'experiment', identification, interference, triggering and stability "
                "would not be required."
            ),
        ).to_dict()
    )

    if not isinstance(frame, dict) or not frame:
        report.add(
            "DSX-SPEC-080",
            "CRITICAL",
            "validity_frame block is missing",
            detail="Required sub-blocks: " + ", ".join(required),
            remedy=(
                "Add a validity_frame: block with the required sub-blocks. "
                "See templates/ANALYSIS-SPEC.yaml."
            ),
            where="spec.validity_frame",
        )
        return

    missing = [name for name in required if not frame.get(name) or not isinstance(frame.get(name), dict)]
    if missing:
        for name in missing:
            report.add(
                "DSX-SPEC-081",
                "CRITICAL",
                f"validity_frame.{name} is required and missing",
                detail=f"question_type/design.kind requires: {', '.join(required)}",
                remedy=f"Declare validity_frame.{name} with its required sub-fields.",
                where=f"spec.validity_frame.{name}",
            )
    else:
        report.ok("validity_frame required sub-blocks present")

    for block_name, field_name, vocab in _VALIDITY_FRAME_MEMBERSHIP:
        block = frame.get(block_name)
        if not isinstance(block, dict):
            continue
        value = block.get(field_name)
        if is_blank(value):
            continue
        # Case-insensitive membership: most vocabularies are already lowercase (normalize()
        # is a no-op against their keys), but MISSINGNESS_MECHANISMS is a case-sensitive
        # acronym set (MCAR/MAR/MNAR, per R-02) — comparing against normalized keys keeps
        # exactly one comparison path instead of special-casing this one field.
        if normalize(value) not in {normalize(k) for k in vocab}:
            report.add(
                "DSX-SPEC-082",
                "HIGH",
                f"validity_frame.{block_name}.{field_name} {value!r} is not recognised",
                detail="Allowed: " + ", ".join(sorted(vocab)),
                remedy=f"Set validity_frame.{block_name}.{field_name} to one of the allowed values.",
                where=f"spec.validity_frame.{block_name}.{field_name}",
            )

    # DSX-SPEC-083 (REQ-P11.3-04): the exclusions sub-block is closed-key. Scoped
    # to frame.get("exclusions") ONLY — the membership loop above deliberately
    # tolerates unknown keys in every other sub-block (and the inference block
    # tolerates them too), and this guard does NOT widen that tolerance (D-09). The
    # sub-block is accepted as either a single rule-dict or a list of rule-dicts;
    # each entry's keys must fall inside _EXCLUSIONS_ALLOWED_KEYS so a data-dependent
    # row count cannot be registered in a content-locked frame. A non-dict/list
    # value is left to the content check's presence guard (T-11.3-10).
    exclusions = frame.get("exclusions")
    if isinstance(exclusions, (dict, list)):
        entries = exclusions if isinstance(exclusions, list) else [exclusions]
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            unexpected = set(entry.keys()) - _EXCLUSIONS_ALLOWED_KEYS
            if not unexpected:
                continue
            report.add(
                "DSX-SPEC-083",
                "HIGH",
                "unexpected key in the closed exclusions sub-block",
                detail=(
                    "validity_frame.exclusions carries key(s) outside the closed set "
                    f"{sorted(_EXCLUSIONS_ALLOWED_KEYS)}: {sorted(unexpected)}. A "
                    "data-dependent row count (e.g. n_excluded) has no place in the frame."
                ),
                remedy=(
                    "Remove the unexpected key(s). Row counts belong in results/ or the "
                    "data profile, not in validity_frame — the frame is content-locked at "
                    "plan time, and a count that moves with the data would silently change "
                    "the frame digest."
                ),
                where="spec.validity_frame.exclusions",
            )


# The nine inference: field names this contract recognises, split across two
# requirements. A machine-readable manifest pinning the declared field list against
# drift; its one consumer is the drift-guard test
# tests/test_dsx.py::test_inference_fields_constant_matches_req_p6_04, plus
# describe_vocabulary()'s inference_fields key below.
#
# The first six are the REQ-P6-04 manifest. The last three —
# threshold_calibration, prior_justification, decision_threshold — are REQ-P9's
# monitoring-discipline clearing declarations (D-05): threshold_calibration and
# prior_justification are DSX-PAR-011's disjunctive clearing pair (alongside
# alpha_spending), and threshold_calibration alone is also DSX-PAR-010's
# alternative to alpha_spending. decision_threshold is recorded and never parsed
# by any check (T-9-01) — it exists so an operator's stated posterior-probability
# decision rule (e.g. P(B>A) > 0.95) is on record next to the fields that gate on
# it. All three new fields are deliberately free-text scalars, not a
# {method:, sims:, fpr:} sub-dict: giving every clearing declaration on both
# paradigms the same shape is what makes the brief-D-12 cost-symmetry argument
# mechanically provable by one shared text-only blank-check predicate
# (is_blank_text) instead of by inspection (references/paradigm-symmetry.md).
#
# This tuple is not an enforced closed set: _validate_inference_shape vocabulary-checks
# only three of these nine fields (paradigm, paradigm_justification, declared_at, via
# _INFERENCE_MEMBERSHIP below) and rejects exactly one non-member field, the one named by
# _INFERENCE_REMOVED_FIELD. An unrecognised or misspelled key under inference: — e.g.
# `inference: {paradgim: bayesian}` — is accepted silently today; there is no unknown-key
# check for this block. `dsx vocab`'s inference_fields key and this template's scaffold
# are therefore the only two mechanisms by which an operator can discover or correct a
# misspelled field name (D-05).
#
# M-02 removes `stopping_rule`: the stopping-rule concept lives in design.peeking_policy,
# not here.
_INFERENCE_FIELDS = (
    "paradigm", "paradigm_justification", "declared_at",
    "primary_procedure", "alpha_spending", "fallback_rule",
    "threshold_calibration", "prior_justification", "decision_threshold",
)

_INFERENCE_MEMBERSHIP: "tuple[tuple[str, Any], ...]" = (
    ("paradigm", PARADIGMS),
    ("paradigm_justification", PARADIGM_JUSTIFICATIONS),
    ("declared_at", DECLARATION_POINTS),
)

# The field M-02 removed from inference: — declaring it is redirected, not silently
# ignored. The concept it named (the stopping rule) lives in design.peeking_policy.
_INFERENCE_REMOVED_FIELD = "stopping_rule"


def _validate_inference_shape(spec: dict, report: Report) -> None:
    """Shape validation of the optional ``inference:`` block.

    Codes DSX-SPEC-085 (sub-field outside its closed vocabulary) and DSX-SPEC-086 (the
    field M-02 removed is declared).

    Citation: Deng, A., Lu, J. & Chen, S. (2016), "Continuous Monitoring of A/B Tests
    without Pain: Optional Stopping in Bayesian Testing", IEEE DSAA 2016 — the primary
    source establishing that a decision procedure's realised error rate depends on the
    declared inferential paradigm and monitoring plan, which is why inference.paradigm
    must be declared rather than assumed. The exact section/theorem locator within this
    paper is unverified at time of writing and is flagged for human confirmation in the
    06-06 plan summary; the author/year/title/venue anchor itself is not in doubt and
    matches brief.md section 7.
    Structural criterion: presence-and-membership test on three closed-vocabulary
    sub-fields, plus a fourth check for the presence of a removed field name. No
    numeric threshold is computed here.
    """
    inference = spec.get("inference")
    if not isinstance(inference, dict) or not inference:
        return

    from .decisions import DecisionRecord

    declared_paradigm = inference.get("paradigm")
    report.context.setdefault("decisions", []).append(
        DecisionRecord(
            id="",
            invocation_id="",
            layer="deterministic",
            choice=(
                f"paradigm={declared_paradigm}" if not is_blank(declared_paradigm)
                else "paradigm=undeclared"
            ),
            inputs=["inference.paradigm"],
            rule=(
                "inference.paradigm must be a member of PARADIGMS "
                "(frequentist, bayesian) (REQ-P6-04)."
            ),
            citation="Deng, Lu & Chen (2016), Continuous Monitoring of A/B Tests without Pain",
            counterfactual=(
                "Declaring the other paradigm would route this analysis to that "
                "paradigm's symmetric monitoring-discipline checks (Phase 9's "
                "DSX-PAR-010/011 pair) instead of the ones this declaration selects."
            ),
        ).to_dict()
    )

    for field_name, vocab in _INFERENCE_MEMBERSHIP:
        value = inference.get(field_name)
        if is_blank(value):
            continue
        if normalize(value) not in vocab:
            report.add(
                "DSX-SPEC-085",
                "HIGH",
                f"inference.{field_name} {value!r} is not recognised",
                detail="Allowed: " + ", ".join(sorted(vocab)),
                remedy=f"Set inference.{field_name} to one of the allowed values.",
                where=f"spec.inference.{field_name}",
            )

    if _INFERENCE_REMOVED_FIELD in inference:
        report.add(
            "DSX-SPEC-086",
            "HIGH",
            f"inference.{_INFERENCE_REMOVED_FIELD} is not a field under inference:",
            detail=(
                "No equivalent field exists under inference: — the stopping-rule "
                "concept (M-02) lives in design.peeking_policy."
            ),
            remedy="Remove inference.stopping_rule; declare design.peeking_policy instead.",
            where=f"spec.inference.{_INFERENCE_REMOVED_FIELD}",
        )


def describe_vocabulary() -> "dict[str, Any]":
    """Machine-readable dump of every closed vocabulary — used by `dsx vocab`.

    Registry-driven (D-05): a dict-backed vocabulary dumps as a key-sorted dict of its
    descriptions; a set-backed vocabulary dumps as a sorted list. `chart_capabilities` stays
    special-cased — it is not a vocabulary, it is a capability matrix keyed by vocabulary.
    `inference_fields` is a second special case (D-05, REQ-P9): the flat, sorted list of
    every `inference:` field name this contract recognises, not a vocabulary of values. It
    exists because there is no unknown-key check under `inference:` — `dsx vocab` and the
    template scaffold are the only two mechanisms by which an operator can discover or
    correct a misspelled field name. `prereg_facts` is a third special case (Phase 10,
    REQ-P10-01): the closed namespace of short fact names the `fallback_rule`
    mini-language may reference, mapped to the dotted spec path each one reads — a
    namespace of field *names*, not a vocabulary of values, and one of the two ways an
    operator can discover a fact name the mini-language will accept (the other is
    reading `PREREG_FACTS` itself, imported by `dsx/frame/prereg.py`).
    """
    out: "dict[str, Any]" = {}
    for name, obj in _VOCABULARIES:
        out[name] = {k: obj[k] for k in sorted(obj)} if isinstance(obj, dict) else sorted(obj)
    out["chart_capabilities"] = {
        key: sorted(values) for key, values in sorted(CHART_CAPABILITIES.items())
    }
    out["inference_fields"] = sorted(_INFERENCE_FIELDS)
    out["prereg_facts"] = {k: PREREG_FACTS[k] for k in sorted(PREREG_FACTS)}
    return out
