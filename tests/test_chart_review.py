"""Test suite for dsx/checks/chart_review.py — DSX-CRV-010/011/012/013
(REQ-P11.3-06). Stdlib unittest — no pytest dependency.

Run:  python3 -m unittest tests.test_chart_review -v
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsx.checks import chart_review  # noqa: E402
from dsx.findings import Report, Severity  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = ROOT / "examples"
FIXTURES_DIR = ROOT / "tests" / "fixtures" / "chart-review"

_CRV_CODES = ("DSX-CRV-010", "DSX-CRV-011", "DSX-CRV-012", "DSX-CRV-013")


def codes(report: Report) -> set[str]:
    return {f.code for f in report.findings}


def severity_of(report: Report, code: str) -> "Severity | None":
    for finding in report.findings:
        if finding.code == code:
            return finding.severity
    return None


class TestChartReview(unittest.TestCase):
    """One behavior per fire/no-fire clause (chart-review-schema.md:84-87)."""

    def test_good_fixture_fires_none_of_the_four_crv_codes(self):
        report = chart_review.check({}, phase_dir=str(EXAMPLES_DIR))
        self.assertEqual(codes(report) & set(_CRV_CODES), set())

    # D-05: DSX-CRV-010
    def test_bad_schema_tag_fires_crv_010_high(self):
        report = chart_review.check(
            {}, phase_dir=str(FIXTURES_DIR / "bad-schema-tag")
        )
        self.assertIn("DSX-CRV-010", codes(report))
        self.assertEqual(severity_of(report, "DSX-CRV-010"), Severity.HIGH)

    def test_good_fixture_does_not_fire_crv_010(self):
        report = chart_review.check({}, phase_dir=str(EXAMPLES_DIR))
        self.assertNotIn("DSX-CRV-010", codes(report))

    # D-05: DSX-CRV-011
    def test_ten_point_scale_fires_crv_011_medium(self):
        report = chart_review.check(
            {}, phase_dir=str(FIXTURES_DIR / "ten-point-scale")
        )
        self.assertIn("DSX-CRV-011", codes(report))
        self.assertEqual(severity_of(report, "DSX-CRV-011"), Severity.MEDIUM)

    def test_good_fixture_does_not_fire_crv_011(self):
        report = chart_review.check({}, phase_dir=str(EXAMPLES_DIR))
        self.assertNotIn("DSX-CRV-011", codes(report))

    # D-05: DSX-CRV-012
    def test_missing_sentinel_fires_crv_012_high(self):
        report = chart_review.check(
            {}, phase_dir=str(FIXTURES_DIR / "missing-sentinel")
        )
        self.assertIn("DSX-CRV-012", codes(report))
        self.assertEqual(severity_of(report, "DSX-CRV-012"), Severity.HIGH)

    def test_good_fixture_does_not_fire_crv_012(self):
        report = chart_review.check({}, phase_dir=str(EXAMPLES_DIR))
        self.assertNotIn("DSX-CRV-012", codes(report))

    # D-05: DSX-CRV-013
    def test_untokenised_finding_line_fires_crv_013_medium(self):
        report = chart_review.check(
            {}, phase_dir=str(FIXTURES_DIR / "untokenised-finding")
        )
        self.assertIn("DSX-CRV-013", codes(report))
        self.assertEqual(severity_of(report, "DSX-CRV-013"), Severity.MEDIUM)

    def test_good_fixture_does_not_fire_crv_013(self):
        report = chart_review.check({}, phase_dir=str(EXAMPLES_DIR))
        self.assertNotIn("DSX-CRV-013", codes(report))


class TestChartReviewD13Boundary(unittest.TestCase):
    """D-13: the four codes must never read final_assessment, scores.*,
    agent-transcribed gates.A-D, or verdict prose. tests/fixtures/chart-review/
    forbidden-input-flip/CHART-REVIEW.md is structurally identical to
    examples/good-CHART-REVIEW.md (same schema tag, no forbidden scale
    substring, the terminal sentinel, every finding line tokenised or absent)
    but flips every one of those forbidden fields to its worst-case value.
    Flipping ONLY a forbidden-input field must never change which DSX-CRV-*
    codes fire — mirrors tests/test_frame_boundary.py::
    TestFrameParadigmReadBoundary's flip-only-the-forbidden-field method."""

    def test_forbidden_input_flip_fires_none_of_the_four_crv_codes(self):
        report = chart_review.check(
            {}, phase_dir=str(FIXTURES_DIR / "forbidden-input-flip")
        )
        self.assertEqual(codes(report) & set(_CRV_CODES), set())

    def test_forbidden_input_flip_matches_good_fixture_verdict_exactly(self):
        good = chart_review.check({}, phase_dir=str(EXAMPLES_DIR))
        flipped = chart_review.check(
            {}, phase_dir=str(FIXTURES_DIR / "forbidden-input-flip")
        )
        self.assertEqual(
            codes(good) & set(_CRV_CODES), codes(flipped) & set(_CRV_CODES)
        )


