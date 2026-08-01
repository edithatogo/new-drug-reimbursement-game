"""Auditable application games derived from Pekarsky with named extensions.

The functions here are application models, not generic runtime mechanics. Each
result carries the assumptions and source/extension classification so callers
cannot mistake a variant for source-equation conformance.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal


def _finite(name: str, value: float, *, positive: bool = False) -> float:
    if not math.isfinite(value) or (positive and value <= 0):
        requirement = "positive and finite" if positive else "finite"
        raise ValueError(f"{name} must be {requirement}")
    return value


@dataclass(frozen=True, slots=True)
class Game1Result:
    offered_price: float | None
    reimbursed: bool
    quantity: float
    firm_rent: float
    institution_nebh: float
    threshold: float
    assumptions: tuple[str, ...]
    parameterization: Literal["source-exact", "extension"]


def solve_game1_grid(
    *,
    threshold: float,
    incremental_effect: float,
    production_cost: float = 0.0,
    price_step: float = 1.0,
    max_price: float | None = None,
    tie_policy: Literal["reimburse", "reject"] = "reimburse",
) -> Game1Result:
    """Solve a finite price grid approximating the continuous-price game.

    The grid chooses the highest reimbursable offer, with an explicit tie rule.
    ``threshold`` corresponds to the health shadow price in the source corner
    solution; quantity/effect is fixed in this application boundary.
    """

    _finite("threshold", threshold, positive=True)
    _finite("incremental_effect", incremental_effect, positive=True)
    _finite("production_cost", production_cost)
    _finite("price_step", price_step, positive=True)
    upper = threshold if max_price is None else _finite("max_price", max_price, positive=True)
    if upper < price_step:
        raise ValueError("max_price must be at least price_step")
    if tie_policy not in {"reimburse", "reject"}:
        raise ValueError("tie_policy must be reimburse or reject")
    prices = [round(index * price_step, 12) for index in range(int(upper / price_step) + 1)]
    eligible = [price for price in prices if price < threshold or (price == threshold and tie_policy == "reimburse")]
    if not eligible:
        return Game1Result(None, False, 0.0, 0.0, 0.0, threshold, ("threshold is not observed at a reimbursable grid point",), "extension")
    price = max(eligible)
    rent = (price - production_cost) * incremental_effect
    return Game1Result(
        price, True, incremental_effect, rent, (threshold - price) * incremental_effect,
        threshold, ("fixed quantity/effect", "firm knows the threshold", f"institution tie policy: {tie_policy}"),
        "source-exact" if production_cost == 0 and tie_policy == "reimburse" else "extension",
    )


def solve_game1_hidden_threshold(
    *, thresholds: tuple[float, ...], incremental_effect: float, production_cost: float = 0.0,
) -> Game1Result:
    """Conservative hidden-threshold extension: offer at the minimum possible threshold."""

    if not thresholds:
        raise ValueError("thresholds must be non-empty")
    checked = tuple(_finite("threshold", value, positive=True) for value in thresholds)
    return solve_game1_grid(threshold=min(checked), incremental_effect=incremental_effect,
                            production_cost=production_cost, price_step=min(checked),
                            tie_policy="reimburse")


def solve_game1_bargaining(*, threshold: float, incremental_effect: float,
                           bargaining_share: float) -> Game1Result:
    """Extension in which the institution and firm split threshold surplus."""

    _finite("bargaining_share", bargaining_share)
    if not 0 <= bargaining_share <= 1:
        raise ValueError("bargaining_share must be between zero and one")
    result = solve_game1_grid(threshold=threshold, incremental_effect=incremental_effect,
                              price_step=threshold, tie_policy="reimburse")
    price = threshold * bargaining_share
    return Game1Result(price, True, incremental_effect, price * incremental_effect,
                       (threshold - price) * incremental_effect, threshold,
                       (*result.assumptions, "bargained surplus share"), "extension")


def solve_game1_net_rebate(*, threshold: float, incremental_effect: float,
                           confidential_rebate: float) -> Game1Result:
    """Extension reporting a list price and a lower net reimbursed price."""

    _finite("confidential_rebate", confidential_rebate)
    if confidential_rebate < 0 or confidential_rebate > threshold:
        raise ValueError("confidential_rebate must be between zero and threshold")
    result = solve_game1_grid(threshold=threshold, incremental_effect=incremental_effect,
                              price_step=threshold, tie_policy="reimburse")
    net_price = threshold - confidential_rebate
    return Game1Result(threshold, True, incremental_effect, net_price * incremental_effect,
                       confidential_rebate * incremental_effect, threshold,
                       (*result.assumptions, "net price after confidential rebate"), "extension")


def solve_game1_contract_enforcement(*, threshold: float, incremental_effect: float,
                                     contract_price: float) -> Game1Result:
    """Extension that rejects a contract price above the health threshold."""

    _finite("contract_price", contract_price)
    if contract_price < 0:
        raise ValueError("contract_price must be non-negative")
    if contract_price > threshold:
        return Game1Result(None, False, 0.0, 0.0, 0.0, threshold,
                           ("contract enforcement rejects price above threshold",), "extension")
    return Game1Result(contract_price, True, incremental_effect,
                       contract_price * incremental_effect,
                       (threshold - contract_price) * incremental_effect, threshold,
                       ("contract enforcement",), "extension")


@dataclass(frozen=True, slots=True)
class Game2Result:
    action: Literal["do_nothing", "lobby", "borrow"]
    success_probability: float
    firm_payoff: float
    institution_payoff: float
    capital_market_payoff: float
    payoffs_by_action: tuple[tuple[str, float], ...]
    assumptions: tuple[str, ...]


def solve_game2(
    *,
    baseline_firm_payoff: float,
    benefit_if_success: float,
    rd_cost: float,
    success_probability: float,
    interest_rate: float,
    lobby_cost: float = 0.0,
    institution_benefit: float = 0.0,
    borrow_limit: float = 0.0,
) -> Game2Result:
    """Choose among do-nothing, lobbying, and borrowing by backward induction."""

    for name, value in (("baseline_firm_payoff", baseline_firm_payoff), ("benefit_if_success", benefit_if_success), ("rd_cost", rd_cost), ("interest_rate", interest_rate), ("lobby_cost", lobby_cost), ("institution_benefit", institution_benefit), ("borrow_limit", borrow_limit)):
        _finite(name, value)
    _finite("success_probability", success_probability)
    if not 0 <= success_probability <= 1 or interest_rate < 0 or rd_cost < 0 or lobby_cost < 0 or borrow_limit < 0:
        raise ValueError("probability and cost/rate parameters are out of bounds")
    success_gain = success_probability * benefit_if_success
    do_nothing = baseline_firm_payoff
    lobby = baseline_firm_payoff + success_gain - rd_cost - lobby_cost
    borrowed = baseline_firm_payoff + success_gain - rd_cost * (1 + interest_rate) if borrow_limit >= rd_cost else float("-inf")
    choices = (("do_nothing", do_nothing), ("lobby", lobby), ("borrow", borrowed))
    action, payoff = max(choices, key=lambda item: (item[1], -("do_nothing", "lobby", "borrow").index(item[0])))
    success = success_probability if action != "do_nothing" else 0.0
    institution = institution_benefit * success
    capital = rd_cost * interest_rate if action == "borrow" else 0.0
    return Game2Result(action, success, payoff, institution, capital, choices,
                       ("success/failure is Bernoulli", "firm observes its own financing cost", "capital market is paid principal interest only"))


@dataclass(frozen=True, slots=True)
class Game3Result:
    first_price: float
    second_price: float
    development_value: float
    public_spillover: float
    firm_payoff: float
    institution_payoff: float
    state_trace: tuple[str, ...]
    assumptions: tuple[str, ...]


def evaluate_game3(
    *,
    first_price: float,
    second_price: float,
    development_cost: float,
    manufacturing_cost: float,
    clinical_probability: float,
    manufacturing_innovation: float = 0.0,
    premium: float = 0.0,
    rebate: float = 0.0,
    public_investment: float = 0.0,
    global_spillover: float = 0.0,
) -> Game3Result:
    """Evaluate a two-drug lifecycle path with explicit contract adjustments."""

    for name, value in (("first_price", first_price), ("second_price", second_price), ("development_cost", development_cost), ("manufacturing_cost", manufacturing_cost), ("manufacturing_innovation", manufacturing_innovation), ("premium", premium), ("rebate", rebate), ("public_investment", public_investment), ("global_spillover", global_spillover)):
        _finite(name, value)
    _finite("clinical_probability", clinical_probability)
    if not 0 <= clinical_probability <= 1 or min(first_price, second_price, development_cost, manufacturing_cost, manufacturing_innovation, premium, rebate, public_investment, global_spillover) < 0:
        raise ValueError("Game 3 probabilities/costs must be non-negative and bounded")
    success_value = clinical_probability * (first_price + second_price + premium - rebate)
    development_value = success_value - development_cost + public_investment
    firm = success_value - development_cost - manufacturing_cost + manufacturing_innovation
    institution = clinical_probability * (public_investment + global_spillover - premium + rebate)
    return Game3Result(first_price, second_price, development_value, global_spillover, firm, institution,
                       ("development", "clinical_success" if clinical_probability == 1 else "clinical_success_or_failure", "second_drug", "competition_and_lifecycle"),
                       ("prices are period-specific", "premium/rebate/public investment are explicit contract terms", "global spillover is reported, not appropriated by the firm"))
