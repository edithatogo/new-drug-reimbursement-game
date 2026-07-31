"""Candidate-only evidence readiness for methodological calibration pilots."""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Any
from urllib.parse import urlparse

from .chapter7 import Chapter7Scenario
from .evidence import ParameterRole


class ReadinessStatus(StrEnum):
    SUPPORTED = "supported"
    CANDIDATE_ONLY = "candidate_only"
    NOT_IDENTIFIABLE = "not_identifiable"
    INCOMPATIBLE = "incompatible"


class CandidateKind(StrEnum):
    POLICY_PROXY = "policy_proxy"
    RESEARCH_ESTIMATE = "research_estimate"
    METHOD_GUIDANCE = "method_guidance"


class UncertaintyStatus(StrEnum):
    NOT_QUANTIFIED = "not_quantified"
    POINT_ONLY = "point_only"
    DISTRIBUTION_AVAILABLE = "distribution_available"


@dataclass(frozen=True, slots=True)
class PilotContext:
    jurisdiction: str
    payer: str
    budget_boundary: str
    currency_unit: str
    health_unit: str


@dataclass(frozen=True, slots=True)
class CandidateSource:
    uri: str
    sha256: str
    artifact_kind: str
    exact_location: str


@dataclass(frozen=True, slots=True)
class ParameterCandidate:
    candidate_id: str
    kind: CandidateKind
    value: float | None
    unit: str
    price_year: int | None
    study_period: str | None
    programme_id: str | None
    alignment_id: str | None
    roles_considered: tuple[ParameterRole, ...]
    estimand: str
    geographic_scope: str
    budget_scope: str
    evidence_method: str
    uncertainty_status: UncertaintyStatus
    transformation: str
    assumptions: tuple[str, ...]
    mapping_limitations: tuple[str, ...]
    approval_state: str
    source: CandidateSource


@dataclass(frozen=True, slots=True)
class CandidateDossier:
    dossier_id: str
    context: PilotContext
    candidates: tuple[ParameterCandidate, ...]


@dataclass(frozen=True, slots=True)
class RoleReadiness:
    role: ParameterRole
    status: ReadinessStatus
    considered_candidate_ids: tuple[str, ...]
    numeric_candidate_ids: tuple[str, ...]
    reason: str


@dataclass(frozen=True, slots=True)
class ScenarioReadiness:
    scenario: Chapter7Scenario
    status: ReadinessStatus
    required_roles: tuple[ParameterRole, ...]
    pending_constraints: tuple[str, ...]
    reason: str


@dataclass(frozen=True, slots=True)
class PilotReadinessReceipt:
    dossier_id: str
    dossier_revision: str
    roles: tuple[RoleReadiness, ...]
    scenarios: tuple[ScenarioReadiness, ...]
    approved_calibration_permitted: bool
    next_gate: str


_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_MAX_CANDIDATES = 256
_DOSSIER_KEYS = {"schema_version", "dossier_kind", "dossier_id", "context", "candidates"}
_CONTEXT_KEYS = {"jurisdiction", "payer", "budget_boundary", "currency_unit", "health_unit"}
_CANDIDATE_KEYS = {
    "candidate_id",
    "kind",
    "value",
    "unit",
    "price_year",
    "study_period",
    "programme_id",
    "alignment_id",
    "roles_considered",
    "estimand",
    "geographic_scope",
    "budget_scope",
    "evidence_method",
    "uncertainty_status",
    "transformation",
    "assumptions",
    "mapping_limitations",
    "approval_state",
    "source",
}
_SOURCE_KEYS = {"uri", "sha256", "artifact_kind", "exact_location"}
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


def candidate_dossier_from_mapping(value: dict[str, Any]) -> CandidateDossier:
    """Parse a strict candidate-only pilot dossier."""

    _exact_keys("candidate dossier", value, _DOSSIER_KEYS)
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise ValueError("candidate dossier requires schema_version 1")
    if value["dossier_kind"] != "parameter-evidence-candidates":
        raise ValueError("candidate dossier has an unsupported dossier_kind")
    context_value = _mapping(value, "context")
    _exact_keys("pilot context", context_value, _CONTEXT_KEYS)
    context = PilotContext(
        jurisdiction=_text(context_value, "jurisdiction"),
        payer=_text(context_value, "payer"),
        budget_boundary=_text(context_value, "budget_boundary"),
        currency_unit=_text(context_value, "currency_unit"),
        health_unit=_text(context_value, "health_unit"),
    )
    raw_candidates = value["candidates"]
    if not isinstance(raw_candidates, list) or not raw_candidates:
        raise ValueError("candidate dossier requires a non-empty candidates array")
    if len(raw_candidates) > _MAX_CANDIDATES:
        raise ValueError(f"candidate dossier cannot exceed {_MAX_CANDIDATES} records")
    candidates = tuple(_candidate_from_mapping(_object(item), context) for item in raw_candidates)
    identifiers = [candidate.candidate_id for candidate in candidates]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("candidate_id values must be unique")
    return CandidateDossier(_text(value, "dossier_id"), context, candidates)


