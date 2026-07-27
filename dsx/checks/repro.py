"""Reproducibility checks. Codes DSX-REP-*.

An analysis nobody can re-run is an opinion with a chart attached. These checks
enforce the four things that make a result recoverable six months later: a pinned
environment, a bounded and identified dataset, a seed for anything stochastic,
and a pointer to the code that produced the numbers.
"""

from __future__ import annotations

from pathlib import Path

from ..findings import Report
from ..spec import as_number, is_blank, items, normalize, section

STOCHASTIC_MARKERS = (
    "random_forest", "gradient_boosting", "xgboost", "lightgbm", "catboost",
    "neural", "mlp", "kmeans", "k_means", "dbscan", "umap", "tsne", "t_sne",
    "bootstrap", "permutation", "mcmc", "bayesian", "sgd", "dropout",
    "random_search", "train_test_split", "sampling", "monte_carlo",
)


def check(
    spec: dict,
    phase_dir: "str | None" = None,
    *,
    strict: bool = False,
) -> Report:
    report = Report(check="repro")
    repro = section(spec, "reproducibility")

    _check_seed(spec, repro, report)
    _check_environment(repro, report)
    _check_data_identity(spec, report)
    _check_code_pointer(repro, report, phase_dir)
    _check_notebook_hygiene(repro, report)
    if strict:
        _check_repro_lock(spec, repro, report)
    return report


def _uses_stochastic_method(spec: dict) -> list[str]:
    blob = " ".join(
        [
            normalize(str(section(spec, "model").get("algorithm", ""))),
            normalize(str(section(spec, "model").get("task", ""))),
            normalize(str(section(spec, "analysis").get("test", ""))),
            normalize(str(section(spec, "analysis").get("method", ""))),
            normalize(str(section(spec, "model").get("split", ""))),
        ]
    )
    return [marker for marker in STOCHASTIC_MARKERS if marker in blob]


def _check_seed(spec: dict, repro: dict, report: Report) -> None:
    markers = _uses_stochastic_method(spec)
    seed = repro.get("random_seed")
    if not markers:
        return
    if seed is None or as_number(seed) is None:
        report.add(
            "DSX-REP-001",
            "HIGH",
            "Stochastic methods used with no random seed declared",
            detail=(
                "Detected: "
                + ", ".join(markers)
                + ". Without a fixed seed the same code produces different numbers on every "
                "run, so no result here can be confirmed or refuted."
            ),
            remedy=(
                "Declare reproducibility.random_seed and set it for every library involved — "
                "the language RNG, numpy, and the modelling framework each have their own."
            ),
            where="spec.reproducibility.random_seed",
            stochastic=markers,
        )
    else:
        report.ok(f"seed {seed} declared for {len(markers)} stochastic component(s)")


def _check_environment(repro: dict, report: Report) -> None:
    has_lock = not is_blank(repro.get("lockfile"))
    has_versions = not is_blank(repro.get("package_versions"))
    if not has_lock and not has_versions:
        report.add(
            "DSX-REP-010",
            "MEDIUM",
            "No environment pinning declared",
            detail=(
                "Statistical libraries change defaults between versions — solver choices, "
                "correction methods, tie handling. An unpinned environment silently changes "
                "results."
            ),
            remedy=(
                "Declare reproducibility.lockfile (requirements.txt, uv.lock, environment.yml) "
                "or list package_versions for the libraries that produced the numbers."
            ),
            where="spec.reproducibility",
        )
    else:
        report.ok("environment pinned")

    if is_blank(repro.get("language_version")):
        report.add(
            "DSX-REP-011", "LOW", "Language runtime version is not declared",
            remedy="Record the Python or R version used.",
            where="spec.reproducibility.language_version",
        )


def _check_data_identity(spec: dict, report: Report) -> None:
    sources = items(spec, "data")
    if not sources:
        return
    unidentified = []
    for source in sources:
        has_hash = not is_blank(source.get("hash"))
        has_snapshot = not is_blank(source.get("snapshot_at"))
        has_bounds = not is_blank(source.get("period"))
        if not (has_hash or has_snapshot or (has_bounds and not is_blank(source.get("rows")))):
            unidentified.append(str(source.get("name", "?")))

    if unidentified:
        report.add(
            "DSX-REP-020",
            "MEDIUM",
            f"{len(unidentified)} data source(s) cannot be pinned to a specific extract",
            detail=(
                "Unpinned: "
                + ", ".join(unidentified)
                + ". A live table re-queried later returns different rows — late arrivals, "
                "backfills, corrections — so the analysis cannot be reproduced."
            ),
            remedy=(
                "Record a content hash, a snapshot timestamp, or the period plus the row count "
                "for each source."
            ),
            where="spec.data",
            unidentified=unidentified,
        )
    else:
        report.ok(f"all {len(sources)} data source(s) identifiable")


