async function request(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: {
      ...(options.body ? { "Content-Type": "application/json" } : {}),
      ...options.headers,
    },
  });

  const contentType = response.headers.get("content-type") || "";
  const body = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const error = new Error(
      body?.error?.message || body || `HTTP ${response.status}`,
    );
    error.status = response.status;
    error.code = body?.error?.code;
    throw error;
  }
  return body;
}

export const api = {
  config: () => request("/api/config"),
  health: () => request("/api/health"),
  knowledgeBases: () => request("/api/knowledge-bases"),
  createKnowledgeBase: (name) =>
    request("/api/knowledge-bases", {
      method: "POST",
      body: JSON.stringify({ name }),
    }),
  deleteKnowledgeBase: (kbId) =>
    request(`/api/knowledge-bases/${encodeURIComponent(kbId)}`, {
      method: "DELETE",
    }),
  documents: (kbId) =>
    request(`/api/knowledge-bases/${encodeURIComponent(kbId)}/documents`),
  deleteDocument: (kbId, documentId) =>
    request(
      `/api/knowledge-bases/${encodeURIComponent(kbId)}/documents/${encodeURIComponent(documentId)}`,
      { method: "DELETE" },
    ),
  importDocument: (kbId, payload) =>
    request(`/api/knowledge-bases/${encodeURIComponent(kbId)}/documents`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  search: (kbId, payload) =>
    request(`/api/knowledge-bases/${encodeURIComponent(kbId)}/search`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  refresh: (kbId) =>
    request(`/api/knowledge-bases/${encodeURIComponent(kbId)}/refresh`, {
      method: "POST",
    }),
  sampleDocuments: async () => {
    const response = await fetch("/sample-documents.json");
    if (!response.ok) {
      throw new Error("Unable to load sample documents");
    }
    return response.json();
  },
};
