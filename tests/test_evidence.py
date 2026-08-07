import copy
import json
import unittest
from pathlib import Path
from typing import Any

from reimbursement_game.evidence import (
    Marginality,
    ParameterRole,
    UncertaintyKind,
    evidence_packet_from_mapping,
)

FIXTURE = Path("fixtures/evidence/synthetic-chapter7-parameter-packet-v1.json")


def fixture_value() -> dict[str, Any]:
    value = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class EvidencePacketTests(unittest.TestCase):
    def test_parses_strict_approved_derived_packet(self) -> None:
        packet = evidence_packet_from_mapping(fixture_value())
        self.assertEqual(packet.context.jurisdiction, "SYNTHETIC-NOT-FOR-DECISIONS")
        self.assertEqual(len(packet.records), 9)
        investment = next(record for record in packet.records if record.role is ParameterRole.INVESTMENT_ICER)
        self.assertEqual(investment.samples, (2.0, 2.4))
        self.assertEqual(investment.marginality, Marginality.MARGINAL)
        self.assertEqual(investment.uncertainty_kind, UncertaintyKind.POSTERIOR_SAMPLES)

    def test_rejects_raw_unapproved_or_ambiguous_records(self) -> None:
        for field, replacement, message in (
            ("approval_state", "candidate", "explicitly approved"),
            ("derived_only", False, "raw records are forbidden"),
            ("marginality", "incremental", "requires marginality"),
        ):
            with self.subTest(field=field):
                value = fixture_value()
                value["records"][0][field] = replacement
                with self.assertRaisesRegex(ValueError, message):
                    evidence_packet_from_mapping(value)

    def test_rejects_unit_context_and_provenance_failures(self) -> None:
        mutations = (
            (("records", 0, "unit"), "USD/QALY", "requires unit"),
            (("records", 0, "source", "sha256"), "not-a-hash", "sha256"),
            (("context", "decision_date"), "01/08/2026", "ISO-8601"),
            (("records", 0, "causal_assumptions"), [], "non-empty"),
        )
        for path, replacement, message in mutations:
            with self.subTest(path=path):
                value = fixture_value()
                target: Any = value
                for part in path[:-1]:
                    target = target[part]
                target[path[-1]] = replacement
                with self.assertRaisesRegex(ValueError, message):
                    evidence_packet_from_mapping(value)

    def test_rejects_non_finite_misaligned_or_out_of_scale_samples(self) -> None:
        for samples, message in (
            ([2.0], "at least two"),
            ([2.0, float("nan")], "finite"),
            ([2.0, 6.0], "scale_limits"),
        ):
            with self.subTest(samples=samples):
                value = fixture_value()
                value["records"][4]["uncertainty"]["samples"] = samples
                with self.assertRaisesRegex(ValueError, message):
                    evidence_packet_from_mapping(value)

    def test_rejects_duplicate_ids_and_unexpected_fields(self) -> None:
        duplicate = fixture_value()
        duplicate["records"][1]["record_id"] = duplicate["records"][0]["record_id"]
        with self.assertRaisesRegex(ValueError, "unique"):
            evidence_packet_from_mapping(duplicate)
        unexpected = copy.deepcopy(duplicate)
        unexpected["records"][1]["record_id"] = "unique-again"
        unexpected["records"][0]["raw_payload"] = "forbidden"
        with self.assertRaisesRegex(ValueError, "unexpected=.*raw_payload"):
            evidence_packet_from_mapping(unexpected)


if __name__ == "__main__":
    unittest.main()
