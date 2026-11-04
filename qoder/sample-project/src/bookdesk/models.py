"""Catalog data model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Book:
    book_id: str
    title: str
    author: str
    published_year: int
    rating: float
    archived: bool = False
    tags: tuple[str, ...] = ()
