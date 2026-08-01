import unittest

from reimbursement_game.research_extensions import (
    choose_adaptive_evidence_action,
    evaluate_distributional_equity,
    evaluate_portfolio_spillover,
    settle_managed_entry,
)


class ResearchExtensionTests(unittest.TestCase):
    def test_equity_preserves_subgroup_contributions(self) -> None:
        result = evaluate_distributional_equity((10.0, 20.0), (1.0, 3.0))
        self.assertAlmostEqual(result.weighted_health, 17.5)
        self.assertEqual(sum(result.equity_weights), 1.0)

    def test_managed_entry_rebate_and_clawback(self) -> None:
        result = settle_managed_entry(
            list_price=100, rebate_rate=0.1, monitoring_passed=False,
            clawback_rate=0.2, termination_threshold=10,
        )
        self.assertEqual(result.net_price, 72)
        self.assertTrue(result.terminated)

    def test_adaptive_evidence_uses_supplied_information_value(self) -> None:
        self.assertEqual(
            choose_adaptive_evidence_action(state="uncertain", information_value=5, stop_threshold=10).action,
            "stop",
        )
        self.assertEqual(
            choose_adaptive_evidence_action(state="none", information_value=0, stop_threshold=1).action,
            "stop",
        )

    def test_portfolio_spillover_is_separate(self) -> None:
        result = evaluate_portfolio_spillover(local_value=5, global_value=20, payer_share=0.25)
        self.assertEqual(result.global_value, 20)
        self.assertEqual(evaluate_portfolio_spillover(local_value=0, global_value=0, payer_share=0).global_value, 0)

    def test_extensions_fail_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "aligned"):
            evaluate_distributional_equity((1,), (1, 2))
        with self.assertRaisesRegex(ValueError, "at most"):
            settle_managed_entry(list_price=1, rebate_rate=2, monitoring_passed=True)


if __name__ == "__main__":
    unittest.main()
