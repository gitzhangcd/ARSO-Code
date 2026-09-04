#!/usr/bin/env python3
"""Export the frozen seven-object B01 JSON Schema surface deterministically."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from design_intelligence.contracts.b01 import (
    DesignContextBinding,
    DesignDecision,
    DesignRoute,
    DesignSpec,
    DesignTaskBinding,
    ReferenceIntentBinding,
    StyleBrief,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "generated" / "json_schema"

MODEL_EXPORTS = (
    ("di.b01.style_brief", StyleBrief),
    ("di.b01.reference_intent_binding", ReferenceIntentBinding),
    ("di.b01.design_context_binding", DesignContextBinding),
    ("di.b01.design_decision", DesignDecision),
    ("di.b01.design_route", DesignRoute),
    ("di.b01.design_spec", DesignSpec),
    ("di.b01.design_task_binding", DesignTaskBinding),
)


def render_schema(model: type) -> str:
    return json.dumps(
        model.model_json_schema(),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def expected_documents() -> dict[str, str]:
    return {
        f"{object_type}.schema.json": render_schema(model)
        for object_type, model in MODEL_EXPORTS
    }


def export(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    expected = expected_documents()
    for path in output_dir.glob("di.b01.*.schema.json"):
        if path.name not in expected:
            path.unlink()
    for name, content in expected.items():
        (output_dir / name).write_text(content, encoding="utf-8")


def check(output_dir: Path) -> int:
    expected = expected_documents()
    actual_names = {path.name for path in output_dir.glob("di.b01.*.schema.json")}
    if actual_names != set(expected):
        return 1
    for name, content in expected.items():
        path = output_dir / name
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.check:
        return check(args.output)
    export(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
