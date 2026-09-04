# B01 Field Decision Ledger

日期：2026-09-04  
阶段：P2.0｜B01 Owner Contract Recovery + Field-Level Exact Schema Freeze  
状态：`RECOVERY DECISIONS COMPLETE / OWNER CONTRACT PENDING`

## 1. Ledger 规则

本文件记录 B01 七个 mandatory canonical objects 的 field-level recovery decision。每个决定只能属于：

```text
DIRECT_FROZEN
NORMALIZED_RECOVERY
NEW_FREEZE_DECISION
DEFERRED
REJECTED
```

`di_contracts_v1` 只允许作为 structural evidence，不能单独支撑 `DIRECT_FROZEN` 或 `NEW_FREEZE_DECISION`。

## 2. Wire notation

```text
CanonicalRef := ExactObjectRef | ObjectRef
JSONValue    := null | bool | integer | finite-number | string | list[JSONValue] | map[string, JSONValue]
Tuple[T]     := ordered immutable sequence of T
```

`CanonicalRef` 仅允许 persistent exact references；不含 `LogicalObjectRef`。当被引用对象的 primitive owner 尚未冻结其 object class 时，B01 使用 `CanonicalRef`，避免越权替 B02 / B04 / Infrastructure / ARSO 决定版本策略。

## 3. Imported global canonical shell

B01 不重新定义 global core metadata 的内部 schema。它直接继承 `DI-V5-EXACT-CONTRACT` §6 的字段角色：

| Field | Wire type / role | Applicable | Decision | CanonicalPayload |
|---|---|---|---|---|
| `schema_version` | `SchemaVersion` | all 7 | DIRECT_FROZEN | included |
| `id` | `ObjectId` | all 7 | DIRECT_FROZEN | excluded |
| `object_type` | `ObjectType` | all 7 | DIRECT_FROZEN | included |
| `created_at` | UTC datetime | all 7 | DIRECT_FROZEN | excluded by N09 semantic-hash rule |
| `created_by` | shared core `ActorRef` | all 7 | DIRECT_FROZEN field role | excluded by N09 semantic-hash rule |
| `tenant_scope` | shared core `TenantScope` | all 7 | DIRECT_FROZEN field role | excluded; scope metadata is not B01 semantic content |
| `provenance` | shared core `Provenance` | all 7 | DIRECT_FROZEN field role | excluded; provenance does not alter intended design semantics |
| `extensions` | `map[string, JSONValue]` namespaced | all 7 | DIRECT_FROZEN field role + NEW_FREEZE_DECISION payload policy | included |
| `logical_id` | `LogicalId` | canonical revisions | DIRECT_FROZEN by global version contract | excluded |
| `revision` | shared core `ObjectRevision` | canonical revisions | DIRECT_FROZEN role | excluded; server ordering metadata |
| `parent_refs` | `Tuple[ExactObjectRef]` | canonical revisions | DIRECT_FROZEN role | excluded; lineage metadata is validated separately |

### B01-H01｜CanonicalPayload normalization

For B01 semantic content hashes:

