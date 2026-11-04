import "./styles.css";
import { api } from "./api.js";
import {
  chunkText,
  formatDuration,
  inferTitle,
  normalizeDocumentText,
  sha256Hex,
  titleFromFilename,
} from "./lib/text.js";
import { ModelClient } from "./model-client.js";

const STORAGE_KEYS = {
  activeKb: "stepfun.activeKb",
  backend: "stepfun.backend",
  batchSize: "stepfun.batchSize",
};

const state = {
  config: null,
  health: null,
  knowledgeBases: [],
  documents: [],
  activeKbId: localStorage.getItem(STORAGE_KEYS.activeKb),
  backendPreference: localStorage.getItem(STORAGE_KEYS.backend) || "auto",
  batchSize: Number(localStorage.getItem(STORAGE_KEYS.batchSize) || 16),
  model: null,
  modelLoading: false,
  importInProgress: false,
  searchInProgress: false,
  lastTrace: null,
  importHistory: [],
};

const elementIds = [
  "runtimeStatus",
  "runtimeStatusText",
  "dbStatus",
  "dbStatusText",
  "settingsButton",
  "kbList",
  "documentList",
  "documentCount",
  "sampleButton",
  "dropZone",
  "fileInput",
  "pasteTitle",
  "pasteText",
  "importProgress",
  "importStage",
  "importPercent",
  "importBar",
  "importDetail",
  "searchForm",
  "searchInput",
  "searchButton",
  "timingStrip",
  "embeddingTime",
  "searchTime",
  "totalTime",
  "exportTraceButton",
  "resultsList",
  "modelDialog",
  "runtimeDiagnostics",
  "batchSizeSelect",
  "reloadModelButton",
  "newKbDialog",
  "newKbForm",
  "newKbName",
  "toastRegion",
];

const elements = Object.fromEntries(
  elementIds.map((id) => [id, document.getElementById(id)]),
);

const modelClient = new ModelClient({ onMessage: handleWorkerMessage });

function showToast(message, kind = "info") {
  const toast = document.createElement("div");
  toast.className = `toast toast-${kind}`;
  toast.textContent = message;
  elements.toastRegion.append(toast);
  requestAnimationFrame(() => toast.classList.add("visible"));
  setTimeout(() => {
    toast.classList.remove("visible");
    setTimeout(() => toast.remove(), 250);
  }, 4_200);
}

function setPill(element, textElement, text, status) {
  element.className = `status-pill status-${status}`;
  textElement.textContent = text;
}

function setDbStatus(connected, detail) {
  setPill(
    elements.dbStatus,
    elements.dbStatusText,
    connected ? `seekdb · ${detail}` : "seekdb 未连接",
    connected ? "ready" : "error",
  );
}

function setRuntimeStatus(status, label) {
  setPill(elements.runtimeStatus, elements.runtimeStatusText, label, status);
}

function activeKnowledgeBase() {
  return state.knowledgeBases.find((item) => item.id === state.activeKbId);
}

function setActiveKb(kbId) {
  state.activeKbId = kbId;
  if (kbId) {
    localStorage.setItem(STORAGE_KEYS.activeKb, kbId);
  } else {
    localStorage.removeItem(STORAGE_KEYS.activeKb);
  }
  renderKnowledgeBases();
  loadDocuments().catch((error) => showToast(error.message, "error"));
}

function renderKnowledgeBases() {
  elements.kbList.replaceChildren();
  if (!state.knowledgeBases.length) {
    const empty = document.createElement("p");
    empty.className = "empty-copy";
    empty.textContent = "还没有知识库，点击 + 创建。";
    elements.kbList.append(empty);
    return;
  }

  for (const kb of state.knowledgeBases) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `kb-item${kb.id === state.activeKbId ? " active" : ""}`;
    button.addEventListener("click", () => setActiveKb(kb.id));

    const mark = document.createElement("span");
    mark.className = "kb-glyph";
    mark.textContent = kb.name.slice(0, 1).toUpperCase();

    const copy = document.createElement("span");
    copy.className = "kb-copy";
    const name = document.createElement("strong");
    name.textContent = kb.name;
    const meta = document.createElement("small");
    meta.textContent = `${kb.documentCount} 文档 · ${kb.chunkCount} 分块`;
    copy.append(name, meta);

    const arrow = document.createElement("span");
    arrow.className = "kb-arrow";
    arrow.textContent = "↗";
    button.append(mark, copy, arrow);
    elements.kbList.append(button);
  }
}

