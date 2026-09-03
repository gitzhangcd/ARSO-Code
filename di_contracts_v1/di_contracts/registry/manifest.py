from __future__ import annotations

from di_contracts.core.types import CanonicalObjectClass as C, PrimitiveOwner as O, ReferenceKind as R, SchemaVersion, StateDomain as D, ObjectType
from .models import ObjectRegistryEntry

V1 = SchemaVersion("1.0")


def e(name: str, owner: O, cls: C, domain: D, py: str, *, artifact=False, sys_snap=False, know_snap=False, review_snap=False, intervene=False, logical=False):
    versioned = cls == C.CANONICAL_REVISION
    if versioned:
        ref = R.EXACT_OBJECT_REF
    elif cls in {C.IMMUTABLE_FACT, C.IMMUTABLE_ROOT, C.IMMUTABLE_GRAPH_NODE, C.SNAPSHOT}:
        ref = R.OBJECT_REF
    else:
        ref = R.NONE
    return ObjectRegistryEntry(
        object_type=ObjectType(name), primitive_owner=owner, object_class=cls, state_domain=domain,
        schema_version=V1, python_type=py, versioned=versioned, persistent_ref_kind=ref,
        logical_authoring_ref_allowed=logical, artifact_eligible=artifact,
        system_snapshot_eligible=sys_snap, knowledge_snapshot_eligible=know_snap,
        review_snapshot_eligible=review_snap, system_intervention_target_eligible=intervene,
        historical_ssot=cls not in {C.OPERATIONAL_CONTROL_STATE, C.DERIVED_VIEW},
    )


