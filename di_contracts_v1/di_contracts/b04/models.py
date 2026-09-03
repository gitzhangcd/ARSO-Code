from __future__ import annotations
from enum import StrEnum
from di_contracts.core.models import CanonicalRevision, ExactObjectRef, ImmutableFact, ObjectRef
from di_contracts.core.types import ObjectType

class FashionEvaluationFamily(StrEnum):
    BUSINESS_INTENT="BUSINESS_INTENT"; DESIGN_SEMANTIC_QUALITY="DESIGN_SEMANTIC_QUALITY"; EXECUTION_FIDELITY="EXECUTION_FIDELITY"; FASHION_PLAUSIBILITY="FASHION_PLAUSIBILITY"; CONTEXTUAL_PREFERENCE="CONTEXTUAL_PREFERENCE"
class ObjectiveDirection(StrEnum):
    MAXIMIZE="MAXIMIZE"; MINIMIZE="MINIMIZE"; TARGET="TARGET"
class ObjectiveDefinition(CanonicalRevision):
    objective_key: str
    display_name: str
    semantic_definition: str
    evaluation_family: FashionEvaluationFamily
    default_direction: ObjectiveDirection
    allowed_subject_types: tuple[ObjectType, ...]
    expected_target_types: tuple[ObjectType, ...] = ()
class EvaluationContract(CanonicalRevision):
    objective_definition_refs: tuple[ExactObjectRef, ...]
    objective_spec_refs: tuple[ExactObjectRef, ...]
    measurement_spec_refs: tuple[ExactObjectRef, ...]
    evaluator_binding_policy_refs: tuple[ExactObjectRef, ...] = ()
class EvaluatorCalibrationProfile(CanonicalRevision):
    evaluator_binding_ref: ExactObjectRef
    objective_ref: ExactObjectRef
    validity_scope_ref: ObjectRef
    calibration_result_refs: tuple[ObjectRef, ...] = ()
class StructuredFinding(ImmutableFact):
    evaluation_record_ref: ObjectRef
    objective_definition_ref: ExactObjectRef
    finding_type: str
    semantic_path: str | None = None
    region_ref: ObjectRef | None = None
    status: str | None = None
    expected_summary: str | None = None
    observed_summary: str | None = None
    confidence: float | None = None
