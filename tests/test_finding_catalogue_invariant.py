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


if __name__ == "__main__":
    unittest.main()