def assess_pilot_readiness(dossier: CandidateDossier) -> PilotReadinessReceipt:
    """Assess role and scenario readiness without promoting any candidate."""

    role_receipts = []
    by_role: dict[ParameterRole, list[ParameterCandidate]] = {
        role: [] for role in ParameterRole
    }
    for candidate in dossier.candidates:
        for role in candidate.roles_considered:
            by_role[role].append(candidate)
    for role in ParameterRole:
        candidates = tuple(by_role[role])
        numeric = tuple(candidate for candidate in candidates if candidate.value is not None)
        if not candidates or not numeric:
            reason = _missing_role_reason(role, candidates)
            status = ReadinessStatus.NOT_IDENTIFIABLE
        elif any(candidate.approval_state != "candidate" for candidate in numeric):
            reason = "pilot dossiers may contain candidate records only"
            status = ReadinessStatus.INCOMPATIBLE
        else:
            uncertainty_gap = any(
                candidate.uncertainty_status is not UncertaintyStatus.DISTRIBUTION_AVAILABLE
                for candidate in numeric
            )
            reason = "Numeric candidates exist, but Atlas and health-economics approval are absent."
            if uncertainty_gap:
                reason += " At least one candidate also lacks a quantified distribution."
            status = ReadinessStatus.CANDIDATE_ONLY
        role_receipts.append(
            RoleReadiness(
                role=role,
                status=status,
                considered_candidate_ids=tuple(
                    candidate.candidate_id for candidate in candidates
                ),
                numeric_candidate_ids=tuple(candidate.candidate_id for candidate in numeric),
                reason=reason,
            )
        )
    role_status = {receipt.role: receipt.status for receipt in role_receipts}
    scenario_receipts = []
    for scenario in Chapter7Scenario:
        required = tuple(sorted(_REQUIRED_ROLES[scenario], key=lambda role: role.value))
        pending_constraints = _pending_constraints(scenario)
        statuses = {role_status[role] for role in required}
        if ReadinessStatus.INCOMPATIBLE in statuses:
            status = ReadinessStatus.INCOMPATIBLE
            reason = "At least one required role is incompatible with the candidate contract."
        elif ReadinessStatus.NOT_IDENTIFIABLE in statuses:
            status = ReadinessStatus.NOT_IDENTIFIABLE
            missing = ", ".join(
                role.value
                for role in required
                if role_status[role] is ReadinessStatus.NOT_IDENTIFIABLE
            )
            reason = f"Required roles are not identifiable: {missing}."
        elif incompatibility := _scenario_incompatibility(scenario, by_role):
            status = ReadinessStatus.INCOMPATIBLE
            reason = incompatibility
        elif ReadinessStatus.CANDIDATE_ONLY in statuses:
            status = ReadinessStatus.CANDIDATE_ONLY
            reason = "All required roles have candidates, but none are approved model evidence."
        else:
            status = ReadinessStatus.SUPPORTED
            reason = "Every required role is supported by approved compatible evidence."
        scenario_receipts.append(
            ScenarioReadiness(scenario, status, required, pending_constraints, reason)
        )
    revision = _dossier_revision(dossier)
    return PilotReadinessReceipt(
        dossier_id=dossier.dossier_id,
        dossier_revision=revision,
        roles=tuple(role_receipts),
        scenarios=tuple(scenario_receipts),
        approved_calibration_permitted=False,
        next_gate=(
            "Reimbursement Atlas and an independent health economist must review a "
            "specific decision context before any record can be promoted."
        ),
    )


def promote_candidate_dossier(_dossier: CandidateDossier) -> None:
    """Refuse automatic promotion across the Atlas/human-review boundary."""

    raise ValueError(
        "candidate evidence cannot be promoted automatically; Atlas and human approval are required"
    )


