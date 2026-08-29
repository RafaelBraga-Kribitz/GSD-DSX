"""Nyquist validation for Phase 15 (cuped-and-bi-declaration-checks-new-codes-d-05).

Phase 15 is a code phase: it adds the `cuped` variance-adjustment vocabulary
keystone, two always-run declaration-only gate checks (DSX-EXP-070 CRITICAL for a
non-pre-experiment CUPED covariate; DSX-MET-021 HIGH for a metric pooled across
buckets sampled at different rates with no reweighting), an optional APA research
table template, and a no-normality-auto-switch guarantee — all additively
(catalogue 258 -> 260, frozen Phase-12 snapshot unmutated).

Unlike Phases 13/14/16, every requirement here already shipped a dedicated
behavioural test at execution time (S4-3). This module is the phase-scoped
coverage anchor the way tests/test_phase16_reproduce.py was for Phase 16: it does
NOT re-prove the deep behaviour, it pins the structural facts those behavioural
tests depend on so a silent regression — a deleted guard, a downgraded severity, a
stripped citation, a dropped vocabulary member, or a data library pulled onto the
declaration gate — names itself.

Coverage map (see 15-VALIDATION.md):
  REQ-P15-01  `cuped` is a legal VARIANCE_ADJUSTMENTS member and CUPED_COVARIATE_TIMINGS
              is the two-valued covariate-timing vocabulary
              (behaviour: tests/test_cuped_vocab.py)
  REQ-P15-02  a non-pre-experiment CUPED covariate blocks at `dsx gate plan` via
              DSX-EXP-070 (CRITICAL); the check is declaration-only and cites the
              WSDM primary source (behaviour: tests/test_cuped.py)
  REQ-P15-03  the extended good fixture stays silent at every gate threshold
              (behaviour: tests/test_good_fixture_phase15.py)
  REQ-P15-04  a changing-denominator cohort declaration blocks via DSX-MET-021 (HIGH),
              provably disjoint from DSX-MET-020; survivorship half not shipped
              (behaviour: tests/test_cohort_denominator.py)
  REQ-P15-05  templates/APA-TABLE-research.md ships, optional + research-domain
              (behaviour: tests/test_apa_template.py)
  REQ-P15-06  no normality-test auto-switch on the decision surface
              (behaviour: tests/test_no_shapiro_autoswitch.py)
  REQ-P15-07  the catalogue extends additively to 260 and the frozen Phase-12
              snapshot is byte-unchanged (behaviour: tests/test_finding_catalogue_invariant.py)

CRLF-safe: files are read as text with single-line / `^...$` MULTILINE anchors, so
the repo's CRLF checkout cannot break a match. Stdlib-only (gate-path hygiene
applies to the tests too).
"""
import re
import unittest
from pathlib import Path

from dsx.spec import CUPED_COVARIATE_TIMINGS, VARIANCE_ADJUSTMENTS

ROOT = Path(__file__).resolve().parents[1]

# A declaration-only gate check must never pull a data library or an execution
# primitive onto the deterministic gate path (D-01).
FORBIDDEN_GATE_IMPORTS = re.compile(
    r"^\s*(?:import|from)\s+"
    r"(?:pandas|scipy|numpy|csv|subprocess|runpy|os|shutil)\b",
    re.MULTILINE,
)

# The four legacy variance adjustments that must survive the additive `cuped` add.
LEGACY_VARIANCE_ADJUSTMENTS = {
    "cluster_robust",
    "delta_method",
    "bootstrap_cluster",
    "mixed_effects",
}


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def catalogue_severity(code):
    """Return the severity cell of a finding-code row, or None if absent."""
    row = re.search(
        r"^\|\s*`?" + re.escape(code) + r"`?\s*\|\s*([A-Z]+)\s*\|",
        read("references/finding-codes.md"),
        re.MULTILINE,
    )
    return row.group(1) if row else None


