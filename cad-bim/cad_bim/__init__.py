"""Neutral CAD/BIM build pipeline.

Given a PDF drawing, DXF, or JSON design spec, this package produces
IFC4 (Revit / openBIM) and STEP AP214 (SolidWorks / mechanical CAD).

It does not write native ``.rvt`` or ``.sldprt`` files. Those formats are
closed binaries and require the host application or a licensed cloud engine.
"""

from cad_bim.core.model import DesignIntent
from cad_bim.edit.ops import apply_ops
from cad_bim.pipeline import build, inspect_input, run_demo

__all__ = ["DesignIntent", "apply_ops", "build", "inspect_input", "run_demo"]
__version__ = "0.1.0"
