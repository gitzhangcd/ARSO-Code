from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "src" / "design_intelligence"
CORE = SOURCE / "contracts" / "core"
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

P2_PLUS_FORBIDDEN_SYMBOLS = {
    "StyleBrief",
    "DesignContextBinding",
    "DesignDecision",
    "DesignRoute",
    "DesignSpec",
    "FashionOntology",
    "DesignGrammar",
    "SemanticParameterSpace",
    "ExactReferenceResolver",
    "CanonicalObjectStore",
    "BranchHeadPointer",
    "ApproveDesignCommand",
    "ReviewSessionClosedEvent",
}


def test_p1_public_api_exact_sets() -> None:
    import design_intelligence.contracts as contracts
    import design_intelligence.contracts.core as core
    import design_intelligence.registry as registry

    assert set(core.__all__) == P1_REQUIRED_CORE
    assert set(contracts.__all__) == P1_REQUIRED_CORE
    assert set(registry.__all__) == P1_REQUIRED_REGISTRY


def test_p2_plus_symbols_are_not_implemented_early() -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in SOURCE.rglob("*.py"))
    for symbol in P2_PLUS_FORBIDDEN_SYMBOLS:
        assert symbol not in text


def test_only_core_and_registry_may_define_classes_during_p1() -> None:
    for path in SOURCE.rglob("*.py"):
        if CORE in path.parents or REGISTRY in path.parents:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        class_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        assert class_names == [], f"P1 forbids classes outside core/registry in {path}: {class_names}"
