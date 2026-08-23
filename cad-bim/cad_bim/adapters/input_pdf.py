from __future__ import annotations

from pathlib import Path

import pymupdf as fitz

from cad_bim.core.model import DesignIntent, Vec2, Wall, infer_domain


def load_pdf(path: str | Path) -> DesignIntent:
    document = fitz.open(str(path))
    walls: list[Wall] = []
    warnings: list[str] = []
    texts: list[str] = []
    drawings = 0

    for page_index, page in enumerate(document):
        texts.extend(word[4] for word in page.get_text("words"))
        page_drawings = page.get_drawings()
        drawings += len(page_drawings)
        wall_index = len(walls)
        for drawing in page_drawings:
            points = _drawing_points(drawing)
            for start, end in zip(points, points[1:]):
                if _length(start, end) < 8:
                    continue
                wall_index += 1
                # PDF page units are points; treat them as millimetres scaled to metres
                # when the drawing looks architectural (span > 200 pt ≈ 2 m if 1pt=1cm).
                walls.append(
                    Wall(
                        id=f"W{wall_index}",
                        start=_to_meters(start),
                        end=_to_meters(end),
                        name=f"Wall {wall_index}",
                    )
                )
        if not page_drawings and page.get_images():
            warnings.append(
                f"Page {page_index + 1} looks like a raster scan. "
                "Vector extraction found no paths; dimensions must be checked by hand."
            )

    if drawings == 0 and not walls:
        warnings.append(
            "PDF has no vector geometry. Scanned drawings cannot be built precisely "
            "from pixels alone — provide a DXF or a JSON spec."
        )

    document.close()
    return DesignIntent(
        name=Path(path).stem,
        domain=infer_domain(walls, []),
        walls=walls,
        source=str(path),
        warnings=warnings,
        metadata={"extracted_text": texts[:80], "drawing_count": drawings},
    )


def _drawing_points(drawing: dict) -> list[Vec2]:
    points: list[Vec2] = []
    for item in drawing.get("items", []):
        kind = item[0]
        if kind == "l":
            p1, p2 = item[1], item[2]
            if not points:
                points.append(Vec2(float(p1.x), float(p1.y)))
            points.append(Vec2(float(p2.x), float(p2.y)))
        elif kind == "re":
            rect = item[1]
            x0, y0, x1, y1 = float(rect.x0), float(rect.y0), float(rect.x1), float(rect.y1)
            points.extend(
                [
                    Vec2(x0, y0),
                    Vec2(x1, y0),
                    Vec2(x1, y1),
                    Vec2(x0, y1),
                    Vec2(x0, y0),
                ]
            )
    return points


def _to_meters(point: Vec2) -> Vec2:
    # 1 PDF point ≈ 1/72 inch. Architectural sketches in this pipeline use 1 pt = 10 mm.
    return Vec2(point.x * 0.01, point.y * 0.01)


def _length(a: Vec2, b: Vec2) -> float:
    return ((b.x - a.x) ** 2 + (b.y - a.y) ** 2) ** 0.5
