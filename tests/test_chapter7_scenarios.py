import csv
import json
import math
import unittest
from pathlib import Path

from reimbursement_game.case_io import _required_number, chapter7_inputs_from_case
from reimbursement_game.chapter7 import (
    Scenario1Inputs,
    Scenario2Inputs,
    Scenario3Inputs,
    Scenario4Inputs,
    evaluate_chapter7_scenario,
)


class Chapter7ScenarioTests(unittest.TestCase):
    def test_shared_all_scenario_fixture(self) -> None:
        fixture = Path("fixtures/conformance/chapter7-scenarios-v1.csv")
        with fixture.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len(rows), 4)
        for row in rows:
            with self.subTest(case_id=row["case_id"]):
                inputs = self._inputs(row)
                result = evaluate_chapter7_scenario(inputs)
                self.assertEqual(row["scenario"], result.scenario)
                self.assertTrue(result.adoption_required)
                for field in (
                    "iper",
                    "reimbursement_health_effect",
                    "alternative_health_gain",
                    "nebh",
                    "beta",
                    "evci",
                    "net_financial_cost",
                ):
                    self.assertTrue(
                        math.isclose(
                            getattr(result, field),
                            float(row[f"expected_{field}"]),
                            rel_tol=1e-12,
                            abs_tol=1e-10,
                        ),
                        field,
                    )
                self.assertEqual(result.economically_preferred, result.nebh >= -result.tolerance)

    def test_source_domains_fail_closed(self) -> None:
        invalid = (
            Scenario1Inputs(1, 1, expansion_icer=math.nan, evidence_revision="source"),
            Scenario2Inputs(
                1,
                1,
                expansion_icer=20,
                contraction_icer=21,
                displacement_icer=20,
                evidence_revision="source",
            ),
            Scenario3Inputs(
                1,
                1,
                expansion_icer=30,
                contraction_icer=20,
                displacement_icer=25,
                evidence_revision="source",
            ),
            Scenario3Inputs(
                1,
                1,
                expansion_icer=20,
                contraction_icer=60,
                displacement_icer=70,
                evidence_revision="source",
            ),
            Scenario4Inputs(
                100,
                1,
                contraction_icer=50,
                displacement_icer=40,
                investment_icer=60,
                present_value_multiplier=2,
                annual_program_health_effect=100 / 60 / 2,
                evidence_revision="source",
            ),
            Scenario4Inputs(
                100,
                1,
                contraction_icer=100,
                displacement_icer=50,
                investment_icer=25,
                present_value_multiplier=2,
                annual_program_health_effect=3,
                evidence_revision="source",
            ),
        )
        for inputs in invalid:
            with self.subTest(inputs=inputs):
                with self.assertRaises(ValueError):
                    evaluate_chapter7_scenario(inputs)

    def test_shared_invalid_scenario_fixture(self) -> None:
        fixture = Path("fixtures/conformance/chapter7-scenarios-invalid-v1.csv")
        with fixture.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len(rows), 8)
        for row in rows:
            with self.subTest(case_id=row["case_id"]):
                with self.assertRaises(ValueError):
                    evaluate_chapter7_scenario(self._inputs(row))

    def test_scenario_four_requires_dynamic_provenance(self) -> None:
        with self.assertRaisesRegex(ValueError, "evidence_revision"):
            evaluate_chapter7_scenario(
                Scenario4Inputs(
                    200_000,
                    10,
                    contraction_icer=100_000,
                    displacement_icer=50_000,
                    investment_icer=25_000,
                    present_value_multiplier=2,
                    annual_program_health_effect=4,
                    evidence_revision="",
                )
            )

    def test_scenario_four_preserves_dynamic_provenance(self) -> None:
        result = evaluate_chapter7_scenario(
            Scenario4Inputs(
                200_000,
                10,
                contraction_icer=100_000,
                displacement_icer=50_000,
                investment_icer=25_000,
                present_value_multiplier=2,
                annual_program_health_effect=4,
                evidence_revision="reviewed-parameter-packet-sha256",
            )
        )
        self.assertEqual(result.evidence_revision, "reviewed-parameter-packet-sha256")

    def test_parser_rejects_scenario_incompatible_fields(self) -> None:
        case = json.loads(
            Path("examples/cases/chapter7_scenario2.json").read_text(encoding="utf-8")
        )
        case["investment_icer"] = 25_000
        with self.assertRaisesRegex(ValueError, "scenario-incompatible"):
            chapter7_inputs_from_case(case)

        del case["investment_icer"]
        case["incremental_cost"] = "200000"
        with self.assertRaisesRegex(ValueError, "JSON number"):
            chapter7_inputs_from_case(case)

        case["incremental_cost"] = 200_000
        case["schema_version"] = True
        with self.assertRaisesRegex(ValueError, "schema_version 1"):
            chapter7_inputs_from_case(case)

    def test_required_number_missing_field(self) -> None:
        with self.assertRaises(KeyError):
            _required_number({}, "missing_field")

    def test_schema_scenario_one_forbids_dynamic_fields(self) -> None:
        schema = json.loads(
            Path("schemas/pekarsky-chapter7-scenario.schema.json").read_text(encoding="utf-8")
        )
        forbidden = {
            item["required"][0] for item in schema["oneOf"][0]["not"]["anyOf"]
        }
        self.assertTrue(
            {
                "contraction_icer",
                "displacement_icer",
                "investment_icer",
                "present_value_multiplier",
                "annual_program_health_effect",
            }
            <= forbidden
        )

    def test_currency_rescaling_does_not_change_economic_preference(self) -> None:
        baseline = evaluate_chapter7_scenario(
            Scenario1Inputs(110, 1, expansion_icer=100, evidence_revision="source")
        )
        scaled = evaluate_chapter7_scenario(
            Scenario1Inputs(110e12, 1, expansion_icer=100e12, evidence_revision="source")
        )
        self.assertFalse(baseline.economically_preferred)
        self.assertFalse(scaled.economically_preferred)
        self.assertAlmostEqual(baseline.nebh, scaled.nebh)

    def test_health_unit_rescaling_does_not_change_economic_preference(self) -> None:
        baseline = evaluate_chapter7_scenario(
            Scenario1Inputs(
                1.0001e-7,
                1e-9,
                expansion_icer=100,
                evidence_revision="source",
            )
        )
        scaled = evaluate_chapter7_scenario(
            Scenario1Inputs(
                1.0001e-7,
                1e-3,
                expansion_icer=1e-4,
                evidence_revision="source",
            )
        )
        self.assertFalse(baseline.economically_preferred)
        self.assertFalse(scaled.economically_preferred)

    def test_tiny_scenario_two_equality_is_currency_scale_invariant(self) -> None:
        baseline = Scenario2Inputs(
            1e-13,
            1,
            expansion_icer=1e-13,
            contraction_icer=2e-13,
            displacement_icer=1e-13,
            evidence_revision="source",
        )
        scaled = Scenario2Inputs(
            0.1,
            1,
            expansion_icer=0.1,
            contraction_icer=0.2,
            displacement_icer=0.1,
            evidence_revision="source",
        )
        for inputs in (baseline, scaled):
            with self.assertRaisesRegex(ValueError, "n = m"):
                evaluate_chapter7_scenario(inputs)

    def test_all_versioned_examples_parse_and_evaluate(self) -> None:
        for scenario in range(1, 5):
            path = Path(f"examples/cases/chapter7_scenario{scenario}.json")
            case = json.loads(path.read_text(encoding="utf-8"))
            result = evaluate_chapter7_scenario(chapter7_inputs_from_case(case))
            self.assertEqual(result.scenario, f"scenario_{scenario}")
            self.assertEqual(result.evidence_revision, case["evidence_revision"])

    @staticmethod
    def _inputs(row: dict[str, str]) -> object:
        common = (float(row["incremental_cost"]), float(row["incremental_health_effect"]))
        if row["scenario"] == "scenario_1":
            return Scenario1Inputs(
                *common,
                expansion_icer=float(row["n"]),
                evidence_revision=(
                    row["evidence_revision"]
                    if "evidence_revision" in row
                    else "synthetic-fixture-v1"
                ),
            )
        if row["scenario"] == "scenario_2":
            return Scenario2Inputs(
                *common,
                expansion_icer=float(row["n"]),
                contraction_icer=float(row["m"]),
                displacement_icer=float(row["d"]),
                evidence_revision=(
                    row["evidence_revision"]
                    if "evidence_revision" in row
                    else "synthetic-fixture-v1"
                ),
            )
        if row["scenario"] == "scenario_3":
            return Scenario3Inputs(
                *common,
                expansion_icer=float(row["n"]),
                contraction_icer=float(row["m"]),
                displacement_icer=float(row["d"]),
                evidence_revision=(
                    row["evidence_revision"]
                    if "evidence_revision" in row
                    else "synthetic-fixture-v1"
                ),
            )
        return Scenario4Inputs(
            *common,
            contraction_icer=float(row["m"]),
            displacement_icer=float(row["d"]),
            investment_icer=float(row["mu"]),
            present_value_multiplier=float(row["phi"]),
            annual_program_health_effect=float(row["annual_program_health_effect"]),
            evidence_revision=(
                "synthetic-fixture-v1"
                if row.get("evidence_revision") is None
                else row["evidence_revision"]
            ),
        )


if __name__ == "__main__":
    unittest.main()
