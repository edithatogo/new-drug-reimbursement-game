#!/usr/bin/env python3
"""Generate systematic parameter sweeps and figures for Pekarsky scenarios and games.

This script delegates to the reimbursement_game.sweeps module to create:
1. Chapter 7 Scenarios 1-4 comparative net health benefit sweeps
2. Chapter 8 Strategic Bargaining Surplus Division
3. Research Extensions (Outcomes-Based Managed Entry Settlement)
"""

from __future__ import annotations

import argparse
from pathlib import Path

from reimbursement_game.sweeps import generate_all_figures


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate scenario sweep figures")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/figures"),
        help="Target figure output directory",
    )
    args = parser.parse_args()

    paths = generate_all_figures(args.output_dir)
    print(f"Generated {len(paths)} scenario sweep figures:")
    for path in paths:
        print(f" - {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
