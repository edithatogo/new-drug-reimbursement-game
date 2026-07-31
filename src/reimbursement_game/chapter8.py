"""Exact and generalized Chapter-8-style reimbursement games.

The model follows the strategic structure in Pekarsky (2015), Chapter 8: a firm
selects an IPER and the institution reimburses when the offer is no greater than
the health shadow price. The continuous-price corner solution is implemented
analytically. :func:`solve_pekarsky_game1` enforces the source model's
quantitative identifying conditions. :func:`solve_revealed_threshold_game` is
a generalized extension and must not be presented as exact equation 8.2
conformance.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

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


def solve_pekarsky_game1(
    *,
    incremental_health_effect: float,
    context: EconomicContext,
    opportunities: OpportunitySet,
) -> Chapter8Equilibrium:
    """Solve Chapter 8 Game 1 under its exact quantitative conditions.

    The exact model requires a fixed budget, ``m > n > 0``, ``n <= d <= m``,
    no additional competing strategies, and a zero incremental manufacturing
    cost-effectiveness ratio (IMER). Qualitative institutional assumptions are
    recorded in the source-conformance audit and remain caller attestations.
    """

    if context is not EconomicContext.FIXED:
        raise ValueError("Pekarsky Game 1 requires a fixed budget")
    n = opportunities.expansion_icer
    m = opportunities.contraction_icer
    d = opportunities.displacement_icer
    if n is None or m is None or d is None:
        raise ValueError("Pekarsky Game 1 requires expansion, contraction, and displacement ICERs")
    if not m > n:
        raise ValueError("Pekarsky Game 1 requires allocative inefficiency m > n")
    if not n <= d <= m:
        raise ValueError("Pekarsky Game 1 requires n <= d <= m")
    if opportunities.additional_alternatives:
        raise ValueError("Pekarsky Game 1 does not include additional alternative strategies")
    return solve_revealed_threshold_game(
        incremental_health_effect=incremental_health_effect,
        context=context,
        opportunities=opportunities,
        incremental_imer=0.0,
    )


def solve_revealed_threshold_game(
    *,
    incremental_health_effect: float,
    context: EconomicContext,
    opportunities: OpportunitySet,
    incremental_imer: float = 0.0,
) -> Chapter8Equilibrium:
    """Solve a generalized public-threshold corner solution.

    Assumptions:
    - target quantity/effect does not increase below the threshold;
    - the firm knows the threshold;
    - the institution reimburses when indifferent;
    - the firm does not lobby for a price above the threshold in this game;
    - ``incremental_imer`` is incremental manufacturing cost per incremental
      health unit; Pekarsky Game 1 fixes it at zero.

    Unlike the exact source game, this extension permits other budget contexts,
    opportunity sets, and a non-zero IMER. Use :func:`solve_pekarsky_game1`
    when claiming equation 8.2 conformance.
    """

    if not math.isfinite(incremental_health_effect) or incremental_health_effect <= 0:
        raise ValueError("incremental_health_effect must be positive and finite")
    if not math.isfinite(incremental_imer) or incremental_imer < 0:
        raise ValueError("incremental_imer must be non-negative and finite")
    beta, _ = health_shadow_price(context, opportunities)
    if incremental_imer > beta:
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
    rent = (price - incremental_imer) * incremental_health_effect
    return Chapter8Equilibrium(
        offered_iper=price,
        reimbursed=True,
        firm_economic_rent=rent,
        institution_nebh=evaluation.net_economic_benefit_health,
        health_shadow_price=beta,
        reason="firm chooses the highest reimbursable IPER",
    )
