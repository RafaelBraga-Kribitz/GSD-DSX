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
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dsx import cli  # noqa: E402
from dsx.frame.paradigm import _MONITORING_DISCIPLINE  # noqa: E402
from dsx.loader import load  # noqa: E402

CORPUS_DIR = ROOT / "examples" / "known-bad"
SPEC_SUFFIX = "-ANALYSIS-SPEC.yaml"
POSTMORTEM_SUFFIX = "-POSTMORTEM.md"
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
    "DSX-EXP-007",  # frequentist fixture: design.mde (0.02) exceeds decision.minimum_practical_effect (0.01)
    "DSX-MET-040",  # metrics[0].source is warehouse.* with no metrics[0].sql definition
    "DSX-NAR-001",  # claims declared but narrative.path missing (ship-only check)
    "DSX-REP-001",  # bayesian fixture: bayesian_ab is a stochastic method with no reproducibility.random_seed
    "DSX-REP-030",  # reproducibility.entrypoint is not declared
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
_TARGET_DEFECT_CODES: "dict[str, dict[str, str]]" = {
    "weak-identification-mmm": {"plan": "DSX-VAL-040", "verify": "DSX-INT-030"},
    "interference-shared-budget": {"plan": "DSX-INT-010"},
    "triggering-dilution": {"plan": "DSX-INT-030"},
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
}


def _effective_target_map() -> "dict[str, dict[str, frozenset[str]]]":
    """Combine the corpus's two per-fixture expectation maps into the single
    (slug -> point -> expected CRITICAL codes) form `_classify_target_defect` decides.

    `_TARGET_DEFECT_CODES` contributes one code at the exact gate point it names.
    `_EXPECTED_CAUGHT_DEFECTS` contributes its whole set at every point in
    `_CRITICAL_THRESHOLD_POINTS`, because a check family registered at every gate
    point is expected to catch at every CRITICAL-threshold one. Contributions union
    rather than overwrite: a fixture may legitimately appear in both maps, and losing
    either contribution would silently retire a guarantee one of the two phases shipped.
    """
    merged: "dict[str, dict[str, set[str]]]" = {}
    for slug, points in _TARGET_DEFECT_CODES.items():
        for point, code in points.items():
            merged.setdefault(slug, {}).setdefault(point, set()).add(code)
    for slug, codes in _EXPECTED_CAUGHT_DEFECTS.items():
        if not codes:
            continue
        for point in _CRITICAL_THRESHOLD_POINTS:
            merged.setdefault(slug, {}).setdefault(point, set()).update(codes)
    return {
        slug: {point: frozenset(codes) for point, codes in points.items()}
        for slug, points in merged.items()
    }


def _own_target_codes(slug: str) -> "frozenset[str]":
    """Every code `slug` is this corpus's declared demonstration of, across both maps."""
    return frozenset(
        set(_TARGET_DEFECT_CODES.get(slug, {}).values())
        | set(_EXPECTED_CAUGHT_DEFECTS.get(slug, frozenset()))
    )


def _slugs(pattern: str, suffix: str) -> set[str]:
    return {p.name[: -len(suffix)] for p in CORPUS_DIR.glob(pattern)}


class TestKnownBadCorpus(unittest.TestCase):
    def _spec_paths(self) -> list[Path]:
        return sorted(CORPUS_DIR.glob(f"*{SPEC_SUFFIX}"))

    def _postmortem_paths(self) -> list[Path]:
        return sorted(CORPUS_DIR.glob(f"*{POSTMORTEM_SUFFIX}"))

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
        """
        with tempfile.TemporaryDirectory() as tmp:
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = cli.main(
                    ["gate", point, "--spec", str(spec_path), "--phase-dir", tmp, "--json"]
                )
            raw = err.getvalue() or out.getvalue()
            report = json.loads(raw)
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


if __name__ == "__main__":
    unittest.main()
