"""UOGTO-aligned JSON-LD exporter."""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any, ClassVar


class UogtoExporter:
    context: ClassVar[Mapping[str, Any]] = {
        "uogto": "https://w3id.org/uogto/core#",
        "hta": "https://w3id.org/uogto/packs/hta#",
        "ndrg": "https://w3id.org/uogto/packs/new-drug-reimbursement#",
        "identifier": "uogto:identifier",
        "name": "uogto:name",
        "hasPlayer": {"@id": "uogto:hasPlayer", "@type": "@id"},
        "governedByRule": {"@id": "uogto:governedByRule", "@type": "@id"},
    }

    def export_game(self, case: Mapping[str, Any]) -> Mapping[str, Any]:
        case_id = str(case.get("case_id", "case"))
        base = f"urn:ndrg:{case_id}:"
        incremental_cost = float(case["incremental_cost"])
        incremental_health_effect = float(case["incremental_health_effect"])
        if not math.isfinite(incremental_cost) or not math.isfinite(incremental_health_effect):
            raise ValueError("UOGTO economic values must be finite")
        return {
            "@context": self.context,
            "@id": base + "game",
            "@type": ["uogto:GameInstance", "ndrg:NewDrugReimbursementGame"],
            "identifier": case_id,
            "name": str(case.get("name", "New-drug reimbursement case")),
            "hasPlayer": [base + "firm", base + "institution"],
            "governedByRule": [base + "threshold-rule", base + "budget-rule"],
            "ndrg:incrementalCost": incremental_cost,
            "ndrg:incrementalHealthEffect": incremental_health_effect,
            "ndrg:economicContext": str(case["context"]),
        }
