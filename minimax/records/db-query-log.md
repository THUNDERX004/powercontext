# seekdb 查询记录

由 `sddctx` 自动追加。参数中的资产正文只记录长度，不写入日志。

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`133.227 ms`

## initialize:create-fulltext-index

```sql
CREATE FULLTEXT INDEX ft_engineering_assets_search
```

- 参数：`{"table": "engineering_assets"}`
- 返回行数：`0`
- 耗时：`693.626 ms`

## import:inserted:specs/SPEC-001-工程约束.md

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec:specs/SPEC-001-工程约束.md", "path": "specs/SPEC-001-工程约束.md", "version": 1, "content_chars": 260}`
- 返回行数：`1`
- 耗时：`8.709 ms`

## import:inserted:specs/SPEC-001-工程约束.md#SPEC-001-1

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec-entry:specs/SPEC-001-工程约束.md#SPEC-001-1", "path": "specs/SPEC-001-工程约束.md#SPEC-001-1", "version": 1, "content_chars": 36}`
- 返回行数：`1`
- 耗时：`1.014 ms`

## import:inserted:specs/SPEC-001-工程约束.md#SPEC-001-2

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec-entry:specs/SPEC-001-工程约束.md#SPEC-001-2", "path": "specs/SPEC-001-工程约束.md#SPEC-001-2", "version": 1, "content_chars": 32}`
- 返回行数：`1`
- 耗时：`1.324 ms`

## import:inserted:specs/SPEC-001-工程约束.md#SPEC-001-3

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec-entry:specs/SPEC-001-工程约束.md#SPEC-001-3", "path": "specs/SPEC-001-工程约束.md#SPEC-001-3", "version": 1, "content_chars": 25}`
- 返回行数：`1`
- 耗时：`1.433 ms`

## import:inserted:specs/SPEC-001-工程约束.md#SPEC-001-4

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec-entry:specs/SPEC-001-工程约束.md#SPEC-001-4", "path": "specs/SPEC-001-工程约束.md#SPEC-001-4", "version": 1, "content_chars": 40}`
- 返回行数：`1`
- 耗时：`1.072 ms`

## import:inserted:specs/SPEC-002-书目录查询.md

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec:specs/SPEC-002-书目录查询.md", "path": "specs/SPEC-002-书目录查询.md", "version": 1, "content_chars": 421}`
- 返回行数：`1`
- 耗时：`2.017 ms`

## import:inserted:specs/SPEC-002-书目录查询.md#SPEC-002-1

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec-entry:specs/SPEC-002-书目录查询.md#SPEC-002-1", "path": "specs/SPEC-002-书目录查询.md#SPEC-002-1", "version": 1, "content_chars": 83}`
- 返回行数：`1`
- 耗时：`1.157 ms`

## import:inserted:specs/SPEC-002-书目录查询.md#SPEC-002-2

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec-entry:specs/SPEC-002-书目录查询.md#SPEC-002-2", "path": "specs/SPEC-002-书目录查询.md#SPEC-002-2", "version": 1, "content_chars": 54}`
- 返回行数：`1`
- 耗时：`0.931 ms`

## import:inserted:specs/SPEC-002-书目录查询.md#SPEC-002-3

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec-entry:specs/SPEC-002-书目录查询.md#SPEC-002-3", "path": "specs/SPEC-002-书目录查询.md#SPEC-002-3", "version": 1, "content_chars": 38}`
- 返回行数：`1`
- 耗时：`0.99 ms`

## import:inserted:specs/SPEC-002-书目录查询.md#SPEC-002-4

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec-entry:specs/SPEC-002-书目录查询.md#SPEC-002-4", "path": "specs/SPEC-002-书目录查询.md#SPEC-002-4", "version": 1, "content_chars": 51}`
- 返回行数：`1`
- 耗时：`1.364 ms`

## import:inserted:specs/SPEC-002-书目录查询.md#SPEC-002-5

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec-entry:specs/SPEC-002-书目录查询.md#SPEC-002-5", "path": "specs/SPEC-002-书目录查询.md#SPEC-002-5", "version": 1, "content_chars": 29}`
- 返回行数：`1`
- 耗时：`1.415 ms`

