"""Frozen seven-entry B01 Object Registry manifest."""

from __future__ import annotations

from design_intelligence.contracts.core import CanonicalObjectClass, ObjectType, SchemaVersion

from .models import (
    ObjectRegistryEntry,
    ObjectRegistryManifest,
    PrimitiveOwner,
    ReferenceKind,
    StateDomain,
)


_B01_OWNER = PrimitiveOwner("DI_B01")
_TASK_DOMAIN = StateDomain("TASK")
_SCHEMA_VERSION = SchemaVersion("1.0")


def _b01_entry(
    *,
    object_type: str,
    python_type: str,
    object_class: CanonicalObjectClass,
    versioned: bool,
    persistent_ref_kind: ReferenceKind,
    logical_authoring_ref_allowed: bool,
    review_snapshot_eligible: bool,
) -> ObjectRegistryEntry:
    return ObjectRegistryEntry(
        object_type=ObjectType(object_type),
        python_type=python_type,
        schema_version=_SCHEMA_VERSION,
        canonical=True,
        primitive_owner=_B01_OWNER,
        capability_owners=(_B01_OWNER,),
        object_class=object_class,
        state_domain=_TASK_DOMAIN,
        versioned=versioned,
        persistent_ref_kind=persistent_ref_kind,
        historical_ssot=True,
        logical_authoring_ref_allowed=logical_authoring_ref_allowed,
        system_snapshot_eligible=False,
        knowledge_snapshot_eligible=False,
        review_snapshot_eligible=review_snapshot_eligible,
        system_intervention_target_eligible=False,
        artifact_eligible=False,
    )


def _revision_entry(object_type: str, python_type: str) -> ObjectRegistryEntry:
    return _b01_entry(
        object_type=object_type,
        python_type=python_type,
        object_class=CanonicalObjectClass.CANONICAL_REVISION,
        versioned=True,
        persistent_ref_kind=ReferenceKind.EXACT_OBJECT_REF,
        logical_authoring_ref_allowed=True,
        review_snapshot_eligible=True,
    )


B01_REGISTRY_MANIFEST = ObjectRegistryManifest(
    entries=(
        _revision_entry(
            "di.b01.style_brief",
            "design_intelligence.contracts.b01.StyleBrief",
        ),
        _revision_entry(
            "di.b01.design_context_binding",
            "design_intelligence.contracts.b01.DesignContextBinding",
        ),
        _revision_entry(
            "di.b01.design_decision",
            "design_intelligence.contracts.b01.DesignDecision",
        ),
        _revision_entry(
            "di.b01.design_route",
            "design_intelligence.contracts.b01.DesignRoute",
        ),
        _revision_entry(
            "di.b01.design_spec",
            "design_intelligence.contracts.b01.DesignSpec",
        ),
        _revision_entry(
            "di.b01.reference_intent_binding",
            "design_intelligence.contracts.b01.ReferenceIntentBinding",
        ),
        _b01_entry(
            object_type="di.b01.design_task_binding",
            python_type="design_intelligence.contracts.b01.DesignTaskBinding",
            object_class=CanonicalObjectClass.IMMUTABLE_FACT,
            versioned=False,
            persistent_ref_kind=ReferenceKind.OBJECT_REF,
            logical_authoring_ref_allowed=False,
            review_snapshot_eligible=False,
        ),
    )
)
