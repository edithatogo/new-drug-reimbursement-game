"""New-drug reimbursement game application package."""

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
from .application_games import (
    Game1Result,
    Game2Result,
    Game3Result,
    evaluate_game3,
    solve_game1_grid,
    solve_game1_hidden_threshold,
    solve_game1_bargaining,
    solve_game1_net_rebate,
    solve_game1_contract_enforcement,
    solve_game2,
)
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

__all__ = [
    "CalibratedScenario",
    "CalibrationReceipt",
    "Chapter7Scenario",
    "Chapter7ScenarioEvaluation",
    "Chapter8Equilibrium",
    "EconomicContext",
    "EvidencePacket",
    "OpportunitySet",
    "ParameterEvidenceRecord",
    "ParameterRole",
    "ReimbursementEvaluation",
    "ReimbursementInputs",
    "Scenario1Inputs",
    "Scenario2Inputs",
    "Scenario3Inputs",
    "Scenario4Inputs",
    "VoiageSampleBundle",
    "calibrate_chapter7_scenario",
    "evaluate_chapter7_scenario",
    "evaluate_reimbursement",
    "health_shadow_price",
    "incremental_price_effectiveness_ratio",
    "solve_pekarsky_game1",
    "solve_revealed_threshold_game",
    "Game1Result",
    "Game2Result",
    "Game3Result",
    "evaluate_game3",
    "solve_game1_grid",
    "solve_game1_hidden_threshold",
    "solve_game1_bargaining",
    "solve_game1_net_rebate",
    "solve_game1_contract_enforcement",
    "solve_game2",
]

__version__ = "0.4.0"
