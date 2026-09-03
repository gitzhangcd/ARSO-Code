# Phase 0 规范权威说明

审计日期：2026-09-04  
仓库：ARSOFashion  
阶段：规范摄取、冻结治理与 Exact V1 分阶段实现  
结论：权威链已经建立；Phase 0、Phase 1、P0、P1 均已通过评审/冻结；P2 尚未授权

## 规范输入路径说明

规范已经统一迁移到 `specs/`。该目录是唯一规范入口，包含预期的 7 份规范；原目录路径不再使用。Phase 1 以来持续使用 SHA-256 manifest 验证规范源没有发生意外漂移。

## 规范权威顺序

| 优先级 | 仓库内规范 | 文档身份与状态 | 规范职责 |
|---:|---|---|---|
| 1 | `specs/00-CODE-FREEZE/DI_V5_Exact_V1_Schema_API_Contract_Freeze_Specification.md` | `DI-V5-EXACT-CONTRACT`、`V1.0-FC1`、`FREEZE CANDIDATE` | 第一层代码级权威；冻结标准化后的 F0-F6 语义，并定义 CS/AC 发布门禁。 |
| 2 | `specs/01-AUTHORITY/Design-Intelligence-V5.0-Engineering-Specification-V1.0.txt` | `DI-V5-ENG`、`V1.0`；架构为 `FROZEN`，exact schema 为 `FREEZE CANDIDATE` | 统一的工程、运行时和对象所有权 contract。 |
| 3 | `specs/01-AUTHORITY/Cross-Spec-Consistency-Freeze.txt` | DI-E01-E08 Cross-Spec 一致性权威 | 一致性 normalization 与冻结边界。 |
| 4 | `specs/02-UPSTREAM/ARSO-Engineering-Specification-V2.2.1.txt` | ARSO Engineering V2.2.1 | 通用 ARSO primitive 及集成边界 canonical owner。 |
| 5 | `specs/02-UPSTREAM/Design-Intelligence-V5.0-Application-Specification.txt` | `DI-V5-AS`、5.0 | 产品语义及 B01-B08 应用职责。 |
| 6 | `specs/02-UPSTREAM/Design-Intelligence-x-ARSO-V2.2.1-Implementation-Blueprint.txt` | Blueprint V1.0 | 集成蓝图与低优先级实施背景。 |
| 7 | `specs/03-RESEARCH/ARSO-Research-Specification-V2.2.1.txt` | Research V2.2.1 | 科学依据与研究主张边界，不是代码级 schema 权威。 |

高优先级覆盖低优先级。低优先级内容不得改变已冻结的高优先级 contract。

## 规范解析规则

1. 先在优先级 1 的 Exact Contract 中定位对应对象或不变量。
2. 若优先级 1 已给出 exact 定义，直接遵守，不重新解释。
3. 若只冻结语义/所有权，再按优先级 2 至 7 依次查找。
4. 低优先级只能补充高优先级未定义的背景。
5. 仍缺少字段级 exact schema 时，记录 `SPEC_GAP` 并停止对应实现。
6. 冻结要求无法同时满足时，记录 `SPEC_CONFLICT` 并停止对应实现。
7. `OPEN` / `DEFERRED` 不因上下文暗示自动变成实现要求。

## 冻结状态总表

| 状态 | 当前范围 |
|---|---|
| `FROZEN` | 架构；primitive/capability ownership；标准化 F0-F6 语义；P0 nominal identity/base policy；P1 exact refs、RFC 8785 hash foundation 与 registry foundation。 |
| `FREEZE CANDIDATE` | 完整 Exact V1 schema/API 集合；ARSO exact integration；完整 command/event/protocol；完整 registry inventory；semantic resolver；CAS；snapshot firewalls。 |
| `OPEN` | 物理数据库 schema；存储引擎；事件总线；算法、模型、阈值；检索与排序；executor/model 选择；实证结论。 |
| `DEFERRED` | 自动生产激活与部署；全局语义自主演化；meta-learning；cross-domain/cross-enterprise transfer；持续生产自修改。 |

## 当前已冻结阶段

```text
Phase 0: COMPLETE / REVIEWED / APPROVED
Phase 1: COMPLETE / VERIFIED / FROZEN
P0: COMPLETE / REVIEWED / FROZEN
P1: COMPLETE / REVIEWED / FROZEN
P2: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

P0 决策记录：`P0_FREEZE_DECISION.md`。
P1 决策记录：`P1_FREEZE_DECISION.md`。

## P2 前置门禁

P2 目标是 `Full B01 Exact Schemas`。优先级 1 规范已经明确指出：B01 的 primitive ownership 与 semantic role 已冻结，但当前仓库中的 F6.1 executable baseline **不包含完整 B01 field-level exact schemas**；不得从低优先级叙述或 candidate baseline 猜测缺失字段。

因此 P1 merge 后，P2 是否授权必须先判断：

```text
B01 owner exact contract available and sufficiently complete?
```

若答案为否：

```text
P2 implementation = BLOCKED
允许先进入 B01 Contract Recovery / Spec Freeze
```

若答案为是：

```text
P2 implementation may be authorized
```

无论哪种情况，在明确授权前不得写 B01 production models。

## Exact V1 最终发布规则

只有当 mandatory schemas、authoritative ARSO imports、完整 Command/Event/Protocol、semantic resolver、CAS、snapshot firewalls、CS-01–CS-32、AC-01–AC-18 全部通过且不存在未解决 `SPEC_CONFLICT` 时，Exact V1 才能从 `FREEZE CANDIDATE` 升级为 `FROZEN`。
