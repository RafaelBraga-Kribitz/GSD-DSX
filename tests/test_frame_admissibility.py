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


def _fam(**overrides) -> "admissibility.Family":
    base = dict(
        id="fam",
        family="fam",
        estimand="difference_in_means",
        inference_method="frequentist",
        dependence="none",
        aliases=(),
        buys=(),
        charges=(),
        traceability="fixture",
        citation="Example (2020)",
        locator_status="verified",
        notes="fixture",
    )
    base.update(overrides)
    return admissibility.Family(**base)


class TestAliasIndex(_CacheClearingTestCase):
    def test_index_maps_pair_to_normalized_alias_to_family_id(self):
        ontology = admissibility.load_ontology()
        index = admissibility.alias_index(ontology)
        pair = ("difference_in_proportions", "none")
        self.assertIn(pair, index)
        self.assertEqual(index[pair]["fishers_exact"], "fishers_exact")

    def test_collision_within_same_pair_raises_check_error_naming_both_and_alias(self):
        fam_a = _fam(id="fam_a", aliases=("shared_alias",))
        fam_b = _fam(id="fam_b", aliases=("Shared-Alias",))
        ontology = admissibility.Ontology(
            families=(fam_a, fam_b), rules=(), tokens={}, dropped_uncited=()
        )
        with self.assertRaises(CheckError) as ctx:
            admissibility.alias_index(ontology)
        message = str(ctx.exception)
        self.assertIn("fam_a", message)
        self.assertIn("fam_b", message)
        self.assertIn("shared_alias", message.lower())

    def test_same_alias_in_different_pairs_does_not_raise(self):
        ontology = admissibility.load_ontology()
        index = admissibility.alias_index(ontology)
        independent = index[("difference_in_proportions", "none")]
        clustered = index[("difference_in_proportions", "clustered")]
        self.assertEqual(independent["two_proportion_z"], "two_proportion_z")
        self.assertEqual(clustered["two_proportion_z"], "two_proportion_z_cluster_robust")


class TestCandidateFamilies(_CacheClearingTestCase):
    def test_matches_both_axes_sorted_lexicographically_by_id(self):
        ontology = admissibility.load_ontology()
        candidates = admissibility.candidate_families(
            ontology, "difference_in_proportions", "clustered"
        )
        self.assertEqual([f.id for f in candidates], ["two_proportion_z_cluster_robust"])

    def test_case_and_hyphen_insensitive_axis_match(self):
        ontology = admissibility.load_ontology()
        candidates = admissibility.candidate_families(
            ontology, "Difference-In-Proportions", "CLUSTERED"
        )
        self.assertEqual([f.id for f in candidates], ["two_proportion_z_cluster_robust"])

    def test_unknown_pair_returns_empty_tuple(self):
        ontology = admissibility.load_ontology()
        self.assertEqual(
            admissibility.candidate_families(ontology, "ratio_of_means", "spatial"), ()
        )

    def test_blank_or_none_axis_returns_empty_tuple(self):
        ontology = admissibility.load_ontology()
        self.assertEqual(admissibility.candidate_families(ontology, "", "none"), ())
        self.assertEqual(
            admissibility.candidate_families(ontology, "difference_in_means", ""), ()
        )
        self.assertEqual(
            admissibility.candidate_families(ontology, None, "none"), ()  # type: ignore[arg-type]
        )

    def test_order_independent_of_family_order_in_ontology(self):
        ontology = admissibility.load_ontology()
        reversed_ontology = dataclasses.replace(
            ontology, families=tuple(reversed(ontology.families))
        )
        original = [
            f.id
            for f in admissibility.candidate_families(
                ontology, "regression_coefficient", "clustered"
            )
        ]
        flipped = [
            f.id
            for f in admissibility.candidate_families(
                reversed_ontology, "regression_coefficient", "clustered"
            )
        ]
        self.assertEqual(original, flipped)
        self.assertEqual(original, sorted(original))


