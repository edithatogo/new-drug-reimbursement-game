import copy
import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any

from reimbursement_game.chapter7 import Chapter7Scenario
from reimbursement_game.cli import main
from reimbursement_game.evidence import ParameterRole, evidence_packet_from_mapping
from reimbursement_game.pilot_readiness import (
    ReadinessStatus,
    assess_pilot_readiness,
    candidate_dossier_from_mapping,
)

DOSSIER = Path("fixtures/evidence/nhs-england-methodological-candidates-v1.json")
RECEIPT = Path("docs/generated/nhs-england-pilot-readiness.json")


def dossier_value() -> dict[str, Any]:
    value = json.loads(DOSSIER.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def candidate(
    candidate_id: str,
    role: str,
    value: float,
    unit: str,
    *,
    alignment_id: str | None = "aligned",
    programme_id: str | None = None,
) -> dict[str, Any]:
    item = copy.deepcopy(dossier_value()["candidates"][0])
    item.update(
        {
            "candidate_id": candidate_id,
            "kind": "research_estimate",
            "value": value,
            "unit": unit,
            "price_year": 2026,
            "study_period": "synthetic test period",
            "programme_id": programme_id,
            "alignment_id": alignment_id,
            "roles_considered": [role],
            "estimand": f"synthetic {role} test candidate",
        }
    )
    return item


class PilotReadinessTests(unittest.TestCase):
    def test_nhs_dossier_has_expected_fail_closed_readiness(self) -> None:
        receipt = assess_pilot_readiness(candidate_dossier_from_mapping(dossier_value()))
        roles = {row.role: row for row in receipt.roles}
        scenarios = {row.scenario: row for row in receipt.scenarios}
        self.assertEqual(roles[ParameterRole.EXPANSION_ICER].status, ReadinessStatus.CANDIDATE_ONLY)
        self.assertEqual(roles[ParameterRole.DISPLACEMENT_ICER].status, ReadinessStatus.NOT_IDENTIFIABLE)
        self.assertIn(
            "nice-reference-case-time-horizon-guidance",
            roles[ParameterRole.HORIZON].considered_candidate_ids,
        )
        self.assertEqual(roles[ParameterRole.HORIZON].numeric_candidate_ids, ())
        self.assertEqual(
            [row.status for row in receipt.scenarios],
            [
                ReadinessStatus.CANDIDATE_ONLY,
                ReadinessStatus.NOT_IDENTIFIABLE,
                ReadinessStatus.NOT_IDENTIFIABLE,
                ReadinessStatus.NOT_IDENTIFIABLE,
            ],
        )
        self.assertIn("n = m", scenarios[Chapter7Scenario.FIXED_EFFICIENT].pending_constraints[1])
        self.assertIn(
            "m > n", scenarios[Chapter7Scenario.FIXED_ALLOCATIVE_INEFFICIENCY].pending_constraints[1]
        )
        self.assertIn(
            "case-specific",
            scenarios[Chapter7Scenario.FIXED_TECHNICAL_INVESTMENT].pending_constraints[-1],
        )
        self.assertFalse(receipt.approved_calibration_permitted)

    def test_parser_rejects_promotion_invalid_values_units_and_provenance(self) -> None:
        mutations = (
            (("candidates", 0, "approval_state"), "approved", "remain candidate"),
            (("candidates", 0, "value"), float("nan"), "finite"),
            (("candidates", 0, "unit"), "bananas", "require unit"),
            (("candidates", 0, "source", "sha256"), "bad", "sha256"),
            (("candidates", 0, "source", "uri"), "http://example.com", "HTTPS"),
        )
        for path, replacement, message in mutations:
            with self.subTest(path=path):
                value = dossier_value()
                target: Any = value
                for part in path[:-1]:
                    target = target[part]
                target[path[-1]] = replacement
                with self.assertRaisesRegex(ValueError, message):
                    candidate_dossier_from_mapping(value)

    def test_parser_enforces_role_domains_and_shared_role_boundary(self) -> None:
        cases = (
            (candidate("bad-phi", "phi", 1.0, "dimensionless"), "greater than 1"),
            (candidate("bad-horizon", "horizon", 3.5, "year"), "whole number"),
            (candidate("bad-annual", "annual_program_health_effect", 2.0, "GBP/QALY"), "QALY/year"),
            (candidate("bad-discount", "discount_rate", 1.0, "proportion/year"), r"\[0, 1\)"),
        )
        for item, message in cases:
            with self.subTest(candidate=item["candidate_id"]):
                value = dossier_value()
                value["candidates"] = [item]
                with self.assertRaisesRegex(ValueError, message):
                    candidate_dossier_from_mapping(value)
        mixed = candidate("mixed", "n", 100.0, "GBP/QALY")
        mixed["roles_considered"] = ["n", "d"]
        value = dossier_value()
        value["candidates"] = [mixed]
        with self.assertRaisesRegex(ValueError, "only n and m"):
            candidate_dossier_from_mapping(value)

    def test_only_horizon_method_guidance_may_be_nonnumeric(self) -> None:
        value = dossier_value()
        value["candidates"][0]["value"] = None
        with self.assertRaisesRegex(ValueError, "only horizon method guidance"):
            candidate_dossier_from_mapping(value)

    def test_candidate_count_is_bounded_before_scenario_analysis(self) -> None:
        value = dossier_value()
        template = value["candidates"][0]
        value["candidates"] = []
        for index in range(257):
            item = copy.deepcopy(template)
            item["candidate_id"] = f"candidate-{index}"
            value["candidates"].append(item)
        with self.assertRaisesRegex(ValueError, "cannot exceed 256"):
            candidate_dossier_from_mapping(value)

    def test_scenario_two_and_three_require_aligned_economic_constraints(self) -> None:
        value = dossier_value()
        value["candidates"] = [
            candidate("n", "n", 10.0, "GBP/QALY", alignment_id="one"),
            candidate("m", "m", 20.0, "GBP/QALY", alignment_id="two"),
            candidate("d", "d", 30.0, "GBP/QALY", alignment_id="three"),
        ]
        scenarios = {
            row.scenario: row
            for row in assess_pilot_readiness(candidate_dossier_from_mapping(value)).scenarios
        }
        self.assertEqual(scenarios[Chapter7Scenario.FIXED_EFFICIENT].status, ReadinessStatus.INCOMPATIBLE)
        self.assertEqual(
            scenarios[Chapter7Scenario.FIXED_ALLOCATIVE_INEFFICIENCY].status,
            ReadinessStatus.INCOMPATIBLE,
        )
        self.assertIn("aligned", scenarios[Chapter7Scenario.FIXED_ALLOCATIVE_INEFFICIENCY].reason)

    def test_structurally_compatible_candidates_never_become_supported(self) -> None:
        value = dossier_value()
        value["candidates"] = [
            candidate("n-and-m", "n", 20.0, "GBP/QALY", alignment_id="decision"),
            candidate("d", "d", 15.0, "GBP/QALY", alignment_id="decision"),
        ]
        value["candidates"][0]["roles_considered"] = ["n", "m"]
        receipt = assess_pilot_readiness(candidate_dossier_from_mapping(value))
        scenario_two = next(
            row for row in receipt.scenarios if row.scenario is Chapter7Scenario.FIXED_EFFICIENT
        )
        self.assertEqual(scenario_two.status, ReadinessStatus.CANDIDATE_ONLY)
        self.assertFalse(receipt.approved_calibration_permitted)

    def test_scenario_four_requires_one_aligned_programme(self) -> None:
        roles = (
            ("m", 20.0, "GBP/QALY"),
            ("d", 15.0, "GBP/QALY"),
            ("mu", 10.0, "GBP/QALY"),
            ("phi", 2.0, "dimensionless"),
            ("annual_program_health_effect", 5.0, "QALY/year"),
            ("horizon", 10.0, "year"),
            ("discount_rate", 0.035, "proportion/year"),
        )
        value = dossier_value()
        value["candidates"] = [
            candidate(
                f"candidate-{role}",
                role,
                number,
                unit,
                alignment_id="decision",
                programme_id=(
                    "programme-a" if role not in {"m", "d", "discount_rate"} else None
                ),
            )
            for role, number, unit in roles
        ]
        scenario = assess_pilot_readiness(candidate_dossier_from_mapping(value)).scenarios[3]
        self.assertEqual(scenario.status, ReadinessStatus.INCOMPATIBLE)
        value["candidates"][-1]["programme_id"] = "programme-a"
        scenario = assess_pilot_readiness(candidate_dossier_from_mapping(value)).scenarios[3]
        self.assertEqual(scenario.status, ReadinessStatus.CANDIDATE_ONLY)
        self.assertIn("case-specific", scenario.pending_constraints[-1])

    def test_revision_covers_semantic_and_provenance_fields(self) -> None:
        baseline = assess_pilot_readiness(candidate_dossier_from_mapping(dossier_value()))
        for field, replacement in (
            ("value", 15001),
            ("price_year", 2020),
            ("budget_scope", "different scope"),
            ("transformation", "different transformation"),
            ("mapping_limitations", ["different limitation"]),
        ):
            with self.subTest(field=field):
                value = dossier_value()
                value["candidates"][0][field] = replacement
                changed = assess_pilot_readiness(candidate_dossier_from_mapping(value))
                self.assertNotEqual(changed.dossier_revision, baseline.dossier_revision)

    def test_candidate_dossier_cannot_be_parsed_as_evidence_packet(self) -> None:
        with self.assertRaisesRegex(ValueError, "fields mismatch"):
            evidence_packet_from_mapping(dossier_value())

    def test_cli_matches_committed_receipt_exactly(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["pilot-readiness", str(DOSSIER)]), 0)
        self.assertEqual(output.getvalue(), RECEIPT.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
