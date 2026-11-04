import assert from "node:assert/strict";
import test from "node:test";
import { SeekdbStore } from "../../server/seekdb-store.js";

const integrationEnabled = process.env.STEPFUN_INTEGRATION === "1";

function unitVector(position) {
  const vector = Array(configDimension()).fill(0);
  vector[position] = 1;
  return vector;
}

function configDimension() {
  return 384;
}

test(
  "seekdb import, refresh and hybrid search round trip",
  { skip: !integrationEnabled },
  async () => {
    const store = new SeekdbStore();
    let kb;
    try {
      await store.initialize();
      kb = await store.createKnowledgeBase(`integration-${Date.now()}`);
      const imported = await store.importDocument(kb.id, {
        document: {
          title: "Index refresh marker",
          sourceName: "integration.txt",
          contentHash: "b".repeat(64),
          chunks: [
            {
              index: 0,
              text: "seekdb 在写入之后调用 refresh index，使新增向量可以立即检索。",
            },
          ],
        },
        embeddings: [unitVector(0)],
        model: {
          id: "integration-model",
          revision: "test",
          dtype: "fp16",
          backend: "wasm",
        },
      });
      assert.equal(imported.chunkCount, 1);
      assert.ok(imported.timings.visibilityAttempts >= 1);

      const searched = await store.search(kb.id, {
        query: "向量 检索 新增",
        queryEmbedding: unitVector(0),
        topK: 3,
      });
      assert.ok(searched.results.length >= 1);
      assert.equal(searched.engine, "seekdb DBMS_HYBRID_SEARCH");
      assert.equal(searched.ranker, "RRF (k=60)");

      const documents = await store.listDocuments(kb.id);
      assert.equal(documents.length, 1);
      await store.deleteDocument(kb.id, imported.documentId);
      assert.equal((await store.listDocuments(kb.id)).length, 0);
    } finally {
      if (kb) {
        await store.deleteKnowledgeBase(kb.id).catch(() => {});
      }
      await store.close();
    }
  },
);
