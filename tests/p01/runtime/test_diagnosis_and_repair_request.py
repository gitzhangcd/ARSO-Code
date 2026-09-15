from pathlib import Path

from arso.p01.adapters.fake.fixture import SyntheticFixtureProvider
from arso.p01.contracts.enums import DiagnosisConditionType
from arso.p01.runtime.diagnosis import SyntheticDiagnosisInjector
from arso.p01.runtime.truth_firewall import TruthFirewall


ROOT = Path("experiments/p0_1_oracle_diagnosis/fixtures/synthetic_001")


def _assignment(condition):
    from arso.p01.contracts.trial import P01TrialAssignment

    return P01TrialAssignment(
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


def test_none_materializes_null_payload_without_sealed_access():
    provider = SyntheticFixtureProvider(ROOT, TruthFirewall())
    injector = SyntheticDiagnosisInjector(provider)
    injection = injector.materialize(_assignment(DiagnosisConditionType.NONE))
    assert injection.visible_payload is None
    assert provider.sealed_access_log == ()


def test_wrong_uses_frozen_wrong_payload_without_sealed_access():
    provider = SyntheticFixtureProvider(ROOT, TruthFirewall())
    injector = SyntheticDiagnosisInjector(provider)
    injection = injector.materialize(_assignment(DiagnosisConditionType.WRONG))
    assert "formatting" in injection.visible_payload.lower()
    assert "reversed" not in injection.visible_payload.lower()
    assert provider.sealed_access_log == ()


def test_oracle_exposes_only_approved_visible_payload():
    provider = SyntheticFixtureProvider(ROOT, TruthFirewall())
    injector = SyntheticDiagnosisInjector(provider)
    injection = injector.materialize(_assignment(DiagnosisConditionType.ORACLE))
    assert (
        injection.visible_payload
        == "The A↔B mapping rule in the transformation specification is reversed."
    )
    assert "expected_patch" not in injection.model_dump()


def test_implicit_has_no_explicit_fault_locus_or_mechanism():
    provider = SyntheticFixtureProvider(ROOT, TruthFirewall())
    injector = SyntheticDiagnosisInjector(provider)
    injection = injector.materialize(_assignment(DiagnosisConditionType.IMPLICIT))
    text = injection.visible_payload.lower()
    assert "mapping" not in text
    assert "reversed" not in text
    assert "fault" not in text
