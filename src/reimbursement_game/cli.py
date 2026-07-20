"""Command-line interface."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
from typing import Any

from .adapters.kairos import KairosScenarioExporter
from .adapters.uogto import UogtoExporter
from .case_io import inputs_from_case
from .chapter8 import solve_revealed_threshold_game
from .economics import evaluate_reimbursement


def _load(path: str) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("case file must contain a JSON object")
    return value


def _print(value: object) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ndr-game")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("evaluate", "equilibrium", "uogto", "kairos"):
        command = sub.add_parser(name)
        command.add_argument("case")
    args = parser.parse_args(argv)
    case = _load(args.case)
    if args.command == "evaluate":
        _print(asdict(evaluate_reimbursement(inputs_from_case(case))))
    elif args.command == "equilibrium":
        inputs = inputs_from_case(case)
        result = solve_revealed_threshold_game(
            incremental_health_effect=inputs.incremental_health_effect,
            context=inputs.context,
            opportunities=inputs.opportunities,
            marginal_cost_per_health_effect=float(
                case.get("marginal_cost_per_health_effect", 0.0)
            ),
        )
        _print(asdict(result))
    elif args.command == "uogto":
        _print(UogtoExporter().export_game(case))
    elif args.command == "kairos":
        events = [
            {"kind": "firm_sets_price", "time": 0, "payload": {"case_id": case.get("case_id")}},
            {"kind": "institution_decides", "time": 1, "payload": {}},
        ]
        _print(KairosScenarioExporter().export_scenario(events))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
