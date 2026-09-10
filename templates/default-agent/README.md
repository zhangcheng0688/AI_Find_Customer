# 通用 Demo Agent

白标产品的默认模板：一个扣子 Bot + 一个 RAGFlow dataset。

不是某个行业（电缆/催办）的业务包。绑定字段：

- `coze_space_id` / `coze_bot_id` 或 `workflow_id`
- `ragflow_dataset_id`
- 控制台展示名、开场白

P1 在扣子里建好 Bot、在 RAGFlow 灌「产品自己的说明文档」后，把 ID 填进租户 `EngineBinding`。
