import copy
import json
import unittest

from scripts.validate_empirical_readiness import COVERAGE, RELEASE, RUN, readiness_violations


def load(path):  # type: ignore[no-untyped-def]
    return json.loads(path.read_text(encoding="utf-8"))


class EmpiricalReadinessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.run = load(RUN)
        self.coverage = load(COVERAGE)
        self.release = load(RELEASE)

    def test_committed_negative_coverage_is_consistent(self) -> None:
        self.assertEqual(readiness_violations(self.run, self.coverage, self.release), [])

    def test_incomplete_evidence_cannot_promote(self) -> None:
        coverage = copy.deepcopy(self.coverage)
        coverage["decision"] = "promote_empirical_calibration"
        self.assertIn(
            "incomplete evidence must defer empirical promotion",
            readiness_violations(self.run, coverage, self.release),
        )

    def test_unknown_sources_and_missing_fields_fail(self) -> None:
        coverage = copy.deepcopy(self.coverage)
        coverage["fields"][0]["sources"] = ["unreceipted-source"]
        coverage["fields"] = [item for item in coverage["fields"] if item["field"] != "price_year"]
        violations = readiness_violations(self.run, coverage, self.release)
        self.assertTrue(any("unknown source" in item for item in violations))
        self.assertTrue(any("omits required fields" in item for item in violations))

    def test_payload_retention_and_bad_hash_fail(self) -> None:
        run = copy.deepcopy(self.run)
        fetched = next(item for item in run["sources"] if item["status"] == "fetched")
        fetched["payload_retained"] = True
        fetched["sha256"] = "bad"
        violations = readiness_violations(run, self.coverage, self.release)
        self.assertTrue(any("must not retain payload" in item for item in violations))
        self.assertTrue(any("invalid sha256" in item for item in violations))

    def test_release_must_keep_calibrated_claims_prohibited(self) -> None:
        release = copy.deepcopy(self.release)
        release["prohibited"] = ["regulatory claims"]
        self.assertTrue(any("must prohibit" in item for item in readiness_violations(self.run, self.coverage, release)))


if __name__ == "__main__":
    unittest.main()