class TestPhase15BiChecks(unittest.TestCase):
    # ---- REQ-P15-01 : cuped vocabulary keystone ----
    def test_req01_cuped_is_a_legal_variance_adjustment(self):
        self.assertIn("cuped", VARIANCE_ADJUSTMENTS)
        # Additive: the four legacy members survive; the set is exactly five.
        self.assertTrue(LEGACY_VARIANCE_ADJUSTMENTS <= VARIANCE_ADJUSTMENTS)
        self.assertEqual(len(VARIANCE_ADJUSTMENTS), 5, VARIANCE_ADJUSTMENTS)

    def test_req01_covariate_timing_vocab_is_two_valued(self):
        self.assertEqual(
            CUPED_COVARIATE_TIMINGS, {"pre_experiment", "post_treatment"}
        )

    def test_req01_behavioural_module_present(self):
        self.assertTrue(
            (ROOT / "tests" / "test_cuped_vocab.py").is_file(),
            "REQ-P15-01 behaviour test tests/test_cuped_vocab.py is missing",
        )

    # ---- REQ-P15-02 : DSX-EXP-070 CUPED gate check ----
    def test_req02_exp070_registered_critical(self):
        self.assertEqual(
            catalogue_severity("DSX-EXP-070"), "CRITICAL",
            "DSX-EXP-070 must be CRITICAL — a post-treatment CUPED covariate has to "
            "exit 1 at the plan threshold (REQ-P15-02)",
        )

    def test_req02_cuped_check_is_declaration_only(self):
        src = read("dsx/checks/design.py")
        self.assertIsNone(
            FORBIDDEN_GATE_IMPORTS.search(src),
            "dsx/checks/design.py imports a data library or execution primitive — "
            "the CUPED check must stay declaration-only (REQ-P15-02, D-01)",
        )
        # The CUPED variance-reduction arithmetic lives in dsx/mathx.py and must NOT
        # be imported onto the gate path (the diluted-effect / INT-030 boundary).
        self.assertNotIn("cuped_theta", src)
        self.assertNotIn("cuped_variance_reduction", src)

    def test_req02_cuped_check_cites_wsdm_primary_source(self):
        # D-05 bar: cite Deng et al. 2013 WSDM, not the Unified playbook snippet.
        self.assertIn("Deng", read("dsx/checks/design.py"))

    def test_req02_behavioural_module_present(self):
        self.assertTrue(
            (ROOT / "tests" / "test_cuped.py").is_file(),
            "REQ-P15-02 behaviour test tests/test_cuped.py is missing",
        )

    # ---- REQ-P15-03 : extended good fixture silent everywhere ----
    def test_req03_behavioural_module_present(self):
        self.assertTrue(
            (ROOT / "tests" / "test_good_fixture_phase15.py").is_file(),
            "REQ-P15-03 behaviour test tests/test_good_fixture_phase15.py is missing",
        )

    # ---- REQ-P15-04 : DSX-MET-021 changing-denominator, disjoint from MET-020 ----
    def test_req04_met021_registered_high(self):
        self.assertEqual(
            catalogue_severity("DSX-MET-021"), "HIGH",
            "DSX-MET-021 must be HIGH — it blocks the changing-denominator fixture "
            "at verify/ship, matching its sibling DSX-MET-020 (REQ-P15-04)",
        )

    def test_req04_cohort_check_is_declaration_only(self):
        self.assertIsNone(
            FORBIDDEN_GATE_IMPORTS.search(read("dsx/checks/metrics.py")),
            "dsx/checks/metrics.py imports a data library or execution primitive — "
            "the cohort-denominator check must stay declaration-only (REQ-P15-04, D-01)",
        )

    def test_req04_met020_and_met021_read_disjoint_surfaces(self):
        # MET-020 reads results.period_comparisons; MET-021 reads
        # results.cohort_comparisons. Both surfaces must be named in the module so
        # the two codes cannot double-report on one defect (T-15-10 / trap #1).
        src = read("dsx/checks/metrics.py")
        self.assertIn("period_comparisons", src)
        self.assertIn("cohort_comparisons", src)

    def test_req04_cohort_check_cites_kdd_primary_source(self):
        # D-05 bar: cite Crook et al. 2009 KDD (Pitfall 4).
        self.assertIn("Crook", read("dsx/checks/metrics.py"))

    def test_req04_survivorship_code_not_minted(self):
        # HQ-8: Brown 1992 does not transfer; the survivorship half stays a §6.5
        # non-promotion. No DSX code names survivorship.
        cat = read("references/finding-codes.md").lower()
        self.assertNotIn("survivorship", cat)

    def test_req04_behavioural_module_present(self):
        self.assertTrue(
            (ROOT / "tests" / "test_cohort_denominator.py").is_file(),
            "REQ-P15-04 behaviour test tests/test_cohort_denominator.py is missing",
        )

    # ---- REQ-P15-05 : APA research-table template ----
    def test_req05_apa_template_ships(self):
        self.assertTrue(
            (ROOT / "templates" / "APA-TABLE-research.md").is_file(),
            "REQ-P15-05 deliverable templates/APA-TABLE-research.md is missing",
        )

    def test_req05_behavioural_module_present(self):
        self.assertTrue(
            (ROOT / "tests" / "test_apa_template.py").is_file(),
            "REQ-P15-05 behaviour test tests/test_apa_template.py is missing",
        )

    # ---- REQ-P15-06 : no normality-test auto-switch guard ----
    def test_req06_no_shapiro_guard_present(self):
        self.assertTrue(
            (ROOT / "tests" / "test_no_shapiro_autoswitch.py").is_file(),
            "REQ-P15-06 guard tests/test_no_shapiro_autoswitch.py is missing",
        )

    # ---- REQ-P15-07 : additive catalogue + frozen snapshot ----
    def test_req07_frozen_phase12_snapshot_present(self):
        self.assertTrue(
            (ROOT / "tests" / "fixtures" / "finding-codes-phase12.md").is_file(),
            "REQ-P15-07 frozen anchor tests/fixtures/finding-codes-phase12.md is missing",
        )

    def test_req07_both_new_codes_in_catalogue(self):
        # The additive delta the invariant's set-identity leg pins.
        for code in ("DSX-EXP-070", "DSX-MET-021"):
            self.assertIsNotNone(
                catalogue_severity(code),
                f"{code} is not a row in references/finding-codes.md",
            )

    def test_req07_invariant_module_present(self):
        self.assertTrue(
            (ROOT / "tests" / "test_finding_catalogue_invariant.py").is_file(),
            "REQ-P15-07 invariant tests/test_finding_catalogue_invariant.py is missing",
        )


if __name__ == "__main__":
    unittest.main()
