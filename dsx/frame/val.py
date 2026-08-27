"""DSX-VAL-* — the validity-frame content checks (Phase 7).

Phase 6's ``_validate_validity_frame_shape`` (``dsx/spec.py``) already checks
*shape*: is the ``validity_frame:`` block present, is each required sub-block
present, does each closed-vocabulary sub-field hold a member of its
vocabulary. This module checks *content* of a sub-block that is present and
structurally well-formed: is the estimand it declares actually complete, and
is it actually falsifiable. Do not duplicate the shape checks here — a
missing sub-block is Phase 6's ``DSX-SPEC-080``/``DSX-SPEC-081`` territory,
and firing a ``DSX-VAL-*`` code on top of that would double-report a single
defect.

Two of the family's nine planned codes shipped in plan 07-03 (``DSX-VAL-010``,
``DSX-VAL-011``, both about the ``estimand`` sub-block), and two more shipped
in plan 07-04 (``DSX-VAL-020``, the unit triad; ``DSX-VAL-021``, unit drift).
Plan 07-05 added three more: ``DSX-VAL-030`` (dependence — a declared
dependence structure with no admissible method family) and the identification
pair ``DSX-VAL-040``/``DSX-VAL-041`` (weak identification naming no
constraint; strong identification also carrying a constraint that informs the
parameter's scale). This plan (07-06) adds the last three: ``DSX-VAL-050``
(sampling frame — presence and internal consistency between declared
exclusions and the declared selection risk), ``DSX-VAL-060`` (missingness —
a declared mechanism paired with an implied method the mechanism does not
license, at HIGH or CRITICAL depending on the pairing), and ``DSX-VAL-070``
(measurement — a construct declared with no operationalisation). All nine
planned codes now exist behind the same ``check()`` dispatcher.

D-11 (mechanically proven by ``tests/test_frame_boundary.py``'s
``TestFrameParadigmReadBoundary``): no code path in this module reads the
declared inference paradigm field, in any form — not through ``get()``, not
by direct dictionary indexing, not in a message string. A prior does not
save an analysis from pseudo-replication; a check that branches on the
declared paradigm is in the wrong layer.
"""

from __future__ import annotations

from ..decisions import DecisionRecord
from ..findings import Report
from ..mathx import design_effect
from ..spec import (
    CONSTRAINT_SOURCES,
    DEPENDENCE_ADMISSIBLE_METHODS,
    IDENTIFICATION_STRENGTHS,
    MISSINGNESS_MECHANISMS,
    falsifier_is_discriminating,
    get,
    is_blank,
    is_placeholder_or_refusal,
    normalize,
)

# The four estimand attributes DSX-VAL-010 requires present. `falsifier` is
# deliberately excluded — it routes entirely through DSX-VAL-011
# (_check_estimand_falsifiability), so a blank falsifier fires exactly one
# code, not two (D-05, disambiguating D-02 and D-05 read together).
_ESTIMAND_REQUIRED_FIELDS: "tuple[str, ...]" = (
    "quantity",
    "population",
    "contrast",
    "time_window",
)

_ESTIMAND_CITATION = (
    "International Council for Harmonisation (ICH) (2019), E9(R1) Addendum, "
    "EMA/CHMP/ICH/436221/2017, Step 5, section A.3.3 (\"Estimand attributes\") "
    "and section A.3.2; Hernan, M.A. & Robins, J.M. (2016), American Journal of "
    "Epidemiology 183(8):758-764, Table 1; Popper, K.R. (1959/2002 reissue), "
    "The Logic of Scientific Discovery, Part I, Chapter 1, section 6"
)

# The design-effect illustration inputs (D-10, D-11): the Cochrane Handbook's
# own worked example, not derived from any spec field — the contract has no
# cluster-size or intraclass-correlation field anywhere to derive one from.
_UNIT_TRIAD_ICC = 0.02
_UNIT_TRIAD_M = 29.8

_UNIT_TRIAD_CITATION = (
    "Kish, L. (1965), Survey Sampling, section 8.2, page 258 (design-effect "
    "definition) and pages 161-162 (intraclass correlation); Higgins, J.P.T., "
    "Eldridge, S. and Li, T. (2024), Cochrane Handbook for Systematic Reviews "
    "of Interventions version 6.5, sections 23.1.4 and 23.1.4.1. Section 8.2 "
    "was confirmed for the design-effect definition; no section number was "
    "confirmed for the design-effect formula itself, and that locator is "
    "UNVERIFIED — do not invent one."
)

_UNIT_DRIFT_CITATION = (
    "Hernan, M.A. & Robins, J.M. (2020), Causal Inference: What If, Chapter 1, "
    "section 1.2 (\"Average causal effects\")"
)

_DEPENDENCE_CITATION = (
    "Cameron, A.C. & Miller, D.L. (2015), \"A Practitioner's Guide to Cluster-Robust "
    "Inference\", Journal of Human Resources 50(2):317-372, for the clustered, "
    "repeated_measures, temporal and spatial pairings; Gelman, A. & Hill, J. (2007), "
    "Data Analysis Using Regression and Multilevel/Hierarchical Models, Cambridge "
    "University Press, for the hierarchical pairing. The exact section locator "
    "inside Cameron and Miller and the exact chapter locator inside Gelman and Hill "
    "are both UNVERIFIED — author, year, title and venue were confirmed for each; "
    "the internal locators were not. Do not invent either."
)

_IDENTIFICATION_CITATION = (
    "Gelman, A., Simpson, D. & Betancourt, M. (2017), \"The Prior Can Often Only Be "
    "Understood in the Context of the Likelihood\", Entropy 19(10), article 555, "
    "section 3.3 (\"For complex models, certain aspects of the prior will always be "
    "relevant\") and section 1.2 (\"Existing methods for setting priors already "
    "depend on the likelihood\"). Whether the typeset MDPI journal version uses the "
    "same section numbers as the arXiv final version is UNVERIFIED — cited by "
    "section number and title together so the locator survives either. The "
    "partition of CONSTRAINT_SOURCES this check tests against is project-defined; "
    "no published source draws it."
)

# Constraint-source classification for DSX-VAL-041 (D-05): which constraint sources
# carry information about the parameter's *scale*, as opposed to informing only
# whether an effect exists at all. Derived from each member's own description text
# in CONSTRAINT_SOURCES (dsx/spec.py):
#   - informative_priors: "A prior distribution encodes external information about
#     the parameter" — the prior is, by its own definition, parameter-scale
#     information.
#   - penalisation: "A penalty term ... shrinks the estimate toward a null or
#     reference value" — the shrinkage target is a parameter-scale constraint.
#   - design_restriction: "The study design itself restricts the parameter space"
#     — a restriction on the parameter space is, definitionally, information about
#     the parameter's scale.
#   - hierarchical_pooling: "Partial pooling ... constrains group-level estimates"
#     — pooling toward a shared distribution constrains the parameter's scale.
# "none" is deliberately absent: its own description ("No external constraint
# informs the estimate beyond the observed data") is the negation of membership.
#
# This four-against-one partition is PROJECT-DEFINED — no published source draws
# it. Gelman, Simpson & Betancourt (2017) support the underlying premise (their
# section 3.3 argues the prior is always relevant for complex models) and their
# section 1.2 gives a prior taxonomy that lines up with two of these four members
# (structural priors -> hierarchical_pooling; regularizing priors ->
# penalisation), but they publish no such four-way partition, and
# design_restriction has no counterpart in their paper at all. Say so in the
# docstring too (D-05's whole point) — this comment is not a substitute for the
# disclosure at the point of use.
_PARAMETER_SCALE_CONSTRAINT_SOURCES: "frozenset[str]" = frozenset(
    {"informative_priors", "penalisation", "design_restriction", "hierarchical_pooling"}
)

