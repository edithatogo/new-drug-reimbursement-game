"""Synthetic disclosure-control primitives for public demonstrations.

These controls are a fail-closed research baseline. They do not authorize or
implement processing of actual restricted or confidential data.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from typing import Any


def synthetic_aggregate(values: Sequence[float], *, minimum_group_size: int = 5,
                        rounding_base: int = 5, maximum_dominance: float = 0.8) -> float:
    """Return a rounded synthetic aggregate or reject a disclosure-risky cell."""

    if minimum_group_size < 5 or len(values) < minimum_group_size:
        raise ValueError("group is below the synthetic disclosure-control minimum")
    if rounding_base <= 0:
        raise ValueError("rounding_base must be positive")
    checked = tuple(float(value) for value in values)
    total = sum(checked)
    magnitude = sum(abs(value) for value in checked)
    if magnitude and max(abs(value) for value in checked) / magnitude >= maximum_dominance:
        raise ValueError("group fails the synthetic dominance review")
    return float(round(total / rounding_base) * rounding_base)


def serialize_public_synthetic(payload: dict[str, Any], *, audience: str,
                               disclosure_status: str, synthetic_only: bool) -> str:
    """Serialize only explicitly approved synthetic public output."""

    if audience != "public" or disclosure_status != "approved" or not synthetic_only:
        raise ValueError("public export requires approved synthetic-only disclosure metadata")
    forbidden = {"confidential_rebate", "net_price", "contract_identifier", "patient_id"}
    if forbidden.intersection(payload):
        raise ValueError("public payload contains a prohibited field")
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))
