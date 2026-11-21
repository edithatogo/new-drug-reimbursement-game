"""Verify the synthetic reimbursement pilot with an installed Voiage wheel."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from hashlib import sha256
from importlib import import_module
from importlib.metadata import version
from math import fsum
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[1]
_RECIPE = _ROOT / ("crates/new-drug-reimbursement-game/examples/reimbursement_evidence_pilot.rs")
_PROVIDER_REVISION = "bd880dd756d2ba56cc5f479bc078cea31b53c1d1"
_PACKAGE_RECEIPT = "4dedd2b14aad9ffc12e0975202c82091ff678a372bd9312bafff2b97be4e7c01"
_SPECIFICATION = "urn:ndrg:si04:synthetic-committed-offer-v1"
_INSTANCE = "urn:ndrg:si04:synthetic-two-state-instance"
_RUN = "urn:ndrg:si04:valued-policy-run"
_ANALYSIS = "si04-synthetic-committed-offer"
_BASELINE = "baseline_committed_response"
_PURPOSE = "synthetic_reimbursement_research"
_EXPECTED = {
    _BASELINE: (0.0, 0.0, 0.0, 0.0),
    "fixed_disclosed_response": (0.0, 0.0, 0.0, 0.0),
    "research_only": (0.0, 0.0, -0.75, -0.75),
    "disclosure_only": (2.0, -1.5, 0.0, 0.5),
    "research_with_disclosed_response": (2.0, -1.5, -0.75, -0.25),
}


def _encode(packet: dict[str, Any]) -> bytes:
    return json.dumps(packet, sort_keys=True, allow_nan=False, separators=(",", ":")).encode()


def _native_projection(
    report: bytes, game_digest: str
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    header, *rows = (line.split("\t") for line in report.decode().splitlines())
    schema, profile, algorithm_version, specification, instance, run, tolerance = header
    if len(rows) != 2:
        raise ValueError("the native pilot must report both evidence states")

    choices: list[dict[str, str]] = []
    worlds: list[dict[str, Any]] = []
    for world, signal, probability, payer, firm, action in rows:
        choices.append(
            {"world_id": world, "observation": signal, "native_node_id": world, "action_id": action}
        )
        worlds.append(
            {
                "world_id": world,
                "probability": float(probability),
                "signal": signal,
                "action_utilities": {
                    "withhold": {"institution": 0.0, "firm": 0.0, "sponsor": 0.0},
                    "reimburse": {"institution": float(payer), "firm": float(firm), "sponsor": 0.0},
                },
            }
        )

    projection = {
        "projection_version": "1.0.0",
        "provider_revision": _PROVIDER_REVISION,
        "package_receipt_sha256": _PACKAGE_RECEIPT,
        "game_sha256": game_digest,
        "analysis_id": _ANALYSIS,
        "design_id": "disclosure_only",
        "policy_id": "evidence_response",
        "native_player_id": "institution",
        "choices": choices,
        "native": {
            "schema_version": schema,
            "semantic_profile": profile,
            "algorithm": "paignia/backward-induction",
            "algorithm_version": algorithm_version,
            "status": "completed",
            "game_class": "finite_acyclic_extensive",
            "information_structure": "perfect_information",
            "solution_concept": "tolerance_aware_backward_induction_policy",
            "selection_rule": "input_order_pairwise_tolerance_then_lexicographic",
            "catalogue": "one_found",
            "tolerance": float(tolerance),
            "identities": {
                "specification_id": specification,
                "game_instance_id": instance,
                "solver_run_id": run,
                "session_id": None,
                "policy_artifact_id": None,
                "solver_trace_id": None,
            },
        },
    }
    return projection, worlds


def _comparison(worlds: list[dict[str, Any]]) -> dict[str, Any]:
    fixed = {
        "design_id": _BASELINE,
        "comparator_design_id": None,
        "recipients": [],
        "policy_ids": ["precommitted_reimbursement"],
        "selection_mode": "fixed",
        "selector": "agent:institution",
        "selected_policy_id": "precommitted_reimbursement",
        "transfers": [],
        "costs": [],
        "rights_receipt_ids": [],
        "blackwell_assurance": None,
        "equilibrium_receipt": None,
    }
    fixed_disclosed = {
        **fixed,
        "design_id": "fixed_disclosed_response",
        "comparator_design_id": _BASELINE,
        "recipients": ["institution"],
        "rights_receipt_ids": ["institution-consent", "sponsor-authority"],
    }
    disclosure = {
        **fixed_disclosed,
        "design_id": "disclosure_only",
        "policy_ids": ["precommitted_reimbursement", "evidence_response"],
        "selection_mode": "declared_response",
        "selected_policy_id": "evidence_response",
    }
    research_cost = [{"agent_id": "sponsor", "category": "information", "amount": 0.75}]
    return {
        "schema_version": "1.0.0",
        "analysis_id": _ANALYSIS,
        "analysis_type": "signed_social_information_value",
        "method_maturity": "experimental",
        "value_unit": "synthetic-common-monetary-unit",
        "purpose": _PURPOSE,
        "agents": [
            {"agent_id": "institution", "roles": ["decision_maker", "recipient"]},
            {"agent_id": "firm", "roles": ["stakeholder"]},
            {"agent_id": "sponsor", "roles": ["controller"]},
        ],
        "welfare": {
            "aggregator": "weighted_sum",
            "cardinal_comparability": "declared",
            "ledger_stage": "post_transfer",
            "weights": {"institution": 1.0, "firm": 1.0, "sponsor": 1.0},
            "rationale": "One declared synthetic monetary basis with equal welfare weights",
        },
        "topology": {
            "signal_id": "clinical_signal",
            "source_agent_id": "sponsor",
            "controller_agent_id": "sponsor",
            "information_scope": "private",
            "eligible_recipients": ["institution"],
            "baseline_recipients": [],
        },
        "actions": ["withhold", "reimburse"],
        "worlds": worlds,
        "policies": [
            {
                "policy_id": "precommitted_reimbursement",
                "decision_agent_id": "institution",
                "decisions": [{"observation": "unobserved", "action_id": "reimburse"}],
            },
            {
                "policy_id": "evidence_response",
                "decision_agent_id": "institution",
                "decisions": [
                    {"observation": "clinical_positive", "action_id": "reimburse"},
                    {"observation": "clinical_negative", "action_id": "withhold"},
                ],
            },
        ],
        "receipts": [
            {
                "receipt_id": "institution-consent",
                "subject_agent_id": "institution",
                "consent_status": "granted",
                "purpose": _PURPOSE,
                "legal_basis": "synthetic_consent",
                "data_scope": "clinical_signal",
            },
            {
                "receipt_id": "sponsor-authority",
                "subject_agent_id": "sponsor",
                "consent_status": "not_required",
                "purpose": _PURPOSE,
                "legal_basis": "synthetic_controller_authority",
                "data_scope": "clinical_signal",
            },
        ],
        "baseline_design_id": _BASELINE,
        "designs": [
            fixed,
            fixed_disclosed,
            {
                **fixed,
                "design_id": "research_only",
                "comparator_design_id": _BASELINE,
                "costs": research_cost,
            },
            disclosure,
            {**disclosure, "design_id": "research_with_disclosed_response", "costs": research_cost},
        ],
        "tie_policy": {"absolute_tolerance": 1e-12, "relative_tolerance": 0.0},
        "provenance": {
            "world_law_source": "Two equally likely synthetic evidence states",
            "utility_source": _SPECIFICATION,
            "policy_source": _RUN,
            "rights_source": "Synthetic consent and sponsor authority for disclosure to the institution",
        },
    }


def _one_world_benchmark(
    comparison: dict[str, Any], exact_design: str, verified_values: dict[str, float]
) -> dict[str, Any]:
    """Enumerate the outcomes of a deliberately small one-world approximation."""
    evaluator = import_module("voiage.methods.signed_social_information")
    baseline, contingent = comparison["policies"]
    exact_value = verified_values[exact_design]
    trials = []
    for world in comparison["worlds"]:
        local_policy = {
            **contingent,
            "decisions": [
                row for row in contingent["decisions"] if row["observation"] == world["signal"]
            ],
        }
        approximate = {
            **comparison,
            "worlds": [{**world, "probability": 1.0}],
            "policies": [baseline, local_policy],
        }
        evaluation = evaluator.signed_social_information_value(approximate).to_contract_dict()
        selected = evaluation["optimum"]["selected_design_id"]
        selected_value = next(
            design["signed_values"]["social"]
            for design in evaluation["designs"]
            if design["design_id"] == selected
        )
        trials.append(
            {
                "world_id": world["world_id"],
                "probability": world["probability"],
                "selected_design_id": selected,
                "wrong_design": selected != exact_design,
                "regret": exact_value - verified_values[selected],
                "absolute_value_error": abs(exact_value - selected_value),
            }
        )
    scores = {
        "wrong_design_probability": fsum(
            row["probability"] for row in trials if row["wrong_design"]
        ),
        "expected_decision_regret": fsum(row["probability"] * row["regret"] for row in trials),
        "mean_absolute_value_error": fsum(
            row["probability"] * row["absolute_value_error"] for row in trials
        ),
    }
    expected = {
        "wrong_design_probability": 0.5,
        "expected_decision_regret": 0.25,
        "mean_absolute_value_error": 0.5,
    }
    if scores != expected:
        raise ValueError(
            f"one-world approximation differs from the independent reference: {scores}"
        )
    return {"trials": trials, **scores}


def verify_pilot(report: bytes, expected_report_sha256: str) -> dict[str, Any]:
    report_digest = sha256(report).hexdigest()
    if report_digest != expected_report_sha256:
        raise ValueError("native pilot report does not match its producer digest")

    game_digest = sha256(_RECIPE.read_bytes()).hexdigest()
    projection, worlds = _native_projection(report, game_digest)
    comparison = _comparison(worlds)
    specification = _encode(comparison)
    decisions = _encode(projection)
    adapter = import_module("voiage.experimental.paignia_static_policy")
    adapter_path = Path(adapter.__file__ or "").resolve()
    if not adapter_path.is_relative_to(Path(sys.prefix).resolve()):
        raise RuntimeError("run the pilot with an installed Voiage wheel")
    binding = adapter.PaigniaStaticPolicyBinding(
        provider_revision=_PROVIDER_REVISION,
        package_receipt_sha256=_PACKAGE_RECEIPT,
        game_sha256=game_digest,
        specification_id=_SPECIFICATION,
        game_instance_id=_INSTANCE,
        solver_run_id=_RUN,
        native_player_id="institution",
        comparison_sha256=sha256(specification).hexdigest(),
        projection_sha256=sha256(decisions).hexdigest(),
    )
    result = adapter.value_paignia_static_policy(
        specification, decisions, binding
    ).to_contract_dict()
    observed = {
        item["design_id"]: (
            item["signed_values"]["by_agent"]["institution"],
            item["signed_values"]["by_agent"]["firm"],
            item["signed_values"]["by_agent"]["sponsor"],
            item["signed_values"]["social"],
        )
        for item in result["designs"]
    }
    if observed != _EXPECTED or result["optimum"]["selected_design_id"] != "disclosure_only":
        raise ValueError(
            f"the pilot differs from the independent contingent-offer ledger: {observed}"
        )
    return {
        "case": _ANALYSIS,
        "native_report_sha256": report_digest,
        "provider_binding": asdict(binding),
        "voiage_version": version("voiage"),
        "voiage_adapter_sha256": sha256(adapter_path.read_bytes()).hexdigest(),
        "comparison": comparison,
        "one_world_benchmark": _one_world_benchmark(
            comparison,
            result["optimum"]["selected_design_id"],
            {design: values[3] for design, values in observed.items()},
        ),
        "policy_projection": json.loads(decisions),
        "result": result,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("native_report", type=Path)
    parser.add_argument("native_report_sha256", help="SHA-256 from the trusted native execution")
    args = parser.parse_args()
    print(
        json.dumps(
            verify_pilot(args.native_report.read_bytes(), args.native_report_sha256), indent=2
        )
    )


if __name__ == "__main__":
    main()
