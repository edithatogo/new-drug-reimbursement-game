"""Clean-room price-effectiveness analysis primitives.

Conceptual source
-----------------
Pekarsky, B.A.K. (2015), Chapters 6–8, especially the definitions of IPER,
reimbursement as adoption plus financing, NEBhR, EVCI, and equations 7.2–7.5.
DOI: 10.1007/978-3-319-08903-4.

The module does not reproduce source prose. It expresses the economic identities
as independently written code and makes uncertain extensions explicit.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum


class EconomicContext(StrEnum):
    """Budget-financing context for reimbursement."""

    EXPANDABLE = "expandable"
    FIXED = "fixed"


@dataclass(frozen=True, slots=True)
class AlternativeStrategy:
    """A competing use of one unit of health-budget resource.

    ``health_gain_per_currency`` is expressed in health units per currency unit.
    Keeping the primitive in productivity units prevents the application from
    silently treating every technical-efficiency parameter as an ICER.
    """

    name: str
    health_gain_per_currency: float
    provenance: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("alternative strategy name must not be empty")
        if not math.isfinite(self.health_gain_per_currency):
            raise ValueError("alternative productivity must be finite")
        if self.health_gain_per_currency < 0:
            raise ValueError("alternative productivity must be non-negative")


@dataclass(frozen=True, slots=True)
class OpportunitySet:
    """Expansion, contraction, displacement, and additional alternatives.

    ``expansion_icer`` corresponds to Pekarsky's ``n``.
    ``contraction_icer`` corresponds to ``m``.
    ``displacement_icer`` corresponds to ``d``.

    Additional alternatives make technical-efficiency and later extensions
    explicit. The best alternative is chosen by productivity; alternatives are
    not automatically summed unless the caller defines a combined strategy.
    """

    expansion_icer: float | None = None
    contraction_icer: float | None = None
    displacement_icer: float | None = None
    additional_alternatives: tuple[AlternativeStrategy, ...] = ()

    def __post_init__(self) -> None:
        for field_name, value in (
            ("expansion_icer", self.expansion_icer),
            ("contraction_icer", self.contraction_icer),
            ("displacement_icer", self.displacement_icer),
        ):
            if value is not None and (not math.isfinite(value) or value <= 0):
                raise ValueError(f"{field_name} must be finite and greater than zero")

    def reallocation_productivity(self) -> float:
        """Health gain per currency from moving resources from ``m`` to ``n``.

        This is ``max(0, 1/n - 1/m)``. It is zero when either parameter is
        unavailable or when the supplied ordering does not imply a gain.
        """

        if self.expansion_icer is None or self.contraction_icer is None:
            return 0.0
        return max(0.0, 1.0 / self.expansion_icer - 1.0 / self.contraction_icer)

    def candidates(self) -> tuple[AlternativeStrategy, ...]:
        candidates = list(self.additional_alternatives)
        reallocation = self.reallocation_productivity()
        if reallocation > 0:
            candidates.append(
                AlternativeStrategy(
                    name="reallocate_from_m_to_n",
                    health_gain_per_currency=reallocation,
                    provenance="Pekarsky 2015, Chapter 7",
                )
            )
        if self.expansion_icer is not None:
            candidates.append(
                AlternativeStrategy(
                    name="expand_best_available_programme",
                    health_gain_per_currency=1.0 / self.expansion_icer,
                    provenance="Pekarsky 2015, Chapters 6–7",
                )
            )
        return tuple(candidates)

    def best_alternative(self, *, fixed_budget: bool) -> AlternativeStrategy | None:
        """Return the best alternative relevant to the financing context.

        Under a fixed budget, the reallocation gain is incremental to the
        displacement loss; ordinary expansion is not separately added. Under an
        expandable/constrained budget, the best expansion use is relevant.
        """

        if fixed_budget:
            candidates = [
                item for item in self.additional_alternatives if item.health_gain_per_currency >= 0
            ]
            reallocation = self.reallocation_productivity()
            if reallocation > 0:
                candidates.append(
                    AlternativeStrategy(
                        "reallocate_from_m_to_n",
                        reallocation,
                        "Pekarsky 2015, Chapter 7",
                    )
                )
        else:
            candidates = list(self.additional_alternatives)
            if self.expansion_icer is not None:
                candidates.append(
                    AlternativeStrategy(
                        "expand_best_available_programme",
                        1.0 / self.expansion_icer,
                        "Pekarsky 2015, Chapters 6–7",
                    )
                )
        if not candidates:
            return None
        return max(candidates, key=lambda item: (item.health_gain_per_currency, item.name))


@dataclass(frozen=True, slots=True)
class ReimbursementInputs:
    incremental_cost: float
    incremental_health_effect: float
    context: EconomicContext
    opportunities: OpportunitySet

    def __post_init__(self) -> None:
        if not math.isfinite(self.incremental_cost) or self.incremental_cost <= 0:
            raise ValueError("incremental_cost must be finite and greater than zero")
        if not math.isfinite(self.incremental_health_effect) or self.incremental_health_effect <= 0:
            raise ValueError("incremental_health_effect must be finite and greater than zero")
        if self.context is EconomicContext.FIXED and self.opportunities.displacement_icer is None:
            raise ValueError("fixed-budget reimbursement requires displacement_icer")


@dataclass(frozen=True, slots=True)
class ReimbursementEvaluation:
    iper: float
    health_shadow_price: float
    adoption_health_gain: float
    displacement_health_loss: float
    best_alternative_health_gain: float
    reimbursement_population_health_effect: float
    net_economic_benefit_health: float
    economic_value_clinical_innovation: float
    reimburse: bool
    binding_alternative: str | None


def incremental_price_effectiveness_ratio(cost: float, health_effect: float) -> float:
    """Return incremental price per incremental health effect (IPER)."""

    if not math.isfinite(cost) or cost <= 0:
        raise ValueError("cost must be finite and greater than zero")
    if not math.isfinite(health_effect) or health_effect <= 0:
        raise ValueError("health_effect must be finite and greater than zero")
    return cost / health_effect


def health_shadow_price(
    context: EconomicContext,
    opportunities: OpportunitySet,
) -> tuple[float, str | None]:
    """Derive the maximum IPER consistent with zero NEBhR.

    For a fixed budget, the inverse shadow price is the health loss from
    displacement plus the productivity of the best alternative strategy:

    ``1 / beta = 1 / d + g_best``.

    With the reallocation alternative only, this becomes Pekarsky's Chapter 7
    expression ``1 / beta = 1/d + 1/n - 1/m``. When ``n == m`` it reduces to
    ``beta == d``; when ``d == m`` it reduces to ``beta == n``.

    For an expandable/constrained budget, the best alternative expansion has
    productivity ``1/n`` and therefore ``beta == n`` when that is the only
    alternative.
    """

    fixed = context is EconomicContext.FIXED
    best = opportunities.best_alternative(fixed_budget=fixed)
    best_productivity = 0.0 if best is None else best.health_gain_per_currency
    displacement_loss = 0.0
    if fixed:
        if opportunities.displacement_icer is None:
            raise ValueError("fixed-budget context requires displacement_icer")
        displacement_loss = 1.0 / opportunities.displacement_icer
    denominator = displacement_loss + best_productivity
    if denominator <= 0 or not math.isfinite(denominator):
        raise ValueError("no positive opportunity cost is defined for this context")
    return 1.0 / denominator, None if best is None else best.name


def evaluate_reimbursement(inputs: ReimbursementInputs) -> ReimbursementEvaluation:
    """Evaluate adoption plus financing against the best alternative strategy."""

    iper = incremental_price_effectiveness_ratio(
        inputs.incremental_cost, inputs.incremental_health_effect
    )
    beta, binding = health_shadow_price(inputs.context, inputs.opportunities)
    fixed = inputs.context is EconomicContext.FIXED
    displacement_loss = 0.0
    if fixed:
        assert inputs.opportunities.displacement_icer is not None
        displacement_loss = inputs.incremental_cost / inputs.opportunities.displacement_icer
    alternative = inputs.opportunities.best_alternative(fixed_budget=fixed)
    alternative_gain = (
        0.0
        if alternative is None
        else inputs.incremental_cost * alternative.health_gain_per_currency
    )
    reimbursement_effect = inputs.incremental_health_effect - displacement_loss
    nebh = reimbursement_effect - alternative_gain
    evci = beta * inputs.incremental_health_effect
    derived_values = {
        "iper": iper,
        "health_shadow_price": beta,
        "displacement_health_loss": displacement_loss,
        "best_alternative_health_gain": alternative_gain,
        "reimbursement_population_health_effect": reimbursement_effect,
        "net_economic_benefit_health": nebh,
        "economic_value_clinical_innovation": evci,
    }
    non_finite = [name for name, value in derived_values.items() if not math.isfinite(value)]
    if non_finite:
        raise ValueError(f"derived economic values must be finite: {', '.join(non_finite)}")
    tolerance = 1e-12 * max(1.0, abs(beta), abs(iper))
    return ReimbursementEvaluation(
        iper=iper,
        health_shadow_price=beta,
        adoption_health_gain=inputs.incremental_health_effect,
        displacement_health_loss=displacement_loss,
        best_alternative_health_gain=alternative_gain,
        reimbursement_population_health_effect=reimbursement_effect,
        net_economic_benefit_health=nebh,
        economic_value_clinical_innovation=evci,
        reimburse=iper <= beta + tolerance,
        binding_alternative=binding,
    )
