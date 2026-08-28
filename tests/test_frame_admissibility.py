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
from dsx.loader import load  # noqa: E402

FAMILIES_PATH = ROOT / "references" / "families.yaml"
GOOD_SPEC_PATH = ROOT / "examples" / "good-ANALYSIS-SPEC.yaml"


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

    def test_one_uncited_ranking_rule_is_dropped_and_named(self):
        # WR-03 (11-REVIEW.md): the run-time drop must cover ranking_rules
        # too, not just families -- a rule's citation is surfaced directly
        # inside a live DSX-ADM-010 finding's detail text via
        # dominating_rules(), so an uncited rule reaching a live gate run
        # (e.g. a hand-edited file that skipped --check) must not be usable
        # to cite an empty string in a finding.
        text = _MINIMAL_VALID_YAML.replace(
            '    citation: "Example, A. (2020), Example Journal"\n'
            '    locator_status: "verified"\n'
            '    notes: "fixture"\n'
            "families:",
            '    citation: ""\n'
            '    locator_status: "unverified"\n'
            '    notes: "deliberately uncited fixture rule"\n'
            "families:",
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "uncited-rule.yaml", text)
            ontology = admissibility.load_ontology(path)
            self.assertEqual(ontology.rules, ())
            self.assertEqual(ontology.dropped_uncited, ("example_rule",))
            # The families block, untouched by this fixture edit, still loads.
            self.assertEqual(len(ontology.families), 1)


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

    def test_order_independent_of_ontology_file_order_when_two_rules_dominate(self):
        # WR-01 (11-REVIEW.md): every other order-sensitive path in this
        # module refuses to let the ontology file's own entry order leak
        # into an outcome (alias_index() raises on a collision rather than
        # last-one-wins; candidate_families() sorts by id;
        # resolve_declared_procedure() takes the lexicographically first id
        # on a tie). dominating_rules() must do the same -- its return order
        # must not depend on which of two dominating rules the ontology file
        # happens to list first. Not reachable in the committed
        # references/families.yaml today (no family is currently named
        # `over` by two different ranking_rules entries), so this is
        # synthetic by necessity, exactly the case the review's own
        # reproduction used.
        def _family(fid):
            return admissibility.Family(
                id=fid, family=fid, estimand="e", inference_method="frequentist",
                dependence="none", aliases=(), buys=(), charges=(),
                traceability="", citation="c", locator_status="verified", notes="",
            )

        def _rule(rid, prefers):
            return admissibility.RankingRule(
                id=rid, prefers=prefers, over="b", condition="always",
                strength="uniform_domination", citation="c",
                locator_status="verified", notes="",
            )

        candidates = (_family("a"), _family("b"), _family("z"))
        rule_a_first = _rule("rule_a_first", "a")
        rule_z_last = _rule("rule_z_last", "z")

        forward = admissibility.dominating_rules(
            "b", candidates, (rule_a_first, rule_z_last)
        )
        reversed_ = admissibility.dominating_rules(
            "b", candidates, (rule_z_last, rule_a_first)
        )
        self.assertEqual([r.id for r in forward], [r.id for r in reversed_])
        self.assertEqual([r.id for r in forward], ["rule_a_first", "rule_z_last"])


# ── Task 2: admissible_families() -- the pure return shape naming ───────────
# assumptions bought and charged (REQ-P11-03, REQ-P11-04, D-16)


_ADMISSIBLE_ENTRY_KEYS = {
    "rank", "id", "family", "buys", "charges", "citation", "locator_status",
    "notes", "placed_by",
}


