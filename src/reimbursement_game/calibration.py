"""Evidence-bound assembly of strict Chapter 7 scenario inputs and samples."""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping
from dataclasses import dataclass

from .chapter7 import (
    Chapter7Inputs,
    Chapter7Scenario,
    Chapter7ScenarioEvaluation,
    Scenario1Inputs,
    Scenario2Inputs,
    Scenario3Inputs,
    Scenario4Inputs,
    evaluate_chapter7_scenario,
)
from .evidence import EvidenceContext, EvidencePacket, ParameterEvidenceRecord, ParameterRole


@dataclass(frozen=True, slots=True)
class EvidenceReference:
    role: ParameterRole
    record_id: str
    evidence_revision: str
    source_sha256: str


@dataclass(frozen=True, slots=True)
class ParameterSamples:
    role: ParameterRole
    values: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class VoiageSampleBundle:
    """Dependency-free samples ready for Voiage schema construction."""

    strategy_names: tuple[str, str]
    net_benefit_samples: tuple[tuple[float, float], ...]
    parameter_samples: tuple[ParameterSamples, ...]
    perspective: str
    health_unit: str
    evidence_revision: str


@dataclass(frozen=True, slots=True)
class CalibrationReceipt:
    case_id: str
    scenario: Chapter7Scenario
    packet_id: str
    packet_revision: str
    evidence_revision: str
    context: EvidenceContext
    evidence: tuple[EvidenceReference, ...]
    sample_count: int
    synthetic: bool
    decision_use_permitted: bool


@dataclass(frozen=True, slots=True)
class CalibratedScenario:
    inputs: Chapter7Inputs
    evaluation: Chapter7ScenarioEvaluation
    receipt: CalibrationReceipt
    voiage_samples: VoiageSampleBundle


_REQUIRED_ROLES: dict[Chapter7Scenario, frozenset[ParameterRole]] = {
    Chapter7Scenario.EXPANDABLE_EFFICIENT: frozenset({ParameterRole.EXPANSION_ICER}),
    Chapter7Scenario.FIXED_EFFICIENT: frozenset(
        {
            ParameterRole.EXPANSION_ICER,
            ParameterRole.CONTRACTION_ICER,
            ParameterRole.DISPLACEMENT_ICER,
        }
    ),
    Chapter7Scenario.FIXED_ALLOCATIVE_INEFFICIENCY: frozenset(
        {
            ParameterRole.EXPANSION_ICER,
            ParameterRole.CONTRACTION_ICER,
            ParameterRole.DISPLACEMENT_ICER,
        }
    ),
    Chapter7Scenario.FIXED_TECHNICAL_INVESTMENT: frozenset(
        {
            ParameterRole.CONTRACTION_ICER,
            ParameterRole.DISPLACEMENT_ICER,
            ParameterRole.INVESTMENT_ICER,
            ParameterRole.PRESENT_VALUE_MULTIPLIER,
            ParameterRole.ANNUAL_PROGRAM_HEALTH_EFFECT,
            ParameterRole.HORIZON,
            ParameterRole.DISCOUNT_RATE,
        }
    ),
}


def calibrate_chapter7_scenario(
    *,
    case_id: str,
    scenario: Chapter7Scenario,
    incremental_cost: float,
    incremental_health_effect: float,
    packet: EvidencePacket,
    record_ids: Mapping[ParameterRole, str],
) -> CalibratedScenario:
    """Bind one strict scenario to an explicit set of approved evidence records."""

    if not case_id.strip():
        raise ValueError("calibration case_id must be non-empty")
    cost = _positive("incremental_cost", incremental_cost)
    effect = _positive("incremental_health_effect", incremental_health_effect)
    required = _REQUIRED_ROLES[scenario]
    if set(record_ids) != required:
        missing = sorted(role.value for role in required - set(record_ids))
        unexpected = sorted(role.value for role in set(record_ids) - required)
        raise ValueError(
            f"scenario evidence selection mismatch; missing={missing}, unexpected={unexpected}"
        )
    by_id = {record.record_id: record for record in packet.records}
    selected: dict[ParameterRole, ParameterEvidenceRecord] = {}
    for role, record_id in record_ids.items():
        if record_id not in by_id:
            raise ValueError(f"selected evidence record does not exist: {record_id}")
        record = by_id[record_id]
        if record.role is not role:
            raise ValueError(
                f"selected evidence record {record_id} has role {record.role.value}, expected {role.value}"
            )
        selected[role] = record
    if scenario is Chapter7Scenario.FIXED_TECHNICAL_INVESTMENT:
        programme_roles = {
            ParameterRole.INVESTMENT_ICER,
            ParameterRole.PRESENT_VALUE_MULTIPLIER,
            ParameterRole.ANNUAL_PROGRAM_HEALTH_EFFECT,
            ParameterRole.HORIZON,
            ParameterRole.DISCOUNT_RATE,
        }
        programmes = {selected[role].programme_id for role in programme_roles}
        if len(programmes) != 1:
            raise ValueError("Scenario 4 investment evidence must describe one programme")
    references = tuple(
        EvidenceReference(
            role=role,
            record_id=selected[role].record_id,
            evidence_revision=selected[role].evidence_revision,
            source_sha256=selected[role].source_sha256,
        )
        for role in sorted(selected, key=lambda item: item.value)
    )
    evidence_revision = _calibration_revision(
        case_id, scenario, cost, effect, packet, references
    )
    inputs = _scenario_inputs(
        scenario,
        cost,
        effect,
        {role: record.value for role, record in selected.items()},
        evidence_revision,
    )
    evaluation = evaluate_chapter7_scenario(inputs)
    sample_count = _sample_count(selected)
    expanded = {
        role: _broadcast(record.samples, sample_count) for role, record in selected.items()
    }
    strategy_samples = []
    for index in range(sample_count):
        sample_inputs = _scenario_inputs(
            scenario,
            cost,
            effect,
            {role: values[index] for role, values in expanded.items()},
            evidence_revision,
        )
        sample_evaluation = evaluate_chapter7_scenario(sample_inputs)
        strategy_samples.append(
            (
                sample_evaluation.reimbursement_health_effect,
                sample_evaluation.alternative_health_gain,
            )
        )
    synthetic = packet.context.jurisdiction == "SYNTHETIC-NOT-FOR-DECISIONS"
    receipt = CalibrationReceipt(
        case_id=case_id,
        scenario=scenario,
        packet_id=packet.packet_id,
        packet_revision=packet.packet_revision,
        evidence_revision=evidence_revision,
        context=packet.context,
        evidence=references,
        sample_count=sample_count,
        synthetic=synthetic,
        decision_use_permitted=False,
    )
    bundle = VoiageSampleBundle(
        strategy_names=("reimburse", "best_available_alternative"),
        net_benefit_samples=tuple(strategy_samples),
        parameter_samples=tuple(
            ParameterSamples(role, expanded[role])
            for role in sorted(expanded, key=lambda item: item.value)
        ),
        perspective="health",
        health_unit=packet.context.health_unit,
        evidence_revision=evidence_revision,
    )
    return CalibratedScenario(inputs, evaluation, receipt, bundle)


