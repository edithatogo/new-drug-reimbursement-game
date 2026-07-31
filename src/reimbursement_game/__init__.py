"""New-drug reimbursement game application package."""

from .chapter8 import Chapter8Equilibrium, solve_pekarsky_game1, solve_revealed_threshold_game
from .economics import (
    EconomicContext,
    OpportunitySet,
    ReimbursementEvaluation,
    ReimbursementInputs,
    evaluate_reimbursement,
    health_shadow_price,
    incremental_price_effectiveness_ratio,
)

__all__ = [
    "Chapter8Equilibrium",
    "EconomicContext",
    "OpportunitySet",
    "ReimbursementEvaluation",
    "ReimbursementInputs",
    "evaluate_reimbursement",
    "health_shadow_price",
    "incremental_price_effectiveness_ratio",
    "solve_revealed_threshold_game",
    "solve_pekarsky_game1",
]

__version__ = "0.4.0"
