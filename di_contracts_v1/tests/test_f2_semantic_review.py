import pytest
from pydantic import ValidationError

from di_contracts.b07 import (
    BranchHeadPointer, BranchHeadStatus, DesignStateRevision, HumanDecision,
    HumanDecisionType, ReviewStageProjection, SemanticStage,
)
from conftest import NOW, actor, exact, oid, ref, tenant


def state_base():
    return dict(
        schema_version="1.0", id=oid("s"), object_type="di.b07.design_state_revision",
        created_at=NOW, created_by=actor(), tenant_scope=tenant(), provenance={},
        lineage_ref=ref("di.b07.design_lineage_root", "l"), branch_ref=ref("di.b07.design_branch_root", "b"),
        brief_ref=exact("di.b01.style_brief", "q"), semantic_stage=SemanticStage.BRIEF,
        transition_reason="init",
    )


def test_brief_prefix_valid():
    assert DesignStateRevision(**state_base()).semantic_stage == SemanticStage.BRIEF


def test_brief_prefix_rejects_downstream_refs():
    data = state_base(); data["decision_ref"] = exact("di.b01.design_decision", "d")
    with pytest.raises(ValidationError): DesignStateRevision(**data)


def test_specified_requires_context_decision_routes_selected_and_spec():
    data = state_base(); data.update(semantic_stage=SemanticStage.SPECIFIED)
    with pytest.raises(ValidationError): DesignStateRevision(**data)


def test_selected_route_must_be_candidate():
    data = state_base(); r1=exact("di.b01.design_route", "1"); r2=exact("di.b01.design_route", "2")
    data.update(
        semantic_stage=SemanticStage.ROUTE_SELECTED,
        context_binding_ref=exact("di.b01.design_context_binding", "c"),
        decision_ref=exact("di.b01.design_decision", "d"),
        candidate_route_refs=(r1,), selected_route_ref=r2,
    )
    with pytest.raises(ValidationError): DesignStateRevision(**data)


def test_branch_pointer_is_operational_and_frozen_value():
    p = BranchHeadPointer(
        schema_version="1.0", id=oid("p"), object_type="di.b07.branch_head_pointer",
        tenant_scope=tenant(), concurrency_version=1, updated_at=NOW, updated_by=actor(),
        branch_ref=ref("di.b07.design_branch_root", "b"), head_state_ref=ref("di.b07.design_state_revision", "s"), status=BranchHeadStatus.ACTIVE,
    )
    with pytest.raises(ValidationError): p.concurrency_version = 2


def test_human_decision_requires_review_snapshot():
    # Pydantic required field itself enforces review-visible context.
    with pytest.raises(ValidationError):
        HumanDecision(
            schema_version="1.0", id=oid("h"), object_type="di.b07.human_decision",
            created_at=NOW, created_by=actor(), tenant_scope=tenant(), provenance={},
            lineage_ref=ref("di.b07.design_lineage_root", "l"), review_session_ref=ref("di.b07.review_session_root", "e"),
            review_round_ref=ref("di.b07.review_round_opened", "r"), decision_type=HumanDecisionType.APPROVE,
            subject_refs=(ref("di.b03.design_instance", "i"),),
        )
