"""Entrypoint fit-before-split scans. Codes DSX-CODE-*.

Stdlib-only. Source is parsed with `ast` (Python 3.9+ -- `ast.unparse` is
used to render argument tokens); `.py` is read as UTF-8 with an optional
BOM, `.ipynb` is read the same way (also `utf-8-sig`) and contributes
CODE cells verbatim, blanking markdown cells CHARACTER-WISE (every
newline survives, every other character does not) so that reported line
indices are unchanged by the cell filter -- a Jupyter magic or shell
escape (`%matplotlib inline`, `!pip install pandas`) is repaired
in-place, blank-per-blanked-line, only after a first parse attempt fails
and only for `.ipynb`, then re-parsed once. For a `.ipynb`, `Line N`
indexes the RECONSTRUCTED CELL CONCATENATION described above -- not the
Nth line of the `.ipynb` JSON file, which a user cannot usefully open at
that offset either way; this module does not change that coordinate
space, only preserves it exactly across the markdown filter. `lines`
is built from the CPython tokenizer's own line partition
(`_source_lines`), not `str.splitlines()` -- the latter also breaks on
form feed, several C1 control-code separators, and the Unicode
line/paragraph separator characters, which would desynchronise
AST-derived line numbers from text-derived ones. When the source cannot
be parsed, the legacy per-line text scan runs instead and every finding
says so on four channels (a pass line, per-finding `scan` data, a
detail-string sentence, and a decision-record input). `ast.parse`
accepts the RUNNING interpreter's grammar, so which path an entrypoint
takes can depend on the interpreter's Python version; both are disclosed
in the decision records. Missing / non-text / unscannable entrypoints
are named as NOT scanned rather than silently skipped (repro covers
missing paths). Nothing here makes any DSX-CODE-* sound, complete or
exhaustive -- real leaks remain uncaught by construction and by design.
"""

from __future__ import annotations

import ast
import json
import re
import sys
from dataclasses import dataclass, replace
from pathlib import Path

from ..decisions import DecisionRecord, record_decision
from ..findings import Report
from ..spec import is_blank, section

# Phase 11.1 (REQ-P11.1-03): how many lines a target reference is allowed to
# trail behind the statistical-test call it explains. Fixed, not derived, so
# the number is a stated decision (see `_stat_test_lines_referencing`'s
# docstring) rather than a magic constant scattered through the function body.
_TARGET_REFERENCE_LOOKBACK = 3

SPLIT_MARKERS = (
    "train_test_split",
    "TimeSeriesSplit",
    "GroupKFold",
    "StratifiedKFold",
    "StratifiedGroupKFold",
    "KFold(",
    "ShuffleSplit",
    "GroupShuffleSplit",
    "TimeSeriesSplit(",
)

FIT_LEAK_MARKERS = (
    r"\.fit\s*\(",
    r"\.fit_transform\s*\(",
    r"\.partial_fit\s*\(",
)

SCALER_FULL_RE = re.compile(
    r"(?i)StandardScaler\s*\(\s*\)\s*\.\s*fit_transform\s*\(\s*(X|df|features)\b"
)

RESAMPLE_BEFORE_RE = re.compile(
    r"(?i)\b(SMOTE|RandomOverSampler|RandomUnderSampler|ADASYN)\b"
)

# Phase 11.1.1 plan 01 (threat T-11.1-01, Decision 9). This pattern becomes
# DEAD on the AST primary path -- any `.fit(...)` call is already a Call
# node, of which `Pipeline(...).fit(X_train` is a strict subset -- but
# stays reachable on the fallback and is kept for it (that redundancy is
# stated here rather than left to be rediscovered).
#
# `.*` was replaced with a bounded `[^)\n]{0,200}` -- NOT the unbounded
# `[^)\n]*` the plan's own design section proposed. Measured this session:
# swapping only the character class (still unbounded) does NOT make the
# adversarial shape `"Pipeline(" * n + ").fit(X_trai"` linear -- it stays
# quadratic, 0.0018 / 0.0070 / 0.0278 / 0.1123 / 0.4360 s at n = 250 / 500
# / 1,000 / 2,000 / 4,000, because `re.search` still retries the O(n)
# scan-to-the-only-")" from each of the n literal "Pipeline(" starting
# positions when the overall match fails everywhere. Only bounding the
# repetition (so each retry costs O(1), not O(remaining-length)) makes it
# linear by construction: 0.0003 / 0.0006 / 0.0012 / 0.0026 / 0.0048 s at
# the same sizes, and 0.33 s even at n = 256,000. The bound trades one
# real miss for that guarantee -- a `Pipeline(...)` argument list longer
# than 200 characters, or one containing a nested `)` (e.g. a nested
# tuple), no longer matches; `examples/` has no `Pipeline(` occurrence at
# all, so no fixture is affected. Match set unchanged across 14 probe
# shapes except that one nested-paren case, which the mere `.*` ->
# `[^)\n]*` swap already excludes on its own (a `)` inside the argument
# list was never going to survive dropping `.`).
PIPELINE_FIT_TRAIN_RE = re.compile(
    r"(?i)Pipeline\s*\([^)\n]{0,200}\)\s*\.\s*fit\s*\(\s*X_train\b"
)

# Phase 11.1 (REQ-P11.1-01): full-frame cleaning idioms computed before any split
# exists — a fillna imputation whose text also names a mean/median/mode aggregate,
# or a row filter that both subscripts/filters a frame and names a std/quantile
# call.
#
# Phase 11.1.1 (threat T-11.1-01): each of these was previously ONE pattern that
# combined its two halves with sequential `.*`-prefixed lookaheads, under a
# comment claiming the construction was linear. That claim was false and is
# retracted here. `re.search()` retries a failing zero-width pattern at every
# start position, and the spread filter's `.*\w+` had overlapping character
# classes on top of that. Measured on a non-matching line, the spread filter grew
# with a fitted exponent of 3.0 (cubic — 800 characters took 1.4 seconds) and the
# imputation filter with an exponent of 2.0 (quadratic). Both run once per
# non-comment line of an analyst-supplied entrypoint with no length cap, so an
# ordinary long line could stall a blocking gate; and because the scan stops at
# the first match, that cost fell on CLEAN files, not leaky ones.
#
# Each half is now its own unambiguous pattern — no leading `.*`, no overlapping
# character classes — and the co-occurrence is decided in Python with `and`.
# That is linear and measurably so (2,000,000 characters in 0.05 seconds), and it
# matches exactly the same lines as the previous construction. The bar is pinned
# by test_full_frame_cleaning_predicates_timing_no_catastrophic_backtracking.
_IMPUTE_FILLNA_RE = re.compile(r"\.fillna\s*\(")
_IMPUTE_STAT_RE = re.compile(r"\.(?:mean|median|mode)\s*\(")
_SPREAD_SUBSCRIPT_RE = re.compile(r"\w\s*\[")
_SPREAD_STAT_RE = re.compile(r"\.(?:std|quantile)\s*\(")


def _is_full_frame_impute(line: str) -> bool:
    """True when `line` both calls `.fillna(` and names a mean/median/mode
    aggregate — the whole-frame imputation idiom (REQ-P11.1-01)."""
    return bool(_IMPUTE_FILLNA_RE.search(line) and _IMPUTE_STAT_RE.search(line))


