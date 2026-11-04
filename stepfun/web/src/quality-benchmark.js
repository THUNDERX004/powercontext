import "./styles.css";
import { ModelClient } from "./model-client.js";

const params = new URLSearchParams(location.search);
const dtype = params.get("dtype") === "fp32" ? "fp32" : "fp16";
const backend = params.get("backend") || "auto";
const batchSize = Math.max(1, Math.min(32, Number(params.get("batch")) || 8));
const statusElement = document.getElementById("benchmarkStatus");
const outputElement = document.getElementById("benchmarkOutput");

function setStatus(message) {
  statusElement.textContent = message;
}

function cosine(left, right) {
  let dot = 0;
  let leftNorm = 0;
  let rightNorm = 0;
  for (let index = 0; index < left.length; index += 1) {
    dot += left[index] * right[index];
    leftNorm += left[index] * left[index];
    rightNorm += right[index] * right[index];
  }
  return dot / Math.sqrt(leftNorm * rightNorm);
}

function median(values) {
  if (!values.length) {
    return null;
  }
  const sorted = [...values].sort((left, right) => left - right);
  const middle = Math.floor(sorted.length / 2);
  return sorted.length % 2
    ? sorted[middle]
    : (sorted[middle - 1] + sorted[middle]) / 2;
}

function recallAt(rankings, expectedTitles, k) {
  const hits = rankings.reduce(
    (sum, ranking, index) =>
      sum +
      (ranking.slice(0, k).includes(expectedTitles[index]) ? 1 : 0),
    0,
  );
  return hits / rankings.length;
}

function meanReciprocalRank(rankings, expectedTitles) {
  const reciprocalRanks = rankings.map((ranking, index) => {
    const rank = ranking.indexOf(expectedTitles[index]);
    return rank >= 0 ? 1 / (rank + 1) : 0;
  });
  return (
    reciprocalRanks.reduce((sum, value) => sum + value, 0) /
    reciprocalRanks.length
  );
}

function ndcgAt(rankings, expectedTitles, k) {
  const scores = rankings.map((ranking, index) => {
    const rank = ranking.slice(0, k).indexOf(expectedTitles[index]);
    return rank >= 0 ? 1 / Math.log2(rank + 2) : 0;
  });
  return scores.reduce((sum, value) => sum + value, 0) / scores.length;
}

const modelClient = new ModelClient({
  onMessage(message) {
    if (message.type === "model-progress") {
      setStatus(
        `下载 ${message.file} · ${Math.round((message.progress || 0) * 100)}%`,
      );
    } else if (message.type === "fallback") {
      setStatus("WebGPU 初始化失败，切换到 WASM 继续评测");
    }
  },
});

try {
  const [documentsResponse, queriesResponse] = await Promise.all([
    fetch("/sample-documents.json"),
    fetch("/evaluation-queries.json"),
  ]);
  const documents = await documentsResponse.json();
  const queries = await queriesResponse.json();
  const titles = documents.map((document) => document.title);

  setStatus(`加载 ${dtype.toUpperCase()} 模型`);
  const model = await modelClient.load(backend, dtype);
  setStatus("向量化评测文档");
  const documentStart = performance.now();
  const documentEmbeddings = await modelClient.embed(
    documents.map((document) => document.text),
    batchSize,
  );
  const documentEmbeddingMs = performance.now() - documentStart;

  const rankings = [];
  const topResults = [];
  const queryLatencies = [];
  for (let index = 0; index < queries.length; index += 1) {
    setStatus(`评测查询 ${index + 1}/${queries.length}`);
    const queryStart = performance.now();
    const queryEmbedding = await modelClient.embed([queries[index].query], 1);
    queryLatencies.push(performance.now() - queryStart);
    const scored = documentEmbeddings.embeddings
      .map((embedding, documentIndex) => ({
        title: titles[documentIndex],
        score: cosine(queryEmbedding.embeddings[0], embedding),
      }))
      .sort((left, right) => right.score - left.score);
    rankings.push(scored.map((item) => item.title));
    topResults.push({
      query: queries[index].query,
      expectedTitle: queries[index].expectedTitle,
      top3: scored.slice(0, 3),
    });
  }

  const expectedTitles = queries.map((query) => query.expectedTitle);
  const result = {
    schemaVersion: 1,
    timestamp: new Date().toISOString(),
    browser: navigator.userAgent,
    model: {
      id: model.modelId,
      revision: model.revision,
      backend: model.backend,
      dtype: model.dtype,
      dimension: model.dimension,
      webgpuAvailable: model.webgpuAvailable,
      gpuAdapter: model.gpuAdapter,
      loadMs: model.loadMs,
      warmupMs: model.warmupMs,
      downloadedBytes: model.downloadedBytes,
    },
    dataset: {
      documentCount: documents.length,
      queryCount: queries.length,
      batchSize,
      topK: 3,
    },
    timings: {
      documentEmbeddingMs,
      documentThroughputPerSecond:
        (documents.length * 1_000) / Math.max(documentEmbeddingMs, 0.001),
      queryEmbeddingMedianMs: median(queryLatencies),
      queryEmbeddingSamplesMs: queryLatencies,
    },
    quality: {
      recallAt1: recallAt(rankings, expectedTitles, 1),
      recallAt3: recallAt(rankings, expectedTitles, 3),
      recallAt5: recallAt(rankings, expectedTitles, 5),
      mrrAt5: meanReciprocalRank(rankings, expectedTitles),
      ndcgAt5: ndcgAt(rankings, expectedTitles, 5),
    },
    topResults,
  };

  window.__QUALITY_BENCHMARK__ = result;
  document.body.dataset.status = "complete";
  setStatus("评测完成");
  outputElement.textContent = JSON.stringify(result, null, 2);
} catch (error) {
  window.__QUALITY_BENCHMARK__ = {
    ok: false,
    error: error?.message || String(error),
  };
  document.body.dataset.status = "error";
  setStatus("评测失败");
  outputElement.textContent = error?.stack || String(error);
}
