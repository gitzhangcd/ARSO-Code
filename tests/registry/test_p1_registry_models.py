from __future__ import annotations

import pytest
from pydantic import ValidationError

from design_intelligence.contracts.core import CanonicalObjectClass


EXPECTED_FIELDS = {
    "object_type",
    "python_type",
    "schema_version",
    "canonical",
    "primitive_owner",
    "capability_owners",
    "object_class",
    "state_domain",
    "versioned",
    "persistent_ref_kind",
    "historical_ssot",
    "logical_authoring_ref_allowed",
    "system_snapshot_eligible",
    "knowledge_snapshot_eligible",
    "review_snapshot_eligible",
    "system_intervention_target_eligible",
    "artifact_eligible",
}


def _registry():
    import design_intelligence.registry as registry
    return registry


def _entry(**overrides):
    registry = _registry()
    data = {
        "object_type": "di.test.revision",
        "python_type": "design_intelligence.test.TestRevision",
        "schema_version": "1.0",
        "canonical": True,
        "primitive_owner": "DI_TEST",
        "capability_owners": ("DI_TEST",),
        "object_class": CanonicalObjectClass.CANONICAL_REVISION,
        "state_domain": "TASK",
        "versioned": True,
        "persistent_ref_kind": registry.ReferenceKind.EXACT_OBJECT_REF,
        "historical_ssot": True,
        "logical_authoring_ref_allowed": True,
        "system_snapshot_eligible": False,
        "knowledge_snapshot_eligible": False,
        "review_snapshot_eligible": False,
        "system_intervention_target_eligible": False,
        "artifact_eligible": False,
    }
    data.update(overrides)
    return registry.ObjectRegistryEntry(**data)


def test_registry_entry_has_exact_minimum_field_surface() -> None:
    registry = _registry()
    assert set(registry.ObjectRegistryEntry.model_fields) == EXPECTED_FIELDS


def test_registry_entry_requires_every_governance_field() -> None:
    registry = _registry()
    assert all(field.is_required() for field in registry.ObjectRegistryEntry.model_fields.values())


def test_primitive_owner_and_state_domain_are_distinct_nominal_strings() -> None:
    registry = _registry()
    assert registry.PrimitiveOwner is not registry.StateDomain
    assert registry.PrimitiveOwner("DI_B03").root == "DI_B03"
    assert registry.StateDomain("TASK").root == "TASK"
    with pytest.raises(ValidationError):
        registry.PrimitiveOwner(123)


def test_reference_kind_has_exact_closed_values() -> None:
    registry = _registry()
    assert {member.value for member in registry.ReferenceKind} == {
        "EXACT_OBJECT_REF",
        "OBJECT_REF",
        "NONE",
    }


def test_manifest_rejects_duplicate_object_type() -> None:
    registry = _registry()
    first = _entry()
    second = _entry(python_type="design_intelligence.test.OtherRevision")
    with pytest.raises(ValidationError):
        registry.ObjectRegistryManifest(entries=(first, second))


def test_manifest_accepts_unique_object_types() -> None:
    registry = _registry()
    first = _entry()
    second = _entry(
        object_type="di.test.fact",
        python_type="design_intelligence.test.TestFact",
        object_class=CanonicalObjectClass.IMMUTABLE_FACT,
        versioned=False,
        persistent_ref_kind=registry.ReferenceKind.OBJECT_REF,
    )
    manifest = registry.ObjectRegistryManifest(entries=(first, second))
    assert len(manifest.entries) == 2


@pytest.mark.parametrize(
    ("overrides"),
    [
        {"versioned": False},
        {"historical_ssot": False},
        {"persistent_ref_kind": "OBJECT_REF"},
    ],
)
def test_canonical_revision_rejects_invalid_persistence_policy(overrides: dict[str, object]) -> None:
    registry = _registry()
    if overrides.get("persistent_ref_kind") == "OBJECT_REF":
        overrides = {**overrides, "persistent_ref_kind": registry.ReferenceKind.OBJECT_REF}
    with pytest.raises(ValidationError):
        _entry(**overrides)


@pytest.mark.parametrize(
    "object_class",
    [
        CanonicalObjectClass.IMMUTABLE_FACT,
        CanonicalObjectClass.IMMUTABLE_ROOT,
        CanonicalObjectClass.IMMUTABLE_GRAPH_NODE,
        CanonicalObjectClass.SNAPSHOT,
    ],
)
def test_nonversioned_historical_classes_require_object_ref(object_class: CanonicalObjectClass) -> None:
    registry = _registry()
    valid = _entry(
        object_class=object_class,
        versioned=False,
        persistent_ref_kind=registry.ReferenceKind.OBJECT_REF,
    )
    assert valid.historical_ssot is True

    with pytest.raises(ValidationError):
        _entry(
            object_class=object_class,
            versioned=True,
            persistent_ref_kind=registry.ReferenceKind.OBJECT_REF,
        )
    with pytest.raises(ValidationError):
        _entry(
            object_class=object_class,
            versioned=False,
            persistent_ref_kind=registry.ReferenceKind.EXACT_OBJECT_REF,
        )
    with pytest.raises(ValidationError):
        _entry(
            object_class=object_class,
            versioned=False,
            persistent_ref_kind=registry.ReferenceKind.OBJECT_REF,
            historical_ssot=False,
        )


def test_operational_control_state_requires_nonhistorical_nonpersistent_policy() -> None:
    registry = _registry()
    valid = _entry(
        object_class=CanonicalObjectClass.OPERATIONAL_CONTROL_STATE,
        versioned=False,
        persistent_ref_kind=registry.ReferenceKind.NONE,
        historical_ssot=False,
    )
    assert valid.historical_ssot is False

    with pytest.raises(ValidationError):
        _entry(
            object_class=CanonicalObjectClass.OPERATIONAL_CONTROL_STATE,
            versioned=False,
            persistent_ref_kind=registry.ReferenceKind.OBJECT_REF,
            historical_ssot=False,
        )


def test_unmaterialized_derived_view_requires_nonhistorical_nonpersistent_policy() -> None:
    registry = _registry()
    valid = _entry(
        object_class=CanonicalObjectClass.DERIVED_VIEW,
        versioned=False,
        persistent_ref_kind=registry.ReferenceKind.NONE,
        historical_ssot=False,
    )
    assert valid.historical_ssot is False

    with pytest.raises(ValidationError):
        _entry(
            object_class=CanonicalObjectClass.DERIVED_VIEW,
            versioned=False,
            persistent_ref_kind=registry.ReferenceKind.OBJECT_REF,
            historical_ssot=False,
        )
