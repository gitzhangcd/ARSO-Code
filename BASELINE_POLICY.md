# Candidate Baseline 使用规则

## 定位

`di_contracts_v1/` 是 Phase 0 审计时发现的可执行 candidate baseline。
它保留了 F6.1 部分实现和 46 项现有测试，用于后续阶段进行差异分析和回归验证。

它的正式状态是：

```text
Executable baseline: PASS
Exact V1: FREEZE CANDIDATE
Normative authority: NO
```

## 使用限制

- `di_contracts_v1/` 不得作为规范权威。
- 不得把其中的 model、registry entry 或生成物直接认定为 `FROZEN` contract。
- 不得从该 baseline 复制或推测缺失的 B01、B02 exact schema。
- 不得把其中使用通用 `ObjectRef` 表达的 ARSO object 当作权威 ARSO type import。
- 不得因为现有 46 项测试通过而声称 CS-01 至 CS-32 或 AC-01 至 AC-18 已通过。
- 现有实现与 `specs/` 冲突时，必须以规范优先级为准，并记录 implementation drift。

## 后续迁移规则

Baseline 中的候选实现只能在对应 P0-P15 阶段按以下流程逐项吸收：

```text
读取 owner exact contract
→ 先写 conformance test 并确认失败
→ 评估 baseline 是否符合规范
→ 编写最小正式实现
→ 运行阶段测试与完整回归
→ 输出阶段审计
→ 人工 Freeze Checkpoint
```

未经上述流程，不得把 `di_contracts_v1/` 整体移动、重命名或发布为正式 package。

