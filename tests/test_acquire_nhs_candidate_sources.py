import hashlib
import unittest
from email.message import Message
from unittest.mock import patch

from scripts.acquire_nhs_candidate_sources import (
    MAX_BYTES,
    fetch,
    field_coverage,
    validate_source_url,
)


class FakeResponse:
    def __init__(self, payload: bytes, url: str = "https://www.nice.org.uk/final") -> None:
        self.payload = payload
        self.url = url
        self.status = 200
        self.headers = Message()
        self.headers["Content-Type"] = "application/json"
        self.headers["ETag"] = '"revision"'

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self, size: int = -1) -> bytes:
        return self.payload if size < 0 else self.payload[:size]

    def geturl(self) -> str:
        return self.url


class AcquisitionTests(unittest.TestCase):
    def test_rejects_non_https_and_unlisted_hosts(self) -> None:
        for url in ("http://www.nice.org.uk/test", "https://example.com/test", "file:///tmp/source"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                validate_source_url(url)

    def test_fetch_hashes_without_retaining_payload(self) -> None:
        payload = b'{"evidence":"candidate"}'
        with patch("scripts.acquire_nhs_candidate_sources.urllib.request.urlopen", return_value=FakeResponse(payload)):
            result = fetch("nice", "https://www.nice.org.uk/source", 1)
        self.assertEqual(result["sha256"], hashlib.sha256(payload).hexdigest())
        self.assertEqual(result["final_uri"], "https://www.nice.org.uk/final")
        self.assertFalse(result["payload_retained"])
        self.assertNotIn("payload", result)

    def test_atlas_latest_release_records_immutable_identity(self) -> None:
        payload = b'{"tag_name":"v1.2.3","published_at":"2026-08-02T00:00:00Z","target_commitish":"main","id":123}'
        with patch(
            "scripts.acquire_nhs_candidate_sources.urllib.request.urlopen",
            return_value=FakeResponse(payload, "https://api.github.com/releases/123"),
        ):
            result = fetch(
                "atlas-latest-release",
                "https://api.github.com/repos/edithatogo/reimbursement-atlas/releases/latest",
                1,
            )
        self.assertEqual(
            result["immutable_release_identity"],
            {
                "tag_name": "v1.2.3",
                "published_at": "2026-08-02T00:00:00Z",
                "target_commitish": "main",
                "release_id": 123,
            },
        )

    def test_fetch_fails_closed_on_oversize_source(self) -> None:
        with patch(
            "scripts.acquire_nhs_candidate_sources.urllib.request.urlopen",
            return_value=FakeResponse(b"x" * (MAX_BYTES + 1)),
        ):
            result = fetch("nice", "https://www.nice.org.uk/source", 1)
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["error_type"], "ValueError")

    def test_coverage_keeps_displacement_and_atlas_packet_missing(self) -> None:
        coverage = field_coverage()
        self.assertEqual(coverage["displaced_programme"], "missing")
        self.assertEqual(coverage["atlas_approved_n_m_d_packet"], "not_found_v0.1.1")


if __name__ == "__main__":
    unittest.main()
