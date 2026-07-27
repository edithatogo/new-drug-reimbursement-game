"""Small Python conformance oracle for finite perfect-information games.

This module exists to test contracts while the Rust runtime is extracted. It is
not a replacement for the planned Rust game-theory capability.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class OracleResult:
    payoffs: dict[str, float]
    choices: dict[str, str]


def solve_game(spec: dict[str, Any]) -> OracleResult:
    nodes = spec["nodes"]
    choices: dict[str, str] = {}
    visiting: set[str] = set()

    def visit(node_id: str) -> dict[str, float]:
        if node_id in visiting:
            raise ValueError("game contains a cycle")
        visiting.add(node_id)
        node = nodes[node_id]
        kind = node["kind"]
        if kind == "terminal":
            result = {str(k): float(v) for k, v in node["payoffs"].items()}
            if any(not math.isfinite(value) for value in result.values()):
                raise ValueError("terminal payoffs must be finite")
        elif kind == "chance":
            result = {}
            total = 0.0
            for edge in node["edges"]:
                probability = float(edge["probability"])
                if not math.isfinite(probability):
                    raise ValueError("chance probabilities must be finite")
                total += probability
                child = visit(str(edge["target"]))
                for player, value in child.items():
                    result[player] = result.get(player, 0.0) + probability * value
            if abs(total - 1.0) > 1e-9:
                raise ValueError("chance probabilities must sum to one")
        elif kind == "decision":
            player = str(node["player"])
            candidates: list[tuple[float, str, dict[str, float]]] = []
            for edge in node["edges"]:
                child = visit(str(edge["target"]))
                candidates.append((child.get(player, 0.0), str(edge["action"]), child))
            if not candidates:
                raise ValueError("decision node has no actions")
            candidates.sort(key=lambda item: (-item[0], item[1]))
            _, action, result = candidates[0]
            choices[node_id] = action
        else:
            raise ValueError(f"unsupported node kind: {kind}")
        visiting.remove(node_id)
        return result

    return OracleResult(payoffs=visit(str(spec["root"])), choices=choices)
