#!/usr/bin/env python3
"""Generate the 星伴锦程 / 星童猫咪 development schedule workbook."""

from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = Path(__file__).resolve().parents[1] / "docs" / "xingban-jincheng" / "星童猫咪-开发时间计划表.xlsx"

NAVY = "1B3A4B"
TEAL = "2A6F6F"
GOLD = "C4A35A"
RED = "B42318"
ORANGE = "C05621"
GREEN = "276749"
SLATE = "334155"
WHITE = "FFFFFF"
PALE = "F7F4EF"
PALE_TEAL = "E6F1F1"
PALE_GOLD = "F8F1DE"
PALE_NAVY = "E8EEF2"
PALE_RED = "FDECEC"
PALE_GREEN = "E8F5E9"
PALE_ORANGE = "FFF3E6"
ROW_ALT = "FBFAF7"
GRAY = "64748B"

THIN = Border(
    left=Side(style="thin", color="D6D3CD"),
    right=Side(style="thin", color="D6D3CD"),
    top=Side(style="thin", color="D6D3CD"),
    bottom=Side(style="thin", color="D6D3CD"),
)
WRAP = Alignment(wrap_text=True, vertical="center")
CENTER = Alignment(wrap_text=True, vertical="center", horizontal="center")


def fill(hex_color: str) -> PatternFill:
    return PatternFill("solid", fgColor=hex_color)


def font(bold=False, color=SLATE, size=11) -> Font:
    return Font(name="微软雅黑", bold=bold, color=color, size=size)


def header_row(ws, headers, fill_color=NAVY, font_color=WHITE, height=28):
    ws.row_dimensions[1].height = height
    for col, title in enumerate(headers, 1):
        cell = ws.cell(1, col, title)
        cell.fill = fill(fill_color)
        cell.font = font(True, font_color, 11)
        cell.alignment = CENTER
        cell.border = THIN


def style_cell(cell, *, align=WRAP, bg=None, bold=False, color=SLATE, size=10):
    cell.font = font(bold, color, size)
    cell.alignment = align
    cell.border = THIN
    if bg:
        cell.fill = fill(bg)


def set_widths(ws, widths: dict[str, float]):
    for letter, width in widths.items():
        ws.column_dimensions[letter].width = width


def write_rows(ws, rows, start=2, center_cols=None, date_cols=None, stripe=True):
    center_cols = center_cols or set()
    date_cols = date_cols or set()
    for r_i, row in enumerate(rows):
        excel_row = start + r_i
        ws.row_dimensions[excel_row].height = 36
        bg = ROW_ALT if stripe and r_i % 2 else WHITE
        for c_i, value in enumerate(row, 1):
            cell = ws.cell(excel_row, c_i, value)
            align = CENTER if c_i in center_cols else WRAP
            style_cell(cell, align=align, bg=bg)
            if c_i in date_cols and value:
                cell.number_format = "YYYY-MM-DD"


def freeze(ws, cell="A2"):
    ws.freeze_panes = cell
    ws.auto_filter.ref = ws.dimensions
    ws.sheet_view.showGridLines = False
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.oddHeader.left.text = "星伴锦程 · 星童猫咪"
    ws.oddFooter.right.text = "第 &P 页 / 共 &N 页"


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

MILESTONES = [
    ("M0", "2026-09-13", "P0 立项冻结", "产品/创始人",
     "年龄段、零售价、BOM 上限、方案 A/B、首发渠道、预算签字",
     "一页纸范围 + Won't 清单归档，进入设计与开发"),
    ("M1", "2026-11-08", "软件可对话", "后端+AI / 小程序",
     "账号、设备模型、ASR-LLM-TTS、小程序能绑虚拟设备、安全黄金集 ≥100",
     "手机当假设备可完成 10 轮儿童向问答，危险问题被拦截"),
    ("M2", "2026-12-06", "EVT 工程样机过关", "硬件+嵌入式",
     "5–8 台手板：唤醒、对话、触摸、充电；续航与发热有数",
     "问题清单关闭或正式转入 DVT，不再改电子架构"),
    ("M3", "2027-02-28", "DVT 设计验证过关", "硬件项目",
     "10–20 台结构整机；跌落/按压/线材/按键寿命；开模资料齐",
     "家长盲测可接受；结构冻结，允许开模"),
    ("M4", "2027-04-25", "50 户众测过关", "产品+运营",
     "真实家庭 ≥50、使用 ≥14 天；安全事件=0；续航/脏污/订阅意愿有数",
     "致命缺陷清零，允许预售文案对外"),
    ("M5", "2027-05-16", "认证 + PVT 过关", "硬件+合规",
     "GB 6675 / 无线电 / 电池资料；PVT 良率与工时；说明书隐私政策定稿",
     "可下首批量产指令"),
    ("M6", "2027-06-18", "正式开卖", "全员",
     "首批到仓抽检、小程序过审、OTA 回滚、客服排班、限流开关、预售履约",
     "店铺公开售卖并开始履约"),
    ("M7", "2027-08-31", "规模化观察", "产品+运营",
     "30 天退货、订阅转化、售后、内容事故月报齐全",
     "决定是否第二配色 / 扩产 / 开二代"),
]

MONTHS = [
    "2026-08", "2026-09", "2026-10", "2026-11", "2026-12",
    "2027-01", "2027-02", "2027-03", "2027-04", "2027-05",
    "2027-06", "2027-07", "2027-08",
]

