"""Tests for scripts/gen-finding-catalogue.py — D-05 citation/reference-value/
test-linkage enforcement (REQ-P6-11, D-20 through D-23).

`scripts/gen-finding-catalogue.py` is a script, not an installed module, so it is
loaded by path via `importlib.util.spec_from_file_location`.

Run:  python3 -m unittest tests.test_gen_finding_catalogue -v
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = _ROOT / "scripts" / "gen-finding-catalogue.py"


def _load_script():
    spec = importlib.util.spec_from_file_location("gen_finding_catalogue", _SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


g = _load_script()


def _write(root: Path, name: str, content: str) -> None:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# ── Task 1: check_d05 core mechanics (synthetic code_root/tests_root) ──────────


class TestD05Core(unittest.TestCase):
    def test_check_d05_ignores_uncovered_prefix(self):
        # DSX-VIZ-030 matches no allow-list prefix — must return [] no matter how
        # bare its docstring is, and even against directories that do not exist.
        rows = [("DSX-VIZ-030", "HIGH", "t", "viz")]
        missing = Path(tempfile.mkdtemp()) / "does-not-exist"
        self.assertEqual(g.check_d05(rows, missing, missing), [])

    def test_check_d05_flags_missing_citation(self):
        with tempfile.TemporaryDirectory() as code_dir, tempfile.TemporaryDirectory() as tests_dir:
            _write(
                Path(code_dir),
                "check.py",
                '''
def f(report):
    """
    Reference value: 42
    """
    report.add("DSX-PAR-001", "HIGH", "t")
''',
            )
            _write(Path(tests_dir), "test_marker.py", "# D-05: DSX-PAR-001\n")
            rows = [("DSX-PAR-001", "HIGH", "t", "frame/paradigm")]
            problems = g.check_d05(rows, Path(code_dir), Path(tests_dir))
            self.assertTrue(any("Citation" in p and "DSX-PAR-001" in p for p in problems))

    def test_check_d05_flags_missing_reference_value(self):
        with tempfile.TemporaryDirectory() as code_dir, tempfile.TemporaryDirectory() as tests_dir:
            _write(
                Path(code_dir),
                "check.py",
                '''
def f(report):
    """
    Citation: Example, A. (2020), "A Study", Table 1.
    """
    report.add("DSX-PAR-001", "HIGH", "t")
''',
            )
            _write(Path(tests_dir), "test_marker.py", "# D-05: DSX-PAR-001\n")
            rows = [("DSX-PAR-001", "HIGH", "t", "frame/paradigm")]
            problems = g.check_d05(rows, Path(code_dir), Path(tests_dir))
            self.assertTrue(
                any("Reference value" in p and "DSX-PAR-001" in p for p in problems)
            )

    def test_check_d05_flags_missing_test_marker(self):
        with tempfile.TemporaryDirectory() as code_dir, tempfile.TemporaryDirectory() as tests_dir:
            _write(
                Path(code_dir),
                "check.py",
                '''
def f(report):
    """
    Citation: Example, A. (2020), "A Study", Table 1.
    Reference value: 42
    """
    report.add("DSX-PAR-001", "HIGH", "t")
''',
            )
            # tests_dir deliberately left without a matching marker file.
            _write(Path(tests_dir), "test_other.py", "# D-05: DSX-PAR-002\n")
            rows = [("DSX-PAR-001", "HIGH", "t", "frame/paradigm")]
            problems = g.check_d05(rows, Path(code_dir), Path(tests_dir))
            self.assertTrue(any("marker" in p and "DSX-PAR-001" in p for p in problems))

    def test_check_d05_passes_fully_compliant_code(self):
        with tempfile.TemporaryDirectory() as code_dir, tempfile.TemporaryDirectory() as tests_dir:
            _write(
                Path(code_dir),
                "check.py",
                '''
def f(report):
    """
    Citation: Example, A. (2020), "A Study", Table 1.
    Reference value: 42
    """
    report.add("DSX-PAR-001", "HIGH", "t")
''',
            )
            _write(Path(tests_dir), "test_marker.py", "# D-05: DSX-PAR-001\n")
            rows = [("DSX-PAR-001", "HIGH", "t", "frame/paradigm")]
            self.assertEqual(g.check_d05(rows, Path(code_dir), Path(tests_dir)), [])

    def test_resolve_docstrings_function_level(self):
        with tempfile.TemporaryDirectory() as code_dir:
            _write(
                Path(code_dir),
                "check.py",
                '''
"""Module docstring — must not be picked up when a function docstring exists."""


def f(report):
    """Citation: Function Level (2020), "Case"."""
    report.add("DSX-PAR-001", "HIGH", "t")
''',
            )
            docstrings = g._resolve_docstrings(Path(code_dir))
            self.assertIn("Function Level", docstrings["DSX-PAR-001"])

    def test_resolve_docstrings_module_level_fallback(self):
        with tempfile.TemporaryDirectory() as code_dir:
            _write(
                Path(code_dir),
                "check.py",
                '''
"""Citation: Module Level (2020), "Case".

