# Exact V1 规范权威说明

审计日期：2026-09-04  
仓库：ARSO-Code  
阶段：规范摄取、冻结治理与 Exact V1 分阶段实现  
结论：Phase 0、Phase 1、P0、P1 已冻结；P2.0 已完成 B01 owner-contract recovery，正在最终验证；P2 尚未授权

## 规范输入路径说明

`specs/` 是唯一规范入口。

Phase 1 冻结时存在 7 份原始 authority/upstream/research source。P2.0 新增第 8 份 scoped normative contract：

```text
specs/00-CODE-FREEZE/DI_B01_Exact_V1_Owner_Contract.md
```

因此 `specs/SPEC_SOURCE_CHECKSUMS.sha256` 从本阶段起必须验证 `8 / 8` 文件：原 7 份来源内容保持原 checksum，不允许因为增加 B01 owner contract 而重写历史来源。

## 规范权威顺序

| 优先级 | 仓库内规范 | 文档身份与状态 | 规范职责 |
|---:|---|---|---|
| 1A | `specs/00-CODE-FREEZE/DI_V5_Exact_V1_Schema_API_Contract_Freeze_Specification.md` | `DI-V5-EXACT-CONTRACT`、`V1.0-FC1`、`FREEZE CANDIDATE` | 全局 Code-Level Authority；冻结 F0-F6 normalization、cross-domain invariants、CS/AC release gates。 |
| 1B | `specs/00-CODE-FREEZE/DI_B01_Exact_V1_Owner_Contract.md` | `DI-B01-EXACT-CONTRACT`、`V1.0-FC1`、`FREEZE CANDIDATE` | 仅补齐 N11 明确留下的 B01 field-level owner contract；不得覆盖 1A。 |
| 2 | `specs/01-AUTHORITY/Design-Intelligence-V5.0-Engineering-Specification-V1.0.txt` | `DI-V5-ENG`、`V1.0`；Architecture `FROZEN`、exact schema `FREEZE CANDIDATE` | 工程、运行时、对象所有权与边界。 |
| 3 | `specs/01-AUTHORITY/Cross-Spec-Consistency-Freeze.txt` | DI-E01-E08 Cross-Spec 一致性权威 | normalization 与跨规范冻结边界。 |
| 4 | `specs/02-UPSTREAM/ARSO-Engineering-Specification-V2.2.1.txt` | ARSO Engineering V2.2.1 | 通用 ARSO primitive 与集成边界 canonical owner。 |
| 5 | `specs/02-UPSTREAM/Design-Intelligence-V5.0-Application-Specification.txt` | `DI-V5-AS`、5.0 | 产品语义与 B01-B08 应用职责。 |
| 6 | `specs/02-UPSTREAM/Design-Intelligence-x-ARSO-V2.2.1-Implementation-Blueprint.txt` | Blueprint V1.0 | 集成蓝图与低优先级实施背景。 |
| 7 | `specs/03-RESEARCH/ARSO-Research-Specification-V2.2.1.txt` | Research V2.2.1 | 科学依据与研究主张边界，不是代码级 schema 权威。 |

规则：

```text
1B MUST NOT override 1A.
2+ MUST NOT override 1A/1B where the scoped contract is frozen.
```

## 规范解析规则

1. 先查 1A 的全局 Exact Contract。
2. 对 B01 field-level schema，再查 1B；1B 只能填补 N11 completeness gap。
3. 若 1A/1B 已给出 exact 定义，直接遵守，不重新解释。
4. 仍未定义的区域按 2→7 顺序恢复背景/证据。
5. 缺少 exact contract 时记录 `SPEC_GAP`；不得从 candidate baseline 猜测。
6. 无法同时满足的冻结要求记录 `SPEC_CONFLICT` 并停止该路径。
7. `OPEN` / `DEFERRED` 不因实现便利自动升级为 contract。

## 冻结状态总表

| 状态 | 当前范围 |
|---|---|
| `FROZEN` | Architecture；primitive/capability ownership；标准化 F0-F6 语义；P0 nominal identity/base policy；P1 exact refs/RFC8785 hash/registry foundation。 |
| `FREEZE CANDIDATE` | 全局 Exact V1；`DI-B01-EXACT-CONTRACT` 在用户 P2.0 Freeze 前保持 candidate；ARSO exact integration；完整 command/event/protocol；完整 registry inventory；resolver；CAS；snapshot firewalls。 |
| `OPEN` | 物理数据库 schema；存储引擎；事件总线；算法、模型、阈值；检索/排序；executor/model 选择；实证结论。 |
| `DEFERRED` | 自动生产激活与部署；全局语义自主演化；meta-learning；cross-domain/cross-enterprise transfer；持续生产自修改。 |

## 当前阶段

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

P0 决策：`P0_FREEZE_DECISION.md`。  
P1 决策：`P1_FREEZE_DECISION.md`。

P2.0 recovery evidence：

```text
B01_SOURCE_RECOVERY_MATRIX.md
B01_FIELD_DECISION_LEDGER.md
B01_CROSS_SPEC_FREEZE_AUDIT.md
specs/00-CODE-FREEZE/DI_B01_Exact_V1_Owner_Contract.md
```

## P2 授权门禁

P2 目标：`Full B01 Exact Schemas`。

P2.0 candidate 当前已经将 `GAP-001 / AC-01` 的 B01 field-level owner gap 收敛为：

```text
7 / 7 objects covered
SPEC_CONFLICT = 0
blocking B01 field-level SPEC_GAP = 0
```

但这些结论必须经过最终 automated verification + independent Freeze Review + 用户明确 P2.0 Freeze 后，才允许：

```text
P2 = AUTHORIZED
```

在此之前不得写 `src/design_intelligence/contracts/b01/*.py`。

## Exact V1 最终发布规则

只有 mandatory schemas、authoritative ARSO imports、完整 Command/Event/Protocol、semantic resolver、CAS、snapshot firewalls、CS-01–CS-32、AC-01–AC-18 全部通过且不存在未解决 `SPEC_CONFLICT` 时，Exact V1 才能从 `FREEZE CANDIDATE` 升级为 `FROZEN`。