def _candidate_from_mapping(
    value: dict[str, Any], context: PilotContext
) -> ParameterCandidate:
    _exact_keys("parameter candidate", value, _CANDIDATE_KEYS)
    if _text(value, "approval_state") != "candidate":
        raise ValueError("methodological pilot records must remain candidate")
    try:
        kind = CandidateKind(_text(value, "kind"))
        uncertainty = UncertaintyStatus(_text(value, "uncertainty_status"))
    except ValueError as exc:
        raise ValueError("unsupported candidate classification") from exc
    raw_roles = value["roles_considered"]
    if not isinstance(raw_roles, list) or not raw_roles:
        raise ValueError("roles_considered must be a non-empty array")
    try:
        roles = tuple(ParameterRole(_array_text(role, "roles_considered")) for role in raw_roles)
    except ValueError as exc:
        raise ValueError("roles_considered contains an unsupported role") from exc
    if len(roles) != len(set(roles)):
        raise ValueError("roles_considered must not contain duplicates")
    if len(roles) > 1 and not set(roles) <= {
        ParameterRole.EXPANSION_ICER,
        ParameterRole.CONTRACTION_ICER,
    }:
        raise ValueError("only n and m may share one candidate record")
    raw_value = value["value"]
    number = None if raw_value is None else _number_item(raw_value, "candidate value")
    if number is None and (
        kind is not CandidateKind.METHOD_GUIDANCE
        or roles != (ParameterRole.HORIZON,)
    ):
        raise ValueError("only horizon method guidance may have a null candidate value")
    if number is not None:
        if ParameterRole.DISCOUNT_RATE in roles:
            if not 0 <= number < 1:
                raise ValueError("discount-rate candidate must be in [0, 1)")
        elif number <= 0:
            raise ValueError("candidate value must be positive")
        if ParameterRole.PRESENT_VALUE_MULTIPLIER in roles and number <= 1:
            raise ValueError("present-value multiplier candidate must be greater than 1")
        if ParameterRole.HORIZON in roles and not number.is_integer():
            raise ValueError("numeric horizon candidate must be a whole number of years")
    unit = _text(value, "unit")
    expected_units = {_role_unit(role, context) for role in roles}
    if len(expected_units) != 1:
        raise ValueError("roles_considered cannot mix roles with different units")
    expected_unit = next(iter(expected_units))
    if unit != expected_unit:
        raise ValueError(f"candidate roles require unit {expected_unit}")
    price_year_value = value["price_year"]
    if price_year_value is not None and (
        type(price_year_value) is not int or price_year_value < 1900
    ):
        raise ValueError("price_year must be null or an integer at least 1900")
    study_period = _optional_text(value, "study_period")
    programme_id = _optional_text(value, "programme_id")
    alignment_id = _optional_text(value, "alignment_id")
    source_value = _mapping(value, "source")
    _exact_keys("candidate source", source_value, _SOURCE_KEYS)
    uri = _text(source_value, "uri")
    parsed = urlparse(uri)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("candidate source URI must use absolute HTTPS")
    sha256 = _text(source_value, "sha256")
    if not _SHA256.fullmatch(sha256):
        raise ValueError("candidate source sha256 must be 64 lowercase hexadecimal characters")
    return ParameterCandidate(
        candidate_id=_text(value, "candidate_id"),
        kind=kind,
        value=number,
        unit=unit,
        price_year=price_year_value,
        study_period=study_period,
        programme_id=programme_id,
        alignment_id=alignment_id,
        roles_considered=roles,
        estimand=_text(value, "estimand"),
        geographic_scope=_text(value, "geographic_scope"),
        budget_scope=_text(value, "budget_scope"),
        evidence_method=_text(value, "evidence_method"),
        uncertainty_status=uncertainty,
        transformation=_text(value, "transformation"),
        assumptions=_text_array(value, "assumptions"),
        mapping_limitations=_text_array(value, "mapping_limitations"),
        approval_state="candidate",
        source=CandidateSource(
            uri=uri,
            sha256=sha256,
            artifact_kind=_text(source_value, "artifact_kind"),
            exact_location=_text(source_value, "exact_location"),
        ),
    )


def _missing_role_reason(
    role: ParameterRole, candidates: tuple[ParameterCandidate, ...]
) -> str:
    if role is ParameterRole.DISPLACEMENT_ICER:
        return "No source identifies the programme actually displaced by a reimbursement decision."
    if role is ParameterRole.HORIZON and candidates:
        return "NICE requires a sufficient horizon but does not supply one universal numeric horizon."
    if role in {
        ParameterRole.INVESTMENT_ICER,
        ParameterRole.PRESENT_VALUE_MULTIPLIER,
        ParameterRole.ANNUAL_PROGRAM_HEALTH_EFFECT,
    }:
        return "No reviewed source supplies the required programme-specific Scenario 4 quantity."
    return "No numeric candidate was identified for this role."


