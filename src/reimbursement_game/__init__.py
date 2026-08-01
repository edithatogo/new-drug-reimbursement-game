"""New-drug reimbursement game application package."""

from .application_games import (
    Game1Result,
    Game2Result,
    Game3Result,
    evaluate_game3,
    solve_game1_bargaining,
    solve_game1_contract_enforcement,
    solve_game1_grid,
    solve_game1_hidden_threshold,
    solve_game1_net_rebate,
    solve_game2,
)
from .calibration import (
    CalibratedScenario,
    CalibrationReceipt,
    VoiageSampleBundle,
    calibrate_chapter7_scenario,
)
from .chapter7 import (
    Chapter7Scenario,
    Chapter7ScenarioEvaluation,
    Scenario1Inputs,
    Scenario2Inputs,
    Scenario3Inputs,
    Scenario4Inputs,
    evaluate_chapter7_scenario,
)
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
from .evidence import EvidencePacket, ParameterEvidenceRecord, ParameterRole
from .research_extensions import (
    AdaptiveEvidenceDecision,
    EquityEvaluation,
    ManagedEntrySettlement,
    PortfolioSpillover,
    choose_adaptive_evidence_action,
    evaluate_distributional_equity,
    evaluate_portfolio_spillover,
    settle_managed_entry,
)

__all__ = [
    "AdaptiveEvidenceDecision",
    "CalibratedScenario",
    "CalibrationReceipt",
    "Chapter7Scenario",
    "Chapter7ScenarioEvaluation",
    "Chapter8Equilibrium",
    "EconomicContext",
    "EquityEvaluation",
    "EvidencePacket",
    "Game1Result",
    "Game2Result",
    "Game3Result",
    "ManagedEntrySettlement",
    "OpportunitySet",
    "ParameterEvidenceRecord",
    "ParameterRole",
    "PortfolioSpillover",
    "ReimbursementEvaluation",
    "ReimbursementInputs",
    "Scenario1Inputs",
    "Scenario2Inputs",
    "Scenario3Inputs",
    "Scenario4Inputs",
    "VoiageSampleBundle",
    "calibrate_chapter7_scenario",
    "choose_adaptive_evidence_action",
    "evaluate_chapter7_scenario",
    "evaluate_distributional_equity",
    "evaluate_game3",
    "evaluate_portfolio_spillover",
    "evaluate_reimbursement",
    "health_shadow_price",
    "incremental_price_effectiveness_ratio",
    "settle_managed_entry",
    "solve_game1_bargaining",
    "solve_game1_contract_enforcement",
    "solve_game1_grid",
    "solve_game1_hidden_threshold",
    "solve_game1_net_rebate",
    "solve_game2",
    "solve_pekarsky_game1",
    "solve_revealed_threshold_game",
]

__version__ = "0.4.0"
