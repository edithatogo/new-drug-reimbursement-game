#!/usr/bin/env python3
"""Validate the bounded T13 maximal public-data acquisition bundles."""

from __future__ import annotations

import json
import re
import hashlib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor/tracks/t13_empirical_calibration_20260802"
EXPECTED = {
    1: "maximal-wp1-authority-committee-corpus-2026-08-04.json",
    2: "maximal-wp2-secondary-care-aggregates-2026-08-04.json",
    3: "maximal-wp3-organisation-stable-identifiers-2026-08-04.json",
    4: "maximal-wp4-regulatory-clinical-commercial-2026-08-04.json",
    5: "maximal-wp5-literature-methods-corpus-2026-08-04.json",
    6: "maximal-wp6-rights-approved-derived-projection-2026-08-04.json",
}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
RIGHTS = {"reuse_confirmed", "citation_only", "terms_ambiguous", "restricted", "prohibited"}
PACKET = "maximal-public-context-packet-v0.2.0.json"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def acquisition_violations(track: Path = TRACK) -> list[str]:
    violations: list[str] = []
    seen_ids: set[str] = set()
    for number, filename in EXPECTED.items():
        path = track / filename
        if not path.is_file():
            violations.append(f"WP{number}: missing bundle {filename}")
            continue
        try:
            bundle = _load(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            violations.append(f"WP{number}: unreadable bundle: {exc}")
            continue

        if bundle.get("schema_version") != "1.0":
            violations.append(f"WP{number}: unsupported schema version")
        if not str(bundle.get("work_package", "")).upper().startswith(f"WP{number}"):
            violations.append(f"WP{number}: work-package identifier mismatch")
        for key in ("generated_at", "scope", "coverage", "negative_or_deferred", "rights_boundary", "completion_status", "validation"):
            if key not in bundle:
                violations.append(f"WP{number}: missing {key}")

        sources = bundle.get("sources")
        if not isinstance(sources, list) or not sources:
            violations.append(f"WP{number}: sources must be a non-empty list")
            continue
        for index, source in enumerate(sources):
            prefix = f"WP{number} source {index + 1}"
            if not isinstance(source, dict):
                violations.append(f"{prefix}: not an object")
                continue
            source_id = source.get("source_id")
            if not isinstance(source_id, str) or not source_id:
                violations.append(f"{prefix}: missing source_id")
            elif source_id in seen_ids:
                violations.append(f"{prefix}: duplicate source_id {source_id}")
            else:
                seen_ids.add(source_id)
            for key in ("publisher", "title", "requested_url", "final_url", "retrieval", "terms", "supported_fields", "unsupported_fields", "refresh_rule"):
                if key not in source:
                    violations.append(f"{prefix}: missing {key}")
            retrieval = source.get("retrieval", {})
            if not isinstance(retrieval, dict):
                violations.append(f"{prefix}: retrieval must be an object")
                continue
            digest = source.get("sha256") or retrieval.get("sha256")
            multi_digests = retrieval.get("sha256_by_service")
            has_multi = isinstance(multi_digests, dict) and multi_digests and all(
                isinstance(value, str) and SHA256.fullmatch(value) for value in multi_digests.values()
            )
            if digest is not None and (not isinstance(digest, str) or not SHA256.fullmatch(digest)):
                violations.append(f"{prefix}: invalid SHA-256")
            if digest is None and not has_multi and not source.get("no_hash_reason"):
                violations.append(f"{prefix}: missing hash and no-hash reason")
            terms = source.get("terms", {})
            classification = terms.get("classification") if isinstance(terms, dict) else None
            if classification not in RIGHTS:
                violations.append(f"{prefix}: invalid or missing rights classification")
            for boundary in ("displaced programme", "confidential price"):
                supported = json.dumps(source.get("supported_fields", "")).lower()
                if boundary in supported:
                    violations.append(f"{prefix}: prohibited inferred field promoted: {boundary}")

        deferred = bundle.get("negative_or_deferred")
        if not isinstance(deferred, list):
            violations.append(f"WP{number}: negative_or_deferred must be a list")

    packet_path = track / PACKET
    if packet_path.is_file():
        try:
            packet = _load(packet_path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            violations.append(f"WP7: unreadable packet: {exc}")
            return violations
        references = packet.get("source_bundles")
        if not isinstance(references, list) or len(references) != len(EXPECTED):
            violations.append("WP7: packet must reference every WP1-WP6 bundle")
        else:
            for reference in references:
                if not isinstance(reference, dict) or not isinstance(reference.get("path"), str):
                    violations.append("WP7: invalid bundle reference")
                    continue
                referenced = ROOT / reference["path"]
                if not referenced.is_file():
                    violations.append(f"WP7: missing referenced bundle {reference['path']}")
                elif hashlib.sha256(referenced.read_bytes()).hexdigest() != reference.get("sha256"):
                    violations.append(f"WP7: stale referenced bundle {reference['path']}")
        if packet.get("parameter_roles") != {}:
            violations.append("WP7: public-context packet must not contain calibration parameter roles")
        promotion = packet.get("promotion", {})
        if not isinstance(promotion, dict) or promotion.get("empirical_calibration") != "disabled" or promotion.get("decision_use") != "prohibited":
            violations.append("WP7: empirical or decision-use boundary is not fail-closed")
        if packet.get("authority") != "repository-derived; not an Atlas-approved calibration packet":
            violations.append("WP7: packet authority is overstated")
    return violations


def main() -> int:
    violations = acquisition_violations()
    if violations:
        print("Maximal public-data validation failed:")
        for violation in violations:
            print(f"- {violation}")
        return 1
    print("Maximal public-data validation passed (WP1-WP6; context-only, no raw payloads)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
