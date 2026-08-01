"""Kairos scenario export without duplicating a scheduler."""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class KairosTraceReceipt:
    """Deterministic receipt for an event trace handed to Kairos."""

    digest: str
    event_count: int
    schema: str


class KairosScenarioExporter:
    """Emit a deterministic event contract for a future native Kairos adapter."""

    schema = "https://github.com/edithatogo/kairos/conformance/game-events/v0"

    def export_scenario(self, events: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
        normalized = []
        previous_time = 0.0
        for index, event in enumerate(events):
            time = float(event.get("time", index))
            if not math.isfinite(time) or time < 0:
                raise ValueError("Kairos event time must be finite and non-negative")
            if index and time < previous_time:
                raise ValueError("Kairos event times must be non-decreasing")
            kind = str(event.get("kind", "")).strip()
            if not kind:
                raise ValueError("Kairos event kind must be non-empty")
            payload = event.get("payload", {})
            if not isinstance(payload, Mapping):
                raise ValueError("Kairos event payload must be a mapping")
            normalized.append(
                {
                    "sequence": index,
                    "time": time,
                    "kind": kind,
                    "payload": dict(payload),
                }
            )
            previous_time = time
        return {
            "schema": self.schema,
            "target": "edithatogo/kairos",
            "events": normalized,
        }

    def trace_receipt(self, events: Sequence[Mapping[str, Any]]) -> KairosTraceReceipt:
        """Normalize events and return a content-addressed handoff receipt."""

        exported = self.export_scenario(events)
        digest = hashlib.sha256(
            json.dumps(exported, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return KairosTraceReceipt(
            digest=f"sha256:{digest}",
            event_count=len(exported["events"]),
            schema=str(exported["schema"]),
        )
