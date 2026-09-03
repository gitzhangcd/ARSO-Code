import pytest
from pydantic import ValidationError

from di_contracts.core.types import CanonicalObjectClass as C, PrimitiveOwner as O, ReferenceKind as R, StateDomain as D
from di_contracts.registry.manifest import REGISTRY_ENTRIES, e
from di_contracts.registry.models import ObjectRegistryEntry
from di_contracts.registry.validation import RegistryIndex
from conftest import exact, ref


def test_registry_object_types_unique():
    names = [x.object_type.root for x in REGISTRY_ENTRIES]
    assert len(names) == len(set(names))


def test_one_primitive_owner_per_entry():
    assert all(isinstance(x.primitive_owner, O) for x in REGISTRY_ENTRIES)


def test_revision_uses_exact_ref():
    for x in REGISTRY_ENTRIES:
        if x.object_class == C.CANONICAL_REVISION:
            assert x.persistent_ref_kind == R.EXACT_OBJECT_REF
            assert x.versioned


def test_non_versioned_immutable_uses_object_ref():
    immutable = {C.IMMUTABLE_FACT, C.IMMUTABLE_ROOT, C.IMMUTABLE_GRAPH_NODE, C.SNAPSHOT}
    for x in REGISTRY_ENTRIES:
        if x.object_class in immutable:
            assert x.persistent_ref_kind == R.OBJECT_REF
            assert not x.versioned


def test_operational_not_historical_ssot():
    for x in REGISTRY_ENTRIES:
        if x.object_class == C.OPERATIONAL_CONTROL_STATE:
            assert not x.historical_ssot
            assert x.persistent_ref_kind == R.NONE


def test_design_spec_not_system_artifact():
    idx = RegistryIndex(REGISTRY_ENTRIES)
    entry = idx.require("di.b01.design_spec")
    assert not entry.artifact_eligible
    assert not entry.system_snapshot_eligible
    assert not entry.system_intervention_target_eligible


def test_generation_compiler_is_system_artifact_and_intervention_target():
    idx = RegistryIndex(REGISTRY_ENTRIES)
    entry = idx.require("di.b03.generation_compiler")
    assert entry.artifact_eligible
    assert entry.system_snapshot_eligible
    assert entry.system_intervention_target_eligible


def test_design_spec_rejected_as_intervention_target():
    idx = RegistryIndex(REGISTRY_ENTRIES)
    with pytest.raises(ValueError):
        idx.validate_intervention_target(exact("di.b01.design_spec"))


def test_generation_compiler_allowed_as_intervention_target():
    idx = RegistryIndex(REGISTRY_ENTRIES)
    idx.validate_intervention_target(exact("di.b03.generation_compiler"))


def test_reference_kind_mismatch_rejected():
    idx = RegistryIndex(REGISTRY_ENTRIES)
    with pytest.raises(ValueError):
        idx.validate_reference_kind(ref("di.b03.generation_compiler"))


def test_invalid_registry_combo_rejected():
    with pytest.raises(ValidationError):
        ObjectRegistryEntry(
            object_type="di.test.bad", primitive_owner=O.DI_B01,
            object_class=C.CANONICAL_REVISION, state_domain=D.TASK, schema_version="1.0",
            python_type="X", versioned=False, persistent_ref_kind=R.OBJECT_REF,
        )
