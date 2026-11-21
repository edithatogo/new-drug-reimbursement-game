"""Regression cases for the application and Voiage provider boundary."""

from __future__ import annotations

import json
import sys
import unittest
from dataclasses import replace
from importlib.util import find_spec
from pathlib import Path
from unittest.mock import patch

from reimbursement_game.adapters.voiage import VoiageAdapter
from reimbursement_game.calibration import ParameterSamples, VoiageSampleBundle
from reimbursement_game.evidence import ParameterRole


def valid_bundle() -> VoiageSampleBundle:
    return VoiageSampleBundle(
        strategy_names=("reimburse", "alternative"),
        net_benefit_samples=((1.0, 2.0), (2.0, 1.0)),
        parameter_samples=(ParameterSamples(ParameterRole.EXPANSION_ICER, (10.0, 20.0)),),
        perspective="health",
        health_unit="QALY",
        evidence_revision="sha256:" + "a" * 64,
    )


class VoiageBoundaryConsistencyTests(unittest.TestCase):
    def assert_rejected_before_import(self, bundle: VoiageSampleBundle, message: str) -> None:
        adapter = VoiageAdapter()
        # A validation failure must be the same whether the provider is installed
        # or not. No provider mock should conceal a missing boundary check.
        with patch.dict(
            sys.modules,
            {"numpy": None, "voiage": None, "voiage.schema": None},
        ):
            for method in (adapter.prepare_inputs, adapter.handoff_receipt):
                with self.subTest(method=method.__name__):
                    with self.assertRaisesRegex(ValueError, message):
                        method(bundle)

    def test_duplicate_parameter_roles_are_not_overwritten(self) -> None:
        bundle = valid_bundle()
        self.assert_rejected_before_import(
            replace(
                bundle,
                parameter_samples=(
                    *bundle.parameter_samples,
                    ParameterSamples(ParameterRole.EXPANSION_ICER, (30.0, 40.0)),
                ),
            ),
            "roles must be unique",
        )

    def test_nonfinite_parameters_are_rejected_in_both_paths(self) -> None:
        for invalid in (float("nan"), float("inf"), -float("inf")):
            with self.subTest(invalid=invalid):
                self.assert_rejected_before_import(
                    replace(
                        valid_bundle(),
                        parameter_samples=(
                            ParameterSamples(ParameterRole.EXPANSION_ICER, (10.0, invalid)),
                        ),
                    ),
                    "finite numbers",
                )

    def test_empty_strategy_name_is_rejected_in_both_paths(self) -> None:
        self.assert_rejected_before_import(
            replace(valid_bundle(), strategy_names=("reimburse", " ")),
            "names must be non-empty",
        )

    def test_duplicate_strategy_names_are_rejected_in_both_paths(self) -> None:
        self.assert_rejected_before_import(
            replace(valid_bundle(), strategy_names=("reimburse", "reimburse")),
            "names must be unique",
        )

    def test_misaligned_parameters_are_rejected_in_both_paths(self) -> None:
        self.assert_rejected_before_import(
            replace(
                valid_bundle(),
                parameter_samples=(ParameterSamples(ParameterRole.EXPANSION_ICER, (10.0,)),),
            ),
            "align with strategy samples",
        )

    def test_incompatible_valuation_basis_is_rejected_in_both_paths(self) -> None:
        bundle = valid_bundle()
        for invalid in (
            replace(bundle, perspective="monetary"),
            replace(bundle, health_unit=""),
        ):
            with self.subTest(perspective=invalid.perspective, health_unit=invalid.health_unit):
                self.assert_rejected_before_import(
                    invalid, "requires an explicit health perspective"
                )

    def test_unpinned_evidence_revision_is_rejected_in_both_paths(self) -> None:
        self.assert_rejected_before_import(
            replace(valid_bundle(), evidence_revision="unversioned"),
            "requires a sha256 evidence revision",
        )

    def test_strategy_labels_must_match_sample_width_in_both_paths(self) -> None:
        self.assert_rejected_before_import(
            replace(valid_bundle(), strategy_names=("reimburse",)),
            "names must align with sample columns",
        )

    def test_missing_parameter_samples_are_rejected_in_both_paths(self) -> None:
        self.assert_rejected_before_import(
            replace(valid_bundle(), parameter_samples=()),
            "requires parameter samples",
        )

    def test_receipt_retains_joint_parameter_draw_order(self) -> None:
        bundle = valid_bundle()
        receipt = VoiageAdapter().handoff_receipt(bundle)
        reordered = replace(
            bundle,
            parameter_samples=(ParameterSamples(ParameterRole.EXPANSION_ICER, (20.0, 10.0)),),
        )
        self.assertNotEqual(receipt.digest, VoiageAdapter().handoff_receipt(reordered).digest)
        self.assertEqual(receipt, VoiageAdapter().handoff_receipt(bundle))

    @unittest.skipUnless(find_spec("voiage"), "requires the optional Voiage installation")
    def test_installed_provider_preserves_draw_order_and_exact_evpi(self) -> None:
        from voiage.schema import ParameterSet, ValueArray

        adapter = VoiageAdapter()
        bundle = valid_bundle()
        values, parameters = adapter.prepare_inputs(bundle)
        self.assertIsInstance(values, ValueArray)
        self.assertIsInstance(parameters, ParameterSet)
        self.assertEqual(values.strategy_names, ["reimburse", "alternative"])
        self.assertEqual(values.numpy_values.tolist(), [[1.0, 2.0], [2.0, 1.0]])
        self.assertEqual(parameters.to_polars().to_dict(as_series=False), {"n": [10.0, 20.0]})
        self.assertEqual(adapter.evpi(bundle.net_benefit_samples), 0.5)

    @unittest.skipUnless(find_spec("voiage"), "requires the optional Voiage installation")
    def test_signed_information_fixture_preserves_signed_values_and_accounts(self) -> None:
        from voiage import signed_social_information_value

        path = (
            Path(__file__).resolve().parents[1]
            / "fixtures/conformance/voiage-input-contract-v1.json"
        )
        fixture = json.loads(path.read_text(encoding="utf-8"))
        information_use = fixture["information_use"]
        result = signed_social_information_value(fixture["voiage_request"]).to_contract_dict()
        designs = {design["design_id"]: design for design in result["designs"]}
        for expected in fixture["expected_values"]:
            with self.subTest(metric=expected["metric"]):
                design = designs[expected["design_id"]]
                actor = expected["actor"]
                values = design["signed_values"]
                amount = values["social"] if actor is None else values["by_agent"][actor]
                self.assertEqual(amount, expected["value"])
                self.assertEqual(result["value_unit"], expected["unit"])
                self.assertEqual(
                    design["comparator_design_id"], information_use["comparator_design_id"]
                )
                self.assertEqual(design["recipients"], information_use["recipients"])
                self.assertEqual(design["selected_policy_id"], information_use["selected_policy"])
                self.assertFalse(values["clipped_at_zero"])
        ledgers = designs["observe_with_accounting"]["ledgers"]
        self.assertEqual(ledgers["transfer"]["institution"], 1.0)
        self.assertEqual(ledgers["transfer"]["public"], -1.0)
        self.assertEqual(ledgers["cost"]["institution"], 0.5)

    @unittest.skipUnless(find_spec("voiage"), "requires the optional Voiage installation")
    def test_parameter_evpi_excludes_the_within_state_replicate_contrast(self) -> None:
        path = (
            Path(__file__).resolve().parents[1]
            / "fixtures/conformance/voiage-noise-identities-v1.json"
        )
        fixture = json.loads(path.read_text(encoding="utf-8"))
        schedule = fixture["sampling_plan"]
        outcomes = fixture["outcomes"]
        parameter_ids = set(schedule["inner_replicates"])
        self.assertEqual(len(parameter_ids), schedule["outer_draws"])
        self.assertEqual({outcome["parameter_draw_id"] for outcome in outcomes}, parameter_ids)
        self.assertCountEqual(
            [
                (parameter, replicate)
                for parameter, replicates in schedule["inner_replicates"].items()
                for replicate in replicates
            ],
            [(outcome["parameter_draw_id"], outcome["replicate_id"]) for outcome in outcomes],
        )
        reference = fixture["reference"]
        ordered = [outcome["values"] for outcome in outcomes]
        means = [[sum(column) / len(column) for column in zip(*ordered, strict=True)]]
        self.assertEqual(means, reference["conditional_values"])

        adapter = VoiageAdapter()
        self.assertEqual(adapter.evpi(means), reference["parameter_evpi"])
        self.assertEqual(
            adapter.evpi(ordered), reference["invalid_evpi_if_replicates_become_parameter_draws"]
        )


if __name__ == "__main__":
    unittest.main()
