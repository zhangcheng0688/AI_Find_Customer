from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import ifcopenshell

from cad_bim.core.model import DesignIntent


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str


@dataclass
class VerificationReport:
    passed: bool
    checks: list[CheckResult] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "checks": [asdict(item) for item in self.checks],
        }


def verify_outputs(intent: DesignIntent, artifacts: dict[str, Path]) -> VerificationReport:
    checks: list[CheckResult] = []
    if "ifc" in artifacts:
        checks.extend(_verify_ifc(intent, artifacts["ifc"]))
    if "step" in artifacts:
        checks.extend(_verify_step(intent, artifacts["step"]))
    if "dxf" in artifacts:
        checks.append(_file_exists("dxf_written", artifacts["dxf"]))
    return VerificationReport(passed=all(item.passed for item in checks), checks=checks)


def _verify_ifc(intent: DesignIntent, path: Path) -> list[CheckResult]:
    checks = [_file_exists("ifc_written", path)]
    if not path.exists():
        return checks
    model = ifcopenshell.open(str(path))
    checks.append(
        CheckResult("ifc_schema", model.schema.upper().startswith("IFC4"), f"schema={model.schema}")
    )
    expected = {
        "IfcWall": len(intent.walls),
        "IfcDoor": sum(1 for item in intent.openings if item.kind == "door"),
        "IfcWindow": sum(1 for item in intent.openings if item.kind == "window"),
        "IfcSlab": len(intent.slabs),
        "IfcSpace": len(intent.spaces),
    }
    for ifc_class, count in expected.items():
        actual = len(model.by_type(ifc_class))
        checks.append(
            CheckResult(
                f"count_{ifc_class}",
                actual == count,
                f"expected={count} actual={actual}",
            )
        )
    checks.append(
        CheckResult(
            "ifc_spatial_tree",
            bool(model.by_type("IfcProject") and model.by_type("IfcBuildingStorey")),
            "project/site/building/storey present",
        )
    )
    walls_with_body = [wall for wall in model.by_type("IfcWall") if wall.Representation]
    checks.append(
        CheckResult(
            "ifc_wall_geometry",
            len(walls_with_body) == len(model.by_type("IfcWall")),
            f"walls_with_body={len(walls_with_body)}",
        )
    )
    return checks


def _verify_step(intent: DesignIntent, path: Path) -> list[CheckResult]:
    checks = [_file_exists("step_written", path)]
    if not path.exists():
        return checks
    text = path.read_text(encoding="utf-8", errors="ignore")
    checks.append(CheckResult("step_header", text.startswith("ISO-10303-21;"), "ISO-10303-21 header"))
    checks.append(
        CheckResult(
            "step_schema",
            "AUTOMOTIVE_DESIGN" in text.upper() or "CONFIG_CONTROL_DESIGN" in text.upper(),
            "AP214/AP203 schema",
        )
    )
    solid = any(
        token in text
        for token in (
            "MANIFOLD_SOLID_BREP",
            "ADVANCED_BREP_SHAPE_REPRESENTATION",
            "CLOSED_SHELL",
            "BREP_WITH_VOIDS",
        )
    )
    checks.append(CheckResult("step_solid", solid, "BRep solid entities present"))
    if intent.parts:
        min_bytes = 1500
        checks.append(
            CheckResult(
                "step_size",
                path.stat().st_size >= min_bytes,
                f"size={path.stat().st_size} bytes",
            )
        )
    return checks


def _file_exists(name: str, path: Path) -> CheckResult:
    return CheckResult(name, path.exists() and path.stat().st_size > 0, str(path))
