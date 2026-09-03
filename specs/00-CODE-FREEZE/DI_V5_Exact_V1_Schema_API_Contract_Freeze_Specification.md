# Design Intelligence Exact V1 Schema & API Contract Freeze Specification

## ARSO V2.2.1 Reference Application Edition
### F0–F6 Cross-Phase Consistency Normalization + Code-Level Normative Contract

**Document ID:** `DI-V5-EXACT-CONTRACT`  
**Version:** `V1.0-FC1`  
**Date:** `2026-09-03`  
**Document Type:** Schema / API / Registry / Command / Event / Protocol / Conformance Specification  
**Status:** `FREEZE CANDIDATE`  
**Normative Target:** F6.1 Exact V1 Contract Implementation & Automated Conformance

---

# 0. Executive Freeze Decision

F0–F6 的总体方向不存在需要推翻的架构级冲突。其核心路线是一致的：

\[
Engineering\ Architecture
\rightarrow
Canonical\ Contract
\rightarrow
Exact\ Reference
\rightarrow
Immutable\ Runtime
\rightarrow
Typed\ Control
\rightarrow
Automated\ Conformance
\]

但在从“工程规范”压缩到“Exact V1 可编码合同”的过程中，出现了三类问题：

1. **已在 F6 被正常化的漂移**：对象所有权、Review closure、InterventionTransaction、Memory/Knowledge maturity、CompiledReferenceBinding 等；
2. **本轮仍需正式消歧的合同漂移**：Canonical hash、MemoryItem lifecycle、KnowledgeSnapshot validity duplication、Knowledge object 的 Artifact eligibility 语义；
3. **不是概念冲突、但会阻止 Exact V1 冻结的完整性缺口**：B01/B02 exact schemas、ARSO exact imports、Command/Event inventory、Protocol signatures、CS-01–CS-32 全量自动化等。

因此：

```text
Architecture / Ownership / Boundary        FROZEN
F0–F6 normalized semantic contract         FROZEN by this document
Exact schema implementation                FREEZE CANDIDATE
Automated acceptance surface               INCOMPLETE
Physical database schema                   OPEN
Algorithms / models / thresholds           OPEN
```

本文件从现在起作为 **Codex / Work 编码时的第一层 Code-Level Authority**。

---

# 1. Normative Authority Order

若规范之间出现冲突，采用以下优先级：

```text
1. 本文件：
   Design Intelligence Exact V1 Schema & API Contract Freeze Specification

2. Design Intelligence V5.0 Engineering Specification V1.0

3. DI-E01–E08 Engineering Cross-Spec Consistency Freeze

4. ARSO Engineering Specification V2.2.1

5. Design Intelligence V5.0 Application Specification

6. Design Intelligence × ARSO V2.2.1 Implementation Blueprint

7. ARSO Research Specification V2.2.1
```

规则：

```text
A lower-priority source MUST NOT override
an explicitly frozen higher-priority contract.

If a genuine contradiction remains:
STOP implementation,
emit SPEC_CONFLICT,
do not invent a local resolution.
```

---

# 2. F0–F6 Cross-Phase Audit

## 2.1 Audit Dimensions

本轮按以下维度重新检查：

```text
Object Ownership
Canonicality
Identity
Version
Reference
Mutability
State Domain
Snapshot Boundary
Lineage
Command / Event Authority
Evaluation Epistemics
Diagnosis / Probe Ordering
Intervention Authority
Knowledge Writeback
Conformance Coverage
```

---

## 2.2 Normalization Register

### N01｜Review Session Closure

**Earlier drift:** ReviewSession 容易被设计成带 mutable `closed_at` 的“immutable object”。

**Final rule:**

```text
ReviewSessionRoot = immutable root
ReviewSessionClosed = event / operational closure fact
```

禁止 retroactive mutation ReviewSessionRoot。

**Status:** `RESOLVED / FROZEN`

---

### N02｜InterventionTransaction

**Earlier drift:** InterventionTransaction 曾容易被理解为历史 Intervention 真相。

**Final rule:**

```text
di.b06.intervention_transaction
object_class = OPERATIONAL_CONTROL_STATE
historical_ssot = false
persistent_ref_kind = NONE
```

历史 Intervention truth 使用 ARSO：

```text
InterventionPlan
InterventionResult
ValidationPlan
ValidationResult
```

**Status:** `RESOLVED / FROZEN`

---

### N03｜SystemChangeCandidate Lifecycle

**Earlier drift:** Candidate 可能携带 mutable lifecycle status。

**Final rule:**

```text
SystemChangeCandidate = immutable proposal fact
```

不得把：

```text
PROPOSED
VALIDATING
PROMOTED
REJECTED
```

作为可变字段写回 Candidate。

过程状态属于 orchestration/event layer。

**Status:** `RESOLVED / FROZEN`

---

### N04｜MemoryMaturity vs KnowledgeMaturity

**Final types:**

```text
MemoryMaturity:
  RAW
  CURATED
  REUSABLE
  STALE
  QUARANTINED
```

```text
KnowledgeMaturity:
  RAW
  CANDIDATE
  PROVISIONAL
  VALIDATED
  STABLE
```

