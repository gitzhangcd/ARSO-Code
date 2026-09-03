from __future__ import annotations

from datetime import datetime

from pydantic import model_validator

from di_contracts.core.base import FrozenDIModel
from di_contracts.core.models import CanonicalRef
from di_contracts.core.types import (
    CanonicalObjectClass,
    ContentHash,
    ObjectId,
    ObjectType,
    PrimitiveOwner,
    ReferenceKind,
    SchemaVersion,
    StateDomain,
    ensure_utc,
)


class ObjectRegistryEntry(FrozenDIModel):
    object_type: ObjectType
    primitive_owner: PrimitiveOwner
    capability_owners: tuple[PrimitiveOwner, ...] = ()
    object_class: CanonicalObjectClass
    state_domain: StateDomain
    schema_version: SchemaVersion
    python_type: str
    canonical: bool = True
    versioned: bool
    persistent_ref_kind: ReferenceKind
    logical_authoring_ref_allowed: bool = False
    artifact_eligible: bool = False
    system_snapshot_eligible: bool = False
    knowledge_snapshot_eligible: bool = False
    review_snapshot_eligible: bool = False
    system_intervention_target_eligible: bool = False
    historical_ssot: bool = True

    @model_validator(mode="after")
    def validate_class_ref_invariants(self):
        if self.object_class == CanonicalObjectClass.CANONICAL_REVISION:
            if not self.versioned or self.persistent_ref_kind != ReferenceKind.EXACT_OBJECT_REF:
                raise ValueError("CANONICAL_REVISION must be versioned and use ExactObjectRef")
        elif self.object_class in {
            CanonicalObjectClass.IMMUTABLE_FACT,
            CanonicalObjectClass.IMMUTABLE_ROOT,
            CanonicalObjectClass.IMMUTABLE_GRAPH_NODE,
            CanonicalObjectClass.SNAPSHOT,
        }:
            if self.versioned or self.persistent_ref_kind != ReferenceKind.OBJECT_REF:
                raise ValueError("non-versioned immutable objects must use ObjectRef")
        elif self.object_class in {
            CanonicalObjectClass.OPERATIONAL_CONTROL_STATE,
            CanonicalObjectClass.DERIVED_VIEW,
        }:
            if self.persistent_ref_kind != ReferenceKind.NONE:
                raise ValueError("operational/view types cannot expose persistent historical refs")
            if self.historical_ssot:
                raise ValueError("operational/view types cannot be historical SSOT")
        return self


class ObjectRegistryManifest(FrozenDIModel):
    schema_version: SchemaVersion
    manifest_id: ObjectId
    entries: tuple[ObjectRegistryEntry, ...]
    generated_at: datetime
    content_hash: ContentHash

    @model_validator(mode="after")
    def validate_unique_types(self):
        names = [e.object_type.root for e in self.entries]
        if len(names) != len(set(names)):
            raise ValueError("duplicate object_type in registry manifest")
        return self
