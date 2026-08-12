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
from dsx.loader import load  # noqa: E402

CORPUS_DIR = ROOT / "examples" / "known-bad"
SPEC_SUFFIX = "-ANALYSIS-SPEC.yaml"
POSTMORTEM_SUFFIX = "-POSTMORTEM.md"

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

# The code-family prefixes named in each post-mortem's "Which absent code would
# have caught it" section — the codes each fixture exists to motivate (DSX-INT-010
# for the interference fixture, DSX-PAR-010/DSX-PAR-011 for the atomic monitoring
# pair, D-06). "DSX-PAR-01" deliberately excludes DSX-PAR-001 (the unrelated,
# already-shipped INFO-severity paradigm-manifest finding, REQ-P6-09).
#
# "DSX-VAL-040" (plan 07-07) is listed as the exact code, not the family prefix
# "DSX-VAL-". The weak-identification-mmm fixture is the first fixture in this
# corpus whose target code ships in the same phase as the fixture, so its target
# code lives here (never in _INCIDENTAL_GAP_CODES — see
# test_ship_gate_findings_are_all_documented_incidental_corpus_gaps's amended
# docstring) and is also the sole entry in _EXPECTED_PLAN_BLOCKERS below. A family
# prefix here would also make illegal the DSX-VAL-041 entry plan 07-05 already
# added to _INCIDENTAL_GAP_CODES, under
# test_incidental_allowlist_names_no_target_family_code, which asserts that no
# allow-listed code starts with any entry in this tuple.
_TARGET_CODE_FAMILIES = ("DSX-INT-", "DSX-PAR-01", "DSX-VAL-040")