## import:inserted:sample-project/src/bookdesk/__init__.py

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "code:sample-project/src/bookdesk/__init__.py", "path": "sample-project/src/bookdesk/__init__.py", "version": 1, "content_chars": 157}`
- 返回行数：`1`
- 耗时：`0.779 ms`

## import:inserted:sample-project/src/bookdesk/catalog.py

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "code:sample-project/src/bookdesk/catalog.py", "path": "sample-project/src/bookdesk/catalog.py", "version": 1, "content_chars": 1781}`
- 返回行数：`1`
- 耗时：`1.311 ms`

## import:inserted:sample-project/src/bookdesk/models.py

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "code:sample-project/src/bookdesk/models.py", "path": "sample-project/src/bookdesk/models.py", "version": 1, "content_chars": 284}`
- 返回行数：`1`
- 耗时：`0.814 ms`

## import:inserted:sample-project/tests/conftest.py

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "test:sample-project/tests/conftest.py", "path": "sample-project/tests/conftest.py", "version": 1, "content_chars": 754}`
- 返回行数：`1`
- 耗时：`1.554 ms`

## import:inserted:sample-project/tests/test_catalog_regression.py

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "test:sample-project/tests/test_catalog_regression.py", "path": "sample-project/tests/test_catalog_regression.py", "version": 1, "content_chars": 1290}`
- 返回行数：`1`
- 耗时：`1.34 ms`

## import:inserted:sample-project/tests/test_catalog_year_filter.py

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "test:sample-project/tests/test_catalog_year_filter.py", "path": "sample-project/tests/test_catalog_year_filter.py", "version": 1, "content_chars": 1621}`
- 返回行数：`1`
- 耗时：`1.293 ms`

## context:spec

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["spec_entry"], "limit": 30}`
- 返回行数：`9`
- 耗时：`19.932 ms`

## context:code

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["code"], "limit": 18}`
- 返回行数：`3`
- 耗时：`21.866 ms`

## context:test

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["test"], "limit": 18}`
- 返回行数：`3`
- 耗时：`3.904 ms`

## context:spec

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 u_并 u_验 u_证 u_兼 u_容 u_性 b_年份 b_份下 b_下限 b_限筛 b_筛选 b_选并 b_并验 b_验证 b_证兼 b_兼容 b_容性", "project_key": "minimax-sdd", "kinds": ["spec_entry"], "limit": 30}`
- 返回行数：`8`
- 耗时：`26.077 ms`

## context:code

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 u_并 u_验 u_证 u_兼 u_容 u_性 b_年份 b_份下 b_下限 b_限筛 b_筛选 b_选并 b_并验 b_验证 b_证兼 b_兼容 b_容性", "project_key": "minimax-sdd", "kinds": ["code"], "limit": 18}`
- 返回行数：`3`
- 耗时：`2.702 ms`

## context:test

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 u_并 u_验 u_证 u_兼 u_容 u_性 b_年份 b_份下 b_下限 b_限筛 b_筛选 b_选并 b_并验 b_验证 b_证兼 b_兼容 b_容性", "project_key": "minimax-sdd", "kinds": ["test"], "limit": 18}`
- 返回行数：`3`
- 耗时：`25.869 ms`

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`10.282 ms`

## import:inserted:sample-project/src/integration.py

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "test:seekdb-integration", "asset_id": "test:integration.py", "path": "sample-project/src/integration.py", "version": 1, "content_chars": 63}`
- 返回行数：`1`
- 耗时：`4.29 ms`

## integration:search

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "min_year min year", "project_key": "test:seekdb-integration", "kinds": ["code"], "limit": 5}`
- 返回行数：`1`
- 耗时：`18.531 ms`

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`7.682 ms`

## import:updated:specs/SPEC-002-书目录查询.md

```sql
UPDATE engineering_assets SET content_hash, version=version+1
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec:specs/SPEC-002-书目录查询.md", "path": "specs/SPEC-002-书目录查询.md", "version": 2, "content_chars": 471}`
- 返回行数：`1`
- 耗时：`10.72 ms`

