from __future__ import annotations

from pathlib import Path

from cad_bim.render.shots import ShotList


def write_blender_script(shots: ShotList, path: str | Path, ifc_path: str | None = None) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_script(shots, ifc_path), encoding="utf-8")
    return path


def _script(shots: ShotList, ifc_path: str | None) -> str:
    import_block = (
        f'IFC_PATH = r"{ifc_path}"\n'
        if ifc_path
        else "IFC_PATH = None\n"
    )
    camera_calls = "\n".join(_camera_call(index, shot) for index, shot in enumerate(shots.shots))
    return f'''"""Cinematic walkthrough for Blender 4/5 + Cycles.

Usage:
    blender --background --python cinematic.py
Or open Blender, install Bonsai, then run this in the scripting tab.

This is a real 3D camera path. Do not replace it with image-to-video.
"""
from __future__ import annotations

import math
from pathlib import Path

import bpy
from mathutils import Vector

{import_block}
FPS = {shots.fps}
RES = {shots.resolution!r}
OUTPUT = Path(bpy.path.abspath("//")) / "walkthrough.mp4"


def ease(t: float) -> float:
    return t * t * (3.0 - 2.0 * t)


def import_ifc():
    if not IFC_PATH:
        return
    try:
        import bonsai.bim.ifc
        bpy.ops.bim.load_project(filepath=IFC_PATH)
    except Exception:
        # Fallback: user can File > Import > IFC via Bonsai manually.
        print("Bonsai not available; create a proxy box so the camera path is still reviewable.")
        bpy.ops.mesh.primitive_cube_add(size=2, location=(4, 3, 1.5))


def setup_world():
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 128
    scene.cycles.use_denoising = True
    scene.render.fps = FPS
    scene.render.resolution_x, scene.render.resolution_y = RES
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    scene.view_settings.view_transform = "AgX"
    if not scene.world:
        scene.world = bpy.data.worlds.new("World")
    scene.world.use_nodes = True
    nodes = scene.world.node_tree.nodes
    nodes.clear()
    background = nodes.new("ShaderNodeBackground")
    background.inputs["Color"].default_value = (0.03, 0.04, 0.06, 1)
    background.inputs["Strength"].default_value = 0.4
    out = nodes.new("ShaderNodeOutputWorld")
    scene.world.node_tree.links.new(background.outputs["Color"], out.inputs["Surface"])
    sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN"))
    sun.data.energy = 4.0
    sun.data.angle = math.radians(3.0)
    sun.rotation_euler = (math.radians(55), 0.0, math.radians(40))
    bpy.context.collection.objects.link(sun)


def add_shot(name, start, end, frame_start, frames, lens):
    cam_data = bpy.data.cameras.new(name)
    cam_data.lens = lens
    cam_data.dof.use_dof = True
    cam_data.dof.aperture_fstop = 2.8
    cam = bpy.data.objects.new(name, cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = Vector(start[0])
    _look_at(cam, Vector(start[1]))
    cam.keyframe_insert("location", frame=frame_start)
    cam.keyframe_insert("rotation_euler", frame=frame_start)
    cam.location = Vector(end[0])
    _look_at(cam, Vector(end[1]))
    cam.keyframe_insert("location", frame=frame_start + frames)
    cam.keyframe_insert("rotation_euler", frame=frame_start + frames)
    for fcurve in cam.animation_data.action.fcurves:
        for key in fcurve.keyframe_points:
            key.interpolation = "BEZIER"
            key.easing = "EASE_IN_OUT"
    return cam


def _look_at(obj, target):
    direction = target - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def _look(pose):
    return ((pose["x"], pose["y"], pose["z"]), pose["look_at"])


def build():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    import_ifc()
    setup_world()
    frame = 1
    cameras = []
{camera_calls}
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = frame - 1
    if cameras:
        scene.camera = cameras[0]
    scene.render.filepath = str(OUTPUT)
    print(f"Shot list ready. Frames 1-{{scene.frame_end}}. Render animation when lighting is approved.")


if __name__ == "__main__":
    build()
'''


def _camera_call(index: int, shot) -> str:
    indent = "    "
    return (
        f"{indent}cameras.append(add_shot({shot.name!r}, _look({shot.start.__dict__!r}), "
        f"_look({shot.end.__dict__!r}), frame, {shot.frames}, {shot.start.lens_mm}))\n"
        f"{indent}frame += {shot.frames}"
    )
