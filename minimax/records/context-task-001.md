# SDD Development Context: 为 Catalog.search 增加 min_year 年份下限筛选：按 Book.published_year 包含边界，并保持关键词、标签、归档选项与既有排序行为不变。

- Project: `minimax-sdd`

## Applicable specification entries

### [SPEC-002-4] `specs/SPEC-002-书目录查询.md#SPEC-002-4` (v1, score=31.4465)

年份筛选必须与关键词、标签和 `include_archived` 条件同时生效，并继续保持既有排序。

### [SPEC-002-1] `specs/SPEC-002-书目录查询.md#SPEC-002-1` (v1, score=12.3457)

`Catalog.search` 支持可选参数 `min_year: int | None = None`，用于按 `Book.published_year` 筛选。

### [SPEC-002-2] `specs/SPEC-002-书目录查询.md#SPEC-002-2` (v5, score=9.8397)

提供 `min_year` 时，只返回出版年份大于或等于 `min_year` 的书籍；等于边界时必须返回。

### [SPEC-001-2] `specs/SPEC-001-工程约束.md#SPEC-001-2` (v1, score=9.2194)

为既有公开接口增加参数时必须提供默认值，保证旧调用方式继续有效。

### [SPEC-001-4] `specs/SPEC-001-工程约束.md#SPEC-001-4` (v1, score=7.8755)

搜索结果排序必须确定：评分降序，出版年份降序，相同年份按 book_id 升序。

### [SPEC-001-3] `specs/SPEC-001-工程约束.md#SPEC-001-3` (v1, score=7.285)

搜索与筛选不得修改目录中保存的书籍、标签或统计值。

### [SPEC-002-3] `specs/SPEC-002-书目录查询.md#SPEC-002-3` (v1, score=5.0339)

未提供 `min_year` 时，搜索结果必须与加入该参数前的行为完全一致。

### [SPEC-002-5] `specs/SPEC-002-书目录查询.md#SPEC-002-5` (v1, score=4.6376)

年份筛选只作用于本次调用，不得影响后续不带筛选的搜索结果。

### [SPEC-001-1] `specs/SPEC-001-工程约束.md#SPEC-001-1` (v1, score=1.7717)

业务样例只使用 Python 标准库，不得通过外部服务实现目录搜索逻辑。

## Relevant code

### `sample-project/src/bookdesk/catalog.py` (v2, score=6.3557)
Symbols: `Catalog, __init__, add, get, all_books, search, _matches`

```python
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
```

### `sample-project/src/bookdesk/models.py` (v1, score=5.3316)
Symbols: `Book`

```python
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
```

### `sample-project/src/bookdesk/__init__.py` (v1, score=2.2505)
Symbols: ``

```python
"""Book catalog used by the SDD validation sample."""

from bookdesk.catalog import Catalog
from bookdesk.models import Book

__all__ = ["Book", "Catalog"]
```

## Verification tests

### `sample-project/tests/conftest.py` (v2, score=5.2849)
Symbols: `catalog`

```python
from __future__ import annotations

import pytest
from bookdesk.catalog import Catalog
from bookdesk.models import Book


@pytest.fixture()
def catalog() -> Catalog:
    value = Catalog()
    for book in (
        Book("B-001", "数据库系统", "Alice", 2018, 4.8, tags=("database", "classic")),
        Book("B-002", "查询优化", "Alice Chen", 2020, 4.7, tags=("database", "performance")),
        Book("B-003", "向量检索", "Bob", 2021, 4.9, tags=("database", "vector")),
        Book("B-004", "旧版检索手册", "Carol", 2017, 5.0, archived=True, tags=("database",)),
        Book("B-005", "上下文工程", "Dana", 2023, 4.7, tags=("context", "agent")),
        Book("B-006", "搜索引擎实践", "Alice", 2020, 4.2, tags=("search", "database")),
    ):
        value.add(book)
    return value
```

### `sample-project/tests/test_catalog_year_filter.py` (v2, score=4.8298)
Symbols: `test_min_year_returns_only_matching_books, test_min_year_includes_boundary, test_min_year_none_keeps_existing_results, test_min_year_combines_with_keyword_and_tags, test_min_year_combines_with_archived_option, test_min_year_above_everything_returns_empty, test_min_year_does_not_mutate_catalog`

```python
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
```

### `sample-project/tests/test_catalog_regression.py` (v1, score=3.1045)
Symbols: `test_empty_search_keeps_existing_sort, test_keyword_search_reads_title_author_and_tags, test_tag_filter_requires_every_requested_tag, test_archived_books_are_opt_in, test_get_and_duplicate_add_behaviour`

```python
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
```

## Task state (PowerContext)

- task_id: `catalog-year-filter`
- objective: 为 Catalog.search 增加 min_year 年份下限筛选并验证兼容性
- completed: ["导入规格、代码和测试资料", "运行目标及回归测试", "使用 MiniMax 修改代码"]
- pending: []
- verifications: `5`
- updated_at: `2026-11-05T02:41:55+00:00`