class TestAdmissibleFamilies(_CacheClearingTestCase):
    def test_returns_plain_json_serialisable_dict_with_expected_keys(self):
        import json

        result = admissibility.admissible_families(load(GOOD_SPEC_PATH))
        self.assertEqual(
            set(result),
            {
                "estimand", "dependence", "declared_procedure", "resolution",
                "resolved_family", "admissible", "refusal", "refusal_cause",
                "ontology_entries",
            },
        )
        # No dataclass, no tuple anywhere in the returned structure.
        json.dumps(result)

    def test_good_fixture_resolves_to_exactly_one_admissible_family(self):
        result = admissibility.admissible_families(load(GOOD_SPEC_PATH))
        self.assertEqual(
            [e["id"] for e in result["admissible"]],
            ["two_proportion_z_cluster_robust"],
        )
        self.assertEqual(result["resolution"], "in_candidate_set")
        self.assertEqual(result["refusal"], "")
        self.assertEqual(result["refusal_cause"], "")
        self.assertTrue(_ADMISSIBLE_ENTRY_KEYS <= set(result["admissible"][0]))

    def test_blank_estimand_refuses_with_required_axis_blank(self):
        spec = {
            "validity_frame": {
                "estimand": {"type": ""},
                "dependence": {"structure": "none"},
            }
        }
        result = admissibility.admissible_families(spec)
        self.assertEqual(result["admissible"], [])
        self.assertEqual(result["refusal"], "no_admissible_procedure")
        self.assertEqual(result["refusal_cause"], "required_axis_blank")

    def test_blank_dependence_refuses_with_required_axis_blank(self):
        spec = {
            "validity_frame": {
                "estimand": {"type": "difference_in_means"},
                "dependence": {"structure": ""},
            }
        }
        result = admissibility.admissible_families(spec)
        self.assertEqual(result["refusal_cause"], "required_axis_blank")

    def test_no_matching_family_refuses_with_no_matching_family(self):
        spec = {
            "validity_frame": {
                "estimand": {"type": "ratio_of_means"},
                "dependence": {"structure": "hierarchical"},
            }
        }
        result = admissibility.admissible_families(spec)
        self.assertEqual(result["admissible"], [])
        self.assertEqual(result["refusal_cause"], "no_matching_family")

    def test_unresolved_declared_procedure_refuses_but_still_lists_candidates(self):
        spec = {
            "validity_frame": {
                "estimand": {"type": "difference_in_means"},
                "dependence": {"structure": "none"},
            },
            "inference": {"primary_procedure": "not_a_real_test"},
        }
        result = admissibility.admissible_families(spec)
        self.assertEqual(result["refusal_cause"], "declared_procedure_unresolved")
        self.assertTrue(result["admissible"])

    def test_outside_candidate_set_declared_procedure_refuses(self):
        spec = {
            "validity_frame": {
                "estimand": {"type": "difference_in_means"},
                "dependence": {"structure": "none"},
            },
            "inference": {"primary_procedure": "fishers_exact"},
        }
        result = admissibility.admissible_families(spec)
        self.assertEqual(result["refusal_cause"], "declared_procedure_unresolved")
        self.assertTrue(result["admissible"])

    def test_causes_checked_in_order_blank_axis_first(self):
        # Both a blank axis AND a non-matching pair could apply -- blank axis
        # must win, proving the checked order.
        spec = {
            "validity_frame": {
                "estimand": {"type": ""},
                "dependence": {"structure": "spatial"},
            }
        }
        result = admissibility.admissible_families(spec)
        self.assertEqual(result["refusal_cause"], "required_axis_blank")

    def test_undeclared_procedure_is_not_a_refusal(self):
        spec = {
            "validity_frame": {
                "estimand": {"type": "difference_in_means"},
                "dependence": {"structure": "none"},
            }
        }
        result = admissibility.admissible_families(spec)
        self.assertEqual(result["resolution"], "not_declared")
        self.assertEqual(result["refusal"], "")
        self.assertEqual(len(result["admissible"]), 2)

    def test_none_and_non_mapping_spec_return_blank_axis_refusal_shape(self):
        for spec in (None, ["not", "a", "mapping"]):
            with self.subTest(spec=spec):
                result = admissibility.admissible_families(spec)
                self.assertEqual(result["refusal_cause"], "required_axis_blank")
                self.assertEqual(result["admissible"], [])

    def test_calling_twice_produces_json_identical_results(self):
        import json

        spec = load(GOOD_SPEC_PATH)
        first = admissibility.admissible_families(spec)
        second = admissibility.admissible_families(spec)
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))

    def test_ontology_entries_counts_loaded_families(self):
        ontology = admissibility.load_ontology()
        result = admissibility.admissible_families(load(GOOD_SPEC_PATH))
        self.assertEqual(result["ontology_entries"], len(ontology.families))

    def test_refusal_cause_vocabulary_is_closed_to_exactly_three_members(self):
        self.assertEqual(
            set(admissibility._REFUSAL_CAUSES),
            {
                "required_axis_blank",
                "no_matching_family",
                "declared_procedure_unresolved",
            },
        )


