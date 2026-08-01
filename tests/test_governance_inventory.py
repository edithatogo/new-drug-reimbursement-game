from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from types import ModuleType


def load_script() -> ModuleType:
    path = Path(__file__).parents[1] / "scripts" / "governance_inventory.py"
    spec = importlib.util.spec_from_file_location("governance_inventory", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GovernanceInventoryTests(unittest.TestCase):
    def test_repository_governance_inventory_is_valid_and_current(self) -> None:
        module = load_script()
        root = Path(__file__).parents[1]
        inventory = module.build_inventory(root)

        self.assertEqual(module.validate_inventory(inventory), [])
        self.assertEqual(inventory["project"]["python_runtime_dependencies"], [])
        self.assertIs(inventory["provenance"]["network_resolution"], False)
        self.assertEqual(
            module.encoded(inventory),
            (root / module.OUTPUT).read_text(encoding="utf-8"),
        )

    def test_reconciled_voiage_licence_is_not_left_open(self) -> None:
        module = load_script()
        inventory = module.build_inventory(Path(__file__).parents[1])

        self.assertEqual(inventory["open_decisions"], [])
        voiage = next(item for item in inventory["ecosystem"] if item["name"] == "Voiage")
        self.assertEqual(voiage["license_decision"], "Apache-2.0 (LICENSE, README, and package metadata aligned at pinned revision)")
