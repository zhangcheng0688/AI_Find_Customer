# 开源 CAD / BIM 全景：哪些能进船舶舾装链路

别人那份清单**有参考价值**，适合作索引，不适合当架构。
星数高 ≠ 能进 AM12 / Revit / SolidWorks 交付。下面按「对你这条链路有没有用」重排。

## 先拆四层（清单把它们混在一起了）

| 层 | 干什么 | 代表 | 进不进主干 |
| --- | --- | --- | --- |
| 几何内核 | 做实体、布尔、STEP | OCCT / CadQuery / build123d / pythonocc | 进。本仓库 STEP 已走 OCC（gmsh） |
| 交换格式 | 图纸 ↔ BIM ↔ 机械 | ezdxf、IfcOpenShell、STEP | 进。两套都要，不能互相替代 |
| 宿主自动化 | 在正版软件里改原生文件 | pyRevit、Dynamo、SW API、Revit MCP | 有 Windows+许可证再接 |
| AI 生成 / 算量 | 文本出零件、从模型抽 Excel | text-to-cad、cad2data、DDC skills | 旁路。不能当互转底座 |

## 逐条结论

### 采纳（已经在用，或下一步该接）

- **IfcOpenShell**：IFC 读写的事实标准。BIM / Revit 通道必须用它。本仓库已经用。
- **ezdxf**：DXF 图纸解析/回写。和 IfcOpenShell **不是替代关系**——一个吃 2D 图，一个吃 BIM。清单里「用 IfcOpenShell 替代 ezdxf」是错的。
- **CadQuery / build123d / pythonocc-core**：机械参数化的升级内核。比当前 gmsh 挤出更适合复杂零件；SolidWorks 仍吃 STEP。
- **pyRevit / Dynamo / Autodesk revit-ifc**：有 Revit 的 Windows 机时，用来把 IFC 绑成原生族、或跑 Design Automation。
- **xarial/codestack、solidworks-automation-skill**：有 SolidWorks 时写 `.sldprt` 特征树。没宿主就继续 STEP。
- **Bonsai（在 IfcOpenShell 仓库里）**：IFC 进 Blender 做效果图/漫游，不当建模主干。

### 有条件采用（ingest / 旁路，不当建模内核）

- **cad2data**：能在**不装 Revit** 的 Windows 上把 `.rvt` 抽成 XLSX + DAE（网格）+ 可选 IFC。用途是**读客户已有 Revit 做算量**，不是写出可编辑的 `.rvt`，也不是 AM12 要的 STEP 实体。转换器是 Windows exe，闭源格式解析要自己评估授权后再用。
- **DDC 221 skills / OpenConstructionERP**：施工算量、成本、进度的 prompt 范式，可借鉴；解决不了几何合格。
- **earthtojake/text-to-cad（~14k★）**：Agent skill，主输出是机械 STEP/STL/URDF，不是墙板门窗，更不是舾装目录。星数是 skill 生态热度。Zoo 官方 Text-to-CAD API 另走商业 KittyCAD 内核。可借鉴「技能形态」，不要换成建模底座。
- **xeokit / ThatOpen web-ifc-viewer / Astral3D**：Web 看模。交付给客户浏览时用，不参与构建。
- **Mayo**：STEP/IGES 查看转换，适合人工抽检。
- **FreeCAD**：无头交叉验证可以，不当专业交付宿主。
- **Speckle**：多工具版本化中台，团队协同时再上。

### 现在不要进主干

- **OpenSCAD**：CSG 脚本，不适合 BIM 空间和 SW 级 BRep。
- **CADAM / Multi-Agent-CAD / Text2CAD 论文代码**：演示 text-to-CAD，几何稳定性和 BIM 语义都不够交货。
- **atopile**：电路板，赛道无关。
- **partcad**：硬件包管理，有标准件库再看。
- **SOLIDWORKS-for-Linux**：Wine 跑 SW，不能当生产。
- **solidworks_urdf_exporter**：机器人，和舾装无关。
- **Revit MCP / zexus**：必须 Revit 进程在；没有 Windows 许可证就是空的。有宿主后可以作为 IFC 通道的补丁，不是替代。
- **awatif / OpenBIMtoFEM / BIM2SAM.AI**：结构分析。内舾装默认不算受力；船级社真要算再接，别现在掺进建模。
- **IFC5-development**：跟标准，不写业务代码。

