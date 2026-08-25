from __future__ import annotations

from pathlib import Path

import numpy as np

import ifcopenshell
import ifcopenshell.api.aggregate
import ifcopenshell.api.context
import ifcopenshell.api.feature
import ifcopenshell.api.geometry
import ifcopenshell.api.profile
import ifcopenshell.api.project
import ifcopenshell.api.pset
import ifcopenshell.api.root
import ifcopenshell.api.spatial
import ifcopenshell.api.unit

from cad_bim.core.geometry import close_ring, unit_vector
from cad_bim.core.model import DesignIntent, Opening, Slab, Space, Wall


def write_ifc(intent: DesignIntent, path: str | Path) -> Path:
    path = Path(path)
    model = ifcopenshell.api.project.create_file(version="IFC4")
    project = ifcopenshell.api.root.create_entity(model, ifc_class="IfcProject", name=intent.name)
    length = ifcopenshell.api.unit.add_si_unit(model, unit_type="LENGTHUNIT")
    area = ifcopenshell.api.unit.add_si_unit(model, unit_type="AREAUNIT")
    volume = ifcopenshell.api.unit.add_si_unit(model, unit_type="VOLUMEUNIT")
    ifcopenshell.api.unit.assign_unit(model, units=[length, area, volume])

    model_ctx = ifcopenshell.api.context.add_context(model, context_type="Model")
    body = ifcopenshell.api.context.add_context(
        model,
        context_type="Model",
        context_identifier="Body",
        target_view="MODEL_VIEW",
        parent=model_ctx,
    )

    site = ifcopenshell.api.root.create_entity(model, ifc_class="IfcSite", name="Site")
    building = ifcopenshell.api.root.create_entity(model, ifc_class="IfcBuilding", name=intent.name)
    storey = ifcopenshell.api.root.create_entity(model, ifc_class="IfcBuildingStorey", name="Level 0")
    ifcopenshell.api.aggregate.assign_object(model, relating_object=project, products=[site])
    ifcopenshell.api.aggregate.assign_object(model, relating_object=site, products=[building])
    ifcopenshell.api.aggregate.assign_object(model, relating_object=building, products=[storey])

    walls_by_id: dict[str, object] = {}
    for wall in intent.walls:
        walls_by_id[wall.id] = _add_wall(model, body, storey, wall)

    for opening in intent.openings:
        host = walls_by_id.get(opening.wall_id)
        source_wall = intent.wall_by_id(opening.wall_id)
        if host is None or source_wall is None:
            continue
        _add_opening(model, body, storey, host, source_wall, opening)

    for slab in intent.slabs:
        _add_slab(model, body, storey, slab)

    for space in intent.spaces:
        _add_space(model, body, storey, space)

    path.parent.mkdir(parents=True, exist_ok=True)
    model.write(str(path))
    return path


def _add_wall(model, body, storey, wall: Wall):
    entity = ifcopenshell.api.root.create_entity(model, ifc_class="IfcWall", name=wall.name or wall.id)
    ifcopenshell.api.spatial.assign_container(model, relating_structure=storey, products=[entity])
    representation = ifcopenshell.api.geometry.create_2pt_wall(
        model,
        element=entity,
        context=body,
        p1=wall.start.as_tuple(),
        p2=wall.end.as_tuple(),
        elevation=wall.elevation,
        height=wall.height,
        thickness=wall.thickness,
        is_si=True,
    )
    ifcopenshell.api.geometry.assign_representation(model, product=entity, representation=representation)
    pset = ifcopenshell.api.pset.add_pset(model, product=entity, name="Pset_WallCommon")
    ifcopenshell.api.pset.edit_pset(
        model,
        pset=pset,
        properties={"IsExternal": True, "LoadBearing": True, "Reference": wall.id},
    )
    _tag(
        model,
        entity,
        {
            "cad_id": wall.id,
            "kind": "wall",
            "thickness": wall.thickness,
            "height": wall.height,
            "length": wall.length,
        },
    )
    return entity


