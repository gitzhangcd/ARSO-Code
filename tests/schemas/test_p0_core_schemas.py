from pydantic import BaseModel

from design_intelligence.contracts.core.types import (
    CanonicalObjectClass,
    LogicalId,
    ObjectId,
    ObjectType,
    SchemaVersion,
)


class SchemaProbe(BaseModel):
    object_id: ObjectId
    logical_id: LogicalId
    schema_version: SchemaVersion
    object_type: ObjectType
    object_class: CanonicalObjectClass


def test_nominal_types_generate_distinct_named_definitions() -> None:
    schema = SchemaProbe.model_json_schema()
    defs = schema["$defs"]
    assert {"ObjectId", "LogicalId", "SchemaVersion", "ObjectType"}.issubset(defs)
    for name in ("ObjectId", "LogicalId", "SchemaVersion", "ObjectType"):
        assert defs[name]["type"] == "string"


def test_object_class_schema_has_exact_wire_enum() -> None:
    schema = SchemaProbe.model_json_schema()
    enum_values = set(schema["$defs"]["CanonicalObjectClass"]["enum"])
    assert enum_values == {
        "CANONICAL_REVISION",
        "IMMUTABLE_FACT",
        "IMMUTABLE_ROOT",
        "IMMUTABLE_GRAPH_NODE",
        "SNAPSHOT",
        "OPERATIONAL_CONTROL_STATE",
        "DERIVED_VIEW",
    }


def test_p0_does_not_freeze_unowned_lexical_patterns() -> None:
    schema = SchemaProbe.model_json_schema()
    defs = schema["$defs"]
    for name in ("ObjectId", "LogicalId", "SchemaVersion", "ObjectType"):
        assert "pattern" not in defs[name]