# Sentinel + F2–F5 canonical types implemented in this candidate package.
REGISTRY_ENTRIES = (
    e("di.b01.design_spec", O.DI_B01, C.CANONICAL_REVISION, D.TASK, "external.B01.DesignSpec", review_snap=True, logical=True),
    e("di.b03.generation_compiler", O.DI_B03, C.CANONICAL_REVISION, D.SYSTEM, "di_contracts.b03.GenerationCompiler", artifact=True, sys_snap=True, intervene=True),
    e("di.b03.compiler_mapping_trace", O.DI_B03, C.IMMUTABLE_FACT, D.RUNTIME, "di_contracts.b03.CompilerMappingTrace"),
    e("di.b03.generation_package", O.DI_B03, C.IMMUTABLE_FACT, D.RUNTIME, "di_contracts.b03.GenerationPackage"),
    e("di.b03.design_instance", O.DI_B03, C.IMMUTABLE_FACT, D.TASK, "di_contracts.b03.DesignInstance", review_snap=True),
    e("di.b04.objective_definition", O.DI_B04, C.CANONICAL_REVISION, D.SYSTEM, "di_contracts.b04.ObjectiveDefinition", artifact=True, sys_snap=True, intervene=True),
    e("di.b04.evaluation_contract", O.DI_B04, C.CANONICAL_REVISION, D.SYSTEM, "di_contracts.b04.EvaluationContract", artifact=True, sys_snap=True, intervene=True),
    e("di.b04.evaluator_calibration_profile", O.DI_B04, C.CANONICAL_REVISION, D.SYSTEM, "di_contracts.b04.EvaluatorCalibrationProfile", artifact=True, sys_snap=True, intervene=True),
    e("di.b04.structured_finding", O.DI_B04, C.IMMUTABLE_FACT, D.RUNTIME, "di_contracts.b04.StructuredFinding"),
    e("di.b05.diagnostic_policy", O.DI_B05, C.CANONICAL_REVISION, D.SYSTEM, "di_contracts.b05.DiagnosticPolicy", artifact=True, sys_snap=True, intervene=True),
    e("di.b05.evidence_construction_policy", O.DI_B05, C.CANONICAL_REVISION, D.SYSTEM, "di_contracts.b05.EvidenceConstructionPolicy", artifact=True, sys_snap=True, intervene=True),
    e("di.b05.diagnostic_calibration_profile", O.DI_B05, C.CANONICAL_REVISION, D.SYSTEM, "di_contracts.b05.DiagnosticCalibrationProfile", artifact=True, sys_snap=True, intervene=True),
    e("di.b05.fashion_failure_extension", O.DI_B05, C.CANONICAL_REVISION, D.SYSTEM, "di_contracts.b05.FashionFailureExtension", artifact=True, sys_snap=True, intervene=True),
    e("di.b05.probe_recommendation", O.DI_B05, C.IMMUTABLE_FACT, D.RUNTIME, "di_contracts.b05.ProbeRecommendation"),
    e("di.b06.system_change_candidate", O.DI_B06, C.IMMUTABLE_FACT, D.SYSTEM, "di_contracts.b06.SystemChangeCandidate"),
    e("di.b06.intervention_risk", O.DI_B06, C.IMMUTABLE_FACT, D.RUNTIME, "di_contracts.b06.InterventionRisk"),
    e("di.b06.intervention_transaction", O.DI_B06, C.OPERATIONAL_CONTROL_STATE, D.SYSTEM, "di_contracts.b06.InterventionTransaction"),
    e("di.b06.optimization_lineage_root", O.DI_B06, C.IMMUTABLE_ROOT, D.SYSTEM, "di_contracts.b06.OptimizationLineageRoot"),
    e("di.b07.design_lineage_root", O.DI_B07, C.IMMUTABLE_ROOT, D.TASK, "di_contracts.b07.DesignLineageRoot"),
    e("di.b07.design_branch_root", O.DI_B07, C.IMMUTABLE_ROOT, D.TASK, "di_contracts.b07.DesignBranchRoot"),
    e("di.b07.branch_head_pointer", O.DI_B07, C.OPERATIONAL_CONTROL_STATE, D.TASK, "di_contracts.b07.BranchHeadPointer"),
    e("di.b07.design_state_revision", O.DI_B07, C.IMMUTABLE_GRAPH_NODE, D.TASK, "di_contracts.b07.DesignStateRevision", review_snap=True),
    e("di.b07.review_session_root", O.DI_B07, C.IMMUTABLE_ROOT, D.REVIEW, "di_contracts.b07.ReviewSessionRoot"),
    e("di.b07.review_round_opened", O.DI_B07, C.IMMUTABLE_FACT, D.REVIEW, "di_contracts.b07.ReviewRoundOpened"),
    e("di.b07.review_round_outcome", O.DI_B07, C.IMMUTABLE_FACT, D.REVIEW, "di_contracts.b07.ReviewRoundOutcome"),
    e("di.b07.design_review_snapshot", O.DI_B07, C.SNAPSHOT, D.REVIEW, "di_contracts.b07.DesignReviewSnapshot"),
    e("di.b07.review_presentation_manifest", O.DI_B07, C.IMMUTABLE_FACT, D.REVIEW, "di_contracts.b07.ReviewPresentationManifest"),
    e("di.b07.human_decision", O.DI_B07, C.IMMUTABLE_FACT, D.REVIEW, "di_contracts.b07.HumanDecision"),
    e("di.b07.design_edit_request", O.DI_B07, C.IMMUTABLE_FACT, D.REVIEW, "di_contracts.b07.DesignEditRequest"),
    e("di.b07.approval_record", O.DI_B07, C.IMMUTABLE_FACT, D.REVIEW, "di_contracts.b07.ApprovalRecord"),
    e("di.b08.memory_item", O.DI_B08, C.CANONICAL_REVISION, D.KNOWLEDGE, "di_contracts.b08.MemoryItem"),
    e("di.b08.memory_curation_decision", O.DI_B08, C.IMMUTABLE_FACT, D.KNOWLEDGE, "di_contracts.b08.MemoryCurationDecision"),
    e("di.b08.preference_signal", O.DI_B08, C.IMMUTABLE_FACT, D.KNOWLEDGE, "di_contracts.b08.PreferenceSignal"),
    e("di.b08.brand_dna_profile", O.DI_B08, C.CANONICAL_REVISION, D.KNOWLEDGE, "di_contracts.b08.BrandDNAProfile", artifact=True, know_snap=True),
    e("di.b08.enterprise_knowledge_item", O.DI_B08, C.CANONICAL_REVISION, D.KNOWLEDGE, "di_contracts.b08.EnterpriseKnowledgeItem", artifact=True, know_snap=True),
    e("di.b08.learning_proposal", O.DI_B08, C.IMMUTABLE_FACT, D.KNOWLEDGE, "di_contracts.b08.LearningProposal"),
    e("di.b08.knowledge_claim", O.DI_B08, C.IMMUTABLE_FACT, D.KNOWLEDGE, "di_contracts.b08.KnowledgeClaim"),
    e("di.b08.promotion_evidence_pack", O.DI_B08, C.SNAPSHOT, D.KNOWLEDGE, "di_contracts.b08.PromotionEvidencePack"),
    e("di.b08.knowledge_promotion_decision", O.DI_B08, C.IMMUTABLE_FACT, D.KNOWLEDGE, "di_contracts.b08.KnowledgePromotionDecision"),
    e("di.b08.knowledge_validity", O.DI_B08, C.CANONICAL_REVISION, D.KNOWLEDGE, "di_contracts.b08.KnowledgeValidity", know_snap=True),
    e("di.b08.retention_policy", O.DI_B08, C.CANONICAL_REVISION, D.KNOWLEDGE, "di_contracts.b08.RetentionPolicy", artifact=True, know_snap=True),
    e("di.b08.knowledge_access_policy", O.DI_B08, C.CANONICAL_REVISION, D.KNOWLEDGE, "di_contracts.b08.KnowledgeAccessPolicy", artifact=True, know_snap=True),
    e("di.b08.knowledge_snapshot", O.DI_B08, C.SNAPSHOT, D.KNOWLEDGE, "di_contracts.b08.KnowledgeSnapshot"),
    e("di.b08.knowledge_lineage_root", O.DI_B08, C.IMMUTABLE_ROOT, D.KNOWLEDGE, "di_contracts.b08.KnowledgeLineageRoot"),
)
