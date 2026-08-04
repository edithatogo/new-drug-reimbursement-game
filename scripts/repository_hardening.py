#!/usr/bin/env python3
"""Validate repository-owned GitHub security and contribution context.

The checked-in receipt makes changes to the small set of governance files
reviewable without relying on live GitHub settings.  Rulesets and repository
visibility remain intentionally outside this local check.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "docs/generated/repository-hardening-receipt.json"
TRACKED = (
    ".github/CODEOWNERS",
    ".github/pull_request_template.md",
    ".github/workflows/ci.yml",
    ".github/workflows/dependency-review.yml",
    ".github/workflows/sbom.yml",
    ".github/workflows/scorecard.yml",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "codecov.yml",
    "renovate.json",
    "SECURITY.md",
    "security-insights.yml",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected() -> dict[str, object]:
    files = {name: digest(ROOT / name) for name in TRACKED}
    return {
        "schema": "repository-hardening-receipt/v1",
        "scope": "repository-owned GitHub metadata and contribution/security context",
        "files": files,
        "workflow_controls": {
            "default_permissions": "contents: read",
            "concurrency": "cancel-in-progress",
            "job_timeouts_minutes": 30,
            "immutable_actions": True,
            "coverage_upload": "codecov OIDC",
        },
        "external_gates": ["branch rulesets", "repository visibility", "required checks"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    current = expected()
    if args.write:
        RECEIPT.parent.mkdir(parents=True, exist_ok=True)
        RECEIPT.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n")
        print(f"wrote {RECEIPT.relative_to(ROOT)}")
        return 0
    if not RECEIPT.exists():
        print(f"missing {RECEIPT.relative_to(ROOT)}")
        return 1
    recorded = json.loads(RECEIPT.read_text())
    if recorded != current:
        print("repository hardening receipt drift detected")
        return 1
    print("repository hardening receipt: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
