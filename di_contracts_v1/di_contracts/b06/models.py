from __future__ import annotations
from enum import StrEnum
from pydantic import model_validator
from di_contracts.core.base import FrozenDIModel
from di_contracts.core.models import ExactObjectRef, ImmutableFact, ImmutableRoot, ObjectRef, OperationalControlState

class EffectivePermissionStatus(StrEnum):
    DENIED="DENIED"; READ_ONLY="READ_ONLY"; SANDBOX_ONLY="SANDBOX_ONLY"; HUMAN_GATED="HUMAN_GATED"; AUTO_ALLOWED="AUTO_ALLOWED"
class InterventionTransactionPhase(StrEnum):
    PLANNED="PLANNED"; AUTHORIZED="AUTHORIZED"; SANDBOX_APPLIED="SANDBOX_APPLIED"; VALIDATING="VALIDATING"; ACCEPTED="ACCEPTED"; REJECTED="REJECTED"; INCONCLUSIVE="INCONCLUSIVE"

class ProposedSystemChange(FrozenDIModel):
    target_ref: ExactObjectRef
    proposed_after_ref: ExactObjectRef
    operation_type: str
    supporting_hypothesis_refs: tuple[ObjectRef, ...]
    preserve_refs: tuple[ExactObjectRef | ObjectRef, ...] = ()
    rationale_ref: ObjectRef | None = None

class SystemChangeCandidate(ImmutableFact):
    optimization_lineage_ref: ObjectRef
    base_system_snapshot_ref: ObjectRef
    action_decision_ref: ObjectRef
    diagnostic_belief_refs: tuple[ObjectRef, ...]
    hypothesis_refs: tuple[ObjectRef, ...]
    target_loci: tuple[str, ...]
    proposed_changes: tuple[ProposedSystemChange, ...]
    intervention_risk_ref: ObjectRef
    validation_plan_ref: ObjectRef

    @model_validator(mode="after")
    def require_rationale(self):
        if not self.diagnostic_belief_refs or not self.hypothesis_refs or not self.proposed_changes:
            raise ValueError("candidate requires diagnosis, hypothesis, and proposed changes")
        return self

class InterventionRisk(ImmutableFact):
    candidate_ref: ObjectRef
    affected_artifact_refs: tuple[ExactObjectRef, ...]
    affected_loci: tuple[str, ...]
    permission_status: EffectivePermissionStatus
    protected_scope_refs: tuple[ExactObjectRef | ObjectRef, ...] = ()
    required_guard_refs: tuple[ObjectRef, ...] = ()
    requires_human_gate: bool = False

class OptimizationLineageRoot(ImmutableRoot):
    root_subject_ref: ExactObjectRef | ObjectRef
    root_diagnostic_belief_ref: ObjectRef
    root_hypothesis_refs: tuple[ObjectRef, ...] = ()
    base_system_snapshot_ref: ObjectRef

class InterventionTransaction(OperationalControlState):
    optimization_lineage_ref: ObjectRef
    candidate_ref: ObjectRef
    action_decision_ref: ObjectRef
    intervention_plan_ref: ObjectRef
    validation_plan_ref: ObjectRef
    phase: InterventionTransactionPhase
    sandbox_snapshot_ref: ObjectRef | None = None
    intervention_result_ref: ObjectRef | None = None
    validation_result_ref: ObjectRef | None = None
