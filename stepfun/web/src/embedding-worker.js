import { env, pipeline } from "@huggingface/transformers";

const MODEL_ID = "onnx-community/all-MiniLM-L6-v2-ONNX";
const MODEL_REVISION = "aff7a1dc4e8a1ea593e6ea21e95c22ef0a25966f";
const DIMENSION = 384;

env.allowLocalModels = false;
env.allowRemoteModels = true;
env.useBrowserCache = true;
if (env.backends?.onnx?.wasm) {
  env.backends.onnx.wasm.numThreads = 1;
  env.backends.onnx.wasm.proxy = false;
}

let extractor = null;
let activeBackend = null;
let activeDtype = null;
let loadingPromise = null;

function post(type, payload = {}) {
  self.postMessage({ type, ...payload });
}

async function inspectWebGPU() {
  if (!self.navigator?.gpu) {
    return { available: false, adapter: null };
  }
  try {
    const adapter = await self.navigator.gpu.requestAdapter();
    return {
      available: Boolean(adapter),
      adapter: adapter
        ? {
            vendor: adapter.info?.vendor || null,
            architecture: adapter.info?.architecture || null,
            device: adapter.info?.device || null,
            description: adapter.info?.description || null,
            isFallbackAdapter: adapter.info?.isFallbackAdapter ?? null,
          }
        : null,
    };
  } catch {
    return { available: false, adapter: null };
  }
}

function progressHandler(requestId) {
  return (event) => {
    if (!event || typeof event !== "object") {
      return;
    }
    if (event.status === "progress" || event.status === "download") {
      post("model-progress", {
        requestId,
        file: event.file || event.name || "model",
        progress: Number.isFinite(event.progress) ? event.progress : 0,
        loaded: Number.isFinite(event.loaded) ? event.loaded : 0,
        total: Number.isFinite(event.total) ? event.total : 0,
      });
    }
  };
}

async function loadPipeline(requestId, requestedBackend, requestedDtype = "fp16") {
  const dtype = requestedDtype === "fp32" ? "fp32" : "fp16";
  const desiredBackend =
    requestedBackend === "wasm"
      ? "wasm"
      : requestedBackend === "webgpu"
        ? "webgpu"
        : "auto";
  const requestedKey = `${desiredBackend}:${dtype}`;
  const activeKey =
    activeBackend && activeDtype ? `${activeBackend}:${activeDtype}` : null;
  if (extractor && activeKey === requestedKey) {
    post("ready", {
      requestId,
      backend: activeBackend,
      dtype: activeDtype,
      modelId: MODEL_ID,
      revision: MODEL_REVISION,
      reused: true,
    });
    return;
  }
  if (loadingPromise) {
    await loadingPromise;
    post("ready", {
      requestId,
      backend: activeBackend,
      dtype: activeDtype,
      modelId: MODEL_ID,
      revision: MODEL_REVISION,
      reused: true,
    });
    return;
  }

  loadingPromise = (async () => {
    if (extractor && activeKey !== requestedKey) {
      await extractor.dispose?.();
      extractor = null;
      activeBackend = null;
      activeDtype = null;
    }

    const loadStart = performance.now();
    const downloadProgress = new Map();
    const trackedProgress = (event) => {
      progressHandler(requestId)(event);
      const file = event?.file || event?.name;
      if (file && Number.isFinite(event.loaded)) {
        downloadProgress.set(file, event.loaded);
      }
    };
    const webgpuProbe = await inspectWebGPU();
    const webgpuAvailable = webgpuProbe.available;
    let backend =
      requestedBackend === "wasm"
        ? "wasm"
        : webgpuAvailable
          ? "webgpu"
          : "wasm";

    post("model-status", {
      requestId,
      phase: "loading",
      backend,
      webgpuAvailable,
      gpuAdapter: webgpuProbe.adapter,
      message:
        backend === "webgpu"
          ? "正在加载 WebGPU 模型"
          : "正在加载 WASM 模型",
    });

    try {
      extractor = await pipeline("feature-extraction", MODEL_ID, {
        revision: MODEL_REVISION,
        device: backend,
        dtype,
        progress_callback: trackedProgress,
      });
    } catch (webgpuError) {
      if (backend !== "webgpu") {
        throw webgpuError;
      }
      post("fallback", {
        requestId,
        from: "webgpu",
        to: "wasm",
        reason: webgpuError?.message || String(webgpuError),
      });
      backend = "wasm";
      extractor = await pipeline("feature-extraction", MODEL_ID, {
        revision: MODEL_REVISION,
        device: "wasm",
        dtype,
        progress_callback: trackedProgress,
      });
    }

    const warmupStart = performance.now();
    const warmup = await extractor("seekdb local retrieval warmup", {
      pooling: "mean",
      normalize: true,
    });
    if (warmup?.dims?.at(-1) !== DIMENSION) {
      throw new Error(`Unexpected model dimension: ${warmup?.dims}`);
    }
    const warmupMs = performance.now() - warmupStart;
    activeBackend = backend;
    activeDtype = dtype;
    post("ready", {
      requestId,
      backend,
      dtype,
      modelId: MODEL_ID,
      revision: MODEL_REVISION,
      dimension: DIMENSION,
      webgpuAvailable,
      gpuAdapter: webgpuProbe.adapter,
      warmupMs,
      loadMs: performance.now() - loadStart,
      downloadedBytes: Array.from(downloadProgress.values()).reduce(
        (sum, value) => sum + value,
        0,
      ),
      reused: false,
    });
  })();

  try {
    await loadingPromise;
  } finally {
    loadingPromise = null;
  }
}

async function embed(requestId, texts, batchSize) {
  if (!extractor || !activeBackend) {
    throw new Error("Embedding model is not ready");
  }
  if (!Array.isArray(texts) || texts.length === 0) {
    throw new Error("At least one text is required");
  }

  const size = Math.max(1, Math.min(32, Number(batchSize) || 16));
  const embeddings = [];
  const start = performance.now();
  for (let offset = 0; offset < texts.length; offset += size) {
    const batch = texts.slice(offset, offset + size);
    const batchStart = performance.now();
    const output = await extractor(batch, {
      pooling: "mean",
      normalize: true,
    });
    const rows = output.tolist();
    if (!Array.isArray(rows) || rows.length !== batch.length) {
      throw new Error("Unexpected embedding output shape");
    }
    for (const row of rows) {
      if (!Array.isArray(row) || row.length !== DIMENSION) {
        throw new Error(`Unexpected embedding dimension: ${row?.length}`);
      }
      embeddings.push(row);
    }

    post("embedding-progress", {
      requestId,
      completed: Math.min(offset + batch.length, texts.length),
      total: texts.length,
      batchMs: performance.now() - batchStart,
      elapsedMs: performance.now() - start,
    });
  }

  const elapsedMs = performance.now() - start;
  post("embedded", {
    requestId,
    embeddings,
    backend: activeBackend,
    dtype: activeDtype,
    modelId: MODEL_ID,
    revision: MODEL_REVISION,
    elapsedMs,
    throughput: (texts.length * 1_000) / Math.max(elapsedMs, 0.001),
  });
}

self.onmessage = async ({ data }) => {
  const { type, requestId } = data || {};
  try {
    if (type === "load") {
      await loadPipeline(
        requestId,
        data.backend || "auto",
        data.dtype || "fp16",
      );
    } else if (type === "embed") {
      await embed(requestId, data.texts, data.batchSize);
    } else {
      throw new Error(`Unknown worker command: ${type}`);
    }
  } catch (error) {
    post("error", {
      requestId,
      message: error?.message || String(error),
      stack: error?.stack || null,
    });
  }
};