_SAMPLING_FRAME_CITATION = (
    "Lohr, S.L. (2021), Sampling: Design and Analysis, 3rd edition, Chapter 1, "
    "sections 1.2, 1.3 and 1.3.4 (\"Undercoverage\"); Chapter 16, section 16.1 "
    "(\"Coverage Error\")."
)

_MEASUREMENT_CITATION = (
    "Cronbach, L.J. & Meehl, P.E. (1955), \"Construct Validity in Psychological "
    "Tests\", Psychological Bulletin 52(4):281-302, the nomological net "
    "discussion at page 290."
)

_MISSINGNESS_CITATION = (
    "Little, R.J.A. & Rubin, D.B. (2019), Statistical Analysis with Missing Data, "
    "3rd edition, Chapter 3 (\"Complete-Case and Available-Case Analysis, Including "
    "Weighting Methods\"), section 3.2; White, I.R. & Carlin, J.B. (2010), "
    "\"Bias and efficiency of multiple imputation compared with complete-case "
    "analysis for missing covariate values\", Statistics in Medicine 29(28):2920-2931, "
    "DOI 10.1002/sim.3944."
)

# The mechanism x implied-method pairing table (D-07). This is NOT a printed table
# from any source — research confirmed no such table appears in Little & Rubin's
# third edition. It is assembled from Chapter 3 section 3.2's stated conditions for
# complete-case and available-case analysis, plus White & Carlin (2010)'s documented
# sub-case in which complete-case analysis is unbiased under missing-at-random
# missingness (missingness independent of the outcome given the covariates).
# REQUIREMENTS.md's phrase "the Rubin MCAR/MAR/MNAR validity table" names the
# concept this table encodes, not a citable artifact — do not describe this table,
# in any docstring or comment, as reproducing a printed source.
#
# Per-method severity within a mechanism (D-05, REQ-P11.3-03): the value is
# (mode, methods, fallback_severity).
#   - mode "deny": `methods` is a {method: severity} mapping — the denied methods
#     under this mechanism, each keyed to its own severity, because the harm is not
#     uniform across denied methods. Complete-case / available-case under MAR only
#     sacrifice power while reporting honest uncertainty (HIGH); single imputation
#     treated as if observed additionally fabricates precision — it drops the
#     missing-data variance component (Rubin's B forced to 0), so its interval is
#     anti-conservative, a strictly-worse structural defect (CRITICAL). The
#     per-method keying is deliberate: a reversion to one-severity-per-mechanism
#     would let single imputation pass at HIGH. `fallback_severity` is the severity
#     for a denied method not individually keyed (defence in depth; every current
#     denied method is keyed).
#   - mode "allow": `methods` is a frozenset of the ONLY methods this mechanism
#     licenses; anything outside it is not licensed, at `fallback_severity`.
# missing_completely_at_random has no entry: it denies nothing, so it is handled
# by the absence of a key, not by an explicit empty deny set.
# not_assessed also has no entry — that absence is what makes the mechanism a
# skip: an author who has declared they have not evaluated the mechanism has not
# made the claim this check judges.
_MISSINGNESS_METHOD_VALIDITY: "dict[str, tuple[str, object, str]]" = {
    "mar": (
        "deny",
        {
            "complete_case": "HIGH",
            "available_case": "HIGH",
            "single_imputation": "CRITICAL",
        },
        "HIGH",
    ),
    "mnar": (
        "allow",
        frozenset({"mechanism_model", "selection_model", "pattern_mixture_model"}),
        "CRITICAL",
    ),
}