def _scenario_inputs(
    scenario: Chapter7Scenario,
    cost: float,
    effect: float,
    values: Mapping[ParameterRole, float],
    evidence_revision: str,
) -> Chapter7Inputs:
    if scenario is Chapter7Scenario.EXPANDABLE_EFFICIENT:
        return Scenario1Inputs(
            cost,
            effect,
            expansion_icer=values[ParameterRole.EXPANSION_ICER],
            evidence_revision=evidence_revision,
        )
    if scenario is Chapter7Scenario.FIXED_EFFICIENT:
        return Scenario2Inputs(
            cost,
            effect,
            expansion_icer=values[ParameterRole.EXPANSION_ICER],
            contraction_icer=values[ParameterRole.CONTRACTION_ICER],
            displacement_icer=values[ParameterRole.DISPLACEMENT_ICER],
            evidence_revision=evidence_revision,
        )
    if scenario is Chapter7Scenario.FIXED_ALLOCATIVE_INEFFICIENCY:
        return Scenario3Inputs(
            cost,
            effect,
            expansion_icer=values[ParameterRole.EXPANSION_ICER],
            contraction_icer=values[ParameterRole.CONTRACTION_ICER],
            displacement_icer=values[ParameterRole.DISPLACEMENT_ICER],
            evidence_revision=evidence_revision,
        )
    return Scenario4Inputs(
        cost,
        effect,
        contraction_icer=values[ParameterRole.CONTRACTION_ICER],
        displacement_icer=values[ParameterRole.DISPLACEMENT_ICER],
        investment_icer=values[ParameterRole.INVESTMENT_ICER],
        present_value_multiplier=values[ParameterRole.PRESENT_VALUE_MULTIPLIER],
        annual_program_health_effect=values[
            ParameterRole.ANNUAL_PROGRAM_HEALTH_EFFECT
        ],
        evidence_revision=evidence_revision,
    )


def _sample_count(selected: Mapping[ParameterRole, ParameterEvidenceRecord]) -> int:
    counts = {len(record.samples) for record in selected.values() if len(record.samples) > 1}
    if not counts:
        raise ValueError("Voiage handoff requires sample-based uncertainty")
    if len(counts) != 1:
        raise ValueError("selected evidence uncertainty samples must be aligned")
    return counts.pop()


def _broadcast(values: tuple[float, ...], sample_count: int) -> tuple[float, ...]:
    if len(values) == sample_count:
        return values
    if len(values) == 1:
        return values * sample_count
    raise ValueError("selected evidence uncertainty samples must be aligned")


def _calibration_revision(
    case_id: str,
    scenario: Chapter7Scenario,
    cost: float,
    effect: float,
    packet: EvidencePacket,
    references: tuple[EvidenceReference, ...],
) -> str:
    payload = {
        "case_id": case_id,
        "scenario": scenario.value,
        "incremental_cost": cost,
        "incremental_health_effect": effect,
        "packet_id": packet.packet_id,
        "packet_revision": packet.packet_revision,
        "records": [
            {
                "role": reference.role.value,
                "record_id": reference.record_id,
                "evidence_revision": reference.evidence_revision,
                "source_sha256": reference.source_sha256,
            }
            for reference in references
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _positive(name: str, value: float) -> float:
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be positive and finite")
    return value
