from __future__ import annotations
from di_contracts.core.models import CanonicalRevision, ExactObjectRef, ImmutableFact, ObjectRef
from di_contracts.core.types import ObjectType

class EvidenceConstructionPolicy(CanonicalRevision):
    allowed_source_types: tuple[str, ...]
    allowed_content_types: tuple[str, ...]
    allowed_relation_types: tuple[str, ...]
    allowed_acquisition_types: tuple[str, ...]
    required_observability_channels: tuple[str, ...] = ()
    independence_grouping_policy_ref: ExactObjectRef | None = None
    deduplication_policy_ref: ExactObjectRef | None = None

class DiagnosticPolicy(CanonicalRevision):
    evidence_construction_policy_ref: ExactObjectRef
    failure_extension_refs: tuple[ExactObjectRef, ...] = ()
    diagnosis_engine_ref: ExactObjectRef | ObjectRef
    calibration_profile_ref: ExactObjectRef | None = None
    require_open_set_support: bool = True
    require_identifiability_assessment: bool = True
    require_counterevidence_tracking: bool = True

class DiagnosticCalibrationProfile(CanonicalRevision):
    diagnostic_policy_ref: ExactObjectRef
    diagnosis_engine_ref: ExactObjectRef | ObjectRef
    calibration_result_refs: tuple[ObjectRef, ...] = ()
    known_limitation_refs: tuple[ObjectRef, ...] = ()

class FashionFailureExtension(CanonicalRevision):
    failure_key: str
    parent_locus: str
    semantic_definition: str
    applicable_object_types: tuple[ObjectType, ...]
    known_confounder_refs: tuple[ObjectRef, ...] = ()
    applicable_probe_types: tuple[str, ...] = ()

class ProbeRecommendation(ImmutableFact):
    diagnostic_belief_ref: ObjectRef
    identifiability_assessment_ref: ObjectRef
    target_hypothesis_refs: tuple[ObjectRef, ...] = ()
    recommended_probe_type: str
    evidence_gap: str
    expected_discrimination: str | None = None
    expected_information_value: float | None = None
    rationale_ref: ObjectRef | None = None
