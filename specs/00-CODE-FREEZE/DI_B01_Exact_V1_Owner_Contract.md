# Design Intelligence B01 Exact V1 Owner Contract

## Business / Design Semantic State｜Field-Level Schema Freeze

**Document ID:** `DI-B01-EXACT-CONTRACT`  
**Version:** `V1.0-FC1`  
**Date:** `2026-09-04`  
**Document Type:** Scoped Owner Schema / Registry / CanonicalPayload Contract  
**Status:** `FREEZE CANDIDATE`  
**Parent Authority:** `DI-V5-EXACT-CONTRACT V1.0-FC1`  
**Normative Scope:** B01 field-level exact contract only

---

# 0. Authority and Scope

This document fills the B01 field-level completeness gap explicitly left by `DI-V5-EXACT-CONTRACT` N11.

Authority relation:

```text
1A  DI-V5-EXACT-CONTRACT
    global / cross-domain / release authority

1B  DI-B01-EXACT-CONTRACT
    B01 field-level scoped authority

2+  existing authority chain
```

Rules:

```text
DI-B01-EXACT-CONTRACT MUST NOT override 1A.
A lower-priority source MUST NOT override this B01 owner contract after freeze.
A genuine contradiction emits SPEC_CONFLICT.
No B01 production implementation is authorized merely by this document's existence.
```

This document owns exactly seven canonical B01 objects:

```text
StyleBrief
DesignContextBinding
DesignDecision
DesignRoute
DesignSpec
ReferenceIntentBinding
DesignTaskBinding
```

It does not own B02 semantic definitions, B03 execution values, B04 evaluation primitives, B07 design-state lineage, Infrastructure assets, or ARSO primitives.

---

# 1. Frozen Global Distinctions

The following boundaries are inherited unchanged:

```text
TaskState != SystemState != KnowledgeState != ReviewState
StyleBrief != ReferenceTaskSpec
DesignDecision != DesignSpec
DesignSpec != GenerationPackage
DesignSpec != ordinary SystemArtifact
ReferenceAsset != ReferenceIntentBinding != CompiledReferenceBinding
Constraint != Preference
```

No B01 object may shadow ARSO canonical primitives.

---

# 2. Wire Type Notation

```text
CanonicalRef := ExactObjectRef | ObjectRef
JSONValue    := null | bool | integer | finite-number | string | list[JSONValue] | map[string, JSONValue]
Tuple[T]     := ordered immutable sequence of T
```

`CanonicalRef` is a committed persistent exact reference. It MUST NOT contain `LogicalObjectRef`.

When a referenced primitive belongs to another owner whose object class is not yet frozen, B01 uses `CanonicalRef` instead of deciding that owner's version policy.

---

# 3. Canonical Shell Dependency

This owner contract imports the global canonical metadata roles from `DI-V5-EXACT-CONTRACT` §6.

Stable canonical fields, where applicable:

```text
schema_version: SchemaVersion
id: ObjectId
object_type: ObjectType
created_at: UTC datetime
created_by: ActorRef
tenant_scope: TenantScope
provenance: Provenance
extensions: map[string, JSONValue]
```

Canonical revisions additionally contain:

```text
logical_id: LogicalId
revision: ObjectRevision
parent_refs: Tuple[ExactObjectRef]
```

`ActorRef`, `TenantScope`, `Provenance`, and `ObjectRevision` are shared core-support types and are not redefined by B01. Their internal schema must come from the authoritative global/core contract implementation.

---

# 4. B01 CanonicalPayload Policy

For all B01 semantic content hashes:

```text
INCLUDE:
  schema_version
  object_type
  every B01 owner semantic/binding field
  extensions

EXCLUDE:
  id
  logical_id
  revision
  parent_refs
  created_at
  created_by
  tenant_scope
  provenance
  content_hash itself
```

Rationale:

