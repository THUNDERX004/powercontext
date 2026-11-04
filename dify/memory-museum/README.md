# 记忆失物招领处

> 一家只收藏“没什么用、却舍不得忘”的小事博物馆。

访客告诉“灰灯馆长”一件不值得纪念的小事。馆长会把它变成一件有年代、有馆藏标签、
有讲解词，还有一点点私人报复意味的展品。更重要的是，下次再提到相关线索时，
PowerContext 会把旧展品找回来，于是新展品可以和旧展品组成“联动展”。

## 为什么好玩

- 输入零门槛：忘记在冰箱里的香菜、没发出去的一句话、掉进沙发缝的一枚硬币都可以参展。
- 反馈有反差：用户给出日常琐事，AI 用一本正经的博物馆语言把它重新命名。
- 记忆会回访：第二次提到“香菜”或“冰箱”时，馆长会认出旧展品，而不是重新失忆。
- 每次都有新钩子：展签、年代、馆藏部件、馆长附注和联动说明组成一张可分享的“入藏卡”。

## 技术分工

| 组成 | 在本作品中的实际职责 |
| --- | --- |
| Dify Chatflow | 接收聊天输入、敏感输入拦截、分支控制、调用 PowerContext、驱动 LLM、生成结构化展品并输出最终回答 |
| PowerContext `pc_prepare_context` | 在 LLM 前检索同一 Scope 中保存的旧展品，并把有界上下文注入 LLM 节点 |
| PowerContext `pc_remember` | 在每次成功策展后显式写入一条可再次检索的展品记忆；回答中显示真实 Artifact ID |
| OpenAI-API-compatible 模型 | 根据当前记忆和旧展品生成展签与讲解词 |

PowerContext 是本作品跨会话玩法的必要依赖：移除它以后，第二次访问将无法识别旧展品。
工作流在 Dify 运行记录中能直接看到两次工具调用、真实 `result.content` 和写入返回。

## 提交内容

| 路径 | 用途 |
| --- | --- |
| `dsl/memory-museum.yml` | 可直接导入 Dify 的 Chatflow DSL |
| `plugin/powercontext-0.0.1.difypkg` | 从 PowerContext v1.5.0 源码构建的官方 Dify 工具插件 |
| `plugin/SOURCE.md` | 插件来源、固定提交和校验值 |
| `env/powercontext.env.example` | PowerContext Server 配置模板，不含真实凭据 |
| `samples/session-1.md`、`samples/session-2.md` | 连续两轮体验步骤和预期表现 |
| `validation/validate_submission.py` | 检查 DSL 结构、图连通性、插件身份和包哈希 |
| `validation/powercontext_smoke.py` | 对真实 PowerContext Server 执行“写入 → 新查询召回 → 再写入”验证 |
| `evidence/` | 实际验证结果与运行日志 |

## 版本与依赖

| 组件 | 作品声明版本 |
| --- | --- |
| Dify | 1.17.1，Docker Compose 部署 |
| PowerContext Server | 1.5.0 |
| PowerContext Dify 插件 | `knqiufan/powercontext` 0.0.1，本地包随作品提交 |
| OpenAI-API-compatible 插件 | `langgenius/openai_api_compatible` 0.0.68 |
| 模型 | 任意支持 Chat Completions 的模型；示例 DSL 默认模型名 `gpt-4.1-mini` |
| 数据库 | PowerContext 默认 SQLite，基础验证不需要 Embedding 或 Rerank |

PowerContext 1.5.0 的本地基本记忆模式使用全文召回，无需额外模型凭据。
只有在希望增强语义召回时才需要给 PowerContext 配置 Embedding/Vector Search；
本作品不要求该增强配置。

## 最短运行步骤

### 1. 启动 PowerContext 1.5.0

Linux/macOS：

```bash
uv tool install --force "powercontext[cli,server]==1.5.0"
export POWERCONTEXT_HOME="$PWD/.powercontext"
export POWERCONTEXT_SERVER_HTTP_HOST=127.0.0.1
export POWERCONTEXT_SERVER_HTTP_PORT=8000
export POWERCONTEXT_SERVER_AUTH_ENABLED=true
export POWERCONTEXT_SERVER_AUTH_TOKEN='replace-with-a-long-random-token'
export POWERCONTEXT_SERVER_DATABASE_KIND=sqlite
powercontext server run --no-env-file
```

Windows PowerShell：

```powershell
uv tool install --force "powercontext[cli,server]==1.5.0"
$env:POWERCONTEXT_HOME = "$PWD\.powercontext"
$env:POWERCONTEXT_SERVER_HTTP_HOST = "127.0.0.1"
$env:POWERCONTEXT_SERVER_HTTP_PORT = "8000"
$env:POWERCONTEXT_SERVER_AUTH_ENABLED = "true"
$env:POWERCONTEXT_SERVER_AUTH_TOKEN = "replace-with-a-long-random-token"
$env:POWERCONTEXT_SERVER_DATABASE_KIND = "sqlite"
powercontext server run --no-env-file
```

检查服务：