\[
MemoryMaturity \neq KnowledgeMaturity
\]

**Status:** `RESOLVED / FROZEN`

---

### N05｜MemoryItem lifecycle overlap

**Detected drift:** Earlier MemoryItem schemas also carried a second `lifecycle_status`, which overlaps with `STALE/QUARANTINED` already encoded in MemoryMaturity.

**Final rule for Exact V1:**

```text
MemoryItem MUST NOT carry a second generic lifecycle_status field.
```

Memory lifecycle is represented through:

```text
maturity
retention_policy_ref
validity_ref
MemoryCurationDecision / events
```

Archive/deprecation/destructive-retention behavior belongs to RetentionPolicy and immutable governance decisions.

**Status:** `NORMALIZED NOW / FROZEN`

---

### N06｜CompiledReferenceBinding Canonicality

**Final rule:**

```text
CompiledReferenceBinding = nested execution value
NOT a standalone canonical primitive
```

Three-layer reference model remains:

```text
ReferenceAsset               [Infrastructure]
ReferenceIntentBinding       [B01]
CompiledReferenceBinding     [B03 nested value]
```

\[
ReferenceAsset \neq ReferenceIntent \neq CompiledReferenceBinding
\]

**Status:** `RESOLVED / FROZEN`

---

### N07｜KnowledgeSnapshot validity duplication

**Detected drift:** F6.1 baseline introduced candidate `knowledge_validity_refs`.

**Final Exact V1 rule:**

`KnowledgeSnapshot` MUST freeze exact knowledge content and applicable policy closure, but MUST NOT duplicate validity links already owned by the referenced knowledge revisions unless an upstream object lacks such linkage.

Minimum V1 snapshot:

```text
fashion_ontology_ref
design_grammar_ref
semantic_parameter_space_ref
brand_dna_ref
enterprise_knowledge_refs[]
eligibility_policy_refs[]
access_policy_refs[]
content_hash
created_at
```

`knowledge_validity_refs` is **not mandatory Exact V1**.

**Status:** `NORMALIZED NOW / FROZEN`

---

### N08｜Knowledge object Artifact eligibility

**Detected ambiguity:** `artifact_eligible` was at risk of meaning either “generic versioned asset” or “ARSO System Artifact”.

**Final semantic definition:**

```text
artifact_eligible
=
eligible to participate as an ARSO behavior-affecting System Artifact
```

It does **not** mean merely “versioned object”.

Therefore:

```text
BrandDNAProfile
EnterpriseKnowledgeItem
KnowledgeValidity
RetentionPolicy
KnowledgeAccessPolicy
```

are Knowledge-domain canonical objects and are **not direct System Artifact targets by default**.

Runtime activation occurs through:

```text
SystemSnapshot.knowledge_snapshot_ref
```

not by individually injecting enterprise knowledge objects into SystemSnapshot.

B02 semantic assets may be represented in the KnowledgeSnapshot closure and may also be artifact-governed when explicitly required by owner policy; direct activation still must respect snapshot boundaries.

**Status:** `NORMALIZED NOW / FROZEN`

---

### N09｜Canonical Hash Contract

**Detected drift:** F0/F1 direction required deterministic canonical hashing, while F6.1 implementation only proves a Python-side deterministic candidate; cross-language JCS compatibility is not yet demonstrated.

**Normative target:**

For JSON-native canonical payloads:

\[
content\_hash
=
SHA256(
RFC8785\_CanonicalJSON(
CanonicalPayload
))
\]

CanonicalPayload excludes:

```text
content_hash itself
transport-only metadata
mutable operational fields
```

For semantic revision hashes, V1 excludes:

```text
created_at
created_by
```

unless the object's explicit identity policy says otherwise.

**Release condition:** Cross-language fixtures MUST prove byte-identical canonicalization.

Until that test passes:

```text
Hash Algorithm Contract = FROZEN
Hash Implementation = FREEZE CANDIDATE
```

---

### N10｜ARSO Primitive Ownership

No DI shadow copies are permitted for:

```text
ReferenceTaskSpec
SystemSnapshot
RunRecord
RuntimeEvent
ObservabilityProfile
ObjectiveSpec
MeasurementSpec
EvaluatorBinding
EvaluationRecord
EvidenceItem
EvidenceBundle
DiagnosticBelief
HypothesisRecord
IdentifiabilityAssessment
ProbePlan
ProbeResult
ActionDecision
InterventionPlan
InterventionResult
ValidationPlan
ValidationResult
ExperimentAssignment
BudgetReservation
```

Exact V1 production code MUST import/adapt authoritative ARSO contract types.

Temporary integration stubs MAY exist during development, but:

```text
stub != Exact V1 canonical type
```

**Status:** `BOUNDARY FROZEN / EXACT IMPORT BLOCKER REMAINS`

---

### N11｜B01/B02 Exact Schema Completeness

F0–F6 freeze the ownership and semantic role of B01/B02 but the available F6.1 executable baseline does not yet contain full exact B01/B02 schemas.

Therefore this document MUST NOT fabricate missing field-level contracts.

Mandatory canonical objects remain:

