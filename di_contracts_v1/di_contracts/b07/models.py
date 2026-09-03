from __future__ import annotations

from enum import StrEnum

from pydantic import model_validator

from di_contracts.core.models import ExactObjectRef, ImmutableFact, ImmutableGraphNode, ImmutableRoot, ObjectRef, OperationalControlState, SnapshotObject


class SemanticStage(StrEnum):
    BRIEF = "BRIEF"
    CONTEXT_BOUND = "CONTEXT_BOUND"
    DECIDED = "DECIDED"
    ROUTES_AVAILABLE = "ROUTES_AVAILABLE"
    ROUTE_SELECTED = "ROUTE_SELECTED"
    SPECIFIED = "SPECIFIED"


class ReviewStageProjection(StrEnum):
    NOT_IN_REVIEW = "NOT_IN_REVIEW"
    IN_REVIEW = "IN_REVIEW"
    CHANGES_REQUESTED = "CHANGES_REQUESTED"
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"
    FINAL_APPROVED = "FINAL_APPROVED"


class ExecutionStageProjection(StrEnum):
    NOT_EXECUTED = "NOT_EXECUTED"
    HAS_INSTANCE = "HAS_INSTANCE"


class BranchHeadStatus(StrEnum):
    ACTIVE = "ACTIVE"
    READ_ONLY = "READ_ONLY"
    ARCHIVED = "ARCHIVED"


class HumanDecisionType(StrEnum):
    VIEW = "VIEW"
    SHORTLIST = "SHORTLIST"
    PREFER = "PREFER"
    REJECT = "REJECT"
    REQUEST_EDIT = "REQUEST_EDIT"
    APPROVE = "APPROVE"
    FINAL_APPROVE = "FINAL_APPROVE"


class ReviewRoundOutcomeType(StrEnum):
    CHANGES_REQUESTED = "CHANGES_REQUESTED"
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"
    FINAL_APPROVED = "FINAL_APPROVED"
    SUPERSEDED = "SUPERSEDED"
    CANCELLED = "CANCELLED"


class DesignLineageRoot(ImmutableRoot):
    root_brief_ref: ExactObjectRef
    root_state_ref: ObjectRef
    project_ref: ObjectRef | None = None
    collection_ref: ObjectRef | None = None
    style_ref: ObjectRef | None = None


class DesignBranchRoot(ImmutableRoot):
    lineage_ref: ObjectRef
    base_state_ref: ObjectRef
    parent_branch_ref: ObjectRef | None = None


class BranchHeadPointer(OperationalControlState):
    branch_ref: ObjectRef
    head_state_ref: ObjectRef
    status: BranchHeadStatus


class DesignStateRevision(ImmutableGraphNode):
    lineage_ref: ObjectRef
    branch_ref: ObjectRef
    parent_state_refs: tuple[ObjectRef, ...] = ()
    brief_ref: ExactObjectRef
    context_binding_ref: ExactObjectRef | None = None
    decision_ref: ExactObjectRef | None = None
    candidate_route_refs: tuple[ExactObjectRef, ...] = ()
    selected_route_ref: ExactObjectRef | None = None
    spec_ref: ExactObjectRef | None = None
    selected_instance_refs: tuple[ObjectRef, ...] = ()
    semantic_stage: SemanticStage
    execution_stage: ExecutionStageProjection = ExecutionStageProjection.NOT_EXECUTED
    review_stage_projection: ReviewStageProjection = ReviewStageProjection.NOT_IN_REVIEW
    transition_reason: str

    @model_validator(mode="after")
    def validate_prefix(self):
        s = self.semantic_stage
        if s == SemanticStage.BRIEF:
            if any([self.context_binding_ref, self.decision_ref, self.selected_route_ref, self.spec_ref]) or self.candidate_route_refs:
                raise ValueError("BRIEF state may only carry brief_ref")
        if s in {SemanticStage.CONTEXT_BOUND, SemanticStage.DECIDED, SemanticStage.ROUTES_AVAILABLE, SemanticStage.ROUTE_SELECTED, SemanticStage.SPECIFIED} and self.context_binding_ref is None:
            raise ValueError("context_binding_ref required")
        if s in {SemanticStage.DECIDED, SemanticStage.ROUTES_AVAILABLE, SemanticStage.ROUTE_SELECTED, SemanticStage.SPECIFIED} and self.decision_ref is None:
            raise ValueError("decision_ref required")
        if s in {SemanticStage.ROUTES_AVAILABLE, SemanticStage.ROUTE_SELECTED, SemanticStage.SPECIFIED} and not self.candidate_route_refs:
            raise ValueError("candidate_route_refs required")
        if s in {SemanticStage.ROUTE_SELECTED, SemanticStage.SPECIFIED}:
            if self.selected_route_ref is None or self.selected_route_ref not in self.candidate_route_refs:
                raise ValueError("selected_route_ref must be one of candidate_route_refs")
        if s == SemanticStage.SPECIFIED and self.spec_ref is None:
            raise ValueError("spec_ref required")
        return self