- N09 explicitly excludes `created_at` and `created_by` from V1 semantic revision hashes unless an owner says otherwise.
- B01 freezes semantic-content hashes, not object identity/order/lineage hashes.
- Exact object identity is independently protected by `version_id` / `object_id` plus content hash.
- Parentage remains authoritative through `parent_refs` and store validation.
- Namespaced `extensions` are part of the B01 serialized semantic payload and therefore participate in the hash.

This is the B01 owner-specific normalization required by P1's deliberate refusal to guess generic CanonicalPayload extraction.

---

# 5. Shared Nested Values

## 5.1 RequirementStrength

Exact V1 values:

```text
MUST
PREFER
EXPLORE
AVOID
FORBID
```

Semantic rule:

```text
MUST / FORBID = constraint semantics
PREFER / EXPLORE / AVOID = preference/exploration semantics
```

The five values MUST NOT be collapsed into one numeric weight.

## 5.2 BriefRequirement

```yaml
BriefRequirement:
  statement: str
  strength: RequirementStrength
  dimension: str | null
```

This is a nested B01 value, not a canonical object.

It is the single Exact V1 representation for functional requirements, must-have/must-avoid requirements, and hard/soft requirement semantics. Separate overlapping lifecycle fields are forbidden.

## 5.3 ContextRefBinding

```yaml
ContextRefBinding:
  context_ref: CanonicalRef
  role: str
```

This nested value binds an exact external context object to a B01 task role. It MUST NOT embed or copy the target object's owner fields.

## 5.4 DesignSpecAssignment

```yaml
DesignSpecAssignment:
  parameter_key: str
  value: JSONValue
  strength: RequirementStrength | null
```

The assignment is B01-owned instance-level intent. The parameter definition / allowed parameter space remains B02-owned.

---

# 6. StyleBrief

## 6.1 Classification

```text
object_type = di.b01.style_brief
object_class = CANONICAL_REVISION
state_domain = TASK
versioned = true
persistent_ref_kind = EXACT_OBJECT_REF
historical_ssot = true
logical_authoring_ref_allowed = true
```

## 6.2 Exact owner fields

In addition to the canonical revision shell:

```yaml
StyleBrief:
  category: str | null
  customer_segments: Tuple[str]
  market_channels: Tuple[str]
  season_occasions: Tuple[str]
  commercial_role: str | null
  price_positioning: str | null
  style_intent: Tuple[str]
  mood_aesthetic: Tuple[str]
  design_focus: Tuple[str]
  reference_intent_refs: Tuple[ExactObjectRef]
  material_context: Tuple[str]
  fit_silhouette_direction: Tuple[str]
  novelty_expectation: str | null
  requirements: Tuple[BriefRequirement]
```

All fields are present in the exact wire shape. Tuple fields may be empty unless a domain validator defines a stricter use-case-specific rule. Nullable scalar fields may be null.

## 6.3 Semantic normalization

The upstream semantic headings:

```text
Functional Requirements
Must Have
Must Avoid
Hard / Soft Constraints
```

are normalized into `requirements[*]` using `RequirementStrength` and optional `dimension`; they MUST NOT also appear as duplicated owner fields.

Negative rules:

```text
StyleBrief != prompt
StyleBrief != ReferenceTaskSpec
```

---

# 7. ReferenceIntentBinding

## 7.1 Classification

```text
object_type = di.b01.reference_intent_binding
object_class = CANONICAL_REVISION
state_domain = TASK
versioned = true
persistent_ref_kind = EXACT_OBJECT_REF
historical_ssot = true
logical_authoring_ref_allowed = true
```

## 7.2 Exact owner fields

```yaml
ReferenceIntentBinding:
  reference_asset_ref: CanonicalRef
  intent_codes: Tuple[str]
  application_scope: Tuple[str]
  preserve: Tuple[str]
  allow_change: Tuple[str]
  strength: RequirementStrength
```

`intent_codes` MUST be non-empty at owner validation.

Exact V1 implementations MUST recognize at least the following standard codes:

```text
SILHOUETTE_REFERENCE
DETAIL_REFERENCE
MATERIAL_REFERENCE
COLOR_REFERENCE
STRUCTURE_REFERENCE
MOOD_REFERENCE
KEEP_REFERENCE
EDIT_REFERENCE
```

