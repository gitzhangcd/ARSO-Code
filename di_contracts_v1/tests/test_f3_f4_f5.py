import pytest
from pydantic import ValidationError

from di_contracts.b03 import CompilationStatus, MappingDisposition
from di_contracts.b05 import ProbeRecommendation
from di_contracts.b06 import SystemChangeCandidate
from di_contracts.b08 import (
    KnowledgeGateStatus, KnowledgeMaturity, KnowledgePromotionDecision,
    KnowledgePromotionDecisionType, KnowledgeScope, KnowledgeScopeType,
    MemoryMaturity, PreferenceSignalType,
)
from conftest import NOW, actor, exact, oid, ref, tenant


def immutable_base(type_name: str, seed: str):
    return dict(schema_version="1.0", id=oid(seed), object_type=type_name, created_at=NOW, created_by=actor(), tenant_scope=tenant(), provenance={})


def test_mapping_disposition_contains_traceable_drop_states():
    assert MappingDisposition.DROPPED_UNSUPPORTED.value == "DROPPED_UNSUPPORTED"
    assert MappingDisposition.APPROXIMATED.value == "APPROXIMATED"


def test_compilation_status_has_no_ambiguous_partial_success():
    assert {x.value for x in CompilationStatus} == {"COMPILED", "COMPILED_WITH_APPROXIMATION", "FAILED"}


def test_probe_recommendation_has_no_execution_authority_fields():
    fields = set(ProbeRecommendation.model_fields)
    forbidden = {"authorization", "executor_binding_ref", "variables_changed", "variables_held_fixed", "budget_request"}
    assert fields.isdisjoint(forbidden)


def test_system_change_candidate_requires_diagnosis_and_hypothesis():
    data = immutable_base("di.b06.system_change_candidate", "c")
    data.update(
        optimization_lineage_ref=ref("di.b06.optimization_lineage_root", "o"),
        base_system_snapshot_ref=ref("arso.core.system_snapshot", "s"),
        action_decision_ref=ref("arso.core.action_decision", "a"),
        diagnostic_belief_refs=(), hypothesis_refs=(), target_loci=("R6",), proposed_changes=(),
        intervention_risk_ref=ref("di.b06.intervention_risk", "r"), validation_plan_ref=ref("arso.core.validation_plan", "v"),
    )
    with pytest.raises(ValidationError): SystemChangeCandidate(**data)


def test_memory_and_knowledge_maturity_are_distinct_enums():
    assert MemoryMaturity is not KnowledgeMaturity
    assert "REUSABLE" in {x.value for x in MemoryMaturity}
    assert "STABLE" in {x.value for x in KnowledgeMaturity}


def test_global_knowledge_scope_has_no_ref():
    x = KnowledgeScope(scope_type=KnowledgeScopeType.GLOBAL)
    assert x.scope_ref is None
    with pytest.raises(ValidationError):
        KnowledgeScope(scope_type=KnowledgeScopeType.GLOBAL, scope_ref=ref("di.test.scope", "s"))


def test_non_global_knowledge_scope_requires_ref():
    with pytest.raises(ValidationError): KnowledgeScope(scope_type=KnowledgeScopeType.BRAND)


def test_preference_signal_type_excludes_view():
    assert "VIEW" not in {x.value for x in PreferenceSignalType}


def test_stable_promotion_requires_all_gates_pass():
    data = immutable_base("di.b08.knowledge_promotion_decision", "k")
    data.update(
        knowledge_lineage_ref=ref("di.b08.knowledge_lineage_root", "l"),
        proposal_ref=ref("di.b08.learning_proposal", "p"), knowledge_claim_ref=ref("di.b08.knowledge_claim", "c"),
        evidence_pack_ref=ref("di.b08.promotion_evidence_pack", "e"),
        kg0=KnowledgeGateStatus.PASS, kg1=KnowledgeGateStatus.PASS, kg2=KnowledgeGateStatus.FAIL,
        kg3=KnowledgeGateStatus.PASS, kg4=KnowledgeGateStatus.PASS,
        final_decision=KnowledgePromotionDecisionType.PROMOTE, approved_maturity=KnowledgeMaturity.STABLE,
    )
    with pytest.raises(ValidationError): KnowledgePromotionDecision(**data)
