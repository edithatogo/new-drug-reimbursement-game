import csv
import unittest
from pathlib import Path

from reimbursement_game.chapter8 import solve_pekarsky_game1, solve_revealed_threshold_game
from reimbursement_game.economics import EconomicContext, OpportunitySet


class Chapter8Tests(unittest.TestCase):
    def test_firm_offers_at_threshold(self) -> None:
        opportunities = OpportunitySet(
            expansion_icer=20_000,
            contraction_icer=60_000,
            displacement_icer=40_000,
        )
        result = solve_pekarsky_game1(
            incremental_health_effect=10,
            context=EconomicContext.FIXED,
            opportunities=opportunities,
        )
        self.assertTrue(result.reimbursed)
        self.assertAlmostEqual(result.offered_iper or 0, result.health_shadow_price)
        self.assertAlmostEqual(result.institution_nebh, 0.0, places=10)
        self.assertAlmostEqual(result.firm_economic_rent, result.health_shadow_price * 10)

    def test_no_trade_above_minimum_viable_price(self) -> None:
        opportunities = OpportunitySet(displacement_icer=20_000)
        result = solve_revealed_threshold_game(
            incremental_health_effect=1,
            context=EconomicContext.FIXED,
            opportunities=opportunities,
            incremental_imer=30_000,
        )
        self.assertFalse(result.reimbursed)
        self.assertIsNone(result.offered_iper)

    def test_exact_game_rejects_non_source_contexts(self) -> None:
        cases = (
            (
                EconomicContext.EXPANDABLE,
                OpportunitySet(expansion_icer=20_000),
                "fixed budget",
            ),
            (
                EconomicContext.FIXED,
                OpportunitySet(
                    expansion_icer=60_000,
                    contraction_icer=20_000,
                    displacement_icer=40_000,
                ),
                "m > n",
            ),
            (
                EconomicContext.FIXED,
                OpportunitySet(
                    expansion_icer=20_000,
                    contraction_icer=60_000,
                    displacement_icer=70_000,
                ),
                "n <= d <= m",
            ),
        )
        for context, opportunities, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    solve_pekarsky_game1(
                        incremental_health_effect=1,
                        context=context,
                        opportunities=opportunities,
                    )

    def test_generalized_nonzero_imer_is_explicit_extension(self) -> None:
        opportunities = OpportunitySet(
            expansion_icer=20_000,
            contraction_icer=60_000,
            displacement_icer=40_000,
        )
        result = solve_revealed_threshold_game(
            incremental_health_effect=10,
            context=EconomicContext.FIXED,
            opportunities=opportunities,
            incremental_imer=5_000,
        )
        self.assertAlmostEqual(
            result.firm_economic_rent,
            (result.health_shadow_price - 5_000) * 10,
        )

    def test_versioned_game1_conformance_fixture(self) -> None:
        fixture = Path("fixtures/conformance/chapter8-game1-v1.csv")
        with fixture.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        self.assertGreater(len(rows), 0)
        for row in rows:
            with self.subTest(case_id=row["case_id"]):
                self.assertEqual(row["schema_version"], "1")
                result = solve_pekarsky_game1(
                    incremental_health_effect=float(row["incremental_health_effect"]),
                    context=EconomicContext.FIXED,
                    opportunities=OpportunitySet(
                        expansion_icer=float(row["expansion_icer"]),
                        contraction_icer=float(row["contraction_icer"]),
                        displacement_icer=float(row["displacement_icer"]),
                    ),
                )
                self.assertAlmostEqual(result.offered_iper or 0, float(row["expected_price"]))
                self.assertAlmostEqual(
                    result.firm_economic_rent,
                    float(row["expected_firm_rent"]),
                )
                self.assertAlmostEqual(result.institution_nebh, float(row["expected_nebh"]))


if __name__ == "__main__":
    unittest.main()