The value set is intentionally open because upstream specifications present these as typical intent categories rather than an exhaustive enum. Additional codes MUST NOT change the meaning of the standard codes.

Negative rules:

```text
ReferenceIntentBinding MUST NOT store prompt fragments.
ReferenceIntentBinding MUST NOT store executor/model parameters.
ReferenceIntentBinding MUST NOT store compiled prompt positions or masks.
```

Those belong to B03 `CompiledReferenceBinding` / GenerationPackage lowering.

---

# 8. DesignContextBinding

## 8.1 Classification

```text
object_type = di.b01.design_context_binding
object_class = CANONICAL_REVISION
state_domain = TASK
versioned = true
persistent_ref_kind = EXACT_OBJECT_REF
historical_ssot = true
logical_authoring_ref_allowed = true
```

## 8.2 Exact owner fields

```yaml
DesignContextBinding:
  style_brief_ref: ExactObjectRef
  bindings: Tuple[ContextRefBinding]
```

`bindings` may be empty. If present, every target must resolve to a canonical object whose owner allows persistent reference.

Allowed target-owner families may include B02 semantic assets, B08/enterprise knowledge objects, Infrastructure assets, or ARSO-owned context primitives. B01 stores only exact ref + role.

Forbidden embedded copies include:

```text
FashionOntology contents
DesignGrammar contents
SemanticParameterSpace definitions
ReferenceAsset metadata
ReferenceTaskSpec contents
EvaluationRecord contents
```

---

# 9. DesignDecision

## 9.1 Classification

```text
object_type = di.b01.design_decision
object_class = CANONICAL_REVISION
state_domain = TASK
versioned = true
persistent_ref_kind = EXACT_OBJECT_REF
historical_ssot = true
logical_authoring_ref_allowed = true
```

## 9.2 Exact owner fields

```yaml
DesignDecision:
  brief_ref: ExactObjectRef
  context_binding_ref: ExactObjectRef
  primary_focus: str | null
  secondary_focus: Tuple[str]
  visual_hierarchy: Tuple[str]
  silhouette_strategy: str | null
  volume_distribution: Tuple[str]
  construction_emphasis: Tuple[str]
  surface_complexity: str | null
  material_expression: Tuple[str]
  novelty_allocation: str | null
  commercial_risk_allocation: str | null
```

Semantic rule:

```text
DesignDecision = DesignStrategy / allocation
DesignDecision != DetailedGarmentDescription
DesignDecision != DesignSpec
```

---

# 10. DesignRoute

## 10.1 Classification

```text
object_type = di.b01.design_route
object_class = CANONICAL_REVISION
state_domain = TASK
versioned = true
persistent_ref_kind = EXACT_OBJECT_REF
historical_ssot = true
logical_authoring_ref_allowed = true
```

## 10.2 Exact owner fields

```yaml
DesignRoute:
  decision_ref: ExactObjectRef
  route_name: str
  mechanisms: Tuple[str]
  constraints: Tuple[BriefRequirement]
  rationale: str | null
```

`mechanisms` MUST be non-empty at owner validation.

No mutable selection flag is permitted on the route. Route selection belongs to the immutable DesignState lineage through `selected_route_ref`.

Negative rules:

```text
DesignRoute != RandomVariant
DesignRoute MUST NOT contain executor/model/prompt/random-seed fields
```

---

# 11. DesignSpec

## 11.1 Classification

```text
object_type = di.b01.design_spec
object_class = CANONICAL_REVISION
state_domain = TASK
versioned = true
persistent_ref_kind = EXACT_OBJECT_REF
historical_ssot = true
logical_authoring_ref_allowed = true
```

## 11.2 Exact owner fields

```yaml
DesignSpec:
  route_ref: ExactObjectRef
  semantic_parameter_space_ref: CanonicalRef
  assignments: Tuple[DesignSpecAssignment]
  reference_intent_refs: Tuple[ExactObjectRef]
  constraints: Tuple[BriefRequirement]
```

