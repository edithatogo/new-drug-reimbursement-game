#!/usr/bin/env python3
"""Build and install the Python distribution in an isolated temporary environment."""

from __future__ import annotations

import gzip
import hashlib
import io
import os
import subprocess
import sys
import tarfile
import tempfile
import venv
from pathlib import Path


def run(command: list[str], *, cwd: Path, environment: dict[str, str] | None = None) -> None:
    """Run a packaging command with no shell interpolation."""

    subprocess.run(command, cwd=cwd, check=True, env=environment)


def sha256(path: Path) -> str:
    """Hash a built artifact."""

    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_sdist(path: Path, epoch: int) -> None:
    """Rewrite tar metadata and the gzip wrapper deterministically."""

    source = io.BytesIO(gzip.decompress(path.read_bytes()))
    target = io.BytesIO()
    with tarfile.open(fileobj=source, mode="r:") as archive:
        with tarfile.open(fileobj=target, mode="w", format=tarfile.PAX_FORMAT) as normalized:
            for member in sorted(archive.getmembers(), key=lambda item: item.name):
                content = archive.extractfile(member) if member.isfile() else None
                member.mtime = epoch
                member.uid = 0
                member.gid = 0
                member.uname = ""
                member.gname = ""
                member.pax_headers = {}
                normalized.addfile(member, content)
    path.write_bytes(gzip.compress(target.getvalue(), mtime=epoch))


def main() -> int:
    """Build wheel/sdist, install the wheel without dependencies, and import it."""

    root = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="ndrg-package-") as temporary:
        workspace = Path(temporary)
        epoch = subprocess.check_output(
            ["git", "log", "-1", "--format=%ct"], cwd=root, text=True
        ).strip()
        environment = os.environ.copy()
        environment["SOURCE_DATE_EPOCH"] = epoch
        artifacts: list[list[Path]] = []
        for name in ("first", "second"):
            dist = workspace / name
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
                environment=environment,
            )
            built = sorted([*dist.glob("*.whl"), *dist.glob("*.tar.gz")])
            if len(built) != 2:
                raise RuntimeError("build must produce exactly one wheel and one source distribution")
            for source_distribution in dist.glob("*.tar.gz"):
                normalize_sdist(source_distribution, int(epoch))
            artifacts.append(built)
        first_hashes = [(path.name, sha256(path)) for path in artifacts[0]]
        second_hashes = [(path.name, sha256(path)) for path in artifacts[1]]
        if first_hashes != second_hashes:
            raise RuntimeError(
                f"repeated builds produced different artifact hashes: "
                f"{first_hashes!r} != {second_hashes!r}"
            )
        wheels = [path for path in artifacts[0] if path.suffix == ".whl"]
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
