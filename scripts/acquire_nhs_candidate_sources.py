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
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


SOURCES = {
    "nice-ta1121-recommendations": "https://www.nice.org.uk/guidance/ta1121/chapter/1-Recommendations",
    "nice-ta1121-resource-impact": "https://www.nice.org.uk/guidance/ta1121/resources/resource-impact-summary-report-pdf-20159191246021",
    "nhs-payment-scheme-2026-27": "https://www.england.nhs.uk/publication/2026-27-nhs-payment-scheme/",
    "cheshire-merseyside-ta1121": "https://www.cheshireandmerseyside.nhs.uk/media/xaclztnz/nice_adherence_202504-202603.pdf",
    "kent-medway-ta1121": "https://www.kentandmedwayformulary.nhs.uk/therapeutic-sections/cardiovascular-system/heart-failure/",
    "northwest-tag-acoramidis": "https://nwknowledgenow.nhs.uk/wp-content/uploads/2026/03/TAG-Agreements-March-2026.pdf",
}


def fetch(source_id: str, url: str, timeout: float) -> dict[str, object]:
    retrieved = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    request = urllib.request.Request(url, headers={"User-Agent": "new-drug-reimbursement-game/nhs-candidate-fetch"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read()
            return {
                "source_id": source_id,
                "uri": url,
                "retrieved_at": retrieved,
                "status": "fetched",
                "http_status": response.status,
                "content_type": response.headers.get_content_type(),
                "byte_count": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
    except Exception as exc:  # noqa: BLE001 - receipt must retain negative results
        return {"source_id": source_id, "uri": url, "retrieved_at": retrieved, "status": "error", "error": str(exc)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=20.0)
    args = parser.parse_args()
    receipt = {
        "schema_version": 1,
        "kind": "nhs_candidate_source_acquisition",
        "approval_state": "candidate_only",
        "sources": [fetch(source_id, url, args.timeout) for source_id, url in SOURCES.items()],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "source_count": len(receipt["sources"])}, indent=2))
    return 0 if all(item["status"] == "fetched" for item in receipt["sources"]) else 1


if __name__ == "__main__":
    sys.exit(main())
