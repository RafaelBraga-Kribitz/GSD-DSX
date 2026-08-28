"""REQ-P6-14 and REQ-P6-15: Documentation presence regression tests.

These tests pin structural content required by Phase 6 completion. They assert
the presence of documented facts, not the clarity or completeness of the prose
describing them — that is a human judgement carried on the phase's manual-
verification list (06-UAT 2026-08-10), not decided by a machine. A substring
assertion is the only part of that human-verified documentation a machine can
hold: it proves the named sentences still exist.
"""

import unittest
from pathlib import Path


def _normalize_whitespace(text: str) -> str:
    """Collapse every run of whitespace, including the carriage returns this
    repository checks out on Windows, to a single space, so a substring check
    against a sentence that wraps across lines does not depend on line endings."""
    return " ".join(text.split())


ROOT = Path(__file__).resolve().parent.parent


class TestReversalsDocPresence(unittest.TestCase):
    """REQ-P6-14: `.planning/REVERSALS.md` must carry the D-14 reversal-record
    TEMPLATE with all five fields, and the `SELF-001` convention DEFINED.
    """

    @classmethod
    def setUpClass(cls):
        cls.reversals_text = (ROOT / ".planning" / "REVERSALS.md").read_text(
            encoding="utf-8"
        )
        cls.reversals_normalized = _normalize_whitespace(cls.reversals_text)

    def test_1_d14_template_header_exists(self):
        """The template header must include the (D-14) marker."""
        self.assertIn(
            "### Reversal record REV-NNN (D-14)",
            self.reversals_text,
            ".planning/REVERSALS.md must carry the template header "
            '"### Reversal record REV-NNN (D-14)"',
        )

    def test_2_template_date_field_exists(self):
        """Template must include the **Date:** field."""
        self.assertIn(
            "**Date:**",
            self.reversals_text,
            ".planning/REVERSALS.md template must include the **Date:** field",
        )

    def test_3_template_reversed_field_exists(self):
        """Template must include the **Reversed:** field."""
        self.assertIn(
            "**Reversed:**",
            self.reversals_text,
            ".planning/REVERSALS.md template must include the **Reversed:** field",
        )

    def test_4_template_new_evidence_field_exists(self):
        """Template must include the **New evidence:** field."""
        self.assertIn(
            "**New evidence:**",
            self.reversals_text,
            ".planning/REVERSALS.md template must include the **New evidence:** field",
        )

    def test_5_template_would_have_made_correct_field_exists(self):
        """Template must include the **What would have made the original correct:** field."""
        self.assertIn(
            "**What would have made the original correct:**",
            self.reversals_text,
            ".planning/REVERSALS.md template must include the "
            '"**What would have made the original correct:**" field',
        )

    def test_6_template_what_did_not_change_field_exists(self):
        """Template must include the **What did not change:** field."""
        self.assertIn(
            "**What did not change:**",
            self.reversals_text,
            ".planning/REVERSALS.md template must include the "
            '"**What did not change:**" field',
        )

    def test_7_self_001_convention_named(self):
        """The SELF-001 convention must be named in the document."""
        self.assertIn(
            "SELF-001",
            self.reversals_text,
            ".planning/REVERSALS.md must name the SELF-001 convention",
        )

    def test_8_self_001_convention_defined_not_merely_mentioned(self):
        """The SELF-001 convention must be explicitly DEFINED.

        The definition must appear in prose that states what 'SELF-001' marks,
        distinguishing between mentioned and defined.
        """
        self.assertIn(
            "is the finding logged",
            self.reversals_normalized,
            ".planning/REVERSALS.md must contain the SELF-001 definition sentence "
            '"is the finding logged", which distinguishes the convention as '
            "defined rather than merely mentioned",
        )


class TestReadmeSuppressionsMigration(unittest.TestCase):
    """REQ-P6-15: `README.md` must document suppressions[] with its authority
    requirement as the pre-v2.0.0 migration path, AND state the known limit
    that "a frame that lies passes".
    """

    @classmethod
    def setUpClass(cls):
        cls.readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
        cls.readme_normalized = _normalize_whitespace(cls.readme_text)

    def test_1_migration_section_heading_exists(self):
        """The migration-path section must be present."""
        self.assertIn(
            "### Migrating a pre-v2.0.0 spec",
            self.readme_text,
            "README.md must carry the section heading "
            '"### Migrating a pre-v2.0.0 spec"',
        )

    def test_2_suppressions_array_documented(self):
        """The suppressions[] array must be named in the migration section."""
        self.assertIn(
            "suppressions[]",
            self.readme_text,
            "README.md must document suppressions[] in the migration section",
        )

    def test_3_authority_requirement_documented(self):
        """The authority field requirement must be documented."""
        self.assertIn(
            "authority",
            self.readme_text,
            "README.md must document the authority requirement for suppressions",
        )

    def test_4_dsx_spec_070_grandfather_path_named(self):
        """The DSX-SPEC-070 grandfather finding must be named."""
        self.assertIn(
            "DSX-SPEC-070",
            self.readme_text,
            "README.md must name DSX-SPEC-070 as the grandfather finding for "
            "a suppression with no resolvable authority",
        )

    def test_5_known_limits_heading_exists(self):
        """The Known limits section must be present."""
        self.assertIn(
            "## Known limits",
            self.readme_text,
            "README.md must carry the section heading `## Known limits`",
        )

    def test_6_frame_lies_honesty_caveat_stated(self):
        """The central honesty caveat must be stated in Known limits."""
        self.assertIn(
            "a frame that lies passes",
            self.readme_normalized,
            "README.md must state in Known limits that 'a frame that lies passes', "
            "the central limit on frame coherence checks",
        )


if __name__ == "__main__":
    unittest.main()