class TestChartReviewDegradesSafely(unittest.TestCase):
    """T-11.3-11 (D-01): a missing/truncated/undecodable CHART-REVIEW.md must
    degrade to an ok/empty report, never a gate-path traceback — mirrors
    figures.check's and val.check's absent/malformed -> empty-report
    convention."""

    def test_missing_chart_review_file_returns_empty_report_without_raising(self):
        with tempfile.TemporaryDirectory() as empty_dir:
            report = chart_review.check({}, phase_dir=empty_dir)
        self.assertEqual(codes(report), set())

    def test_no_phase_dir_returns_empty_report_without_raising(self):
        with tempfile.TemporaryDirectory() as empty_dir:
            import os

            cwd = os.getcwd()
            os.chdir(empty_dir)
            try:
                report = chart_review.check({}, phase_dir=None)
            finally:
                os.chdir(cwd)
        self.assertEqual(codes(report), set())

    def test_undecodable_chart_review_file_returns_empty_report_without_raising(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "CHART-REVIEW.md"
            # 0xFF is not valid UTF-8 in this position — forces a UnicodeDecodeError
            # on a plain text-mode read, exactly the failure mode this test proves
            # degrades rather than raising.
            target.write_bytes(b"---\nschema: dsx-chart-review-v1\n---\n\xff\xfe\x00")
            report = chart_review.check({}, phase_dir=tmp_dir)
        self.assertEqual(codes(report), set())

    def test_truncated_frontmatter_returns_empty_report_without_raising(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "CHART-REVIEW.md"
            # No closing '---' delimiter for the frontmatter block at all.
            target.write_text(
                "---\nschema: dsx-chart-review-v1\ncapability: dsx\n",
                encoding="utf-8",
            )
            report = chart_review.check({}, phase_dir=tmp_dir)
        # Frontmatter with no closing delimiter degrades to "no schema tag
        # resolved" -> DSX-CRV-010 fires and DSX-CRV-012 fires (no sentinel);
        # neither is a raise, which is the property this test proves.
        self.assertIn("DSX-CRV-010", codes(report))
        self.assertIn("DSX-CRV-012", codes(report))

    def test_unparseable_frontmatter_yaml_returns_empty_report_without_raising(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "CHART-REVIEW.md"
            # Tabs are invalid YAML indentation in dsx/loader.py's bundled
            # parser (SpecParseError) — this exercises the parse-failure
            # branch of the frontmatter split, not just the missing-file path.
            target.write_text(
                "---\n\tschema: dsx-chart-review-v1\n---\n\n## CHART AUDIT COMPLETE\n",
                encoding="utf-8",
            )
            report = chart_review.check({}, phase_dir=tmp_dir)
        self.assertIn("DSX-CRV-010", codes(report))


if __name__ == "__main__":
    unittest.main()
