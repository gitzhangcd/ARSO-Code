# B01 Source Recovery Matrix

日期：2026-09-04
阶段：P2.0｜B01 Owner Contract Recovery + Field-Level Exact Schema Freeze
状态：`RECOVERY CANDIDATE`

## 1. 使用说明

本矩阵记录 B01 七个 mandatory canonical objects 在现有 authority chain 中的证据强度。

评级：

```text
STRONG        = 已有可直接转化为 exact contract 的字段/边界证据
PARTIAL       = 有稳定结构或部分字段，但仍缺 exact type/cardinality/requiredness 等
SEMANTIC_ONLY = 语义角色稳定，但没有可直接编码的 field-level contract
MISSING       = 当前 authority chain 中未发现足够 owner-level 定义
```

本矩阵不自行冻结字段；它只回答“我们现在拥有什么证据”。最终 field-level 决策进入 `B01_FIELD_DECISION_LEDGER.md`。

## 2. 全局恢复证据

### 2.1 Highest-priority mandatory surface

`DI-V5-EXACT-CONTRACT` N11 冻结 B01 mandatory canonical surface：

```text
StyleBrief
DesignContextBinding
DesignDecision
DesignRoute
DesignSpec
ReferenceIntentBinding
DesignTaskBinding
```

并明确：现有 F6.1 executable baseline 不包含完整 B01 field-level exact schemas；禁止 fabricated contracts。

结论：

```text
Object set = DIRECT_FROZEN
Field-level completeness = BLOCKED pending P2.0 recovery/freeze
```

### 2.2 Global identity/reference policy

Exact Contract + Engineering 已冻结：

```text
ObjectId != LogicalId != Revision != SchemaVersion
ExactObjectRef != ObjectRef != LogicalObjectRef
revision = server-assigned ordering metadata
parentage = parent_refs
LogicalObjectRef = authoring only
runtime/commit/compile/evaluate/snapshot require exact resolution
```

结论：B01 owner contract 无权重新定义这些全局语义。

### 2.3 Semantic closure constraints

Exact Contract N14 已冻结至少：

```text
Decision.brief_ref == State.brief_ref
Route.decision_ref == State.decision_ref
Spec.route_ref == State.selected_route_ref
```

这些约束可以证明 `DesignDecision.brief_ref`、`DesignRoute.decision_ref`、`DesignSpec.route_ref` 具有高强度字段存在证据，但 exact ref kind / requiredness 仍需结合 owner classification 冻结。

### 2.4 Candidate baseline limits

`di_contracts_v1` 只提供：

```text
di.b01.design_spec
→ external.B01.DesignSpec
```

sentinel registry entry；没有可导入的 B01 owner model，也没有其余 6 个 B01 canonical models。

因此 candidate baseline 对 B01 field recovery 的权重：

```text
STRUCTURAL EVIDENCE ONLY
NOT OWNER AUTHORITY
```

---

# 3. Object Matrix

## 3.1 StyleBrief

### Source evidence

**Exact Contract**

- mandatory B01 canonical object；
- `StyleBrief != ReferenceTaskSpec` 由 global distinction/frozen boundary 保持；
- semantic chain 起点；
- DesignDecision semantic closure 需要 `brief_ref` 与 DesignState brief 一致。

**Engineering / Cross-Spec**

- 持续采用 `StyleBrief → DesignContextBinding → DesignDecision → DesignRoute → DesignSpec`；
- StyleBrief 属 B01 semantic ownership；
- 不应吸收 ARSO `ReferenceTaskSpec` owner fields。

**Application Specification**

稳定语义集合至少包括：

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

稳定 requirement semantics：

```text
MUST
PREFER
EXPLORE
AVOID
FORBID
```

并明确：

```text
Constraint != Preference
StyleBrief != prompt
```

### Recovery strength

