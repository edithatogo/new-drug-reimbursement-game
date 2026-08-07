import io
import json
import unittest
from contextlib import redirect_stdout

from reimbursement_game.cli import main

CHAPTER8_CASE = "examples/cases/chapter8_example.json"
CHAPTER7_CASE = "examples/cases/chapter7_scenario1.json"
PILOT_DOSSIER = "fixtures/evidence/nhs-england-methodological-candidates-v1.json"

class CliTests(unittest.TestCase):
    def test_evaluate_command(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["evaluate", CHAPTER8_CASE]), 0)
        value = json.loads(output.getvalue())
        self.assertIn("net_economic_benefit_health", value)
        self.assertIn("reimburse", value)

    def test_scenario_command(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["scenario", CHAPTER7_CASE]), 0)
        value = json.loads(output.getvalue())
        self.assertIn("case_id", value)
        self.assertIn("currency_unit", value)
        self.assertIn("health_unit", value)
        self.assertIn("case_evidence_revision", value)

    def test_equilibrium_command(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["equilibrium", CHAPTER8_CASE]), 0)
        value = json.loads(output.getvalue())
        self.assertIn("offered_iper", value)
        self.assertIn("firm_economic_rent", value)

    def test_uogto_command(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["uogto", CHAPTER8_CASE]), 0)
        value = json.loads(output.getvalue())
        self.assertIn("uogto:GameInstance", value.get("@type", []))

    def test_kairos_command(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["kairos", CHAPTER8_CASE]), 0)
        value = json.loads(output.getvalue())
        self.assertIn("events", value)

    def test_pilot_readiness_command(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["pilot-readiness", PILOT_DOSSIER]), 0)
        value = json.loads(output.getvalue())
        self.assertIn("dossier_id", value)
        self.assertIn("approved_calibration_permitted", value)
        self.assertFalse(value["approved_calibration_permitted"])

if __name__ == "__main__":
    unittest.main()