```text
B01:
  StyleBrief
  DesignContextBinding
  DesignDecision
  DesignRoute
  DesignSpec
  ReferenceIntentBinding
  DesignTaskBinding

B02:
  FashionOntology
  DesignGrammar
  SemanticParameterSpace
  ApplicabilityRule
```

Their exact field-level schemas are a **release blocker** until imported from or frozen against their owning B01/B02 contracts.

**Status:** `NO CONCEPT CONFLICT / COMPLETENESS BLOCKER`

---

### N12｜Command / Event Inventory

F6.1 executable baseline proves only a partial inventory.

Known implemented command types include:

```text
ApproveDesignCommand
ForkDesignBranchCommand
RequestDesignEditCommand
RequestFashionSemanticCommitCommand
```

Known event normalization includes:

```text
ReviewSessionClosedEvent
```

Exact V1 MUST define the complete command/event surface required by the frozen runtime; no implicit state mutation is permitted.

**Status:** `INCOMPLETE / RELEASE BLOCKER`

---

### N13｜Protocol Surface

Required protocol capabilities include at least:

```text
CanonicalObjectStore
ExactReferenceResolver
BranchHead CAS Store
ArtifactRegistry
AssetStore
Executor / Model Gateway
ARSO Contract Integration Boundary
```

Exact method signatures and static type conformance remain incomplete in F6.1.

**Status:** `INCOMPLETE / RELEASE BLOCKER`

---

### N14｜Semantic Closure

Schema-level validation alone cannot establish semantic closure because referenced objects must be resolved.

Required resolver checks include:

```text
Decision.brief_ref == State.brief_ref
Route.decision_ref == State.decision_ref
Spec.route_ref == State.selected_route_ref
ExactObjectRef.object_type matches target
ExactObjectRef.logical_id matches target
ExactObjectRef.version_id matches exact target id
ExactObjectRef.content_hash matches target payload
```

**Status:** `CONTRACT FROZEN / STORE-RESOLVER TEST BLOCKER`

---

### N15｜CAS and Historical Immutability

Final rule:

```text
BranchHeadPointer = OPERATIONAL_CONTROL_STATE
DesignStateRevision = IMMUTABLE_GRAPH_NODE
```

Mutation command MUST carry:

```text
expected_head_state_ref
```

Mismatch:

```text
HEAD_CONFLICT
```

No Last-Write-Wins.

**Status:** `FROZEN / CAS FIXTURE BLOCKER REMAINS`

---

### N16｜Exact V1 Freeze Status

The existence of a passing partial baseline does not upgrade Exact V1 to FROZEN.

Required final condition:

```text
All mandatory schemas exist
+ authoritative ARSO types integrated
+ full command/event inventory
+ protocol type checks
+ semantic resolver tests
+ CAS tests
+ snapshot firewalls
+ CS-01–CS-32
+ cross-language hash fixture
= PASS
```

Only then:

```text
Exact V1 Pydantic Schemas:
FREEZE CANDIDATE -> FROZEN
```

**Status:** `FROZEN RELEASE RULE`

---

# 3. Global Schema Policy

## 3.1 Runtime Baseline

```text
Python >= 3.12
Pydantic v2
typing.Protocol for behavioral interfaces
ISO-8601 UTC timestamps
opaque identifiers
strict validation
```

Core canonical Pydantic models:

```python
model_config = ConfigDict(
    extra="forbid",
    frozen=True,
)
```

Operational control state may be represented by immutable update DTOs or controlled store mutation, but MUST NOT masquerade as historical SSOT.

---

## 3.2 Extensions

Domain-specific extension fields MUST be placed under namespaced:

```text
extensions:
  <namespace>:
    ...
```

Forbidden:

```text
adding arbitrary domain fields to ARSO Core models
```

Extensions MUST NOT override Core semantics.

---

# 4. Canonical Type System

## 4.1 Object Classes

```text
CANONICAL_REVISION
IMMUTABLE_FACT
IMMUTABLE_ROOT
IMMUTABLE_GRAPH_NODE
SNAPSHOT
OPERATIONAL_CONTROL_STATE
DERIVED_VIEW
```

## 4.2 Persistence / Reference Matrix

| Object Class | Historical SSOT | Versioned | Persistent Ref |
|---|---:|---:|---|
| CANONICAL_REVISION | yes | yes | ExactObjectRef |
| IMMUTABLE_FACT | yes | no | ObjectRef |
| IMMUTABLE_ROOT | yes | no | ObjectRef |
| IMMUTABLE_GRAPH_NODE | yes | no | ObjectRef |
| SNAPSHOT | yes | no | ObjectRef |
| OPERATIONAL_CONTROL_STATE | no | no | none |
| DERIVED_VIEW | no | no | none unless materialized |

\[
HistoricalTruthImmutable
\]

\[
OperationalPointersMayMutate
\]

---

# 5. Identity, Version & Reference

## 5.1 Nominal Identity Types

The implementation MUST distinguish:

```text
ObjectId
LogicalId
SchemaVersion
ObjectType
```

\[
ID \neq LogicalID \neq Revision \neq SchemaVersion
\]

`revision` is server-assigned ordering metadata only.

Parentage is defined by:

