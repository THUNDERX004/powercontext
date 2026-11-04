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
