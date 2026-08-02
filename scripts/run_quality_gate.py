#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


def run(command: list[str]) -> int:
    """Run one quality command without hiding its output."""

    print("+", " ".join(command), flush=True)
    environment = os.environ.copy()
    source_path = str((Path.cwd() / "src").resolve())
    environment["PYTHONPATH"] = source_path + os.pathsep + environment.get("PYTHONPATH", "")
    return subprocess.run(command, check=False, env=environment).returncode


def main() -> int:
    """Run portable Python gates and available Rust gates."""

    commands = [
        [sys.executable, "scripts/validate_scope.py"],
        [sys.executable, "scripts/validate_data_boundaries.py"],
        [sys.executable, "scripts/validate_claim_boundaries.py"],
        [sys.executable, "scripts/validate_confidential_boundaries.py"],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
        [sys.executable, "-m", "compileall", "-q", "src", "scripts", "tests"],
        [sys.executable, "scripts/discover_ecosystem.py", "--offline-fixture-mode"],
        [sys.executable, "scripts/governance_inventory.py", "--check"],
        [sys.executable, "scripts/validate_extraction.py"],
        [sys.executable, "scripts/repository_hardening.py", "--check"],
    ]
    if shutil.which("cargo"):
        commands.extend(
            [
                ["cargo", "fmt", "--all", "--", "--check"],
                ["cargo", "clippy", "--workspace", "--all-targets", "--", "-D", "warnings"],
                ["cargo", "test", "--workspace"],
            ]
        )
    return max(run(command) for command in commands)


if __name__ == "__main__":
    raise SystemExit(main())
