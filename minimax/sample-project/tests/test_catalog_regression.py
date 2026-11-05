from __future__ import annotations

from bookdesk.catalog import Catalog
from bookdesk.models import Book


def test_empty_search_keeps_existing_sort(catalog: Catalog) -> None:
    assert [book.book_id for book in catalog.search()] == ["B-003", "B-001", "B-005", "B-002", "B-006"]


def test_keyword_search_reads_title_author_and_tags(catalog: Catalog) -> None:
    assert [book.book_id for book in catalog.search("alice")] == ["B-001", "B-002", "B-006"]
    assert [book.book_id for book in catalog.search("向量")] == ["B-003"]


def test_tag_filter_requires_every_requested_tag(catalog: Catalog) -> None:
    assert [book.book_id for book in catalog.search(tags=("database", "performance"))] == ["B-002"]


def test_archived_books_are_opt_in(catalog: Catalog) -> None:
    assert "B-004" not in [book.book_id for book in catalog.search()]
    assert catalog.search(include_archived=True)[0].book_id == "B-004"


def test_get_and_duplicate_add_behaviour(catalog: Catalog) -> None:
    assert catalog.get("B-001") is not None
    assert catalog.get("missing") is None
    try:
        catalog.add(Book("B-001", "duplicate", "x", 2000, 1.0))
    except ValueError as error:
        assert "duplicate" in str(error)
    else:
        raise AssertionError("duplicate book_id must be rejected")