# intensity 0 empty, 1 light, 2 mid, 3 peak, M = milestone month
GANTT = [
    ("阶段", "P0 立项",                     [3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("阶段", "P1 EVT",                      [0, 2, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("阶段", "P2 DVT",                      [0, 0, 0, 0, 2, 3, 3, 0, 0, 0, 0, 0, 0]),
    ("阶段", "P3 PVT+认证",                 [0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 0, 0, 0]),
    ("阶段", "P4 首发上线",                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 0, 0]),
    ("阶段", "P5 规模化",                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3]),
    ("硬件", "产品定义 / 竞品拆机",         [3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("硬件", "ID / CMF / 手板",             [1, 3, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("硬件", "电子架构 + EVT 打板",         [0, 2, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("硬件", "DVT 结构与可靠性",            [0, 0, 0, 1, 2, 3, 3, 1, 0, 0, 0, 0, 0]),
    ("硬件", "开模 T0 / T1",                [0, 0, 0, 0, 0, 2, 3, 3, 3, 1, 0, 0, 0]),
    ("硬件", "认证送检",                    [0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 0, 0, 0]),
    ("硬件", "PVT + 首批量产入库",          [0, 0, 0, 0, 0, 0, 0, 2, 3, 3, 3, 1, 0]),
    ("软件", "端云骨架 / 配网 / 账号",      [2, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("软件", "儿童对话 + 安全过滤",         [0, 1, 3, 3, 3, 2, 1, 0, 0, 0, 0, 0, 0]),
    ("软件", "真机联调 / OTA / 低功耗",     [0, 0, 0, 2, 3, 3, 3, 2, 0, 0, 0, 0, 0]),
    ("软件", "CMS / 记忆 / 订阅",           [0, 0, 1, 2, 2, 3, 3, 3, 2, 1, 0, 0, 0]),
    ("软件", "压测 / 灰度 / 生产值班",      [0, 0, 0, 0, 0, 0, 1, 2, 3, 3, 3, 2, 1]),
    ("上线", "主体 / 商标 / 软著 / 备案",   [3, 3, 3, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0]),
    ("上线", "内容库与合规文案",            [1, 2, 3, 3, 3, 3, 3, 2, 1, 0, 0, 0, 0]),
    ("上线", "种子 10 户 + 众测 50 户",     [0, 0, 0, 0, 2, 1, 1, 3, 3, 1, 0, 0, 0]),
    ("上线", "店铺 / 预售 / 达人 / 开卖",   [0, 0, 0, 0, 0, 1, 2, 2, 3, 3, 3, 1, 0]),
    ("上线", "售后 / 订阅运营 / 复盘",      [0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 3, 3, 3]),
]

# id, stream, phase, name, start, end, weeks, depend, owner, deliverable, acceptance, priority
TASKS = [
    # —— 产品 / 项目（计入上线工作流，便于三线统计）——
    ("P-001", "产品", "P0", "冻结一页纸范围与 Won't", "2026-08-24", "2026-09-06", 2, "", "产品", "范围一页纸", "年龄/定价/方案A或B/开卖日签字", "P0"),
    ("P-002", "产品", "P0", "用户画像与 3–8 岁场景走查", "2026-08-24", "2026-09-06", 2, "", "产品", "场景卡 8 张", "卧室/出行/睡前三条主路径写清", "P0"),
    ("P-003", "产品", "P0", "竞品拆解（芙崽/AI童伴/模组猫）", "2026-08-24", "2026-09-13", 3, "", "产品+硬件", "拆解纪要", "BOM 对照与可抄/不可抄清单", "P0"),
    ("P-004", "产品", "P0", "零售价、BOM 上限、订阅定价模型", "2026-08-31", "2026-09-13", 2, "P-001", "产品+财务", "定价表", "硬件毛利与年订阅覆盖 token 可算", "P0"),
    ("P-005", "产品", "P0", "选定方案 A 自研或 B 轻硬件", "2026-09-07", "2026-09-13", 1, "P-003,P-004", "创始人", "路径决议", "M0 会议纪要", "P0"),
    ("P-006", "产品", "全程", "双周演示与门禁评审", "2026-08-24", "2027-08-31", 53, "", "产品", "演示纪要", "只接受真机或真小程序", "P0"),

    # —— 硬件 ——
    ("H-001", "硬件", "P0", "电子架构冻结（主控/麦/喇叭/电池/触摸/1 路执行器）", "2026-08-31", "2026-09-20", 3, "P-005", "电子", "架构图", "无摄像头；Wi-Fi 方案确定", "P0"),
    ("H-002", "硬件", "P1", "ID 概念三套（幼态/星空/家猫）", "2026-09-14", "2026-10-11", 4, "P-002", "ID 外包", "三套效果图", "可评审、可估模具", "P0"),
    ("H-003", "硬件", "P1", "ID 评审选定一套并冻结脸型比例", "2026-10-12", "2026-10-18", 1, "H-002", "产品+ID", "冻结稿", "只留一套进手板", "P0"),
    ("H-004", "硬件", "P1", "内部堆叠与电池仓、喇叭腔", "2026-09-21", "2026-10-25", 5, "H-001,H-003", "结构", "堆叠 3D", "450g / 22cm 内可放下", "P0"),
    ("H-005", "硬件", "P1", "CMF 与毛绒面料、填充物打样", "2026-10-12", "2026-11-08", 4, "H-003", "ID+供应链", "面料小样", "手感、掉毛、色牢度初评", "P0"),
    ("H-006", "硬件", "P1", "外观手板（3D 打印 + 贴绒）", "2026-10-19", "2026-11-22", 5, "H-003,H-004", "结构+ID", "手板 2 只", "可抱、可拍照、可评脸", "P0"),
    ("H-007", "硬件", "P1", "EVT 原理图与器件选型", "2026-09-21", "2026-10-25", 5, "H-001", "电子", "原理图", "电芯、功放、麦阵列确定", "P0"),
    ("H-008", "硬件", "P1", "EVT PCB 与贴片（5–8 套）", "2026-10-26", "2026-11-22", 4, "H-007", "电子", "EVT 板", "上电、USB、射频连通", "P0"),
    ("H-009", "硬件", "P1", "声学：AEC、喇叭频响、唤醒距离", "2026-11-09", "2026-12-06", 4, "H-008", "嵌入式", "声学报告", "1.5m 可唤醒，回声可对话", "P0"),
    ("H-010", "硬件", "P1", "电源、充电、续航、发热", "2026-11-09", "2026-12-06", 4, "H-008", "电子", "续航报告", "日用 2h、目标一周；体表可接受", "P0"),
    ("H-011", "硬件", "P1", "触摸 / IMU / 执行器手感", "2026-11-16", "2026-12-06", 3, "H-008", "电子+结构", "交互纪要", "摸头/肚有反馈，不吓人", "P1"),
    ("H-012", "硬件", "P1", "EVT 整机装配与问题清单（M2）", "2026-11-23", "2026-12-06", 2, "H-006,H-009,H-010,S-012", "硬件项目", "EVT 报告", "能唤醒对话充电，架构不再改", "P0"),
    ("H-013", "硬件", "P1", "毛绒 OEM 寻源 2–3 家打样", "2026-09-14", "2026-11-15", 9, "H-003", "供应链", "报价与样衣", "交期/MOQ/品控书面", "P0"),
    ("H-014", "硬件", "P1", "电子 OEM / 模组厂寻源对比", "2026-09-14", "2026-11-08", 8, "H-001", "供应链", "对比表", "至少 2 家可量产", "P0"),
    ("H-015", "硬件", "P2", "DVT 结构优化与拆装维修性", "2026-12-07", "2027-01-17", 6, "H-012", "结构", "DVT 3D", "可换外套/可修喇叭", "P0"),
    ("H-016", "硬件", "P2", "DVT PCB 改版与贴片", "2026-12-07", "2027-01-17", 6, "H-012", "电子", "DVT 板", "EVT 问题关闭", "P0"),
    ("H-017", "硬件", "P2", "DVT 整机 10–20 台", "2027-01-18", "2027-02-14", 4, "H-015,H-016,H-013", "硬件项目", "DVT 整机", "可进可靠性与家长盲测", "P0"),
    ("H-018", "硬件", "P2", "可靠性：跌落/按压/线材/按键", "2027-01-25", "2027-02-28", 5, "H-017", "硬件项目", "可靠性报告", "用例通过或让步签字", "P0"),
    ("H-019", "硬件", "P2", "可水洗策略与护理说明草案", "2027-01-18", "2027-02-14", 4, "H-013,H-015", "产品+供应链", "护理草案", "外套可拆或明确不可洗", "P1"),
    ("H-020", "硬件", "P2", "开模资料包与模具厂选定", "2027-01-18", "2027-02-07", 3, "H-015", "结构+供应链", "开模包", "分模、缩水、材料齐", "P0"),
    ("H-021", "硬件", "P2", "模具开工至 T0", "2027-02-08", "2027-03-21", 6, "H-020,M3", "供应链", "T0 样件", "尺寸与披缝初评", "P0"),
    ("H-022", "硬件", "P3", "T1 修模与确认", "2027-03-22", "2027-04-18", 4, "H-021", "结构", "T1 样件", "可进入 PVT 装配", "P0"),
    ("H-023", "硬件", "P3", "认证送检：GB 6675 / CCC", "2027-03-01", "2027-05-16", 11, "H-017", "合规+硬件", "检测报告", "结论可用于上架", "P0"),
    ("H-024", "硬件", "P3", "无线电 SRRC（及蓝牙如有）", "2027-03-01", "2027-05-09", 10, "H-016", "电子+合规", "型号核准", "频段与标签齐", "P0"),
    ("H-025", "硬件", "P3", "电池 UN38.3 与运输鉴定", "2027-02-15", "2027-04-25", 10, "H-016", "供应链", "运输鉴定", "电商可发货", "P0"),
    ("H-026", "硬件", "P3", "PVT 50–100 台组装", "2027-04-12", "2027-05-16", 5, "H-022,H-016", "硬件项目", "PVT 整机", "不靠工程师手改", "P0"),
    ("H-027", "硬件", "P3", "产线 SOP、工装、抽检标准", "2027-04-12", "2027-05-16", 5, "H-026", "供应链", "SOP", "新人按文档可装", "P0"),
    ("H-028", "硬件", "P3", "包装、说明书、年龄警示定稿", "2027-04-19", "2027-05-16", 4, "L-018,H-019", "产品+合规", "包材定稿", "与认证描述一致", "P0"),
    ("H-029", "硬件", "P4", "首批量产 500–2000 台", "2027-05-17", "2027-06-13", 4, "H-026,H-023,H-027", "供应链", "成品入库", "抽检通过", "P0"),
    ("H-030", "硬件", "P4", "售后备件 5%（板/喇叭/外套/线）", "2027-05-17", "2027-06-13", 4, "H-029", "供应链", "备件入库", "开卖不断件", "P1"),
    ("H-031", "硬件", "P5", "售后失效分析与小改", "2027-06-21", "2027-08-31", 10, "H-029", "硬件项目", "失效月报", "高发不良有对策", "P1"),
    ("H-032", "硬件", "P5", "第二配色 / 节日款评估", "2027-07-12", "2027-08-31", 7, "M7", "产品+ID", "评估纪要", "只评估不开新结构", "P2"),

    # —— 软件 ——
    ("S-001", "软件", "P0", "技术栈冻结（芯片 SDK / 云 / ASR/TTS / LLM 网关）", "2026-08-24", "2026-09-13", 3, "P-005", "后端+嵌入式", "技术决策", "有降级供应商", "P0"),
    ("S-002", "软件", "P1", "账号、家庭、孩子档案、设备三元组", "2026-09-14", "2026-10-11", 4, "S-001", "后端", "数据模型", "一家庭多孩子可扩展但不首发", "P0"),
    ("S-003", "软件", "P1", "配网、绑定、解绑协议", "2026-09-21", "2026-10-25", 5, "S-002", "嵌入式+后端", "配网文档", "小程序 2 分钟内绑上", "P0"),
    ("S-004", "软件", "P1", "固件 BSP：麦、喇叭、按键、充电状态", "2026-09-21", "2026-11-08", 7, "S-001,H-007", "嵌入式", "BSP", "EVT 板可录音播放", "P0"),
    ("S-005", "软件", "P1", "端云心跳、对话会话、超时挂断", "2026-10-12", "2026-11-08", 4, "S-002,S-004", "后端+嵌入式", "协议", "断网可感知", "P0"),
    ("S-006", "软件", "P1", "云端 ASR–安全–LLM–TTS 最小链路", "2026-10-12", "2026-11-08", 4, "S-001", "AI 应用", "对话 API", "文本进音频出，延迟有数", "P0"),
    ("S-007", "软件", "P1", "家长小程序：绑定/解绑/设备状态", "2026-10-12", "2026-11-08", 4, "S-003", "小程序", "小程序 v0.1", "虚拟设备可绑，M1", "P0"),
    ("S-008", "软件", "P1", "星童猫咪人设 v0 与语气规范", "2026-10-12", "2026-11-15", 5, "P-002", "产品+AI", "人设卡", "短句、可打断、不说教", "P0"),
    ("S-009", "软件", "P1", "儿童安全过滤器 v1 + 黄金集 100 条", "2026-10-19", "2026-11-08", 3, "S-006", "AI+合规", "过滤规则+集", "高危类 100% 拦截抽样", "P0"),
    ("S-010", "软件", "P1", "离线兜底：安抚语/缓存故事", "2026-11-02", "2026-11-29", 4, "S-004,S-008", "嵌入式", "离线包", "无网也能安抚+讲 3 个故事", "P0"),
    ("S-011", "软件", "P1", "唤醒词与误唤醒抑制", "2026-11-09", "2026-12-13", 5, "S-004,H-009", "嵌入式", "唤醒报告", "误唤醒可接受阈值书面化", "P0"),
    ("S-012", "软件", "P1", "假设备联调验收（M1）", "2026-11-02", "2026-11-08", 1, "S-006,S-007,S-009", "后端+小程序", "M1 纪要", "10 轮问答+拦截演示", "P0"),
    ("S-013", "软件", "P2", "真机 AEC 与打断（插话）", "2026-12-07", "2027-01-17", 6, "S-011,H-012", "嵌入式+AI", "体验报告", "孩子插话能停", "P0"),
    ("S-014", "软件", "P2", "OTA 与版本回滚", "2026-12-14", "2027-01-24", 6, "S-005", "嵌入式+后端", "OTA 流程", "演练失败可回滚", "P0"),
    ("S-015", "软件", "P2", "低功耗、休眠、充电态策略", "2027-01-04", "2027-02-07", 5, "S-004,H-010", "嵌入式", "功耗报告", "待机达标", "P0"),
    ("S-016", "软件", "P2", "长期记忆 v1（称呼/偏好/害怕）", "2026-12-14", "2027-02-07", 8, "S-008,S-002", "AI 应用", "记忆方案", "可关、可删、家长可见摘要", "P1"),
    ("S-017", "软件", "P2", "内容 CMS：故事/儿歌/百科", "2026-12-07", "2027-02-14", 10, "S-006", "后端+内容", "CMS", "编辑可不发版上新", "P0"),
    ("S-018", "软件", "P2", "家长端：时长、宵禁、内容开关", "2026-11-16", "2026-12-27", 6, "S-007", "小程序", "小程序 v0.3", "宵禁到期强制结束", "P0"),
    ("S-019", "软件", "P2", "家长端：每日主题摘要（不默认全文）", "2027-01-04", "2027-02-14", 6, "S-018,S-016", "小程序", "摘要页", "家长 30 秒看完", "P1"),
    ("S-020", "软件", "P2", "黄金集扩到 200 条并回归", "2026-12-07", "2027-02-21", 11, "S-009", "AI+产品", "评测报告", "众测前必过", "P0"),
    ("S-021", "软件", "P2", "DVT 装机联调（M3 软件侧）", "2027-02-01", "2027-02-28", 4, "S-013,S-014,H-017", "嵌入式+后端", "联调纪要", "真机稳定对话+OTA", "P0"),
    ("S-022", "软件", "P3", "用量、精力值、年订阅", "2027-02-15", "2027-04-11", 8, "S-002,P-004", "后端", "计费", "用尽可降级离线，不黑屏死机", "P0"),
    ("S-023", "软件", "P3", "审计日志与一键关闭云端对话", "2027-03-01", "2027-04-11", 6, "S-006", "后端+合规", "开关", "开卖日可紧急只留离线", "P0"),
    ("S-024", "软件", "P3", "压测、限流、降级（TTS/LLM）", "2027-03-15", "2027-05-02", 7, "S-006,S-022", "后端", "压测报告", "开卖峰值有预案", "P0"),
    ("S-025", "软件", "P3", "众测缺陷关闭（体验/安全/崩溃）", "2027-03-22", "2027-04-25", 5, "L-012,S-021", "全软件", "缺陷榜", "致命=0，M4", "P0"),
    ("S-026", "软件", "P3", "儿童数据删除/导出与家长同意流", "2027-03-01", "2027-04-18", 7, "S-002,L-008", "后端+小程序", "合规流", "7 日内可删", "P0"),
    ("S-027", "软件", "P3", "观测：成功率、延迟、挂断、拦截率", "2027-03-15", "2027-05-09", 8, "S-023", "后端", "看板", "值班看一张图", "P0"),
    ("S-028", "软件", "P4", "生产环境、备份、密钥、灰度", "2027-05-03", "2027-05-30", 4, "S-024,S-027", "后端", "运行手册", "演练恢复", "P0"),
    ("S-029", "软件", "P4", "小程序审核与隐私清单过审", "2027-05-03", "2027-06-06", 5, "S-026,L-010", "小程序+合规", "过审截图", "开卖前可用", "P0"),
    ("S-030", "软件", "P4", "开卖日值班与回滚演练", "2027-06-07", "2027-06-18", 2, "S-028,S-014", "后端+嵌入式", "值班表", "回滚 ≤30 分钟", "P0"),
    ("S-031", "软件", "P5", "人设/内容/成本迭代", "2027-06-21", "2027-08-31", 10, "M6", "AI+内容", "双周版本", "token 成本下降有数", "P1"),
    ("S-032", "软件", "P5", "客服工单与设备远程诊断", "2027-06-14", "2027-07-25", 6, "S-027", "后端+运营", "工单流", "配网失败可远程看日志", "P1"),

    # —— 上线 / 合规 ——
    ("L-001", "上线", "P0", "公司主体、对公账户、合同模板", "2026-08-24", "2026-10-18", 8, "", "创始人+财务", "主体齐备", "可签模具与 OEM", "P0"),
    ("L-002", "上线", "P0", "商标检索与申请：星伴锦程、星童猫咪", "2026-08-24", "2026-12-06", 15, "", "合规", "申请回执", "检索无高冲突再宣发", "P0"),
    ("L-003", "上线", "P1", "域名、官网骨架、品牌 VI 初稿", "2026-09-14", "2026-11-22", 10, "P-001", "运营+设计", "官网 v0", "能讲清产品一句话", "P1"),
    ("L-004", "上线", "P1", "软著申请（端+云+小程序）", "2026-10-19", "2026-12-20", 9, "S-012", "合规", "材料提交", "开卖前拿到或在审", "P1"),
    ("L-005", "上线", "P2", "外观专利（开模前）", "2027-01-18", "2027-02-28", 6, "H-003,H-015", "合规+ID", "申请", "开模前递交", "P1"),
    ("L-006", "上线", "P1", "确认生成式 AI / 小程序 / APP 备案路径", "2026-10-12", "2026-11-15", 5, "S-001", "合规", "备案清单", "该排队的 11 月已排", "P0"),
    ("L-007", "上线", "P1", "儿童数据分类与存储地域决策", "2026-09-21", "2026-10-25", 5, "S-002", "合规+后端", "分类表", "敏感字段不出境默认", "P0"),
    ("L-008", "上线", "P2", "儿童个人信息保护评估与家长单独同意", "2026-12-07", "2027-02-28", 12, "L-007,S-026", "合规", "评估稿", "法务或顾问过目", "P0"),
    ("L-009", "上线", "P2", "隐私政策、用户协议、年龄与充电安全文案", "2027-01-04", "2027-03-14", 10, "L-008", "合规+产品", "三份文案", "与包装、小程序一致", "P0"),
    ("L-010", "上线", "P3", "小程序隐私清单与权限最小化", "2027-03-15", "2027-05-02", 7, "L-009,S-018", "小程序+合规", "清单", "无定位/通讯录/相册除非必要", "P0"),
    ("L-011", "上线", "P1", "内容分级标准与人审 SOP", "2026-10-12", "2026-11-22", 6, "S-008", "内容+合规", "SOP", "谁审、谁抽检写清", "P0"),
    ("L-012", "上线", "P2", "首发内容库（故事80/儿歌40/百科120/安抚60）", "2026-11-16", "2027-02-28", 15, "S-017,L-011", "内容", "内容包", "全部人审可上架", "P0"),
    ("L-013", "上线", "P2", "种子家庭 10 户（12 月）", "2026-12-07", "2026-12-27", 3, "H-012,S-012", "产品", "种子反馈", "愿不愿意抱、怕不怕声", "P0"),
    ("L-014", "上线", "P3", "众测招募与知情同意（≥50 户）", "2027-02-15", "2027-03-07", 3, "H-017,L-008", "运营", "名单+协议", "真孩子、真家长", "P0"),
    ("L-015", "上线", "P3", "众测执行 14 天+（M4）", "2027-03-08", "2027-04-25", 7, "L-014,H-026,S-021", "产品+运营", "众测报告", "安全事件=0", "P0"),
    ("L-016", "上线", "P3", "店铺资质：天猫/抖音/企微私域选主渠道", "2027-03-01", "2027-04-18", 7, "L-001,P-005", "运营", "店铺", "主渠道 1 个 + 私域", "P0"),
    ("L-017", "上线", "P3", "详情页、拍摄（必须真机）", "2027-04-05", "2027-05-16", 6, "H-026,L-012", "运营+设计", "详情页", "不承诺未做能力", "P0"),
    ("L-018", "上线", "P3", "说明书、开箱、年龄警示与包装文案", "2027-04-05", "2027-05-16", 6, "L-009,H-019", "产品", "说明书", "认证描述一致", "P0"),
    ("L-019", "上线", "P3", "客服 SOP、退换货、质保话术", "2027-04-12", "2027-05-23", 6, "L-016", "运营", "SOP", "配网失败/脏污/不说话三套", "P0"),
    ("L-020", "上线", "P3", "物流仓、保价、电池发货规则", "2027-04-19", "2027-05-30", 6, "H-025,L-016", "供应链+运营", "仓配", "可发一线城市 48h", "P0"),
    ("L-021", "上线", "P4", "预售页与产能锁量（禁止超卖）", "2027-05-10", "2027-06-06", 4, "H-029,L-017", "运营", "预售", "锁量 ≤ 入库", "P0"),
    ("L-022", "上线", "P4", "达人测品与开卖传播日历", "2027-05-10", "2027-06-17", 5, "L-017,L-015", "运营", "日历", "开卖周内容排满", "P1"),
    ("L-023", "上线", "P4", "开卖日检查单与舆情值班（M6）", "2027-06-07", "2027-06-18", 2, "H-029,S-030,L-019,L-021", "产品", "M6 签字", "检查单全绿", "P0"),
    ("L-024", "上线", "P4", "开卖后 14 天履约与舆情", "2027-06-18", "2027-07-02", 2, "L-023", "运营+客服", "日报", "超时发货/差评有人接", "P0"),
    ("L-025", "上线", "P5", "订阅转化与内容运营", "2027-06-21", "2027-08-31", 10, "S-022,L-024", "运营", "周报", "转化漏斗可见", "P1"),
    ("L-026", "上线", "P5", "M7 复盘：退货/安全/是否扩产", "2027-08-17", "2027-08-31", 2, "L-025,H-031", "创始人", "复盘纪要", "书面决定下一步", "P0"),
]

PEOPLE = [
    ("产品 / 项目负责人", "1", "全程", "范围、门禁、众测、开卖检查单", "内部"),
    ("硬件项目 / 供应链", "1", "P0–P5", "样机、模具、认证、良率、备件", "内部，认证可顾问"),
    ("工业设计 + CMF", "外包", "P0–P2", "三套概念、冻结稿、面料", "按阶段付费"),
    ("结构工程师", "外包", "P1–P3", "堆叠、模具、T0/T1", "开模前必须到位"),
    ("电子 + 嵌入式", "1", "P0–P4", "原理图、固件、声学、OTA", "内部核心"),
    ("后端 / AI 应用", "1–2", "P0–P5", "对话、安全、记忆、订阅、观测", "内部核心"),
    ("小程序", "1", "P1–P4", "家长端六页 + 合规流", "可兼职前端"),
    ("内容 / 审核", "1", "P1–P5", "CMS 供稿、人审、社群话术", "可兼职运营"),
    ("运营 / 客服", "1", "P3–P5", "店铺、众测招募、SOP、舆情", "开卖前 8 周到岗"),
    ("合规顾问（兼职）", "顾问", "P0–P4", "儿童数据、备案、检测机构对接", "按节点"),
]

DECISIONS = [
    ("D1", "2026-09-13", "走方案 A 还是 B", "创始人", "决定开模深度与开卖日"),
    ("D2", "2026-09-20", "主控与模组品牌", "电子", "决定 EVT 能否按期打板"),
    ("D3", "2026-10-18", "ID 选哪一套脸", "产品+创始人", "之后改脸=重做手板"),
    ("D4", "2026-10-18", "生命感：震动还是点头（只留 1 路）", "硬件+产品", "多舵机禁止首发"),
    ("D5", "2026-11-15", "ASR/TTS/LLM 供应商与国内备案", "AI+合规", "影响延迟与成本"),
    ("D6", "2027-02-28", "是否开模（DVT 门禁）", "创始人+硬件", "不过 M3 不准开模"),
    ("D7", "2027-03-01", "主销售渠道只留一个", "运营", "避免店铺精力分散"),
    ("D8", "2027-04-25", "是否公开预售", "产品+运营", "众测致命缺陷则延期"),
    ("D9", "2027-05-16", "首批量终数（500–2000）", "供应链+财务", "按意向与良率"),
    ("D10", "2027-08-31", "是否第二配色或开二代", "创始人", "看 M7 数据"),
]

RISKS = [
    ("R1", "高", "认证排队超 12 周", "开卖整体后移", "3 月第一周送检；P3 含 2 周缓冲；不加新功能换时间", "合规+硬件", "P3"),
    ("R2", "高", "模具 T1 反复改脸", "4–6 周延期", "开模前结构冻结；改脸进二代", "结构", "P2–P3"),
    ("R3", "高", "儿童高危回复漏出", "下架/舆情", "双过滤器+200 条黄金集+一键关云端", "AI+合规", "全程"),
    ("R4", "高", "M1 软件对话延期", "EVT 变成不会说话的毛绒", "软件领先；假设备先验收", "后端", "P1"),
    ("R5", "中", "续航/发热到 PVT 才爆", "退货", "EVT 必须出续航发热报告", "电子", "P1"),
    ("R6", "中", "毛绒脏污、掉毛、过敏", "差评", "面料检测、可拆外套、护理说明", "供应链", "P2–P4"),
    ("R7", "中", "大模型成本吃掉订阅", "亏损", "本地唤醒、短回复、日封顶、精力值", "AI+产品", "P3–P5"),
    ("R8", "中", "范围膨胀（多舵机/摄像头/多语）", "全线延期", "Won't 写进 M0，变更走门禁", "产品", "全程"),
    ("R9", "中", "商标或宣发冲突", "改名成本", "P0 启动检索，宣发前再核", "合规", "P0–P1"),
    ("R10", "低", "首批超卖无法履约", "投诉", "预售锁量 ≤ 入库", "运营", "P4"),
    ("R11", "低", "开卖日云服务峰值", "对话不可用", "压测+限流+离线安抚兜底", "后端", "P4"),
    ("R12", "中", "源 PPT 未读导致节点错位", "计划与资金不匹配", "收到 PPT 后 1 周内回填 6 项假设", "产品", "P0"),
]


def phase_fill(phase: str) -> str:
    return {
        "P0": PALE_GOLD,
        "P1": PALE_TEAL,
        "P2": PALE_NAVY,
        "P3": PALE_ORANGE,
        "P4": PALE_GREEN,
        "P5": "F3E8FF",
        "全程": "F1F5F9",
    }.get(phase, WHITE)


def prio_fill(prio: str) -> str:
    return {"P0": PALE_RED, "P1": PALE_GOLD, "P2": PALE_NAVY}.get(prio, WHITE)


def stream_fill(stream: str) -> str:
    return {"硬件": PALE_TEAL, "软件": PALE_NAVY, "上线": PALE_GOLD, "产品": PALE_ORANGE}.get(stream, WHITE)


# ---------------------------------------------------------------------------
# Sheets
# ---------------------------------------------------------------------------

def sheet_cover(wb):
    ws = wb.active
    ws.title = "封面与假设"
    ws.sheet_properties.tabColor = NAVY
    ws.merge_cells("B2:G2")
    ws["B2"] = "星伴锦程 · 星童猫咪  全链路开发时间计划表"
    ws["B2"].font = Font(name="微软雅黑", bold=True, size=20, color=NAVY)
    ws.merge_cells("B3:G3")
    ws["B3"] = "硬件量产  ×  软件可用  ×  合规上架  ×  电商开卖     |     v1.0  ·  2026-08-23"
    ws["B3"].font = font(False, GRAY, 12)

    meta = [
        ("计划起点", "2026-08-24（周一）"),
        ("方案 A 开卖日（默认）", "2027-06-18"),
        ("方案 B 开卖日（轻硬件）", "2027-03-20"),
        ("规模化观察", "2027-06-19 ～ 2027-08-31"),
        ("首发年龄", "3–8 岁（2 岁及以下只做安抚音）"),
        ("首发形态", "毛绒猫 + 1 路生命感执行器 + 家长微信小程序 + 云端对话"),
        ("首批量", "500–2000 台"),
        ("源材料", "星伴锦程商业计划书.pptx ＋ 星童猫咪.pptx（云端未读到原文，按标准结构编排）"),
    ]
    ws["B5"] = "关键参数"
    ws["B5"].font = font(True, NAVY, 14)
    for i, (k, v) in enumerate(meta):
        ws.cell(6 + i, 2, k)
        ws.cell(6 + i, 3, v)
        style_cell(ws.cell(6 + i, 2), bg=PALE_NAVY, bold=True)
        ws.merge_cells(start_row=6 + i, start_column=3, end_row=6 + i, end_column=6)
        style_cell(ws.cell(6 + i, 3), bg=PALE)
        ws.row_dimensions[6 + i].height = 22

    ws["B15"] = "使用方法"
    ws["B15"].font = font(True, NAVY, 14)
    how = [
        "1. 「里程碑门禁」是唯一准点表：门禁没过，不准进入下一阶段，也不准改开卖承诺。",
        "2. 「月度三线甘特」看资源冲突：同一月份若硬件开模、软件众测、上线备案叠在一起，先保认证与安全。",
        "3. 「全量任务清单」是周会主表。只改 状态 / 实际开始 / 实际结束 / 备注。状态仅四值：未开始 / 进行中 / 阻塞 / 完成。",
        "4. 硬件 / 软件 / 上线与合规 三张表是同一清单的筛选视图，避免有人只看自己那条线。",
        "5. 收到两份 PPT 后，优先回填：年龄、定价、是否自研主板、渠道、编制、资金能撑到哪一里程碑。",
        "6. 原则：软件早于硬件；先 50 户真孩子众测再预售；首发无摄像头、不多舵机。",
    ]
    for i, line in enumerate(how):
        ws.merge_cells(start_row=16 + i, start_column=2, end_row=16 + i, end_column=7)
        ws.cell(16 + i, 2, line)
        style_cell(ws.cell(16 + i, 2), bg=PALE if i % 2 == 0 else WHITE)
        ws.row_dimensions[16 + i].height = 22

    ws["B23"] = "方案怎么选"
    ws["B23"].font = font(True, NAVY, 14)
    headers = ["方案", "周期", "硬件路径", "开卖日", "适合谁"]
    for c, h in enumerate(headers, 2):
        cell = ws.cell(24, c, h)
        style_cell(cell, align=CENTER, bg=TEAL, bold=True, color=WHITE)
    rows = [
        ("A 标准自研（默认）", "约 42 周", "自研 ID/结构/主板，EVT→DVT→PVT，开模+认证", "2027-06-18", "要自有外观、可迭代、可控毛利"),
        ("B 轻硬件加速", "约 28 周", "外购对话模组 + 毛绒 OEM / 小改公模", "2027-03-20", "先验证内容与付费，再开模"),
    ]
    for i, row in enumerate(rows):
        for c, val in enumerate(row, 2):
            style_cell(ws.cell(25 + i, c, val), bg=PALE_TEAL if i == 0 else PALE_GOLD)
        ws.row_dimensions[25 + i].height = 32

    ws["B28"] = "首发做 / 首发不做"
    ws["B28"].font = font(True, NAVY, 14)
    headers = ["层", "首发做", "首发不做（二期再评）"]
    for c, h in enumerate(headers, 2):
        cell = ws.cell(29, c, h)
        style_cell(cell, align=CENTER, bg=NAVY, bold=True, color=WHITE)
    scope = [
        ("硬件", "毛绒、触摸、麦+喇叭、Wi-Fi、Type-C、1 路震动或点头", "四足行走、多舵机表情、前摄摄像头"),
        ("软件", "对话、故事/儿歌/百科、安抚、离线兜底、OTA、家长时长与开关", "开放社交、自动加好友、不受控视频生成"),
        ("商业", "硬件销售 + 年订阅（算力/内容）", "先免费无限聊再找变现"),
        ("合规", "玩具安全、无线电、电池、儿童个人信息、内容安全", "未认证公开售卖"),
    ]
    for i, row in enumerate(scope):
        for c, val in enumerate(row, 2):
            style_cell(ws.cell(30 + i, c, val), bg=WHITE if i % 2 else PALE)
        ws.row_dimensions[30 + i].height = 36

    ws["B35"] = "配套说明见 docs/xingban-jincheng/星童猫咪-全链路开发时间计划.md"
    ws["B35"].font = font(False, GRAY, 10)

    set_widths(ws, {"A": 3, "B": 28, "C": 42, "D": 56, "E": 28, "F": 22, "G": 18})
    ws.freeze_panes = "B5"
    ws.sheet_view.showGridLines = False
    ws.row_dimensions[2].height = 28
    ws.print_title_rows = "1:3"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.paperSize = ws.PAPERSIZE_A4


def sheet_milestones(wb):
    ws = wb.create_sheet("里程碑门禁")
    ws.sheet_properties.tabColor = GOLD
    headers = ["门禁", "目标日期", "名称", "主责", "准入条件（不齐不准评审）", "通过标准（通过才能进下一阶段）"]
    header_row(ws, headers, GOLD, NAVY)
    for i, row in enumerate(MILESTONES):
        excel_row = 2 + i
        ws.row_dimensions[excel_row].height = 48
        for c, val in enumerate(row, 1):
            cell = ws.cell(excel_row, c, val)
            bg = PALE_GOLD if i % 2 == 0 else WHITE
            if row[0] == "M6":
                bg = PALE_GREEN
            style_cell(cell, align=CENTER if c <= 4 else WRAP, bg=bg, bold=(row[0] == "M6"))
    set_widths(ws, {"A": 10, "B": 14, "C": 22, "D": 20, "E": 62, "F": 52})
    freeze(ws)
    ws.auto_filter.ref = f"A1:F{1 + len(MILESTONES)}"


def sheet_gantt(wb):
    ws = wb.create_sheet("月度三线甘特")
    ws.sheet_properties.tabColor = TEAL
    headers = ["工作流", "工作包"] + MONTHS + ["说明"]
    header_row(ws, headers, TEAL)
    intensity = {0: WHITE, 1: "C5E1E1", 2: "7FB8B8", 3: "2A6F6F"}
    notes = {
        "P0 立项": "M0 9/13",
        "P1 EVT": "M2 12/06",
        "P2 DVT": "M3 02/28",
        "P3 PVT+认证": "M4 04/25 · M5 05/16",
        "P4 首发上线": "M6 06/18 开卖",
        "P5 规模化": "M7 08/31",
        "电子架构 + EVT 打板": "关键路径",
        "开模 T0 / T1": "关键路径，禁止改脸",
        "认证送检": "关键路径 8–12 周",
        "端云骨架 / 配网 / 账号": "必须领先硬件",
        "儿童对话 + 安全过滤": "M1 11/08",
        "种子 10 户 + 众测 50 户": "先众测再预售",
        "店铺 / 预售 / 达人 / 开卖": "锁量 ≤ 入库",
    }
    stream_colors = {"阶段": PALE_GOLD, "硬件": PALE_TEAL, "软件": PALE_NAVY, "上线": PALE_ORANGE}
    for r_i, (stream, name, vals) in enumerate(GANTT):
        excel_row = 2 + r_i
        ws.row_dimensions[excel_row].height = 22
        c0 = ws.cell(excel_row, 1, stream)
        c1 = ws.cell(excel_row, 2, name)
        style_cell(c0, align=CENTER, bg=stream_colors[stream], bold=True)
        style_cell(c1, bg=stream_colors[stream], bold=True)
        for c_i, v in enumerate(vals):
            cell = ws.cell(excel_row, 3 + c_i, {0: "", 1: "░", 2: "▒", 3: "█"}.get(v, ""))
            style_cell(cell, align=CENTER, bg=intensity[v], color=WHITE if v == 3 else SLATE, bold=True)
        note = ws.cell(excel_row, 16, notes.get(name, ""))
        style_cell(note, bg=PALE)
    # milestone markers row
    ws.row_dimensions[2 + len(GANTT)].height = 20
    mark = ws.cell(2 + len(GANTT), 1, "")
    style_cell(mark, bg=PALE)
    ws.cell(2 + len(GANTT), 2, "门禁落点")
    style_cell(ws.cell(2 + len(GANTT), 2), bold=True, bg=PALE_GOLD)
    marks = {
        "2026-09": "M0",
        "2026-11": "M1",
        "2026-12": "M2",
        "2027-02": "M3",
        "2027-04": "M4",
        "2027-05": "M5",
        "2027-06": "M6 开卖",
        "2027-08": "M7",
    }
    for i, m in enumerate(MONTHS):
        cell = ws.cell(2 + len(GANTT), 3 + i, marks.get(m, ""))
        style_cell(cell, align=CENTER, bg=PALE_GOLD if m in marks else PALE, bold=True, color=RED if m == "2027-06" else NAVY)
    style_cell(ws.cell(2 + len(GANTT), 16, "深色=高峰，不要在开模+认证月叠加新功能"), bg=PALE_GOLD)

    legend_row = 3 + len(GANTT)
    ws.cell(legend_row, 2, "图例：空白=不投入  ░低  ▒中  █高峰（关键路径）")
    style_cell(ws.cell(legend_row, 2), bg=PALE)
    ws.merge_cells(start_row=legend_row, start_column=2, end_row=legend_row, end_column=6)

    set_widths(ws, {"A": 10, "B": 28, **{get_column_letter(3 + i): 11 for i in range(13)}, "P": 32})
    ws.freeze_panes = "C2"
    ws.sheet_view.showGridLines = False
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.paperSize = ws.PAPERSIZE_A3
    ws.oddHeader.left.text = "星伴锦程 · 星童猫咪 · 月度三线甘特"


def task_headers():
    return [
        "任务ID", "工作流", "阶段", "任务", "计划开始", "计划结束", "工期(周)",
        "前置依赖", "角色", "交付物", "验收标准", "优先级",
        "状态", "实际开始", "实际结束", "备注",
    ]


def write_task_sheet(wb, title, tab_color, rows, table_name):
    ws = wb.create_sheet(title)
    ws.sheet_properties.tabColor = tab_color
    headers = task_headers()
    header_row(ws, headers, tab_color)
    dv = DataValidation(type="list", formula1='"未开始,进行中,阻塞,完成"', allow_blank=True)
    dv.error = "只能选：未开始 / 进行中 / 阻塞 / 完成"
    dv.errorTitle = "状态"
    ws.add_data_validation(dv)
    dv.add(f"M2:M{1 + len(rows)}")

    for i, t in enumerate(rows):
        excel_row = 2 + i
        ws.row_dimensions[excel_row].height = 38
        values = list(t) + ["未开始", "", "", ""]
        for c, val in enumerate(values, 1):
            cell = ws.cell(excel_row, c, val)
            bg = WHITE if i % 2 else ROW_ALT
            if c == 2:
                bg = stream_fill(str(val))
            elif c == 3:
                bg = phase_fill(str(val))
            elif c == 12:
                bg = prio_fill(str(val))
            elif c == 13:
                bg = PALE
            align = CENTER if c in {1, 2, 3, 5, 6, 7, 12, 13} else WRAP
            style_cell(cell, align=align, bg=bg, bold=(c == 1))
            if c in {5, 6, 14, 15} and val:
                cell.number_format = "YYYY-MM-DD"

    set_widths(ws, {
        "A": 10, "B": 10, "C": 8, "D": 42, "E": 13, "F": 13, "G": 10,
        "H": 22, "I": 16, "J": 16, "K": 32, "L": 10, "M": 10, "N": 13, "O": 13, "P": 22,
    })
    freeze(ws)
    last = 1 + len(rows)
    ws.auto_filter.ref = f"A1:P{last}"
    # status coloring
    green_font = Font(name="微软雅黑", color="166534", bold=True)
    red_font = Font(name="微软雅黑", color="B42318", bold=True)
    orange_font = Font(name="微软雅黑", color="C05621", bold=True)
    ws.conditional_formatting.add(f"M2:M{last}", FormulaRule(formula=['$M2="完成"'], fill=fill(PALE_GREEN), font=green_font))
    ws.conditional_formatting.add(f"M2:M{last}", FormulaRule(formula=['$M2="阻塞"'], fill=fill(PALE_RED), font=red_font))
    ws.conditional_formatting.add(f"M2:M{last}", FormulaRule(formula=['$M2="进行中"'], fill=fill(PALE_GOLD), font=orange_font))
    return ws


def sheet_people(wb):
    ws = wb.create_sheet("人员与决策")
    ws.sheet_properties.tabColor = SLATE
    ws["A1"] = "建议编制（创业最小班底，部分外包）"
    ws["A1"].font = font(True, NAVY, 14)
    ws.merge_cells("A1:E1")
    headers = ["角色", "人数", "在场阶段", "主责", "编制说明"]
    for c, h in enumerate(headers, 1):
        cell = ws.cell(3, c, h)
        style_cell(cell, align=CENTER, bg=NAVY, bold=True, color=WHITE)
    for i, row in enumerate(PEOPLE):
        for c, val in enumerate(row, 1):
            style_cell(ws.cell(4 + i, c, val), bg=WHITE if i % 2 else PALE)
        ws.row_dimensions[4 + i].height = 28
    ws.row_dimensions[3].height = 22

    start = 16
    ws.cell(start, 1, "必须由创始人 / 产品拍板的 10 个决策（日期到了必须开会，不能用微信群聊代替）")
    ws.cell(start, 1).font = font(True, NAVY, 14)
    ws.merge_cells(start_row=start, start_column=1, end_row=start, end_column=5)
    headers = ["决策ID", "最晚日期", "议题", "拍板人", "为什么不能拖"]
    for c, h in enumerate(headers, 1):
        cell = ws.cell(start + 2, c, h)
        style_cell(cell, align=CENTER, bg=GOLD, bold=True, color=NAVY)
    for i, row in enumerate(DECISIONS):
        for c, val in enumerate(row, 1):
            style_cell(ws.cell(start + 3 + i, c, val), bg=PALE_GOLD if i % 2 == 0 else WHITE)
        ws.row_dimensions[start + 3 + i].height = 26

    ws.cell(start + 15, 1, "双周节奏：第 1 天冻结切片 → 第 2–8 天做 → 第 9 天联调 → 第 10 天演示。演示必须是真机或真小程序。")
    ws.merge_cells(start_row=start + 15, start_column=1, end_row=start + 15, end_column=5)
    style_cell(ws.cell(start + 15, 1), bg=PALE_TEAL, bold=True)

    set_widths(ws, {"A": 26, "B": 14, "C": 42, "D": 28, "E": 36})
    ws.sheet_view.showGridLines = False
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1


def sheet_risks(wb):
    ws = wb.create_sheet("风险与缓冲")
    ws.sheet_properties.tabColor = RED
    headers = ["风险ID", "等级", "风险", "影响", "缓释", "主责", "窗口"]
    header_row(ws, headers, RED)
    for i, row in enumerate(RISKS):
        excel_row = 2 + i
        ws.row_dimensions[excel_row].height = 40
        for c, val in enumerate(row, 1):
            cell = ws.cell(excel_row, c, val)
            bg = WHITE if i % 2 else ROW_ALT
            if c == 2:
                bg = {"高": PALE_RED, "中": PALE_GOLD, "低": PALE_GREEN}[val]
            style_cell(cell, align=CENTER if c in {1, 2, 6, 7} else WRAP, bg=bg, bold=(c == 2))

    note_row = 3 + len(RISKS)
    ws.merge_cells(start_row=note_row, start_column=1, end_row=note_row + 2, end_column=7)
    ws.cell(
        note_row,
        1,
        "显式缓冲：P2（DVT）与 P3（认证/模具）各预留 2 周，只给模具和检测机构，不给新功能。"
        "关键路径 = 外观冻结 → EVT 电声 → DVT 结构 → 开模 → 认证 → PVT 良率 → 入库 → 开卖。"
        "软件不在关键路径上，但 M1 若延期超过 3 周，后面所有体验结论作废。",
    )
    style_cell(ws.cell(note_row, 1), bg=PALE_GOLD, bold=True)
    ws.row_dimensions[note_row].height = 20
    ws.row_dimensions[note_row + 1].height = 20
    ws.row_dimensions[note_row + 2].height = 20

    set_widths(ws, {"A": 10, "B": 8, "C": 28, "D": 22, "E": 48, "F": 14, "G": 12})
    freeze(ws)
    ws.auto_filter.ref = f"A1:G{1 + len(RISKS)}"


def sheet_this_week(wb):
    ws = wb.create_sheet("本周启动清单")
    ws.sheet_properties.tabColor = GREEN
    ws["A1"] = "2026-08-24 当周必须启动（否则 M0 会空转）"
    ws["A1"].font = font(True, NAVY, 16)
    ws.merge_cells("A1:D1")
    headers = ["#", "行动", "产出", "谁"]
    for c, h in enumerate(headers, 1):
        cell = ws.cell(3, c, h)
        style_cell(cell, align=CENTER, bg=GREEN, bold=True, color=WHITE)
    items = [
        ("1", "把两份 PPT 关键页导出：定价、年龄、渠道、是否自研主板", "6 项假设回填到封面", "产品"),
        ("2", "签 M0 一页纸：范围、Won't、BOM 上限、开卖日", "签字版一页纸", "创始人"),
        ("3", "选定方案 A 或 B", "路径决议", "创始人"),
        ("4", "启动商标检索：星伴锦程、星童猫咪", "检索报告", "合规"),
        ("5", "约 2 家毛绒厂、2 家电子/模组厂", "拜访日历", "供应链"),
        ("6", "冻结技术栈：端侧芯片、云、ASR/TTS、LLM 网关", "技术决策一页", "后端+嵌入式"),
        ("7", "列出儿童安全黄金集前 50 条问法", "问法表", "产品+AI"),
        ("8", "注册域名，起草隐私政策目录", "域名+目录", "运营+合规"),
        ("9", "把双周演示日钉死到日历", "日历邀请", "产品"),
        ("10", "用本表建看板，状态只允许四值", "周会链接", "产品"),
    ]
    for i, row in enumerate(items):
        for c, val in enumerate(row, 1):
            style_cell(ws.cell(4 + i, c, val), align=CENTER if c in {1, 4} else WRAP, bg=PALE_GREEN if i % 2 == 0 else WHITE)
        ws.row_dimensions[4 + i].height = 28
    set_widths(ws, {"A": 6, "B": 62, "C": 28, "D": 16})
    ws.sheet_view.showGridLines = False


def main():
    wb = Workbook()
    sheet_cover(wb)
    sheet_milestones(wb)
    sheet_gantt(wb)
    write_task_sheet(wb, "全量任务清单", NAVY, TASKS, "AllTasks")
    write_task_sheet(wb, "硬件任务", TEAL, [t for t in TASKS if t[1] == "硬件"], "HwTasks")
    write_task_sheet(wb, "软件任务", "3B6FB6", [t for t in TASKS if t[1] == "软件"], "SwTasks")
    write_task_sheet(wb, "上线与合规任务", GOLD, [t for t in TASKS if t[1] in {"上线", "产品"}], "LaunchTasks")
    sheet_people(wb)
    sheet_risks(wb)
    sheet_this_week(wb)

    # print settings for task sheets
    for name in ("全量任务清单", "硬件任务", "软件任务", "上线与合规任务"):
        ws = wb[name]
        ws.page_setup.paperSize = ws.PAPERSIZE_A3
        ws.print_title_rows = "1:1"
        ws.page_setup.horizontalCentered = True

    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)
    print(f"wrote {OUT}  tasks={len(TASKS)}")


if __name__ == "__main__":
    main()
