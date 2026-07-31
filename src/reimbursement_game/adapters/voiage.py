"""Voiage adapter.

VOI algorithms are intentionally not reimplemented in this repository.
"""

from __future__ import annotations

import math
from collections.abc import Sequence


class VoiageAdapter:
    """Convert application net-benefit samples to Voiage's DecisionAnalysis."""

    def evpi(self, net_benefit_samples: Sequence[Sequence[float]]) -> float:
        # Validate the boundary before importing the optional ecosystem.  This
        # keeps malformed application data distinguishable from an unavailable
        # Voiage installation and prevents ragged arrays being silently
        # coerced into object arrays.
        rows = [list(row) for row in net_benefit_samples]
        if not rows or not rows[0]:
            raise ValueError("Voiage net-benefit samples must be a non-empty matrix")
        width = len(rows[0])
        if width < 2 or any(len(row) != width for row in rows):
            raise ValueError("Voiage net-benefit samples must be rectangular with at least two strategies")
        if any(not math.isfinite(float(value)) for row in rows for value in row):
            raise ValueError("Voiage net-benefit samples must contain only finite numbers")
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
