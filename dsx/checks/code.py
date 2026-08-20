"""Entrypoint fit-before-split scans. Codes DSX-CODE-*.

Stdlib-only: `.py` as text; `.ipynb` via json cell source concat in line order.
Missing / non-text entrypoints are skipped (repro covers missing paths).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from ..decisions import DecisionRecord, record_decision
from ..findings import Report
from ..spec import is_blank, section

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

PIPELINE_FIT_TRAIN_RE = re.compile(
    r"(?i)Pipeline\s*\(.*\)\s*\.\s*fit\s*\(\s*X_train\b"
)

# Phase 11.1 (REQ-P11.1-01): full-frame cleaning idioms computed before any split
# exists — a fillna imputation whose text also names a mean/median/mode aggregate,
# or a row filter that both subscripts/filters a frame and names a std/quantile
# call. Two independent lookaheads each, one bounded scan per lookahead — not a
# nested quantifier — so co-occurrence on the line is order-independent and
# linear, following the discipline dsx/spec.py's `_FALSIFIER_NUMBER_RE` comment
# documents (threat T-11.1-01): a nested quantifier here would expose the gate to
# catastrophic backtracking on adversarial, analyst-authored entrypoint text.
FULL_FRAME_IMPUTE_RE = re.compile(
    r"(?=.*\.fillna\s*\()(?=.*\.(?:mean|median|mode)\s*\()"
)
FULL_FRAME_SPREAD_FILTER_RE = re.compile(
    r"(?=.*\w+\s*\[)(?=.*\.(?:std|quantile)\s*\()"
)

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
FIT_CALL_RE = re.compile(
    r"\.fit(?:_transform)?\s*\(\s*([A-Za-z_][\w.\[\]'\"]*)\s*[),]"
)


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
    Structural criterion: DSX-CODE-021 is a membership test of an extracted
    first-argument token against TRAINING_FRAME_NAMES (matched as a prefix, not
    equality), combined with a >= index comparison between the triggering
    fit-call line and the first split-marker line.
    """
    report = Report(check="code")
    repro = section(spec, "reproducibility")
    entry = repro.get("entrypoint")
    if is_blank(entry):
        return report

    path = _resolve_entrypoint(str(entry), phase_dir)
    if path is None:
        return report

    source = _read_source(path)
    if source is None:
        return report

    lines = source.splitlines()
    first_split = _first_line_matching(lines, SPLIT_MARKERS)
    first_fit = _first_fit_leak_line(lines)
    has_model = bool(section(spec, "model"))

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

    fit_after_split_index: "int | None" = None
    fit_after_split_token: "str | None" = None
    if first_split is not None:
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


def _read_source(path: Path) -> str | None:
    suffix = path.suffix.lower()
    if suffix == ".py":
        try:
            return path.read_text(encoding="utf-8")
        except OSError:
            return None
    if suffix == ".ipynb":
        try:
            nb = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        chunks: list[str] = []
        for cell in nb.get("cells") or []:
            if cell.get("cell_type") not in {"code", "markdown"}:
                continue
            src = cell.get("source") or ""
            if isinstance(src, list):
                chunks.append("".join(src))
            else:
                chunks.append(str(src))
        return "\n".join(chunks)
    return None


def _first_line_matching(lines: list[str], markers: tuple[str, ...]) -> int | None:
    for index, line in enumerate(lines):
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
                if "fit(" in line or "fit_transform" in line or "partial_fit" in line:
                    return index
    return None


def _first_full_frame_cleaning_line(lines: list[str]) -> int | None:
    """Lowest line index matching `FULL_FRAME_IMPUTE_RE` or
    `FULL_FRAME_SPREAD_FILTER_RE` (REQ-P11.1-01). Repeats `_first_line_matching`'s
    skip guard rather than reusing it — that helper takes plain substrings, this
    one takes compiled patterns, and merging the two would widen a function three
    shipped codes already depend on."""
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if re.match(r"^(from|import)\b", stripped):
            continue
        if FULL_FRAME_IMPUTE_RE.search(line) or FULL_FRAME_SPREAD_FILTER_RE.search(line):
            return index
    return None


def _fit_call_arguments(lines: list[str]) -> "list[tuple[int, str]]":
    """Index-and-token pairs for every non-comment, non-import line where
    `FIT_CALL_RE` matches (REQ-P11.1-01). The group-extraction guard is the
    `if match is None: continue` below — `FIT_CALL_RE`'s trailing `\\s*[),]`
    already makes a malformed call (no closing parenthesis, or a bare numeric
    first argument) fail to match at all, so no line yielding a token is ever
    dereferenced without a match object to back it."""
    results: "list[tuple[int, str]]" = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if re.match(r"^(from|import)\b", stripped):
            continue
        match = FIT_CALL_RE.search(line)
        if match is None:
            continue
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
