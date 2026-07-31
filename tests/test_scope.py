import subprocess
import tomllib
import unittest
from pathlib import Path


class ScopeTests(unittest.TestCase):
    def test_no_disallowed_runtime_dependencies(self) -> None:
        project = tomllib.loads(Path("pyproject.toml").read_text())
        dependencies = " ".join(project["project"].get("dependencies", [])).lower()
        for name in (
            "nashpy",
            "gambit",
            "pygambit",
            "open_spiel",
            "openspiel",
            "bcea",
            "heemod",
            "dampack",
        ):
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
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            check=True,
            capture_output=True,
            text=True,
        )
        tracked_files = (Path(name) for name in result.stdout.split("\0") if name)
        self.assertFalse(any(path.suffix.lower() in forbidden_extensions for path in tracked_files))

    def test_ecosystem_lock_pins_owned_repositories(self) -> None:
        lock = tomllib.loads(Path("ecosystem.lock.toml").read_text())
        repositories = [item["repository"] for item in lock["component"]]
        self.assertTrue(all("github.com/edithatogo/" in repo for repo in repositories))

    def test_dimensional_derivation_records_source_and_scope_boundary(self) -> None:
        ledger = Path("docs/research/dimensional-derivation-ledger.md").read_text()
        normalized = " ".join(ledger.split())
        self.assertIn("10.1007/978-3-319-08903-4", ledger)
        self.assertIn("Chapter 7", ledger)
        self.assertIn("NEBhR = Delta E - Delta C / d - Delta C * g*", ledger)
        self.assertIn(
            "8455ad153cf5b6c1570bfc945108efe659904b3c8f89fdf7b74b88c9523c4848",
            ledger,
        )
        self.assertIn("Source fidelity passes for Scenarios 1–3", normalized)
        self.assertIn("Scenario 4 identities against the 2012 Appendix 5", normalized)
        self.assertIn(
            "10b727b52872483ac60f3958c9e4dd2c6fba2d1e875b1fac5cd9d52469341723",
            ledger,
        )


if __name__ == "__main__":
    unittest.main()