def _is_full_frame_spread_filter(line: str) -> bool:
    """True when `line` both subscripts a frame and names a std/quantile call —
    the whole-frame outlier-filter idiom (REQ-P11.1-01)."""
    return bool(_SPREAD_SUBSCRIPT_RE.search(line) and _SPREAD_STAT_RE.search(line))

# Phase 11.1 (REQ-P11.1-01): the training-frame name lexicon, locked by this plan
# per 11.1-RESEARCH.md's "Training-Frame Name Lexicon" section (marked [ASSUMED]
# there — a naming-convention survey, not a corpus study; the roadmap deferred the
# binding call to a discuss pass that did not run). Case-sensitive: Python
# identifiers are case-sensitive, and a case-insensitive match risks false
# negatives on unrelated identifiers that happen to share letters. `X_train` must
# be present — `PIPELINE_FIT_TRAIN_RE` above already hardcodes that one literal,
# and the two must never disagree about the same line.
TRAINING_FRAME_NAMES = (
    "X_train", "y_train", "train_X", "train_y", "X_tr", "y_tr", "Xtrain", "ytrain",
    "train_df", "df_train", "train_data", "train_set", "train_features", "features_train",
)

# Phase 11.1 (REQ-P11.1-01): first-argument-token extraction for a `.fit(`/
# `.fit_transform(` call. One bounded character-class repetition only (identifier
# characters plus dot, square brackets and both quote characters) — no nested
# quantifier, no alternation containing a quantifier (threat T-11.1-01). The
# trailing `\s*[),]` requires a closing paren or comma to actually follow the
# captured token, so a malformed call with no closing parenthesis fails to match
# at all rather than capturing a truncated token (T-11.1-02), and a bare numeric
# first argument fails to match at all because the token must open on
# `[A-Za-z_]`.
#
# Phase 11.1.1 plan 02 (§2.2/§3.4 of 11.1.1-AST-DESIGN.md, Edit F). Widened so
# the FALLBACK agrees with the AST path instead of contradicting it:
# `partial_fit` joins the alternation (longest-first, so it is tried before the
# `fit` prefix it would otherwise partially match) to match FIT_METHOD_NAMES,
# and an OPTIONAL keyword prefix is added, gated on the SAME
# FIT_FIRST_PARAM_NAMES allowlist `_first_argument` uses. An any-identifier
# prefix would make `model.fit(y=y_test)` a CRITICAL finding on the fallback
# while the AST path stays silent -- two mechanisms disagreeing about one
# source line, in the false-positive direction, on a path one stray character
# reaches (T-11.1.1-07). The capture group and the trailing `\s*[),]` stay
# byte-identical to the pre-widened pattern: the capture is still the VALUE,
# never the keyword name, and the trailing requirement still makes a call with
# no closing parenthesis fail to match rather than capture a truncated token.
# Re-measured, not inherited (11.1.1-RESEARCH.md Pitfall 6): 0.0000 s on
# 19,995 non-matching characters, 0.0003 s on a 1,000,000-character `x=`
# near-miss -- see test_fit_call_re_timing_no_catastrophic_backtracking_with_
# keyword_form.
FIT_CALL_RE = re.compile(
    r"\.(?:fit_transform|partial_fit|fit)\s*\(\s*"
    r"(?:(?:X|x|data|df|frame|features)\s*=\s*)?"
    r"([A-Za-z_][\w.\[\]'\"]*)\s*[),]"
)

# Phase 11.1 (REQ-P11.1-03): the statistical-test call idiom the reproduction's
# hypothesis stage uses in place of any `.fit(`-shaped call — a co-occurrence
# match, not a fit-scan, is what catches it. One bounded alternation of
# literal function names followed by one bounded whitespace repetition and an
# opening parenthesis: no nested quantifier, no leading `.*`, and linear in line
# length — measured at a fitted growth exponent of 0.7 (threat T-11.1-12). This
# pattern previously cited `FULL_FRAME_IMPUTE_RE`'s comment as its precedent;
# that comment's linearity claim was false and was retracted in Phase 11.1.1, so
# this one now states its own measured property instead of borrowing one.
# A leading `\b` keeps a longer identifier that merely contains one of these
# names (e.g. `my_ttest_ind_variant(`) from matching.
STAT_TEST_CALL_RE = re.compile(
    r"\b(?:chi2_contingency|ttest_ind|ttest_rel|pearsonr|mannwhitneyu|f_oneway|kruskal)"
    r"\s*\("
)

# Phase 11.1.1 plan 03 (this comment is the key_link's other end --
# README.md's "### What the entrypoint scan does not catch" must name the
# SAME forms; if the two drift, one of them is lying to a reader who has
# no way to tell which). Nothing below makes DSX-CODE-001, DSX-CODE-021
# or any other DSX-CODE-* sound, complete or exhaustive. FIT_METHOD_NAMES
# and FIT_FIRST_PARAM_NAMES together decide what counts as a fit call and
# what counts as its argument -- and therefore decide the shape of every
# real leak this module cannot see:
#   - a call the scan cannot resolve to a name: dynamic dispatch
#     (getattr(model, "fit")(data), or handlers["fit"](data)); a bound
#     method held in a variable (f = model.fit, then f(data)); a fit
#     performed inside an imported helper; a split reached only through
#     an alias or a helper function rather than a call to a name in
#     SPLIT_CALL_NAMES;
#   - an argument shape the scan does not read: a keyword outside
#     FIT_FIRST_PARAM_NAMES, such as model.fit(training_frame=data); a
#     starred first argument (model.fit(*args)); a full frame laundered
#     through a training_frame-shaped variable name that _is_training_
#     frame matches by prefix without following the assignment;
#   - a file the scan never opens: source assembled in a string and run
#     with exec or eval (a REGRESSION from the old text scan, not a
#     standing limit -- see README.md);
#   - on the FALLBACK path only (an entrypoint that failed to parse): a
#     backslash-continued fit call, which the joining helper was
#     deliberately never written to handle; and a trailing comment fit
#     call (z = 1  # scaler.fit(data)), which every text guard in this
#     module tests only for a LEADING "#" and therefore still matches.
#
# Phase 11.1.1 plan 01 (§3.3 of 11.1.1-AST-DESIGN.md). Identical to
# FIT_LEAK_MARKERS' method set, so the AST path and the fallback agree.
# `partial_fit` is included for parity with FIT_LEAK_MARKERS (which
# already has it) even though FIT_CALL_RE lacks it -- widening the AST
# method set to match rather than deliberately narrowing it to preserve
# that pre-existing asymmetry. `grep -rn "partial_fit" examples/ tests/`
# returns nothing before this plan, so no fixture can move.
FIT_METHOD_NAMES = frozenset({"fit", "fit_transform", "partial_fit"})

# Phase 11.1.1 plan 02 (§3.4 of 11.1.1-AST-DESIGN.md, T-11.1.1-07). The
# keyword-argument ALLOWLIST both `_first_argument` (AST path) and the
# widened `FIT_CALL_RE` (fallback) resolve a fit call's first argument
# through -- a decision, not an omission. A BLOCKLIST ("any keyword
# except y, sample_weight, groups") would report an unrelated keyword's
# value as "the frame this was fitted on", which is precisely the
# false-positive flood T-11.1.1-07 names: a false-positive flood is as
# damaging to a blocking gate as a blind spot, and faster to erode
# trust. The cost this allowlist accepts: `model.fit(training_frame=data)`
# draws nothing (named in the phase's uncaught-by-design record) --
# pinnable, and preferred over the flood.
FIT_FIRST_PARAM_NAMES = ("X", "x", "data", "df", "frame", "features")

