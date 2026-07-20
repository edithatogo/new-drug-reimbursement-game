"""Voiage adapter.

VOI algorithms are intentionally not reimplemented in this repository.
"""

from __future__ import annotations

from collections.abc import Sequence


class VoiageAdapter:
    """Convert application net-benefit samples to Voiage's DecisionAnalysis."""

    def evpi(self, net_benefit_samples: Sequence[Sequence[float]]) -> float:
        try:
            import numpy as np
            from voiage.analysis import DecisionAnalysis
            from voiage.schema import ValueArray
        except ImportError as exc:  # pragma: no cover - optional ecosystem checkout
            raise RuntimeError(
                "Install or check out edithatogo/voiage to use VOI analysis"
            ) from exc
        array = np.asarray(net_benefit_samples, dtype=float)
        value_array = ValueArray.from_numpy(array)
        return float(DecisionAnalysis(value_array).evpi())
