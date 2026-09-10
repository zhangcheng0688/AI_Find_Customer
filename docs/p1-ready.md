# 扣子 / RAGFlow 接入清单

主路径是 **Coze Studio + RAGFlow**。企微后挂，不挡白标 Agent 上线。密钥禁止进 Git。

## Coze Studio（扣子底座）

官方：https://github.com/coze-dev/coze-studio （Apache 2.0）  
本机默认 UI：`http://localhost:8888`（只给搭建者，不对外当产品）。

| 变量 | 说明 |
|------|------|
| `COZE_OPENAPI_BASE` | 开源 Studio API 根地址 |
| `COZE_WORKSPACE_ID` | 映射到租户的 workspace |
| `COZE_BOT_ID` / `COZE_WORKFLOW_ID` | Demo Agent |
| `COZE_PAT` 或等价 token | 调用凭证 |
| 模型 Key | 在扣子后台「模型管理」配置 |

## RAGFlow（知识底座）

| 变量 | 说明 |
|------|------|
| `RAGFLOW_BASE_URL` | API |
| `RAGFLOW_API_KEY` | 密钥 |
| `RAGFLOW_DATASET_ID` | 租户知识库 |
| `RAGFLOW_DATASET_PREFIX` | 多租户前缀 |

灌库用 **你的产品说明 / FAQ**，不要灌电缆规格书。

## 模型

| 变量 | 说明 |
|------|------|
| `LLM_BASE_URL` | OpenAI 兼容（扣子也可直接配） |
| `LLM_API_KEY` | DeepSeek / 通义 / GLM 任一 |

## 企微（可选，非 7 天主路径）

| 变量 | 说明 |
|------|------|
| `WECOM_CORP_ID` | 企业 ID |
| `WECOM_BOT_SECRET` / `WECOM_BOT_ID` | 机器人凭证 |
