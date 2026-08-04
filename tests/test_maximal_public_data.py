import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.build_maximal_public_packet import ACQUISITION_TARGET_COMMIT, build
from scripts.validate_maximal_public_data import EXPECTED, PACKET, TRACK, acquisition_violations


class MaximalPublicDataValidationTests(unittest.TestCase):
    def test_committed_bundles_pass(self) -> None:
        self.assertEqual(acquisition_violations(), [])

    def test_missing_bundle_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            violations = acquisition_violations(Path(directory))
        self.assertEqual(len(violations), len(EXPECTED))
        self.assertTrue(all("missing bundle" in item for item in violations))

    def test_missing_hash_and_reason_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            for number, filename in EXPECTED.items():
                bundle = {
                    "schema_version": "1.0",
                    "work_package": f"WP{number}",
                    "generated_at": "2026-08-04T00:00:00Z",
                    "scope": "test",
                    "sources": [{
                        "source_id": f"source-{number}",
                        "authority_rank": 1,
                        "publisher": "publisher",
                        "title": "title",
                        "requested_url": "https://example.invalid",
                        "final_url": "https://example.invalid",
                        "retrieval": {},
                        "terms": {"classification": "citation_only"},
                        "supported_fields": [],
                        "unsupported_fields": [],
                        "refresh_rule": "retry",
                    }],
                    "coverage": {},
                    "negative_or_deferred": [],
                    "rights_boundary": "test",
                    "completion_status": "test",
                    "validation": {},
                }
                (target / filename).write_text(json.dumps(bundle), encoding="utf-8")
            violations = acquisition_violations(target)
        self.assertEqual(len(violations), len(EXPECTED))
        self.assertTrue(all("missing hash and no-hash reason" in item for item in violations))

    def test_packet_is_context_only_and_fail_closed(self) -> None:
        packet = build("a" * 40)
        self.assertEqual(packet["parameter_roles"], {})
        self.assertEqual(packet["promotion"]["empirical_calibration"], "disabled")
        self.assertEqual(packet["promotion"]["decision_use"], "prohibited")
        self.assertIn("no attributable displaced programme or stable displaced-programme identifier", packet["negative_scope"])

    def test_default_packet_target_is_immutable(self) -> None:
        self.assertEqual(build()["acquisition_target_commit"], ACQUISITION_TARGET_COMMIT)

    def _copy_acquisition(self, directory: str) -> Path:
        target = Path(directory)
        for filename in [*EXPECTED.values(), PACKET]:
            shutil.copyfile(TRACK / filename, target / filename)
        return target

    def test_stale_bundle_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self._copy_acquisition(directory)
            with (target / EXPECTED[1]).open("a", encoding="utf-8") as stream:
                stream.write(" ")
            violations = acquisition_violations(target)
        self.assertTrue(any("stale referenced bundle" in item for item in violations))

    def test_empirical_promotion_and_parameter_roles_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self._copy_acquisition(directory)
            path = target / PACKET
            packet = json.loads(path.read_text(encoding="utf-8"))
            packet["promotion"]["empirical_calibration"] = "enabled"
            packet["parameter_roles"] = {"n": 1}
            path.write_text(json.dumps(packet), encoding="utf-8")
            violations = acquisition_violations(target)
        self.assertTrue(any("empirical or decision-use boundary" in item for item in violations))
        self.assertTrue(any("must not contain calibration parameter roles" in item for item in violations))

    def test_acquisition_target_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self._copy_acquisition(directory)
            path = target / PACKET
            packet = json.loads(path.read_text(encoding="utf-8"))
            packet["acquisition_target_commit"] = "0" * 40
            path.write_text(json.dumps(packet), encoding="utf-8")
            violations = acquisition_violations(target)
        self.assertTrue(any("governed immutable commit" in item for item in violations))


if __name__ == "__main__":
    unittest.main()