def check(spec: dict) -> Report:
    """Emit the validity-frame content findings (``DSX-VAL-*``).

    Reads ``validity_frame:`` and degrades to an empty report — never a
    traceback — when the block is absent or is not a dictionary (threat
    T-7-01: a malformed sub-block must not take the whole gate down). This is
    deliberately distinct from Phase 6's shape check: an absent block is
    already ``DSX-SPEC-080`` territory, so this function does not re-report
    it.

    Structural criterion: dispatches to one private helper per adjudicated
    concept; no numeric threshold, effect size or statistic is computed
    anywhere in this module (D-02).
    """
    report = Report(check="val")

    frame = get(spec, "validity_frame")
    if not isinstance(frame, dict):
        return report

    _check_estimand_completeness(frame, report)
    _check_estimand_falsifiability(frame, report)
    _check_unit_triad(spec, frame, report)
    _check_unit_drift(spec, frame, report)
    _check_dependence(frame, report)
    _check_identification(frame, report)
    _check_sampling_frame(frame, report)
    _check_missingness(frame, report)
    _check_measurement(frame, report)
    _check_exclusions(frame, report)

    estimand = frame.get("estimand")
    if isinstance(estimand, dict):
        blank_fields = [
            name for name in _ESTIMAND_REQUIRED_FIELDS if is_blank(estimand.get(name))
        ]
        discriminating = falsifier_is_discriminating(estimand.get("falsifier"))
        choice = (
            "estimand completeness: "
            + ("blocked" if blank_fields else "passed")
            + "; estimand falsifiability: "
            + ("passed" if discriminating else "blocked")
        )
        counterfactual = (
            "A declaration with quantity, population, contrast and time_window all "
            "present, and a falsifier naming a discriminating predicate or a numeric "
            "threshold, would have produced neither DSX-VAL-010 nor DSX-VAL-011."
        )
        report.context.setdefault("decisions", []).append(
            DecisionRecord(
                id="",
                invocation_id="",
                layer="deterministic",
                choice=choice,
                inputs=[
                    f"validity_frame.estimand.{name}"
                    for name in (*_ESTIMAND_REQUIRED_FIELDS, "falsifier")
                ],
                rule=(
                    "DSX-VAL-010 fires when any of quantity, population, contrast or "
                    "time_window is blank under is_blank(); DSX-VAL-011 fires when "
                    "falsifier_is_discriminating(falsifier) is False — blank, an "
                    "angle-bracket placeholder, a refusal token, or prose naming no "
                    "discriminating predicate and no numeric/percentage-point token."
                ),
                citation=_ESTIMAND_CITATION,
                counterfactual=counterfactual,
            ).to_dict()
        )

    units = frame.get("units")
    if isinstance(units, dict):
        observation = units.get("observation")
        assignment = units.get("assignment")
        dependence = frame.get("dependence")
        method_family = (
            dependence.get("method_family_required") if isinstance(dependence, dict) else None
        )
        triad_blocked = (
            not is_blank(observation)
            and not is_blank(assignment)
            and normalize(observation) != normalize(assignment)
            and is_blank(method_family)
        )
        report.context.setdefault("decisions", []).append(
            DecisionRecord(
                id="",
                invocation_id="",
                layer="deterministic",
                choice="unit triad: " + ("blocked" if triad_blocked else "passed"),
                inputs=[
                    "validity_frame.units.observation",
                    "validity_frame.units.assignment",
                    "validity_frame.dependence.method_family_required",
                ],
                rule=(
                    "DSX-VAL-020 fires when normalize(units.observation) != "
                    "normalize(units.assignment) and dependence.method_family_required is "
                    "blank under is_blank(); either unit being blank skips the comparison."
                ),
                citation=_UNIT_TRIAD_CITATION,
                counterfactual=(
                    "A spec where the observation unit equals the assignment unit, or "
                    "where dependence.method_family_required names an admissible method "
                    "family, would have produced no DSX-VAL-020."
                ),
            ).to_dict()
        )

        design = spec.get("design")
        design = design if isinstance(design, dict) else {}
        assignment_for_drift = units.get("assignment")
        analysis = units.get("analysis")
        randomization_unit = design.get("randomization_unit")
        design_analysis_unit = design.get("analysis_unit")
        drift_blocked = (
            not is_blank(assignment_for_drift)
            and not is_blank(randomization_unit)
            and normalize(assignment_for_drift) != normalize(randomization_unit)
        ) or (
            not is_blank(analysis)
            and not is_blank(design_analysis_unit)
            and normalize(analysis) != normalize(design_analysis_unit)
        )
        report.context.setdefault("decisions", []).append(
            DecisionRecord(
                id="",
                invocation_id="",
                layer="deterministic",
                choice="unit drift: " + ("blocked" if drift_blocked else "passed"),
                inputs=[
                    "validity_frame.units.assignment",
                    "design.randomization_unit",
                    "validity_frame.units.analysis",
                    "design.analysis_unit",
                ],
                rule=(
                    "DSX-VAL-021 fires once per disagreeing pair: "
                    "normalize(units.assignment) != normalize(design.randomization_unit), "
                    "or normalize(units.analysis) != normalize(design.analysis_unit); each "
                    "comparison is skipped unless both of its sides are non-blank."
                ),
                citation=_UNIT_DRIFT_CITATION,
                counterfactual=(
                    "A spec where the validity frame's assignment and analysis units "
                    "agree with design.randomization_unit and design.analysis_unit "
                    "respectively would have produced no DSX-VAL-021."
                ),
            ).to_dict()
        )

    dependence = frame.get("dependence")
    if isinstance(dependence, dict):
        structure = dependence.get("structure")
        method_family = dependence.get("method_family_required")
        normalized_structure = normalize(structure) if not is_blank(structure) else None
        dependence_blocked = (
            normalized_structure is not None
            and normalized_structure != "none"
            and normalized_structure in DEPENDENCE_ADMISSIBLE_METHODS
            and (
                is_blank(method_family)
                or normalize(method_family)
                not in DEPENDENCE_ADMISSIBLE_METHODS[normalized_structure]
            )
        )
        report.context.setdefault("decisions", []).append(
            DecisionRecord(
                id="",
                invocation_id="",
                layer="deterministic",
                choice="dependence: " + ("blocked" if dependence_blocked else "passed"),
                inputs=[
                    "validity_frame.dependence.structure",
                    "validity_frame.dependence.method_family_required",
                ],
                rule=(
                    "DSX-VAL-030 fires when dependence.structure names a member of "
                    "dsx.spec.DEPENDENCE_ADMISSIBLE_METHODS and "
                    "dependence.method_family_required is blank under is_blank() or "
                    "not a normalize()d member of that structure's admissible set; a "
                    "blank structure, structure 'none', or a structure outside the "
                    "closed vocabulary skips the check entirely."
                ),
                citation=_DEPENDENCE_CITATION,
                counterfactual=(
                    "A spec declaring an admissible method_family_required for its "
                    "declared dependence structure, or declaring no dependence "
                    "structure (structure 'none' or absent), would have produced no "
                    "DSX-VAL-030."
                ),
            ).to_dict()
        )

    identification = frame.get("identification")
    if isinstance(identification, dict):
        strength = identification.get("strength")
        constraint_source = identification.get("constraint_source")
        normalized_strength = normalize(strength) if not is_blank(strength) else None
        normalized_constraint = (
            normalize(constraint_source) if not is_blank(constraint_source) else None
        )
        weak_blocked = normalized_strength == "weak" and normalized_constraint == "none"
        strong_flagged = (
            normalized_strength == "strong"
            and normalized_constraint in _PARAMETER_SCALE_CONSTRAINT_SOURCES
        )
        if weak_blocked:
            choice = "identification: blocked (DSX-VAL-040 — weak with no constraint)"
        elif strong_flagged:
            choice = (
                "identification: flagged (DSX-VAL-041 — strong with a "
                "parameter-scale constraint)"
            )
        else:
            choice = "identification: passed"
        report.context.setdefault("decisions", []).append(
            DecisionRecord(
                id="",
                invocation_id="",
                layer="deterministic",
                choice=choice,
                inputs=[
                    "validity_frame.identification.strength",
                    "validity_frame.identification.constraint_source",
                ],
                rule=(
                    "DSX-VAL-040 fires when strength normalizes to 'weak' and "
                    "constraint_source normalizes to 'none'; DSX-VAL-041 fires when "
                    "strength normalizes to 'strong' and constraint_source "
                    "normalizes to a member of _PARAMETER_SCALE_CONSTRAINT_SOURCES; "
                    "a blank or out-of-vocabulary strength or constraint_source "
                    "skips the check entirely."
                ),
                citation=_IDENTIFICATION_CITATION,
                counterfactual=(
                    "A weak declaration naming a real constraint, or a strong "
                    "declaration with constraint_source none, would have produced "
                    "neither code."
                ),
            ).to_dict()
        )

    sampling_frame = frame.get("sampling_frame")
    if isinstance(sampling_frame, dict):
        claim_population = sampling_frame.get("claim_population")
        known_exclusions = sampling_frame.get("known_exclusions")
        selection_risk = sampling_frame.get("selection_risk")
        sampling_frame_blocked = is_blank(claim_population) or (
            not is_blank(known_exclusions) and is_blank(selection_risk)
        )
        report.context.setdefault("decisions", []).append(
            DecisionRecord(
                id="",
                invocation_id="",
                layer="deterministic",
                choice="sampling frame: " + ("blocked" if sampling_frame_blocked else "passed"),
                inputs=[
                    "validity_frame.sampling_frame.claim_population",
                    "validity_frame.sampling_frame.known_exclusions",
                    "validity_frame.sampling_frame.selection_risk",
                ],
                rule=(
                    "DSX-VAL-050 fires when claim_population is blank under "
                    "is_blank(), or when known_exclusions is a non-empty "
                    "collection and selection_risk is blank under is_blank(); "
                    "at most one finding per sub-block."
                ),
                citation=_SAMPLING_FRAME_CITATION,
                counterfactual=(
                    "A spec naming a non-blank claim_population, with a non-blank "
                    "selection_risk whenever known_exclusions is non-empty, would "
                    "have produced no DSX-VAL-050."
                ),
            ).to_dict()
        )

    missingness = frame.get("missingness")
    if isinstance(missingness, dict):
        mechanism = missingness.get("mechanism")
        method_implied = missingness.get("method_implied")
        normalized_mechanism = (
            normalize(mechanism)
            if not is_blank(mechanism)
            and normalize(mechanism) in {normalize(k) for k in MISSINGNESS_MECHANISMS}
            else None
        )
        entry = (
            _MISSINGNESS_METHOD_VALIDITY.get(normalized_mechanism)
            if normalized_mechanism is not None
            else None
        )
        if entry is not None:
            mode, methods, _severity = entry
            normalized_method = (
                normalize(method_implied) if not is_blank(method_implied) else None
            )
            if mode == "deny":
                missingness_blocked = normalized_method is not None and normalized_method in methods
            else:
                missingness_blocked = normalized_method is None or normalized_method not in methods
        else:
            missingness_blocked = False
        report.context.setdefault("decisions", []).append(
            DecisionRecord(
                id="",
                invocation_id="",
                layer="deterministic",
                choice="missingness: " + ("blocked" if missingness_blocked else "passed"),
                inputs=[
                    "validity_frame.missingness.mechanism",
                    "validity_frame.missingness.method_implied",
                ],
                rule=(
                    "DSX-VAL-060 fires when the normalize()d mechanism has an entry in "
                    "_MISSINGNESS_METHOD_VALIDITY and the normalize()d method_implied "
                    "fails that entry's pairing test; a blank or out-of-vocabulary "
                    "mechanism, or a mechanism with no table entry "
                    "(missing_completely_at_random or not_assessed), skips the check "
                    "entirely. The missingness.rate field is never read."
                ),
                citation=_MISSINGNESS_CITATION,
                counterfactual=(
                    "A missing-at-random mechanism paired with a method other than "
                    "complete-case or available-case analysis, or a missing-not-at-random "
                    "mechanism paired with an explicit mechanism model, would have "
                    "produced no DSX-VAL-060."
                ),
            ).to_dict()
        )

    measurement = frame.get("measurement")
    if isinstance(measurement, dict):
        construct = measurement.get("construct")
        operationalisation = measurement.get("operationalisation")
        measurement_blocked = not is_blank(construct) and is_blank(operationalisation)
        report.context.setdefault("decisions", []).append(
            DecisionRecord(
                id="",
                invocation_id="",
                layer="deterministic",
                choice="measurement: " + ("blocked" if measurement_blocked else "passed"),
                inputs=[
                    "validity_frame.measurement.construct",
                    "validity_frame.measurement.operationalisation",
                ],
                rule=(
                    "DSX-VAL-070 fires when construct is non-blank under "
                    "is_blank() and operationalisation is blank under is_blank()."
                ),
                citation=_MEASUREMENT_CITATION,
                counterfactual=(
                    "A spec declaring an operationalisation whenever a construct "
                    "is declared would have produced no DSX-VAL-070."
                ),
            ).to_dict()
        )

    return report


