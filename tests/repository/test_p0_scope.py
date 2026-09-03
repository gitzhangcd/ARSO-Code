from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "src" / "design_intelligence" / "contracts" / "core"

P0_REQUIRED_SYMBOLS = (
    "ObjectId",
    "LogicalId",
    "SchemaVersion",
    "ObjectType",
    "CanonicalObjectClass",
    "DIModel",
    "FrozenDIModel",
)

P1_FORBIDDEN_SYMBOLS = (
    "ExactObjectRef",
    "ObjectRef",
    "LogicalObjectRef",
    "CanonicalPayload",
    "canonical_hash",
    "compute_content_hash",
    "ObjectRegistry",
)


def test_p0_required_core_symbols_are_present() -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in CORE.glob("*.py"))
    for symbol in P0_REQUIRED_SYMBOLS:
        assert symbol in text


def test_p1_symbols_are_not_implemented_early() -> None:
    source_root = ROOT / "src" / "design_intelligence"
    text = "\n".join(path.read_text(encoding="utf-8") for path in source_root.rglob("*.py"))
    for symbol in P1_FORBIDDEN_SYMBOLS:
        assert symbol not in text


def test_non_core_contract_namespaces_remain_skeleton_only() -> None:
    source_root = ROOT / "src" / "design_intelligence"
    for path in source_root.rglob("*.py"):
        if CORE in path.parents or path == CORE / "__init__.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        class_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        assert class_names == [], f"P0 forbids non-core classes in {path}: {class_names}"