def _scenario_incompatibility(
    scenario: Chapter7Scenario,
    by_role: dict[ParameterRole, list[ParameterCandidate]],
) -> str | None:
    candidates_by_role = {
        role: tuple(candidate for candidate in candidates if candidate.value is not None)
        for role, candidates in by_role.items()
    }
    aligned_groups = _aligned_groups(candidates_by_role)
    if scenario is Chapter7Scenario.FIXED_EFFICIENT:
        compatible = False
        for group in aligned_groups.values():
            if not group.get(ParameterRole.DISPLACEMENT_ICER):
                continue
            compatible = any(
                math.isclose(_candidate_number(n), _candidate_number(m), rel_tol=1e-12)
                for n in group.get(ParameterRole.EXPANSION_ICER, ())
                for m in group.get(ParameterRole.CONTRACTION_ICER, ())
            )
            if compatible:
                break
        if not compatible:
            return "No aligned candidate combination satisfies Scenario 2's required equality n = m."
    elif scenario is Chapter7Scenario.FIXED_ALLOCATIVE_INEFFICIENCY:
        compatible = any(_scenario3_group_compatible(group) for group in aligned_groups.values())
        if not compatible:
            return "No aligned candidate combination satisfies Scenario 3's ordering n < m and n <= d <= m."
    elif scenario is Chapter7Scenario.FIXED_TECHNICAL_INVESTMENT:
        if not any(_scenario4_group_compatible(group) for group in aligned_groups.values()):
            return (
                "No aligned decision context with one investment programme satisfies "
                "Scenario 4's static ordering d <= m and mu < m."
            )
    return None


def _pending_constraints(scenario: Chapter7Scenario) -> tuple[str, ...]:
    if scenario is Chapter7Scenario.EXPANDABLE_EFFICIENT:
        return ("n requires Atlas and independent health-economics approval",)
    if scenario is Chapter7Scenario.FIXED_EFFICIENT:
        return ("d must identify actual displacement", "n = m must be established in one aligned context")
    if scenario is Chapter7Scenario.FIXED_ALLOCATIVE_INEFFICIENCY:
        return (
            "d must identify actual displacement",
            "m > n and n <= d <= m must be established in one aligned context",
        )
    return (
        "mu, phi, annual effect, horizon, and discounting must identify one investment programme",
        "m and d must align to the same decision context without being conflated with that programme",
        "a numeric horizon and time profile must be approved",
        "phi * annual_program_health_effect = incremental_cost / mu is case-specific and remains unchecked",
    )


def _candidate_number(candidate: ParameterCandidate) -> float:
    if candidate.value is None:  # pragma: no cover - filtered by caller
        raise AssertionError("numeric candidate expected")
    return candidate.value


def _aligned_groups(
    candidates_by_role: dict[ParameterRole, tuple[ParameterCandidate, ...]],
) -> dict[str, dict[ParameterRole, list[ParameterCandidate]]]:
    groups: dict[str, dict[ParameterRole, list[ParameterCandidate]]] = {}
    for role, candidates in candidates_by_role.items():
        for candidate in candidates:
            if candidate.alignment_id is None:
                continue
            groups.setdefault(candidate.alignment_id, {}).setdefault(role, []).append(candidate)
    return groups


def _scenario3_group_compatible(
    group: dict[ParameterRole, list[ParameterCandidate]],
) -> bool:
    n_values = tuple(map(_candidate_number, group.get(ParameterRole.EXPANSION_ICER, ())))
    m_values = tuple(map(_candidate_number, group.get(ParameterRole.CONTRACTION_ICER, ())))
    d_values = tuple(map(_candidate_number, group.get(ParameterRole.DISPLACEMENT_ICER, ())))
    if not n_values or not m_values or not d_values:
        return False
    minimum_n = min(n_values)
    maximum_m = max(m_values)
    return maximum_m > minimum_n and any(minimum_n <= d <= maximum_m for d in d_values)


