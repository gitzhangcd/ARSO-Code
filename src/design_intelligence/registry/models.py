"""P1 Object Registry contract models."""

from __future__ import annotations

from enum import StrEnum

from pydantic import ConfigDict, RootModel, model_validator

from design_intelligence.contracts.core import (
    CanonicalObjectClass,
    FrozenDIModel,
    ObjectType,
    SchemaVersion,
)


class PrimitiveOwner(RootModel[str]):
    """Nominal primitive-owner identity; closed inventory is deferred."""

    model_config = ConfigDict(strict=True, frozen=True)


class StateDomain(RootModel[str]):
    """Nominal state-domain identity; closed inventory is deferred."""

    model_config = ConfigDict(strict=True, frozen=True)


class ReferenceKind(StrEnum):
    """Frozen persistent-reference kinds from the persistence matrix."""

    EXACT_OBJECT_REF = "EXACT_OBJECT_REF"
    OBJECT_REF = "OBJECT_REF"
    NONE = "NONE"


class ObjectRegistryEntry(FrozenDIModel):
    """Minimum registry declaration required by Exact Contract section 20."""

    object_type: ObjectType
    python_type: str
    schema_version: SchemaVersion
    canonical: bool
    primitive_owner: PrimitiveOwner
    capability_owners: tuple[PrimitiveOwner, ...]
    object_class: CanonicalObjectClass
    state_domain: StateDomain
    versioned: bool
    persistent_ref_kind: ReferenceKind
    historical_ssot: bool
    logical_authoring_ref_allowed: bool
    system_snapshot_eligible: bool
    knowledge_snapshot_eligible: bool
    review_snapshot_eligible: bool
    system_intervention_target_eligible: bool
    artifact_eligible: bool


class ObjectRegistryManifest(FrozenDIModel):
    """Immutable container for a registry entry set; full inventory is deferred."""

    entries: tuple[ObjectRegistryEntry, ...]

    @model_validator(mode="after")
    def reject_duplicate_object_types(self) -> "ObjectRegistryManifest":
        object_types = [entry.object_type.root for entry in self.entries]
        if len(object_types) != len(set(object_types)):
            raise ValueError("registry manifest contains duplicate object_type")
        return self
