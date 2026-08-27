"""Corpus invariants over ``examples/known-bad/`` (REQ-P6-13, ROADMAP Success
Criterion 5).

The corpus is discovered by globbing the directory, never by a hardcoded
filename list, so Phase 12 can grow it without editing this module. Every
invariant here is structural or compositional — no test asserts a specific
finding code fires, because the defect each fixture encodes is semantic and
each code-specific block assertion lands with the phase that ships its code.

Run:  python3 -m unittest tests.test_known_bad_corpus -v
"""

from __future__ import annotations

import io
import json
import re
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from _trail_seed import seed_plan_header  # noqa: E402
from dsx import cli  # noqa: E402
from dsx.frame.paradigm import _MONITORING_DISCIPLINE  # noqa: E402
from dsx.loader import load  # noqa: E402

CORPUS_DIR = ROOT / "examples" / "known-bad"
SPEC_SUFFIX = "-ANALYSIS-SPEC.yaml"
POSTMORTEM_SUFFIX = "-POSTMORTEM.md"
ATTRIBUTION_SUFFIX = "-ATTRIBUTION.yaml"
SYMMETRY_AUDIT_PATH = ROOT / "references" / "paradigm-symmetry.md"

# The three controlled design.peeking_policy values REQ-P9-01 names as "the
# honest fix" — asserted by name so the audit cannot silently drop one while
# still reading as complete prose.
_CONTROLLED_PEEKING_POLICIES = ("sequential_obf", "sequential_pocock", "always_valid")

# The two reference-value anchors the audit's "Reference values and their
# sources" section commits to: DSX-PAR-010's 0.05 nominal alpha and
# DSX-PAR-011's 1/(K+1) = 0.05 bound at K = 19.
_SYMMETRY_AUDIT_REFERENCE_VALUES = ("0.142", "0.05")

# The catch-attribution shape Phase 12 (REQ-P12-02) will formalise into structured tags.
_FINDING_CODE_RE = re.compile(r"\bDSX-[A-Z]+-\d+\b")

# The two gate points whose default `dsx gate` threshold is CRITICAL
# (dsx/cli.py::GATE_THRESHOLDS). The corpus's positive guarantee is that every
# fixture clears both of these today — this is the half of the claim ROADMAP
# Success Criterion 5 actually depends on.
_CRITICAL_THRESHOLD_POINTS = ("plan", "execute")

# The measured union of every CRITICAL/HIGH finding `dsx gate ship --json` emits
# against each of the three committed fixtures (measured 2026-08-08 with
# --phase-dir pointed at a fresh tempfile.TemporaryDirectory() per run — see
# 06-12-SUMMARY.md for the full per-fixture, per-point exit-code and finding-code
# table this constant was measured from). Each entry names the corpus-completeness
# gap that causes it — never the semantic defect the fixture exists to encode.
_INCIDENTAL_GAP_CODES = {
    "DSX-CLM-031",  # claims[].evidence points at "RESULTS.md#..." — a file this corpus never commits
    "DSX-COH-031",  # assumptions[0] is declared but neither checked: true nor waived
    "DSX-DEC-001",  # Phase 12 (REQ-P12-01): the three coverage-class fixtures
                    # (garden-of-forking-paths-p-hacking, retracted-fabricated-
                    # field-experiment) declare a results.tests block with a CI but
                    # no decision.replay block, so the replay-completeness check
                    # fires HIGH — a corpus-completeness gap (these fixtures never
                    # commit a replay harness), never the encoded miss each exists
                    # to demonstrate (undisclosed forking / data fabrication).
    "DSX-EXP-007",  # frequentist fixture: design.mde (0.02) exceeds decision.minimum_practical_effect (0.01)
    "DSX-EXP-051",  # full-frame-cleaning + post-hoc-procedure-switch declare
                    # comparisons_looked_at:5 with no multiplicity.family and no
                    # results.tests, so the Phase 11.3-01 (D-02) family-independent
                    # rebase fires HIGH — a true undisclosed-multiple-comparisons
                    # observation incidental to each fixture's encoded target defect
                    # (data leakage / procedure switch), not that defect itself. §4
                    # persona round (Statistician+Auditor, rigour): documented, not
                    # silenced by narrowing the check.
    "DSX-MET-040",  # metrics[0].source is warehouse.* with no metrics[0].sql definition
    "DSX-NAR-001",  # claims declared but narrative.path missing (ship-only check)
    "DSX-REP-001",  # bayesian fixture: bayesian_ab is a stochastic method with no reproducibility.random_seed
    "DSX-REP-030",  # reproducibility.entrypoint is not declared
    "DSX-REP-050",  # Phase 12 (REQ-P12-01): the three coverage-class fixtures declare
                    # a non-empty results.tests block but no reproducibility.repro_lock,
                    # so the repro-lock-required-with-results check fires HIGH — the same
                    # corpus-completeness gap as DSX-REP-030 (no reproducibility harness is
                    # committed for these hand-authored fixtures), never the encoded miss.
    "DSX-STA-041",  # bayesian fixture: declared analysis.test (bayesian_ab) is outside the stats
                    # recommendation engine's acceptable set for this outcome shape
    "DSX-VAL-041",  # bayesian fixture: strength: strong with constraint_source:
                    # informative_priors is a true, honest declaration (it is a Bayesian
                    # analysis and does use informative priors) — a correct secondary
                    # observation about a fixture built to demonstrate a different defect
                    # (uncontrolled continuous monitoring), not the encoded defect itself
                    # (plan 07-05, D-14)
}

# Per-fixture target-defect map (D-15 structural rewrite, plan 08-02): for each fixture
# slug (filename with "-ANALYSIS-SPEC.yaml" stripped, matching `_slugs`), the finding
# code that fixture exists to demonstrate, keyed by the gate point at which it is
# expected to block. A fixture absent from this map — or absent at a given gate point
# — defaults to "clears that gate point cleanly", which is today's behaviour for every
# fixture and is preserved exactly. Replaces the old family-prefix allow-list and the
# old plan-only expected-blocker dict: a family-prefix string can express at most one
# code per family, and Phase 8 is the first phase to ship four codes in one family
# (`DSX-INT-*`), so a family prefix can no longer distinguish the code a fixture exists
# to demonstrate from an unrelated code from the same family the fixture happens to
# also trip — see test_incidental_allowlist_names_no_slugs_own_target_code below.
#
# weak-identification-mmm -> DSX-VAL-040 already ships in this milestone (Phase 7,
# plan 07-07) — the first fixture in this corpus whose target code lands in the same
# milestone as the fixture itself. This entry replaces the old plan-only expected-
# blocker dict that previously encoded it (07-07, D-15 Option A); the per-fixture map
# generalises that single-purpose mechanism without changing the guarantee it made —
# still plan-only, still MUST block with the mapped code among the CRITICAL findings,
# `dsx gate execute` is untouched because the "val" check is not in the execute gate
# profile (dsx/cli.py::GATE_PROFILES).
#
# Plan 08-03 adds interference-shared-budget -> {"plan": "DSX-INT-010"}.
# Plan 08-04 adds triggering-dilution -> {"plan": "DSX-INT-030"}.
# A later Phase 9 plan adds the two monitoring fixtures for its own atomic pair
# (DSX-PAR-010/DSX-PAR-011).
#
# Fragility note (measured 2026-08-12, plan 08-02; re-measured 2026-08-13, plan 08-04):
# both bayesian-continuous-monitoring and frequentist-uncontrolled-continuous declare
# validity_frame.triggering with analysis_population: eligible and dilution_adjusted:
# false — two of DSX-INT-030's three trigger conditions. Both still escape (confirmed
# once DSX-INT-030 shipped) only because each declares a single metric of type: ratio,
# outside the additive partition {count, sum, average}. Adding a metric of type count,
# sum or average to either fixture will make it block dsx gate plan on DSX-INT-030 and
# will require an entry in this map.
#
# Resolved fragility note (plan 08-04): weak-identification-mmm declares
# analysis_population: eligible, dilution_adjusted: false, AND a metrics[0].type of sum
# (additive) — three of DSX-INT-030's structural conditions, exactly as D-01/D-09 state
# them (an additive metric analysed on the eligible population with dilution_adjusted
# not true). D-09's stated firing condition names only those two triggering-block
# fields plus D-11's additive-metric-type test — no expected_trigger_rate/materiality
# gate — so plan 08-04's implementation deliberately does NOT special-case
# expected_trigger_rate: 1.0, and this fixture now blocks dsx gate plan/verify/ship on
# DSX-INT-030 alongside its own DSX-VAL-040. The "verify" key below is not a claim that
# DSX-INT-030 fires ONLY at verify for this fixture — it also fires at plan and ship,
# same as "interference" is registered everywhere "val" is (dsx/cli.py::GATE_PROFILES)
# — it is a second, distinct key so its value can live beside "plan": "DSX-VAL-040" in
# this per-fixture dict without colliding; _own_target_codes() flattens every point's
# value for a slug into one set regardless of which key holds it, which is what the
# ship-completeness test (test_ship_gate_findings_are_all_documented_incidental_corpus_gaps)
# actually consults. Not fixed by editing the fixture: its expected_trigger_rate: 1.0
# is an honest declaration (a full-period national aggregate with no eligibility gate
# below 100% coverage), not a defect, and DSX-INT-030 correctly names an additive metric
# is analysed on that eligible population with no adjustment declared — a second,
# genuine defect this fixture happens to also encode, not a false positive.
# Plan 10-05 adds post-hoc-procedure-switch -> {"verify": "DSX-PRE-030"}: `prereg`
# (dsx/frame/prereg.py) is registered in the verify and ship gate profiles only
# (dsx/cli.py::GATE_PROFILES), never plan or execute, so this is the second
# verify-only-key entry in this map after weak-identification-mmm's DSX-INT-030 —
# the shape this map exists for. See test_post_hoc_procedure_switch_fixture_blocks_
# verify_and_ship_naming_pre_030 for the positive-direction proof the generic
# test below cannot supply, exactly as test_weak_identification_mmm_fixture_
# blocks_verify_and_ship_naming_int_030 supplies it for the other verify-only entry.
#
# Plan 11.1-08 (REQ-P11.1-07/08) widens a point's value to accept either a bare
# code string (every entry above) or a frozenset of several code strings, for
# full-frame-cleaning's "execute" entry below: the entrypoint check family
# (`code`, DSX-CODE-*) and the machine-learning check family (`ml`, DSX-ML-*)
# are both registered at the `execute` gate point but not at `plan`
# (dsx/cli.py::GATE_PROFILES), and this phase's fixture demonstrates three
# CRITICAL codes from the `code` family at that one point at once — the first
# point-scoped entry in this map to need the multi-code shape
# `_classify_target_defect`'s own docstring already documents and accepts.
# full-frame-cleaning's own DSX-ML-090 (HIGH, not CRITICAL) cannot live in this
# map at all: `_classify_target_defect` only ever checks CRITICAL findings, so a
# HIGH code placed here would be reported "missing" from every CRITICAL list it
# is compared against. It is instead recorded under a second, non-critical-
# threshold key ("ship") purely so `_own_target_codes` (which reads every key's
# value regardless of name) recognises it as this fixture's own code for the
# ship-completeness test — mirroring weak-identification-mmm's own second key
# above, which documents the identical "this key is a dict-collision-avoidance
# device, not a claim the code fires only at that one point" reasoning.
_TARGET_DEFECT_CODES: "dict[str, dict[str, str | frozenset[str]]]" = {
    "weak-identification-mmm": {"plan": "DSX-VAL-040", "verify": "DSX-INT-030"},
    "interference-shared-budget": {"plan": "DSX-INT-010"},
    "triggering-dilution": {"plan": "DSX-INT-030"},
    "post-hoc-procedure-switch": {"verify": "DSX-PRE-030"},
    # Plan 11.1-08 (REQ-P11.1-07/08): full-frame-cleaning's three CRITICAL
    # entrypoint-scan codes, all shipped in this same plan's task 1 groundwork
    # (DSX-CODE-020/DSX-CODE-021 in plan 11.1-01; DSX-CODE-030 in plan 11.1-03),
    # scoped to "execute" — the `code` check family is registered at the
    # `execute` gate point but not at `plan` (dsx/cli.py::GATE_PROFILES), so
    # there is nothing for this fixture to catch at plan. Measured 2026-08-20
    # against the fixture as committed by this plan's task 2: `dsx gate execute`
    # with the entrypoint seeded into the temporary phase directory exits 1 with
    # exactly these three codes among its CRITICAL findings (see the paired
    # POSTMORTEM.md's measured table).
    #
    # The fixture's fourth own code, DSX-ML-090 (HIGH, shipped in plan 11.1-06),
    # also fires at execute (the `ml` check family is registered there too) but
    # cannot be recorded in this "execute" entry: `_classify_target_defect` only
    # ever checks CRITICAL-severity findings, and a HIGH code placed alongside
    # the three CRITICAL ones above would be reported "missing" from that
    # CRITICAL-only comparison every time. It is recorded under a second,
    # distinguishing key ("ship", where it also fires) purely so
    # `_own_target_codes` — which flattens every key's value for a slug
    # regardless of the key's name — recognises it as this fixture's own code
    # for the ship-completeness test below. This mirrors
    # weak-identification-mmm's own second key above: the key name is a
    # dict-collision-avoidance device, not a claim the code fires only at that
    # one point.
    "full-frame-cleaning": {
        "execute": frozenset({"DSX-CODE-020", "DSX-CODE-021", "DSX-CODE-030"}),
        "ship": "DSX-ML-090",
    },
    # Plan 11.2-08 (REQ-P11.2-03): the flagship "offer bundled incentives to
    # reduce churn" fixture — a prescriptive claim smuggled under a descriptive
    # question. Its four catches split cleanly across gate points by which check
    # family is registered where (dsx/cli.py::GATE_PROFILES):
    #
    #   - "plan" -> {DSX-COH-001, DSX-COH-010}: `coherence` is registered at
    #     plan (and verify/ship). DSX-COH-001 fires because claims[0].type
    #     `prescriptive` (strength 4) exceeds question_type `descriptive`
    #     (strength 0); DSX-COH-010 fires because the decision rule carries the
    #     purpose-gated causal verb `reduce` under a descriptive question. Both
    #     are CRITICAL, so this is the point-scoped guarantee the generic
    #     critical-threshold test consumes.
    #   - "verify"/"ship" -> {DSX-CLM-020}: `claims` is registered at verify and
    #     ship only, never plan or execute. DSX-CLM-020 fires because a
    #     prescriptive claim recommends an intervention with no identification
    #     strategy behind it. (Before WR-01 this set also listed DSX-CLM-011, but
    #     _check_causal_language now exempts prescriptive — DSX-CLM-011 there
    #     double-coded the DSX-CLM-020 fact with a strength-downgrade remedy;
    #     11.2 code review, §4 persona round. The flagship still blocks on
    #     DSX-CLM-020 CRITICAL.) This key is consulted only by _own_target_codes
    #     (which flattens every point's value regardless of key name) for the
    #     ship-completeness test — the same dict-collision-avoidance device
    #     weak-identification-mmm's "verify" key and full-frame-cleaning's "ship"
    #     key already use, not a claim these codes fire ONLY at verify/ship.
    #     DSX-COH-001/DSX-COH-010 also fire at verify/ship (coherence is
    #     registered there too) and are recognised as this fixture's own codes
    #     via the "plan" key above.
    #   - NO "execute" entry: `coherence` and `claims` are both absent from the
    #     execute gate profile, so the fixture exits 0 there and must default to
    #     the clears-cleanly branch.
    #
    # Measured 2026-08-26 against a fresh tempfile.TemporaryDirectory() per gate
    # point (never the shared examples/known-bad/DECISIONS.jsonl — RESEARCH
    # landmine f). Deliberately NOT added to _EXPECTED_CAUGHT_DEFECTS with codes:
    # that map contributes its whole set at BOTH plan and execute, and these
    # coherence codes fire at plan but not execute, so an entry there would
    # wrongly demand DSX-COH-001/010 at execute too. Its _EXPECTED_CAUGHT_DEFECTS
    # entry is an empty frozenset() (below), for the key-parity test only.
    "prescriptive-churn-recommendation": {
        "plan": frozenset({"DSX-COH-001", "DSX-COH-010"}),
        "verify": frozenset({"DSX-CLM-020"}),
        "ship": frozenset({"DSX-CLM-020"}),
    },
}


