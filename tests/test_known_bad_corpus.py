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
}

# The code-family prefixes named in each post-mortem's "Which absent code would
# have caught it" section — the codes each fixture exists to motivate (DSX-INT-010
# for the interference fixture, DSX-PAR-010/DSX-PAR-011 for the atomic monitoring
# pair, D-06). "DSX-PAR-01" deliberately excludes DSX-PAR-001 (the unrelated,
# already-shipped INFO-severity paradigm-manifest finding, REQ-P6-09).
_TARGET_CODE_FAMILIES = ("DSX-INT-", "DSX-PAR-01")

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
        """The corpus's positive gate guarantee: every fixture clears both
        CRITICAL-threshold gate points, `plan` and `execute`, today."""
        specs = self._spec_paths()
        self.assertTrue(specs, "no known-bad specs found to gate")
        for path in specs:
            for point in _CRITICAL_THRESHOLD_POINTS:
                with self.subTest(spec=path.name, point=point):
                    code, findings = self._gate_findings(path, point)
                    critical = [f["code"] for f in findings if f["severity"] == "CRITICAL"]
                    self.assertEqual(
                        code, 0,
                        f"{path.name} failed dsx gate {point} (CRITICAL threshold): {critical}",
                    )

    def test_ship_gate_findings_are_all_documented_incidental_corpus_gaps(self):
        """Every CRITICAL/HIGH finding `dsx gate ship` produces against a fixture
        is a member of the documented `_INCIDENTAL_GAP_CODES` allow-list.

        This test failing after a later phase ships a new check is the intended
        signal, not a defect: when the code a fixture was built to motivate (e.g.
        DSX-INT-010, DSX-PAR-010/DSX-PAR-011) finally fires against its fixture,
        that code moves from "not shipped" to "shipped and blocking", and the
        corpus documentation (this module's constants, the fixture headers, the
        post-mortems) must move that code from incidental-gap to caught-defect.
        This assertion is what forces that edit instead of letting it rot.
        """
        specs = self._spec_paths()
        self.assertTrue(specs, "no known-bad specs found to gate")
        for path in specs:
            with self.subTest(spec=path.name):
                _code, findings = self._gate_findings(path, "ship")
                blocking = {
                    f["code"] for f in findings if f["severity"] in ("CRITICAL", "HIGH")
                }
                undocumented = blocking - _INCIDENTAL_GAP_CODES
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
