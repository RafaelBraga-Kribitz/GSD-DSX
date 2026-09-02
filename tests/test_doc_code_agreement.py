"""REQ-P20-04 — doc/code AGREEMENT cross-check (read-only, D-02).

This is a *cross-check*, not a generated mirror: references/test-selection.md is
~280 lines of irreducible hand-written prose a generator cannot emit (20-CONTEXT
D-02), so we bind the doc to the routing engines and fail RED at build/CI time on
any divergence — the ``--check`` model. Per D-01 NO runtime doc/code-divergence
finding code is minted; a divergence is a broken build, not a spec-audit finding.

Two-tier binding:

  Tier 1 — STRICT cell-equality. Every Decision-table data row parses to
  ``recommend_test`` arguments and its primary Test cell EQUALS
  ``recommend_test(...)['test']``; any in-cell alternative is a MEMBER of
  ``['alternatives']``; and the proportion/2/no cell's Boschloo fallback is
  asserted present in ``['alternatives']`` — the exact cell the Boschloo
  divergence class lived in.

  Tier 2 — honest SET-MEMBERSHIP. Each of the six ``recommend_*`` mirror tables
  has every declared coefficient/test asserted a MEMBER of that engine's
  acceptable set for the row's declared key. Membership, never single-cell
  equality, because these tables are legitimately set-valued (Spearman-vs-Kendall)
  and equality would be a false model.

A VISIBLE, enumerated skip-list makes every un-bound row a DECLARED exclusion, and
an exhaustiveness assertion proves every pipe-delimited table row in the file is
either bound or explicitly skip-listed — so the test can NEVER pass by silently
failing to parse a row (the anti-false-pass control).

Standing v2.3 rule: the doc table and ``recommend_test`` move in lockstep. If this
cross-check ever surfaces a divergence, 20-D (sole writer of the doc and stats.py)
repairs whichever side is wrong in the SAME commit. Expected outcome today:
no divergence, both files byte-frozen. Stdlib only; CRLF-safe throughout.
"""

import pathlib
import re
import unittest

from dsx.checks import stats
from dsx.spec import normalize

DOC = pathlib.Path(__file__).resolve().parents[1] / "references" / "test-selection.md"
TEXT = DOC.read_text(encoding="utf-8")

# ── Presentation-form -> code-token normalisation (the parser bindings) ────────

# Unicode presentation glyphs the doc uses (kept as named constants so the source
# is legible and the literals cannot be mistyped).
EM_DASH = "—"   # —
GE = "≥"        # ≥
APPROX = "≈"    # ≈
PHI = "φ"       # φ
DASHES = {EM_DASH, "–", "-"}  # em / en / hyphen — any bare dash cell == "not applicable"

# Doc Test-label / coefficient spellings whose normalize() form differs from the
# engine's code token. Everything not listed here normalises directly (e.g.
# "Welch t" -> welch_t, "chi-square" -> chi_square) and needs no entry.
LABEL_MAP = {
    "negative_binomial": "negative_binomial_regression",
    "ordinal_logistic": "ordinal_logistic_regression",
    "cox": "cox_proportional_hazards",
    "scheffé": "scheffe",   # "Scheffé" — normalize() does not strip the accent
    "wilson_score": "wilson",
}

# Decision-table Groups cell -> n_groups; "any" is the count/time-to-event
# single-router case (recommend_test ignores n_groups there).
GROUPS = {"2": 2, "3+": 3, "any": 1}
# Paired cell -> paired flag; a bare dash means "not applicable" == False.
PAIRED = {"no": False, "yes": True}
# Distribution cell -> recommend_test kwargs (exact doc phrasings).
DIST = {
    "normal or n " + GE + " 200": {"normal": True, "n_per_group": 200},
    "skewed and n < 200": {"normal": False},
    "normal differences": {"normal": True},
    "skewed differences": {"normal": False},
    "normal, equal variance": {"normal": True, "equal_variance": True},
    "normal, unequal variance": {"normal": True, "equal_variance": False},
    "skewed": {"normal": False},
    "variance " + APPROX + " mean": {"overdispersed": False},
    "variance > mean": {"overdispersed": True},
    "censored": {},
}

# ### Correlation coefficient cells are prose (no backticks); match declared names.
CORR_PATTERNS = [
    ("point-biserial", "point_biserial"),
    ("pearson", "pearson_correlation"),
    ("spearman", "spearman_correlation"),
    ("kendall", "kendall_tau_b"),
    ("cramér", "cramers_v"),  # Cramér
    ("cramer", "cramers_v"),
    (PHI, "phi"),
]

