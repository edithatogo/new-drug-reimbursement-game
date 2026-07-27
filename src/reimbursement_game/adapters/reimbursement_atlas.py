"""Read reviewed, derived Reimbursement Atlas exports.

The adapter never downloads raw schedule data and never bypasses Atlas licence
or human-review gates.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


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