## import:inserted:specs/SPEC-002-书目录查询.md#SPEC-002-6

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec-entry:specs/SPEC-002-书目录查询.md#SPEC-002-6", "path": "specs/SPEC-002-书目录查询.md#SPEC-002-6", "version": 1, "content_chars": 36}`
- 返回行数：`1`
- 耗时：`2.819 ms`

## context:spec

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_验 u_证 u_更 u_新 u_后 u_规 u_格 u_内 u_容 u_被 u_重 u_读 u_取 b_验证 b_证更 b_更新 b_新后 b_后规 b_规格 b_格内 b_内容 b_容被 b_被重 b_重新 b_新读 b_读取", "project_key": "minimax-sdd", "kinds": ["spec_entry"], "limit": 30}`
- 返回行数：`9`
- 耗时：`17.229 ms`

## context:code

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_验 u_证 u_更 u_新 u_后 u_规 u_格 u_内 u_容 u_被 u_重 u_读 u_取 b_验证 b_证更 b_更新 b_新后 b_后规 b_规格 b_格内 b_内容 b_容被 b_被重 b_重新 b_新读 b_读取", "project_key": "minimax-sdd", "kinds": ["code"], "limit": 18}`
- 返回行数：`3`
- 耗时：`12.599 ms`

## context:test

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_验 u_证 u_更 u_新 u_后 u_规 u_格 u_内 u_容 u_被 u_重 u_读 u_取 b_验证 b_证更 b_更新 b_新后 b_后规 b_规格 b_格内 b_内容 b_容被 b_被重 b_重新 b_新读 b_读取", "project_key": "minimax-sdd", "kinds": ["test"], "limit": 18}`
- 返回行数：`3`
- 耗时：`2.695 ms`

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`1.57 ms`

## import:updated:specs/SPEC-002-书目录查询.md

```sql
UPDATE engineering_assets SET content_hash, version=version+1
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec:specs/SPEC-002-书目录查询.md", "path": "specs/SPEC-002-书目录查询.md", "version": 3, "content_chars": 421}`
- 返回行数：`1`
- 耗时：`6.606 ms`

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`9.527 ms`

## import:updated:specs/SPEC-002-书目录查询.md

```sql
UPDATE engineering_assets SET content_hash, version=version+1
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec:specs/SPEC-002-书目录查询.md", "path": "specs/SPEC-002-书目录查询.md", "version": 4, "content_chars": 454}`
- 返回行数：`1`
- 耗时：`11.692 ms`

## import:updated:specs/SPEC-002-书目录查询.md#SPEC-002-2

```sql
UPDATE engineering_assets SET content_hash, version=version+1
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec-entry:specs/SPEC-002-书目录查询.md#SPEC-002-2", "path": "specs/SPEC-002-书目录查询.md#SPEC-002-2", "version": 2, "content_chars": 87}`
- 返回行数：`1`
- 耗时：`4.362 ms`

## context:spec

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_验 u_证 u_更 u_新 u_后 u_规 u_格 u_内 u_容 u_被 u_重 u_读 u_取 b_验证 b_证更 b_更新 b_新后 b_后规 b_规格 b_格内 b_内容 b_容被 b_被重 b_重新 b_新读 b_读取", "project_key": "minimax-sdd", "kinds": ["spec_entry"], "limit": 30}`
- 返回行数：`8`
- 耗时：`5.924 ms`

## context:code

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_验 u_证 u_更 u_新 u_后 u_规 u_格 u_内 u_容 u_被 u_重 u_读 u_取 b_验证 b_证更 b_更新 b_新后 b_后规 b_规格 b_格内 b_内容 b_容被 b_被重 b_重新 b_新读 b_读取", "project_key": "minimax-sdd", "kinds": ["code"], "limit": 18}`
- 返回行数：`3`
- 耗时：`3.835 ms`

## context:test

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_验 u_证 u_更 u_新 u_后 u_规 u_格 u_内 u_容 u_被 u_重 u_读 u_取 b_验证 b_证更 b_更新 b_新后 b_后规 b_规格 b_格内 b_内容 b_容被 b_被重 b_重新 b_新读 b_读取", "project_key": "minimax-sdd", "kinds": ["test"], "limit": 18}`
- 返回行数：`3`
- 耗时：`3.69 ms`

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`1.958 ms`

## import:updated:specs/SPEC-002-书目录查询.md

