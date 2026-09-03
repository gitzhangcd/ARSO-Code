from __future__ import annotations

import pytest

from design_intelligence.contracts.core import (
    CanonicalObjectClass,
    ExactObjectRef,
    ObjectRef,
    ObjectType,
)
from design_intelligence.registry import (
    ObjectRegistryEntry,
    ObjectRegistryManifest,
    PrimitiveOwner,
    ReferenceKind,
    StateDomain,
)


def _entry(
    *,
    object_type: str,
    object_class: CanonicalObjectClass,
    persistent_ref_kind: ReferenceKind,
    historical_ssot: bool,
    versioned: bool,
    system_snapshot_eligible: bool = False,
    knowledge_snapshot_eligible: bool = False,
    review_snapshot_eligible: bool = False,
    system_intervention_target_eligible: bool = False,
) -> ObjectRegistryEntry:
    return ObjectRegistryEntry(
        object_type=object_type,
        python_type=f"design_intelligence.test.{object_type.replace('.', '_')}",
        schema_version="1.0",
        canonical=True,
        primitive_owner=PrimitiveOwner("DI_TEST"),
        capability_owners=(PrimitiveOwner("DI_TEST"),),
        object_class=object_class,
        state_domain=StateDomain("TASK"),
        versioned=versioned,
        persistent_ref_kind=persistent_ref_kind,
        historical_ssot=historical_ssot,
        logical_authoring_ref_allowed=False,
        system_snapshot_eligible=system_snapshot_eligible,
        knowledge_snapshot_eligible=knowledge_snapshot_eligible,
        review_snapshot_eligible=review_snapshot_eligible,
        system_intervention_target_eligible=system_intervention_target_eligible,
        artifact_eligible=False,
    )


def _manifest() -> ObjectRegistryManifest:
    return ObjectRegistryManifest(
        entries=(
            _entry(
                object_type="di.test.revision",
                object_class=CanonicalObjectClass.CANONICAL_REVISION,
                persistent_ref_kind=ReferenceKind.EXACT_OBJECT_REF,
                historical_ssot=True,
                versioned=True,
                system_snapshot_eligible=True,
                system_intervention_target_eligible=True,
            ),
            _entry(
                object_type="di.test.fact",
                object_class=CanonicalObjectClass.IMMUTABLE_FACT,
                persistent_ref_kind=ReferenceKind.OBJECT_REF,
                historical_ssot=True,
                versioned=False,
                knowledge_snapshot_eligible=True,
                review_snapshot_eligible=True,
            ),
            _entry(
                object_type="di.test.operational",
                object_class=CanonicalObjectClass.OPERATIONAL_CONTROL_STATE,
                persistent_ref_kind=ReferenceKind.NONE,
                historical_ssot=False,
                versioned=False,
            ),
        )
    )


def _exact_ref(object_type: str = "di.test.revision") -> ExactObjectRef:
    return ExactObjectRef(
        object_type=object_type,
        logical_id="logical-id",
        version_id="version-id",
        content_hash="sha256:" + "1" * 64,
    )


def _object_ref(object_type: str = "di.test.fact") -> ObjectRef:
    return ObjectRef(
        object_type=object_type,
        object_id="object-id",
        content_hash="sha256:" + "2" * 64,
    )


def _index():
    from design_intelligence.registry import RegistryIndex
    return RegistryIndex(_manifest())


def test_registry_index_require_and_contains_use_exact_object_type() -> None:
    index = _index()
    object_type = ObjectType("di.test.revision")
    assert index.contains(object_type) is True
    assert index.require(object_type).object_type == object_type
    assert index.contains(ObjectType("di.test.missing")) is False
    with pytest.raises(KeyError):
        index.require(ObjectType("di.test.missing"))


def test_registry_index_validates_exact_reference_kind() -> None:
    index = _index()
    index.validate_reference_kind(_exact_ref())
    with pytest.raises(ValueError):
        index.validate_reference_kind(_exact_ref("di.test.fact"))


def test_registry_index_validates_object_reference_kind() -> None:
    index = _index()
    index.validate_reference_kind(_object_ref())
    with pytest.raises(ValueError):
        index.validate_reference_kind(_object_ref("di.test.revision"))


def test_registry_entry_with_none_reference_policy_rejects_persistent_ref() -> None:
    index = _index()
    with pytest.raises(ValueError):
        index.validate_reference_kind(_object_ref("di.test.operational"))


def test_system_snapshot_eligibility_guard() -> None:
    index = _index()
    index.require_system_snapshot_eligible(_exact_ref())
    with pytest.raises(ValueError):
        index.require_system_snapshot_eligible(_object_ref())


def test_knowledge_snapshot_eligibility_guard() -> None:
    index = _index()
    index.require_knowledge_snapshot_eligible(_object_ref())
    with pytest.raises(ValueError):
        index.require_knowledge_snapshot_eligible(_exact_ref())


def test_review_snapshot_eligibility_guard() -> None:
    index = _index()
    index.require_review_snapshot_eligible(_object_ref())
    with pytest.raises(ValueError):
        index.require_review_snapshot_eligible(_exact_ref())


def test_system_intervention_target_eligibility_guard() -> None:
    index = _index()
    index.require_system_intervention_target_eligible(_exact_ref())
    with pytest.raises(ValueError):
        index.require_system_intervention_target_eligible(_object_ref())
