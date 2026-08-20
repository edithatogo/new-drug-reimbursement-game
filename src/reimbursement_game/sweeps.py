"""Systematic scenario sweep and analytical figure generation.

This module provides data generation and plotting helpers for:
1. Chapter 7 Scenarios 1-4 comparative net health benefit frontiers.
2. Chapter 8 Game 1 strategic bargaining surplus division.
3. Research extensions for outcomes-based managed entry agreements.
"""

from __future__ import annotations

from pathlib import Path

from .application_games import solve_game1_bargaining
from .chapter7 import (
    Scenario1Inputs,
    Scenario2Inputs,
    Scenario3Inputs,
    Scenario4Inputs,
    evaluate_chapter7_scenario,
)
from .research_extensions import settle_managed_entry


def generate_chapter7_comparison_figure(output_path: Path) -> None:
    """Generate Figure 1: Chapter 7 Scenarios 1-4 Net Health Benefit Sweeps."""
    try:
        import matplotlib
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("matplotlib and numpy are required to generate sweep figures") from exc

    matplotlib.use("Agg")

    costs = np.linspace(5000, 60000, 200)
    delta_h = 1.0  # 1 QALY incremental gain
    rev = "2026-08-20-synthetic-sweep"

    # Base parameters reflecting standard NHS / health economic scales
    n_expansion = 20000.0    # Expansion ICER (Scenario 1 & 3)
    n_efficient = 30000.0    # Expansion ICER for Scenario 2 (where n = m)
    m_contraction = 30000.0  # Contraction ICER
    d_displacement = 25000.0 # Displacement ICER
    mu_invest = 15000.0      # Investment ICER
    phi_pv = 1.25            # Present value multiplier

    s1_nebh = [
        evaluate_chapter7_scenario(
            Scenario1Inputs(
                incremental_cost=float(c),
                incremental_health_effect=delta_h,
                expansion_icer=n_expansion,
                evidence_revision=rev,
            )
        ).nebh
        for c in costs
    ]

    s2_nebh = [
        evaluate_chapter7_scenario(
            Scenario2Inputs(
                incremental_cost=float(c),
                incremental_health_effect=delta_h,
                expansion_icer=n_efficient,
                contraction_icer=m_contraction,
                displacement_icer=d_displacement,
                evidence_revision=rev,
            )
        ).nebh
        for c in costs
    ]

    s3_nebh = [
        evaluate_chapter7_scenario(
            Scenario3Inputs(
                incremental_cost=float(c),
                incremental_health_effect=delta_h,
                expansion_icer=n_expansion,
                contraction_icer=m_contraction,
                displacement_icer=d_displacement,
                evidence_revision=rev,
            )
        ).nebh
        for c in costs
    ]

    s4_nebh = [
        evaluate_chapter7_scenario(
            Scenario4Inputs(
                incremental_cost=float(c),
                incremental_health_effect=delta_h,
                contraction_icer=m_contraction,
                displacement_icer=d_displacement,
                investment_icer=mu_invest,
                present_value_multiplier=phi_pv,
                annual_program_health_effect=float(c) / (mu_invest * phi_pv),
                evidence_revision=rev,
            )
        ).nebh
        for c in costs
    ]

    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ax.plot(costs, s1_nebh, label="Scenario 1: Expandable Efficient", color="#1f77b4", linewidth=2)
    ax.plot(costs, s2_nebh, label="Scenario 2: Fixed Efficient", color="#ff7f0e", linewidth=2)
    ax.plot(costs, s3_nebh, label="Scenario 3: Fixed Allocative Inefficiency", color="#2ca02c", linewidth=2)
    ax.plot(costs, s4_nebh, label="Scenario 4: Fixed Technical Investment", color="#d62728", linewidth=2, linestyle="--")

    ax.axhline(0, color="gray", linestyle=":", linewidth=1, label="Indifference (NEBH = 0)")
    ax.set_title("Pekarsky Chapter 7: Net Health Benefit across Budget Scenarios", fontsize=12, fontweight="bold")
    ax.set_xlabel("Incremental Cost (£)", fontsize=10)
    ax.set_ylabel("Net Economic Benefit to Health (QALYs)", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(frameon=True, fontsize=9)
    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path)
    plt.close(fig)


