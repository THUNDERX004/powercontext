# 运行证据

本目录保存可重复执行、可核对的验证结果。

| 文件 | 说明 |
| --- | --- |
| `powercontext-smoke.json` | 对真实 PowerContext 1.5.0 执行 Scope 创建、两次 Memory 写入和跨会话召回 |
| `powercontext-smoke.log` | 上述验证的控制台输出 |
| `submission-validation.json` | Dify DSL 图结构、工具节点、依赖身份、插件包哈希和安全检查 |
| `submission-validation.log` | 上述静态验证的控制台输出 |
| `dify-node-schema.json` | 使用 Dify 1.17.1 固定依赖 `graphon==0.7.0` 校验每个节点的数据模型 |
| `dify-node-schema.log` | 上述节点模型验证的控制台输出 |
| `workflow-logic-tests.log` | 从 DSL 提取四个 Python Code 节点后的单元测试输出 |
| `plugin-package.log` | Dify Plugin CLI 内部 checksum 与包文件 SHA-256 |

验证不会使用或写入真实账户凭据。PowerContext 的访问 Token 只从
`POWERCONTEXT_TOKEN` 环境变量读取，不会打印到日志或证据 JSON。

`powercontext-smoke.json` 本次记录来自本机 `127.0.0.1:18000` 的隔离实例，认证模式为
`loopback-unauthenticated`。正式部署应使用 `env/powercontext.env.example` 所示鉴权配置。

这些验证覆盖真实 PowerContext API、DSL 图结构、插件包身份、Dify 节点模型和 Code 节点逻辑。
完整 Dify Web 导入和浏览器体验仍需在 Docker Compose 部署的 Dify 1.17.1 环境中执行；
作品说明给出了对应步骤，且不把节点级验证误称为完整应用验收。
