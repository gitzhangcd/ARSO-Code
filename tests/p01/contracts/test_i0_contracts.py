from pydantic import ValidationError

from arso.p01.contracts import (
    DiagnosisConditionSpec,
    DiagnosisConditionType,
    DiagnosisInjection,
    IntegrityStatus,
    P01IntegrityReport,
    P01MatchedBlock,
    RepairRequest,
)


def test_repair_request_has_no_raw_condition_field() -> None:
    assert "condition_type" not in RepairRequest.model_fields


def test_repair_request_rejects_expected_repair_target() -> None:
    payload = {
        "request_id": "req-1",
        "trial_id": "trial-1",
        "reference_task_ref": "task-1",
        "baseline_system_ref": "snapshot-1",
        "visible_evidence_ref": "evidence-1",
        "diagnosis_injection_ref": "diag-1",
        "mutation_policy_ref": "mutation-1",
        "repair_instruction_ref": "instruction-1",
        "model_binding_ref": "model-1",
        "sampling_config_ref": "sampling-1",
        "output_contract_ref": "output-1",
        "budget_ref": "budget-1",
        "seed_ref": "seed-1",
        "expected_repair_target": "forbidden",
    }
    try:
        RepairRequest.model_validate(payload)
    except ValidationError:
        pass
    else:
        raise AssertionError("RepairRequest accepted sealed repair target")


def test_none_diagnosis_injection_allows_no_visible_payload() -> None:
    injection = DiagnosisInjection(
        injection_id="diag-1",
        trial_id="trial-1",
        condition=DiagnosisConditionType.NONE,
        visible_payload=None,
        visible_payload_hash=None,
        materialization_method="frozen-template",
        source_visibility="REPAIR_VISIBLE",
    )
    assert injection.visible_payload is None


def test_matched_block_requires_all_four_conditions() -> None:
    block = P01MatchedBlock(
        matched_block_id="block-1",
        scenario_ref="scenario-1",
        fixture_ref="fixture-1",
        replicate_index=0,
        required_conditions=(
            DiagnosisConditionType.ORACLE,
            DiagnosisConditionType.WRONG,
            DiagnosisConditionType.NONE,
            DiagnosisConditionType.IMPLICIT,
        ),
        shared_control_spec_ref="control-1",
        expected_trial_refs=("t1", "t2", "t3", "t4"),
        status="PLANNED",
    )
    assert set(block.required_conditions) == set(DiagnosisConditionType)


def test_condition_spec_is_frozen_before_run() -> None:
    spec = DiagnosisConditionSpec(
        condition_id="cond-oracle",
        condition_type=DiagnosisConditionType.ORACLE,
        template_ref="template-1",
        materialization_policy_ref="policy-1",
        source_policy="SEALED_ORACLE_ONLY",
        visibility_policy="REPAIR_VISIBLE_PAYLOAD_ONLY",
        frozen_before_run=True,
        content_hash="sha256:" + "0" * 64,
    )
    assert spec.frozen_before_run is True


def test_integrity_report_has_explicit_final_status() -> None:
    report = P01IntegrityReport(
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
        truth_firewall_pass=True,
        diagnosis_visibility_pass=True,
        evaluator_leakage_pass=True,
        retry_policy_pass=True,
        budget_accounting_pass=True,
        raw_record_complete=True,
        violations=(),
        final_status=IntegrityStatus.PASS,
    )
    assert report.final_status is IntegrityStatus.PASS
