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
  crashed run. ``read_all()`` is the other half of that guarantee: an
  unparseable trailing line (the half-written tail of a crash) is skipped, not
  fatal, so one crash never invalidates every record written before it.
"""

from __future__ import annotations

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
    with Path(path).open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def read_all(path: "str | Path") -> "list[dict]":
    """Return every parseable record. Missing file -> []. A truncated or
    otherwise unparseable line is skipped, not fatal (tolerant reader)."""
    p = Path(path)
    if not p.exists():
        return []
    records: "list[dict]" = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue  # tolerant reader — a half-written crash-tail line is skipped, not fatal
    return records