class ReviewSessionRoot(ImmutableRoot):
    lineage_ref: ObjectRef
    branch_ref: ObjectRef
    purpose: str
    approval_policy_ref: ExactObjectRef | ObjectRef


class ReviewRoundOpened(ImmutableFact):
    session_ref: ObjectRef
    round_index: int
    input_state_ref: ObjectRef
    review_snapshot_ref: ObjectRef


class ReviewRoundOutcome(ImmutableFact):
    round_ref: ObjectRef
    outcome: ReviewRoundOutcomeType
    decided_at: object
    resulting_state_ref: ObjectRef | None = None


class ReviewPresentationManifest(ImmutableFact):
    candidate_order: tuple[ObjectRef, ...]
    candidate_labels: tuple[str, ...] = ()
    grouping: tuple[str, ...] = ()
    score_visibility: bool = False
    diagnosis_visibility: bool = False
    reference_visibility: bool = True
    ai_recommendation_visibility: bool = False
    blinded: bool = False
    randomized: bool = False
    ui_version_ref: ObjectRef


class DesignReviewSnapshot(SnapshotObject):
    design_state_ref: ObjectRef
    visible_instance_refs: tuple[ObjectRef, ...] = ()
    visible_evaluation_refs: tuple[ObjectRef, ...] = ()
    visible_evaluation_presentation_refs: tuple[ObjectRef, ...] = ()
    visible_diagnostic_presentation_refs: tuple[ObjectRef, ...] = ()
    visible_reference_refs: tuple[ObjectRef, ...] = ()
    presentation_manifest_ref: ObjectRef
    review_runtime_snapshot_ref: ObjectRef


class HumanDecision(ImmutableFact):
    lineage_ref: ObjectRef
    review_session_ref: ObjectRef
    review_round_ref: ObjectRef
    review_snapshot_ref: ObjectRef
    decision_type: HumanDecisionType
    subject_refs: tuple[ExactObjectRef | ObjectRef, ...]
    rationale: str | None = None


class DesignEditRequest(ImmutableFact):
    review_round_ref: ObjectRef
    source_state_ref: ObjectRef
    target_semantic_paths: tuple[str, ...] = ()
    target_visual_regions: tuple[ObjectRef, ...] = ()
    requested_changes: tuple[str, ...] = ()
    preserve_paths: tuple[str, ...] = ()
    forbidden_paths: tuple[str, ...] = ()
    rationale: str | None = None


class ApprovalType(StrEnum):
    APPROVED = "APPROVED"
    FINAL_APPROVED = "FINAL_APPROVED"


class ApprovalRecord(ImmutableFact):
    lineage_ref: ObjectRef
    review_session_ref: ObjectRef
    review_round_ref: ObjectRef
    review_snapshot_ref: ObjectRef
    approved_state_ref: ObjectRef
    approval_policy_ref: ExactObjectRef | ObjectRef
    approval_type: ApprovalType
    human_decision_ref: ObjectRef
