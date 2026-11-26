"""Source and algorithm admission controls for the native evidence pilot."""

import hashlib
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from scripts import verify_reimbursement_information_pilot as pilot

_HEADER = (
    "1.0.0\tpaignia/static-finite-perfect-information-sparse-zero/1.0.0\t{}"
    "\turn:ndrg:si04:synthetic-committed-offer-v1\turn:ndrg:si04:synthetic-two-state-instance"
    "\turn:ndrg:si04:valued-policy-run\t0.000000000001{}\n"
)
_WORLDS = (
    "favourable\tclinical_positive\t0.5\t4\t3\treimburse\n"
    "adverse\tclinical_negative\t0.5\t-4\t3\twithhold\n"
)
_SIGNED = (_HEADER.format("1.0.1", f"\t{pilot._PROVIDER_REVISION}") + _WORLDS).encode()
_LEGACY = (_HEADER.format("1.0.0", "") + _WORLDS).encode()


class ReimbursementInformationPilotTests(unittest.TestCase):
    def test_signed_provider_binds_both_native_packages_and_keeps_the_algorithm(self):
        policy, worlds = pilot._native_projection(_SIGNED)
        self.assertEqual(policy["provider_revision"], pilot._PROVIDER_REVISION)
        self.assertEqual(policy["package_receipt_sha256"], pilot._PACKAGE_RECEIPT)
        self.assertEqual(
            policy["game_sha256"], hashlib.sha256(pilot._RECIPE.read_bytes()).hexdigest()
        )
        self.assertEqual(policy["native"]["algorithm_version"], "1.0.1")
        self.assertEqual(
            [item["action_id"] for item in policy["choices"]], ["reimburse", "withhold"]
        )
        self.assertEqual([item["probability"] for item in worlds], [0.5, 0.5])

    def test_preserves_the_exact_historical_report(self):
        self.assertEqual(hashlib.sha256(_LEGACY).hexdigest(), pilot._HISTORICAL_REPORT)
        policy, _ = pilot._native_projection(_LEGACY)
        self.assertEqual(policy["provider_revision"], "bd880dd756d2ba56cc5f479bc078cea31b53c1d1")
        self.assertEqual(policy["native"]["algorithm_version"], "1.0.0")
        with self.assertRaisesRegex(ValueError, "identify the signed Paignia provider"):
            pilot._native_projection(_LEGACY + b"\n")

    def test_rejects_misattributed_algorithm_and_lock_sources(self):
        claimed = (_HEADER.format("1.0.0", f"\t{pilot._PROVIDER_REVISION}") + _WORLDS).encode()
        with self.assertRaisesRegex(ValueError, "algorithm does not match"):
            pilot._native_projection(claimed)

        source = f"git+https://github.com/edithatogo/paignia?rev={pilot._PROVIDER_REVISION}#{pilot._PROVIDER_REVISION}"
        with TemporaryDirectory() as workdir:
            root = Path(workdir)
            (root / "Cargo.lock").write_text(
                f'[[package]]\nname = "paignia-core"\nsource = "{source}"\n'
                '[[package]]\nname = "paignia-solve"\nsource = "mismatched"\n'
            )
            with (
                patch.object(pilot, "_ROOT", root),
                self.assertRaisesRegex(ValueError, "lock differs"),
            ):
                pilot._native_projection(_SIGNED)
