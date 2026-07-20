"""Declared-assumption Chapter-8-style reimbursement game.

The model follows the strategic structure in Pekarsky (2015), Chapter 8: a firm
selects an IPER and the institution reimburses when the offer is no greater than
the health shadow price. The continuous-price corner solution is implemented
analytically. It is not claimed to cover bargaining, hidden rebates, repeated
interaction, heterogeneous indications, or private information.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from .economics import (
    EconomicContext,
    OpportunitySet,
    ReimbursementInputs,
    evaluate_reimbursement,
    health_shadow_price,
)


@dataclass(frozen=True, slots=True)
class Chapter8Equilibrium:
    offered_iper: float | None
    reimbursed: bool
    firm_economic_rent: float
    institution_nebh: float
    health_shadow_price: float
    reason: str


def solve_revealed_threshold_game(
    *,
    incremental_health_effect: float,
    context: EconomicContext,
    opportunities: OpportunitySet,
    marginal_cost_per_health_effect: float = 0.0,
) -> Chapter8Equilibrium:
    """Solve the public-threshold corner solution under stated assumptions.

    Assumptions:
    - target quantity/effect does not increase below the threshold;
    - the firm knows the threshold;
    - the institution reimburses when indifferent;
    - the firm does not lobby for a price above the threshold in this game;
    - marginal production cost is expressed per incremental health unit.
    """

    if not math.isfinite(incremental_health_effect) or incremental_health_effect <= 0:
        raise ValueError("incremental_health_effect must be positive and finite")
    if (
        not math.isfinite(marginal_cost_per_health_effect)
        or marginal_cost_per_health_effect < 0
    ):
        raise ValueError("marginal_cost_per_health_effect must be non-negative and finite")
    beta, _ = health_shadow_price(context, opportunities)
    if marginal_cost_per_health_effect > beta:
        return Chapter8Equilibrium(
            offered_iper=None,
            reimbursed=False,
            firm_economic_rent=0.0,
            institution_nebh=0.0,
            health_shadow_price=beta,
            reason="minimum viable price exceeds the institution's shadow price",
        )
    price = beta
    cost = price * incremental_health_effect
    evaluation = evaluate_reimbursement(
        ReimbursementInputs(
            incremental_cost=cost,
            incremental_health_effect=incremental_health_effect,
            context=context,
            opportunities=opportunities,
        )
    )
    rent = (price - marginal_cost_per_health_effect) * incremental_health_effect
    return Chapter8Equilibrium(
        offered_iper=price,
        reimbursed=True,
        firm_economic_rent=rent,
        institution_nebh=evaluation.net_economic_benefit_health,
        health_shadow_price=beta,
        reason="firm chooses the highest reimbursable IPER",
    )