# Phase 11.1.1 plan 01 (§3.6). The call-name equivalent of SPLIT_MARKERS,
# deduplicated (SPLIT_MARKERS lists TimeSeriesSplit twice, once bare and
# once with a trailing "(" -- a name set does not need that). SPLIT_MARKERS
# itself is left untouched; it is still the fallback's detector and the
# text half of first_split's union (Decision 5).
SPLIT_CALL_NAMES = frozenset({
    "train_test_split", "TimeSeriesSplit", "GroupKFold", "StratifiedKFold",
    "StratifiedGroupKFold", "KFold", "ShuffleSplit", "GroupShuffleSplit",
})


@dataclass(frozen=True)
class _CallSite:
    """One `ast.Call` site, in ZERO-BASED physical line coordinates.

    Phase 11.1.1 plan 01 (Decision 6). `(line, col_offset)` is NOT a total
    order over the call sites in one file -- nested and chained calls
    collide on both: `ast.parse("m.fit(x).fit(y)")` gives two calls at
    `(0, 0)`, and `examples/analysis/leaky_model.py` has `fit_transform`
    and `StandardScaler` both at line 6 column 4. Determinism would then
    rest on `sorted` being stable and `ast.walk` being breadth-first -- an
    accident no test could catch. Ascending `end_col_offset` breaks the
    tie towards the innermost/leftmost-ending call, which is what today's
    left-to-right `finditer` scan already reports. Measured this session:
    `m.fit(full_frame_a).fit(full_frame_b)` reports `full_frame_a` first,
    both before and after this change.
    """

    line: int
    col: int
    end_col: int
    name: str
    node: "ast.Call"


def _resolve_callee_name(node: "ast.Call") -> str:
    """Only the FINAL segment of the callee is used for matching (Phase
    11.1.1 plan 01, §3.2) -- `sklearn.model_selection.train_test_split(...)`
    and a bare `train_test_split(...)` must be treated identically. A
    chained receiver is resolved for free: `StandardScaler().fit_transform(X)`
    is an outer Call whose `func` is an Attribute whose `.value` is the
    inner Call -- the outer call's name is `fit_transform`, and the inner
    `StandardScaler()` is its own separate `_CallSite` named
    `StandardScaler`, matching nothing. A callee this cannot resolve
    (`getattr(m, "fit")(df)`, `handlers["fit"](df)`) returns `""`, which
    matches nothing in `FIT_METHOD_NAMES` or `SPLIT_CALL_NAMES` by
    construction -- named in the phase's uncaught-by-design record."""
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return ""


def _call_sites(tree: "ast.AST") -> "tuple[_CallSite, ...]":
    """Walk `tree` ONCE, collect every `ast.Call`, resolve its callee name,
    and return the tuple sorted by `(line, col, end_col)` (Decision 6).

    Phase 11.1.1 plan 01 (§3.1). Every consumer below reads this ONE
    tuple; nothing re-walks. That is a correctness requirement -- walk
    order would otherwise decide which token is reported, since
    `ast.walk` is breadth-first and NOT source-ordered -- as much as a
    performance one (one walk per `check()` call, not one per code)."""
    sites: "list[_CallSite]" = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            end_col = node.end_col_offset
            sites.append(
                _CallSite(
                    line=node.lineno - 1,
                    col=node.col_offset,
                    end_col=end_col if end_col is not None else node.col_offset,
                    name=_resolve_callee_name(node),
                    node=node,
                )
            )
    return tuple(sorted(sites, key=lambda s: (s.line, s.col, s.end_col)))


def _prose_line_indices(tree: "ast.AST") -> "frozenset[int]":
    """ZERO-BASED physical line indices that are pure prose -- a docstring,
    a bare string statement, or the strictly interior lines of a
    multi-line string constant -- and therefore skip-worthy for a
    primary-path TEXT scan that must not let prose decide a verdict.

    Phase 11.1.1 plan 01 (Decision 4). Rule A masks every line of an
    `ast.Expr` whose `.value` is a string `ast.Constant` -- every
    docstring (module, class, function) and every bare string statement.
    Rule B masks only the STRICTLY INTERIOR lines of a multi-line string
    constant -- NOT the opening line and NOT the closing line. The
    opening line is spared because it can carry real code (an assignment
    of a triple-quoted string on its opening line); the closing line
    carries real code exactly as often (a second statement chained after
    the closing triple-quote), and masking it would delete true-positive
    CRITICAL findings on that exact statement shape -- review reproduced
    two. Masking WHOLE LINES ONLY, never "any line a string touches", is
    also load-bearing:
    `df['Age'] = df['Age'].fillna(df['Age'].mean())` sits on three
    single-line string constants and must not be masked.

    In this wave the mask has exactly one consumer: the split-marker text
    scan, via `_first_line_matching`'s `masked` parameter (Decision 5).
    """
    masked: "set[int]" = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            # Rule A: the whole bare-string statement (docstring or
            # otherwise) is prose, opening and closing line included.
            for lineno in range(node.lineno, node.end_lineno + 1):
                masked.add(lineno - 1)
        if (
            isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and node.end_lineno is not None
            and node.end_lineno > node.lineno
        ):
            # Rule B: only the interior lines of a multi-line string
            # constant, wherever it appears (not only in a bare
            # statement) -- the opening and closing lines are spared.
            for lineno in range(node.lineno + 1, node.end_lineno):
                masked.add(lineno - 1)
    return frozenset(masked)


def _first_argument(node: "ast.Call") -> "ast.AST | None":
    """Resolve `node`'s first argument, positional-then-allowlisted-keyword
    (Phase 11.1.1 plan 02, §3.4). Returns `None` -- no token, no finding --
    when nothing qualifies.

    1. A non-empty, non-starred `node.args[0]` wins (`model.fit(data)`).
       `ast.Starred` (`model.fit(*args)`) is skipped, not resolved --
       named in the phase's uncaught-by-design record.
    2. Otherwise the value of the first KEYWORD, in source order, whose
       `arg` is in `FIT_FIRST_PARAM_NAMES` (`model.fit(X=data, y=target)`
       -> `data`; `**kwargs` has `arg is None` and is skipped).
    3. Otherwise `None`.
    4. **If the resolved node is an `ast.Constant`, return `None`.** No
       token, no finding. This preserves today's documented exclusion of
       `model.fit(42)` and extends it to strings and `None`/`True`/`False`
       -- all four are `ast.Constant`, so one rule covers the class.
       Without this rule the primary path would newly emit a CRITICAL
       finding reading "fits on '42'", naming a token that is not a frame
       at all.
    """
    resolved: "ast.AST | None" = None
    if node.args and not isinstance(node.args[0], ast.Starred):
        resolved = node.args[0]
    else:
        for kw in node.keywords:
            if kw.arg is not None and kw.arg in FIT_FIRST_PARAM_NAMES:
                resolved = kw.value
                break
    if isinstance(resolved, ast.Constant):
        return None
    return resolved