def _add_opening(model, body, storey, host, wall: Wall, opening: Opening) -> None:
    feature = ifcopenshell.api.root.create_entity(
        model, ifc_class="IfcOpeningElement", name=f"{opening.id}-void"
    )
    ifc_class = "IfcDoor" if opening.kind == "door" else "IfcWindow"
    filling = ifcopenshell.api.root.create_entity(
        model, ifc_class=ifc_class, name=opening.name or opening.id
    )
    ifcopenshell.api.spatial.assign_container(model, relating_structure=storey, products=[filling])

    matrix = _opening_matrix(wall, opening)
    ifcopenshell.api.geometry.edit_object_placement(model, product=feature, matrix=matrix, is_si=True)
    ifcopenshell.api.geometry.edit_object_placement(model, product=filling, matrix=matrix, is_si=True)
    void = ifcopenshell.api.geometry.add_wall_representation(
        model,
        context=body,
        length=opening.width,
        height=opening.height,
        thickness=wall.thickness + 0.05,
    )
    ifcopenshell.api.geometry.assign_representation(model, product=feature, representation=void)
    if opening.kind == "door":
        representation = ifcopenshell.api.geometry.add_door_representation(
            model, context=body, overall_width=opening.width, overall_height=opening.height
        )
    else:
        representation = ifcopenshell.api.geometry.add_window_representation(
            model, context=body, overall_width=opening.width, overall_height=opening.height
        )
    if representation:
        ifcopenshell.api.geometry.assign_representation(model, product=filling, representation=representation)
    ifcopenshell.api.feature.add_feature(model, feature=feature, element=host)
    ifcopenshell.api.feature.add_filling(model, opening=feature, element=filling)
    _tag(
        model,
        filling,
        {
            "cad_id": opening.id,
            "kind": opening.kind,
            "wall_id": opening.wall_id,
            "offset": opening.offset,
            "width": opening.width,
            "height": opening.height,
            "sill": opening.sill,
        },
    )


def _add_slab(model, body, storey, slab: Slab) -> None:
    entity = ifcopenshell.api.root.create_entity(model, ifc_class="IfcSlab", name=slab.name or slab.id)
    ifcopenshell.api.spatial.assign_container(model, relating_structure=storey, products=[entity])
    matrix = np.eye(4)
    matrix[2, 3] = slab.elevation
    ifcopenshell.api.geometry.edit_object_placement(model, product=entity, matrix=matrix, is_si=True)
    polyline = [point.as_tuple() for point in slab.outline]
    representation = ifcopenshell.api.geometry.add_slab_representation(
        model, context=body, depth=slab.thickness, polyline=polyline
    )
    ifcopenshell.api.geometry.assign_representation(model, product=entity, representation=representation)
    _tag(model, entity, {"cad_id": slab.id, "kind": "slab", "thickness": slab.thickness})


def _add_space(model, body, storey, space: Space) -> None:
    entity = ifcopenshell.api.root.create_entity(model, ifc_class="IfcSpace", name=space.name)
    ifcopenshell.api.aggregate.assign_object(model, relating_object=storey, products=[entity])
    matrix = np.eye(4)
    matrix[2, 3] = space.elevation
    ifcopenshell.api.geometry.edit_object_placement(model, product=entity, matrix=matrix, is_si=True)
    ring = close_ring(space.outline)
    profile = ifcopenshell.api.profile.add_arbitrary_profile(
        model, profile=[point.as_tuple() for point in ring], name=space.name
    )
    representation = ifcopenshell.api.geometry.add_profile_representation(
        model, context=body, profile=profile, depth=space.height
    )
    ifcopenshell.api.geometry.assign_representation(model, product=entity, representation=representation)
    _tag(model, entity, {"cad_id": space.id, "kind": "space", "height": space.height})


def _tag(model, product, properties: dict) -> None:
    pset = ifcopenshell.api.pset.add_pset(model, product=product, name="Pset_CadBim")
    ifcopenshell.api.pset.edit_pset(model, pset=pset, properties=properties)


def _opening_matrix(wall: Wall, opening: Opening) -> np.ndarray:
    ux, uy = unit_vector(wall.start, wall.end)
    px = -uy
    py = ux
    mid = opening.offset + opening.width / 2.0
    matrix = np.eye(4)
    matrix[0, 0], matrix[1, 0], matrix[2, 0] = ux, uy, 0.0
    matrix[0, 1], matrix[1, 1], matrix[2, 1] = px, py, 0.0
    matrix[0, 2], matrix[1, 2], matrix[2, 2] = 0.0, 0.0, 1.0
    matrix[0, 3] = wall.start.x + ux * mid
    matrix[1, 3] = wall.start.y + uy * mid
    matrix[2, 3] = wall.elevation + opening.sill
    return matrix
