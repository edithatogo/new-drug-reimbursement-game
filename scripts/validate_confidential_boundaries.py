#!/usr/bin/env python3
"""Validate T16 audience, reconstruction, and confidential export boundaries."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "conductor/tracks/t16_confidential_data_controls_20260802/disclosure-matrix.json"
if not MATRIX.is_file():
    MATRIX = ROOT / "conductor/archive/t16_confidential_data_controls_20260802/disclosure-matrix.json"
RELEASE = ROOT / "docs/governance/release-packet/research-only-release-authorization-2026-08-02.json"


def matrix_violations(matrix: dict) -> list[str]:
    violations: list[str] = []
    default = matrix.get("default", {})
    if default.get("export_permitted") is not False or default.get("disclosure_status") != "prohibited":
        violations.append("disclosure default must prohibit export")
    for output in matrix.get("outputs", []):
        name = output.get("id", "unnamed")
        public = output.get("audience") == "public"
        export = output.get("export_permitted") is True
        if public and (output.get("disclosure_status") != "approved" or not output.get("synthetic_only")):
            violations.append(f"public output must be approved and synthetic-only: {name}")
        if export and (not output.get("authorizer") or not output.get("destination")):
            violations.append(f"export lacks authorizer or destination: {name}")
        if not output.get("synthetic_only") and public:
            violations.append(f"non-synthetic output cannot be public: {name}")
        if output.get("disclosure_status") in {"deferred", "prohibited"} and export:
            violations.append(f"deferred or prohibited output cannot be exported: {name}")
    return violations


def main() -> int:
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    violations = matrix_violations(matrix)
    scope = " ".join(release.get("permitted", [])).lower()
    if "synthetic" not in scope:
        violations.append("research-only release does not explicitly authorize synthetic scope")
    if violations:
        print("confidential-boundary validation failed:")
        for violation in violations:
            print(f"- {violation}")
        return 1
    print("confidential-boundary validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
