"""Helpers for relative-% claims that need an absolute base."""

from __future__ import annotations

import re

# Relative percent: "40%", "up 12%", "increased by 3.5%" — not "pp" / "percentage points".
_REL_PCT_RE = re.compile(
    r"(?i)(?:\b(?:up|down|increase(?:d|s)?|decrease(?:d|s)?|grew|dropped|rose|fell"
    r"|by|of)\b[^\n.]{0,24})?\b(\d+(?:\.\d+)?)\s*%(?!\s*(?:ci|confidence|interval|pp|"
    r"percentage\s*points))"
)

_BASE_NEAR_RE = re.compile(
    r"(?i)(?:\bfrom\s+\d|\bn\s*=|\bof\s+[\d,]+\s+(?:users?|customers?|rows?|signups?|"
    r"accounts?|people|patients?|observations?)|\bbase(?:_?\s*n)?\s*[=:]|"
    r"\bdenominator\b|\bout of\s+[\d,]|\b[\d,]+\s+(?:users?|customers?|signups?)\b)"
)


def has_relative_percent(text: str) -> bool:
    """True when text contains a relative % that is not a CI level or coverage share."""
    if not text:
        return False
    for match in _REL_PCT_RE.finditer(text):
        value = match.group(1)
        start, end = match.span()
        window = text[max(0, start - 28) : min(len(text), end + 28)].lower()
        if value in {"80", "90", "95", "99"} and (
            "ci" in window or "confidence" in window or "interval" in window
        ):
            continue
        if "percentage point" in window or re.search(r"\bpp\b", window):
            continue
        # "to 100%" / "at 50%" as allocation targets are not relative lifts.
        if re.search(r"(?i)\b(to|at|of)\s+" + re.escape(value) + r"\s*%", window):
            if not re.search(
                r"(?i)\b(up|down|increase|decrease|grew|dropped|rose|fell|lift|gain)\b",
                window,
            ):
                continue
        return True
    return False


def has_nearby_base_language(text: str) -> bool:
    return bool(text and _BASE_NEAR_RE.search(text))


def claim_supplies_base(claim: dict | None) -> bool:
    if not claim:
        return False
    if claim.get("base_n") is not None and claim.get("base_n") != "":
        return True
    if claim.get("from_value") is not None and claim.get("to_value") is not None:
        return True
    return False


def relative_percent_without_base(text: str, claim: dict | None = None) -> bool:
    """True when a relative % appears without base language or claim base fields."""
    if not has_relative_percent(text):
        return False
    if claim_supplies_base(claim):
        return False
    if has_nearby_base_language(text):
        return False
    return True


def normalize_ws(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())
