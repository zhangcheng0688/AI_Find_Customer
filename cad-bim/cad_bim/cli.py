from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from cad_bim.adapters.computer_use import describe_host_requirements
from cad_bim.pipeline import build, inspect_input, run_demo


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="cad-bim",
        description="Build IFC (Revit/BIM) and STEP (SolidWorks) from PDF, DXF, or a JSON spec.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    build_cmd = sub.add_parser("build", help="Parse an input and emit IFC/STEP/DXF")
    build_cmd.add_argument("source", type=Path)
    build_cmd.add_argument("--out", type=Path, default=Path("out"))
    build_cmd.add_argument("--targets", default="auto", help="Comma list: ifc,step,dxf or auto")

    inspect_cmd = sub.add_parser("inspect", help="Parse an input and print DesignIntent JSON")
    inspect_cmd.add_argument("source", type=Path)

    demo_cmd = sub.add_parser("demo", help="Build the bundled office and bracket examples")
    demo_cmd.add_argument("--out", type=Path, default=Path("out/demo"))

    hosts = sub.add_parser("hosts", help="Explain native host / computer-use requirements")
    hosts.add_argument("app", choices=("revit", "solidworks", "autocad", "am12"))

    args = parser.parse_args(argv)

    if args.command == "inspect":
        intent = inspect_input(args.source)
        json.dump(intent.to_dict(), sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0
    if args.command == "hosts":
        print(describe_host_requirements(args.app))
        return 0
    if args.command == "demo":
        results = run_demo(args.out)
        payload = {name: result.to_dict() for name, result in results.items()}
        json.dump(payload, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0 if all(result.report.passed for result in results.values()) else 1

    targets = None if args.targets == "auto" else args.targets.split(",")
    result = build(args.source, args.out, targets=targets)
    json.dump(result.to_dict(), sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0 if result.report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
