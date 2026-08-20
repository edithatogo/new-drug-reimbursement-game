"""Command-line interface."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .adapters.kairos import KairosScenarioExporter
from .adapters.reimbursement_atlas import ReimbursementAtlasParameterExport
from .adapters.uogto import UogtoExporter
from .calibration import calibrate_chapter7_scenario
from .case_io import chapter7_inputs_from_case, inputs_from_case
from .chapter7 import Chapter7Scenario, evaluate_chapter7_scenario
from .chapter8 import solve_pekarsky_game1
from .economics import evaluate_reimbursement
from .evidence import ParameterRole
from .pilot_readiness import assess_pilot_readiness, candidate_dossier_from_mapping
from .sweeps import generate_all_figures


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
    for name in ("evaluate", "scenario", "equilibrium", "uogto", "kairos"):
        command = sub.add_parser(name)
        command.add_argument("case")
    sweep_command = sub.add_parser("sweep", help="generate scenario sweep figures")
    sweep_command.add_argument("--output-dir", default="docs/figures", help="target figure output directory")
    evidence_command = sub.add_parser("evidence")
    evidence_command.add_argument("packet")
    readiness_command = sub.add_parser("pilot-readiness")
    readiness_command.add_argument("dossier")
    calibration_command = sub.add_parser("calibrate")
    calibration_command.add_argument("packet")
    calibration_command.add_argument("scenario", choices=[item.value for item in Chapter7Scenario])
    calibration_command.add_argument("incremental_cost", type=float)
    calibration_command.add_argument("incremental_health_effect", type=float)
    calibration_command.add_argument("--case-id", required=True)
    calibration_command.add_argument(
        "--record",
        action="append",
        default=[],
        metavar="ROLE=RECORD_ID",
        help="select exactly one approved evidence record for each required role",
    )
    args = parser.parse_args(argv)
    if args.command == "sweep":
        output_dir = Path(args.output_dir)
        paths = generate_all_figures(output_dir)
        _print(
            {
                "status": "success",
                "output_dir": str(output_dir),
                "generated_figures": [str(path) for path in paths],
            }
        )
        return 0
    if args.command == "pilot-readiness":
        dossier = candidate_dossier_from_mapping(_load(args.dossier))
        _print(asdict(assess_pilot_readiness(dossier)))
        return 0
    if args.command == "evidence":
        packet = ReimbursementAtlasParameterExport(args.packet).packet()
        _print(
            {
                "packet_id": packet.packet_id,
                "packet_revision": packet.packet_revision,
                "context": asdict(packet.context),
                "records": [
                    {
                        "record_id": record.record_id,
                        "role": record.role,
                        "evidence_revision": record.evidence_revision,
                        "uncertainty_kind": record.uncertainty_kind,
                        "sample_count": len(record.samples),
                    }
                    for record in packet.records
                ],
                "decision_use_permitted": False,
            }
        )
        return 0
    if args.command == "calibrate":
        packet = ReimbursementAtlasParameterExport(args.packet).packet()
        calibrated = calibrate_chapter7_scenario(
            case_id=args.case_id,
            scenario=Chapter7Scenario(args.scenario),
            incremental_cost=args.incremental_cost,
            incremental_health_effect=args.incremental_health_effect,
            packet=packet,
            record_ids=_record_selection(args.record),
        )
        _print(
            {
                "evaluation": asdict(calibrated.evaluation),
                "receipt": asdict(calibrated.receipt),
                "voiage_handoff": {
                    "strategy_names": calibrated.voiage_samples.strategy_names,
                    "sample_count": len(calibrated.voiage_samples.net_benefit_samples),
                    "parameter_roles": [
                        item.role for item in calibrated.voiage_samples.parameter_samples
                    ],
                    "perspective": calibrated.voiage_samples.perspective,
                    "health_unit": calibrated.voiage_samples.health_unit,
                    "evidence_revision": calibrated.voiage_samples.evidence_revision,
                },
            }
        )
        return 0
    case = _load(args.case)
    if args.command == "evaluate":
        _print(asdict(evaluate_reimbursement(inputs_from_case(case))))
    elif args.command == "scenario":
        output = asdict(evaluate_chapter7_scenario(chapter7_inputs_from_case(case)))
        output.update(
            {
                "case_id": case["case_id"],
                "currency_unit": case["currency_unit"],
                "health_unit": case["health_unit"],
                "case_evidence_revision": case["evidence_revision"],
            }
        )
        _print(output)
    elif args.command == "equilibrium":
        inputs = inputs_from_case(case)
        result = solve_pekarsky_game1(
            incremental_health_effect=inputs.incremental_health_effect,
            context=inputs.context,
            opportunities=inputs.opportunities,
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


def _record_selection(values: list[str]) -> dict[ParameterRole, str]:
    selection: dict[ParameterRole, str] = {}
    for value in values:
        role_value, separator, record_id = value.partition("=")
        if not separator or not record_id.strip():
            raise ValueError("--record must use ROLE=RECORD_ID format")
        try:
            role = ParameterRole(role_value)
        except ValueError as exc:
            raise ValueError(f"unsupported evidence role: {role_value}") from exc
        if role in selection:
            raise ValueError(f"duplicate evidence role selection: {role.value}")
        selection[role] = record_id
    return selection


if __name__ == "__main__":
    raise SystemExit(main())