def _render_token(node: "ast.AST") -> str:
    """`ast.unparse`, ONE rendering path (Phase 11.1.1 plan 02, §3.5) --
    not `ast.get_source_segment`, which needs the original source threaded
    through every helper, returns `None` when position info is
    incomplete, and reproduces a multi-line argument as multi-line text
    that would then be pasted into a single-line `detail` string.
    `_is_training_frame` PREFIX-matches the rendered token against
    `TRAINING_FRAME_NAMES`; the leading identifier is never quoted, so
    unparse's normalisations cannot change a membership verdict. The one
    user-visible normalisation: a source token written `data[["Age"]]` is
    reported as `data[['Age']]` -- the verdict is unaffected, only the
    quoted `detail` text differs from the source (announced in plan 03's
    behaviour-change list)."""
    return ast.unparse(node)


def check(spec: dict, phase_dir: "str | None" = None) -> Report:
    """Entrypoint fit-before-split, full-frame-cleaning and fit-after-split scans
    (DSX-CODE-*).

    Phase 11.1 (REQ-P11.1-01) adds DSX-CODE-020 (a full-frame cleaning idiom —
    fillna+mean/median/mode, or a std/quantile-based row filter — occurring
    before the first split marker, or occurring at all when no split marker
    exists) and DSX-CODE-021 (a `.fit`/`.fit_transform` call at or after the
    first split marker whose first-argument token does not start with a member
    of `TRAINING_FRAME_NAMES`). Both are line-index ordering/membership checks
    over entrypoint source text, never a numeric computation — consistent with
    the project-wide D-01/D-02 boundary that a gate never computes statistics.

    Citation: Kaufman, S., Rosset, S., Perlich, C. and Stitelman, O. (2012),
    "Leakage in Data Mining: Formulation, Detection, and Avoidance," ACM
    Transactions on Knowledge Discovery from Data, 6(4), Article 15, DOI
    10.1145/2382577.2382579. The exact section stating the preprocessing-
    boundary formulation is UNVERIFIED — the full paper text was not
    independently re-read in this session (author/title/venue/year confirmed
    via 11.1-RESEARCH.md's citation-admissibility table, itself verified
    against ACM DL/Google Scholar/Semantic Scholar); do not invent a locator.

    Structural criterion: DSX-CODE-020 is an ordering comparison between two
    line indices in one file — the first full-frame-cleaning-idiom line index
    against the first split-marker line index (or the idiom's presence alone,
    when no split marker exists) — not a numeric threshold test.
    Structural criterion: DSX-CODE-021 is a membership test of the
    first-argument expression, rendered from the call node, against
    TRAINING_FRAME_NAMES (matched as a prefix, not equality), combined with a
    >= comparison between the fit call's physical line index and the first
    split call's physical line index.

    Phase 11.1 (REQ-P11.1-03) adds DSX-CODE-030 (a statistical-test call whose
    argument text references the declared `model.target` column, occurring
    before the first split marker, or occurring at all when no split marker
    exists) and DSX-CODE-031 (the same call at or after the first split
    marker). This closes the check's other blind spot: the reproduction's
    hypothesis stage contains no fit call at all — it cross-tabulates a
    candidate feature against the target and runs a chi-square test, then
    appends accepted hypotheses to the dataset for the downstream stages
    (`references/The AI Data Scientist.md`, Table 1 / section 2.2).

    Citation: Kaufman, S., Rosset, S., Perlich, C. and Stitelman, O. (2012),
    "Leakage in Data Mining: Formulation, Detection, and Avoidance," ACM
    Transactions on Knowledge Discovery from Data, 6(4), Article 15, DOI
    10.1145/2382577.2382579. The section stating that leakage can be
    introduced through the evaluation path rather than the training path is
    UNVERIFIED — the full paper text was not independently re-read in this
    session; do not invent a locator.

    Structural criterion: DSX-CODE-030 and DSX-CODE-031 are a co-occurrence of
    a statistical-test-function name match (STAT_TEST_CALL_RE) and a target-
    column reference within a bounded line window (see
    `_stat_test_lines_referencing`), compared against the first split-marker
    line index with the same strictly-less-than / >= split DSX-CODE-020 and
    DSX-CODE-021 already use.
    """
    report = Report(check="code")
    repro = section(spec, "reproducibility")
    entry = repro.get("entrypoint")
    if is_blank(entry):
        # Phase 11.1.1 plan 01 (Decision 3b): a skipped scan must never be
        # mistaken for a clean one. Every remaining early return below
        # names itself the same way, before returning.
        report.ok("entrypoint NOT scanned — no entrypoint declared (no leak scan ran)")
        return report

    path = _resolve_entrypoint(str(entry), phase_dir)
    if path is None:
        report.ok(
            f"entrypoint NOT scanned — entrypoint path not found: {entry!r} "
            "(no leak scan ran)"
        )
        return report

    source = _read_source(path)
    if source is None:
        # _read_source returns None for an unresolvable OSError, an
        # unsupported suffix, or an unparseable notebook JSON document — it
        # does not distinguish which, so this reason names the whole class.
        report.ok(
            "entrypoint NOT scanned — could not be read (unreadable, "
            "unsupported suffix, or invalid notebook JSON) (no leak scan ran)"
        )
        return report

    suffix = path.suffix.lower()
    lines = _source_lines(source)
    tree, parse_reason = _parse_source(source, suffix)
    degraded = tree is None
    if degraded:
        report.ok(f"entrypoint NOT parsed — text-only fallback scan ({parse_reason})")
    else:
        report.ok("entrypoint parsed with ast (call-level scan)")

    scan_path_input = (
        f"scan_path:text-fallback:{parse_reason}" if degraded else "scan_path:ast"
    )
    python_input = f"python:{sys.version_info.major}.{sys.version_info.minor}"

    # Phase 11.1.1 plan 01 (§3, Decisions 4-6): one walk, one call-site
    # tuple, one prose mask -- computed once per check() call and read by
    # every consumer below, never re-walked. Empty on the fallback path
    # (tree is None), which is exactly what makes the fallback's
    # first_split union degrade to text-only and its DSX-CODE-001
    # detection degrade to `_first_fit_leak_line`.
    call_sites = _call_sites(tree) if tree is not None else ()
    prose_mask = _prose_line_indices(tree) if tree is not None else frozenset()

    # Phase 11.1.1 plan 01 (Decision 5): first_split is the UNION of the
    # AST split-call index and the masked text-marker scan, not a
    # replacement of one by the other. An AST-only split detector reads an
    # aliased or helper-wrapped split as no split at all, which silences
    # DSX-CODE-021 entirely and makes DSX-CODE-010 assert something the
    # file contradicts. A split marker that appears only inside a
    # docstring stops counting (the mask removes that line) -- stricter,
    # and announced.
    text_split = _first_line_matching(lines, SPLIT_MARKERS, masked=prose_mask)
    ast_split_lines = [s.line for s in call_sites if s.name in SPLIT_CALL_NAMES]
    ast_split = min(ast_split_lines) if ast_split_lines else None
    split_candidates = [v for v in (text_split, ast_split) if v is not None]
    first_split = min(split_candidates) if split_candidates else None

    # Phase 11.1.1 plan 01 (§3.3-3.4, CR-01/CR-02): DSX-CODE-001 is driven
    # from call sites on the parsed path -- closing whitespace, tab,
    # backslash-continuation and multi-line forms, and structurally
    # retiring the docstring/prose false positive, since a string constant
    # holds no Call node. The fallback keeps the shipped text
    # implementation, with CR-03's redundant literal re-check removed
    # (see `_first_fit_leak_line`).
    if tree is not None:
        ast_fit_lines = [s.line for s in call_sites if s.name in FIT_METHOD_NAMES]
        first_fit = min(ast_fit_lines) if ast_fit_lines else None
    else:
        first_fit = _first_fit_leak_line(lines)

    model_section = section(spec, "model")
    has_model = bool(model_section)

    if first_fit is not None and (first_split is None or first_fit < first_split):
        # Allow Pipeline(...).fit(X_train after a split — only when split precedes.
        report.add(
            "DSX-CODE-001",
            "CRITICAL",
            "Fit/transform appears before the first train/test split marker",
            detail=(
                f"Line {first_fit + 1} fits or fit_transforms before any split marker "
                f"({'none' if first_split is None else f'line {first_split + 1}'}). "
                "Fitting on the full frame leaks test statistics into training."
            ),
            remedy=(
                "Split first, then fit only on the training fold "
                "(or use a Pipeline fitted on X_train after the split)."
            ),
            where=f"entrypoint:{entry}",
            fit_line=first_fit + 1,
        )

    cleaning_index = _first_full_frame_cleaning_line(lines)
    cleaning_blocked = cleaning_index is not None and (
        first_split is None or cleaning_index < first_split
    )
    if cleaning_blocked:
        report.add(
            "DSX-CODE-020",
            "CRITICAL",
            "Full-frame cleaning statistic computed before the split",
            detail=(
                f"Line {cleaning_index + 1}: {lines[cleaning_index].strip()[:120]} "
                f"(split: {'none' if first_split is None else f'line {first_split + 1}'})."
            ),
            remedy=(
                "Split first, then compute the imputation value or the outlier "
                "threshold on the training rows only and apply it to both sides."
            ),
            where=f"entrypoint:{entry}",
        )

    # Phase 11.1.1 plan 02 (§3.4-3.5 of 11.1.1-AST-DESIGN.md, Edit D):
    # DSX-CODE-021 is resolved from call sites on the parsed path -- the
    # SAME `call_sites` tuple plan 01 built for DSX-CODE-001 above, never
    # re-walked. Filters to FIT_METHOD_NAMES, resolves the first argument
    # (§3.4), renders it (§3.5), and applies exactly the pre-existing
    # predicate: first site with `site.line >= first_split` and
    # `not _is_training_frame(token)`, then break. The fallback keeps the
    # widened FIT_CALL_RE / _fit_call_arguments (Edit F below), which now
    # AGREES with the AST path's keyword allowlist instead of
    # contradicting it.
    fit_after_split_index: "int | None" = None
    fit_after_split_token: "str | None" = None
    if first_split is not None:
        if tree is not None:
            for site in call_sites:
                if site.name not in FIT_METHOD_NAMES or site.line < first_split:
                    continue
                argument = _first_argument(site.node)
                if argument is None:
                    continue
                token = _render_token(argument)
                if not _is_training_frame(token):
                    fit_after_split_index = site.line
                    fit_after_split_token = token
                    break
        else:
            for index, token in _fit_call_arguments(lines):
                if index >= first_split and not _is_training_frame(token):
                    fit_after_split_index = index
                    fit_after_split_token = token
                    break
    fit_after_split_blocked = fit_after_split_index is not None
    if fit_after_split_blocked:
        report.add(
            "DSX-CODE-021",
            "CRITICAL",
            "Fit call after the split is not fitted on a recognised training frame",
            detail=(
                f"Line {fit_after_split_index + 1} fits on "
                f"{fit_after_split_token!r}, which is not a recognised training "
                f"frame (split at line {first_split + 1})."
            ),
            remedy=(
                "Fit on the training frame the split produced, and transform the "
                "held-out frame with the already-fitted object."
            ),
            where=f"entrypoint:{entry}",
        )

    # Phase 11.1 (D-04): a decision record at the point where both index
    # comparisons above have been made — fired or cleared, a judgment was made
    # either way, so this always appends exactly one record per check() call
    # that reaches this point (i.e. whenever the entrypoint resolved and its
    # source was readable).
    record_decision(
        report,
        DecisionRecord(
            id="",
            invocation_id="",
            layer="deterministic",
            choice=(
                "full-frame cleaning before split: "
                + ("blocked" if cleaning_blocked else "passed")
                + "; fit call after split not on training frame: "
                + ("blocked" if fit_after_split_blocked else "passed")
            ),
            inputs=[
                f"entrypoint:{entry}",
                f"cleaning_line:{'none' if cleaning_index is None else cleaning_index + 1}",
                f"split_line:{'none' if first_split is None else first_split + 1}",
                f"fit_line:{'none' if fit_after_split_index is None else fit_after_split_index + 1}",
                scan_path_input,
                python_input,
            ],
            rule=(
                "DSX-CODE-020 fires when the cleaning-idiom line index is "
                "strictly less than the first split-marker line index, or when "
                "no split marker exists at all. DSX-CODE-021 fires when a "
                "fit/fit_transform call's line index is greater than or equal "
                "to the first split-marker line index and its first-argument "
                "token does not start with a member of TRAINING_FRAME_NAMES."
            ),
            citation=(
                "Kaufman, S., Rosset, S., Perlich, C. and Stitelman, O. (2012), "
                "\"Leakage in Data Mining: Formulation, Detection, and "
                "Avoidance,\" ACM Transactions on Knowledge Discovery from "
                "Data, 6(4), Article 15."
            ),
            counterfactual=(
                "A split marker present above the cleaning line (or no "
                "full-frame cleaning idiom at all) would have cleared "
                "DSX-CODE-020; a fit call whose first-argument token begins "
                "with a TRAINING_FRAME_NAMES member would have cleared "
                "DSX-CODE-021."
            ),
        ),
    )

    # Phase 11.1 (REQ-P11.1-03): statistical-test-sees-target scan. The target
    # is read from the model section already resolved above, through the same
    # `section()`/`is_blank()` accessors `_check_features` uses for the same
    # field in dsx/checks/ml.py — this keeps whitespace/blank handling
    # identical across both check families without adding a parameter to
    # check()'s signature (dsx/cli.py::run_checks calls it with exactly two
    # arguments; has_model above is already derived internally the same way).
    raw_target = model_section.get("target")
    target_text = raw_target if isinstance(raw_target, str) else ""
    stat_test_lines = (
        [] if is_blank(target_text) else _stat_test_lines_referencing(lines, target_text)
    )

    stat_before_index: "int | None" = None
    stat_after_index: "int | None" = None
    for index in stat_test_lines:
        if first_split is None or index < first_split:
            if stat_before_index is None:
                stat_before_index = index
        elif stat_after_index is None:
            stat_after_index = index

    stat_before_blocked = stat_before_index is not None
    if stat_before_blocked:
        report.add(
            "DSX-CODE-030",
            "CRITICAL",
            "Statistical test references the declared target before the split",
            detail=(
                f"Line {stat_before_index + 1}: "
                f"{lines[stat_before_index].strip()[:120]} (target: "
                f"{target_text!r}, split: "
                f"{'none' if first_split is None else f'line {first_split + 1}'})."
            ),
            remedy=(
                "Compute the test on the training rows only, or state the test "
                "as exploratory and exclude any feature it selected."
            ),
            where=f"entrypoint:{entry}",
        )

    stat_after_blocked = stat_after_index is not None
    if stat_after_blocked:
        report.add(
            "DSX-CODE-031",
            "HIGH",
            "Statistical test references the declared target at or after the split",
            detail=(
                f"Line {stat_after_index + 1}: "
                f"{lines[stat_after_index].strip()[:120]} (target: "
                f"{target_text!r}, split: line {first_split + 1})."
            ),
            remedy="Name the frame the test was computed on.",
            where=f"entrypoint:{entry}",
        )

    # Phase 11.1 (D-04): a second decision record covering both DSX-CODE-030
    # and DSX-CODE-031, appended at the point where the index split has been
    # made — the same shape plan 11.1-01 established above for DSX-CODE-020/
    # DSX-CODE-021, kept as its own record rather than folded into the first
    # because it judges a different scan (target reference, not cleaning/fit).
    record_decision(
        report,
        DecisionRecord(
            id="",
            invocation_id="",
            layer="deterministic",
            choice=(
                "statistical test on target before split: "
                + ("blocked" if stat_before_blocked else "passed")
                + "; statistical test on target at or after split: "
                + ("blocked" if stat_after_blocked else "passed")
            ),
            inputs=[
                f"entrypoint:{entry}",
                f"target:{'none' if is_blank(target_text) else target_text}",
                f"split_line:{'none' if first_split is None else first_split + 1}",
                f"stat_before_line:{'none' if stat_before_index is None else stat_before_index + 1}",
                f"stat_after_line:{'none' if stat_after_index is None else stat_after_index + 1}",
                scan_path_input,
                python_input,
            ],
            rule=(
                "DSX-CODE-030 fires when a statistical-test call referencing "
                "model.target has a line index strictly less than the first "
                "split-marker line index, or when no split marker exists at "
                "all. DSX-CODE-031 fires when such a call's line index is "
                "greater than or equal to the first split-marker line index. "
                "A blank or absent target skips the scan entirely."
            ),
            citation=(
                "Kaufman, S., Rosset, S., Perlich, C. and Stitelman, O. (2012), "
                "\"Leakage in Data Mining: Formulation, Detection, and "
                "Avoidance,\" ACM Transactions on Knowledge Discovery from "
                "Data, 6(4), Article 15."
            ),
            counterfactual=(
                "A split marker present above the statistical-test call would "
                "have moved the finding from DSX-CODE-030 to DSX-CODE-031; a "
                "blank model.target would have cleared both."
            ),
        ),
    )

    # Phase 11.1.1 plan 01 (threat T-11.1.1-13, Decision 8): the `break`
    # used to sit inside the inner `if`, so a SUPPRESSED match (prior
    # already names X_train) did not stop the outer loop -- it kept
    # rebuilding `prior = "\n".join(lines[:index])`, an O(index)
    # operation, for every one of the remaining matching lines, making the
    # whole loop O(n^2) on the PRIMARY path. Measured this session with an
    # `X_train = 1` line above N matching `StandardScaler().fit_transform`
    # lines: 0.0223 / 0.0852 / 0.4545 / 1.4211 s at 2,000 / 4,000 / 8,000 /
    # 16,000 -- roughly 4x per doubling, 1.4 s at 16,000, already over the
    # house budget. Hoisting the `break` out of the inner `if` is provably
    # behaviour-preserving: `lines[:j]` is a prefix superset of `lines[:i]`
    # for `j > i`, so once "X_train" is in `prior` it is in every later
    # `prior` too, and the loop is dead after the first suppressed match
    # exactly as much as after the first accepted one. Pinned by
    # test_scaler_full_loop_timing_is_linear, whose input is this exact
    # shape.
    for index, line in enumerate(lines):
        if SCALER_FULL_RE.search(line):
            prior = "\n".join(lines[:index])
            if "X_train" not in prior and "x_train" not in prior.lower():
                report.add(
                    "DSX-CODE-002",
                    "HIGH",
                    "StandardScaler().fit_transform on full frame with no prior X_train",
                    detail=f"Line {index + 1}: {line.strip()[:120]}",
                    remedy="Fit the scaler on X_train only, then transform X_train and X_test.",
                    where=f"entrypoint:{entry}",
                )
            break

    for index, line in enumerate(lines):
        if RESAMPLE_BEFORE_RE.search(line):
            if first_split is None or index < first_split:
                report.add(
                    "DSX-CODE-003",
                    "HIGH",
                    "Resampler (SMOTE / RandomOverSampler / …) before split",
                    detail=f"Line {index + 1}: {line.strip()[:120]}",
                    remedy="Split first; resample only the training fold.",
                    where=f"entrypoint:{entry}",
                )
                break

    if has_model and path.suffix.lower() in {".py", ".ipynb"} and first_split is None:
        report.add(
            "DSX-CODE-010",
            "MEDIUM",
            "model: block present but entrypoint has no declared split marker",
            detail=(
                "Expected train_test_split / TimeSeriesSplit / GroupKFold (or similar) "
                "in the entrypoint when a model is declared."
            ),
            remedy="Split in code and name the method, or document an external split.",
            where=f"entrypoint:{entry}",
        )
    elif first_split is not None:
        report.ok(f"entrypoint split marker at line {first_split + 1}")

    # Phase 11.1.1 plan 01 (Decision 7, §2.3 channels 2 and 3): a single
    # post-pass, applied immediately before return, tags every finding with
    # which scan produced the report and, on the fallback, appends the
    # degraded-scan sentence to its detail. Finding is frozen
    # (dsx/findings.py), so dataclasses.replace is required; a list-slice
    # assignment preserves order, which the determinism guarantee depends
    # on. Doing this as a post-pass keeps all eight report.add(...) call
    # sites' first three arguments untouched, which is what
    # scripts/gen-finding-catalogue.py --check requires.
    if degraded:
        degraded_note = (
            " [scanned as text only: this entrypoint could not be parsed as "
            f"Python ({parse_reason}), so the weaker text scan ran and may "
            "have missed leaks it cannot see]."
        )
        report.findings[:] = [
            replace(
                f,
                detail=(f.detail + degraded_note).strip(),
                data={**f.data, "scan": "text-fallback"},
            )
            for f in report.findings
        ]
    else:
        report.findings[:] = [
            replace(f, data={**f.data, "scan": "ast"}) for f in report.findings
        ]

    return report