# ## Trend context cells are prose that does not match recommend_trend's keys;
# each maps to the engine key whose acceptable set covers the row's declared test.
TREND_KEY = {
    "ordered dose / proportion": "dose_response",  # Cochran-Armitage ∈ dose_response
    "ordered groups": "ordered_trend",             # Jonckheere-Terpstra ∈ ordered_trend
    "temporal": "temporal",                        # Mann-Kendall + Sen's slope
}

# ── VISIBLE, enumerated skip-list (declared exclusions) ────────────────────────
# Whole sections that mint no acceptable-set mirror.
SKIP_SECTIONS = {
    "Categorical",                            # REQ-P19-03 mints zero codes — rows only
    "Variance pretest and power reporting",   # gate-only, keyed on declared roles
}
# Row-level exclusions inside otherwise-bound sections. Each entry is
# (lowercase substring that uniquely identifies the row, reason).
SKIP_ROW_MARKERS = [
    ("`agreement`", "agreement/reliability route — outside recommend_association's association scope (DSX-STA-051 negative space)"),
    ("`method_comparison`", "method-comparison route — Bland-Altman, outside recommend_association scope"),
    ("distance correlation", "catalog-only pointer, no routing target (REQ-P18-01)"),
    ("partial correlation", "catalog-only pointer, conditions on an undeclared covariate set"),
    ("linear mixed model", "pointer row — unbalanced/missing-cell RM belongs in an LMM, not a routing target"),
    ("| gee |", "pointer row — population-averaged repeated contrast, not a routing target"),
    ("student-newman-keuls", "deprecated post-hoc, never a member of any acceptable set"),
    ("unprotected lsd", "deprecated post-hoc at k>3, never a member of any acceptable set"),
    ("one-sample count vs a rate", "count-model row; recommend_proportion_ci covers proportion contexts only"),
    ("risk difference (rd)", "surfaced-not-gated interval (Newcombe), no proportion-CI membership"),
    ("odds ratio (or)", "surfaced-not-gated interval (Woolf)"),
    ("number needed to treat (nnt)", "NNT-with-CI is a DSX-STA-122 reporting gate, not a recommend_proportion_ci member"),
    ("zero-inflated / hurdle", "pointer row — excess-zero count structure, no routing target this phase"),
    ("vuong test", "deprecated misuse-finding, no replacement endorsed"),
]

# ── Parsing primitives (CRLF-safe) ─────────────────────────────────────────────


def _lines(text):
    return re.split(r"\r?\n", text)


def sig(line):
    """Whitespace-collapsed signature of a row — stable across leading indent."""
    return re.sub(r"\s+", " ", line.strip())


def row_cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _is_separator(line):
    cells = [c for c in row_cells(line) if c]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c) for c in cells)


def block(text, heading_prefix):
    """Return the text from the first heading starting with ``heading_prefix`` up to
    the next heading of the same-or-higher level (fewer/equal leading '#')."""
    lines = _lines(text)
    level = len(heading_prefix) - len(heading_prefix.lstrip("#"))
    start = next(i for i, l in enumerate(lines) if l.strip().startswith(heading_prefix))
    for j in range(start + 1, len(lines)):
        s = lines[j].strip()
        if s.startswith("#"):
            hashes = len(s) - len(s.lstrip("#"))
            if hashes <= level:
                return "\n".join(lines[start + 1:j])
    return "\n".join(lines[start + 1:])


def parse_tables(block_text):
    """Split a markdown block into its tables. Returns a list of tables, each a
    list of RAW data-row lines (header + separator excluded)."""
    tables = []
    cur = None
    in_table = False
    for line in _lines(block_text):
        if line.strip().startswith("|"):
            if _is_separator(line):
                in_table = True
                continue
            if not in_table:      # header row — starts a new table
                cur = []
                tables.append(cur)
                continue
            cur.append(line)      # data row
        else:
            in_table = False
    return [t for t in tables if t]


def first_table(heading_prefix):
    return parse_tables(block(TEXT, heading_prefix))[0]


def canon(token):
    """Doc token -> code spelling: strip backticks/bold/footnote/parenthetical,
    normalize(), then apply the explicit LABEL_MAP. An unmapped token falls
    through to its normalize() form (so a genuine mismatch fails loudly)."""
    t = re.sub(r"`", "", token)
    t = re.sub(r"\*\*", "", t)
    t = re.sub(r"\[\^[^\]]*\]", "", t)
    t = re.sub(r"\([^)]*\)", "", t)
    t = normalize(t)
    return LABEL_MAP.get(t, t)


