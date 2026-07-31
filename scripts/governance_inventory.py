#!/usr/bin/env python3
"""Build and verify the deterministic dependency and licence inventory."""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from pathlib import Path
from typing import Any

OUTPUT = Path("docs/generated/governance-inventory.json")
ALLOWED_PROJECT_LICENCES = {"Apache-2.0"}


def build_inventory(root: Path) -> dict[str, Any]:
    """Return the repository-owned dependency and provenance inventory."""

    pyproject = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    cargo = tomllib.loads((root / "Cargo.toml").read_text(encoding="utf-8"))
    ecosystem = tomllib.loads((root / "ecosystem.lock.toml").read_text(encoding="utf-8"))
    project = pyproject["project"]
    workspace = cargo["workspace"]
    components = [
        {
            "name": component["name"],
            "repository": component["repository"],
            "revision": component["revision"],
            "license_decision": component["license"],
        }
        for component in ecosystem.get("component", [])
    ]
    return {
        "schema_version": 1,
        "project": {
            "name": project["name"],
            "version": project["version"],
            "license": project["license"],
            "python_runtime_dependencies": sorted(project.get("dependencies", [])),
            "python_optional_dependencies": {
                name: sorted(values)
                for name, values in sorted(project.get("optional-dependencies", {}).items())
            },
            "rust_workspace_members": sorted(workspace["members"]),
            "rust_version": cargo["workspace"]["package"]["rust-version"],
            "rust_license": cargo["workspace"]["package"]["license"],
        },
        "ecosystem": components,
        "open_decisions": [
            {
                "component": component["name"],
                "decision": component["license"],
            }
            for component in ecosystem.get("component", [])
            if "REVIEW_REQUIRED" in component["license"]
        ],
        "provenance": {
            "source_files": ["Cargo.toml", "ecosystem.lock.toml", "pyproject.toml"],
            "network_resolution": False,
            "generated_from_pins": True,
        },
    }


def validate_inventory(inventory: dict[str, Any]) -> list[str]:
    """Return fail-closed governance findings."""

    errors: list[str] = []
    project = inventory["project"]
    for field in ("license", "rust_license"):
        if project[field] not in ALLOWED_PROJECT_LICENCES:
            errors.append(f"unsupported project licence in {field}: {project[field]}")
    if project["python_runtime_dependencies"]:
        errors.append("base Python package must remain dependency-free")
    for component in inventory["ecosystem"]:
        revision = component["revision"]
        if len(revision) != 40 or any(character not in "0123456789abcdef" for character in revision):
            errors.append(f"ecosystem revision is not immutable: {component['name']}")
        if not component["license_decision"].strip():
            errors.append(f"missing licence decision: {component['name']}")
    return errors


def encoded(inventory: dict[str, Any]) -> str:
    """Encode the inventory canonically."""

    return json.dumps(inventory, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main(argv: list[str] | None = None) -> int:
    """Write or check the inventory."""

    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    root = Path.cwd()
    inventory = build_inventory(root)
    errors = validate_inventory(inventory)
    if errors:
        for error in errors:
            print(f"governance inventory error: {error}", file=sys.stderr)
        return 1
    content = encoded(inventory)
    output = root / OUTPUT
    if args.write:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")
        print(f"wrote {OUTPUT}")
        return 0
    if not output.exists() or output.read_text(encoding="utf-8") != content:
        print(f"governance inventory drift: run {sys.argv[0]} --write", file=sys.stderr)
        return 1
    print("governance inventory validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
