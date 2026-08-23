from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

Domain = Literal["bim", "mechanical", "both"]
OpeningKind = Literal["door", "window"]


@dataclass(frozen=True)
class Vec2:
    x: float
    y: float

    def as_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)


@dataclass
class Wall:
    id: str
    start: Vec2
    end: Vec2
    height: float = 3.0
    thickness: float = 0.2
    elevation: float = 0.0
    name: str = ""

    @property
    def length(self) -> float:
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        return (dx * dx + dy * dy) ** 0.5


@dataclass
class Opening:
    id: str
    wall_id: str
    kind: OpeningKind
    offset: float
    width: float
    height: float
    sill: float = 0.0
    name: str = ""


@dataclass
class Slab:
    id: str
    outline: list[Vec2]
    thickness: float = 0.2
    elevation: float = 0.0
    name: str = "Slab"


@dataclass
class Space:
    id: str
    name: str
    outline: list[Vec2]
    height: float = 3.0
    elevation: float = 0.0


@dataclass
class Hole:
    x: float
    y: float
    radius: float


@dataclass
class MechanicalPart:
    id: str
    name: str
    profile: list[Vec2]
    thickness: float
    holes: list[Hole] = field(default_factory=list)
    material: str = "Steel"
    units: str = "mm"


@dataclass
class DesignIntent:
    """Neutral semantic + geometry model shared by every adapter."""

    name: str
    domain: Domain
    walls: list[Wall] = field(default_factory=list)
    openings: list[Opening] = field(default_factory=list)
    slabs: list[Slab] = field(default_factory=list)
    spaces: list[Space] = field(default_factory=list)
    parts: list[MechanicalPart] = field(default_factory=list)
    source: str = ""
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def wall_by_id(self, wall_id: str) -> Wall | None:
        return next((wall for wall in self.walls if wall.id == wall_id), None)

    def opening_by_id(self, opening_id: str) -> Opening | None:
        return next((item for item in self.openings if item.id == opening_id), None)

    def part_by_id(self, part_id: str) -> MechanicalPart | None:
        return next((part for part in self.parts if part.id == part_id), None)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DesignIntent:
        walls = [
            Wall(
                id=item["id"],
                start=Vec2(**_point(item["start"])),
                end=Vec2(**_point(item["end"])),
                height=float(item.get("height", 3.0)),
                thickness=float(item.get("thickness", 0.2)),
                elevation=float(item.get("elevation", 0.0)),
                name=item.get("name", ""),
            )
            for item in data.get("walls", [])
        ]
        openings = [
            Opening(
                id=item["id"],
                wall_id=item["wall_id"],
                kind=item["kind"],
                offset=float(item["offset"]),
                width=float(item["width"]),
                height=float(item["height"]),
                sill=float(item.get("sill", 0.0)),
                name=item.get("name", ""),
            )
            for item in data.get("openings", [])
        ]
        slabs = [
            Slab(
                id=item["id"],
                outline=[Vec2(**_point(p)) for p in item["outline"]],
                thickness=float(item.get("thickness", 0.2)),
                elevation=float(item.get("elevation", 0.0)),
                name=item.get("name", "Slab"),
            )
            for item in data.get("slabs", [])
        ]
        spaces = [
            Space(
                id=item["id"],
                name=item.get("name", item["id"]),
                outline=[Vec2(**_point(p)) for p in item["outline"]],
                height=float(item.get("height", 3.0)),
                elevation=float(item.get("elevation", 0.0)),
            )
            for item in data.get("spaces", [])
        ]
        parts = [
            MechanicalPart(
                id=item["id"],
                name=item.get("name", item["id"]),
                profile=[Vec2(**_point(p)) for p in item["profile"]],
                thickness=float(item["thickness"]),
                holes=[Hole(**hole) for hole in item.get("holes", [])],
                material=item.get("material", "Steel"),
                units=item.get("units", "mm"),
            )
            for item in data.get("parts", [])
        ]
        return cls(
            name=data.get("name", "untitled"),
            domain=data.get("domain") or infer_domain(walls, parts),
            walls=walls,
            openings=openings,
            slabs=slabs,
            spaces=spaces,
            parts=parts,
            source=data.get("source", ""),
            warnings=list(data.get("warnings", [])),
            metadata=dict(data.get("metadata", {})),
        )


def infer_domain(walls: list[Wall], parts: list[MechanicalPart]) -> Domain:
    has_bim = bool(walls)
    has_mech = bool(parts)
    if has_bim and has_mech:
        return "both"
    if has_mech:
        return "mechanical"
    return "bim"


def _point(value: Any) -> dict[str, float]:
    if isinstance(value, dict):
        return {"x": float(value["x"]), "y": float(value["y"])}
    return {"x": float(value[0]), "y": float(value[1])}
