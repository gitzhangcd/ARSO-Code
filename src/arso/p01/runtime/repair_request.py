"""Builds the strict repair-visible request used by the synthetic harness."""

from arso.p01.contracts.diagnosis import DiagnosisInjection
from arso.p01.contracts.repair import RepairRequest
from arso.p01.contracts.trial import P01TrialAssignment


class SyntheticRepairRequestBuilder:
    def build(
        self,
        assignment: P01TrialAssignment,
        fixture: dict[str, object],
        diagnosis: DiagnosisInjection,
    ) -> RepairRequest:
        return RepairRequest(
            request_id=f"req-{assignment.trial_id}",
            trial_id=assignment.trial_id,
            reference_task_ref=assignment.reference_task_ref,
            baseline_system_ref=assignment.base_snapshot_ref,
            visible_evidence_ref=assignment.visible_evidence_ref,
            diagnosis_injection_ref=diagnosis.injection_id,
            mutation_policy_ref=assignment.mutation_policy_ref,
            repair_instruction_ref=assignment.repair_instruction_ref,
            model_binding_ref=assignment.repair_operator_ref,
            sampling_config_ref="deterministic_v1",
            output_contract_ref="repair_proposal_v1",
            budget_ref=assignment.budget_policy_ref,
            seed_ref=assignment.seed_assignment_ref,
        )
