import json
import unittest
from pathlib import Path

from reimbursement_game.reference_game import solve_game


class ReferenceGameTests(unittest.TestCase):
    def test_fixture(self) -> None:
        spec = json.loads(Path("examples/games/perfect_information_game.json").read_text())
        result = solve_game(spec)
        self.assertEqual(result.choices["institution_decision"], "reimburse")
        self.assertEqual(result.payoffs["institution"], 1.0)

    def test_non_finite_probability_fails_closed(self) -> None:
        spec = {
            "root": "chance",
            "nodes": {
                "chance": {
                    "kind": "chance",
                    "edges": [{"probability": float("nan"), "target": "end"}],
                },
                "end": {"kind": "terminal", "payoffs": {"player": 1}},
            },
        }
        with self.assertRaisesRegex(ValueError, "probabilities must be finite"):
            solve_game(spec)

    def test_non_finite_payoff_fails_closed(self) -> None:
        spec = {
            "root": "end",
            "nodes": {"end": {"kind": "terminal", "payoffs": {"player": float("nan")}}},
        }
        with self.assertRaisesRegex(ValueError, "payoffs must be finite"):
            solve_game(spec)


if __name__ == "__main__":
    unittest.main()
