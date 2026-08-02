import contextlib
import io
import json
import unittest

from reimbursement_game.disclosure import serialize_public_synthetic, synthetic_aggregate
from scripts.validate_confidential_boundaries import MATRIX, matrix_violations


class ConfidentialBoundaryTests(unittest.TestCase):
    def test_committed_matrix_is_fail_closed(self) -> None:
        self.assertEqual(matrix_violations(json.loads(MATRIX.read_text(encoding="utf-8"))), [])

    def test_matrix_mutations_are_rejected(self) -> None:
        base = {"default": {"disclosure_status": "approved", "export_permitted": True}, "outputs": []}
        self.assertTrue(matrix_violations(base))
        unsafe = {"default": {"disclosure_status": "prohibited", "export_permitted": False}, "outputs": [
            {"id": "unsafe", "audience": "public", "disclosure_status": "deferred", "synthetic_only": False,
             "export_permitted": True, "authorizer": None, "destination": None}
        ]}
        self.assertGreaterEqual(len(matrix_violations(unsafe)), 3)

    def test_synthetic_aggregation_rejects_small_and_dominant_cells(self) -> None:
        with self.assertRaisesRegex(ValueError, "below"):
            synthetic_aggregate([1, 2, 3, 4])
        with self.assertRaisesRegex(ValueError, "dominance"):
            synthetic_aggregate([100, 1, 1, 1, 1])
        self.assertEqual(synthetic_aggregate([2, 3, 4, 5, 6]), 20)

    def test_public_serializer_rejects_restricted_and_prohibited_fields_without_leaking(self) -> None:
        sentinel = "UNIQUE-CONFIDENTIAL-CANARY-1947"
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
            with self.assertRaises(ValueError):
                serialize_public_synthetic({"value": sentinel}, audience="restricted",
                                           disclosure_status="deferred", synthetic_only=False)
            with self.assertRaises(ValueError):
                serialize_public_synthetic({"net_price": sentinel}, audience="public",
                                           disclosure_status="approved", synthetic_only=True)
        self.assertNotIn(sentinel, captured.getvalue())

    def test_public_serializer_accepts_labelled_synthetic_output(self) -> None:
        self.assertEqual(
            serialize_public_synthetic({"aggregate": 20}, audience="public",
                                       disclosure_status="approved", synthetic_only=True),
            '{"aggregate":20}',
        )


if __name__ == "__main__":
    unittest.main()
