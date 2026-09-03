"""REQ-P20-02 — the zero-mint / catalogue-close proof (D-01, D-08).

Phase 20 is the *terminal* phase of its milestone and mints ZERO codes: it adds no
``report.add`` call site, so the finding catalogue closed at exactly 275 and the
pre-allocated ``DSX-STA`` range stops at 122 with the 123-129 band unused and the
130s reserve untouched. (A later milestone, Phase 22, additively mints DSX-VIZ-071,
moving the live total to 276 — the count-pin below tracks the live total in
lockstep, while the zero-mint tell here is the untouched DSX-STA reserve band.) This module turns that "mints zero codes" claim into a runnable oracle
rather than an unverified assertion, and also pins two standing invariants already
satisfied during Phases 18-19 (all fifteen milestone codes are D-05-allowlisted by
EXACT string; ``DSX-STA-`` is not an allowlisted prefix).

Five checks, each a machine oracle:

  1. references/finding-codes.md declares the pinned live total (275 at the Phase-20
     zero-mint close; 276 after Phase 22's additive DSX-VIZ-071 mint — the generated
     catalogue, never hand-edited).
  2. tests/fixtures/finding-codes-phase12.md declares 256 (the byte-frozen Phase-12
     snapshot) and its parsed code-set is a SUBSET of the current catalogue — the
     catalogue only ever grows additively, so nothing in the frozen snapshot may
     have been dropped or renamed.
  3. The fifteen milestone codes (Phase-18 050/051/060/061/062 and Phase-19
     070/080/081/090/100/110/111/120/121/122) are ALL members of
     ``gen-finding-catalogue.py::_D05_ALLOWLIST_CODES`` by exact string, and
     ``"DSX-STA-"`` is NOT in ``_D05_ALLOWLIST_PREFIXES`` — a prefix add would
     retroactively obligate ~40 uncited legacy DSX-STA codes (the exact-code path
     is the deliberate one).
  4. The reserve band from 123 upward (constructed from a numeric range, never
     hard-coded) is ABSENT from the catalogue's DSX-STA codes — the deliberate
     zero-mint tell, mirroring REQ-P19-03's absent 06x decade.
  5. The canonical good fixture examples/good-ANALYSIS-SPEC.yaml fires NONE of the
     fifteen at ship (the read-only silence proof over the happy-path corpus).

The generator is loaded via ``importlib.util`` so its ``__main__`` guard does not
run — this module only reads its module-level constants. Stdlib only (unittest, re,
pathlib, importlib.util); CRLF-safe throughout (encoding="utf-8", no line-anchored
regex over raw bytes).
"""

import importlib.util
import pathlib
import re
import unittest

from dsx.checks import stats
from dsx.loader import load

_ROOT = pathlib.Path(__file__).resolve().parents[1]
_CATALOGUE = _ROOT / "references" / "finding-codes.md"
_PHASE12_SNAPSHOT = _ROOT / "tests" / "fixtures" / "finding-codes-phase12.md"
_GENERATOR = _ROOT / "scripts" / "gen-finding-catalogue.py"

# The fifteen codes this milestone minted, by EXACT string: the Phase-18 five
# (correlation scale/kind + agreement completeness) and the Phase-19 ten (RM /
# trend / resampling / post-hoc / variance-role / power / proportion-count). Named
# literally here so the allowlist assertion is exact-match, not prefix-match.
_MILESTONE_CODES = frozenset(
    {
        "DSX-STA-050", "DSX-STA-051", "DSX-STA-060", "DSX-STA-061", "DSX-STA-062",
        "DSX-STA-070", "DSX-STA-080", "DSX-STA-081", "DSX-STA-090", "DSX-STA-100",
        "DSX-STA-110", "DSX-STA-111", "DSX-STA-120", "DSX-STA-121", "DSX-STA-122",
    }
)

_TOTAL_RE = re.compile(r"Total:\s*(\d+)\s*codes", re.IGNORECASE)
_CODE_RE = re.compile(r"DSX-[A-Z]+-\d+")
_STA_RE = re.compile(r"DSX-STA-(\d+)")


