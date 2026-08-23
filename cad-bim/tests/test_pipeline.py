from __future__ import annotations

from pathlib import Path

import ezdxf
import ifcopenshell
import pymupdf as fitz

from cad_bim.adapters.input_dxf import load_dxf
from cad_bim.adapters.input_pdf import load_pdf
from cad_bim.adapters.output_dxf import write_dxf
from cad_bim.core.model import DesignIntent
from cad_bim.pipeline import build, inspect_input


def test_office_spec_builds_ifc_for_revit(examples_dir: Path, tmp_path: Path) -> None:
    result = build(examples_dir / "office_plan.json", tmp_path / "office", targets=("ifc", "step", "dxf"))
    assert result.report.passed, result.report.to_dict()
    model = ifcopenshell.open(str(result.artifacts["ifc"]))
    assert model.schema == "IFC4"
    assert len(model.by_type("IfcWall")) == 4
    assert len(model.by_type("IfcDoor")) == 1
    assert len(model.by_type("IfcWindow")) == 1
    assert len(model.by_type("IfcSlab")) == 1
    assert len(model.by_type("IfcSpace")) == 1
    assert model.by_type("IfcRelVoidsElement")
    assert result.artifacts["step"].read_text(encoding="utf-8", errors="ignore").startswith("ISO-10303-21;")


def test_bracket_spec_builds_step_for_solidworks(examples_dir: Path, tmp_path: Path) -> None:
    result = build(examples_dir / "l_bracket.json", tmp_path / "bracket", targets=("step", "dxf"))
    assert result.report.passed, result.report.to_dict()
    text = result.artifacts["step"].read_text(encoding="utf-8", errors="ignore")
    assert "AUTOMOTIVE_DESIGN" in text
    assert "MANIFOLD_SOLID_BREP" in text or "CLOSED_SHELL" in text
    assert "ifc" not in result.artifacts


def test_dxf_roundtrip_preserves_walls(examples_dir: Path, tmp_path: Path) -> None:
    intent = inspect_input(examples_dir / "office_plan.json")
    dxf_path = write_dxf(intent, tmp_path / "office.dxf")
    parsed = load_dxf(dxf_path)
    assert len(parsed.walls) == 4
    assert {wall.length for wall in parsed.walls} == {wall.length for wall in intent.walls}
    rebuilt = build(dxf_path, tmp_path / "from-dxf", targets=("ifc",))
    assert rebuilt.report.passed, rebuilt.report.to_dict()
    assert len(ifcopenshell.open(str(rebuilt.artifacts["ifc"])).by_type("IfcWall")) == 4


def test_vector_pdf_extracts_walls(tmp_path: Path) -> None:
    pdf_path = tmp_path / "room.pdf"
    document = fitz.open()
    page = document.new_page(width=900, height=700)
    page.draw_rect(fitz.Rect(50, 50, 850, 650), color=(0, 0, 0), width=2)
    page.insert_text((60, 40), "Office 8x6")
    document.save(pdf_path)
    document.close()

    intent = load_pdf(pdf_path)
    assert intent.walls
    assert "raster" not in " ".join(intent.warnings).lower()
    result = build(pdf_path, tmp_path / "from-pdf", targets=("ifc",))
    assert result.artifacts["ifc"].exists()
    assert ifcopenshell.open(str(result.artifacts["ifc"])).by_type("IfcWall")


def test_raster_pdf_does_not_invent_geometry(tmp_path: Path) -> None:
    pdf_path = tmp_path / "scan.pdf"
    document = fitz.open()
    page = document.new_page(width=300, height=300)
    page.insert_text((40, 40), "scanned sheet")
    document.save(pdf_path)
    document.close()
    intent = load_pdf(pdf_path)
    assert intent.walls == []
    assert intent.warnings


def test_json_spec_roundtrip(examples_dir: Path) -> None:
    original = inspect_input(examples_dir / "office_plan.json")
    clone = DesignIntent.from_dict(original.to_dict())
    assert clone.name == original.name
    assert len(clone.walls) == 4
    assert clone.openings[0].kind == "door"


def test_dxf_mechanical_layers(tmp_path: Path) -> None:
    document = ezdxf.new()
    document.layers.add("PART")
    document.layers.add("HOLE")
    msp = document.modelspace()
    msp.add_lwpolyline([(0, 0), (80, 0), (80, 8), (0, 8)], close=True, dxfattribs={"layer": "PART"})
    msp.add_circle((40, 4), 4, dxfattribs={"layer": "HOLE"})
    path = tmp_path / "plate.dxf"
    document.saveas(path)
    intent = load_dxf(path)
    assert intent.domain == "mechanical"
    assert len(intent.parts) == 1
    assert len(intent.parts[0].holes) == 1
