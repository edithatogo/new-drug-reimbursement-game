import unittest

from reimbursement_game.application_games import (
    evaluate_game3,
    solve_game1_bargaining,
    solve_game1_contract_enforcement,
    solve_game1_grid,
    solve_game1_hidden_threshold,
    solve_game1_net_rebate,
    solve_game2,
)


class ApplicationGamesTests(unittest.TestCase):
    def test_game1_grid_reaches_reimbursable_threshold(self) -> None:
        result = solve_game1_grid(threshold=10, incremental_effect=2, price_step=1)
        self.assertEqual(result.offered_price, 10)
        self.assertEqual(result.parameterization, "source-exact")

    def test_game1_tie_rejection_and_hidden_threshold(self) -> None:
        rejected = solve_game1_grid(threshold=10, incremental_effect=2, price_step=1, tie_policy="reject")
        self.assertEqual(rejected.offered_price, 9)
        hidden = solve_game1_hidden_threshold(thresholds=(10, 12), incremental_effect=2)
        self.assertEqual(hidden.offered_price, 10)

    def test_game1_named_variants_are_explicit_extensions(self) -> None:
        self.assertEqual(solve_game1_bargaining(threshold=10, incremental_effect=2, bargaining_share=0.5).offered_price, 5)
        rebate = solve_game1_net_rebate(threshold=10, incremental_effect=2, synthetic_rebate=2)
        self.assertEqual(rebate.firm_rent, 16)
        self.assertIn("synthetic rebate; reconstructable public demonstration", rebate.assumptions)
        self.assertFalse(solve_game1_contract_enforcement(threshold=10, incremental_effect=2, contract_price=11).reimbursed)
        with self.assertRaisesRegex(ValueError, "incremental_effect"):
            solve_game1_contract_enforcement(threshold=10, incremental_effect=0, contract_price=5)

    def test_game2_deterministic_backward_choice(self) -> None:
        result = solve_game2(
            baseline_firm_payoff=1,
            benefit_if_success=20,
            rd_cost=4,
            success_probability=0.5,
            interest_rate=0.1,
            lobby_cost=3,
            institution_benefit=5,
            borrow_limit=4,
        )
        self.assertEqual(result.action, "borrow")
        self.assertEqual(result.capital_market_payoff, 0.4)

    def test_game3_contract_and_spillover_are_explicit(self) -> None:
        result = evaluate_game3(
            first_price=10,
            second_price=12,
            development_cost=5,
            manufacturing_cost=2,
            clinical_probability=0.5,
            premium=2,
            rebate=1,
            public_investment=3,
            global_spillover=7,
        )
        self.assertEqual(result.state_trace[0], "development")
        self.assertEqual(result.public_spillover, 7)
        self.assertAlmostEqual(result.development_value, 9.5)

    def test_games_reject_invalid_probabilities(self) -> None:
        with self.assertRaisesRegex(ValueError, "out of bounds"):
            solve_game2(
                baseline_firm_payoff=1,
                benefit_if_success=2,
                rd_cost=1,
                success_probability=2,
                interest_rate=0,
            )


if __name__ == "__main__":
    unittest.main()