def backtick_tokens(cell):
    return {canon(m) for m in re.findall(r"`([^`]+)`", cell)}


def extract_methods(cell):
    """Acceptable-set column -> {code tokens}. Prefer a backticked code token per
    fragment; else canon() the prose. Fragments split on ';' and '/'."""
    out = set()
    for frag in re.split(r"[;/]", cell):
        frag = frag.strip()
        if not frag:
            continue
        ticks = re.findall(r"`([^`]+)`", frag)
        if ticks:
            out.update(canon(t) for t in ticks)
        else:
            out.add(canon(frag))
    return out


def corr_coeffs(cell):
    low = cell.lower()
    got = set()
    for pat, tok in CORR_PATTERNS:
        if pat in low:
            got.add(tok)
    return got


def token_of(cell):
    m = re.findall(r"`([^`]+)`", cell)
    return canon(m[0]) if m else canon(cell)


def parse_test_cell(cell):
    c = re.sub(r"\[\^[^\]]*\]", "", cell)   # drop [^1] footnote marker
    c = re.sub(r"\*\*", "", c)              # drop bold
    c = re.sub(r"\([^)]*\)", "", c)         # drop parenthetical (…fallback…)
    parts = [p.strip() for p in re.split(r"\s+or\s+|,", c) if p.strip()]
    return canon(parts[0]), [canon(p) for p in parts[1:]]


def _collect_bound_signatures():
    """The 31 rows this cross-check binds (15 decision + 16 mirror). Computed
    independently of the engine so the exhaustiveness net does not depend on any
    assertion having run first."""
    b = set()
    for raw in first_table("## Decision table"):
        b.add(sig(raw))
    for raw in first_table("### Correlation"):
        b.add(sig(raw))
    for raw in first_table("## Repeated measures"):
        b.add(sig(raw))
    for raw in first_table("## Trend"):
        b.add(sig(raw))
    for raw in first_table("## Resampling"):
        b.add(sig(raw))
    for raw in first_table("## Post-hoc"):
        b.add(sig(raw))
    for raw in first_table("## Proportion and count extras"):
        if normalize(row_cells(raw)[0]) == "single_proportion":
            b.add(sig(raw))
    return b


def _all_data_rows(text):
    """Every pipe-delimited DATA row in the file, paired with its level-2 section
    title (headers and separators excluded)."""
    out = []
    in_table = False
    h2 = None
    for line in _lines(text):
        st = line.strip()
        if st.startswith("## ") and not st.startswith("###"):
            h2 = st[3:].strip()
            in_table = False
            continue
        if st.startswith("#"):
            in_table = False
            continue
        if st.startswith("|"):
            if _is_separator(st):
                in_table = True
                continue
            if not in_table:       # header
                continue
            out.append((h2, st))
        else:
            in_table = False
    return out


