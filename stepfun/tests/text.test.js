import assert from "node:assert/strict";
import test from "node:test";
import {
  chunkText,
  inferTitle,
  normalizeDocumentText,
  sha256Hex,
  titleFromFilename,
} from "../web/src/lib/text.js";

test("normalizeDocumentText removes BOM, NULs and normalizes line endings", () => {
  assert.equal(
    normalizeDocumentText("\uFEFFalpha\r\nbeta\rgamma\u0000"),
    "alpha\nbeta\ngamma",
  );
});

test("chunkText creates bounded, indexed chunks", () => {
  const paragraph = "A local embedding model keeps the text on this device. ".repeat(
    40,
  );
  const chunks = chunkText(paragraph, { maxChars: 300, overlapChars: 40 });
  assert.ok(chunks.length > 1);
  assert.deepEqual(
    chunks.map((chunk) => chunk.index),
    chunks.map((_, index) => index),
  );
  assert.ok(chunks.every((chunk) => chunk.text.length <= 300));
  assert.ok(chunks.every((chunk) => chunk.charCount === chunk.text.length));
});

test("chunkText preserves CJK punctuation boundaries", () => {
  const text = "第一段介绍浏览器本地推理。第二句介绍 seekdb 检索。\n\n第三段说明索引刷新。";
  const chunks = chunkText(text, { maxChars: 100, overlapChars: 10 });
  assert.equal(chunks.length, 1);
  assert.match(chunks[0].text, /浏览器本地推理/u);
  assert.match(chunks[0].text, /索引刷新/u);
});

test("sha256Hex is stable and emits a 64-character digest", async () => {
  const hash = await sha256Hex("seekdb");
  assert.match(hash, /^[a-f0-9]{64}$/);
  assert.equal(
    hash,
    "0972b56d61c7e464885c9cee26944f5fa35496630917f4665425384896503e14",
  );
});

test("filename and text title helpers produce concise titles", () => {
  assert.equal(titleFromFilename("hybrid_search-notes.md"), "hybrid search notes");
  assert.equal(
    inferTitle("# 本地知识库\n\n正文", "fallback"),
    "本地知识库",
  );
});
