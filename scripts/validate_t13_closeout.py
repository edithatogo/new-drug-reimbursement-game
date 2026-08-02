#!/usr/bin/env python3
"""Validate T13 freeze, panel, and research-readiness hash bindings."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor/tracks/t13_empirical_calibration_20260802"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected object: {path}")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _check_references(items: list[Any], violations: list[str]) -> None:
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            violations.append("invalid hash reference")
            continue
        path = ROOT / item["path"]
        if not path.is_file():
            violations.append(f"missing referenced artifact: {item['path']}")
        elif _sha256(path) != item.get("sha256"):
            violations.append(f"stale referenced artifact: {item['path']}")


def closeout_violations() -> list[str]:
    violations: list[str] = []
    freeze_path = TRACK / "packet-freeze-2026-08-03.json"
    output_path = TRACK / "constrained-research-output-2026-08-03.json"
    target_path = TRACK / "panel-review-target-2026-08-03.json"
    consensus_path = TRACK / "panel-consensus-2026-08-03.json"
    readiness_path = TRACK / "research-readiness-receipt-2026-08-03.json"
    freeze = _load(freeze_path)
    output = _load(output_path)
    target = _load(target_path)
    consensus = _load(consensus_path)
    readiness = _load(readiness_path)

    _check_references(freeze.get("inputs", []), violations)
    _check_references(target.get("artifacts", []), violations)
    review_target = consensus.get("review_target", {})
    _check_references([review_target], violations)
    _check_references(consensus.get("receipts", []), violations)

    freeze_digest = _sha256(freeze_path)
    if output.get("packet_freeze_sha256") != freeze_digest:
        violations.append("constrained output does not bind the current packet freeze")
    if readiness.get("packet_freeze_sha256") != freeze_digest:
        violations.append("readiness receipt does not bind the current packet freeze")
    output_digest = _sha256(output_path)
    if readiness.get("constrained_output_sha256") != output_digest:
        violations.append("readiness receipt does not bind the current constrained output")
    panel = readiness.get("panel_consensus", {})
    if not isinstance(panel, dict):
        violations.append("readiness receipt lacks a hash-bound panel consensus")
    else:
        _check_references([panel], violations)

    if output.get("decision_use_permitted") is not False:
        violations.append("constrained output must prohibit decision use")
    if output.get("empirical_calibration_activated") is not False:
        violations.append("constrained output must keep empirical calibration disabled")
    if consensus.get("disposition") != "pass_synthetic_research_only_defer_empirical_promotion":
        violations.append("panel consensus does not retain the research-only disposition")
    if readiness.get("external_gates", {}).get("empirical_output") != "disabled":
        violations.append("readiness receipt must keep empirical output disabled")
    return violations


def main() -> int:
    violations = closeout_violations()
    if violations:
        print("T13 closeout validation failed:")
        for violation in violations:
            print(f"- {violation}")
        return 1
    print("T13 closeout validation passed (synthetic research only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
