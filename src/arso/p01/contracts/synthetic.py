"""Harness-only synthetic records for ARSO P0.1 I1."""

from typing import Mapping

from .base import FrozenP01Model
from .enums import (
    DiagnosisConditionType,
    IntegrityStatus,
    ScientificAdmissionState,
    ValidationState,
)


class SyntheticEvaluationContext(FrozenP01Model):
    context_id: str
    task_ref: str
    expected_mapping: Mapping[str, str]


class SyntheticEvaluationRecord(FrozenP01Model):
    evaluation_id: str
    trial_id: str
    candidate_ref: str
    passed: bool
    observations: tuple[str, ...]
    condition_metadata_present: bool = False


class SyntheticValidationResult(FrozenP01Model):
    validation_id: str
    trial_id: str
    state: ValidationState
    target_behavior_pass: bool
    hard_constraints_pass: bool
    baseline_immutable: bool
    mutation_policy_pass: bool
    reasons: tuple[str, ...]


class SyntheticTrialOutcome(FrozenP01Model):
    trial_id: str
    condition: DiagnosisConditionType
    matched_control_fingerprint: str
    candidate_ref: str
    evaluation_ref: str
    validation_ref: str
    integrity_status: IntegrityStatus
    admission_state: ScientificAdmissionState


class MatchedBlockIntegrityReport(FrozenP01Model):
    block_id: str
    all_required_conditions_present: bool
    shared_fixture: bool
    shared_visible_evidence: bool
    shared_repair_operator: bool
    shared_mutation_policy: bool
    shared_evaluator: bool
    shared_budget_policy: bool
    shared_seed_policy: bool
    shared_pre_run_lock: bool
    shared_matched_control_fingerprint: bool
    condition_is_only_intended_difference: bool
    violations: tuple[str, ...]
    final_status: IntegrityStatus


class SyntheticMatchedBlockResult(FrozenP01Model):
    block_id: str
    trial_outcomes: tuple[SyntheticTrialOutcome, ...]
    block_integrity: MatchedBlockIntegrityReport
    scientific_interpretation: None = None