function renderDocuments() {
  elements.documentList.replaceChildren();
  elements.documentCount.textContent = String(state.documents.length);
  if (!state.documents.length) {
    const empty = document.createElement("p");
    empty.className = "empty-copy";
    empty.textContent = state.activeKbId
      ? "导入第一份文本后，文档会出现在这里。"
      : "先创建一个知识库。";
    elements.documentList.append(empty);
    return;
  }

  for (const documentItem of state.documents) {
    const row = document.createElement("div");
    row.className = "document-item";

    const copy = document.createElement("div");
    const title = document.createElement("strong");
    title.textContent = documentItem.title;
    const meta = document.createElement("small");
    meta.textContent = `${documentItem.chunkCount} 分块 · ${documentItem.dtype.toUpperCase()}`;
    copy.append(title, meta);

    const remove = document.createElement("button");
    remove.type = "button";
    remove.className = "remove-document";
    remove.title = "删除文档";
    remove.setAttribute("aria-label", `删除 ${documentItem.title}`);
    remove.textContent = "×";
    remove.addEventListener("click", () => deleteDocument(documentItem));
    row.append(copy, remove);
    elements.documentList.append(row);
  }
}

async function refreshKnowledgeBases() {
  const response = await api.knowledgeBases();
  state.knowledgeBases = response.items;
  if (
    !state.activeKbId ||
    !state.knowledgeBases.some((item) => item.id === state.activeKbId)
  ) {
    state.activeKbId = state.knowledgeBases[0]?.id || null;
  }
  renderKnowledgeBases();
  return state.knowledgeBases;
}

async function loadDocuments() {
  if (!state.activeKbId) {
    state.documents = [];
    renderDocuments();
    return;
  }
  const response = await api.documents(state.activeKbId);
  state.documents = response.items;
  renderDocuments();
}

async function createKnowledgeBase(name, { silent = false } = {}) {
  const kb = await api.createKnowledgeBase(name);
  await refreshKnowledgeBases();
  setActiveKb(kb.id);
  if (!silent) {
    showToast(`已创建知识库「${kb.name}」`, "success");
  }
  return kb;
}

async function deleteDocument(documentItem) {
  if (!state.activeKbId) {
    return;
  }
  if (!window.confirm(`删除「${documentItem.title}」及其全部分块？`)) {
    return;
  }
  try {
    await api.deleteDocument(state.activeKbId, documentItem.id);
    await Promise.all([refreshKnowledgeBases(), loadDocuments()]);
    showToast("文档已从 seekdb 删除", "success");
  } catch (error) {
    showToast(error.message, "error");
  }
}

