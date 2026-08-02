#!/usr/bin/env python3
"""Build deterministic T13 public-evidence and synthetic-output artifacts."""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from reimbursement_game.calibration import calibrate_chapter7_scenario  # noqa: E402
from reimbursement_game.chapter7 import Chapter7Scenario  # noqa: E402
from reimbursement_game.evidence import (  # noqa: E402
    ParameterRole,
    evidence_packet_from_mapping,
)

TRACK = ROOT / "conductor/tracks/t13_empirical_calibration_20260802"
FIXTURE = ROOT / "fixtures/evidence/synthetic-chapter7-parameter-packet-v1.json"
INPUT_PATHS = (
    "conductor/tracks/t13_empirical_calibration_20260802/acquisition-run-2026-08-02.json",
    "conductor/tracks/t13_empirical_calibration_20260802/field-coverage-2026-08-02.json",
    "conductor/tracks/t13_empirical_calibration_20260802/grey-literature-receipt-2026-08-02.json",
    "conductor/tracks/t13_empirical_calibration_20260802/nhs-england-foi-submission-2026-08-02.json",
    "conductor/tracks/t13_empirical_calibration_20260802/source-inventory.json",
    "conductor/tracks/t13_empirical_calibration_20260802/receipts/atlas-v0.1.1-ta1121-negative-2026-08-02.json",
    "docs/governance/health-economist-approval.md",
    "docs/research/source-conformance-audit.md",
    "fixtures/evidence/synthetic-chapter7-parameter-packet-v1.json",
)
SELECTIONS = {
    Chapter7Scenario.EXPANDABLE_EFFICIENT: {
        ParameterRole.EXPANSION_ICER: "n-allocative"
    },
    Chapter7Scenario.FIXED_EFFICIENT: {
        ParameterRole.EXPANSION_ICER: "n-efficient",
        ParameterRole.CONTRACTION_ICER: "m-contraction",
        ParameterRole.DISPLACEMENT_ICER: "d-displacement",
    },
    Chapter7Scenario.FIXED_ALLOCATIVE_INEFFICIENCY: {
        ParameterRole.EXPANSION_ICER: "n-allocative",
        ParameterRole.CONTRACTION_ICER: "m-contraction",
        ParameterRole.DISPLACEMENT_ICER: "d-displacement",
    },
    Chapter7Scenario.FIXED_TECHNICAL_INVESTMENT: {
        ParameterRole.CONTRACTION_ICER: "m-contraction",
        ParameterRole.DISPLACEMENT_ICER: "d-displacement",
        ParameterRole.INVESTMENT_ICER: "mu-investment",
        ParameterRole.PRESENT_VALUE_MULTIPLIER: "phi-present-value",
        ParameterRole.ANNUAL_PROGRAM_HEALTH_EFFECT: "annual-program-effect",
        ParameterRole.HORIZON: "horizon",
        ParameterRole.DISCOUNT_RATE: "discount-rate",
    },
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def build_artifacts(reviewed_revision: str) -> dict[str, bytes]:
    if len(reviewed_revision) != 40 or any(char not in "0123456789abcdef" for char in reviewed_revision):
        raise ValueError("reviewed revision must be a 40-character lowercase Git commit")
    missing = [path for path in INPUT_PATHS if not (ROOT / path).is_file()]
    if missing:
        raise ValueError(f"T13 closeout inputs are missing: {missing}")

    freeze = {
        "schema": "t13-research-packet-freeze/v1",
        "repository": "edithatogo/new-drug-reimbursement-game",
        "reviewed_revision": reviewed_revision,
        "scope": "public context, synthetic conformance, and research-method controls only",
        "inputs": [
            {"path": path, "sha256": _sha256(ROOT / path)} for path in INPUT_PATHS
        ],
        "parameter_roles": {
            "publicly_supported_context": [
                "commissioner",
                "provider class",
                "programme budgeting category",
                "pathway position",
                "comparators",
                "implementation timing",
                "three-year national resource-impact horizon",
                "market-share assumptions",
            ],
            "not_identifiable": ["n", "m", "d", "mu", "phi", "annual_program_health_effect"],
            "method_only": ["discount_rate", "horizon"],
        },
        "price_year_disposition": "No programme-specific price year or confidential net price is available; no conversion is performed.",
        "external_gates": {
            "nhs_displacement_context": "pending_response",
            "atlas_approved_packet": "not_available_at_v0.1.1",
            "health_economist_research_methods": "satisfied",
            "empirical_promotion": "prohibited",
        },
        "invalidation": "Any changed input hash, evidence revision, source term, method decision, or repository target requires regeneration and review.",
    }

    packet = evidence_packet_from_mapping(json.loads(FIXTURE.read_text(encoding="utf-8")))
    scenarios: list[dict[str, Any]] = []
    for scenario, records in SELECTIONS.items():
        calibrated = calibrate_chapter7_scenario(
            case_id=f"t13-synthetic-{scenario.value}",
            scenario=scenario,
            incremental_cost=120.0,
            incremental_health_effect=20.0,
            packet=packet,
            record_ids=records,
        )
        scenarios.append(
            {
                "scenario": scenario.value,
                "classification": "synthetic_conformance_only",
                "evaluation": dataclasses.asdict(calibrated.evaluation),
                "calibration_receipt": dataclasses.asdict(calibrated.receipt),
                "voiage_sample_bundle": dataclasses.asdict(calibrated.voiage_samples),
            }
        )
    output = {
        "schema": "t13-constrained-research-output/v1",
        "reviewed_revision": reviewed_revision,
        "packet_freeze_sha256": hashlib.sha256(_json_bytes(freeze)).hexdigest(),
        "release_label": "synthetic_research_only",
        "decision_use_permitted": False,
        "empirical_calibration_activated": False,
        "public_context": {
            "technology_appraisal": "NICE TA1121",
            "intervention": "acoramidis",
            "comparators": ["tafamidis", "vutrisiran"],
            "commissioner": "NHS England",
            "programme_budgeting_category": "PBC 10X Problems of circulation",
            "pathway_position": "first line",
        },
        "scenarios": scenarios,
        "prohibited_claims": [
            "calibrated reimbursement result",
            "identified NHS displacement parameter",
            "payer recommendation",
            "HTA conclusion",
            "policy conclusion",
            "regulatory validation",
        ],
        "limitations": [
            "All numeric scenario inputs are synthetic fixtures.",
            "No approved Atlas TA1121 parameter packet is available.",
            "No authoritative separately displaced NHS programme or baseline unit is available.",
            "Commercial net prices are neither requested nor used.",
            "Scenario 4 remains a mathematical sensitivity and conformance case only.",
        ],
    }
    return {
        "packet-freeze-2026-08-03.json": _json_bytes(freeze),
        "constrained-research-output-2026-08-03.json": _json_bytes(output),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reviewed-revision", required=True)
    parser.add_argument("--output-dir", type=Path, default=TRACK)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    artifacts = build_artifacts(args.reviewed_revision)
    failures: list[str] = []
    for name, content in artifacts.items():
        path = args.output_dir / name
        if args.check:
            if not path.is_file() or path.read_bytes() != content:
                failures.append(str(path))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    if failures:
        print("T13 closeout artifacts are stale: " + ", ".join(failures))
        return 1
    print("T13 research closeout artifacts are current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
