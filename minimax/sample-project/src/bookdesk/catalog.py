"""In-memory book catalog."""

from __future__ import annotations

from bookdesk.models import Book


class Catalog:
    def __init__(self) -> None:
        self._books: dict[str, Book] = {}

    def add(self, book: Book) -> None:
        if book.book_id in self._books:
            raise ValueError(f"duplicate book_id: {book.book_id}")
        self._books[book.book_id] = book

    def get(self, book_id: str) -> Book | None:
        return self._books.get(book_id)

    def all_books(self) -> tuple[Book, ...]:
        return tuple(self._books.values())

    def search(
        self,
        query: str = "",
        tags: tuple[str, ...] | None = None,
        include_archived: bool = False,
        min_year: int | None = None,
    ) -> list[Book]:
        """Search active books and return a deterministically ordered snapshot."""
        normalized_query = query.strip().casefold()
        required_tags = {tag.casefold() for tag in (tags or ())}
        result = [
            book
            for book in self._books.values()
            if (include_archived or not book.archived)
            and self._matches(book, normalized_query)
            and required_tags.issubset({tag.casefold() for tag in book.tags})
            and (min_year is None or book.published_year >= min_year)
        ]

        result.sort(key=lambda book: (-book.rating, -book.published_year, book.book_id))
        return result

    @staticmethod
    def _matches(book: Book, normalized_query: str) -> bool:
        if not normalized_query:
            return True
        haystack = " ".join((book.title, book.author, *book.tags)).casefold()
        return normalized_query in haystack