def _declared_total(path: pathlib.Path) -> int:
    """The 'Total: N codes.' header value; CRLF-safe (regex is not line-anchored)."""
    text = path.read_text(encoding="utf-8")
    m = _TOTAL_RE.search(text)
    assert m is not None, f"no 'Total: N codes' header in {path.name}"
    return int(m.group(1))


def _codes_in(path: pathlib.Path) -> "set[str]":
    return set(_CODE_RE.findall(path.read_text(encoding="utf-8")))


def _load_generator():
    """Import scripts/gen-finding-catalogue.py without running its __main__ guard."""
    spec = importlib.util.spec_from_file_location("gfc_zero_mint", _GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestPhase20ZeroMintClose(unittest.TestCase):
    def test_catalogue_declares_expected_total(self) -> None:
        """The generated catalogue declares the pinned live total. Phase 20 minted
        zero (the catalogue closed at 275); Phase 22 then additively minted
        DSX-VIZ-071, moving the live total to 276. This leg stays in lockstep with
        tests/test_finding_catalogue_invariant.py::_EXPECTED_TOTAL; Phase 20's
        zero-mint tell is carried by the reserve-band-absent and snapshot-subset
        checks below, not by this absolute total."""
        self.assertEqual(
            _declared_total(_CATALOGUE), 276,
            "references/finding-codes.md must declare 276 codes (275 at the Phase-20 "
            "zero-mint close, +1 for Phase 22's additive DSX-VIZ-071 mint)",
        )

    def test_phase12_snapshot_frozen_at_256_and_subset(self) -> None:
        """The frozen Phase-12 snapshot declares 256 and is a subset of the catalogue."""
        self.assertEqual(
            _declared_total(_PHASE12_SNAPSHOT), 256,
            "tests/fixtures/finding-codes-phase12.md must declare 256 (byte-frozen)",
        )
        snapshot_codes = _codes_in(_PHASE12_SNAPSHOT)
        current_codes = _codes_in(_CATALOGUE)
        dropped = snapshot_codes - current_codes
        self.assertFalse(
            dropped,
            f"Phase-12 snapshot codes missing from the current catalogue "
            f"(the catalogue must only grow additively): {sorted(dropped)}",
        )

    def test_fifteen_codes_allowlisted_by_exact_string(self) -> None:
        """All fifteen milestone codes are D-05-allowlisted by exact code, not prefix."""
        gen = _load_generator()
        allowlist = set(gen._D05_ALLOWLIST_CODES)
        missing = _MILESTONE_CODES - allowlist
        self.assertFalse(
            missing,
            f"milestone codes missing from _D05_ALLOWLIST_CODES by exact string: "
            f"{sorted(missing)}",
        )
        self.assertNotIn(
            "DSX-STA-", gen._D05_ALLOWLIST_PREFIXES,
            "DSX-STA- must NOT be an allowlisted prefix (would obligate ~40 uncited "
            "legacy codes); the fifteen are named by exact code instead",
        )

    def test_reserve_band_123_onward_absent(self) -> None:
        """The 123-onward DSX-STA reserve is absent from the catalogue — the zero-mint tell."""
        present = {int(n) for n in _STA_RE.findall(_CATALOGUE.read_text(encoding="utf-8"))}
        # Construct the reserve band programmatically (123-129 band + 130s reserve and
        # beyond); never hard-code the tokens, so a future mint into the band is caught.
        reserve = {n for n in range(123, 200)}
        leaked = sorted(reserve & present)
        self.assertFalse(
            leaked,
            f"reserve band leaked into the catalogue (Phase 20 must mint zero codes): "
            f"{['DSX-STA-%d' % n for n in leaked]}",
        )
        # And the tell holds positively: the highest DSX-STA code is 122.
        self.assertEqual(
            max(present), 122,
            "the pre-allocated DSX-STA range must stop at 122 (123-onward unused)",
        )

    def test_good_fixture_silent_on_the_fifteen(self) -> None:
        """The canonical good fixture fires none of the fifteen at ship."""
        report = stats.check(load(str(_ROOT / "examples" / "good-ANALYSIS-SPEC.yaml")))
        fired = _MILESTONE_CODES & {f.code for f in report.findings}
        self.assertFalse(
            fired,
            f"good fixture fired a milestone code (must stay silent): {sorted(fired)}",
        )


if __name__ == "__main__":
    unittest.main()
