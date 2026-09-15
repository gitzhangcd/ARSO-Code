"""Trial-assignment and matched-block contracts for ARSO P0.1."""

from pydantic import model_validator

from design_intelligence.contracts.core import ContentHash

from .base import FrozenP01Model
from .enums import DiagnosisConditionType


class P01MatchedBlock(FrozenP01Model):
    matched_block_id: str
    scenario_ref: str
    fixture_ref: str
    replicate_index: int
    required_conditions: tuple[DiagnosisConditionType, ...]
    shared_control_spec_ref: str
    expected_trial_refs: tuple[str, ...]
    status: str

    @model_validator(mode="after")
    def require_exact_treatment_set(self) -> "P01MatchedBlock":
        expected = set(DiagnosisConditionType)
        observed = set(self.required_conditions)
        if len(self.required_conditions) != len(expected) or observed != expected:
            raise ValueError("matched block must contain ORACLE, WRONG, NONE, and IMPLICIT exactly once")
        return self


class P01TrialAssignment(FrozenP01Model):
    trial_id: str
    batch_ref: str
    scenario_ref: str
    matched_block_id: str
    condition: DiagnosisConditionType
    replicate_index: int
    fixture_ref: str
    fixture_qualification_ref: str
    reference_task_ref: str
    base_snapshot_ref: str
    visible_evidence_ref: str
    diagnosis_condition_ref: str
    repair_operator_ref: str
    repair_instruction_ref: str
    mutation_policy_ref: str
    evaluator_binding_ref: str
    validation_plan_ref: str
    budget_policy_ref: str
    retry_policy_ref: str
    seed_assignment_ref: str
    pre_run_lock_hash: ContentHash
    matched_control_fingerprint: ContentHash
    created_at: str
