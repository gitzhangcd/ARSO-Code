"""Thin deterministic four-condition runner for the P0.1 synthetic harness."""

from pathlib import Path
from typing import Mapping

from arso.p01.adapters.fake.evaluator import SyntheticExactEvaluator
from arso.p01.adapters.fake.fixture import SyntheticFixtureProvider
from arso.p01.adapters.fake.repair import DeterministicFakeRepairOperator
from arso.p01.contracts.enums import DiagnosisConditionType
from arso.p01.contracts.synthetic import (
    SyntheticEvaluationContext,
    SyntheticMatchedBlockResult,
    SyntheticTrialOutcome,
)
from arso.p01.contracts.trial import P01TrialAssignment

from .admission import ScientificAdmissionGate
from .candidate import CandidateMaterializer
from .diagnosis import SyntheticDiagnosisInjector
from .evaluator_blindness import EvaluatorBlindnessGuard
from .integrity import TrialIntegrityChecker
from .matched_control import MatchedControlChecker
from .repair_request import SyntheticRepairRequestBuilder
from .truth_firewall import TruthFirewall
from .validation import SyntheticValidator


DEFAULT_ROOT = Path("experiments/p0_1_oracle_diagnosis/fixtures/synthetic_001")


class SyntheticMatchedBlockRunner:
    def __init__(self, provider: SyntheticFixtureProvider) -> None:
        self.provider = provider

    @classmethod
    def default(cls) -> "SyntheticMatchedBlockRunner":
        return cls(SyntheticFixtureProvider(DEFAULT_ROOT, TruthFirewall()))

    @staticmethod
    def _assignment(condition: DiagnosisConditionType) -> P01TrialAssignment:
        return P01TrialAssignment(
            trial_id=f"trial-{condition.value.lower()}",
            batch_ref="synthetic-harness-only",
            scenario_ref="synthetic_001",
            matched_block_id="synthetic-block-001",
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

    def run(
        self,
        contamination: Mapping[str, Mapping[str, object]] | None = None,
    ) -> SyntheticMatchedBlockResult:
        assignments = [self._assignment(condition) for condition in DiagnosisConditionType]
        contamination = contamination or {}
        assignments = [
            assignment.model_copy(update=dict(contamination.get(assignment.condition.value, {})))
            for assignment in assignments
        ]

        injector = SyntheticDiagnosisInjector(self.provider)
        request_builder = SyntheticRepairRequestBuilder()
        materializer = CandidateMaterializer()
        evaluator = SyntheticExactEvaluator()
        blindness_guard = EvaluatorBlindnessGuard()
        validator = SyntheticValidator()
        integrity_checker = TrialIntegrityChecker()
        admission_gate = ScientificAdmissionGate()

        outcomes: list[SyntheticTrialOutcome] = []

        for assignment in assignments:
            public = self.provider.load_public()
            diagnosis = injector.materialize(assignment)
            request = request_builder.build(assignment, public, diagnosis)

            repair_operator = DeterministicFakeRepairOperator(
                {diagnosis.injection_id: diagnosis.visible_payload}
            )
            proposal = repair_operator.repair(request)

            baseline = dict(public["baseline"]["mapping"])
            baseline_before = dict(baseline)
            candidate = materializer.materialize(
                base_snapshot_ref=assignment.base_snapshot_ref,
                baseline_mapping=baseline,
                proposal=proposal,
                allowed_targets={"transformation_spec.mapping"},
            )

            evaluation_truth = self.provider.load_evaluation_truth()
            context = SyntheticEvaluationContext(
                context_id=f"evaluation-context-{assignment.trial_id}",
                task_ref=assignment.reference_task_ref,
                expected_mapping=dict(evaluation_truth["expected_patch"]),
            )
            blindness_guard.check(
                {
                    "candidate_ref": candidate.candidate_id,
                    "task_ref": context.task_ref,
                }
            )
            evaluation = evaluator.evaluate(candidate, context)

            mutation_policy_pass = set(candidate.changed_targets).issubset(
                {"transformation_spec.mapping"}
            )
            validation = validator.validate(
                assignment.trial_id,
                target_behavior_pass=evaluation.passed,
                hard_constraints_pass=evaluation.passed,
                baseline_immutable=(baseline == baseline_before),
                mutation_policy_pass=mutation_policy_pass,
            )

            integrity = integrity_checker.check(
                assignment.trial_id,
                lock_hash_valid=True,
                fixture_hash_valid=True,
                matched_control_valid=True,
                model_match=True,
                evidence_match=True,
                repair_operator_match=True,
                mutation_policy_match=mutation_policy_pass,
                evaluator_match=True,
                budget_policy_match=True,
                seed_policy_match=True,
                truth_firewall_pass=True,
                diagnosis_visibility_pass=(
                    assignment.condition is DiagnosisConditionType.ORACLE
                    or diagnosis.visible_payload is None
                    or not self.provider.sealed_access_log
                    or all(
                        event[0] != "ORACLE_DIAGNOSIS_MATERIALIZATION"
                        or event[1] == "ORACLE"
                        for event in self.provider.sealed_access_log
                    )
                ),
                evaluator_leakage_pass=(not evaluation.condition_metadata_present),
                retry_policy_pass=True,
                budget_accounting_pass=True,
                raw_record_complete=True,
            )
            admission = admission_gate.admit(integrity, validation)

            outcomes.append(
                SyntheticTrialOutcome(
                    trial_id=assignment.trial_id,
                    condition=assignment.condition,
                    matched_control_fingerprint=str(
                        assignment.matched_control_fingerprint
                    ),
                    candidate_ref=candidate.candidate_id,
                    evaluation_ref=evaluation.evaluation_id,
                    validation_ref=validation.validation_id,
                    integrity_status=integrity.final_status,
                    admission_state=admission,
                )
            )

        block_integrity = MatchedControlChecker().check(tuple(assignments))
        return SyntheticMatchedBlockResult(
            block_id="synthetic-block-001",
            trial_outcomes=tuple(outcomes),
            block_integrity=block_integrity,
            scientific_interpretation=None,
        )
