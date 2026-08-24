"""Claim discipline. Codes DSX-CLM-*.

The last mile of an analysis is language, and language is where rigour is
usually lost: an association gets written up as a cause, a sample result gets
generalised to a population that was never sampled, an estimate gets quoted to
four significant figures on the strength of an interval two orders of magnitude
wide. These checks read the claims and hold them to the evidence the spec
actually declares.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

from ..findings import Report
from ..pct_base import relative_percent_without_base
from ..spec import (
    IDENTIFICATION_STRATEGIES,
    as_number,
    causal_verb_matches,
    get,
    is_blank,
    items,
    normalize,
    section,
)

HEDGE_TERMS = (
    "associated with", "correlated with", "suggests", "consistent with", "may",
    "might", "appears to", "is linked to", "under the assumption", "conditional on",
    "we estimate", "indicative of",
)

GENERALISATION_TERMS = (
    "all users", "every customer", "everyone", "the market", "always", "universally",
    "in general", "across the board", "all segments",
)

_NUMBER_RE = re.compile(r"(\d+\.\d+|\d+)\s*(%|pp|percentage points)?")


def check(
    spec: dict,
    phase_dir: "str | None" = None,
    *,
    strict: bool = False,
) -> Report:
    report = Report(check="claims")
    claims = items(spec, "claims")
    if not claims:
        report.add(
            "DSX-CLM-001",
            "HIGH",
            "No claims declared",
            detail=(
                "The claims block is the list of statements the deliverable will make. "
                "Without it there is nothing to hold to the evidence."
            ),
            remedy="Declare each headline statement with a type and an evidence pointer.",
            where="spec.claims",
        )
        return report

    design = section(spec, "design")
    strategy = normalize(design.get("identification", "")) if design.get("identification") else ""
    if normalize(design.get("kind", "")) == "experiment" and not strategy:
        strategy = "randomized_experiment"
    strength = IDENTIFICATION_STRATEGIES.get(strategy, {}).get("strength", "none")
    roots = _resolve_roots(phase_dir)
    results = section(spec, "results")
    raw_tests = results.get("tests") if results else None
    tests = raw_tests if isinstance(raw_tests, list) else []

    for index, claim in enumerate(claims):
        where = f"spec.claims[{index}]"
        text = str(claim.get("text", ""))
        ctype = normalize(claim.get("type", ""))
        _check_causal_language(claim, text, ctype, where, report)
        _check_causal_support(claim, ctype, strategy, strength, where, report)
        _check_evidence_pointer(claim, where, report, roots)
        _check_numeric_overlap(claim, text, tests, where, report)
        _check_predictive_support(claim, ctype, spec, where, report)
        _check_generalisation(claim, text, spec, where, report)
        _check_precision(claim, text, where, report)
        _check_relative_percent_base(claim, text, where, report)

    if strict:
        _check_limitations_required(spec, report)

    report.ok(f"{len(claims)} claim(s) audited")
    return report


def _resolve_roots(phase_dir: "str | None") -> list[Path]:
    roots: list[Path] = []
    if phase_dir:
        roots.append(Path(phase_dir))
    roots.append(Path.cwd())
    return roots


def _check_causal_language(
    claim: dict, text: str, ctype: str, where: str, report: Report
) -> None:
    lowered = text.lower()
    hits = causal_verb_matches(lowered)
    if not hits:
        return
    if ctype == "causal":
        return
    hedged = any(term in lowered for term in HEDGE_TERMS)
    if hedged and ctype == "association":
        report.add(
            "DSX-CLM-010",
            "MEDIUM",
            f"Claim mixes causal verbs with hedging: {', '.join(hits[:3])}",
            detail=(
                f"“{text[:160]}” is typed as '{ctype}' and does hedge, but still leans on "
                "causal verbs. Readers take the verb and drop the hedge."
            ),
            remedy="Rewrite with a neutral verb: 'is associated with', 'co-moves with', 'predicts'.",
            where=where,
        )
        return
    report.add(
        "DSX-CLM-011",
        "CRITICAL",
        f"Claim typed '{ctype or 'untyped'}' uses causal language: {', '.join(hits[:3])}",
        detail=(
            f"“{text[:160]}” asserts causation while the spec does not classify it as a causal "
            "claim. This is the overreach that turns a correlation into a roadmap commitment."
        ),
        remedy=(
            "Either retype the claim as causal and declare an identification strategy that "
            "supports it, or rewrite it in associational language."
        ),
        where=where,
        verbs=hits,
    )


def _check_causal_support(
    claim: dict, ctype: str, strategy: str, strength: str, where: str, report: Report
) -> None:
    if ctype != "causal":
        return
    claim_strategy = normalize(claim.get("identification", "")) or strategy
    if not claim_strategy or claim_strategy == "none":
        report.add(
            "DSX-CLM-020",
            "CRITICAL",
            "Causal claim with no identification strategy behind it",
            detail=(
                f"“{str(claim.get('text', ''))[:160]}” asserts an effect, but neither the claim "
                "nor the design declares how confounding is ruled out."
            ),
            remedy=(
                "Declare design.identification, or downgrade the claim to an association."
            ),
            where=where,
        )
        return

    claim_strength = IDENTIFICATION_STRATEGIES.get(claim_strategy, {}).get("strength", "none")
    if claim_strength == "weak":
        lowered = str(claim.get("text", "")).lower()
        if not any(term in lowered for term in HEDGE_TERMS):
            report.add(
                "DSX-CLM-021",
                "HIGH",
                f"Unhedged causal claim resting on a weak strategy ('{claim_strategy}')",
                detail=(
                    "Matching and regression adjustment identify effects only if every "
                    "confounder is measured — an assumption no dataset can confirm. Stating the "
                    "conclusion flatly hides that dependence."
                ),
                remedy=(
                    "Add the conditional explicitly: 'conditional on the observed covariates, "
                    "we estimate…', and cite the sensitivity analysis."
                ),
                where=where,
            )
    else:
        report.ok(f"causal claim supported by '{claim_strategy}' ({claim_strength})")


def _check_evidence_pointer(
    claim: dict, where: str, report: Report, roots: list[Path]
) -> None:
    evidence = claim.get("evidence")
    if is_blank(evidence):
        report.add(
            "DSX-CLM-030",
            "HIGH",
            "Claim has no evidence pointer",
            detail=(
                f"“{str(claim.get('text', ''))[:160]}” cannot be traced to a result, so it "
                "cannot be re-checked when the data changes."
            ),
            remedy="Point at the artefact and anchor that produced it, e.g. RESULTS.md#uplift.",
            where=where,
        )
        return

    raw = str(evidence).strip()
    path_part, _, anchor = raw.partition("#")
    path_part = path_part.strip()
    if not path_part:
        report.add(
            "DSX-CLM-031",
            "HIGH",
            "Evidence pointer does not resolve to an existing file",
            detail=f"Got {raw!r} — anchor without a file path.",
            remedy="Use file.md#anchor or a bare file path.",
            where=where,
        )
        return

    resolved = _find_evidence_file(path_part, roots)
    if resolved is None:
        report.add(
            "DSX-CLM-031",
            "HIGH",
            "Evidence pointer does not resolve to an existing file",
            detail=f"Evidence file {path_part!r} not found under: {', '.join(str(r) for r in roots)}",
            remedy="Commit the evidence artefact or fix the pointer.",
            where=where,
        )
        return

    if anchor:
        if not _anchor_present(resolved, anchor):
            report.add(
                "DSX-CLM-032",
                "HIGH",
                f"Evidence anchor #{anchor} not found in {path_part}",
                detail=f"Opened {resolved}.",
                remedy="Add the heading/id to the markdown, or fix the anchor name.",
                where=where,
            )
        else:
            report.ok(f"evidence {path_part}#{anchor} resolved")
    else:
        report.ok(f"evidence file {path_part} exists")


def _find_evidence_file(relative: str, roots: list[Path]) -> Path | None:
    candidate = Path(relative)
    if candidate.is_absolute() and candidate.exists():
        return candidate
    for root in roots:
        path = root / relative
        if path.exists():
            return path
    if candidate.exists():
        return candidate
    return None


def _anchor_present(path: Path, anchor: str) -> bool:
    """True if markdown contains a matching heading or explicit HTML id."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    needle = anchor.strip().lower().replace(" ", "-")
    if re.search(rf'id=["\']{re.escape(anchor)}["\']', text, re.IGNORECASE):
        return True
    if re.search(rf'name=["\']{re.escape(anchor)}["\']', text, re.IGNORECASE):
        return True
    for line in text.splitlines():
        heading = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", line)
        if not heading:
            continue
        title = heading.group(1).strip().lower()
        # strip simple markdown emphasis
        title = re.sub(r"[*_`]", "", title)
        slug = re.sub(r"[^a-z0-9]+", "-", title).strip("-")
        if slug == needle or title.replace(" ", "-") == needle or title == needle:
            return True
    return False


