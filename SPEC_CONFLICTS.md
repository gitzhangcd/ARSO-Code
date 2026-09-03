# Phase 0 规范冲突与歧义报告

审计日期：2026-09-03  
未解决的真实 `SPEC_CONFLICT` 数量：**0**  
当前阻断性的 `SPEC_GAP` / 输入歧义数量：**4**  
已解决的路径歧义数量：**1**

## 审计结论

优先级 1 的 Exact Contract 明确指出，F0-F6 不存在需要推翻架构的冲突。
本轮审计按照既定规范优先级解析后，没有发现两项无法同时满足的冻结要求。

Implementation deviation 不属于 specification conflict。相关问题已经记录在
`CONTRACT_GAP_REPORT.md`，不得用当前实现反向修改规范。

## 未解决的歧义与缺口

| ID | 类型 | 发现 | 影响 | 必须采取的处理 |
|---|---|---|---|---|
| A-01 | RESOLVED | 原审计发现任务指定路径与仓库实际路径不同。 | 规范现已统一迁移到 `specs/`，该歧义不再阻断。 | 通过 `SPEC_SOURCE_CHECKSUMS.sha256` 持续验证规范源。 |
| A-02 | 文档身份歧义 | 优先级 3 的 `Cross-Spec-Consistency-Freeze.txt` 内部声明了与优先级 2 相同的 `DI-V5-ENG` 标题、ID 和版本，差异主要是格式及残留引用标记。 | 无法独立验证预期的 Cross-Spec 文档身份。 | 最终 contract freeze 前，补充或确认正确的优先级 3 规范源。 |
| A-03 | SPEC_GAP | 规范引用的 B01/B02 owner exact field-level contract 文件缺失。 | AC-01/AC-02 及所有依赖工作被阻断；低优先级叙述性规范不能安全补全字段。 | 增加权威 B01/B02 exact contract，或明确冻结替代规范。 |
| A-04 | SPEC_GAP | 优先级 1 要求完整的 command/event inventory，但有意没有给出完整枚举。 | 如果自行设计，则 AC-04/AC-05 必然依赖猜测。 | 实施前产出并由 owner 评审、冻结完整 inventory。 |
| A-05 | SPEC_GAP | N09 已冻结 RFC 8785 和部分排除字段，但没有明确每种对象 CanonicalPayload 中所有稳定 identity/parentage field 的处理方式。 | 当前代码排除的字段多于规范明确列出的最小集合，hash identity 可能发生漂移。 | AC-13 前冻结按 class 划分的 payload inclusion/exclusion fixture。 |

## 被高优先级规范覆盖的低优先级陈述

以下内容不属于未解决冲突，因为既定优先级已经给出确定的处理结果。

| 主题 | 低优先级陈述 | 高优先级处理结果 |
|---|---|---|
| Evaluation primitive 所有权 | Application Specification 的 ownership table 把 `EvaluationRecord` 和 `MeasurementRecord` 列在 B04 下。 | 优先级 1 的 N10 和 7.5 节规定 ObjectiveSpec、MeasurementSpec、EvaluatorBinding、EvaluationRecord 由 ARSO canonical owner 持有。DI-B04 只拥有 fashion-specific definition/extension，禁止 DI shadow。 |
| Diagnosis primitive 所有权 | Application Specification 的 ownership table 把 EvidenceBundle、DiagnosticBelief、DiagnosticHypothesis 和 ProbePlan 列在 B05 下。 | 优先级 1 的 N10 和 7.6 节规定通用 Evidence、Diagnosis、Hypothesis、Identifiability、ProbePlan、ProbeResult 均归 ARSO。DI-B05 只拥有 policy、extension 和 ProbeRecommendation。 |
| Intervention primitive 所有权 | Application Specification 的 ownership table 把 ActionDecision 和 validation result 概念列在 B06 下。 | 优先级 1 的 N02、N10 和 7.7 节规定 ActionDecision、InterventionPlan/Result、ValidationPlan/Result、BudgetReservation 归 ARSO；DI InterventionTransaction 只能是 operational control state。 |
| KnowledgeSnapshot validity closure | 早期 F6.1 baseline/report 把 `knowledge_validity_refs` 视为未解决 candidate。 | 优先级 1 的 N07 规定该字段不是 Exact V1 mandatory field；当被引用 revision 已拥有 validity link 时，不得复制 closure。 |
| Memory lifecycle | 早期 baseline/report 把 lifecycle overlap 视为未解决。 | 优先级 1 的 N05 已冻结单一 MemoryMaturity lifecycle，并禁止第二个通用 `lifecycle_status`。 |
| Knowledge artifact eligibility | 当前 manifest 把 BrandDNAProfile、RetentionPolicy、KnowledgeAccessPolicy 标记为 artifact eligible。 | 优先级 1 的 N08 把 `artifact_eligible` 定义为影响 ARSO 行为的 System Artifact eligibility，并规定这些 knowledge object 默认不是直接 System Artifact target。这属于 implementation drift，不属于 spec conflict。 |

## 必须停止的实现路径

在对应权威输入就绪前，以下工作必须以 `SPEC_GAP` 停止：

1. 新增或修改 B01/B02 exact field。
2. 自行设计缺失的 command 或 event type/field。
3. 把临时 DI-shaped ARSO stub 当作 canonical ARSO primitive。
4. 在缺少按 class 划分的 payload fixture 和 RFC 8785 cross-language evidence 时，
   声明 canonical hash 已冻结。
5. 在所有 CS/AC gate 通过之前，把 Exact V1 提升为 `FROZEN`。

## 当前冲突状态

```text
SPEC_CONFLICT: 当前没有未解决项
SPEC_GAP: 存在，并且阻断后续工作
IMPLEMENTATION_DRIFT: 存在，并且阻断冻结
PHASE_1_AUTHORIZED: no
```
