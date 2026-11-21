"""Regression cases for the application and Voiage provider boundary."""

from __future__ import annotations

import sys
import unittest
from dataclasses import replace
from importlib.util import find_spec
from unittest.mock import patch

from reimbursement_game.adapters.voiage import VoiageAdapter
from reimbursement_game.calibration import ParameterSamples, VoiageSampleBundle
from reimbursement_game.evidence import ParameterRole


def valid_bundle() -> VoiageSampleBundle:
    return VoiageSampleBundle(
        strategy_names=("reimburse", "alternative"),
        net_benefit_samples=((1.0, 2.0), (2.0, 1.0)),
        parameter_samples=(
            ParameterSamples(ParameterRole.EXPANSION_ICER, (10.0, 20.0)),
        ),
        perspective="health",
        health_unit="QALY",
        evidence_revision="sha256:" + "a" * 64,
    )


class VoiageBoundaryConsistencyTests(unittest.TestCase):
    def assert_rejected_before_import(
        self, bundle: VoiageSampleBundle, message: str
    ) -> None:
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
                parameter_samples=(
                    ParameterSamples(ParameterRole.EXPANSION_ICER, (10.0,)),
                ),
            ),
            "align with strategy samples",
        )

    def test_receipt_retains_joint_parameter_draw_order(self) -> None:
        bundle = valid_bundle()
        receipt = VoiageAdapter().handoff_receipt(bundle)
        reordered = replace(
            bundle,
            parameter_samples=(
                ParameterSamples(ParameterRole.EXPANSION_ICER, (20.0, 10.0)),
            ),
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


if __name__ == "__main__":
    unittest.main()
