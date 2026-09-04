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
P2.0: RECOVERY IMPLEMENTATION COMPLETE / FINAL VERIFICATION IN PROGRESS
P2: NOT AUTHORIZED
P3+: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

P0 与 P1 已经通过人工 Freeze Checkpoint 并合入 `main`。

P2.0 的职责是恢复并冻结 B01 field-level owner contract，不是实现 B01 Python schemas。当前 scoped authority candidate：

```text
specs/00-CODE-FREEZE/DI_B01_Exact_V1_Owner_Contract.md
```

P2.0 证据文件：

```text
B01_SOURCE_RECOVERY_MATRIX.md
B01_FIELD_DECISION_LEDGER.md
B01_CROSS_SPEC_FREEZE_AUDIT.md
```

在用户明确批准 P2.0 Freeze 之前：

```text
P2 = NOT AUTHORIZED
```

禁止新增：

```text
src/design_intelligence/contracts/b01/*.py
```

不得以“验证 owner contract”为理由提前实现 B01 production classes。

## 审计文档语言

- 审计报告、差距报告、冲突报告、实施清单、状态说明和冻结结论以中文撰写。
- 文件名、代码标识符、类型名、协议名、测试编号与状态关键词（`FROZEN`、`FREEZE CANDIDATE`、`OPEN`、`DEFERRED`、`SPEC_CONFLICT`、`SPEC_GAP`）保留英文。
- 引用英文规范原句时必须同时给出中文解释。

## 规范权威顺序

修改 canonical contract 前必须先阅读 `SPEC_AUTHORITY.md`。

当前顺序：

1A. `specs/00-CODE-FREEZE/DI_V5_Exact_V1_Schema_API_Contract_Freeze_Specification.md`
1B. `specs/00-CODE-FREEZE/DI_B01_Exact_V1_Owner_Contract.md`（仅 B01 field-level scoped authority；不得覆盖 1A）
2. `specs/01-AUTHORITY/Design-Intelligence-V5.0-Engineering-Specification-V1.0.txt`
3. `specs/01-AUTHORITY/Cross-Spec-Consistency-Freeze.txt`
4. `specs/02-UPSTREAM/ARSO-Engineering-Specification-V2.2.1.txt`
5. `specs/02-UPSTREAM/Design-Intelligence-V5.0-Application-Specification.txt`
6. `specs/02-UPSTREAM/Design-Intelligence-x-ARSO-V2.2.1-Implementation-Blueprint.txt`
7. `specs/03-RESEARCH/ARSO-Research-Specification-V2.2.1.txt`

1B 只允许填补 1A N11 明确留下的 B01 completeness gap。低优先级内容不得修改已冻结的高优先级 contract。

如果存在真实矛盾：

```text
SPEC_CONFLICT
→ stop affected path
```

如果缺少精确 contract 且没有经过 owner recovery/freeze：

```text
SPEC_GAP
→ do not guess
```

`di_contracts_v1/` 只读、只作为 executable evidence，不是 owner authority。

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
Confidence != Identifiability
ProbeRecommendation != ProbePlan
History != Memory != Knowledge
MemoryMaturity != KnowledgeMaturity

EveryLongTermFeedbackLoop
must cross an immutable version/snapshot boundary.
```

P2.0 还必须保持：

```text
Constraint != Preference
DesignRoute != RandomVariant
committed B01 refs contain no LogicalObjectRef
B01 task semantics are not System Artifacts
```

## ARSO 对象所有权

不得为以下 ARSO canonical primitive 创建 DI shadow type：

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

生产 contract 必须通过明确 integration boundary 导入/适配权威 ARSO type；临时 stub 不属于 Exact V1 canonical type。

## 引用与变更规则

- committed/runtime object 必须使用 exact persistent ref，并验证 `content_hash`。
- `LogicalObjectRef` 只能用于 authoring workflow。
- 禁止隐式 `latest/current/newest/most recent`。
- 历史 canonical object 不可变。
- 变更遵循 `Command -> validation -> new immutable object/revision -> Event -> CAS pointer update`。
- Branch head 更新必须比较 expected head；不匹配返回 `HEAD_CONFLICT`，禁止 Last-Write-Wins。

## P2.0 Freeze Gate

P2.0 只有同时满足以下条件才可以推荐 Freeze：

```text
7 / 7 B01 canonical objects covered
every owner field has type/cardinality/requiredness/ref policy
all 7 object classifications fixed
all 7 registry policies fixed
all 7 CanonicalPayload policies fixed
no unexplained field
no silent candidate promotion
8 / 8 normative checksums
no B01 production Python leakage
SPEC_CONFLICT = 0
blocking B01 field-level SPEC_GAP = 0
independent Freeze Review = PASS
user explicitly approves P2.0 Freeze
```

在这之前 P2 不得启动。

## Exact V1 状态边界

```text
FROZEN:
  已经通过人工 Freeze Checkpoint 的架构/阶段 contract

FREEZE CANDIDATE:
  尚未完成全部 Exact V1 release gates 的 schema/API contract

OPEN:
  algorithms/models/thresholds/physical DB/storage/event bus

DEFERRED:
  production auto-activation/global ontology+grammar autonomous evolution/
  meta-learning/cross-domain transfer/continuous production self-modification
```

不得把 `OPEN` 当作 frozen contract；不得实现 `DEFERRED` 能力。

只有 CS-01–CS-32、AC-01–AC-18 全部通过且无 unresolved `SPEC_CONFLICT`，Exact V1 才能声明 `FROZEN`。
