"""Test suite for ``dsx/frame/admissibility.py`` -- ``DSX-ADM-*`` frequentist
procedure admissibility (Phase 11, REQ-P11-02). Stdlib unittest -- no pytest
dependency.

Two tasks, two groups of tests:

- ``TestLoadOntology*`` -- ``load_ontology()``'s refuse-not-degrade contract
  and its citation-drop behaviour (task 1).
- ``TestAliasIndex*``, ``TestCandidateFamilies*``,
  ``TestResolveDeclaredProcedure*``, ``TestDeclaredProcedure*`` -- exact-match,
  pair-scoped alias resolution (task 2).

No finding is emitted anywhere in this module -- this plan builds the loader
and the resolver only.

Run:  python3 -m unittest tests.test_frame_admissibility -v
"""

from __future__ import annotations

import dataclasses
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dsx.findings import CheckError  # noqa: E402
from dsx.frame import admissibility  # noqa: E402

FAMILIES_PATH = ROOT / "references" / "families.yaml"


# A single, always-valid minimal ontology fixture -- one token, one rule, one
# family -- used as the base every structural-error test breaks one piece of.
_MINIMAL_VALID_YAML = """\
assumption_vocabulary:
  - token: "example_token"
    citation: "Example, A. (2020), Example Journal"
    locator_status: "verified"
    notes: "fixture"
ranking_rules:
  - id: "example_rule"
    prefers: "family_a"
    over: "family_b"
    condition: "fixture condition"
    strength: "default_preference"
    citation: "Example, A. (2020), Example Journal"
    locator_status: "verified"
    notes: "fixture"
families:
  - id: "family_a"
    estimand: "difference_in_means"
    family: "family_a"
    inference_method: "frequentist"
    dependence: "none"
    aliases: ["alias_a"]
    buys: []
    charges: []
    traceability: "fixture"
    citation: "Example, A. (2020), Example Journal"
    locator_status: "verified"
    notes: "fixture"
"""


def _write_yaml(tmp_dir: Path, name: str, text: str) -> Path:
    path = tmp_dir / name
    path.write_text(text, encoding="utf-8")
    return path


class _CacheClearingTestCase(unittest.TestCase):
    """Clears ``admissibility``'s module-global ontology cache before and
    after every test, mirroring ``dsx/suppressions.py``'s ``known_codes()``
    cache-clearing convention -- one test's cached path must never leak into
    the next."""

    def setUp(self) -> None:
        admissibility._ONTOLOGY_CACHE.clear()

    def tearDown(self) -> None:
        admissibility._ONTOLOGY_CACHE.clear()


class TestLoadOntologyGoldenPath(_CacheClearingTestCase):
    def test_default_path_returns_fourteen_families_and_four_rules(self):
        ontology = admissibility.load_ontology()
        self.assertEqual(len(ontology.families), 14, ontology.families)
        self.assertEqual(len(ontology.rules), 4, ontology.rules)

    def test_second_call_returns_the_identical_cached_object(self):
        first = admissibility.load_ontology()
        second = admissibility.load_ontology()
        self.assertIs(first, second)

    def test_real_file_drops_no_family_and_carries_nineteen_tokens(self):
        ontology = admissibility.load_ontology()
        self.assertEqual(ontology.dropped_uncited, ())
        self.assertEqual(len(ontology.tokens), 19, ontology.tokens)

    def test_tokens_maps_every_assumption_vocabulary_token_to_its_citation(self):
        ontology = admissibility.load_ontology()
        self.assertTrue(all(isinstance(v, str) and v for v in ontology.tokens.values()))
        self.assertIn("exchangeability", ontology.tokens)
        self.assertIn("Hernan", ontology.tokens["exchangeability"])


class TestLoadOntologyMissingFile(_CacheClearingTestCase):
    def test_missing_path_raises_check_error_naming_the_path(self):
        missing = Path("references") / "does-not-exist-for-test.yaml"
        with self.assertRaises(CheckError) as ctx:
            admissibility.load_ontology(missing)
        self.assertIn(str(missing), str(ctx.exception))