```text
parent_refs
```

not `revision + 1`.

---

## 5.2 ExactObjectRef

```yaml
ExactObjectRef:
  object_type:
  logical_id:
  version_id:
  content_hash:
```

Validation MUST prove all four agree with the resolved target.

---

## 5.3 ObjectRef

```yaml
ObjectRef:
  object_type:
  object_id:
  content_hash:
```

Used for non-versioned immutable objects.

---

## 5.4 LogicalObjectRef

```yaml
LogicalObjectRef:
  object_type:
  logical_id:
```

Allowed only in authoring workflows.

\[
LogicalRef
\rightarrow
ResolveExact
\rightarrow
Commit/Compile/Run/Evaluate/Snapshot
\]

Runtime MUST reject:

```text
latest
current latest
most recent available
```

as implicit dependency semantics.

---

# 6. Canonical Metadata

The Exact V1 model family SHOULD use class-specific bases rather than forcing every command/event/control state through a single canonical-object base.

Stable DI canonical objects require, where applicable:

```text
schema_version
id
object_type
created_at
created_by
tenant_scope
provenance
extensions
```

Versioned revisions additionally require:

```text
logical_id
revision
parent_refs
```

Commands and events have their own identity/correlation metadata and MUST NOT be registered as canonical domain primitives merely because they are persisted.

---

# 7. Ownership Registry

## 7.1 Global Rule

\[
OneCanonicalObject
\Rightarrow
OnePrimitiveOwner
\]

Capability ownership may differ from primitive ownership.

---

## 7.2 B01

```text
StyleBrief
DesignContextBinding
DesignDecision
DesignRoute
DesignSpec
ReferenceIntentBinding
DesignTaskBinding
```

---

## 7.3 B02

```text
FashionOntology
DesignGrammar
SemanticParameterSpace
ApplicabilityRule
```

---

## 7.4 B03

```text
GenerationCompiler
CompilerMappingTrace
GenerationPackage
DesignInstance
```

Nested, non-canonical:

```text
CompiledReferenceBinding
CompilerMappingEntry
GenerationConstraintBundle
```

---

## 7.5 B04

DI-owned:

```text
ObjectiveDefinition
EvaluationContract
EvaluatorCalibrationProfile
StructuredFinding
```

ARSO-owned runtime primitives:

```text
ObjectiveSpec
MeasurementSpec
EvaluatorBinding
EvaluationRecord
```

No DI shadow copies.

---

## 7.6 B05

DI-owned:

```text
DiagnosticPolicy
EvidenceConstructionPolicy
DiagnosticCalibrationProfile
FashionFailureExtension
ProbeRecommendation
```

ARSO-owned:

```text
ObservabilityProfile
EvidenceItem
EvidenceBundle
DiagnosticBelief
HypothesisRecord
IdentifiabilityAssessment
ProbePlan
ProbeResult
```

---

## 7.7 B06

DI-owned:

```text
SystemChangeCandidate
InterventionRisk
InterventionTransaction
OptimizationLineageRoot
```

ARSO-owned:

```text
ActionDecision
InterventionPlan
InterventionResult
ValidationPlan
ValidationResult
BudgetReservation
```

---

## 7.8 B07

```text
DesignStateRevision
DesignEdit
DesignEditRequest
DesignBranchRoot
BranchHeadPointer
ForkRecord
MergeAnalysis
SemanticMergeConflict
MergeResolution
MergeRecord
ReviewSessionRoot
ReviewRoundOpened
ReviewRoundOutcome
DesignReviewSnapshot
ReviewPresentationManifest
DesignComment
DesignAnnotation
HumanDecision
ApprovalRecord
DesignLineageRoot
```

`ReviewSessionClosedEvent` is an Event, not a canonical primitive.

---

## 7.9 B08

```text
MemoryItem
MemoryCurationDecision
PreferenceSignal
BrandDNAProfile
EnterpriseKnowledgeItem
LearningProposal
KnowledgeClaim
PromotionEvidencePack
KnowledgePromotionDecision
KnowledgeValidity
RetentionPolicy
KnowledgeAccessPolicy
KnowledgeSnapshot
KnowledgeLineageRoot
```

---

## 7.10 Infrastructure

```text
ReferenceAsset
AssetRef
Artifact
ArtifactRef
ExecutorCapabilityProfile
ExecutorBinding
ObjectStore
AssetStore
ArtifactRegistry
```

---

# 8. State Domain Firewall

\[
TaskState
\neq
SystemState
\neq
KnowledgeState
\neq
ReviewState
\]

## Task semantic objects

```text
StyleBrief
DesignDecision
DesignRoute
DesignSpec
DesignStateRevision
DesignInstance
```

## System objects

```text
Compiler
Policies
Executor bindings
Evaluator bindings
Retrieval mechanism
Runtime configuration
Diagnostic policies
```

## Knowledge objects

```text
Memory
BrandDNA
Enterprise knowledge
Knowledge claims
Knowledge snapshots
```

## Review objects

```text
Review sessions/rounds
Review snapshots
Human decisions
Approval
```

A registry entry MUST declare `state_domain`.

State domain does not determine mutability; `object_class` does.

---

