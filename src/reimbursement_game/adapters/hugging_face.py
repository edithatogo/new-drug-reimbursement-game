"""Owner-scoped Hugging Face publication contracts."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HuggingFacePublicationContract:
    repository_id: str
    kind: str
    licence: str
    source_terms: str
    revision: str

    def validate(self) -> None:
        owner, separator, name = self.repository_id.partition("/")
        if owner != "edithatogo" or not separator or not name or "/" in name or any(char.isspace() for char in name):
            raise ValueError("Hugging Face repository must be in the edithatogo namespace")
        if self.kind not in {"dataset", "space"}:
            raise ValueError("Hugging Face publication kind must be dataset or space")
        if not self.licence.strip() or not self.source_terms.strip() or not self.revision.strip():
            raise ValueError("Hugging Face publication requires licence, source terms, and revision")
        if "raw" in self.source_terms.lower() or "restricted" in self.source_terms.lower():
            raise ValueError("Hugging Face publication cannot contain raw or restricted source terms")
