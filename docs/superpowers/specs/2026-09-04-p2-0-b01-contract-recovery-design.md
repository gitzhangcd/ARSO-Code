# P2.0｜B01 Owner Contract Recovery + Field-Level Exact Schema Freeze

日期：2026-09-04
状态：`WRITTEN SPEC CANDIDATE`
父阶段：P1 `FROZEN`
后续阶段：P2 `Full B01 Exact Schemas Implementation`

## 1. 目标

P2.0 不是 B01 production implementation，而是消除 `GAP-001 / AC-01` 的前置规范工作。

目标是从既有权威规范中恢复、归一化并冻结 B01 的 field-level owner contract，使后续 P2 可以在不猜字段、不提升 candidate baseline 为权威的前提下实现 Exact V1 Pydantic schemas。

P2.0 必须覆盖 exactly 7 个 B01 canonical objects：

```text
StyleBrief
DesignContextBinding
DesignDecision
DesignRoute
DesignSpec
ReferenceIntentBinding
DesignTaskBinding
```

该集合由 `DI-V5-EXACT-CONTRACT` N11 作为最高优先级 B01 mandatory surface 固定。

## 2. 非目标

P2.0 明确禁止：

```text
src/design_intelligence/contracts/b01/*.py production models
B02 production schemas
ARSO shadow primitives
resolver/store/CAS
Command/Event/Protocol implementation
complete Exact V1 registry inventory
B03 compiler implementation
UI / LLM / image / vector DB / optimizer
```

P2.0 可以产生规范、审计、source ledger、field ledger、checksum/governance 更新，但不能以“为了验证设计”为由偷偷引入 B01 production class。

## 3. 权威顺序

P2.0 继续遵守仓库既有 authority order：

1. `specs/00-CODE-FREEZE/DI_V5_Exact_V1_Schema_API_Contract_Freeze_Specification.md`
2. `specs/01-AUTHORITY/Design-Intelligence-V5.0-Engineering-Specification-V1.0.txt`
3. `specs/01-AUTHORITY/Cross-Spec-Consistency-Freeze.txt`
4. `specs/02-UPSTREAM/ARSO-Engineering-Specification-V2.2.1.txt`
5. `specs/02-UPSTREAM/Design-Intelligence-V5.0-Application-Specification.txt`
6. `specs/02-UPSTREAM/Design-Intelligence-x-ARSO-V2.2.1-Implementation-Blueprint.txt`
7. `specs/03-RESEARCH/ARSO-Research-Specification-V2.2.1.txt`

Candidate baseline `di_contracts_v1/` 只作为 executable evidence，不是 owner contract authority。

## 4. P2.0 的 Authority 产物

最终拟新增 scoped exact owner authority：

```text
specs/00-CODE-FREEZE/DI_B01_Exact_V1_Owner_Contract.md
```

它的权威关系为：

```text
1A  DI-V5-EXACT-CONTRACT
    global / cross-domain / release authority

1B  DI-B01-EXACT-CONTRACT
    B01 field-level scoped authority

2+  existing authority chain
```

约束：`DI-B01-EXACT-CONTRACT` MUST NOT override 1A；它只允许填补 N11 明确留下的 B01 field-level completeness gap。

## 5. Recovery Decision Taxonomy

每一个最终字段、nested value、enum/value-set、reference、object classification、registry property 和 CanonicalPayload decision 都必须带一个恢复状态：

```text
DIRECT_FROZEN
NORMALIZED_RECOVERY
NEW_FREEZE_DECISION
DEFERRED
REJECTED
```

定义：

- `DIRECT_FROZEN`：高优先级来源已经给出可直接编码的字段/语义/边界。
- `NORMALIZED_RECOVERY`：多个已有来源共同稳定同一语义，但 wire type / cardinality / exact field name 需要在 P2.0 归一化。
- `NEW_FREEZE_DECISION`：既有来源不足以唯一决定 wire contract，但该决定是完成 N11 所必需，并且不改变更高优先级语义。
- `DEFERRED`：当前不是 B01 Exact V1 必需字段，或需要后续 owner/runtime contract 才能决定。
- `REJECTED`：candidate-only、低优先级漂移、重复 owner 或违反 frozen boundary 的字段/设计。

禁止出现无状态、无来源的 field。

## 6. Field Decision Ledger 必填列

最终 `B01_FIELD_DECISION_LEDGER.md` 对每个字段至少记录：

