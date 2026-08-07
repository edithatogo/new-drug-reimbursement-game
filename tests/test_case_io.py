import unittest
from reimbursement_game.case_io import inputs_from_case, chapter7_inputs_from_case
from reimbursement_game.economics import EconomicContext

class TestCaseIO(unittest.TestCase):
    def test_inputs_from_case_valid(self):
        case = {
            "incremental_cost": 100.0,
            "incremental_health_effect": 10.0,
            "context": "fixed",
            "opportunities": {
                "expansion_icer": 10.0,
                "contraction_icer": 20.0,
                "displacement_icer": 15.0,
                "additional_alternatives": [
                    {"name": "alt1", "health_gain_per_currency": 0.05, "provenance": "src1"}
                ]
            }
        }
        result = inputs_from_case(case)
        self.assertEqual(result.incremental_cost, 100.0)
        self.assertEqual(result.incremental_health_effect, 10.0)
        self.assertEqual(result.context, EconomicContext.FIXED)
        self.assertEqual(result.opportunities.expansion_icer, 10.0)
        self.assertEqual(result.opportunities.contraction_icer, 20.0)
        self.assertEqual(result.opportunities.displacement_icer, 15.0)

    def test_chapter7_inputs_from_case_valid(self):
        case = {
            "schema_version": 1,
            "model_kind": "pekarsky-2015-ch7",
            "case_id": "test_case",
            "currency_unit": "USD",
            "health_unit": "QALY",
            "evidence_revision": "rev1",
            "scenario": "scenario_1",
            "incremental_cost": 100.0,
            "incremental_health_effect": 10.0,
            "expansion_icer": 20.0,
        }
        result = chapter7_inputs_from_case(case)
        self.assertEqual(result.incremental_cost, 100.0)
        self.assertEqual(result.incremental_health_effect, 10.0)
        self.assertEqual(result.expansion_icer, 20.0)
        self.assertEqual(result.evidence_revision, "rev1")

if __name__ == '__main__':
    unittest.main()
