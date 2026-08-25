from __future__ import annotations

import contextlib
import os
from pathlib import Path

import gmsh

from cad_bim.core.geometry import ensure_ccw
from cad_bim.core.model import DesignIntent, MechanicalPart, Wall


def write_step(intent: DesignIntent, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    gmsh.initialize()
    try:
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.model.add(intent.name or "model")
        if intent.parts:
            for part in intent.parts:
                _add_part(part)
        elif intent.walls:
            for wall in intent.walls:
                _add_wall_solid(wall)
        else:
            raise ValueError("DesignIntent has no mechanical parts or walls to emit as STEP")
        gmsh.model.occ.synchronize()
        with open(os.devnull, "w") as devnull, contextlib.redirect_stdout(devnull):
            gmsh.write(str(path))
    finally:
        gmsh.finalize()
    return path


def _add_part(part: MechanicalPart) -> None:
    profile = ensure_ccw(part.profile)
    if len(profile) < 3:
        raise ValueError(f"Part {part.id} needs at least 3 profile points")
    factory = gmsh.model.occ
    points = [factory.addPoint(p.x, p.y, 0.0) for p in profile]
    lines = [factory.addLine(points[i], points[(i + 1) % len(points)]) for i in range(len(points))]
    loop = factory.addCurveLoop(lines)
    surface = factory.addPlaneSurface([loop])
    extruded = factory.extrude([(2, surface)], 0.0, 0.0, part.thickness)
    volumes = [tag for dim, tag in extruded if dim == 3]
    if not volumes:
        raise RuntimeError(f"Failed to extrude part {part.id}")
    volume = volumes[0]
    for hole in part.holes:
        cylinder = factory.addCylinder(
            hole.x,
            hole.y,
            -1.0,
            0.0,
            0.0,
            part.thickness + 2.0,
            hole.radius,
        )
        result, _ = factory.cut([(3, volume)], [(3, cylinder)], removeObject=True, removeTool=True)
        if not result:
            raise RuntimeError(f"Failed to cut hole in part {part.id}")
        volume = result[0][1]


def _add_wall_solid(wall: Wall) -> None:
    """Emit architectural walls as millimetre solids so SolidWorks can open a BIM-derived STEP."""
    scale = 1000.0
    sx, sy = wall.start.x * scale, wall.start.y * scale
    ex, ey = wall.end.x * scale, wall.end.y * scale
    dx, dy = ex - sx, ey - sy
    length = (dx * dx + dy * dy) ** 0.5
    if length <= 1e-6:
        return
    ux, uy = dx / length, dy / length
    half = wall.thickness * scale / 2.0
    px, py = -uy * half, ux * half
    corners = [
        (sx + px, sy + py),
        (ex + px, ey + py),
        (ex - px, ey - py),
        (sx - px, sy - py),
    ]
    factory = gmsh.model.occ
    points = [factory.addPoint(x, y, wall.elevation * scale) for x, y in corners]
    lines = [factory.addLine(points[i], points[(i + 1) % 4]) for i in range(4)]
    loop = factory.addCurveLoop(lines)
    surface = factory.addPlaneSurface([loop])
    factory.extrude([(2, surface)], 0.0, 0.0, wall.height * scale)
