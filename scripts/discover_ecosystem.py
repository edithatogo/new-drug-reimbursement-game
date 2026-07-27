#!/usr/bin/env python3
"""Discover owner-controlled ecosystem checkouts without mutating them.

The local manifest is intentionally ignored because it contains machine-specific
absolute paths. The generated Markdown report is portable and safe to commit.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import subprocess
import sys
import tomllib
from typing import Iterable, Sequence
from urllib.parse import urlparse

SKIP_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "target",
    "__pycache__",
    ".cache",
    ".cargo",
    ".rustup",
    ".npm",
    ".pnpm-store",
    ".yarn",
    "Library",
    "AppData",
}
DEFAULT_MAX_DEPTH = 4


@dataclass(frozen=True)
class Component:
    """An ecosystem component pinned by ``ecosystem.lock.toml``."""

    name: str
    repository: str
    revision: str
    role: str
    license: str
    integration: str

    @property
    def slug(self) -> str:
        """Return the repository basename without a ``.git`` suffix."""

        return normalized_repo_parts(self.repository)[1]


@dataclass(frozen=True)
class Candidate:
    """Observed state of a local Git checkout."""

    path: str
    remote: str
    normalized_remote: str
    head: str
    branch: str
    clean: bool
    pin_available: bool
    head_matches_pin: bool
    bare: bool
    source: str
    distance: int

    @property
    def score(self) -> tuple[int, int, int, int, int]:
        """Rank exact, pinned, clean, non-bare, nearby clones in that order."""

        return (
            1 if self.normalized_remote else 0,
            1 if self.pin_available else 0,
            1 if self.clean else 0,
            1 if not self.bare else 0,
            -self.distance,
        )


@dataclass(frozen=True)
class Selection:
    """Discovery result for one component."""

    component: Component
    candidate: Candidate | None
    status: str
    ambiguity: tuple[str, ...] = ()


def run_git(path: Path, args: Sequence[str], *, check: bool = False) -> subprocess.CompletedProcess[str]:
    """Run Git against ``path`` and return captured UTF-8 text."""

    command = ["git", "-C", str(path), *args]
    return subprocess.run(
        command,
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def normalize_remote(remote: str) -> str:
    """Normalize common GitHub HTTPS and SSH remote syntaxes."""

    value = remote.strip()
    if not value:
        return ""
    if value.startswith("git@github.com:"):
        value = "https://github.com/" + value.split(":", 1)[1]
    elif value.startswith("ssh://"):
        parsed = urlparse(value)
        host = (parsed.hostname or "").lower()
        path = parsed.path.lstrip("/")
        value = f"https://{host}/{path}"
    elif value.startswith("git://"):
        parsed = urlparse(value)
        value = f"https://{(parsed.hostname or '').lower()}/{parsed.path.lstrip('/')}"
    elif "://" not in value and value.count("/") == 1:
        value = "https://github.com/" + value

    parsed = urlparse(value)
    if not parsed.netloc:
        return value.removesuffix(".git").rstrip("/").lower()
    host = parsed.netloc.lower()
    path = parsed.path.strip("/").removesuffix(".git")
    return f"https://{host}/{path}".lower()


def normalized_repo_parts(repository: str) -> tuple[str, str]:
    """Return normalized GitHub owner and repository names."""

    normalized = normalize_remote(repository)
    parts = urlparse(normalized).path.strip("/").split("/")
    if len(parts) < 2:
        raise ValueError(f"invalid repository URL: {repository}")
    return parts[-2], parts[-1]


def load_components(lock_path: Path) -> list[Component]:
    """Read and validate ecosystem component pins."""

    payload = tomllib.loads(lock_path.read_text(encoding="utf-8"))
    raw_components = payload.get("component", [])
    if not isinstance(raw_components, list) or not raw_components:
        raise ValueError("ecosystem.lock.toml has no [[component]] entries")

    components: list[Component] = []
    for raw in raw_components:
        revision = str(raw["revision"])
        if len(revision) != 40 or any(character not in "0123456789abcdef" for character in revision):
            raise ValueError(f"{raw['name']} does not use a full lowercase commit SHA")
        repository = str(raw["repository"])
        owner, _ = normalized_repo_parts(repository)
        if owner.lower() != "edithatogo":
            raise ValueError(f"component is not owner-controlled: {repository}")
        components.append(
            Component(
                name=str(raw["name"]),
                repository=repository,
                revision=revision,
                role=str(raw.get("role", "")),
                license=str(raw.get("license", "")),
                integration=str(raw.get("integration", "")),
            )
        )
    return components


def candidate_roots(repo_root: Path) -> list[Path]:
    """Return bounded, deduplicated roots that commonly contain Git clones."""

    home = Path.home()
    roots = [
        repo_root.parent,
        repo_root.parent.parent,
        home / "src",
        home / "dev",
        home / "code",
        home / "projects",
        home / "repos",
        home / "GitHub",
        home / "Documents" / "GitHub",
        home / "source" / "repos",
    ]
    env_value = os.environ.get("NDRG_ECOSYSTEM_ROOTS", "")
    if env_value:
        roots.extend(Path(item).expanduser() for item in env_value.split(os.pathsep) if item.strip())

    result: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        try:
            resolved = root.expanduser().resolve()
        except OSError:
            continue
        marker = os.path.normcase(str(resolved))
        if (
            marker in seen
            or not resolved.exists()
            or not resolved.is_dir()
            or resolved.parent == resolved
        ):
            continue
        seen.add(marker)
        result.append(resolved)
    return result


def iter_git_roots(root: Path, *, max_depth: int = DEFAULT_MAX_DEPTH) -> Iterable[Path]:
    """Yield Git worktree roots below ``root`` without traversing large caches."""

    root = root.resolve()
    for current, directories, _files in os.walk(root):
        current_path = Path(current)
        try:
            relative_depth = len(current_path.relative_to(root).parts)
        except ValueError:
            continue
        directories[:] = [
            name
            for name in directories
            if name not in SKIP_DIRECTORIES and not name.startswith(".")
        ]
        if (current_path / ".git").exists():
            yield current_path
            directories[:] = []
            continue
        if relative_depth >= max_depth:
            directories[:] = []


def path_distance(repo_root: Path, candidate: Path) -> int:
    """Estimate path distance for deterministic nearest-clone ranking."""

    left = repo_root.resolve().parts
    right = candidate.resolve().parts
    common = 0
    for left_part, right_part in zip(left, right, strict=False):
        if os.path.normcase(left_part) != os.path.normcase(right_part):
            break
        common += 1
    return (len(left) - common) + (len(right) - common)


def inspect_candidate(path: Path, component: Component, repo_root: Path, source: str) -> Candidate | None:
    """Inspect a possible checkout and return it only for an exact remote match."""

    top_level = run_git(path, ["rev-parse", "--show-toplevel"])
    if top_level.returncode != 0:
        return None
    actual_path = Path(top_level.stdout.strip()).resolve()
    remote_result = run_git(actual_path, ["remote", "get-url", "origin"])
    if remote_result.returncode != 0:
        remotes = run_git(actual_path, ["remote"]).stdout.splitlines()
        remote = ""
        for remote_name in remotes:
            result = run_git(actual_path, ["remote", "get-url", remote_name])
            if normalize_remote(result.stdout) == normalize_remote(component.repository):
                remote = result.stdout.strip()
                break
    else:
        remote = remote_result.stdout.strip()

    normalized = normalize_remote(remote)
    if normalized != normalize_remote(component.repository):
        return None

    head_result = run_git(actual_path, ["rev-parse", "HEAD"])
    branch_result = run_git(actual_path, ["symbolic-ref", "--quiet", "--short", "HEAD"])
    status_result = run_git(actual_path, ["status", "--porcelain=v1", "--untracked-files=normal"])
    pin_result = run_git(actual_path, ["cat-file", "-e", f"{component.revision}^{{commit}}"])
    bare_result = run_git(actual_path, ["rev-parse", "--is-bare-repository"])

    head = head_result.stdout.strip() if head_result.returncode == 0 else ""
    return Candidate(
        path=str(actual_path),
        remote=remote,
        normalized_remote=normalized,
        head=head,
        branch=branch_result.stdout.strip() if branch_result.returncode == 0 else "DETACHED",
        clean=status_result.returncode == 0 and not status_result.stdout.strip(),
        pin_available=pin_result.returncode == 0,
        head_matches_pin=head == component.revision,
        bare=bare_result.stdout.strip().lower() == "true",
        source=source,
        distance=path_distance(repo_root, actual_path),
    )


def discover_component(
    component: Component,
    repo_root: Path,
    roots: Sequence[Path],
    *,
    max_depth: int = DEFAULT_MAX_DEPTH,
) -> Selection:
    """Discover and deterministically select one checkout for ``component``."""

    candidates: dict[str, Candidate] = {}
    local_cache = repo_root / ".local" / "ecosystem" / component.slug
    if local_cache.exists():
        candidate = inspect_candidate(local_cache, component, repo_root, "bootstrap-cache")
        if candidate:
            candidates[os.path.normcase(candidate.path)] = candidate

    for root in roots:
        direct = root / component.slug
        if direct.exists():
            candidate = inspect_candidate(direct, component, repo_root, "pre-existing")
            if candidate:
                candidates[os.path.normcase(candidate.path)] = candidate
        for checkout in iter_git_roots(root, max_depth=max_depth):
            candidate = inspect_candidate(checkout, component, repo_root, "pre-existing")
            if candidate:
                candidates[os.path.normcase(candidate.path)] = candidate

    if not candidates:
        return Selection(component=component, candidate=None, status="missing")

    ordered = sorted(candidates.values(), key=lambda item: item.score, reverse=True)
    best = ordered[0]
    tied = [item for item in ordered if item.score == best.score]
    if len(tied) > 1:
        return Selection(
            component=component,
            candidate=None,
            status="ambiguous",
            ambiguity=tuple(item.path for item in tied),
        )
    status = "resolved-at-pin" if best.head_matches_pin else "resolved"
    return Selection(component=component, candidate=best, status=status)


def clone_missing(component: Component, repo_root: Path) -> Path:
    """Clone one missing owner-controlled component into the ignored cache."""

    destination = repo_root / ".local" / "ecosystem" / component.slug
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        return destination
    subprocess.run(
        ["git", "clone", "--origin", "origin", component.repository, str(destination)],
        check=True,
    )
    fetch = run_git(destination, ["fetch", "origin", component.revision])
    if fetch.returncode != 0:
        raise RuntimeError(
            f"cloned {component.repository}, but could not fetch pinned revision {component.revision}"
        )
    return destination


def write_local_manifest(path: Path, selections: Sequence[Selection]) -> None:
    """Write a machine-specific manifest containing absolute local paths."""

    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "components": [
            {
                "name": selection.component.name,
                "repository": selection.component.repository,
                "revision": selection.component.revision,
                "status": selection.status,
                "ambiguity": list(selection.ambiguity),
                "candidate": asdict(selection.candidate) if selection.candidate else None,
            }
            for selection in selections
        ],
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_portable_report(path: Path, selections: Sequence[Selection]) -> None:
    """Write a tracked report without absolute machine paths."""

    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Ecosystem discovery report",
        "",
        "This report contains no absolute local paths. The ignored machine-readable manifest is",
        "`.local/ecosystem-paths.json`.",
        "",
        "| Component | Repository | Selection | Source | HEAD | Pin | Pin available | Clean | Branch |",
        "|---|---|---|---|---|---|---:|---:|---|",
    ]
    for selection in selections:
        candidate = selection.candidate
        if candidate is None:
            lines.append(
                f"| {selection.component.name} | `{normalize_remote(selection.component.repository)}` | "
                f"{selection.status} | — | — | `{selection.component.revision[:12]}` | no | — | — |"
            )
            continue
        lines.append(
            f"| {selection.component.name} | `{candidate.normalized_remote}` | {selection.status} | "
            f"{candidate.source} | `{candidate.head[:12]}` | `{selection.component.revision[:12]}` | "
            f"{'yes' if candidate.pin_available else 'no'} | {'yes' if candidate.clean else 'no'} | "
            f"`{candidate.branch}` |"
        )
    lines.extend(
        [
            "",
            "The selected working tree does not need to be checked out at the pin. Integrations must",
            "read or test the pinned commit explicitly and must not mutate sibling working trees.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def offline_fixture_check(components: Sequence[Component]) -> int:
    """Validate lock parsing and normalization without claiming clones exist."""

    failures: list[str] = []
    for component in components:
        normalized = normalize_remote(component.repository)
        owner, repository = normalized_repo_parts(component.repository)
        if owner != "edithatogo" or not repository or not normalized.startswith("https://github.com/"):
            failures.append(component.name)
    if failures:
        print("offline ecosystem contract validation failed:", ", ".join(failures))
        return 1
    print(f"offline ecosystem contract validation passed ({len(components)} components; clones not asserted)")
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--lock", type=Path, default=Path("ecosystem.lock.toml"))
    parser.add_argument("--json", action="store_true", help="print the local manifest payload")
    parser.add_argument("--check", action="store_true", help="fail unless every component and pin resolves")
    parser.add_argument("--clone-missing", action="store_true", help="clone unresolved components into .local")
    parser.add_argument("--offline-fixture-mode", action="store_true")
    parser.add_argument("--max-depth", type=int, default=DEFAULT_MAX_DEPTH)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Discover checkouts, optionally clone missing ones, and write manifests."""

    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    lock_path = args.lock if args.lock.is_absolute() else repo_root / args.lock
    try:
        components = load_components(lock_path)
    except (OSError, KeyError, TypeError, ValueError, tomllib.TOMLDecodeError) as error:
        print(f"ecosystem lock validation failed: {error}", file=sys.stderr)
        return 2

    if args.offline_fixture_mode:
        return offline_fixture_check(components)

    roots = candidate_roots(repo_root)
    selections = [
        discover_component(component, repo_root, roots, max_depth=args.max_depth)
        for component in components
    ]

    if args.clone_missing:
        for selection in selections:
            if selection.status == "missing":
                try:
                    clone_missing(selection.component, repo_root)
                except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
                    print(f"clone failed for {selection.component.name}: {error}", file=sys.stderr)
                    return 3
        roots = candidate_roots(repo_root)
        selections = [
            discover_component(component, repo_root, roots, max_depth=args.max_depth)
            for component in components
        ]

    local_manifest = repo_root / ".local" / "ecosystem-paths.json"
    portable_report = repo_root / "docs" / "generated" / "ecosystem-discovery.md"
    write_local_manifest(local_manifest, selections)
    write_portable_report(portable_report, selections)

    payload = json.loads(local_manifest.read_text(encoding="utf-8"))
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for selection in selections:
            candidate = selection.candidate
            if candidate:
                print(
                    f"{selection.component.name}: {selection.status}; {candidate.path}; "
                    f"HEAD={candidate.head[:12]}; pin={'yes' if candidate.pin_available else 'no'}; "
                    f"clean={'yes' if candidate.clean else 'no'}"
                )
            else:
                print(f"{selection.component.name}: {selection.status}")

    if args.check:
        unresolved = [
            selection
            for selection in selections
            if selection.candidate is None or not selection.candidate.pin_available
        ]
        if unresolved:
            print("ecosystem discovery check failed:", file=sys.stderr)
            for selection in unresolved:
                detail = ", ".join(selection.ambiguity) if selection.ambiguity else selection.status
                print(f"- {selection.component.name}: {detail}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
