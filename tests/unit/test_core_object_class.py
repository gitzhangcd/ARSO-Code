from design_intelligence.contracts.core import types


EXPECTED_VALUES = {
    "CANONICAL_REVISION",
    "IMMUTABLE_FACT",
    "IMMUTABLE_ROOT",
    "IMMUTABLE_GRAPH_NODE",
    "SNAPSHOT",
    "OPERATIONAL_CONTROL_STATE",
    "DERIVED_VIEW",
}


def test_canonical_object_class_symbol_exists() -> None:
    assert hasattr(types, "CanonicalObjectClass")


def test_canonical_object_class_values_match_frozen_contract() -> None:
    assert hasattr(types, "CanonicalObjectClass")
    enum_type = types.CanonicalObjectClass
    assert {member.value for member in enum_type} == EXPECTED_VALUES


def test_canonical_object_class_is_string_enum() -> None:
    assert hasattr(types, "CanonicalObjectClass")
    enum_type = types.CanonicalObjectClass
    assert enum_type.CANONICAL_REVISION == "CANONICAL_REVISION"


def test_core_and_contract_packages_export_only_p0_public_api() -> None:
    import design_intelligence.contracts as contracts
    import design_intelligence.contracts.core as core

    expected = {
        "CanonicalObjectClass",
        "DIModel",
        "FrozenDIModel",
        "LogicalId",
        "ObjectId",
        "ObjectType",
        "SchemaVersion",
    }
    assert set(core.__all__) == expected
    assert set(contracts.__all__) == expected
    for name in expected:
        assert hasattr(core, name)
        assert hasattr(contracts, name)


def test_unfrozen_object_class_alias_is_not_introduced() -> None:
    assert not hasattr(types, "ObjectClass")