def _classify_target_defect(
    slug: str,
    point: str,
    exit_code: int,
    findings: list[dict],
    target_map: "dict[str, dict[str, str | frozenset[str]]]",
) -> list[str]:
    """Classify one (slug, point) gate result against `target_map` and return a list of
    problem strings (empty when the result matches the map's expectation).

    Exactly two rules: when `target_map` has no code for `slug` at `point`, `exit_code`
    must be 0. When it has one or more, `exit_code` must be 1 and every one of those
    codes must appear among `findings` whose severity is CRITICAL. `target_map` is a
    parameter, never the module constant read directly — that is what lets a synthetic
    map exercise this function without touching the filesystem or the gate (the second
    of the two proofs this module's rewrite owes, matching
    tests/test_frame_boundary.py's discipline).

    A map value may be a bare string (the single-target shape plan 08-02 introduced for
    `_TARGET_DEFECT_CODES`, where one fixture demonstrates one code at one gate point)
    or a frozenset of strings (the multi-code shape plan 09-03's
    `_EXPECTED_CAUGHT_DEFECTS` needs, where a fixture's target check is registered at
    every CRITICAL-threshold point). Both normalize to a set here, so the two maps are
    decided by this one classifier rather than by two divergent inline branches —
    which is what let a merge of the two phases silently keep one guarantee and drop
    the other.
    """
    raw = target_map.get(slug, {}).get(point)
    expected: frozenset[str]
    if raw is None:
        expected = frozenset()
    elif isinstance(raw, str):
        expected = frozenset({raw})
    else:
        expected = frozenset(raw)
    critical = [f["code"] for f in findings if f.get("severity") == "CRITICAL"]
    problems: list[str] = []
    if not expected:
        if exit_code != 0:
            problems.append(
                f"{slug!r} has no target code at {point!r} but exited {exit_code} "
                f"(CRITICAL findings: {critical})"
            )
        return problems
    if exit_code != 1:
        problems.append(
            f"{slug!r} is mapped to {sorted(expected)!r} at {point!r} but exited "
            f"{exit_code}, not 1"
        )
    missing = expected - set(critical)
    if missing:
        problems.append(
            f"{slug!r} is mapped to {sorted(expected)!r} at {point!r} but "
            f"{sorted(missing)!r} is not among the CRITICAL findings: {critical}"
        )
    return problems

# The two retired, false gate-behaviour claims this plan (06-12) removed from
# every committed file under examples/known-bad/ — named identically to the two
# <!-- planner-discipline-allow: ... --> literals in 06-12-PLAN.md.
_RETIRED_OVERCLAIMS = ("validate/gate checks pass it", "passes every gate")

# The three drift markers retired by UAT gap G-01. The prior-averaged reference
# value is Deng, Lu & Chen (2016) Theorem 1's `1/(K+1)` — exactly 0.05 at K = 19
# — and NOT Ville's inequality's `1/k`, which gives 1/19 ~ 0.0526 at the same
# threshold. Both bounds are individually correct statements about different
# quantities, which is precisely why the conflation survived review: no sentence
# was false on its own. The guard therefore names the misattributing phrasings
# rather than the numbers, so corrected prose stays free to explain the
# distinction (and must, to stop the error returning).
_RETIRED_BOUND_MISATTRIBUTIONS = (
    "prior-averaged Ville bound",
    "martingale (Ville's inequality) argument",
    "commonly rounded and reported as",
)

# Documents outside the corpus that carried the same drift. brief.md section 6.5
# is what a Phase 9 planner reads before drafting DSX-PAR-011, so leaving it
# unguarded is how this error would return after the fixture was corrected.
_BOUND_CLAIM_DOCUMENTS = (
    ROOT / "brief.md",
    ROOT / ".planning" / "REQUIREMENTS.md",
    ROOT / ".planning" / "ROADMAP.md",
)

# The two retired locator-error phrasings closed by plan 09-07 (REQ-P9-03):
# both tie the 1/(K+1) number directly to the numbered "Theorem 1", when the
# paper states the bound as unnumbered prose immediately following Theorem 1
# and again, in its operational form, in Section 3.2 — Theorem 1 itself states
# only the optional-stopping equality that licenses the bound under known
# prior odds. Scoped to examples/known-bad/ only, deliberately kept separate
# from _RETIRED_BOUND_MISATTRIBUTIONS (which is also applied to brief.md,
# .planning/REQUIREMENTS.md and .planning/ROADMAP.md by
# test_no_planning_document_misattributes_the_prior_averaged_bound): those
# three planning documents legitimately carry the corrected form of this
# citation, so a tuple applied to them must not name phrasings the corrected
# prose is expected to state. The guard names the phrasings rather than the
# numbers, so corrected prose stays free to explain the distinction between
# what Theorem 1 states and where the number itself appears.
_RETIRED_LOCATOR_ERRORS = (
    "2016, Theorem 1",
    "Theorem 1 caps",
)


# Per-fixture expected-caught-defect map (D-03): keyed by fixture slug — the same
# value _slugs() produces, the spec filename with -ANALYSIS-SPEC.yaml stripped —
# mapping to the set of CRITICAL finding codes that fixture's own target check is
# now expected to catch at dsx gate plan/execute.
#
# An empty set means the code this fixture exists to motivate has not shipped yet,
# so the fixture must still clear both CRITICAL-threshold gate points exactly like
# every other fixture (test_every_spec_passes_the_critical_threshold_gate_points'
# ordinary exit-0 branch). An entry gains codes in the same commit that ships the
# check catching that fixture — never before, and never silently left behind
# afterwards: test_expected_caught_defects_keys_match_the_corpus_on_disk requires
# every fixture on disk to have a key here, and
# test_ship_gate_findings_are_all_documented_incidental_corpus_gaps requires a
# fixture's own target-family code to be accounted for here rather than laundered
# into _INCIDENTAL_GAP_CODES once it ships.
#
# Distinct from _TARGET_DEFECT_CODES above, and deliberately kept as a second map
# rather than folded into it (merge of plan 08-02 and plan 09-01, 2026-08-13):
# _TARGET_DEFECT_CODES is keyed by gate point and carries at most one code per point,
# for a fixture whose target check fires at some points but not others — Phase 7's
# weak-identification-mmm, whose "val" family is absent from the `execute` GATE_PROFILES
# entry, is the case it exists for, and it is the shape plans 08-03/08-04 add their
# DSX-INT-* entries to. This dict is the general per-fixture, both-critical-points form
# D-03 specifies, for target checks — like Phase 9's DSX-PAR-010/DSX-PAR-011 pair —
# whose check family is registered at every gate point and so is expected to catch at
# both. Neither shape subsumes the other, so both are live and both are enforced;
# _effective_target_map() below is the single place they are combined.
#
# A fixture whose target code has not shipped yet carries an empty frozenset: it must
# still clear both CRITICAL-threshold gate points like any other fixture. Two entries
# are empty for that reason today — interference-shared-budget (DSX-INT-010 ships in
# plan 08-03) and triggering-dilution (DSX-INT-030 ships in plan 08-04).
_EXPECTED_CAUGHT_DEFECTS: "dict[str, frozenset[str]]" = {
    "bayesian-continuous-monitoring": frozenset({"DSX-PAR-011"}),
    "frequentist-uncontrolled-continuous": frozenset({"DSX-PAR-010"}),
    "interference-shared-budget": frozenset(),
    "triggering-dilution": frozenset(),
    "weak-identification-mmm": frozenset(),
    # Empty by design, not by omission: this map's frozenset applies at every
    # point in _CRITICAL_THRESHOLD_POINTS ("plan", "execute"), and `prereg`
    # structurally cannot fire there — it is registered in GATE_PROFILES["verify"]
    # and ["ship"] only. The fixture's real catch (DSX-PRE-030 at "verify") lives
    # in _TARGET_DEFECT_CODES above instead, the point-scoped shape.
    "post-hoc-procedure-switch": frozenset(),
    # Plan 11.1-08: also empty by design, for the same reason as
    # post-hoc-procedure-switch immediately above but the other way round —
    # this fixture's own codes fire at "execute" (both the `code` and `ml`
    # families are registered there) but not at "plan" (neither family is
    # registered there at all), so there is nothing this both-points map could
    # correctly claim. The fixture's real catch (three CRITICAL codes at
    # "execute", plus DSX-ML-090 recorded under the "ship" key) lives entirely
    # in _TARGET_DEFECT_CODES above, the point-scoped shape.
    "full-frame-cleaning": frozenset(),
    # Plan 11.2-08: empty by design, not omission — for the same reason as
    # post-hoc-procedure-switch and full-frame-cleaning above. This map's
    # frozenset applies at every point in _CRITICAL_THRESHOLD_POINTS ("plan",
    # "execute"), but the flagship's own catches are DSX-COH-001/DSX-COH-010 at
    # plan (which fire at plan but NOT execute — `coherence` is absent from the
    # execute gate profile) and DSX-CLM-011/DSX-CLM-020 at verify/ship (`claims`
    # is registered at verify/ship only). None of the four fires at both
    # critical-threshold points, so there is nothing this both-points map could
    # correctly claim. The fixture's real, point-scoped catches live entirely in
    # _TARGET_DEFECT_CODES above. The key is required here solely so
    # test_expected_caught_defects_keys_match_the_corpus_on_disk stays green.
    "prescriptive-churn-recommendation": frozenset(),
    # Phase 12 (REQ-P12-01, D-01/D-02): the three coverage-class fixtures are
    # MISSES — each encodes a real-world defect (undisclosed garden-of-forking-
    # paths specification search, data fabrication, undisclosed selective
    # exclusion) that a declaration-only gate structurally cannot catch. No
    # shipped check fires their target defect, so the caught-defect set is empty
    # by design. The currently-ABSENT code that would attribute each miss, and the
    # §6.5 backlog item it promotes, live in each fixture's <slug>-ATTRIBUTION.yaml
    # sidecar (D-06/D-07), never in these harness maps (D-05: do not overload the
    # present-code maps with the absent-code polarity). The key is required here
    # solely so test_expected_caught_defects_keys_match_the_corpus_on_disk stays green.
    "garden-of-forking-paths-p-hacking": frozenset(),
    "retracted-fabricated-field-experiment": frozenset(),
    "operator-known-answer-selective-exclusion": frozenset(),
}


