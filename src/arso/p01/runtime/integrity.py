"""Trial-level scientific integrity derivation for the P0.1 synthetic harness."""

from arso.p01.contracts.enums import IntegrityStatus
from arso.p01.contracts.integrity import P01IntegrityReport


class TrialIntegrityChecker:
    def check(
        self,
        trial_id: str,
        *,
        lock_hash_valid: bool,
        fixture_hash_valid: bool,
        matched_control_valid: bool,
        model_match: bool,
        evidence_match: bool,
        repair_operator_match: bool,
        mutation_policy_match: bool,
        evaluator_match: bool,
        budget_policy_match: bool,
        seed_policy_match: bool,
        truth_firewall_pass: bool,
        diagnosis_visibility_pass: bool,
        evaluator_leakage_pass: bool,
        retry_policy_pass: bool,
        budget_accounting_pass: bool,
        raw_record_complete: bool,
    ) -> P01IntegrityReport:
        checks = {
            "lock_hash_valid": lock_hash_valid,
            "fixture_hash_valid": fixture_hash_valid,
            "matched_control_valid": matched_control_valid,
            "model_match": model_match,
            "evidence_match": evidence_match,
            "repair_operator_match": repair_operator_match,
            "mutation_policy_match": mutation_policy_match,
            "evaluator_match": evaluator_match,
            "budget_policy_match": budget_policy_match,
            "seed_policy_match": seed_policy_match,
            "truth_firewall_pass": truth_firewall_pass,
            "diagnosis_visibility_pass": diagnosis_visibility_pass,
            "evaluator_leakage_pass": evaluator_leakage_pass,
            "retry_policy_pass": retry_policy_pass,
            "budget_accounting_pass": budget_accounting_pass,
            "raw_record_complete": raw_record_complete,
        }
        violations = tuple(name for name, value in checks.items() if not value)
        status = IntegrityStatus.PASS if not violations else IntegrityStatus.FAIL
        return P01IntegrityReport(
            integrity_report_id=f"integrity-{trial_id}",
            trial_id=trial_id,
            violations=violations,
            final_status=status,
            **checks,
        )
