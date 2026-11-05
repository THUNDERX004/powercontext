"""Target tests for SPEC-002. These fail before the model's code change."""

from __future__ import annotations

from bookdesk.catalog import Catalog


def test_min_year_returns_only_matching_books(catalog: Catalog) -> None:
    assert [book.book_id for book in catalog.search(min_year=2021)] == ["B-003", "B-005"]


def test_min_year_includes_boundary(catalog: Catalog) -> None:
    assert [book.book_id for book in catalog.search(min_year=2020)] == ["B-003", "B-005", "B-002", "B-006"]


def test_min_year_none_keeps_existing_results(catalog: Catalog) -> None:
    before = [book.book_id for book in catalog.search()]
    after = [book.book_id for book in catalog.search(min_year=None)]
    assert after == before


def test_min_year_combines_with_keyword_and_tags(catalog: Catalog) -> None:
    assert [
        book.book_id
        for book in catalog.search("database", tags=("database", "vector"), min_year=2020)
    ] == ["B-003"]
    assert [book.book_id for book in catalog.search("alice", min_year=2021)] == []


def test_min_year_combines_with_archived_option(catalog: Catalog) -> None:
    first = next(book.book_id for book in catalog.search(min_year=2017, include_archived=True))
    assert first == "B-004"
    assert "B-004" not in [book.book_id for book in catalog.search(min_year=2017)]


def test_min_year_above_everything_returns_empty(catalog: Catalog) -> None:
    assert catalog.search(min_year=9999) == []


def test_min_year_does_not_mutate_catalog(catalog: Catalog) -> None:
    catalog.search(min_year=2021)
    assert [book.book_id for book in catalog.search()] == ["B-003", "B-001", "B-005", "B-002", "B-006"]
