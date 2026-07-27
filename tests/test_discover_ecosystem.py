from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path("scripts/discover_ecosystem.py")
SPEC = importlib.util.spec_from_file_location("discover_ecosystem", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class EcosystemDiscoveryTests(unittest.TestCase):
    def test_normalize_remote_variants(self) -> None:
        expected = "https://github.com/edithatogo/voiage"
        variants = (
            "https://github.com/edithatogo/voiage.git",
            "git@github.com:edithatogo/voiage.git",
            "ssh://git@github.com/edithatogo/voiage.git",
            "git://github.com/edithatogo/voiage.git",
            "edithatogo/voiage",
        )
        for value in variants:
            with self.subTest(value=value):
                self.assertEqual(MODULE.normalize_remote(value), expected)

    def test_loads_owner_controlled_components(self) -> None:
        components = MODULE.load_components(Path("ecosystem.lock.toml"))
        self.assertEqual(
            [component.name for component in components],
            ["UOGTO", "Kairos", "Voiage", "Reimbursement Atlas"],
        )
        self.assertTrue(all(len(component.revision) == 40 for component in components))

    def test_discovers_exact_remote_and_pin(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            checkout = root / "voiage"
            checkout.mkdir()
            subprocess.run(
                ["git", "init", "-b", "main", str(checkout)], check=True, capture_output=True
            )
            subprocess.run(["git", "-C", str(checkout), "config", "user.name", "Test"], check=True)
            subprocess.run(
                ["git", "-C", str(checkout), "config", "user.email", "test@example.invalid"],
                check=True,
            )
            (checkout / "README.md").write_text("fixture\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(checkout), "add", "README.md"], check=True)
            subprocess.run(
                ["git", "-C", str(checkout), "commit", "-m", "fixture"],
                check=True,
                capture_output=True,
            )
            head = subprocess.run(
                ["git", "-C", str(checkout), "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(checkout),
                    "remote",
                    "add",
                    "origin",
                    "git@github.com:edithatogo/voiage.git",
                ],
                check=True,
            )
            component = MODULE.Component(
                name="Voiage",
                repository="https://github.com/edithatogo/voiage",
                revision=head,
                role="test",
                license="test",
                integration="test",
            )
            result = MODULE.discover_component(component, root / "application", [root], max_depth=2)
            self.assertEqual(result.status, "resolved-at-pin")
            self.assertIsNotNone(result.candidate)
            assert result.candidate is not None
            self.assertEqual(result.candidate.head, head)
            self.assertTrue(result.candidate.clean)
            self.assertTrue(result.candidate.pin_available)

    def test_offline_fixture_check_does_not_assert_local_clones(self) -> None:
        components = MODULE.load_components(Path("ecosystem.lock.toml"))
        self.assertEqual(MODULE.offline_fixture_check(components), 0)


if __name__ == "__main__":
    unittest.main()
