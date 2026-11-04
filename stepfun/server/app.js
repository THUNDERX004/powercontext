import express from "express";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { config } from "./config.js";
import { AppError, notFound } from "./errors.js";
import {
  validateDocumentImport,
  validateKnowledgeBaseName,
  validateSearchPayload,
} from "./validation.js";

const distDirectory = path.resolve(
  fileURLToPath(new URL("../dist", import.meta.url)),
);

function asyncRoute(handler) {
  return (request, response, next) => {
    Promise.resolve(handler(request, response, next)).catch(next);
  };
}

export async function createApplication({ store, vite } = {}) {
  if (!store) {
    throw new Error("createApplication requires a SeekdbStore instance");
  }

  const app = express();
  const indexHtml = vite
    ? null
    : fs.readFileSync(path.join(distDirectory, "index.html"), "utf8");
  app.disable("x-powered-by");
  app.use((request, response, next) => {
    response.setHeader("X-Content-Type-Options", "nosniff");
    response.setHeader("Referrer-Policy", "same-origin");
    response.setHeader("Cross-Origin-Opener-Policy", "same-origin");
    response.setHeader("Cross-Origin-Embedder-Policy", "credentialless");
    next();
  });
  app.use(express.json({ limit: config.bodyLimit }));

  app.get(
    "/api/config",
    asyncRoute(async (_request, response) => {
      response.json({
        model: config.model,
        seekdb: {
          database: config.seekdb.database,
          endpoint: "server-side only",
          vectorDimension: config.vectorDimension,
          hybridRanker: "RRF",
        },
        limits: {
          maxChunksPerDocument: config.maxChunksPerDocument,
          maxChunkChars: config.maxChunkChars,
          maxTopK: config.maxTopK,
        },
      });
    }),
  );

  app.get(
    "/api/health",
    asyncRoute(async (_request, response) => {
      const start = process.hrtime.bigint();
      try {
        const database = await store.health();
        const totalLatencyMs =
          Number(process.hrtime.bigint() - start) / 1_000_000;
        response.json({
          ok: true,
          database: { ...database, totalLatencyMs },
        });
      } catch (error) {
        response.status(503).json({
          ok: false,
          error: {
            code: "DATABASE_UNAVAILABLE",
            message: error.message,
          },
        });
      }
    }),
  );

  app.get(
    "/api/knowledge-bases",
    asyncRoute(async (_request, response) => {
      response.json({ items: await store.listKnowledgeBases() });
    }),
  );

  app.post(
    "/api/knowledge-bases",
    asyncRoute(async (request, response) => {
      const name = validateKnowledgeBaseName(request.body?.name);
      const knowledgeBase = await store.createKnowledgeBase(name);
      response.status(201).json(knowledgeBase);
    }),
  );

  app.delete(
    "/api/knowledge-bases/:kbId",
    asyncRoute(async (request, response) => {
      response.json(await store.deleteKnowledgeBase(request.params.kbId));
    }),
  );

  app.post(
    "/api/knowledge-bases/:kbId/documents",
    asyncRoute(async (request, response) => {
      const payload = validateDocumentImport(request.body);
      const imported = await store.importDocument(request.params.kbId, payload);
      response.status(201).json(imported);
    }),
  );

  app.get(
    "/api/knowledge-bases/:kbId/documents",
    asyncRoute(async (request, response) => {
      response.json({
        items: await store.listDocuments(request.params.kbId),
      });
    }),
  );

  app.delete(
    "/api/knowledge-bases/:kbId/documents/:documentId",
    asyncRoute(async (request, response) => {
      response.json(
        await store.deleteDocument(
          request.params.kbId,
          request.params.documentId,
        ),
      );
    }),
  );

  app.post(
    "/api/knowledge-bases/:kbId/search",
    asyncRoute(async (request, response) => {
      const payload = validateSearchPayload(request.body);
      const searched = await store.search(request.params.kbId, payload);
      response.json(searched);
    }),
  );

  app.post(
    "/api/knowledge-bases/:kbId/refresh",
    asyncRoute(async (request, response) => {
      const refreshed = await store.refreshKnowledgeBase(request.params.kbId);
      response.json(refreshed);
    }),
  );

  app.use("/api", (_request, _response, next) => {
    next(notFound("API route not found"));
  });

  if (vite) {
    app.use(vite.middlewares);
  } else {
    app.use(express.static(distDirectory, { index: false }));
    app.use((request, response, next) => {
      if (request.method !== "GET") {
        return next(notFound());
      }
      response.type("html").send(indexHtml);
    });
  }

  app.use((error, _request, response, _next) => {
    const status = error instanceof AppError ? error.status : 500;
    const code =
      error instanceof AppError ? error.code : "INTERNAL_SERVER_ERROR";
    if (status >= 500) {
      console.error("[stepfun] request failed", error);
    }
    response.status(status).json({
      error: {
        code,
        message: status >= 500 ? "Request failed" : error.message,
        ...(error instanceof AppError && error.details
          ? { details: error.details }
          : {}),
      },
    });
  });

  return app;
}
