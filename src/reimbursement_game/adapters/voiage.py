"""Voiage adapter.

VOI algorithms are intentionally not reimplemented in this repository.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from ..calibration import VoiageSampleBundle


@dataclass(frozen=True, slots=True)
class VoiageHandoffReceipt:
    """Deterministic, non-authorizing receipt for a Voiage input handoff."""

    digest: str
    sample_count: int
    strategy_names: tuple[str, str]
    parameter_roles: tuple[str, ...]
    perspective: str
    health_unit: str
    evidence_revision: str


class VoiageAdapter:
    """Convert application net-benefit samples to Voiage's DecisionAnalysis."""

    def evpi(self, net_benefit_samples: Sequence[Sequence[float]]) -> float:
        # Validate the boundary before importing the optional ecosystem.  This
        # keeps malformed application data distinguishable from an unavailable
        # Voiage installation and prevents ragged arrays being silently
        # coerced into object arrays.
        rows = _validated_rows(net_benefit_samples)
        try:
            import numpy as np
            from voiage.analysis import DecisionAnalysis
            from voiage.schema import ValueArray
        except ImportError as exc:  # pragma: no cover - optional ecosystem checkout
            raise RuntimeError(
                "Install or check out edithatogo/voiage to use VOI analysis"
            ) from exc
        array = np.asarray(rows, dtype=float)
        value_array = ValueArray.from_numpy(array)
        return float(DecisionAnalysis(value_array).evpi())

    def prepare_inputs(self, bundle: VoiageSampleBundle) -> tuple[Any, Any]:
        """Construct the pinned Voiage ValueArray and ParameterSet schemas.

        This method performs no VOI calculation and does not generate samples.
        """

        rows = _validated_rows(bundle.net_benefit_samples)
        if bundle.perspective != "health" or not bundle.health_unit.strip():
            raise ValueError("Voiage calibration bundle requires an explicit health perspective")
        if not bundle.evidence_revision.startswith("sha256:"):
            raise ValueError("Voiage calibration bundle requires a sha256 evidence revision")
        if len(bundle.strategy_names) != len(rows[0]):
            raise ValueError("Voiage strategy names must align with sample columns")
        parameter_values = {item.role.value: item.values for item in bundle.parameter_samples}
        if not parameter_values:
            raise ValueError("Voiage calibration bundle requires parameter samples")
        if any(len(values) != len(rows) for values in parameter_values.values()):
            raise ValueError("Voiage parameter samples must align with strategy samples")
        try:
            import numpy as np
            from voiage.schema import ParameterSet, ValueArray
        except ImportError as exc:  # pragma: no cover - optional ecosystem checkout
            raise RuntimeError(
                "Install or check out pinned edithatogo/voiage to prepare VOI inputs"
            ) from exc
        values = ValueArray.from_numpy(np.asarray(rows, dtype=float), list(bundle.strategy_names))
        parameters = ParameterSet.from_numpy_or_dict(
            {name: np.asarray(samples, dtype=float) for name, samples in parameter_values.items()}
        )
        return values, parameters

    def handoff_receipt(self, bundle: VoiageSampleBundle) -> VoiageHandoffReceipt:
        """Return a hash-bound receipt without importing or running Voiage."""

        rows = _validated_rows(bundle.net_benefit_samples)
        if bundle.perspective != "health" or not bundle.health_unit.strip():
            raise ValueError("Voiage calibration bundle requires an explicit health perspective")
        if not bundle.evidence_revision.startswith("sha256:"):
            raise ValueError("Voiage calibration bundle requires a sha256 evidence revision")
        if len(bundle.strategy_names) != len(rows[0]):
            raise ValueError("Voiage strategy names must align with sample columns")
        parameter_roles = tuple(item.role.value for item in bundle.parameter_samples)
        if not parameter_roles:
            raise ValueError("Voiage calibration bundle requires parameter samples")
        if any(len(item.values) != len(rows) for item in bundle.parameter_samples):
            raise ValueError("Voiage parameter samples must align with strategy samples")
        payload = {
            "evidence_revision": bundle.evidence_revision,
            "health_unit": bundle.health_unit,
            "net_benefit_samples": rows,
            "parameter_roles": parameter_roles,
            "parameter_samples": [list(item.values) for item in bundle.parameter_samples],
            "perspective": bundle.perspective,
            "strategy_names": list(bundle.strategy_names),
        }
        digest = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return VoiageHandoffReceipt(
            digest=f"sha256:{digest}",
            sample_count=len(rows),
            strategy_names=bundle.strategy_names,
            parameter_roles=parameter_roles,
            perspective=bundle.perspective,
            health_unit=bundle.health_unit,
            evidence_revision=bundle.evidence_revision,
        )


def _validated_rows(samples: Sequence[Sequence[float]]) -> list[list[float]]:
    rows = [list(row) for row in samples]
    if not rows or not rows[0]:
        raise ValueError("Voiage net-benefit samples must be a non-empty matrix")
    width = len(rows[0])
    if width < 2 or any(len(row) != width for row in rows):
        raise ValueError(
            "Voiage net-benefit samples must be rectangular with at least two strategies"
        )
    if any(not math.isfinite(float(value)) for row in rows for value in row):
        raise ValueError("Voiage net-benefit samples must contain only finite numbers")
    return rows
