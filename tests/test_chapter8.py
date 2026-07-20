import unittest

from reimbursement_game.chapter8 import solve_revealed_threshold_game
from reimbursement_game.economics import EconomicContext, OpportunitySet


class Chapter8Tests(unittest.TestCase):
    def test_firm_offers_at_threshold(self) -> None:
        opportunities = OpportunitySet(
            expansion_icer=20_000,
            contraction_icer=60_000,
            displacement_icer=40_000,
        )
        result = solve_revealed_threshold_game(
            incremental_health_effect=10,
            context=EconomicContext.FIXED,
            opportunities=opportunities,
            marginal_cost_per_health_effect=5_000,
        )
        self.assertTrue(result.reimbursed)
        self.assertAlmostEqual(result.offered_iper or 0, result.health_shadow_price)
        self.assertAlmostEqual(result.institution_nebh, 0.0, places=10)
        self.assertGreater(result.firm_economic_rent, 0)

    def test_no_trade_above_minimum_viable_price(self) -> None:
        opportunities = OpportunitySet(displacement_icer=20_000)
        result = solve_revealed_threshold_game(
            incremental_health_effect=1,
            context=EconomicContext.FIXED,
            opportunities=opportunities,
            marginal_cost_per_health_effect=30_000,
        )
        self.assertFalse(result.reimbursed)
        self.assertIsNone(result.offered_iper)


if __name__ == "__main__":
    unittest.main()
