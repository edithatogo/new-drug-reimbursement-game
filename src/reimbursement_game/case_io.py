"""JSON case parsing for the application."""

from __future__ import annotations

from typing import Any

from .chapter7 import (
    Chapter7Inputs,
    Scenario1Inputs,
    Scenario2Inputs,
    Scenario3Inputs,
    Scenario4Inputs,
)
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


def chapter7_inputs_from_case(case: dict[str, Any]) -> Chapter7Inputs:
    """Parse a strict versioned Chapter 7 scenario document."""

    if case.get("schema_version") != 1:
        raise ValueError("Chapter 7 case requires schema_version 1")
    if case.get("model_kind") != "pekarsky-2015-ch7":
        raise ValueError("Chapter 7 case requires model_kind pekarsky-2015-ch7")
    for field in ("case_id", "currency_unit", "health_unit", "evidence_revision"):
        if not isinstance(case.get(field), str) or not str(case[field]).strip():
            raise ValueError(f"Chapter 7 case requires non-empty {field}")
    common = {
        "incremental_cost": float(case["incremental_cost"]),
        "incremental_health_effect": float(case["incremental_health_effect"]),
    }
    scenario = case.get("scenario")
    if scenario == "scenario_1":
        return Scenario1Inputs(**common, expansion_icer=float(case["expansion_icer"]))
    if scenario == "scenario_2":
        return Scenario2Inputs(
            **common,
            expansion_icer=float(case["expansion_icer"]),
            contraction_icer=float(case["contraction_icer"]),
            displacement_icer=float(case["displacement_icer"]),
        )
    if scenario == "scenario_3":
        return Scenario3Inputs(
            **common,
            expansion_icer=float(case["expansion_icer"]),
            contraction_icer=float(case["contraction_icer"]),
            displacement_icer=float(case["displacement_icer"]),
        )
    if scenario == "scenario_4":
        return Scenario4Inputs(
            **common,
            contraction_icer=float(case["contraction_icer"]),
            displacement_icer=float(case["displacement_icer"]),
            investment_icer=float(case["investment_icer"]),
            present_value_multiplier=float(case["present_value_multiplier"]),
            annual_program_health_effect=float(case["annual_program_health_effect"]),
            evidence_revision=str(case["evidence_revision"]),
        )
    raise ValueError("Chapter 7 case scenario must be scenario_1, scenario_2, scenario_3, or scenario_4")


def _optional_float(value: Any) -> float | None:
    return None if value is None else float(value)