def _resolve_entrypoint(entry: str, phase_dir: "str | None") -> Path | None:
    candidates: list[Path] = []
    if phase_dir:
        candidates.append(Path(phase_dir) / entry)
    candidates.append(Path(entry))
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def _source_lines(source: str) -> list[str]:
    """The CPython tokenizer's own line partition -- NOT `str.splitlines()`.

    Phase 11.1.1 plan 01 (Decision 1). `ast` node positions index the
    tokenizer's line partition, which splits only on `\\r\\n`, a lone `\\r`
    or `\\n`. `str.splitlines()` additionally splits on `\\x0b \\x0c \\x1c
    \\x1d \\x1e \\x85` and the Unicode line/paragraph separators, and the
    tokenizer does not -- so one such character anywhere in the
    entrypoint, including inside a string literal, would desynchronise
    every AST-derived line index from every text-derived one.
    `cleaning_index < first_split` would then be comparing two different
    axes. Measured this session, reproduced in
    `tests/test_dsx.py::TestPhase11_1Code`: a lone form-feed line above a
    split marker makes `splitlines()` report one line too many, shifting
    every reported "Line N" below it by one; the same happens for a
    U+2028 character embedded inside an otherwise ordinary single-line
    string literal.

    Normalising `\\r\\n` and a lone `\\r` to `\\n`, then splitting on `\\n`
    only, and dropping a single trailing empty element (matching
    `str.splitlines()`'s own treatment of a final trailing newline),
    reproduces the tokenizer's partition exactly -- so AST-derived and
    text-derived indices coincide by construction rather than by luck.
    This is also where the repo-wide CRLF rule is discharged for this
    module: no pattern below needs `\\r?\\n` of its own, because every
    pattern is matched against these already-normalised lines, never
    against the raw source.
    """
    normalised = source.replace("\r\n", "\n").replace("\r", "\n")
    parts = normalised.split("\n")
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return parts