def generate_game_equilibria_figure(output_path: Path) -> None:
    """Generate Figure 2: Game 1 Strategic Bargaining Surplus Division."""
    try:
        import matplotlib
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("matplotlib and numpy are required to generate sweep figures") from exc

    matplotlib.use("Agg")

    threshold = 30000.0
    delta_h = 2.0
    bargaining_shares = np.linspace(0.0, 1.0, 101)

    firm_rents: list[float] = []
    institution_benefits: list[float] = []

    for share in bargaining_shares:
        result = solve_game1_bargaining(
            threshold=threshold,
            incremental_effect=delta_h,
            bargaining_share=float(share),
        )
        firm_rents.append(result.firm_rent)
        institution_benefits.append(result.institution_nebh)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ax.plot(bargaining_shares, firm_rents, label="Manufacturer Economic Rent (£)", color="#9467bd", linewidth=2)
    ax.plot(bargaining_shares, institution_benefits, label="Health System Net Benefit (£-equiv)", color="#17becf", linewidth=2)

    ax.set_title("Pekarsky Game 1: Surplus Division by Manufacturer Bargaining Power", fontsize=12, fontweight="bold")
    ax.set_xlabel("Manufacturer Bargaining Share (alpha)", fontsize=10)
    ax.set_ylabel("Surplus Value (£)", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(frameon=True, fontsize=9)
    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path)
    plt.close(fig)


def generate_ced_valuation_figure(output_path: Path) -> None:
    """Generate Figure 3: Outcomes-Based Managed Entry Agreement Settlement."""
    try:
        import matplotlib
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("matplotlib and numpy are required to generate sweep figures") from exc

    matplotlib.use("Agg")

    list_price = 50000.0
    rebate_rates = np.linspace(0.0, 0.6, 50)

    net_prices_passed: list[float] = []
    net_prices_failed: list[float] = []

    for rate in rebate_rates:
        passed = settle_managed_entry(
            list_price=list_price,
            rebate_rate=float(rate),
            monitoring_passed=True,
            clawback_rate=0.2,
        )
        failed = settle_managed_entry(
            list_price=list_price,
            rebate_rate=float(rate),
            monitoring_passed=False,
            clawback_rate=0.2,
        )
        net_prices_passed.append(passed.net_price)
        net_prices_failed.append(failed.net_price)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ax.plot(rebate_rates, net_prices_passed, label="Monitoring Passed (Standard Net Price)", color="#2ca02c", linewidth=2)
    ax.plot(rebate_rates, net_prices_failed, label="Monitoring Failed (Net Price after 20% Clawback)", color="#d62728", linewidth=2, linestyle="--")

    ax.set_title("Research Extension: Outcomes-Based Managed Entry Settlement", fontsize=12, fontweight="bold")
    ax.set_xlabel("Contract Base Rebate Rate", fontsize=10)
    ax.set_ylabel("Effective Net Settlement Price (£)", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(frameon=True, fontsize=9)
    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path)
    plt.close(fig)


def generate_all_figures(output_dir: Path) -> list[Path]:
    """Generate all analytical figures and return their file paths."""
    output_dir.mkdir(parents=True, exist_ok=True)
    fig1 = output_dir / "figure1_chapter7_scenarios_frontier.png"
    fig2 = output_dir / "figure2_game_theoretic_pricing_equilibria.png"
    fig3 = output_dir / "figure3_dynamic_and_ced_valuation.png"

    generate_chapter7_comparison_figure(fig1)
    generate_game_equilibria_figure(fig2)
    generate_ced_valuation_figure(fig3)

    return [fig1, fig2, fig3]
