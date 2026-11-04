# SPEC-002 书目录查询

- 编号: SPEC-002
- 状态: 有效
- 适用模块: bookdesk.catalog.Catalog.search

## 条目

- SPEC-002-1: `Catalog.search` 支持可选参数 `min_year: int | None = None`，用于按 `Book.published_year` 筛选。
- SPEC-002-2: 提供 `min_year` 时，只返回出版年份大于或等于 `min_year` 的书籍；等于边界时必须返回。
- SPEC-002-3: 未提供 `min_year` 时，搜索结果必须与加入该参数前的行为完全一致。
- SPEC-002-4: 年份筛选必须与关键词、标签和 `include_archived` 条件同时生效，并继续保持既有排序。
- SPEC-002-5: 年份筛选只作用于本次调用，不得影响后续不带筛选的搜索结果。