| 维度 | 评级 | 说明 |
|---|---|---|
| owner / mandatory surface | STRONG | N11 明确 |
| semantic role | STRONG | 多规范一致 |
| field names | SEMANTIC_ONLY | Application 多为概念标题，未必是 wire field name |
| wire types | MISSING | 需 P2.0 freeze |
| requiredness | MISSING | 需 P2.0 freeze |
| reference kinds | PARTIAL | Reference Intent 等 owner/ref 边界可恢复，exact kind未完全给出 |
| object class | PARTIAL | canonicality明确，是否 canonical revision需逐证据冻结 |
| registry policy | PARTIAL | owner明确，eligibility/refs需冻结 |
| CanonicalPayload | MISSING | 必须 owner-specific freeze |
| negative boundaries | STRONG | brief != prompt, brief != ReferenceTaskSpec |

初始结论：`RECOVERABLE / NOT YET EXACT`。

---

## 3.2 DesignContextBinding

### Source evidence

**Exact / Engineering / Cross-Spec**

- mandatory B01 object；
- semantic chain明确位于 StyleBrief 与 DesignDecision 之间；
- 名称和职责稳定为 context binding，而不是 context content owner。

当前未发现完整 field-level YAML。

### Recovery constraints

P2.0 必须保持：

```text
DesignContextBinding
= refs/bindings to owner context
!= duplicate B02 / Infrastructure / ARSO context schema
```

任何由其他 primitive owner 管理的 context 只能通过 reference 进入 B01 binding。

### Recovery strength

| 维度 | 评级 | 说明 |
|---|---|---|
| owner / mandatory surface | STRONG | N11 |
| semantic role | STRONG | chain position + binding semantics |
| field names | MISSING | 未发现完整 owner schema |
| wire types | MISSING | 需 freeze |
| requiredness | MISSING | 需 freeze |
| reference kinds | PARTIAL | 其职责天然为 binding，但 target set/ref kinds仍需确定 |
| object class | PARTIAL | canonicality明确，revision policy待恢复 |
| registry policy | MISSING | 需 owner freeze |
| CanonicalPayload | MISSING | 需 owner freeze |
| negative boundaries | STRONG | 不复制其他 owner context content |

初始结论：`HIGH-PRIORITY NORMALIZED_RECOVERY REQUIRED`。

---

## 3.3 DesignDecision

### Source evidence

**Exact Contract**

- mandatory B01 object；
- N14 明确 `Decision.brief_ref == State.brief_ref`，提供 `brief_ref` 的强字段证据。

**Application Specification**

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

语义定位：strategy / allocation，而不是 garment description。

### Recovery strength

| 维度 | 评级 | 说明 |
|---|---|---|
| owner / mandatory surface | STRONG | N11 |
| semantic role | STRONG | strategy/allocation |
| field names | PARTIAL | `brief_ref` 强；其余多为 semantic headings |
| wire types | MISSING | strategy groups需归一化 |
| requiredness | PARTIAL | `brief_ref` 接近 mandatory；其他待 freeze |
| reference kinds | PARTIAL | brief ref exact kind需与 StyleBrief classification一起冻结 |
| object class | PARTIAL | canonical object但 versioning待逐证据确认 |
| registry policy | MISSING | 需 freeze |
| CanonicalPayload | MISSING | 需 freeze |
| negative boundaries | STRONG | Decision != DesignSpec / garment description |

初始结论：`RECOVERABLE WITH FIELD NORMALIZATION`。

---

## 3.4 DesignRoute

### Source evidence

**Exact Contract**

- mandatory B01 object；
- N14 明确 `Route.decision_ref == State.decision_ref`，提供 `decision_ref` 强字段证据。

**Application / Engineering**

- `DesignRoute != RandomVariant`；
- route 表示 Decision 约束下的一条设计路线/方案机制；
- semantic chain稳定。

当前未发现完整 exact route YAML。

### Recovery strength

| 维度 | 评级 | 说明 |
|---|---|---|
| owner / mandatory surface | STRONG | N11 |
| semantic role | STRONG | controlled route, not random variant |
| field names | PARTIAL | `decision_ref` 强；route-specific fields待恢复 |
| wire types | MISSING | 需 freeze |
| requiredness | PARTIAL | decision relation强；其余待 freeze |
| reference kinds | PARTIAL | decision ref kind待 classification冻结 |
| object class | PARTIAL | canonicality强，revision policy待 freeze |
| registry policy | MISSING | 需 freeze |
| CanonicalPayload | MISSING | 需 freeze |
| negative boundaries | STRONG | Route != RandomVariant |

