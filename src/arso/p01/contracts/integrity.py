"""Scientific-integrity report contract for ARSO P0.1."""

from .base import FrozenP01Model
from .enums import IntegrityStatus


class P01IntegrityReport(FrozenP01Model):
    integrity_report_id: str
    trial_id: str
    lock_hash_valid: bool
    fixture_hash_valid: bool
    matched_control_valid: bool
    model_match: bool
    evidence_match: bool
    repair_operator_match: bool
    mutation_policy_match: bool
    evaluator_match: bool
    budget_policy_match: bool
    seed_policy_match: bool
    truth_firewall_pass: bool
    diagnosis_visibility_pass: bool
    evaluator_leakage_pass: bool
    retry_policy_pass: bool
    budget_accounting_pass: bool
    raw_record_complete: bool
    violations: tuple[str, ...]
    final_status: IntegrityStatus
