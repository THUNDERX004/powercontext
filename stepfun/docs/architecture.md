# Architecture

```mermaid
sequenceDiagram
    participant U as User
    participant UI as Browser UI
    participant W as Browser Worker
    participant M as ONNX FP16 Model
    participant A as Node API
    participant D as seekdb

    U->>UI: Select document
    UI->>UI: Normalize + chunk + SHA-256
    UI->>W: Embed chunk batch
    W->>M: Local inference (WebGPU or WASM)
    M-->>W: 384-d normalized embeddings
    W-->>UI: Vectors + backend + timing
    UI->>A: Text + vectors + metadata
    A->>D: collection.upsert()
    A->>D: collection.refresh_index()
    A->>D: Filtered vector visibility probe
    D-->>A: Imported chunk visible
    A-->>UI: 201 Created

    U->>UI: Search query
    UI->>W: Embed query locally
    W->>M: Local inference
    M-->>W: Query vector
    W-->>UI: Query vector
    UI->>A: Query text + query vector
    A->>D: DBMS_HYBRID_SEARCH(query + knn + RRF)
    D-->>A: Fused ordered results
    A-->>UI: Results + database timing
    UI-->>U: Original text fragments
```

## Trust boundaries

- Browser: owns document text before upload and all embedding computation.
- Node API: has database credentials; never performs embedding inference.
- seekdb: owns collection tables, fulltext index, HNSW index, and hybrid rank
  execution.

The Node process listens on `127.0.0.1` by default. It is a local companion
service, not a cloud proxy.
