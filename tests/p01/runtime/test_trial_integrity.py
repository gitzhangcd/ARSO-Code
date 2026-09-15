from arso.p01.contracts.enums import IntegrityStatus
from arso.p01.runtime.integrity import TrialIntegrityChecker


def _checks(**updates):
    values = dict(
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
        truth_firewall_pass=True,
        diagnosis_visibility_pass=True,
        evaluator_leakage_pass=True,
        retry_policy_pass=True,
        budget_accounting_pass=True,
        raw_record_complete=True,
    )
    values.update(updates)
    return values


def test_clean_trial_integrity_passes():
    report = TrialIntegrityChecker().check("trial-1", **_checks())
    assert report.final_status is IntegrityStatus.PASS
    assert report.violations == ()


def test_integrity_failure_is_derived_and_coded():
    report = TrialIntegrityChecker().check(
        "trial-1",
        **_checks(truth_firewall_pass=False, mutation_policy_match=False),
    )
    assert report.final_status is IntegrityStatus.FAIL
    assert "truth_firewall_pass" in report.violations
    assert "mutation_policy_match" in report.violations
