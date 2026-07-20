"""Stable application ports separating domain logic from ecosystem capability."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Protocol


class GameEnginePort(Protocol):
    """Domain-neutral game execution/solution boundary."""

    def solve(self, game_specification: Mapping[str, Any]) -> Mapping[str, Any]: ...


class ValueOfInformationPort(Protocol):
    """VOI boundary implemented by Voiage."""

    def evpi(self, net_benefit_samples: Sequence[Sequence[float]]) -> float: ...


class SimulationPort(Protocol):
    """Simulation boundary implemented by Kairos."""

    def export_scenario(self, events: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]: ...


class EvidenceRepositoryPort(Protocol):
    """Reviewed evidence boundary implemented by Reimbursement Atlas exports."""

    def records(self) -> Sequence[Mapping[str, Any]]: ...


class OntologyPort(Protocol):
    """Semantic export boundary aligned with UOGTO."""

    def export_game(self, case: Mapping[str, Any]) -> Mapping[str, Any]: ...
