from pathlib import Path

import pytest
from pydantic import BaseModel, ConfigDict, ValidationError


ROOT = Path(__file__).resolve().parents[2]
TYPE_NAMES = ("ObjectId", "LogicalId", "SchemaVersion", "ObjectType")


def _types_module():
    from design_intelligence.contracts.core import types

    return types


def test_core_types_module_exists() -> None:
    assert (ROOT / "src/design_intelligence/contracts/core/types.py").is_file()


def test_nominal_identity_symbols_exist() -> None:
    module = _types_module()
    for name in TYPE_NAMES:
        assert hasattr(module, name)


def test_nominal_identity_types_are_runtime_distinct() -> None:
    module = _types_module()
    for name in TYPE_NAMES:
        assert hasattr(module, name)
    ObjectId = module.ObjectId
    LogicalId = module.LogicalId
    SchemaVersion = module.SchemaVersion
    ObjectType = module.ObjectType
    assert len({ObjectId, LogicalId, SchemaVersion, ObjectType}) == 4


def test_nominal_identity_accepts_strict_strings() -> None:
    module = _types_module()
    for name in TYPE_NAMES:
        assert hasattr(module, name)

    class IdentityProbe(BaseModel):
        model_config = ConfigDict(strict=True)
        object_id: module.ObjectId
        logical_id: module.LogicalId
        schema_version: module.SchemaVersion
        object_type: module.ObjectType

    probe = IdentityProbe(
        object_id="object-opaque-id-0001",
        logical_id="logical-opaque-id-001",
        schema_version="1.0",
        object_type="di.test.object",
    )
    assert isinstance(probe.object_id, module.ObjectId)
    assert isinstance(probe.logical_id, module.LogicalId)
    assert isinstance(probe.schema_version, module.SchemaVersion)
    assert isinstance(probe.object_type, module.ObjectType)


def test_nominal_identity_rejects_non_strings() -> None:
    module = _types_module()
    for name in TYPE_NAMES:
        assert hasattr(module, name)
    for type_ in (module.ObjectId, module.LogicalId, module.SchemaVersion, module.ObjectType):
        with pytest.raises(ValidationError):
            type_(123)


def test_nominal_identity_rejects_cross_type_instances() -> None:
    module = _types_module()
    for name in TYPE_NAMES:
        assert hasattr(module, name)

    class IdentityProbe(BaseModel):
        model_config = ConfigDict(strict=True)
        object_id: module.ObjectId
        logical_id: module.LogicalId
        schema_version: module.SchemaVersion
        object_type: module.ObjectType

    object_id = module.ObjectId("object-opaque-id-0001")
    with pytest.raises(ValidationError):
        IdentityProbe(
            object_id=object_id,
            logical_id=object_id,
            schema_version="1.0",
            object_type="di.test.object",
        )


def test_nominal_identity_values_are_frozen() -> None:
    module = _types_module()
    for name in TYPE_NAMES:
        assert hasattr(module, name)
    object_id = module.ObjectId("object-opaque-id-0001")
    with pytest.raises(ValidationError):
        object_id.root = "changed"
