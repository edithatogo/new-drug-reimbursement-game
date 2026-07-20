#!/usr/bin/env python3
"""Validate ecosystem, dependency, Hugging Face, and copyright boundaries."""

from __future__ import annotations

from pathlib import Path
import sys
import tomllib


def main() -> int:
    errors: list[str] = []
    project = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    dependencies = " ".join(project["project"].get("dependencies", [])).lower()
    prohibited = ("nashpy", "pygambit", "open_spiel", "openspiel", "bcea", "heemod", "dampack")
    for package in prohibited:
        if package in dependencies:
            errors.append(f"prohibited runtime dependency: {package}")

    for line in Path("hf/manifest.yaml").read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("- id:"):
            repo_id = line.split(":", 1)[1].strip()
            if not repo_id.startswith("edithatogo/"):
                errors.append(f"out-of-scope Hugging Face repository: {repo_id}")

    for path in Path(".").rglob("*"):
        if path.is_file() and path.suffix.lower() in {".pdf", ".epub", ".mobi"}:
            errors.append(f"book-like binary must not be committed: {path}")

    lock = tomllib.loads(Path("ecosystem.lock.toml").read_text(encoding="utf-8"))
    for component in lock.get("component", []):
        repository = component["repository"]
        if "github.com/edithatogo/" not in repository:
            errors.append(f"non-owner ecosystem component: {repository}")
        revision = component["revision"]
        if len(revision) != 40 or any(character not in "0123456789abcdef" for character in revision):
            errors.append(f"component revision is not a full commit SHA: {component['name']}")

    if errors:
        print("scope validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("scope validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
