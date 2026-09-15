"""Machine-verifiable pre-run lock for the P0.1 pilot."""

from design_intelligence.contracts.core import ContentHash

from .base import FrozenP01Model


class P01PreRunLock(FrozenP01Model):
    schema_version: str
    experiment_id: str
    batch_id: str
    authority_refs: tuple[str, ...]
    scenario_manifest_ref: str
    fixture_bundle_ref: str
    qualification_bundle_ref: str
    condition_spec_refs: tuple[str, ...]
    repair_instruction_ref: str
    repair_operator_ref: str
    mutation_policy_ref: str
    model_binding_ref: str
    model_parameters_ref: str
    evaluator_binding_ref: str
    validation_plan_ref: str
    budget_policy_ref: str
    retry_policy_ref: str
    seed_schedule_ref: str
    runtime_semantics_ref: str
    analysis_plan_ref: str
    created_at: str
    created_by: str
    canonical_payload_hash: ContentHash