初始结论：`RECOVERABLE WITH ROUTE-CONTRACT DESIGN DECISIONS`。

---

## 3.5 DesignSpec

### Source evidence

**Exact Contract**

- mandatory B01 object；
- N14 明确 `Spec.route_ref == State.selected_route_ref`，提供 `route_ref` 强字段证据；
- global normalization保持 `DesignSpec != GenerationPackage`；
- global registry policy明确 `DesignSpec.artifact_eligible = false`、`DesignSpec.system_intervention_target_eligible = false`；
- `DesignSpec != ordinary SystemArtifact`。

**Application / Engineering**

语义定位：

```text
AuthoritativeStructuredIntent
!= GlobalGroundTruth
!= prompt
```

candidate baseline 仅有 sentinel，不提供 owner fields。

### Recovery strength

| 维度 | 评级 | 说明 |
|---|---|---|
| owner / mandatory surface | STRONG | N11 |
| semantic role | STRONG | authoritative structured intent |
| field names | PARTIAL | `route_ref` 强，其余 semantic spec fields待恢复 |
| wire types | MISSING | 需 freeze |
| requiredness | PARTIAL | route relation强，其余待 freeze |
| reference kinds | PARTIAL | route ref待 classification冻结 |
| object class | STRONG/PARTIAL | candidate/global registry语义支持 canonical revision方向，但仍需 owner-level正式记录 |
| registry policy | STRONG for negative flags | artifact=false, intervention-target=false 已由 global rule冻结 |
| CanonicalPayload | MISSING | P2.0 必须明确 |
| negative boundaries | STRONG | Spec != GenerationPackage != ordinary SystemArtifact |

初始结论：`RECOVERABLE / IMPORTANT GLOBAL NEGATIVE POLICIES ALREADY FROZEN`。

---

## 3.6 ReferenceIntentBinding

### Source evidence

**Exact Contract N06 / Engineering / Cross-Spec**

三层模型冻结：

```text
ReferenceAsset               [Infrastructure]
ReferenceIntentBinding       [B01]
CompiledReferenceBinding     [B03 nested value]
```

`CompiledReferenceBinding` 明确不是 standalone canonical primitive。

**Application / Engineering**

稳定 intent vocabulary 示例：

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

当前没有完整 exact field-level binding YAML。

### Recovery strength

| 维度 | 评级 | 说明 |
|---|---|---|
| owner / mandatory surface | STRONG | N11 + N06 owner boundary |
| semantic role | STRONG | reference intent layer |
| field names | MISSING | 需从职责归一化 |
| wire types | MISSING | 需 freeze |
| requiredness | MISSING | 需 freeze |
| reference kinds | PARTIAL | 必须指向 Infrastructure ReferenceAsset，但 exact persistent/authoring ref policy待 freeze |
| object class | PARTIAL | B01 canonical surface明确，具体 class待 freeze |
| registry policy | MISSING | 需 freeze |
| CanonicalPayload | MISSING | 需 freeze |
| negative boundaries | STRONG | Asset != IntentBinding != CompiledBinding |

初始结论：`MOST IMPORTANT NEW_FREEZE_DECISION AREA`。

---

## 3.7 DesignTaskBinding

### Source evidence

**Engineering + Cross-Spec**

存在明确字段级 YAML：

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

该对象用于显式连接 DI task semantics 与 ARSO task contract。

稳定 distinction：

```text
StyleBrief != ReferenceTaskSpec
```

### Recovery strength

| 维度 | 评级 | 说明 |
|---|---|---|
| owner / mandatory surface | STRONG | N11 + Engineering formal addition |
| semantic role | STRONG | DI ↔ ARSO task bridge |
| field names | STRONG | 已有 YAML |
| wire types | PARTIAL | ref target owner可判定，但 exact ref kind仍需逐项 freeze |
| requiredness | PARTIAL | YAML 未完整表达 optionality/cardinality semantics |
| reference kinds | PARTIAL | 多数 ref target明确，Exact/Object ref需冻结 |
| object class | PARTIAL | canonical surface明确，revision/fact classification需恢复 |
| registry policy | MISSING | 需 owner freeze |
| CanonicalPayload | MISSING | 需 freeze |
| negative boundaries | STRONG | Binding != ReferenceTaskSpec；不创建 ARSO shadow |

