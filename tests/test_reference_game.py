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


if __name__ == "__main__":
    unittest.main()
