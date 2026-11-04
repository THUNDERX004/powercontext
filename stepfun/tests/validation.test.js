import assert from "node:assert/strict";
import test from "node:test";
import { config } from "../server/config.js";
import {
  sanitizeFulltextQuery,
  validateDocumentImport,
  validateEmbedding,
  validateKnowledgeBaseName,
  validateSearchPayload,
} from "../server/validation.js";

function vector(seed = 1) {
  return Array.from(
    { length: config.vectorDimension },
    (_, index) => Math.sin((index + 1) * seed) / 20,
  );
}

test("knowledge-base names reject control characters", () => {
  assert.equal(validateKnowledgeBaseName("  产品资料  "), "产品资料");
  assert.throws(() => validateKnowledgeBaseName("bad\u0000name"), /control/);
});

test("embedding validation enforces dimension and finite values", () => {
  assert.equal(validateEmbedding(vector()).length, 384);
  assert.throws(() => validateEmbedding([1, 2, 3]), /384 dimensions/);
  const nonFinite = vector();
  nonFinite[8] = Number.NaN;
  assert.throws(() => validateEmbedding(nonFinite), /non-finite/);
});

test("document import validates chunk/vector cardinality", () => {
  const chunks = [
    { index: 0, text: "first searchable chunk" },
    { index: 1, text: "second searchable chunk" },
  ];
  const result = validateDocumentImport({
    document: {
      title: "Test",
      sourceName: "test.txt",
      contentHash: "a".repeat(64),
      chunks,
    },
    embeddings: [vector(1), vector(2)],
    model: {
      id: config.model.id,
      revision: config.model.revision,
      dtype: "fp16",
      backend: "wasm",
    },
  });
  assert.equal(result.document.chunks.length, 2);
  assert.equal(result.embeddings.length, 2);
  assert.equal(result.model.dtype, "fp16");

  assert.throws(
    () =>
      validateDocumentImport({
        document: {
          title: "Test",
          contentHash: "a".repeat(64),
          chunks,
        },
        embeddings: [vector()],
      }),
    /one vector per chunk/,
  );
});

test("search validation and fulltext sanitization are deterministic", () => {
  const parsed = validateSearchPayload({
    query: "  seekdb + vector (hybrid)  ",
    queryEmbedding: vector(),
    topK: 5,
  });
  assert.equal(parsed.query, "seekdb + vector (hybrid)");
  assert.equal(parsed.topK, 5);
  assert.equal(
    sanitizeFulltextQuery("seekdb + vector (hybrid)"),
    "seekdb vector hybrid",
  );
  assert.equal(
    sanitizeFulltextQuery("数据库：向量 + 全文？"),
    "数据库 向量 全文",
  );
});