class TestResolveDeclaredProcedure(_CacheClearingTestCase):
    def test_not_declared_on_blank(self):
        ontology = admissibility.load_ontology()
        for declared in ("", "   ", None):
            with self.subTest(declared=declared):
                resolution = admissibility.resolve_declared_procedure(
                    ontology, "difference_in_means", "none", declared
                )
                self.assertEqual(resolution.status, "not_declared")
                self.assertEqual(resolution.family_id, "")

    def test_in_candidate_set_on_exact_normalized_alias(self):
        ontology = admissibility.load_ontology()
        resolution = admissibility.resolve_declared_procedure(
            ontology, "difference_in_proportions", "clustered", "two_proportion_z"
        )
        self.assertEqual(resolution.status, "in_candidate_set")
        self.assertEqual(resolution.family_id, "two_proportion_z_cluster_robust")
        self.assertEqual(resolution.outside_axes, ())

    def test_case_and_hyphen_insensitive_resolution(self):
        ontology = admissibility.load_ontology()
        resolution = admissibility.resolve_declared_procedure(
            ontology, "difference_in_proportions", "clustered", "TWO-PROPORTION-Z"
        )
        self.assertEqual(resolution.status, "in_candidate_set")

    def test_outside_candidate_set_names_the_family_and_its_own_axes(self):
        ontology = admissibility.load_ontology()
        resolution = admissibility.resolve_declared_procedure(
            ontology, "difference_in_means", "none", "fishers_exact"
        )
        self.assertEqual(resolution.status, "outside_candidate_set")
        self.assertEqual(resolution.family_id, "fishers_exact")
        self.assertEqual(
            resolution.outside_axes, ("difference_in_proportions", "none")
        )

    def test_unresolved_on_unknown_alias(self):
        ontology = admissibility.load_ontology()
        resolution = admissibility.resolve_declared_procedure(
            ontology, "difference_in_means", "none", "welch_tt"
        )
        self.assertEqual(resolution.status, "unresolved")
        self.assertEqual(resolution.family_id, "")

    def test_near_miss_variants_of_a_real_alias_are_unresolved(self):
        ontology = admissibility.load_ontology()
        # "welch_t" is a real alias; a prefix, and two one/two-character
        # edits of it, are deliberately not.
        near_misses = ["welch_", "welch_tx", "welch_txx"]
        for declared in near_misses:
            with self.subTest(declared=declared):
                resolution = admissibility.resolve_declared_procedure(
                    ontology, "difference_in_means", "none", declared
                )
                self.assertEqual(resolution.status, "unresolved")

    def test_status_vocabulary_is_closed_to_exactly_four_values(self):
        self.assertEqual(
            set(admissibility._RESOLUTION_STATUSES),
            {"not_declared", "in_candidate_set", "outside_candidate_set", "unresolved"},
        )


class TestDeclaredProcedure(_CacheClearingTestCase):
    def test_non_dict_spec_returns_empty_string(self):
        self.assertEqual(admissibility.declared_procedure(None), "")
        self.assertEqual(admissibility.declared_procedure("not a spec"), "")  # type: ignore[arg-type]
        self.assertEqual(admissibility.declared_procedure([]), "")  # type: ignore[arg-type]

    def test_no_inference_block_returns_empty_string(self):
        self.assertEqual(admissibility.declared_procedure({}), "")

    def test_non_mapping_inference_value_returns_empty_string(self):
        self.assertEqual(
            admissibility.declared_procedure({"inference": "not a mapping"}), ""
        )

    def test_blank_primary_procedure_returns_empty_string(self):
        self.assertEqual(
            admissibility.declared_procedure({"inference": {"primary_procedure": ""}}),
            "",
        )
        self.assertEqual(admissibility.declared_procedure({"inference": {}}), "")

    def test_declared_string_returned_unchanged(self):
        self.assertEqual(
            admissibility.declared_procedure(
                {"inference": {"primary_procedure": "welch_t"}}
            ),
            "welch_t",
        )


# ── Task 1: rank_admissible() -- the comparator, the rule table, and ────────
# byte-stable order (D-12, D-13, D-14, D-15)


