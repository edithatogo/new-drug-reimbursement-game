"""Research-only post-2015 extensions with explicit assumptions.

These helpers do not replace Pekarsky source equations or Voiage/Kairos
capabilities. They provide deterministic application state for exploration.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal


def _positive(name: str, value: float) -> float:
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be positive and finite")
    return value


def _non_negative(name: str, value: float) -> float:
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be finite and non-negative")
    return value


@dataclass(frozen=True, slots=True)
class EquityEvaluation:
    weighted_health: float
    subgroup_contributions: tuple[float, ...]
    equity_weights: tuple[float, ...]
    parameterization: Literal["extension"] = "extension"


def evaluate_distributional_equity(
    subgroup_health: tuple[float, ...], equity_weights: tuple[float, ...]
) -> EquityEvaluation:
    """Apply caller-supplied equity weights without hiding subgroup outcomes."""

    if not subgroup_health or len(subgroup_health) != len(equity_weights):
        raise ValueError("subgroup health and equity weights must be non-empty and aligned")
    if any(not math.isfinite(value) or value < 0 for value in subgroup_health):
        raise ValueError("subgroup health must be finite and non-negative")
    if any(not math.isfinite(value) or value <= 0 for value in equity_weights):
        raise ValueError("equity weights must be positive and finite")
    total = sum(equity_weights)
    normalized = tuple(value / total for value in equity_weights)
    contributions = tuple(value * weight for value, weight in zip(subgroup_health, normalized, strict=True))
    return EquityEvaluation(sum(contributions), contributions, normalized)


@dataclass(frozen=True, slots=True)
class ManagedEntrySettlement:
    net_price: float
    clawback: float
    terminated: bool
    monitoring_passed: bool
    parameterization: Literal["extension"] = "extension"


def settle_managed_entry(
    *, list_price: float, rebate_rate: float, monitoring_passed: bool,
    clawback_rate: float = 0.0, termination_threshold: float = 0.0,
) -> ManagedEntrySettlement:
    """Settle an outcomes-based agreement with explicit monitoring/clawback."""

    for name, value in (("list_price", list_price), ("rebate_rate", rebate_rate), ("clawback_rate", clawback_rate), ("termination_threshold", termination_threshold)):
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"{name} must be finite and non-negative")
    if rebate_rate > 1 or clawback_rate > 1:
        raise ValueError("rebate and clawback rates must be at most one")
    net = list_price * (1 - rebate_rate)
    clawback = net * clawback_rate if not monitoring_passed else 0.0
    terminated = (not monitoring_passed) and clawback >= termination_threshold > 0
    return ManagedEntrySettlement(net - clawback, clawback, terminated, monitoring_passed)


@dataclass(frozen=True, slots=True)
class AdaptiveEvidenceDecision:
    action: Literal["continue", "stop"]
    information_value: float
    threshold: float
    state: str
    parameterization: Literal["extension"] = "extension"


def choose_adaptive_evidence_action(*, state: str, information_value: float, stop_threshold: float) -> AdaptiveEvidenceDecision:
    """Choose a bounded evidence action using a Voiage-supplied value."""

    if not state.strip():
        raise ValueError("evidence state must be non-empty")
    _non_negative("information_value", information_value)
    _positive("stop_threshold", stop_threshold)
    action: Literal["continue", "stop"] = "stop" if information_value < stop_threshold else "continue"
    return AdaptiveEvidenceDecision(action, information_value, stop_threshold, state)


@dataclass(frozen=True, slots=True)
class PortfolioSpillover:
    local_value: float
    global_value: float
    payer_share: float
    parameterization: Literal["extension"] = "extension"


def evaluate_portfolio_spillover(*, local_value: float, global_value: float, payer_share: float) -> PortfolioSpillover:
    """Separate local value from globally distributed innovation spillovers."""

    _non_negative("local_value", local_value)
    _non_negative("global_value", global_value)
    if not math.isfinite(payer_share) or not 0 <= payer_share <= 1:
        raise ValueError("payer_share must be finite and between zero and one")
    return PortfolioSpillover(local_value, global_value, payer_share)
