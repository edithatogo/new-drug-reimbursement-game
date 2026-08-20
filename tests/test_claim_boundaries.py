import json
import unittest

from scripts.validate_claim_boundaries import (
    MATRIX,
    validate_claims,
    validate_repository_boundaries,
)


class ClaimBoundaryTests(unittest.TestCase):
    def test_current_repository_claims_are_fail_closed(self) -> None:
        self.assertEqual(validate_repository_boundaries(), [])

    def test_rejects_regulatory_promotion(self) -> None:
        matrix = json.loads(MATRIX.read_text())
        for item in matrix["claims"]:
            if item["claim"] == "MHRA compliant or medical-device approved":
                item["status"] = "permitted"
        self.assertIn(
            "claim is not fail-closed: MHRA compliant or medical-device approved",
            validate_claims(matrix),
        )


if __name__ == "__main__":
    unittest.main()
