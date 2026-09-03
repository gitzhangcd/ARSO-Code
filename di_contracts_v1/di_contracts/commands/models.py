from __future__ import annotations
from typing import Literal
from di_contracts.core.models import ExactObjectRef, ObjectRef
from .base import DICommand, BranchMutationCommand

class ForkDesignBranchCommand(DICommand):
    source_branch_ref: ObjectRef
    expected_source_head_state_ref: ObjectRef
    expected_source_concurrency_version: int
    fork_from_state_ref: ObjectRef

class RequestDesignEditCommand(BranchMutationCommand):
    edit_request_ref: ObjectRef

class ApproveDesignCommand(DICommand):
    review_session_ref: ObjectRef
    review_round_ref: ObjectRef
    review_snapshot_ref: ObjectRef
    approved_state_ref: ObjectRef
    human_decision_ref: ObjectRef
    approval_policy_ref: ExactObjectRef | ObjectRef

class RequestFashionSemanticCommitCommand(DICommand):
    promotion_decision_ref: ObjectRef
    target_owner: Literal["DI_B02"] = "DI_B02"
    target_object_ref: ExactObjectRef | None = None
    proposed_content_ref: ObjectRef
    expected_parent_refs: tuple[ExactObjectRef, ...] = ()
