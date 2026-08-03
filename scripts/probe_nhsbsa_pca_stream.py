#!/usr/bin/env python3
"""Stream an NHSBSA PCA CSV and retain only identifier match counts and hashes."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import urllib.request
from datetime import UTC, datetime
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--terms", nargs="+", default=["acoramidis", "tafamidis", "vutrisiran"])
    parser.add_argument("--max-bytes", type=int, default=500_000_000)
    args = parser.parse_args()

    terms = [term.lower() for term in args.terms]
    counts = dict.fromkeys(terms, 0)
    total_rows = 0
    total_bytes = 0
    digest = hashlib.sha256()
    status: dict[str, object] = {
        "schema_version": "1.0",
        "retrieved_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "requested_uri": args.url,
        "payload_retained": False,
        "terms": terms,
    }
    try:
        request = urllib.request.Request(args.url, headers={"User-Agent": "new-drug-reimbursement-game/pca-stream-probe"})
        with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310
            status.update({"http_status": response.status, "content_type": response.headers.get_content_type(), "etag": response.headers.get("ETag")})
            reader = csv.DictReader(line.decode("utf-8", "replace") for line in _hashed_lines(response, digest, args.max_bytes, lambda n: _set_bytes(status, n)))
            if not reader.fieldnames or "BNF_PRESENTATION_NAME" not in reader.fieldnames:
                raise ValueError("CSV lacks BNF_PRESENTATION_NAME; schema review required")
            for row in reader:
                total_rows += 1
                name = (row.get("BNF_PRESENTATION_NAME") or "").lower()
                for term in terms:
                    if term in name:
                        counts[term] += 1
    except Exception as exc:
        status.update({"status": "error", "error_type": type(exc).__name__, "error": str(exc)})
    else:
        status.update({"status": "scanned", "row_count": total_rows, "match_counts": counts, "sha256": digest.hexdigest()})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0 if status.get("status") == "scanned" else 1


def _set_bytes(status: dict[str, object], value: int) -> None:
    status["byte_count"] = value


def _hashed_lines(response: object, digest: object, max_bytes: int, update: object):
    total = 0
    while True:
        line = response.readline()  # type: ignore[attr-defined]
        if not line:
            return
        total += len(line)
        if total > max_bytes:
            raise ValueError(f"stream exceeds max bytes {max_bytes}")
        digest.update(line)  # type: ignore[attr-defined]
        update(total)  # type: ignore[operator]
        yield line


if __name__ == "__main__":
    raise SystemExit(main())
