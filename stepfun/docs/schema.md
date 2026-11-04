# seekdb Schema

## Catalog table

```sql
CREATE TABLE stepfun_kb_catalog (
  id VARCHAR(32) PRIMARY KEY,
  name VARCHAR(64) NOT NULL,
  collection_name VARCHAR(64) NOT NULL UNIQUE,
  created_at VARCHAR(40) NOT NULL,
  updated_at VARCHAR(40) NOT NULL
) DEFAULT CHARSET = utf8mb4;
```

The catalog is the durable mapping between the UI knowledge-base ID and the
physical seekdb collection.

## Document registry

```sql
CREATE TABLE stepfun_kb_documents (
  document_id CHAR(64) PRIMARY KEY,
  kb_id VARCHAR(32) NOT NULL,
  title VARCHAR(200) NOT NULL,
  source_name VARCHAR(240) NOT NULL,
  content_hash CHAR(64) NOT NULL,
  chunk_count INT NOT NULL,
  imported_at VARCHAR(40) NOT NULL,
  model_id VARCHAR(160) NOT NULL,
  embedding_dtype VARCHAR(20) NOT NULL,
  inference_backend VARCHAR(20) NOT NULL,
  UNIQUE KEY uq_stepfun_kb_hash (kb_id, content_hash),
  KEY idx_stepfun_kb_id (kb_id)
) DEFAULT CHARSET = utf8mb4;
```

`document_id` and `content_hash` are SHA-256 hashes of normalized document
text. The unique key de-duplicates repeated imports within one knowledge base.

## Collection schema

Each `stepfun_kb_<id>` collection is created through `seekdb-js`:

```text
FulltextIndexConfig("ik", { ik_mode: "smart" })
VectorIndexConfig(
  hnsw: {
    dimension: 384,
    distance: "cosine",
    type: "hnsw",
    m: 16,
    ef_construction: 200,
    ef_search: 64
  },
  embeddingFunction: null
)
```

The dense embedding function is `null` because embeddings are computed in the
user's browser. The fulltext parser uses smart IK mode for mixed Chinese and
English corpus text.

Each collection row stores:

- collection ID: `<document SHA-256>:<chunk index>`
- document: chunk text
- embedding: 384-dimensional normalized FP16-derived JavaScript number array
- metadata: document ID, title, source name, content hash, chunk index,
  character count, import time, model ID, dtype, and active backend

## Hybrid query

```javascript
await collection.hybridSearch({
  query: {
    whereDocument: { $contains: fulltextQuery },
    nResults: candidateSize,
  },
  knn: {
    queryEmbeddings: [queryEmbedding],
    nResults: candidateSize,
  },
  rank: {
    rrf: {
      rankWindowSize: candidateSize,
      rankConstant: 60,
    },
  },
  nResults: topK,
  include: ["documents", "metadatas", "distances"],
});
```

The SDK expands this request into seekdb's `DBMS_HYBRID_SEARCH` stored
procedure. Candidate retrieval, de-duplication, and RRF ranking execute in the
database.
