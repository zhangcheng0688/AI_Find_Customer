# cad-bim

给定 PDF 图纸、DXF，或一份 JSON 设计说明，这套管线产出：

- **IFC4** — Revit / openBIM 的主通道
- **STEP AP214** — SolidWorks / 机械 CAD 的主通道
- **DXF** — 回写的中性 2D 图纸

它**不会**写出原生 `.rvt` / `.sldprt` / `.dwg`。这些是闭源二进制，全世界没有可靠的开源写入器。行业通行做法就是标准格式交换，不是妥协。

```
PDF / DXF / JSON spec
        │
        ▼
  DesignIntent（中性语义 + 几何）
        │
        ├── adapters/output_ifc  →  *.ifc   → Revit 打开或链接
        ├── adapters/output_step →  *.step  → SolidWorks 打开为实体
        └── adapters/output_dxf  →  *.dxf
                │
                ▼
        verify/（回读计数 + STEP BRep 头）
```

## 你能交付什么，不能交付什么

| 目标 | 本机现在就能做 | 需要 Windows + 许可证 / 云端引擎 |
| --- | --- | --- |
| BIM 构建 | IFC4：墙、板、门窗洞口、空间、属性 | 无 |
| Revit 构建 | 把 IFC 给 Revit 打开/链接 | 原生 `.rvt`、族参数完整保留：pyRevit 或 Autodesk Design Automation |
| SolidWorks 构建 | STEP AP214 实体（含孔） | 原生 `.sldprt` 特征树：SolidWorks COM API |
| AutoCAD | DXF 读写 | 稳定写 DWG：AutoCAD 或 ODA |

GUI 点选（Markov 那条 computer-use 路线）只作为**最后一英里兜底**，不是主干。`cad-bim hosts revit` 会打印对应约束，不会假装已经驱动了软件本体。

## 安装

需要系统里有 OpenGL 运行库（gmsh 的 OCC 内核写 STEP 时用）：

```bash
sudo apt-get install -y libglu1-mesa   # Linux
python3 -m pip install -e cad-bim
```

macOS / Windows 一般不用额外装 GL。

## 用法

```bash
# 看输入被解析成什么
python3 -m cad_bim inspect cad-bim/examples/office_plan.json

# BIM：JSON / DXF / 矢量 PDF → IFC + STEP
python3 -m cad_bim build cad-bim/examples/office_plan.json --out out/office --targets ifc,step,dxf

# 机械：L 支架 → STEP
python3 -m cad_bim build cad-bim/examples/l_bracket.json --out out/bracket --targets step,dxf

# 自带两条样例一次跑完
python3 -m cad_bim demo --out out/demo

# 原生宿主差在哪
python3 -m cad_bim hosts revit
python3 -m cad_bim hosts solidworks
```

把生成的 `*.ifc` 丢进 Revit（打开或链接），把 `*.step` 丢进 SolidWorks（打开零件）。几何是实体，不是网格。

## 输入约定

**JSON spec** 是最稳的输入：墙中心线、门窗沿墙偏移、板/空间轮廓、机械轮廓 + 孔，全部显式给出。见 `examples/`。

**DXF** 认这些图层：

| 图层 | 含义 |
| --- | --- |
| `WALL` / `A-WALL` | 墙中心线（LINE 或多段线） |
| `DOOR` / `WINDOW` | 门窗（圆、块插入点、闭合多段线） |
| `SLAB` / `SPACE` | 楼板 / 房间轮廓 |
| `PART` / `PROFILE` | 机械拉伸轮廓 |
| `HOLE` | 圆孔 |

**矢量 PDF** 抽路径当墙线。扫描件**不会**瞎猜尺寸——会写进 `warnings`，请改用 DXF 或 JSON。

## 成熟开源件（本管线实际用到的）

| 角色 | 项目 | 许可证 |
| --- | --- | --- |
| IFC 读写 / BIM 语义 | [IfcOpenShell](https://github.com/IfcOpenShell/IfcOpenShell) | LGPL-3.0 |
| DXF | [ezdxf](https://github.com/mozman/ezdxf) | MIT |
| STEP BRep（OCC） | [gmsh](https://gitlab.onelab.info/gmsh/gmsh) OCC kernel | GPL / commercial |
| 矢量 PDF | [PyMuPDF](https://github.com/pymupdf/PyMuPDF) | AGPL / commercial |
| 参数化建模（可选下一层） | [CadQuery](https://github.com/CadQuery/cadquery)、[build123d](https://github.com/gumyr/build123d) | Apache-2.0 |
| Revit 内脚本（需 Windows） | [pyRevit](https://github.com/pyrevitlabs/pyRevit) | GPL-3.0 |

主干是 API / 格式驱动。computer-use 只预留接口，不参与默认构建。

## 测试

```bash
cd cad-bim && python3 -m pytest -q
```