```sql
UPDATE engineering_assets SET content_hash, version=version+1
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec:specs/SPEC-002-书目录查询.md", "path": "specs/SPEC-002-书目录查询.md", "version": 5, "content_chars": 421}`
- 返回行数：`1`
- 耗时：`8.75 ms`

## import:updated:specs/SPEC-002-书目录查询.md#SPEC-002-2

```sql
UPDATE engineering_assets SET content_hash, version=version+1
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec-entry:specs/SPEC-002-书目录查询.md#SPEC-002-2", "path": "specs/SPEC-002-书目录查询.md#SPEC-002-2", "version": 3, "content_chars": 54}`
- 返回行数：`1`
- 耗时：`4.902 ms`

## context:spec

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["spec_entry"], "limit": 30}`
- 返回行数：`9`
- 耗时：`10.206 ms`

## context:code

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["code"], "limit": 18}`
- 返回行数：`3`
- 耗时：`26.173 ms`

## context:test

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["test"], "limit": 18}`
- 返回行数：`3`
- 耗时：`14.082 ms`

## context:spec

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["spec_entry"], "limit": 30}`
- 返回行数：`9`
- 耗时：`7.181 ms`

## context:code

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["code"], "limit": 18}`
- 返回行数：`3`
- 耗时：`3.535 ms`

## context:test

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["test"], "limit": 18}`
- 返回行数：`3`
- 耗时：`23.945 ms`

## context:spec

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 u_并 u_验 u_证 u_兼 u_容 u_性 b_年份 b_份下 b_下限 b_限筛 b_筛选 b_选并 b_并验 b_验证 b_证兼 b_兼容 b_容性", "project_key": "minimax-sdd", "kinds": ["spec_entry"], "limit": 30}`
- 返回行数：`8`
- 耗时：`10.261 ms`

## context:code

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 u_并 u_验 u_证 u_兼 u_容 u_性 b_年份 b_份下 b_下限 b_限筛 b_筛选 b_选并 b_并验 b_验证 b_证兼 b_兼容 b_容性", "project_key": "minimax-sdd", "kinds": ["code"], "limit": 18}`
- 返回行数：`3`
- 耗时：`4.596 ms`

## context:test

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 u_并 u_验 u_证 u_兼 u_容 u_性 b_年份 b_份下 b_下限 b_限筛 b_筛选 b_选并 b_并验 b_验证 b_证兼 b_兼容 b_容性", "project_key": "minimax-sdd", "kinds": ["test"], "limit": 18}`
- 返回行数：`3`
- 耗时：`4.448 ms`

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`9.954 ms`

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`2.383 ms`

## import:inserted:sample-project/src/integration.py

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "test:seekdb-integration", "asset_id": "test:integration.py", "path": "sample-project/src/integration.py", "version": 1, "content_chars": 63}`
- 返回行数：`1`
- 耗时：`3.651 ms`

## integration:search

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "min_year min year", "project_key": "test:seekdb-integration", "kinds": ["code"], "limit": 5}`
- 返回行数：`1`
- 耗时：`19.43 ms`

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`8.779 ms`

## import:inserted:sample-project/src/integration.py

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "test:seekdb-integration", "asset_id": "test:integration.py", "path": "sample-project/src/integration.py", "version": 1, "content_chars": 63}`
- 返回行数：`1`
- 耗时：`3.555 ms`

## integration:search

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "min_year min year", "project_key": "test:seekdb-integration", "kinds": ["code"], "limit": 5}`
- 返回行数：`1`
- 耗时：`18.67 ms`

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`7.09 ms`

## context:spec

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["spec_entry"], "limit": 30}`
- 返回行数：`9`
- 耗时：`37.666 ms`

## context:code

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["code"], "limit": 18}`
- 返回行数：`3`
- 耗时：`9.096 ms`

## context:test

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["test"], "limit": 18}`
- 返回行数：`3`
- 耗时：`19.536 ms`

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`50.723 ms`

## context:spec

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["spec_entry"], "limit": 30}`
- 返回行数：`9`
- 耗时：`66.812 ms`

## context:code

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["code"], "limit": 18}`
- 返回行数：`3`
- 耗时：`29.709 ms`

## context:test

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["test"], "limit": 18}`
- 返回行数：`3`
- 耗时：`14.069 ms`

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`28.038 ms`

