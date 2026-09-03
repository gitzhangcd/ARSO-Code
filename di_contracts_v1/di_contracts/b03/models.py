from __future__ import annotations
from enum import StrEnum
from pydantic import Field
from di_contracts.core.base import FrozenDIModel
from di_contracts.core.models import CanonicalRevision, ExactObjectRef, ImmutableFact, ObjectRef

class MappingDisposition(StrEnum):
    TEXT_EXPLICIT="TEXT_EXPLICIT"; REFERENCE_BOUND="REFERENCE_BOUND"; REGION_BOUND="REGION_BOUND"; PARAMETER_BOUND="PARAMETER_BOUND"; CONSTRAINT_BOUND="CONSTRAINT_BOUND"; IMPLICITLY_SATISFIED="IMPLICITLY_SATISFIED"; APPROXIMATED="APPROXIMATED"; NOT_APPLICABLE="NOT_APPLICABLE"; DROPPED_UNSUPPORTED="DROPPED_UNSUPPORTED"; DROPPED_BY_POLICY="DROPPED_BY_POLICY"
class CompilationStatus(StrEnum):
    COMPILED="COMPILED"; COMPILED_WITH_APPROXIMATION="COMPILED_WITH_APPROXIMATION"; FAILED="FAILED"
class GenerationOperation(StrEnum):
    TEXT_TO_IMAGE="TEXT_TO_IMAGE"; REFERENCE_GUIDED_GENERATION="REFERENCE_GUIDED_GENERATION"; IMAGE_EDIT="IMAGE_EDIT"
class ExecutionPurpose(StrEnum):
    INITIAL_INSTANTIATION="INITIAL_INSTANTIATION"; RECONSTRUCTION="RECONSTRUCTION"; VARIATION="VARIATION"; CONTROLLED_EDIT="CONTROLLED_EDIT"; PROBE="PROBE"

class GenerationCompiler(CanonicalRevision):
    compiler_family: str
    template_ref: ExactObjectRef | None = None
    reference_binding_policy_ref: ExactObjectRef | None = None
    constraint_lowering_policy_ref: ExactObjectRef | None = None

class CompiledReferenceBinding(FrozenDIModel):
    reference_asset_ref: ObjectRef
    reference_intent_ref: ExactObjectRef
    usage_mode: str
    strength: float | None = None
    region_binding_ref: ObjectRef | None = None

class CompilerMappingEntry(FrozenDIModel):
    semantic_path: str
    source_semantic_ref: ExactObjectRef
    disposition: MappingDisposition
    approximation_note: str | None = None
    drop_reason: str | None = None

class CompilerMappingTrace(ImmutableFact):
    design_spec_ref: ExactObjectRef
    compiler_ref: ExactObjectRef
    executor_binding_ref: ObjectRef
    entries: tuple[CompilerMappingEntry, ...]

class GenerationConstraintBundle(FrozenDIModel):
    preserve_refs: tuple[ObjectRef, ...] = ()
    change_refs: tuple[ObjectRef, ...] = ()
    allow_change_refs: tuple[ObjectRef, ...] = ()
    forbid_change_refs: tuple[ObjectRef, ...] = ()
    positive_requirement_refs: tuple[ObjectRef, ...] = ()
    negative_requirement_refs: tuple[ObjectRef, ...] = ()
    preference_refs: tuple[ObjectRef, ...] = ()

class GenerationPackage(ImmutableFact):
    design_spec_ref: ExactObjectRef
    compiler_ref: ExactObjectRef
    executor_binding_ref: ObjectRef
    operation: GenerationOperation
    execution_purpose: ExecutionPurpose
    textual_payload: str | None = None
    reference_bindings: tuple[CompiledReferenceBinding, ...] = ()
    constraints: GenerationConstraintBundle = Field(default_factory=GenerationConstraintBundle)
    mapping_trace_ref: ObjectRef

class DesignInstance(ImmutableFact):
    design_spec_ref: ExactObjectRef
    generation_package_ref: ObjectRef
    run_ref: ObjectRef
    executor_binding_ref: ObjectRef
    asset_refs: tuple[ObjectRef, ...]
    operation: GenerationOperation
    source_instance_refs: tuple[ObjectRef, ...] = ()
    parent_instance_refs: tuple[ObjectRef, ...] = ()
