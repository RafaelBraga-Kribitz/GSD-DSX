"""The finding-code catalogue invariant (REQ-P12-02, D-18).

Phase 12 mints ZERO finding codes and adds nothing to ``GATE_PROFILES`` — it is a
calibration phase over the existing checks, not a check-shipping phase. This module
pins that contract: the shipped catalogue (``references/finding-codes.md``, generated
by ``scripts/gen-finding-catalogue.py`` from the real ``report.add(...)`` call sites)
must stay at exactly 256 codes. A silently-minted code — or a silently-removed one —
turns this red.

CRLF discipline (repo CLAUDE.md): this checkout may hold ``\r\n`` line endings, so the
catalogue is parsed by whitespace-collapse and by a non-line-anchored row regex, never
by a bare ``\n``-anchored pattern that a CRLF checkout would silently break.

Run:  python -m unittest tests.test_finding_catalogue_invariant -v
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_CATALOGUE_PATH = ROOT / "references" / "finding-codes.md"
# The frozen Phase-12 code-set snapshot (D-07): a byte-copy of the *generated*
# catalogue, compared by set identity to catch a cardinality-preserving swap the
# count invariant alone would pass.
_SNAPSHOT_PATH = ROOT / "tests" / "fixtures" / "finding-codes-phase12.md"

# The pinned count. Phase 12 ships no new code, so this must not move (D-18).
_EXPECTED_TOTAL = 256

# The declared-total line — matched after whitespace-collapse, so it is agnostic to
# ``\n`` vs ``\r\n`` and to any incidental wrapping of the surrounding prose.
_TOTAL_RE = re.compile(r"\*\*Total:\s*(\d+)\s*codes\.\*\*")

# Every catalogue row is a Markdown table cell `| `DSX-<FAMILY>-<digits>` | ...`. The
# same shape ``tests/test_known_bad_corpus.py::_catalogue_codes`` reads; not line
# anchored, so it is CRLF-safe.
_ROW_RE = re.compile(r"\|\s*`(DSX-[A-Z]+-\d+)`\s*\|")


class TestCatalogueInvariant(unittest.TestCase):
    def test_finding_catalogue_stays_at_256_codes(self):
        """The catalogue declares, and enumerates, exactly 256 codes (D-18).

        Two independent readings of the same generated artifact must agree on 256:
        the human-facing ``**Total: N codes.**`` line and the machine count of
        ``DSX-*`` table rows. Requiring both to equal 256 catches a stale Total line
        as well as a minted or dropped code, without re-walking the ``dsx/`` AST here —
        this test stays a pure reader of the same file ``gen-finding-catalogue.py
        --check`` gates.
        """
        raw = _CATALOGUE_PATH.read_text(encoding="utf-8")

        # CRLF-tolerant: collapse ALL whitespace (spaces, tabs, `\n`, `\r\n`) to single
        # spaces before matching the declared total — never a line-anchored regex.
        collapsed = " ".join(raw.split())
        match = _TOTAL_RE.search(collapsed)
        self.assertIsNotNone(
            match,
            f"no '**Total: N codes.**' line found in {_CATALOGUE_PATH} — the catalogue "
            "format changed; the D-18 invariant can no longer be read",
        )
        declared_total = int(match.group(1))
        self.assertEqual(
            declared_total, _EXPECTED_TOTAL,
            f"catalogue declares {declared_total} codes, expected {_EXPECTED_TOTAL} — "
            "Phase 12 mints no finding code, so the total must not move (D-18); if a "
            "code was legitimately added or removed, that change belongs to a "
            "check-shipping phase, not this calibration phase",
        )

        # Independent cross-check: the enumerated rows agree with the declared total,
        # each code appearing exactly once (the generator dedupes).
        rows = _ROW_RE.findall(raw)
        self.assertEqual(
            len(rows), _EXPECTED_TOTAL,
            f"enumerated {len(rows)} catalogue rows, expected {_EXPECTED_TOTAL} — the "
            "declared Total and the actual rows disagree, or a code was minted/dropped",
        )
        self.assertEqual(
            len(set(rows)), _EXPECTED_TOTAL,
            f"catalogue holds {len(rows) - len(set(rows))} duplicate row(s); expected "
            f"{_EXPECTED_TOTAL} unique codes",
        )


    def test_code_set_is_set_identical_to_phase12_snapshot(self):
        """The current catalogue's DSX-* code SET is identical to the frozen
        Phase-12 snapshot (REQ-P13-06, D-07).

        The count invariant above pins cardinality, but a mint-one/drop-one swap
        preserves the count and slips through it. A set-identity diff is strictly
        stronger: it names any code added since Phase 12 and any code dropped. The
        snapshot is a byte-copy of the generated ``references/finding-codes.md``;
        both sides are parsed with the same CRLF-safe, non-line-anchored ``_ROW_RE``
        the count invariant uses, so there is no parser drift and a CRLF checkout
        cannot silently empty either side.
        """
        current_set = set(_ROW_RE.findall(_CATALOGUE_PATH.read_text(encoding="utf-8")))
        snapshot_set = set(_ROW_RE.findall(_SNAPSHOT_PATH.read_text(encoding="utf-8")))

        self.assertEqual(
            len(snapshot_set), _EXPECTED_TOTAL,
            f"frozen Phase-12 snapshot enumerates {len(snapshot_set)} distinct codes, "
            f"expected {_EXPECTED_TOTAL} — the snapshot fixture is not a clean byte-copy "
            "of the generated catalogue",
        )

        added = sorted(current_set - snapshot_set)
        removed = sorted(snapshot_set - current_set)
        self.assertEqual(
            current_set, snapshot_set,
            f"catalogue code SET drifted from the Phase-12 snapshot (D-07): "
            f"added={added} removed={removed} — Phase 13 mints and drops ZERO codes, so "
            "the sets must be identical; a cardinality-preserving swap the count "
            "invariant passes is caught here",
        )


if __name__ == "__main__":
    unittest.main()
