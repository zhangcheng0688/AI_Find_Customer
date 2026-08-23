from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from cad_bim.adapters.input_dxf import load_dxf
from cad_bim.adapters.input_pdf import load_pdf
from cad_bim.adapters.input_spec import load_spec
from cad_bim.adapters.output_dxf import write_dxf
from cad_bim.adapters.output_ifc import write_ifc
from cad_bim.adapters.output_step import write_step
from cad_bim.core.model import DesignIntent
from cad_bim.verify.checks import VerificationReport, verify_outputs

SUPPORTED_TARGETS = ("ifc", "step", "dxf")


@dataclass
class BuildResult:
    intent: DesignIntent
    artifacts: dict[str, Path]
    report: VerificationReport
    skipped: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "name": self.intent.name,
            "domain": self.intent.domain,
            "source": self.intent.source,
            "warnings": self.intent.warnings,
            "artifacts": {key: str(path) for key, path in self.artifacts.items()},
            "skipped": self.skipped,
            "verification": self.report.to_dict(),
        }


def inspect_input(path: str | Path) -> DesignIntent:
    return _load(Path(path))


def build(
    source: str | Path,
    out_dir: str | Path,
    targets: Iterable[str] | None = None,
) -> BuildResult:
    intent = _load(Path(source))
    return emit(intent, out_dir, targets)


def emit(
    intent: DesignIntent,
    out_dir: str | Path,
    targets: Iterable[str] | None = None,
) -> BuildResult:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    wanted = _normalize_targets(targets, intent)
    artifacts: dict[str, Path] = {}
    skipped: list[str] = []

    if "ifc" in wanted:
        if intent.walls or intent.slabs or intent.spaces:
            artifacts["ifc"] = write_ifc(intent, out / f"{intent.name}.ifc")
        else:
            skipped.append("ifc: no BIM entities (walls/slabs/spaces)")
    if "step" in wanted:
        if intent.parts or intent.walls:
            artifacts["step"] = write_step(intent, out / f"{intent.name}.step")
        else:
            skipped.append("step: no parts or walls to solidify")
    if "dxf" in wanted:
        artifacts["dxf"] = write_dxf(intent, out / f"{intent.name}.dxf")

    report = verify_outputs(intent, artifacts)
    (out / "intent.json").write_text(json.dumps(intent.to_dict(), indent=2), encoding="utf-8")
    (out / "report.json").write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    return BuildResult(intent=intent, artifacts=artifacts, report=report, skipped=skipped)


def run_demo(out_dir: str | Path) -> dict[str, BuildResult]:
    root = Path(__file__).resolve().parent.parent / "examples"
    results = {
        "office": build(root / "office_plan.json", Path(out_dir) / "office", targets=("ifc", "step", "dxf")),
        "bracket": build(root / "l_bracket.json", Path(out_dir) / "bracket", targets=("step", "dxf")),
    }
    return results


def _load(path: Path) -> DesignIntent:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return load_spec(path)
    if suffix == ".dxf":
        return load_dxf(path)
    if suffix == ".pdf":
        return load_pdf(path)
    raise ValueError(f"Unsupported input type {suffix}. Use .json, .dxf, or .pdf")


def _normalize_targets(targets: Iterable[str] | None, intent: DesignIntent) -> set[str]:
    if targets is None:
        if intent.domain == "mechanical":
            return {"step", "dxf"}
        if intent.domain == "bim":
            return {"ifc", "step", "dxf"}
        return set(SUPPORTED_TARGETS)
    wanted = {item.strip().lower() for item in targets}
    unknown = wanted - set(SUPPORTED_TARGETS)
    if unknown:
        raise ValueError(f"Unknown targets: {sorted(unknown)}")
    return wanted