class DocCodeAgreementTest(unittest.TestCase):
    # ── Tier 1: strict cell-equality of the Decision table to recommend_test ──

    def test_decision_table_cell_equality_and_boschloo(self):
        rows = first_table("## Decision table")
        self.assertEqual(len(rows), 15, "expected 15 decision-table data rows")
        boschloo_seen = False
        for raw in rows:
            outcome, groups, paired, dist, test, _effect = row_cells(raw)
            dist_key = "censored" if dist in DASHES else dist
            if dist in DASHES:
                kwargs = {}
            else:
                self.assertIn(dist, DIST, f"unmapped Distribution cell {dist!r} in row: {raw}")
                kwargs = dict(DIST[dist])
            ng = GROUPS[groups]
            pr = PAIRED.get(paired, False) if paired not in DASHES else False
            rec = stats.recommend_test(outcome, ng, paired=pr, **kwargs)
            primary, alts = parse_test_cell(test)
            self.assertEqual(rec["test"], primary,
                             f"decision-table primary Test disagrees with engine for row: {raw}")
            engine_alts = {canon(a) for a in rec["alternatives"]}
            for a in alts:
                self.assertIn(a, engine_alts,
                              f"in-cell alternative {a!r} not in engine alternatives for row: {raw}")
            if outcome == "proportion" and ng == 2 and pr is False:
                self.assertTrue(any("boschloo" in canon(a) for a in rec["alternatives"]),
                                f"Boschloo fallback missing from proportion/2/no alternatives: {raw}")
                boschloo_seen = True
        self.assertTrue(boschloo_seen, "the proportion/2/no Boschloo cell was never reached")

    # ── Tier 2: honest set-membership of the six mirror tables ──

    def test_correlation_membership(self):
        rows = first_table("### Correlation")
        self.assertEqual(len(rows), 3)
        for raw in rows:
            cells = row_cells(raw)
            kind = canon(cells[0])
            engine = set(stats.recommend_association(kind)["tests"])
            got = corr_coeffs(cells[1])
            self.assertTrue(got, f"no coefficient parsed from correlation row: {raw}")
            self.assertTrue(got <= engine,
                            f"declared coefficients {got} not a subset of {engine} for {kind}: {raw}")

    def test_repeated_measures_membership(self):
        rows = first_table("## Repeated measures")
        self.assertEqual(len(rows), 3)
        for raw in rows:
            cells = row_cells(raw)
            keys = [normalize(k) for k in cells[0].split("/")]
            got = backtick_tokens(cells[1])
            self.assertTrue(got, f"no test parsed from RM row: {raw}")
            for k in keys:
                engine = set(stats.recommend_rm(k)["tests"])
                self.assertTrue(got <= engine,
                                f"RM tests {got} not a subset of {engine} for {k}: {raw}")

    def test_trend_membership(self):
        rows = first_table("## Trend")
        self.assertEqual(len(rows), 3)
        for raw in rows:
            cells = row_cells(raw)
            key = TREND_KEY[cells[0].lower()]
            got = backtick_tokens(cells[1])
            engine = set(stats.recommend_trend(key)["tests"])
            self.assertTrue(got, f"no test parsed from trend row: {raw}")
            self.assertTrue(got <= engine,
                            f"trend tests {got} not a subset of {engine} for {key}: {raw}")

    def test_resampling_membership(self):
        rows = first_table("## Resampling")
        self.assertEqual(len(rows), 2)
        for raw in rows:
            cells = row_cells(raw)
            keys = [normalize(k) for k in cells[0].split("/")]
            got = extract_methods(cells[1])
            self.assertTrue(got, f"no method parsed from resampling row: {raw}")
            for k in keys:
                engine = set(stats.recommend_resampling(k)["tests"])
                self.assertTrue(got <= engine,
                                f"resampling methods {got} not a subset of {engine} for {k}: {raw}")

    def test_posthoc_membership(self):
        rows = first_table("## Post-hoc")
        self.assertEqual(len(rows), 4)
        for raw in rows:
            cells = row_cells(raw)
            key = token_of(cells[0])
            got = extract_methods(cells[1])
            engine = set(stats.recommend_posthoc(key)["tests"])
            self.assertTrue(got, f"no post-hoc parsed from row: {raw}")
            self.assertTrue(got <= engine,
                            f"post-hoc {got} not a subset of {engine} for {key}: {raw}")

    def test_proportion_ci_membership(self):
        rows = first_table("## Proportion and count extras")
        bound = 0
        for raw in rows:
            cells = row_cells(raw)
            if normalize(cells[0]) == "single_proportion":
                got = extract_methods(cells[1])
                engine = set(stats.recommend_proportion_ci("single_proportion")["tests"])
                self.assertTrue(got, f"no interval parsed from single-proportion row: {raw}")
                self.assertTrue(got <= engine,
                                f"proportion-CI methods {got} not a subset of {engine}: {raw}")
                bound += 1
        self.assertEqual(bound, 1, "expected exactly one bound single-proportion row")

    # ── Anti-false-pass: every table row bound or explicitly skip-listed ──

    def test_skiplist_exhaustive(self):
        bound = _collect_bound_signatures()
        self.assertEqual(len(bound), 31,
                         f"expected 31 bound rows (15 decision + 16 mirror), got {len(bound)}")
        rows = _all_data_rows(TEXT)
        self.assertGreaterEqual(len(rows), 40, "too few table rows scanned — parser under-read the file")
        unaccounted = []
        for h2, raw in rows:
            s = sig(raw)
            if s in bound:
                continue
            if h2 in SKIP_SECTIONS:
                continue
            low = raw.lower()
            if any(marker in low for marker, _ in SKIP_ROW_MARKERS):
                continue
            unaccounted.append(raw)
        self.assertFalse(unaccounted,
                         "table rows neither bound nor skip-listed (silent-unparse guard):\n"
                         + "\n".join(unaccounted))


if __name__ == "__main__":
    unittest.main()