def _check_estimand_completeness(frame: dict, report: Report) -> None:
    """Emit DSX-VAL-010 when a required estimand attribute is blank.

    Citation: International Council for Harmonisation (ICH) (2019), E9(R1)
    Addendum, EMA/CHMP/ICH/436221/2017, Step 5, section A.3.3 ("Estimand
    attributes") and section A.3.2; Hernan, M.A. & Robins, J.M. (2016),
    American Journal of Epidemiology 183(8):758-764, Table 1; Hernan, M.A. &
    Robins, J.M. (2020), Causal Inference: What If, Chapter 1, section 1.2
    ("Average causal effects").

    Honesty disclosure (D-05's whole point): the five-field estimand
    decomposition this module uses (quantity, population, contrast,
    time_window, falsifier) is project-defined. The addendum and Hernan and
    Robins (2016) each name four of the five attributes checked here, but
    neither treats ``falsifier`` as an estimand attribute at all, and
    ``time_window`` appears in the addendum as a sub-specification of the
    estimand rather than as one of its named attributes. No cited source
    states this five-field decomposition as written; it is this project's own
    grouping, adopted for decidability, not asserted as a published result.

    Structural criterion: presence (non-blank, per ``is_blank()``) of the
    four required sub-fields quantity, population, contrast and time_window.
    ``falsifier`` is intentionally excluded from this criterion — it is
    adjudicated separately by ``_check_estimand_falsifiability`` (DSX-VAL-011)
    so a blank falsifier fires exactly one code, not two.
    """
    estimand = frame.get("estimand")
    if not isinstance(estimand, dict):
        return

    blank_fields = [
        name for name in _ESTIMAND_REQUIRED_FIELDS if is_blank(estimand.get(name))
    ]
    if not blank_fields:
        return

    detail = (
        "Blank estimand attribute(s): "
        + ", ".join(blank_fields)
        + ". A blank falsifier is not counted here — see DSX-VAL-011."
    )
    remedy = (
        "Name all four attributes: quantity (the difference, rate or quantity being "
        "estimated, e.g. 'difference in 7-day activation rate'), population (who the "
        "estimate covers, e.g. 'new non-bot signups, 2026-06-01 to 2026-06-14'), "
        "contrast (what is being compared, e.g. 'onboarding checklist vs current "
        "onboarding'), and time_window (the period over which the effect is measured, "
        "e.g. '7 days from signup')."
    )
    report.add(
        "DSX-VAL-010",
        "CRITICAL",
        "estimand is missing required attribute(s)",
        detail=detail,
        remedy=remedy,
        where="spec.validity_frame.estimand",
    )


def _check_estimand_falsifiability(frame: dict, report: Report) -> None:
    """Emit DSX-VAL-011 when the estimand's falsifier does not discriminate.

    Citation: Popper, K.R. (1959/2002 reissue), The Logic of Scientific
    Discovery, Part I, Chapter 1, section 6 ("Falsifiability as a Criterion
    of Demarcation"), pages 17-18.
    Structural criterion: the falsifier must name at least one observable
    outcome under which the claim is withdrawn — tested via
    ``falsifier_is_discriminating()``, which requires a comparison predicate
    (``FALSIFIER_DISCRIMINATORS``) or a numeric/percentage-point token, and
    is False for a blank, angle-bracket-placeholder or refusal-token value.
    """
    estimand = frame.get("estimand")
    if not isinstance(estimand, dict):
        return

    falsifier = estimand.get("falsifier")
    if falsifier_is_discriminating(falsifier):
        return

    if is_placeholder_or_refusal(falsifier):
        detail = (
            f"falsifier {falsifier!r} is blank, an angle-bracket placeholder, or a "
            "refusal token — no honest falsifier was declared."
        )
    else:
        detail = (
            f"falsifier {falsifier!r} is present but names no discriminating predicate "
            "(e.g. 'includes zero', 'crosses', 'below', 'above', 'exceeds') and no "
            "numeric or percentage-point threshold."
        )
    remedy = (
        "Name at least one observable outcome under which the claim would be "
        "withdrawn — a discriminating predicate plus a numeric threshold, in the "
        "shape of the good fixture's falsifier: '95% CI on the activation uplift "
        "includes zero, or its lower bound sits below +1.0pp'."
    )
    report.add(
        "DSX-VAL-011",
        "HIGH",
        "estimand falsifier does not discriminate",
        detail=detail,
        remedy=remedy,
        where="spec.validity_frame.estimand.falsifier",
    )


