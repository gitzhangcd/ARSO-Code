# ARSO-Code 仓库协作规则

## 本地技能触发规则

- 当用户输入 `/graphify` 时，必须先调用 `graphify` 技能，再执行其他操作。

## 项目状态

```text
Phase 0: COMPLETE / REVIEWED / APPROVED
Phase 1: COMPLETE / VERIFIED / FROZEN
P0: FROZEN
P1: FROZEN
P2.0A: FROZEN AS INCLUDED REMEDIATION
P2.0: FROZEN BY USER DECISION / MAIN PUBLICATION PENDING
P2: AUTHORIZATION APPROVED / EFFECTIVE AFTER VERIFIED MAIN PUBLICATION
P3+: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

P2.0 Freeze 记录：`P2_0_FREEZE_DECISION.md`。

## 规范权威顺序

修改 canonical contract 前必须先阅读 `SPEC_AUTHORITY.md`。

当前顺序：

1A. `specs/00-CODE-FREEZE/DI_V5_Exact_V1_Schema_API_Contract_Freeze_Specification.md`
1B. `specs/00-CODE-FREEZE/DI_Shared_Canonical_Shell_Exact_V1_Contract.md`
1C. `specs/00-CODE-FREEZE/DI_B01_Exact_V1_Owner_Contract.md`
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
2+ MUST NOT override frozen higher-priority scope.
```

`di_contracts_v1/` 只读，只作为 executable evidence，不是 normative authority。

## Frozen architecture invariants

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

P2.0/P2.0A 不改变 P0/P1 已冻结的 ObjectId/LogicalId/SchemaVersion/ObjectType、Exact refs、hash engine 或 registry foundation。

## ARSO ownership boundary

不得为以下 ARSO canonical primitives 创建 DI shadow type：

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

## Reference / mutation rules

- committed/runtime object 使用 exact persistent ref 并验证 `content_hash`。
- `LogicalObjectRef` 只能用于 authoring workflow。
- 禁止隐式 latest/current/newest。
- 历史 canonical object 不可变。
- 变更遵循 `Command -> validation -> new immutable object/revision -> Event -> CAS pointer update`。
- Branch head 更新需要 expected head/CAS；冲突返回 `HEAD_CONFLICT`。

## P2.0 frozen checkpoint

Frozen scope：

```text
7 / 7 B01 canonical object owner contracts
B01 owner-field wire shape / refs / requiredness / cardinality
B01 object classification / registry policy
B01 CanonicalPayload policy
B01 semantic closure and negative boundaries
shared canonical shell support contracts required by B01
```

Evidence：

```text
B01 owner-field SPEC_GAP = 0
shared-core blocking SPEC_GAP = 0
SC01-SC04 = CLOSED
SPEC_CONFLICT = 0
P2.0A independent review: Critical=0 / Important=0 / Minor=0
P2 contract-level implementability = PASS
9 / 9 normative checksums
```

`P2_0_FREEZE_DECISION.md` 是本 checkpoint 的人工 Freeze 决策记录。

## P2 activation gate

用户已经批准：

```text
P2｜Full B01 Exact Schemas
```

但在本 branch 上仍不得开始 production implementation。P2 只有在：

```text
freeze-decision exact head fresh verification PASS
-> PR #4 merged to main with expected-head protection
-> resulting main checkpoint fresh verification PASS
```

之后才正式成为：

```text
P2: AUTHORIZED
```

P2 生效后必须在独立 P2 branch 上按 Superpowers planning + TDD 执行；`main` 继续代表最近的人类批准 frozen checkpoint。

## Exact V1 状态边界

```text
FROZEN: human-approved scoped checkpoint
FREEZE CANDIDATE: 全局 Exact V1 尚未完成全部 release gates
OPEN: algorithms/models/thresholds/storage/event bus 等未冻结选择
DEFERRED: production auto-activation/global semantic autonomous evolution/meta-learning/cross-domain transfer
```

只有 CS-01–CS-32、AC-01–AC-18 全部通过且无 unresolved `SPEC_CONFLICT`，Exact V1 才能声明全局 `FROZEN`。
