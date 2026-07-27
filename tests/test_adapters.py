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
            path.write_text('{"record_id":"x"}\n', encoding="utf-8")
            self.assertEqual(ReimbursementAtlasExport(path).records()[0]["record_id"], "x")


if __name__ == "__main__":
    unittest.main()
