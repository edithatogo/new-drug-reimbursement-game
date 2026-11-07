from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "paignia_consumer_guard", ROOT / "scripts/validate_extraction.py"
)
assert SPEC is not None and SPEC.loader is not None
GUARD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GUARD)


def copy_contract(destination: Path) -> None:
    for name in (
        "Cargo.toml",
        "Cargo.lock",
        "extraction-manifest.json",
        "ecosystem.lock.toml",
        "crates/new-drug-reimbursement-game/Cargo.toml",
    ):
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, target)


class PaigniaDependencyTests(unittest.TestCase):
    def test_current_immutable_provider_contract_passes(self) -> None:
        self.assertEqual(GUARD.validate_provider(ROOT), [])

    def test_duplicate_local_core_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            copy_contract(root)
            (root / "crates/paignia-core").mkdir()
            errors = GUARD.validate_provider(root)
            self.assertTrue(any("parallel local game core" in error for error in errors))

    def test_mutable_git_branch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            copy_contract(root)
            provider = json.loads((root / "extraction-manifest.json").read_text())["provider"]
            path = root / "crates/new-drug-reimbursement-game/Cargo.toml"
            path.write_text(
                path.read_text().replace(f'rev = "{provider["revision"]}"', 'branch = "main"')
            )
            errors = GUARD.validate_provider(root)
            self.assertTrue(any("immutable git+rev" in error for error in errors))

    def test_alternate_path_provider_workspace_member_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            copy_contract(root)
            parallel = root / "crates/parallel-game-core"
            parallel.mkdir()
            (parallel / "Cargo.toml").write_text(
                '[package]\nname = "paignia-core"\nversion = "0.1.0"\n'
            )
            path = root / "Cargo.toml"
            path.write_text(
                path.read_text().replace(
                    '  "crates/new-drug-reimbursement-game",',
                    '  "crates/new-drug-reimbursement-game",\n'
                    '  "crates/parallel-game-core",',
                )
            )
            errors = GUARD.validate_provider(root)
            self.assertTrue(any("only its application member" in error for error in errors))

    def test_lock_source_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            copy_contract(root)
            provider = json.loads((root / "extraction-manifest.json").read_text())["provider"]
            path = root / "Cargo.lock"
            path.write_text(path.read_text().replace(f'#{provider["revision"]}', "#" + "0" * 40))
            errors = GUARD.validate_provider(root)
            self.assertTrue(any("lock source mismatch" in error for error in errors))

    def test_local_patch_override_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            copy_contract(root)
            path = root / "Cargo.toml"
            with path.open("a") as handle:
                handle.write(
                    '\n[patch."https://github.com/edithatogo/paignia"]\n'
                    'paignia-core = { path = "local-core" }\n'
                )
            errors = GUARD.validate_provider(root)
            self.assertTrue(any("patch overrides immutable source" in error for error in errors))

    def test_ecosystem_pin_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            copy_contract(root)
            provider = json.loads((root / "extraction-manifest.json").read_text())["provider"]
            path = root / "ecosystem.lock.toml"
            path.write_text(path.read_text().replace(provider["revision"], "0" * 40))
            errors = GUARD.validate_provider(root)
            self.assertTrue(any("ecosystem pin" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
