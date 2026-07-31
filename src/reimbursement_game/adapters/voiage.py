"""Voiage adapter.

VOI algorithms are intentionally not reimplemented in this repository.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any

from ..calibration import VoiageSampleBundle


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
