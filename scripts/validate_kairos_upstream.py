#!/usr/bin/env python3
"""Create a fail-closed Kairos upstream qualification receipt.

This check is intentionally local and deterministic.  It proves the pinned
checkout and records whether a release contract exists; it never treats local
tests or repository-owner approval as upstream maintainer acceptance.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def run(*args: str, cwd: Path) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True, stderr=subprocess.STDOUT).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkout", type=Path, default=Path(".local/ecosystem/kairos"))
    parser.add_argument("--revision", default="fae901558f07b7b717a676adbafbe2cdc78dea1c")
    parser.add_argument("--output", type=Path, default=Path("docs/governance/kairos-upstream-qualification.json"))
    args = parser.parse_args()
    checkout = args.checkout.resolve()
    if not checkout.is_dir():
        raise SystemExit(f"Kairos checkout not found: {checkout}")
    head = run("git", "rev-parse", "HEAD", cwd=checkout)
    tags = run("git", "tag", "--points-at", args.revision, cwd=checkout).splitlines()
    manifest_path = checkout / "packaging/release-package-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.is_file() else {}
    receipt = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repository": "https://github.com/edithatogo/kairos",
        "pinned_revision": args.revision,
        "checkout_head": head,
        "revision_matches": head == args.revision,
        "tags_at_pinned_revision": tags,
        "release_stage": manifest.get("release_stage"),
        "production_publish_enabled": manifest.get("production_publish_enabled"),
        "local_compatibility_evidence": "available; not equivalent to upstream acceptance",
        "upstream_contract_status": "pending",
        "upstream_maintainer_acceptance": "not_found",
        "decision": "adapter_isolated_candidate_only",
        "limitations": [
            "No release tag or maintainer acceptance receipt was found at the pinned revision.",
            "Local checkout and tests do not establish a released DTO/API contract.",
            "Do not claim native Kairos integration or extraction authorization from this receipt.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    return 0 if receipt["revision_matches"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