def _check_unit_triad(spec: dict, frame: dict, report: Report) -> None:
    """Emit DSX-VAL-020 when the observation unit is finer than the
    assignment unit and no method family accounts for the resulting
    dependence.

    Citation: Kish, L. (1965), Survey Sampling, section 8.2, page 258
    (design-effect definition) and pages 161-162 (intraclass correlation);
    Higgins, J.P.T., Eldridge, S. and Li, T. (2024), Cochrane Handbook for
    Systematic Reviews of Interventions version 6.5, sections 23.1.4 and
    23.1.4.1. Section 8.2 was confirmed for the design-effect definition; no
    section number was confirmed for the design-effect formula itself, and
    that locator is UNVERIFIED — do not invent one.

    The number this function prints (the Cochrane Handbook's own worked
    example: an intraclass correlation of 0.02 and an average cluster size of
    29.8 yielding 1.576) is a fixed illustration, never a figure computed
    from this spec. The contract carries no cluster-size field and no
    intraclass-correlation field anywhere (D-11), and D-02 forbids computing
    a statistic on the gate path in any case — the gate has nothing to
    compute from even if it wanted to.

    Structural criterion: normalize(units.observation) != normalize(units.assignment)
    (D-08 — plain string inequality, deliberate: the units fields carry no
    closed, orderable vocabulary in this contract, so an ordering that could
    rank one unit finer than another would have to be invented) with
    dependence.method_family_required blank under is_blank(). Either unit
    being blank skips the comparison entirely — a blank unit is Phase 6's
    shape territory, not this check's.

    Known risk, accepted (D-08): a spec naming the same unit two ways (e.g.
    'user' vs 'user_id') fires this at CRITICAL on a naming inconsistency,
    not a true dependence defect. The remedy names both ways out so an
    author hitting this can tell which one applies.
    """
    units = frame.get("units")
    if not isinstance(units, dict):
        return

    observation = units.get("observation")
    assignment = units.get("assignment")
    if is_blank(observation) or is_blank(assignment):
        return
    if normalize(observation) == normalize(assignment):
        return

    dependence = frame.get("dependence")
    method_family = (
        dependence.get("method_family_required") if isinstance(dependence, dict) else None
    )
    if not is_blank(method_family):
        return

    deff = design_effect(_UNIT_TRIAD_M, _UNIT_TRIAD_ICC)
    detail = (
        f"observation unit {observation!r} is finer than assignment unit {assignment!r}, "
        "with no validity_frame.dependence.method_family_required declared. Observations "
        "sharing an assignment unit are correlated with one another; treating the finer "
        "observation unit as independent understates variance. The design effect "
        "DEFF = 1 + (m - 1) x ICC quantifies the inflation: an intraclass correlation of "
        f"{_UNIT_TRIAD_ICC} and an average cluster size of {_UNIT_TRIAD_M} yield "
        f"DEFF = {deff:g} (dsx.mathx.design_effect({_UNIT_TRIAD_M}, {_UNIT_TRIAD_ICC})), "
        "so the true standard error is roughly sqrt(DEFF) times the naive one and an "
        "interval computed at the naive standard error is too narrow by that same factor. "
        "This number is a fixed illustration from the Cochrane Handbook's own published "
        "worked example — it is not computed from this spec. The contract carries no "
        "cluster-size or intraclass-correlation field anywhere, so there is nothing here "
        "to compute your own design effect from."
    )
    remedy = (
        "Either align the two unit names if they denote the same thing — a naming "
        f"inconsistency between {observation!r} and {assignment!r} (e.g. 'user' vs "
        "'user_id') also fires this finding — or declare "
        "validity_frame.dependence.method_family_required (cluster_robust, delta_method, "
        "bootstrap_cluster, or mixed_effects) to account for the dependence between them."
    )
    report.add(
        "DSX-VAL-020",
        "CRITICAL",
        "observation unit finer than assignment unit with no method family declared",
        detail=detail,
        remedy=remedy,
        where="spec.validity_frame.units",
    )


def _check_unit_drift(spec: dict, frame: dict, report: Report) -> None:
    """Emit DSX-VAL-021 when the validity frame's own unit declarations
    disagree with ``design:``'s.

    Citation: Hernan, M.A. & Robins, J.M. (2020), Causal Inference: What If,
    Chapter 1, section 1.2 ("Average causal effects") — the unit a claim is
    made about must be fixed before the claim is made.

    Structural criterion: string agreement (after ``normalize()``) between
    two declarations of the same unit across two blocks — no ordering, no
    ranking, no judgment of whether a mismatch is handled. Two comparisons,
    and nothing else: ``validity_frame.units.assignment`` against
    ``design.randomization_unit``, and ``validity_frame.units.analysis``
    against ``design.analysis_unit``. Each comparison is skipped unless both
    of its sides are non-blank — there is nothing to disagree with when one
    side is undeclared.

    This is pure agreement detection between two blocks (D-09), and that is
    the whole of its job. It does not assess whether a mismatch is handled —
    that judgment belongs to ``DSX-EXP-021`` (``dsx/checks/design.py``) for
    the design block's own randomization/analysis pair, and to
    ``DSX-VAL-020`` for the validity frame's own observation/assignment
    pair. No suppression logic connects this check to either of those —
    the disjointness is achieved by reading disjoint field pairs, not by one
    check silencing another.
    """
    units = frame.get("units")
    if not isinstance(units, dict):
        return

    design = spec.get("design")
    design = design if isinstance(design, dict) else {}

    assignment = units.get("assignment")
    randomization_unit = design.get("randomization_unit")
    if (
        not is_blank(assignment)
        and not is_blank(randomization_unit)
        and normalize(assignment) != normalize(randomization_unit)
    ):
        report.add(
            "DSX-VAL-021",
            "HIGH",
            "validity frame assignment unit disagrees with design randomization unit",
            detail=(
                f"validity_frame.units.assignment is {assignment!r}, but "
                f"design.randomization_unit is {randomization_unit!r} — the two "
                "declarations of the assignment unit disagree."
            ),
            remedy=(
                "Align validity_frame.units.assignment and design.randomization_unit to "
                "name the same unit; this check cannot know which declaration is right."
            ),
            where="spec.validity_frame.units.assignment",
        )

    analysis = units.get("analysis")
    design_analysis_unit = design.get("analysis_unit")
    if (
        not is_blank(analysis)
        and not is_blank(design_analysis_unit)
        and normalize(analysis) != normalize(design_analysis_unit)
    ):
        report.add(
            "DSX-VAL-021",
            "HIGH",
            "validity frame analysis unit disagrees with design analysis unit",
            detail=(
                f"validity_frame.units.analysis is {analysis!r}, but "
                f"design.analysis_unit is {design_analysis_unit!r} — the two "
                "declarations of the analysis unit disagree."
            ),
            remedy=(
                "Align validity_frame.units.analysis and design.analysis_unit to name "
                "the same unit; this check cannot know which declaration is right."
            ),
            where="spec.validity_frame.units.analysis",
        )


