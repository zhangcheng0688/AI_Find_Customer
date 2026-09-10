# 7 天上线计划（冻结版）

权威需求：[`PRD与技术栈.md`](./PRD与技术栈.md) v1.1。栈已锁定：**Go + Gin** / React+TS / Postgres+Redis+MinIO。

PRD 原文 P1 是 **2 周** 打通企微闭环、P2 再 **3–4 周** 做完整多租户壳。7 天要「搭出来、上线」，必须把 **上线** 定义成可对外演示的试点，而不是把 P0–P2 全部做完。

## 1. D7「上线」是什么（验收口径）

试点环境（一台 4C16G + Compose，可公网或内网）必须同时满足：

1. **一键起核心**：Postgres / Redis / MinIO 健康；API / 渠道网关 / 控制台可访问。
2. **询价闭环（可先模拟企微）**：入站文本 → 任务引擎建 Mission → 返回报价/答复草稿 → 控制台看得见。
3. **无人值守**：超时后任务引擎自动催办至少 1 次（演示间隔可缩到秒级；生产默认 T+24h / T+72h）。
4. **可升级 / 可取消**：第二次超时通知负责人（handed_off）；客户已回或人工关闭则取消后续催办。
5. **不串租**：所有查询强制 `tenant_id`；换租户看不到数据。
6. **红线不破**：不用 Dify / n8n / FastGPT / MaxKB；Activepieces 不用 `packages/ee`；不用 OpenClaw 替换 Coze 或任务引擎。
7. **能给别人点开**：控制台有白标占位（名称 / Logo / 主题色）；有演示脚本。

## 2. 7 天明确不做（避免膨胀）

| 不做 | 原因 |
|------|------|
| 真多租户计费 / 配额拦截 / 支付 | P2，不挡试点 |
| 飞书 | 与企微同构，D8+ |
| 业务人员在 Coze 画布上自己改流程 | 引擎能挂上即可，不承诺实施培训 |
| RAG 质量调到抽样 80% | 先通链路，再灌电缆规格书 |
| K8s / 信创 / 达梦 / Bisheng | P4–P5 |
| 自定义域名 / 完整 SSO | P2–P3 |
| 美化成完整 Ant Design Pro 中后台 | 控制台先 Pro 风格一页任务台 |

真企微长连接、真 Coze、真 RAGFlow：**D5–D6 有凭证和机器再接**；没有则继续用模拟入站 + mock 检索，**不挡 D7 演示上线**。

## 3. 架构怎么在 7 天落地

```
企微或 POST /dev/ingest
        │
        ▼
channel-gateway（鉴权占位 · 幂等 · 租户路由）
        │
        ▼
apps/api 产品壳
  · Tenant / Branding
  · Mission 状态机（主动长程的核心）
  · 催办调度（先内置 ticker；Activepieces 作 P1 profile）
        │
        ├─ 智能步骤：Coze OpenAPI（没有则 mock orchestrator）
        └─ 知识：RAGFlow（没有则 mock 引用）
        │
        ▼
控制台任务台 + 企微出站（没有则只写任务流水）
```

编排大脑仍是 Coze；主动长程仍是任务引擎。7 天用 mock 填引擎空缺，**接口形状按真引擎预留**。

## 4. 逐日计划

### Day 1 — 地基可跑（今天开始）

- Compose：Postgres 16 / Redis 7 / MinIO + 健康检查 + `.env.example`
- `apps/api`：`GET /health`、dev tenant seed、Mission CRUD、状态机非法迁移报错
- 单测覆盖状态机；`scripts/smoke-mission.sh`
- Coze / RAGFlow / Activepieces：`profile: engines` 文档化，不阻塞中间件

**当日 DoD：** curl 能建任务并改状态；无 Docker 时 API 可用 SQLite 本地演示。

### Day 2 — 入站闭环 + 控制台

