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
    common_keys = {
        "schema_version",
        "model_kind",
        "case_id",
        "scenario",
        "incremental_cost",
        "incremental_health_effect",
        "currency_unit",
        "health_unit",
        "evidence_revision",
    }
    scenario_keys = {
        "scenario_1": {"expansion_icer"},
        "scenario_2": {"expansion_icer", "contraction_icer", "displacement_icer"},
        "scenario_3": {"expansion_icer", "contraction_icer", "displacement_icer"},
        "scenario_4": {
            "contraction_icer",
            "displacement_icer",
            "investment_icer",
            "present_value_multiplier",
            "annual_program_health_effect",
        },
    }
    scenario = case.get("scenario")
    if scenario not in scenario_keys:
        raise ValueError(
            "Chapter 7 case scenario must be scenario_1, scenario_2, scenario_3, or scenario_4"
        )
    expected_keys = common_keys | scenario_keys[str(scenario)]
    unexpected = sorted(set(case) - expected_keys)
    missing = sorted(expected_keys - set(case))
    if unexpected:
        raise ValueError(f"Chapter 7 case contains scenario-incompatible fields: {unexpected}")
    if missing:
        raise ValueError(f"Chapter 7 case is missing required fields: {missing}")
    common = {
        "incremental_cost": _required_number(case, "incremental_cost"),
        "incremental_health_effect": _required_number(case, "incremental_health_effect"),
    }
    if scenario == "scenario_1":
        return Scenario1Inputs(**common, expansion_icer=_required_number(case, "expansion_icer"))
    if scenario == "scenario_2":
        return Scenario2Inputs(
            **common,
            expansion_icer=_required_number(case, "expansion_icer"),
            contraction_icer=_required_number(case, "contraction_icer"),
            displacement_icer=_required_number(case, "displacement_icer"),
        )
    if scenario == "scenario_3":
        return Scenario3Inputs(
            **common,
            expansion_icer=_required_number(case, "expansion_icer"),
            contraction_icer=_required_number(case, "contraction_icer"),
            displacement_icer=_required_number(case, "displacement_icer"),
        )
    if scenario == "scenario_4":
        return Scenario4Inputs(
            **common,
            contraction_icer=_required_number(case, "contraction_icer"),
            displacement_icer=_required_number(case, "displacement_icer"),
            investment_icer=_required_number(case, "investment_icer"),
            present_value_multiplier=_required_number(case, "present_value_multiplier"),
            annual_program_health_effect=_required_number(
                case, "annual_program_health_effect"
            ),
            evidence_revision=str(case["evidence_revision"]),
        )
    raise AssertionError("unreachable validated Chapter 7 scenario")


def _optional_float(value: Any) -> float | None:
    return None if value is None else float(value)


def _required_number(case: dict[str, Any], field: str) -> float:
    value = case[field]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"Chapter 7 case field {field} must be a JSON number")
    return float(value)
