from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

HostApp = Literal["revit", "solidworks", "autocad", "am12"]


class HostApplicationRequired(RuntimeError):
    """Raised when a native host or licensed cloud engine is required."""


@dataclass(frozen=True)
class HostJob:
    host: HostApp
    model_path: Path
    action: str = "import_and_validate"


def describe_host_requirements(host: HostApp) -> str:
    if host == "revit":
        return (
            "Native .rvt write needs Windows + a Revit license (pyRevit / Revit API) "
            "or Autodesk Platform Services Design Automation. IFC4 from this pipeline "
            "is the license-free handoff Revit already opens and links."
        )
    if host == "solidworks":
        return (
            "Native .sldprt write needs Windows + SolidWorks COM API. "
            "STEP AP214 from this pipeline opens as a solid; the feature tree does not come along."
        )
    if host == "autocad":
        return (
            "Native DWG write still needs AutoCAD or the ODA SDK. "
            "DXF from this pipeline is the open exchange path."
        )
    return (
        "AM12 has no public script API. Import (IMP) is a GUI last mile: "
        "computer-use on a licensed workstation, not this geometry kernel."
    )


def run_host_job(job: HostJob) -> None:
    raise HostApplicationRequired(
        f"Refusing to pretend {job.host} ran '{job.action}' on {job.model_path}. "
        + describe_host_requirements(job.host)
    )
