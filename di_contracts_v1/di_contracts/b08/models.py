from __future__ import annotations
from datetime import datetime
from enum import StrEnum
from pydantic import model_validator
from di_contracts.core.base import FrozenDIModel
from di_contracts.core.models import ActorRef, CanonicalRevision, ExactObjectRef, ImmutableFact, ImmutableRoot, ObjectRef, SnapshotObject

class MemoryType(StrEnum):
    CASE="CASE"; PREFERENCE="PREFERENCE"; DESIGN_PATTERN="DESIGN_PATTERN"; FAILURE_PATTERN="FAILURE_PATTERN"; INTERVENTION="INTERVENTION"; EVALUATION="EVALUATION"; KNOWLEDGE_CANDIDATE="KNOWLEDGE_CANDIDATE"; META_EXPERIENCE="META_EXPERIENCE"
class MemoryMaturity(StrEnum):
    RAW="RAW"; CURATED="CURATED"; REUSABLE="REUSABLE"; STALE="STALE"; QUARANTINED="QUARANTINED"
class KnowledgeMaturity(StrEnum):
    RAW="RAW"; CANDIDATE="CANDIDATE"; PROVISIONAL="PROVISIONAL"; VALIDATED="VALIDATED"; STABLE="STABLE"
class KnowledgeScopeType(StrEnum):
    INSTANCE="INSTANCE"; STYLE="STYLE"; COLLECTION="COLLECTION"; PROJECT="PROJECT"; USER="USER"; TEAM="TEAM"; BRAND="BRAND"; TENANT="TENANT"; CATEGORY="CATEGORY"; FASHION_DOMAIN="FASHION_DOMAIN"; GLOBAL="GLOBAL"
class RetentionClass(StrEnum):
    SESSION="SESSION"; TEMPORARY="TEMPORARY"; PROJECT_LIFETIME="PROJECT_LIFETIME"; TENANT_LONG_TERM="TENANT_LONG_TERM"; DOMAIN_LONG_TERM="DOMAIN_LONG_TERM"; PERMANENT_AUDIT="PERMANENT_AUDIT"
class KnowledgeUseMode(StrEnum):
    OBSERVE_ONLY="OBSERVE_ONLY"; RETRIEVAL_ONLY="RETRIEVAL_ONLY"; RECOMMEND="RECOMMEND"; SOFT_CONSTRAINT="SOFT_CONSTRAINT"; HARD_CONSTRAINT="HARD_CONSTRAINT"
class KnowledgeGateStatus(StrEnum):
    PASS="PASS"; FAIL="FAIL"; INCONCLUSIVE="INCONCLUSIVE"; NOT_RUN="NOT_RUN"
class KnowledgePromotionDecisionType(StrEnum):
    PROMOTE="PROMOTE"; PROMOTE_WITH_LIMITED_SCOPE="PROMOTE_WITH_LIMITED_SCOPE"; REMAIN_PROVISIONAL="REMAIN_PROVISIONAL"; REJECT="REJECT"; QUARANTINE="QUARANTINE"
class KnowledgeValidityStatus(StrEnum):
    ELIGIBLE="ELIGIBLE"; STALE="STALE"; QUARANTINED="QUARANTINED"; DEPRECATED="DEPRECATED"; INVALIDATED="INVALIDATED"
class PreferenceSignalType(StrEnum):
    SHORTLIST="SHORTLIST"; PREFER="PREFER"; APPROVE="APPROVE"; REJECT="REJECT"; EDIT="EDIT"; REPEAT_SELECTION="REPEAT_SELECTION"

class KnowledgeScope(FrozenDIModel):
    scope_type: KnowledgeScopeType
    scope_ref: ExactObjectRef | ObjectRef | None = None
    @model_validator(mode="after")
    def validate_scope(self):
        if self.scope_type == KnowledgeScopeType.GLOBAL and self.scope_ref is not None:
            raise ValueError("GLOBAL knowledge scope must not carry scope_ref")
        if self.scope_type != KnowledgeScopeType.GLOBAL and self.scope_ref is None:
            raise ValueError("non-GLOBAL knowledge scope requires scope_ref")
        return self

class MemoryItem(CanonicalRevision):
    memory_type: MemoryType
    scope: KnowledgeScope
    maturity: MemoryMaturity
    content_ref: ExactObjectRef | ObjectRef
    source_object_refs: tuple[ExactObjectRef | ObjectRef, ...]
    evidence_refs: tuple[ObjectRef, ...] = ()
    retention_policy_ref: ExactObjectRef
    access_policy_ref: ExactObjectRef

class MemoryCurationDecision(ImmutableFact):
    source_refs: tuple[ExactObjectRef | ObjectRef, ...]
    candidate_memory_type: MemoryType
    candidate_scope: KnowledgeScope
    action: str
    resulting_memory_ref: ExactObjectRef | None = None
    policy_ref: ExactObjectRef