function handleWorkerMessage(message) {
  if (message.type === "model-status") {
    setRuntimeStatus(
      "loading",
      message.backend === "webgpu"
        ? "加载 WebGPU · FP16"
        : "加载 WASM · FP16",
    );
    updateImportProgress({
      stage: "加载本地向量模型",
      percent: 0,
      detail:
        message.backend === "webgpu"
          ? "已选择 WebGPU 后端，正在下载并初始化 FP16 权重。"
          : "WebGPU 不可用或已手动选择 WASM，正在初始化 FP16 权重。",
    });
    return;
  }

  if (message.type === "model-progress") {
    const percent = Math.round((message.progress || 0) * 100);
    updateImportProgress({
      stage: "下载并缓存模型",
      percent,
      detail: `${message.file} · ${formatBytes(message.loaded)} / ${formatBytes(message.total)}`,
    });
    return;
  }

  if (message.type === "fallback") {
    showToast("WebGPU 初始化失败，已自动降级到 WASM", "warning");
    setRuntimeStatus("loading", "自动降级 WASM · FP16");
    return;
  }

  if (message.type === "ready") {
    state.model = message;
    state.modelLoading = false;
    state.backendPreference =
      message.backend === "wasm" &&
      state.backendPreference === "webgpu"
        ? "wasm"
        : state.backendPreference;
    setRuntimeStatus(
      "ready",
      `${message.backend === "webgpu" ? "WebGPU" : "WASM"} · FP16`,
    );
    updateRuntimeDiagnostics(message);
    hideImportProgress();
    showToast(
      `本地模型已就绪 · ${message.backend === "webgpu" ? "WebGPU" : "WASM"}`,
      "success",
    );
    return;
  }

  if (message.type === "embedding-progress") {
    const percent = Math.round(
      (message.completed / Math.max(1, message.total)) * 100,
    );
    updateImportProgress({
      stage: `本地向量化 ${message.completed}/${message.total}`,
      percent,
      detail: `当前批次 ${formatDuration(message.batchMs)} · 累计 ${formatDuration(message.elapsedMs)}`,
    });
    return;
  }

  if (message.type === "error") {
    state.modelLoading = false;
    setRuntimeStatus("error", "本地模型不可用");
    updateImportProgress({
      stage: "模型初始化失败",
      percent: 0,
      detail: message.message,
      error: true,
    });
    showToast(`模型加载失败：${message.message}`, "error");
  }
}

async function loadModel(backend = state.backendPreference) {
  if (state.modelLoading) {
    return;
  }
  state.modelLoading = true;
  state.model = null;
  setRuntimeStatus("loading", "初始化本地模型");
  updateImportProgress({
    stage: "检测浏览器能力",
    percent: 0,
    detail: "正在检查 WebGPU，并准备浏览器本地 ONNX 推理。",
  });
  try {
    await modelClient.load(backend);
  } catch (error) {
    state.modelLoading = false;
    throw error;
  }
}

function updateImportProgress({ stage, percent, detail, error = false }) {
  elements.importProgress.hidden = false;
  elements.importProgress.classList.toggle("is-error", error);
  elements.importStage.textContent = stage;
  elements.importPercent.textContent = `${Math.max(0, Math.min(100, Math.round(percent)))}%`;
  elements.importBar.style.width = `${Math.max(0, Math.min(100, percent))}%`;
  elements.importDetail.textContent = detail;
}

function hideImportProgress() {
  if (!state.importInProgress) {
    elements.importProgress.hidden = true;
    elements.importProgress.classList.remove("is-error");
  }
}

function formatBytes(bytes) {
  if (!bytes) {
    return "0 B";
  }
  const units = ["B", "KB", "MB", "GB"];
  const power = Math.min(
    Math.floor(Math.log(bytes) / Math.log(1_024)),
    units.length - 1,
  );
  return `${(bytes / 1_024 ** power).toFixed(power > 1 ? 1 : 0)} ${units[power]}`;
}

async function ensureReady() {
  if (!state.activeKbId) {
    const kb = await createKnowledgeBase("我的知识库", { silent: true });
    state.activeKbId = kb.id;
  }
  if (!state.model) {
    showToast("正在等待本地模型初始化", "warning");
    throw new Error("The local embedding model is still loading");
  }
}

