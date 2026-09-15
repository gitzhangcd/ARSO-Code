from arso.p01.contracts.enums import IntegrityStatus, ScientificAdmissionState, ValidationState
from arso.p01.runtime.admission import ScientificAdmissionGate


def test_validation_acceptance_does_not_bypass_failed_integrity():
    from arso.p01.contracts.integrity import P01IntegrityReport
    from arso.p01.contracts.synthetic import SyntheticValidationResult

    integrity = P01IntegrityReport(
        integrity_report_id="ir-1",
        trial_id="trial-1",
        lock_hash_valid=True,
        fixture_hash_valid=True,
        matched_control_valid=True,
        model_match=True,
        evidence_match=True,
        repair_operator_match=True,
        mutation_policy_match=True,
        evaluator_match=True,
        budget_policy_match=True,
        seed_policy_match=True,
        truth_firewall_pass=False,
        diagnosis_visibility_pass=True,
        evaluator_leakage_pass=True,
        retry_policy_pass=True,
        budget_accounting_pass=True,
        raw_record_complete=True,
        violations=("truth-firewall",),
        final_status=IntegrityStatus.FAIL,
    )
    validation = SyntheticValidationResult(
        validation_id="v-1",
        trial_id="trial-1",
        state=ValidationState.ACCEPTED,
        target_behavior_pass=True,
        hard_constraints_pass=True,
        baseline_immutable=True,
        mutation_policy_pass=True,
        reasons=(),
    )
    assert (
        ScientificAdmissionGate().admit(integrity, validation)
        is ScientificAdmissionState.INVALID_CONTAMINATION
    )
