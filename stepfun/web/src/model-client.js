export class ModelClient {
  constructor({ onMessage }) {
    this.worker = new Worker(
      new URL("./embedding-worker.js", import.meta.url),
      { type: "module", name: "local-embedding" },
    );
    this.pending = new Map();
    this.onMessage = onMessage;
    this.worker.addEventListener("message", (event) => {
      const data = event.data || {};
      if (data.requestId && this.pending.has(data.requestId)) {
        const pending = this.pending.get(data.requestId);
        if (data.type === "error") {
          this.pending.delete(data.requestId);
          pending.reject(new Error(data.message));
          this.onMessage?.(data);
          return;
        }
        if (data.type === pending.successType) {
          this.pending.delete(data.requestId);
          pending.resolve(data);
          this.onMessage?.(data);
          return;
        }
      }
      this.onMessage?.(data);
    });
  }

  #send(type, payload, successType) {
    const requestId = crypto.randomUUID();
    return new Promise((resolve, reject) => {
      this.pending.set(requestId, { resolve, reject, successType });
      this.worker.postMessage({ type, requestId, ...payload });
    });
  }

  load(backend = "auto", dtype = "fp16") {
    return this.#send("load", { backend, dtype }, "ready");
  }

  embed(texts, batchSize) {
    return this.#send("embed", { texts, batchSize }, "embedded");
  }
}
