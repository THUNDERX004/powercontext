# 端侧 AI 推理性能优化与 seekdb 混合检索

## 方案

Local Lexicon 将“推理”和“检索”明确分层：Transformers.js 在浏览器 Worker 中运行 `onnx-community/all-MiniLM-L6-v2-ONNX`，完成文档与查询的 384 维 embedding；Node 服务只接收浏览器已算好的向量、原文和元数据，通过 `seekdb` SDK 写入独立 collection。查询时 `collection.hybridSearch()` 将全文条件、稠密查询向量和 RRF 参数交给 seekdb，数据库返回融合后的单一排序结果。

模型固定 revision `aff7a1dc4e8a1ea593e6ea21e95c22ef0a25966f`，Apache-2.0。应用先探测 `navigator.gpu.requestAdapter()`，可用时显式配置 WebGPU + FP16；适配器不存在、初始化失败或用户指定 WASM 时，以相同权重精度加载 WASM 后端。界面持续显示实际后端，不把“检测到 WebGPU”误报为“已使用 WebGPU”。

## 量化与质量

按 ONNX 图文件加外部权重文件统计：

| 精度 | 实测体积 | 压缩比 |
| --- | ---: | ---: |
| FP32 | 90,318,300 bytes | 1.000 |
| FP16 | 45,184,187 bytes | 1.9989 |

质量使用固定 8 文档、8 查询集，在同机 Edge 和 WebGPU 上分别计算 FP32/FP16 embedding 的稠密排序。重复 3 次，FP16 的 Recall@1、Recall@3、Recall@5、MRR@5、nDCG@5 均为 1.000，与 FP32 的变化均为 0。该集合用于提交前回归，不代表所有真实语料都能达到满分；后续可替换为更大领域集。

## 性能

测试环境：Windows 10.0.26200、AMD Ryzen 7 9700X（8C/16T）、32 GB RAM、NVIDIA RTX 5080、Microsoft Edge 156.0.4314.58、seekdb 1.4.0.0。8 篇文本、8 个分块。

| 配置 | 8 文档向量化（3 次中位数） | 吞吐 | 查询向量化（5 次中位数） | seekdb 检索（5 次中位数） | 端到端（5 次中位数） |
| --- | ---: | ---: | ---: | ---: | ---: |
| FP32 + WebGPU | 89.03 ms | 89.86 docs/s | 7.04 ms | — | — |
| FP16 + WebGPU | 83.83 ms | 95.43 docs/s | 7.27 ms | 4.58 ms | 25.15 ms |
| FP16 + WASM | 604.28 ms | 13.24 docs/s | 9.84 ms | 4.54 ms | 26.72 ms |

端到端计时从提交查询开始，包含本地 query embedding、HTTP、seekdb 混合检索和结果 DOM 渲染。首次加载与预热后请求分开保存：本机 FP16+WebGPU 首次模型/缓存加载 14.46 s、预热 191.24 ms；FP16+WASM 首次加载 12.86 s、预热 30.47 ms。网络与缓存状态会影响首次加载，因此不将其视为稳定模型性能。

## seekdb 数据设计

知识库目录和文档登记保存在 `stepfun_kb_catalog`、`stepfun_kb_documents`；每个知识库对应独立 `stepfun_kb_<id>` collection。collection 同时配置 `ik` 全文索引和 384 维 cosine HNSW。文档 SHA-256 作为文档 ID，`<sha256>:<chunkIndex>` 作为分块 ID；重复导入会 upsert 已存在分块并删除变短后的尾部旧分块。

写路径为：`upsert → refresh_index() → 按 documentId 过滤的向量可见性轮询 → 登记元数据`。验证失败不会报告导入成功。检索调用使用元数据过滤、全文 query、KNN 向量和 `rank.rrf`，没有客户端双路召回或结果回放。

## 结论

FP16 在本次评测集上未造成可观测质量下降，8 文档 WebGPU 吞吐比 FP32 基线高约 6.2%；WASM 路径完整可用，端到端比 WebGPU 高约 1.6 ms，主要差异在文档向量化吞吐。所有原始数据、截图和复现命令均随源码提交。
