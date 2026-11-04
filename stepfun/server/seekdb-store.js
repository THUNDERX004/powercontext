import crypto from "node:crypto";
import {
  FulltextIndexConfig,
  Schema,
  SeekdbClient,
  VectorIndexConfig,
} from "seekdb";
import { config } from "./config.js";
import { conflict, notFound, serviceUnavailable } from "./errors.js";
import { sanitizeFulltextQuery } from "./validation.js";

const delay = (milliseconds) =>
  new Promise((resolve) => setTimeout(resolve, milliseconds));

function elapsed(startedAt) {
  return Number(process.hrtime.bigint() - startedAt) / 1e6;
}

function asIsoTimestamp() {
  return new Date().toISOString();
}

function normalizeRow(row) {
  return Object.fromEntries(
    Object.entries(row).map(([key, value]) => [
      key.toLowerCase(),
      value == null ? value : String(value),
    ]),
  );
}

export class SeekdbStore {
  constructor(options = {}) {
    this.client = new SeekdbClient({
      ...config.seekdb,
      ...options,
    });
    this.initialization = null;
    this.kbLocks = new Map();
  }

  async initialize() {
    if (!this.initialization) {
      this.initialization = this.#initialize();
    }
    try {
      return await this.initialization;
    } catch (error) {
      this.initialization = null;
      throw error;
    }
  }

