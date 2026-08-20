import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from reimbursement_game.cli import main
from reimbursement_game.sweeps import generate_all_figures


class ScenarioSweepsTests(unittest.TestCase):
    def test_generate_all_figures_creates_non_empty_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out_dir = Path(temp_dir)
            paths = generate_all_figures(out_dir)
            self.assertEqual(len(paths), 3)
            for path in paths:
                self.assertTrue(path.is_file())
                self.assertGreater(path.stat().st_size, 1000)

    def test_cli_sweep_command_executes_successfully(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = io.StringIO()
            with redirect_stdout(output):
                status = main(["sweep", "--output-dir", temp_dir])
            self.assertEqual(status, 0)
            value = json.loads(output.getvalue())
            self.assertEqual(value["status"], "success")
            self.assertEqual(len(value["generated_figures"]), 3)


if __name__ == "__main__":
    unittest.main()
