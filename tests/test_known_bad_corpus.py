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
import re
import sys
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


def _slugs(pattern: str, suffix: str) -> set[str]:
    return {p.name[: -len(suffix)] for p in CORPUS_DIR.glob(pattern)}


class TestKnownBadCorpus(unittest.TestCase):
    def _spec_paths(self) -> list[Path]:
        return sorted(CORPUS_DIR.glob(f"*{SPEC_SUFFIX}"))

    def _postmortem_paths(self) -> list[Path]:
        return sorted(CORPUS_DIR.glob(f"*{POSTMORTEM_SUFFIX}"))

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


if __name__ == "__main__":
    unittest.main()
