import pytest

from arso.p01.contracts.enums import DiagnosisConditionType, IntegrityStatus
from arso.p01.contracts.trial import P01TrialAssignment
from arso.p01.runtime.matched_control import MatchedControlChecker


@pytest.fixture
def four_assignments():
    values = []
    for condition in DiagnosisConditionType:
        values.append(
            P01TrialAssignment(
                trial_id=f"trial-{condition.value.lower()}",
                batch_ref="synthetic-harness-only",
                scenario_ref="synthetic_001",
                matched_block_id="block-1",
                condition=condition,
                replicate_index=0,
                fixture_ref="synthetic_001",
                fixture_qualification_ref="synthetic_001_qualification",
                reference_task_ref="synthetic_001",
                base_snapshot_ref="synthetic_001_baseline",
                visible_evidence_ref="synthetic_001_public_evidence",
                diagnosis_condition_ref=f"condition-{condition.value.lower()}",
                repair_operator_ref="deterministic_fake_repair_v1",
                repair_instruction_ref="synthetic_repair_instruction_v1",
                mutation_policy_ref="mapping_only_v1",
                evaluator_binding_ref="synthetic_exact_evaluator_v1",
                validation_plan_ref="synthetic_validation_v1",
                budget_policy_ref="synthetic_budget_v1",
                retry_policy_ref="no_retry_v1",
                seed_assignment_ref="deterministic_seed_v1",
                pre_run_lock_hash="sha256:" + "1" * 64,
                matched_control_fingerprint="sha256:" + "2" * 64,
                created_at="2026-09-15T00:00:00Z",
            )
        )
    return values


def test_clean_block_passes_matched_control_check(four_assignments):
    report = MatchedControlChecker().check(tuple(four_assignments))
    assert report.final_status is IntegrityStatus.PASS
    assert report.condition_is_only_intended_difference is True


def test_evidence_mismatch_invalidates_block(four_assignments):
    bad = list(four_assignments)
    bad[1] = bad[1].model_copy(update={"visible_evidence_ref": "different-evidence"})
    report = MatchedControlChecker().check(tuple(bad))
    assert report.final_status is IntegrityStatus.FAIL
    assert report.shared_visible_evidence is False


def test_missing_condition_invalidates_block(four_assignments):
    report = MatchedControlChecker().check(tuple(four_assignments[:-1]))
    assert report.final_status is IntegrityStatus.FAIL
    assert report.all_required_conditions_present is False
