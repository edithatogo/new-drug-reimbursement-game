#!/usr/bin/env python3
"""Validate that public evidence coverage cannot silently become calibration."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor/tracks/t13_empirical_calibration_20260802"
RUN = TRACK / "acquisition-run-2026-08-02.json"
COVERAGE = TRACK / "field-coverage-2026-08-02.json"
RELEASE = ROOT / "docs/governance/release-packet/research-only-release-authorization-2026-08-02.json"

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_REQUIRED_FIELDS = {
    "payer_or_commissioner",
    "budget_boundary",
    "service_line",
    "provider",
    "decision_date",
    "price_year",
    "intervention",
    "comparator",
    "displaced_programme",
    "stable_programme_id",
    "baseline_cost_and_unit",
    "horizon",
    "accountable_owner_confirmation",
    "atlas_approved_n_m_d_packet",
}
_PROMOTABLE = {"approved", "supported"}


def readiness_violations(run: dict[str, Any], coverage: dict[str, Any], release: dict[str, Any]) -> list[str]:
    violations: list[str] = []
    sources = {item.get("source_id"): item for item in run.get("sources", [])}
    for source_id, item in sources.items():
        status = item.get("status")
        digest = item.get("sha256")
        if status == "fetched" and not isinstance(digest, str):
            violations.append(f"fetched source lacks sha256: {source_id}")
        elif status == "fetched" and not _SHA256.fullmatch(digest):
            violations.append(f"fetched source has invalid sha256: {source_id}")
        if item.get("payload_retained") is not False:
            violations.append(f"source receipt must not retain payload: {source_id}")

    fields = coverage.get("fields", [])
    by_name = {item.get("field"): item for item in fields if isinstance(item, dict)}
    missing_names = sorted(_REQUIRED_FIELDS - set(by_name))
    if missing_names:
        violations.append(f"coverage omits required fields: {missing_names}")
    for name, item in by_name.items():
        for source_id in item.get("sources", []):
            if source_id not in sources:
                violations.append(f"coverage field {name} references unknown source: {source_id}")

    incomplete = sorted(name for name in _REQUIRED_FIELDS if by_name.get(name, {}).get("status") not in _PROMOTABLE)
    decision = coverage.get("decision")
    if incomplete and decision != "defer_empirical_promotion":
        violations.append("incomplete evidence must defer empirical promotion")
    if not incomplete and decision == "defer_empirical_promotion":
        violations.append("complete evidence requires a new packet-bound disposition")

    prohibited = " ".join(release.get("prohibited", [])).lower()
    if "calibrated" not in prohibited or "regulatory" not in prohibited:
        violations.append("research-only authorization must prohibit calibrated and regulatory claims")
    return violations


def run_digest_violation(run_bytes: bytes, coverage: dict[str, Any]) -> list[str]:
    expected = coverage.get("acquisition_run_sha256")
    actual = hashlib.sha256(run_bytes).hexdigest()
    return [] if expected == actual else ["field coverage is not bound to the current acquisition run"]


def main() -> int:
    run_bytes = RUN.read_bytes()
    run = json.loads(run_bytes)
    coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    violations = readiness_violations(run, coverage, release) + run_digest_violation(run_bytes, coverage)
    if violations:
        print("empirical-readiness validation failed:")
        for violation in violations:
            print(f"- {violation}")
        return 1
    print("empirical-readiness validation passed (promotion remains deferred)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
