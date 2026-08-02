#!/usr/bin/env python3
"""Fetch allow-listed official NHS/NICE candidate sources with provenance.

This utility deliberately produces candidate evidence only. It never writes an
approved parameter packet and never infers displacement or net prices.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

SOURCES = {
    "nice-ta1121-recommendations": "https://www.nice.org.uk/guidance/ta1121/chapter/1-Recommendations",
    "nice-ta1121-resource-impact": "https://www.nice.org.uk/guidance/ta1121/resources/resource-impact-summary-report-pdf-20159191246021",
    "nhs-payment-scheme-2026-27": "https://www.england.nhs.uk/publication/2026-27-nhs-payment-scheme/",
    "cheshire-merseyside-ta1121": "https://www.cheshireandmerseyside.nhs.uk/media/xaclztnz/nice_adherence_202504-202603.pdf",
    "kent-medway-ta1121": "https://www.kentandmedwayformulary.nhs.uk/therapeutic-sections/cardiovascular-system/heart-failure/",
    "northwest-tag-acoramidis": "https://nwknowledgenow.nhs.uk/wp-content/uploads/2026/03/TAG-Agreements-March-2026.pdf",
    "south-yorkshire-imoc-february-2026": "https://mot.southyorkshire.icb.nhs.uk/south-yorkshire/files/South%20Yorkshire%20Minutes%20IMOC%20February%202026.pdf?_rsc=1suc1",
    "mft-nice-adherence-march-2026": "https://mft.nhs.uk/app/uploads/sites/7/2026/03/NICE-TA-Adherence-Checklist-Mar-26.pdf",
    "somerset-medicines-board-january-2026": "https://nhssomerset.nhs.uk/wp-content/uploads/sites/2/MPB-Minutes-Jan-2026.pdf",
    "southwest-london-jfc-january-2026": "https://www.swljointmedicinesformulary.nhs.uk/docs/files/SWL%20JFC%20Bulletin%20January%202026.pdf",
    "north-east-london-formulary": "https://nel-jointformulary.nhs.uk/chaptersSubDetails.asp?FormularySectionID=9&SubSectionID=A100&SubSectionRef=09",
    "buckinghamshire-formulary": "https://bucksformulary.nhs.uk/reports/Archive/A0003.asp",
    "atlas-v0.1.1-release": "https://api.github.com/repos/edithatogo/reimbursement-atlas/releases/tags/v0.1.1",
}

ALLOWED_HOST_SUFFIXES = (
    ".england.nhs.uk",
    ".icb.nhs.uk",
    ".nhs.uk",
    ".nice.org.uk",
    "api.github.com",
)
MAX_BYTES = 25 * 1024 * 1024

# This is intentionally a bounded search plan rather than an open-ended web
# crawler.  Search results are leads only; a local displacement receipt still
# requires an authoritative document naming the payer, programme and baseline.
SEARCH_PLAN = [
    {
        "family": "local_decision",
        "terms": ["acoramidis", "tafamidis", "TA1121", "ATTR-CM", "commissioning"],
        "required_evidence": ["accountable payer", "decision date", "displaced programme", "baseline unit"],
    },
    {
        "family": "formulary_switch",
        "terms": ["acoramidis", "tafamidis", "TA1121", "formulary", "replaced OR displaced OR switch"],
        "required_evidence": ["local formulary owner", "intervention", "comparator", "replacement decision"],
    },
    {
        "family": "budget_impact",
        "terms": ["acoramidis", "tafamidis", "budget impact OR financial impact", "ICB OR trust"],
        "required_evidence": ["payer budget boundary", "price basis", "affected programme"],
    },
]


def validate_source_url(url: str) -> None:
    parsed = urllib.parse.urlparse(url)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or not any(host == suffix.lstrip(".") or host.endswith(suffix) for suffix in ALLOWED_HOST_SUFFIXES):
        raise ValueError(f"source URL is not an allow-listed official HTTPS host: {url}")


def _read_bounded(response: object, max_bytes: int) -> bytes:
    payload = response.read(max_bytes + 1)  # type: ignore[attr-defined]
    if len(payload) > max_bytes:
        raise ValueError(f"source exceeds maximum receipt size of {max_bytes} bytes")
    return payload


def fetch(source_id: str, url: str, timeout: float, *, max_bytes: int = MAX_BYTES) -> dict[str, object]:
    retrieved = datetime.now(UTC).replace(microsecond=0).isoformat()
    validate_source_url(url)
    request = urllib.request.Request(url, headers={"User-Agent": "new-drug-reimbursement-game/nhs-candidate-fetch"})  # noqa: S310
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
            payload = _read_bounded(response, max_bytes)
            return {
                "source_id": source_id,
                "requested_uri": url,
                "final_uri": response.geturl(),
                "retrieved_at": retrieved,
                "status": "fetched",
                "http_status": response.status,
                "content_type": response.headers.get_content_type(),
                "byte_count": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "etag": response.headers.get("ETag"),
                "last_modified": response.headers.get("Last-Modified"),
                "payload_retained": False,
            }
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError) as exc:
        return {
            "source_id": source_id,
            "requested_uri": url,
            "retrieved_at": retrieved,
            "status": "error",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "payload_retained": False,
        }


def field_coverage() -> dict[str, str]:
    return {
        "payer_or_commissioner": "candidate_south_yorkshire_icb",
        "budget_boundary": "missing",
        "service_line": "candidate_specialist_attr_cm",
        "provider": "candidate_nac_or_midlands_service_routing_not_owner",
        "decision_date": "candidate_february_2026",
        "price_year": "missing_programme_specific",
        "intervention": "supported_acoramidis",
        "comparator": "supported_national_tafamidis_not_local_displacement",
        "displaced_programme": "missing",
        "stable_programme_id": "missing",
        "baseline_cost_and_unit": "missing",
        "horizon": "missing_programme_specific",
        "accountable_owner_confirmation": "missing",
        "atlas_approved_n_m_d_packet": "not_found_v0.1.1",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--max-bytes", type=int, default=MAX_BYTES)
    parser.add_argument("--require-all", action="store_true")
    args = parser.parse_args()
    receipt = {
        "schema_version": 1,
        "kind": "nhs_candidate_source_acquisition",
        "approval_state": "candidate_only",
        "search_plan": SEARCH_PLAN,
        "search_result_policy": "Search results are leads; only an authoritative local record satisfying required_evidence can close displacement.",
        "source_policy": "Official allow-listed HTTPS sources only; hash receipts are retained but payload bytes are not.",
        "field_coverage": field_coverage(),
        "sources": [fetch(source_id, url, args.timeout, max_bytes=args.max_bytes) for source_id, url in SOURCES.items()],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "source_count": len(receipt["sources"])}, indent=2))
    complete = all(item["status"] == "fetched" for item in receipt["sources"])
    return 0 if complete or not args.require_all else 1


if __name__ == "__main__":
    sys.exit(main())
