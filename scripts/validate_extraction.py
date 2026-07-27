#!/usr/bin/env python3
"""Validate that domain-neutral Rust crates form a self-contained extraction set."""

from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path


def main() -> int:
    """Validate the committed extraction manifest and crate boundaries."""

    root = Path.cwd()
    manifest = json.loads((root / "extraction-manifest.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    crates = [root / path for path in manifest["crates"]]
    declared_names: set[str] = set()
    dependencies: dict[str, set[str]] = {}
    for crate in crates:
        cargo_path = crate / "Cargo.toml"
        source_path = crate / "src"
        if not cargo_path.is_file() or not source_path.is_dir():
            errors.append(f"incomplete extraction crate: {crate.relative_to(root)}")
            continue
        cargo = tomllib.loads(cargo_path.read_text(encoding="utf-8"))
        name = cargo["package"]["name"]
        declared_names.add(name)
        dependencies[name] = set(cargo.get("dependencies", {}))
        for source in source_path.rglob("*.rs"):
            content = source.read_text(encoding="utf-8").lower()
            for term in manifest["forbidden_vocabulary"]:
                if re.search(rf"\b{re.escape(term.lower())}\b", content):
                    errors.append(
                        f"forbidden extraction vocabulary {term!r}: {source.relative_to(root)}"
                    )
    expected = set(manifest["allowed_internal_dependencies"])
    if declared_names != expected:
        errors.append(
            f"manifest crate names differ: expected {sorted(expected)}, got {sorted(declared_names)}"
        )
    for crate, allowed in manifest["allowed_internal_dependencies"].items():
        internal = dependencies.get(crate, set()) & declared_names
        if internal != set(allowed):
            errors.append(
                f"unexpected internal dependencies for {crate}: {sorted(internal)}"
            )
    if errors:
        print("extraction validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"extraction validation passed ({len(crates)} crates)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
