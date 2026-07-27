import json
import tempfile
import unittest
from pathlib import Path

from reimbursement_game.adapters.kairos import KairosScenarioExporter
from reimbursement_game.adapters.reimbursement_atlas import ReimbursementAtlasExport
from reimbursement_game.adapters.uogto import UogtoExporter


class AdapterTests(unittest.TestCase):
    def test_kairos_contract(self) -> None:
        value = KairosScenarioExporter().export_scenario([{"kind": "move"}])
        self.assertEqual(value["target"], "edithatogo/kairos")
        self.assertEqual(value["events"][0]["sequence"], 0)

    def test_uogto_export(self) -> None:
        case = json.loads(Path("examples/cases/chapter8_example.json").read_text())
        value = UogtoExporter().export_game(case)
        self.assertIn("uogto:GameInstance", value["@type"])
        self.assertEqual(value["ndrg:economicContext"], "fixed")

    def test_atlas_jsonl_reader(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "records.jsonl"
            path.write_text(
                '{"record_id":"x","approval_state":"approved","provenance":"reviewed export"}\n',
                encoding="utf-8",
            )
            self.assertEqual(ReimbursementAtlasExport(path).records()[0]["record_id"], "x")

    def test_adapters_reject_non_finite_numbers(self) -> None:
        with self.assertRaisesRegex(ValueError, "event time must be finite"):
            KairosScenarioExporter().export_scenario([{"kind": "move", "time": float("nan")}])
        case = json.loads(Path("examples/cases/chapter8_example.json").read_text())
        case["incremental_cost"] = float("inf")
        with self.assertRaisesRegex(ValueError, "economic values must be finite"):
            UogtoExporter().export_game(case)

    def test_atlas_reader_rejects_unapproved_or_scalar_records(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "records.jsonl"
            path.write_text('{"record_id":"x","approval_state":"candidate"}\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "explicitly approved"):
                ReimbursementAtlasExport(path).records()
            path.write_text('"scalar"\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "JSON objects"):
                ReimbursementAtlasExport(path).records()


if __name__ == "__main__":
    unittest.main()
