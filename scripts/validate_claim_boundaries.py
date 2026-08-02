#!/usr/bin/env python3
"""Validate that research-only artifacts cannot imply regulatory readiness."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "conductor/tracks/t14_regulatory_validation_20260802/claims-matrix.json"
READINESS = ROOT / "docs/generated/nhs-england-pilot-readiness.json"
RELEASE = ROOT / "docs/governance/release-packet/research-only-release-authorization-2026-08-02.json"

REQUIRED_PROHIBITED_CLAIMS = {
    "empirically calibrated reimbursement result",
    "NICE HTA submission or recommendation",
    "MHRA compliant or medical-device approved",
    "payer, policy, or regulatory recommendation",
}


def validate_claims(matrix: dict[str, object]) -> list[str]:
    errors: list[str] = []
    claims = {str(item["claim"]): str(item["status"]) for item in matrix.get("claims", [])}
    for claim in REQUIRED_PROHIBITED_CLAIMS:
        status = claims.get(claim)
        if status is None or not status.startswith("prohibited"):
            errors.append(f"claim is not fail-closed: {claim}")
    return errors


def validate_repository_boundaries() -> list[str]:
    errors = validate_claims(json.loads(MATRIX.read_text(encoding="utf-8")))
    readiness = json.loads(READINESS.read_text(encoding="utf-8"))
    if readiness.get("approved_calibration_permitted") is not False:
        errors.append("NHS readiness must keep approved_calibration_permitted false")
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    if release.get("scope") != "research software and methodology only":
        errors.append("release authorization is not research-only")
    return errors


def main() -> int:
    errors = validate_repository_boundaries()
    if errors:
        print("claim-boundary validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("claim-boundary validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