def _check_numeric_overlap(
    claim: dict, text: str, tests: list, where: str, report: Report
) -> None:
    """Claim numbers must overlap results.tests effects/CIs when tests exist."""
    if not tests:
        return
    claim_numbers = _extract_claim_magnitudes(text, claim)
    if not claim_numbers:
        return

    reference: list[float] = []
    for test in tests:
        if not isinstance(test, dict):
            continue
        effect = as_number(test.get("effect"))
        if effect is not None:
            reference.append(effect)
            # percentage-point / percent reporting often uses 100x scale
            reference.append(effect * 100.0)
        ci = test.get("ci")
        if isinstance(ci, (list, tuple)) and len(ci) == 2:
            for bound in ci:
                value = as_number(bound)
                if value is not None:
                    reference.append(value)
                    reference.append(value * 100.0)
    claim_ci = claim.get("ci")
    if isinstance(claim_ci, (list, tuple)) and len(claim_ci) == 2:
        for bound in claim_ci:
            value = as_number(bound)
            if value is not None:
                reference.append(value)
                reference.append(value * 100.0)

    if not reference:
        return

    unmatched = []
    for number in claim_numbers:
        if not any(_close_enough(number, ref) for ref in reference):
            unmatched.append(number)
    if unmatched:
        report.add(
            "DSX-CLM-033",
            "CRITICAL",
            "Claim numbers do not overlap results.tests",
            detail=(
                f"Unmatched claim figure(s): {', '.join(f'{n:g}' for n in unmatched)}. "
                "When results.tests is filled, every headline magnitude must appear as an "
                "effect or CI bound (allowing a 100× scale for pp/%)."
            ),
            remedy=(
                "Align the claim text with results.tests, or declare claim.ci from the "
                "same interval."
            ),
            where=where,
        )
    else:
        report.ok("claim magnitudes overlap results.tests")


