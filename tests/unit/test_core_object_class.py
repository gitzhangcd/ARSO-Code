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

P0_PUBLIC_API = {
    "CanonicalObjectClass",
    "DIModel",
    "FrozenDIModel",
    "LogicalId",
    "ObjectId",
    "ObjectType",
    "SchemaVersion",
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


def test_p0_public_api_remains_available_after_p1() -> None:
    import design_intelligence.contracts as contracts
    import design_intelligence.contracts.core as core

    assert P0_PUBLIC_API.issubset(core.__all__)
    assert P0_PUBLIC_API.issubset(contracts.__all__)
    for name in P0_PUBLIC_API:
        assert hasattr(core, name)
        assert hasattr(contracts, name)


def test_unfrozen_object_class_alias_is_not_introduced() -> None:
    assert not hasattr(types, "ObjectClass")
