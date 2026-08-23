from __future__ import annotations

import json
from pathlib import Path

from cad_bim.core.model import DesignIntent
from cad_bim.render.blender_export import write_blender_script
from cad_bim.render.playbook import describe_walkthrough
from cad_bim.render.shots import ShotList, plan_walkthrough


def write_walkthrough_pack(
    intent: DesignIntent,
    out_dir: str | Path,
    ifc_path: str | Path | None = None,
) -> dict[str, Path]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    shots: ShotList = plan_walkthrough(intent)
    shots_path = out / "shots.json"
    shots_path.write_text(json.dumps(shots.to_dict(), indent=2), encoding="utf-8")
    script_path = write_blender_script(
        shots,
        out / "cinematic.py",
        ifc_path=str(ifc_path) if ifc_path else None,
    )
    playbook_path = out / "PLAYBOOK.txt"
    playbook_path.write_text(describe_walkthrough() + "\n", encoding="utf-8")
    return {
        "shots": shots_path,
        "blender": script_path,
        "playbook": playbook_path,
    }
