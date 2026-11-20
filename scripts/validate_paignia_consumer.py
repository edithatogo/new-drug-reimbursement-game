#!/usr/bin/env python3
"""Qualify the Chapter 8 application against the retained Paignia archives on macOS."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "https://github.com/edithatogo/new-drug-reimbursement-game"
PROVIDER = "https://github.com/edithatogo/paignia"
PROFILE = "paignia/static-finite-perfect-information-sparse-zero/1.0.0"
NAMES = ("paignia-core", "paignia-solve")
CRATE = Path("crates/new-drug-reimbursement-game")
TEST_TARGET = "paignia_chapter8_application"
EVIDENCE_PATH = "docs/validation/receipts/t17-reimbursement-chapter8.log"
SANDBOX = """(version 1)
(allow default)
(deny network*)
(deny file-read* (subpath (param "PROVIDER")) (subpath (param "CARGO_GIT")))
(deny file-read-data file-map-executable
    (require-all (require-any (subpath "/Users") (subpath "/Volumes"))
                 (require-not (subpath (param "STAGE")))
                 (require-not (subpath (param "TOOLCHAIN")))))
(deny file-write*
    (require-all (require-not (subpath (param "STAGE")))
                 (require-not (literal "/dev/null"))))
"""


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verified_file(path: Path, expected_hash: str) -> Path:
    if sha256(path) != expected_hash:
        raise ValueError(f"SHA-256 mismatch for {path}")
    return path


def verify_and_unpack(provider: Path, handoff: dict, archives: Path, stage: Path) -> dict:
    if handoff["semantic_profile"] != PROFILE or handoff["scope"] != (
        "qualified-application-handoff-bundle"
    ):
        raise ValueError("unsupported provider handoff scope or profile")
    references = {}
    for field in ("package_receipt", "profile_contract"):
        entry = handoff[field]
        path = (provider / entry["path"]).resolve()
        if not path.is_relative_to(provider):
            raise ValueError(f"{field} must be inside the provider checkout")
        references[field] = verified_file(path, entry["sha256"])
    package = json.loads(references["package_receipt"].read_text())
    if (
        package["provider_revision"] != handoff["provider_revision"]
        or package["provider_tree_sha"] != handoff["provider_tree_sha"]
        or package["rustc_version"] != handoff["selected_compiler"]
        or package["provider_worktree_dirty"] is not False
    ):
        raise ValueError("package receipt and handoff describe different provider inputs")
    result = {}
    retained = stage / "archives"
    retained.mkdir()
    for name in NAMES:
        entry = package["artifacts"][name]
        if entry["archive_sha256"] != handoff["artifacts"][name]:
            raise ValueError(f"handoff and package receipt disagree for {name}")
        folder = f"{name}-{entry['version']}"
        archive = retained / f"{folder}.crate"
        shutil.copyfile(archives / archive.name, archive)
        verified_file(archive, entry["archive_sha256"])
        with tarfile.open(archive) as source:
            source.extractall(stage / "packages", filter="data")
        result[name] = (stage / "packages" / folder, entry["version"])
    return result


def stage_application(application: Path, revision: str, artifacts: dict) -> dict:
    manifest = application / CRATE / "Cargo.toml"
    text = manifest.read_text()
    dependencies = tomllib.loads(text)["dependencies"]
    for name, (package, version) in artifacts.items():
        if dependencies.get(name) != {"git": PROVIDER, "rev": revision, "version": version}:
            raise ValueError(f"unexpected development dependency on {name}")
        path = json.dumps(os.path.relpath(package, manifest.parent))
        replacement = (
            f'{name} = {{ path = {path}, version = "={version}", default-features = false }}'
        )
        text, count = re.subn(
            rf"^{name} = .*$",
            lambda _, line=replacement: line,
            text,
            flags=re.MULTILINE,
        )
        if count != 1:
            raise ValueError(f"expected one declaration for {name}")
    manifest.write_text(text)
    workspace = application / "Cargo.toml"
    path = json.dumps(os.path.relpath(artifacts["paignia-core"][0], application))
    with workspace.open("a") as stream:
        stream.write(f"\n[patch.crates-io]\npaignia-core = {{ path = {path} }}\n")
    return tomllib.loads((application / "Cargo.lock").read_text())


def stage_registry(registry: Path, cargo_home: Path, lock: dict) -> None:
    """Stage only locked published crate bytes plus their sparse index metadata."""
    locked = [entry for entry in lock["package"] if "checksum" in entry]
    names = [(f"{entry['name']}-{entry['version']}.crate", entry["checksum"]) for entry in locked]
    staged = False
    for cache in sorted((registry / "cache").glob("index.crates.io-*")):
        index = registry / "index" / cache.name
        if not (index / ".cache").is_dir() or not all(
            (cache / name).is_file() for name, _ in names
        ):
            continue
        destination = cargo_home / "registry" / "cache" / cache.name
        destination.mkdir(parents=True)
        for name, checksum in names:
            shutil.copyfile(verified_file(cache / name, checksum), destination / name)
        staged_index = cargo_home / "registry" / "index" / cache.name
        shutil.copytree(index / ".cache", staged_index / ".cache")
        shutil.copyfile(index / "config.json", staged_index / "config.json")
        staged = True
    if not staged:
        raise ValueError("the Cargo cache needs the application's locked registry archives")


def verify_resolution(metadata: dict, locked: dict, resolved: dict, artifacts: dict) -> None:
    expected = {**locked, "package": []}
    for original in locked["package"]:
        entry = original.copy()
        if entry["name"] in NAMES:
            del entry["source"]
        expected["package"].append(entry)
    if expected != resolved:
        raise ValueError("artifact resolution changed the locked dependency closure")
    packages = {entry["name"]: entry for entry in metadata["packages"]}
    if len(packages) != len(metadata["packages"]):
        raise ValueError("artifact resolution contains duplicate package names")
    nodes = {entry["id"]: entry for entry in metadata["resolve"]["nodes"]}
    ids = {}
    for name, (package, version) in artifacts.items():
        entry = packages[name]
        if (
            entry["source"] is not None
            or entry["version"] != version
            or Path(entry["manifest_path"]).resolve() != package / "Cargo.toml"
            or nodes[entry["id"]]["features"]
        ):
            raise ValueError(f"resolution did not use the default-feature-free {name} archive")
        ids[name] = entry["id"]
    application = packages[CRATE.name]["id"]
    if (
        not set(ids.values()).issubset(nodes[application]["dependencies"])
        or ids["paignia-core"] not in nodes[ids["paignia-solve"]]["dependencies"]
    ):
        raise ValueError("application and solver dependency edges do not use the paired archives")


def passing_tests(output: str) -> int:
    summaries = re.findall(r"^test result:.*$", output, re.MULTILINE)
    if len(summaries) != 1 or not re.fullmatch(
        r"test result: ok\. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; "
        r"finished in \d+\.\d+s",
        summaries[0],
    ):
        raise ValueError("expected exactly four Chapter 8 tests without failures or skips")
    return 4


def run_case(args: argparse.Namespace, stage: Path) -> None:
    provider, registry = args.provider.resolve(), args.cargo_registry.resolve()
    cargo_git = registry.parent / "git"
    if any(stage.is_relative_to(path) for path in (ROOT, provider, cargo_git)):
        raise ValueError("evidence staging must be outside the application and provider checkouts")
    handoff_path = args.handoff.resolve()
    handoff = json.loads(handoff_path.read_text())
    artifacts = verify_and_unpack(provider, handoff, args.archives.resolve(), stage)
    revision = args.revision
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("provide the full application commit SHA")
    tree = subprocess.check_output(
        ["git", "rev-parse", f"{revision}^{{tree}}"], cwd=ROOT, text=True
    )
    snapshot = stage / "application.tar"
    subprocess.run(["git", "archive", "-o", str(snapshot), revision], cwd=ROOT, check=True)
    application = stage / "application"
    with tarfile.open(snapshot) as source:
        source.extractall(application, filter="data")
    locked = stage_application(application, handoff["provider_revision"], artifacts)
    stage_registry(registry, stage / "cargo-home", locked)
    sdk = subprocess.check_output(["/usr/bin/xcrun", "--show-sdk-path"], text=True).strip()
    compiler = handoff["selected_compiler"].split()[1]
    cargo = Path(
        subprocess.check_output(
            ["rustup", "which", "--toolchain", compiler, "cargo"],
            text=True,
        ).strip()
    ).resolve()
    toolchain = cargo.parent.parent
    profile = stage / "source-isolation.sb"
    profile.write_text(SANDBOX)
    temp = stage / "tmp"
    temp.mkdir()
    env = {
        "PATH": f"{cargo.parent}:/usr/bin:/bin",
        "SDKROOT": sdk,
        "CARGO_HOME": str(stage / "cargo-home"),
        "CARGO_TARGET_DIR": str(stage / "build"),
        "CARGO_NET_OFFLINE": "true",
        "CARGO_TERM_COLOR": "never",
        "RUSTC": str(cargo.with_name("rustc")),
        "TMPDIR": str(temp),
        "LC_ALL": "C",
    }
    sandbox = [
        "/usr/bin/sandbox-exec",
        "-D",
        f"STAGE={stage}",
        "-D",
        f"PROVIDER={provider}",
        "-D",
        f"CARGO_GIT={cargo_git}",
        "-D",
        f"TOOLCHAIN={toolchain}",
        "-f",
        str(profile),
    ]
    aliases = [
        (stage, "$STAGE"),
        (provider, "$PROVIDER"),
        (cargo_git, "$CARGO_GIT"),
        (toolchain, "$TOOLCHAIN"),
        (ROOT, "$APPLICATION_CHECKOUT"),
    ]
    log = stage / "execution.log"
    commands = []

    def retain(text: str) -> str:
        for path, label in aliases:
            text = text.replace(str(path), label)
        with log.open("a") as stream:
            stream.write(text + "\n")
        return text

    def run(command: list[str], *, deny: bool = False) -> str:
        commands.append(retain("$ " + shlex.join(sandbox + command))[2:])
        result = subprocess.run(
            sandbox + command, cwd=application, env=env, capture_output=True, text=True, check=False
        )
        retain(result.stdout + result.stderr + f"exit={result.returncode}")
        if deny:
            if result.returncode != 1 or "Operation not permitted" not in result.stderr:
                raise ValueError("the sandbox did not deny the selected source read")
        else:
            result.check_returncode()
        return result.stdout

    retain(
        f"{platform.platform()} | {sys.version}\nApplication commit {revision}\n"
        f"Application tree {tree.strip()}\nApplication archive SHA-256 {sha256(snapshot)}\n"
        f"Verifier SHA-256 {sha256(Path(__file__))}\n"
        f"Provider handoff SHA-256 {sha256(handoff_path)}\n{json.dumps(handoff, indent=2)}\n"
        "Local paths use the aliases in the commands. The same sandbox wraps every command."
        f"\nWorking directory $STAGE/application\n{json.dumps(env, indent=2)}\n{SANDBOX}"
    )
    probe = provider / "README.md"
    with probe.open("rb") as source:
        if not source.read(1):
            raise ValueError("expected a readable provider README for the isolation probe")
    run(["/bin/cat", str(probe)], deny=True)
    for cached_manifest in sorted((cargo_git / "checkouts").glob("paignia-*/*/Cargo.toml")):
        run(["/bin/cat", str(cached_manifest)], deny=True)
    run(["/bin/cat", "examples/cases/chapter8_example.json"])
    run([str(cargo), "--version"])
    if run([env["RUSTC"], "--version"]).strip() != handoff["selected_compiler"]:
        raise ValueError("consumer compiler differs from the qualified package profile")
    metadata_args = [str(cargo), "metadata", "--offline", "--format-version", "1"]
    run(metadata_args)
    metadata = run([*metadata_args, "--locked"])
    lockfile = application / "Cargo.lock"
    verify_resolution(json.loads(metadata), locked, tomllib.loads(lockfile.read_text()), artifacts)
    (stage / "resolved-graph.json").write_text(metadata)
    retain(f"Resolved lock SHA-256 {sha256(lockfile)}\n{lockfile.read_text()}")
    output = run([str(cargo), "test", "--offline", "--locked", "--test", TEST_TARGET])
    count = passing_tests(output)
    retain(
        "Verified the exact application lock, both unpacked archive paths, dependency edges, "
        "and feature sets."
    )
    receipt = {
        "schema_version": 1,
        "scope": "real-application-artifact-consumer",
        "case_kind": "application-model",
        "repository": REPOSITORY,
        "revision": revision,
        "case_name": "Chapter 8 Game 1 finite reimbursement offers",
        "expected_result_basis": "Pekarsky (2015), equation 8.2. See "
        "docs/architecture/paignia-chapter8-application.md at the application revision.",
        "provider_revision": handoff["provider_revision"],
        "semantic_profile": PROFILE,
        "profile_sha256": handoff["profile_contract"]["sha256"],
        "artifacts": handoff["artifacts"],
        "result": "passed",
        "tests_passed": count,
        "tests_failed": 0,
        "tests_skipped": 0,
        "commands": commands,
        "execution_evidence": {"path": EVIDENCE_PATH, "sha256": sha256(log)},
    }
    (stage / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", required=True, type=Path)
    parser.add_argument("--handoff", required=True, type=Path)
    parser.add_argument("--archives", required=True, type=Path)
    parser.add_argument("--revision", required=True)
    parser.add_argument(
        "--work-dir",
        required=True,
        type=Path,
        help="evidence directory outside both Cargo checkouts",
    )
    parser.add_argument("--cargo-registry", type=Path, default=Path.home() / ".cargo" / "registry")
    args = parser.parse_args()
    expected = (ROOT / ".python-version").read_text().strip()
    if platform.python_implementation() != "CPython" or platform.python_version() != expected:
        parser.error(f"use the application's qualified CPython {expected} environment")
    if sys.platform != "darwin" or not Path("/usr/bin/sandbox-exec").is_file():
        parser.error("this verifier requires the macOS sandbox-exec source isolation policy")
    args.work_dir.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(dir=args.work_dir.resolve(), prefix="paignia-consumer."))
    print(f"Artifact execution evidence: {stage}", flush=True)
    try:
        run_case(args, stage)
    except (
        KeyError,
        OSError,
        ValueError,
        subprocess.CalledProcessError,
        tarfile.TarError,
    ) as error:
        print(f"Artifact qualification failed: {error}", file=sys.stderr)
        return 1
    print("Chapter 8 artifact qualification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
