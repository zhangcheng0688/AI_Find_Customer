from __future__ import annotations

import json
from pathlib import Path

from cad_bim.core.model import DesignIntent


def load_spec(path: str | Path) -> DesignIntent:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    intent = DesignIntent.from_dict(payload)
    intent.source = str(path)
    return intent