def _effective_target_map() -> "dict[str, dict[str, frozenset[str]]]":
    """Combine the corpus's two per-fixture expectation maps into the single
    (slug -> point -> expected CRITICAL codes) form `_classify_target_defect` decides.

    `_TARGET_DEFECT_CODES` contributes one code, or (plan 11.1-08) several codes as a
    frozenset, at the exact gate point it names — flattened into individual code
    strings here rather than added as one container, the same flattening
    `_own_target_codes` performs for the identical reason: adding an un-flattened
    frozenset would put a whole frozenset in as one hashable-but-wrong element of the
    point's set, so `_classify_target_defect` would compare a real gate's individual
    finding codes against a set containing one frozenset and never match.
    `_EXPECTED_CAUGHT_DEFECTS` contributes its whole set at every point in
    `_CRITICAL_THRESHOLD_POINTS`, because a check family registered at every gate
    point is expected to catch at every CRITICAL-threshold one. Contributions union
    rather than overwrite: a fixture may legitimately appear in both maps, and losing
    either contribution would silently retire a guarantee one of the two phases shipped.
    """
    merged: "dict[str, dict[str, set[str]]]" = {}
    for slug, points in _TARGET_DEFECT_CODES.items():
        for point, code in points.items():
            bucket = merged.setdefault(slug, {}).setdefault(point, set())
            if isinstance(code, str):
                bucket.add(code)
            else:
                bucket.update(code)
    for slug, codes in _EXPECTED_CAUGHT_DEFECTS.items():
        if not codes:
            continue
        for point in _CRITICAL_THRESHOLD_POINTS:
            merged.setdefault(slug, {}).setdefault(point, set()).update(codes)
    return {
        slug: {point: frozenset(codes) for point, codes in points.items()}
        for slug, points in merged.items()
    }


def _own_target_codes(
    slug: str,
    target_map: "dict[str, dict[str, str | frozenset[str]]] | None" = None,
    expected_map: "dict[str, frozenset[str]] | None" = None,
) -> "frozenset[str]":
    """Every code `slug` is this corpus's declared demonstration of, across both maps.

    Plan 11.1-08: flattens a `_TARGET_DEFECT_CODES` value into its individual code
    strings rather than collecting the raw mapping value — a point's value may be a
    bare string (the single-target shape plan 08-02 introduced) or a frozenset of
    several codes (the multi-code shape this plan's fixture needs, since its
    `execute`-point entry names three codes at once). Collecting `.values()` directly,
    as this function did before this plan, would put a whole frozenset into the
    returned set as one unhashable-looking element instead of its member codes,
    which is exactly the drift `test_ship_gate_findings_are_all_documented_incidental_corpus_gaps`
    would otherwise silently mis-evaluate: a fixture's own multi-code entry would
    fail to match any single code in a real gate's findings, reporting every one of
    that fixture's own codes as undocumented.

    `target_map` and `expected_map` default to the module constants
    `_TARGET_DEFECT_CODES`/`_EXPECTED_CAUGHT_DEFECTS` — every real call site in this
    module calls this function with one argument, exactly as before this plan — but
    accepting them as parameters lets a synthetic map exercise the flattening
    independent of the filesystem and the real gate, the same testability discipline
    `_classify_target_defect`'s own docstring already sets out for `target_map` there.
    """
    if target_map is None:
        target_map = _TARGET_DEFECT_CODES
    if expected_map is None:
        expected_map = _EXPECTED_CAUGHT_DEFECTS
    codes: "set[str]" = set()
    for value in target_map.get(slug, {}).values():
        if isinstance(value, str):
            codes.add(value)
        else:
            codes.update(value)
    codes.update(expected_map.get(slug, frozenset()))
    return frozenset(codes)


def _seed_entrypoint(tmp: "str | Path", spec_path: "str | Path") -> None:
    """Copy a fixture's own declared reproducibility entrypoint into the temporary
    phase directory `_gate_findings` gates against (plan 11.1-08, REQ-P11.1-07/08).

    The harness deliberately points the resolve root at a fresh temporary directory
    on every call (see `_gate_findings`'s own docstring) so the decision trail is
    never written under `examples/` — but that same choice makes a fixture's own
    entrypoint unreachable to the entrypoint check (`dsx/checks/code.py`), which
    resolves a relative `reproducibility.entrypoint` against that same temporary
    root (`dsx/cli.py::run_checks` passes it the resolve root, not the spec's own
    directory). Confirmed by measurement before this helper was written: running
    `dsx gate execute` against `examples/good-ANALYSIS-SPEC.yaml` with a fresh
    `tempfile.mkdtemp()` as `--phase-dir` fires `DSX-REP-031` ("declared entrypoint
    does not exist") and the `code` check's own findings are empty — the entrypoint
    scan silently sees nothing to scan, for every fixture, regardless of what its
    entrypoint source actually contains.

    Loads the specification with the real `dsx.loader.load` (never re-parsing the
    YAML by hand) and reads `reproducibility.entrypoint` exactly as
    `dsx/checks/code.py::check` reads it. When that value is a non-blank string and
    a file of that name exists beside `spec_path`, copies it into `tmp` at the same
    relative path, creating parent directories as needed, so `_resolve_entrypoint`
    finds it under the temporary phase directory exactly as it would under a real
    phase directory holding the fixture's own files. Returns quietly — no copy, no
    error — when the entrypoint is blank, absent, or names a file that does not
    exist beside the spec: today that is every pre-existing fixture in this corpus
    (none declares `reproducibility.entrypoint` at all — confirmed by
    `grep -n entrypoint examples/known-bad/*.yaml`, which matches only prose
    comments, never a live YAML key), so this call is a no-op for all of them and
    every pre-existing fixture's exit code at every gate point is unchanged.
    """
    spec = load(str(spec_path))
    repro = spec.get("reproducibility")
    entry = repro.get("entrypoint") if isinstance(repro, dict) else None
    if not isinstance(entry, str) or not entry.strip():
        return
    source = Path(spec_path).parent / entry
    if not source.is_file():
        return
    dest = Path(tmp) / entry
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(source, dest)


def _slugs(pattern: str, suffix: str) -> set[str]:
    return {p.name[: -len(suffix)] for p in CORPUS_DIR.glob(pattern)}


# The 256-code shipped catalogue is the source of truth for which finding codes a
# fixture's <slug>-ATTRIBUTION.yaml sidecar may name as its currently-ABSENT
# catch (D-07). It is enumerated from references/finding-codes.md — the same
# generated catalogue scripts/gen-finding-catalogue.py::collect() writes from the
# real report.add(...) call sites, so this test cannot drift from what the checks
# actually emit — rather than re-walking the dsx/ AST here. Every catalogue row is
# a Markdown table cell of the form `| `DSX-<FAMILY>-<digits>` | <severity> | ...`.
_FINDING_CATALOGUE_PATH = ROOT / "references" / "finding-codes.md"
_CATALOGUE_ROW_RE = re.compile(r"\|\s*`(DSX-[A-Z]+-\d+)`\s*\|")


def _catalogue_codes() -> "frozenset[str]":
    """Every shipped finding code, enumerated from the generated catalogue.

    Returns the exact set of `DSX-*` codes listed in references/finding-codes.md
    (256 today, pinned invariant under D-18). Parsed by table-row regex rather
    than by importing and AST-walking dsx/ so this harness stays a pure reader of
    the same generated artifact `scripts/gen-finding-catalogue.py --check` gates.
    """
    text = _FINDING_CATALOGUE_PATH.read_text(encoding="utf-8")
    return frozenset(_CATALOGUE_ROW_RE.findall(text))


# The named §6.5 backlog codes an attribution sidecar may reference as its
# absent_code even though they are NOT in the shipped catalogue — REFERENCING an
# unbuilt backlog code is the point of the miss-attribution polarity (D-05/D-07)
# and is explicitly NOT minting (D-18: the catalogue stays 256, unchanged). This
# is the allowlist-with-inline-reason house style of _INCIDENTAL_GAP_CODES
# (:64-100), one entry per §6.5 row that names a concrete unshipped code. A wildcard
# family (item 4's "DSX-ADM-*, second axis") is deliberately NOT enumerated here —
# it is a family, not a code — so no sidecar can reference it as a bare code.
# test_attribution_sidecars_reference_valid_codes_and_items asserts this set is
# disjoint from the shipped catalogue, so a code that later ships must be moved out
# of here rather than silently double-counted as both backlog and catalogue.
_SECTION_65_BACKLOG_CODES = {
    "DSX-PAR-020",  # §6.5 item 1 (brief.md:371): prior justification — unwritten, D-12a mirror pending
    "DSX-PAR-021",  # §6.5 item 1 (brief.md:371): prior sensitivity — unwritten, D-12a mirror pending
    "DSX-PAR-022",  # §6.5 item 2 (brief.md:372): prior predictive check — writable but unshipped (REV-001)
    "DSX-PAR-030",  # §6.5 item 3 (brief.md:373): convergence declarations — unwritten, D-12a mirror pending
}

# The nine §6.5 gated-backlog item ids (brief.md:369-379 table, one id per row), the
# closed set a sidecar's promotes_backlog_item must name so the D-13 entry conditions
# are machine-countable ("≥N cases naming this item" = count of sidecars). Exactly
# nine, in the brief's row order. The two ids the plan-12-01 sidecars actually use —
# item 1 and item 7 — are load-bearing strings and must match the sidecars verbatim;
# the other seven follow the same 6.5-item-<N>-<slug> shape, one per remaining row.
_SECTION_65_ITEM_IDS = frozenset({
    "6.5-item-1-prior-justification-and-sensitivity",  # brief.md:371 row 1 (DSX-PAR-020/-021)
    "6.5-item-2-prior-predictive-check",               # brief.md:372 row 2 (DSX-PAR-022, REV-001)
    "6.5-item-3-convergence-declarations",             # brief.md:373 row 3 (DSX-PAR-030)
    "6.5-item-4-bayesian-admissibility",               # brief.md:374 row 4 (DSX-ADM-*, second axis)
    "6.5-item-5-quiz-fading-mode",                     # brief.md:375 row 5 (dsx quiz, not a check)
    "6.5-item-6-ratio-metric-dilution",                # brief.md:376 row 6 (Deng & Hu 2015, REV-002 removal)
    "6.5-item-7-feature-provenance",                   # brief.md:377 row 7 (per-feature origin list)
    "6.5-item-8-magnitude-without-computed-effect",    # brief.md:378 row 8 (magnitude residual)
    "6.5-item-9-subgroup-harm-declaration",            # brief.md:379 row 9 (prescriptive subgroup harm)
})


# ── Phase 12-05 (REQ-P12-03, D-04/D-09/D-10): stratified catch rate + FPR ──────────
#
# The good-side control corpus committed by plan 12-04 (examples/good-corpus/, 12
# genuinely clean specs spanning both paradigms and all three outcome shapes) is the
# FPR denominator with resolution D-04 requires — a rate over ≥10 clean specs, not
# the old 0/1 baseline. Discovered by the same glob-on-suffix discipline as the
# known-bad corpus (never a hardcoded slug list).
GOOD_CORPUS_DIR = ROOT / "examples" / "good-corpus"

# The four fresh-tempdir artifact-stripping "noise" codes (RESEARCH Pitfall 1): each
# fires purely because the isolated `--phase-dir` a live gate run uses has none of
# the fixture's own committed sibling artifacts (data profile, figure manifest,
# narrative, evidence) to resolve against — every one names a file-path `where`, not
# a statistical-validity concept, so none is a real false positive (D-04). This is
# the documented allowlist-with-inline-reason the plan-12-04 record calls for,
# mirroring _INCIDENTAL_GAP_CODES' house style (:64-101) — and it is deliberately a
# NEW, separate constant, never read from _INCIDENTAL_GAP_CODES or
# _GOLDEN_SHIP_FINDINGS (D-09: no reported number is lifted from a stale ledger).
#
# In practice plan 12-04 took the minimal-reference / cwd-resolvable route (every
# referenced artifact resolves from the repo-root cwd, not from `--phase-dir`), so
# none of these fires against the current good-corpus and the honest FPR is 0/12.
# This allowlist is the standing guard that keeps the FPR honest if a future control
# spec ever references a sibling artifact that the fresh tempdir cannot resolve.
_FPR_TEMPDIR_NOISE_CODES = {
    "DSX-DQ-001":  "data[].assertions/profile_path resolve against a sibling DATA-PROFILE absent from the fresh tempdir",
    "DSX-CLM-031": "claims[].evidence points at a sibling file absent from the fresh tempdir",
    "DSX-FIG-001": "visuals[].artifact_path names a figure file absent from the fresh tempdir",
    "DSX-NAR-010": "narrative body/artifact absent from the fresh tempdir",
}

# Minimum ABSENT/miss-partition representation (D-10 floor): the headline is the pair
# (miss-rate, FPR), and the miss-rate is measured over the ABSENT partition — the
# live-confirmed miss cases (attribution sidecars, kind="miss", whose named absent
# code fires nowhere). Flooring that partition is what stops a 100%-present corpus
# reporting a passing calibration: a corpus with fewer than this many miss cases is a
# regression-pin dressed as detection, not a measurement of what the gate misses.
# Set to 3, matching the corpus's own ≥3 pair floor (test_corpus_holds_at_least_three_pairs).
_ABSENT_PARTITION_FLOOR = 3