## import:updated:sample-project/src/bookdesk/catalog.py

```sql
UPDATE engineering_assets SET content_hash, version=version+1
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "code:sample-project/src/bookdesk/catalog.py", "path": "sample-project/src/bookdesk/catalog.py", "version": 2, "content_chars": 1675}`
- 返回行数：`1`
- 耗时：`24.345 ms`

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`27.413 ms`

## context:spec

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["spec_entry"], "limit": 30}`
- 返回行数：`9`
- 耗时：`24.975 ms`

## context:code

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["code"], "limit": 18}`
- 返回行数：`3`
- 耗时：`24.697 ms`

## context:test

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["test"], "limit": 18}`
- 返回行数：`3`
- 耗时：`30.139 ms`

## context:spec

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["spec_entry"], "limit": 30}`
- 返回行数：`9`
- 耗时：`11.754 ms`

## context:code

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["code"], "limit": 18}`
- 返回行数：`3`
- 耗时：`6.298 ms`

## context:test

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["test"], "limit": 18}`
- 返回行数：`3`
- 耗时：`23.254 ms`

## context:spec

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 u_并 u_验 u_证 u_兼 u_容 u_性 b_年份 b_份下 b_下限 b_限筛 b_筛选 b_选并 b_并验 b_验证 b_证兼 b_兼容 b_容性", "project_key": "minimax-sdd", "kinds": ["spec_entry"], "limit": 30}`
- 返回行数：`8`
- 耗时：`22.905 ms`

## context:code

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 u_并 u_验 u_证 u_兼 u_容 u_性 b_年份 b_份下 b_下限 b_限筛 b_筛选 b_选并 b_并验 b_验证 b_证兼 b_兼容 b_容性", "project_key": "minimax-sdd", "kinds": ["code"], "limit": 18}`
- 返回行数：`3`
- 耗时：`4.281 ms`

## context:test

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 u_并 u_验 u_证 u_兼 u_容 u_性 b_年份 b_份下 b_下限 b_限筛 b_筛选 b_选并 b_并验 b_验证 b_证兼 b_兼容 b_容性", "project_key": "minimax-sdd", "kinds": ["test"], "limit": 18}`
- 返回行数：`3`
- 耗时：`3.654 ms`

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`27.331 ms`

## import:updated:specs/SPEC-002-书目录查询.md

```sql
UPDATE engineering_assets SET content_hash, version=version+1
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec:specs/SPEC-002-书目录查询.md", "path": "specs/SPEC-002-书目录查询.md", "version": 6, "content_chars": 454}`
- 返回行数：`1`
- 耗时：`11.433 ms`

## import:updated:specs/SPEC-002-书目录查询.md#SPEC-002-2

```sql
UPDATE engineering_assets SET content_hash, version=version+1
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec-entry:specs/SPEC-002-书目录查询.md#SPEC-002-2", "path": "specs/SPEC-002-书目录查询.md#SPEC-002-2", "version": 4, "content_chars": 87}`
- 返回行数：`1`
- 耗时：`2.709 ms`

## context:spec

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_验 u_证 u_更 u_新 u_后 u_规 u_格 u_内 u_容 u_被 u_重 u_读 u_取 b_验证 b_证更 b_更新 b_新后 b_后规 b_规格 b_格内 b_内容 b_容被 b_被重 b_重新 b_新读 b_读取", "project_key": "minimax-sdd", "kinds": ["spec_entry"], "limit": 30}`
- 返回行数：`8`
- 耗时：`27.669 ms`

## context:code

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_验 u_证 u_更 u_新 u_后 u_规 u_格 u_内 u_容 u_被 u_重 u_读 u_取 b_验证 b_证更 b_更新 b_新后 b_后规 b_规格 b_格内 b_内容 b_容被 b_被重 b_重新 b_新读 b_读取", "project_key": "minimax-sdd", "kinds": ["code"], "limit": 18}`
- 返回行数：`3`
- 耗时：`28.287 ms`

