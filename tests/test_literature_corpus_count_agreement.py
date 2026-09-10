"""REQ-P30-02 — literature corpus-count AGREEMENT gate (read-only, off gate path).

Closes exactly the one genuine gap the Phase-30 audit surfaced: no existing test
bound the literature record's mapping-table row-15 corpus counts to the live example
corpus, which is precisely the drift that let the doc read "39 known-bad specs" while
the live corpus had grown to 42 (Phases 27-29 added three fixtures).

This asserts DOC == LIVE agreement, never a hardcoded expected number, so it cannot
under-pin to a stale literal and cannot over-fire on formatting. It pins nothing beyond
the row-15 counts (GA-4: "close exactly this gap and no more"). It mints no code and is
off the gate path (D-01/D-02): a divergence here is a stale record, a broken build, not
a spec-audit finding.
"""
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "literature" / "the-ai-data-scientist.md"

# CRLF-tolerant: \s+ spans the intra-line whitespace between the count and the phrase;
# the doc is read as text so line endings never reach the match.
_KNOWN_BAD_RE = re.compile(r"(\d+)\s+known-bad specs")
_GOOD_CONTROL_RE = re.compile(r"(\d+)\s+good-control specs")


def _doc_count(pattern: "re.Pattern[str]", text: str, label: str) -> int:
    m = pattern.search(text)
    # Anti-false-pass: fail loudly if the row-15 phrasing is absent or renamed,
    # rather than silently treating a missing count as agreement.
    assert m is not None, f"{label} count phrase not found in {DOC.name}"
    return int(m.group(1))


def _live_spec_count(subdir: str) -> int:
    return len(list((ROOT / "examples" / subdir).glob("*-ANALYSIS-SPEC.yaml")))


class TestLiteratureCorpusCountAgreement(unittest.TestCase):
    """The literature row-15 counts must equal the live corpus glob counts."""

    def setUp(self) -> None:
        self.text = DOC.read_text(encoding="utf-8")

    def test_known_bad_count_matches_live_corpus(self) -> None:
        doc_n = _doc_count(_KNOWN_BAD_RE, self.text, "known-bad")
        live_n = _live_spec_count("known-bad")
        self.assertEqual(
            doc_n,
            live_n,
            f"literature doc row-15 says {doc_n} known-bad specs but "
            f"examples/known-bad/ has {live_n} *-ANALYSIS-SPEC.yaml files",
        )

    def test_good_control_count_matches_live_corpus(self) -> None:
        doc_n = _doc_count(_GOOD_CONTROL_RE, self.text, "good-control")
        live_n = _live_spec_count("good-corpus")
        self.assertEqual(
            doc_n,
            live_n,
            f"literature doc row-15 says {doc_n} good-control specs but "
            f"examples/good-corpus/ has {live_n} *-ANALYSIS-SPEC.yaml files",
        )


if __name__ == "__main__":
    unittest.main()
