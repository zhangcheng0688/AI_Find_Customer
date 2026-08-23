WALKTHROUGH_PLAYBOOK = """精致漫游不要走「AI 图生成视频」。

静帧好看，是因为 Grok / Flux 只画一帧，构图和光可以装。
漫游差，是因为视频模型没有稳定的三维场景：墙会漂、材质会闪、透视会歪。
这不是插件调参能修好的，是路线选错了。

推荐三层，按交付质量往上走：

A. 日常可用（你现在就能上）
   Twinmotion（年营收 < 100 万美元免费）
   - 把本管线的 IFC 经 Revit/Datasmith，或 FBX/glTF 推进去
   - 动画工具在「易用档」里最强：天气、植被、黄金时刻、路径
   - 适合船舶舱室 / 软装 / 建筑概念漫游

B. 更真、更大气（Windows + RTX）
   D5 Render + Blender LiveSync，或 Twinmotion 升 Unreal Engine 5
   - D5：实时路径追踪，材质库和氛围强，Blender 可直播
   - UE5：电影级天花板（Lumen / Path Tracer / 剪辑），学习成本高
   - Enscape：只适合设计评审，不像片子

C. 开源、可脚本化（本仓库默认交出的脚本）
   Blender + Bonsai（读 IFC）+ Cycles 路径追踪
   - 自带 Add Camera Rigs（dolly / crane）
   - 镜头：24–35mm、慢推、横移、停顿，不要手持晃
   - 24fps、ACES、物理太阳 + HDRI、轻微景深
   - GitHub 可参考：IfcOpenShell/Bonsai、Look-Before-Move（镜头规划研究）

AI 只放在两头，不要当漫游引擎：
   1) 用 Grok 出气氛分镜 / 材质风格板
   2) 在 Twinmotion 或 Blender 里按那张图打光、铺材质
   3) 可选：两张真实 3D 静帧做 Kling 首尾帧，只当概念，不当客户验收片

绝对不要：
   - 单张效果图丢给图生视频当正式漫游
   - 视口录屏 / 默认 Eevee / 匀速直线穿模
   - 用 Markov 那种 GUI 点软件当渲染方案
"""


def describe_walkthrough() -> str:
    return WALKTHROUGH_PLAYBOOK.strip()