# 9. Task Binding & Protected Reference Task

\[
StyleBrief \neq ReferenceTaskSpec
\]

Required bridge:

```text
DesignTaskBinding
```

Conceptually:

\[
ReferenceTaskSpec =
Bind(
StyleBrief,
EnterprisePolicy,
EvaluationObjectives,
Risk,
Budget
)
\]

ReferenceTaskSpec is ARSO-owned and protected.

Ordinary optimization MUST NOT silently alter:

```text
goal
hard constraints
evaluation objectives
risk boundary
data policy
intervention policy
```

Changing these requires a new ReferenceTaskSpec version / experiment condition.

---

# 10. System Artifact Firewall

## 10.1 System Artifact eligible examples

```text
GenerationCompiler
CompilerTemplate
ReferenceBindingPolicy
ConstraintLoweringPolicy
Measurement implementation
Evaluator implementation / prompt
DiagnosticPolicy
ActionPolicy
RetrievalPolicy
RoutePolicy
DecisionPolicy
```

## 10.2 Not ordinary System Artifacts

```text
StyleBrief
DesignDecision
DesignRoute
DesignSpec
DesignStateRevision
DesignInstance
HumanDecision
ApprovalRecord
```

\[
DesignSpec \neq SystemArtifact
\]

A normal E06 System Intervention MUST NOT mutate DesignSpec.

---

# 11. Snapshot Architecture

## 11.1 SystemSnapshot

ARSO-owned.

Answers:

> What behavior/configuration system executed the run?

May include:

```text
artifact refs
executor bindings
evaluator bindings
adapter versions
external dependencies
environment
runtime config
knowledge_snapshot_ref
retrieval implementation/config
```

MUST NOT contain per-case:

```text
StyleBrief
DesignDecision
DesignRoute
DesignSpec
```

---

## 11.2 KnowledgeSnapshot

B08-owned.

Answers:

> What governed knowledge content was available?

Contains exact knowledge-content closure, not retrieval algorithm implementation.

---

## 11.3 DesignReviewSnapshot

B07-owned.

Answers:

> What exactly did the reviewer see?

Must freeze:

```text
exact DesignState
visible DesignInstances
visible Evaluations
materialized Evaluation presentations
materialized Diagnostic presentations
visible References
presentation manifest
review runtime snapshot
```

Dynamic derived views MUST be materialized before becoming historical review provenance.

---

# 12. Run Closure

\[
RunClosure =
ReferenceTaskSpec
+
ExactInputState
+
SystemSnapshot
+
Randomness
+
RuntimeTrace
\]

Generation:

\[
RunClosure_{gen}
=
T^{ref}
+
DesignSpec_v
+
SystemSnapshot_s
+
\xi
+
RunRecord
\]

Generation SystemSnapshot and Evaluation SystemSnapshot are separately traceable.

---

# 13. E02 / E07 Semantic Runtime

Production semantic chain:

\[
StyleBrief
\rightarrow
DesignContextBinding
\rightarrow
DesignDecision
\rightarrow
DesignRoute
\rightarrow
DesignSpec
\]

## 13.1 Command-first mutation

```text
Command
↓
Authorization
↓
Resolve Exact Refs
↓
Expected Head Check
↓
Transition Guard
↓
Semantic Validation
↓
Create New Canonical Revisions
↓
Create DesignStateRevision
↓
Append Events
↓
CAS Head Pointer
```

Forbidden:

```text
UI -> UPDATE DesignSpec
Agent -> direct database write
```

---

## 13.2 DesignStateRevision

`DesignStateRevision` is an immutable graph node and may represent a valid semantic prefix.

Upstream change invalidates downstream active-head references, but historical objects are retained.

---

## 13.3 Branching

```text
DesignBranchRoot = immutable root
BranchHeadPointer = operational state
```

Every branch mutation requires `expected_head_state_ref`.

---

## 13.4 Review

```text
ReviewSessionRoot = immutable
ReviewRoundOpened = immutable fact
ReviewRoundOutcome = immutable fact
review_stage_projection = projection only
```

HumanDecision MUST bind an exact DesignReviewSnapshot.

Approval is a governed workflow fact, not DesignQuality and not CommercialRelease.

---

## 13.5 Merge

Merge is semantic synthesis:

```text
Common Ancestor
→ Semantic Diff
→ SemanticMergeConflict
→ MergeResolution
→ B01 synthesis
→ B02 validation
→ New DesignSpec revision
```

Generic JSON merge is forbidden.

---

# 14. E03 Generation Boundary

\[
DesignSpec \neq GenerationPackage
\]

\[
DesignSpec
\rightarrow
GenerationCompiler
\rightarrow
GenerationPackage
\rightarrow
Executor
\rightarrow
DesignInstance
\]

Reference model:

```text
ReferenceAsset
→ ReferenceIntentBinding
→ CompiledReferenceBinding
```

Retry semantics:

```text
ExecutionRetry
!= Recompile
!= ExecutorSwitch
!= DesignRevision
```

`DesignInstance` MUST NOT own:

```text
quality_score
approval
commercial_success
```

---

# 15. E04 Evaluation Contract

