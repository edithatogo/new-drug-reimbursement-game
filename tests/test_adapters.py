import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

from reimbursement_game.adapters.kairos import KairosScenarioExporter
from reimbursement_game.adapters.reimbursement_atlas import (
    ReimbursementAtlasExport,
    ReimbursementAtlasParameterExport,
)
from reimbursement_game.adapters.uogto import UogtoExporter
from reimbursement_game.adapters.voiage import VoiageAdapter
from reimbursement_game.calibration import (
    ParameterSamples,
    VoiageSampleBundle,
    calibrate_chapter7_scenario,
)
from reimbursement_game.chapter7 import Chapter7Scenario
from reimbursement_game.evidence import ParameterRole


class AdapterTests(unittest.TestCase):
    def test_kairos_contract(self) -> None:
        value = KairosScenarioExporter().export_scenario([{"kind": "move"}])
        self.assertEqual(value["target"], "edithatogo/kairos")
        self.assertEqual(value["events"][0]["sequence"], 0)

    def test_kairos_trace_receipt_is_deterministic(self) -> None:
        adapter = KairosScenarioExporter()
        events = [{"kind": "move", "time": 0}, {"kind": "resolve", "time": 1}]
        self.assertEqual(adapter.trace_receipt(events), adapter.trace_receipt(events))
        self.assertEqual(adapter.trace_receipt(events).event_count, 2)

    def test_kairos_rejects_invalid_event_boundaries(self) -> None:
        adapter = KairosScenarioExporter()
        with self.assertRaisesRegex(ValueError, "non-decreasing"):
            adapter.export_scenario([{"kind": "a", "time": 1}, {"kind": "b", "time": 0}])
        with self.assertRaisesRegex(ValueError, "payload"):
            adapter.export_scenario([{"kind": "a", "payload": []}])
        with self.assertRaisesRegex(ValueError, "non-empty"):
            adapter.export_scenario([{"kind": " "}])

    def test_uogto_export(self) -> None:
        case = json.loads(Path("examples/cases/chapter8_example.json").read_text())
        value = UogtoExporter().export_game(case)
        self.assertIn("uogto:GameInstance", value["@type"])
        self.assertEqual(value["@id"], "urn:ndrg:synthetic-ch8-001:game")
        self.assertEqual(value["hasPlayer"], [
            "urn:ndrg:synthetic-ch8-001:firm",
            "urn:ndrg:synthetic-ch8-001:institution",
        ])
        self.assertEqual(len(value["governedByRule"]), 2)
        self.assertEqual(value["ndrg:economicContext"], "fixed")

    def test_atlas_jsonl_reader(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "records.jsonl"
            path.write_text(
                '{"record_id":"x","approval_state":"approved","provenance":"reviewed export"}\n',
                encoding="utf-8",
            )
            self.assertEqual(ReimbursementAtlasExport(path).records()[0]["record_id"], "x")

    def test_atlas_parameter_export_and_voiage_schema_handoff(self) -> None:
        packet = ReimbursementAtlasParameterExport(
            "fixtures/evidence/synthetic-chapter7-parameter-packet-v1.json"
        ).packet()
        calibrated = calibrate_chapter7_scenario(
            case_id="adapter-synthetic-s1",
            scenario=Chapter7Scenario.EXPANDABLE_EFFICIENT,
            incremental_cost=120,
            incremental_health_effect=20,
            packet=packet,
            record_ids={ParameterRole.EXPANSION_ICER: "n-allocative"},
        )
        numpy_module = ModuleType("numpy")

        def fake_asarray(values, dtype):  # type: ignore[no-untyped-def]
            sequence = tuple(values)
            if sequence and isinstance(sequence[0], (list, tuple)):
                sequence = tuple(tuple(row) for row in sequence)
            return sequence, dtype

        numpy_module.asarray = fake_asarray  # type: ignore[attr-defined]
        schema_module = ModuleType("voiage.schema")

        class FakeValueArray:
            @classmethod
            def from_numpy(cls, values, strategy_names):  # type: ignore[no-untyped-def]
                return {"values": values, "strategy_names": strategy_names}

        class FakeParameterSet:
            @classmethod
            def from_numpy_or_dict(cls, values):  # type: ignore[no-untyped-def]
                return values

        schema_module.ValueArray = FakeValueArray  # type: ignore[attr-defined]
        schema_module.ParameterSet = FakeParameterSet  # type: ignore[attr-defined]
        voiage_module = ModuleType("voiage")
        voiage_module.schema = schema_module  # type: ignore[attr-defined]
        with patch.dict(
            sys.modules,
            {
                "numpy": numpy_module,
                "voiage": voiage_module,
                "voiage.schema": schema_module,
            },
        ):
            values, parameters = VoiageAdapter().prepare_inputs(calibrated.voiage_samples)
        self.assertEqual(
            values["strategy_names"], ["reimburse", "best_available_alternative"]
        )
        self.assertEqual(sorted(parameters), ["n"])
        self.assertEqual(len(values["values"][0]), 2)

    def test_voiage_handoff_receipt_is_deterministic_and_revision_bound(self) -> None:
        packet = ReimbursementAtlasParameterExport(
            "fixtures/evidence/synthetic-chapter7-parameter-packet-v1.json"
        ).packet()
        calibrated = calibrate_chapter7_scenario(
            case_id="receipt-s1",
            scenario=Chapter7Scenario.EXPANDABLE_EFFICIENT,
            incremental_cost=120,
            incremental_health_effect=20,
            packet=packet,
            record_ids={ParameterRole.EXPANSION_ICER: "n-allocative"},
        )
        adapter = VoiageAdapter()
        first = adapter.handoff_receipt(calibrated.voiage_samples)
        second = adapter.handoff_receipt(calibrated.voiage_samples)
        self.assertEqual(first, second)
        self.assertTrue(first.digest.startswith("sha256:"))
        self.assertEqual(first.sample_count, 2)

    def test_voiage_handoff_receipt_rejects_invalid_parameter_samples(self) -> None:
        bundle = VoiageSampleBundle(
            strategy_names=("reimburse", "alternative"),
            net_benefit_samples=((1.0, 2.0), (2.0, 1.0)),
            parameter_samples=(
                ParameterSamples(ParameterRole.EXPANSION_ICER, (1.0, float("nan"))),
            ),
            perspective="health",
            health_unit="QALY",
            evidence_revision="sha256:test",
        )
        with self.assertRaisesRegex(ValueError, "finite"):
            VoiageAdapter().handoff_receipt(bundle)

    def test_atlas_parameter_export_rejects_legacy_and_symlink_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            legacy = Path(directory) / "records.jsonl"
            legacy.write_text("{}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "versioned JSON"):
                ReimbursementAtlasParameterExport(legacy).packet()
            link = Path(directory) / "packet.json"
            link.symlink_to(
                Path.cwd() / "fixtures/evidence/synthetic-chapter7-parameter-packet-v1.json"
            )
            with self.assertRaisesRegex(ValueError, "non-symlink"):
                ReimbursementAtlasParameterExport(link).packet()

    def test_adapters_reject_non_finite_numbers(self) -> None:
        with self.assertRaisesRegex(ValueError, "event time must be finite"):
            KairosScenarioExporter().export_scenario([{"kind": "move", "time": float("nan")}])
        case = json.loads(Path("examples/cases/chapter8_example.json").read_text())
        case["incremental_cost"] = float("inf")
        with self.assertRaisesRegex(ValueError, "economic values must be finite"):
            UogtoExporter().export_game(case)

    def test_voiage_boundary_rejects_malformed_samples_before_optional_import(self) -> None:
        adapter = VoiageAdapter()
        with self.assertRaisesRegex(ValueError, "non-empty matrix"):
            adapter.evpi([])
        with self.assertRaisesRegex(ValueError, "at least two strategies"):
            adapter.evpi([[1.0], [2.0]])
        with self.assertRaisesRegex(ValueError, "rectangular"):
            adapter.evpi([[1.0, 2.0], [3.0]])
        with self.assertRaisesRegex(ValueError, "finite numbers"):
            adapter.evpi([[1.0, float("nan")], [3.0, 4.0]])

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
