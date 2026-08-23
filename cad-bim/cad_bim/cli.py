from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from cad_bim.adapters.computer_use import describe_host_requirements
from cad_bim.inputs import describe_inputs
from cad_bim.pipeline import build, inspect_input, run_demo
from cad_bim.render.package import write_walkthrough_pack
from cad_bim.render.playbook import describe_walkthrough


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
    build_cmd.add_argument("--patch", type=Path, help="JSON list of direct-edit operations")

    edit_cmd = sub.add_parser("edit", help="Load a model, apply direct edits, rebuild IFC/STEP/DXF")
    edit_cmd.add_argument("source", type=Path)
    edit_cmd.add_argument("--patch", type=Path, required=True)
    edit_cmd.add_argument("--out", type=Path, default=Path("out"))
    edit_cmd.add_argument("--targets", default="auto")

    inspect_cmd = sub.add_parser("inspect", help="Parse an input and print DesignIntent JSON")
    inspect_cmd.add_argument("source", type=Path)

    demo_cmd = sub.add_parser("demo", help="Build the bundled office and bracket examples")
    demo_cmd.add_argument("--out", type=Path, default=Path("out/demo"))

    hosts = sub.add_parser("hosts", help="Explain native host / computer-use requirements")
    hosts.add_argument("app", choices=("revit", "solidworks", "autocad", "am12"))

    sub.add_parser("inputs", help="Print the input contract for CAD / Revit / SolidWorks work")

    walk_cmd = sub.add_parser("walkthrough", help="Write a cinematic shot list + Blender Cycles script")
    walk_cmd.add_argument("source", type=Path)
    walk_cmd.add_argument("--out", type=Path, default=Path("out/walkthrough"))
    walk_cmd.add_argument("--ifc", type=Path, help="Optional IFC for Bonsai import")

    sub.add_parser("cinematic", help="Explain why AI walkthroughs look cheap and what to use instead")

    args = parser.parse_args(argv)

    if args.command == "inspect":
        intent = inspect_input(args.source)
        json.dump(intent.to_dict(), sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0
    if args.command == "hosts":
        print(describe_host_requirements(args.app))
        return 0
    if args.command == "inputs":
        print(describe_inputs())
        return 0
    if args.command == "cinematic":
        print(describe_walkthrough())
        return 0
    if args.command == "walkthrough":
        intent = inspect_input(args.source)
        artifacts = write_walkthrough_pack(intent, args.out, ifc_path=args.ifc)
        json.dump({key: str(path) for key, path in artifacts.items()}, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0
    if args.command == "demo":
        results = run_demo(args.out)
        payload = {name: result.to_dict() for name, result in results.items()}
        json.dump(payload, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0 if all(result.report.passed for result in results.values()) else 1

    targets = None if args.targets == "auto" else args.targets.split(",")
    operations = None
    if getattr(args, "patch", None):
        operations = json.loads(Path(args.patch).read_text(encoding="utf-8"))
        if isinstance(operations, dict) and "ops" in operations:
            operations = operations["ops"]
    result = build(args.source, args.out, targets=targets, operations=operations)
    json.dump(result.to_dict(), sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0 if result.report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