def _false_positive_findings(
    findings: list[dict], noise_codes: "dict[str, str] | set[str]"
) -> "set[str]":
    """A control spec's real false-positive codes: its CRITICAL/HIGH blocking findings
    minus the documented tempdir-noise codes (each of which names a file-path `where`,
    not a statistical-validity concept — RESEARCH Pitfall 1, D-04). Takes the findings
    list and the noise allowlist as parameters so a synthetic proof exercises the
    exclusion without the filesystem or the gate — the module's two-proofs discipline
    (see `TestClassifyTargetDefectHelper`). `noise_codes` may be a set or a
    code->reason mapping; membership (`in`) reads the codes either way."""
    return {
        f["code"]
        for f in findings
        if f.get("severity") in ("CRITICAL", "HIGH")
        and f["code"] not in noise_codes
    }


def _headline(
    present: "tuple[int, int]", absent: "tuple[int, int]", fpr: "tuple[int, int]"
) -> "tuple[float, float]":
    """The headline pair (miss-rate, FPR) (D-10). miss-rate is the ABSENT partition's
    rate alone (`absent` = (misses, denominator)); FPR is the good-control-corpus rate
    (`fpr` = (false-positive specs, control-spec count)). `present` = (caught,
    denominator) is accepted for signature symmetry but MUST NOT influence the output:
    that is exactly what makes adding an already-caught target-PRESENT case
    mathematically incapable of moving the headline. Each rate floors to 0.0 on an
    empty denominator rather than raising — but the caller floors the ABSENT partition
    (`_ABSENT_PARTITION_FLOOR`) so a real run never reports over an empty miss set."""
    miss_rate = absent[0] / absent[1] if absent[1] else 0.0
    fp_rate = fpr[0] / fpr[1] if fpr[1] else 0.0
    return (miss_rate, fp_rate)


def _friction(
    blocking: "set[str] | frozenset[str]", own: "set[str] | frozenset[str]"
) -> "tuple[int, int]":
    """The per-family friction pair ``(raw, net)`` (D-11). ``blocking`` is the set of
    ship-blocking finding codes a fixture fires (CRITICAL/HIGH at ship — the same live
    set the golden test consumes); ``own`` is that fixture's own-target codes
    (``_own_target_codes(slug)``). ``raw`` is the full count of ship-blocking findings —
    the honest gross over-block, which no relabel can shrink; ``net`` is ``raw`` minus
    the ship-blocking findings that are the fixture's own declared target — the
    over-blocking BEYOND what the fixture exists to demonstrate.

    Both numbers are returned; friction is never reported net-only (D-11), so a fixture
    that over-blocks on unrelated codes cannot look clean by attributing two of them to
    itself: an inflated ``own`` shrinks ``net`` while ``raw`` stays put, and guard (c)
    (``test_target_defect_codes_fire_and_are_named``) closes the relabel path by
    requiring every ``own`` code to fire live and be publicly declared. Pure arithmetic
    over two sets, taking both as parameters so a synthetic proof exercises it without
    the filesystem or the gate (the module's two-proofs discipline)."""
    raw = len(set(blocking))
    net = raw - len(set(blocking) & set(own))
    return (raw, net)


def _friction_rate(total: int, cells: int) -> float:
    """A friction count expressed as a per-cell rate over the non-target in-profile
    (fixture × gate-point) cells (D-11): ``total`` (a raw or net over-block count)
    divided by ``cells`` (``_non_target_in_profile_cells``). Floors to 0.0 on an empty
    denominator rather than raising, matching ``_headline``'s empty-denominator floor —
    friction is a rate, not a bare count, so a larger corpus does not read as more
    friction merely for holding more fixtures."""
    return total / cells if cells else 0.0


def _non_target_in_profile_cells(
    effective: "dict[str, dict[str, frozenset[str]]]",
    slugs: "set[str] | frozenset[str]",
    points: "tuple[str, ...]",
) -> int:
    """Count the non-target in-profile (fixture × gate-point) cells that normalise the
    friction rate (D-11): every ``(slug, point)`` cell over ``slugs`` × ``points`` where
    ``effective`` (``_effective_target_map()``) has NO expected own-target code for that
    fixture at that point. These are the cells at which any blocking finding is
    over-blocking rather than the fixture's intended catch. Takes ``effective`` and the
    ``slugs``/``points`` axes as parameters so a synthetic proof exercises the count
    without the filesystem, the same testability discipline the other helpers keep."""
    return sum(
        1
        for slug in slugs
        for point in points
        if not effective.get(slug, {}).get(point)
    )


