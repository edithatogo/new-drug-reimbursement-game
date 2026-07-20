import json
from pathlib import Path
import tomllib
import unittest


class ScopeTests(unittest.TestCase):
    def test_no_disallowed_runtime_dependencies(self) -> None:
        project = tomllib.loads(Path("pyproject.toml").read_text())
        dependencies = " ".join(project["project"].get("dependencies", [])).lower()
        for name in ("nashpy", "gambit", "pygambit", "open_spiel", "openspiel", "bcea", "heemod", "dampack"):
            self.assertNotIn(name, dependencies)

    def test_hf_manifest_is_owner_scoped(self) -> None:
        manifest = Path("hf/manifest.yaml").read_text()
        for line in manifest.splitlines():
            if line.strip().startswith("- id:"):
                repo_id = line.split(":", 1)[1].strip()
                self.assertTrue(repo_id.startswith("edithatogo/"))

    def test_ontology_cites_source_without_book_file(self) -> None:
        ontology = Path("ontology/new-drug-reimbursement-game.ttl").read_text()
        self.assertIn("10.1007/978-3-319-08903-4", ontology)
        forbidden_extensions = {".pdf", ".epub", ".mobi"}
        self.assertFalse(any(path.suffix.lower() in forbidden_extensions for path in Path(".").rglob("*")))

    def test_ecosystem_lock_pins_owned_repositories(self) -> None:
        lock = tomllib.loads(Path("ecosystem.lock.toml").read_text())
        repositories = [item["repository"] for item in lock["component"]]
        self.assertTrue(all("github.com/edithatogo/" in repo for repo in repositories))


if __name__ == "__main__":
    unittest.main()