def _check_dependence(frame: dict, report: Report) -> None:
    """Emit DSX-VAL-030 when a declared dependence structure has no admissible
    method family accounting for it.

    Citation: Cameron, A.C. & Miller, D.L. (2015), "A Practitioner's Guide to
    Cluster-Robust Inference", Journal of Human Resources 50(2):317-372, for
    the clustered, repeated_measures, temporal and spatial pairings; Gelman,
    A. & Hill, J. (2007), Data Analysis Using Regression and
    Multilevel/Hierarchical Models, Cambridge University Press, for the
    hierarchical pairing. The exact section locator inside Cameron and Miller
    and the exact chapter locator inside Gelman and Hill are both UNVERIFIED —
    author, year, title and venue were confirmed for each; the internal
    locators were not. Do not invent either.

    Structural criterion: membership of the declared, normalize()d method
    family in dsx.spec.DEPENDENCE_ADMISSIBLE_METHODS[structure], the
    admissible set for the declared, normalize()d dependence structure.

    A blank structure, a structure that normalizes to 'none' (a declared
    independence — the nothing-to-validate case, not a defect), or a
    structure outside the closed vocabulary (DSX-SPEC-082's territory — a
    shape defect, not this check's) are all skipped without emitting, so one
    defect never earns two codes.
    """
    dependence = frame.get("dependence")
    if not isinstance(dependence, dict):
        return

    structure = dependence.get("structure")
    if is_blank(structure):
        return

    normalized_structure = normalize(structure)
    if normalized_structure == "none":
        return
    if normalized_structure not in DEPENDENCE_ADMISSIBLE_METHODS:
        return

    admissible = DEPENDENCE_ADMISSIBLE_METHODS[normalized_structure]
    admissible_listed = ", ".join(sorted(admissible))
    method_family = dependence.get("method_family_required")

    if is_blank(method_family):
        detail = (
            f"dependence.structure is {structure!r}, but no "
            "dependence.method_family_required was declared. Admissible method "
            f"families for {structure!r}: {admissible_listed}."
        )
    elif normalize(method_family) not in admissible:
        detail = (
            f"dependence.structure is {structure!r}, but the declared "
            f"dependence.method_family_required {method_family!r} does not address "
            f"it. Admissible method families for {structure!r}: {admissible_listed}."
        )
    else:
        return

    remedy = (
        "Declare validity_frame.dependence.method_family_required as one of "
        f"{admissible_listed} to account for the dependence introduced by the "
        f"{structure!r} structure."
    )
    report.add(
        "DSX-VAL-030",
        "CRITICAL",
        "dependence structure declared with no admissible method family",
        detail=detail,
        remedy=remedy,
        where="spec.validity_frame.dependence",
    )


def _check_identification(frame: dict, report: Report) -> None:
    """Emit DSX-VAL-040 when weak identification names no constraint at all,
    and DSX-VAL-041 when strong identification also carries a constraint that
    informs the parameter's scale.

    Citation: Gelman, A., Simpson, D. & Betancourt, M. (2017), "The Prior Can
    Often Only Be Understood in the Context of the Likelihood", Entropy
    19(10), article 555, section 3.3 ("For complex models, certain aspects of
    the prior will always be relevant") and section 1.2 ("Existing methods
    for setting priors already depend on the likelihood"). Whether the
    typeset MDPI journal version uses the same section numbers as the arXiv
    final version is UNVERIFIED — cited by section number and title together
    so the locator survives either.

    Honesty disclosure (D-05's whole point): no published source partitions
    CONSTRAINT_SOURCES into members that carry parameter-scale information
    and members that do not. Gelman, Simpson & Betancourt support the
    underlying premise, and their section 1.2 gives a prior taxonomy that
    lines up with two of the four members classified here (structural priors
    -> hierarchical_pooling; regularizing priors -> penalisation), but they
    publish no such partition, and design_restriction has no counterpart in
    their paper at all. This partition is project-defined.

    Structural criterion: membership test against a project-defined partition
    of the constraint-source vocabulary —
    _PARAMETER_SCALE_CONSTRAINT_SOURCES, derived from each member's own
    description text in dsx.spec.CONSTRAINT_SOURCES, not from any published
    source. This partition is project-defined; repeating the disclosure here
    so it survives being read in isolation from the paragraph above.

    A blank strength or constraint_source, or either value outside its closed
    vocabulary, is skipped without emitting — DSX-SPEC-082's territory, not
    this check's. The two codes are mutually exclusive by construction: one
    requires strength 'weak', the other strength 'strong'.
    """
    identification = frame.get("identification")
    if not isinstance(identification, dict):
        return

    strength = identification.get("strength")
    constraint_source = identification.get("constraint_source")
    if is_blank(strength) or is_blank(constraint_source):
        return

    normalized_strength = normalize(strength)
    normalized_constraint = normalize(constraint_source)
    if normalized_strength not in IDENTIFICATION_STRENGTHS:
        return
    if normalized_constraint not in CONSTRAINT_SOURCES:
        return

    if normalized_strength == "weak" and normalized_constraint == "none":
        detail = (
            f"identification.strength is {strength!r} with "
            f"identification.constraint_source {constraint_source!r} — an "
            "identification strategy resting on covariate adjustment with no "
            "design-based support and no external constraint gives an estimate "
            "nothing anchors."
        )
        remedy = (
            "Name the constraint that is actually doing the work "
            "(informative_priors, penalisation, design_restriction or "
            "hierarchical_pooling), or restate identification.strength honestly if "
            "no such constraint applies."
        )
        report.add(
            "DSX-VAL-040",
            "CRITICAL",
            "weak identification declared with no constraint",
            detail=detail,
            remedy=remedy,
            where="spec.validity_frame.identification",
        )
        return

    if (
        normalized_strength == "strong"
        and normalized_constraint in _PARAMETER_SCALE_CONSTRAINT_SOURCES
    ):
        detail = (
            f"identification.strength is {strength!r} — a design described as "
            f"ruling out confounding — but identification.constraint_source is "
            f"{constraint_source!r}, which also informs the parameter's scale. "
            "The two declarations are in tension. This is a prompt to reconcile "
            "them, not an assertion that the analysis is wrong — the severity is "
            "high rather than critical precisely because it may be neither."
        )
        remedy = (
            "Say which declaration is load-bearing: if the design alone "
            "identifies the effect, consider whether constraint_source should be "
            f"none; if the {constraint_source!r} constraint is doing real work, "
            "consider whether strength is better stated as moderate."
        )
        report.add(
            "DSX-VAL-041",
            "HIGH",
            "strong identification also carries a parameter-scale constraint",
            detail=detail,
            remedy=remedy,
            where="spec.validity_frame.identification",
        )