`assignments` MUST be non-empty at owner validation.

`semantic_parameter_space_ref` grounds `parameter_key` vocabulary in a B02-owned semantic parameter space without copying B02 parameter definitions into B01.

Semantic rule:

```text
DesignSpec = AuthoritativeStructuredIntent
DesignSpec != GlobalGroundTruth
DesignSpec != Prompt
DesignSpec != GenerationPackage
DesignSpec != ordinary SystemArtifact
```

Forbidden B03/runtime fields include:

```text
prompt
negative_prompt
image_reference_payload
mask
executor
model_parameters
resolution
aspect_ratio
generation_status
```

---

# 12. DesignTaskBinding

## 12.1 Classification

```text
object_type = di.b01.design_task_binding
object_class = IMMUTABLE_FACT
state_domain = TASK
versioned = false
persistent_ref_kind = OBJECT_REF
historical_ssot = true
logical_authoring_ref_allowed = false
```

A changed input produces a new immutable binding fact; it does not mutate or version the previous binding.

## 12.2 Exact owner fields

In addition to the immutable-fact canonical shell:

```yaml
DesignTaskBinding:
  design_state_ref: ObjectRef
  style_brief_ref: ExactObjectRef
  evaluation_contract_ref: CanonicalRef
  enterprise_hard_policy_refs: Tuple[CanonicalRef]
  risk_policy_ref: CanonicalRef | null
  budget_policy_ref: CanonicalRef | null
  intervention_policy_ref: CanonicalRef | null
  reference_task_spec_ref: ExactObjectRef
```

`design_state_ref` targets B07 `DesignStateRevision`, whose `IMMUTABLE_GRAPH_NODE` classification is globally frozen by N15.

`reference_task_spec_ref` targets ARSO `ReferenceTaskSpec`. DesignTaskBinding MUST NOT duplicate the ARSO task fields:

```text
goal
solution geometry
hard constraints
soft objectives
objective refs
risk
cost
data policy
intervention policy
```

---

# 13. Registry Contract

All entries use:

```text
schema_version = 1.0
canonical = true
primitive_owner = DI_B01
capability_owners = [DI_B01]
state_domain = TASK
historical_ssot = true
system_snapshot_eligible = false
knowledge_snapshot_eligible = false
system_intervention_target_eligible = false
artifact_eligible = false
```

Exact registry matrix:

| object_type | python_type | object_class | versioned | persistent_ref_kind | logical_authoring_ref_allowed | review_snapshot_eligible |
|---|---|---|---:|---|---:|---:|
| `di.b01.style_brief` | `design_intelligence.contracts.b01.StyleBrief` | CANONICAL_REVISION | true | EXACT_OBJECT_REF | true | true |
| `di.b01.reference_intent_binding` | `design_intelligence.contracts.b01.ReferenceIntentBinding` | CANONICAL_REVISION | true | EXACT_OBJECT_REF | true | true |
| `di.b01.design_context_binding` | `design_intelligence.contracts.b01.DesignContextBinding` | CANONICAL_REVISION | true | EXACT_OBJECT_REF | true | true |
| `di.b01.design_decision` | `design_intelligence.contracts.b01.DesignDecision` | CANONICAL_REVISION | true | EXACT_OBJECT_REF | true | true |
| `di.b01.design_route` | `design_intelligence.contracts.b01.DesignRoute` | CANONICAL_REVISION | true | EXACT_OBJECT_REF | true | true |
| `di.b01.design_spec` | `design_intelligence.contracts.b01.DesignSpec` | CANONICAL_REVISION | true | EXACT_OBJECT_REF | true | true |
| `di.b01.design_task_binding` | `design_intelligence.contracts.b01.DesignTaskBinding` | IMMUTABLE_FACT | false | OBJECT_REF | false | false |

`DesignSpec.artifact_eligible=false` and `DesignSpec.system_intervention_target_eligible=false` are inherited direct global rules. The corresponding negative values for the other B01 task-semantic/binding objects are frozen here to preserve the Task/System boundary.

