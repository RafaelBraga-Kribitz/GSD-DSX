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
from .checks import (
    claims,
    code,
    coherence,
    decision,
    design,
    dq,
    figures,
    metrics,
    ml,
    narrative,
    repro,
    smells,
    stats,
    viz,
)
from .decisions import (
    DecisionRecord,
    InvocationHeader,
    append as append_decision,
    collect_from_report,
    decisions_path,
    frame_digest,
    next_invocation_id,
    read_all,
)
from .findings import EXIT_ERROR, CheckError, Report, Severity, emit, merge
from .frame import paradigm
from .loader import SpecParseError, load
from .spec import describe_vocabulary, validate_structure
from .suppressions import apply_suppressions

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
    "smells": smells.check,
    "figures": figures.check,
    "narrative": narrative.check,
    "code": code.check,
    "decision": decision.check,
    "paradigm": paradigm.check,
}

# Which checks each GSD loop point cares about. Keeping this here rather than in
# the capability manifest means the gate command stays short and the policy stays
# versioned with the code that implements it.
#
# "paradigm" (DSX-PAR-001, informational, REQ-P6-09) is registered at all four
# points, not just verify/ship: it must be visible wherever a gate runs, and
# INFO severity means it structurally cannot flip any gate's exit code.
GATE_PROFILES: dict[str, tuple[str, ...]] = {
    "plan": ("spec", "design", "metrics", "coherence", "paradigm"),
    "execute": ("spec", "ml", "repro", "dq", "code", "paradigm"),
    "verify": (
        "spec", "design", "stats", "ml", "metrics", "claims", "viz", "repro",
        "dq", "coherence", "smells", "figures", "narrative", "code", "decision",
        "paradigm",
    ),
    "ship": (
        "spec", "design", "stats", "ml", "metrics", "claims", "viz", "repro",
        "dq", "coherence", "smells", "figures", "narrative", "code", "decision",
        "paradigm",
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
            reports.append(repro.check(spec, phase_dir, strict=strict))
        elif name == "dq":
            reports.append(dq.check(spec, root))
        elif name == "claims":
            reports.append(claims.check(spec, root, strict=strict))
        elif name == "coherence":
            reports.append(coherence.check(spec, strict=strict))
        elif name == "figures":
            reports.append(figures.check(spec, root, strict=strict))
        elif name == "smells":
            reports.append(smells.check(spec))
        elif name == "narrative":
            reports.append(narrative.check(spec, root, gate_point=gate_point))
        elif name == "code":
            reports.append(code.check(spec, root))
        elif name == "design":
            reports.append(design.check(spec, strict=strict))
        elif name == "decision":
            reports.append(decision.check(spec, gate_point=gate_point))
        elif name in CHECKS:
            reports.append(CHECKS[name](spec))
        else:
            raise CheckError(
                f"unknown check {name!r}; known: "
                + ", ".join(sorted(set(CHECKS) | {"repro"}))
            )
    merged = merge("+".join(names), reports)
    return apply_suppressions(spec, merged)


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
    root = args.phase_dir or str(path.parent)
    report = run_checks(
        spec,
        GATE_PROFILES[point],
        args.phase_dir,
        gate_point=point,
        resolve_root=root,
    )
    report.check = f"gate:{point}"
    report.context["spec_path"] = str(path)
    _write_decision_trail(report, spec, root, point, args.verbose)
    if args.report:
        Path(args.report).write_text(
            _markdown_report(report, threshold, str(path)), encoding="utf-8"
        )
    return emit(report, threshold, args.json, args.verbose)


def _write_decision_trail(
    report: Report, spec: dict, root: str, point: str, verbose: bool
) -> None:
    """Append this gate run's invocation header and decision records to
    ``DECISIONS.jsonl`` (D-14, D-16). Only ``dsx gate`` calls this —
    ``validate``/``check``/``audit`` are read-only inspection commands, not
    the plan-through-ship trail D-04 wants rendered.

    Wrapped in ``try/except OSError`` and swallowed on failure: this is the
    mirror of D-04, ``dsx explain``'s side of the same rule. A trail that
    cannot be written is a missing trail, not a failed gate — the write is a
    side channel, never part of the block contract, so it can never change
    ``point``'s exit code. Surfaced only under ``--verbose``.
    """
    try:
        target = decisions_path(root)
        inv = next_invocation_id(target)
        append_decision(
            target,
            InvocationHeader(
                invocation_id=inv,
                gate_point=point,
                dsx_version=__version__,
                frame_digest=frame_digest(spec),
            ),
        )
        for n, raw in enumerate(collect_from_report(report), start=1):
            fields = {k: v for k, v in raw.items() if k != "record_type"}
            fields["id"] = f"DEC-{n:03d}"
            fields["invocation_id"] = inv
            append_decision(target, DecisionRecord(**fields))
    except OSError as exc:
        if verbose:
            print(f"dsx: could not write decision trail — {exc}", file=sys.stderr)


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


def cmd_explain(args: argparse.Namespace) -> int:
    """Render the decision trail (D-04, REQ-P6-08). A pure reader over
    ``DECISIONS.jsonl``: never imports the block-contract primitives (the
    severity ladder, the per-gate threshold table, the report emitter) or
    ``Report`` itself, never blocks, always returns 0 — modelled on
    ``cmd_vocab``'s bare ``return 0``, not on ``cmd_validate``'s pattern of
    returning the emitted report's exit code.

    Root resolution is defensive by necessity, not by style: ``find_spec``
    raises ``CheckError`` on a missing explicit ``--spec`` path, and ``main()``
    maps that to exit 2 for every other subcommand. A missing spec is a
    missing trail here, not an error, so the exception is caught and root
    falls back to ``--phase-dir`` (or cwd).
    """
    try:
        path = find_spec(args.spec, args.phase_dir)
        root = args.phase_dir or str(path.parent)
    except CheckError:
        root = args.phase_dir or "."

    records = read_all(decisions_path(root))
    not_found_message = None

    if args.invocation:
        selected = [r for r in records if r.get("invocation_id") == args.invocation]
        if not selected:
            not_found_message = f"no decision trail found for invocation {args.invocation!r}"
    else:
        last_id = None
        for record in records:
            if record.get("record_type") == "invocation":
                last_id = record.get("invocation_id")
        selected = (
            [r for r in records if r.get("invocation_id") == last_id] if last_id else []
        )

    if args.json:
        print(json.dumps(selected, indent=2, sort_keys=True))
    elif not_found_message:
        print(not_found_message)
    else:
        print(_render_decision_trail(selected))
    return 0


def _render_decision_trail(records: "list[dict]") -> str:
    """Human-readable text: the invocation header line, then one block per
    decision record. ``counterfactual`` is rendered prominently, not as a
    footnote — 'what would have to be different for me to choose otherwise'
    is the rule the record teaches, not just the instance it recorded."""
    if not records:
        return "no decision trail was found."

    lines: "list[str]" = []
    header = next((r for r in records if r.get("record_type") == "invocation"), None)
    if header:
        lines.append(
            f"invocation {header.get('invocation_id')} "
            f"(gate={header.get('gate_point')}, dsx={header.get('dsx_version')}, "
            f"frame_digest={header.get('frame_digest')})"
        )

    for record in records:
        if record.get("record_type") != "decision":
            continue
        lines.append("")
        lines.append(f"{record.get('id')} [{record.get('layer')}] {record.get('choice')}")
        if record.get("rule"):
            lines.append(f"  rule:           {record['rule']}")
        if record.get("citation"):
            lines.append(f"  citation:       {record['citation']}")
        if record.get("counterfactual"):
            lines.append(f"  counterfactual: {record['counterfactual']}")

    return "\n".join(lines) if lines else "no decision trail was found."


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


def cmd_seal(args: argparse.Namespace) -> int:
    from .checks.figures import file_sha256

    path = Path(args.path)
    if not path.exists():
        raise CheckError(f"file not found: {path}")
    digest = file_sha256(path)
    if args.json:
        print(json.dumps({"path": str(path).replace("\\", "/"), "svg_sha256": digest}, indent=2))
    else:
        print(digest)
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
    applied = report.context.get("suppressions_applied") or []
    if applied:
        lines += ["## Suppressions applied", ""]
        for row in applied:
            chart = f" (chart_id={row['chart_id']})" if row.get("chart_id") else ""
            lines += [
                f"- `{row['code']}`{chart}: {row['reason']} — authority: {row['authority']}",
            ]
        lines.append("")
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

    def add_common(
        p: argparse.ArgumentParser,
        default_block: str = "HIGH",
        *,
        include_block_on: bool = True,
    ) -> None:
        p.add_argument("--spec", help="path to ANALYSIS-SPEC (auto-discovered when omitted)")
        p.add_argument("--phase-dir", help="GSD phase directory to search and resolve paths against")
        if include_block_on:
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

    p_explain = sub.add_parser(
        "explain",
        help="render the decision trail from DECISIONS.jsonl — read-only, never blocks",
    )
    add_common(p_explain, include_block_on=False)
    p_explain.add_argument("--invocation", help="render only this invocation id's records")
    p_explain.set_defaults(func=cmd_explain)

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

    p_seal = sub.add_parser(
        "seal",
        help="compute sha256:… for a figure file to paste into visuals[].svg_sha256",
    )
    p_seal.add_argument("path", help="path to an SVG/PNG/HTML figure")
    p_seal.add_argument("--json", action="store_true")
    p_seal.set_defaults(func=cmd_seal)

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
