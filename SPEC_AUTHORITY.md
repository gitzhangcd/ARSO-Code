# Exact V1 规范权威说明

审计日期：2026-09-04  
仓库：ARSO-Code  
阶段：规范摄取、冻结治理与 Exact V1 分阶段实现  
结论：Phase 0、Phase 1、P0、P1 已冻结；B01 owner-field recovery 已完成，但 P2.0 Freeze 被 shared canonical-shell `SPEC_GAP` 阻断；P2 尚未授权

## 规范输入路径说明

`specs/` 是唯一规范入口。

Phase 1 冻结时存在 7 份原始 authority/upstream/research source。P2.0 新增第 8 份 scoped normative candidate：

```text
specs/00-CODE-FREEZE/DI_B01_Exact_V1_Owner_Contract.md
```

`specs/SPEC_SOURCE_CHECKSUMS.sha256` 当前验证 `8 / 8` 文件；原 7 份来源 checksum 保持不变。

## 规范权威顺序

| 优先级 | 仓库内规范 | 文档身份与状态 | 规范职责 |
|---:|---|---|---|
| 1A | `specs/00-CODE-FREEZE/DI_V5_Exact_V1_Schema_API_Contract_Freeze_Specification.md` | `DI-V5-EXACT-CONTRACT`、`V1.0-FC1`、`FREEZE CANDIDATE` | 全局 Code-Level Authority；冻结 F0-F6 normalization、cross-domain invariants、CS/AC release gates。 |
| 1B | `specs/00-CODE-FREEZE/DI_B01_Exact_V1_Owner_Contract.md` | `DI-B01-EXACT-CONTRACT`、`V1.0-FC1`、`FREEZE CANDIDATE` | 仅补齐 N11 的 B01 field-level owner contract；不得覆盖 1A，也不拥有 shared-core support type internals。 |
| 2 | `specs/01-AUTHORITY/Design-Intelligence-V5.0-Engineering-Specification-V1.0.txt` | `DI-V5-ENG`、`V1.0`；Architecture `FROZEN`、exact schema `FREEZE CANDIDATE` | 工程、运行时、对象所有权与边界。 |
| 3 | `specs/01-AUTHORITY/Cross-Spec-Consistency-Freeze.txt` | DI-E01-E08 Cross-Spec 一致性权威 | normalization 与跨规范冻结边界。 |
| 4 | `specs/02-UPSTREAM/ARSO-Engineering-Specification-V2.2.1.txt` | ARSO Engineering V2.2.1 | 通用 ARSO primitive 与集成边界 canonical owner。 |
| 5 | `specs/02-UPSTREAM/Design-Intelligence-V5.0-Application-Specification.txt` | `DI-V5-AS`、5.0 | 产品语义与 B01-B08 应用职责。 |
| 6 | `specs/02-UPSTREAM/Design-Intelligence-x-ARSO-V2.2.1-Implementation-Blueprint.txt` | Blueprint V1.0 | 集成蓝图与低优先级实施背景。 |
| 7 | `specs/03-RESEARCH/ARSO-Research-Specification-V2.2.1.txt` | Research V2.2.1 | 科学依据与研究主张边界。 |

规则：

```text
1B MUST NOT override 1A.
1B MUST NOT fabricate global/shared-core support contracts outside B01 ownership.
2+ MUST NOT override 1A/1B where frozen.
```

## 规范解析规则

1. 先查 1A global Exact Contract。
2. B01 field-level schema 查 1B；1B 只填补 N11 completeness gap。
3. 若 1A/1B 已给出 exact 定义，直接遵守。
4. 未定义区域按 2→7 恢复证据。
5. shared-core type 若只有 field role、没有 exact internal contract，也属于 `SPEC_GAP`；不得从 candidate baseline 复制。
6. 无法同时满足的 frozen requirement → `SPEC_CONFLICT`。
7. `OPEN` / `DEFERRED` 不因实现便利自动升级为 contract。

## 冻结状态总表

| 状态 | 当前范围 |
|---|---|
| `FROZEN` | Architecture；primitive/capability ownership；标准化 F0-F6 语义；P0 nominal identity/base policy；P1 exact refs/RFC8785 hash/registry foundation。 |
| `FREEZE CANDIDATE` | 全局 Exact V1；`DI-B01-EXACT-CONTRACT`；ARSO exact integration；完整 command/event/protocol；complete registry；resolver；CAS；snapshot firewalls。 |
| `OPEN` | 物理数据库 schema；存储引擎；事件总线；算法、模型、阈值；检索/排序；executor/model 选择；实证结论。 |
| `DEFERRED` | 自动生产激活与部署；全局语义自主演化；meta-learning；cross-domain/cross-enterprise transfer；持续生产自修改。 |

## 当前阶段

```text
Phase 0: COMPLETE / REVIEWED / APPROVED
Phase 1: COMPLETE / VERIFIED / FROZEN
P0: FROZEN
P1: FROZEN
P2.0: B01 OWNER-FIELD RECOVERY PASS / FREEZE BLOCKED BY SHARED-CORE SPEC_GAP
P2.0A: RECOMMENDED / NOT AUTHORIZED
P2: NOT AUTHORIZED
P3+: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

P2.0 evidence：

```text
B01_SOURCE_RECOVERY_MATRIX.md
B01_FIELD_DECISION_LEDGER.md
B01_CROSS_SPEC_FREEZE_AUDIT.md
B01_P2_0_FREEZE_REVIEW.md
specs/00-CODE-FREEZE/DI_B01_Exact_V1_Owner_Contract.md
```

## P2.0 独立 Review 结论

B01 owner-field layer：

```text
7 / 7 objects covered
B01 SPEC_CONFLICT = 0
blocking B01 owner-field SPEC_GAP = 0
P2.0 automated verification = PASS
```

但是完整 B01 canonical model 还依赖 shared canonical shell，而以下 exact wire contract 尚未由 authority chain 冻结：

```text
P2.0-SC01 ActorRef
P2.0-SC02 TenantScope
P2.0-SC03 Provenance
P2.0-SC04 ObjectRevision
```

当前完整结构只能在 `di_contracts_v1` candidate 中找到，不能作为正式 authority。

因此：

```text
P2.0 Freeze = BLOCKED
P2 = NOT AUTHORIZED
```

推荐下一步但尚未授权：

```text
P2.0A｜Shared Canonical Shell Support Contract Recovery
```

其最小范围应恢复：

```text
ActorRef
ActorId / ActorType as required
TenantScope
TenantId / TenantScopeType as required
Provenance
ObjectRevision
```

不得通过修改已冻结 P0/P1 语义来规避该缺口；应在 1A 下新增 scoped shared-core companion contract，并通过独立 Freeze Review。

## P2 授权门禁

只有在：

```text
B01 owner contract frozen
+
shared canonical shell exact contract frozen
+
no blocking P2 prerequisite SPEC_GAP
+
user explicitly authorizes P2
```

后，才允许实现 `Full B01 Exact Schemas`。

在此之前不得新增 `src/design_intelligence/contracts/b01/*.py`。

## Exact V1 最终发布规则

只有 mandatory schemas、authoritative ARSO imports、完整 Command/Event/Protocol、semantic resolver、CAS、snapshot firewalls、CS-01–CS-32、AC-01–AC-18 全部通过且不存在 unresolved `SPEC_CONFLICT` 时，Exact V1 才能从 `FREEZE CANDIDATE` 升级为 `FROZEN`。
