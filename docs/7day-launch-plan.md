# 7 天上线计划（纠正版）

权威产品定义：[`北极星.md`](./北极星.md)。  
PRD v1.1 仍作技术约束（License、Coze、RAGFlow、多租户壳），**其中电缆/企微催办首发闭环作废**，不按那条故事排期。

**你要做的项目：** 扣子（Coze Studio）做 Agent 编排底座 + RAGFlow 做知识 + **你自己的白标 UI** 包在外面，做成可对外交付的产品。

栈已锁定：壳 API = **Go + Gin**；控制台 = React + TS；数据 = Postgres / Redis / MinIO。

## 1. D7「上线」是什么

一台机器上，别人打开的是 **你的控制台**，不是扣子官方后台、也不是 RAGFlow 原生页。

1. Compose（或脚本）拉起：Postgres/Redis/MinIO + **Coze Studio** + **RAGFlow** + 你的 API/控制台。
2. 控制台可换 Logo / 产品名 / 主题色（白标）。
3. 在你的 UI 里：选一个 Bot → 对话；回答来自 **扣子工作流**，需要资料时走 **RAGFlow**，页面能看到引用。
4. 租户逻辑隔离：租户 A 的 Bot / 知识库，租户 B 进不去（壳上 `tenant_id` 映射 Coze workspace + RAGFlow dataset）。
5. 红线：不用 Dify/n8n/FastGPT/MaxKB。

## 2. 7 天不做

| 不做 | 说明 |
|------|------|
| 电缆询价、催办销售、企微长连接当主路径 | 不是本产品 |
| 把扣子 / RAGFlow 原生 UI 当对外产品 | 你要自己的壳 |
| 完整计费、飞书、K8s、信创 | 上线之后 |
| 一次做完「行业模板市场」 | 先 1 个通用 Demo Agent |

企微渠道可以后挂（channel-gateway 已有占位），**不挡这 7 天**。

## 3. 架构（纠正后）

```
用户 ──► 你的控制台（白标 UI）
              │
              ▼
         apps/api 产品壳
         租户 · 品牌 · Bot 绑定
         EngineBinding: coze_space / rag_dataset
              │
      ┌───────┴───────┐
      ▼               ▼
 Coze Studio      RAGFlow
 Agent/工作流      解析/检索/引用
 Apache 2.0       Apache 2.0
```

壳不替代扣子画布：搭建者仍可在扣子里画 Agent（或你后续把关键配置收进自己的 UI）。对外用户只进你的页面。

## 4. 逐日

### Day 1 — 口径与壳（已部分完成）

- 文档改成「白标 Agent = 扣子 + RAGFlow + 自研 UI」
- 现有 API 健康检查、租户 seed、白标字段保留（这是壳，不是电缆业务）
- 去掉产品叙事里的电缆询价

**DoD：** 任何人读 README / 北极星 都不会以为这是电缆项目。

### Day 2 — 白标控制台骨架（你要漂亮 UI 的底）

控制台主路径改成产品页，而不是「催办任务表」：

- 首页：我的 Agent（名称、状态、绑定的扣子 Bot / 知识库）
- 对话页：输入框 + 消息流（先 mock，接口形状按真扣子）
- 设置页：Logo、产品名、主题色
- 视觉：按 Ant Design Pro 后台质感铺布局（你后面可以再换皮肤）

**DoD：** 不看扣子后台，也能在你的域名感页面里完成一次对话（允许回答仍是 mock）。

### Day 3 — 真拉起扣子底座

- 按 [coze-dev/coze-studio](https://github.com/coze-dev/coze-studio) 官方 compose 起服务（默认 UI `:8888`）
- 注册管理员、配模型（DeepSeek / 通义 / GLM 任一 Key）
- 在扣子里建 **一个** Demo Agent（通用助手即可）
- `apps/api` 增加 `EngineBinding`：tenant → `coze_space_id` / `coze_bot_or_workflow_id`

**DoD：** 浏览器能打开扣子；API 能记下绑定。对外仍不把 `:8888` 当产品。

### Day 4 — 真拉起 RAGFlow

- 官方 RAGFlow compose（内存吃得比扣子凶，机器建议 8C32G；4C16G 能起就起，起不来就文档写清最低配）
- 建 dataset，上传 1～2 份说明文档（产品自己的介绍，**不是电缆规格书**）
- 壳记录 `ragflow_dataset_id`，按租户前缀隔离

**DoD：** RAGFlow API 能检索并返回带引用的片段。

### Day 5 — 接上：你的 UI → 扣子 → RAGFlow

运行时（对用户不可见）：

```
控制台发消息
  → API（验租户）
  → 需要知识：RAGFlow retrieve
  → 扣子运行 Agent/工作流（把检索结果当上下文）
  → 流式或一次返回到你的对话页
```

扣子暂时调不通就：UI 仍走同一 API，后端降级「RAG 片段 + 直连模型」，**不要把电缆 mock 催办接回来**。

**DoD：** 你的对话页一条真实问题，能看到扣子（或降级模型）的回答 + RAG 引用。

### Day 6 — 白标打磨

- 控制台去掉扣子/RAGFlow 商标露出（NOTICE 留在 docs，页面上是你的品牌）
- 登录先 dev；主题色/Logo 生效
- 两个租户：知识库与 Bot 绑定互不可见
- 反向代理：对外只暴露你的 console（扣子/RAG 管理口仅内网）

**DoD：** 演示链接看起来像「你的 Agent 产品」，不像开源套壳后台。

### Day 7 — 上线

- 一键脚本：中间件 → 扣子 → RAGFlow → api → console
- `docs/runbook.md`：端口、模型 Key、备份
- smoke：健康检查 + 对话一轮 + 引用非空
- 给你可转发的 URL 和演示账号

## 5. 机器与你要提供的

| 项 | 用途 |
|----|------|
| 建议 8C32G（最低 4C16G 先起扣子） | 扣子 + RAGFlow 同机 |
| Docker | 两个引擎官方都靠 compose |
| 模型 API Key | 扣子后台配模型 |
| （可选）域名 + TLS | 对外像产品 |

没有 Docker 的云开发机只能继续跑壳；**引擎必须在有 Docker 的主机上**。

## 6. 和现有代码怎么相处

已经写的 Mission / 催办 / `/dev/ingest` **降为内部可选**（以后做主动任务再用），不再当 7 天主路径。  
主路径改为：`控制台对话 → API → Coze + RAGFlow`。

电缆模板目录废弃，改为通用 `templates/default-agent`（扣子 Bot + RAG dataset 绑定说明）。
