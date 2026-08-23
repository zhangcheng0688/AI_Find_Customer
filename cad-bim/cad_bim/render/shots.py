from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from cad_bim.core.geometry import bbox, centroid
from cad_bim.core.model import DesignIntent, Vec2


@dataclass(frozen=True)
class CameraPose:
    x: float
    y: float
    z: float
    look_at: tuple[float, float, float]
    lens_mm: float = 35.0


@dataclass
class Shot:
    name: str
    kind: str
    frames: int
    start: CameraPose
    end: CameraPose
    notes: str


@dataclass
class ShotList:
    name: str
    fps: int
    resolution: tuple[int, int]
    engine: str
    shots: list[Shot] = field(default_factory=list)
    guidance: list[str] = field(default_factory=list)

    @property
    def duration_seconds(self) -> float:
        return sum(shot.frames for shot in self.shots) / self.fps

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["duration_seconds"] = self.duration_seconds
        return payload


def plan_walkthrough(intent: DesignIntent, fps: int = 24) -> ShotList:
    if intent.parts and not intent.spaces and not intent.walls:
        return _mechanical_turntable(intent, fps)
    return _interior_walk(intent, fps)


def _interior_walk(intent: DesignIntent, fps: int) -> ShotList:
    room = _room_frame(intent)
    cx, cy, min_x, min_y, max_x, max_y, height = room
    eye = 1.55
    look = (cx, cy, 1.2)
    door = next((item for item in intent.openings if item.kind == "door"), None)
    window = next((item for item in intent.openings if item.kind == "window"), None)

    entry = (min_x + 0.8, cy, eye)
    if door and intent.wall_by_id(door.wall_id):
        wall = intent.wall_by_id(door.wall_id)
        t = (door.offset + door.width / 2.0) / max(wall.length, 1e-6)
        entry = (
            wall.start.x + (wall.end.x - wall.start.x) * t,
            wall.start.y + (wall.end.y - wall.start.y) * t,
            eye,
        )

    shots = [
        Shot(
            name="01_establish",
            kind="hold",
            frames=fps * 3,
            start=CameraPose(min_x - 1.2, min_y - 1.2, height * 0.85, look, 24.0),
            end=CameraPose(min_x - 0.6, min_y - 0.6, height * 0.75, look, 24.0),
            notes="Wide establishing, 24mm, slow push. No handheld.",
        ),
        Shot(
            name="02_enter",
            kind="dolly",
            frames=fps * 5,
            start=CameraPose(entry[0], entry[1], eye, look, 35.0),
            end=CameraPose(cx - 0.4, cy - 0.2, eye, look, 35.0),
            notes="Enter at eye height. Ease in/out. Architecture wants stability.",
        ),
        Shot(
            name="03_lateral",
            kind="track",
            frames=fps * 4,
            start=CameraPose(min_x + 0.9, cy - 0.8, eye, (cx, max_y, 1.3), 35.0),
            end=CameraPose(max_x - 0.9, cy - 0.8, eye, (cx, max_y, 1.3), 35.0),
            notes="Lateral track along the long wall. Keep horizon locked.",
        ),
        Shot(
            name="04_window_light",
            kind="push",
            frames=fps * 4,
            start=CameraPose(cx, cy, eye, _window_target(intent, window, (cx, max_y, 1.4)), 50.0),
            end=CameraPose(cx, cy + 0.6, eye, _window_target(intent, window, (cx, max_y, 1.4)), 50.0),
            notes="Golden-hour window as hero. 50mm, shallow DOF.",
        ),
        Shot(
            name="05_hold",
            kind="hold",
            frames=fps * 2,
            start=CameraPose(cx, cy, 1.4, (cx, cy, 1.1), 35.0),
            end=CameraPose(cx, cy, 1.4, (cx, cy, 1.1), 35.0),
            notes="Two-second hold before cut. Grade in ACES.",
        ),
    ]
    return ShotList(
        name=intent.name,
        fps=fps,
        resolution=(1920, 1080),
        engine="cycles",
        shots=shots,
        guidance=[
            "Do not image-to-video this. Render in Twinmotion or Blender Cycles.",
            "Match Grok stills as lighting/material style frames only.",
            "24fps, ACES, physical sun + HDRI, slight DOF, no shake.",
        ],
    )


def _mechanical_turntable(intent: DesignIntent, fps: int) -> ShotList:
    part = intent.parts[0]
    center = centroid(part.profile)
    radius = max(abs(p.x - center.x) for p in part.profile) + 40.0
    height = part.thickness * 1.6
    look = (center.x, center.y, part.thickness / 2.0)
    shots = [
        Shot(
            name="01_hero",
            kind="hold",
            frames=fps * 2,
            start=CameraPose(center.x + radius, center.y - radius, height, look, 50.0),
            end=CameraPose(center.x + radius, center.y - radius, height, look, 50.0),
            notes="Hero still. Studio HDRI, three-point light.",
        ),
        Shot(
            name="02_orbit",
            kind="orbit",
            frames=fps * 6,
            start=CameraPose(center.x + radius, center.y, height, look, 50.0),
            end=CameraPose(center.x, center.y + radius, height, look, 50.0),
            notes="Quarter orbit. Keep the silhouette readable.",
        ),
    ]
    return ShotList(
        name=intent.name,
        fps=fps,
        resolution=(1920, 1080),
        engine="cycles",
        shots=shots,
        guidance=["Turntable, not a walkthrough. Export STEP for SolidWorks; render in Blender/Twinmotion."],
    )


def _room_frame(intent: DesignIntent) -> tuple[float, float, float, float, float, float, float]:
    points: list[Vec2] = []
    for space in intent.spaces:
        points.extend(space.outline)
    for slab in intent.slabs:
        points.extend(slab.outline)
    for wall in intent.walls:
        points.extend([wall.start, wall.end])
    if not points:
        points = [Vec2(0.0, 0.0), Vec2(8.0, 6.0)]
    min_x, min_y, max_x, max_y = bbox(points)
    height = max((wall.height for wall in intent.walls), default=3.0)
    return ((min_x + max_x) / 2.0, (min_y + max_y) / 2.0, min_x, min_y, max_x, max_y, height)


def _window_target(intent: DesignIntent, window, fallback: tuple[float, float, float]) -> tuple[float, float, float]:
    if window is None or intent.wall_by_id(window.wall_id) is None:
        return fallback
    wall = intent.wall_by_id(window.wall_id)
    t = (window.offset + window.width / 2.0) / max(wall.length, 1e-6)
    return (
        wall.start.x + (wall.end.x - wall.start.x) * t,
        wall.start.y + (wall.end.y - wall.start.y) * t,
        window.sill + window.height * 0.5,
    )