## context:test

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_验 u_证 u_更 u_新 u_后 u_规 u_格 u_内 u_容 u_被 u_重 u_读 u_取 b_验证 b_证更 b_更新 b_新后 b_后规 b_规格 b_格内 b_内容 b_容被 b_被重 b_重新 b_新读 b_读取", "project_key": "minimax-sdd", "kinds": ["test"], "limit": 18}`
- 返回行数：`3`
- 耗时：`14.395 ms`

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`1.682 ms`

## import:updated:specs/SPEC-002-书目录查询.md

```sql
UPDATE engineering_assets SET content_hash, version=version+1
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec:specs/SPEC-002-书目录查询.md", "path": "specs/SPEC-002-书目录查询.md", "version": 7, "content_chars": 421}`
- 返回行数：`1`
- 耗时：`6.112 ms`

## import:updated:specs/SPEC-002-书目录查询.md#SPEC-002-2

```sql
UPDATE engineering_assets SET content_hash, version=version+1
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "spec-entry:specs/SPEC-002-书目录查询.md#SPEC-002-2", "path": "specs/SPEC-002-书目录查询.md#SPEC-002-2", "version": 5, "content_chars": 54}`
- 返回行数：`1`
- 耗时：`3.656 ms`

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`1.768 ms`

## import:inserted:sample-project/src/integration.py

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "test:seekdb-integration", "asset_id": "test:integration.py", "path": "sample-project/src/integration.py", "version": 1, "content_chars": 63}`
- 返回行数：`1`
- 耗时：`10.424 ms`

## integration:search

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "min_year min year", "project_key": "test:seekdb-integration", "kinds": ["code"], "limit": 5}`
- 返回行数：`1`
- 耗时：`12.51 ms`

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`1.756 ms`

## context:spec

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["spec_entry"], "limit": 30}`
- 返回行数：`9`
- 耗时：`12.185 ms`

## context:code

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["code"], "limit": 18}`
- 返回行数：`3`
- 耗时：`8.675 ms`

## context:test

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["test"], "limit": 18}`
- 返回行数：`3`
- 耗时：`27.998 ms`

## context:spec

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["spec_entry"], "limit": 30}`
- 返回行数：`9`
- 耗时：`14.196 ms`

## context:code

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["code"], "limit": 18}`
- 返回行数：`3`
- 耗时：`33.24 ms`

## context:test

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["test"], "limit": 18}`
- 返回行数：`3`
- 耗时：`7.96 ms`

## context:spec

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 u_并 u_验 u_证 u_兼 u_容 u_性 b_年份 b_份下 b_下限 b_限筛 b_筛选 b_选并 b_并验 b_验证 b_证兼 b_兼容 b_容性", "project_key": "minimax-sdd", "kinds": ["spec_entry"], "limit": 30}`
- 返回行数：`8`
- 耗时：`33.698 ms`

## context:code

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 u_并 u_验 u_证 u_兼 u_容 u_性 b_年份 b_份下 b_下限 b_限筛 b_筛选 b_选并 b_并验 b_验证 b_证兼 b_兼容 b_容性", "project_key": "minimax-sdd", "kinds": ["code"], "limit": 18}`
- 返回行数：`3`
- 耗时：`28.002 ms`

## context:test

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 u_并 u_验 u_证 u_兼 u_容 u_性 b_年份 b_份下 b_下限 b_限筛 b_筛选 b_选并 b_并验 b_验证 b_证兼 b_兼容 b_容性", "project_key": "minimax-sdd", "kinds": ["test"], "limit": 18}`
- 返回行数：`3`
- 耗时：`30.62 ms`

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`25.137 ms`

## import:inserted:sample-project/src/integration.py

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "test:seekdb-integration", "asset_id": "test:integration.py", "path": "sample-project/src/integration.py", "version": 1, "content_chars": 63}`
- 返回行数：`1`
- 耗时：`2.379 ms`

## integration:search

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "min_year min year", "project_key": "test:seekdb-integration", "kinds": ["code"], "limit": 5}`
- 返回行数：`1`
- 耗时：`11.428 ms`

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`1.719 ms`

## import:updated:sample-project/tests/conftest.py

```sql
UPDATE engineering_assets SET content_hash, version=version+1
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "test:sample-project/tests/conftest.py", "path": "sample-project/tests/conftest.py", "version": 2, "content_chars": 753}`
- 返回行数：`1`
- 耗时：`6.837 ms`