# Phase 11.1.1 plan 01 (§1.3 of 11.1.1-AST-DESIGN.md). Jupyter cell sources
# routinely contain line magics (`%matplotlib inline`), cell magics
# (`%%time`), and shell escapes (`!pip install pandas`) -- all three raise
# SyntaxError from ast.parse. The repair blanks each such line to an empty
# string, IN PLACE, so the blanked line count and every other line's index
# are unchanged, then the caller re-parses once. Not repaired, and named in
# the phase's uncaught-by-design record: the `?`/`??` introspection suffix
# (`df.head?`) and a cell magic whose BODY is not Python (`%%bash`, `%%sql`,
# `%%R`, `%%writefile`) -- blanking the magic line alone leaves a
# non-Python body behind, so the notebook still fails to parse.
_NOTEBOOK_MAGIC_LINE_RE = re.compile(r"^\s*(%%|%|!)")
_NOTEBOOK_MAGIC_ASSIGN_RE = re.compile(r"^\s*\w[\w.]*\s*=\s*%")


def _repair_notebook_magics(source: str) -> str:
    lines = _source_lines(source)
    repaired = [
        ""
        if _NOTEBOOK_MAGIC_LINE_RE.match(line) or _NOTEBOOK_MAGIC_ASSIGN_RE.match(line)
        else line
        for line in lines
    ]
    return "\n".join(repaired)