---

# 14. Semantic Closure Contract

The following relations are normative. Schema validation proves shape; P13 resolver tests must later prove target agreement:

```text
DesignContextBinding.style_brief_ref
  == DesignDecision.brief_ref

DesignDecision.brief_ref
  == DesignStateRevision.brief_ref

DesignRoute.decision_ref
  == DesignStateRevision.decision_ref

DesignSpec.route_ref
  == DesignStateRevision.selected_route_ref

StyleBrief.reference_intent_refs[*]
  -> ReferenceIntentBinding

DesignSpec.reference_intent_refs[*]
  -> ReferenceIntentBinding

DesignTaskBinding.style_brief_ref
  -> task exact StyleBrief

DesignTaskBinding.design_state_ref
  -> bound DesignStateRevision
```

Every committed B01 ref must be exact/persistent. `LogicalObjectRef` is authoring-only and MUST resolve before commit/compile/run/evaluate/snapshot.

---

# 15. Recovery Decision Register

## Directly frozen or strongly recovered

```text
B01 mandatory surface = exactly 7
StyleBrief semantic areas
RequirementStrength semantic values
DesignDecision semantic dimensions
DesignRoute mechanism-distinguishable semantics
DesignSpec AuthoritativeStructuredIntent semantics
DesignTaskBinding source YAML fields
N14 brief/decision/route closure relations
DesignSpec negative artifact/intervention policy
three-layer reference separation
```

## P2.0 NEW_FREEZE_DECISION surface

The following wire choices are explicitly frozen by this scoped owner contract because prior sources did not uniquely determine them:

```text
six authored semantic B01 objects -> CANONICAL_REVISION
DesignTaskBinding -> IMMUTABLE_FACT
B01 object_type strings
B01 target Python type paths
DesignContextBinding exact shape
ReferenceIntentBinding exact shape
StyleBrief semantic-field wire normalization
DesignDecision exact wire field names/cardinality
DesignRoute exact wire shape
DesignSpec assignment-based exact shape
DesignTaskBinding optionality for risk/budget/intervention policy refs
B01 review-snapshot eligibility
negative artifact/intervention flags for non-DesignSpec B01 objects
B01 owner-specific CanonicalPayload exclusion/inclusion policy
```

These choices are owner-level normalization, not claims that the lower-priority prose already contained these exact wire schemas.

---

# 16. Rejected Candidate / Drift Surface

The following MUST NOT be promoted into B01 Exact V1 unless a future frozen owner revision explicitly changes this contract:

```text
external.B01.DesignSpec sentinel as owner schema
implicit latest/current reference semantics
prompt fields on DesignSpec
executor/model fields on DesignRoute or DesignSpec
mutable selected/status fields on DesignRoute
embedded ARSO ReferenceTaskSpec fields inside StyleBrief or DesignTaskBinding
embedded B02 definitions inside DesignContextBinding or DesignSpec
compiled reference fields inside ReferenceIntentBinding
```

---

# 17. P2.0 Freeze Conditions

This owner contract is eligible to move from `FREEZE CANDIDATE` to `FROZEN` only when:

```text
7/7 B01 canonical objects covered
all owner fields have type/cardinality/requiredness/ref policy
all 7 object classifications fixed
all 7 registry policies fixed
all 7 CanonicalPayload policies fixed
source ledger and field ledger trace every normalization
SPEC_CONFLICT = 0
blocking B01 field-level SPEC_GAP = 0
cross-spec audit PASS
no B01 production Python model added during P2.0
user explicitly approves P2.0 Freeze
```

Only after that approval may P2 `Full B01 Exact Schemas Implementation` be authorized.

Current status:

```text
DI-B01-EXACT-CONTRACT: FREEZE CANDIDATE
P2.0: RECOVERY IMPLEMENTATION IN PROGRESS
P2: NOT AUTHORIZED
Exact V1 global: FREEZE CANDIDATE
```