| 列 | 说明 |
|---|---|
| Object | B01 owner object |
| Field / Value Type | field 或 nested value |
| Wire Type | Exact V1 type |
| Cardinality | scalar / optional / list / map 等 |
| Requiredness | required / optional |
| Semantic Owner | B01 / Infrastructure / ARSO 等 |
| Reference Kind | ExactObjectRef / ObjectRef / LogicalObjectRef / none |
| Source | 规范路径 + section/normalization |
| Decision State | 五类 recovery status |
| CanonicalPayload | included / excluded / owner-specific note |
| Rationale | 为什么该决定不构成 fabrication |

## 7. 全局 Canonical Shell Recovery

在业务字段前，P2.0 必须逐对象判断是否使用 canonical revision shell。

可用的全局 canonical metadata policy 包括：

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

若对象属于 versioned canonical revision，则还要逐对象决定并记录：

```text
logical_id
revision
parent_refs
```

P2.0 不允许一句“B01 都 versioned”代替逐对象 classification 证据。

每个对象必须明确：

```text
object_class
state_domain
versioned
historical_ssot
persistent_ref_kind
logical_authoring_ref_allowed
system_snapshot_eligible
knowledge_snapshot_eligible
review_snapshot_eligible
system_intervention_target_eligible
artifact_eligible
```

这些 registry properties 的值必须由 owner semantics + global registry rules共同推出，不能从 `di_contracts_v1` manifest 直接抄写。

## 8. B01 Semantic Chain Closure

P2.0 必须让 schema 能表达 frozen semantic chain：

```text
StyleBrief
→ DesignContextBinding
→ DesignDecision
→ DesignRoute
→ DesignSpec
```

并支持后续 P13 resolver 验证：

```text
Decision.brief_ref == State.brief_ref
Route.decision_ref == State.decision_ref
Spec.route_ref == State.selected_route_ref
```

P2.0 只冻结 ref field 和 ref kind；target resolution / content-hash semantic closure 仍属于 P13。

## 9. Object-Specific Recovery Rules

### 9.1 StyleBrief

`StyleBrief != prompt`，且 `StyleBrief != ReferenceTaskSpec`。

Application-level stable semantics 包括至少：

```text
Category
Customer
Market / Channel
Season / Occasion
Commercial Role
Price / Positioning
Style Intent
Must Have / Avoid
Reference Intent
Material Context
Fit / Silhouette
Novelty
Hard / Soft Constraints
```

同时必须保持 typed requirement semantics：

```text
MUST
PREFER
EXPLORE
AVOID
FORBID
```

`Constraint != Preference`。P2.0 可以把这些稳定语义归一化为 nested value contracts，但必须逐项记录为 `NORMALIZED_RECOVERY` 或 `NEW_FREEZE_DECISION`，不得直接把叙述性标题当成最终 field name。

### 9.2 DesignContextBinding

必须保持“上下文绑定”职责，而不是复制 StyleBrief 内容。P2.0 需要恢复它绑定的 exact context refs、与 `StyleBrief` 的关系以及 canonical classification。

若某个 context source 实际由 B02、Infrastructure 或 ARSO owner，B01 只能持 ref，不得复制 owner schema。

### 9.3 DesignDecision

`DesignDecision = strategy / allocation`，不是 garment description，也不是 DesignSpec。

稳定语义至少包括：

```text
Primary Focus
Secondary Focus
Visual Hierarchy
Silhouette Strategy
Volume Distribution
Construction Emphasis
Surface / Material Expression
Novelty Allocation
Commercial / Risk Allocation
```

具体 wire groups 与 field names 通过 ledger 冻结。

### 9.4 DesignRoute

`DesignRoute != RandomVariant`。

它必须表示在 DesignDecision 约束下的一条可执行设计路线/方案假设，并持有可被后续 semantic closure 验证的 `decision_ref`。

P2.0 必须决定 route identity、route intent、mechanism/strategy representation、selection relation 与 route-level constraints 的 exact contract；没有足够来源的 candidate field 不得自动保留。

### 9.5 DesignSpec

`DesignSpec = AuthoritativeStructuredIntent`。

必须保持：

```text
DesignSpec != GlobalGroundTruth
DesignSpec != GenerationPackage
DesignSpec != ordinary SystemArtifact
```

它应表达 selected route 对设计意图的权威结构化实例，并持有可支持 `Spec.route_ref == State.selected_route_ref` 的 exact route reference。

P2.0 必须单独冻结 DesignSpec 的 CanonicalPayload policy；P1 hash engine 不负责猜字段。

### 9.6 ReferenceIntentBinding

必须保持三层边界：

