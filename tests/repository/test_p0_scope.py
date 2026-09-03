from __future__ import annotations

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


def test_p0_required_core_symbols_are_present() -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in CORE.glob("*.py"))
    for symbol in P0_REQUIRED_SYMBOLS:
        assert symbol in text
