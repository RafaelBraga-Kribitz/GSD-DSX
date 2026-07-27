"""dsx command-line interface — the surface GSD gates call.

Every subcommand obeys one contract:

    exit 0  the spec satisfies the check at the configured blocking severity
    exit 1  at least one finding at or above that severity
    exit 2  the check could not run (bad path, unparseable spec, internal error)

GSD's ``command-exit-zero`` gate predicate maps 1 to "block" and 2 to the gate's
``onError`` route, which is exactly the distinction we want: a spec we judged bad
stops the loop; a spec we could not read is an operational error, not a verdict.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Callable

from . import __version__
from .checks import claims, coherence, design, dq, metrics, ml, repro, stats, viz
from .findings import EXIT_ERROR, CheckError, Report, Severity, emit, merge
from .loader import SpecParseError, load
from .spec import describe_vocabulary, validate_structure

DEFAULT_SPEC_NAMES = (
    "ANALYSIS-SPEC.yaml",
    "ANALYSIS-SPEC.yml",
    "ANALYSIS-SPEC.json",
    "analysis-spec.yaml",
)

# Registry of individual checks. `dsx audit` runs all of them.
CHECKS: dict[str, Callable] = {
    "spec": validate_structure,
    "design": design.check,
    "stats": stats.check,
    "ml": ml.check,
    "metrics": metrics.check,
    "claims": claims.check,
    "viz": viz.check,
    "coherence": coherence.check,
    "dq": dq.check,
}

# Which checks each GSD loop point cares about. Keeping this here rather than in
# the capability manifest means the gate command stays short and the policy stays
# versioned with the code that implements it.
GATE_PROFILES: dict[str, tuple[str, ...]] = {
    "plan": ("spec", "design", "metrics", "coherence"),
    "execute": ("spec", "ml", "repro", "dq"),
    "verify": (
        "spec", "design", "stats", "ml", "metrics", "claims", "viz", "repro",
        "dq", "coherence",
    ),
    "ship": (
        "spec", "design", "stats", "ml", "metrics", "claims", "viz", "repro",
        "dq", "coherence",
    ),
}

# Default blocking severity per gate. Planning blocks on structural defects;
# shipping blocks on anything material.
GATE_THRESHOLDS: dict[str, str] = {
    "plan": "CRITICAL",
    "execute": "CRITICAL",
    "verify": "HIGH",
    "ship": "HIGH",
}


def find_spec(explicit: "str | None", phase_dir: "str | None") -> Path:
    if explicit:
        path = Path(explicit)
        if not path.exists():
            raise CheckError(f"spec not found: {path}")
        return path

    roots = [Path(phase_dir)] if phase_dir else []
    roots.extend([Path.cwd(), Path.cwd() / ".planning"])
    for root in roots:
        for name in DEFAULT_SPEC_NAMES:
            candidate = root / name
            if candidate.exists():
                return candidate
    searched = ", ".join(str(r) for r in roots)
    raise CheckError(
        "no ANALYSIS-SPEC found. Looked for "
        + ", ".join(DEFAULT_SPEC_NAMES)
        + f" in: {searched}. Run `dsx init` to scaffold one."
    )


def run_checks(
    spec: dict,
    names: "tuple[str, ...]",
    phase_dir: "str | None",
    *,
    gate_point: "str | None" = None,
    resolve_root: "str | None" = None,
) -> Report:
    """Run named checks.

    ``phase_dir`` is the GSD phase directory (entrypoint existence checks).
    ``resolve_root`` is where relative evidence/profile paths resolve — defaults
    to ``phase_dir``, then cwd. Callers typically pass the spec's parent so
    ``--spec examples/good-….yaml`` finds sibling artifacts.
    """
    reports: list[Report] = []
    strict = gate_point in {"verify", "ship"}
    root = resolve_root or phase_dir
    for name in names:
        if name == "repro":
            reports.append(repro.check(spec, phase_dir))
        elif name == "dq":
            reports.append(dq.check(spec, root))
        elif name == "claims":
            reports.append(claims.check(spec, root))
        elif name == "coherence":
            reports.append(coherence.check(spec, strict=strict))
        elif name in CHECKS:
            reports.append(CHECKS[name](spec))
        else:
            raise CheckError(
                f"unknown check {name!r}; known: "
                + ", ".join(sorted(set(CHECKS) | {"repro"}))
            )
    return merge("+".join(names), reports)


# ── Subcommands ──────────────────────────────────────────────────────────────


def cmd_validate(args: argparse.Namespace) -> int:
    path = find_spec(args.spec, args.phase_dir)
    spec = load(path)
    report = run_checks(
        spec,
        ("spec",),
        args.phase_dir,
        resolve_root=args.phase_dir or str(path.parent),
    )
    report.context["spec_path"] = str(path)
    return emit(report, Severity.parse(args.block_on), args.json, args.verbose)


def cmd_check(args: argparse.Namespace) -> int:
    path = find_spec(args.spec, args.phase_dir)
    spec = load(path)
    names = tuple(args.checks) if args.checks else tuple(CHECKS) + ("repro",)
    report = run_checks(
        spec,
        names,
        args.phase_dir,
        resolve_root=args.phase_dir or str(path.parent),
    )
    report.context["spec_path"] = str(path)
    return emit(report, Severity.parse(args.block_on), args.json, args.verbose)


def cmd_audit(args: argparse.Namespace) -> int:
    path = find_spec(args.spec, args.phase_dir)
    spec = load(path)
    report = run_checks(
        spec,
        tuple(CHECKS) + ("repro",),
        args.phase_dir,
        gate_point="ship",
        resolve_root=args.phase_dir or str(path.parent),
    )
    report.context["spec_path"] = str(path)
    code = emit(report, Severity.parse(args.block_on), args.json, args.verbose)
    if args.report:
        Path(args.report).write_text(
            _markdown_report(report, Severity.parse(args.block_on), str(path)),
            encoding="utf-8",
        )
    return code


def cmd_gate(args: argparse.Namespace) -> int:
    """Run the profile for a GSD loop point. This is what capability.json calls."""
    point = args.point
    if point not in GATE_PROFILES:
        raise CheckError(
            f"unknown gate point {point!r}; expected one of {', '.join(GATE_PROFILES)}"
        )
    threshold = Severity.parse(args.block_on or GATE_THRESHOLDS[point])

    try:
        path = find_spec(args.spec, args.phase_dir)
    except CheckError:
        if args.allow_missing:
            print(
                f"dsx: no ANALYSIS-SPEC found for gate '{point}' — skipping "
                "(dsx.require_spec is disabled)",
                file=sys.stdout,
            )
            return 0
        raise

    spec = load(path)
    report = run_checks(
        spec,
        GATE_PROFILES[point],
        args.phase_dir,
        gate_point=point,
        resolve_root=args.phase_dir or str(path.parent),
    )
    report.check = f"gate:{point}"
    report.context["spec_path"] = str(path)
    if args.report:
        Path(args.report).write_text(
            _markdown_report(report, threshold, str(path)), encoding="utf-8"
        )
    return emit(report, threshold, args.json, args.verbose)


def cmd_profile(args: argparse.Namespace) -> int:
    from .profiler import profile_csv, write_profile

    pk = [p.strip() for p in (args.pk or "").split(",") if p.strip()] or None
    sentinels: list = []
    for raw in args.sentinel or []:
        try:
            sentinels.append(int(raw))
        except ValueError:
            try:
                sentinels.append(float(raw))
            except ValueError:
                sentinels.append(raw)

    profile = profile_csv(
        args.csv,
        primary_key=pk,
        time_column=args.time,
        sentinels=sentinels or None,
    )
    out = Path(args.out or "DATA-PROFILE.yaml")
    write_profile(profile, out)
    summary = {
        "wrote": str(out).replace("\\", "/"),
        "row_count": profile["row_count"],
        "source_hash": profile["source_hash"],
        "primary_key_unique": profile["primary_key_unique"],
        "sentinels_found": profile["sentinels_found"],
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(
            f"wrote {out} — {profile['row_count']} rows, "
            f"hash={profile['source_hash'][:19]}…"
        )
    return 0


def cmd_recommend(args: argparse.Namespace) -> int:
    from .checks.stats import recommend_test

    recommendation = recommend_test(
        args.outcome_type,
        args.groups,
        paired=args.paired,
        normal=_tri(args.normal),
        equal_variance=_tri(args.equal_variance),
        n_per_group=args.n_per_group,
        overdispersed=_tri(args.overdispersed),
    )
    print(json.dumps(recommendation, indent=2))
    return 0


def cmd_power(args: argparse.Namespace) -> int:
    from .mathx import mde_two_proportions, power_two_proportions, sample_size_two_proportions

    out: dict[str, object] = {"alpha": args.alpha, "power": args.power, "baseline": args.baseline}
    if args.mde is not None:
        out["mde"] = args.mde
        out["required_n_per_arm"] = sample_size_two_proportions(
            args.baseline, args.mde, args.alpha, args.power
        )
        if args.n_per_arm:
            out["achieved_power_at_n"] = round(
                power_two_proportions(args.baseline, args.mde, args.n_per_arm, args.alpha), 4
            )
    if args.n_per_arm:
        out["n_per_arm"] = args.n_per_arm
        out["detectable_mde"] = round(
            mde_two_proportions(args.baseline, args.n_per_arm, args.alpha, args.power), 6
        )
    print(json.dumps(out, indent=2))
    return 0


def cmd_vocab(args: argparse.Namespace) -> int:
    print(json.dumps(describe_vocabulary(), indent=2))
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    template = Path(__file__).resolve().parent.parent / "templates" / "ANALYSIS-SPEC.yaml"
    if not template.exists():
        raise CheckError(f"template not found at {template}")
    target = Path(args.output or "ANALYSIS-SPEC.yaml")
    if target.exists() and not args.force:
        raise CheckError(f"{target} already exists; pass --force to overwrite")
    target.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"wrote {target}")
    return 0


def _tri(value: "str | None") -> "bool | None":
    if value is None:
        return None
    lowered = value.strip().lower()
    if lowered in ("true", "yes", "1"):
        return True
    if lowered in ("false", "no", "0"):
        return False
    return None


def _markdown_report(report: Report, threshold: Severity, spec_path: str) -> str:
    counts = report.counts()
    verdict = "BLOCKED" if report.blocks(threshold) else "PASSED"
    lines = [
        f"# dsx report — {report.check}",
        "",
        f"- **Verdict:** {verdict} (blocking at {threshold.label})",
        f"- **Spec:** `{spec_path}`",
        "- **Findings:** "
        + ", ".join(f"{k} {v}" for k, v in counts.items() if v),
        "",
    ]
    if report.findings:
        lines += ["## Findings", ""]
        for finding in sorted(report.findings, key=lambda f: (-f.severity, f.code)):
            lines += [
                f"### {finding.code} — {finding.title}",
                "",
                f"**Severity:** {finding.severity.label}  ",
                f"**Where:** `{finding.where or 'n/a'}`",
                "",
            ]
            if finding.detail:
                lines += [finding.detail, ""]
            if finding.remedy:
                lines += [f"**Fix:** {finding.remedy}", ""]
    if report.passed_checks:
        lines += ["## Passed", ""]
        lines += [f"- {item}" for item in sorted(set(report.passed_checks))]
        lines.append("")
    return "\n".join(lines)


# ── Parser ───────────────────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dsx",
        description="Deterministic guardrails for data-science, analytics and BI work.",
    )
    parser.add_argument("--version", action="version", version=f"dsx {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    def add_common(p: argparse.ArgumentParser, default_block: str = "HIGH") -> None:
        p.add_argument("--spec", help="path to ANALYSIS-SPEC (auto-discovered when omitted)")
        p.add_argument("--phase-dir", help="GSD phase directory to search and resolve paths against")
        p.add_argument("--block-on", default=default_block,
                       help="minimum severity that fails the command (default: %(default)s)")
        p.add_argument("--json", action="store_true", help="emit machine-readable JSON")
        p.add_argument("--verbose", action="store_true", help="list checks that passed")

    p_validate = sub.add_parser("validate", help="structural validation of the spec only")
    add_common(p_validate, "CRITICAL")
    p_validate.set_defaults(func=cmd_validate)

    p_check = sub.add_parser("check", help="run selected checks")
    p_check.add_argument("checks", nargs="*", help="subset to run: " + ", ".join(sorted(CHECKS)) + ", repro")
    add_common(p_check)
    p_check.set_defaults(func=cmd_check)

    p_audit = sub.add_parser("audit", help="run every check")
    add_common(p_audit)
    p_audit.add_argument("--report", help="also write a markdown report to this path")
    p_audit.set_defaults(func=cmd_audit)

    p_gate = sub.add_parser("gate", help="run the profile for a GSD loop point")
    p_gate.add_argument("point", choices=sorted(GATE_PROFILES))
    add_common(p_gate, "")
    p_gate.add_argument("--report", help="also write a markdown report to this path")
    p_gate.add_argument("--allow-missing", action="store_true",
                        help="exit 0 when no spec exists instead of erroring")
    p_gate.set_defaults(func=cmd_gate)

    p_rec = sub.add_parser("recommend-test", help="derive the correct test from the data's shape")
    p_rec.add_argument("outcome_type", help="proportion | continuous | count | ordinal | time_to_event")
    p_rec.add_argument("--groups", type=int, default=2)
    p_rec.add_argument("--paired", action="store_true")
    p_rec.add_argument("--normal", choices=["true", "false"])
    p_rec.add_argument("--equal-variance", choices=["true", "false"])
    p_rec.add_argument("--overdispersed", choices=["true", "false"])
    p_rec.add_argument("--n-per-group", type=int)
    p_rec.set_defaults(func=cmd_recommend)

    p_power = sub.add_parser("power", help="sample size, achieved power and detectable effect")
    p_power.add_argument("--baseline", type=float, required=True, help="baseline proportion")
    p_power.add_argument("--mde", type=float, help="absolute minimum detectable effect")
    p_power.add_argument("--n-per-arm", type=int)
    p_power.add_argument("--alpha", type=float, default=0.05)
    p_power.add_argument("--power", type=float, default=0.80)
    p_power.set_defaults(func=cmd_power)

    p_vocab = sub.add_parser("vocab", help="dump every closed vocabulary as JSON")
    p_vocab.set_defaults(func=cmd_vocab)

    p_init = sub.add_parser("init", help="scaffold an ANALYSIS-SPEC from the template")
    p_init.add_argument("--output", "-o")
    p_init.add_argument("--force", action="store_true")
    p_init.set_defaults(func=cmd_init)

    p_profile = sub.add_parser(
        "profile",
        help="compute a DATA-PROFILE.yaml from a local CSV (stdlib)",
    )
    p_profile.add_argument("csv", help="path to a CSV extract")
    p_profile.add_argument("--out", "-o", default="DATA-PROFILE.yaml")
    p_profile.add_argument("--pk", help="comma-separated primary key columns")
    p_profile.add_argument("--time", help="time column for gap detection")
    p_profile.add_argument(
        "--sentinel",
        action="append",
        help="banned sentinel value to scan for (repeatable)",
    )
    p_profile.add_argument("--json", action="store_true")
    p_profile.set_defaults(func=cmd_profile)

    return parser


def main(argv: "list[str] | None" = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (CheckError, SpecParseError) as exc:
        print(f"dsx: {exc}", file=sys.stderr)
        return EXIT_ERROR
    except ValueError as exc:
        print(f"dsx: invalid input — {exc}", file=sys.stderr)
        return EXIT_ERROR
    except KeyboardInterrupt:  # pragma: no cover
        return 130


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