## 清单里三句需要改掉的话

1. 「用 IfcOpenShell 替代 ezdxf，才能处理 AM12/Revit」  
   AM12 吃的是 **STEP**。IfcOpenShell 处理 IFC，不管 AM12 导入。Revit 吃 IFC。图纸仍要 ezdxf。三件事三套格式。

2. 「text-to-cad 是 AI-CAD 制高点，和 CadQuery 对齐就能全自动设计」  
   它对齐的是**机械零件口头描述 → STEP**。你的输入是 PDF/DXF 和舾装规格，输出是可验收几何。CadQuery 已经是正确的机械层；缺的是语义映射和验证，不是再挂一个 14k 星的 skill 仓库。

3. 「cad2data 正是互转方向」  
   它是 **RVT/DWG → 表 + 网格** 的抽取器。互转底座仍是 IFC / STEP / DXF。抽取可以当上游 ingest。

## 对「船舶内舾装三维设计」的落点

继续本仓库已经铺的主干，不要换成那张星标表：

```
PDF / DXF / 规格
  → ezdxf 读图
  → DesignIntent（语义）
  → IfcOpenShell 出 IFC  → Revit
  → OCC/CadQuery 出 STEP → SolidWorks / AM12
  → 多引擎验证
  → Twinmotion / Blender Cycles 漫游
```

下一步按收益排序：

1. 机械侧把 gmsh 挤出升级到 CadQuery/build123d（更好的 BRep、圆角、装配）。
2. 若经常拿到客户 `.rvt`：在 Windows 上试用 cad2data 只做 **ingest → IFC/表**，再进本管线改。
3. 有 Revit/SW 正版机：再接 pyRevit / SW API，补原生文件最后一英里。
4. text-to-cad skill 只用来生成**标准件/支架类零件草案**，必须经过本管线验证才能进交付。

## 第二份工具表（text-to-cad / Agent Hub / GeoLibre 等）

不全是「不错的方案」。有的是真项目但被写过了；有的名字对不上号；有的根本不在 CAD/BIM 赛道。

| 表上的名字 | 实际是什么 | 对舾装/Revit/SW |
| --- | --- | --- |
| Codex text-to-cad + build123d | 真：agent 写 build123d，出 STEP。爆炸图、运动机构不是标配 | 机械零件草案有用。**下一步该接 build123d**，替换 gmsh 挤出 |
| CAD Agent Hub | 没有叫这个、还能同时开 CATIA+UG 出 CATPart 的现成仓库。接近的是 NX_MCP、CAE-Agent-Hub、论文里的 CATIA-MCP | 必须本机有 NX/CATIA。不是云端互转 |
| GeoLibre | 真：开源 GIS（地图/STAC/COG）。能读 DXF 当地理图层 | **不是 CAD**。船厂总图/码头坐标才用 |
| Codex + Botrail | 没核到叫 Botrail 的工业孪生开源平台 | 先当宣传名，不要当可调用方案 |
| PartLoom AI Platform | 没核到这个 MIT 产品。CAD-IR 是论文/规范（ArtisanCAD、CADIR），要 CATIA 或 SW 后端回放 | 有宿主才有意义。不是无许可写 `.sldprt` |
| Multi-Agent-CAD（清华 MAC） | 真。99.3% 是 10 条提示、141 个特征，对比 text-to-cad skill。出可打印零件 | 标准件草案。不是 BIM/Revit/整船 |
| CAD-1000-hours | 真：Markov 的 GUI 录屏数据集 | 训练点软件的模型。46% 任务完成率那条路，不当交付 |
| CADxStudio | 网页机械 CAD SaaS | 浏览器玩零件，进不了 IFC/AM12 验收 |
| GenCAD | 真：照片/草图 → CAD 命令序列（研究） | 草图参考。STL/程序 ≠ 可验收 STEP/IFC |

和第一份清单同一句话：**能进主干的还是 build123d/OCCT + IFC/STEP；MCP/COM 要正版软件；GIS、录屏数据集、网页 CAD 都是旁路。**