  async #initialize() {
    await this.client.execute("SELECT 1 AS ready");
    await this.client.execute(`
      CREATE TABLE IF NOT EXISTS ${config.catalogTable} (
        id VARCHAR(32) PRIMARY KEY,
        name VARCHAR(64) NOT NULL,
        collection_name VARCHAR(64) NOT NULL UNIQUE,
        created_at VARCHAR(40) NOT NULL,
        updated_at VARCHAR(40) NOT NULL
      ) DEFAULT CHARSET = utf8mb4
    `);
    await this.client.execute(`
      CREATE TABLE IF NOT EXISTS ${config.documentTable} (
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
      ) DEFAULT CHARSET = utf8mb4
    `);
  }

  async close() {
    await this.client.close();
  }

  async health() {
    const start = process.hrtime.bigint();
    const rows = await this.client.execute(
      "SELECT VERSION() AS version, DATABASE() AS database_name",
    );
    const row = rows?.[0] ? normalizeRow(rows[0]) : {};
    return {
      connected: true,
      latencyMs: elapsed(start),
      version: row.version || "unknown",
      database: row.database_name || config.seekdb.database,
    };
  }

  async listKnowledgeBases() {
    await this.initialize();
    const rows =
      (await this.client.execute(`
        SELECT
          c.id,
          c.name,
          c.collection_name,
          c.created_at,
          c.updated_at,
          COUNT(d.document_id) AS document_count,
          COALESCE(SUM(d.chunk_count), 0) AS chunk_count
        FROM ${config.catalogTable} c
        LEFT JOIN ${config.documentTable} d ON d.kb_id = c.id
        GROUP BY c.id, c.name, c.collection_name, c.created_at, c.updated_at
        ORDER BY c.updated_at DESC
      `)) || [];

    return rows.map((row) => {
      const item = normalizeRow(row);
      return {
        id: item.id,
        name: item.name,
        documentCount: Number(item.document_count || 0),
        chunkCount: Number(item.chunk_count || 0),
        createdAt: item.created_at,
        updatedAt: item.updated_at,
      };
    });
  }

  async createKnowledgeBase(name) {
    await this.initialize();
    const id = crypto.randomBytes(8).toString("hex");
    const collectionName = `${config.collectionPrefix}${id}`;
    const now = asIsoTimestamp();
    const schema = new Schema({
      fulltextIndex: new FulltextIndexConfig("ik", { ik_mode: "smart" }),
      vectorIndex: new VectorIndexConfig({
        hnsw: {
          dimension: config.vectorDimension,
          distance: "cosine",
          type: "hnsw",
          m: 16,
          ef_construction: 200,
          ef_search: 64,
        },
        embeddingFunction: null,
      }),
    });

    await this.client.createCollection({ name: collectionName, schema });
    try {
      await this.client.execute(
        `INSERT INTO ${config.catalogTable}
          (id, name, collection_name, created_at, updated_at)
         VALUES (?, ?, ?, ?, ?)`,
        [id, name, collectionName, now, now],
      );
    } catch (error) {
      await this.client.deleteCollection(collectionName).catch(() => {});
      throw error;
    }

    return {
      id,
      name,
      documentCount: 0,
      chunkCount: 0,
      createdAt: now,
      updatedAt: now,
    };
  }

  async deleteKnowledgeBase(id) {
    await this.initialize();
    const kb = await this.#getKnowledgeBaseRow(id);
    await this.client.deleteCollection(kb.collection_name);
    await this.client.execute(
      `DELETE FROM ${config.documentTable} WHERE kb_id = ?`,
      [id],
    );
    await this.client.execute(`DELETE FROM ${config.catalogTable} WHERE id = ?`, [
      id,
    ]);
    return { id };
  }

  async importDocument(kbId, payload) {
    await this.initialize();
    return this.#withKbLock(kbId, async () => {
      const kb = await this.#getKnowledgeBaseRow(kbId);
      const collection = await this.#openCollection(kb.collection_name);
      const { document, embeddings, model } = payload;
      const documentId = document.contentHash;
      const ids = document.chunks.map(
        (chunk) => `${documentId}:${chunk.index}`,
      );
      const importedAt = asIsoTimestamp();
      const metadatas = document.chunks.map((chunk) => ({
        documentId,
        title: document.title,
        sourceName: document.sourceName,
        contentHash: document.contentHash,
        chunkIndex: chunk.index,
        charCount: chunk.text.length,
        importedAt,
        modelId: model.id,
        dtype: model.dtype,
        backend: model.backend,
      }));

      const existingRows = await this.client.execute(
        `SELECT chunk_count FROM ${config.documentTable}
         WHERE kb_id = ? AND content_hash = ?
         LIMIT 1`,
        [kbId, document.contentHash],
      );
      const previousChunkCount = Number(existingRows?.[0]?.chunk_count || 0);

      const writeStart = process.hrtime.bigint();
      try {
        if (previousChunkCount > document.chunks.length) {
          const staleIds = Array.from(
            { length: previousChunkCount - document.chunks.length },
            (_, offset) => `${documentId}:${document.chunks.length + offset}`,
          );
          await collection.delete({ ids: staleIds });
        }

        await collection.upsert({
          ids,
          documents: document.chunks.map((chunk) => chunk.text),
          embeddings,
          metadatas,
        });
        const writeMs = elapsed(writeStart);

        const refreshStart = process.hrtime.bigint();
        await collection.refresh_index();
        const refreshMs = elapsed(refreshStart);

        const visibility = await this.#waitForVisibility(
          collection,
          documentId,
          ids[0],
          embeddings[0],
        );

        await this.client.execute(
          `INSERT INTO ${config.documentTable}
            (document_id, kb_id, title, source_name, content_hash, chunk_count,
             imported_at, model_id, embedding_dtype, inference_backend)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
           ON DUPLICATE KEY UPDATE
             title = VALUES(title),
             source_name = VALUES(source_name),
             chunk_count = VALUES(chunk_count),
             imported_at = VALUES(imported_at),
             model_id = VALUES(model_id),
             embedding_dtype = VALUES(embedding_dtype),
             inference_backend = VALUES(inference_backend)`,
          [
            documentId,
            kbId,
            document.title,
            document.sourceName,
            document.contentHash,
            document.chunks.length,
            importedAt,
            model.id,
            model.dtype,
            model.backend,
          ],
        );
        await this.#touchKnowledgeBase(kbId);

        return {
          documentId,
          title: document.title,
          sourceName: document.sourceName,
          chunkCount: document.chunks.length,
          replacedExisting: previousChunkCount > 0,
          timings: {
            writeMs,
            indexRefreshMs: refreshMs,
            visibilityWaitMs: visibility.waitMs,
            visibilityAttempts: visibility.attempts,
          },
          importedAt,
        };
      } catch (error) {
        await collection.delete({ ids }).catch(() => {});
        throw error;
      }
    });
  }

  async listDocuments(kbId) {
    await this.initialize();
    await this.#getKnowledgeBaseRow(kbId);
    const rows =
      (await this.client.execute(
        `SELECT document_id, title, source_name, chunk_count, imported_at,
                model_id, embedding_dtype, inference_backend
         FROM ${config.documentTable}
         WHERE kb_id = ?
         ORDER BY imported_at DESC`,
        [kbId],
      )) || [];

    return rows.map((row) => {
      const item = normalizeRow(row);
      return {
        id: item.document_id,
        title: item.title,
        sourceName: item.source_name,
        chunkCount: Number(item.chunk_count),
        importedAt: item.imported_at,
        modelId: item.model_id,
        dtype: item.embedding_dtype,
        backend: item.inference_backend,
      };
    });
  }

  async deleteDocument(kbId, documentId) {
    await this.initialize();
    return this.#withKbLock(kbId, async () => {
      const kb = await this.#getKnowledgeBaseRow(kbId);
      const rows = await this.client.execute(
        `SELECT chunk_count FROM ${config.documentTable}
         WHERE kb_id = ? AND document_id = ?
         LIMIT 1`,
        [kbId, documentId],
      );
      if (!rows?.length) {
        throw notFound("Document not found");
      }

      const collection = await this.#openCollection(kb.collection_name);
      const chunkCount = Number(rows[0].chunk_count);
      const ids = Array.from(
        { length: chunkCount },
        (_, index) => `${documentId}:${index}`,
      );
      await collection.delete({ ids });
      await collection.refresh_index();
      await this.client.execute(
        `DELETE FROM ${config.documentTable}
         WHERE kb_id = ? AND document_id = ?`,
        [kbId, documentId],
      );
      await this.#touchKnowledgeBase(kbId);
      return { documentId };
    });
  }

  async search(kbId, payload) {
    await this.initialize();
    const kb = await this.#getKnowledgeBaseRow(kbId);
    const collection = await this.#openCollection(kb.collection_name);
    const fulltextQuery = sanitizeFulltextQuery(payload.query);
    const candidateSize = Math.min(
      100,
      Math.max(payload.topK * 5, payload.topK, 20),
    );

    const searchStart = process.hrtime.bigint();
    const response = await collection.hybridSearch({
      query: {
        whereDocument: { $contains: fulltextQuery },
        nResults: candidateSize,
      },
      knn: {
        queryEmbeddings: [payload.queryEmbedding],
        nResults: candidateSize,
      },
      rank: {
        rrf: {
          rankWindowSize: candidateSize,
          rankConstant: 60,
        },
      },
      nResults: payload.topK,
      include: ["documents", "metadatas", "distances"],
    });
    const searchMs = elapsed(searchStart);

    const ids = response.ids?.[0] || [];
    const results = ids.map((id, index) => ({
      id,
      document: response.documents?.[0]?.[index] ?? null,
      metadata: response.metadatas?.[0]?.[index] ?? null,
      distance: response.distances?.[0]?.[index] ?? null,
    }));

    return {
      query: payload.query,
      fulltextQuery,
      results,
      engine: "seekdb DBMS_HYBRID_SEARCH",
      ranker: "RRF (k=60)",
      timings: {
        databaseSearchMs: searchMs,
        totalServerMs: searchMs,
      },
    };
  }

  async refreshKnowledgeBase(kbId) {
    await this.initialize();
    const kb = await this.#getKnowledgeBaseRow(kbId);
    const collection = await this.#openCollection(kb.collection_name);
    const start = process.hrtime.bigint();
    await collection.refresh_index();
    const refreshMs = elapsed(start);
    await this.#touchKnowledgeBase(kbId);
    return { refreshMs };
  }

  async #openCollection(name) {
    return this.client.getCollection({
      name,
      embeddingFunction: null,
    });
  }

  async #getKnowledgeBaseRow(id) {
    const rows = await this.client.execute(
      `SELECT id, name, collection_name, created_at, updated_at
       FROM ${config.catalogTable}
       WHERE id = ?
       LIMIT 1`,
      [id],
    );
    if (!rows?.length) {
      throw notFound("Knowledge base not found");
    }
    return normalizeRow(rows[0]);
  }

  async #touchKnowledgeBase(id) {
    await this.client.execute(
      `UPDATE ${config.catalogTable} SET updated_at = ? WHERE id = ?`,
      [asIsoTimestamp(), id],
    );
  }

  async #waitForVisibility(collection, documentId, expectedId, vector) {
    const start = process.hrtime.bigint();
    const delays = [0, 50, 100, 150, 250, 400, 650, 900, 1200];
    for (let attempt = 0; attempt < delays.length; attempt += 1) {
      if (delays[attempt] > 0) {
        await delay(delays[attempt]);
      }
      const result = await collection.query({
        queryEmbeddings: [vector],
        where: { documentId },
        nResults: 1,
        include: ["documents"],
      });
      if ((result.ids?.[0] || []).includes(expectedId)) {
        return {
          attempts: attempt + 1,
          waitMs: elapsed(start),
        };
      }
    }

    throw serviceUnavailable(
      "The document was written but did not become searchable after index refresh",
      { documentId, expectedChunkId: expectedId },
    );
  }

  async #withKbLock(kbId, operation) {
    const previous = this.kbLocks.get(kbId) || Promise.resolve();
    let release;
    const current = new Promise((resolve) => {
      release = resolve;
    });
    this.kbLocks.set(kbId, current);

    await previous.catch(() => {});
    try {
      return await operation();
    } finally {
      release();
      if (this.kbLocks.get(kbId) === current) {
        this.kbLocks.delete(kbId);
      }
    }
  }
}
