import json
import unittest
from dataclasses import replace
from pathlib import Path
from typing import Any

from reimbursement_game.calibration import calibrate_chapter7_scenario
from reimbursement_game.chapter7 import Chapter7Scenario
from reimbursement_game.evidence import ParameterRole, evidence_packet_from_mapping

FIXTURE = Path("fixtures/evidence/synthetic-chapter7-parameter-packet-v1.json")


def packet():  # type: ignore[no-untyped-def]
    value: Any = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return evidence_packet_from_mapping(value)


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


class CalibrationTests(unittest.TestCase):
    def test_assembles_all_four_scenarios_with_receipts_and_samples(self) -> None:
        for scenario, selection in SELECTIONS.items():
            with self.subTest(scenario=scenario):
                result = calibrate_chapter7_scenario(
                    case_id=f"synthetic-{scenario.value}",
                    scenario=scenario,
                    incremental_cost=120.0,
                    incremental_health_effect=20.0,
                    packet=packet(),
                    record_ids=selection,
                )
                self.assertEqual(result.evaluation.scenario, scenario)
                self.assertTrue(result.receipt.evidence_revision.startswith("sha256:"))
                self.assertEqual(result.receipt.sample_count, 2)
                self.assertTrue(result.receipt.synthetic)
                self.assertFalse(result.receipt.decision_use_permitted)
                self.assertEqual(len(result.voiage_samples.net_benefit_samples), 2)
                self.assertEqual(
                    result.voiage_samples.strategy_names,
                    ("reimburse", "best_available_alternative"),
                )

    def test_receipt_revision_is_deterministic_and_input_bound(self) -> None:
        arguments = dict(
            case_id="synthetic-s3",
            scenario=Chapter7Scenario.FIXED_ALLOCATIVE_INEFFICIENCY,
            incremental_cost=120.0,
            incremental_health_effect=20.0,
            packet=packet(),
            record_ids=SELECTIONS[Chapter7Scenario.FIXED_ALLOCATIVE_INEFFICIENCY],
        )
        first = calibrate_chapter7_scenario(**arguments)
        second = calibrate_chapter7_scenario(**arguments)
        changed = calibrate_chapter7_scenario(**(arguments | {"incremental_health_effect": 21.0}))
        self.assertEqual(first.receipt.evidence_revision, second.receipt.evidence_revision)
        self.assertNotEqual(first.receipt.evidence_revision, changed.receipt.evidence_revision)

    def test_rejects_missing_duplicate_role_or_wrong_programme_evidence(self) -> None:
        with self.assertRaisesRegex(ValueError, "selection mismatch"):
            calibrate_chapter7_scenario(
                case_id="missing",
                scenario=Chapter7Scenario.FIXED_EFFICIENT,
                incremental_cost=120,
                incremental_health_effect=20,
                packet=packet(),
                record_ids={ParameterRole.EXPANSION_ICER: "n-efficient"},
            )
        wrong_role = dict(SELECTIONS[Chapter7Scenario.FIXED_EFFICIENT])
        wrong_role[ParameterRole.EXPANSION_ICER] = "d-displacement"
        with self.assertRaisesRegex(ValueError, "has role d"):
            calibrate_chapter7_scenario(
                case_id="wrong-role",
                scenario=Chapter7Scenario.FIXED_EFFICIENT,
                incremental_cost=120,
                incremental_health_effect=20,
                packet=packet(),
                record_ids=wrong_role,
            )
        evidence = packet()
        records = tuple(
            replace(record, programme_id="different-programme")
            if record.role is ParameterRole.HORIZON
            else record
            for record in evidence.records
        )
        with self.assertRaisesRegex(ValueError, "one programme"):
            calibrate_chapter7_scenario(
                case_id="wrong-programme",
                scenario=Chapter7Scenario.FIXED_TECHNICAL_INVESTMENT,
                incremental_cost=120,
                incremental_health_effect=20,
                packet=replace(evidence, records=records),
                record_ids=SELECTIONS[Chapter7Scenario.FIXED_TECHNICAL_INVESTMENT],
            )

    def test_rejects_unaligned_uncertainty_and_invalid_draw_domains(self) -> None:
        evidence = packet()
        records = tuple(
            replace(record, samples=(10.0, 11.0, 12.0))
            if record.record_id == "d-displacement"
            else record
            for record in evidence.records
        )
        with self.assertRaisesRegex(ValueError, "aligned"):
            calibrate_chapter7_scenario(
                case_id="unaligned",
                scenario=Chapter7Scenario.FIXED_ALLOCATIVE_INEFFICIENCY,
                incremental_cost=120,
                incremental_health_effect=20,
                packet=replace(evidence, records=records),
                record_ids=SELECTIONS[Chapter7Scenario.FIXED_ALLOCATIVE_INEFFICIENCY],
            )
        invalid_draws = tuple(
            replace(record, samples=(5.0, 13.0))
            if record.record_id == "n-allocative"
            else record
            for record in evidence.records
        )
        with self.assertRaisesRegex(ValueError, "m > n"):
            calibrate_chapter7_scenario(
                case_id="domain-failure",
                scenario=Chapter7Scenario.FIXED_ALLOCATIVE_INEFFICIENCY,
                incremental_cost=120,
                incremental_health_effect=20,
                packet=replace(evidence, records=invalid_draws),
                record_ids=SELECTIONS[Chapter7Scenario.FIXED_ALLOCATIVE_INEFFICIENCY],
            )


if __name__ == "__main__":
    unittest.main()
