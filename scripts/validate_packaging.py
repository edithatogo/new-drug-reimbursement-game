#!/usr/bin/env python3
"""Build and install the Python distribution in an isolated temporary environment."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import venv
from pathlib import Path


def run(command: list[str], *, cwd: Path) -> None:
    """Run a packaging command with no shell interpolation."""

    subprocess.run(command, cwd=cwd, check=True)


def main() -> int:
    """Build wheel/sdist, install the wheel without dependencies, and import it."""

    root = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="ndrg-package-") as temporary:
        workspace = Path(temporary)
        dist = workspace / "dist"
        run(
            [
                sys.executable,
                "-m",
                "build",
                "--outdir",
                str(dist),
                str(root),
            ],
            cwd=root,
        )
        wheels = sorted(dist.glob("*.whl"))
        source_distributions = sorted(dist.glob("*.tar.gz"))
        if len(wheels) != 1 or len(source_distributions) != 1:
            raise RuntimeError("build must produce exactly one wheel and one source distribution")
        environment = workspace / "venv"
        venv.EnvBuilder(with_pip=True, clear=True).create(environment)
        python = environment / "bin" / "python"
        pip = environment / "bin" / "pip"
        run([str(pip), "install", "--no-deps", str(wheels[0])], cwd=workspace)
        run(
            [
                str(python),
                "-c",
                (
                    "import reimbursement_game; "
                    "assert reimbursement_game.__version__ == '0.4.0'"
                ),
            ],
            cwd=workspace,
        )
    print("clean-environment packaging validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