Reference value: 1
"""
report.add("DSX-PAR-001", "HIGH", "t")
''',
            )
            docstrings = g._resolve_docstrings(Path(code_dir))
            self.assertIn("Module Level", docstrings["DSX-PAR-001"])

    def test_collect_test_markers_finds_marker(self):
        with tempfile.TemporaryDirectory() as tests_dir:
            _write(
                Path(tests_dir),
                "test_marker.py",
                "class T:\n    def test_x(self):\n        pass  # D-05: DSX-PAR-001\n",
            )
            markers = g._collect_test_markers(Path(tests_dir))
            self.assertIn("DSX-PAR-001", markers)

    def test_dsx_par_prefix_group_registered(self):
        prefixes = [prefix for prefix, _heading, _blurb in g.PREFIX_GROUPS]
        self.assertIn("DSX-PAR", prefixes)

    def test_dsx_crv_prefix_group_registered(self):
        # REQ-P11.3-06/D-12: dsx/checks/chart_review.py is a brand-new family —
        # this is Pitfall 2's loud-failure guard (the rows would otherwise
        # silently vanish from the rendered catalogue while staying in the count).
        prefixes = [prefix for prefix, _heading, _blurb in g.PREFIX_GROUPS]
        self.assertIn("DSX-CRV", prefixes)

    def test_dsx_crv_prefix_in_d05_allowlist(self):
        # REQ-P11.3-06/D-12: Pitfall 3's loud-failure guard — DSX-CRV-* must be
        # opted into D-05 citation enforcement, not silently exempt from it.
        self.assertIn("DSX-CRV-", g._D05_ALLOWLIST_PREFIXES)

    def test_every_collected_code_resolves_to_a_prefix_group(self):
        prefixes = [prefix for prefix, _heading, _blurb in g.PREFIX_GROUPS]
        unresolved = [
            row[0]
            for row in g.collect()
            if not any(row[0].startswith(prefix + "-") for prefix in prefixes)
        ]
        self.assertEqual(unresolved, [])

    def test_every_d05_allowlist_prefix_ends_in_a_hyphen(self):
        # WR-03/D-20: a bare numeric-string prefix (no trailing hyphen) silently
        # over-matches any longer code sharing its digits — every family-prefix
        # entry must be hyphen-terminated so it can only ever match a whole
        # family, never part of a numeric suffix.
        for prefix in g._D05_ALLOWLIST_PREFIXES:
            self.assertTrue(
                prefix.endswith("-"), f"{prefix!r} is not hyphen-terminated"
            )

    def test_check_d05_does_not_cover_a_longer_numeric_neighbour_of_an_enforced_code(self):
        enforced_code = next(iter(g._D05_ALLOWLIST_CODES))
        neighbour_code = enforced_code + "9"  # an unenumerated longer neighbour
        with tempfile.TemporaryDirectory() as code_dir, tempfile.TemporaryDirectory() as tests_dir:
            # No citation, no reference value, no test marker for either code —
            # a non-compliant docstring is what would surface a false-positive
            # over-match if the neighbour were accidentally covered.
            _write(
                Path(code_dir),
                "check.py",
                '''
def f(report):
    """No citation or reference value here."""
    report.add("{enforced}", "HIGH", "t")
    report.add("{neighbour}", "HIGH", "t")
'''.format(enforced=enforced_code, neighbour=neighbour_code),
            )
            _write(Path(tests_dir), "test_marker.py", f"# D-05: {enforced_code}\n")

            neighbour_rows = [(neighbour_code, "HIGH", "t", "check")]
            self.assertEqual(
                g.check_d05(neighbour_rows, Path(code_dir), Path(tests_dir)),
                [],
                "an unenumerated longer numeric neighbour must not be covered",
            )

            enforced_rows = [(enforced_code, "HIGH", "t", "check")]
            problems = g.check_d05(enforced_rows, Path(code_dir), Path(tests_dir))
            self.assertTrue(
                problems,
                "the enforced code itself, with a non-compliant docstring, must "
                "still produce a problem",
            )

    def test_d05_covered_code_set_on_the_real_tree_is_exactly_the_documented_set(self):
        rows = g.collect()
        prefixes = g._D05_ALLOWLIST_PREFIXES
        codes = g._D05_ALLOWLIST_CODES
        covered = {row[0] for row in rows if row[0].startswith(prefixes) or row[0] in codes}
        family_matched = {row[0] for row in rows if row[0].startswith(prefixes)}
        self.assertEqual(covered, family_matched | codes)


# ── Task 2: enforcement proven against a committed violating fixture ───────────

_FIXTURE_DIR = _ROOT / "tests" / "fixtures" / "d05"


class TestD05EnforcementFixture(unittest.TestCase):
    """Proves both halves of D-05 can actually fail (ROADMAP Success Criterion 4).

    `tests/fixtures/d05/bad_check.py` is not test*-named, so `unittest discover`
    never collects it as a test module (nothing in it is ever imported or run).
    """

    def test_violating_fixture_flags_missing_reference_value(self):
        rows = [("DSX-PAR-999", "HIGH", "t", "fixtures")]
        with tempfile.TemporaryDirectory() as tests_dir:
            _write(Path(tests_dir), "test_marker.py", "# D-05: DSX-PAR-999\n")
            problems = g.check_d05(rows, _FIXTURE_DIR, Path(tests_dir))
        self.assertTrue(
            any("Reference value" in p and "DSX-PAR-999" in p for p in problems),
            f"enforcement failed to detect the violating fixture: {problems!r}",
        )

    def test_violating_fixture_flags_missing_test_marker(self):
        rows = [("DSX-PAR-999", "HIGH", "t", "fixtures")]
        # No `# D-05: DSX-PAR-999` marker anywhere under this empty tests root.
        empty_tests_dir = Path(tempfile.mkdtemp())
        problems = g.check_d05(rows, _FIXTURE_DIR, empty_tests_dir)
        self.assertTrue(
            any("marker" in p and "DSX-PAR-999" in p for p in problems),
            f"enforcement failed to detect the missing test marker: {problems!r}",
        )

    def test_check_d05_ignores_uncovered_code_against_fixture_dir(self):
        rows = [("DSX-VIZ-030", "HIGH", "t", "viz")]
        self.assertEqual(
            g.check_d05(rows, _FIXTURE_DIR, Path(tempfile.mkdtemp())), []
        )

    def test_compliant_fixture_code_produces_no_problem(self):
        rows = [("DSX-SPEC-089", "HIGH", "t", "fixtures")]
        with tempfile.TemporaryDirectory() as tests_dir:
            _write(Path(tests_dir), "test_marker.py", "# D-05: DSX-SPEC-089\n")
            problems = g.check_d05(rows, _FIXTURE_DIR, Path(tests_dir))
        self.assertEqual(problems, [])

    def test_unittest_discover_excludes_fixture_module(self):
        # Isolated subprocess scoped to the fixture directory alone (start_dir ==
        # top_level_dir) — avoids self-recursively re-running the whole `tests/`
        # suite (which would include this very test) while still proving
        # `unittest discover`'s default `test*.py` pattern never collects
        # `bad_check.py`.
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(_FIXTURE_DIR), "-v"],
            cwd=str(_ROOT),
            capture_output=True,
            text=True,
        )
        # unittest exits 5 (not 0) when discovery finds zero tests — that IS the
        # assertion: bad_check.py's two functions must never be collected.
        self.assertIn("NO TESTS RAN", result.stderr, result.stderr)
        self.assertNotIn("bad_check", result.stderr)

    def test_collect_excludes_fixture_only_codes(self):
        fixture_codes = {row[0] for row in g.collect()}
        self.assertNotIn("DSX-PAR-999", fixture_codes)
        self.assertNotIn("DSX-SPEC-089", fixture_codes)


class TestD05RealTreeStandingGuarantee(unittest.TestCase):
    """The standing guarantee: the real tree returns zero D-05 problems.

    This is what turns D-05 from a convention into a build gate for every later
    phase — the 206 pre-existing codes produce zero new failures, and every
    allow-listed code this phase ships is compliant.
    """

    def test_real_tree_check_d05_is_empty(self):
        self.assertEqual(g.check_d05(g.collect(), g.ROOT / "dsx", g.ROOT / "tests"), [])


# ── Task 1: check_families_citations() — the build-time citation gate over the
#    ontology data (D-23, D-24) ──────────────────────────────────────────────

_REAL_FAMILIES_YAML = _ROOT / "references" / "families.yaml"


def _minimal_families_yaml(
    *,
    family_citation: str | None = '"Author, A. (2020), Some Paper"',
    assumption_citation: str | None = '"Author, A. (2020), Some Paper"',
    rule_citation: str | None = '"Author, A. (2020), Some Paper"',
    include_families_key: bool = True,
) -> str:
    """A minimal, schema-shaped families.yaml, with each block's citation
    independently overridable so a single field can be blanked or omitted
    without disturbing the other two blocks."""

    def _citation_line(value: str | None) -> str:
        if value is None:
            return ""  # key omitted entirely
        return f"    citation: {value}\n"

    families_block = ""
    if include_families_key:
        families_block = (
            "families:\n"
            '  - id: "family_one"\n'
            '    estimand: "difference_in_proportions"\n'
            '    family: "family_one"\n'
            '    inference_method: "frequentist"\n'
            '    dependence: "none"\n'
            '    aliases: ["family_one"]\n'
            "    buys: []\n"
            '    charges: ["exchangeability"]\n'
            '    traceability: "n/a"\n'
            f"{_citation_line(family_citation)}"
            '    locator_status: "verified"\n'
            '    notes: "n/a"\n'
        )

    return (
        "vocabulary_is_not_exhaustive: true\n\n"
        "assumption_vocabulary:\n"
        '  - token: "exchangeability"\n'
        f"{_citation_line(assumption_citation)}"
        '    locator_status: "verified"\n'
        '    notes: "n/a"\n\n'
        "ranking_rules:\n"
        '  - id: "rule_one"\n'
        '    prefers: "a"\n'
        '    over: "b"\n'
        '    condition: "c"\n'
        '    strength: "default_preference"\n'
        f"{_citation_line(rule_citation)}"
        '    locator_status: "verified"\n'
        '    notes: "n/a"\n\n'
        f"{families_block}"
    )


class TestFamiliesCitationGate(unittest.TestCase):
    def test_committed_families_yaml_has_no_citation_problems(self):
        self.assertEqual(g.check_families_citations(_REAL_FAMILIES_YAML), [])

    def test_blank_family_citation_reports_one_problem_naming_the_id(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "families.yaml"
            path.write_text(
                _minimal_families_yaml(family_citation='""'), encoding="utf-8"
            )
            problems = g.check_families_citations(path)
            self.assertEqual(len(problems), 1, problems)
            self.assertIn("family_one", problems[0])

    def test_missing_family_citation_key_reports_one_problem_naming_the_id(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "families.yaml"
            path.write_text(
                _minimal_families_yaml(family_citation=None), encoding="utf-8"
            )
            problems = g.check_families_citations(path)
            self.assertEqual(len(problems), 1, problems)
            self.assertIn("family_one", problems[0])

    def test_blank_assumption_vocabulary_citation_reports_problem_naming_the_token(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "families.yaml"
            path.write_text(
                _minimal_families_yaml(assumption_citation='""'), encoding="utf-8"
            )
            problems = g.check_families_citations(path)
            self.assertEqual(len(problems), 1, problems)
            self.assertIn("exchangeability", problems[0])

    def test_blank_ranking_rule_citation_reports_problem_naming_the_id(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "families.yaml"
            path.write_text(
                _minimal_families_yaml(rule_citation='""'), encoding="utf-8"
            )
            problems = g.check_families_citations(path)
            self.assertEqual(len(problems), 1, problems)
            self.assertIn("rule_one", problems[0])

    def test_reports_every_problem_rather_than_stopping_at_the_first(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "families.yaml"
            path.write_text(
                _minimal_families_yaml(
                    family_citation='""',
                    assumption_citation='""',
                    rule_citation='""',
                ),
                encoding="utf-8",
            )
            problems = g.check_families_citations(path)
            self.assertEqual(len(problems), 3, problems)

    def test_nonexistent_path_reports_one_problem_naming_the_path(self):
        missing = Path(tempfile.mkdtemp()) / "does-not-exist.yaml"
        problems = g.check_families_citations(missing)
        self.assertEqual(len(problems), 1, problems)
        self.assertIn(str(missing), problems[0])

    def test_top_level_sequence_reports_one_problem_naming_the_path(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "families.yaml"
            path.write_text('- "a"\n- "b"\n', encoding="utf-8")
            problems = g.check_families_citations(path)
            self.assertEqual(len(problems), 1, problems)
            self.assertIn(str(path), problems[0])

    def test_families_key_absent_reports_one_problem_naming_the_path(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "families.yaml"
            path.write_text(
                _minimal_families_yaml(include_families_key=False), encoding="utf-8"
            )
            problems = g.check_families_citations(path)
            self.assertEqual(len(problems), 1, problems)
            self.assertIn(str(path), problems[0])

    def test_families_key_not_a_list_reports_one_problem_naming_the_path(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "families.yaml"
            content = _minimal_families_yaml(include_families_key=False)
            content += 'families: "not a list"\n'
            path.write_text(content, encoding="utf-8")
            problems = g.check_families_citations(path)
            self.assertEqual(len(problems), 1, problems)
            self.assertIn(str(path), problems[0])

    def test_repeated_calls_do_not_duplicate_the_repository_root_on_sys_path(self):
        # Other test modules under this suite insert ROOT (or an equivalent
        # path) onto sys.path themselves at import time, unguarded — so the
        # baseline count here is whatever the rest of the discovered suite
        # already left behind, not necessarily zero or one. What this test
        # proves is narrower and still exact: *this function's own guard*
        # never adds a second entry once ROOT is already present.
        g.check_families_citations(_REAL_FAMILIES_YAML)
        before = sys.path.count(str(g.ROOT))
        g.check_families_citations(_REAL_FAMILIES_YAML)
        after = sys.path.count(str(g.ROOT))
        self.assertEqual(before, after)
        self.assertGreaterEqual(before, 1)

    def test_check_exits_0_against_the_committed_tree(self):
        result = subprocess.run(
            [sys.executable, str(_SCRIPT), "--check"],
            cwd=str(_ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("D-24:", result.stderr)

    def test_check_exits_1_with_d24_prefix_on_an_uncited_family(self):
        import shutil

        with tempfile.TemporaryDirectory() as tmp:
            tree = Path(tmp) / "tree"
            shutil.copytree(_ROOT, tree, ignore=shutil.ignore_patterns(".git"))
            fam_path = tree / "references" / "families.yaml"
            text = fam_path.read_text(encoding="utf-8")
            # Blank the first family's citation line — two_proportion_z is the
            # first entry in the committed file.
            text = text.replace(
                'citation: "Agresti, A. (2013), Categorical Data Analysis, 3rd edition"\n'
                '    locator_status: "unverified"\n'
                "    notes: \"No chapter locator was confirmed by this project for the "
                "two-proportion z-test's normal-approximation source.",
                'citation: ""\n'
                '    locator_status: "unverified"\n'
                "    notes: \"No chapter locator was confirmed by this project for the "
                "two-proportion z-test's normal-approximation source.",
                1,
            )
            fam_path.write_text(text, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(tree / "scripts" / "gen-finding-catalogue.py"), "--check"],
                cwd=str(tree),
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            d24_lines = [
                line for line in result.stderr.splitlines() if line.startswith("D-24:")
            ]
            self.assertTrue(d24_lines, result.stderr)
            self.assertIn("two_proportion_z", d24_lines[0])
            # The two prefixes are told apart: no line carries both.
            for line in result.stderr.splitlines():
                self.assertFalse(
                    line.startswith("D-05:") and "D-24:" in line, result.stderr
                )
                self.assertFalse(
                    line.startswith("D-24:") and "D-05:" in line, result.stderr
                )


# ── Task 2: "DSX-ADM-" in _D05_ALLOWLIST_PREFIXES — proving the citation
#    enforcement is live for the new family, not merely allow-listed (D-25) ───


class TestDsxAdmAllowlistEntry(unittest.TestCase):
    def test_dsx_adm_prefix_present_and_every_entry_hyphen_terminated(self):
        self.assertIn("DSX-ADM-", g._D05_ALLOWLIST_PREFIXES)
        for prefix in g._D05_ALLOWLIST_PREFIXES:
            self.assertTrue(prefix.endswith("-"), f"{prefix!r} is not hyphen-terminated")

    def test_check_d05_on_the_real_tree_is_still_empty_with_dsx_adm_covered(self):
        self.assertEqual(g.check_d05(g.collect(), g.ROOT / "dsx", g.ROOT / "tests"), [])

    def test_covered_code_set_on_the_real_tree_includes_both_new_codes(self):
        rows = g.collect()
        covered = {
            row[0]
            for row in rows
            if row[0].startswith(g._D05_ALLOWLIST_PREFIXES) or row[0] in g._D05_ALLOWLIST_CODES
        }
        self.assertIn("DSX-ADM-010", covered)
        self.assertIn("DSX-ADM-020", covered)

    def test_missing_citation_line_on_dsx_adm_010_is_reported(self):
        # Proves the gate is *live*, not merely that the real tree passes --
        # a passing-real-tree-only assertion would pass identically with the
        # prefix absent.
        with tempfile.TemporaryDirectory() as code_dir, tempfile.TemporaryDirectory() as tests_dir:
            _write(
                Path(code_dir),
                "check.py",
                '''
def f(report):
    """
    Structural criterion: fires when x.
    """
    report.add("DSX-ADM-010", "HIGH", "t")
''',
            )
            _write(Path(tests_dir), "test_marker.py", "# D-05: DSX-ADM-010\n")
            rows = [("DSX-ADM-010", "HIGH", "t", "frame/admissibility")]
            problems = g.check_d05(rows, Path(code_dir), Path(tests_dir))
            self.assertTrue(
                any("Citation" in p and "DSX-ADM-010" in p for p in problems), problems
            )

    def test_missing_structural_criterion_line_on_dsx_adm_010_is_reported(self):
        with tempfile.TemporaryDirectory() as code_dir, tempfile.TemporaryDirectory() as tests_dir:
            _write(
                Path(code_dir),
                "check.py",
                '''
def f(report):
    """
    Citation: Example, A. (2020), "A Study", Table 1.
    """
    report.add("DSX-ADM-010", "HIGH", "t")
''',
            )
            _write(Path(tests_dir), "test_marker.py", "# D-05: DSX-ADM-010\n")
            rows = [("DSX-ADM-010", "HIGH", "t", "frame/admissibility")]
            problems = g.check_d05(rows, Path(code_dir), Path(tests_dir))
            self.assertTrue(
                any("Reference value" in p and "DSX-ADM-010" in p for p in problems), problems
            )

    def test_missing_test_marker_for_dsx_adm_010_is_reported(self):
        with tempfile.TemporaryDirectory() as code_dir, tempfile.TemporaryDirectory() as tests_dir:
            _write(
                Path(code_dir),
                "check.py",
                '''
def f(report):
    """
    Citation: Example, A. (2020), "A Study", Table 1.
    Structural criterion: fires when x.
    """
    report.add("DSX-ADM-010", "HIGH", "t")
''',
            )
            # Deliberately no "# D-05: DSX-ADM-010" marker anywhere in tests_dir.
            _write(Path(tests_dir), "test_other.py", "# D-05: DSX-ADM-020\n")
            rows = [("DSX-ADM-010", "HIGH", "t", "frame/admissibility")]
            problems = g.check_d05(rows, Path(code_dir), Path(tests_dir))
            self.assertTrue(any("marker" in p and "DSX-ADM-010" in p for p in problems), problems)

    def test_check_exits_0_on_the_committed_tree(self):
        result = subprocess.run(
            [sys.executable, str(_SCRIPT), "--check"],
            cwd=str(_ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


# ── Task 3: canonical-declaration pin for codes emitted with divergent text from
#    more than one report.add() site (v2.0.0 milestone audit GAP-PROC-05) ───────
#
# These five codes each fire from multiple report.add() sites with a different
# (severity, title). collect() warns ("declared twice with different text") but
# does not block, and only the last-seen row lands in the rendered catalogue — so
# an edit to one site that diverges from its siblings, or a new site with new
# text, passes silently today. This pins the exact declaration set the
# generator's own extract() sees for each, and pins the membership of the
# divergent set itself, so the next code that starts diverging (Phases 11.2/11.3
# add more codes to the same catalogue) fails here and forces a conscious
# dedupe-or-pin decision rather than drifting unnoticed.

_PH = "<…>"  # what extract() renders any f-string interpolation as

_CANONICAL_DECLARATIONS = {
    "DSX-SPEC-070": {
        ("HIGH", "suppression entry is not a mapping"),
        ("HIGH", "suppression is missing code"),
        ("HIGH", f"suppression of {_PH} is missing reason"),
        ("HIGH", f"suppression of {_PH} is missing authority"),
    },
    "DSX-VAL-021": {
        ("HIGH", "validity frame assignment unit disagrees with design randomization unit"),
        ("HIGH", "validity frame analysis unit disagrees with design analysis unit"),
    },
    "DSX-VAL-060": {
        ("HIGH", "missingness mechanism paired with a method it does not license"),
        ("CRITICAL", "missingness mechanism paired with a method it does not license"),
    },
    "DSX-COH-030": {
        ("CRITICAL", "Causal/prescriptive question has an empty assumptions list"),
        ("HIGH", "Causal/prescriptive question has an empty assumptions list"),
    },
    "DSX-PAR-002": {
        ("HIGH", f"inference.paradigm ({_PH}) is declared with no paradigm_justification"),
        ("HIGH", "inference.paradigm is not declared under an uncontrolled continuous design"),
    },
    # Phase 11.2-05 (D-03): DSX-CLM-020/021 now fire from two literal report.add
    # sites each — one causal, one prescriptive — reusing the identical codes and
    # severities so relabelling causal→prescriptive buys zero severity arbitrage.
    # The text is parameterised on claim type; the severity is unchanged.
    "DSX-CLM-020": {
        ("CRITICAL", "Causal claim with no identification strategy behind it"),
        (
            "CRITICAL",
            "Prescriptive claim recommends an intervention with no identification "
            "strategy behind it",
        ),
    },
    "DSX-CLM-021": {
        ("HIGH", f"Unhedged causal claim resting on a weak strategy ('{_PH}')"),
        (
            "HIGH",
            f"Prescriptive claim recommends an intervention on a weak strategy ('{_PH}')",
        ),
    },
}


class TestCanonicalDeclarations(unittest.TestCase):
    """Pin the divergent-text finding codes (milestone audit GAP-PROC-05)."""

    @staticmethod
    def _declarations_by_code() -> "dict[str, set]":
        by_code: "dict[str, set]" = {}
        for source in sorted((_ROOT / "dsx").rglob("*.py")):
            for code, severity, title in g.extract(source):
                by_code.setdefault(code, set()).add((severity, title))
        return by_code

    def test_each_known_divergent_code_has_its_pinned_declarations(self):
        by_code = self._declarations_by_code()
        for code, expected in _CANONICAL_DECLARATIONS.items():
            self.assertEqual(
                by_code.get(code, set()),
                expected,
                f"{code} declaration set drifted from its pin — if this change is "
                "deliberate, update _CANONICAL_DECLARATIONS and say why in the commit",
            )

    def test_divergent_code_set_is_exactly_the_pinned_five(self):
        by_code = self._declarations_by_code()
        divergent = {code for code, decls in by_code.items() if len(decls) > 1}
        self.assertEqual(
            divergent,
            set(_CANONICAL_DECLARATIONS),
            "the set of finding codes emitted with divergent (severity, title) "
            "changed — a new code started diverging or a pinned one converged; "
            "dedupe it or add it to _CANONICAL_DECLARATIONS deliberately",
        )


if __name__ == "__main__":
    unittest.main()