async function importDocument(
  { title, sourceName, text },
  { notifySuccess = true } = {},
) {
  await ensureReady();
  const normalized = normalizeDocumentText(text);
  if (!normalized) {
    throw new Error("Document is empty");
  }
  if (normalized.length > 200_000) {
    throw new Error("Single document exceeds the 200,000 character UI limit");
  }

  const chunks = chunkText(normalized, {
    maxChars: 1_200,
    overlapChars: 120,
  });
  if (!chunks.length) {
    throw new Error("No searchable text chunks were produced");
  }
  if (chunks.length > (state.config?.limits.maxChunksPerDocument || 512)) {
    throw new Error("Document produces too many chunks");
  }

  const contentHash = await sha256Hex(normalized);
  const embedStart = performance.now();
  updateImportProgress({
    stage: `准备 ${chunks.length} 个文本分块`,
    percent: 0,
    detail: `本地模型 ${state.model.backend.toUpperCase()} · FP16 · 批大小 ${state.batchSize}`,
  });
  const embedded = await modelClient.embed(
    chunks.map((chunk) => chunk.text),
    state.batchSize,
  );
  const embeddingWallMs = performance.now() - embedStart;

  updateImportProgress({
    stage: "写入 seekdb 并刷新索引",
    percent: 96,
    detail: "服务端正在 upsert 原文、向量与元数据，并等待索引可见。",
  });
  const imported = await api.importDocument(state.activeKbId, {
    document: {
      title: title.slice(0, 200),
      sourceName: sourceName.slice(0, 240),
      contentHash,
      chunks,
    },
    embeddings: embedded.embeddings,
    model: {
      id: embedded.modelId,
      revision: embedded.revision,
      dtype: embedded.dtype,
      backend: embedded.backend,
    },
  });

  await Promise.all([refreshKnowledgeBases(), loadDocuments()]);
  const importTrace = {
    ...imported,
    model: {
      id: embedded.modelId,
      revision: embedded.revision,
      dtype: embedded.dtype,
      backend: embedded.backend,
    },
    timings: {
      ...imported.timings,
      embeddingMs: embedded.elapsedMs,
      embeddingWallMs,
      throughput: embedded.throughput,
    },
  };
  state.importHistory.push(importTrace);
  if (state.importHistory.length > 50) {
    state.importHistory.shift();
  }
  updateImportProgress({
    stage: "导入完成",
    percent: 100,
    detail: `${imported.chunkCount} 个分块已写入且可检索。`,
  });
  setTimeout(hideImportProgress, 900);
  if (notifySuccess) {
    showToast(`「${imported.title}」已写入 seekdb`, "success");
  }
  return importTrace;
}

async function importFiles(files) {
  if (state.importInProgress) {
    showToast("已有导入任务正在进行", "warning");
    return;
  }
  const selected = Array.from(files).slice(0, 24);
  if (!selected.length) {
    return;
  }
  state.importInProgress = true;
  let importedCount = 0;
  try {
    for (let index = 0; index < selected.length; index += 1) {
      const file = selected[index];
      if (file.size > 2_000_000) {
        showToast(`跳过过大的文件：${file.name}`, "warning");
        continue;
      }
      updateImportProgress({
        stage: `读取文件 ${index + 1}/${selected.length}`,
        percent: 1,
        detail: file.name,
      });
      const text = await file.text();
      await importDocument({
        title: titleFromFilename(file.name) || inferTitle(text),
        sourceName: file.name,
        text,
      }, { notifySuccess: false });
      importedCount += 1;
    }
    if (importedCount > 0) {
      showToast(`已导入 ${importedCount} 份文件`, "success");
    }
  } catch (error) {
    updateImportProgress({
      stage: "导入失败",
      percent: 100,
      detail: error.message,
      error: true,
    });
    showToast(error.message, "error");
  } finally {
    state.importInProgress = false;
    elements.fileInput.value = "";
    setTimeout(hideImportProgress, 1_200);
  }
}

