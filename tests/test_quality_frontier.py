"""Deterministic property-style and contract checks for the economic core."""

from __future__ import annotations

import random
import unittest

from reimbursement_game.economics import (
    EconomicContext,
    OpportunitySet,
    ReimbursementInputs,
    evaluate_reimbursement,
    health_shadow_price,
)


class QualityFrontierTests(unittest.TestCase):
    """Bounded invariant and contract checks (seeded for reproducibility)."""

    def test_seeded_shadow_price_invariants(self) -> None:
        rng = random.Random(20260801)  # noqa: S311 - deterministic test data, not secrets
        for _ in range(128):
            expansion = rng.uniform(1_000.0, 200_000.0)
            contraction = rng.uniform(1_000.0, 200_000.0)
            displacement = rng.uniform(1_000.0, 200_000.0)
            opportunities = OpportunitySet(expansion, contraction, displacement)
            beta, binding = health_shadow_price(EconomicContext.FIXED, opportunities)
            self.assertGreater(beta, 0.0)
            self.assertEqual(binding, "reallocate_from_m_to_n" if expansion < contraction else None)
            effect = rng.uniform(0.01, 100.0)
            result = evaluate_reimbursement(
                ReimbursementInputs(beta * effect, effect, EconomicContext.FIXED, opportunities)
            )
            self.assertAlmostEqual(result.net_economic_benefit_health, 0.0, places=8)
            self.assertTrue(result.reimburse)

    def test_price_ordering_is_monotone_for_reimbursement_decision(self) -> None:
        opportunities = OpportunitySet(20_000.0, 60_000.0, 40_000.0)
        beta, _ = health_shadow_price(EconomicContext.FIXED, opportunities)
        decisions = []
        for multiplier in (0.25, 0.5, 0.75, 1.0, 1.25, 2.0):
            result = evaluate_reimbursement(
                ReimbursementInputs(beta * multiplier * 10.0, 10.0, EconomicContext.FIXED, opportunities)
            )
            decisions.append(result.reimburse)
        self.assertEqual(decisions, [True, True, True, True, False, False])

    def test_input_contract_rejects_missing_fixed_budget_displacement(self) -> None:
        with self.assertRaisesRegex(ValueError, "displacement_icer"):
            ReimbursementInputs(1.0, 1.0, EconomicContext.FIXED, OpportunitySet(expansion_icer=10_000.0))


if __name__ == "__main__":
    unittest.main()
