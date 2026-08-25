from __future__ import annotations

from pathlib import Path

import ifcopenshell
import ifcopenshell.util.element
import ifcopenshell.util.placement
import ifcopenshell.util.unit

from cad_bim.core.model import DesignIntent, Opening, Slab, Space, Vec2, Wall, infer_domain


def load_ifc(path: str | Path) -> DesignIntent:
    model = ifcopenshell.open(str(path))
    scale = ifcopenshell.util.unit.calculate_unit_scale(model)
    walls: list[Wall] = []
    openings: list[Opening] = []
    slabs: list[Slab] = []
    spaces: list[Space] = []
    warnings: list[str] = []

    for entity in model.by_type("IfcWall"):
        tag = _cadbim(entity)
        matrix = _placement(entity, scale)
        start = Vec2(float(matrix[0, 3]), float(matrix[1, 3]))
        direction = (float(matrix[0, 0]), float(matrix[1, 0]))
        length = float(tag.get("length") or _extrusion_length(entity) or 1.0)
        end = Vec2(start.x + direction[0] * length, start.y + direction[1] * length)
        walls.append(
            Wall(
                id=str(tag.get("cad_id") or tag.get("id") or entity.Name or entity.GlobalId),
                start=start,
                end=end,
                height=float(tag.get("height") or _extrusion_depth(entity) or 3.0),
                thickness=float(tag.get("thickness") or 0.2),
                elevation=float(matrix[2, 3]),
                name=entity.Name or "",
            )
        )
        if entity.Representation is None:
            warnings.append(f"IfcWall {entity.Name} has no body representation")

    wall_ids = {wall.id for wall in walls}
    for filling in list(model.by_type("IfcDoor")) + list(model.by_type("IfcWindow")):
        tag = _cadbim(filling)
        kind = tag.get("kind") or ("door" if filling.is_a("IfcDoor") else "window")
        wall_id = str(tag.get("wall_id") or _host_wall_id(filling) or "")
        if wall_id not in wall_ids and walls:
            wall_id = walls[0].id
            warnings.append(f"{filling.Name} had no host wall; attached to {wall_id}")
        openings.append(
            Opening(
                id=str(tag.get("cad_id") or filling.Name or filling.GlobalId),
                wall_id=wall_id,
                kind=kind,  # type: ignore[arg-type]
                offset=float(tag.get("offset") or 0.0),
                width=float(tag.get("width") or getattr(filling, "OverallWidth", None) or 0.9),
                height=float(tag.get("height") or getattr(filling, "OverallHeight", None) or 2.1),
                sill=float(tag.get("sill") or 0.0),
                name=filling.Name or "",
            )
        )

    for entity in model.by_type("IfcSlab"):
        tag = _cadbim(entity)
        outline = _profile_points(entity, scale)
        if not outline:
            warnings.append(f"IfcSlab {entity.Name} has no readable footprint")
            continue
        slabs.append(
            Slab(
                id=str(tag.get("cad_id") or tag.get("id") or entity.Name or entity.GlobalId),
                outline=outline,
                thickness=float(tag.get("thickness") or _extrusion_depth(entity) or 0.2),
                name=entity.Name or "Slab",
            )
        )

    for entity in model.by_type("IfcSpace"):
        tag = _cadbim(entity)
        outline = _profile_points(entity, scale)
        if not outline:
            continue
        spaces.append(
            Space(
                id=str(tag.get("cad_id") or tag.get("id") or entity.Name or entity.GlobalId),
                name=entity.Name or "Space",
                outline=outline,
                height=float(tag.get("height") or _extrusion_depth(entity) or 3.0),
            )
        )

    project = model.by_type("IfcProject")
    return DesignIntent(
        name=project[0].Name if project and project[0].Name else Path(path).stem,
        domain=infer_domain(walls, []),
        walls=walls,
        openings=openings,
        slabs=slabs,
        spaces=spaces,
        source=str(path),
        warnings=warnings,
        metadata={"schema": model.schema, "tool": "ifc"},
    )


def _cadbim(entity) -> dict:
    psets = ifcopenshell.util.element.get_psets(entity)
    data = dict(psets.get("Pset_CadBim") or {})
    data.pop("id", None)  # IfcOpenShell injects the pset entity id
    common = psets.get("Pset_WallCommon") or {}
    if common.get("Reference") and not data.get("cad_id"):
        data["cad_id"] = common["Reference"]
    return data


def _placement(entity, scale: float):
    if entity.ObjectPlacement is None:
        import numpy as np

        return np.eye(4)
    matrix = ifcopenshell.util.placement.get_local_placement(entity.ObjectPlacement).copy()
    matrix[0, 3] *= scale
    matrix[1, 3] *= scale
    matrix[2, 3] *= scale
    return matrix


def _extrusion_depth(entity) -> float | None:
    solid = _first_extrusion(entity)
    return float(solid.Depth) if solid is not None else None


def _extrusion_length(entity) -> float | None:
    solid = _first_extrusion(entity)
    if solid is None:
        return None
    profile = solid.SweptArea
    if profile is not None and profile.is_a("IfcRectangleProfileDef"):
        return float(profile.XDim)
    return float(solid.Depth)


def _first_extrusion(entity):
    if entity.Representation is None:
        return None
    for representation in entity.Representation.Representations:
        for item in representation.Items or []:
            if item.is_a("IfcExtrudedAreaSolid"):
                return item
    return None


def _profile_points(entity, scale: float) -> list[Vec2]:
    solid = _first_extrusion(entity)
    if solid is None:
        return []
    profile = solid.SweptArea
    if profile is None or not hasattr(profile, "OuterCurve"):
        return []
    curve = profile.OuterCurve
    if curve.is_a("IfcIndexedPolyCurve") and curve.Points:
        coords = curve.Points.CoordList
        return [Vec2(float(x) * scale, float(y) * scale) for x, y, *_ in coords]
    return []


def _host_wall_id(filling) -> str | None:
    for rel in getattr(filling, "FillsVoids", []) or []:
        opening = rel.RelatingOpeningElement
        for void in getattr(opening, "VoidsElements", []) or []:
            host = void.RelatingBuildingElement
            tag = _cadbim(host)
            return str(tag.get("cad_id") or tag.get("id") or host.Name or host.GlobalId)
    return None
