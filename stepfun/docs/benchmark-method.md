# Benchmark Method

## Scope

Two kinds of measurements are intentionally separated:

1. `results/quality`: model-level FP32/FP16 embedding quality and batched vectorization on the pinned public model.
2. `results/evidence`: the actual application using Edge, local browser inference, seekdb writes, index refresh, hybrid retrieval, and collection isolation.

No performance number from a precomputed server-side embedding is used in either report.

## Environment

- Date: 2026-11-04
- OS: Windows 10.0.26200
- CPU: AMD Ryzen 7 9700X, 8 cores / 16 threads
- RAM: 32 GB
- GPU: NVIDIA GeForce RTX 5080; AMD Radeon integrated graphics also present
- Browser: Microsoft Edge 156.0.4314.58
- Node.js: 24.20.0
- seekdb: 1.4.0.0
- SDK: `seekdb` 1.4.0
- Transformers.js: 4.3.2

## Model Size

Only ONNX graph and external weight files are counted:

| Precision | Files | Bytes |
| --- | --- | ---: |
| FP32 | `model.onnx` + `model.onnx_data` | 90,318,300 |
| FP16 | `model_fp16.onnx` + `model_fp16.onnx_data` | 45,184,187 |

`compression ratio = 90,318,300 / 45,184,187 = 1.9989`.

## Quality Set

- 8 short documents from `public/sample-documents.json`.
- 8 Chinese/English queries from `public/evaluation-queries.json`.
- One binary relevant document per query.
- Metrics: Recall@1, Recall@3, Recall@5, MRR@5, nDCG@5.
- FP32 and FP16 each run 3 times in fresh pages using the same Edge binary and WebGPU provider.

The small, intentionally easy set is a regression guard rather than a broad semantic benchmark. A production submission should add a larger domain-specific relevance set.

## End-to-End Application Run

The browser harness:

1. Loads the page with a fresh browser context.
2. Waits for browser-local model initialization and verifies the actual backend label.
3. Imports eight sample documents and waits for all import requests to pass refresh visibility.
4. Runs the target query five times and takes the median.
5. Creates a temporary empty knowledge base, verifies no results leak from the original collection, switches back, and deletes the temporary collection.

For WASM verification, the harness starts Edge with GPU access disabled and additionally asserts that `navigator.gpu.requestAdapter()` yields no adapter. The UI must report `WASM · FP16`, not claim WebGPU.

## Timing Boundaries

- Document vectorization: browser Worker model call for the eight-document batch.
- Query vectorization: browser Worker model call for one query.
- seekdb retrieval: SDK set-variable + `DBMS_HYBRID_SEARCH` + row materialization returned to the API.
- End-to-end: query submission through local query embedding, HTTP, seekdb hybrid retrieval, and one animation-frame DOM render.
- First load: model/tokenizer cache lookup and ONNX session initialization, including network download on a cold browser profile.
- Warmed request: an already initialized model used for subsequent embedding calls.

The original samples are retained in JSON so medians can be recomputed.

## Raw Evidence

- `results/quality/summary-auto.json`: FP32/FP16 WebGPU aggregate and deltas.
- `results/quality/quality-fp32-auto.json`: three FP32 WebGPU runs.
- `results/quality/quality-fp16-auto.json`: three FP16 WebGPU runs.
- `results/quality/summary-wasm.json`: FP16 WASM aggregate.
- `results/quality/quality-fp16-wasm.json`: three FP16 WASM runs.
- `results/evidence/browser-smoke-webgpu.json`: full application WebGPU run.
- `results/evidence/browser-smoke-wasm.json`: full application automatic WASM run.

Re-run with:

```powershell
$env:QUALITY_REPEATS = "3"
npm run benchmark:quality

$env:QUALITY_BACKEND = "wasm"
$env:QUALITY_DTYPES = "fp16"
npm run benchmark:quality

npm run test:browser
$env:STEPFUN_DISABLE_WEBGPU = "1"
npm run test:browser
```
