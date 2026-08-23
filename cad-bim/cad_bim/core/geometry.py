from __future__ import annotations

import math

from cad_bim.core.model import Vec2, Wall


def distance(a: Vec2, b: Vec2) -> float:
    return math.hypot(b.x - a.x, b.y - a.y)


def unit_vector(start: Vec2, end: Vec2) -> tuple[float, float]:
    length = distance(start, end)
    if length <= 1e-9:
        return (1.0, 0.0)
    return ((end.x - start.x) / length, (end.y - start.y) / length)


def point_along(start: Vec2, end: Vec2, offset: float) -> Vec2:
    ux, uy = unit_vector(start, end)
    return Vec2(start.x + ux * offset, start.y + uy * offset)


def project_param(wall: Wall, point: Vec2) -> float:
    ux, uy = unit_vector(wall.start, wall.end)
    return (point.x - wall.start.x) * ux + (point.y - wall.start.y) * uy


def distance_to_segment(wall: Wall, point: Vec2) -> float:
    length = wall.length
    if length <= 1e-9:
        return distance(wall.start, point)
    t = min(max(project_param(wall, point) / length, 0.0), 1.0)
    closest = point_along(wall.start, wall.end, t * length)
    return distance(closest, point)


def close_ring(points: list[Vec2], tolerance: float = 1e-6) -> list[Vec2]:
    if len(points) < 3:
        return list(points)
    if distance(points[0], points[-1]) > tolerance:
        return [*points, points[0]]
    return list(points)


def ring_area(points: list[Vec2]) -> float:
    ring = close_ring(points)
    area = 0.0
    for i in range(len(ring) - 1):
        area += ring[i].x * ring[i + 1].y - ring[i + 1].x * ring[i].y
    return 0.5 * area


def ensure_ccw(points: list[Vec2]) -> list[Vec2]:
    if ring_area(points) < 0:
        return list(reversed(points))
    return list(points)


def bbox(points: list[Vec2]) -> tuple[float, float, float, float]:
    xs = [p.x for p in points]
    ys = [p.y for p in points]
    return (min(xs), min(ys), max(xs), max(ys))


def centroid(points: list[Vec2]) -> Vec2:
    if not points:
        return Vec2(0.0, 0.0)
    return Vec2(sum(p.x for p in points) / len(points), sum(p.y for p in points) / len(points))