async function importPaste() {
  if (state.importInProgress) {
    showToast("已有导入任务正在进行", "warning");
    return;
  }
  const text = elements.pasteText.value;
  if (!normalizeDocumentText(text)) {
    showToast("请先粘贴正文", "warning");
    return;
  }
  state.importInProgress = true;
  try {
    await importDocument(
      {
        title: elements.pasteTitle.value.trim() || inferTitle(text),
        sourceName: "粘贴文本",
        text,
      },
      { notifySuccess: true },
    );
    elements.pasteText.value = "";
    elements.pasteTitle.value = "";
  } catch (error) {
    updateImportProgress({
      stage: "导入失败",
      percent: 100,
      detail: error.message,
      error: true,
    });
    showToast(error.message, "error");
  } finally {
    state.importInProgress = false;
    setTimeout(hideImportProgress, 1_200);
  }
}

async function loadSamples() {
  if (state.importInProgress) {
    showToast("请等待当前导入结束", "warning");
    return;
  }
  state.importInProgress = true;
  try {
    const samples = await api.sampleDocuments();
    if (!Array.isArray(samples) || !samples.length) {
      throw new Error("示例数据为空");
    }
    for (let index = 0; index < samples.length; index += 1) {
      const sample = samples[index];
      updateImportProgress({
        stage: `导入示例 ${index + 1}/${samples.length}`,
        percent: 1,
        detail: sample.title,
      });
      await importDocument(sample, { notifySuccess: false });
    }
    showToast(`已导入 ${samples.length} 份示例文档`, "success");
  } catch (error) {
    updateImportProgress({
      stage: "示例导入失败",
      percent: 100,
      detail: error.message,
      error: true,
    });
    showToast(error.message, "error");
  } finally {
    state.importInProgress = false;
    setTimeout(hideImportProgress, 1_200);
  }
}

function highlight(text, query) {
  const fragment = document.createDocumentFragment();
  const tokens = Array.from(
    new Set(
      query
        .normalize("NFKC")
        .split(/[^\p{L}\p{N}]+/u)
        .filter((token) => token.length >= 2),
    ),
  ).slice(0, 12);
  if (!tokens.length) {
    fragment.append(document.createTextNode(text));
    return fragment;
  }

  const pattern = new RegExp(
    `(${tokens
      .sort((left, right) => right.length - left.length)
      .map((token) => token.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"))
      .join("|")})`,
    "giu",
  );
  let offset = 0;
  for (const match of text.matchAll(pattern)) {
    if (match.index > offset) {
      fragment.append(document.createTextNode(text.slice(offset, match.index)));
    }
    const mark = document.createElement("mark");
    mark.textContent = match[0];
    fragment.append(mark);
    offset = match.index + match[0].length;
  }
  fragment.append(document.createTextNode(text.slice(offset)));
  return fragment;
}

function renderResults(response, trace) {
  elements.resultsList.replaceChildren();
  elements.timingStrip.hidden = false;
  elements.embeddingTime.textContent = formatDuration(
    trace.timings.queryEmbeddingMs,
  );
  elements.searchTime.textContent = formatDuration(
    response.timings.databaseSearchMs,
  );
  elements.totalTime.textContent = formatDuration(trace.timings.endToEndMs);
  state.lastTrace = trace;

  if (!response.results.length) {
    const empty = document.createElement("div");
    empty.className = "empty-results";
    const symbol = document.createElement("span");
    symbol.className = "empty-index";
    symbol.textContent = "∅";
    const copy = document.createElement("p");
    copy.textContent =
      "数据库没有返回结果。请尝试更具体的词语，或先导入相关文档。";
    empty.append(symbol, copy);
    elements.resultsList.append(empty);
    return;
  }

  response.results.forEach((result, index) => {
    const metadata = result.metadata || {};
    const article = document.createElement("article");
    article.className = "result-card";

    const rank = document.createElement("div");
    rank.className = "result-rank";
    rank.textContent = String(index + 1).padStart(2, "0");

    const body = document.createElement("div");
    body.className = "result-body";
    const head = document.createElement("div");
    head.className = "result-head";
    const title = document.createElement("h3");
    title.textContent = metadata.title || "未命名文档";
    const source = document.createElement("span");
    source.textContent = metadata.sourceName || "未知来源";
    head.append(title, source);

    const snippet = document.createElement("p");
    snippet.append(highlight(result.document || "", response.query));

    const footer = document.createElement("div");
    footer.className = "result-footer";
    const chunk = document.createElement("span");
    chunk.textContent = `分块 ${Number(metadata.chunkIndex || 0) + 1} · ${metadata.charCount || result.document?.length || 0} 字符`;
    const score = document.createElement("span");
    score.textContent =
      result.distance == null
        ? "RRF ranked"
        : `score ${Number(result.distance).toFixed(5)}`;
    footer.append(chunk, score);

    body.append(head, snippet, footer);
    article.append(rank, body);
    elements.resultsList.append(article);
  });
}

