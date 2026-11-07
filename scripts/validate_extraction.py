#!/usr/bin/env python3
"""Validate immutable Paignia consumption and reject a parallel local game core."""

from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path


def validate_provider(root: Path) -> list[str]:
    """Check source ownership and pin/lock coherence without claiming execution."""
    manifest = json.loads((root / "extraction-manifest.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    if manifest.get("mode") != "external_provider":
        errors.append("application must consume the external Paignia provider")
    provider = manifest["provider"]
    revision = provider.get("revision")
    if not isinstance(revision, str) or re.fullmatch(r"[0-9a-f]{40}", revision) is None:
        errors.append("Paignia provider requires an actual immutable 40-character revision")
    if manifest.get("crates") or manifest.get("allowed_internal_dependencies"):
        errors.append("generic game packages must not remain application-owned workspace members")
    ecosystem = tomllib.loads((root / "ecosystem.lock.toml").read_text(encoding="utf-8"))
    pins = [item for item in ecosystem["component"] if item["name"] == "Paignia"]
    if len(pins) != 1 or any(
        pins[0].get(key) != provider[key] for key in ("repository", "revision")
    ):
        errors.append("Paignia ecosystem pin does not match the Cargo provider contract")
    for name in manifest["forbidden_local_crates"]:
        if (root / name).exists():
            errors.append(f"parallel local game core is forbidden: {name}")

    workspace = tomllib.loads((root / "Cargo.toml").read_text(encoding="utf-8"))
    if workspace["workspace"]["members"] != ["crates/new-drug-reimbursement-game"]:
        errors.append("consumer workspace must contain only its application member")
    for member in workspace["workspace"]["members"]:
        if member in manifest["forbidden_local_crates"]:
            errors.append(f"workspace still declares a local game core: {member}")
    packages = provider["packages"]
    for patches in workspace.get("patch", {}).values():
        for name, declaration in patches.items():
            actual = declaration.get("package", name) if isinstance(declaration, dict) else name
            if actual in packages:
                errors.append(f"Paignia dependency patch overrides immutable source: {name}")

    application = tomllib.loads(
        (root / "crates/new-drug-reimbursement-game/Cargo.toml").read_text(encoding="utf-8")
    )
    lock = tomllib.loads((root / "Cargo.lock").read_text(encoding="utf-8"))
    expected_source = f"git+{provider['repository']}?rev={revision}#{revision}"
    for name in packages:
        dependency = application.get("dependencies", {}).get(name)
        if not isinstance(dependency, dict):
            errors.append(f"missing Paignia package dependency: {name}")
            continue
        if any(key in dependency for key in ("path", "branch", "tag")):
            errors.append(f"Paignia dependency must use immutable git+rev only: {name}")
        if dependency.get("git") != provider["repository"] or dependency.get("rev") != revision:
            errors.append(f"Paignia repository/revision mismatch: {name}")
        if dependency.get("version") != provider["version"]:
            errors.append(f"Paignia package version mismatch: {name}")
        entries = [item for item in lock["package"] if item["name"] == name]
        if len(entries) != 1 or entries[0].get("source") != expected_source:
            errors.append(f"Paignia lock source mismatch: {name}")
        elif entries[0]["version"] != provider["version"]:
            errors.append(f"Paignia lock version mismatch: {name}")
    return errors


def main() -> int:
    errors = validate_provider(Path.cwd())
    if errors:
        print("Paignia consumer boundary validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Paignia consumer boundary passed (2 immutable dependencies; no local core)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
