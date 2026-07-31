"""Governed parameter-evidence records for Chapter 7 calibration.

Reimbursement Atlas owns acquisition, licensing, transformation, and human
review.  This module accepts only approved derived exports and adds the
application-specific parameter-role interpretation needed by Chapter 7.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from typing import Any
from urllib.parse import urlparse


class ParameterRole(StrEnum):
    EXPANSION_ICER = "n"
    DISPLACEMENT_ICER = "d"
    CONTRACTION_ICER = "m"
    INVESTMENT_ICER = "mu"
    PRESENT_VALUE_MULTIPLIER = "phi"
    ANNUAL_PROGRAM_HEALTH_EFFECT = "annual_program_health_effect"
    HORIZON = "horizon"
    DISCOUNT_RATE = "discount_rate"


class EvidenceMethod(StrEnum):
    OBSERVED = "observed"
    ELICITED = "elicited"
    MODELLED = "modelled"
    INFERRED = "inferred"


class Marginality(StrEnum):
    MARGINAL = "marginal"
    INCREMENTAL = "incremental"
    NOT_APPLICABLE = "not_applicable"


class UncertaintyKind(StrEnum):
    DETERMINISTIC = "deterministic"
    EMPIRICAL_SAMPLES = "empirical_samples"
    POSTERIOR_SAMPLES = "posterior_samples"


@dataclass(frozen=True, slots=True)
class EvidenceContext:
    jurisdiction: str
    payer: str
    budget_boundary: str
    service_line: str
    price_year: int
    decision_date: str
    implementation_horizon_years: int
    currency_unit: str
    health_unit: str


@dataclass(frozen=True, slots=True)
class ParameterEvidenceRecord:
    record_id: str
    role: ParameterRole
    value: float
    unit: str
    programme_id: str
    evidence_method: EvidenceMethod
    marginality: Marginality
    causal_assumptions: tuple[str, ...]
    uncertainty_kind: UncertaintyKind
    samples: tuple[float, ...]
    scale_min: float
    scale_max: float
    source_uri: str
    source_sha256: str
    source_licence: str
    transformation: str
    reviewer: str
    approval_state: str
    evidence_revision: str
    derived_only: bool
    context: EvidenceContext


@dataclass(frozen=True, slots=True)
class EvidencePacket:
    packet_id: str
    packet_revision: str
    context: EvidenceContext
    records: tuple[ParameterEvidenceRecord, ...]

    def records_for_role(self, role: ParameterRole) -> tuple[ParameterEvidenceRecord, ...]:
        return tuple(record for record in self.records if record.role is role)


_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_PACKET_KEYS = {"schema_version", "export_kind", "packet_id", "packet_revision", "context", "records"}
_CONTEXT_KEYS = {
    "jurisdiction",
    "payer",
    "budget_boundary",
    "service_line",
    "price_year",
    "decision_date",
    "implementation_horizon_years",
    "currency_unit",
    "health_unit",
}
_RECORD_KEYS = {
    "record_id",
    "role",
    "value",
    "unit",
    "programme_id",
    "evidence_method",
    "marginality",
    "causal_assumptions",
    "uncertainty",
    "scale_limits",
    "source",
    "transformation",
    "reviewer",
    "approval_state",
    "evidence_revision",
    "derived_only",
}


def evidence_packet_from_mapping(value: dict[str, Any]) -> EvidencePacket:
    """Parse a strict version-1 approved-derived Atlas evidence packet."""

    _exact_keys("evidence packet", value, _PACKET_KEYS)
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise ValueError("evidence packet requires schema_version 1")
    if value["export_kind"] != "approved-derived-parameter-evidence":
        raise ValueError("evidence packet must be an approved derived parameter export")
    packet_id = _text(value, "packet_id")
    packet_revision = _revision(value, "packet_revision")
    context_value = _mapping(value, "context")
    context = _context_from_mapping(context_value)
    raw_records = value["records"]
    if not isinstance(raw_records, list) or not raw_records:
        raise ValueError("evidence packet records must be a non-empty array")
    records = tuple(
        _record_from_mapping(_record_mapping(item), context) for item in raw_records
    )
    identifiers = [record.record_id for record in records]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("evidence packet record_id values must be unique")
    return EvidencePacket(packet_id, packet_revision, context, records)


def _context_from_mapping(value: dict[str, Any]) -> EvidenceContext:
    _exact_keys("evidence context", value, _CONTEXT_KEYS)
    price_year = _integer(value, "price_year", minimum=1900)
    implementation_horizon = _integer(value, "implementation_horizon_years", minimum=1)
    decision_date = _text(value, "decision_date")
    try:
        date.fromisoformat(decision_date)
    except ValueError as exc:
        raise ValueError("decision_date must be an ISO-8601 calendar date") from exc
    return EvidenceContext(
        jurisdiction=_text(value, "jurisdiction"),
        payer=_text(value, "payer"),
        budget_boundary=_text(value, "budget_boundary"),
        service_line=_text(value, "service_line"),
        price_year=price_year,
        decision_date=decision_date,
        implementation_horizon_years=implementation_horizon,
        currency_unit=_text(value, "currency_unit"),
        health_unit=_text(value, "health_unit"),
    )


def _record_from_mapping(
    value: dict[str, Any], context: EvidenceContext
) -> ParameterEvidenceRecord:
    _exact_keys("evidence record", value, _RECORD_KEYS)
    try:
        role = ParameterRole(_text(value, "role"))
        method = EvidenceMethod(_text(value, "evidence_method"))
        marginality = Marginality(_text(value, "marginality"))
    except ValueError as exc:
        raise ValueError("evidence record contains an unsupported role or classification") from exc
    approval_state = _text(value, "approval_state")
    if approval_state != "approved":
        raise ValueError("evidence records must be explicitly approved")
    if value["derived_only"] is not True:
        raise ValueError("evidence records must be derived_only; raw records are forbidden")
    unit = _text(value, "unit")
    expected_unit, expected_marginality = _role_contract(role, context)
    if unit != expected_unit:
        raise ValueError(f"evidence role {role.value} requires unit {expected_unit}")
    if marginality is not expected_marginality:
        raise ValueError(
            f"evidence role {role.value} requires marginality {expected_marginality.value}"
        )
    point_value = _role_number(role, _number(value, "value"), "value")
    assumptions = value["causal_assumptions"]
    if not isinstance(assumptions, list) or not assumptions:
        raise ValueError("causal_assumptions must be a non-empty string array")
    causal_assumptions = tuple(_array_text(item, "causal_assumptions") for item in assumptions)
    uncertainty = _mapping(value, "uncertainty")
    _exact_keys("uncertainty", uncertainty, {"kind", "samples"})
    try:
        uncertainty_kind = UncertaintyKind(_text(uncertainty, "kind"))
    except ValueError as exc:
        raise ValueError("unsupported uncertainty kind") from exc
    raw_samples = uncertainty["samples"]
    if not isinstance(raw_samples, list) or not raw_samples:
        raise ValueError("uncertainty samples must be a non-empty array")
    samples = tuple(
        _role_number(role, _number_item(item, "uncertainty sample"), "uncertainty sample")
        for item in raw_samples
    )
    if uncertainty_kind is UncertaintyKind.DETERMINISTIC and samples != (point_value,):
        raise ValueError("deterministic uncertainty must contain only the point value")
    if uncertainty_kind is not UncertaintyKind.DETERMINISTIC and len(samples) < 2:
        raise ValueError("sample-based uncertainty requires at least two aligned samples")
    limits = _mapping(value, "scale_limits")
    _exact_keys("scale_limits", limits, {"min", "max"})
    scale_min = _number(limits, "min")
    scale_max = _number(limits, "max")
    if scale_min > point_value or scale_max < point_value or scale_min >= scale_max:
        raise ValueError("scale_limits must be ordered and contain the point value")
    if any(sample < scale_min or sample > scale_max for sample in samples):
        raise ValueError("uncertainty samples must fall within scale_limits")
    source = _mapping(value, "source")
    _exact_keys("source", source, {"uri", "sha256", "licence"})
    source_uri = _text(source, "uri")
    parsed_uri = urlparse(source_uri)
    if parsed_uri.scheme not in {"https", "doi"} or not parsed_uri.netloc:
        raise ValueError("source URI must be an absolute HTTPS or DOI URI")
    source_sha256 = _text(source, "sha256")
    if not _SHA256.fullmatch(source_sha256):
        raise ValueError("source sha256 must be 64 lowercase hexadecimal characters")
    return ParameterEvidenceRecord(
        record_id=_text(value, "record_id"),
        role=role,
        value=point_value,
        unit=unit,
        programme_id=_text(value, "programme_id"),
        evidence_method=method,
        marginality=marginality,
        causal_assumptions=causal_assumptions,
        uncertainty_kind=uncertainty_kind,
        samples=samples,
        scale_min=scale_min,
        scale_max=scale_max,
        source_uri=source_uri,
        source_sha256=source_sha256,
        source_licence=_text(source, "licence"),
        transformation=_text(value, "transformation"),
        reviewer=_text(value, "reviewer"),
        approval_state=approval_state,
        evidence_revision=_revision(value, "evidence_revision"),
        derived_only=True,
        context=context,
    )


def _role_contract(
    role: ParameterRole, context: EvidenceContext
) -> tuple[str, Marginality]:
    if role in {
        ParameterRole.EXPANSION_ICER,
        ParameterRole.DISPLACEMENT_ICER,
        ParameterRole.CONTRACTION_ICER,
        ParameterRole.INVESTMENT_ICER,
    }:
        return f"{context.currency_unit}/{context.health_unit}", Marginality.MARGINAL
    if role is ParameterRole.PRESENT_VALUE_MULTIPLIER:
        return "dimensionless", Marginality.NOT_APPLICABLE
    if role is ParameterRole.ANNUAL_PROGRAM_HEALTH_EFFECT:
        return f"{context.health_unit}/year", Marginality.INCREMENTAL
    if role is ParameterRole.HORIZON:
        return "year", Marginality.NOT_APPLICABLE
    return "proportion/year", Marginality.NOT_APPLICABLE


def _role_number(role: ParameterRole, value: float, field: str) -> float:
    if role is ParameterRole.DISCOUNT_RATE:
        if not 0 <= value < 1:
            raise ValueError(f"{field} for discount_rate must be in [0, 1)")
    elif value <= 0:
        raise ValueError(f"{field} for {role.value} must be positive")
    if role is ParameterRole.PRESENT_VALUE_MULTIPLIER and value <= 1:
        raise ValueError(f"{field} for phi must be greater than 1")
    if role is ParameterRole.HORIZON and not value.is_integer():
        raise ValueError(f"{field} for horizon must be a whole number of years")
    return value


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


def _record_mapping(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("evidence packet records must be objects")
    return value


def _text(value: dict[str, Any], field: str) -> str:
    item = value[field]
    if not isinstance(item, str) or not item.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return item


def _array_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} entries must be non-empty strings")
    return value


def _revision(value: dict[str, Any], field: str) -> str:
    revision = _text(value, field)
    if not revision.startswith("sha256:") or not _SHA256.fullmatch(revision[7:]):
        raise ValueError(f"{field} must use sha256:<64 lowercase hex> format")
    return revision


def _number(value: dict[str, Any], field: str) -> float:
    return _number_item(value[field], field)


def _number_item(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be a JSON number")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{field} must be finite")
    return number


def _integer(value: dict[str, Any], field: str, *, minimum: int) -> int:
    item = value[field]
    if type(item) is not int or item < minimum:
        raise ValueError(f"{field} must be an integer greater than or equal to {minimum}")
    return item