def _parse_failure_reason(exc: BaseException) -> str:
    """A VARIABLE reason, never a hardcoded "syntax error at line N" --
    RecursionError, MemoryError and ValueError carry no `lineno` and would
    otherwise print the literal word "None" (Phase 11.1.1 plan 01)."""
    lineno = getattr(exc, "lineno", None)
    if lineno is not None:
        return f"syntax error at line {lineno}"
    return type(exc).__name__


def _parse_source(source: str, suffix: str) -> "tuple[ast.Module | None, str]":
    """Attempt `ast.parse` once, with one notebook-only repair retry on
    failure. Returns `(tree, reason)` — `tree` is `None` and `reason` names
    why when both attempts (or the only attempt, for a non-notebook
    source) failed; `reason` is `""` on success.

    Phase 11.1.1 plan 01 (Decision 7). One `ast.parse` per `check()` call,
    one flag — no per-code fallback and no partial tree. Two scanners
    would otherwise disagree about `first_split` inside one run, and a
    gate whose codes disagree about where the split is cannot be used as
    evidence.

    The guard is `(SyntaxError, ValueError, RecursionError, MemoryError)`.
    `except SyntaxError` alone crashes the gate on an ordinary long
    chained expression: measured this session, CPython 3.12.10 raises
    RecursionError on a chain of 70,000 binary operators at a lowered
    recursion limit; CPython 3.14.6's C parser does not honour
    `sys.setrecursionlimit` until a far larger depth, consistent with the
    documented claim that it parses 10,000 chained operators and only
    raises at 50,000. `KeyboardInterrupt` and `SystemExit` are not
    `Exception` subclasses and are not caught.

    `ast.parse` accepts the RUNNING interpreter's grammar, so which path
    an entrypoint takes can depend on the interpreter's Python version --
    disclosed via `python:{major}.{minor}` in both decision records, not
    hidden (Decision 7, T-11.1.1-12).
    """
    try:
        return ast.parse(source), ""
    except (SyntaxError, ValueError, RecursionError, MemoryError) as exc:
        first_reason = _parse_failure_reason(exc)
        if suffix != ".ipynb":
            return None, first_reason
        try:
            return ast.parse(_repair_notebook_magics(source)), ""
        except (SyntaxError, ValueError, RecursionError, MemoryError) as exc2:
            return None, _parse_failure_reason(exc2)


def _read_source(path: Path) -> str | None:
    suffix = path.suffix.lower()
    if suffix == ".py":
        try:
            raw = path.read_bytes()
        except OSError:
            return None
        try:
            # utf-8-sig decodes BOM-less UTF-8 identically and strips a
            # leading byte-order mark when one is present. A BOM read as
            # plain "utf-8" reaches ast.parse as U+FEFF and raises
            # SyntaxError: invalid non-printable character U+FEFF.
            return raw.decode("utf-8-sig")
        except (UnicodeDecodeError, ValueError):
            # Phase 11.1.1 plan 01 (Decision 3a): an undecodable entrypoint
            # is never silently a pass. Today a UnicodeDecodeError
            # propagates out of check() as a gate ERROR (exit 2); swallowing
            # it to None instead would convert that loud failure into a
            # silent exit-0 pass with zero findings, zero pass lines and
            # zero decision records -- worse than either. A
            # replacement-character read still finds any leak on the lines
            # that decoded, and the degraded read is named on the pass
            # line by check() itself. errors="replace" cannot itself raise.
            return raw.decode("utf-8", errors="replace")
    if suffix == ".ipynb":
        try:
            # Phase 11.1.1 plan 02 (§1.1(a) of 11.1.1-AST-DESIGN.md,
            # extended to .ipynb for consistency with the .py read above).
            # A BOM breaks json.loads exactly as it breaks ast.parse --
            # read as plain "utf-8" it reaches json.loads as a leading
            # U+FEFF character and raises json.JSONDecodeError, which
            # this except clause already returns None for -- silently
            # marking a real, readable notebook as unscannable rather
            # than scanning it. utf-8-sig decodes BOM-less UTF-8
            # identically and strips a leading BOM when one is present.
            nb = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            return None
        chunks: list[str] = []
        for cell in nb.get("cells") or []:
            cell_type = cell.get("cell_type")
            is_code = cell_type == "code"
            is_markdown = cell_type == "markdown"
            if not (is_code or is_markdown):
                # raw / unknown cell types are dropped entirely, exactly as
                # before.
                continue
            src = cell.get("source") or ""
            chunk = "".join(src) if isinstance(src, list) else str(src)
            if is_markdown:
                # Phase 11.1.1 plan 01 (Decision 2): markdown cells are
                # blanked CHARACTER-WISE, not line-counted. The rejected
                # alternative, `max(1, len(src.splitlines()))` blank lines,
                # under-counts by one whenever the cell text ends in a
                # newline -- the common nbformat shape -- and miscounts
                # again for \r, \x0c and the Unicode line separators.
                # Measured this session against three markdown shapes: a
                # 2-element list ending in a newline needs 3 line slots,
                # not the 2 the count formula gives; the same list with no
                # trailing newline needs 2 and the formula happens to
                # agree; a plain string ending in a newline needs 3, not 2.
                # Since preserving line geometry is the SOLE reason
                # blank-padding was chosen over dropping markdown cells
                # outright, an arithmetic that does not preserve it
                # defeats its own purpose. Blanking every non-newline
                # character of the SAME chunk the code-cell branch would
                # otherwise contribute preserves geometry BY CONSTRUCTION:
                # every newline survives, every other character does not.
                chunk = re.sub(r"[^\r\n]", "", chunk)
            chunks.append(chunk)
        return "\n".join(chunks)
    return None


