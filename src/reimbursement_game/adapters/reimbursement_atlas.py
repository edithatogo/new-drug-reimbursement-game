"""Read reviewed, derived Reimbursement Atlas exports.

The adapter never downloads raw schedule data and never bypasses Atlas licence
or human-review gates.
"""

from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..evidence import EvidencePacket, evidence_packet_from_mapping

_MAX_PARAMETER_EXPORT_BYTES = 10 * 1024 * 1024


@dataclass(frozen=True, slots=True)
class AtlasPacketReceipt:
    digest: str
    packet_id: str
    packet_revision: str
    record_count: int
    licences: tuple[str, ...]


class ReimbursementAtlasParameterExport:
    """Read one strict approved-derived parameter evidence packet."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def packet(self) -> EvidencePacket:
        if self.path.is_symlink() or not self.path.is_file():
            raise ValueError("Atlas parameter export must be a regular non-symlink file")
        if self.path.suffix.lower() != ".json":
            raise ValueError("Atlas parameter export must use the versioned JSON packet format")
        if self.path.stat().st_size > _MAX_PARAMETER_EXPORT_BYTES:
            raise ValueError("Atlas parameter export exceeds the 10 MiB safety limit")
        value = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError("Atlas parameter export must contain a JSON object")
        return evidence_packet_from_mapping(value)

    def receipt(self) -> AtlasPacketReceipt:
        """Return a content-addressed receipt for an approved-derived packet."""

        packet = self.packet()
        if any(record.approval_state != "approved" or not record.derived_only for record in packet.records):
            raise ValueError("Atlas packet receipt requires approved-derived records")
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        digest = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        licences = tuple(sorted({record.source_licence for record in packet.records}))
        return AtlasPacketReceipt(f"sha256:{digest}", packet.packet_id, packet.packet_revision, len(packet.records), licences)


class ReimbursementAtlasExport:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def records(self) -> list[dict[str, Any]]:
        suffix = self.path.suffix.lower()
        if suffix in {".jsonl", ".ndjson"}:
            values = [
                json.loads(line)
                for line in self.path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
        elif suffix == ".json":
            value = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(value, list):
                raise ValueError("Atlas JSON export must contain a list of records")
            values = value
        elif suffix == ".csv":
            with self.path.open(newline="", encoding="utf-8") as handle:
                values = list(csv.DictReader(handle))
        else:
            raise ValueError("supported Atlas export formats are JSON, JSONL, and CSV")

        records = []
        for value in values:
            if not isinstance(value, dict):
                raise ValueError("Atlas export records must be JSON objects")
            record = dict(value)
            if str(record.get("approval_state", "")).lower() != "approved":
                raise ValueError("Atlas export records must be explicitly approved")
            if not str(record.get("provenance", "")).strip():
                raise ValueError("Atlas export records must include provenance")
            records.append(record)
        return records
