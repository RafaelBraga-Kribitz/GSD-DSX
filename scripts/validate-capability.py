#!/usr/bin/env python3
"""Validate capability.json against the GSD capability contract before shipping.

GSD validates the manifest at install time; failing there means a broken install
for the user. This re-implements the conformance rules from the ADR-894 /
ADR-1016 manifest reference so the failure happens here instead.

    python3 scripts/validate-capability.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "capabilities" / "dsx" / "capability.json"

# The closed vocabulary of loop extension points (12, additive-only).
POINTS = {
    "discuss:pre", "discuss:post",
    "plan:pre", "plan:post",
    "execute:pre", "execute:wave:pre", "execute:wave:post", "execute:post",
    "verify:pre", "verify:post",
    "ship:pre", "ship:post",
}

# Agent roles published by each step, from gsd-core/bin/lib/loop-host-contract.cjs.
ROLES_BY_POINT = {
    "discuss:pre": {"orchestrator"}, "discuss:post": {"orchestrator"},
    "plan:pre": {"researcher", "planner", "checker"},
    "plan:post": {"researcher", "planner", "checker"},
    "execute:pre": {"executor", "verifier"}, "execute:wave:pre": {"executor", "verifier"},
    "execute:wave:post": {"executor", "verifier"}, "execute:post": {"executor", "verifier"},
    "verify:pre": {"orchestrator"}, "verify:post": {"orchestrator"},
    "ship:pre": {"orchestrator"}, "ship:post": {"orchestrator"},
}

RESERVED_PREFIXES = ("gsd-", "gsd-core-", "anthropic-")
TIERS = {"core", "standard", "full"}
ON_ERROR = {"skip", "halt"}
CONFIG_TYPES = {"boolean", "string", "number", "enum"}
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+")
COMMAND_MAX_LENGTH = 4096


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot read {MANIFEST}: {exc}", file=sys.stderr)
        return 1

    cap_id = manifest.get("id", "")

    # ── envelope ─────────────────────────────────────────────────────────────
    if not KEBAB.match(cap_id):
        errors.append(f"id {cap_id!r} must be kebab-case")
    if cap_id != MANIFEST.parent.name:
        errors.append(f"id {cap_id!r} must equal the folder name {MANIFEST.parent.name!r}")
    if cap_id.startswith(RESERVED_PREFIXES):
        errors.append(f"id {cap_id!r} uses a reserved prefix ({', '.join(RESERVED_PREFIXES)})")
    if manifest.get("role") != "feature":
        errors.append("role must be 'feature'")
    if not SEMVER.match(str(manifest.get("version", ""))):
        errors.append("version must be semver")
    for field in ("title", "description"):
        if not str(manifest.get(field, "")).strip():
            errors.append(f"{field} must be a non-empty string")
    if manifest.get("tier") not in TIERS:
        errors.append(f"tier must be one of {sorted(TIERS)}")
    if not isinstance(manifest.get("requires"), list):
        errors.append("requires must be present as an array")

    compat = manifest.get("runtimeCompat")
    if not isinstance(compat, dict):
        errors.append("runtimeCompat is required for a feature capability")
    else:
        supported = compat.get("supported")
        if not isinstance(supported, list) or not supported:
            errors.append("runtimeCompat.supported must be a non-empty array")
        elif "*" in supported and len(supported) > 1:
            errors.append("runtimeCompat.supported may not mix '*' with concrete ids")
        if "*" in (compat.get("unsupported") or []):
            errors.append("runtimeCompat.unsupported may not contain '*'")

    # ── owned artefacts ──────────────────────────────────────────────────────
    skills = manifest.get("skills") or []
    agents = manifest.get("agents") or []
    for name in skills + agents:
        if name.startswith(RESERVED_PREFIXES):
            errors.append(f"{name!r} uses a reserved prefix")
        if not KEBAB.match(name):
            errors.append(f"{name!r} must be kebab-case")
    if len(set(skills)) != len(skills):
        errors.append("duplicate skill stem")
    if len(set(agents)) != len(agents):
        errors.append("duplicate agent stem")

    for name in skills:
        if not (ROOT / "skills" / name / "SKILL.md").exists():
            errors.append(f"declared skill {name!r} has no skills/{name}/SKILL.md")
    for name in agents:
        path = ROOT / "agents" / f"{name}.md"
        if not path.exists():
            errors.append(f"declared agent {name!r} has no agents/{name}.md")
        else:
            head = path.read_text(encoding="utf-8").split("\n", 3)
            if not head or head[0].strip() != "---":
                errors.append(f"agents/{name}.md has no frontmatter")
            elif f"name: {name}" not in "\n".join(head[:4]):
                errors.append(f"agents/{name}.md frontmatter name does not match {name!r}")

    # Every file on disk should be declared, or it will not install.
    for path in sorted((ROOT / "agents").glob("*.md")):
        if path.stem not in agents:
            warnings.append(f"agents/{path.name} exists but is not declared in the manifest")
    for path in sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir()):
        if path.name not in skills:
            warnings.append(f"skills/{path.name}/ exists but is not declared in the manifest")

    # ── config ───────────────────────────────────────────────────────────────
    for key, schema in (manifest.get("config") or {}).items():
        if not key.startswith(f"{cap_id}."):
            warnings.append(
                f"config key {key!r} is outside the '{cap_id}.' namespace — collision risk "
                "with core or another capability"
            )
        if schema.get("type") not in CONFIG_TYPES:
            errors.append(f"config {key!r}: type must be one of {sorted(CONFIG_TYPES)}")
        if "default" not in schema:
            errors.append(f"config {key!r}: default is required")
        if not str(schema.get("description", "")).strip():
            errors.append(f"config {key!r}: description is required")
        if schema.get("type") == "enum":
            values = schema.get("values")
            if not isinstance(values, list) or not values:
                errors.append(f"config {key!r}: enum requires a non-empty values array")
            elif schema.get("default") not in values:
                errors.append(f"config {key!r}: default is not in values")
        elif schema.get("type") == "boolean" and not isinstance(schema.get("default"), bool):
            errors.append(f"config {key!r}: default must be a boolean")

    config_keys = set(manifest.get("config") or {})

    def check_when(when: str | None, where: str) -> None:
        if when and when not in config_keys:
            errors.append(f"{where}: when={when!r} is not a config key this capability owns")

    # ── steps ────────────────────────────────────────────────────────────────
    produced_per_point: dict[str, set[str]] = {}
    for index, step in enumerate(manifest.get("steps") or []):
        where = f"steps[{index}]"
        point = step.get("point")
        if point not in POINTS:
            errors.append(f"{where}: point {point!r} is not one of the 12 loop extension points")
        ref = step.get("ref")
        if not isinstance(ref, dict) or len(ref) != 1:
            errors.append(f"{where}: ref must be exactly one of skill | agent | command")
        else:
            kind, name = next(iter(ref.items()))
            if kind == "skill" and name not in skills:
                errors.append(f"{where}: ref.skill {name!r} is not declared in skills")
            if kind == "agent" and name not in agents:
                errors.append(f"{where}: ref.agent {name!r} is not declared in agents")
            if kind not in ("skill", "agent", "command"):
                errors.append(f"{where}: ref kind {kind!r} is invalid")
        for field in ("produces", "consumes"):
            if not isinstance(step.get(field), list):
                errors.append(f"{where}: {field} must be present as an array")
        if step.get("onError") not in ON_ERROR:
            errors.append(f"{where}: onError must be 'skip' or 'halt'")
        check_when(step.get("when"), where)
        _check_fragment(step.get("fragment"), where, errors)

        bucket = produced_per_point.setdefault(point or "?", set())
        for artefact in step.get("produces") or []:
            if artefact in bucket:
                errors.append(f"{where}: {artefact!r} is produced twice at {point}")
            bucket.add(artefact)

    # ── contributions ────────────────────────────────────────────────────────
    for index, contribution in enumerate(manifest.get("contributions") or []):
        where = f"contributions[{index}]"
        point = contribution.get("point")
        if point not in POINTS:
            errors.append(f"{where}: point {point!r} is invalid")
        else:
            role = contribution.get("into")
            allowed = ROLES_BY_POINT[point]
            if role not in allowed:
                errors.append(
                    f"{where}: into={role!r} is not published at {point} (allowed: {sorted(allowed)})"
                )
        for field in ("produces", "consumes"):
            if not isinstance(contribution.get(field), list):
                errors.append(f"{where}: {field} must be present as an array")
        if not isinstance(contribution.get("fragment"), dict):
            errors.append(f"{where}: fragment is required")
        _check_fragment(contribution.get("fragment"), where, errors)
        check_when(contribution.get("when"), where)
        if contribution.get("onError") not in ON_ERROR | {None}:
            errors.append(f"{where}: onError must be 'skip' or 'halt'")

    # ── gates ────────────────────────────────────────────────────────────────
    for index, gate in enumerate(manifest.get("gates") or []):
        where = f"gates[{index}]"
        if gate.get("point") not in POINTS:
            errors.append(f"{where}: point {gate.get('point')!r} is invalid")
        check = gate.get("check")
        if not isinstance(check, dict):
            errors.append(f"{where}: check must be an object")
        else:
            shapes = [k for k in ("query", "predicate", "agentVerdict") if k in check]
            if len(shapes) != 1:
                errors.append(f"{where}: check must carry exactly one of query|predicate|agentVerdict")
            elif shapes[0] == "predicate":
                predicate = check["predicate"]
                if predicate.get("kind") != "command-exit-zero":
                    errors.append(f"{where}: unknown predicate kind {predicate.get('kind')!r}")
                command = predicate.get("command", "")
                if not isinstance(command, str) or not command.strip():
                    errors.append(f"{where}: predicate.command must be a non-empty string")
                elif len(command) > COMMAND_MAX_LENGTH:
                    errors.append(f"{where}: predicate.command exceeds {COMMAND_MAX_LENGTH} chars")
                else:
                    for placeholder in re.findall(r"\$\{([A-Z_]+)\}", command):
                        if placeholder not in ("PHASE_NUMBER", "PHASE_DIR", "PHASE_REQ_IDS"):
                            warnings.append(
                                f"{where}: ${{{placeholder}}} is not a GSD gate placeholder — "
                                "it will be left for sh to expand"
                            )
                timeout = predicate.get("timeout")
                if timeout is not None and (
                    not isinstance(timeout, (int, float)) or timeout <= 0
                ):
                    errors.append(f"{where}: predicate.timeout must be a positive number")
            elif shapes[0] == "agentVerdict" and gate.get("blocking"):
                errors.append(f"{where}: agentVerdict gates may not be blocking")
        if not isinstance(gate.get("blocking"), bool):
            errors.append(f"{where}: blocking must be present and boolean")
        if gate.get("onError") not in ON_ERROR:
            errors.append(f"{where}: onError must be 'skip' or 'halt'")
        check_when(gate.get("when"), where)

    # ── report ───────────────────────────────────────────────────────────────
    for warning in warnings:
        print(f"warn: {warning}")
    if errors:
        print(f"\nFAIL: {len(errors)} conformance error(s)", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(
        f"capability '{cap_id}' v{manifest['version']} is conformant: "
        f"{len(manifest.get('steps') or [])} steps, "
        f"{len(manifest.get('contributions') or [])} contributions, "
        f"{len(manifest.get('gates') or [])} gates, "
        f"{len(skills)} skills, {len(agents)} agents, {len(config_keys)} config keys"
    )
    return 0


def _check_fragment(fragment, where: str, errors: list[str]) -> None:
    if fragment is None:
        return
    if not isinstance(fragment, dict) or len(fragment) != 1:
        errors.append(f"{where}: fragment must be exactly one of path | inline")
        return
    if "path" in fragment:
        rel = fragment["path"]
        if ".." in Path(rel).parts:
            errors.append(f"{where}: fragment path {rel!r} escapes the capability directory")
        elif not (MANIFEST.parent / rel).exists():
            errors.append(f"{where}: fragment path {rel!r} does not exist")
    elif "inline" not in fragment:
        errors.append(f"{where}: fragment must carry path or inline")


if __name__ == "__main__":
    sys.exit(main())
