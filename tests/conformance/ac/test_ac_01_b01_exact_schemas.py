from __future__ import annotations

import importlib
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
from design_intelligence.registry.b01 import B01_REGISTRY_MANIFEST


ROOT = Path(__file__).resolve().parents[3]
GENERATED = ROOT / "generated" / "json_schema"

CANONICAL_FIELDS = {
    "schema_version",
    "id",
    "object_type",
    "created_at",
    "created_by",
    "tenant_scope",
    "provenance",
    "extensions",
}
REVISION_FIELDS = CANONICAL_FIELDS | {"logical_id", "revision", "parent_refs"}

MODEL_CONTRACTS = {
    StyleBrief: (
        "di.b01.style_brief",
        REVISION_FIELDS
        | {
            "category",
            "customer_segments",
            "market_channels",
            "season_occasions",
            "commercial_role",
            "price_positioning",
            "style_intent",
            "mood_aesthetic",
            "design_focus",
            "reference_intent_refs",
            "material_context",
            "fit_silhouette_direction",
            "novelty_expectation",
            "requirements",
        },
    ),
    ReferenceIntentBinding: (
        "di.b01.reference_intent_binding",
        REVISION_FIELDS
        | {
            "reference_asset_ref",
            "intent_codes",
            "application_scope",
            "preserve",
            "allow_change",
            "strength",
        },
    ),
    DesignContextBinding: (
        "di.b01.design_context_binding",
        REVISION_FIELDS | {"style_brief_ref", "bindings"},
    ),
    DesignDecision: (
        "di.b01.design_decision",
        REVISION_FIELDS
        | {
            "brief_ref",
            "context_binding_ref",
            "primary_focus",
            "secondary_focus",
            "visual_hierarchy",
            "silhouette_strategy",
            "volume_distribution",
            "construction_emphasis",
            "surface_complexity",
            "material_expression",
            "novelty_allocation",
            "commercial_risk_allocation",
        },
    ),
    DesignRoute: (
        "di.b01.design_route",
        REVISION_FIELDS | {"decision_ref", "route_name", "mechanisms", "constraints", "rationale"},
    ),
    DesignSpec: (
        "di.b01.design_spec",
        REVISION_FIELDS
        | {
            "route_ref",
            "semantic_parameter_space_ref",
            "assignments",
            "reference_intent_refs",
            "constraints",
        },
    ),
    DesignTaskBinding: (
        "di.b01.design_task_binding",
        CANONICAL_FIELDS
        | {
            "design_state_ref",
            "style_brief_ref",
            "evaluation_contract_ref",
            "enterprise_hard_policy_refs",
            "risk_policy_ref",
            "budget_policy_ref",
            "intervention_policy_ref",
            "reference_task_spec_ref",
        },
    ),
}


def test_ac_01_covers_exactly_seven_b01_canonical_objects() -> None:
    assert len(MODEL_CONTRACTS) == 7
    assert {object_type for object_type, _ in MODEL_CONTRACTS.values()} == {
        "di.b01.style_brief",
        "di.b01.reference_intent_binding",
        "di.b01.design_context_binding",
        "di.b01.design_decision",
        "di.b01.design_route",
        "di.b01.design_spec",
        "di.b01.design_task_binding",
    }


def test_json_schema_exactness_for_all_b01_models() -> None:
    for model, (object_type, required_fields) in MODEL_CONTRACTS.items():
        schema = model.model_json_schema()
        assert schema["additionalProperties"] is False
        assert set(schema["properties"]) == required_fields
        assert set(schema["required"]) == required_fields
        assert schema["properties"]["object_type"]["const"] == object_type


def test_registry_and_model_surface_agree_exactly() -> None:
    entries = B01_REGISTRY_MANIFEST.entries
    assert len(entries) == 7

    by_type = {object_type: model for model, (object_type, _) in MODEL_CONTRACTS.items()}
    assert {entry.object_type.root for entry in entries} == set(by_type)

    for entry in entries:
        module_name, class_name = entry.python_type.rsplit(".", 1)
        resolved = getattr(importlib.import_module(module_name), class_name)
        assert resolved is by_type[entry.object_type.root]
        assert resolved.model_json_schema()["properties"]["object_type"]["const"] == entry.object_type.root


def test_generated_json_schema_artifacts_are_exact_and_reproducible_inputs() -> None:
    expected_names = {
        f"{object_type}.schema.json" for object_type, _ in MODEL_CONTRACTS.values()
    }
    actual_names = {path.name for path in GENERATED.glob("di.b01.*.schema.json")}
    assert actual_names == expected_names

    for model, (object_type, _) in MODEL_CONTRACTS.items():
        path = GENERATED / f"{object_type}.schema.json"
        raw = path.read_text(encoding="utf-8")
        assert raw.endswith("\n")
        assert json.loads(raw) == model.model_json_schema()
        assert raw == json.dumps(
            model.model_json_schema(),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ) + "\n"
