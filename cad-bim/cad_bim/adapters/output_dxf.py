from __future__ import annotations

from pathlib import Path

import ezdxf

from cad_bim.core.model import DesignIntent


def write_dxf(intent: DesignIntent, path: str | Path) -> Path:
    path = Path(path)
    document = ezdxf.new("R2010")
    for name, color in (
        ("WALL", 1),
        ("DOOR", 3),
        ("WINDOW", 4),
        ("SLAB", 5),
        ("SPACE", 6),
        ("PART", 2),
        ("HOLE", 1),
    ):
        document.layers.add(name, color=color)
    msp = document.modelspace()

    for wall in intent.walls:
        msp.add_line(wall.start.as_tuple(), wall.end.as_tuple(), dxfattribs={"layer": "WALL"})
    for opening in intent.openings:
        wall = intent.wall_by_id(opening.wall_id)
        if wall is None:
            continue
        layer = "DOOR" if opening.kind == "door" else "WINDOW"
        dx = wall.end.x - wall.start.x
        dy = wall.end.y - wall.start.y
        length = wall.length or 1.0
        cx = wall.start.x + dx * ((opening.offset + opening.width / 2.0) / length)
        cy = wall.start.y + dy * ((opening.offset + opening.width / 2.0) / length)
        msp.add_circle((cx, cy), opening.width / 2.0, dxfattribs={"layer": layer})
    for slab in intent.slabs:
        msp.add_lwpolyline([p.as_tuple() for p in slab.outline], close=True, dxfattribs={"layer": "SLAB"})
    for space in intent.spaces:
        msp.add_lwpolyline([p.as_tuple() for p in space.outline], close=True, dxfattribs={"layer": "SPACE"})
    for part in intent.parts:
        msp.add_lwpolyline([p.as_tuple() for p in part.profile], close=True, dxfattribs={"layer": "PART"})
        for hole in part.holes:
            msp.add_circle((hole.x, hole.y), hole.radius, dxfattribs={"layer": "HOLE"})

    path.parent.mkdir(parents=True, exist_ok=True)
    document.saveas(path)
    return path
