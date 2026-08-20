import io
import json
import unittest
from contextlib import redirect_stdout

from reimbursement_game.cli import main

CHAPTER8_CASE = "examples/cases/chapter8_example.json"
CHAPTER7_CASE = "examples/cases/chapter7_scenario1.json"
PACKET = "fixtures/evidence/synthetic-chapter7-parameter-packet-v1.json"

class CliTests(unittest.TestCase):
    def test_evaluate_command_outputs_expected_values(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["evaluate", CHAPTER8_CASE]), 0)
        value = json.loads(output.getvalue())
        self.assertAlmostEqual(value["net_economic_benefit_health"], -4.5833, places=3)
        self.assertAlmostEqual(value["economic_value_clinical_innovation"], 171428.57, places=1)
        self.assertFalse(value["reimburse"])

    def test_scenario_command_outputs_expected_values(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["scenario", CHAPTER7_CASE]), 0)
        value = json.loads(output.getvalue())
        self.assertEqual(value["scenario"], "scenario_1")
        self.assertAlmostEqual(value["nebh"], 2.0, places=1)
        self.assertTrue(value["economically_preferred"])
        self.assertEqual(value["case_id"], "synthetic-ch7-s1")

    def test_equilibrium_command_outputs_expected_values(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["equilibrium", CHAPTER8_CASE]), 0)
        value = json.loads(output.getvalue())
        self.assertAlmostEqual(value["offered_iper"], 17142.857, places=3)
        self.assertAlmostEqual(value["firm_economic_rent"], 171428.571, places=3)
        self.assertEqual(value["reason"], "firm chooses the highest reimbursable IPER")

    def test_uogto_command_outputs_expected_structure(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["uogto", CHAPTER8_CASE]), 0)
        value = json.loads(output.getvalue())
        self.assertEqual(value["@context"]["uogto"], "https://w3id.org/uogto/core#")
        self.assertEqual(value["@type"], ["uogto:GameInstance", "ndrg:NewDrugReimbursementGame"])

    def test_kairos_command_outputs_expected_events(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["kairos", CHAPTER8_CASE]), 0)
        value = json.loads(output.getvalue())
        self.assertEqual(len(value["events"]), 2)
        self.assertEqual(value["events"][0]["kind"], "firm_sets_price")
        self.assertEqual(value["events"][1]["kind"], "institution_decides")

    def test_calibrate_role_selection_failure(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            with self.assertRaisesRegex(ValueError, "unsupported evidence role: unknown"):
                main([
                    "calibrate",
                    PACKET,
                    "scenario_3",
                    "120",
                    "20",
                    "--case-id",
                    "cli-synthetic-s3",
                    "--record",
                    "unknown=123"
                ])

        with redirect_stdout(output):
            with self.assertRaisesRegex(ValueError, "--record must use ROLE=RECORD_ID format"):
                main([
                    "calibrate",
                    PACKET,
                    "scenario_3",
                    "120",
                    "20",
                    "--case-id",
                    "cli-synthetic-s3",
                    "--record",
                    "invalid-format"
                ])


if __name__ == "__main__":
    unittest.main()
