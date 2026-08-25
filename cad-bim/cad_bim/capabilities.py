from pathlib import Path

CAPABILITIES_PATH = Path(__file__).resolve().parent.parent / "CAPABILITIES.md"


def describe_capabilities() -> str:
    if CAPABILITIES_PATH.exists():
        return CAPABILITIES_PATH.read_text(encoding="utf-8").strip()
    return "See cad-bim/CAPABILITIES.md"
