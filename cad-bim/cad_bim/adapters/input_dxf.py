from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import ezdxf
from ezdxf.document import Drawing

from cad_bim.core.geometry import centroid, distance_to_segment, project_param
from cad_bim.core.model import (
    DesignIntent,
    Hole,
    MechanicalPart,
    Opening,
    Slab,
    Space,
    Vec2,
    Wall,
    infer_domain,
)

WALL_LAYERS = {"WALL", "A-WALL", "A-WALL-EXTR", "WALLS"}
DOOR_LAYERS = {"DOOR", "A-DOOR", "DOORS"}
WINDOW_LAYERS = {"WINDOW", "A-GLAZ", "A-WINDOW", "WINDOWS"}
SLAB_LAYERS = {"SLAB", "A-FLOR", "FLOOR", "SLABS"}
SPACE_LAYERS = {"SPACE", "A-AREA", "ROOM", "SPACES"}
PART_LAYERS = {"PART", "PROFILE", "OUTLINE", "PARTS"}
HOLE_LAYERS = {"HOLE", "HOLES", "DRILL"}


def load_dxf(path: str | Path) -> DesignIntent:
    document = ezdxf.readfile(str(path))
    return parse_dxf(document, source=str(path))


def parse_dxf(document: Drawing, source: str = "") -> DesignIntent:
    msp = document.modelspace()
    walls: list[Wall] = []
    openings: list[Opening] = []
    slabs: list[Slab] = []
    spaces: list[Space] = []
    parts: list[MechanicalPart] = []
    warnings: list[str] = []

    wall_index = 0
    for entity in msp:
        layer = (entity.dxf.layer or "").upper()
        if entity.dxftype() in {"LINE"} and layer in WALL_LAYERS:
            wall_index += 1
            start = Vec2(float(entity.dxf.start.x), float(entity.dxf.start.y))
            end = Vec2(float(entity.dxf.end.x), float(entity.dxf.end.y))
            walls.append(Wall(id=f"W{wall_index}", start=start, end=end, name=f"Wall {wall_index}"))
        elif entity.dxftype() in {"LWPOLYLINE", "POLYLINE"} and layer in WALL_LAYERS:
            points = _polyline_points(entity)
            for start, end in zip(points, points[1:]):
                wall_index += 1
                walls.append(Wall(id=f"W{wall_index}", start=start, end=end, name=f"Wall {wall_index}"))

    slab_index = space_index = part_index = 0
    pending_openings: list[tuple[str, Vec2, float]] = []
    holes_by_hint: dict[str, list[Hole]] = defaultdict(list)

    for entity in msp:
        layer = (entity.dxf.layer or "").upper()
        if entity.dxftype() in {"LWPOLYLINE", "POLYLINE"}:
            points = _polyline_points(entity)
            closed = bool(getattr(entity, "closed", False))
            if not closed or len(points) < 3:
                continue
            if layer in SLAB_LAYERS:
                slab_index += 1
                slabs.append(Slab(id=f"S{slab_index}", outline=points, name=f"Slab {slab_index}"))
            elif layer in SPACE_LAYERS:
                space_index += 1
                spaces.append(Space(id=f"SP{space_index}", name=f"Space {space_index}", outline=points))
            elif layer in PART_LAYERS:
                part_index += 1
                parts.append(
                    MechanicalPart(
                        id=f"P{part_index}",
                        name=f"Part {part_index}",
                        profile=points,
                        thickness=8.0,
                    )
                )
            elif layer in DOOR_LAYERS | WINDOW_LAYERS:
                kind = "door" if layer in DOOR_LAYERS else "window"
                width = max(
                    abs(points[i].x - points[(i + 1) % len(points)].x)
                    + abs(points[i].y - points[(i + 1) % len(points)].y)
                    for i in range(len(points))
                )
                pending_openings.append((kind, centroid(points), width if width > 0.2 else 0.9))
        elif entity.dxftype() == "CIRCLE" and layer in HOLE_LAYERS:
            holes_by_hint["default"].append(
                Hole(x=float(entity.dxf.center.x), y=float(entity.dxf.center.y), radius=float(entity.dxf.radius))
            )
        elif entity.dxftype() == "CIRCLE" and layer in DOOR_LAYERS | WINDOW_LAYERS:
            kind = "door" if layer in DOOR_LAYERS else "window"
            pending_openings.append((kind, Vec2(float(entity.dxf.center.x), float(entity.dxf.center.y)), 0.9))
        elif entity.dxftype() == "INSERT" and layer in DOOR_LAYERS | WINDOW_LAYERS:
            kind = "door" if layer in DOOR_LAYERS else "window"
            pending_openings.append((kind, Vec2(float(entity.dxf.insert.x), float(entity.dxf.insert.y)), 0.9))

    if holes_by_hint["default"] and parts:
        parts[0].holes.extend(holes_by_hint["default"])
    elif holes_by_hint["default"] and not parts:
        warnings.append("DXF has HOLE circles but no PART/PROFILE closed polyline")

    opening_index = 0
    for kind, point, width in pending_openings:
        wall = min(walls, key=lambda item: distance_to_segment(item, point), default=None)
        if wall is None:
            warnings.append(f"No wall found for {kind} at ({point.x:.3f}, {point.y:.3f})")
            continue
        opening_index += 1
        offset = max(0.0, min(project_param(wall, point) - width / 2.0, max(wall.length - width, 0.0)))
        openings.append(
            Opening(
                id=f"O{opening_index}",
                wall_id=wall.id,
                kind=kind,  # type: ignore[arg-type]
                offset=offset,
                width=width,
                height=2.1 if kind == "door" else 1.5,
                sill=0.0 if kind == "door" else 0.9,
                name=f"{kind.title()} {opening_index}",
            )
        )

    if not walls and not parts:
        warnings.append("DXF contained no WALL/PART geometry on recognized layers")

    return DesignIntent(
        name=Path(source).stem if source else "dxf",
        domain=infer_domain(walls, parts),
        walls=walls,
        openings=openings,
        slabs=slabs,
        spaces=spaces,
        parts=parts,
        source=source,
        warnings=warnings,
        metadata={"units": str(document.units), "layers": sorted({e.dxf.layer for e in msp})},
    )


def _polyline_points(entity) -> list[Vec2]:
    if entity.dxftype() == "LWPOLYLINE":
        return [Vec2(float(x), float(y)) for x, y, *_ in entity.get_points("xy")]
    return [Vec2(float(p[0]), float(p[1])) for p in entity.points()]