class TestRankAdmissible(_CacheClearingTestCase):
    def test_ranked_entry_has_expected_fields_and_sequence_types(self):
        ontology = admissibility.load_ontology()
        candidates = admissibility.candidate_families(
            ontology, "difference_in_means", "none"
        )
        ranked = admissibility.rank_admissible(candidates, ontology.rules)
        self.assertEqual(len(ranked), 2)
        for index, entry in enumerate(ranked, start=1):
            self.assertEqual(entry.rank, index)
            self.assertIsInstance(entry.buys, tuple)
            self.assertIsInstance(entry.charges, tuple)

    def test_welch_over_students_places_welch_first(self):
        ontology = admissibility.load_ontology()
        candidates = admissibility.candidate_families(
            ontology, "difference_in_means", "none"
        )
        ranked = admissibility.rank_admissible(candidates, ontology.rules)
        self.assertEqual([e.id for e in ranked], ["welch_t", "students_t"])
        self.assertEqual(ranked[0].placed_by, "")
        self.assertEqual(ranked[1].placed_by, "welch_over_students")

    def test_interacted_adjustment_overrides_fewer_assumptions_criterion(self):
        ontology = admissibility.load_ontology()
        candidates = admissibility.candidate_families(
            ontology, "regression_coefficient", "none"
        )
        ranked = admissibility.rank_admissible(candidates, ontology.rules)
        self.assertEqual(ranked[0].id, "linear_regression_interacted_adjustment")
        self.assertGreater(len(ranked[0].charges), len(ranked[1].charges))
        self.assertEqual(ranked[1].placed_by, "interacted_adjustment_over_unadjusted")

    def test_manski_fallback_and_lexicographic_tiebreak_in_one_ranking(self):
        # A single real four-family candidate set exercises both non-rule
        # placement branches in sequence: boschloo_over_fishers_exact places
        # the first two by a cited rule, fishers -> two_proportion_z falls
        # back to the fewer-assumptions criterion (2 charges vs 5), and
        # two_proportion_z -> two_proportion_z_always_valid (5 charges each,
        # no rule between them) falls back to the lexicographic tiebreak.
        ontology = admissibility.load_ontology()
        candidates = admissibility.candidate_families(
            ontology, "difference_in_proportions", "none"
        )
        ranked = admissibility.rank_admissible(candidates, ontology.rules)
        self.assertEqual(
            [e.id for e in ranked],
            [
                "boschloo_exact",
                "fishers_exact",
                "two_proportion_z",
                "two_proportion_z_always_valid",
            ],
        )
        self.assertEqual(ranked[0].placed_by, "")
        self.assertEqual(ranked[1].placed_by, "boschloo_over_fishers_exact")
        self.assertEqual(ranked[2].placed_by, admissibility._MANSKI_RULE)
        self.assertEqual(ranked[3].placed_by, admissibility._TIEBREAK_RULE)

    def test_permutation_of_input_order_produces_byte_identical_ranking(self):
        import itertools

        ontology = admissibility.load_ontology()
        candidates = list(
            admissibility.candidate_families(
                ontology, "difference_in_proportions", "none"
            )
        )
        base = [
            e.id
            for e in admissibility.rank_admissible(tuple(candidates), ontology.rules)
        ]
        outcomes = {
            tuple(
                e.id
                for e in admissibility.rank_admissible(tuple(p), ontology.rules)
            )
            for p in itertools.permutations(candidates)
        }
        self.assertEqual(len(outcomes), 1)
        self.assertEqual(list(next(iter(outcomes))), base)

    def test_calling_twice_produces_equal_output(self):
        ontology = admissibility.load_ontology()
        candidates = admissibility.candidate_families(
            ontology, "difference_in_proportions", "none"
        )
        first = admissibility.rank_admissible(candidates, ontology.rules)
        second = admissibility.rank_admissible(candidates, ontology.rules)
        self.assertEqual(first, second)

    def test_empty_candidate_tuple_returns_empty_tuple(self):
        ontology = admissibility.load_ontology()
        self.assertEqual(admissibility.rank_admissible((), ontology.rules), ())

    def test_single_element_candidate_tuple_ranks_first_with_no_placement(self):
        ontology = admissibility.load_ontology()
        candidates = admissibility.candidate_families(
            ontology, "difference_in_proportions", "clustered"
        )
        self.assertEqual(len(candidates), 1)
        ranked = admissibility.rank_admissible(candidates, ontology.rules)
        self.assertEqual(len(ranked), 1)
        self.assertEqual(ranked[0].rank, 1)
        self.assertEqual(ranked[0].placed_by, "")

    def test_rule_whose_partner_is_absent_from_candidates_is_inert(self):
        # welch_over_students names students_t and welch_t; scoping the
        # candidate set to a pair that contains neither must never surface
        # that rule id as a placed_by value.
        ontology = admissibility.load_ontology()
        candidates = admissibility.candidate_families(
            ontology, "difference_in_proportions", "none"
        )
        ranked = admissibility.rank_admissible(candidates, ontology.rules)
        placed_by_values = {e.placed_by for e in ranked}
        self.assertNotIn("welch_over_students", placed_by_values)


class TestDominatingRules(_CacheClearingTestCase):
    def test_returns_rules_naming_the_family_as_dominated(self):
        ontology = admissibility.load_ontology()
        candidates = admissibility.candidate_families(
            ontology, "difference_in_means", "none"
        )
        rules = admissibility.dominating_rules(
            "students_t", candidates, ontology.rules
        )
        self.assertEqual([r.id for r in rules], ["welch_over_students"])

    def test_returns_empty_tuple_when_no_rule_dominates(self):
        ontology = admissibility.load_ontology()
        candidates = admissibility.candidate_families(
            ontology, "difference_in_means", "none"
        )
        self.assertEqual(
            admissibility.dominating_rules("welch_t", candidates, ontology.rules), ()
        )

    def test_returns_empty_tuple_for_a_one_element_candidate_set(self):
        ontology = admissibility.load_ontology()
        candidates = admissibility.candidate_families(
            ontology, "difference_in_proportions", "clustered"
        )
        self.assertEqual(len(candidates), 1)
        self.assertEqual(
            admissibility.dominating_rules(
                candidates[0].id, candidates, ontology.rules
            ),
            (),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
