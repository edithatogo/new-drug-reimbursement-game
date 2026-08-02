import unittest
from pathlib import Path

from scripts.validate_data_boundaries import boundary_violations, release_boundary_violations


class DataBoundaryTests(unittest.TestCase):
    def test_rejects_restricted_data_paths_and_archives(self) -> None:
        violations = boundary_violations(
            [Path("data/raw/patients.csv"), Path("exports/results.parquet"), Path("secrets/token.txt")]
        )
        self.assertEqual(len(violations), 3)

    def test_allows_governance_discussion_and_normal_source_files(self) -> None:
        self.assertEqual(
            boundary_violations(
                [
                    Path("conductor/tracks/t15_raw_data_governance_20260802/spec.md"),
                    Path("docs/governance/confidential/negative-receipt.md"),
                    Path("src/reimbursement_game/evidence.py"),
                ]
            ),
            [],
        )

    def test_release_receipt_preserves_restricted_scope_exclusions(self) -> None:
        self.assertEqual(release_boundary_violations(), [])


if __name__ == "__main__":
    unittest.main()
