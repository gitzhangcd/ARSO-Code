"""Repair-visible request contract for ARSO P0.1."""

from .base import FrozenP01Model


class RepairRequest(FrozenP01Model):
    request_id: str
    trial_id: str
    reference_task_ref: str
    baseline_system_ref: str
    visible_evidence_ref: str
    diagnosis_injection_ref: str
    mutation_policy_ref: str
    repair_instruction_ref: str
    model_binding_ref: str
    sampling_config_ref: str
    output_contract_ref: str
    budget_ref: str
    seed_ref: str
