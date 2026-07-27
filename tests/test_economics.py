import math
import unittest

from reimbursement_game.economics import (
    AlternativeStrategy,
    EconomicContext,
    OpportunitySet,
    ReimbursementInputs,
    evaluate_reimbursement,
    health_shadow_price,
)


class EconomicsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.opportunities = OpportunitySet(
            expansion_icer=20_000.0,
            contraction_icer=60_000.0,
            displacement_icer=40_000.0,
        )

    def test_chapter_seven_shadow_price_identity(self) -> None:
        beta, binding = health_shadow_price(EconomicContext.FIXED, self.opportunities)
        expected = 1.0 / (1.0 / 40_000.0 + 1.0 / 20_000.0 - 1.0 / 60_000.0)
        self.assertAlmostEqual(beta, expected)
        self.assertEqual(binding, "reallocate_from_m_to_n")

    def test_threshold_yields_zero_nebh(self) -> None:
        beta, _ = health_shadow_price(EconomicContext.FIXED, self.opportunities)
        effect = 10.0
        result = evaluate_reimbursement(
            ReimbursementInputs(
                incremental_cost=beta * effect,
                incremental_health_effect=effect,
                context=EconomicContext.FIXED,
                opportunities=self.opportunities,
            )
        )
        self.assertAlmostEqual(result.net_economic_benefit_health, 0.0, places=10)
        self.assertTrue(result.reimburse)

    def test_price_below_shadow_price_is_positive(self) -> None:
        beta, _ = health_shadow_price(EconomicContext.FIXED, self.opportunities)
        result = evaluate_reimbursement(
            ReimbursementInputs(
                incremental_cost=beta * 0.8 * 10.0,
                incremental_health_effect=10.0,
                context=EconomicContext.FIXED,
                opportunities=self.opportunities,
            )
        )
        self.assertGreater(result.net_economic_benefit_health, 0.0)

    def test_price_above_shadow_price_is_negative(self) -> None:
        beta, _ = health_shadow_price(EconomicContext.FIXED, self.opportunities)
        result = evaluate_reimbursement(
            ReimbursementInputs(
                incremental_cost=beta * 1.2 * 10.0,
                incremental_health_effect=10.0,
                context=EconomicContext.FIXED,
                opportunities=self.opportunities,
            )
        )
        self.assertLess(result.net_economic_benefit_health, 0.0)
        self.assertFalse(result.reimburse)

    def test_currency_unit_rescaling_preserves_health_result(self) -> None:
        beta, _ = health_shadow_price(EconomicContext.FIXED, self.opportunities)
        baseline = evaluate_reimbursement(
            ReimbursementInputs(
                incremental_cost=beta * 10.0,
                incremental_health_effect=10.0,
                context=EconomicContext.FIXED,
                opportunities=self.opportunities,
            )
        )
        scale = 100.0
        rescaled_opportunities = OpportunitySet(
            expansion_icer=self.opportunities.expansion_icer * scale,
            contraction_icer=self.opportunities.contraction_icer * scale,
            displacement_icer=self.opportunities.displacement_icer * scale,
        )
        rescaled = evaluate_reimbursement(
            ReimbursementInputs(
                incremental_cost=beta * scale * 10.0,
                incremental_health_effect=10.0,
                context=EconomicContext.FIXED,
                opportunities=rescaled_opportunities,
            )
        )
        self.assertAlmostEqual(rescaled.net_economic_benefit_health, baseline.net_economic_benefit_health)
        self.assertAlmostEqual(rescaled.health_shadow_price, baseline.health_shadow_price * scale)

    def test_non_identifiable_context_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "opportunity cost"):
            health_shadow_price(EconomicContext.EXPANDABLE, OpportunitySet())

    def test_efficient_fixed_budget_reduces_to_d(self) -> None:
        opportunities = OpportunitySet(
            expansion_icer=30_000.0,
            contraction_icer=30_000.0,
            displacement_icer=45_000.0,
        )
        beta, _ = health_shadow_price(EconomicContext.FIXED, opportunities)
        self.assertAlmostEqual(beta, 45_000.0)

    def test_optimal_displacement_reduces_to_n(self) -> None:
        opportunities = OpportunitySet(
            expansion_icer=25_000.0,
            contraction_icer=50_000.0,
            displacement_icer=50_000.0,
        )
        beta, _ = health_shadow_price(EconomicContext.FIXED, opportunities)
        self.assertAlmostEqual(beta, 25_000.0)

    def test_expandable_context_reduces_to_n(self) -> None:
        opportunities = OpportunitySet(expansion_icer=35_000.0)
        beta, binding = health_shadow_price(EconomicContext.EXPANDABLE, opportunities)
        self.assertAlmostEqual(beta, 35_000.0)
        self.assertEqual(binding, "expand_best_available_programme")

    def test_named_technical_alternative_can_bind(self) -> None:
        opportunities = OpportunitySet(
            displacement_icer=50_000.0,
            additional_alternatives=(
                AlternativeStrategy("technical_efficiency_project", 1 / 10_000.0, "synthetic"),
            ),
        )
        beta, binding = health_shadow_price(EconomicContext.FIXED, opportunities)
        self.assertAlmostEqual(beta, 1 / (1 / 50_000 + 1 / 10_000))
        self.assertEqual(binding, "technical_efficiency_project")
        self.assertTrue(math.isfinite(beta))


if __name__ == "__main__":
    unittest.main()
