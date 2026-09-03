from __future__ import annotations

from di_contracts.core.models import ExactObjectRef, ObjectRef
from di_contracts.core.types import ReferenceKind, StateDomain
from .models import ObjectRegistryEntry


class RegistryIndex:
    def __init__(self, entries: tuple[ObjectRegistryEntry, ...]):
        self._entries = {e.object_type.root: e for e in entries}
        if len(self._entries) != len(entries):
            raise ValueError("duplicate object_type")

    def require(self, object_type: str) -> ObjectRegistryEntry:
        try:
            return self._entries[object_type]
        except KeyError as exc:
            raise KeyError(f"unknown object_type: {object_type}") from exc

    def validate_reference_kind(self, ref: ExactObjectRef | ObjectRef) -> None:
        entry = self.require(ref.object_type.root)
        expected = ReferenceKind.EXACT_OBJECT_REF if isinstance(ref, ExactObjectRef) else ReferenceKind.OBJECT_REF
        if entry.persistent_ref_kind != expected:
            raise ValueError("reference kind mismatch")

    def validate_system_snapshot_eligibility(self, ref: ExactObjectRef | ObjectRef) -> None:
        entry = self.require(ref.object_type.root)
        if not entry.system_snapshot_eligible:
            raise ValueError("object type is not eligible for SystemSnapshot")

    def validate_knowledge_snapshot_eligibility(self, ref: ExactObjectRef | ObjectRef) -> None:
        entry = self.require(ref.object_type.root)
        if not entry.knowledge_snapshot_eligible:
            raise ValueError("object type is not eligible for KnowledgeSnapshot")

    def validate_review_snapshot_eligibility(self, ref: ExactObjectRef | ObjectRef) -> None:
        entry = self.require(ref.object_type.root)
        if not entry.review_snapshot_eligible:
            raise ValueError("object type is not eligible for DesignReviewSnapshot")

    def validate_intervention_target(self, ref: ExactObjectRef | ObjectRef) -> None:
        entry = self.require(ref.object_type.root)
        if not entry.system_intervention_target_eligible:
            raise ValueError("object type is not an intervention target")
