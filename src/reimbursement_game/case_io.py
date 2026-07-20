"""JSON case parsing for the application."""

from __future__ import annotations

from typing import Any

from .economics import (
    AlternativeStrategy,
    EconomicContext,
    OpportunitySet,
    ReimbursementInputs,
)


def inputs_from_case(case: dict[str, Any]) -> ReimbursementInputs:
    raw_opportunities = case["opportunities"]
    alternatives = tuple(
        AlternativeStrategy(
            name=str(item["name"]),
            health_gain_per_currency=float(item["health_gain_per_currency"]),
            provenance=str(item.get("provenance", "user supplied")),
        )
        for item in raw_opportunities.get("additional_alternatives", [])
    )
    opportunities = OpportunitySet(
        expansion_icer=_optional_float(raw_opportunities.get("expansion_icer")),
        contraction_icer=_optional_float(raw_opportunities.get("contraction_icer")),
        displacement_icer=_optional_float(raw_opportunities.get("displacement_icer")),
        additional_alternatives=alternatives,
    )
    return ReimbursementInputs(
        incremental_cost=float(case["incremental_cost"]),
        incremental_health_effect=float(case["incremental_health_effect"]),
        context=EconomicContext(str(case["context"])),
        opportunities=opportunities,
    )


def _optional_float(value: Any) -> float | None:
    return None if value is None else float(value)