- `apps/channel-gateway`：`POST /dev/ingest`（tenantId, botId, userId, text, externalMsgId）
- 同一 `externalMsgId` 不重复建任务
- 控制台：任务列表、状态筛选、白标读配置、一键模拟询价
- 网关与 API 走同一租户头 `X-Tenant-Id`

**当日 DoD：** 模拟一条询价 → Mission 落库 → 控制台可见 → 返回 mock 回复。

### Day 3 — 无人值守催办

- Mission：`open → waiting → running → done | failed | handed_off`
- 内置 chaser：`due_at` 到期发催办 A；再到期催办 B + 升级负责人
- 取消：写 `cancel_reason`，不再催
- 演示环境 `DEMO_CHASE_AFTER` 默认 30s（生产 24h/72h）
- 审计：关键动作写入 `context_json` 流水（谁、何时、何种动作）

**当日 DoD：** 不点任何按钮，到期后任务自己推进；控制台能看到催办记录。

### Day 4 — 部署形态

- API / Gateway / Console 的 Dockerfile + Compose `profile: app`
- Caddy/Nginx 反代说明（TLS）
- `docs/runbook.md`：端口、启动顺序、备份（Postgres 卷）
- 电缆模板目录补「询价报价 + 催办」话术占位（还不是 Coze 导出）

**当日 DoD：** 在目标机 `docker compose up -d`（或 SQLite 开发模式）能对外访问控制台。

### Day 5 — 真引擎 / 真企微（有条件）

**你需要提供（缺则跳过，保持 mock）：**

| 项 | 用途 |
|----|------|
| 4C16G 云主机（或现成 Linux） | 真上线 |
| 企微 Bot 凭证 | 长连接收发 |
| 至少一个模型 API Key | 真回复（DeepSeek / 通义 / GLM） |
| （可选）域名 | HTTPS |

- 企微：channel-gateway 换长连接，内部 JSON 不变
- Coze Studio / RAGFlow：能拉起就拉起；拉不起则保持 HTTP mock，列进 `docs/p1-ready.md`

**当日 DoD：** 要么真企微一条消息进任务引擎，要么书面确认「演示线继续 mock，生产凭证 D8 再接」。

### Day 6 — 首发闭环打磨

- 话术：询价 → 带「来源占位」的答复草稿 → 催办 A/B
- 转人工：低置信或价格承诺 → `handed_off`
- 两租户 smoke：B 租户看不到 A 的任务
- `templates/cable-quote` 演示脚本（curl + 控制台路径）

**当日 DoD：** 按 PRD 6.2 / 6.3 能讲完一条完整故事（允许检索为 mock 引用）。

### Day 7 — 上线日

- 跑 `scripts/smoke-mission.sh` + ingest smoke，结果写入 `docs/p0-acceptance.md`
- 冻结演示账号（dev tenant）、端口、演示口令
- 监控最小值：健康检查 + 结构化日志
- 交付：启动命令、红线、下一步（真 Coze 工作流、灌规格书、第二租户白标）

**当日 DoD：** 你能把控制台 URL 发给别人演示；串租事故 = 0。

## 5. 人力与节奏

单人可扛这 7 天（PRD §22）。每日结束必须有可演示增量，禁止只改文档。

阻塞升级规则：同一问题超过 2 小时（镜像拉不起来、企微权限不足）→ 降级为 mock，**不中断 D7**。

## 6. 风险（7 天视角）

| 风险 | 对策 |
|------|------|
| Coze/RAGFlow 镜像重、难一次起 | 默认不随核心 Compose 启动；接口先 mock |
| 无企微测试企业 | `/dev/ingest` 顶上线演示 |
| 无云主机 | 本机 Compose/SQLite 先演示，D4 再迁 |
| 需求膨胀到「完整 SaaS」 | 以本文 D7 口径为准，其余进 D8+ 的 P2 |

## 7. D8 起（不在这 7 天承诺）

P2 多租户壳、白标域名、配额、模板一键实例化、真 RAG 灌库与 80% 抽样、飞书、Activepieces 社区版接催办触发器。
