#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


def run(command: list[str]) -> dict[str, object]:
    """Run one quality command without hiding its output."""

    print("+", " ".join(command), flush=True)
    environment = os.environ.copy()
    venv_bin = (Path(__file__).resolve().parents[1] / ".venv/bin").resolve()
    if venv_bin.is_dir():
        environment["PATH"] = str(venv_bin) + os.pathsep + environment.get("PATH", "")
    source_path = str((Path.cwd() / "src").resolve())
    environment["PYTHONPATH"] = source_path + os.pathsep + environment.get("PYTHONPATH", "")
    started = time.monotonic()
    returncode = subprocess.run(command, check=False, env=environment).returncode
    return {
        "name": Path(command[0]).name + ":" + " ".join(command[1:]),
        "result": "pass" if returncode == 0 else "fail",
        "duration_seconds": round(time.monotonic() - started, 3),
        "evidence": " ".join(command),
    }


def revision() -> str:
    """Return the exact Git revision without mutating repository state."""

    process = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return process.stdout.strip()


def write_receipt(path: Path, checks: list[dict[str, object]]) -> None:
    """Write a repository-standards verification receipt."""

    receipt = {
        "schema_version": 1,
        "repository": "edithatogo/new-drug-reimbursement-game",
        "revision": revision(),
        "generated_at": dt.datetime.now(dt.UTC).isoformat().replace("+00:00", "Z"),
        "seed": None,
        "result": "pass" if all(check["result"] == "pass" for check in checks) else "fail",
        "checks": checks,
        "artifacts": [],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(f"verification receipt: {path}")


def main() -> int:
    """Run portable Python gates and available Rust gates."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--receipt",
        type=Path,
        default=Path(".local/verification-receipt.json"),
        help="path for the repository-standards verification receipt",
    )
    args = parser.parse_args()

    commands = [
        [sys.executable, "scripts/validate_scope.py"],
        [sys.executable, "scripts/validate_data_boundaries.py"],
        [sys.executable, "scripts/validate_claim_boundaries.py"],
        [sys.executable, "scripts/validate_confidential_boundaries.py"],
        [sys.executable, "scripts/validate_empirical_readiness.py"],
        [sys.executable, "scripts/validate_t13_closeout.py"],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
        [sys.executable, "-m", "compileall", "-q", "src", "scripts", "tests"],
        [sys.executable, "scripts/discover_ecosystem.py", "--offline-fixture-mode"],
        [sys.executable, "scripts/governance_inventory.py", "--check"],
        [sys.executable, "scripts/validate_extraction.py"],
        [sys.executable, "scripts/repository_hardening.py", "--check"],
        ["ruff", "check", "."],
        ["ty", "check", "src"],
    ]
    if shutil.which("cargo"):
        commands.extend(
            [
                ["cargo", "fmt", "--all", "--", "--check"],
                ["cargo", "clippy", "--workspace", "--all-targets", "--", "-D", "warnings"],
                ["cargo", "test", "--workspace"],
            ]
        )
    checks = [run(command) for command in commands]
    write_receipt(args.receipt, checks)
    return 0 if all(check["result"] == "pass" for check in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
