import { config } from "./config.js";
import { badRequest } from "./errors.js";

const HEX_HASH = /^[a-f0-9]{64}$/i;

export function requireObject(value, label) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw badRequest(`${label} must be an object`);
  }
  return value;
}

export function requireString(value, label, { min = 1, max = 10_000 } = {}) {
  if (typeof value !== "string") {
    throw badRequest(`${label} must be a string`);
  }
  const normalized = value.trim();
  if (normalized.length < min || normalized.length > max) {
    throw badRequest(`${label} must contain ${min}-${max} characters`);
  }
  return normalized;
}

export function validateKnowledgeBaseName(value) {
  const name = requireString(value, "name", { min: 1, max: 64 });
  if (/[\u0000-\u001f\u007f]/.test(name)) {
    throw badRequest("name contains control characters");
  }
  return name;
}

export function validateEmbedding(vector, index = 0) {
  if (!Array.isArray(vector)) {
    throw badRequest(`embeddings[${index}] must be an array`);
  }
  if (vector.length !== config.vectorDimension) {
    throw badRequest(
      `embeddings[${index}] must have ${config.vectorDimension} dimensions`,
      { expected: config.vectorDimension, actual: vector.length },
    );
  }

  let squaredNorm = 0;
  for (const component of vector) {
    if (typeof component !== "number" || !Number.isFinite(component)) {
      throw badRequest(`embeddings[${index}] contains a non-finite value`);
    }
    squaredNorm += component * component;
  }

  if (squaredNorm < 1e-8) {
    throw badRequest(`embeddings[${index}] must not be the zero vector`);
  }
  return vector;
}

export function validateDocumentImport(payload) {
  const body = requireObject(payload, "request body");
  const document = requireObject(body.document, "document");
  const chunks = document.chunks;

  if (!Array.isArray(chunks) || chunks.length < 1) {
    throw badRequest("document.chunks must contain at least one chunk");
  }
  if (chunks.length > config.maxChunksPerDocument) {
    throw badRequest(
      `document.chunks exceeds the ${config.maxChunksPerDocument} chunk limit`,
    );
  }

  const title = requireString(document.title, "document.title", {
    min: 1,
    max: config.maxTitleChars,
  });
  const sourceName = requireString(
    document.sourceName || document.title,
    "document.sourceName",
    { min: 1, max: config.maxSourceChars },
  );
  const contentHash = requireString(document.contentHash, "document.contentHash", {
    min: 64,
    max: 64,
  });
  if (!HEX_HASH.test(contentHash)) {
    throw badRequest("document.contentHash must be a SHA-256 hex digest");
  }

  const normalizedChunks = chunks.map((chunk, index) => {
    const item = requireObject(chunk, `document.chunks[${index}]`);
    const text = requireString(item.text, `document.chunks[${index}].text`, {
      min: 1,
      max: config.maxChunkChars,
    });
    if (item.index !== undefined && item.index !== index) {
      throw badRequest(`document.chunks[${index}].index must equal ${index}`);
    }
    return { index, text };
  });

  if (!Array.isArray(body.embeddings) || body.embeddings.length !== chunks.length) {
    throw badRequest("embeddings must contain one vector per chunk");
  }
  const embeddings = body.embeddings.map(validateEmbedding);

  const model = requireObject(body.model || {}, "model");
  return {
    document: {
      title,
      sourceName,
      contentHash: contentHash.toLowerCase(),
      chunks: normalizedChunks,
    },
    embeddings,
    model: {
      id: requireString(model.id || config.model.id, "model.id", {
        min: 1,
        max: 160,
      }),
      revision:
        typeof model.revision === "string" ? model.revision.slice(0, 80) : null,
      dtype:
        typeof model.dtype === "string" ? model.dtype.slice(0, 20) : "unknown",
      backend:
        typeof model.backend === "string" ? model.backend.slice(0, 20) : "unknown",
    },
  };
}

export function validateSearchPayload(payload) {
  const body = requireObject(payload, "request body");
  const query = requireString(body.query, "query", { min: 1, max: 240 });
  const queryEmbedding = validateEmbedding(body.queryEmbedding);
  const rawTopK = body.topK ?? config.defaultTopK;
  if (
    !Number.isInteger(rawTopK) ||
    rawTopK < 1 ||
    rawTopK > config.maxTopK
  ) {
    throw badRequest(`topK must be an integer from 1 to ${config.maxTopK}`);
  }
  return { query, queryEmbedding, topK: rawTopK };
}

export function sanitizeFulltextQuery(query) {
  const sanitized = query
    .normalize("NFKC")
    .replace(/[^\p{L}\p{N}\s]+/gu, " ")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 200);

  if (!sanitized) {
    throw badRequest("query must contain at least one letter or number");
  }
  return sanitized;
}