# ── Task 3: check() -- DSX-ADM-010 and DSX-ADM-020, one guard-set commit ────
# (REQ-P11-03, REQ-P11-04, D-06, D-12, D-13, D-14, D-16, D-17, D-19, D-21)


class TestCheck(_CacheClearingTestCase):
    def test_returns_empty_report_when_applies_to_frame_is_false(self):
        report = admissibility.check(load(GOOD_SPEC_PATH), applies_to_frame=False)
        self.assertEqual(report.findings, [])
        self.assertFalse(report.context.get("decisions"))

    def test_returns_empty_report_for_non_mapping_spec(self):
        for spec in (None, "not a spec", ["not", "a", "mapping"]):
            with self.subTest(spec=spec):
                report = admissibility.check(spec, applies_to_frame=True)
                self.assertEqual(report.findings, [])

    def test_good_fixture_emits_zero_findings_and_one_unescalated_decision(self):
        report = admissibility.check(load(GOOD_SPEC_PATH), applies_to_frame=True)
        self.assertEqual(report.findings, [])
        decisions = report.context.get("decisions") or []
        self.assertEqual(len(decisions), 1)
        self.assertFalse(decisions[0]["escalate"])

    def test_blank_estimand_type_emits_dsx_adm_020(self):
        spec = {
            "validity_frame": {
                "estimand": {"type": ""},
                "dependence": {"structure": "none"},
            }
        }
        report = admissibility.check(spec, applies_to_frame=True)
        self.assertEqual([f.code for f in report.findings], ["DSX-ADM-020"])
        self.assertEqual(report.findings[0].severity.name, "CRITICAL")
        self.assertIn("estimand", report.findings[0].where)

    def test_blank_dependence_structure_emits_dsx_adm_020_naming_dependence_field(self):
        spec = {
            "validity_frame": {
                "estimand": {"type": "difference_in_means"},
                "dependence": {"structure": ""},
            }
        }
        report = admissibility.check(spec, applies_to_frame=True)
        self.assertEqual([f.code for f in report.findings], ["DSX-ADM-020"])
        self.assertIn("dependence", report.findings[0].where)

    def test_no_matching_family_emits_dsx_adm_020_naming_both_axis_values(self):
        spec = {
            "validity_frame": {
                "estimand": {"type": "ratio_of_means"},
                "dependence": {"structure": "hierarchical"},
            }
        }
        report = admissibility.check(spec, applies_to_frame=True)
        self.assertEqual([f.code for f in report.findings], ["DSX-ADM-020"])
        self.assertIn("ratio_of_means", report.findings[0].detail)
        self.assertIn("hierarchical", report.findings[0].detail)

    def test_unresolved_declared_procedure_emits_dsx_adm_020_naming_the_label(self):
        spec = {
            "validity_frame": {
                "estimand": {"type": "difference_in_means"},
                "dependence": {"structure": "none"},
            },
            "inference": {"primary_procedure": "not_a_real_test"},
        }
        report = admissibility.check(spec, applies_to_frame=True)
        self.assertEqual([f.code for f in report.findings], ["DSX-ADM-020"])
        self.assertIn("not_a_real_test", report.findings[0].detail)

    def test_outside_candidate_set_emits_dsx_adm_020_naming_family_and_axes(self):
        spec = {
            "validity_frame": {
                "estimand": {"type": "difference_in_means"},
                "dependence": {"structure": "none"},
            },
            "inference": {"primary_procedure": "fishers_exact"},
        }
        report = admissibility.check(spec, applies_to_frame=True)
        self.assertEqual([f.code for f in report.findings], ["DSX-ADM-020"])
        self.assertIn("fishers_exact", report.findings[0].detail)

    def test_every_dsx_adm_020_path_escalates(self):
        specs = [
            {
                "validity_frame": {
                    "estimand": {"type": ""},
                    "dependence": {"structure": "none"},
                }
            },
            {
                "validity_frame": {
                    "estimand": {"type": "ratio_of_means"},
                    "dependence": {"structure": "hierarchical"},
                }
            },
            {
                "validity_frame": {
                    "estimand": {"type": "difference_in_means"},
                    "dependence": {"structure": "none"},
                },
                "inference": {"primary_procedure": "not_a_real_test"},
            },
        ]
        for spec in specs:
            with self.subTest(spec=spec):
                report = admissibility.check(spec, applies_to_frame=True)
                decisions = report.context.get("decisions") or []
                self.assertEqual(len(decisions), 1)
                self.assertTrue(decisions[0]["escalate"])

    # D-05: DSX-ADM-010
    def test_students_t_under_independent_difference_in_means_emits_dsx_adm_010(self):
        spec = {
            "validity_frame": {
                "estimand": {"type": "difference_in_means"},
                "dependence": {"structure": "none"},
            },
            "inference": {"primary_procedure": "students_t"},
        }
        report = admissibility.check(spec, applies_to_frame=True)
        self.assertEqual([f.code for f in report.findings], ["DSX-ADM-010"])
        finding = report.findings[0]
        self.assertEqual(finding.severity.name, "HIGH")
        self.assertIn("welch_over_students", finding.detail)
        self.assertIn("welch_t", finding.detail)
        self.assertIn("welch_t", finding.remedy)
        decisions = report.context.get("decisions") or []
        self.assertEqual(len(decisions), 1)
        self.assertFalse(decisions[0]["escalate"])

    def test_cv1_declaration_emits_dsx_adm_010_stating_the_hedge_not_a_domination(self):
        spec = {
            "validity_frame": {
                "estimand": {"type": "regression_coefficient"},
                "dependence": {"structure": "clustered"},
            },
            "inference": {"primary_procedure": "linear_regression_cv1"},
        }
        report = admissibility.check(spec, applies_to_frame=True)
        self.assertEqual([f.code for f in report.findings], ["DSX-ADM-010"])
        detail = report.findings[0].detail.lower()
        self.assertIn("reliability_hedged", detail)
        self.assertNotIn("uniformly dominates", detail)
        self.assertNotIn("uniform domination", detail)

    def test_no_committed_spec_emits_dsx_adm_010(self):
        import glob

        specs = sorted(
            glob.glob(str(ROOT / "examples" / "*-ANALYSIS-SPEC.yaml"))
            + glob.glob(str(ROOT / "examples" / "known-bad" / "*-ANALYSIS-SPEC.yaml"))
            + [str(ROOT / "templates" / "ANALYSIS-SPEC.yaml")]
        )
        hits = [
            path
            for path in specs
            if any(
                f.code == "DSX-ADM-010"
                for f in admissibility.check(
                    load(path), applies_to_frame=True
                ).findings
            )
        ]
        self.assertEqual(hits, [])

    def test_clear_path_lists_ranked_but_not_top_ids_as_alternatives_rejected(self):
        spec = {
            "validity_frame": {
                "estimand": {"type": "difference_in_proportions"},
                "dependence": {"structure": "none"},
            },
            "inference": {"primary_procedure": "boschloo_exact"},
        }
        report = admissibility.check(spec, applies_to_frame=True)
        self.assertEqual(report.findings, [])
        decisions = report.context.get("decisions") or []
        self.assertEqual(len(decisions), 1)
        rejected = decisions[0]["alternatives_rejected"]
        self.assertEqual(
            rejected,
            ["fishers_exact", "two_proportion_z", "two_proportion_z_always_valid"],
        )

    # D-05: DSX-ADM-020
    def test_known_codes_contains_both_dsx_adm_codes(self):
        from dsx.suppressions import known_codes

        # known_codes() is a module-global cache; a prior import of
        # dsx.suppressions in this same process may have cached it before
        # this module's report.add(...) call sites existed on disk during
        # earlier test runs in this file -- clear it so this assertion
        # reflects the live tree, matching the module's own re-scan pattern.
        import dsx.suppressions as suppressions

        suppressions._KNOWN = None
        codes = known_codes()
        self.assertIn("DSX-ADM-010", codes)
        self.assertIn("DSX-ADM-020", codes)


if __name__ == "__main__":
    unittest.main(verbosity=2)
