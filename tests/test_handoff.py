from __future__ import annotations

from pathlib import Path
import tomllib
import unittest


class HandoffContractTests(unittest.TestCase):
    def test_activation_prompt_chains_into_implementation(self) -> None:
        prompt = Path("CODEX_REPOSITORY_ACTIVATION_PROMPT.md").read_text(encoding="utf-8")
        self.assertIn("CODEX_IMPLEMENTATION_PROMPT.md", prompt)
        self.assertIn("edithatogo/new-drug-reimbursement-game", prompt)
        self.assertIn("codex/ecosystem-integration", prompt)
        self.assertIn("Do not conclude after repository setup", prompt)

    def test_version_surfaces_are_synchronized(self) -> None:
        project = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual(project["project"]["version"], "0.4.0")
        package_init = Path("src/reimbursement_game/__init__.py").read_text(encoding="utf-8")
        self.assertIn('__version__ = "0.4.0"', package_init)
        citation = Path("CITATION.cff").read_text(encoding="utf-8")
        self.assertIn("version: 0.4.0", citation)

    def test_conductor_tracks_map_to_implementation_workstreams(self) -> None:
        tracks = Path("conductor/tracks.yaml").read_text(encoding="utf-8")
        for track_id in ("T00", "T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08", "T09"):
            self.assertIn(f"id: {track_id}", tracks)


if __name__ == "__main__":
    unittest.main()