初始结论：`STRONGEST FIELD-RECOVERY CANDIDATE`。

---

# 4. Cross-Object Normalization Register

## B01-N01｜Canonical Surface Count

历史文档有 5/6/7 个 B01 object 的层次差异，但最高优先级 N11 已最终固定：

```text
B01 canonical surface = exactly 7 mandatory objects
```

状态：`DIRECT_FROZEN`。

## B01-N02｜Semantic Chain

```text
StyleBrief
→ DesignContextBinding
→ DesignDecision
→ DesignRoute
→ DesignSpec
```

多规范一致，且 N14 冻结关键 closure relations。

状态：`DIRECT_FROZEN` for chain semantics；field wiring待 ledger。

## B01-N03｜StyleBrief / ARSO Task Separation

```text
StyleBrief != ReferenceTaskSpec
```

`DesignTaskBinding` 是显式桥。

状态：`DIRECT_FROZEN`。

## B01-N04｜Reference Three-Layer Separation

```text
ReferenceAsset != ReferenceIntentBinding != CompiledReferenceBinding
```

状态：`DIRECT_FROZEN`。

## B01-N05｜DesignSpec Execution Boundary

```text
DesignSpec != GenerationPackage
DesignSpec != ordinary SystemArtifact
DesignSpec.artifact_eligible = false
DesignSpec.system_intervention_target_eligible = false
```

状态：`DIRECT_FROZEN`。

## B01-N06｜Requirement Semantics

```text
MUST / PREFER / EXPLORE / AVOID / FORBID
Constraint != Preference
```

语义稳定，但 exact nested value contract 尚未冻结。

状态：`NORMALIZED_RECOVERY REQUIRED`。

---

# 5. Initial Gap Register

| Gap | Object | 当前缺口 | P2.0 处理 |
|---|---|---|---|
| B01-G01 | StyleBrief | semantic headings → exact fields/types/requiredness | field normalization |
| B01-G02 | DesignContextBinding | 完整 field-level owner schema 缺失 | recover binding target set + refs |
| B01-G03 | DesignDecision | strategy semantics → exact grouped fields | field normalization |
| B01-G04 | DesignRoute | route-specific exact contract 缺失 | owner freeze decisions |
| B01-G05 | DesignSpec | structured intent exact fields + payload policy缺失 | owner freeze decisions |
| B01-G06 | ReferenceIntentBinding | exact fields/cardinality/ref policy缺失 | dedicated freeze design |
| B01-G07 | DesignTaskBinding | exact types/requiredness/ref kinds/classification缺失 | complete strong source recovery |
| B01-G08 | all 7 | object class + registry policy不完整 | cross-object classification audit |
| B01-G09 | all 7 | CanonicalPayload composition未冻结 | owner-specific payload ledger |

当前没有发现需要立即宣告的 `SPEC_CONFLICT`；当前问题属于 completeness / normalization gaps。

---

# 6. Recovery Order

为了降低连锁返工，field ledger 按以下顺序展开：

```text
R0  shared canonical shell + classification policy
R1  DesignTaskBinding
R2  StyleBrief
R3  ReferenceIntentBinding
R4  DesignContextBinding
R5  DesignDecision
R6  DesignRoute
R7  DesignSpec
R8  cross-object ref closure + registry matrix
R9  CanonicalPayload matrix
```

理由：

- DesignTaskBinding 的 direct field evidence 最强，可用于校准 ref/type decision style；
- StyleBrief 是核心链的 semantic root；
- ReferenceIntentBinding 是 StyleBrief 内最明显的 owner-boundary gap，应提前冻结；
- Decision/Route/Spec 按依赖顺序恢复；
- payload policy 最后统一审视，避免前面 schema 变化导致重复冻结。

---

# 7. Current Decision

```text
P2.0 SOURCE RECOVERY: STARTED
B01 object surface: 7 / 7 IDENTIFIED
Full field-level exact contract: NOT YET FROZEN
SPEC_CONFLICT: 0 discovered so far
Blocking field-level SPEC_GAP: PRESENT
P2 production implementation: NOT AUTHORIZED
```
