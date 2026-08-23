from __future__ import annotations

from pathlib import Path

import ifcopenshell

from cad_bim.adapters.input_ifc import load_ifc
from cad_bim.pipeline import build, inspect_input


def test_ifc_walls_have_body_geometry(examples_dir: Path, tmp_path: Path) -> None:
    result = build(examples_dir / "office_plan.json", tmp_path, targets=("ifc",))
    model = ifcopenshell.open(str(result.artifacts["ifc"]))
    assert all(wall.Representation for wall in model.by_type("IfcWall"))


def test_direct_bim_edit_roundtrips_ifc(examples_dir: Path, tmp_path: Path) -> None:
    first = build(examples_dir / "office_plan.json", tmp_path / "v1", targets=("ifc",))
    edited = build(
        first.artifacts["ifc"],
        tmp_path / "v2",
        targets=("ifc",),
        operations=[
            {"op": "set_wall", "id": "W1", "thickness": 0.3, "height": 3.2},
            {"op": "set_opening", "id": "D1", "width": 1.0},
            {
                "op": "add_opening",
                "id": "WIN2",
                "wall_id": "W2",
                "kind": "window",
                "offset": 2.0,
                "width": 1.2,
                "height": 1.5,
                "sill": 0.9,
            },
        ],
    )
    assert edited.report.passed, edited.report.to_dict()
    model = ifcopenshell.open(str(edited.artifacts["ifc"]))
    assert len(model.by_type("IfcWindow")) == 2
    intent = load_ifc(edited.artifacts["ifc"])
    assert intent.wall_by_id("W1").thickness == 0.3
    assert intent.wall_by_id("W1").height == 3.2
    assert intent.opening_by_id("D1").width == 1.0


def test_direct_solidworks_edit_rebuilds_step(examples_dir: Path, tmp_path: Path) -> None:
    result = build(
        examples_dir / "l_bracket.json",
        tmp_path,
        targets=("step",),
        operations=[
            {"op": "set_part", "id": "P1", "thickness": 16},
            {"op": "add_hole", "id": "P1", "x": 20, "y": 4, "radius": 3},
        ],
    )
    assert result.report.passed, result.report.to_dict()
    assert result.intent.part_by_id("P1").thickness == 16
    assert len(result.intent.part_by_id("P1").holes) == 3


def test_direct_cad_edit_from_dxf(examples_dir: Path, tmp_path: Path) -> None:
    original = inspect_input(examples_dir / "office_plan.json")
    from cad_bim.adapters.output_dxf import write_dxf

    dxf = write_dxf(original, tmp_path / "office.dxf")
    result = build(
        dxf,
        tmp_path / "edited",
        targets=("dxf", "ifc"),
        operations=[{"op": "move_wall", "id": "W1", "dx": 1.0, "dy": 0.0}],
    )
    assert result.report.passed, result.report.to_dict()
    assert abs(result.intent.wall_by_id("W1").start.x - 1.0) < 1e-6