# Named-exception set for fixtures whose target code has already shipped in the
# same milestone as the fixture (plan 07-07, D-15, Option A of that plan's
# recorded decision). A fixture listed here cannot honestly claim to clear the
# plan gate that its own target code blocks — so rather than weakening or
# deleting the corpus's blanket "every fixture clears plan and execute" guarantee
# (test_every_spec_passes_the_critical_threshold_gate_points), this dictionary
# converts the lost assertion into a stronger one: a listed fixture MUST block
# `dsx gate plan` with its mapped code among the CRITICAL findings, and MUST still
# clear `dsx gate execute` (the "val" check that emits every DSX-VAL-* code is not
# in the execute gate profile — dsx/cli.py's GATE_PROFILES — so half of the usual
# guarantee survives untouched even for a listed fixture).
_EXPECTED_PLAN_BLOCKERS = {
    "weak-identification-mmm-ANALYSIS-SPEC.yaml": "DSX-VAL-040",
}

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
# Distinct from _EXPECTED_PLAN_BLOCKERS above: that dict is a narrower, single-code,
# plan-only exception for a fixture whose target check already fires only at `plan`
# (its check family is absent from the `execute` GATE_PROFILES entry). This dict is
# the general per-fixture, both-critical-points form D-03 specifies, for target
# checks — like Phase 9's DSX-PAR-010/DSX-PAR-011 pair — whose check family is
# registered at every gate point and so is expected to catch at both.
_EXPECTED_CAUGHT_DEFECTS: "dict[str, frozenset[str]]" = {
    "bayesian-continuous-monitoring": frozenset(),
    "frequentist-uncontrolled-continuous": frozenset(),
    "interference-shared-budget": frozenset(),
    "weak-identification-mmm": frozenset(),
}


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

    def test_every_spec_passes_the_critical_threshold_gate_points(self):
        """The corpus's per-fixture contract, as it now stands, rather than a
        blanket pass: a fixture with no expected catch (neither
        `_EXPECTED_PLAN_BLOCKERS` nor a non-empty `_EXPECTED_CAUGHT_DEFECTS`
        entry) clears both CRITICAL-threshold gate points, `plan` and
        `execute`, today. A fixture listed in `_EXPECTED_PLAN_BLOCKERS` is
        required to do the opposite at `plan` only — it MUST block, with its
        mapped code among the CRITICAL findings — because its target code
        ships in the same milestone as the fixture but its check family is
        absent from the `execute` gate profile (plan 07-07, D-15). A fixture
        with a non-empty `_EXPECTED_CAUGHT_DEFECTS` entry MUST block at every
        CRITICAL-threshold point, with every expected code among the CRITICAL
        findings, because its target check's family is registered at both
        `plan` and `execute` (D-03)."""
        specs = self._spec_paths()
        self.assertTrue(specs, "no known-bad specs found to gate")
        for path in specs:
            slug = path.name[: -len(SPEC_SUFFIX)]
            expected_blocker = _EXPECTED_PLAN_BLOCKERS.get(path.name)
            expected_caught = _EXPECTED_CAUGHT_DEFECTS.get(slug, frozenset())
            for point in _CRITICAL_THRESHOLD_POINTS:
                with self.subTest(spec=path.name, point=point):
                    code, findings = self._gate_findings(path, point)
                    critical = [f["code"] for f in findings if f["severity"] == "CRITICAL"]
                    if expected_blocker is not None and point == "plan":
                        self.assertEqual(
                            code, 1,
                            f"{path.name} was expected to block dsx gate plan on "
                            f"{expected_blocker!r} but exited {code}: {critical}",
                        )
                        self.assertIn(
                            expected_blocker, critical,
                            f"{path.name} blocked dsx gate plan, but its expected code "
                            f"{expected_blocker!r} is not among the CRITICAL findings: {critical}",
                        )
                    elif expected_caught:
                        self.assertEqual(
                            code, 1,
                            f"{path.name} was expected to block dsx gate {point} on "
                            f"{sorted(expected_caught)} but exited {code}: {critical}",
                        )
                        missing = expected_caught - set(critical)
                        self.assertFalse(
                            missing,
                            f"{path.name} blocked dsx gate {point}, but expected codes "
                            f"{sorted(missing)} are not among the CRITICAL findings: {critical}",
                        )
                    else:
                        self.assertEqual(
                            code, 0,
                            f"{path.name} failed dsx gate {point} (CRITICAL threshold): {critical}",
                        )

    def test_ship_gate_findings_are_all_documented_incidental_corpus_gaps(self):
        """Every CRITICAL/HIGH finding `dsx gate ship` produces against a fixture
        is either a member of the documented `_INCIDENTAL_GAP_CODES` allow-list,
        or — for a fixture listed in `_EXPECTED_PLAN_BLOCKERS` — is that
        fixture's own mapped target code (plan 07-07, D-15).

        This test failing after a later phase ships a new check is the intended
        signal, not a defect: when the code a fixture was built to motivate (e.g.
        DSX-INT-010, DSX-PAR-010/DSX-PAR-011) finally fires against its fixture,
        that code moves from "not shipped" to "shipped and blocking", and the
        corpus documentation (this module's constants, the fixture headers, the
        post-mortems) must move that code from incidental-gap to caught-defect.
        This assertion is what forces that edit instead of letting it rot.

        A fixture's mapped target code is excluded from the undocumented set
        here, rather than added to `_INCIDENTAL_GAP_CODES`, because it is that
        fixture's encoded defect, not a corpus-completeness gap — putting it in
        the incidental allow-list would be exactly the misuse
        `test_incidental_allowlist_names_no_target_family_code` exists to forbid.
        """
        specs = self._spec_paths()
        self.assertTrue(specs, "no known-bad specs found to gate")
        for path in specs:
            with self.subTest(spec=path.name):
                slug = path.name[: -len(SPEC_SUFFIX)]
                _code, findings = self._gate_findings(path, "ship")
                blocking = {
                    f["code"] for f in findings if f["severity"] in ("CRITICAL", "HIGH")
                }
                allowed = set(_INCIDENTAL_GAP_CODES) | _EXPECTED_CAUGHT_DEFECTS.get(
                    slug, frozenset()
                )
                expected_blocker = _EXPECTED_PLAN_BLOCKERS.get(path.name)
                if expected_blocker is not None:
                    allowed = allowed | {expected_blocker}
                undocumented = blocking - allowed
                self.assertEqual(
                    undocumented, set(),
                    f"{path.name} blocks dsx gate ship on undocumented codes: "
                    f"{sorted(undocumented)} — add each to _INCIDENTAL_GAP_CODES with its "
                    "cause, or if it is a target-family code, the corpus's guarantee has "
                    "changed and the header/post-mortem prose must be updated to match",
                )

    def test_incidental_allowlist_names_no_target_family_code(self):
        """The machine-checkable form of the corpus's real guarantee: the
        fixtures block only on completeness gaps, never on the semantic defect
        they exist to encode. Holds without asserting that any unshipped code
        fires, so the module's standing no-code-specific-assertion rule survives
        intact."""
        for code in sorted(_INCIDENTAL_GAP_CODES):
            for family in _TARGET_CODE_FAMILIES:
                with self.subTest(code=code, family=family):
                    self.assertFalse(
                        code.startswith(family),
                        f"{code} is in the incidental-gap allow-list but belongs to target "
                        f"family {family!r} — a fixture would then never block on the "
                        "defect it exists to encode even after that code ships",
                    )

    def test_expected_caught_defects_keys_match_the_corpus_on_disk(self):
        """A fixture added later without an `_EXPECTED_CAUGHT_DEFECTS` entry must
        fail loudly here rather than silently falling through
        `test_every_spec_passes_the_critical_threshold_gate_points`'s exit-0
        branch as if its target check would never be expected to catch it."""
        disk_slugs = _slugs(f"*{SPEC_SUFFIX}", SPEC_SUFFIX)
        map_slugs = set(_EXPECTED_CAUGHT_DEFECTS)
        self.assertEqual(
            map_slugs, disk_slugs,
            f"_EXPECTED_CAUGHT_DEFECTS keys and the corpus on disk disagree: "
            f"{sorted(map_slugs ^ disk_slugs)} — every fixture must have an entry "
            "(even an empty frozenset()) and every key must name a real fixture",
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


if __name__ == "__main__":
    unittest.main()
