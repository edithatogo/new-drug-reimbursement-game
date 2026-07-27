"""Kairos scenario export without duplicating a scheduler."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any


class KairosScenarioExporter:
    """Emit a deterministic event contract for a future native Kairos adapter."""

    schema = "https://github.com/edithatogo/kairos/conformance/game-events/v0"

    def export_scenario(self, events: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
        normalized = []
        for index, event in enumerate(events):
            time = float(event.get("time", index))
            if not math.isfinite(time):
                raise ValueError("Kairos event time must be finite")
            normalized.append(
                {
                    "sequence": index,
                    "time": time,
                    "kind": str(event["kind"]),
                    "payload": dict(event.get("payload", {})),
                }
            )
        return {
            "schema": self.schema,
            "target": "edithatogo/kairos",
            "events": normalized,
        }
