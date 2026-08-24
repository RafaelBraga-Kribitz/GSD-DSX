"""Decision-record schema, append-only crash-safe emitter, tolerant reader.

Top-level peer to ``dsx/findings.py`` — the second output contract this package
writes, not just reads. Stdlib only (D-01): a decision trail is worthless if the
gate that would emit it can't run because a dependency is missing.

The append contract (D-19), normative for any future writer of this file:

- **File:** ``DECISIONS.jsonl``, written beside the resolved spec (see
  ``decisions_path()``) — the same root ``dsx gate``/``dsx check`` already
  resolve for evidence and profile paths.
- **Format:** one JSON object per line (JSON Lines). Each line is
  ``json.dumps(record.to_dict(), sort_keys=True)`` followed by a single ``\\n``.
  No trailing commas, no enclosing array — the file is never parsed as a whole
  JSON document, always line by line.
- **Required fields:** every record carries a ``record_type`` of either
  ``"invocation"`` or ``"decision"`` (see ``RECORD_TYPES``). An invocation
  header (``InvocationHeader``) carries ``invocation_id``, ``gate_point``,
  ``dsx_version`` and ``frame_digest`` — the grouping anchor for one gate run's
  trail. A decision record (``DecisionRecord``) carries ``id``,
  ``invocation_id``, ``layer``, ``choice``, ``inputs``, ``rule``, ``citation``,
  ``counterfactual``, ``alternatives_rejected``, ``confidence`` and
  ``escalate`` — the ten brief-5.5 fields plus the ``invocation_id`` that ties
  it back to its header.
- **Layers:** ``layer`` is one of two values (``DECISION_LAYERS``):
  ``"deterministic"`` (a dsx check's own rule-based judgment) or
  ``"stochastic"`` (an agent's judgment call, with a confidence and a
  counterfactual). The gate emits ``layer: "deterministic"`` records only.
  A dsx agent may begin appending ``layer: "stochastic"`` entries to the same
  file with no further code change here — the schema already carries
  ``confidence`` and ``escalate`` for that case.
- **Durability:** ``append()`` writes, ``flush()``es and ``os.fsync()``s the
  file descriptor per record, so a line that finished writing survives a
  crashed run. ``read_all()`` is the other half of that guarantee, and it
  tolerates three distinct on-disk conditions, not just one: an unparseable
  line (the half-written tail of a crash), an undecodable byte (a hand-edit,
  filesystem-level corruption of an already-committed byte, or any future
  non-ASCII write), and an unreadable path (a directory, a device node, a
  revoked permission) — none of these is fatal, so one crash or one corrupted
  byte never invalidates every record written before it, and never raises
  into a caller that documents an unconditional "never blocks" contract.
- **Concurrency (WR-02):** ``next_invocation_id()`` and the caller's
  subsequent ``append()`` are a non-atomic read-then-write with no locking
  between the two steps. Concurrent ``dsx gate`` invocations against a single
  root are unsupported today — see ``next_invocation_id()``'s docstring for
  the exact collision mechanism. No lock, lock file or platform-specific
  advisory-locking import is introduced; serialising concurrent gate runs
  against one root is the operator's responsibility.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

DECISION_LAYERS = {"deterministic", "stochastic"}
RECORD_TYPES = {"invocation", "decision"}


@dataclass(frozen=True)
class DecisionRecord:
    """One decision-trail entry — brief section 5.5's schema.

    ``counterfactual`` is the field that teaches: what would have made this
    choice go the other way. Mirrors ``dsx.findings.Finding``'s frozen-dataclass
    idiom.
    """

    id: str
    invocation_id: str
    layer: str
    choice: str
    inputs: "list[str]" = field(default_factory=list)
    rule: str = ""
    citation: str = ""
    counterfactual: str = ""
    alternatives_rejected: "list[str]" = field(default_factory=list)
    confidence: "str | None" = None
    escalate: bool = False

    def to_dict(self) -> "dict[str, Any]":
        out = asdict(self)
        out["record_type"] = "decision"
        return out


@dataclass(frozen=True)
class InvocationHeader:
    """The per-invocation grouping anchor (D-16) for one gate run's trail.

    The frame digest lives here, once per invocation — not on every decision
    record — because it is a property of the invocation (which spec, at which
    content), not of any individual choice made during it.
    """

    invocation_id: str
    gate_point: str
    dsx_version: str
    frame_digest: str

    def to_dict(self) -> "dict[str, Any]":
        out = asdict(self)
        out["record_type"] = "invocation"
        return out


def append(path: "str | Path", record: "DecisionRecord | InvocationHeader") -> None:
    """Append one record. flush()+fsync() so a completed line survives a crash;
    the reader (read_all) skips an unparseable tail line rather than failing
    the file."""
    line = json.dumps(record.to_dict(), sort_keys=True)
    # newline="\n" pins the D-19 byte contract (one JSON object per line ending
    # in a single \n). Default text mode translates \n -> \r\n on Windows, and
    # Phase 10 made DECISIONS.jsonl a content-locked gate input (byte
    # comparison), so trail fidelity now has to hold byte-for-byte across
    # platforms — read_all()'s splitlines() tolerated \r\n on the read side, but
    # the write must still honour the documented single-\n contract.
    with Path(path).open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(line + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def read_all(path: "str | Path") -> "list[dict]":
    """Return every parseable record. Never raises for any on-disk state of
    ``path`` — it degrades rather than fails, and its callers (``cmd_explain``,
    the gate-path ``next_invocation_id``) depend on that unconditionally:

    - **Missing path** -> ``[]``.
    - **Unreadable path** (a directory rather than a file, a device node, a
      revoked permission) -> ``[]``, caught as ``OSError`` around the read.
    - **Undecodable bytes** in the file (not valid UTF-8) -> ``errors="replace"``
      on the decode, so the read itself cannot raise; a line degraded by
      replacement characters then either still parses as JSON or falls into
      the existing unparseable-line skip below.
    - **An unparseable line** (JSON-level truncation, e.g. the half-written
      tail of a crash, or arbitrary non-JSON content) is skipped, not fatal —
      the tolerant-reader design this docstring's module-level durability
      paragraph describes.
    """
    p = Path(path)
    if not p.exists():
        return []
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    records: "list[dict]" = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue  # tolerant reader — a half-written crash-tail line is skipped, not fatal
    return records


def next_invocation_id(path: "str | Path") -> str:
    """Deterministic, file-derived invocation identifier — never uuid, never a
    clock read, so identical input produces identical output. Named
    ``invocation_id``, not ``run_id`` (D-15): ``run_id`` is
    ``visuals[].run_id``, checked by ``DSX-SMELL-013``.

    **Concurrency limitation (WR-02):** the identifier is derived by counting
    existing invocation records; the caller appends the new header separately
    (in ``dsx/cli.py::_write_decision_trail``), and nothing serialises the two
    steps. Two ``dsx gate`` processes racing against one ``DECISIONS.jsonl``
    can both derive the same identifier here and both append a header
    carrying it, after which ``dsx explain``'s grouping — which keys purely
    on invocation-id equality — would interleave two runs' records under one
    header. Concurrent gate invocations against a single root are therefore
    unsupported; serialising them (running one ``dsx gate`` at a time against
    a given root) is the operator's responsibility today. No lock is taken
    here — see the module docstring's append-contract note.
    """
    records = read_all(path)
    n = sum(1 for r in records if r.get("record_type") == "invocation") + 1
    return f"INV-{n:04d}"


def frame_digest(spec: "dict[str, Any]") -> str:
    """Stable digest over the ``validity_frame:``/``inference:`` blocks only.
    Key-order invariant (``sort_keys=True``); unchanged by edits elsewhere in
    the spec. Change-detection, not a security control."""
    payload = json.dumps(
        {"validity_frame": spec.get("validity_frame"), "inference": spec.get("inference")},
        sort_keys=True,
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def decisions_path(root: "str | Path") -> Path:
    """``DECISIONS.jsonl`` beside the resolved spec (D-14). Does not
    re-implement ``find_spec()``'s search: the caller already has the resolved
    root (``args.phase_dir or str(path.parent)``)."""
    return Path(root) / "DECISIONS.jsonl"


def record_decision(report: Any, decision_record: "DecisionRecord") -> None:
    """Append one decision record onto ``report.context["decisions"]``.

    Phase 11.1 (REQ-P11.1-01): the shared write path for ``dsx/checks/*.py``
    modules. ``tests/test_dsx.py::test_no_check_module_appends_to_a_decisions_list``
    forbids any file under ``dsx/checks/`` from containing the literal
    ``context.setdefault("decisions", ...)``/``context["decisions"]`` idiom
    inline — that test predates this function and still passes unmodified,
    because a check module calling this helper never spells that idiom itself.
    This is not a relaxation of the boundary the test enforces; it is the one
    sanctioned indirection through it, so a check module can still participate
    in the milestone's standing per-phase decision-record deliverable (D-04)
    without duplicating ``dsx/frame/*.py``'s inline-append pattern in a
    package that test explicitly keeps free of it.

    ``dsx/frame/*.py`` modules are unaffected and keep writing inline
    (Phase 6-10 precedent) — this helper exists for callers outside that
    package; nothing here changes how ``collect_from_report`` reads the
    result back, since both paths leave the same shape under
    ``report.context[<check-name>]["decisions"]``.
    """
    report.context.setdefault("decisions", []).append(decision_record.to_dict())


def collect_from_report(report: Any) -> "list[dict]":
    """Flatten every sub-report's ``decisions`` list out of a merged
    ``Report.context`` (``merge()`` nests each sub-report's context under its
    own check name), in iteration order. Producers append plain dicts onto
    ``report.context.setdefault("decisions", [])`` before merge; this keeps
    checks pure and puts the only file write at the CLI layer."""
    out: "list[dict]" = []
    for value in report.context.values():
        if isinstance(value, dict):
            decisions = value.get("decisions")
            if isinstance(decisions, list):
                out.extend(decisions)
    return out
