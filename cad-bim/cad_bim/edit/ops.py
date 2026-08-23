from __future__ import annotations

from typing import Any

from cad_bim.core.model import DesignIntent, Hole, Opening, Vec2, Wall


class UnknownEditOp(ValueError):
    pass


def apply_ops(intent: DesignIntent, operations: list[dict[str, Any]]) -> DesignIntent:
    """Apply direct edits in place and return the same DesignIntent."""
    for index, op in enumerate(operations):
        name = op.get("op")
        handler = OPS.get(name)
        if handler is None:
            raise UnknownEditOp(f"Unsupported op {name!r} at index {index}")
        handler(intent, op)
    return intent


def _require_wall(intent: DesignIntent, op: dict[str, Any]) -> Wall:
    wall = intent.wall_by_id(str(op.get("id", "")))
    if wall is None:
        raise KeyError(f"Unknown wall {op.get('id')}")
    return wall


def _require_opening(intent: DesignIntent, op: dict[str, Any]) -> Opening:
    opening = intent.opening_by_id(str(op.get("id", "")))
    if opening is None:
        raise KeyError(f"Unknown opening {op.get('id')}")
    return opening


def _move_wall(intent: DesignIntent, op: dict[str, Any]) -> None:
    wall = _require_wall(intent, op)
    dx, dy = float(op.get("dx", 0.0)), float(op.get("dy", 0.0))
    wall.start = Vec2(wall.start.x + dx, wall.start.y + dy)
    wall.end = Vec2(wall.end.x + dx, wall.end.y + dy)


def _set_wall(intent: DesignIntent, op: dict[str, Any]) -> None:
    wall = _require_wall(intent, op)
    if "height" in op:
        wall.height = float(op["height"])
    if "thickness" in op:
        wall.thickness = float(op["thickness"])
    if "name" in op:
        wall.name = str(op["name"])
    if "start" in op:
        wall.start = Vec2(float(op["start"][0]), float(op["start"][1]))
    if "end" in op:
        wall.end = Vec2(float(op["end"][0]), float(op["end"][1]))


def _add_wall(intent: DesignIntent, op: dict[str, Any]) -> None:
    wall_id = str(op.get("id") or f"W{len(intent.walls) + 1}")
    intent.walls.append(
        Wall(
            id=wall_id,
            start=Vec2(float(op["start"][0]), float(op["start"][1])),
            end=Vec2(float(op["end"][0]), float(op["end"][1])),
            height=float(op.get("height", 3.0)),
            thickness=float(op.get("thickness", 0.2)),
            name=str(op.get("name", wall_id)),
        )
    )
    if intent.domain == "mechanical":
        intent.domain = "both"


def _delete_wall(intent: DesignIntent, op: dict[str, Any]) -> None:
    wall_id = str(op["id"])
    intent.walls = [wall for wall in intent.walls if wall.id != wall_id]
    intent.openings = [opening for opening in intent.openings if opening.wall_id != wall_id]


def _set_opening(intent: DesignIntent, op: dict[str, Any]) -> None:
    opening = _require_opening(intent, op)
    for field in ("offset", "width", "height", "sill"):
        if field in op:
            setattr(opening, field, float(op[field]))
    if "name" in op:
        opening.name = str(op["name"])


def _add_opening(intent: DesignIntent, op: dict[str, Any]) -> None:
    opening_id = str(op.get("id") or f"O{len(intent.openings) + 1}")
    intent.openings.append(
        Opening(
            id=opening_id,
            wall_id=str(op["wall_id"]),
            kind=op.get("kind", "door"),
            offset=float(op.get("offset", 1.0)),
            width=float(op.get("width", 0.9)),
            height=float(op.get("height", 2.1)),
            sill=float(op.get("sill", 0.0 if op.get("kind", "door") == "door" else 0.9)),
            name=str(op.get("name", opening_id)),
        )
    )


def _delete_opening(intent: DesignIntent, op: dict[str, Any]) -> None:
    opening_id = str(op["id"])
    intent.openings = [item for item in intent.openings if item.id != opening_id]


def _set_part(intent: DesignIntent, op: dict[str, Any]) -> None:
    part = intent.part_by_id(str(op.get("id", "")))
    if part is None:
        raise KeyError(f"Unknown part {op.get('id')}")
    if "thickness" in op:
        part.thickness = float(op["thickness"])
    if "material" in op:
        part.material = str(op["material"])
    if "name" in op:
        part.name = str(op["name"])


def _add_hole(intent: DesignIntent, op: dict[str, Any]) -> None:
    part = intent.part_by_id(str(op.get("id", "")))
    if part is None:
        raise KeyError(f"Unknown part {op.get('id')}")
    part.holes.append(Hole(x=float(op["x"]), y=float(op["y"]), radius=float(op["radius"])))


def _set_hole(intent: DesignIntent, op: dict[str, Any]) -> None:
    part = intent.part_by_id(str(op.get("id", "")))
    if part is None:
        raise KeyError(f"Unknown part {op.get('id')}")
    index = int(op["index"])
    hole = part.holes[index]
    if "x" in op:
        hole.x = float(op["x"])
    if "y" in op:
        hole.y = float(op["y"])
    if "radius" in op:
        hole.radius = float(op["radius"])


def _delete_hole(intent: DesignIntent, op: dict[str, Any]) -> None:
    part = intent.part_by_id(str(op.get("id", "")))
    if part is None:
        raise KeyError(f"Unknown part {op.get('id')}")
    del part.holes[int(op["index"])]


def _rename(intent: DesignIntent, op: dict[str, Any]) -> None:
    intent.name = str(op["name"])


OPS = {
    "move_wall": _move_wall,
    "set_wall": _set_wall,
    "add_wall": _add_wall,
    "delete_wall": _delete_wall,
    "set_opening": _set_opening,
    "add_opening": _add_opening,
    "delete_opening": _delete_opening,
    "set_part": _set_part,
    "add_hole": _add_hole,
    "set_hole": _set_hole,
    "delete_hole": _delete_hole,
    "rename": _rename,
}
