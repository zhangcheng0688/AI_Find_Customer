from cad_bim.pipeline import inspect_input
from cad_bim.render.package import write_walkthrough_pack
from cad_bim.render.shots import plan_walkthrough


def test_office_walkthrough_is_cinematic_not_ai_video(examples_dir, tmp_path) -> None:
    intent = inspect_input(examples_dir / "office_plan.json")
    shots = plan_walkthrough(intent)
    assert shots.fps == 24
    assert shots.duration_seconds >= 15
    assert any(shot.kind == "dolly" for shot in shots.shots)
    assert any("24mm" in shot.notes or shot.start.lens_mm == 24 for shot in shots.shots)
    pack = write_walkthrough_pack(intent, tmp_path, ifc_path=tmp_path / "office.ifc")
    script = pack["blender"].read_text(encoding="utf-8")
    assert "CYCLES" in script
    assert "image-to-video" in script
    assert "BEZIER" in script


def test_bracket_uses_turntable(examples_dir) -> None:
    intent = inspect_input(examples_dir / "l_bracket.json")
    shots = plan_walkthrough(intent)
    assert any(shot.kind == "orbit" for shot in shots.shots)
