# Exact V1 规范权威说明

审计日期：2026-09-05  
仓库：ARSO-Code  
阶段：规范摄取、冻结治理与 Exact V1 分阶段实现  
结论：Phase 0、Phase 1、P0、P1 已冻结；B01 owner-field recovery 已完成；P2.0A shared canonical-shell recovery 已形成 scoped exact contract candidate，正在独立 Freeze Review 前验证；P2 尚未授权。

## 规范输入路径说明

`specs/` 是唯一规范入口。

当前 normative manifest 共 9 份：Phase 1 的 7 份原始来源 + B01 scoped owner contract + shared canonical-shell scoped contract。

```text
specs/00-CODE-FREEZE/DI_Shared_Canonical_Shell_Exact_V1_Contract.md
specs/00-CODE-FREEZE/DI_B01_Exact_V1_Owner_Contract.md
```

`specs/SPEC_SOURCE_CHECKSUMS.sha256` 必须验证 `9 / 9`；原 8 个已登记 digest 不得因为 P2.0A 被改写。

## 规范权威顺序

| 优先级 | 仓库内规范 | 文档身份与状态 | 规范职责 |
|---:|---|---|---|
| 1A | `specs/00-CODE-FREEZE/DI_V5_Exact_V1_Schema_API_Contract_Freeze_Specification.md` | `DI-V5-EXACT-CONTRACT`、`V1.0-FC1`、`FREEZE CANDIDATE` | 全局 Code-Level Authority；F0-F6 normalization、cross-domain invariants、CS/AC release gates。 |
| 1B | `specs/00-CODE-FREEZE/DI_Shared_Canonical_Shell_Exact_V1_Contract.md` | `DI-SHARED-CANONICAL-SHELL-EXACT-CONTRACT`、`V1.0-FC1`、`FREEZE CANDIDATE` | Shared support/nested types 与 CanonicalObject/CanonicalRevision structural shell；不得覆盖 1A。 |
| 1C | `specs/00-CODE-FREEZE/DI_B01_Exact_V1_Owner_Contract.md` | `DI-B01-EXACT-CONTRACT`、`V1.0-FC1`、`FREEZE CANDIDATE` | B01 field-level owner contract；消费 1B shared shell，不得重定义其 internals。 |
| 2 | `specs/01-AUTHORITY/Design-Intelligence-V5.0-Engineering-Specification-V1.0.txt` | `DI-V5-ENG`、`V1.0` | 工程、运行时、对象所有权与边界。 |
| 3 | `specs/01-AUTHORITY/Cross-Spec-Consistency-Freeze.txt` | DI-E01-E08 Cross-Spec 一致性权威 | normalization 与跨规范冻结边界。 |
| 4 | `specs/02-UPSTREAM/ARSO-Engineering-Specification-V2.2.1.txt` | ARSO Engineering V2.2.1 | ARSO primitive 与集成边界 canonical owner。 |
| 5 | `specs/02-UPSTREAM/Design-Intelligence-V5.0-Application-Specification.txt` | `DI-V5-AS`、5.0 | 产品语义与 B01-B08 应用职责。 |
| 6 | `specs/02-UPSTREAM/Design-Intelligence-x-ARSO-V2.2.1-Implementation-Blueprint.txt` | Blueprint V1.0 | 集成蓝图与实施背景。 |
| 7 | `specs/03-RESEARCH/ARSO-Research-Specification-V2.2.1.txt` | Research V2.2.1 | 科学依据与研究主张边界。 |

规则：

```text
1B MUST NOT override 1A.
1C MUST NOT override 1A/1B.
1B support types are not new canonical domain primitives.
2+ MUST NOT override 1A/1B/1C where frozen.
```

## 规范解析规则

1. 先查 1A global Exact Contract。
2. Canonical shell support internals 查 1B。
3. B01 business/design field-level schema 查 1C。
4. 若 1A/1B/1C 已给出 exact 定义，直接遵守，不重新解释。
5. 未定义区域按 2→7 恢复证据；缺 exact contract → `SPEC_GAP`，不得从 candidate baseline 猜测。
6. 真实不可兼容要求 → `SPEC_CONFLICT` 并停止受影响路径。
7. `OPEN` / `DEFERRED` 不因实现便利自动升级为 contract。

## P2.0A scoped contract

P2.0A 只冻结：

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

关键 normalization：

```text
ActorType = open typed vocabulary
standard codes = USER/SERVICE/AGENT/SYSTEM/EXTERNAL

TenantScopeType = GLOBAL | TENANT
GLOBAL != public/permissionless

Provenance = source_refs + external_source_refs
candidate command_ref:ObjectRef = rejected
candidate run_ref:ObjectRef = deferred

ObjectRevision = integer >= 1 ordering metadata
parentage = parent_refs
```

P2.0A 不重新冻结 P0/P1 types，不写 production core/B01 models，不定义 Command/Event/RunRecord exact schema。

## 当前阶段

```text
Phase 0: COMPLETE / REVIEWED / APPROVED
Phase 1: COMPLETE / VERIFIED / FROZEN
P0: FROZEN
P1: FROZEN
P2.0: B01 OWNER-FIELD RECOVERY PASS / REMEDIATION UNDER REVIEW
P2.0A: RECOVERY CONTRACT COMPLETE / INDEPENDENT REVIEW PENDING
P2: NOT AUTHORIZED
P3+: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

P2.0A evidence：

```text
SHARED_CORE_SOURCE_RECOVERY_MATRIX.md
SHARED_CORE_FIELD_DECISION_LEDGER.md
SHARED_CORE_CROSS_SPEC_FREEZE_AUDIT.md
docs/superpowers/specs/2026-09-05-p2-0a-shared-canonical-shell-recovery-design.md
docs/superpowers/plans/2026-09-05-p2-0a-shared-canonical-shell-recovery-implementation.md
specs/00-CODE-FREEZE/DI_Shared_Canonical_Shell_Exact_V1_Contract.md
```

Current recovery candidate result：

```text
SC01 ActorRef       CLOSED IN CANDIDATE
SC02 TenantScope    CLOSED IN CANDIDATE
SC03 Provenance     CLOSED IN CANDIDATE
SC04 ObjectRevision CLOSED IN CANDIDATE
shared-core SPEC_CONFLICT = 0
blocking shared-core field SPEC_GAP = 0
```

这些结论仍需 automated verification + independent Freeze Review；在此之前不得把 P2.0A 或 P2.0 宣布为 `FROZEN`。

## P2 授权门禁

只有：

```text
B01 owner contract Freeze approved
+
shared canonical shell Freeze approved
+
P2.0 final independent review PASS
+
no blocking P2 prerequisite SPEC_GAP
+
user explicitly authorizes P2
```

之后才允许实现 `Full B01 Exact Schemas`。

在此之前不得新增 `src/design_intelligence/contracts/b01/*.py`，也不得因为 P2.0A contract candidate 而提前实现 production shared-core Python types。

## Exact V1 最终发布规则

只有 mandatory schemas、authoritative ARSO imports、完整 Command/Event/Protocol、semantic resolver、CAS、snapshot firewalls、CS-01–CS-32、AC-01–AC-18 全部通过且不存在 unresolved `SPEC_CONFLICT` 时，Exact V1 才能从 `FREEZE CANDIDATE` 升级为 `FROZEN`。