async function search(query) {
  if (!query.trim() || state.searchInProgress) {
    return;
  }
  await ensureReady();
  state.searchInProgress = true;
  elements.searchButton.disabled = true;
  elements.searchButton.classList.add("busy");
  const overallStart = performance.now();
  try {
    const embedStart = performance.now();
    const embedded = await modelClient.embed([query.trim()], state.batchSize);
    const queryEmbeddingMs = performance.now() - embedStart;
    const response = await api.search(state.activeKbId, {
      query: query.trim(),
      queryEmbedding: embedded.embeddings[0],
      topK: 6,
    });
    const networkEndToEndMs = performance.now() - overallStart;
    const trace = {
      schemaVersion: 1,
      timestamp: new Date().toISOString(),
      query: query.trim(),
      knowledgeBase: activeKnowledgeBase()?.name || null,
      model: {
        id: embedded.modelId,
        revision: embedded.revision,
        dtype: embedded.dtype,
        backend: embedded.backend,
      },
      batchSize: 1,
      timings: {
        queryEmbeddingMs,
        databaseSearchMs: response.timings.databaseSearchMs,
        endToEndMs: networkEndToEndMs,
      },
      resultCount: response.results.length,
      resultIds: response.results.map((item) => item.id),
      engine: response.engine,
      ranker: response.ranker,
    };
    renderResults(response, trace);
    await new Promise((resolve) => requestAnimationFrame(resolve));
    trace.timings.endToEndMs = performance.now() - overallStart;
    elements.totalTime.textContent = formatDuration(trace.timings.endToEndMs);
    state.lastTrace = trace;
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    state.searchInProgress = false;
    elements.searchButton.disabled = false;
    elements.searchButton.classList.remove("busy");
  }
}

function exportTrace() {
  if (!state.lastTrace) {
    showToast("还没有可导出的检索轨迹", "warning");
    return;
  }
  const blob = new Blob([`${JSON.stringify(state.lastTrace, null, 2)}\n`], {
    type: "application/json",
  });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `stepfun-query-trace-${Date.now()}.json`;
  link.click();
  URL.revokeObjectURL(link.href);
}

function updateRuntimeDiagnostics(model) {
  const adapter = Boolean(navigator.gpu);
  elements.runtimeDiagnostics.innerHTML = "";
  const lines = [
    ["模型", model.modelId],
    ["Revision", model.revision.slice(0, 12)],
    ["实际后端", model.backend.toUpperCase()],
    ["权重精度", model.dtype.toUpperCase()],
    ["navigator.gpu", adapter ? "存在" : "不存在"],
    ["跨源隔离", globalThis.crossOriginIsolated ? "已启用" : "未启用"],
    ["预热延迟", formatDuration(model.warmupMs)],
  ];
  for (const [label, value] of lines) {
    const row = document.createElement("div");
    const left = document.createElement("span");
    const right = document.createElement("strong");
    left.textContent = label;
    right.textContent = value;
    row.append(left, right);
    elements.runtimeDiagnostics.append(row);
  }
}

function openModelSettings() {
  const radios = document.querySelectorAll(
    'input[name="backendPreference"]',
  );
  for (const radio of radios) {
    radio.checked = radio.value === state.backendPreference;
  }
  elements.batchSizeSelect.value = String(state.batchSize);
  elements.modelDialog.showModal();
}