def _scenario4_group_compatible(
    group: dict[ParameterRole, list[ParameterCandidate]],
) -> bool:
    m_values = tuple(map(_candidate_number, group.get(ParameterRole.CONTRACTION_ICER, ())))
    d_values = tuple(map(_candidate_number, group.get(ParameterRole.DISPLACEMENT_ICER, ())))
    if not m_values or not d_values:
        return False
    investment_roles = (
        ParameterRole.INVESTMENT_ICER,
        ParameterRole.PRESENT_VALUE_MULTIPLIER,
        ParameterRole.ANNUAL_PROGRAM_HEALTH_EFFECT,
        ParameterRole.HORIZON,
        ParameterRole.DISCOUNT_RATE,
    )
    programmes: dict[str, dict[ParameterRole, list[ParameterCandidate]]] = {}
    for role in investment_roles:
        for candidate in group.get(role, ()):
            if candidate.programme_id is not None:
                programmes.setdefault(candidate.programme_id, {}).setdefault(role, []).append(candidate)
    maximum_m = max(m_values)
    if min(d_values) > maximum_m:
        return False
    for programme in programmes.values():
        if not all(programme.get(role) for role in investment_roles):
            continue
        mu_values = tuple(map(_candidate_number, programme[ParameterRole.INVESTMENT_ICER]))
        if min(mu_values) < maximum_m:
            return True
    return False


def _dossier_revision(dossier: CandidateDossier) -> str:
    payload: dict[str, Any] = {
        "dossier_id": dossier.dossier_id,
        "context": {
            "jurisdiction": dossier.context.jurisdiction,
            "payer": dossier.context.payer,
            "budget_boundary": dossier.context.budget_boundary,
            "currency_unit": dossier.context.currency_unit,
            "health_unit": dossier.context.health_unit,
        },
        "candidates": [
            {
                "candidate_id": candidate.candidate_id,
                "kind": candidate.kind.value,
                "value": candidate.value,
                "unit": candidate.unit,
                "price_year": candidate.price_year,
                "study_period": candidate.study_period,
                "programme_id": candidate.programme_id,
                "alignment_id": candidate.alignment_id,
                "roles_considered": [role.value for role in candidate.roles_considered],
                "estimand": candidate.estimand,
                "geographic_scope": candidate.geographic_scope,
                "budget_scope": candidate.budget_scope,
                "evidence_method": candidate.evidence_method,
                "uncertainty_status": candidate.uncertainty_status.value,
                "transformation": candidate.transformation,
                "assumptions": list(candidate.assumptions),
                "mapping_limitations": list(candidate.mapping_limitations),
                "approval_state": candidate.approval_state,
                "source": {
                    "uri": candidate.source.uri,
                    "sha256": candidate.source.sha256,
                    "artifact_kind": candidate.source.artifact_kind,
                    "exact_location": candidate.source.exact_location,
                },
            }
            for candidate in dossier.candidates
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _role_unit(role: ParameterRole, context: PilotContext) -> str:
    if role in {
        ParameterRole.EXPANSION_ICER,
        ParameterRole.DISPLACEMENT_ICER,
        ParameterRole.CONTRACTION_ICER,
        ParameterRole.INVESTMENT_ICER,
    }:
        return f"{context.currency_unit}/{context.health_unit}"
    if role is ParameterRole.PRESENT_VALUE_MULTIPLIER:
        return "dimensionless"
    if role is ParameterRole.ANNUAL_PROGRAM_HEALTH_EFFECT:
        return f"{context.health_unit}/year"
    if role is ParameterRole.HORIZON:
        return "year"
    return "proportion/year"


def _exact_keys(label: str, value: dict[str, Any], expected: set[str]) -> None:
    missing = sorted(expected - set(value))
    unexpected = sorted(set(value) - expected)
    if missing or unexpected:
        raise ValueError(f"{label} fields mismatch; missing={missing}, unexpected={unexpected}")


def _mapping(value: dict[str, Any], field: str) -> dict[str, Any]:
    item = value[field]
    if not isinstance(item, dict):
        raise ValueError(f"{field} must be an object")
    return item


def _object(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("candidate records must be objects")
    return value


def _text(value: dict[str, Any], field: str) -> str:
    item = value[field]
    if not isinstance(item, str) or not item.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return item


def _optional_text(value: dict[str, Any], field: str) -> str | None:
    item = value[field]
    if item is None:
        return None
    if not isinstance(item, str) or not item.strip():
        raise ValueError(f"{field} must be null or a non-empty string")
    return item


def _array_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} entries must be non-empty strings")
    return value


def _text_array(value: dict[str, Any], field: str) -> tuple[str, ...]:
    items = value[field]
    if not isinstance(items, list) or not items:
        raise ValueError(f"{field} must be a non-empty string array")
    return tuple(_array_text(item, field) for item in items)


def _number_item(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be a JSON number or null")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{field} must be finite")
    return number
