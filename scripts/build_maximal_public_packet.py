#!/usr/bin/env python3
"""Build the deterministic T13 maximal public-context packet."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor/tracks/t13_empirical_calibration_20260802"
OUTPUT = TRACK / "maximal-public-context-packet-v0.2.0.json"
ACQUISITION_TARGET_COMMIT = "ae690c19b83147cbaa6dd2b00b177e3fd25910da"
INPUTS = [
    f"maximal-wp{number}-{suffix}-2026-08-04.json"
    for number, suffix in [
        (1, "authority-committee-corpus"),
        (2, "secondary-care-aggregates"),
        (3, "organisation-stable-identifiers"),
        (4, "regulatory-clinical-commercial"),
        (5, "literature-methods-corpus"),
        (6, "rights-approved-derived-projection"),
    ]
]


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected object: {path}")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(target_commit: str | None = None) -> dict[str, Any]:
    bundles = [(TRACK / filename, _load(TRACK / filename)) for filename in INPUTS]
    rights = bundles[-1][1]
    rights_matrix = [
        {
            "source_id": source["source_id"],
            "work_package": bundle["work_package"],
            "authority_rank": source["authority_rank"],
            "classification": source["terms"]["classification"],
            "permitted_use": "approved-derived projection only"
            if source["source_id"] in {
                "wp6-crossref-metadata-terms",
                "wp6-clinicaltrials-api-terms",
                "wp6-pmc12304488-article-licence",
                "wp6-nice-content-reuse",
            }
            else "inventory or source-receipt context only",
        }
        for _, bundle in bundles
        for source in bundle["sources"]
    ]
    return {
        "schema_version": "1.0",
        "packet_id": "atlas-ta1121-acoramidis-public-context-derived-v0.2.0",
        "packet_status": "candidate_public_context_complete_empirical_fields_deferred",
        "authority": "repository-derived; not an Atlas-approved calibration packet",
        "programme": "NICE TA1121 acoramidis versus tafamidis, England",
        "assembled_at": "2026-08-04T14:30:00Z",
        "acquisition_target_commit": target_commit or ACQUISITION_TARGET_COMMIT,
        "source_bundles": [
            {
                "path": str(path.relative_to(ROOT)),
                "sha256": _sha256(path),
                "work_package": bundle["work_package"],
                "completion_status": bundle["completion_status"],
            }
            for path, bundle in bundles
        ],
        "approved_derived_projection": rights["approved_derived_projection"],
        "transformations": [
            "stream source bytes only long enough to hash or aggregate permitted fields",
            "retain source receipts and approved-derived fields; retain no raw payloads",
            "preserve publisher values and identifiers without imputing missing fields",
            "classify supported, unsupported, conflicting, and deferred fields separately",
            "do not convert organisation, service, budget, or guidance identifiers into a displaced-programme identifier",
        ],
        "uncertainty": {
            "administrative_aggregates": "provisional observations are labelled provisional and are not causal or indication-specific",
            "literature": "structural and source-selection uncertainty retained as methods context only",
            "missingness": "no imputation for displacement, baseline unit, confidential price, or calibration parameters",
            "joint_parameter_distribution": "not available",
        },
        "source_terms": {
            "classification_authority": "WP6 field-level adjudication",
            "reuse_confirmed": rights["coverage"]["reuse_confirmed"],
            "inventory_only": rights["coverage"]["citation_only"] + rights["coverage"]["terms_ambiguous"],
            "raw_payload_redistribution": "prohibited",
            "all_source_rights_matrix": rights_matrix,
        },
        "parameter_roles": {},
        "supported_context": [
            "national guidance and implementation chronology",
            "official organisation, provider, service, and medicine identifiers",
            "final and provisional secondary-care aggregate observations with dataset-scope limitations",
            "regulatory, trial-registry, public commercial, bibliographic, and economic-method context",
        ],
        "negative_scope": [
            "no attributable displaced programme or stable displaced-programme identifier",
            "no programme baseline cost or unit",
            "no confidential or net NHS price",
            "no empirical Chapter 7 parameter roles or joint uncertainty distribution",
            "no payer, HTA, policy, regulatory, calibrated, raw-data, or confidential-data claims",
        ],
        "promotion": {
            "public_context_research_only": "eligible after exact-target validation",
            "empirical_calibration": "disabled",
            "decision_use": "prohibited",
            "atlas_owner_approval": "required for any future calibration packet",
        },
        "refresh_and_invalidation": "Any source URL, revision, ETag, byte hash, terms, transformation, destination, packet, or target-commit change invalidates dependent review and requires rebuilding this packet.",
    }


def main() -> int:
    OUTPUT.write_text(json.dumps(build(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