def _check_sampling_frame(frame: dict, report: Report) -> None:
    """Emit DSX-VAL-050 when the sampling frame's claim population is blank,
    or when a declared known exclusion has no accompanying selection-risk
    assessment.

    Citation: Lohr, S.L. (2021), Sampling: Design and Analysis, 3rd edition,
    Chapter 1, sections 1.2, 1.3 and 1.3.4 ("Undercoverage"); Chapter 16,
    section 16.1 ("Coverage Error").

    Structural criterion: presence and internal consistency between the
    declared exclusions and the declared selection risk — not a comparison
    of the frame against the claim population. D-06 defers that comparison:
    the good fixture declares a source with no region filter against a
    claim population naming no region, with a selection risk of "none
    identified", and any rule strong enough to catch a frame that quietly
    excludes part of its claim population would also fail that fixture,
    which must pass at every threshold.

    Uses is_blank() only, never is_placeholder_or_refusal() — this is
    load-bearing, not incidental (D-06). The template's claim_population is
    an angle-bracket placeholder and no decision authorises changing it; a
    placeholder-aware check here would trip the template and widen the
    repair list beyond what any decision covers. This check emits at most
    one finding per sub-block, so an author with both problems is not told
    the same thing twice.
    """
    sampling_frame = frame.get("sampling_frame")
    if not isinstance(sampling_frame, dict):
        return

    claim_population = sampling_frame.get("claim_population")
    known_exclusions = sampling_frame.get("known_exclusions")
    selection_risk = sampling_frame.get("selection_risk")

    if is_blank(claim_population):
        detail = (
            "sampling_frame.claim_population is blank — no population is named "
            "for the frame to be judged against."
        )
        where = "spec.validity_frame.sampling_frame.claim_population"
    elif not is_blank(known_exclusions) and is_blank(selection_risk):
        detail = (
            f"sampling_frame.known_exclusions names {known_exclusions!r}, but "
            "sampling_frame.selection_risk is blank — an exclusion nobody has "
            "assessed is a coverage gap nobody has assessed."
        )
        where = "spec.validity_frame.sampling_frame.selection_risk"
    else:
        return

    remedy = (
        "Name the population the claim will be made about in claim_population; "
        "whenever known_exclusions is non-empty, also state selection_risk — how "
        "the excluded rows could make the sample differ systematically from the "
        "claim population, or 'none identified' if the risk was assessed and "
        "found negligible."
    )
    report.add(
        "DSX-VAL-050",
        "HIGH",
        "sampling frame is not internally consistent",
        detail=detail,
        remedy=remedy,
        where=where,
    )


def _check_missingness(frame: dict, report: Report) -> None:
    """Emit DSX-VAL-060 when a declared missingness mechanism is paired with
    an implied method the mechanism does not license.

    Citation: Little, R.J.A. & Rubin, D.B. (2019), Statistical Analysis with
    Missing Data, 3rd edition, Chapter 3 ("Complete-Case and Available-Case
    Analysis, Including Weighting Methods"), section 3.2; White, I.R. &
    Carlin, J.B. (2010), "Bias and efficiency of multiple imputation compared
    with complete-case analysis for missing covariate values", Statistics in
    Medicine 29(28):2920-2931, DOI 10.1002/sim.3944.

    D-05/D-06 severity split: single imputation treated as if observed under a
    MAR mechanism fires at CRITICAL (not HIGH), carrying its OWN citation —
    Rubin, D.B. (1987), Multiple Imputation for Nonresponse in Surveys, §3.1,
    the total-variance decomposition T = W̄ + (1+1/m)·B. Single imputation
    forces the between-imputation term B to zero, understating variance in the
    anti-conservative direction; that standard-error fabrication is a strictly
    worse defect than the complete-case power sacrifice White & Carlin (2010)
    describe, so it does NOT reuse the White & Carlin remedy.

    Honesty disclosure (D-05's whole point): the (mechanism, method) pairing
    tested here — ``_MISSINGNESS_METHOD_VALIDITY`` — is not a printed table
    from either cited source; it is assembled from Chapter 3 section 3.2's
    stated conditions plus White & Carlin's documented sub-case in which
    complete-case analysis is unbiased under missing-at-random missingness
    (missingness independent of the outcome given the covariates). No such
    table appears in Little & Rubin's third edition. "The Rubin MCAR/MAR/MNAR
    validity table" names the concept this table encodes, not a citable
    artifact — do not describe this table, in any docstring or comment, as
    reproducing a printed source.

    Structural criterion: membership of the declared (mechanism, method) pair
    against the project-assembled table _MISSINGNESS_METHOD_VALIDITY, keyed
    by the normalize()d mechanism — the table is assembled from the cited
    conditions rather than reproduced from a printed table. A blank
    mechanism, a mechanism outside the closed vocabulary (DSX-SPEC-082's
    territory), or a mechanism with no entry in the table
    (missing_completely_at_random, which denies nothing, or not_assessed, an
    honestly declared absence of evaluation) are all skipped without
    emitting. The missingness.rate field is never read by this check — not to
    exempt, not to soften a severity, not to add to the detail text — because
    a rate of zero must not become the cheapest way past it.
    """
    missingness = frame.get("missingness")
    if not isinstance(missingness, dict):
        return

    mechanism = missingness.get("mechanism")
    if is_blank(mechanism):
        return

    normalized_mechanism = normalize(mechanism)
    if normalized_mechanism not in {normalize(k) for k in MISSINGNESS_MECHANISMS}:
        return

    entry = _MISSINGNESS_METHOD_VALIDITY.get(normalized_mechanism)
    if entry is None:
        return

    mode, methods, fallback_severity = entry
    method_implied = missingness.get("method_implied")
    normalized_method = normalize(method_implied) if not is_blank(method_implied) else None

    if mode == "deny":
        valid = normalized_method is None or normalized_method not in methods
    else:
        valid = normalized_method is not None and normalized_method in methods

    if valid:
        return

    # Resolve the emit severity. Under a deny mechanism the harm is per method:
    # `methods` maps each denied method to its own severity (D-05, REQ-P11.3-03), so
    # single_imputation resolves to CRITICAL while complete_case/available_case resolve
    # to HIGH. Under an allow mechanism every unlicensed method is the fallback severity.
    if mode == "deny":
        emit_severity = methods.get(normalized_method, fallback_severity)
    else:
        emit_severity = fallback_severity

    detail = (
        f"missingness.mechanism is {mechanism!r}, but missingness.method_implied is "
        f"{method_implied!r} — a pairing this project-assembled table does not license."
    )
    # Severity is written as a literal string in each branch, not passed through as the
    # `emit_severity` variable, because scripts/gen-finding-catalogue.py's AST-based
    # catalogue extractor (`extract()`) only recognises a `report.add(CODE, SEVERITY,
    # TITLE, ...)` call whose second argument is itself a string literal — a variable
    # there would make DSX-VAL-060 invisible to the generated catalogue (D-16). All three
    # branches reuse the identical title and, for the two CRITICAL branches, the identical
    # "CRITICAL" literal, so the rendered catalogue row and the _CANONICAL_DECLARATIONS
    # pin do not drift — only remedy/detail differ (D-06).
    if mode == "deny" and emit_severity == "HIGH":
        remedy = (
            "White & Carlin (2010) document a real sub-case in which complete-case "
            "analysis is unbiased under a missing-at-random mechanism: when missingness "
            "is independent of the outcome given the covariates in the analysis model. "
            "If that sub-case genuinely applies here, say so explicitly in the spec's "
            "documentation; otherwise declare a method_implied this mechanism licenses, "
            "such as multiple imputation."
        )
        report.add(
            "DSX-VAL-060",
            "HIGH",
            "missingness mechanism paired with a method it does not license",
            detail=detail,
            remedy=remedy,
            where="spec.validity_frame.missingness",
        )
    elif mode == "deny" and emit_severity == "CRITICAL":
        # Single imputation treated as if observed under MAR (D-05, D-06): unlike
        # complete/available-case — which only sacrifice power while reporting honest
        # uncertainty — single imputation fabricates precision. It sets n to the full
        # sample and drops the missing-data variance component, producing an
        # anti-conservative interval: a structural defect no downstream evidence rescues,
        # which is why it blocks at plan (CRITICAL), not HIGH. Its own citation is Rubin
        # (1987) §3.1, NOT the White & Carlin (2010) complete-case sub-case above.
        remedy = (
            "Single imputation treated as if observed fabricates precision: it fixes n "
            "at the full sample and drops the missing-data variance component, so the "
            "reported interval is anti-conservative. Rubin (1987), Multiple Imputation "
            "for Nonresponse in Surveys, §3.1 decomposes the total variance as "
            "T = W̄ + (1+1/m)·B — within- plus between-imputation variance — and single "
            "imputation forces the between-imputation term B to zero. Declare "
            "method_implied as multiple_imputation, or another method that explicitly "
            "propagates the missing-data variance, instead of a single fill treated as "
            "observed."
        )
        report.add(
            "DSX-VAL-060",
            "CRITICAL",
            "missingness mechanism paired with a method it does not license",
            detail=detail,
            remedy=remedy,
            where="spec.validity_frame.missingness",
        )
    else:
        remedy = (
            "A mechanism that depends on the unobserved value itself licenses no "
            "standard method without an explicit model of that mechanism — declare "
            "method_implied as mechanism_model, selection_model or "
            "pattern_mixture_model, or reconsider whether the mechanism is actually "
            "missing_not_at_random."
        )
        report.add(
            "DSX-VAL-060",
            "CRITICAL",
            "missingness mechanism paired with a method it does not license",
            detail=detail,
            remedy=remedy,
            where="spec.validity_frame.missingness",
        )


