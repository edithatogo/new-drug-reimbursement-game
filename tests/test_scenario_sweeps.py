import tempfile
import unittest
from pathlib import Path

from scripts.generate_scenario_sweeps import generate_all_figures


class ScenarioSweepsTests(unittest.TestCase):
    def test_generate_all_figures_creates_non_empty_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out_dir = Path(temp_dir)
            paths = generate_all_figures(out_dir)
            self.assertEqual(len(paths), 3)
            for path in paths:
                self.assertTrue(path.is_file())
                self.assertGreater(path.stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()
