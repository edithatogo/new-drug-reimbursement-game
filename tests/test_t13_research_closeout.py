import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class T13ResearchCloseoutTests(unittest.TestCase):
    def test_builder_is_deterministic_and_fail_closed(self) -> None:
        revision = "0" * 40
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            command = [
                "python3",
                "scripts/build_t13_research_closeout.py",
                "--reviewed-revision",
                revision,
                "--output-dir",
                str(output),
            ]
            subprocess.run(command, check=True, capture_output=True, text=True)
            first = {path.name: path.read_bytes() for path in output.iterdir()}
            subprocess.run(command, check=True, capture_output=True, text=True)
            second = {path.name: path.read_bytes() for path in output.iterdir()}
            self.assertEqual(first, second)

            result = json.loads(first["constrained-research-output-2026-08-03.json"])
            self.assertFalse(result["decision_use_permitted"])
            self.assertFalse(result["empirical_calibration_activated"])
            self.assertEqual(result["release_label"], "synthetic_research_only")
            self.assertEqual(len(result["scenarios"]), 4)
            for scenario in result["scenarios"]:
                self.assertEqual(scenario["classification"], "synthetic_conformance_only")
                self.assertFalse(scenario["calibration_receipt"]["decision_use_permitted"])
                self.assertTrue(scenario["calibration_receipt"]["synthetic"])

    def test_builder_rejects_non_commit_revision(self) -> None:
        result = subprocess.run(
            [
                "python3",
                "scripts/build_t13_research_closeout.py",
                "--reviewed-revision",
                "main",
            ],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("40-character lowercase Git commit", result.stderr)


if __name__ == "__main__":
    unittest.main()
