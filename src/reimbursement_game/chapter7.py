"""Strict evaluators for Pekarsky's four Chapter 7 economic scenarios.

These scenario-specific models are separate from :mod:`economics`, whose
opportunity-set maximization is a generalized repository extension. Chapter 7
assumes adoption is required for every clinically innovative drug; consequently
``economically_preferred`` describes the model comparison and is not an
observed reimbursement decision.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum
from typing import TypeAlias


class Chapter7Scenario(StrEnum):
    EXPANDABLE_EFFICIENT = "scenario_1"
    FIXED_EFFICIENT = "scenario_2"
    FIXED_ALLOCATIVE_INEFFICIENCY = "scenario_3"
    FIXED_TECHNICAL_INVESTMENT = "scenario_4"


@dataclass(frozen=True, slots=True)
class Scenario1Inputs:
    incremental_cost: float
    incremental_health_effect: float
    expansion_icer: float
    evidence_revision: str


@dataclass(frozen=True, slots=True)
class Scenario2Inputs:
    incremental_cost: float
    incremental_health_effect: float
    expansion_icer: float
    contraction_icer: float
    displacement_icer: float
    evidence_revision: str


@dataclass(frozen=True, slots=True)
class Scenario3Inputs:
    incremental_cost: float
    incremental_health_effect: float
    expansion_icer: float
    contraction_icer: float
    displacement_icer: float
    evidence_revision: str


@dataclass(frozen=True, slots=True)
class Scenario4Inputs:
    incremental_cost: float
    incremental_health_effect: float
    contraction_icer: float
    displacement_icer: float
    investment_icer: float
    present_value_multiplier: float
    annual_program_health_effect: float
    evidence_revision: str


Chapter7Inputs: TypeAlias = (
    Scenario1Inputs | Scenario2Inputs | Scenario3Inputs | Scenario4Inputs
)


@dataclass(frozen=True, slots=True)
class Chapter7ScenarioEvaluation:
    scenario: Chapter7Scenario
    iper: float
    reimbursement_health_effect: float
    alternative_health_gain: float
    nebh: float
    beta: float
    evci: float
    net_financial_cost: float
    adoption_required: bool
    economically_preferred: bool
    tolerance: float
    budget_shadow_price_expansion: float | None
    budget_shadow_price_contraction: float | None
    conditional_expansion_shadow_price: float | None
    source_location: str
    parameterization: str
    evidence_revision: str | None


@dataclass(frozen=True, slots=True)
class _IntermediateEvaluation:
    scenario: Chapter7Scenario
    reimbursement_effect: float
    alternative_gain: float
    beta: float
    net_cost: float
    expansion_shadow: float | None
    contraction_shadow: float | None
    conditional_expansion_shadow: float | None
    source: str
    parameterization: str


def _positive(name: str, value: float) -> float:
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be positive and finite")
    return value


def _close(left: float, right: float) -> bool:
    tolerance = 1e-12 * max(abs(left), abs(right))
    return abs(left - right) <= tolerance


def _evaluate_scenario_1(
    inputs: Scenario1Inputs, cost: float, effect: float
) -> _IntermediateEvaluation:
    n = _positive("expansion_icer", inputs.expansion_icer)
    return _IntermediateEvaluation(
        scenario=Chapter7Scenario.EXPANDABLE_EFFICIENT,
        reimbursement_effect=effect,
        alternative_gain=cost / n,
        beta=n,
        net_cost=cost,
        expansion_shadow=n,
        contraction_shadow=None,
        conditional_expansion_shadow=None,
        source="Pekarsky 2015, equation 7.1, printed p. 110/PDF p. 120",
        parameterization="exact",
    )


def _evaluate_scenario_2(
    inputs: Scenario2Inputs, cost: float, effect: float
) -> _IntermediateEvaluation:
    n = _positive("expansion_icer", inputs.expansion_icer)
    m = _positive("contraction_icer", inputs.contraction_icer)
    d = _positive("displacement_icer", inputs.displacement_icer)
    if not _close(n, m):
        raise ValueError("Scenario 2 requires economic efficiency n = m")
    return _IntermediateEvaluation(
        scenario=Chapter7Scenario.FIXED_EFFICIENT,
        reimbursement_effect=effect - cost / d,
        alternative_gain=0.0,
        beta=d,
        net_cost=0.0,
        expansion_shadow=None,
        contraction_shadow=m,
        conditional_expansion_shadow=n,
        source="Pekarsky 2015, Scenario 2, printed pp. 110-114/PDF pp. 120-124",
        parameterization="exact",
    )


def _evaluate_scenario_3(
    inputs: Scenario3Inputs, cost: float, effect: float
) -> _IntermediateEvaluation:
    n = _positive("expansion_icer", inputs.expansion_icer)
    m = _positive("contraction_icer", inputs.contraction_icer)
    d = _positive("displacement_icer", inputs.displacement_icer)
    if not m > n:
        raise ValueError("Scenario 3 requires allocative inefficiency m > n")
    if not n <= d <= m:
        raise ValueError("Scenario 3 requires n <= d <= m")
    reallocation_productivity = (1 / n) * (1 - n / m)
    return _IntermediateEvaluation(
        scenario=Chapter7Scenario.FIXED_ALLOCATIVE_INEFFICIENCY,
        reimbursement_effect=effect - cost / d,
        alternative_gain=cost * reallocation_productivity,
        beta=1 / (1 / d + reallocation_productivity),
        net_cost=0.0,
        expansion_shadow=None,
        contraction_shadow=None,
        conditional_expansion_shadow=None,
        source="Pekarsky 2015, equations 7.2-7.5, printed pp. 116-119/PDF pp. 126-129",
        parameterization="exact",
    )


def _evaluate_scenario_4(
    inputs: Scenario4Inputs, cost: float, effect: float
) -> _IntermediateEvaluation:
    m = _positive("contraction_icer", inputs.contraction_icer)
    d = _positive("displacement_icer", inputs.displacement_icer)
    mu = _positive("investment_icer", inputs.investment_icer)
    phi = _positive("present_value_multiplier", inputs.present_value_multiplier)
    annual_effect = _positive(
        "annual_program_health_effect", inputs.annual_program_health_effect
    )
    if phi <= 1:
        raise ValueError("Scenario 4 requires present_value_multiplier phi > 1")
    if mu >= m:
        raise ValueError("Scenario 4 technical inefficiency requires mu < m")
    if d > m:
        raise ValueError("Scenario 4 requires actual displacement d <= m")
    present_value_gain = phi * annual_effect
    implied_gain = cost / mu
    if not _close(present_value_gain, implied_gain):
        raise ValueError("Scenario 4 requires phi * DeltaE_G = incremental_cost / mu")
    investment_productivity = (1 / mu) * (1 - mu / m)
    alternative_gain = cost * investment_productivity
    if alternative_gain <= 0:
        raise ValueError("Scenario 4 requires a positive net investment health gain")
    return _IntermediateEvaluation(
        scenario=Chapter7Scenario.FIXED_TECHNICAL_INVESTMENT,
        reimbursement_effect=effect - cost / d,
        alternative_gain=alternative_gain,
        beta=1 / (1 / d + investment_productivity),
        net_cost=0.0,
        expansion_shadow=None,
        contraction_shadow=None,
        conditional_expansion_shadow=None,
        source="Pekarsky 2012, Appendix 5, pp. 231-234; Pekarsky 2015, Table 7.2",
        parameterization="source-backed-exogenous-mu",
    )


def evaluate_chapter7_scenario(inputs: Chapter7Inputs) -> Chapter7ScenarioEvaluation:
    """Evaluate one strict Chapter 7 scenario using its source-specific domain."""

    cost = _positive("incremental_cost", inputs.incremental_cost)
    effect = _positive("incremental_health_effect", inputs.incremental_health_effect)
    if not inputs.evidence_revision.strip():
        raise ValueError("Chapter 7 scenarios require a non-empty evidence_revision")
    iper = cost / effect

    if isinstance(inputs, Scenario1Inputs):
        res = _evaluate_scenario_1(inputs, cost, effect)
    elif isinstance(inputs, Scenario2Inputs):
        res = _evaluate_scenario_2(inputs, cost, effect)
    elif isinstance(inputs, Scenario3Inputs):
        res = _evaluate_scenario_3(inputs, cost, effect)
    elif isinstance(inputs, Scenario4Inputs):
        res = _evaluate_scenario_4(inputs, cost, effect)
    else:
        raise TypeError("unsupported Chapter 7 scenario input type")

    nebh = res.reimbursement_effect - res.alternative_gain
    evci = res.beta * effect
    values = (
        iper,
        res.reimbursement_effect,
        res.alternative_gain,
        nebh,
        res.beta,
        evci,
        res.net_cost,
    )
    if not all(math.isfinite(value) for value in values):
        raise ValueError("derived Chapter 7 values must be finite")
    tolerance = 1e-12 * max(
        abs(effect),
        abs(res.reimbursement_effect),
        abs(res.alternative_gain),
    )
    return Chapter7ScenarioEvaluation(
        scenario=res.scenario,
        iper=iper,
        reimbursement_health_effect=res.reimbursement_effect,
        alternative_health_gain=res.alternative_gain,
        nebh=nebh,
        beta=res.beta,
        evci=evci,
        net_financial_cost=res.net_cost,
        adoption_required=True,
        economically_preferred=nebh >= -tolerance,
        tolerance=tolerance,
        budget_shadow_price_expansion=res.expansion_shadow,
        budget_shadow_price_contraction=res.contraction_shadow,
        conditional_expansion_shadow_price=res.conditional_expansion_shadow,
        source_location=res.source,
        parameterization=res.parameterization,
        evidence_revision=inputs.evidence_revision,
    )
