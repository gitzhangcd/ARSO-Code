# ARSO-Code 仓库协作规则

## 本地技能触发规则

- 当用户输入 `/graphify` 时，必须先调用 `graphify` 技能，再执行其他操作。

## 项目说明

本项目是 Design Intelligence V5.0 的 ARSO V2.2.1 Reference Application，是一个规范驱动的实现项目。

```text
Phase 0: COMPLETE / REVIEWED / APPROVED
Phase 1: COMPLETE / VERIFIED / FROZEN
P0: FROZEN
P1: FROZEN
P2.0A: RECOVERY PASS / INDEPENDENT REVIEW PASS / NOT FROZEN
P2.0: B01 RECOVERY PASS / RE-REVIEW PASS / READY FOR USER FREEZE DECISION
P2: NOT AUTHORIZED
P3+: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

P0 与 P1 已通过人工 Freeze Checkpoint 并合入 `main`。

P2.0 已恢复 B01 field-level owner contract；P2.0A 已完成 shared canonical-shell remediation candidate：

```text
specs/00-CODE-FREEZE/DI_Shared_Canonical_Shell_Exact_V1_Contract.md
```

P2.0A scope：

```text
ActorId
ActorType
ActorRef
TenantId
TenantScopeType
TenantScope
Provenance
ObjectRevision
CanonicalObject structural base
CanonicalRevision structural base
ImmutableFact structural base
UTC canonical timestamp normalization
```

Independent Review：

```text
SC01 ActorRef       CLOSED
SC02 TenantScope    CLOSED
SC03 Provenance     CLOSED
SC04 ObjectRevision CLOSED
Critical = 0
Important = 0
Minor = 0
shared-core SPEC_CONFLICT = 0
blocking shared-core field SPEC_GAP = 0
```

P2.0 re-review 已确认：

```text
7 / 7 B01 objects covered
B01 owner-field SPEC_GAP = 0
shared-core blocking SPEC_GAP = 0
P2 contract-level implementability = PASS
P2.0 = READY FOR USER FREEZE DECISION
```

但：

```text
P2.0 != FROZEN
P2 = NOT AUTHORIZED
```

在用户明确批准 P2.0 Freeze 前，不得新增 `src/design_intelligence/contracts/b01/*.py`，也不得把 P2.0A candidate 实现成 production core Python types。

## 审计文档语言

- 审计报告、差距报告、冲突报告、实施清单、状态说明和冻结结论以中文撰写。
- 文件名、代码标识符、类型名、协议名、测试编号与状态关键词保留英文。
- 引用英文规范时给出中文解释。

## 规范权威顺序

修改 canonical contract 前必须先阅读 `SPEC_AUTHORITY.md`。

当前顺序：

1A. `specs/00-CODE-FREEZE/DI_V5_Exact_V1_Schema_API_Contract_Freeze_Specification.md`
1B. `specs/00-CODE-FREEZE/DI_Shared_Canonical_Shell_Exact_V1_Contract.md`（shared support/nested + structural shell scoped `FREEZE CANDIDATE`）
1C. `specs/00-CODE-FREEZE/DI_B01_Exact_V1_Owner_Contract.md`（B01 field-level scoped `FREEZE CANDIDATE`）
2. `specs/01-AUTHORITY/Design-Intelligence-V5.0-Engineering-Specification-V1.0.txt`
3. `specs/01-AUTHORITY/Cross-Spec-Consistency-Freeze.txt`
4. `specs/02-UPSTREAM/ARSO-Engineering-Specification-V2.2.1.txt`
5. `specs/02-UPSTREAM/Design-Intelligence-V5.0-Application-Specification.txt`
6. `specs/02-UPSTREAM/Design-Intelligence-x-ARSO-V2.2.1-Implementation-Blueprint.txt`
7. `specs/03-RESEARCH/ARSO-Research-Specification-V2.2.1.txt`

Rules：

```text
1B MUST NOT override 1A.
1C MUST consume 1B and MUST NOT redefine shared support internals.
2+ MUST NOT override frozen 1A/1B/1C scope.
```

如果存在真实矛盾：

```text
SPEC_CONFLICT -> stop affected path
```

如果缺少精确 contract：

```text
SPEC_GAP -> do not guess
```

`di_contracts_v1/` 只读、只作为 executable evidence，不是 authority。

## Shared canonical shell invariants

```text
ActorId != ObjectId != LogicalId != TenantId
ActorType = open typed vocabulary
TenantScopeType = GLOBAL | TENANT
GLOBAL != public/permissionless

Provenance.source_refs = CanonicalRef only
LogicalObjectRef forbidden in committed provenance
Provenance.command_ref:ObjectRef = forbidden
Provenance.run_ref:ObjectRef = deferred

ObjectRevision = integer >= 1
revision = server-assigned ordering metadata
revision != identity/schema version/concurrency token
parentage = parent_refs

support/nested/structural types != canonical domain primitives
```

P2.0A MUST NOT change P0/P1 frozen contracts for ObjectId/LogicalId/SchemaVersion/ObjectType, Exact refs, hash engine or registry foundation。

## 已冻结的架构不变量

```text
OneCanonicalObject => OnePrimitiveOwner
TaskState != SystemState != KnowledgeState != ReviewState
Evaluation != Evidence != Diagnosis != Action != Intervention
DesignEdit != GenerationEdit != SystemIntervention != KnowledgePromotion

StyleBrief != ReferenceTaskSpec
DesignDecision != DesignSpec
DesignSpec != GenerationPackage
DesignSpec != ordinary SystemArtifact
ReferenceAsset != ReferenceIntentBinding != CompiledReferenceBinding
Constraint != Preference
DesignRoute != RandomVariant

EveryLongTermFeedbackLoop
must cross an immutable version/snapshot boundary.
```

## ARSO 对象所有权

不得为下列 ARSO canonical primitives 创建 DI shadow type：

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

P2.0A 尤其不得通过 `Provenance.run_ref` 提前决定 ARSO RunRecord 的 object class/ref kind。

## 引用与变更规则

- committed/runtime object 使用 exact persistent ref 并验证 `content_hash`。
- `LogicalObjectRef` 只能用于 authoring workflow。
- 禁止隐式 latest/current/newest。
- 历史 canonical object 不可变。
- 变更遵循 `Command -> validation -> new immutable object/revision -> Event -> CAS pointer update`。
- Branch head 更新需要 expected head/CAS；冲突返回 `HEAD_CONFLICT`。

## P2.0 Freeze Gate

P2.0 已满足技术 review 条件，但仍需人工 Freeze：

```text
7 / 7 B01 canonical objects covered
B01 owner-field SPEC_GAP = 0
SC01-SC04 shared shell closed
shared-core SPEC_GAP = 0
all 7 object classifications fixed
all 7 registry policies fixed
all required CanonicalPayload policies fixed
9 / 9 normative checksums
no original-source drift
no candidate-baseline drift
no production core/B01 leakage
P0/P1 regression PASS
SPEC_CONFLICT = 0
P2.0A independent review PASS
P2.0 final independent review PASS
```

最后仍需要：

```text
user explicitly approves P2.0 Freeze
```

批准后按顺序：

```text
merge PR #5 into p2-0-b01-contract-recovery
-> fresh verification of PR #4 exact combined head
-> record P2.0 freeze decision
-> merge PR #4 to main
-> verify main
-> only then explicitly authorize P2
```

## Exact V1 状态边界

```text
FROZEN: human-approved checkpoint
FREEZE CANDIDATE: schema/API contract still awaiting complete release gates
OPEN: algorithms/models/thresholds/storage/event bus and other non-frozen choices
DEFERRED: production auto-activation/global semantic autonomous evolution/meta-learning/cross-domain transfer
```

只有 CS-01–CS-32、AC-01–AC-18 全部通过且无 unresolved `SPEC_CONFLICT`，Exact V1 才能声明 `FROZEN`。
