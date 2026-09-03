# ARSOFashion 仓库协作规则

## 本地技能触发规则

- 当用户输入 `/graphify` 时，必须先调用 `graphify` 技能，再执行其他操作。

## 项目说明

本项目是 Design Intelligence V5.0 的 ARSO V2.2.1 Reference Application。

这是一个规范驱动的实现项目。Phase 0 规范摄取与仓库一致性审计已经完成并通过人工评审。
Phase 1 Contract Repository Skeleton 已完成本地验证，正在等待人工 Freeze Checkpoint。
在用户明确批准进入 P0 之前，不得实现 nominal type、base contract 或其他生产 contract。

## 审计文档语言

- 后续所有审计报告、差距报告、冲突报告、实施清单、状态说明和冻结结论均以中文撰写和展示。
- 文件名、代码标识符、类型名、协议名、测试编号以及规范中的状态关键词（如 `FROZEN`、`FREEZE CANDIDATE`、`OPEN`、`DEFERRED`、`SPEC_CONFLICT`、`SPEC_GAP`）保留英文原文。
- 必须引用英文规范原句时，同时给出简明中文解释，不能仅粘贴英文内容。
- 表格标题、图示说明、结论和行动建议必须使用中文，确保无需阅读英文段落也能理解审计结果。

## 规范权威顺序

修改 canonical contract 之前，必须先阅读 `SPEC_AUTHORITY.md` 以及
`specs/` 下对应的规范。权威顺序如下：

1. `specs/00-CODE-FREEZE/DI_V5_Exact_V1_Schema_API_Contract_Freeze_Specification.md`
2. `specs/01-AUTHORITY/Design-Intelligence-V5.0-Engineering-Specification-V1.0.txt`
3. `specs/01-AUTHORITY/Cross-Spec-Consistency-Freeze.txt`
4. `specs/02-UPSTREAM/ARSO-Engineering-Specification-V2.2.1.txt`
5. `specs/02-UPSTREAM/Design-Intelligence-V5.0-Application-Specification.txt`
6. `specs/02-UPSTREAM/Design-Intelligence-x-ARSO-V2.2.1-Implementation-Blueprint.txt`
7. `specs/03-RESEARCH/ARSO-Research-Specification-V2.2.1.txt`

高优先级规范覆盖低优先级规范。不得因为框架惯例、持久化设计、开发便利、
个人偏好或低优先级文档而修改 `FROZEN` contract。

如果仍存在真实矛盾，必须输出 `SPEC_CONFLICT` 并停止对应实现路径。
如果缺少精确字段级 contract，必须输出 `SPEC_GAP`，不得自行猜测。

## 已冻结的架构不变量

```text
OneCanonicalObject => OnePrimitiveOwner

TaskState != SystemState != KnowledgeState != ReviewState

Evaluation != Evidence != Diagnosis != Action != Intervention

DesignEdit != GenerationEdit != SystemIntervention != KnowledgePromotion

StyleBrief != ReferenceTaskSpec
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

生产 contract 必须通过明确的集成边界导入或适配权威 ARSO type。
临时 stub 不属于 Exact V1 canonical type。

## 引用与变更规则

- 已提交对象和运行时对象必须使用 exact version，并验证 `content_hash`。
- `LogicalObjectRef` 只能用于 authoring workflow。
- 禁止隐式解析 `latest`、`current`、`newest` 或 `most recent`。
- 历史 canonical object 必须不可变。
- 变更必须遵循：`Command -> validation -> new immutable object/revision -> Event -> CAS pointer update`。
- Branch head 更新必须比较 expected head；冲突时返回 `HEAD_CONFLICT`，禁止 Last-Write-Wins。

## 状态边界

```text
FROZEN:
  架构、所有权、边界、标准化后的 F0-F6 语义

FREEZE CANDIDATE:
  Exact V1 可执行 schema/API 集合

OPEN:
  算法、模型、阈值、物理数据库设计、存储与事件总线实现

DEFERRED:
  自动生产部署、全局 ontology/grammar 自主演化、meta-learning、
  cross-domain transfer、持续生产自修改
```

不得把 `OPEN` 选项当作已冻结 contract 实现。不得实现 `DEFERRED` 能力。

## 测试与范围规则

如果相关 conformance test 尚不存在，则对应 schema 不得视为完成。
只有 CS-01 至 CS-32、AC-01 至 AC-18 全部通过且不存在未解决的
`SPEC_CONFLICT`，Exact V1 才能声明为 `FROZEN`。

在 Exact V1 contract layer 冻结之前，不得开发 UI、LLM 集成、图像生成集成、
vector database、自主优化器或生产部署能力。
