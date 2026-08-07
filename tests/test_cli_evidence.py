import io
import json
import unittest
from contextlib import redirect_stdout

from reimbursement_game.cli import main, _record_selection

PACKET = "fixtures/evidence/synthetic-chapter7-parameter-packet-v1.json"


class EvidenceCliTests(unittest.TestCase):
    def test_evidence_summary_is_explicitly_not_for_decision_use(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["evidence", PACKET]), 0)
        value = json.loads(output.getvalue())
        self.assertFalse(value["decision_use_permitted"])
        self.assertEqual(value["packet_id"], "synthetic-chapter7-non-empirical")
        self.assertEqual(len(value["records"]), 9)

    def test_calibrate_outputs_receipt_and_voiage_handoff(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            status = main(
                [
                    "calibrate",
                    PACKET,
                    "scenario_3",
                    "120",
                    "20",
                    "--case-id",
                    "cli-synthetic-s3",
                    "--record",
                    "n=n-allocative",
                    "--record",
                    "m=m-contraction",
                    "--record",
                    "d=d-displacement",
                ]
            )
        self.assertEqual(status, 0)
        value = json.loads(output.getvalue())
        self.assertEqual(value["evaluation"]["scenario"], "scenario_3")
        self.assertTrue(value["receipt"]["synthetic"])
        self.assertFalse(value["receipt"]["decision_use_permitted"])
        self.assertEqual(value["voiage_handoff"]["sample_count"], 2)

    def test_duplicate_role_selection_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate"):
            main(
                [
                    "calibrate",
                    PACKET,
                    "scenario_1",
                    "120",
                    "20",
                    "--case-id",
                    "duplicate",
                    "--record",
                    "n=n-allocative",
                    "--record",
                    "n=n-efficient",
                ]
            )

    def test_unsupported_evidence_role_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported evidence role: invalid_role"):
            _record_selection(["invalid_role=foo"])


if __name__ == "__main__":
    unittest.main()
