import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const appRoot = path.resolve(fileURLToPath(new URL("..", import.meta.url)));

function loadEnvFile(filePath) {
  if (!fs.existsSync(filePath)) {
    return;
  }

  const lines = fs.readFileSync(filePath, "utf8").split(/\r?\n/);
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) {
      continue;
    }

    const separator = trimmed.indexOf("=");
    if (separator < 1) {
      continue;
    }

    const key = trimmed.slice(0, separator).trim();
    let value = trimmed.slice(separator + 1).trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }

    if (!(key in process.env)) {
      process.env[key] = value;
    }
  }
}

loadEnvFile(path.join(appRoot, ".env"));

function integerFromEnv(name, fallback) {
  const raw = process.env[name];
  if (raw === undefined || raw === "") {
    return fallback;
  }
  const parsed = Number.parseInt(raw, 10);
  if (!Number.isFinite(parsed)) {
    throw new Error(`${name} must be an integer`);
  }
  return parsed;
}

export const config = Object.freeze({
  appHost: process.env.APP_HOST || "127.0.0.1",
  appPort: integerFromEnv("APP_PORT", 3000),
  nodeEnv: process.env.NODE_ENV || "development",
  bodyLimit: process.env.REQUEST_BODY_LIMIT || "48mb",
  seekdb: Object.freeze({
    host: process.env.SEEKDB_HOST || "127.0.0.1",
    port: integerFromEnv("SEEKDB_PORT", 2881),
    user: process.env.SEEKDB_USER || "root",
    password: process.env.SEEKDB_PASSWORD || "",
    database: process.env.SEEKDB_DATABASE || "competition",
    charset: process.env.SEEKDB_CHARSET || "utf8mb4",
    queryTimeout: integerFromEnv("SEEKDB_QUERY_TIMEOUT_MS", 30_000),
  }),
  catalogTable: "stepfun_kb_catalog",
  documentTable: "stepfun_kb_documents",
  collectionPrefix: "stepfun_kb_",
  vectorDimension: 384,
  maxChunksPerDocument: 512,
  maxChunkChars: 4_000,
  maxTitleChars: 200,
  maxSourceChars: 240,
  defaultTopK: 6,
  maxTopK: 20,
  maxUploadDocuments: 24,
  model: Object.freeze({
    id: "onnx-community/all-MiniLM-L6-v2-ONNX",
    revision: "aff7a1dc4e8a1ea593e6ea21e95c22ef0a25966f",
    dimension: 384,
    license: "Apache-2.0",
    webgpuDtype: "fp16",
    wasmDtype: "fp16",
  }),
  appRoot,
});