\[
Objective
\neq
Measurement
\neq
Evaluator
\neq
Evaluation
\]

\[
DesignQuality
\neq
GenerationFidelity
\]

Hard constraints are gates, not weighted-average terms.

Constraint status must distinguish:

```text
SATISFIED
PARTIALLY_SATISFIED
VIOLATED
UNDETERMINED
NOT_APPLICABLE
UNOBSERVABLE
```

\[
UNOBSERVABLE \neq VIOLATED
\]

No DI canonical shadow `EvaluationRecord` or `MeasurementRecord`.

---

# 16. E05 Diagnostic Contract

\[
Evaluation
\neq
Evidence
\neq
Diagnosis
\neq
Causality
\]

\[
Confidence \neq Identifiability
\]

`ProbeRecommendation` is advisory and MUST NOT carry executable authority.

Correct order:

```text
DiagnosticBelief
→ Identifiability
→ ProbeRecommendation
→ ActionDecision
```

Only if:

```text
ActionDecision = REQUEST_EVIDENCE
```

may an executable ARSO ProbePlan be created.

Probe loop:

\[
ProbePlan
\rightarrow
ProbeResult
\rightarrow
NewEvidence
\rightarrow
NewDiagnosticBelief
\]

Direct:

```text
ProbeResult -> Repair
```

is forbidden.

---

# 17. E06 Action / Intervention Contract

ARSO action space:

```text
NO_CHANGE
ABSTAIN
REQUEST_EVIDENCE
REQUEST_HUMAN
INTERVENE
SEARCH
STOP
```

\[
Action \neq Search
\]

`SEARCH` alone may create SearchPlan.

Permission:

\[
EffectivePermission
=
Capability
\cap
TaskPolicy
\cap
GovernancePolicy
\]

Values:

```text
DENIED
READ_ONLY
SANDBOX_ONLY
HUMAN_GATED
AUTO_ALLOWED
```

`SystemChangeCandidate` is immutable.

`InterventionTransaction` is operational only.

Validation MUST support VG0–VG3.

\[
ValidatedSystemChange
\neq
ProductionDeployment
\neq
StableKnowledge
\]

---

# 18. E08 Knowledge Contract

E08 is extended capability, not a prerequisite for E01–E07 runtime.

\[
History
\neq
Memory
\neq
Knowledge
\]

\[
Store
\neq
Curate
\neq
Learn
\neq
Promote
\]

PreferenceSignal MUST exclude `VIEW` as a strong preference signal.

Stable Knowledge promotion requires all:

```text
KG0 Provenance Integrity
KG1 Evidence Sufficiency
KG2 Counterevidence & Regression
KG3 Scope Validation
KG4 Governance Approval
```

\[
Promotion
\neq
Commit
\neq
Activation
\]

B08 may propose semantic change; B02 owns the new semantic version.

B08 may propose system learning; E05/E06 govern diagnosis/intervention.

PromotionEvidencePack MUST reference ARSO evidence rather than create a second evidence substrate.

---

# 19. Long-Term Lineage

Exactly four long-term lineage families:

```text
BusinessLineage
DesignLineage
OptimizationLineage
KnowledgeLineage
```

Execution is RuntimeTrace, not a fifth persistent lineage.

All long-term feedback:

\[
EveryLongTermFeedbackLoop
\rightarrow
NewImmutableVersionOrSnapshot
\]

No revisioned “lineage graph blob” may be used as SSOT.

---

# 20. Registry Manifest Contract

Every canonical registry entry MUST declare at least:

```text
object_type
python_type
schema_version
canonical
primitive_owner
capability_owners
object_class
state_domain
versioned
persistent_ref_kind
historical_ssot
logical_authoring_ref_allowed
system_snapshot_eligible
knowledge_snapshot_eligible
review_snapshot_eligible
system_intervention_target_eligible
artifact_eligible
```

Required invariants:

```text
object_type unique
primitive_owner exactly one
object_class compatible with persistent_ref_kind
DesignSpec.system_intervention_target_eligible = false
DesignSpec.artifact_eligible = false
GenerationCompiler.artifact_eligible = true
GenerationCompiler.system_intervention_target_eligible = true
BranchHeadPointer.historical_ssot = false
InterventionTransaction.historical_ssot = false
```

Knowledge-domain objects MUST NOT become direct active system configuration merely because they are versioned.

---

# 21. Command Contract

## 21.1 Global rule

\[
Command \neq Object \neq Event
\]

Commands express requested intent.

Commands MUST include enough data for:

```text
authorization
expected-head/CAS where applicable
exact-ref resolution
idempotency/correlation
```

The exact V1 inventory MUST be complete before FROZEN.

Existing baseline command schemas are informative but not sufficient.

---

# 22. Event Contract

Events record something that happened.

Historical root objects MUST NOT be “closed” by mutation if closure can be represented as an event/fact.

Example:

```text
ReviewSessionClosedEvent
```

Event persistence MUST NOT cause the event type to become a canonical domain primitive automatically.

---

# 23. Protocol Contract

## 23.1 CanonicalObjectStore

Required capability:

