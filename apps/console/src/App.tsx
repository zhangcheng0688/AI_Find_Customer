import { useCallback, useEffect, useMemo, useState } from "react";
import { Button, Layout, Select, Space, Table, Tag, Typography, message } from "antd";
import type { ColumnsType } from "antd/es/table";
import dayjs from "dayjs";

const { Header, Content } = Layout;

const tenantId = import.meta.env.VITE_TENANT_ID || "dev-tenant";
const brandName = import.meta.env.VITE_BRAND_NAME || "Agent 工厂";
const brandLogo = import.meta.env.VITE_BRAND_LOGO || "";
const apiBase = (import.meta.env.VITE_API_BASE || "").replace(/\/$/, "");
const gwBase = (import.meta.env.VITE_GATEWAY_BASE || "").replace(/\/$/, "");

type Mission = {
  id: string;
  tenant_id: string;
  bot_id: string;
  type: string;
  status: string;
  due_at?: string | null;
  assignee?: string;
  context_json?: Record<string, unknown>;
  cancel_reason?: string;
  created_at: string;
  last_action_at?: string | null;
};

const statusColor: Record<string, string> = {
  open: "default",
  waiting: "gold",
  running: "blue",
  done: "green",
  failed: "red",
  handed_off: "purple",
};

function apiUrl(path: string) {
  if (apiBase) return `${apiBase}${path}`;
  return `/api-proxy${path}`;
}

function gwUrl(path: string) {
  if (gwBase) return `${gwBase}${path}`;
  return `/gw-proxy${path}`;
}

async function readJson(res: Response) {
  const text = await res.text();
  try {
    return JSON.parse(text);
  } catch {
    throw new Error(text || res.statusText);
  }
}

export default function App() {
  const [status, setStatus] = useState<string>("");
  const [rows, setRows] = useState<Mission[]>([]);
  const [loading, setLoading] = useState(false);
  const [brand, setBrand] = useState(brandName);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const qs = status ? `?status=${encodeURIComponent(status)}` : "";
      const res = await fetch(apiUrl(`/tenants/${tenantId}/missions${qs}`), {
        headers: { "X-Tenant-Id": tenantId },
      });
      const body = await readJson(res);
      if (!body.ok) throw new Error(body.error || "load failed");
      setRows(body.data || []);
    } catch (e) {
      message.error(String(e));
    } finally {
      setLoading(false);
    }
  }, [status]);

  useEffect(() => {
    fetch(apiUrl(`/tenants/${tenantId}`), { headers: { "X-Tenant-Id": tenantId } })
      .then(readJson)
      .then((body) => {
        if (body?.ok && body.data?.display_name) setBrand(body.data.display_name);
      })
      .catch(() => undefined);
  }, []);

  useEffect(() => {
    void load();
    const t = setInterval(() => void load(), 4000);
    return () => clearInterval(t);
  }, [load]);

  const simulate = async () => {
    try {
      const res = await fetch(gwUrl("/dev/ingest"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tenantId,
          botId: "demo-agent",
          userId: "builder",
          text: "你好，介绍一下你能做什么",
          externalMsgId: `ui-${Date.now()}`,
        }),
      });
      const body = await readJson(res);
      if (!body.ok) throw new Error(body.error || "chat failed");
      message.success(body.mockReply || "已发送");
      await load();
    } catch (e) {
      message.error(String(e));
    }
  };

  const columns: ColumnsType<Mission> = useMemo(
    () => [
      { title: "ID", dataIndex: "id", width: 220, ellipsis: true },
      { title: "类型", dataIndex: "type", width: 90 },
      {
        title: "状态",
        dataIndex: "status",
        width: 110,
        render: (s: string) => <Tag color={statusColor[s] || "default"}>{s}</Tag>,
      },
      { title: "负责人", dataIndex: "assignee", width: 120 },
      {
        title: "时间",
        dataIndex: "created_at",
        width: 170,
        render: (v?: string | null) => (v ? dayjs(v).format("MM-DD HH:mm:ss") : "—"),
      },
      {
        title: "消息",
        dataIndex: "context_json",
        ellipsis: true,
        render: (ctx: Mission["context_json"]) =>
          typeof ctx?.text === "string" ? ctx.text : "",
      },
    ],
    [],
  );

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Header
        style={{
          display: "flex",
          alignItems: "center",
          gap: 12,
          background: "#001529",
        }}
      >
        {brandLogo ? (
          <img src={brandLogo} alt="" style={{ height: 28 }} />
        ) : (
          <span style={{ color: "#fff", fontWeight: 700 }}>AF</span>
        )}
        <Typography.Title level={4} style={{ color: "#fff", margin: 0 }}>
          {brand}
        </Typography.Title>
        <Typography.Text style={{ color: "rgba(255,255,255,0.65)" }}>
          白标工作台 · {tenantId} · 对话将接扣子 + RAGFlow
        </Typography.Text>
      </Header>
      <Content style={{ padding: 24 }}>
        <Space style={{ marginBottom: 16 }}>
          <Select
            allowClear
            placeholder="全部状态"
            style={{ width: 180 }}
            value={status || undefined}
            onChange={(v) => setStatus(v || "")}
            options={[
              "open",
              "waiting",
              "running",
              "done",
              "failed",
              "handed_off",
            ].map((s) => ({ value: s, label: s }))}
          />
          <Button onClick={() => void load()}>刷新</Button>
          <Button type="primary" onClick={() => void simulate()}>
            试问 Agent
          </Button>
        </Space>
        <Table
          rowKey="id"
          loading={loading}
          columns={columns}
          dataSource={rows}
          pagination={{ pageSize: 10 }}
        />
      </Content>
    </Layout>
  );
}