```text
included:
  schema_version
  object_type
  all B01 owner semantic/binding fields
  extensions

excluded:
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

Decision: `NEW_FREEZE_DECISION` for B01 owner policy, consistent with N09. Exact version identity remains protected by `version_id`/`object_id` plus `content_hash`; lineage remains protected by `parent_refs` and store validation rather than being folded into semantic content hash.

## 4. Object classification / registry ledger

Common values for all seven:

```text
canonical = true
primitive_owner = DI_B01
capability_owners = [DI_B01]
state_domain = TASK
historical_ssot = true
system_snapshot_eligible = false
knowledge_snapshot_eligible = false
system_intervention_target_eligible = false
artifact_eligible = false
schema_version = 1.0
```

`StyleBrief`, `DesignDecision`, `DesignRoute`, `DesignSpec` being non-System-Artifacts is direct Engineering evidence. The same negative artifact/intervention policy for `DesignContextBinding`, `ReferenceIntentBinding`, and `DesignTaskBinding` is a `NEW_FREEZE_DECISION` required to preserve `TaskSemanticState != SystemState` and prevent indirect activation through B01 bindings.

| Object | object_type | object_class | versioned | persistent_ref_kind | logical authoring | review snapshot | Decision |
|---|---|---|---:|---|---:|---:|---|
| StyleBrief | `di.b01.style_brief` | `CANONICAL_REVISION` | true | `EXACT_OBJECT_REF` | true | true | NORMALIZED_RECOVERY |
| DesignContextBinding | `di.b01.design_context_binding` | `CANONICAL_REVISION` | true | `EXACT_OBJECT_REF` | true | true | NEW_FREEZE_DECISION |
| DesignDecision | `di.b01.design_decision` | `CANONICAL_REVISION` | true | `EXACT_OBJECT_REF` | true | true | NORMALIZED_RECOVERY |
| DesignRoute | `di.b01.design_route` | `CANONICAL_REVISION` | true | `EXACT_OBJECT_REF` | true | true | NORMALIZED_RECOVERY |
| DesignSpec | `di.b01.design_spec` | `CANONICAL_REVISION` | true | `EXACT_OBJECT_REF` | true | true | NORMALIZED_RECOVERY; candidate sentinel is evidence only |
| ReferenceIntentBinding | `di.b01.reference_intent_binding` | `CANONICAL_REVISION` | true | `EXACT_OBJECT_REF` | true | true | NEW_FREEZE_DECISION |
| DesignTaskBinding | `di.b01.design_task_binding` | `IMMUTABLE_FACT` | false | `OBJECT_REF` | false | false | NEW_FREEZE_DECISION |

### Classification rationale

- The first six are authored task/design semantics whose evolution must retain immutable historical revisions; Engineering already gives `DesignSpec v12 -> v13` as the revision pattern and places Brief/Decision/Route/Spec in Task Semantic State.
- `DesignContextBinding` and `ReferenceIntentBinding` participate in that authored semantic state and therefore follow the same revision rule.
- `DesignTaskBinding` is a historical binding fact over exact task/policy references. Changing any input creates a new fact; it does not mutate/revise a semantic design entity.
- Review eligibility is true for the six semantic revisions because a reproducible design review may need their exact closure. It is false for DesignTaskBinding because task-policy binding is governance/run context, not design review content.

Target Python types for P2 registry entries:

```text
design_intelligence.contracts.b01.StyleBrief
design_intelligence.contracts.b01.DesignContextBinding
design_intelligence.contracts.b01.DesignDecision
design_intelligence.contracts.b01.DesignRoute
design_intelligence.contracts.b01.DesignSpec
design_intelligence.contracts.b01.ReferenceIntentBinding
design_intelligence.contracts.b01.DesignTaskBinding
```

These paths are `NEW_FREEZE_DECISION` for the Exact V1 implementation surface.

---

# 5. Shared B01 nested values

## 5.1 RequirementStrength

```text
MUST
PREFER
EXPLORE
AVOID
FORBID
```

Decision: `DIRECT_FROZEN` semantic values from Application Specification; exact enum representation is `NORMALIZED_RECOVERY`.

## 5.2 BriefRequirement

| Field | Wire type | Cardinality | Required | Owner | Ref kind | Decision | Payload |
|---|---|---|---:|---|---|---|---|
| `statement` | `str` | scalar | yes | B01 | none | NORMALIZED_RECOVERY | included |
| `strength` | `RequirementStrength` | scalar | yes | B01 | none | DIRECT_FROZEN/NORMALIZED_RECOVERY | included |
| `dimension` | `str | null` | scalar | yes | B01 | none | NEW_FREEZE_DECISION | included |

Purpose: one typed requirement representation captures Functional Requirements, Must Have, Must Avoid, and Hard/Soft constraints without duplicating the same semantic requirement across multiple fields. `MUST/FORBID` are constraint semantics; `PREFER/EXPLORE/AVOID` are preference/exploration semantics. `Constraint != Preference` remains explicit.

## 5.3 ContextRefBinding

| Field | Wire type | Cardinality | Required | Owner | Ref kind | Decision | Payload |
|---|---|---|---:|---|---|---|---|
| `context_ref` | `CanonicalRef` | scalar | yes | target owner | exact persistent | NEW_FREEZE_DECISION | included |
| `role` | `str` | scalar | yes | B01 binding semantics | none | NEW_FREEZE_DECISION | included |

This nested value stores only a role + exact persistent ref; it MUST NOT embed copies of B02, B08, Infrastructure, or ARSO-owned context objects.

## 5.4 DesignSpecAssignment

| Field | Wire type | Cardinality | Required | Owner | Ref kind | Decision | Payload |
|---|---|---|---:|---|---|---|---|
| `parameter_key` | `str` | scalar | yes | B01 instance assignment; vocabulary governed by B02 context | none | NEW_FREEZE_DECISION | included |
| `value` | `JSONValue` | scalar JSON value | yes | B01 instance assignment | none | NEW_FREEZE_DECISION | included |
| `strength` | `RequirementStrength | null` | scalar | yes | B01 | none | NEW_FREEZE_DECISION | included |

`DesignSpecAssignment` is an instance-level selected semantic value, not a B02 parameter definition. The referenced `SemanticParameterSpace` remains B02-owned.

---

# 6. R1｜DesignTaskBinding

Direct-source business fields come from Engineering/Cross-Spec YAML. Canonical shell is inherited rather than duplicated below.

| Field | Wire type | Cardinality | Required | Semantic owner | Ref kind | Source/Decision | Payload |
|---|---|---|---:|---|---|---|---|
| `design_state_ref` | `ObjectRef` | scalar | yes | B07 (`DesignStateRevision`) | OBJECT_REF | DIRECT_FROZEN target class via N15 + NORMALIZED_RECOVERY | included |
| `style_brief_ref` | `ExactObjectRef` | scalar | yes | B01 | EXACT_OBJECT_REF | DIRECT field + recovered B01 classification | included |
| `evaluation_contract_ref` | `CanonicalRef` | scalar | yes | B04 | exact persistent | DIRECT field; cross-owner class deferred to B04 owner | included |
| `enterprise_hard_policy_refs` | `Tuple[CanonicalRef]` | list | yes; may be empty | external/ARSO/DI policy owners | exact persistent | DIRECT field + NORMALIZED_RECOVERY cardinality | included |
| `risk_policy_ref` | `CanonicalRef | null` | scalar | yes | policy owner | exact persistent | DIRECT field + NEW_FREEZE_DECISION optionality | included |
| `budget_policy_ref` | `CanonicalRef | null` | scalar | yes | policy owner | exact persistent | DIRECT field + NEW_FREEZE_DECISION optionality | included |
| `intervention_policy_ref` | `CanonicalRef | null` | scalar | yes | policy owner | exact persistent | DIRECT field + NEW_FREEZE_DECISION optionality | included |
| `reference_task_spec_ref` | `ExactObjectRef` | scalar | yes | ARSO | EXACT_OBJECT_REF | DIRECT field; Engineering states ReferenceTaskSpec changes create new version | included |

Rejected:

```text
goal
solution_geometry
hard_constraints
soft_objectives
objective_refs
risk
cost
data_policy
intervention_policy
```

as embedded fields inside DesignTaskBinding because these are `ReferenceTaskSpec` semantics owned by ARSO. The binding references the ARSO object instead of shadowing it.

---

# 7. R2｜StyleBrief

Object classification: `CANONICAL_REVISION`.

All list fields are required in the wire shape and may be empty unless an owner validator later imposes a domain-specific minimum. Nullable scalars are also required fields whose value may be null; this keeps a stable canonical shape without fabricating business mandatory rules.

| Field | Wire type | Cardinality | Required | Semantic owner | Ref kind | Decision | Payload |
|---|---|---|---:|---|---|---|---|
| `category` | `str | null` | scalar | yes | B01 | none | NORMALIZED_RECOVERY from Category | included |
| `customer_segments` | `Tuple[str]` | list | yes | B01 | none | NORMALIZED_RECOVERY from Customer | included |
| `market_channels` | `Tuple[str]` | list | yes | B01 | none | NORMALIZED_RECOVERY from Market/Channel | included |
| `season_occasions` | `Tuple[str]` | list | yes | B01 | none | NORMALIZED_RECOVERY | included |
| `commercial_role` | `str | null` | scalar | yes | B01 | none | NORMALIZED_RECOVERY | included |
| `price_positioning` | `str | null` | scalar | yes | B01 | none | NORMALIZED_RECOVERY | included |
| `style_intent` | `Tuple[str]` | list | yes | B01 | none | NORMALIZED_RECOVERY | included |
| `mood_aesthetic` | `Tuple[str]` | list | yes | B01 | none | NORMALIZED_RECOVERY | included |
| `design_focus` | `Tuple[str]` | list | yes | B01 | none | NORMALIZED_RECOVERY | included |
| `reference_intent_refs` | `Tuple[ExactObjectRef]` | list | yes; may be empty | B01 | EXACT_OBJECT_REF | NORMALIZED_RECOVERY linking stable Reference Intent to canonical binding object | included |
| `material_context` | `Tuple[str]` | list | yes | B01 | none | NORMALIZED_RECOVERY | included |
| `fit_silhouette_direction` | `Tuple[str]` | list | yes | B01 | none | NORMALIZED_RECOVERY | included |
| `novelty_expectation` | `str | null` | scalar | yes | B01 | none | NORMALIZED_RECOVERY | included |
| `requirements` | `Tuple[BriefRequirement]` | list | yes | B01 | none | NORMALIZED_RECOVERY replacing duplicated Must Have/Avoid/Functional/Hard/Soft lists | included |

Rejected as separate duplicated fields:

```text
must_have
must_avoid
functional_requirements
hard_constraints
soft_constraints
```

They are represented by `requirements[*].strength` + `dimension`, preserving the source distinction while avoiding parallel overlapping lifecycles.

Negative boundaries:

```text
StyleBrief != prompt
StyleBrief != ReferenceTaskSpec
```

---

# 8. R3｜ReferenceIntentBinding

Object classification: `CANONICAL_REVISION`.

Known intent codes are a normative **minimum vocabulary**, not a closed enum, because the sources present them as typical examples rather than an exhaustive list:

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

| Field | Wire type | Cardinality | Required | Semantic owner | Ref kind | Decision | Payload |
|---|---|---|---:|---|---|---|---|
| `reference_asset_ref` | `CanonicalRef` | scalar | yes | Infrastructure target / B01 binding | exact persistent | NEW_FREEZE_DECISION; B01 does not decide ReferenceAsset object class | included |
| `intent_codes` | `Tuple[str]` | list | yes; non-empty at owner validation | B01 | none | NORMALIZED_RECOVERY from stable vocabulary; open value set | included |
| `application_scope` | `Tuple[str]` | list | yes | B01 | none | NEW_FREEZE_DECISION answering “where does it apply?” | included |
| `preserve` | `Tuple[str]` | list | yes | B01 | none | NEW_FREEZE_DECISION answering “what must be preserved?” | included |
| `allow_change` | `Tuple[str]` | list | yes | B01 | none | NEW_FREEZE_DECISION answering “what may change?” | included |
| `strength` | `RequirementStrength` | scalar | yes | B01 | none | NORMALIZED_RECOVERY using existing typed requirement semantics | included |

Rejected:

```text
prompt_fragment
compiled_prompt_location
mask
executor_parameter
compiled_reference_payload
```

because those are B03 compiler/executor responsibilities.

Negative boundary:

```text
ReferenceAsset != ReferenceIntentBinding != CompiledReferenceBinding
```

---

# 9. R4｜DesignContextBinding

Object classification: `CANONICAL_REVISION`.

| Field | Wire type | Cardinality | Required | Semantic owner | Ref kind | Decision | Payload |
|---|---|---|---:|---|---|---|---|
| `style_brief_ref` | `ExactObjectRef` | scalar | yes | B01 | EXACT_OBJECT_REF | NEW_FREEZE_DECISION required to make the explicit chain addressable | included |
| `bindings` | `Tuple[ContextRefBinding]` | list | yes; may be empty | B01 binding semantics + target owners | exact persistent | NEW_FREEZE_DECISION | included |

`bindings` MAY target exact B02 semantic assets, B08/enterprise knowledge objects, Infrastructure assets, or ARSO-owned context primitives only when their owner contracts permit persistent reference. B01 stores only ref + role.

Rejected:

```text
embedded_ontology
embedded_grammar
embedded_parameter_space
embedded_reference_asset
embedded_reference_task_spec
embedded_evaluation_record
```

Negative boundary: `DesignContextBinding` binds context; it does not become a second owner of context content.

---

# 10. R5｜DesignDecision

Object classification: `CANONICAL_REVISION`.

| Field | Wire type | Cardinality | Required | Semantic owner | Ref kind | Decision | Payload |
|---|---|---|---:|---|---|---|---|
| `brief_ref` | `ExactObjectRef` | scalar | yes | B01 | EXACT_OBJECT_REF | DIRECT_FROZEN existence via N14 + recovered StyleBrief class | included |
| `context_binding_ref` | `ExactObjectRef` | scalar | yes | B01 | EXACT_OBJECT_REF | NEW_FREEZE_DECISION preserving StyleBrief→Context→Decision chain | included |
| `primary_focus` | `str | null` | scalar | yes | B01 | none | NORMALIZED_RECOVERY | included |
| `secondary_focus` | `Tuple[str]` | list | yes | B01 | none | NORMALIZED_RECOVERY | included |
| `visual_hierarchy` | `Tuple[str]` | list | yes | B01 | none | NORMALIZED_RECOVERY | included |
| `silhouette_strategy` | `str | null` | scalar | yes | B01 | none | NORMALIZED_RECOVERY | included |
| `volume_distribution` | `Tuple[str]` | list | yes | B01 | none | NORMALIZED_RECOVERY | included |
| `construction_emphasis` | `Tuple[str]` | list | yes | B01 | none | NORMALIZED_RECOVERY | included |
| `surface_complexity` | `str | null` | scalar | yes | B01 | none | NORMALIZED_RECOVERY | included |
| `material_expression` | `Tuple[str]` | list | yes | B01 | none | NORMALIZED_RECOVERY | included |
| `novelty_allocation` | `str | null` | scalar | yes | B01 | none | NORMALIZED_RECOVERY | included |
| `commercial_risk_allocation` | `str | null` | scalar | yes | B01 | none | NORMALIZED_RECOVERY | included |

Rejected: detailed garment component/specification assignments. Those belong to DesignSpec.

Negative boundary:

```text
DesignDecision = DesignStrategy
DesignDecision != DetailedGarmentDescription
DesignDecision != DesignSpec
```

---

# 11. R6｜DesignRoute

Object classification: `CANONICAL_REVISION`.

| Field | Wire type | Cardinality | Required | Semantic owner | Ref kind | Decision | Payload |
|---|---|---|---:|---|---|---|---|
| `decision_ref` | `ExactObjectRef` | scalar | yes | B01 | EXACT_OBJECT_REF | DIRECT_FROZEN existence via N14 | included |
| `route_name` | `str` | scalar | yes | B01 | none | NEW_FREEZE_DECISION | included |
| `mechanisms` | `Tuple[str]` | list | yes; non-empty at owner validation | B01 | none | NORMALIZED_RECOVERY from “mechanistically distinguishable route” examples | included |
| `constraints` | `Tuple[BriefRequirement]` | list | yes; may be empty | B01 | none | NEW_FREEZE_DECISION for route-specific constraint closure | included |
| `rationale` | `str | null` | scalar | yes | B01 | none | NEW_FREEZE_DECISION | included |

No `selected: bool` is stored on DesignRoute. Selection belongs to the immutable DesignState lineage (`selected_route_ref`), avoiding mutable selection state on a canonical route revision.

Rejected:

```text
random_seed
executor
model
prompt
compiled_parameters
selected_status
```

Negative boundary: `DesignRoute != RandomVariant` and Route does not become B03 execution configuration.

---

# 12. R7｜DesignSpec

Object classification: `CANONICAL_REVISION`.

| Field | Wire type | Cardinality | Required | Semantic owner | Ref kind | Decision | Payload |
|---|---|---|---:|---|---|---|---|
| `route_ref` | `ExactObjectRef` | scalar | yes | B01 | EXACT_OBJECT_REF | DIRECT_FROZEN existence via N14 | included |
| `semantic_parameter_space_ref` | `CanonicalRef` | scalar | yes | B02 target; B01 binding | exact persistent | NEW_FREEZE_DECISION; avoids copying B02 parameter definitions | included |
| `assignments` | `Tuple[DesignSpecAssignment]` | list | yes; non-empty at owner validation | B01 instance decisions | none | NEW_FREEZE_DECISION guided by typed SemanticParameterSpace + compiler mapping requirements | included |
| `reference_intent_refs` | `Tuple[ExactObjectRef]` | list | yes; may be empty | B01 | EXACT_OBJECT_REF | NORMALIZED_RECOVERY to support downstream reference binding | included |
| `constraints` | `Tuple[BriefRequirement]` | list | yes; may be empty | B01 | none | NORMALIZED_RECOVERY supporting compiler constraint lowering | included |

`DesignSpecAssignment.parameter_key` identifies a selected semantic parameter/path whose definition is governed by the referenced B02 semantic parameter space. B01 owns only the instance-level assignment.

Global registry negatives retained:

```text
artifact_eligible = false
system_intervention_target_eligible = false
system_snapshot_eligible = false
```

Rejected:

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

Those belong to GenerationCompiler / GenerationPackage / execution records.

Negative boundaries:

```text
DesignSpec = AuthoritativeStructuredIntent
DesignSpec != GlobalGroundTruth
DesignSpec != Prompt
DesignSpec != GenerationPackage
DesignSpec != ordinary SystemArtifact
```

---

# 13. Cross-object closure rules

The owner contract must state these as normative semantic constraints; P13 will later prove them through resolver fixtures:

```text
DesignContextBinding.style_brief_ref == DesignDecision.brief_ref
DesignDecision.brief_ref == DesignStateRevision.brief_ref
DesignRoute.decision_ref == DesignStateRevision.decision_ref
DesignSpec.route_ref == DesignStateRevision.selected_route_ref
StyleBrief.reference_intent_refs[*] resolve to ReferenceIntentBinding
DesignSpec.reference_intent_refs[*] resolve to ReferenceIntentBinding
DesignTaskBinding.style_brief_ref resolves to the task's exact StyleBrief
DesignTaskBinding.design_state_ref resolves to the bound DesignStateRevision
```

No committed B01 canonical object may contain `LogicalObjectRef`.

---

# 14. Recovery status summary

| Object | Blocking field-level gap after ledger | Conflict |
|---|---:|---:|
| StyleBrief | 0 | 0 |
| DesignContextBinding | 0 | 0 |
| DesignDecision | 0 | 0 |
| DesignRoute | 0 | 0 |
| DesignSpec | 0 | 0 |
| ReferenceIntentBinding | 0 | 0 |
| DesignTaskBinding | 0 | 0 |

The ledger uses explicit `NEW_FREEZE_DECISION` where sources cannot uniquely determine the wire contract. These are not hidden guesses: they are the P2.0 normalization surface requiring owner-contract review/freeze.

Current status:

```text
SPEC_CONFLICT = 0
blocking B01 field-level SPEC_GAP = 0 in the recovery candidate
P2.0 is NOT yet FROZEN until scoped owner contract + cross-spec audit pass
P2 remains NOT AUTHORIZED
```
