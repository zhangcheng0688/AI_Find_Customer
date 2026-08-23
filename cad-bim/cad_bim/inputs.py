INPUT_CONTRACT = """需要你给我的输入（按优先级，有什么给什么）

1) 最好：一份 JSON 设计说明（最稳，可直接改）
   - 建筑/BIM：墙中心线（米）、墙厚/墙高、门窗沿墙偏移、楼板/房间轮廓
   - 机械/SolidWorks：闭合轮廓（毫米）、拉伸厚度、孔（圆心+半径）、材料
   - 样例：cad-bim/examples/office_plan.json 和 l_bracket.json

2) 简单 CAD：DXF（认 WALL/DOOR/WINDOW/SLAB/SPACE/PART/HOLE 图层）
   DWG 请先另存 DXF。我会读进来改，再写出新的 DXF + IFC/STEP。

3) 已有 BIM：IFC（Revit 导出的 IFC，或本管线生成的 IFC）
   直接改墙/门窗/板/空间，再写回 IFC4 给 Revit 打开或链接。

4) 矢量 PDF 平面图：能抽墙线。扫描件不能当精确尺寸。

5) 修改指令：自然语言，或 JSON 操作列表，例如
   {"op":"set_wall","id":"W1","thickness":0.3}
   {"op":"set_opening","id":"D1","width":1.0}
   {"op":"set_part","id":"P1","thickness":16}
   {"op":"add_hole","id":"P1","x":20,"y":4,"radius":3}

6) 效果图 / 漫游（可选）
   本管线不跑 Blender。把 IFC 丢进 Blender + Bonsai（原 BlenderBIM）做漫游和渲染。
   船舶/软装效果图仍用同一条 IFC/STEP 中台，渲染是后面一层。

不要给我：原生 .rvt / .sldprt / .dwg 当唯一源文件。
我写不回这些闭源格式；请导出 IFC / STEP / DXF，或给我 JSON。
"""


def describe_inputs() -> str:
    return INPUT_CONTRACT.strip()