```python
class CanonicalObjectStore(Protocol):
    def put_new(...): ...
    def put_revision(...): ...
    def get_exact(...): ...
    def list_revisions(...): ...
    def resolve_logical_for_authoring(...): ...
```

`put_revision` MUST validate exact expected parent references.

---

## 23.2 Branch Head CAS

Required capability:

```text
read current head
compare expected head
atomically replace with new head
fail with HEAD_CONFLICT
```

No Last-Write-Wins.

---

## 23.3 ExactReferenceResolver

Must validate:

```text
object_type
logical_id
version_id/object_id
content_hash
```

against stored target.

---

## 23.4 ARSO Integration

DI MUST consume authoritative ARSO contract types through a stable import/interface boundary.

No duplicate DI-owned evidence/diagnosis/probe/action schemas.

---

# 24. Forbidden Schema/API Names

The following are forbidden when ambiguous:

```text
SystemCandidate
Candidate
Validation
Knowledge
State
```

Forbidden shadow types:

```text
di.EvidenceBundle
di.DiagnosticBelief
DiagnosticHypothesis  [use ARSO HypothesisRecord]
di.ProbePlan
di.ActionDecision
InterventionValidationResult
```

Forbidden architectural patterns:

```text
revisioned DesignLineage blob
revisioned OptimizationLineage blob
revisioned KnowledgeLineage blob
implicit "latest" runtime ref
direct DesignSpec system intervention
direct B08 system activation
```

---

# 25. Global Invariants

1. `StyleBrief != Prompt`
2. `StyleBrief != ReferenceTaskSpec`
3. `Decision != Spec`
4. `Route != RandomVariant`
5. `DesignSpec != FashionTruth`
6. `DesignSpec != GenerationPackage`
7. `DesignSpec != SystemArtifact by default`
8. `ReferenceAsset != ReferenceIntent != CompiledReferenceBinding`
9. `DesignQuality != GenerationFidelity`
10. `Objective != Measurement != Evaluator != Evaluation`
11. `Evaluation != Evidence`
12. `Evidence != Diagnosis`
13. `Diagnosis != Causality`
14. `DiagnosticBelief != ForcedClassification`
15. `Confidence != Identifiability`
16. `ProbeRecommendation != ProbePlan`
17. `Probe != Intervention`
18. `Action != Search`
19. `DesignEdit != GenerationEdit`
20. `GenerationEdit != SystemIntervention`
21. `SystemIntervention != KnowledgePromotion`
22. `HumanDecision != HumanEvaluation`
23. `HumanApproval != DesignQuality`
24. `CommercialOutcome != PureDesignReward`
25. `History != Memory != Knowledge`
26. `MemoryMaturity != KnowledgeMaturity`
27. `EnterpriseKnowledge != FashionTruth`
28. `KnowledgePromotion != SemanticOwnership`
29. `KnowledgePromotion != Activation`
30. `Capability != Permission`
31. `TemporalFeedbackLoop != OwnershipCycle`
32. `EveryLongTermLoopMustCrossImmutableVersionBoundary`

---

# 26. CS-01–CS-32 Acceptance Suite

| ID | Requirement |
|---|---|
| CS-01 | 每个 canonical object 只有一个 Primitive Owner |
| CS-02 | Capability Owner 与 Primitive Owner 可显式区分 |
| CS-03 | StyleBrief 不能直接作为 ReferenceTaskSpec |
| CS-04 | 每个 ARSO Run 可解析 exact ReferenceTaskSpec |
| CS-05 | SystemSnapshot 不包含 per-case Brief/Decision/Route/Spec |
| CS-06 | DesignSpec 不被普通 System Intervention 当 artifact 修改 |
| CS-07 | System Artifact 与 Task Semantic Object 类型可区分 |
| CS-08 | B03 EDIT 不创建新的 Design semantics |
| CS-09 | Reference 三层对象严格区分 |
| CS-10 | Design/Optimization/Knowledge lineage 均为 immutable root |
| CS-11 | Execution 不生成第五条长期 Lineage |
| CS-12 | Jobs/Pointers 不成为 historical SSOT |
| CS-13 | Branch head 使用 CAS |
| CS-14 | Historical DesignState 永不更新 |
| CS-15 | Review Session/round root 不被 close action 修改 |
| CS-16 | ReviewStage 只能是 collaboration fact 的 projection |
| CS-17 | ReviewSnapshot 不引用动态未物化 View |
| CS-18 | 任一 HumanDecision 可重建 reviewer 实际看到的内容 |
| CS-19 | Generation 与 Evaluation snapshot 分别追溯 |
| CS-20 | Review 可比较多个不同 executor provenance 的 instances |
| CS-21 | ProbeRecommendation 不可直接执行 |
| CS-22 | REQUEST_EVIDENCE 后才生成 executable ProbePlan |
| CS-23 | ProbeResult 必须先形成 Evidence 再 Rediagnose |
| CS-24 | PromotionEvidencePack 不复制第二套 Evidence |
| CS-25 | B08 无 Knowledge activation authority |
| CS-26 | Knowledge content 与 Retrieval mechanism 分离 |
| CS-27 | MemoryMaturity / KnowledgeMaturity type-safe |
| CS-28 | Semantic writeback 最终由 B02 commit |
| CS-29 | Compiler/Evaluator learning 必须经过 E05/E06 |
| CS-30 | Stable Knowledge 不自动进入 active SystemSnapshot |
| CS-31 | Validated Intervention 不自动成为 Stable Knowledge |
| CS-32 | 所有长期反馈产生新 version/snapshot |