## import:updated:sample-project/tests/test_catalog_year_filter.py

```sql
UPDATE engineering_assets SET content_hash, version=version+1
```

- 参数：`{"project_key": "minimax-sdd", "asset_id": "test:sample-project/tests/test_catalog_year_filter.py", "path": "sample-project/tests/test_catalog_year_filter.py", "version": 2, "content_chars": 1640}`
- 返回行数：`1`
- 耗时：`3.071 ms`

## context:spec

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["spec_entry"], "limit": 30}`
- 返回行数：`9`
- 耗时：`13.078 ms`

## context:code

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["code"], "limit": 18}`
- 返回行数：`3`
- 耗时：`32.529 ms`

## context:test

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["test"], "limit": 18}`
- 返回行数：`3`
- 耗时：`29.757 ms`

## context:spec

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["spec_entry"], "limit": 30}`
- 返回行数：`9`
- 耗时：`13.063 ms`

## context:code

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["code"], "limit": 18}`
- 返回行数：`3`
- 耗时：`8.758 ms`

## context:test

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year book published_year published u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 b_年份 b_份下 b_下限 b_限筛 b_筛选 u_按 u_包 u_含 u_边 u_界 b_包含 b_含边 b_边界 u_并 u_保 u_持 u_关 u_键 u_词 b_并保 b_保持 b_持关 b_关键 b_键词 u_标 u_签 b_标签 u_归 u_档 u_项 u_既 u_有 u_排 u_序 u_行 u_不 u_变 b_归档 b_档选 b_选项 b_项既 b_既有 b_有排 b_排序 b_序行 b_行不 b_不变", "project_key": "minimax-sdd", "kinds": ["test"], "limit": 18}`
- 返回行数：`3`
- 耗时：`20.07 ms`

## context:spec

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 u_并 u_验 u_证 u_兼 u_容 u_性 b_年份 b_份下 b_下限 b_限筛 b_筛选 b_选并 b_并验 b_验证 b_证兼 b_兼容 b_容性", "project_key": "minimax-sdd", "kinds": ["spec_entry"], "limit": 30}`
- 返回行数：`8`
- 耗时：`22.705 ms`

## context:code

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 u_并 u_验 u_证 u_兼 u_容 u_性 b_年份 b_份下 b_下限 b_限筛 b_筛选 b_选并 b_并验 b_验证 b_证兼 b_兼容 b_容性", "project_key": "minimax-sdd", "kinds": ["code"], "limit": 18}`
- 返回行数：`3`
- 耗时：`4.55 ms`

## context:test

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 u_并 u_验 u_证 u_兼 u_容 u_性 b_年份 b_份下 b_下限 b_限筛 b_筛选 b_选并 b_并验 b_验证 b_证兼 b_兼容 b_容性", "project_key": "minimax-sdd", "kinds": ["test"], "limit": 18}`
- 返回行数：`3`
- 耗时：`4.603 ms`
## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`5.45 ms`

## import:inserted:sample-project/src/integration.py

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "test:seekdb-integration", "asset_id": "test:integration.py", "path": "sample-project/src/integration.py", "version": 1, "content_chars": 63}`
- 返回行数：`1`
- 耗时：`2.555 ms`

## integration:search

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "min_year min year", "project_key": "test:seekdb-integration", "kinds": ["code"], "limit": 5}`
- 返回行数：`1`
- 耗时：`10.781 ms`

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`2.384 ms`

## import:inserted:sample-project/src/integration.py

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "test:seekdb-integration", "asset_id": "test:integration.py", "path": "sample-project/src/integration.py", "version": 1, "content_chars": 63}`
- 返回行数：`1`
- 耗时：`1.211 ms`

## integration:search

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "min_year min year", "project_key": "test:seekdb-integration", "kinds": ["code"], "limit": 5}`
- 返回行数：`1`
- 耗时：`2.523 ms`

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`1.724 ms`

## import:inserted:sample-project/src/integration.py

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "test:seekdb-integration", "asset_id": "test:integration.py", "path": "sample-project/src/integration.py", "version": 1, "content_chars": 63}`
- 返回行数：`1`
- 耗时：`1.028 ms`

## integration:search

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "min_year min year", "project_key": "test:seekdb-integration", "kinds": ["code"], "limit": 5}`
- 返回行数：`1`
- 耗时：`21.652 ms`