def _extract_claim_magnitudes(text: str, claim: dict) -> list[float]:
    """Magnitudes that must reconcile with results — not every digit in the prose.

    Only % / pp figures and decimal effect sizes are checked. Bare integers
    (day counts, p95 labels, sample sizes) and conventional confidence levels
    (90%/95%/99% CI) are ignored.
    """
    numbers: list[float] = []
    for match in _NUMBER_RE.finditer(text):
        value = as_number(match.group(1))
        if value is None:
            continue
        unit = (match.group(2) or "").lower()
        raw = match.group(1)
        tail = text[match.end() : match.end() + 12].lower()
        if unit == "%" and value in {80.0, 90.0, 95.0, 99.0} and (
            "ci" in tail or "confidence" in tail or tail.lstrip().startswith("interval")
        ):
            continue
        if unit in {"%", "pp", "percentage points"}:
            numbers.append(value)
            continue
        if "." in raw:
            if value >= 1900 and value <= 2100:
                continue
            numbers.append(value)
    ci = claim.get("ci")
    if isinstance(ci, (list, tuple)) and len(ci) == 2:
        for bound in ci:
            value = as_number(bound)
            if value is not None:
                numbers.append(value)
    return numbers


def _close_enough(a: float, b: float, rel: float = 0.05, abs_tol: float = 0.0005) -> bool:
    if abs(a - b) <= abs_tol:
        return True
    scale = max(abs(a), abs(b), 1e-12)
    return abs(a - b) / scale <= rel