---

# 27. Additional F0–F6 Acceptance Gates

In addition to CS-01–CS-32, Exact V1 requires:

```text
AC-01 full B01 exact schemas
AC-02 full B02 exact schemas
AC-03 authoritative ARSO type imports
AC-04 exact command inventory
AC-05 exact event inventory
AC-06 protocol signatures + static type checks
AC-07 semantic-closure resolver fixtures
AC-08 CanonicalObjectStore revision-parent fixtures
AC-09 BranchHead CAS fixtures
AC-10 SystemSnapshot negative firewall
AC-11 KnowledgeSnapshot negative firewall
AC-12 DesignReviewSnapshot provenance firewall
AC-13 RFC-8785 cross-language hash fixtures
AC-14 registry completeness: all mandatory canonical objects present
AC-15 forbidden shadow-type scan
AC-16 ambiguous bare-name scan
AC-17 MemoryItem has no duplicate lifecycle field
AC-18 KnowledgeSnapshot has no mandatory duplicate validity closure
```

---

# 28. F6.1 Release Gate

The current executable baseline may be reported as:

```text
Package compile              PASS
JSON Schema generation       PASS
Registry generation          PASS
Partial automated tests      PASS
```

but Exact V1 may become `FROZEN` only when:

\[
\boxed{
CS01\text{–}CS32
\land
AC01\text{–}AC18
=
PASS
}
\]

and there are no unresolved `SPEC_CONFLICT` records.

---

# 29. Codex Implementation Rules

Codex MUST:

```text
1. treat this document as first code-level authority
2. never infer a missing exact schema from a lower-priority narrative spec
3. stop on unresolved contract conflict
4. not create DI shadow ARSO primitives
5. not introduce mutable fields into historical canonical objects
6. not use implicit "latest" refs in committed/runtime objects
7. not treat DesignSpec as ordinary System Artifact
8. not make ProbeRecommendation executable
9. not bypass Evidence -> Rediagnosis after ProbeResult
10. not activate Knowledge directly from B08
11. not create a fifth long-term ExecutionLineage
12. generate tests for every registry invariant
13. keep Physical DB design separate from canonical domain contract
14. preserve OPEN/DEFERRED boundaries
```

Codex MUST NOT implement, merely because a placeholder appears in a narrative source:

```text
autonomous global ontology evolution
autonomous grammar evolution
automatic production activation
meta-learning
cross-domain transfer
fully learned router
commercial-outcome causal optimizer
```

---

# 30. Implementation Order

Recommended exact-contract build order:

```text
P0  Core nominal types + base classes
P1  Exact refs + canonical hash + registry
P2  Full B01 exact schemas
P3  Full B02 exact schemas
P4  ARSO exact primitive imports
P5  B03 schemas
P6  B04 extension schemas
P7  B07 semantic/collaboration schemas
P8  B05 diagnostic extension schemas
P9  B06 controlled optimization schemas
P10 B08 governed-learning schemas
P11 Complete Command/Event inventory
P12 Protocol interfaces
P13 Semantic resolver + stores + CAS fixtures
P14 CS-01–CS-32 + AC-01–AC-18
P15 Freeze decision
```

This build order does not imply product feature priority; it is the dependency order for Exact Contract conformance.

---

# 31. Remaining OPEN vs DEFERRED

## OPEN

```text
physical database schema
storage engine
event bus implementation
memory retrieval algorithm
embedding/ranking
model selection
evaluation thresholds
diagnostic algorithm
search algorithm
promotion thresholds
knowledge utility estimator
```

## DEFERRED

```text
automatic production deployment
autonomous global ontology/grammar evolution
meta-learning
cross-domain transfer
cross-enterprise knowledge sharing
continuous production self-modification
fully learned meta-router
commercial-outcome causal optimization
```

---

# 32. Final Normative Statement

> Design Intelligence Exact V1 adopts a single canonical primitive owner for every persistent semantic object; exact-version references before any committed or runtime action; immutable historical semantic, review, optimization and knowledge facts; typed operational control state for pointers/jobs/transactions; separate Task/System/Knowledge/Review state domains; protected ARSO ReferenceTaskSpec and SystemSnapshot boundaries; owner-mediated semantic writeback; ARSO-owned epistemic primitives for evaluation evidence, diagnosis, probes, actions, interventions and validation; immutable human review provenance; and governed knowledge promotion that is distinct from semantic commit and production activation.

The normalized F0–F6 contract is therefore:

\[
\boxed{
ExactIdentity
+
ImmutableHistory
+
SingleOwnership
+
TypedBoundaries
+
ExplicitAuthority
+
AutomatedConformance
}
\]

The **document-level F0–F6 contract is frozen by this specification**.

The **Exact V1 executable schema set remains `FREEZE CANDIDATE` until all CS-01–CS-32 and AC-01–AC-18 gates pass**.
