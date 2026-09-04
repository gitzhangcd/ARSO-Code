from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "src" / "design_intelligence"
CORE = SOURCE / "contracts" / "core"
B01 = SOURCE / "contracts" / "b01"
REGISTRY = SOURCE / "registry"

P1_REQUIRED_CORE = {
    "CanonicalObjectClass",
    "CanonicalRef",
    "ContentHash",
    "DIModel",
    "ExactObjectRef",
    "FrozenDIModel",
    "LogicalId",
    "LogicalObjectRef",
    "ObjectId",
    "ObjectRef",
    "ObjectType",
    "SchemaVersion",
    "canonical_json_bytes",
    "compute_content_hash",
}

P1_REQUIRED_REGISTRY = {
    "ObjectRegistryEntry",
    "ObjectRegistryManifest",
    "PrimitiveOwner",
    "ReferenceKind",
    "RegistryIndex",
    "StateDomain",
}

P3_PLUS_FORBIDDEN_SYMBOLS = {
    "FashionOntology",
    "DesignGrammar",
    "SemanticParameterSpace",
    "ExactReferenceResolver",
    "CanonicalObjectStore",
    "BranchHeadPointer",
    "ApproveDesignCommand",
    "ReviewSessionClosedEvent",
}


def test_p1_public_api_exact_sets_remain_frozen_during_p2() -> None:
    import design_intelligence.contracts as contracts
    import design_intelligence.contracts.core as core
    import design_intelligence.registry as registry

    assert set(core.__all__) == P1_REQUIRED_CORE
    assert set(contracts.__all__) == P1_REQUIRED_CORE
    assert set(registry.__all__) == P1_REQUIRED_REGISTRY


def test_p3_plus_symbols_are_not_implemented_during_p2() -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in SOURCE.rglob("*.py"))
    for symbol in P3_PLUS_FORBIDDEN_SYMBOLS:
        assert symbol not in text


def test_only_authorized_namespaces_may_define_classes_through_p2() -> None:
    for path in SOURCE.rglob("*.py"):
        if CORE in path.parents or B01 in path.parents or REGISTRY in path.parents:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        class_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        assert class_names == [], f"P2 forbids classes outside core/B01/registry in {path}: {class_names}"
