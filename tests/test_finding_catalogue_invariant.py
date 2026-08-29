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

# The pinned count. Phase 16 mints DSX-REP-060/061 (D-08 additive rebaseline), so the
# live catalogue is 258 — up from the 256 the byte-frozen Phase-12 snapshot enumerates.
_EXPECTED_TOTAL = 258

# The byte-frozen Phase-12 snapshot's own size, and the explicit Phase-16 delta over it.
# Kept SEPARATE from _EXPECTED_TOTAL on purpose: tests/fixtures/finding-codes-phase12.md
# is never mutated (D-08) and stays at 256, while the live catalogue is 258 — conflating
# the two would break the snapshot-length leg after the bump (D-08 trap #3).
_SNAPSHOT_TOTAL = 256
_MINTED_CODES = {"DSX-REP-060", "DSX-REP-061"}

# The declared-total line — matched after whitespace-collapse, so it is agnostic to
# ``\n`` vs ``\r\n`` and to any incidental wrapping of the surrounding prose.
_TOTAL_RE = re.compile(r"\*\*Total:\s*(\d+)\s*codes\.\*\*")

# Every catalogue row is a Markdown table cell `| `DSX-<FAMILY>-<digits>` | ...`. The
# same shape ``tests/test_known_bad_corpus.py::_catalogue_codes`` reads; not line
# anchored, so it is CRLF-safe.
_ROW_RE = re.compile(r"\|\s*`(DSX-[A-Z]+-\d+)`\s*\|")


class TestCatalogueInvariant(unittest.TestCase):
    def test_finding_catalogue_stays_at_258_codes(self):
        """The catalogue declares, and enumerates, exactly 258 codes (D-08).

        Two independent readings of the same generated artifact must agree on 258:
        the human-facing ``**Total: N codes.**`` line and the machine count of
        ``DSX-*`` table rows. Requiring both to equal 258 catches a stale Total line
        as well as a minted or dropped code, without re-walking the ``dsx/`` AST here —
        this test stays a pure reader of the same file ``gen-finding-catalogue.py
        --check`` gates. Phase 16 added DSX-REP-060/061 additively (256 -> 258); any
        further movement is a new mint or drop and belongs to its own phase.
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
            "Phase 16 mints exactly DSX-REP-060/061 over the frozen 256 (D-08); if a "
            "code was legitimately added or removed beyond that, that change belongs "
            "to its own check-shipping phase, not a silent edit here",
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


    def test_code_set_is_phase12_snapshot_plus_the_phase16_mint(self):
        """The current catalogue's DSX-* code SET equals the frozen Phase-12
        snapshot PLUS exactly the Phase-16 mint {DSX-REP-060, DSX-REP-061} (D-08).

        The count invariant above pins cardinality, but a mint-one/drop-one swap
        preserves the count and slips through it. A set-identity diff is strictly
        stronger: it names any code added beyond the sanctioned delta and any code
        dropped. The snapshot is a byte-copy of the *Phase-12* generated
        ``references/finding-codes.md`` (256 codes) and is never mutated (D-08); the
        expected live set is therefore ``snapshot ∪ {060, 061}``. Both sides are
        parsed with the same CRLF-safe, non-line-anchored ``_ROW_RE`` the count
        invariant uses, so there is no parser drift and a CRLF checkout cannot
        silently empty either side.
        """
        current_set = set(_ROW_RE.findall(_CATALOGUE_PATH.read_text(encoding="utf-8")))
        snapshot_set = set(_ROW_RE.findall(_SNAPSHOT_PATH.read_text(encoding="utf-8")))

        self.assertEqual(
            len(snapshot_set), _SNAPSHOT_TOTAL,
            f"frozen Phase-12 snapshot enumerates {len(snapshot_set)} distinct codes, "
            f"expected {_SNAPSHOT_TOTAL} — the snapshot fixture is not a clean byte-copy "
            "of the Phase-12 catalogue (it must stay byte-frozen at 256, D-08)",
        )

        expected_set = snapshot_set | _MINTED_CODES
        added = sorted(current_set - expected_set)
        removed = sorted(expected_set - current_set)
        self.assertEqual(
            current_set, expected_set,
            f"catalogue code SET drifted from 'Phase-12 snapshot ∪ {sorted(_MINTED_CODES)}' "
            f"(D-08): added={added} removed={removed} — Phase 16 mints exactly "
            "DSX-REP-060/061 and drops nothing, so the sets must be identical; a "
            "cardinality-preserving swap the count invariant passes is caught here",
        )


if __name__ == "__main__":
    unittest.main()