async function reloadModelFromSettings() {
  state.backendPreference =
    document.querySelector('input[name="backendPreference"]:checked')?.value ||
    "auto";
  state.batchSize = Number(elements.batchSizeSelect.value);
  localStorage.setItem(STORAGE_KEYS.backend, state.backendPreference);
  localStorage.setItem(STORAGE_KEYS.batchSize, String(state.batchSize));
  elements.modelDialog.close();
  try {
    await loadModel(state.backendPreference);
  } catch (error) {
    showToast(error.message, "error");
  }
}

function bindEvents() {
  document.addEventListener("click", (event) => {
    const action = event.target.closest("[data-action]")?.dataset.action;
    if (action === "open-model-settings") {
      openModelSettings();
    } else if (action === "new-kb") {
      elements.newKbDialog.showModal();
      setTimeout(() => elements.newKbName.focus(), 0);
    } else if (action === "import-paste") {
      importPaste();
    } else if (action === "load-samples") {
      loadSamples();
    } else if (action === "reload-model") {
      reloadModelFromSettings();
    }
  });

  elements.dropZone.addEventListener("click", () => elements.fileInput.click());
  elements.dropZone.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      elements.fileInput.click();
    }
  });
  elements.fileInput.addEventListener("change", () =>
    importFiles(elements.fileInput.files),
  );
  for (const eventName of ["dragenter", "dragover"]) {
    elements.dropZone.addEventListener(eventName, (event) => {
      event.preventDefault();
      elements.dropZone.classList.add("dragging");
    });
  }
  for (const eventName of ["dragleave", "drop"]) {
    elements.dropZone.addEventListener(eventName, (event) => {
      event.preventDefault();
      elements.dropZone.classList.remove("dragging");
    });
  }
  elements.dropZone.addEventListener("drop", (event) => {
    importFiles(event.dataTransfer.files);
  });

  elements.searchForm.addEventListener("submit", (event) => {
    event.preventDefault();
    search(elements.searchInput.value);
  });
  document.querySelectorAll("[data-query]").forEach((button) => {
    button.addEventListener("click", () => {
      elements.searchInput.value = button.dataset.query;
      search(button.dataset.query);
    });
  });
  elements.exportTraceButton.addEventListener("click", exportTrace);

  elements.newKbForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const name = elements.newKbName.value.trim();
    if (!name) {
      return;
    }
    try {
      await createKnowledgeBase(name);
      elements.newKbForm.reset();
      elements.newKbDialog.close();
    } catch (error) {
      showToast(error.message, "error");
    }
  });
}

async function initialize() {
  globalThis.__stepfunDiagnostics = () => ({
    model: state.model,
    importHistory: state.importHistory,
    lastTrace: state.lastTrace,
    knowledgeBase: activeKnowledgeBase() || null,
    documentCount: state.documents.length,
  });
  bindEvents();
  renderDocuments();
  try {
    const [config, healthResponse] = await Promise.all([
      api.config(),
      api.health(),
    ]);
    state.config = config;
    state.health = healthResponse.database;
    setDbStatus(true, formatDuration(healthResponse.database.latencyMs));
    await refreshKnowledgeBases();
    if (!state.knowledgeBases.length) {
      await createKnowledgeBase("我的知识库", { silent: true });
    } else if (!state.activeKbId) {
      setActiveKb(state.knowledgeBases[0].id);
    } else {
      await loadDocuments();
    }
  } catch (error) {
    setDbStatus(false);
    setRuntimeStatus("error", "服务不可用");
    showToast(`无法连接应用服务或 seekdb：${error.message}`, "error");
    return;
  }

  try {
    await loadModel(state.backendPreference);
  } catch (error) {
    showToast(`本地模型初始化失败：${error.message}`, "error");
  }
}

initialize();
