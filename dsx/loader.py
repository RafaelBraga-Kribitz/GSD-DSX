"""Spec loading — JSON natively, YAML via PyYAML when present, else a bundled parser.

A blocking gate must never fail because of a missing dependency. If PyYAML is
installed we use it; otherwise we fall back to a parser covering the subset the
ANALYSIS-SPEC template uses: nested mappings, sequences of scalars or mappings,
quoted and bare scalars, ``|`` and ``>`` block scalars, comments, ``null``/``~``.

Anything outside that subset raises a clear SpecParseError naming the line, which
the CLI maps to exit 2 (gate error) rather than exit 1 (gate block) — a spec we
cannot read is not the same thing as a spec we judged bad.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

try:  # pragma: no cover - environment dependent
    import yaml as _pyyaml
except Exception:  # pragma: no cover
    _pyyaml = None


class SpecParseError(ValueError):
    """The spec file could not be parsed."""


_TRUE = {"true", "yes", "on"}
_FALSE = {"false", "no", "off"}
_NULL = {"", "null", "~"}  # matches PyYAML/YAML 1.1 null semantics; "none" is a legitimate string
_NUM_RE = re.compile(r"^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$")


def load(path: "str | Path") -> dict[str, Any]:
    """Load a spec file. Returns a mapping; raises SpecParseError otherwise."""
    p = Path(path)
    if not p.exists():
        raise SpecParseError(f"spec file not found: {p}")
    text = p.read_text(encoding="utf-8")
    data = loads(text, suffix=p.suffix.lower(), origin=str(p))
    if not isinstance(data, dict):
        raise SpecParseError(f"{p}: top level must be a mapping, got {type(data).__name__}")
    return data


def loads(text: str, suffix: str = ".yaml", origin: str = "<string>") -> Any:
    if suffix == ".json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise SpecParseError(f"{origin}: invalid JSON — {exc}") from exc

    stripped = text.lstrip()
    if stripped.startswith("{"):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass  # fall through to the YAML path

    if _pyyaml is not None:
        try:
            return _pyyaml.safe_load(text)
        except Exception as exc:  # pragma: no cover - depends on PyYAML internals
            raise SpecParseError(f"{origin}: invalid YAML — {exc}") from exc

    return _parse_yaml_subset(text, origin)


# ── Bundled YAML-subset parser ───────────────────────────────────────────────


class _Line:
    __slots__ = ("indent", "content", "number")

    def __init__(self, indent: int, content: str, number: int) -> None:
        self.indent = indent
        self.content = content
        self.number = number


def _tokenize(text: str) -> list[_Line]:
    lines: list[_Line] = []
    for number, raw in enumerate(text.splitlines(), start=1):
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise SpecParseError(f"line {number}: tabs are not valid YAML indentation")
        without_comment = _strip_comment(raw)
        if not without_comment.strip():
            continue
        indent = len(without_comment) - len(without_comment.lstrip(" "))
        lines.append(_Line(indent, without_comment.strip(), number))
    return lines


def _strip_comment(raw: str) -> str:
    out: list[str] = []
    quote: str | None = None
    i = 0
    while i < len(raw):
        ch = raw[i]
        if quote:
            if ch == "\\" and i + 1 < len(raw):
                out.append(ch)
                out.append(raw[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = None
            out.append(ch)
        elif ch in ("'", '"'):
            quote = ch
            out.append(ch)
        elif ch == "#" and (i == 0 or raw[i - 1] in " \t"):
            break
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def _parse_yaml_subset(text: str, origin: str) -> Any:
    lines = _tokenize(text)
    if not lines:
        return {}
    value, index = _parse_block(lines, 0, lines[0].indent, origin)
    if index != len(lines):
        raise SpecParseError(
            f"{origin}: line {lines[index].number}: unexpected indentation "
            f"{lines[index].indent} — check that nested keys align"
        )
    return value


def _parse_block(lines: list[_Line], i: int, indent: int, origin: str) -> tuple[Any, int]:
    if lines[i].content.startswith("- "):
        return _parse_sequence(lines, i, indent, origin)
    if lines[i].content == "-":
        return _parse_sequence(lines, i, indent, origin)
    return _parse_mapping(lines, i, indent, origin)


def _parse_mapping(lines: list[_Line], i: int, indent: int, origin: str) -> tuple[dict, int]:
    result: dict[str, Any] = {}
    while i < len(lines) and lines[i].indent == indent:
        line = lines[i]
        if line.content.startswith("- "):
            break
        key, sep, rest = _split_key(line.content)
        if not sep:
            raise SpecParseError(
                f"{origin}: line {line.number}: expected 'key: value', got {line.content!r}"
            )
        if key in result:
            raise SpecParseError(f"{origin}: line {line.number}: duplicate key {key!r}")
        rest = rest.strip()
        i += 1

        if rest in ("|", "|-", ">", ">-"):
            block, i = _parse_block_scalar(lines, i, indent, rest)
            result[key] = block
            continue
        if rest:
            result[key] = _scalar(rest, line.number, origin)
            continue
        if i < len(lines) and lines[i].indent > indent:
            child, i = _parse_block(lines, i, lines[i].indent, origin)
            result[key] = child
        elif i < len(lines) and lines[i].indent == indent and lines[i].content.startswith("- "):
            child, i = _parse_sequence(lines, i, indent, origin)
            result[key] = child
        else:
            result[key] = None
    return result, i


def _parse_sequence(lines: list[_Line], i: int, indent: int, origin: str) -> tuple[list, int]:
    result: list[Any] = []
    while i < len(lines) and lines[i].indent == indent and lines[i].content.startswith("-"):
        line = lines[i]
        item = line.content[1:].strip()
        i += 1

        if not item:
            if i < len(lines) and lines[i].indent > indent:
                child, i = _parse_block(lines, i, lines[i].indent, origin)
                result.append(child)
            else:
                result.append(None)
            continue

        key, sep, rest = _split_key(item)
        if sep:
            # Inline first key of a mapping item; subsequent keys are indented
            # to the column where the key started.
            inner_indent = indent + (len(line.content) - len(line.content[1:].lstrip()))
            mapping: dict[str, Any] = {}
            rest = rest.strip()
            if rest in ("|", "|-", ">", ">-"):
                block, i = _parse_block_scalar(lines, i, inner_indent, rest)
                mapping[key] = block
            elif rest:
                mapping[key] = _scalar(rest, line.number, origin)
            elif i < len(lines) and lines[i].indent > inner_indent:
                child, i = _parse_block(lines, i, lines[i].indent, origin)
                mapping[key] = child
            else:
                mapping[key] = None
            if i < len(lines) and lines[i].indent == inner_indent:
                more, i = _parse_mapping(lines, i, inner_indent, origin)
                for k, v in more.items():
                    if k in mapping:
                        raise SpecParseError(f"{origin}: duplicate key {k!r} in sequence item")
                    mapping[k] = v
            result.append(mapping)
        else:
            result.append(_scalar(item, line.number, origin))
    return result, i


def _parse_block_scalar(
    lines: list[_Line], i: int, indent: int, marker: str
) -> tuple[str, int]:
    parts: list[str] = []
    while i < len(lines) and lines[i].indent > indent:
        parts.append(lines[i].content)
        i += 1
    joiner = "\n" if marker.startswith("|") else " "
    text = joiner.join(parts)
    # Chomping: the bare markers "|" and ">" clip to a single trailing newline;
    # the "-" variants strip it. Matches PyYAML so the two paths agree.
    if text and not marker.endswith("-"):
        text += "\n"
    return text, i


def _split_key(content: str) -> tuple[str, bool, str]:
    quote: str | None = None
    for idx, ch in enumerate(content):
        if quote:
            if ch == quote:
                quote = None
            continue
        if ch in ("'", '"'):
            quote = ch
            continue
        if ch == ":" and (idx + 1 == len(content) or content[idx + 1] in " "):
            return _unquote(content[:idx].strip()), True, content[idx + 1 :]
    return content, False, ""


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        inner = value[1:-1]
        return inner.replace('\\"', '"').replace("\\'", "'") if value[0] == '"' else inner
    return value


def _scalar(raw: str, line_number: int, origin: str) -> Any:
    text = raw.strip()

    if text.startswith("[") and text.endswith("]"):
        body = text[1:-1].strip()
        if not body:
            return []
        return [_scalar(part, line_number, origin) for part in _split_flow(body)]
    if text.startswith("{") and text.endswith("}"):
        body = text[1:-1].strip()
        if not body:
            return {}
        out: dict[str, Any] = {}
        for part in _split_flow(body):
            key, sep, rest = _split_key(part)
            if not sep:
                raise SpecParseError(
                    f"{origin}: line {line_number}: expected 'key: value' inside {{...}}"
                )
            out[key] = _scalar(rest, line_number, origin)
        return out

    if len(text) >= 2 and text[0] == text[-1] and text[0] in ("'", '"'):
        return _unquote(text)

    lowered = text.lower()
    if lowered in _NULL:
        return None
    if lowered in _TRUE:
        return True
    if lowered in _FALSE:
        return False
    if _NUM_RE.match(text):
        if any(c in text for c in ".eE"):
            return float(text)
        return int(text)
    return text


def _split_flow(body: str) -> list[str]:
    parts: list[str] = []
    depth = 0
    quote: str | None = None
    current: list[str] = []
    for ch in body:
        if quote:
            current.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in ("'", '"'):
            quote = ch
            current.append(ch)
            continue
        if ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
            continue
        current.append(ch)
    tail = "".join(current).strip()
    if tail:
        parts.append(tail)
    return parts
