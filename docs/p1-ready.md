# P1 还缺什么（不要在未明确时实现真企微）

## 真企微长连接

| 变量 | 说明 |
|------|------|
| `WECOM_CORP_ID` | 企业 ID |
| `WECOM_BOT_SECRET` / `WECOM_BOT_ID` | 智能机器人凭证（以官方文档为准） |
| `WECOM_TOKEN` | 回调验签（若走回调而非长连接） |

P0 用 `POST /dev/ingest` 代替。密钥禁止进 Git。

## Coze Studio

| 变量 | 说明 |
|------|------|
| `COZE_OPENAPI_BASE` | 开源 Studio OpenAPI 地址 |
| `COZE_WORKSPACE_ID` | 映射到租户的 workspace |
| `COZE_WORKFLOW_ID` | 询价报价工作流 |
| `COZE_PAT` 或等价 token | 调用凭证 |

没有则 API 继续 `orchestrator=mock`。

## RAGFlow

| 变量 | 说明 |
|------|------|
| `RAGFLOW_BASE_URL` | API |
| `RAGFLOW_API_KEY` | 密钥 |
| `RAGFLOW_DATASET_PREFIX` | 租户隔离前缀 |

## 模型

| 变量 | 说明 |
|------|------|
| `LLM_BASE_URL` | OpenAI 兼容 |
| `LLM_API_KEY` | DeepSeek / 通义 / GLM 任一 |

## Activepieces（可选）

只用 MIT 核心。催办 7 天内走 API 内置 chaser；接 AP 时需要 `AP_API_URL` + 项目 ID。禁用 `packages/ee`。