class PreferenceSignal(ImmutableFact):
    actor_ref: ActorRef
    source_human_decision_ref: ObjectRef
    review_snapshot_ref: ObjectRef
    presentation_manifest_ref: ObjectRef
    subject_ref: ExactObjectRef | ObjectRef
    semantic_scope: tuple[str, ...]
    signal_type: PreferenceSignalType
    strength: float | None = None
    confounder_refs: tuple[ObjectRef, ...] = ()

class BrandDNAProfile(CanonicalRevision):
    brand_ref: ObjectRef
    identity_semantic_refs: tuple[ExactObjectRef | ObjectRef, ...] = ()
    preferred_range_refs: tuple[ExactObjectRef | ObjectRef, ...] = ()
    discouraged_range_refs: tuple[ExactObjectRef | ObjectRef, ...] = ()
    supporting_evidence_refs: tuple[ObjectRef, ...] = ()

class EnterpriseKnowledgeItem(CanonicalRevision):
    knowledge_lineage_ref: ObjectRef
    knowledge_type: str
    statement: str
    scope: KnowledgeScope
    supporting_evidence_refs: tuple[ObjectRef, ...] = ()
    counterevidence_refs: tuple[ObjectRef, ...] = ()
    maturity: KnowledgeMaturity

class LearningProposal(ImmutableFact):
    knowledge_lineage_ref: ObjectRef
    proposal_type: str
    target_scope: KnowledgeScope
    proposed_change_ref: ObjectRef
    supporting_evidence_refs: tuple[ObjectRef, ...]
    counterevidence_refs: tuple[ObjectRef, ...]

class KnowledgeClaim(ImmutableFact):
    knowledge_lineage_ref: ObjectRef
    proposal_ref: ObjectRef
    statement: str
    scope: KnowledgeScope
    condition_refs: tuple[ExactObjectRef | ObjectRef, ...]
    predicted_effect_ref: ObjectRef
    falsifier_ref: ObjectRef
    supporting_evidence_refs: tuple[ObjectRef, ...] = ()
    counterevidence_refs: tuple[ObjectRef, ...] = ()

class PromotionEvidencePack(SnapshotObject):
    knowledge_lineage_ref: ObjectRef
    proposal_ref: ObjectRef
    knowledge_claim_ref: ObjectRef
    evidence_bundle_refs: tuple[ObjectRef, ...] = ()
    evaluation_record_refs: tuple[ObjectRef, ...] = ()
    validation_result_refs: tuple[ObjectRef, ...] = ()
    independent_group_count: int
    case_count: int
    tenant_count: int
    temporal_start: datetime | None = None
    temporal_end: datetime | None = None

class KnowledgePromotionDecision(ImmutableFact):
    knowledge_lineage_ref: ObjectRef
    proposal_ref: ObjectRef
    knowledge_claim_ref: ObjectRef
    evidence_pack_ref: ObjectRef
    kg0: KnowledgeGateStatus
    kg1: KnowledgeGateStatus
    kg2: KnowledgeGateStatus
    kg3: KnowledgeGateStatus
    kg4: KnowledgeGateStatus
    final_decision: KnowledgePromotionDecisionType
    approved_scope: KnowledgeScope | None = None
    approved_maturity: KnowledgeMaturity | None = None
    approved_use_mode: KnowledgeUseMode | None = None
    reviewer_refs: tuple[ActorRef, ...] = ()
    @model_validator(mode="after")
    def stable_requires_all_gates(self):
        if self.approved_maturity == KnowledgeMaturity.STABLE:
            gates = (self.kg0, self.kg1, self.kg2, self.kg3, self.kg4)
            if any(g != KnowledgeGateStatus.PASS for g in gates):
                raise ValueError("STABLE promotion requires KG0-KG4 PASS")
        return self

class KnowledgeValidity(CanonicalRevision):
    knowledge_ref: ExactObjectRef
    status: KnowledgeValidityStatus
    valid_scope: KnowledgeScope
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    revalidation_evidence_refs: tuple[ObjectRef, ...] = ()

class RetentionPolicy(CanonicalRevision):
    retention_class: RetentionClass
    archival_required: bool
    destructive_delete_allowed: bool
    audit_preservation_required: bool
    policy_scope: KnowledgeScope

class KnowledgeAccessPolicy(CanonicalRevision):
    knowledge_scope: KnowledgeScope
    exportable: bool = False
    cross_tenant_use: bool = False

class KnowledgeSnapshot(SnapshotObject):
    fashion_ontology_ref: ExactObjectRef
    design_grammar_ref: ExactObjectRef
    semantic_parameter_space_ref: ExactObjectRef
    brand_dna_ref: ExactObjectRef | None = None
    enterprise_knowledge_refs: tuple[ExactObjectRef, ...] = ()
    eligibility_policy_refs: tuple[ExactObjectRef, ...] = ()
    access_policy_refs: tuple[ExactObjectRef, ...] = ()
    knowledge_validity_refs: tuple[ExactObjectRef, ...] = ()

class KnowledgeLineageRoot(ImmutableRoot):
    knowledge_family: str
    root_source_refs: tuple[ExactObjectRef | ObjectRef, ...]
    target_scope: KnowledgeScope
