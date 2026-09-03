from __future__ import annotations

import inspect
import json
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel

from di_contracts import b03, b04, b05, b06, b07, b08
from di_contracts.commands import base as commands_base, models as commands_models
from di_contracts.events import models as event_models
from di_contracts.core.hashing import canonical_json_bytes
from di_contracts.registry.manifest import REGISTRY_ENTRIES

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "generated" / "json_schema"
SCHEMA_DIR.mkdir(parents=True, exist_ok=True)

modules = [b03, b04, b05, b06, b07, b08, commands_base, commands_models, event_models]
exported = []
for module in modules:
    for name, cls in inspect.getmembers(module, inspect.isclass):
        if issubclass(cls, BaseModel) and cls.__module__.startswith("di_contracts"):
            schema = cls.model_json_schema()
            path = SCHEMA_DIR / f"{cls.__module__.replace('.', '_')}__{name}.schema.json"
            path.write_text(json.dumps(schema, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
            exported.append(str(path.relative_to(ROOT)))

manifest_payload = {
    "schema_version": "1.0",
    "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "entry_count": len(REGISTRY_ENTRIES),
    "entries": [e.model_dump(mode="json") for e in REGISTRY_ENTRIES],
}
(ROOT / "generated" / "registry_manifest.json").write_text(
    json.dumps(manifest_payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
)
(ROOT / "generated" / "schema_index.json").write_text(
    json.dumps({"count": len(exported), "schemas": sorted(exported)}, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(f"exported {len(exported)} JSON schemas and {len(REGISTRY_ENTRIES)} registry entries")