## context:spec

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 u_并 u_验 u_证 u_兼 u_容 u_性 b_年份 b_份下 b_下限 b_限筛 b_筛选 b_选并 b_并验 b_验证 b_证兼 b_兼容 b_容性", "project_key": "minimax-sdd", "kinds": ["spec_entry"], "limit": 30}`
- 返回行数：`8`
- 耗时：`28.251 ms`

## context:code

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 u_并 u_验 u_证 u_兼 u_容 u_性 b_年份 b_份下 b_下限 b_限筛 b_筛选 b_选并 b_并验 b_验证 b_证兼 b_兼容 b_容性", "project_key": "minimax-sdd", "kinds": ["code"], "limit": 18}`
- 返回行数：`3`
- 耗时：`23.957 ms`

## context:test

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 u_并 u_验 u_证 u_兼 u_容 u_性 b_年份 b_份下 b_下限 b_限筛 b_筛选 b_选并 b_并验 b_验证 b_证兼 b_兼容 b_容性", "project_key": "minimax-sdd", "kinds": ["test"], "limit": 18}`
- 返回行数：`3`
- 耗时：`4.192 ms`
## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`36.716 ms`

## import:inserted:sample-project/src/integration.py

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "test:seekdb-integration", "asset_id": "test:integration.py", "path": "sample-project/src/integration.py", "version": 1, "content_chars": 63}`
- 返回行数：`1`
- 耗时：`4.381 ms`

## integration:search

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "min_year min year", "project_key": "test:seekdb-integration", "kinds": ["code"], "limit": 5}`
- 返回行数：`1`
- 耗时：`13.196 ms`

## initialize:create-table

```sql
CREATE TABLE IF NOT EXISTS engineering_assets
```

- 参数：`{"database": "minimax_sdd"}`
- 返回行数：`0`
- 耗时：`2.481 ms`

## import:inserted:sample-project/src/integration.py

```sql
INSERT/UPDATE engineering_assets
```

- 参数：`{"project_key": "test:seekdb-integration", "asset_id": "test:integration.py", "path": "sample-project/src/integration.py", "version": 1, "content_chars": 63}`
- 返回行数：`1`
- 耗时：`1.775 ms`

## integration:search

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "min_year min year", "project_key": "test:seekdb-integration", "kinds": ["code"], "limit": 5}`
- 返回行数：`1`
- 耗时：`2.364 ms`

## context:spec

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 u_并 u_验 u_证 u_兼 u_容 u_性 b_年份 b_份下 b_下限 b_限筛 b_筛选 b_选并 b_并验 b_验证 b_证兼 b_兼容 b_容性", "project_key": "minimax-sdd", "kinds": ["spec_entry"], "limit": 30}`
- 返回行数：`8`
- 耗时：`13.822 ms`

## context:code

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 u_并 u_验 u_证 u_兼 u_容 u_性 b_年份 b_份下 b_下限 b_限筛 b_筛选 b_选并 b_并验 b_验证 b_证兼 b_兼容 b_容性", "project_key": "minimax-sdd", "kinds": ["code"], "limit": 18}`
- 返回行数：`3`
- 耗时：`5.017 ms`

## context:test

```sql
SELECT project_key, asset_id, kind, path, title, symbol, content, content_hash, version, MATCH(searchable_text) AGAINST(%s) AS score FROM `engineering_assets` WHERE project_key=%s AND kind IN (%s) AND MATCH(searchable_text) AGAINST(%s) ORDER BY score DESC, path, asset_id LIMIT %s
```

- 参数：`{"analyzed_query": "catalog search min_year min year u_增 u_加 b_增加 u_年 u_份 u_下 u_限 u_筛 u_选 u_并 u_验 u_证 u_兼 u_容 u_性 b_年份 b_份下 b_下限 b_限筛 b_筛选 b_选并 b_并验 b_验证 b_证兼 b_兼容 b_容性", "project_key": "minimax-sdd", "kinds": ["test"], "limit": 18}`
- 返回行数：`3`
- 耗时：`26.15 ms`
