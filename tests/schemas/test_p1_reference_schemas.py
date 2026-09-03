from __future__ import annotations


def _core():
    import design_intelligence.contracts.core as core
    return core


def test_reference_schema_field_sets_are_exact() -> None:
    core = _core()
    assert set(core.ExactObjectRef.model_fields) == {
        "object_type", "logical_id", "version_id", "content_hash"
    }
    assert set(core.ObjectRef.model_fields) == {
        "object_type", "object_id", "content_hash"
    }
    assert set(core.LogicalObjectRef.model_fields) == {"object_type", "logical_id"}


def test_content_hash_schema_freezes_sha256_wire_pattern() -> None:
    core = _core()
    schema = core.ContentHash.model_json_schema()
    assert schema["type"] == "string"
    assert schema["pattern"] == "^sha256:[0-9a-f]{64}$"