def _first_line_matching(
    lines: list[str],
    markers: tuple[str, ...],
    masked: "frozenset[int]" = frozenset(),
) -> int | None:
    """Phase 11.1.1 plan 01 (Decision 5): `masked` -- zero-based line
    indices from `_prose_line_indices` -- are skipped in addition to the
    existing comment/import skip guard, so a split marker that appears
    only inside a docstring stops counting as a split. Empty by default,
    so every caller other than `first_split`'s union is unaffected."""
    for index, line in enumerate(lines):
        if index in masked:
            continue
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if re.match(r"^(from|import)\b", stripped):
            continue
        for marker in markers:
            if marker in line:
                return index
    return None


def _first_fit_leak_line(lines: list[str]) -> int | None:
    """The FALLBACK path's fit-before-split detector -- used only when the
    entrypoint could not be parsed (`_parse_source` returned no tree). The
    parsed path drives DSX-CODE-001 from `_call_sites` instead (Phase
    11.1.1 plan 01, §3.3-3.4 of 11.1.1-AST-DESIGN.md)."""
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if re.match(r"^(from|import)\b", stripped):
            continue
        # Pipeline.fit(X_train) after a split is allowed — still counts as fit;
        # CODE-001 only fires when fit precedes split.
        if PIPELINE_FIT_TRAIN_RE.search(line):
            return index
        for pattern in FIT_LEAK_MARKERS:
            if re.search(pattern, line):
                # Phase 11.1.1 plan 01 (finding CR-03): a redundant literal
                # re-check used to live here --
                # `if "fit(" in line or "fit_transform" in line or
                # "partial_fit" in line` -- which undid FIT_LEAK_MARKERS'
                # own `\s*` tolerance: `model.fit (df)` (a space before the
                # parenthesis) matched the regex but failed this literal
                # check, so the finding never fired. Deleted; the regex
                # match above is authoritative on its own.
                return index
    return None


def _first_full_frame_cleaning_line(lines: list[str]) -> int | None:
    """Lowest line index satisfying `_is_full_frame_impute` or
    `_is_full_frame_spread_filter` (REQ-P11.1-01). Repeats `_first_line_matching`'s
    skip guard rather than reusing it — that helper takes plain substrings, this
    one takes co-occurrence predicates, and merging the two would widen a function
    three shipped codes already depend on."""
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if re.match(r"^(from|import)\b", stripped):
            continue
        if _is_full_frame_impute(line) or _is_full_frame_spread_filter(line):
            return index
    return None


def _fit_call_arguments(lines: list[str]) -> "list[tuple[int, str]]":
    """Index-and-token pairs for EVERY `FIT_CALL_RE` match on every
    non-comment, non-import line (REQ-P11.1-01; widened to `finditer` in
    Phase 11.1.1 plan 02, §2.2/Edit F -- SC3).

    `search` promoted to `finditer`, and the `if match is None: continue`
    guard removed with it: the loop body below now only ever sees real
    match objects, one per match, in left-to-right source order, so a
    semicolon-joined line carrying two fit calls yields BOTH tokens
    instead of letting a safe first call mask a leaky second. `FIT_CALL_RE`'s
    trailing `\\s*[),]` is what still keeps a malformed call (no closing
    parenthesis, or a bare numeric first argument) out -- a call that fails
    to match yields no match object for `finditer` to iterate over, exactly
    as it yielded none for `search` to return. The keyword prefix is
    allowlisted to the same `FIT_FIRST_PARAM_NAMES` the AST path accepts
    (Edit F), so the two mechanisms agree about which keyword names a
    training frame instead of disagreeing on it.

    Exactly ONE extraction path exists per mechanism: no `search`-based
    single-match variant survives beside this one (plan 02 prohibition 3)."""
    results: "list[tuple[int, str]]" = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if re.match(r"^(from|import)\b", stripped):
            continue
        for match in FIT_CALL_RE.finditer(line):
            token = match.group(1)
            if not token:
                continue
            results.append((index, token))
    return results


def _is_training_frame(token: str) -> bool:
    """True when `token` starts with a member of `TRAINING_FRAME_NAMES`
    (REQ-P11.1-01). Prefix matching, not equality — accepts a scaled, dotted or
    subscripted training frame (`X_train_scaled`, `X_train.values`,
    `train_df[cols]`) without a second pattern."""
    return any(token.startswith(name) for name in TRAINING_FRAME_NAMES)


def _stat_test_lines_referencing(lines: list[str], target: str) -> list[int]:
    """Indices of non-comment, non-import lines where `STAT_TEST_CALL_RE`
    matches, and either that line itself or one of the
    `_TARGET_REFERENCE_LOOKBACK` (three) lines immediately preceding it
    references `target` (REQ-P11.1-03).

    The lookback exists because the reproduction's own idiom
    (`references/The AI Data Scientist.md`, Table 1) builds the contingency
    table — the line that actually carries the target reference — on one
    line, then calls the statistical test on the very next line. A lookback
    of one would already catch that exact idiom; three lines is a stated
    margin, not a magic constant.

    The target-reference recogniser is built fresh from the escaped target
    text (`re.escape`), so a column name containing regular-expression
    metacharacters cannot change the pattern's meaning or complexity class
    (threat T-11.1-11). It recognises exactly three forms: a bracket
    subscript with single quotes (`['target']`), a bracket subscript with
    double quotes (`["target"]`), and an attribute access (`.target`). The
    bracket forms are exact by construction — the closing quote immediately
    follows the target text, so a longer identifier sharing that text as a
    substring cannot match. The attribute form requires a literal `.`
    (a non-identifier character) immediately before the target text and a
    trailing `\\b` immediately after it, so neither a longer identifier that
    merely starts with the target text (`.targetted`) nor one that merely
    ends with it (`.my_target`, no literal dot before `target`) is treated as
    a reference — only a real dotted attribute access on exactly that name.
    """
    escaped = re.escape(target)
    reference_re = re.compile(
        r"\['" + escaped + r"'\]"
        r"|\[\"" + escaped + r"\"\]"
        r"|\." + escaped + r"\b"
    )
    results: list[int] = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if re.match(r"^(from|import)\b", stripped):
            continue
        if not STAT_TEST_CALL_RE.search(line):
            continue
        window_start = max(0, index - _TARGET_REFERENCE_LOOKBACK)
        window = lines[window_start : index + 1]
        if any(reference_re.search(candidate) for candidate in window):
            results.append(index)
    return results