```text
ReferenceAsset              [Infrastructure]
ReferenceIntentBinding      [B01]
CompiledReferenceBinding    [B03 nested value]
```

已存在的稳定 intent vocabulary 示例包括：

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

P2.0 必须从 frozen boundary 反推出最小 exact contract，至少能够回答：

```text
Which ReferenceAsset?
Why is it used?
Where does it apply?
What must be preserved?
What may change?
What is the semantic constraint strength?
```

这些问题不等于预先批准同名 fields；最终 field name/type 仍由 ledger 冻结。

### 9.7 DesignTaskBinding

该对象已有较强 direct-source evidence。Engineering / Cross-Spec 给出了字段级 YAML，包括：

```text
id
design_state_ref
style_brief_ref
evaluation_contract_ref
enterprise_hard_policy_refs
risk_policy_ref
budget_policy_ref
intervention_policy_ref
reference_task_spec_ref
created_at
```

P2.0 优先将业务字段视为 `DIRECT_FROZEN` recovery candidate，并补齐：canonical shell、exact ref kinds、owner boundaries、classification、registry policy、CanonicalPayload policy。

尤其保持：

```text
StyleBrief != ReferenceTaskSpec
```

DesignTaskBinding 是 DI task semantics 与 ARSO task contract 的显式桥，不允许把二者合并成一个 primitive。

## 10. Source Matrix

P2.0 使用独立的 `B01_SOURCE_RECOVERY_MATRIX.md` 记录 source strength，而不是让 owner contract 自己掩盖证据不足。

每个对象需要按以下维度评级：

```text
owner / mandatory surface
semantic role
field names
wire types
requiredness
reference kinds
object class
registry policy
canonical payload
negative boundaries
```

评级：

```text
STRONG
PARTIAL
SEMANTIC_ONLY
MISSING
```

## 11. Conflict / Gap Rules

若高优先级来源之间无法同时满足：

```text
SPEC_CONFLICT
→ stop that object path
```

若语义明确但 field-level contract 无法唯一恢复，且没有经过 P2.0 明确的新 freeze decision：

```text
SPEC_GAP
→ do not guess
```

低优先级 source 只能补充未定义区域，不能覆盖更高优先级 frozen boundary。

## 12. Candidate Baseline Policy

`di_contracts_v1` 对 B01 只有 `di.b01.design_spec -> external.B01.DesignSpec` sentinel，不能提供完整 B01 owner schema。

因此：

```text
candidate field != owner truth
candidate registry value != frozen owner policy
sentinel != canonical production model
```

P2.0 可以记录 candidate 与 recovered contract 的差异，但禁止 bulk-copy。

## 13. P2.0 Deliverables

P2.0 最终至少包含：

```text
specs/00-CODE-FREEZE/DI_B01_Exact_V1_Owner_Contract.md
B01_SOURCE_RECOVERY_MATRIX.md
B01_FIELD_DECISION_LEDGER.md
B01_CROSS_SPEC_FREEZE_AUDIT.md
docs/superpowers/specs/2026-09-04-p2-0-b01-contract-recovery-design.md
```

同时按需要更新：

```text
SPEC_AUTHORITY.md
SPEC_SOURCE_CHECKSUMS.sha256
README.md
AGENTS.md
```

## 14. Freeze Gate

只有以下全部成立，P2.0 才可进入 Frozen Checkpoint：

```text
7 / 7 B01 canonical objects covered

Every field has:
  source
  type
  cardinality
  requiredness
  semantic owner
  reference kind
  payload policy

No unexplained field
No candidate-only field promoted silently

Frozen distinctions preserved:
  TaskState != SystemState != KnowledgeState != ReviewState
  StyleBrief != ReferenceTaskSpec
  DesignSpec != GenerationPackage
  DesignSpec != ordinary SystemArtifact
  ReferenceAsset != ReferenceIntentBinding != CompiledReferenceBinding

Object class fixed for all 7
Registry policy fixed for all 7
CanonicalPayload policy fixed for all 7

SPEC_CONFLICT = 0
Blocking field-level SPEC_GAP = 0
```

成功后：

```text
P2.0 = FROZEN
P2 Full B01 Exact Schemas = AUTHORIZABLE
```

若任一 mandatory field-level gap 无法被规范化：

```text
P2.0 = BLOCKED
P2 = NOT AUTHORIZED
```

## 15. Current Gate

```text
P0: FROZEN
P1: FROZEN
P2.0: WRITTEN SPEC CANDIDATE / RECOVERY IN PROGRESS
P2: NOT AUTHORIZED
P3+: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```