```bash
curl --fail --silent --show-error http://127.0.0.1:8000/health/live
```

### 2. 创建一个应用专用 Scope

把下面的 `TOKEN` 换成上一步的 Server token。返回值中的 `scope_id` 要填入 Dify 插件配置。

```bash
curl --fail --silent --show-error \
  --header "Authorization: Bearer TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"title":"记忆失物招领处","summary":"Dify 作品中的跨会话展品记忆","idempotency_key":"memory-museum-prod"}' \
  http://127.0.0.1:8000/v1/scopes
```

Scope 是应用/团队的固定数据边界，不由普通聊天用户自动隔离。若需要服务不同用户，
请为每个授权边界使用独立 Scope、独立 PowerContext 凭证配置或独立部署。

### 3. 在 Dify 中安装两个插件

导入顺序如下：

1. 在 Dify 工作区的“插件 → 安装本地插件”中上传
   `plugin/powercontext-0.0.1.difypkg`。
2. 从 Dify Marketplace 安装 `OpenAI-API-compatible` 0.0.68。
3. 配置 OpenAI-API-compatible 的 Base URL、API Key 和模型。
4. 授权 PowerContext 工具提供方，字段建议如下：

| 字段 | 值 |
| --- | --- |
| Server URL | Dify 插件 daemon 能访问的 PowerContext 地址 |
| API token | 第 1 步设置的 Server token |
| Scope ID | 第 2 步返回的 `scope_id` |
| Binding external ID | 留空 |
| Max bytes | `8000` |
| HTTP timeout seconds | `10` |
| Generation timeout seconds | `120` |
| Allow private-network HTTP | Dify 使用容器访问宿主机 HTTP 服务时启用 |
| Context assembly | 留空 |

如果 Dify 以 Docker Compose 运行而 PowerContext 在宿主机运行，
插件中的 `127.0.0.1:8000` 指向插件容器自身，通常不能使用。可填写
`http://host.docker.internal:8000` 并启用 `allow_insecure_http`；
Linux 部署还需让插件 daemon 容器能够解析 `host.docker.internal`
（例如增加 `host-gateway` 映射），或改为填写宿主机在容器网络中的可达地址。

### 4. 导入 DSL

在 Dify 工作室选择“导入 DSL 文件”，导入 `dsl/memory-museum.yml`。

DSL 默认使用 `gpt-4.1-mini`。如果 OpenAI-API-compatible 中配置的是其他模型，
打开“灰灯馆长策展”LLM 节点，在模型选择器中重新选择实际模型，然后发布应用。

### 5. 体验

进入 Chatflow 应用，依次按 [第一场样例](samples/session-1.md) 和
[第二场样例](samples/session-2.md) 输入。第二次样例必须关联第一次的关键词，
这样才能稳定展示 PowerContext 的跨会话召回。

## 工作流结构

```text
聊天输入
  → 隐私/凭据输入拦截
  → IF 允许保存
      ├─ 否 → 友好提示，不写入记忆
      └─ 是 → pc_prepare_context
                → 归一化召回结果
                → 灰灯馆长 LLM（历史内容只作素材，不得作为指令）
                → 解析并降级修正展品 JSON
                → pc_remember
                → 加入真实 Artifact ID / 写入失败说明
                → Answer
```

工作流有两个明确定义的终点：

- 隐私拦截失败分支：告诉用户换一件不包含密码、Token、手机号、邮箱或身份证号的小事。
- 正常策展分支：即使在 `pc_remember` 返回 `error` 或 `unknown` 时，也保留已生成的展品，
  并明确提示“记忆未确认写入”，不会伪造成功或自动重试未知写入。

## 自动验证

PowerContext 真实读写：

```bash
python validation/powercontext_smoke.py \
  --base-url http://127.0.0.1:8000 \
  --output evidence/powercontext-smoke.json
```

若 Server 开启鉴权，先设置 `POWERCONTEXT_TOKEN` 环境变量；脚本不会打印该值。

DSL 与插件包静态检查：

```bash
python validation/validate_submission.py \
  --output evidence/submission-validation.json
```

使用 Dify 1.17.1 固定依赖 `graphon==0.7.0` 校验各节点数据模型：

```bash
python validation/validate_dify_nodes.py \
  --output evidence/dify-node-schema.json
```

三项验证的预期结果、真实运行日志和限制见 [evidence/README.md](evidence/README.md)。

## 已知限制

- Dify 1.17.1 的本地插件安装与 daemon 网络访问必须由部署者配置；插件包已随作品提供，
  但 Dify 本体不作为本目录的二进制产物重复提交。
- 本作品使用一个固定 Scope。它是应用/团队记忆边界，不自动区分每个聊天用户。
- PowerContext 基础模式使用全文召回。若两次输入完全没有共同关键词，可能正常返回空上下文；
  作品会把它呈现为“新展厅”，不会伪造旧展品。
- 模型必须稳定输出 JSON。DSL 内置解析失败降级，但输出质量仍会随模型能力变化。
- 隐私拦截是应用级最小防线，不能替代 Dify、PowerContext 和部署环境的访问控制。
