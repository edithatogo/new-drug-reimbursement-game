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

    def test_shared_descendants_are_solved_once(self) -> None:
        spec = {
            "root": "root",
            "nodes": {
                "root": {
                    "kind": "chance",
                    "edges": [
                        {"probability": 0.5, "target": "shared"},
                        {"probability": 0.5, "target": "shared"},
                    ],
                },
                "shared": {
                    "kind": "decision",
                    "player": "p",
                    "edges": [
                        {"action": "a", "target": "end-a"},
                        {"action": "b", "target": "end-b"},
                    ],
                },
                "end-a": {"kind": "terminal", "payoffs": {"p": 1}},
                "end-b": {"kind": "terminal", "payoffs": {"p": 0}},
            },
        }
        result = solve_game(spec)
        self.assertEqual(result.payoffs, {"p": 1.0})
        self.assertEqual(result.choices, {"shared": "a"})

    def test_replay_is_deterministic_and_ties_break_by_action(self) -> None:
        """Repeated solves must produce a stable, replayable conformance result."""
        spec = {
            "root": "decision",
            "nodes": {
                "decision": {
                    "kind": "decision",
                    "player": "institution",
                    "edges": [
                        {"action": "z-last", "target": "z"},
                        {"action": "a-first", "target": "a"},
                    ],
                },
                "z": {"kind": "terminal", "payoffs": {"institution": 1}},
                "a": {"kind": "terminal", "payoffs": {"institution": 1}},
            },
        }

        first = solve_game(spec)
        second = solve_game(spec)
        self.assertEqual(first, second)
        self.assertEqual(first.choices, {"decision": "a-first"})


if __name__ == "__main__":
    unittest.main()
