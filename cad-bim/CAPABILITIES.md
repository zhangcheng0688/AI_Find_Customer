# 我能做的事（解决方案清单）

这是当前这条 CAD / BIM / SolidWorks 链路里，**我能直接做、能调用、能交付**的清单。
不是 GitHub 星标合集。星标项目只有进了这条链路，才算我的方案。

打印这份清单：

```bash
python3 -m cad_bim list
```

---

## 1. 核心：给我输入，我出可打开的模型

| # | 我能做 | 你给我 | 你拿到 |
| --- | --- | --- | --- |
| 1 | 读懂平面/规格 | JSON 设计说明、DXF、矢量 PDF、已有 IFC | `intent.json`（中性模型） |
| 2 | BIM / Revit 构建 | 墙、板、门窗、房间（米） | **IFC4**：墙/板/门/窗/空间/属性。Revit 打开或链接 |
| 3 | SolidWorks / AM12 构建 | 零件轮廓、厚度、孔（毫米） | **STEP AP214 实体**（含孔）。SolidWorks / AM12 导入 |
| 4 | CAD 图纸回写 | 同上 | **DXF**（图层 WALL/DOOR/WINDOW/SLAB/SPACE/PART/HOLE） |
| 5 | 直接改，不必重画 | 一句话，或操作 JSON | 改完的 IFC / STEP / DXF |
| 6 | 交叉验证 | — | `report.json`：IFC 计数、墙体几何、STEP BRep 头 |
| 7 | 电影机位漫游包 | 已有模型 | `shots.json` + Blender Cycles 脚本（24fps / dolly / 横移） |

样例已跑通：8×6 m 办公室（4 墙 / 1 门 / 1 窗 / 1 板 / 1 空间）；L 支架带孔 STEP。

---

## 2. 直接改（不用重建模）

| 对象 | 操作 |
| --- | --- |
| CAD / 墙 | 平移、改厚/高/端点、加墙、删墙 |
| BIM / 门窗 | 改宽高偏移、加门窗、删门窗 |
| SolidWorks 零件 | 改厚度/材料、加孔、移孔、改孔径、删孔 |
| 模型 | 改名 |

```bash
python3 -m cad_bim edit cad-bim/examples/office_plan.json --patch cad-bim/examples/office_edit.json --out out/office-v2
python3 -m cad_bim edit cad-bim/examples/l_bracket.json --patch cad-bim/examples/bracket_edit.json --out out/bracket-v2
```

---

## 3. 我能调用的方案（已经挂进链路）

| 角色 | 调用 | 用来干什么 |
| --- | --- | --- |
| BIM 内核 | IfcOpenShell | 写/读/改 IFC4，给 Revit |
| 图纸 | ezdxf | 读/写 DXF |
| 机械实体 | gmsh 里的 Open CASCADE | 写 STEP AP214 |
| 矢量 PDF | PyMuPDF | 抽墙线 |
| 漫游脚本 | Blender + Bonsai（你本机跑） | 按我给的机位做 Cycles 片子 |
| 静帧气氛 | Grok image | 只定光线和材质，不当漫游引擎 |

下一步可接、但还没挂进默认构建：CadQuery/build123d（更复杂零件）、cad2data（Windows 上读客户 `.rvt` 做算量）、pyRevit / SolidWorks API（有正版软件时写原生文件）。

---

## 4. 你只要这样跟我配合

有什么给什么，不必一次给齐：

1. JSON 规格（最稳）
2. DXF（DWG 请另存 DXF）
3. IFC
4. 矢量 PDF + 你核对过的尺寸
5. 改什么：一句话即可

建筑用**米**，机械用**毫米**。

---

## 5. 我做不到的（避免误以为能做）

| 做不到 | 原因 | 替代 |
| --- | --- | --- |
| 写出原生 `.rvt` / `.sldprt` / `.dwg` | 闭源二进制 | IFC / STEP / DXF |
| 本机驱动 Revit / SolidWorks / AutoCAD / AM12 | 要 Windows + 许可证 | 标准格式交接；有机器再跑我写的脚本 |
| 扫描件当精确尺寸 | 没有矢量 | DXF 或 JSON |
| 一句话生成整船舾装并验收 | 没有稳定语义 | 图纸/规格 → 构建 → 改 → 验证 |
| AI 图生视频当正式漫游 | 没有稳定三维 | Twinmotion / D5 / Cycles |
| 把 text-to-cad 当 BIM 内核 | 它只出机械零件草案 | 草案进本管线再验证 |

---

## 6. 命令一览

```bash
python3 -m cad_bim list              # 这份清单
python3 -m cad_bim inputs            # 我要什么输入
python3 -m cad_bim inspect 文件
python3 -m cad_bim build  文件 --out out --targets ifc,step,dxf
python3 -m cad_bim edit   文件 --patch 修改.json --out out
python3 -m cad_bim demo   --out out/demo
python3 -m cad_bim walkthrough 文件 --out out/walkthrough
python3 -m cad_bim cinematic         # 漫游为什么不能走 AI 视频
python3 -m cad_bim hosts revit       # 原生宿主差在哪
```
