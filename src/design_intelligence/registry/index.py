"""Derived P1 registry index and generic policy guards."""

from __future__ import annotations

from design_intelligence.contracts.core import ExactObjectRef, ObjectRef, ObjectType

from .models import ObjectRegistryEntry, ObjectRegistryManifest, ReferenceKind


class RegistryIndex:
    """Exact object-type lookup over an immutable registry manifest."""

    def __init__(self, manifest: ObjectRegistryManifest) -> None:
        self._entries = {entry.object_type.root: entry for entry in manifest.entries}

    def require(self, object_type: ObjectType) -> ObjectRegistryEntry:
        try:
            return self._entries[object_type.root]
        except KeyError:
            raise KeyError(f"unknown registry object_type: {object_type.root}") from None

    def contains(self, object_type: ObjectType) -> bool:
        return object_type.root in self._entries

    def validate_reference_kind(self, ref: ExactObjectRef | ObjectRef) -> None:
        entry = self.require(ref.object_type)
        expected = (
            ReferenceKind.EXACT_OBJECT_REF
            if isinstance(ref, ExactObjectRef)
            else ReferenceKind.OBJECT_REF
        )
        if entry.persistent_ref_kind is not expected:
            raise ValueError(
                "reference kind mismatch for "
                f"{entry.object_type.root}: expected {entry.persistent_ref_kind.value}, "
                f"got {expected.value}"
            )

    def require_system_snapshot_eligible(self, ref: ExactObjectRef | ObjectRef) -> None:
        self._require_eligible(ref, "system_snapshot_eligible")

    def require_knowledge_snapshot_eligible(self, ref: ExactObjectRef | ObjectRef) -> None:
        self._require_eligible(ref, "knowledge_snapshot_eligible")

    def require_review_snapshot_eligible(self, ref: ExactObjectRef | ObjectRef) -> None:
        self._require_eligible(ref, "review_snapshot_eligible")

    def require_system_intervention_target_eligible(
        self, ref: ExactObjectRef | ObjectRef
    ) -> None:
        self._require_eligible(ref, "system_intervention_target_eligible")

    def _require_eligible(self, ref: ExactObjectRef | ObjectRef, field_name: str) -> None:
        self.validate_reference_kind(ref)
        entry = self.require(ref.object_type)
        if not getattr(entry, field_name):
            raise ValueError(
                f"{entry.object_type.root} is not eligible for registry policy {field_name}"
            )
