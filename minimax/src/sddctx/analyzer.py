"""Deterministic token preparation for seekdb's SPACE full-text parser."""

from __future__ import annotations

import re

_IDENTIFIER_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_CJK_PATTERN = re.compile(r"[\u3400-\u9fff]+")

_STOPWORDS = {
    "a",
    "an",
    "and",
    "for",
    "in",
    "of",
    "on",
    "the",
    "to",
    "with",
    "请",
    "为",
    "在",
    "的",
    "和",
    "与",
}


def _ascii_terms(text: str) -> list[str]:
    terms: list[str] = []
    for raw in _IDENTIFIER_PATTERN.findall(text):
        token = raw.lower()
        if len(token) < 2 or token in _STOPWORDS:
            continue
        terms.append(token)
        pieces = [
            part.lower()
            for part in re.split(r"_|(?<=[a-z])(?=[A-Z])", raw)
            if len(part) >= 2 and part.lower() not in _STOPWORDS
        ]
        if len(pieces) > 1:
            terms.extend(pieces)
    return terms


def _cjk_terms(text: str) -> list[str]:
    terms: list[str] = []
    for run in _CJK_PATTERN.findall(text):
        compact = "".join(char for char in run if char not in _STOPWORDS)
        terms.extend(f"u_{char}" for char in compact)
        terms.extend(f"b_{compact[index:index + 2]}" for index in range(len(compact) - 1))
    return terms


def analyze_text(text: str) -> str:
    """Return a space-delimited, duplicate-free lexical representation."""
    terms = _ascii_terms(text) + _cjk_terms(text)
    return " ".join(dict.fromkeys(terms))


def query_terms(task: str) -> list[str]:
    return analyze_text(task).split()


def extract_identifiers(text: str) -> list[str]:
    return list(
        dict.fromkeys(
            token
            for token in _IDENTIFIER_PATTERN.findall(text)
            if len(token) >= 3 and token.lower() not in _STOPWORDS
        )
    )
