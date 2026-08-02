#!/usr/bin/env python3
"""Fail closed when tracked paths cross raw or confidential data boundaries."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROHIBITED_SEGMENTS = {"raw", "confidential", "private", "restricted", "secret", "secrets"}
PROHIBITED_SUFFIXES = {
    ".7z",
    ".avro",
    ".db",
    ".dta",
    ".feather",
    ".gz",
    ".parquet",
    ".pkl",
    ".sas7bdat",
    ".sav",
    ".sqlite",
    ".tar",
    ".xls",
    ".xlsx",
    ".zip",
}
DOCUMENTATION_ROOTS = {"conductor", "docs", "tests"}


def tracked_paths() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return [Path(value) for value in result.stdout.split("\0") if value]


def boundary_violations(paths: list[Path]) -> list[str]:
    violations: list[str] = []
    for path in paths:
        parts = {part.lower() for part in path.parts}
        if path.suffix.lower() in PROHIBITED_SUFFIXES:
            violations.append(f"prohibited tracked data/archive type: {path}")
        if parts & PROHIBITED_SEGMENTS and path.parts[0].lower() not in DOCUMENTATION_ROOTS:
            violations.append(f"prohibited tracked restricted-data path: {path}")
    return violations


def release_boundary_violations() -> list[str]:
    path = ROOT / "docs/governance/release-packet/research-only-release-authorization-2026-08-02.json"
    receipt = json.loads(path.read_text(encoding="utf-8"))
    prohibited = " ".join(receipt.get("prohibited", [])).lower()
    required = ("raw", "confidential", "calibrated", "regulatory")
    return [f"release authorization does not prohibit {term}" for term in required if term not in prohibited]


def main() -> int:
    violations = boundary_violations(tracked_paths()) + release_boundary_violations()
    if violations:
        print("data-boundary validation failed:")
        for violation in violations:
            print(f"- {violation}")
        return 1
    print("data-boundary validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
