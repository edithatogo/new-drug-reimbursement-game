"""Controls for the isolated Chapter 8 artifact admission checks."""

import copy
import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.validate_paignia_consumer import (
    NAMES,
    PROVIDER,
    ROOT,
    application_tree,
    passing_tests,
    verified_file,
    verify_resolution,
)

PROVIDER_REVISION = "1" * 40


class ArtifactQualificationTests(unittest.TestCase):
    def test_rejects_changed_archive_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "package.crate"
            original = b"test archive bytes"
            digest = hashlib.sha256(original).hexdigest()
            archive.write_bytes(original)
            self.assertEqual(verified_file(archive, digest), archive)
            archive.write_bytes(original + b"changed")
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                verified_file(archive, digest)

    def test_application_revision_must_be_an_actual_commit(self):
        revision, tree = subprocess.check_output(
            ["git", "rev-parse", "HEAD", "HEAD^{tree}"],
            cwd=ROOT,
            text=True,
        ).splitlines()
        self.assertEqual(application_tree(revision), tree)
        with self.assertRaisesRegex(ValueError, "must name a commit object"):
            application_tree(tree)

    def test_requires_one_complete_native_summary(self):
        summary = (
            "test result: ok. 6 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; "
            "finished in 0.00s\n"
        )
        self.assertEqual(passing_tests(summary), 6)
        for bad in (
            "",
            summary * 2,
            summary.replace("6 passed", "0 passed"),
            summary.replace("0 ignored", "1 ignored"),
            summary.replace("0 failed", "1 failed"),
            summary.replace("0 filtered out", "1 filtered out"),
        ):
            with self.subTest(bad=bad), self.assertRaisesRegex(ValueError, "exactly 6"):
                passing_tests(bad)

    def test_resolution_requires_archive_paths_features_and_unchanged_registry_closure(self):
        with tempfile.TemporaryDirectory() as temporary:
            stage = Path(temporary).resolve()
            metadata, locked, resolved, archives = _resolution(stage)
            verify_resolution(metadata, locked, resolved, archives, PROVIDER_REVISION)
            for field, value in (
                ("source", "git+https://example.invalid/provider"),
                ("manifest_path", str(stage / "provider" / "Cargo.toml")),
                ("version", "0.2.0"),
            ):
                changed = copy.deepcopy(metadata)
                changed["packages"][0][field] = value
                with self.subTest(field=field), self.assertRaisesRegex(ValueError, "archive"):
                    verify_resolution(changed, locked, resolved, archives, PROVIDER_REVISION)
            changed = copy.deepcopy(metadata)
            changed["resolve"]["nodes"][1]["features"] = ["correlated-equilibrium"]
            with self.assertRaisesRegex(ValueError, "archive"):
                verify_resolution(changed, locked, resolved, archives, PROVIDER_REVISION)
            changed_lock = copy.deepcopy(resolved)
            changed_lock["package"][-1]["checksum"] = "changed"
            with self.assertRaisesRegex(ValueError, "locked dependency closure"):
                verify_resolution(metadata, locked, changed_lock, archives, PROVIDER_REVISION)

    def test_resolution_checks_both_original_lock_sources(self):
        with tempfile.TemporaryDirectory() as temporary:
            metadata, locked, resolved, archives = _resolution(Path(temporary).resolve())
            for index, name in enumerate(NAMES):
                changed_lock = copy.deepcopy(locked)
                changed_lock["package"][index]["source"] = f"git+{PROVIDER}?rev=other#other"
                with self.subTest(name=name), self.assertRaisesRegex(ValueError, "lock source"):
                    verify_resolution(metadata, changed_lock, resolved, archives, PROVIDER_REVISION)

    def test_resolution_requires_app_and_solver_to_use_the_same_core(self):
        with tempfile.TemporaryDirectory() as temporary:
            metadata, locked, resolved, archives = _resolution(Path(temporary).resolve())
            metadata["resolve"]["nodes"][1]["dependencies"] = []
            with self.assertRaisesRegex(ValueError, "dependency edges"):
                verify_resolution(metadata, locked, resolved, archives, PROVIDER_REVISION)


def _resolution(stage):
    app, version = "new-drug-reimbursement-game", "0.1.0"
    archives = {name: (stage / name, version) for name in NAMES}
    packages = [
        {
            "name": name,
            "id": name,
            "source": None,
            "version": version,
            "manifest_path": str(folder / "Cargo.toml"),
        }
        for name, (folder, version) in archives.items()
    ]
    packages.append({"name": app, "id": app})
    nodes = [
        {"id": "paignia-core", "features": [], "dependencies": ["thiserror"]},
        {"id": "paignia-solve", "features": [], "dependencies": ["paignia-core", "thiserror"]},
        {"id": app, "features": [], "dependencies": list(NAMES)},
    ]
    registry_crate = {"name": "thiserror", "version": "1.0.69", "checksum": "expected"}
    source = f"git+{PROVIDER}?rev={PROVIDER_REVISION}#{PROVIDER_REVISION}"
    locked = {
        "version": 3,
        "package": [{"name": name, "version": version, "source": source} for name in NAMES]
        + [registry_crate],
    }
    resolved = {
        "version": 3,
        "package": [{"name": name, "version": version} for name in NAMES] + [registry_crate],
    }
    return {"packages": packages, "resolve": {"nodes": nodes}}, locked, resolved, archives