def _check_code_pointer(repro: dict, report: Report, phase_dir: "str | None") -> None:
    entrypoint = repro.get("entrypoint")
    if is_blank(entrypoint):
        report.add(
            "DSX-REP-030",
            "HIGH",
            "No analysis entrypoint declared",
            detail="Without a named entrypoint, 're-run the analysis' has no referent.",
            remedy="Declare reproducibility.entrypoint — the script or command that reproduces every number.",
            where="spec.reproducibility.entrypoint",
        )
        return

    if phase_dir:
        candidate = Path(phase_dir) / str(entrypoint)
        alt = Path(str(entrypoint))
        if not candidate.exists() and not alt.exists():
            report.add(
                "DSX-REP-031",
                "HIGH",
                f"Declared entrypoint {entrypoint!r} does not exist",
                detail=f"Looked in {candidate} and {alt}.",
                remedy="Fix the path, or commit the script it points at.",
                where="spec.reproducibility.entrypoint",
            )
            return
    report.ok(f"entrypoint declared: {entrypoint}")


def _check_notebook_hygiene(repro: dict, report: Report) -> None:
    entrypoint = str(repro.get("entrypoint") or "")
    if not entrypoint.endswith(".ipynb"):
        return
    if not repro.get("runs_clean_top_to_bottom"):
        report.add(
            "DSX-REP-040",
            "HIGH",
            "Notebook entrypoint not confirmed to run top-to-bottom from a clean kernel",
            detail=(
                "Out-of-order execution leaves results that depend on cells no longer present, "
                "or on state from a deleted cell. The notebook then reproduces nothing."
            ),
            remedy=(
                "Restart the kernel, run all cells, confirm every number matches, then set "
                "reproducibility.runs_clean_top_to_bottom: true. Better: move the logic into a "
                "module the notebook imports."
            ),
            where="spec.reproducibility.runs_clean_top_to_bottom",
        )
    else:
        report.ok("notebook confirmed to run clean top-to-bottom")


def _check_repro_lock(spec: dict, repro: dict, report: Report) -> None:
    tests = items(section(spec, "results"), "tests")
    if not tests:
        return

    # Key omitted vs explicit null — distinguish via raw section membership.
    if "repro_lock" not in repro:
        report.add(
            "DSX-REP-050",
            "HIGH",
            "repro_lock key missing while results.tests is non-empty",
            detail=(
                "Without a lock (or an explicit null opt-out), a null or revised result can "
                "be rationalised after the fact with no configuration trail."
            ),
            remedy=(
                "Add reproducibility.repro_lock with schema_version and "
                "stochasticity_declaration, or set repro_lock: null for an honest opt-out."
            ),
            where="spec.reproducibility.repro_lock",
        )
        return

    lock = repro.get("repro_lock")
    if lock is None:
        report.add(
            "DSX-REP-051",
            "MEDIUM",
            "repro_lock is null (honest opt-out)",
            detail="Explicit null records that configuration was not locked.",
            remedy="Populate repro_lock when the analysis should be investigable later.",
            where="spec.reproducibility.repro_lock",
        )
        return

    if not isinstance(lock, dict):
        report.add(
            "DSX-REP-052",
            "HIGH",
            "repro_lock incomplete (schema_version / stochasticity_declaration)",
            remedy="Use a YAML object with schema_version and stochasticity_declaration.",
            where="spec.reproducibility.repro_lock",
        )
        return

    if is_blank(lock.get("schema_version")) or is_blank(lock.get("stochasticity_declaration")):
        report.add(
            "DSX-REP-052",
            "HIGH",
            "repro_lock incomplete (schema_version / stochasticity_declaration)",
            detail=(
                "The declaration is required so the lock cannot be read as a byte-replay guarantee."
            ),
            remedy="Set both fields. See references/analytical-logic.md.",
            where="spec.reproducibility.repro_lock",
        )
        return

    from .. import __version__ as dsx_version

    declared = lock.get("dsx_version")
    if is_blank(declared):
        report.add(
            "DSX-REP-053",
            "MEDIUM",
            "repro_lock.dsx_version missing or mismatched",
            remedy=f"Set dsx_version to {dsx_version!r}.",
            where="spec.reproducibility.repro_lock.dsx_version",
        )
    elif str(declared) != str(dsx_version):
        report.add(
            "DSX-REP-053",
            "MEDIUM",
            "repro_lock.dsx_version missing or mismatched",
            detail=f"Declared {declared!r}; package is {dsx_version!r}.",
            remedy=f"Update dsx_version to {dsx_version!r} or note why it differs.",
            where="spec.reproducibility.repro_lock.dsx_version",
        )
    else:
        report.ok(f"repro_lock present (dsx_version={dsx_version})")