class TestLoadOntologyStructuralErrors(_CacheClearingTestCase):
    def test_top_level_sequence_raises_check_error_naming_the_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "seq.yaml", "- a\n- b\n")
            with self.assertRaises(CheckError) as ctx:
                admissibility.load_ontology(path)
            self.assertIn(str(path), str(ctx.exception))

    def test_missing_families_key_raises_check_error_naming_the_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = _MINIMAL_VALID_YAML.replace("families:", "not_families:")
            path = _write_yaml(Path(tmp), "no-families.yaml", text)
            with self.assertRaises(CheckError) as ctx:
                admissibility.load_ontology(path)
            self.assertIn(str(path), str(ctx.exception))

    def test_families_not_a_list_raises_check_error_naming_the_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = _MINIMAL_VALID_YAML.split("families:")[0] + 'families: "not a list"\n'
            path = _write_yaml(Path(tmp), "families-not-list.yaml", text)
            with self.assertRaises(CheckError) as ctx:
                admissibility.load_ontology(path)
            self.assertIn(str(path), str(ctx.exception))

    def test_missing_assumption_vocabulary_raises_check_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = _MINIMAL_VALID_YAML.replace(
                "assumption_vocabulary:", "not_assumption_vocabulary:"
            )
            path = _write_yaml(Path(tmp), "no-vocab.yaml", text)
            with self.assertRaises(CheckError) as ctx:
                admissibility.load_ontology(path)
            self.assertIn(str(path), str(ctx.exception))

    def test_missing_ranking_rules_raises_check_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = _MINIMAL_VALID_YAML.replace("ranking_rules:", "not_ranking_rules:")
            path = _write_yaml(Path(tmp), "no-rules.yaml", text)
            with self.assertRaises(CheckError) as ctx:
                admissibility.load_ontology(path)
            self.assertIn(str(path), str(ctx.exception))


class TestLoadOntologyDroppedUncited(_CacheClearingTestCase):
    def test_one_uncited_family_is_dropped_and_named(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = _MINIMAL_VALID_YAML + (
                '  - id: "family_uncited"\n'
                '    estimand: "difference_in_means"\n'
                '    family: "family_uncited"\n'
                '    inference_method: "frequentist"\n'
                '    dependence: "none"\n'
                '    aliases: ["alias_uncited"]\n'
                "    buys: []\n"
                "    charges: []\n"
                '    traceability: "fixture"\n'
                '    citation: ""\n'
                '    locator_status: "unverified"\n'
                '    notes: "deliberately uncited fixture entry"\n'
            )
            path = _write_yaml(Path(tmp), "one-uncited.yaml", text)
            ontology = admissibility.load_ontology(path)
            self.assertEqual(len(ontology.families), 1)
            self.assertEqual(ontology.families[0].id, "family_a")
            self.assertEqual(ontology.dropped_uncited, ("family_uncited",))

    def test_every_family_uncited_returns_zero_families_without_raising(self):
        with tempfile.TemporaryDirectory() as tmp:
            # Blank only the citation line inside the families: block --
            # assumption_vocabulary and ranking_rules keep their own real
            # citations further up in the fixture, so this isolates the
            # families-only drop behaviour.
            lines = _MINIMAL_VALID_YAML.splitlines(keepends=True)
            out = []
            in_families = False
            for line in lines:
                if line.startswith("families:"):
                    in_families = True
                if in_families and line.strip().startswith('citation: "Example'):
                    out.append('    citation: ""\n')
                else:
                    out.append(line)
            text = "".join(out)
            path = _write_yaml(Path(tmp), "all-uncited.yaml", text)
            ontology = admissibility.load_ontology(path)
            self.assertEqual(ontology.families, ())
            self.assertEqual(ontology.dropped_uncited, ("family_a",))


class TestFamilyAndRankingRuleFrozen(_CacheClearingTestCase):
    def test_family_is_frozen_with_tuple_sequence_fields(self):
        ontology = admissibility.load_ontology()
        family = ontology.families[0]
        with self.assertRaises(dataclasses.FrozenInstanceError):
            family.id = "mutated"  # type: ignore[misc]
        self.assertIsInstance(family.aliases, tuple)
        self.assertIsInstance(family.buys, tuple)
        self.assertIsInstance(family.charges, tuple)

    def test_ranking_rule_is_frozen(self):
        ontology = admissibility.load_ontology()
        rule = ontology.rules[0]
        with self.assertRaises(dataclasses.FrozenInstanceError):
            rule.id = "mutated"  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main(verbosity=2)