class TestKnownBadCorpus(unittest.TestCase):
    def _spec_paths(self) -> list[Path]:
        return sorted(CORPUS_DIR.glob(f"*{SPEC_SUFFIX}"))

    def _postmortem_paths(self) -> list[Path]:
        return sorted(CORPUS_DIR.glob(f"*{POSTMORTEM_SUFFIX}"))

    def _attribution_paths(self) -> list[Path]:
        return sorted(CORPUS_DIR.glob(f"*{ATTRIBUTION_SUFFIX}"))

    def _gate_findings(self, spec_path: Path, point: str) -> tuple[int, list[dict]]:
        """Run one real ``dsx gate <point>`` against one fixture and return
        ``(exit_code, findings)``.

        ``--phase-dir`` is a fresh ``tempfile.TemporaryDirectory()`` per call so
        the ``DECISIONS.jsonl`` trail write (``dsx/cli.py::cmd_gate``,
        ``root = args.phase_dir or str(path.parent)``) never lands under
        ``examples/`` — matching the module's existing ``io.StringIO()`` plus
        ``redirect_stdout``/``redirect_stderr`` capture idiom rather than a new
        pattern. Blocking output goes to stderr and passing output to stdout
        (``dsx/findings.py::emit``), so whichever stream is non-empty is the
        one holding the JSON report.

        This fresh-directory-per-call design was correct until Phase 10: no
        check had ever depended on prior gate-run state, so an empty
        temporary directory was as good a root as any other. Phase 10's
        ``prereg`` is the first check to make the decision trail a gate
        input at verify and ship (``dsx/frame/prereg.py::
        _check_content_lock``) — a ``verify`` or ``ship`` call into a
        directory with no recorded plan-time header would otherwise stop
        every fixture in the corpus at exit 2 the moment ``prereg`` is
        registered in ``GATE_PROFILES``. Seed a plan-time header for
        ``spec_path`` into ``tmp`` first whenever ``point`` needs one.

        Plan 11.1-08 (REQ-P11.1-07/08): the same fresh-temporary-directory choice
        also makes a fixture's own declared ``reproducibility.entrypoint``
        unreachable to the entrypoint check, for exactly the same reason — the
        resolve root a real ``dsx gate`` run passes to ``code.check`` is this
        temporary directory, not the fixture's own directory under
        ``examples/known-bad/``. ``_seed_entrypoint`` runs unconditionally, for
        every gate point, immediately before the plan-header seeding above —
        unlike that one, it is not scoped to ``verify``/``ship`` only, because the
        entrypoint check is registered at ``execute`` (``dsx/cli.py::GATE_PROFILES``)
        as well as ``verify``/``ship``. It is a no-op for every fixture that
        declares no entrypoint, which is every fixture in this corpus before this
        plan.
        """
        with tempfile.TemporaryDirectory() as tmp:
            _seed_entrypoint(tmp, spec_path)
            if point in ("verify", "ship"):
                seed_plan_header(tmp, spec_path)
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = cli.main(
                    ["gate", point, "--spec", str(spec_path), "--phase-dir", tmp, "--json"]
                )
            raw = err.getvalue() or out.getvalue()
            # The --json flag is silently ignored on the CheckError path — the
            # exception handler in main() runs entirely outside the emitter —
            # so a missing-plan-header CheckError (or any other exit-2 plain
            # text) would otherwise surface here as an opaque JSONDecodeError
            # rather than a readable assertion failure naming the raw text.
            # This guard is correct independently of anything Phase 10 does
            # and should stay even if every call site above always seeds.
            try:
                report = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise AssertionError(
                    f"dsx gate {point} --spec {spec_path} did not emit parseable "
                    f"JSON (exit code {code}): {raw!r}"
                ) from exc
        return code, report["findings"]

    def test_every_spec_has_a_sibling_postmortem_and_vice_versa(self):
        spec_slugs = _slugs(f"*{SPEC_SUFFIX}", SPEC_SUFFIX)
        postmortem_slugs = _slugs(f"*{POSTMORTEM_SUFFIX}", POSTMORTEM_SUFFIX)
        unmatched = spec_slugs ^ postmortem_slugs
        self.assertEqual(
            unmatched, set(),
            f"orphaned spec or post-mortem (no matching sibling): {sorted(unmatched)}",
        )

    def test_corpus_holds_at_least_three_pairs(self):
        spec_slugs = _slugs(f"*{SPEC_SUFFIX}", SPEC_SUFFIX)
        self.assertGreaterEqual(
            len(spec_slugs), 3,
            f"expected at least three known-bad pairs, found {sorted(spec_slugs)}",
        )

    def test_corpus_includes_an_interference_case_and_a_bayesian_continuous_case(self):
        spec_slugs = _slugs(f"*{SPEC_SUFFIX}", SPEC_SUFFIX)
        self.assertTrue(
            any("interference" in slug for slug in spec_slugs),
            f"no slug names an interference case: {sorted(spec_slugs)}",
        )
        self.assertTrue(
            any("bayesian" in slug and "continuous" in slug for slug in spec_slugs),
            f"no slug names a Bayesian continuous-monitoring case: {sorted(spec_slugs)}",
        )

    def test_corpus_includes_full_coverage_classes(self):
        """Phase 12 D-01: "full size" is falsifiable by *class present*, not by an
        arbitrary count. The corpus must carry at least one case in each of the
        three coverage classes named in REQ-P12-01 — a retracted paper with a
        published post-mortem, a documented p-hacking / garden-of-forking-paths
        case, and one of the operator's own prior analyses whose answer is now
        known. Asserted by class-presence over glob-discovered slugs (never a
        hardcoded slug list, never a target count), exactly like the interference
        / Bayesian-continuous predicate above.
        """
        spec_slugs = _slugs(f"*{SPEC_SUFFIX}", SPEC_SUFFIX)
        self.assertTrue(
            any("retract" in slug for slug in spec_slugs),
            f"no slug names a retracted-paper case: {sorted(spec_slugs)}",
        )
        self.assertTrue(
            any(("p-hack" in slug or "phack" in slug) for slug in spec_slugs),
            f"no slug names a documented p-hacking case: {sorted(spec_slugs)}",
        )
        self.assertTrue(
            any("operator-known" in slug for slug in spec_slugs),
            f"no slug names an operator-known-answer case: {sorted(spec_slugs)}",
        )

    def test_every_spec_loads_without_raising(self):
        specs = self._spec_paths()
        self.assertTrue(specs, "no known-bad specs found to load")
        for path in specs:
            with self.subTest(spec=path.name):
                spec = load(str(path))
                self.assertIsInstance(spec, dict)

    def test_every_spec_passes_dsx_validate(self):
        specs = self._spec_paths()
        self.assertTrue(specs, "no known-bad specs found to validate")
        for path in specs:
            with self.subTest(spec=path.name):
                out, err = io.StringIO(), io.StringIO()
                with redirect_stdout(out), redirect_stderr(err):
                    code = cli.main(["validate", "--spec", str(path)])
                self.assertEqual(code, 0, f"{path.name} failed dsx validate:\n{err.getvalue()}")

    def test_every_postmortem_names_a_catch_attribution_finding_code(self):
        postmortems = self._postmortem_paths()
        self.assertTrue(postmortems, "no known-bad post-mortems found")
        for path in postmortems:
            with self.subTest(postmortem=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertRegex(
                    text, _FINDING_CODE_RE,
                    f"{path.name} names no DSX-<LETTERS>-<digits> finding code",
                )

    def test_every_spec_blocks_only_on_its_target_defect_at_critical_threshold_points(self):
        """The corpus's positive gate guarantee, as it now stands: at each of
        `_CRITICAL_THRESHOLD_POINTS` (`plan`, `execute`), a fixture with no expected
        code for that point in `_effective_target_map()` clears it (exit 0) — today's
        behaviour, preserved exactly. A fixture with one or more expected codes for
        that point MUST block (exit 1) with every one of them among the CRITICAL
        findings — a positive proof the fixture is caught by the code it exists to
        demonstrate, not merely the absence of a negative. Replaces the old blanket
        "every fixture clears plan and execute" assertion, which a family-prefix
        allow-list could not express once a family ships more than one code (plan
        08-02, D-15).

        The expectation is drawn from both per-fixture maps at once (merge of plans
        08-02 and 09-01, 2026-08-13). `_TARGET_DEFECT_CODES` supplies the point-scoped
        single-code case — a fixture whose target code ships in the same milestone but
        whose check family is absent from the `execute` gate profile, which is
        weak-identification-mmm today (plan 07-07). `_EXPECTED_CAUGHT_DEFECTS` supplies
        the both-points multi-code case, for target checks like Phase 9's
        DSX-PAR-010/DSX-PAR-011 pair whose family is registered at every gate point
        (D-03). Both are enforced by this one assertion; asserting only one of them is
        precisely how a merge of the two phases would leave a guarantee that enforces
        neither."""
        specs = self._spec_paths()
        self.assertTrue(specs, "no known-bad specs found to gate")
        for path in specs:
            slug = path.name[: -len(SPEC_SUFFIX)]
            effective = _effective_target_map()
            for point in _CRITICAL_THRESHOLD_POINTS:
                with self.subTest(spec=path.name, point=point):
                    code, findings = self._gate_findings(path, point)
                    problems = _classify_target_defect(
                        slug, point, code, findings, effective
                    )
                    self.assertEqual(problems, [], "; ".join(problems))

    def test_weak_identification_mmm_fixture_blocks_verify_and_ship_naming_int_030(self):
        """The positive direction nothing asserts today (08-REVIEW.md WR-01).
        `_TARGET_DEFECT_CODES["weak-identification-mmm"]` carries `"verify":
        "DSX-INT-030"`, but that entry is never consumed:
        `_CRITICAL_THRESHOLD_POINTS` is `("plan", "execute")`, so `"verify"` is
        never passed to `_classify_target_defect`, and
        `test_ship_gate_findings_are_all_documented_incidental_corpus_gaps` only
        checks that findings are *allowed*, never that this one is *present*.
        This test asserts the positive direction directly against a real gate
        run, so a regression that silently stopped DSX-INT-030 firing for this
        fixture (e.g. an incorrectly-applied CR-01 fix) would turn it red
        instead of quietly shrinking the blocking set."""
        fixture = CORPUS_DIR / "weak-identification-mmm-ANALYSIS-SPEC.yaml"
        for point in ("verify", "ship"):
            with self.subTest(point=point):
                code, findings = self._gate_findings(fixture, point)
                self.assertEqual(code, 1)
                self.assertIn(
                    "DSX-INT-030",
                    {f["code"] for f in findings if f["severity"] == "CRITICAL"},
                )

    def test_post_hoc_procedure_switch_fixture_blocks_verify_and_ship_naming_pre_030(self):
        """The verify/ship positive direction for a second verify-only family
        (REQ-P10-04, ROADMAP Success Criterion 2 and 3), copying the shape of
        `test_weak_identification_mmm_fixture_blocks_verify_and_ship_naming_int_030`
        above. This dedicated test is not optional and is not redundant with
        `test_every_spec_blocks_only_on_its_target_defect_at_critical_threshold_points`:
        that generic test calls `_gate_findings` only for the points in
        `_CRITICAL_THRESHOLD_POINTS` (`"plan"`, `"execute"`), so the `"verify"`
        key this fixture's `_TARGET_DEFECT_CODES` entry carries is never
        consulted by it, and a verify-and-ship-only family would otherwise ship
        with no corpus coverage at all — exactly the gap 08-REVIEW.md WR-01
        named for `weak-identification-mmm` before the test above closed it.
        The next person adding a point-scoped family should not assume the
        generic test covers them; it does not.

        Carries all four of this task's behaviours in one method, `subTest`-ed
        over the gate point so a failure names which point regressed: (1)/(2)
        `dsx gate verify`/`ship` both exit 1 naming `DSX-PRE-030` among their
        CRITICAL findings; (3) that finding's `detail` names both the declared
        branch label and the executed procedure label (ROADMAP Success
        Criterion 2's literal requirement, asserted against a real gate run
        rather than a synthetic report); (4) `dsx gate plan`/`execute` produce
        no `DSX-PRE-` finding of any number, because `prereg` is not
        registered at those points.
        """
        fixture = CORPUS_DIR / "post-hoc-procedure-switch-ANALYSIS-SPEC.yaml"
        declared_branch = "two_proportion_z"
        executed_procedure = "fishers_exact"
        for point in ("verify", "ship"):
            with self.subTest(point=point):
                code, findings = self._gate_findings(fixture, point)
                self.assertEqual(code, 1)
                critical = {
                    f["code"]: f for f in findings if f["severity"] == "CRITICAL"
                }
                self.assertIn("DSX-PRE-030", critical)
                # Whitespace-normalized (this checkout is CRLF) rather than a
                # line-anchored comparison, matching the module's existing idiom.
                detail = " ".join(str(critical["DSX-PRE-030"]["detail"]).split())
                self.assertIn(declared_branch, detail)
                self.assertIn(executed_procedure, detail)

        for point in ("plan", "execute"):
            with self.subTest(point=point):
                _code, findings = self._gate_findings(fixture, point)
                pre_codes = {f["code"] for f in findings if f["code"].startswith("DSX-PRE-")}
                self.assertEqual(
                    pre_codes, set(),
                    f"prereg is not registered at {point!r} but fired {sorted(pre_codes)!r}",
                )

    def test_full_frame_cleaning_fixture_blocks_execute_naming_its_three_codes(self):
        """The execute-point positive direction for full-frame-cleaning (plan
        11.1-08, REQ-P11.1-07/08), copying the shape of the two dedicated
        point-scoped tests above. Not redundant with
        `test_every_spec_blocks_only_on_its_target_defect_at_critical_threshold_points`:
        that generic test already covers `execute` for this fixture (it is one of
        `_CRITICAL_THRESHOLD_POINTS`), but it does not separately prove that the
        entrypoint check produces no finding at `plan` — it only proves `plan`
        exits 0, which a `code`-family finding below the CRITICAL threshold could
        not distinguish from `code` never having run at all. This method proves
        both: (1) `dsx gate execute` exits 1 with every one of this fixture's
        recorded `_TARGET_DEFECT_CODES["full-frame-cleaning"]["execute"]` codes
        among its CRITICAL findings; (2) `dsx gate plan` produces no `DSX-CODE-`
        finding of any number, because the `code` check family is not registered
        at `plan` (`dsx/cli.py::GATE_PROFILES`).
        """
        fixture = CORPUS_DIR / "full-frame-cleaning-ANALYSIS-SPEC.yaml"
        recorded = _TARGET_DEFECT_CODES["full-frame-cleaning"]["execute"]

        code, findings = self._gate_findings(fixture, "execute")
        self.assertEqual(code, 1)
        critical = {f["code"] for f in findings if f["severity"] == "CRITICAL"}
        for expected_code in recorded:
            with self.subTest(code=expected_code):
                self.assertIn(expected_code, critical)

        _plan_code, plan_findings = self._gate_findings(fixture, "plan")
        code_family_codes = {
            f["code"] for f in plan_findings if f["code"].startswith("DSX-CODE-")
        }
        self.assertEqual(
            code_family_codes, set(),
            f"the code check is not registered at 'plan' but fired {sorted(code_family_codes)!r}",
        )

    def test_ship_gate_findings_are_all_documented_incidental_corpus_gaps(self):
        """Every CRITICAL/HIGH finding `dsx gate ship` produces against a fixture
        is either a member of the documented `_INCIDENTAL_GAP_CODES` allow-list,
        or one of that fixture's own codes in either per-fixture map
        (`_own_target_codes`: `_TARGET_DEFECT_CODES` plus `_EXPECTED_CAUGHT_DEFECTS`).

        This test failing after a later phase ships a new check is the intended
        signal, not a defect: when the code a fixture was built to motivate (e.g.
        DSX-INT-010, DSX-VAL-040) finally fires against its fixture, that code
        moves from "not shipped" to "shipped and blocking", and the corpus
        documentation (this module's constants, the fixture headers, the
        post-mortems) must move that code from incidental-gap to caught-defect.
        This assertion is what forces that edit instead of letting it rot.

        A fixture's own target code is now recognised by looking it up in
        `_TARGET_DEFECT_CODES`, rather than excluded by a family prefix, and is
        excluded from the undocumented set here rather than added to
        `_INCIDENTAL_GAP_CODES` — it is that fixture's encoded defect, not a
        corpus-completeness gap, and putting it in the incidental allow-list
        would be exactly the misuse
        `test_incidental_allowlist_names_no_slugs_own_target_code` exists to
        forbid.
        """
        specs = self._spec_paths()
        self.assertTrue(specs, "no known-bad specs found to gate")
        for path in specs:
            slug = path.name[: -len(SPEC_SUFFIX)]
            with self.subTest(spec=path.name):
                slug = path.name[: -len(SPEC_SUFFIX)]
                _code, findings = self._gate_findings(path, "ship")
                blocking = {
                    f["code"] for f in findings if f["severity"] in ("CRITICAL", "HIGH")
                }
                allowed = set(_INCIDENTAL_GAP_CODES) | set(_own_target_codes(slug))
                undocumented = blocking - allowed
                self.assertEqual(
                    undocumented, set(),
                    f"{path.name} blocks dsx gate ship on undocumented codes: "
                    f"{sorted(undocumented)} — add each to _INCIDENTAL_GAP_CODES with its "
                    "cause, or if it is this fixture's own target code, add it to "
                    "_TARGET_DEFECT_CODES and update the header/post-mortem prose to match",
                )

    def test_incidental_allowlist_names_no_slugs_own_target_code(self):
        """The machine-checkable form of the corpus's real guarantee: a fixture's
        own encoded defect can never be laundered into `_INCIDENTAL_GAP_CODES`.
        Checked per-fixture, per-gate-point against `_effective_target_map()` — so
        both `_TARGET_DEFECT_CODES` and `_EXPECTED_CAUGHT_DEFECTS` are covered —
        rather than by a family-prefix string, so a genuinely incidental code from
        the same family as another fixture's target — the case a family prefix could
        not express once a family ships more than one code — is not wrongly
        forbidden."""
        for slug, points in _effective_target_map().items():
            for point, codes in points.items():
                for code in sorted(codes):
                    with self.subTest(slug=slug, point=point, code=code):
                        self.assertNotIn(
                            code, _INCIDENTAL_GAP_CODES,
                            f"{code} is {slug}'s own target code at {point!r} but also "
                            "appears in _INCIDENTAL_GAP_CODES — a fixture's intended "
                            "defect must never be laundered into the incidental allow-list",
                        )

    def test_expected_caught_defects_keys_match_the_corpus_on_disk(self):
        """A fixture added later without an `_EXPECTED_CAUGHT_DEFECTS` entry must
        fail loudly here rather than silently falling through
        `test_every_spec_blocks_only_on_its_target_defect_at_critical_threshold_points`'s
        exit-0 branch as if its target check would never be expected to catch it."""
        disk_slugs = _slugs(f"*{SPEC_SUFFIX}", SPEC_SUFFIX)
        map_slugs = set(_EXPECTED_CAUGHT_DEFECTS)
        self.assertEqual(
            map_slugs, disk_slugs,
            f"_EXPECTED_CAUGHT_DEFECTS keys and the corpus on disk disagree: "
            f"{sorted(map_slugs ^ disk_slugs)} — every fixture must have an entry "
            "(even an empty frozenset()) and every key must name a real fixture",
        )

    def test_target_defect_codes_keys_are_a_subset_of_the_corpus_on_disk(self):
        """A subset assertion, not the equality its sibling
        (`test_expected_caught_defects_keys_match_the_corpus_on_disk`) uses:
        `_TARGET_DEFECT_CODES` is deliberately partial, holding only the
        fixtures that carry a point-scoped guarantee, whereas
        `_EXPECTED_CAUGHT_DEFECTS` must have a key for every fixture on disk.
        Protects against a renamed or removed fixture leaving an orphaned,
        silently-inert dict entry (08-REVIEW.md WR-04): `_classify_target_defect`
        would find no matching slug on disk, the renamed fixture would default
        to the clears-cleanly branch, and the corresponding point-scoped
        guarantee would disappear with no test failing."""
        disk_slugs = _slugs(f"*{SPEC_SUFFIX}", SPEC_SUFFIX)
        stale = set(_TARGET_DEFECT_CODES) - disk_slugs
        self.assertEqual(
            stale, set(),
            f"_TARGET_DEFECT_CODES names fixture(s) no longer on disk: {sorted(stale)}",
        )

    def test_no_corpus_file_repeats_a_retired_gate_overclaim(self):
        """Neither retired over-claim — the header clause asserting today's gate
        checks accept every fixture, and the post-mortem sentence asserting
        clearance at every gate and every severity threshold — can be reintroduced
        silently. Scoped to examples/known-bad/ only; this test module is where
        the retired strings legitimately live and must not match itself.

        Matched against whitespace-normalized text (runs of whitespace, including
        the mid-phrase newline in the postmortem's soft-wrapped prose, collapsed
        to a single space) so a cosmetic line-wrap can't hide a reintroduced claim
        from a plain substring check.
        """
        files = [p for p in sorted(CORPUS_DIR.rglob("*")) if p.is_file()]
        self.assertTrue(files, "no files found under examples/known-bad/")
        for path in files:
            normalized = " ".join(path.read_text(encoding="utf-8").split())
            for retired in _RETIRED_OVERCLAIMS:
                with self.subTest(file=path.name, retired=retired):
                    self.assertNotIn(
                        retired, normalized,
                        f"{path.name} still carries the retired gate over-claim {retired!r}",
                    )

    def test_no_corpus_file_misattributes_the_prior_averaged_bound(self):
        """No file under examples/known-bad/ may attribute Ville's inequality to
        Deng Theorem 1, or reconcile the two bounds' different values with the
        word "rounded". Deng Theorem 1 bounds false-discovery risk at 1/(K+1)
        (0.05 at K = 19) by a likelihood-ratio argument; Ville's inequality is a
        separate result giving 1/k (1/19 ~ 0.0526). 0.0526 is not 0.05 rounded.

        Matched against whitespace-normalized text so a cosmetic line-wrap cannot
        hide a reintroduced misattribution from a plain substring check.
        """
        files = [p for p in sorted(CORPUS_DIR.rglob("*")) if p.is_file()]
        self.assertTrue(files, "no files found under examples/known-bad/")
        for path in files:
            normalized = " ".join(path.read_text(encoding="utf-8").split())
            for retired in _RETIRED_BOUND_MISATTRIBUTIONS:
                with self.subTest(file=path.name, retired=retired):
                    self.assertNotIn(
                        retired, normalized,
                        f"{path.name} misattributes the prior-averaged bound: {retired!r}. "
                        "Deng Theorem 1 gives 1/(K+1); Ville's inequality gives 1/k.",
                    )

    def test_no_planning_document_misattributes_the_prior_averaged_bound(self):
        """The same guard over the documents that feed future phases' drafting.

        Scoped deliberately wider than this module's name: the corpus fixture was
        corrected once already, and the drift returned through the brief rather
        than through the corpus. Guarding only examples/known-bad/ would leave the
        actual source of the error unprotected.
        """
        for path in _BOUND_CLAIM_DOCUMENTS:
            with self.subTest(document=path.name):
                self.assertTrue(path.is_file(), f"{path} is missing")
                normalized = " ".join(path.read_text(encoding="utf-8").split())
                for retired in _RETIRED_BOUND_MISATTRIBUTIONS:
                    self.assertNotIn(
                        retired, normalized,
                        f"{path.name} misattributes the prior-averaged bound: {retired!r}",
                    )

    def test_bayesian_postmortem_states_the_deng_bound_and_its_value(self):
        """The negative guards above cannot tell a corrected file from one that
        dropped the claim entirely, so assert the correct form positively too.
        """
        matches = sorted(CORPUS_DIR.glob(f"*bayesian*{POSTMORTEM_SUFFIX}"))
        self.assertEqual(
            len(matches), 1,
            f"expected exactly one bayesian post-mortem, found {[p.name for p in matches]}",
        )
        normalized = " ".join(matches[0].read_text(encoding="utf-8").split())
        for required in ("1/(K+1)", "1/20 = 0.05", "Theorem 1"):
            with self.subTest(required=required):
                self.assertIn(
                    required, normalized,
                    f"{matches[0].name} no longer states {required!r} — the corrected "
                    "prior-averaged bound must remain stated, not merely un-misattributed",
                )

    def test_no_corpus_file_commits_the_theorem_1_locator_error(self):
        """Neither retired locator-error phrasing — pairing the 1/(K+1) number
        directly with the numbered "Theorem 1" — can be reintroduced silently
        into any file under examples/known-bad/ (plan 09-07, REQ-P9-03).

        Matched against whitespace-normalized text so a cosmetic line-wrap or
        this repository's CRLF checkout cannot hide a reintroduced locator
        error from a plain substring check.
        """
        files = [p for p in sorted(CORPUS_DIR.rglob("*")) if p.is_file()]
        self.assertTrue(files, "no files found under examples/known-bad/")
        for path in files:
            normalized = " ".join(path.read_text(encoding="utf-8").split())
            for retired in _RETIRED_LOCATOR_ERRORS:
                with self.subTest(file=path.name, retired=retired):
                    self.assertNotIn(
                        retired, normalized,
                        f"{path.name} still commits the Theorem 1 locator error: {retired!r}. "
                        "Theorem 1 licenses the bound under optional stopping; it does not "
                        "itself state 1/(K+1), which is unnumbered prose at Section 3.2.",
                    )

    def test_bayesian_fixture_states_the_corrected_attribution(self):
        """The negative guard above cannot tell a corrected fixture from one
        that dropped the claim entirely, so assert the correct three-part
        attribution positively too — mirroring
        test_bayesian_postmortem_states_the_deng_bound_and_its_value.
        """
        matches = sorted(CORPUS_DIR.glob(f"*bayesian*{SPEC_SUFFIX}"))
        self.assertEqual(
            len(matches), 1,
            f"expected exactly one bayesian known-bad spec, found {[p.name for p in matches]}",
        )
        normalized = " ".join(matches[0].read_text(encoding="utf-8").split())
        required = (
            "Theorem 1",
            "1/(K+1)",
            "1/20 = 0.05",
            "unnumbered prose",
            "Section 3.2",
            "locator error",
        )
        for substring in required:
            with self.subTest(required=substring):
                self.assertIn(
                    substring, normalized,
                    f"{matches[0].name} no longer states {substring!r} — the corrected "
                    "three-part attribution must remain stated, not merely un-misattributed",
                )

    def test_brief_states_the_ratio_metric_dilution_entry_condition_as_a_falsifiable_blocker(self):
        """D-18's fourth artifact: the negative guards elsewhere in this module (and in
        this test file's own retired-phrase constants) can tell that a *false* claim was
        removed, but none of them can tell a *corrected* row from one that was quietly
        dropped or softened back to the access premise research proved false (D-12:
        the Deng & Hu (2015) paper is freely public and Formula (3) in section 3.3 is
        readable today — access was never the real blocker). Without this positive
        assertion, brief.md section 6.5's ratio-metric dilution row could be edited back
        to "obtained from primary source" and nothing here would notice.

        Modeled on test_bayesian_postmortem_states_the_deng_bound_and_its_value: normalise
        with whitespace collapse (never a line-anchored regex — this checkout is CRLF) and
        assert a small, deliberately pinned set of substrings that name the claim rather
        than its exact prose.
        """
        normalized = " ".join((ROOT / "brief.md").read_text(encoding="utf-8").split())
        for required in (
            "Ratio-metric dilution for trigger analysis",
            "Formula (3)",
            "per-unit trigger and outcome data reaching the gate",
        ):
            with self.subTest(required=required):
                self.assertIn(
                    required, normalized,
                    f"brief.md no longer states {required!r} — the corrected ratio-metric "
                    "dilution entry condition must remain stated, not softened or dropped",
                )

    def test_paradigm_symmetry_audit_enumerates_both_halves(self):
        """The negative drift guards elsewhere in this module can tell a
        corrected file from a misattributing one, but none of them can tell a
        corrected document from one that dropped the symmetry claim entirely.
        Prose asserting that DSX-PAR-010/DSX-PAR-011 are equally cheap to
        satisfy dishonestly, with nothing underneath it, is exactly the
        failure mode brief D-12 does not survive (D-15).

        This test reads references/paradigm-symmetry.md and compares it
        against dsx.frame.paradigm._MONITORING_DISCIPLINE — the code's real
        clearing conditions — rather than against a hard-coded literal, so a
        clearing declaration added to the code without being added to the
        audit fails here instead of leaving the audit a quietly false claim
        about the tool's behaviour.
        """
        self.assertTrue(SYMMETRY_AUDIT_PATH.is_file(), f"{SYMMETRY_AUDIT_PATH} is missing")
        normalized = " ".join(SYMMETRY_AUDIT_PATH.read_text(encoding="utf-8").split())

        for paradigm, (code, clearing_fields) in _MONITORING_DISCIPLINE.items():
            with self.subTest(paradigm=paradigm, required=code):
                self.assertIn(
                    code, normalized,
                    f"{SYMMETRY_AUDIT_PATH.name} no longer names {code!r}, the finding "
                    f"code _MONITORING_DISCIPLINE maps to paradigm {paradigm!r}",
                )
            for field in clearing_fields:
                with self.subTest(paradigm=paradigm, required=field):
                    self.assertIn(
                        field, normalized,
                        f"{SYMMETRY_AUDIT_PATH.name} no longer names the clearing "
                        f"declaration {field!r} for paradigm {paradigm!r} — a clearing "
                        "declaration added to the code without being added to the audit "
                        "is exactly the drift this test exists to catch",
                    )

        for honest_fix in _CONTROLLED_PEEKING_POLICIES:
            with self.subTest(required=honest_fix):
                self.assertIn(
                    honest_fix, normalized,
                    f"{SYMMETRY_AUDIT_PATH.name} no longer names {honest_fix!r} as one "
                    "of the three controlled peeking policies the honest fix names",
                )

        for reference_value in _SYMMETRY_AUDIT_REFERENCE_VALUES:
            with self.subTest(required=reference_value):
                self.assertIn(
                    reference_value, normalized,
                    f"{SYMMETRY_AUDIT_PATH.name} no longer states the reference value "
                    f"{reference_value!r}",
                )

    def test_attribution_sidecars_reference_valid_codes_and_items(self):
        """D-07 sibling-integrity: every `<slug>-ATTRIBUTION.yaml` names a real
        slug, an absent_code in the validated union (the 256 shipped catalogue
        codes ∪ the named §6.5 backlog codes), and a promotes_backlog_item that is
        one of the nine §6.5 item ids — validated at schema time, before any live
        gate check runs (T-12-07). A hallucinated or misspelled absent_code, or a
        promotes_backlog_item outside the nine ids, fails here.

        Discovery is by glob on the slug (`*-ATTRIBUTION.yaml`, D-06) and every
        sidecar is parsed with `dsx.loader.load` — no hardcoded slug list, no
        `import yaml`, no hand-rolled parser (D-01). The sibling-spec check is a
        SUBSET (`attribution_slugs ⊆ spec_slugs`), not the symmetric difference the
        spec/postmortem pairing uses (`:646`), because sidecars are optional per
        D-03 (present for miss/backlog-promotion cases, absent for pure-catch
        cases) — a spec with no sidecar is fine, a sidecar with no spec is not.
        """
        catalogue = _catalogue_codes()
        self.assertTrue(catalogue, "no finding codes enumerated from the catalogue")
        # Referencing an unbuilt §6.5 backlog code is the miss-attribution point and
        # is NOT minting (D-07/D-18): the backlog set must stay disjoint from the
        # shipped catalogue, so a code that later ships is moved out of the backlog
        # allow-list rather than silently counted as both.
        self.assertEqual(
            _SECTION_65_BACKLOG_CODES & catalogue, set(),
            f"§6.5 backlog codes overlap the shipped catalogue: "
            f"{sorted(_SECTION_65_BACKLOG_CODES & catalogue)} — a shipped code must be "
            "removed from _SECTION_65_BACKLOG_CODES, not referenced as an unbuilt backlog code",
        )
        self.assertEqual(
            len(_SECTION_65_ITEM_IDS), 9,
            f"_SECTION_65_ITEM_IDS must have exactly nine members (one per §6.5 row), "
            f"found {len(_SECTION_65_ITEM_IDS)}: {sorted(_SECTION_65_ITEM_IDS)}",
        )
        validated_union = catalogue | _SECTION_65_BACKLOG_CODES

        spec_slugs = _slugs(f"*{SPEC_SUFFIX}", SPEC_SUFFIX)
        attribution_slugs = _slugs(f"*{ATTRIBUTION_SUFFIX}", ATTRIBUTION_SUFFIX)
        self.assertTrue(attribution_slugs, "no attribution sidecars found to validate")
        orphaned = attribution_slugs - spec_slugs
        self.assertEqual(
            orphaned, set(),
            f"attribution sidecar(s) name a slug with no sibling ANALYSIS-SPEC: "
            f"{sorted(orphaned)} — a sidecar must pair with a real fixture",
        )

        for path in self._attribution_paths():
            with self.subTest(sidecar=path.name):
                data = load(str(path))
                self.assertIsInstance(
                    data, dict, f"{path.name} did not load as a mapping"
                )
                for key in ("absent_code", "promotes_backlog_item"):
                    self.assertIn(
                        key, data,
                        f"{path.name} is missing required key {key!r} (D-07 schema)",
                    )
                self.assertIn(
                    data["absent_code"], validated_union,
                    f"{path.name} names absent_code {data['absent_code']!r} outside the "
                    "validated union (256 catalogue codes ∪ named §6.5 backlog codes) — "
                    "a hallucinated or misspelled code is rejected before any live check",
                )
                self.assertIn(
                    data["promotes_backlog_item"], _SECTION_65_ITEM_IDS,
                    f"{path.name} names promotes_backlog_item "
                    f"{data['promotes_backlog_item']!r}, not one of the nine §6.5 item ids: "
                    f"{sorted(_SECTION_65_ITEM_IDS)}",
                )
                kind = data.get("kind", "miss")
                self.assertIn(
                    kind, ("miss", "caught"),
                    f"{path.name} has kind {kind!r}; the D-07 schema allows only "
                    "'miss' (default) or 'caught'",
                )

    def test_attribution_tags_are_falsifiable_against_live_gate(self):
        """D-08 falsifiability (anti-laundering): each attribution tag is checked
        against a LIVE gate run, so it cannot lie. For every sidecar, build the
        CRITICAL union `all_critical` across ALL FOUR gate points
        (plan/execute/verify/ship) from `self._gate_findings(spec_path, point)` —
        the exact same fresh-tempdir live source the golden corpus tests use
        (`:580`), never a lifted ledger (`_INCIDENTAL_GAP_CODES` /
        `_GOLDEN_SHIP_FINDINGS` are deliberately NOT read here, T-12-01).

        - `kind == "miss"`: the named absent_code must fire NOWHERE CRITICAL across
          the union — a miss whose code actually fires is a laundered catch and a
          hard failure (T-12-05).
        - `kind == "caught"`: the named code MUST fire CRITICAL somewhere in the
          union.

        A named §6.5 backlog code that is not in the shipped catalogue is inherently
        absent live — it can never appear in `all_critical` — so it satisfies the
        miss assertion by construction and can NEVER be credited as a catch (D-08:
        "we'd catch it with a code we haven't written" inflates nothing). That falls
        out of the two assertions directly: a caught tag naming an unshipped code
        fails the `in all_critical` check, exactly as intended.
        """
        sidecars = self._attribution_paths()
        self.assertTrue(sidecars, "no attribution sidecars found to falsify")
        for path in sidecars:
            slug = path.name[: -len(ATTRIBUTION_SUFFIX)]
            data = load(str(path))
            absent_code = data["absent_code"]
            kind = data.get("kind", "miss")
            spec_path = CORPUS_DIR / f"{slug}{SPEC_SUFFIX}"
            with self.subTest(sidecar=path.name, kind=kind):
                self.assertTrue(
                    spec_path.is_file(),
                    f"{path.name} has no sibling spec {spec_path.name} to gate against",
                )
                all_critical: set[str] = set()
                for point in ("plan", "execute", "verify", "ship"):
                    _code, findings = self._gate_findings(spec_path, point)
                    all_critical |= {
                        f["code"] for f in findings if f.get("severity") == "CRITICAL"
                    }
                if kind == "miss":
                    self.assertNotIn(
                        absent_code, all_critical,
                        f"{path.name} tags {absent_code!r} as a miss, but it fires CRITICAL "
                        f"live somewhere across plan/execute/verify/ship "
                        f"({sorted(all_critical)}) — a code that fires is a laundered catch, "
                        "not a miss",
                    )
                else:  # kind == "caught"
                    self.assertIn(
                        absent_code, all_critical,
                        f"{path.name} tags {absent_code!r} as caught, but it never fires "
                        f"CRITICAL live across plan/execute/verify/ship "
                        f"({sorted(all_critical)}) — a hypothetical/unshipped code can never "
                        "be credited as a catch",
                    )

    def test_stratified_catch_rate_and_fpr_report(self):
        """The measurement step (REQ-P12-03, D-04/D-09/D-10): a stratified catch rate
        with independent PRESENT/ABSENT denominators, an FPR over the good-control
        corpus with tempdir-noise resolved, and the headline pair (miss-rate, FPR)
        with a floored ABSENT partition and a target-present-invariance proof.

        Every number is computed LIVE in this method via `self._gate_findings`
        (fresh-tempdir) and `_classify_target_defect` — the same live source the
        golden and falsifiability tests use — and never lifted from
        `_INCIDENTAL_GAP_CODES` or `_GOLDEN_SHIP_FINDINGS` (D-09), neither of which is
        read here.

        Stratification (D-10):
          - PRESENT partition: every (slug, gate-point) cell that `_effective_target_map()`
            expects to fire a target code; caught iff `_classify_target_defect` finds no
            problem (exit 1 with every expected code among the CRITICAL findings).
          - ABSENT partition: the live-confirmed miss cases — attribution sidecars with
            kind "miss" whose named absent code fires nowhere CRITICAL across all four
            gate points (the falsifiability guarantee plan 12-03 already enforces). Each
            is an uncaught defect, attributable to a specific absent code.

        The headline is the pair (miss-rate over the ABSENT partition, FPR over the
        good-control corpus), computed through `_headline`, whose miss-rate depends on
        the ABSENT partition alone — so injecting an already-caught target-PRESENT case
        is mathematically incapable of moving it. The ABSENT partition is FLOORED
        (`_ABSENT_PARTITION_FLOOR`): a 100%-present corpus with too few miss cases
        cannot report a passing calibration.
        """
        # ── Task 1: FPR over the good-control corpus, tempdir-noise resolved ──────────
        good_specs = sorted(GOOD_CORPUS_DIR.glob(f"*{SPEC_SUFFIX}"))
        self.assertGreaterEqual(
            len(good_specs), 10,
            f"the FPR denominator must have resolution (>=10 clean control specs), "
            f"found {len(good_specs)} under {GOOD_CORPUS_DIR}",
        )
        fpr_blockers: "dict[str, list[str]]" = {}
        for path in good_specs:
            _code, findings = self._gate_findings(path, "ship")
            real_fp = _false_positive_findings(findings, _FPR_TEMPDIR_NOISE_CODES)
            if real_fp:
                fpr_blockers[path.name[: -len(SPEC_SUFFIX)]] = sorted(real_fp)
        fpr_num, fpr_denom = len(fpr_blockers), len(good_specs)

        # ── Task 2: PRESENT-partition catch rate (live, per-case, attributable) ───────
        effective = _effective_target_map()
        present_denom = 0
        present_caught = 0
        present_detail: "dict[tuple[str, str], tuple[list[str], bool]]" = {}
        for path in self._spec_paths():
            slug = path.name[: -len(SPEC_SUFFIX)]
            for point in _CRITICAL_THRESHOLD_POINTS:
                expected = effective.get(slug, {}).get(point)
                if not expected:
                    continue
                present_denom += 1
                code, findings = self._gate_findings(path, point)
                problems = _classify_target_defect(slug, point, code, findings, effective)
                caught = problems == []
                present_caught += int(caught)
                present_detail[(slug, point)] = (sorted(expected), caught)
        self.assertGreater(
            present_denom, 0, "no PRESENT-partition cells found in the effective target map"
        )

        # ── Task 2: ABSENT-partition miss-rate (live-confirmed miss tags) ─────────────
        absent_denom = 0
        absent_misses = 0
        absent_detail: "dict[str, tuple[str, bool]]" = {}
        for sidecar in self._attribution_paths():
            data = load(str(sidecar))
            if data.get("kind", "miss") != "miss":
                continue
            absent_denom += 1
            slug = sidecar.name[: -len(ATTRIBUTION_SUFFIX)]
            spec_path = CORPUS_DIR / f"{slug}{SPEC_SUFFIX}"
            absent_code = data["absent_code"]
            # Each ABSENT-partition case is attributable to a specific code.
            self.assertRegex(absent_code, _FINDING_CODE_RE)
            all_critical: set[str] = set()
            for point in ("plan", "execute", "verify", "ship"):
                _code, findings = self._gate_findings(spec_path, point)
                all_critical |= {
                    f["code"] for f in findings if f.get("severity") == "CRITICAL"
                }
            missed = absent_code not in all_critical
            absent_misses += int(missed)
            absent_detail[slug] = (absent_code, missed)

        # Floor the ABSENT partition (D-10): a 100%-present corpus cannot pass as a
        # calibration. The floor is a real minimum-representation gate — a
        # zero-representation corpus is rejected by construction (floor > 0).
        self.assertGreater(
            _ABSENT_PARTITION_FLOOR, 0,
            "the ABSENT-partition floor must be a positive minimum-representation "
            "requirement, or a 100%-present corpus would pass for free",
        )
        self.assertGreaterEqual(
            absent_denom, _ABSENT_PARTITION_FLOOR,
            f"the ABSENT/miss partition has {absent_denom} case(s), below the floor "
            f"{_ABSENT_PARTITION_FLOOR}: a corpus with too few miss cases is a "
            "regression-pin dressed as detection, not a calibration (D-10)",
        )

        # ── Headline = (miss-rate over ABSENT, FPR over good corpus), computed live ───
        present = (present_caught, present_denom)
        absent = (absent_misses, absent_denom)
        fpr = (fpr_num, fpr_denom)
        headline = _headline(present, absent, fpr)
        miss_rate, fp_rate = headline
        self.assertEqual(
            miss_rate, absent_misses / absent_denom,
            "the headline miss-rate must be the ABSENT partition's rate alone (D-10)",
        )
        self.assertEqual(
            fp_rate, fpr_num / fpr_denom,
            "the headline FPR must be the live good-control-corpus rate (D-04)",
        )

        # ── Invariance (D-10): an already-caught target-PRESENT case cannot move it ───
        present_plus = (present_caught + 1, present_denom + 1)  # one synthetic easy catch
        headline_after = _headline(present_plus, absent, fpr)
        self.assertEqual(
            headline, headline_after,
            "injecting a target-PRESENT case moved the (miss-rate, FPR) headline — "
            "adding easy catches must be mathematically incapable of moving it (D-10)",
        )

        # Both partitions carry their own, independent, non-empty denominator.
        self.assertGreater(present_denom, 0)
        self.assertGreater(absent_denom, 0)

    def test_friction_uses_the_same_live_findings_as_golden(self):
        """Friction (guard b, D-11b/D-09): the per-family over-blocking column is
        computed from the SAME live ``self._gate_findings(slug, "ship")`` set the
        golden ship-completeness test
        (``test_ship_gate_findings_are_all_documented_incidental_corpus_gaps``, :1034)
        consumes — never a number lifted from ``_INCIDENTAL_GAP_CODES``,
        ``_GOLDEN_SHIP_FINDINGS`` or any stale ledger. Every raw/net pair here is
        recomputed live and asserted equal to the value derived from the identical
        live blocking set, so a hardcoded or lifted number would break the equality.

        Both raw and net are surfaced and both are expressed as a per-family rate over
        the non-target in-profile (fixture × gate-point) cells (D-11): reporting net
        alone is forbidden, because a fixture that over-blocks on unrelated codes could
        otherwise look clean by attributing two of them to itself.
        """
        specs = self._spec_paths()
        self.assertTrue(specs, "no known-bad specs found to gate")
        total_raw = 0
        total_net = 0
        for path in specs:
            slug = path.name[: -len(SPEC_SUFFIX)]
            with self.subTest(spec=path.name):
                _code, findings = self._gate_findings(path, "ship")
                # The exact blocking set the golden test derives (:1035) — the single
                # live source both this friction column and the golden test share.
                blocking = {
                    f["code"] for f in findings if f["severity"] in ("CRITICAL", "HIGH")
                }
                own = _own_target_codes(slug)
                raw, net = _friction(blocking, own)
                # Tied to the live set: raw is its size; net removes only this
                # fixture's own-target codes. A lifted/hardcoded raw or net would not
                # equal this live recomputation.
                self.assertEqual(raw, len(blocking))
                self.assertEqual(net, len(blocking - own))
                self.assertLessEqual(net, raw)
                total_raw += raw
                total_net += net
        # The corpus DOES over-block at ship (documented incidental corpus gaps), so
        # the per-family equalities above are exercised against non-empty live sets — a
        # zero here would mean friction was lifted from a constant, not measured live.
        self.assertGreater(
            total_raw, 0,
            "expected non-zero live ship-blocking friction across the corpus; a zero "
            "means friction was lifted from a constant rather than the live gate",
        )
        # Friction is a rate over the non-target in-profile (fixture × gate-point)
        # cells, not a bare count (D-11): cells the corpus is NOT expected to fire its
        # own target at, across the in-profile CRITICAL-threshold gate points.
        effective = _effective_target_map()
        slugs = {p.name[: -len(SPEC_SUFFIX)] for p in specs}
        cells = _non_target_in_profile_cells(effective, slugs, _CRITICAL_THRESHOLD_POINTS)
        self.assertGreater(
            cells, 0, "no non-target in-profile cells to normalise friction over"
        )
        raw_rate = _friction_rate(total_raw, cells)
        net_rate = _friction_rate(total_net, cells)
        # BOTH rates are surfaced (net-only is forbidden, D-11) and net never exceeds raw.
        self.assertEqual(raw_rate, total_raw / cells)
        self.assertEqual(net_rate, total_net / cells)
        self.assertLessEqual(net_rate, raw_rate)

    def test_target_defect_codes_fire_and_are_named(self):
        """Incidental→own relabel closure (guard c, D-11c / T-12-04): every entry in
        ``_TARGET_DEFECT_CODES`` — every code the friction column subtracts from raw to
        reach net — must be positively verified two ways, so a code cannot be quietly
        demoted from friction into a fixture's own-target map to shrink net without
        publicly declaring it the intended defect:

          1. It FIRES live as a blocking finding at its mapped gate point — CRITICAL at
             ``plan``/``execute``, CRITICAL or HIGH at ``verify``/``ship`` (the gate
             thresholds of references/finding-codes.md). This closes the fabricated /
             never-fires relabel: an own-target code that does not actually block is
             rejected.
          2. It is NAMED as an intended defect in that slug's POSTMORTEM.md (or, when a
             later phase adds one, its ATTRIBUTION.yaml). One documented cross-fixture
             exception is allowed: a code that is a second fixture's PRIMARY declared
             target — DSX-INT-030 is triggering-dilution's own code, recorded as a
             secondary key on weak-identification-mmm (see the ``_TARGET_DEFECT_CODES``
             comment) — is accepted when it is named in some corpus postmortem/
             attribution, because it is still publicly declared an intended defect, not
             a silent relabel.
        """
        corpus_docs = "\n".join(
            p.read_text(encoding="utf-8")
            for p in self._postmortem_paths() + self._attribution_paths()
        )
        for slug, points in _TARGET_DEFECT_CODES.items():
            spec_path = CORPUS_DIR / f"{slug}{SPEC_SUFFIX}"
            own_docs_parts = []
            for suffix in (POSTMORTEM_SUFFIX, ATTRIBUTION_SUFFIX):
                doc = CORPUS_DIR / f"{slug}{suffix}"
                if doc.is_file():
                    own_docs_parts.append(doc.read_text(encoding="utf-8"))
            own_docs = "\n".join(own_docs_parts)
            for point, value in points.items():
                codes = {value} if isinstance(value, str) else set(value)
                blocking_severities = (
                    ("CRITICAL",)
                    if point in _CRITICAL_THRESHOLD_POINTS
                    else ("CRITICAL", "HIGH")
                )
                _code, findings = self._gate_findings(spec_path, point)
                fired = {
                    f["code"]
                    for f in findings
                    if f.get("severity") in blocking_severities
                }
                for code in sorted(codes):
                    with self.subTest(slug=slug, point=point, code=code):
                        self.assertIn(
                            code, fired,
                            f"{slug}'s own-target code {code} does not fire as a "
                            f"blocking finding ({blocking_severities}) at {point!r} — a "
                            "code that never blocks cannot be credited as this fixture's "
                            "own defect and subtracted from friction (D-11c)",
                        )
                        self.assertTrue(
                            code in own_docs or code in corpus_docs,
                            f"{slug}'s own-target code {code} is named in no "
                            "postmortem/attribution — an own-target code must be "
                            "publicly declared an intended defect, never a silent "
                            "relabel of incidental over-blocking (D-11c)",
                        )


class TestClassifyTargetDefectHelper(unittest.TestCase):
    """Proves `_classify_target_defect` fires against fabricated inputs, independent
    of the filesystem and the real gate — the module's own two-proofs discipline
    (tests/test_frame_boundary.py::TestFrameImportBoundary): a test that only ever
    scans real fixtures can never fail while the map is empty of a given code, and
    therefore enforces nothing on its own."""

    def test_classify_target_defect_fires_when_the_targeted_code_is_absent(self):
        fake_map = {"fixture-a": {"plan": "DSX-XXX-010"}}
        present = [{"code": "DSX-XXX-010", "severity": "CRITICAL"}]
        self.assertEqual(
            _classify_target_defect("fixture-a", "plan", 1, present, fake_map), []
        )
        absent = [{"code": "DSX-YYY-001", "severity": "CRITICAL"}]
        problems = _classify_target_defect("fixture-a", "plan", 1, absent, fake_map)
        self.assertNotEqual(problems, [])

    def test_classify_target_defect_permits_a_same_family_incidental_code_on_an_untargeted_fixture(self):
        fake_map = {"fixture-a": {"plan": "DSX-XXX-010"}}
        # DSX-XXX-040 shares fixture-a's family prefix "DSX-XXX-", but fixture-b has
        # no entry in fake_map at "plan" — it must clear cleanly (exit 0), and the
        # finding list is irrelevant to that classification. This is the precise case
        # a family-prefix string list could not express: it can only ever forbid or
        # permit a whole family, never distinguish one fixture's target from another
        # fixture's incidental finding in the same family.
        findings = [{"code": "DSX-XXX-040", "severity": "CRITICAL"}]
        problems = _classify_target_defect("fixture-b", "plan", 0, findings, fake_map)
        self.assertEqual(problems, [])


class TestOwnTargetCodesFlattening(unittest.TestCase):
    """Proves `_own_target_codes` flattens a multi-code value into its individual
    code strings, against a fabricated map — independent of the filesystem, the
    real gate and the module's own constants (plan 11.1-08, matching the
    two-proofs discipline `TestClassifyTargetDefectHelper` above already sets for
    `_classify_target_defect`)."""

    def test_multi_code_value_flattens_to_individual_codes(self):
        fake_target_map = {
            "fixture-a": {"execute": frozenset({"DSX-XXX-010", "DSX-XXX-011"})}
        }
        own = _own_target_codes("fixture-a", target_map=fake_target_map, expected_map={})
        self.assertEqual(own, frozenset({"DSX-XXX-010", "DSX-XXX-011"}))

    def test_single_string_value_still_returns_that_one_code(self):
        fake_target_map = {"fixture-b": {"plan": "DSX-YYY-020"}}
        own = _own_target_codes("fixture-b", target_map=fake_target_map, expected_map={})
        self.assertEqual(own, frozenset({"DSX-YYY-020"}))

    def test_both_maps_contribute_and_a_second_non_critical_key_is_still_flattened(self):
        # Mirrors full-frame-cleaning's own shape: one multi-code entry at
        # "execute" plus a second, non-critical-threshold-point key ("ship")
        # holding a single HIGH-severity code that cannot live in the
        # CRITICAL-only-checked point set.
        fake_target_map = {
            "fixture-c": {
                "execute": frozenset({"DSX-CODE-020", "DSX-CODE-021"}),
                "ship": "DSX-ML-090",
            }
        }
        fake_expected_map = {"fixture-c": frozenset({"DSX-PAR-010"})}
        own = _own_target_codes(
            "fixture-c", target_map=fake_target_map, expected_map=fake_expected_map
        )
        self.assertEqual(
            own, frozenset({"DSX-CODE-020", "DSX-CODE-021", "DSX-ML-090", "DSX-PAR-010"})
        )

    def test_unmapped_slug_returns_an_empty_frozenset(self):
        own = _own_target_codes("no-such-slug", target_map={}, expected_map={})
        self.assertEqual(own, frozenset())


class TestSeedEntrypoint(unittest.TestCase):
    """Proves `_seed_entrypoint` against real specification fixtures on disk —
    independent of `_gate_findings` and the real gate (plan 11.1-08,
    REQ-P11.1-07/08)."""

    def test_no_declared_entrypoint_leaves_the_temporary_directory_empty(self):
        # weak-identification-mmm declares no reproducibility.entrypoint at all
        # (confirmed: no fixture in this corpus does, before this plan) — seeding
        # must be a true no-op, not merely "does not raise".
        spec_path = CORPUS_DIR / "weak-identification-mmm-ANALYSIS-SPEC.yaml"
        with tempfile.TemporaryDirectory() as tmp:
            _seed_entrypoint(tmp, spec_path)
            self.assertEqual(
                list(Path(tmp).iterdir()), [],
                "_seed_entrypoint copied something for a fixture with no declared "
                "entrypoint",
            )

    def test_declared_entrypoint_is_copied_to_the_same_relative_path(self):
        # A synthetic spec + entrypoint pair, independent of any real corpus
        # fixture, so this test does not depend on what a later task in this
        # plan commits.
        with tempfile.TemporaryDirectory() as spec_dir, tempfile.TemporaryDirectory() as tmp:
            entry_path = Path(spec_dir) / "synthetic-entrypoint.py"
            entry_path.write_text("# synthetic entrypoint for _seed_entrypoint's own test\n")
            spec_path = Path(spec_dir) / "synthetic-ANALYSIS-SPEC.yaml"
            spec_path.write_text(
                "spec_version: 1\n"
                "title: synthetic\n"
                "question_type: descriptive\n"
                "reproducibility:\n"
                "  entrypoint: synthetic-entrypoint.py\n"
            )
            _seed_entrypoint(tmp, spec_path)
            copied = Path(tmp) / "synthetic-entrypoint.py"
            self.assertTrue(copied.is_file(), f"{copied} was not seeded")
            self.assertEqual(copied.read_text(), entry_path.read_text())


class TestStratifiedHeadlineHelpers(unittest.TestCase):
    """Filesystem-independent proofs of the FPR noise-exclusion and the
    headline-invariance arithmetic (plan 12-05), matching the two-proofs discipline
    `TestClassifyTargetDefectHelper` sets for `_classify_target_defect`.

    These are the load-bearing guards: the live
    `test_stratified_catch_rate_and_fpr_report` runs against the plan-12-04
    good-corpus, which is clean by construction (every reference cwd-resolvable, so a
    fresh-tempdir ship run fires nothing) — so the live FPR is 0/12 whether or not the
    tempdir-noise exclusion is wired, and every measured rate is degenerate (all
    catches present, all misses absent). A test that only ever scanned that corpus
    could therefore never go red while the exclusion or the invariance was wrong.
    These fabricated-input proofs supply the non-degenerate RED signal the plan's
    RED→GREEN steps describe."""

    def test_false_positive_findings_excludes_documented_tempdir_noise(self):
        # A block whose `where` names a file path (evidence/figure/profile/narrative)
        # is tempdir noise and is NOT counted as a false positive; only the genuine
        # statistical-validity finding survives.
        findings = [
            {"code": "DSX-DQ-001", "severity": "CRITICAL", "where": "good-DATA-PROFILE.yaml"},
            {"code": "DSX-CLM-031", "severity": "HIGH", "where": "RESULTS.md#claim-1"},
            {"code": "DSX-FIG-001", "severity": "HIGH", "where": "fig-1.svg"},
            {"code": "DSX-NAR-010", "severity": "HIGH", "where": "NARRATIVE.md"},
            {"code": "DSX-STA-002", "severity": "CRITICAL", "where": "analysis.test"},
        ]
        self.assertEqual(
            _false_positive_findings(findings, _FPR_TEMPDIR_NOISE_CODES),
            {"DSX-STA-002"},
        )

    def test_naive_fpr_counting_noise_is_spuriously_higher_than_the_excluded_fpr(self):
        # The exact contrast the plan's RED step names: counting the tempdir-noise
        # codes (empty allowlist) inflates the false-positive set; the documented
        # exclusion removes them, leaving only the real statistical-validity finding.
        findings = [
            {"code": "DSX-DQ-001", "severity": "CRITICAL"},
            {"code": "DSX-CLM-031", "severity": "HIGH"},
            {"code": "DSX-STA-002", "severity": "CRITICAL"},
        ]
        naive = _false_positive_findings(findings, set())
        excluded = _false_positive_findings(findings, _FPR_TEMPDIR_NOISE_CODES)
        self.assertEqual(len(naive), 3)
        self.assertEqual(excluded, {"DSX-STA-002"})
        self.assertLess(len(excluded), len(naive))

    def test_headline_is_the_absent_miss_rate_and_fpr_pair(self):
        # miss-rate = ABSENT partition alone (1/4); FPR = good-corpus rate (3/10).
        self.assertEqual(_headline((2, 5), (1, 4), (3, 10)), (0.25, 0.3))

    def test_headline_is_invariant_to_adding_a_target_present_case(self):
        present, absent, fpr = (2, 5), (1, 4), (1, 10)
        base = _headline(present, absent, fpr)
        plus = _headline((present[0] + 1, present[1] + 1), absent, fpr)
        self.assertEqual(
            base, plus,
            "adding a target-PRESENT case changed the headline — easy catches must "
            "be incapable of moving (miss-rate, FPR) (D-10)",
        )


class TestFrictionArithmetic(unittest.TestCase):
    """Filesystem-independent proof of the friction arithmetic (guard a, D-11),
    matching the two-proofs discipline ``TestClassifyTargetDefectHelper`` and
    ``TestStratifiedHeadlineHelpers`` set: the live
    ``test_friction_uses_the_same_live_findings_as_golden`` runs against the real
    corpus, but a test that only ever scans real fixtures could never go red while the
    raw/net arithmetic was wrong. These fabricated-input proofs supply that RED signal.
    """

    def test_net_is_raw_minus_own_and_both_are_surfaced(self):
        # A fabricated per-family ship-blocking findings dict — no filesystem, no gate:
        # each family maps (its blocking codes, its own-target codes).
        fabricated = {
            "fixture-a": ({"DSX-AAA-001", "DSX-BBB-002", "DSX-CCC-003"}, {"DSX-AAA-001"}),
            "fixture-b": ({"DSX-DDD-004", "DSX-EEE-005"}, {"DSX-DDD-004", "DSX-EEE-005"}),
            "fixture-c": ({"DSX-FFF-006"}, set()),
        }
        for slug, (blocking, own) in fabricated.items():
            with self.subTest(slug=slug):
                result = _friction(blocking, own)
                # BOTH raw and net are surfaced — never net alone (D-11).
                self.assertEqual(len(result), 2)
                raw, net = result
                self.assertEqual(raw, len(blocking))
                self.assertEqual(net, raw - len(blocking & own))
                self.assertLessEqual(net, raw)
        # A worked case: 3 blocking, 1 own -> raw 3, net 2.
        self.assertEqual(_friction({"X", "Y", "Z"}, {"X"}), (3, 2))
        # Fully-own fixture: net collapses to 0, raw stays the gross count.
        self.assertEqual(_friction({"X", "Y"}, {"X", "Y"}), (2, 0))

    def test_relabeling_incidental_to_own_shrinks_net_but_not_raw(self):
        # The exact laundering path guard (c) closes, proven arithmetically here:
        # attributing an incidental block to the fixture's own target shrinks NET but
        # leaves RAW untouched — which is why both must be reported (D-11). Reporting
        # net alone would hide the over-blocking a relabel conceals.
        blocking = {"DSX-AAA-001", "DSX-BBB-002", "DSX-CCC-003"}
        honest_own = {"DSX-AAA-001"}
        inflated_own = {"DSX-AAA-001", "DSX-BBB-002"}  # laundered one incidental as own
        raw_h, net_h = _friction(blocking, honest_own)
        raw_i, net_i = _friction(blocking, inflated_own)
        self.assertEqual(raw_h, raw_i)  # raw is stable — a relabel cannot shrink it
        self.assertLess(net_i, net_h)  # net shrinks when an incidental is relabelled own

    def test_friction_rate_normalises_over_non_target_cells_and_floors_on_empty(self):
        # Friction is a RATE over non-target in-profile cells, not a bare count (D-11).
        self.assertEqual(_friction_rate(6, 3), 2.0)
        self.assertEqual(_friction_rate(0, 5), 0.0)
        # Empty denominator floors to 0.0 rather than raising (mirrors `_headline`).
        self.assertEqual(_friction_rate(4, 0), 0.0)

    def test_non_target_in_profile_cells_counts_only_untargeted_cells(self):
        # Over a fabricated effective target map, a (slug, point) cell counts iff the
        # fixture has NO expected own-target code there — the friction denominator.
        effective = {
            "fixture-a": {"plan": frozenset({"DSX-AAA-001"})},  # targeted at plan only
            "fixture-b": {},  # untargeted at both points
        }
        slugs = {"fixture-a", "fixture-b", "fixture-c"}  # fixture-c absent from the map
        points = ("plan", "execute")
        # fixture-a: execute (plan is targeted) = 1; fixture-b: 2; fixture-c: 2 -> 5.
        self.assertEqual(_non_target_in_profile_cells(effective, slugs, points), 5)


if __name__ == "__main__":
    unittest.main()
