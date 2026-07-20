#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys


def run(command: list[str]) -> int:
    print("+", " ".join(command))
    return subprocess.run(command, check=False).returncode


def main() -> int:
    commands = [
        [sys.executable, "scripts/validate_scope.py"],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
        [sys.executable, "-m", "compileall", "-q", "src", "scripts", "tests"],
    ]
    if shutil.which("cargo"):
        commands.append(["cargo", "test", "--workspace"])
    return max(run(command) for command in commands)


if __name__ == "__main__":
    raise SystemExit(main())
