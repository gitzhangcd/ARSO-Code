from __future__ import annotations

from design_intelligence.contracts.core import CanonicalObjectClass, ObjectType
from design_intelligence.registry import ReferenceKind, RegistryIndex
from design_intelligence.registry.b01 import B01_REGISTRY_MANIFEST


REVISION_OBJECTS = {
    "di.b01.style_brief": "design_intelligence.contracts.b01.StyleBrief",
    "di.b01.reference_intent_binding": "design_intelligence.contracts.b01.ReferenceIntentBinding",
    "di.b01.design_context_binding": "design_intelligence.contracts.b01.DesignContextBinding",
    "di.b01.design_decision": "design_intelligence.contracts.b01.DesignDecision",
    "di.b01.design_route": "design_intelligence.contracts.b01.DesignRoute",
    "di.b01.design_spec": "design_intelligence.contracts.b01.DesignSpec",
}
FACT_OBJECT = {
    "di.b01.design_task_binding": "design_intelligence.contracts.b01.DesignTaskBinding",
}


def test_b01_registry_contains_exactly_seven_unique_entries() -> None:
    entries = B01_REGISTRY_MANIFEST.entries
    assert len(entries) == 7
    object_types = [entry.object_type.root for entry in entries]
    assert len(set(object_types)) == 7
    assert set(object_types) == set(REVISION_OBJECTS) | set(FACT_OBJECT)


def test_all_b01_registry_entries_share_the_frozen_owner_policy() -> None:
    for entry in B01_REGISTRY_MANIFEST.entries:
        assert entry.schema_version.root == "1.0"
        assert entry.canonical is True
        assert entry.primitive_owner.root == "DI_B01"
        assert tuple(owner.root for owner in entry.capability_owners) == ("DI_B01",)
        assert entry.state_domain.root == "TASK"
        assert entry.historical_ssot is True
        assert entry.system_snapshot_eligible is False
        assert entry.knowledge_snapshot_eligible is False
        assert entry.system_intervention_target_eligible is False
        assert entry.artifact_eligible is False


def test_six_authored_b01_objects_use_revision_registry_policy() -> None:
    index = RegistryIndex(B01_REGISTRY_MANIFEST)
    for object_type, python_type in REVISION_OBJECTS.items():
        entry = index.require(ObjectType(object_type))
        assert entry.python_type == python_type
        assert entry.object_class is CanonicalObjectClass.CANONICAL_REVISION
        assert entry.versioned is True
        assert entry.persistent_ref_kind is ReferenceKind.EXACT_OBJECT_REF
        assert entry.logical_authoring_ref_allowed is True
        assert entry.review_snapshot_eligible is True


def test_design_task_binding_uses_immutable_fact_registry_policy() -> None:
    entry = RegistryIndex(B01_REGISTRY_MANIFEST).require(
        ObjectType("di.b01.design_task_binding")
    )
    assert entry.python_type == "design_intelligence.contracts.b01.DesignTaskBinding"
    assert entry.object_class is CanonicalObjectClass.IMMUTABLE_FACT
    assert entry.versioned is False
    assert entry.persistent_ref_kind is ReferenceKind.OBJECT_REF
    assert entry.logical_authoring_ref_allowed is False
    assert entry.review_snapshot_eligible is False


def test_b01_registry_does_not_register_shared_support_types() -> None:
    python_types = {entry.python_type for entry in B01_REGISTRY_MANIFEST.entries}
    forbidden_support_types = {
        "design_intelligence.contracts.core.ActorRef",
        "design_intelligence.contracts.core.TenantScope",
        "design_intelligence.contracts.core.Provenance",
        "design_intelligence.contracts.core.CanonicalObject",
        "design_intelligence.contracts.core.CanonicalRevision",
        "design_intelligence.contracts.core.ImmutableFact",
    }
    assert python_types.isdisjoint(forbidden_support_types)