def _check_predictive_support(
    claim: dict, ctype: str, spec: dict, where: str, report: Report
) -> None:
    if ctype != "predictive":
        return
    if not section(spec, "model"):
        report.add(
            "DSX-CLM-040",
            "HIGH",
            "Predictive claim with no model block",
            detail="A prediction claim needs a declared model, split and out-of-sample score.",
            remedy="Declare the model block, or retype the claim as descriptive.",
            where=where,
        )
        return
    if get(spec, "results.test_score") is None:
        report.add(
            "DSX-CLM-041",
            "HIGH",
            "Predictive claim with no out-of-sample score reported",
            detail="In-sample fit says nothing about predictive performance.",
            remedy="Report results.test_score from data the model never saw during training.",
            where=where,
        )


def _check_generalisation(claim: dict, text: str, spec: dict, where: str, report: Report) -> None:
    lowered = text.lower()
    hits = [term for term in GENERALISATION_TERMS if term in lowered]
    population = claim.get("population")
    sampled = get(spec, "data")
    if hits and is_blank(population):
        report.add(
            "DSX-CLM-050",
            "MEDIUM",
            f"Claim generalises broadly ({', '.join(hits[:2])}) without naming its population",
            detail=(
                f"“{text[:160]}”. The estimate applies to whoever was in the sample — which the "
                "claim does not state, so the reader will assume it means everyone."
            ),
            remedy=(
                "Name the population the estimate covers and the period it was measured over. "
                "If the sample is not representative of the wider group, say so."
            ),
            where=where,
        )
    elif hits and sampled:
        report.ok("broad claim scoped to a declared population")


def _check_precision(claim: dict, text: str, where: str, report: Report) -> None:
    ci = claim.get("ci")
    if not (isinstance(ci, (list, tuple)) and len(ci) == 2):
        return
    lower, upper = as_number(ci[0]), as_number(ci[1])
    if lower is None or upper is None:
        return
    width = abs(upper - lower)
    if width <= 0:
        return

    for match in _NUMBER_RE.finditer(text):
        raw = match.group(1)
        if "." not in raw:
            continue
        decimals = len(raw.split(".")[1])
        # A digit is meaningful only if it is larger than the interval's own resolution.
        resolution = width / 2.0
        if resolution <= 0:
            continue
        justified = max(0, int(math.floor(-math.log10(resolution))) + 1)
        if decimals > justified + 1:
            report.add(
                "DSX-CLM-060",
                "LOW",
                f"Claim quotes {raw} to {decimals} decimals against a CI half-width of {resolution:.3g}",
                detail=(
                    "Reporting more digits than the interval supports projects a precision the "
                    "estimate does not have."
                ),
                remedy=f"Round to about {justified} decimal place(s) and quote the interval alongside.",
                where=where,
            )
            return


def _check_relative_percent_base(
    claim: dict, text: str, where: str, report: Report
) -> None:
    if not relative_percent_without_base(text, claim):
        return
    report.add(
        "DSX-CLM-070",
        "HIGH",
        "Relative % in claim without a declared or nearby base",
        detail=(
            f"“{text[:160]}”. A relative percentage without from/to, n=, or base_n "
            "invites the reader to invent a flattering denominator. Absolute "
            "percentage points with a CI are fine (see DSX-CLM-033)."
        ),
        remedy=(
            "Add nearby base language, or set base_n, or set both from_value and to_value."
        ),
        where=where,
    )


def _check_limitations_required(spec: dict, report: Report) -> None:
    qtype = normalize(spec.get("question_type", ""))
    if qtype not in {"causal", "prescriptive", "predictive"}:
        return
    limitations = spec.get("limitations")
    if isinstance(limitations, list) and any(
        isinstance(item, str) and item.strip() for item in limitations
    ):
        report.ok("limitations declared for a high-stakes question type")
        return
    report.add(
        "DSX-CLM-080",
        "HIGH",
        f"question_type {qtype!r} requires a non-empty limitations list at verify/ship",
        detail=(
            "Causal, prescriptive and predictive answers without stated limits read as "
            "complete. Put the limits where the decision-maker will see them."
        ),
        remedy="Add limitations: with at least one concrete sentence.",
        where="spec.limitations",
    )