# Unadjudicated (D-06, REQ-P7-08's second clause): a measurement whose known
# gaps contradict the claim population is not adjudicated by this check, or
# by any check in this phase. This is decision D-06's text-comparison
# deferral rather than an oversight, and the known-gaps field is therefore
# read by no check in this phase.
def _check_measurement(frame: dict, report: Report) -> None:
    """Emit DSX-VAL-070 when a declared construct has no operationalisation
    naming an observable.

    Citation: Cronbach, L.J. & Meehl, P.E. (1955), "Construct Validity in
    Psychological Tests", Psychological Bulletin 52(4):281-302, the
    nomological net discussion at page 290.

    Structural criterion: a construct with no operationalisation naming an
    observable is rejected. Uses is_blank() only, never
    is_placeholder_or_refusal() — the template's construct and
    operationalisation are both angle-bracket placeholders and this check
    must not trip them (D-06), the same asymmetry _check_sampling_frame
    documents. A blank construct produces no finding whatever the
    operationalisation says — there is nothing to demand an operationalisation
    for, and an absent construct is Phase 6's DSX-SPEC-081 territory.
    """
    measurement = frame.get("measurement")
    if not isinstance(measurement, dict):
        return

    construct = measurement.get("construct")
    operationalisation = measurement.get("operationalisation")
    if is_blank(construct) or not is_blank(operationalisation):
        return

    detail = (
        f"measurement.construct is {construct!r}, but measurement.operationalisation "
        "is blank — the construct names a concept but no rule turns it into a number."
    )
    remedy = (
        "A construct is scientifically admissible only if it occurs in a network of "
        "laws at least some of which involve observables (Cronbach & Meehl, 1955, "
        f"p. 290) — name the exact rule that turns {construct!r} into a number, e.g. "
        "'>=1 key action within 7 days of signup'."
    )
    report.add(
        "DSX-VAL-070",
        "HIGH",
        "measurement construct declared with no operationalisation",
        detail=detail,
        remedy=remedy,
        where="spec.validity_frame.measurement.operationalisation",
    )


def _check_exclusions(frame: dict, report: Report) -> None:
    """Emit DSX-VAL-080 when a declared row-exclusion rule carries no
    justification.

    Citation: Simmons, J.P., Nelson, L.D. & Simonsohn, U. (2011),
    "False-Positive Psychology: Undisclosed Flexibility in Data Collection and
    Analysis Allows Presenting Anything as Significant", Psychological Science
    22(11):1359-1366, DOI 10.1177/0956797611417632 — data exclusion is named
    there as a researcher degree of freedom whose rule and rationale must be
    disclosed. Author, year, title, venue and DOI were confirmed; the exact
    requirement-number and table locator inside the paper are UNVERIFIED — do
    not invent one.

    Structural criterion: a declared row-exclusion rule must carry a
    justification. For each entry whose ``rule`` is non-blank under
    ``is_blank()``, ``justification`` must also be non-blank; nothing else in
    the entry is judged here. This is not the Lohr sampling-frame criterion
    (``_check_sampling_frame``, DSX-VAL-050) nor the White & Carlin missingness
    one (``_check_missingness``, DSX-VAL-060) — a distinct concept with its own
    source.

    The ``exclusions`` sub-block is accepted as EITHER a single rule-dict OR a
    list of rule-dicts (RESEARCH Open Question 1, planner decision); both shapes
    normalise to a list of entries and iterate. A value that is neither a dict
    nor a list degrades to no finding (threat T-11.3-10: a malformed sub-block
    must not take the whole gate down), the same presence-guard shape
    ``_check_sampling_frame`` uses.

    ``applied_before_split`` is RECORD-ONLY in 11.3 (D-10): no branch below
    reads its value. Whether an exclusion was applied before or after the
    train/test split is recorded for the reader, but the firing post-split
    check is a distinct, deferred concept with its own future code — this check
    never branches on ``applied_before_split``. Because ``exclusions`` lives
    UNDER ``validity_frame``, ``dsx.decisions.frame_digest`` already hashes it,
    so a changed cutoff or a flipped ``applied_before_split`` after results
    exist is caught by the existing DSX-PRE-020 content lock with no new
    machinery here (proven by ``tests/test_frame_prereg.py``'s
    ``TestExclusionsContentLock``).
    """
    exclusions = frame.get("exclusions")
    if not isinstance(exclusions, (dict, list)):
        return

    entries = exclusions if isinstance(exclusions, list) else [exclusions]
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        rule = entry.get("rule")
        justification = entry.get("justification")
        if is_blank(rule) or not is_blank(justification):
            continue
        detail = (
            f"exclusions rule {rule!r} is declared with no justification — a "
            "row-exclusion rule with no stated rationale is an undisclosed "
            "researcher degree of freedom."
        )
        remedy = (
            "State why these rows are excluded in the entry's justification: "
            "what the rule removes and why removing it is defensible for the "
            "claim population, not merely convenient for the result. "
            "applied_before_split is recorded but not judged here — a post-split "
            "exclusion is a separate, deferred concern."
        )
        report.add(
            "DSX-VAL-080",
            "HIGH",
            "exclusion rule declared without a justification",
            detail=detail,
            remedy=remedy,
            where="spec.validity_frame.exclusions",
        )
