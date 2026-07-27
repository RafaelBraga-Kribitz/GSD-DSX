"""Figure artifact seals. Codes DSX-FIG-*.

Hermetic proof that a declared chart matches bytes on disk: path exists and
``svg_sha256`` matches a stdlib SHA-256 of the file. No Glyph/MCP dependency —
when ``renderer: glyph``, a seal is still required.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from ..findings import Report
from ..loader import SpecParseError, load
from ..spec import is_blank, items, normalize

MANIFEST_NAMES = (
    "FIGURE-MANIFEST.yaml",
    "FIGURE-MANIFEST.yml",
    "good-FIGURE-MANIFEST.yaml",
)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def check(
    spec: dict,
    phase_dir: "str | None" = None,
    *,
    strict: bool = False,
) -> Report:
    """Audit figure artifacts.

    ``strict=True`` (verify/ship) requires ``svg_sha256`` whenever ``artifact_path``
    is set. Plan/execute callers may pass strict=False.
    """
    report = Report(check="figures")
    visuals = items(spec, "visuals")
    if not visuals:
        report.ok("no visuals declared")
        return report

    roots = _resolve_roots(phase_dir)
    seen_ids: dict[str, int] = {}

    for index, visual in enumerate(visuals):
        where = f"spec.visuals[{index}]"
        label = visual.get("name") or f"visual {index}"
        chart_id = visual.get("chart_id")
        if not is_blank(chart_id):
            key = str(chart_id).strip()
            if key in seen_ids:
                report.add(
                    "DSX-FIG-030",
                    "HIGH",
                    f"Duplicate chart_id {key!r}",
                    detail=f"Also used on visuals[{seen_ids[key]}].",
                    remedy="Give each visual a unique chart_id.",
                    where=f"{where}.chart_id",
                )
            else:
                seen_ids[key] = index

        artifact = visual.get("artifact_path")
        seal = visual.get("svg_sha256")
        renderer = normalize(str(visual.get("renderer") or ""))

        if renderer == "glyph" and is_blank(seal):
            report.add(
                "DSX-FIG-020",
                "HIGH",
                f"'{label}' uses renderer glyph without svg_sha256",
                detail=(
                    "Glyph proof in dsx is a hermetic byte seal, not a live MCP call. "
                    "Seal the SVG with `dsx seal`."
                ),
                remedy="Run `dsx seal <artifact.svg>` and set visuals[].svg_sha256.",
                where=f"{where}.svg_sha256",
            )

        if is_blank(artifact):
            continue

        path = _find_file(str(artifact), roots)
        if path is None:
            report.add(
                "DSX-FIG-001",
                "HIGH",
                f"'{label}' artifact_path {artifact!r} not found",
                detail=f"Looked under: {', '.join(str(r) for r in roots)}",
                remedy="Write the figure, or fix artifact_path.",
                where=f"{where}.artifact_path",
            )
            continue

        if is_blank(seal):
            if strict:
                report.add(
                    "DSX-FIG-011",
                    "HIGH",
                    f"'{label}' has artifact_path but no svg_sha256",
                    detail="Unsealed artifacts can be swapped without the gate noticing.",
                    remedy="Run `dsx seal` on the file and paste the hash into the spec.",
                    where=f"{where}.svg_sha256",
                )
            continue

        expected = str(seal).strip()
        if not expected.startswith("sha256:"):
            expected = "sha256:" + expected
        actual = file_sha256(path)
        if actual != expected:
            report.add(
                "DSX-FIG-010",
                "CRITICAL",
                f"'{label}' svg_sha256 does not match the file on disk",
                detail=f"Declared {expected}; file hashes to {actual}.",
                remedy="Re-seal after regenerating the figure, or restore the sealed bytes.",
                where=f"{where}.svg_sha256",
            )
        else:
            report.ok(f"'{label}' seal matches {path.name}")

    _check_manifest(spec, visuals, roots, report)
    return report


def _resolve_roots(phase_dir: "str | None") -> list[Path]:
    roots: list[Path] = []
    if phase_dir:
        roots.append(Path(phase_dir))
    roots.append(Path.cwd())
    return roots


def _find_file(relative: str, roots: list[Path]) -> Path | None:
    candidate = Path(relative)
    if candidate.is_absolute() and candidate.exists():
        return candidate
    for root in roots:
        path = root / relative
        if path.exists():
            return path
    if candidate.exists():
        return candidate
    return None


def _check_manifest(
    spec: dict, visuals: list[dict], roots: list[Path], report: Report
) -> None:
    figures_cfg = spec.get("figures") if isinstance(spec.get("figures"), dict) else {}
    manifest_rel = None
    if isinstance(figures_cfg, dict):
        manifest_rel = figures_cfg.get("manifest_path")
    manifest_path = None
    if not is_blank(manifest_rel):
        manifest_path = _find_file(str(manifest_rel), roots)
    else:
        for root in roots:
            for name in MANIFEST_NAMES:
                candidate = root / name
                if candidate.exists():
                    manifest_path = candidate
                    break
            if manifest_path:
                break
    if manifest_path is None:
        return

    try:
        manifest = load(manifest_path)
    except SpecParseError as exc:
        report.add(
            "DSX-FIG-040",
            "HIGH",
            "FIGURE-MANIFEST coverage or generator path failed",
            detail=str(exc),
            remedy="Fix the YAML or regenerate the manifest.",
            where=str(manifest_path),
        )
        return

    entries = manifest.get("figures") if isinstance(manifest.get("figures"), list) else []
    entry_by_path: dict[str, dict] = {}
    entry_ids: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        path = str(entry.get("path") or "").replace("\\", "/")
        if path:
            entry_by_path[path] = entry
        cid = entry.get("chart_id")
        if not is_blank(cid):
            entry_ids.add(str(cid).strip())
        generator = entry.get("generator")
        if not is_blank(generator):
            gen_path = _find_file(str(generator), roots)
            if gen_path is None:
                report.add(
                    "DSX-FIG-040",
                    "HIGH",
                    "FIGURE-MANIFEST coverage or generator path failed",
                    detail=f"Manifest generator {generator!r} not found (chart_id={entry.get('chart_id')!r}).",
                    remedy="Commit the generator script or fix the path.",
                    where=str(manifest_path),
                )

    # Every file under figures/ must have an entry
    for root in roots:
        figures_dir = root / "figures"
        if not figures_dir.is_dir():
            continue
        for path in figures_dir.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".svg", ".png", ".html", ".pdf"}:
                continue
            rel = path.relative_to(root).as_posix()
            if rel not in entry_by_path:
                report.add(
                    "DSX-FIG-040",
                    "HIGH",
                    "FIGURE-MANIFEST coverage or generator path failed",
                    detail=f"Figure {rel} has no FIGURE-MANIFEST entry ({manifest_path}).",
                    remedy="Add a figures[] row with chart_id, path, generator.",
                    where=str(manifest_path),
                )

    visual_ids = {
        str(v.get("chart_id")).strip()
        for v in visuals
        if not is_blank(v.get("chart_id"))
    }
    orphan = entry_ids - visual_ids
    for cid in sorted(orphan):
        report.add(
            "DSX-FIG-041",
            "MEDIUM",
            f"Manifest chart_id {cid!r} not referenced by any visuals[].chart_id",
            remedy="Link the visual or remove the orphan manifest row.",
            where=str(manifest_path),
        )
